#!/usr/bin/env node
'use strict';
// E30「记忆」音频：卡片出现的轻柔落点音（确定性合成 soft tap，时间来自
//   src/render_E30_memory_arena.getCardSfxEvents()，与画面卡片出现帧严格对齐）
//   + 环境 BGM audio/emotional_bgm.wav @ -14dB（1s 淡入 / 2s 淡出）
//   + 3 张保留卡恢复时的极轻「留白」提示音。
//
// 混音：JS 内确定性浮点相加，等价 ffmpeg `amix=inputs=N:normalize=0`
//   （仓库自带 @ffmpeg-installer/ffmpeg 为 2018 构建，amix 不支持 normalize=0，
//     沿用 build_audio_v2_common 既有做法；结果可逐样本审计）。ffmpeg 只负责编码/封装。
// 封装：libx264 + aac 192k + yuv420p → outputs/E30_memory_arena_v1.0.mp4
//
// 用法：node scripts/build_audio_E30.js [--mux]

const fs = require('fs');
const os = require('os');
const path = require('path');
const R = require('../src/render_E30_memory_arena');
const C = require('./build_audio_v2_common');

const ROOT = path.resolve(__dirname, '..');
const SAMPLE_RATE = 44100;
const BGM_PATH = path.join(ROOT, 'audio', 'emotional_bgm.wav');
const BGM_GAIN_DB = -14;                 // 环境 BGM（任务卡指定）
const CARD_GAIN_DB = -12;                // 卡片落点音
const CHIME_GAIN_DB = -16;               // 3 张保留卡的轻提示音
const FADE_IN = 1.0, FADE_OUT = 2.0;
const MIX_MODE = 'amix=normalize=0';
const MIX_WAV = process.env.MIX_WAV || path.join(os.tmpdir(), 'E30_memory_arena_mix.wav');
const MP4_OUT = path.join(ROOT, 'outputs', 'E30_memory_arena_v1.0.mp4');

const dbToGain = (db) => Math.pow(10, db / 20);
function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let z = a; z = Math.imul(z ^ (z >>> 15), z | 1); z ^= z + Math.imul(z ^ (z >>> 7), z | 61);
    return ((z ^ (z >>> 14)) >>> 0) / 4294967296;
  };
}

// 轻柔落点音：90ms 的低频木鱼式 thump + 一点滤波噪声，指数衰减（无爆音）。
function synthesizeLanding() {
  const n = Math.round(0.09 * SAMPLE_RATE);
  const out = new Float64Array(n);
  const rnd = mulberry32(30030);
  let noise = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SAMPLE_RATE;
    const env = Math.pow(Math.sin(Math.PI * (i / n)), 1.2) * Math.exp(-t * 12);
    noise = 0.72 * noise + 0.28 * (rnd() * 2 - 1);       // 一阶低通，去掉刺耳高频
    out[i] = env * (0.62 * Math.sin(2 * Math.PI * 172 * t)
      + 0.24 * Math.sin(2 * Math.PI * 286 * t + 0.4)
      + 0.18 * noise);
  }
  let peak = 0; for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(out[i]));
  if (peak > 0) for (let i = 0; i < n; i++) out[i] *= 0.85 / peak;
  return out;
}
// 保留卡提示音：240ms 的柔和双音（660Hz + 990Hz），比落点音更轻。
function synthesizeChime() {
  const n = Math.round(0.24 * SAMPLE_RATE);
  const out = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    const t = i / SAMPLE_RATE;
    const env = Math.pow(Math.sin(Math.PI * (i / n)), 1.5) * Math.exp(-t * 9);
    out[i] = env * 0.5 * (Math.sin(2 * Math.PI * 660 * t) + 0.4 * Math.sin(2 * Math.PI * 990 * t));
  }
  let peak = 0; for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(out[i]));
  if (peak > 0) for (let i = 0; i < n; i++) out[i] *= 0.8 / peak;
  return out;
}

