'use strict';

const { state, id, config } = require('./store');

// ---------------------------------------------------------------------------
// Inventory locking + hold/confirm flow
// ที่นั่งของแต่ละรอบคือสินค้าที่มีจำกัด ต้องกันปัญหา "ขายเกิน" (oversell)
// เมื่อมีคนแย่งกดพร้อมกัน
//
// Node เป็น single-threaded → โค้ดในฟังก์ชัน synchronous หนึ่งตัวจะรันจบ
// โดยไม่ถูกแทรก ทำให้ decrement + สร้าง hold เป็น atomic โดยธรรมชาติ
// (ในระบบหลายเครื่องต้องใช้ Redis WATCH/MULTI, SELECT ... FOR UPDATE,
//  หรือ atomic decrement — ดู README หัวข้อ Distributed transactions)
// ---------------------------------------------------------------------------

function listSlots() {
  return [...state.slots.values()].map((s) => ({
    id: s.id,
    label: s.label,
    capacity: s.capacity,
    remaining: s.remaining,
    soldOut: s.remaining <= 0,
  }));
}

// จองที่นั่งค้างไว้ (hold) — ล็อก 1 ที่จาก inventory ทันที แล้วตั้งเวลาหมดอายุ
function hold({ userId, slotId, queueToken }) {
  const slot = state.slots.get(slotId);
  if (!slot) return { ok: false, error: 'slot_not_found' };

  // หนึ่ง user ถือ hold ที่ยัง active ได้ทีละหนึ่ง (กันการกักของ)
  for (const h of state.holds.values()) {
    if (h.userId === userId && h.expiresAt > Date.now()) {
      return { ok: false, error: 'already_holding', holdId: h.holdId };
    }
  }

  // ---- critical section (atomic ใน event loop เดียว) ----
  if (slot.remaining <= 0) return { ok: false, error: 'sold_out' };
  slot.remaining -= 1;
  // -------------------------------------------------------

  const holdId = id('hold');
  const expiresAt = Date.now() + config.holdTtlMs;
  state.holds.set(holdId, { holdId, userId, slotId, queueToken, expiresAt });
  return { ok: true, holdId, slotId, expiresAt, holdTtlMs: config.holdTtlMs };
}

function releaseHold(holdId, userId, { restock = true } = {}) {
  const h = state.holds.get(holdId);
  if (!h) return { ok: false, error: 'hold_not_found' };
  if (userId && h.userId !== userId) return { ok: false, error: 'forbidden' };
  state.holds.delete(holdId);
  if (restock) {
    const slot = state.slots.get(h.slotId);
    if (slot) slot.remaining += 1; // คืนของเข้าสต็อก
  }
  return { ok: true };
}

// ยืนยันบัตรคิว — เปลี่ยน hold เป็นบัตรจริง (inventory ไม่คืน เพราะขายไปแล้ว)
function confirm({ holdId, userId }) {
  const h = state.holds.get(holdId);
  if (!h) return { ok: false, error: 'hold_expired_or_missing' };
  if (h.userId !== userId) return { ok: false, error: 'forbidden' };
  if (h.expiresAt <= Date.now()) {
    // หมดเวลา hold → ปล่อยคืนแล้วแจ้ง error (จะถูก sweep อยู่แล้ว แต่เคลียร์ทันที)
    releaseHold(holdId, userId, { restock: true });
    return { ok: false, error: 'hold_expired' };
  }

  const slot = state.slots.get(h.slotId);
  const user = state.users.get(userId);
  state.cardCounter += 1;
  const cardNumber = `MS-${String(state.cardCounter).padStart(3, '0')}`;
  const ticketId = id('tk');
  const ticket = {
    ticketId,
    cardNumber,
    userId,
    name: user ? user.name : '',
    phone: user ? user.phone : '',
    slotId: h.slotId,
    slotLabel: slot ? slot.label : h.slotId,
    issuedAt: Date.now(),
  };
  state.tickets.set(ticketId, ticket);
  state.holds.delete(holdId); // confirm แล้ว ไม่คืน inventory
  return { ok: true, ticket };
}

function ticketFor(userId) {
  for (const t of state.tickets.values()) {
    if (t.userId === userId) return t;
  }
  return null;
}

// เก็บกวาด hold ที่หมดอายุ → คืนของเข้าสต็อกอัตโนมัติ
function sweep() {
  const now = Date.now();
  for (const [holdId, h] of state.holds) {
    if (h.expiresAt <= now) {
      state.holds.delete(holdId);
      const slot = state.slots.get(h.slotId);
      if (slot) slot.remaining += 1;
    }
  }
}
setInterval(sweep, 1_000).unref();

module.exports = { listSlots, hold, releaseHold, confirm, ticketFor };
