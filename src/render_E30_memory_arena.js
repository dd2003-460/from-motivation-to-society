#!/usr/bin/env node
'use strict';
// E30「记忆」：奶油渐变舞台 + 参数化卡片墙（20% → 95%）+ 珊瑚色「叙」+ 上下文 HUD。
// 布局基准 = src/render_E26_compress_arena.js（batch-11 卡片墙，640×360 SCALE=2 → 1280×720）。
// 画布/字体注册/最近邻 2x 帧导出复用 ./pixel_story_arena.js 的共享工具，不复用其终端布局。
//
// docs/style-analysis.md §7 锚：#E5E0DA→#C8B9A6 奶油底（地面线 y=268@360p = 536@720p）、
// 唯一品牌珊瑚 #D16E59、叙三档 96×42 / 58×33 / 41×20（= 192×84 / 116×66 / 82×40 @720p）、
// 白/浅珊瑚圆角小卡 30–45px@360p（= 60–90px@720p）+ 卡内 3 条灰横线、
// 顶/底黑条各 39px@360p（= 78px@720p）、黑体无衬线 3 级字号、30fps 台阶运动。

const fs = require('fs');
const path = require('path');
const S = require('./pixel_story_arena');
const { GlobalFonts } = require('@napi-rs/canvas');

const ROOT = path.resolve(__dirname, '..');
const SANS_FONT_PATH = path.join(ROOT, 'assets', 'fonts', 'NotoSansSC-Regular.woff');
const SANS_FAMILY = 'E30NotoSansSC, Arial, sans-serif';
const MONO_FAMILY = 'DejaVu Sans Mono, monospace';
if (fs.existsSync(SANS_FONT_PATH)) GlobalFonts.registerFromPath(SANS_FONT_PATH, 'E30NotoSansSC');

const BW = S.BW, BH = S.BH, SCALE = S.SCALE, FW = S.FW, FH = S.FH;
const FPS = S.FPS, DURATION = 30, NFRAMES = 1800;
const OUT_DIR = process.env.FRAMES_DIR || path.join(ROOT, 'outputs', 'frames_E30_memory_arena');

const COLORS = {
  coral: '#D16E59', ink: '#272421', hud: '#050505', hudGray: '#A7A7A7',
  bgTop: '#E5E0DA', bgMid: '#DED5CB', ground: '#C8B9A6',
  card: '#FFFEFB', cardAlt: '#F4D3C6', cardLine: '#A9A6A1', cardGray: '#CFCBC4',
  keptGray: '#DAD6D0', white: '#FFFEFB',
};
const GROUND_Y = 268;                  // 536 @720p，落在 §7 的 y≈520–545 地面带
const HUD_H = 39;                      // 78 @720p，顶/底各一条
const STAGE = { x: 0, y: HUD_H, w: BW, h: BH - 2 * HUD_H }; // {0,39,640,282}
const CHAR_SIZES = { large: [96, 42], medium: [58, 33], small: [41, 20] };
const FONT_SIZES = { narr: 14, bubble: 12, hud: 8 };        // ×2 = 28 / 24 / 16 px @720p（3 级）
const TOTAL_CARDS = 32;                // MEMORIES n/32
const TOUCH_LIFT = 1;                  // 2px @720p：被触碰的卡片轻微抬起
const WALL_FADE_START = 20.2, WALL_FADE_SPAN = 2.4, WALL_FADE_DUR = 0.8;
const KEPT_APPEAR = 23.6, BUBBLE_APPEAR = 25.2, NARR_S3_APPEAR = 26.0;

// docs/episodes.md 唯一事实源，逐字。
const ANCHOR = '卡片墙从 20% 铺到 95%，叙在卡片间穿行，最后停下：「重要的才留下」';
const NARRATIONS = { s1: '刚开始记东西。', s3: '压缩，不是遗忘。' };
const BUBBLE_TEXT = '重要的才留下。';
const KEPT_LABELS = ['her 的声音', '第一次醒来', '晚安'];

