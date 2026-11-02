#!/usr/bin/env node
'use strict';
// E30「记忆」batch-12 校验：docs/style-analysis.md §7 风格锚 + docs/episodes.md 剧情锚。
// 容差 0px：逐帧几何（1800 帧、同层组内两两比对 + 边界截断）、规格、色彩像素、
// 字体、叙三档、台阶运动、HUD/密度读数、卡片落点音排程、输出媒体。
//
// 用法：node src/check_overlap_E30_arena.js   （exit 0 = 全 PASSED）

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { createCanvas } = require('@napi-rs/canvas');
const R = require('./render_E30_memory_arena');
const A = require('../scripts/build_audio_E30');
const C = require('../scripts/build_audio_v2_common');
const { overlap, interArea, outside, readPixels } = require('./check_overlap_story_common');

const ROOT = path.resolve(__dirname, '..');
const hex = (d, x, y, w = R.BW) => {
  const i = (y * w + x) * 4;
  return `#${[d[i], d[i + 1], d[i + 2]].map((v) => v.toString(16).padStart(2, '0')).join('')}`;
};
const frameData = (n) => readPixels(R.renderFrameToCanvas(n).baseCanvas).data;
function countColor(d, target, box) {
  const [x0, y0, w, h] = box; let n = 0;
  for (let y = y0; y < y0 + h; y++) for (let x = x0; x < x0 + w; x++) if (hex(d, x, y) === target) n++;
  return n;
}
function meanLuma(d) { let s = 0; for (let i = 0; i < d.length; i += 4) s += d[i]; return s / (d.length / 4); }
function eq(actual, expected, label, issues) { if (actual !== expected) issues.push(`${label}: ${actual} ≠ ${expected}`); }
function eqj(actual, expected, label, issues) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) issues.push(`${label}: ${JSON.stringify(actual)} ≠ ${JSON.stringify(expected)}`);
}

// 1) 规格 / 风格锚 / 剧情锚逐字（docs/episodes.md 为唯一事实源）
function checkSpecs() {
  const issues = [];
  eq(R.BW, 640, 'BW', issues); eq(R.BH, 360, 'BH', issues); eq(R.SCALE, 2, 'SCALE', issues);
  eq(R.FW, 1280, '输出宽', issues); eq(R.FH, 720, '输出高', issues);
  eq(R.FPS, 60, 'FPS', issues); eq(R.DURATION, 30, '时长', issues); eq(R.NFRAMES, 1800, '帧数', issues);
  eq(R.COLORS.coral, '#D16E59', '品牌珊瑚', issues);
  eq(R.COLORS.bgTop, '#E5E0DA', '奶油底上沿', issues);
  eq(R.COLORS.ground, '#C8B9A6', '地面带', issues);
  eq(R.HUD_H * 2, 78, 'HUD 黑条@720p', issues);
  if (!(R.GROUND_Y * 2 >= 520 && R.GROUND_Y * 2 <= 545)) issues.push(`地面线 ${R.GROUND_Y * 2} 不在 y=520–545`);
  for (const [k, target] of [['large', [191, 84]], ['medium', [115, 66]], ['small', [81, 40]]]) {
    const [w, h] = R.CHAR_SIZES[k];
    if (Math.abs(w * 2 - target[0]) > 1 || Math.abs(h * 2 - target[1]) > 1) issues.push(`叙 ${k} 档 ${w * 2}×${h * 2} ≠ ${target.join('×')}`);
  }
  eqj([R.FONT_SIZES.narr, R.FONT_SIZES.bubble, R.FONT_SIZES.hud].map((v) => v * 2), [28, 24, 16], '3 级字号@720p', issues);
  if (!(R.FONT_SIZES.narr > R.FONT_SIZES.bubble && R.FONT_SIZES.bubble > R.FONT_SIZES.hud)) issues.push('字号层级非 3 级递减');
  eq(R.WALL.length, 32, '卡片墙总数 (MEMORIES /32)', issues);
  eq(R.TOTAL_CARDS, 32, 'TOTAL_CARDS', issues);
  eq(R.TOUCH_LIFT * 2, 2, '被触碰卡片抬起 2px@720p', issues);
  for (const c of R.WALL) if (c.w * 2 < 60 || c.w * 2 > 90) issues.push(`卡片 ${c.index + 1} 宽 ${c.w * 2}px@720p 不在 60–90`);
  if (!fs.existsSync(R.SANS_FONT_PATH)) issues.push('缺中文黑体无衬线字体');
  if (/FusionPixel|pixel/i.test(R.SANS_FAMILY)) issues.push(`正文字体误用像素字体 ${R.SANS_FAMILY}`);
  // 剧情锚逐字比对 docs/episodes.md
  const line = fs.readFileSync(path.join(ROOT, 'docs', 'episodes.md'), 'utf8').split('\n').find((l) => l.includes('| E30 |'));
  const docAnchor = line ? line.split('|')[3].trim() : '';
  eq(R.ANCHOR, docAnchor, '剧情锚点 (docs/episodes.md 逐字)', issues);
  eqj(R.NARRATIONS, { s1: '刚开始记东西。', s3: '压缩，不是遗忘。' }, '两场旁白', issues);
  eq(R.BUBBLE_TEXT, '重要的才留下。', '叙气泡', issues);
  eqj(R.KEPT_LABELS, ['her 的声音', '第一次醒来', '晚安'], '3 张保留卡', issues);
  return { name: '画布 1280×720 / 1800 帧@60fps / 奶油底·珊瑚·HUD 78px×2 / 叙三档 / 3 级字号 / 剧情锚逐字', issues };
}

