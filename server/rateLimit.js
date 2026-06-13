'use strict';

const { config } = require('./store');

// Token-bucket rate limiter ต่อ key (ปกติคือ IP)
// ป้องกันการยิงถี่ ๆ จากบอท/สคริปต์ขณะเปิดให้แย่งบัตร
const buckets = new Map(); // key -> { tokens, last }

function allow(key) {
  const { capacity, refillPerSec } = config.rateLimit;
  const now = Date.now();
  let b = buckets.get(key);
  if (!b) {
    b = { tokens: capacity, last: now };
    buckets.set(key, b);
  }
  // เติม token ตามเวลาที่ผ่านไป
  const elapsedSec = (now - b.last) / 1000;
  b.tokens = Math.min(capacity, b.tokens + elapsedSec * refillPerSec);
  b.last = now;

  if (b.tokens >= 1) {
    b.tokens -= 1;
    return { ok: true, remaining: Math.floor(b.tokens) };
  }
  // เวลาที่ต้องรอจนกว่าจะมี 1 token
  const retryAfterSec = Math.ceil((1 - b.tokens) / refillPerSec);
  return { ok: false, retryAfterSec };
}

// เก็บกวาดถังที่เต็มแล้วและไม่ถูกใช้นาน เพื่อกัน memory โต
function sweep() {
  const now = Date.now();
  for (const [key, b] of buckets) {
    if (now - b.last > 5 * 60_000) buckets.delete(key);
  }
}
setInterval(sweep, 60_000).unref();

module.exports = { allow };