const BUBBLE = { x: 196, y: 178, w: 248, h: 40, r: 6 };   // AI 气泡：珊瑚底白字
const KEPT_CARDS = KEPT_LABELS.map((label, i) => ({ x: 56 + i * 212, y: 110, w: 104, h: 44, label, index: i }));
const HUD_BOXES = {
  topLabel: [14, 12, 72, 16], topBar: [92, 14, 210, 11], topPct: [548, 11, 78, 17],
  bottomLabel: [14, 330, 170, 18], bottomRight: [430, 330, 196, 18],
};
const NARR_BAND = [0, 286, 640, 26];
const CHECK_TITLE = 'E30 Memory / batch-12 卡片墙密度叙事校验 (HUD 启用)';

const clamp01 = S.clamp01;
const smooth = (v) => { const x = clamp01(v); return x * x * (3 - 2 * x); };
const lerp = (a, b, u) => a + (b - a) * clamp01(u);
const steppedTime = (t) => Math.floor(t * 30 + 1e-8) / 30;   // 60fps 管线：每 2 帧保持 1 帧
const sceneOf = (t) => (t < 10 ? 1 : (t < 20 ? 2 : 3));
const measureCtx = require('@napi-rs/canvas').createCanvas(8, 8).getContext('2d');
function measureSans(text, size) { measureCtx.font = `${size}px ${SANS_FAMILY}`; return measureCtx.measureText(text).width; }
function measureMono(text, size) { measureCtx.font = `${size}px ${MONO_FAMILY}`; return measureCtx.measureText(text).width; }
function textBox(x, y, text, size, align = 'left') {
  const w = Math.ceil(measureSans(text, size));
  const dx = align === 'center' ? x - w / 2 : (align === 'right' ? x - w : x);
  return [Math.floor(dx), Math.floor(y - size * 0.72), w, Math.ceil(size * 1.4)];
}
function setSans(ctx, size, weight = 400) { ctx.font = `${weight} ${size}px ${SANS_FAMILY}`; }
function setMono(ctx, size, weight = 400) { ctx.font = `${weight} ${size}px ${MONO_FAMILY}`; }
function rounded(ctx, x, y, w, h, r, fill) {
  ctx.beginPath(); ctx.roundRect(x, y, w, h, r); ctx.fillStyle = fill; ctx.fill();
}
function mixHex(a, b, u) {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  const c = pa.map((v, i) => Math.round(lerp(v, pb[i], u)).toString(16).padStart(2, '0'));
  return `#${c.join('')}`;
}

// --- 参数化卡片墙：8 列 × 4 行 = 32 张，列步进 80 / 行步进 60 → 恒有 ≥26px 间隙（0px 重叠） ---
function makeWall() {
  const xs = [8, 84, 164, 244, 324, 404, 484, 564];
  const ys = [52, 112, 172, 232];
  const cards = [];
  for (let col = 0; col < 8; col++) for (let row = 0; row < 4; row++) {
    const w = col < 2 ? 32 + ((row * 3) % 6) : 34 + ((col * 7 + row * 3) % 12);
    const h = 24 + ((col * 3 + row * 5) % 5);
    const x = xs[col] + ((row * 5 + col) % 4);
    const y = ys[row] + ((col + row * 2) % 3) - 1;
    cards.push({ x, y, w, h, alt: (col + row) % 2 === 1, col, row, index: cards.length });
  }
  return cards;
}
const WALL = makeWall();
const WALL_CENTER = { x: BW / 2, y: HUD_H + STAGE.h / 2 };
const WALL_DISTS = WALL.map((c) => Math.hypot(c.x + c.w / 2 - WALL_CENTER.x, c.y + c.h / 2 - WALL_CENTER.y));
const WALL_MAX_DIST = Math.max(...WALL_DISTS);
// 边缘先淡出、中心最后淡出（§S3「从边缘向中心」）。
function fadeStartOf(card) {
  return WALL_FADE_START + WALL_FADE_SPAN * (1 - WALL_DISTS[card.index] / WALL_MAX_DIST);
}