function buildMix() {
  const duration = R.DURATION;
  const n = Math.round(duration * SAMPLE_RATE);
  if (!fs.existsSync(BGM_PATH)) throw new Error(`缺少环境 BGM: ${BGM_PATH}`);
  const bgm = C.readWav16(BGM_PATH);
  const bgmMono = bgm.ch[0];
  if (bgm.sampleRate !== SAMPLE_RATE) throw new Error(`BGM 采样率 ${bgm.sampleRate} ≠ ${SAMPLE_RATE}`);

  const events = R.getCardSfxEvents();
  const landing = synthesizeLanding();
  const chime = synthesizeChime();
  const bgmGain = dbToGain(BGM_GAIN_DB);
  const mix = new Float64Array(n);

  // 轨 1：环境 BGM -14dB，首尾淡变。
  for (let i = 0; i < n; i++) {
    const t = i / SAMPLE_RATE;
    let g = bgmGain;
    if (t < FADE_IN) g *= t / FADE_IN;
    if (t > duration - FADE_OUT) g *= Math.max(0, (duration - t) / FADE_OUT);
    mix[i] += (i < bgmMono.length ? bgmMono[i] / 32768 : 0) * g;
  }
  // 轨 2/3：卡片落点音 / 保留卡提示音（帧对齐；逐样本相加 = normalize=0）。
  for (const e of events) {
    const src = e.kind === 'keep_chime' ? chime : landing;
    const gain = dbToGain(e.gainDb === undefined ? CARD_GAIN_DB : e.gainDb);
    const off = Math.round(e.t * SAMPLE_RATE);
    for (let k = 0; k < src.length; k++) {
      const idx = off + k;
      if (idx >= 0 && idx < n) mix[idx] += src[k] * gain;
    }
  }
  // 峰值保护 -0.5 dBFS（等价 clip-guard，不改变各轨相对电平）。
  let peak = 0; for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(mix[i]));
  const LIMIT = 0.944;
  if (peak > LIMIT) for (let i = 0; i < n; i++) mix[i] *= LIMIT / peak;

  const out = new Int16Array(n);
  for (let i = 0; i < n; i++) out[i] = Math.max(-32768, Math.min(32767, Math.round(mix[i] * 32767)));
  C.writeWav16(MIX_WAV, SAMPLE_RATE, 1, [out]);
  const stats = C.inspectMixNoClipping(MIX_WAV);
  if (stats.clipped > 0) throw new Error(`检测到削波: ${stats.clipped} samples`);
  return { n, stats, events };
}

if (require.main === module) {
  const { stats, events } = buildMix();
  const lands = events.filter((e) => e.kind === 'card_land');
  console.log(`卡片落点音: ${lands.length} 次（S1 6 + S2 26，间隔随密度收紧）；保留卡提示音: ${events.length - lands.length} 次`);
  console.log(`BGM: emotional_bgm.wav ${BGM_GAIN_DB}dB (fade ${FADE_IN}/${FADE_OUT}s) | 落点 ${CARD_GAIN_DB}dB | 提示 ${CHIME_GAIN_DB}dB`);
  console.log(`混音: ${MIX_WAV} | ${MIX_MODE} | peak=${stats.peakDb.toFixed(2)} dBFS | clipped=0 | ${stats.duration.toFixed(2)}s`);
  console.log(`等价 ffmpeg: -filter_complex "[0:a]volume=-14dB[a];[a][1:a]amix=inputs=2:normalize=0[out]"`);
  if (process.argv.includes('--mux')) {
    C.muxVideo({ framesDir: process.env.FRAMES_DIR || R.OUT_DIR, mixPath: MIX_WAV, outMp4: MP4_OUT, fps: R.FPS });
  }
}

module.exports = {
  BGM_PATH, BGM_GAIN_DB, CARD_GAIN_DB, CHIME_GAIN_DB, FADE_IN, FADE_OUT,
  MIX_MODE, MIX_WAV, MP4_OUT, SAMPLE_RATE,
  synthesizeLanding, synthesizeChime, buildMix,
};
