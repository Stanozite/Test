'use strict';

const crypto = require('crypto');
const config = require('./config');

// ---------------------------------------------------------------------------
// In-memory store.
// หมายเหตุ: ใช้หน่วยความจำในโปรเซสเดียวเพื่อให้ demo รันได้ทันทีโดยไม่ต้องมี DB
// ในระบบจริงระดับ production ส่วนนี้คือ Redis / Postgres ที่รองรับ
// distributed locking + transaction ข้ามหลายเครื่อง (ดู README หัวข้อ "Scaling")
// ---------------------------------------------------------------------------

function resolveOpensAt() {
  if (config.saleOpensAtEnv) return config.saleOpensAtEnv;
  return Date.now() + config.saleOpensInMs;
}

const state = {
  opensAt: resolveOpensAt(),

  // userId -> { id, name, phone, token }
  users: new Map(),
  tokens: new Map(), // authToken -> userId

  // slotId -> { id, label, capacity, remaining }
  slots: new Map(
    config.slots.map((s) => [s.id, { ...s, remaining: s.capacity }])
  ),

  // คิว FIFO ของห้องรอ: queueToken -> entry
  // entry = { queueToken, userId, joinedAt, status, seq, admittedAt, lastSeenAt }
  // status: 'waiting' | 'admitted' | 'expired' | 'done'
  queue: new Map(),
  queueOrder: [], // queueToken ตามลำดับเข้าคิว (ใช้คำนวณ position)
  seqCounter: 0,

  // holdId -> { holdId, userId, slotId, queueToken, expiresAt }
  holds: new Map(),

  // บัตรคิวที่ยืนยันแล้ว: ticketId -> ticket
  tickets: new Map(),
  cardCounter: 0,

  // anti-bot proof-of-work challenges ที่ยังไม่ถูกใช้
  challenges: new Map(), // nonce -> { nonce, difficulty, expiresAt }
};

function id(prefix) {
  return `${prefix}_${crypto.randomBytes(9).toString('hex')}`;
}

module.exports = { state, id, config };