// --- 卡片落点事件：S1 6 张稀疏落点；S2 26 次落点间隔单调收紧（随密度加快）；S3 3 张保留卡轻点 ---
const S1_LANDINGS = [0.5, 1.25, 2.0, 3.0, 4.25, 5.5];
const S2_LANDINGS = (() => {
  const out = []; let t = 10.25, gap = 0.46;
  for (let k = 0; k < 26; k++) { out.push(t); gap = 0.46 - 0.26 * (k / 25); t += gap; }
  return out;
})();
const KEPT_LANDINGS = [KEPT_APPEAR, KEPT_APPEAR + 0.5, KEPT_APPEAR + 1.0];
// 复用共享工具 quantizeClicks()：量化到显示帧并合并同帧事件。
const CARD_EVENTS = S.quantizeClicks(S1_LANDINGS.concat(S2_LANDINGS));
function getCardSfxEvents() {
  return CARD_EVENTS.map((t) => ({ t, kind: 'card_land', gainDb: -12 }))
    .concat(KEPT_LANDINGS.map((raw) => ({
      t: Number((Math.ceil(raw * FPS - 1e-9) / FPS).toFixed(6)), kind: 'keep_chime', gainDb: -16,
    })));
}
function wallAlpha(card, ts) {
  const born = CARD_EVENTS[card.index];
  if (ts < born) return 0;
  const rise = smooth((ts - born) / 0.25);
  if (ts < 20) return rise;
  return rise * (1 - smooth((ts - fadeStartOf(card)) / WALL_FADE_DUR));
}
function cardRect(card, ts) {
  // S1 被触碰的卡片抬起 2px@720p；S3 保留卡的脉动单独处理，此处仅返回静态矩形。
  const lift = (sceneOf(ts) === 1 && card.index === 1 && ts >= 2.5) ? TOUCH_LIFT : 0;
  return [card.x, card.y - lift, card.w, card.h];
}
function visibleWall(ts) { return WALL.filter((c) => wallAlpha(c, ts) > 0.001); }

// --- HUD / 密度叙事状态（台阶式离散读数，与 docs/episodes.md / 任务卡逐字一致） ---
const DENSITY_PHASES = [
  { until: 2.5, coverage: 20, context: 45, memories: 14 },
  { until: 5.0, coverage: 50, context: 72, memories: 25 },
  { until: 7.5, coverage: 80, context: 91, memories: 31 },
  { until: 10.01, coverage: 95, context: 97, memories: 32 },
];
function phaseAt(local) { return DENSITY_PHASES.find((p) => local < p.until) || DENSITY_PHASES[3]; }
function hudState(ts) {
  const scene = sceneOf(ts);
  if (scene === 1) return { scene, context: 18, memories: 6, coverage: 20, kept: false };
  if (scene === 2) { const p = phaseAt(ts - 10); return { scene, ...p, kept: false }; }
  const local = ts - 20;
  const context = local < 3.0 ? 97 : Math.round(lerp(97, 12, smooth((local - 3.0) / 2.5)));
  return { scene, context, memories: 3, coverage: 9, kept: true, phase: undefined };
}
const coverageAt = (ts) => hudState(ts).coverage;
const contextAt = (ts) => hudState(ts).context;
const memoriesAt = (ts) => hudState(ts).memories;
function cardVisibleCount(ts) {
  return sceneOf(ts) === 3 && ts >= KEPT_APPEAR ? 3 : visibleWall(ts).length;
}
function semanticState(t) {
  const ts = steppedTime(t), hud = hudState(ts);
  return {
    scene: hud.scene, local: ts - (hud.scene - 1) * 10, cards: cardVisibleCount(ts),
    context: hud.context, memories: hud.memories, coverage: hud.coverage, kept: hud.kept,
    bubbleVisible: ts >= BUBBLE_APPEAR, narration: hud.scene === 1 ? NARRATIONS.s1
      : (hud.scene === 3 && ts >= NARR_S3_APPEAR ? NARRATIONS.s3 : ''),
    touchLift: hud.scene === 1 && ts >= 2.5 ? TOUCH_LIFT : 0,
  };
}