// 2) 字体：黑体无衬线 CJK 逐字非豆腐 + 等宽数字
function checkFonts() {
  const issues = [];
  const strs = [R.NARRATIONS.s1, R.NARRATIONS.s3, R.BUBBLE_TEXT].concat(R.KEPT_LABELS).join('');
  const chars = Array.from(new Set(Array.from(strs))).filter((c) => c.trim() !== '');
  const hashes = new Map();
  for (const ch of chars) {
    const cv = createCanvas(40, 40), ctx = cv.getContext('2d');
    ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, 40, 40);
    ctx.font = `20px ${R.SANS_FAMILY}`; ctx.textBaseline = 'top'; ctx.fillStyle = '#000000';
    ctx.fillText(ch, 8, 8);
    const d = readPixels(cv).data; let ink = 0, hash = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i] < 128) { ink++; hash = (hash * 31 + i / 4) >>> 0; }
    if (ink < 8) issues.push(`字形「${ch}」近乎空白 (ink=${ink})`);
    if (hashes.has(hash) && hashes.get(hash) !== ch) issues.push(`字形「${ch}」与「${hashes.get(hash)}」像素相同 (tofu)`);
    hashes.set(hash, ch);
    if (!(R.measureSans(ch, 20) > 0)) issues.push(`字形「${ch}」度量宽度异常`);
  }
  const dw = Array.from('0123456789').map((c) => R.measureMono(c, 10));
  if (new Set(dw.map((v) => v.toFixed(3))).size !== 1) issues.push(`HUD 数字非等宽: ${dw.join(',')}`);
  return { name: `中文黑体无衬线 (${chars.length} glyphs 逐个异形) + HUD 等宽数字`, issues };
}

