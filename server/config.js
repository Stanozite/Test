'use strict';

// ค่าคอนฟิกกลางของระบบแย่งกดบัตรคิว
// ปรับค่าเหล่านี้เพื่อจำลองสถานการณ์ "คนแย่งเยอะ ของน้อย" แบบงานคอนเสิร์ต
module.exports = {
  PORT: process.env.PORT || 3000,

  restaurant: {
    name: 'ร้านสเต็กมหาสาร',
    tagline: 'สเต็กเนื้อนุ่ม คิวยาวเป็นกิโล',
  },

  // เวลาเปิดให้กดบัตร: ดีฟอลต์เปิดอีก 30 วินาทีหลังเซิร์ฟเวอร์สตาร์ท
  // ตั้งเป็น 0 เพื่อเปิดทันที หรือกำหนด epoch ms ผ่าน ENV SALE_OPENS_AT
  saleOpensInMs: Number(process.env.SALE_OPENS_IN_MS ?? 30_000),
  saleOpensAtEnv: process.env.SALE_OPENS_AT ? Number(process.env.SALE_OPENS_AT) : null,

  // รอบเวลา (time slots) แต่ละรอบมีจำนวนที่นั่งจำกัด = inventory ที่ต้องแย่งกัน
  slots: [
    { id: 'r1730', label: 'รอบ 17:30 น.', capacity: 15 },
    { id: 'r1830', label: 'รอบ 18:30 น.', capacity: 15 },
    { id: 'r1930', label: 'รอบ 19:30 น.', capacity: 10 },
    { id: 'r2030', label: 'รอบ 20:30 น.', capacity: 10 },
  ],

  // ---- Virtual waiting room (admission control) ----
  // จำนวนผู้ใช้สูงสุดที่ "เข้าห้องกดบัตร" ได้พร้อมกัน
  admitCapacity: Number(process.env.ADMIT_CAPACITY ?? 5),
  // ทุก ๆ กี่ ms ที่ระบบเลื่อนคิวเข้ามา
  admitIntervalMs: 1_000,
  // ถ้าได้รับอนุญาตเข้าแล้วเงียบหายเกินเวลานี้ ระบบถือว่าสละสิทธิ์ คืน slot ให้คนถัดไป
  admitTtlMs: Number(process.env.ADMIT_TTL_MS ?? 60_000),

  // ---- Inventory hold ----
  // จองที่นั่งค้างไว้ได้นานแค่ไหนก่อนต้องกดยืนยัน ไม่งั้นปล่อยคืน
  holdTtlMs: Number(process.env.HOLD_TTL_MS ?? 45_000),

  // ---- Rate limiting (token bucket ต่อ IP) ----
  rateLimit: {
    capacity: Number(process.env.RATE_CAPACITY ?? 30),      // จำนวน request สูงสุดในถัง
    refillPerSec: Number(process.env.RATE_REFILL ?? 10),    // เติมกลับกี่ token ต่อวินาที
  },

  // ---- Anti-bot: proof-of-work ----
  // ต้องหา counter ที่ทำให้ sha256(nonce:counter) ขึ้นต้นด้วยเลขศูนย์ (hex) ตามจำนวนนี้
  pow: {
    difficulty: Number(process.env.POW_DIFFICULTY ?? 4),
    challengeTtlMs: 2 * 60_000,
  },

  // เปิด/ปิดการบังคับ CAPTCHA (เป็นจุดเสียบต่อ provider จริง เช่น reCAPTCHA/hCaptcha/Turnstile)
  captcha: {
    enabled: process.env.CAPTCHA_ENABLED === 'true',
    // ในโหมด demo ยอมรับ token นี้ผ่านได้เลย
    devBypassToken: 'dev-captcha-ok',
  },
};