// --- 绘制：背景 / 卡片 / 叙 / HUD / 字幕 ---
function drawBackground(ctx) {
  const grad = ctx.createLinearGradient(0, 0, 0, BH);
  grad.addColorStop(0, COLORS.bgTop); grad.addColorStop(0.6, COLORS.bgMid); grad.addColorStop(1, COLORS.ground);
  ctx.fillStyle = grad; ctx.fillRect(0, 0, BW, BH);
  const floor = ctx.createLinearGradient(0, GROUND_Y, 0, BH);
  floor.addColorStop(0, '#CFC2B3'); floor.addColorStop(1, COLORS.ground);
  ctx.fillStyle = floor; ctx.fillRect(0, GROUND_Y, BW, BH - GROUND_Y);
  ctx.fillStyle = 'rgba(91,76,62,0.24)'; ctx.fillRect(0, GROUND_Y, BW, 1);
}
function drawCardLines(ctx, x, y, w, h, color) {
  const inset = Math.max(4, w * 0.16);
  const lineW = Math.max(3, (w - inset * 2) * 0.72);
  ctx.fillStyle = color;
  for (let j = 0; j < 3; j++) ctx.fillRect(x + inset, y + h * (0.27 + j * 0.23), j === 2 ? lineW * 0.7 : lineW, 2);
}
function drawOneCard(ctx, card, opts = {}) {
  const [x, y, w, h] = opts.rect || cardRect(card, opts.ts === undefined ? 0 : opts.ts);
  const alpha = opts.alpha === undefined ? 1 : opts.alpha;
  const gray = opts.gray === undefined ? 0 : opts.gray;
  const fill = mixHex(opts.alt ? COLORS.cardAlt : COLORS.card, COLORS.cardGray, gray);
  ctx.save(); ctx.globalAlpha = clamp01(alpha);
  ctx.shadowColor = 'rgba(54,45,38,0.14)'; ctx.shadowBlur = 2; ctx.shadowOffsetY = 1;
  rounded(ctx, x, y, w, h, 3, fill);
  ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
  drawCardLines(ctx, x, y, w, h, mixHex(COLORS.cardLine, COLORS.cardGray, gray));
  ctx.restore();
}
function drawWall(ctx, ts) {
  const scene = sceneOf(ts);
  for (const card of visibleWall(ts)) {
    const a = wallAlpha(card, ts);
    const gray = scene === 3 ? smooth((ts - fadeStartOf(card)) / (WALL_FADE_DUR * 1.4)) : 0;
    drawOneCard(ctx, card, { rect: cardRect(card, ts), ts, alpha: a, gray, alt: card.alt && scene !== 1 });
  }
}