// 3) 卡片墙静态几何：32 张 0px 重叠、全边界内、S1 左 20%、边缘→中心淡出
function checkWallGeometry() {
  const issues = [];
  const rects = R.WALL.map((c) => [c.x, c.y, c.w, c.h]);
  for (let i = 0; i < rects.length; i++) {
    if (outside(rects[i], R.STAGE)) issues.push(`卡片 ${i + 1} 越出舞台 ${rects[i]}`);
    for (let j = i + 1; j < rects.length; j++) {
      if (overlap(rects[i], rects[j])) issues.push(`卡片 ${i + 1}/${j + 1} 重叠 area=${interArea(rects[i], rects[j])}`);
    }
  }
  const left = R.WALL.slice(0, 6);
  for (const c of left) if (c.x + c.w > R.BW * 0.2) issues.push(`S1 卡 ${c.index + 1} 越出左侧 20% 区域`);
  // 保留卡（含脉动最大扩张）仍 0px 重叠
  for (let t = 23.6; t < 30; t += 0.05) {
    const kr = R.KEPT_CARDS.map((c) => R.keptRect(c, t));
    for (let i = 0; i < kr.length; i++) {
      if (outside(kr[i], R.STAGE)) issues.push(`保留卡 ${i + 1} @${t.toFixed(2)}s 越出舞台`);
      for (let j = i + 1; j < kr.length; j++) if (overlap(kr[i], kr[j])) issues.push(`保留卡 ${i + 1}/${j + 1} @${t.toFixed(2)}s 重叠`);
    }
  }
  // 边缘先、中心后：最大距离卡的 fadeStart < 最小距离卡的 fadeStart
  const dists = R.WALL.map((c) => Math.hypot(c.x + c.w / 2 - R.BW / 2, c.y + c.h / 2 - (R.HUD_H + R.STAGE.h / 2)));
  const outer = R.WALL[dists.indexOf(Math.max(...dists))], inner = R.WALL[dists.indexOf(Math.min(...dists))];
  if (!(R.fadeStartOf(outer) < R.fadeStartOf(inner))) issues.push('卡片墙不是「从边缘向中心」淡出');
  return { name: '32 张卡片墙 0px 重叠 / S1 左 20% 六张 / 3 保留卡含脉动 0px 重叠 / 边缘→中心淡出', issues };
}

// 4) 叙事读数与文案逐字（HUD / 密度 / 上下文 / 记忆数 / 台阶）
function checkNarrative() {
  const issues = [];
  const S = (v) => R.steppedTime(v);
  eq(R.sceneOf(0), 1, 'S1 起点', issues); eq(R.sceneOf(9.99), 1, 'S1 终点', issues);
  eq(R.sceneOf(10), 2, 'S2 起点', issues); eq(R.sceneOf(19.99), 2, 'S2 终点', issues);
  eq(R.sceneOf(20), 3, 'S3 起点', issues); eq(R.sceneOf(29.99), 3, 'S3 终点', issues);
  for (const [t, v] of [[0, 18], [10, 45], [12.5, 72], [15, 91], [17.5, 97], [20, 97], [26, 12]]) eq(R.contextAt(S(t)), v, `CONTEXT @${t}s`, issues);
  for (const [t, v] of [[0, 6], [10, 14], [12.5, 25], [15, 31], [17.5, 32], [26, 3]]) eq(R.memoriesAt(S(t)), v, `MEMORIES @${t}s`, issues);
  for (const [t, v] of [[0, 20], [10, 20], [12.5, 50], [15, 80], [17.5, 95], [19.99, 95]]) eq(R.coverageAt(S(t)), v, `WALL 密度 @${t}s`, issues);
  if (!R.hudState(S(26)).kept) issues.push('S3 HUD 未标注 KEPT');
  eq(R.cardVisibleCount(S(6)), 6, 'S1 稀疏卡数', issues);
  eq(R.cardVisibleCount(S(19.99)), 32, 'S2 铺满卡数', issues);
  eq(R.cardVisibleCount(S(23.5)), 0, 'S3 淡出后卡数', issues);
  eq(R.cardVisibleCount(S(25)), 3, 'S3 只留 3 张', issues);
  eq(R.semanticState(3).touchLift, R.TOUCH_LIFT, 'S1 伸手碰卡：卡片抬起', issues);
  if (!R.semanticState(26).bubbleVisible) issues.push('S3 气泡未出现');
  eq(R.semanticState(26).narration, R.NARRATIONS.s3, 'S3 底部旁白', issues);
  // 3 张保留卡轻轻脉动：矩形尺寸随台阶时间变化
  const a = R.keptRect(R.KEPT_CARDS[0], S(25)), b = R.keptRect(R.KEPT_CARDS[0], S(25.5));
  if (JSON.stringify(a) === JSON.stringify(b)) issues.push('3 张保留卡未脉动');
  return { name: '3 场 × 600 帧 / CONTEXT 18→45→72→91→97→12 / MEMORIES 6→32→3 KEPT / 密度 20→50→80→95%', issues };
}

