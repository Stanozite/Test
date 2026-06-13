'use strict';

const crypto = require('crypto');
const { state, config } = require('./store');

// ---------------------------------------------------------------------------
// Anti-bot: Proof-of-Work (PoW)
// ก่อนเข้าคิวได้ ผู้ใช้ต้องแก้โจทย์ที่ใช้ CPU เล็กน้อย → ทำให้บอทที่จะสร้าง
// "คน" จำนวนมหาศาลมีต้นทุน ขณะที่ผู้ใช้จริงแทบไม่รู้สึก
// แนวคิดเดียวกับ Hashcash / Cloudflare proof-of-work challenge
// ---------------------------------------------------------------------------

function issueChallenge() {
  const nonce = crypto.randomBytes(16).toString('hex');
  const challenge = {
    nonce,
    difficulty: config.pow.difficulty,
    expiresAt: Date.now() + config.pow.challengeTtlMs,
  };
  state.challenges.set(nonce, challenge);
  return challenge;
}

function hash(nonce, counter) {
  return crypto.createHash('sha256').update(`${nonce}:${counter}`).digest('hex');
}

// ตรวจคำตอบ PoW; ใช้ครั้งเดียวแล้วทิ้ง (กัน replay)
function verifyPow(nonce, counter) {
  const ch = state.challenges.get(nonce);
  if (!ch) return { ok: false, error: 'invalid_or_used_challenge' };
  if (Date.now() > ch.expiresAt) {
    state.challenges.delete(nonce);
    return { ok: false, error: 'challenge_expired' };
  }
  const h = hash(nonce, counter);
  const prefix = '0'.repeat(ch.difficulty);
  if (!h.startsWith(prefix)) return { ok: false, error: 'pow_not_satisfied' };

  state.challenges.delete(nonce); // หนึ่ง challenge ต่อหนึ่งการเข้าคิว
  return { ok: true };
}

// จุดเสียบ CAPTCHA จริง — ในโหมด demo รับ devBypassToken ผ่านเลย
// ใน production ให้เรียก verify API ของ provider (reCAPTCHA/hCaptcha/Turnstile)
async function verifyCaptcha(token) {
  if (!config.captcha.enabled) return { ok: true, skipped: true };
  if (token && token === config.captcha.devBypassToken) return { ok: true };
  // TODO(production): POST ไปยัง https://challenges.cloudflare.com/turnstile/v0/siteverify
  //   ด้วย secret + response token แล้วเช็ค .success
  return { ok: false, error: 'captcha_failed' };
}

// เก็บกวาด challenge ที่หมดอายุ
function sweep() {
  const now = Date.now();
  for (const [nonce, ch] of state.challenges) {
    if (now > ch.expiresAt) state.challenges.delete(nonce);
  }
}
setInterval(sweep, 60_000).unref();

module.exports = { issueChallenge, verifyPow, verifyCaptcha };