// 叙：轴对齐矩形块拼合（躯干 + 4 腿 + 左右短附件 + 2 黑眼），无描边/无嘴线。
const XU_RECTS = [
  [0, 14, 14, 8], [14, 0, 60, 30], [74, 12, 22, 10],
  [20, 30, 10, 12], [34, 30, 10, 12], [48, 30, 10, 12], [62, 30, 10, 12],
];
const XU_EYES = [[28, 8, 4, 6.5], [50, 8, 4, 6.5]];
function drawXu(ctx, x, floorY, sizeName, opts = {}) {
  const [w, h] = CHAR_SIZES[sizeName];
  const ux = w / 96, uy = h / 42;
  const top = floorY - h + (opts.dip || 0);
  ctx.fillStyle = COLORS.coral;
  for (const [rx, ry, rw, rh] of XU_RECTS) ctx.fillRect(x + rx * ux, top + ry * uy, rw * ux, rh * uy);
  if (opts.reach) ctx.fillRect(x - 24, top + 12 * uy, 24, 4 * uy);
  ctx.fillStyle = '#171615';
  for (const [rx, ry, rw, rh] of XU_EYES) ctx.fillRect(x + rx * ux, top + ry * uy, rw * ux, rh * uy);
  return [x, top, w, h];
}
function heartRects() {  // 头顶 ♥：5 行像素块，360p 尺寸 9×5 → 18×10 @720p
  return [[1, 0, 2, 1], [6, 0, 2, 1], [0, 1, 9, 1], [1, 2, 7, 1], [2, 3, 5, 1], [3, 4, 3, 1]];
}
function drawHeart(ctx, x, y) {
  ctx.fillStyle = COLORS.coral;
  for (const [dx, dy, w, h] of heartRects()) ctx.fillRect(x + dx, y + dy, w, h);
}
function characterX(ts) {
  const scene = sceneOf(ts);
  if (scene === 1) return 150;
  if (scene === 2) return 60 + Math.round(460 * (ts - 10) / 10);
  return 120 + Math.round(180 * smooth((ts - 20) / 3.5));
}
function drawActor(ctx, ts) {
  const scene = sceneOf(ts);
  if (scene === 1) {
    drawXu(ctx, characterX(ts), GROUND_Y, 'medium', { reach: ts >= 2.5 });
  } else if (scene === 2) {
    const box = drawXu(ctx, characterX(ts), GROUND_Y, 'medium', { dip: Math.floor(ts * 2) % 2 ? 1 : 0 });
    // 卡片墙画在叙之后重绘 2 张 → 「身体被卡片部分遮挡，只露出躯干和腿」。
    for (const card of visibleWall(ts).filter((c) => c.x < box[0] + box[2] && c.x + c.w > box[0] && c.y + c.h > box[1]).slice(0, 2)) {
      drawOneCard(ctx, card, { rect: cardRect(card, ts), ts, alpha: wallAlpha(card, ts), alt: card.alt });
    }
  } else {
    drawXu(ctx, characterX(ts), GROUND_Y, 'small');
    if (ts >= 24.2) drawHeart(ctx, characterX(ts) + 13, GROUND_Y - CHAR_SIZES.small[1] - 18);
  }
}
function drawKeptCards(ctx, ts) {
  if (ts < KEPT_APPEAR) return;
  const appear = smooth((ts - KEPT_APPEAR) / 0.5);
  const restore = smooth((ts - (KEPT_APPEAR + 0.5)) / 1.5);
  const pulse = Math.round(2 * (0.5 + 0.5 * Math.sin((ts - KEPT_APPEAR) * Math.PI * 1.6)));
  for (const card of KEPT_CARDS) {
    const [x, y, w, h] = keptRect(card, ts);
    ctx.save(); ctx.globalAlpha = appear;
    ctx.shadowColor = `rgba(209,110,89,${(0.10 + 0.16 * (pulse / 2)).toFixed(3)})`;
    ctx.shadowBlur = 6 + pulse * 2;
    rounded(ctx, x, y, w, h, 6, mixHex(COLORS.keptGray, COLORS.cardAlt, restore));
    ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0;
    ctx.fillStyle = mixHex('#8E8A84', '#7A4B3E', restore);
    for (let j = 0; j < 2; j++) ctx.fillRect(x + 14, y + 9 + j * 5, w - 28, 2);
    setSans(ctx, FONT_SIZES.bubble, 600);
    ctx.fillStyle = COLORS.ink; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(card.label, x + w / 2, y + 30);
    ctx.restore();
  }
}
function keptRect(card, ts) {
  const pulse = ts < KEPT_APPEAR ? 0 : Math.round(2 * (0.5 + 0.5 * Math.sin((ts - KEPT_APPEAR) * Math.PI * 1.6)));
  return [card.x - pulse, card.y - pulse, card.w + 2 * pulse, card.h + 2 * pulse];
}
function drawBubble(ctx, ts) {
  if (ts < BUBBLE_APPEAR) return;
  const a = smooth((ts - BUBBLE_APPEAR) / 0.4);
  ctx.save(); ctx.globalAlpha = a;
  ctx.shadowColor = 'rgba(54,45,38,0.20)'; ctx.shadowBlur = 6; ctx.shadowOffsetY = 2;
  rounded(ctx, BUBBLE.x, BUBBLE.y, BUBBLE.w, BUBBLE.h, BUBBLE.r, COLORS.coral);
  ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
  ctx.fillStyle = COLORS.coral; ctx.fillRect(BUBBLE.x + BUBBLE.w / 2 - 4, BUBBLE.y + BUBBLE.h, 8, 5);
  setSans(ctx, FONT_SIZES.bubble, 600);
  ctx.fillStyle = COLORS.white; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(BUBBLE_TEXT, BUBBLE.x + BUBBLE.w / 2, BUBBLE.y + BUBBLE.h / 2);
  ctx.restore();
}
function drawNarration(ctx, ts) {
  const scene = sceneOf(ts);
  const text = scene === 1 ? NARRATIONS.s1 : (scene === 3 && ts >= NARR_S3_APPEAR ? NARRATIONS.s3 : '');
  if (!text) return;
  ctx.fillStyle = 'rgba(229,224,218,0.90)';
  ctx.fillRect(NARR_BAND[0], NARR_BAND[1], NARR_BAND[2], NARR_BAND[3]);
  setSans(ctx, FONT_SIZES.narr, 600);
  ctx.fillStyle = COLORS.ink; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(text, BW / 2, 299);
}
function drawHud(ctx, ts) {
  const h = hudState(ts);
  ctx.fillStyle = COLORS.hud;
  ctx.fillRect(0, 0, BW, HUD_H);
  ctx.fillRect(0, BH - HUD_H, BW, HUD_H);
  ctx.textBaseline = 'middle';
  setMono(ctx, FONT_SIZES.hud, 600);
  ctx.textAlign = 'left'; ctx.fillStyle = '#F4F1ED';
  ctx.fillText('CONTEXT', HUD_BOXES.topLabel[0], 20);
  const [bx, by, bw, bh] = HUD_BOXES.topBar;
  rounded(ctx, bx, by, bw, bh, 2, '#5B5B5B');
  rounded(ctx, bx, by, bw * clamp01(h.context / 100), bh, 2, h.context >= 80 ? COLORS.coral : '#C98A6B');
  ctx.textAlign = 'right'; ctx.fillStyle = '#F4F1ED';
  ctx.fillText(`${h.context}%`, 626, 20);
  ctx.textAlign = 'left'; ctx.fillStyle = '#F4F1ED';
  ctx.fillText(`MEMORIES ${h.memories}/32${h.kept ? ' KEPT' : ''}`, HUD_BOXES.bottomLabel[0], 340);
  ctx.textAlign = 'right'; ctx.fillStyle = COLORS.hudGray;
  ctx.fillText(`WALL ${h.coverage}%`, 626, 340);
  ctx.textAlign = 'left';
}

