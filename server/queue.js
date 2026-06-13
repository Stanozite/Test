'use strict';

const { state, id, config } = require('./store');

// ---------------------------------------------------------------------------
// Virtual Waiting Room / Queue management
// ผู้ใช้ทุกคนเข้าคิว FIFO ก่อน ระบบค่อย ๆ "ปล่อย" ผู้ใช้เข้าโซนกดบัตร
// ครั้งละไม่เกิน admitCapacity คน เพื่อกันไม่ให้ backend ล่มตอนคนแห่เข้าพร้อมกัน
// (เหมือนระบบ Queue-it / Cloudflare Waiting Room ของงานคอนเสิร์ต)
// ---------------------------------------------------------------------------

function saleOpen() {
  return Date.now() >= state.opensAt;
}

function admittedCount() {
  let n = 0;
  for (const e of state.queue.values()) if (e.status === 'admitted') n++;
  return n;
}

// เข้าคิว (หนึ่ง user หนึ่ง active entry)
function join(userId) {
  // ถ้ามี entry ที่ยัง active อยู่แล้ว ส่งกลับอันเดิม (กดซ้ำไม่ลัดคิว)
  for (const e of state.queue.values()) {
    if (e.userId === userId && (e.status === 'waiting' || e.status === 'admitted')) {
      return e;
    }
  }
  const queueToken = id('q');
  state.seqCounter += 1;
  const entry = {
    queueToken,
    userId,
    seq: state.seqCounter,
    status: 'waiting',
    joinedAt: Date.now(),
    admittedAt: null,
    lastSeenAt: Date.now(),
  };
  state.queue.set(queueToken, entry);
  state.queueOrder.push(queueToken);
  tick(); // เผื่อยังมีที่ว่างให้เข้าทันที
  return entry;
}

// ตำแหน่งในคิว (นับเฉพาะคนที่ยัง waiting อยู่ข้างหน้าเรา)
function positionOf(entry) {
  if (entry.status !== 'waiting') return 0;
  let pos = 1;
  for (const token of state.queueOrder) {
    const e = state.queue.get(token);
    if (!e || e.status !== 'waiting') continue;
    if (e.seq < entry.seq) pos++;
  }
  return pos;
}

function status(queueToken) {
  const entry = state.queue.get(queueToken);
  if (!entry) return { found: false };
  entry.lastSeenAt = Date.now(); // heartbeat กัน admit หลุดเพราะ TTL
  const position = positionOf(entry);
  const ahead = Math.max(0, position - 1);
  const estimatedWaitSec = entry.status === 'waiting'
    ? Math.ceil((ahead / config.admitCapacity) * (config.admitIntervalMs / 1000))
    : 0;
  return {
    found: true,
    status: entry.status,
    position,
    estimatedWaitSec,
    saleOpen: saleOpen(),
    opensAt: state.opensAt,
    serverNow: Date.now(),
    admitExpiresAt: entry.admittedAt ? entry.admittedAt + config.admitTtlMs : null,
  };
}

function leave(queueToken) {
  const entry = state.queue.get(queueToken);
  if (entry) entry.status = 'done';
  tick();
}

function markDone(queueToken) {
  const entry = state.queue.get(queueToken);
  if (entry) entry.status = 'done';
  tick();
}

// ตรวจว่า queueToken นี้ได้รับอนุญาตให้กดบัตรจริงไหม
function isAdmitted(queueToken, userId) {
  const entry = state.queue.get(queueToken);
  if (!entry) return false;
  if (entry.userId !== userId) return false;
  if (entry.status !== 'admitted') return false;
  entry.lastSeenAt = Date.now();
  return true;
}

// หัวใจของ admission control — เรียกเป็นจังหวะและตอนมีเหตุการณ์สำคัญ
function tick() {
  if (!saleOpen()) return;
  const now = Date.now();

  // 1) เตะคนที่ได้รับอนุญาตแล้วแต่เงียบหายเกิน TTL (สละสิทธิ์) คืน slot
  for (const e of state.queue.values()) {
    if (e.status === 'admitted' && now - e.lastSeenAt > config.admitTtlMs) {
      e.status = 'expired';
    }
  }

  // 2) ปล่อยคนหน้าคิวเข้าโซนกดบัตรจนเต็ม capacity
  let free = config.admitCapacity - admittedCount();
  if (free <= 0) return;
  for (const token of state.queueOrder) {
    if (free <= 0) break;
    const e = state.queue.get(token);
    if (!e || e.status !== 'waiting') continue;
    e.status = 'admitted';
    e.admittedAt = now;
    e.lastSeenAt = now;
    free--;
  }
}

// เดินจังหวะ admission อัตโนมัติ
setInterval(tick, config.admitIntervalMs).unref();

module.exports = {
  join, status, leave, markDone, isAdmitted, tick,
  saleOpen, admittedCount,
};