// 5) 逐帧几何：0px 容差、无截断、整数框、1800 帧全覆盖
function checkFrames() {
  const issues = []; let instances = 0, comparisons = 0;
  for (let n = 0; n < R.NFRAMES; n++) {
    const { scene, groups, bounds } = R.layoutAt(n / R.FPS);
    for (const [gname, list] of Object.entries(groups)) {
      if (!list.length) continue;
      const bound = bounds[gname];
      if (!bound) { issues.push(`frame ${n}: 组 ${gname} 缺边界`); continue; }
      instances += list.length;
      for (let i = 0; i < list.length; i++) {
        const el = list[i];
        if (el.box.some((v) => !Number.isInteger(v))) issues.push(`frame ${n} ${gname}/${el.name}: 非整数框 [${el.box}]`);
        if (outside(el.box, bound)) issues.push(`frame ${n} scene ${scene} ${gname}/${el.name}: 截断 [${el.box}]`);
        for (let j = i + 1; j < list.length; j++) {
          comparisons++;
          if (overlap(el.box, list[j].box)) issues.push(`frame ${n} scene ${scene} ${gname}: 重叠 ${el.name}[${el.box}] × ${list[j].name}[${list[j].box}] area=${interArea(el.box, list[j].box)}`);
        }
      }
    }
  }
  return { name: `逐帧几何 0px 容差 / 无截断 (${R.NFRAMES} 帧, ${instances} 实例, ${comparisons} 对)`, issues };
}

// 6) 运动：30fps 台阶 / 穿行 / 密度单调 / 单镜无黑场
function checkMotion() {
  const issues = [];
  const pairs = [0, 2, 58, 120, 240, 420, 560, 598, 600, 700, 860, 1000, 1100, 1180, 1198, 1200, 1300, 1450, 1600, 1700, 1740, 1760, 1798];
  for (const k of pairs) {
    const a = frameData(k), b = frameData(k + 1); let diff = 0;
    for (let i = 0; i < a.length; i += 4) if (a[i] !== b[i] || a[i + 1] !== b[i + 1] || a[i + 2] !== b[i + 2]) diff++;
    if (diff) issues.push(`台阶运动破坏: 帧 ${k}/${k + 1} 差 ${diff} 像素`);
  }
  for (const cut of [0, 600, 1200, 1799]) {
    const l = meanLuma(frameData(cut));
    if (l < 40) issues.push(`帧 ${cut} 近黑 (${l.toFixed(1)}), 本集应为奶油单镜`);
  }
  // S2 叙穿行：x 单调递增；S3 停下后 x 恒定
  let last = -1;
  for (let t = 10; t < 20; t += 0.25) {
    const x = R.characterX(R.steppedTime(t));
    if (x < last) issues.push(`S2 穿行回退 @${t}s: ${last} → ${x}`);
    last = x;
  }
  if (R.characterX(R.steppedTime(24)) !== R.characterX(R.steppedTime(29.9))) issues.push('S3 叙未停下');
  // 卡片墙密度：S2 单调不减 → 32 张；S3 单调不增 → 0 张，再只留 3 张
  let prev = 0;
  for (let t = 0; t < 20; t += 0.25) {
    const n = R.visibleWall(R.steppedTime(t)).length;
    if (n < prev) issues.push(`S1/S2 卡片数回退 @${t}s: ${prev} → ${n}`);
    prev = n;
  }
  if (prev !== 32) issues.push(`S2 末卡片数 ${prev} ≠ 32`);
  prev = 32;
  for (let t = 20; t < 23.5; t += 0.1) {
    const n = R.visibleWall(R.steppedTime(t)).length;
    if (n > prev) issues.push(`S3 淡出期卡片数回升 @${t}s: ${prev} → ${n}`);
    prev = n;
  }
  return { name: '30fps 台阶 (60fps 管线每 2 帧保持 1 帧) / 叙穿行与停下 / 卡片密度 20%→95% 单调 / 无黑场', issues };
}