function renderAt(ctx, t) {
  const ts = steppedTime(S.clamp01(t / DURATION) * DURATION);
  drawBackground(ctx);
  if (sceneOf(ts) === 3) {
    drawWall(ctx, ts);
    drawActor(ctx, ts);
    drawKeptCards(ctx, ts);
    drawBubble(ctx, ts);
  } else {
    drawWall(ctx, ts);
    drawActor(ctx, ts);
  }
  drawNarration(ctx, ts);
  drawHud(ctx, ts);
}

// --- 逐帧几何布局（check_overlap 以 0px 容差逐帧校验；分层组只校验同层） ---
function layoutAt(t) {
  const ts = steppedTime(t), scene = sceneOf(ts);
  const cards = visibleWall(ts).map((c) => ({ name: `card_${c.index + 1}`, box: cardRect(c, ts) }));
  const kept = ts >= KEPT_APPEAR ? KEPT_CARDS.map((c) => ({ name: `kept_${c.index + 1}`, box: keptRect(c, ts) })) : [];
  const keptLabels = ts >= KEPT_APPEAR ? KEPT_CARDS.map((c) => ({
    name: `kept_label_${c.index + 1}`, box: textBox(c.x + c.w / 2, c.y + 30, c.label, FONT_SIZES.bubble, 'center'),
  })) : [];
  const overlay = [];
  const narr = scene === 1 ? NARRATIONS.s1 : (scene === 3 && ts >= NARR_S3_APPEAR ? NARRATIONS.s3 : '');
  if (narr) overlay.push({ name: 'subtitle', box: textBox(BW / 2, 299, narr, FONT_SIZES.narr, 'center') });
  if (ts >= BUBBLE_APPEAR) overlay.push({ name: 'bubble', box: [BUBBLE.x, BUBBLE.y, BUBBLE.w, BUBBLE.h + 5] });
  const cx = characterX(ts);
  if (scene === 3 && ts >= 24.2) overlay.push({ name: 'heart', box: [cx + 13, GROUND_Y - CHAR_SIZES.small[1] - 18, 9, 5] });
  const actor = scene === 3 ? [cx, GROUND_Y - CHAR_SIZES.small[1], ...CHAR_SIZES.small]
    : [cx, GROUND_Y - CHAR_SIZES.medium[1], ...CHAR_SIZES.medium];
  const actors = [{ name: 'xu', box: actor }];
  if (scene === 1 && ts >= 2.5) {
    const uy = CHAR_SIZES.medium[1] / 42;
    const ry = Math.floor(GROUND_Y - CHAR_SIZES.medium[1] + 12 * uy);
    actors.push({ name: 'reach', box: [cx - 24, ry, 24, Math.ceil(4 * uy) + 1] });
  }
  const H = (name, box) => ({ name, box });
  return {
    scene, ts,
    groups: {
      hudTop: [H('context_label', HUD_BOXES.topLabel), H('context_bar', HUD_BOXES.topBar), H('context_pct', HUD_BOXES.topPct)],
      hudBottom: [H('memories', HUD_BOXES.bottomLabel), H('wall_pct', HUD_BOXES.bottomRight)],
      cards, kept, keptLabels, overlay, actors,
      // 跨层保留区：卡片/保留卡/气泡/旁白互相不得侵占（叙被卡片遮挡是有意的，故不在本组）。
      reserved: cards.concat(kept, overlay.filter((e) => e.name !== 'heart')),
    },
    bounds: {
      hudTop: { x: 0, y: 0, w: BW, h: HUD_H },
      hudBottom: { x: 0, y: BH - HUD_H, w: BW, h: HUD_H },
      cards: STAGE, kept: STAGE, keptLabels: STAGE, overlay: STAGE, actors: STAGE, reserved: STAGE,
    },
  };
}