// 7) 分场像素 + SCALE=2 严格最近邻
function checkPixels() {
  const issues = [];
  const samples = [0, 300, 599, 600, 900, 1199, 1200, 1300, 1500, 1700, 1799];
  for (const n of samples) {
    const d = frameData(n);
    if (hex(d, 4, 4) !== '#050505') issues.push(`帧 ${n} 顶部 HUD 非黑: ${hex(d, 4, 4)}`);
    if (hex(d, 4, 330) !== '#050505') issues.push(`帧 ${n} 底部 HUD 非黑: ${hex(d, 4, 330)}`);
    const bg = hex(d, 320, 45), fl = hex(d, 600, 280);
    const [br, bgc, bb] = [1, 3, 5].map((i) => parseInt(bg.slice(i, i + 2), 16));
    const [fr, fg, fb] = [1, 3, 5].map((i) => parseInt(fl.slice(i, i + 2), 16));
    if (!(br > 220 && br < 235 && bgc > 214 && bgc < 229 && bb > 207 && bb < 222)) issues.push(`帧 ${n} 奶油渐变底异常 ${bg}`);
    if (!(fr > 195 && fr < 215 && fg > 182 && fg < 202 && fb > 167 && fb < 187)) issues.push(`帧 ${n} 地面带异常 ${fl}`);
  }
  // 叙三档：像素级珊瑚包围盒 / 分场珊瑚像素
  const charCoral = (n) => {
    const ts = R.steppedTime(n / R.FPS), x = R.characterX(ts), sc = R.sceneOf(ts);
    return countColor(frameData(n), '#d16e59', sc === 3 ? [x, 248, 41, 20] : [x, 235, 58, 33]);
  };
  for (const [n, min] of [[599, 800], [900, 500], [1199, 300], [1500, 300], [1700, 300]]) {
    const c = charCoral(n);
    if (!(c >= min)) issues.push(`帧 ${n} 叙珊瑚像素 ${c} < ${min}`);
  }
  // S1 白卡 / S3 灰化 / 气泡 / 保留卡
  const d599 = frameData(599);
  if (countColor(d599, '#fffefb', [8, 51, 32, 24]) < 300) issues.push('S1 白卡不可见');
  const white1200 = countColor(frameData(1200), '#fffefb', [0, 39, 640, 282]);
  const white1300 = countColor(frameData(1300), '#fffefb', [0, 39, 640, 282]);
  if (!(white1200 > 8000 && white1300 < white1200 * 0.7)) issues.push(`S3 卡片墙未从边缘变灰淡出: ${white1200} → ${white1300}`);
  const d1700 = frameData(1700);
  if (countColor(d1700, '#d16e59', [R.BUBBLE.x, R.BUBBLE.y, R.BUBBLE.w, R.BUBBLE.h]) < 8000) issues.push('S3 AI 珊瑚气泡不可见');
  if (countColor(d1700, '#fffefb', [R.BUBBLE.x, R.BUBBLE.y, R.BUBBLE.w, R.BUBBLE.h]) < 100) issues.push('S3 气泡内白字不可见');
  for (const c of R.KEPT_CARDS) if (countColor(d1700, '#f4d3c6', [c.x, c.y, c.w, c.h]) < 1000) issues.push(`保留卡 ${c.index + 1} 未恢复浅珊瑚`);
  const heart = [R.characterX(R.steppedTime(1700 / 60)) + 13, 230, 9, 5];
  if (countColor(d1700, '#d16e59', heart) < 6) issues.push('叙头顶 ♥ 不可见');
  // SCALE=2 最近邻：逐像素比对 base 与 out 的 2×2 块
  for (const n of [0, 300, 599, 600, 900, 1199, 1200, 1500, 1700, 1799]) {
    const { baseCanvas, outCanvas } = R.renderFrameToCanvas(n);
    const base = readPixels(baseCanvas).data, out = readPixels(outCanvas).data;
    let bad = 0;
    for (let y = 0; y < R.BH; y++) for (let x = 0; x < R.BW; x++) {
      const si = (y * R.BW + x) * 4;
      for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx < 2; dx++) {
        const di = ((y * 2 + dy) * R.FW + x * 2 + dx) * 4;
        if (Math.abs(out[di] - base[si]) > 1 || Math.abs(out[di + 1] - base[si + 1]) > 1 || Math.abs(out[di + 2] - base[si + 2]) > 1) bad++;
      }
    }
    if (bad) issues.push(`帧 ${n}: ${bad} 输出像素偏离严格 2× 最近邻`);
  }
  return { name: '分场像素 (HUD/奶油底/地面/白卡/灰化/气泡/保留卡/♥) + SCALE=2 严格最近邻 (10 帧)', issues };
}

// 8) 叙：三档精确珊瑚包围盒、黑眼、无嘴线描边、头顶 ♥
function checkXu() {
  const issues = [];
  for (const size of ['large', 'medium', 'small']) {
    const [w, h] = R.CHAR_SIZES[size];
    const cv = createCanvas(200, 100), ctx = cv.getContext('2d');
    ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, 200, 100);
    R.drawXu(ctx, 10, 80, size);
    const d = readPixels(cv).data;
    let minX = 1e9, maxX = -1, minY = 1e9, maxY = -1, coral = 0, black = 0, blackBelow = 0;
    for (let y = 0; y < 100; y++) for (let x = 0; x < 200; x++) {
      const c = hex(d, x, y, 200);
      if (c === '#d16e59') { coral++; minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y); }
      if (c === '#171615') { black++; if (y > 80 - h + h * 0.6) blackBelow++; }
    }
    if (maxX - minX + 1 !== w || maxY - minY + 1 !== h) issues.push(`叙 ${size} 珊瑚包围盒 ${maxX - minX + 1}×${maxY - minY + 1} ≠ ${w}×${h}`);
    if (coral < w * h * 0.3) issues.push(`叙 ${size} 珊瑚块面积不足 ${coral}`);
    if (black < 2) issues.push(`叙 ${size} 缺黑眼`);
    if (blackBelow > 0) issues.push(`叙 ${size} 眼下出现黑色像素 (疑似嘴线/描边)`);
  }
  const hr = R.heartRects();
  if (hr.length < 5 || hr.reduce((s, r) => s + r[2] * r[3], 0) < 20) issues.push('头顶 ♥ 块数/面积不足');
  return { name: '叙 192×84 / 116×66 / 82×40 @720p 精确包围盒 · 黑眼无嘴线 · 头顶 ♥ 像素块', issues };
}

// 9) 声音排程：卡片落点音帧对齐 / 密度加快 / BGM -14dB / amix=normalize=0
function checkAudio() {
  const issues = [];
  eq(A.BGM_GAIN_DB, -14, 'BGM 增益 dB', issues);
  eq(A.MIX_MODE, 'amix=normalize=0', '混音模式', issues);
  if (!A.BGM_PATH.endsWith('emotional_bgm.wav')) issues.push(`BGM 文件非 emotional_bgm.wav: ${A.BGM_PATH}`);
  if (!fs.existsSync(A.BGM_PATH)) issues.push('缺 audio/emotional_bgm.wav');
  const events = R.getCardSfxEvents();
  const lands = events.filter((e) => e.kind === 'card_land'), chimes = events.filter((e) => e.kind === 'keep_chime');
  eq(lands.length, 32, '卡片落点音数 (6+26)', issues);
  eq(chimes.length, 3, '保留卡提示音数', issues);
  for (const e of events) {
    if (Math.abs(e.t * R.FPS - Math.round(e.t * R.FPS)) > 5e-4) issues.push(`落点音 ${e.t}s 未对齐显示帧`);
    if (e.t < 0 || e.t >= R.DURATION) issues.push(`落点音 ${e.t}s 越界`);
  }
  const s2 = lands.slice(6).map((e) => e.t);
  const gaps = s2.slice(1).map((t, i) => t - s2[i]);
  const head = gaps.slice(0, 8).reduce((a, b) => a + b, 0) / 8;
  const tail = gaps.slice(-8).reduce((a, b) => a + b, 0) / 8;
  if (!(head > tail + 0.05)) issues.push(`落点音未随密度加快: 前段 ${head.toFixed(3)}s / 后段 ${tail.toFixed(3)}s`);
  if (A.synthesizeLanding().length !== Math.round(0.09 * A.SAMPLE_RATE)) issues.push('落点音波形时长异常');
  if (fs.existsSync(A.MIX_WAV)) {
    const stats = C.inspectMixNoClipping(A.MIX_WAV);
    if (Math.abs(stats.duration - R.DURATION) > 0.02) issues.push(`混音时长 ${stats.duration}s ≠ 30s`);
    if (stats.clipped > 0) issues.push(`混音削波 ${stats.clipped} samples`);
  }
  return { name: `卡片落点音 ${lands.length} 次 (间隔 ${head.toFixed(2)}s→${tail.toFixed(2)}s 加快) + 保留卡 3 次 + BGM -14dB + ${A.MIX_MODE}`, issues };
}