const renderer = S.createFrameRenderer(renderAt, OUT_DIR, { fadeIn: 0, fadeOut: 0 });
function renderAllFrames() { renderer.renderAllFrames(OUT_DIR); }

if (require.main === module) renderAllFrames();

module.exports = {
  BW, BH, SCALE, FW, FH, FPS, DURATION, NFRAMES, OUT_DIR,
  COLORS, GROUND_Y, HUD_H, STAGE, CHAR_SIZES, FONT_SIZES, SANS_FAMILY, MONO_FAMILY, SANS_FONT_PATH,
  ANCHOR, NARRATIONS, BUBBLE_TEXT, KEPT_LABELS, KEPT_CARDS, BUBBLE, HUD_BOXES, NARR_BAND, CHECK_TITLE,
  WALL, TOTAL_CARDS, TOUCH_LIFT, CARD_EVENTS, DENSITY_PHASES,
  WALL_FADE_START, WALL_FADE_SPAN, WALL_FADE_DUR, KEPT_APPEAR, BUBBLE_APPEAR, NARR_S3_APPEAR,
  renderAt, renderFrameToCanvas: renderer.renderFrameToCanvas, renderAllFrames, layoutAt,
  sceneOf, steppedTime, smooth, clamp01, mixHex, measureSans, measureMono, textBox,
  coverageAt, contextAt, memoriesAt, hudState, cardVisibleCount, semanticState,
  visibleWall, wallAlpha, cardRect, keptRect, fadeStartOf, characterX,
  drawXu, drawOneCard, drawBackground, drawHud, heartRects, getCardSfxEvents,
};