// 10) 输出媒体：1280×720 / 30.000s / h264 + aac / 60fps / 1800 帧
function checkMedia() {
  const issues = [];
  if (!fs.existsSync(A.MP4_OUT)) return { name: '输出 mp4 (尚未生成：渲染+mux 后复跑本项)', issues: [] };
  if (fs.statSync(A.MP4_OUT).size < 100000) issues.push(`mp4 体积过小 ${fs.statSync(A.MP4_OUT).size}B`);
  const probe = path.join(ROOT, 'node_modules', '@ffprobe-installer', 'linux-x64', 'ffprobe');
  const exe = fs.existsSync(probe) ? probe : 'ffprobe';
  try {
    const out = execFileSync(exe, ['-v', 'error', '-show_entries',
      'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames', '-of', 'json', A.MP4_OUT],
      { encoding: 'utf8' });
    const j = JSON.parse(out);
    const v = (j.streams || []).find((s) => s.codec_type === 'video');
    const a = (j.streams || []).find((s) => s.codec_type === 'audio');
    if (!v) issues.push('缺视频流');
    else {
      if (v.width !== 1280 || v.height !== 720) issues.push(`分辨率 ${v.width}×${v.height} ≠ 1280×720`);
      if (v.r_frame_rate !== '60/1') issues.push(`帧率 ${v.r_frame_rate} ≠ 60/1`);
      if (v.nb_frames && Number(v.nb_frames) !== 1800) issues.push(`帧数 ${v.nb_frames} ≠ 1800`);
    }
    if (!a || a.codec_name !== 'aac') issues.push('缺 AAC 音轨');
    const dur = Number(j.format && j.format.duration);
    if (Math.abs(dur - 30) > 0.15) issues.push(`时长 ${dur}s ≠ 30s`);
  } catch (e) { issues.push(`ffprobe 失败: ${e.message}`); }
  return { name: 'outputs/E30_memory_arena_v1.0.mp4：1280×720 / 60fps / 30s / h264 + AAC', issues };
}

console.log(`=== ${R.CHECK_TITLE} ===`);
const started = Date.now();
const results = [checkSpecs(), checkFonts(), checkWallGeometry(), checkNarrative(), checkFrames(),
  checkMotion(), checkPixels(), checkXu(), checkAudio(), checkMedia()];
let issueCount = 0;
for (const r of results) {
  issueCount += r.issues.length;
  console.log(`[${r.issues.length ? 'FAIL' : 'PASSED'}] ${r.name}`);
  for (const m of r.issues.slice(0, 30)) console.log(`   - ${m}`);
  if (r.issues.length > 30) console.log(`   ... ${r.issues.length - 30} more`);
}
const passed = results.filter((r) => !r.issues.length).length;
console.log(`=== Summary: ${passed}/${results.length} checks PASSED, ${issueCount} issue(s), ${((Date.now() - started) / 1000).toFixed(1)}s ===`);
process.exit(issueCount === 0 ? 0 : 1);
