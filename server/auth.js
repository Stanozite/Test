'use strict';

const { state, id } = require('./store');

// Authentication แบบเบา ๆ สำหรับ demo: ลงทะเบียนด้วยชื่อ + เบอร์โทร แล้วได้ bearer token
// ใน production เปลี่ยนเป็น OTP ทาง SMS / OAuth / บัญชีสมาชิกจริง
const PHONE_RE = /^0\d{8,9}$/; // เบอร์ไทย 9-10 หลัก ขึ้นต้น 0

function validateRegistration({ name, phone }) {
  const errors = {};
  if (!name || String(name).trim().length < 2) {
    errors.name = 'กรุณากรอกชื่ออย่างน้อย 2 ตัวอักษร';
  }
  const normPhone = String(phone || '').replace(/[\s-]/g, '');
  if (!PHONE_RE.test(normPhone)) {
    errors.phone = 'เบอร์โทรไม่ถูกต้อง (ตัวอย่าง 0812345678)';
  }
  return { valid: Object.keys(errors).length === 0, errors, normPhone };
}

function register({ name, phone }) {
  const { valid, errors, normPhone } = validateRegistration({ name, phone });
  if (!valid) return { ok: false, errors };

  const userId = id('user');
  const token = id('tok');
  const user = { id: userId, name: String(name).trim(), phone: normPhone, token };
  state.users.set(userId, user);
  state.tokens.set(token, userId);
  return { ok: true, userId, token, name: user.name };
}

// ดึง user จาก Authorization: Bearer <token>
function authenticate(req) {
  const header = req.headers['authorization'] || '';
  const m = header.match(/^Bearer\s+(.+)$/i);
  if (!m) return null;
  const userId = state.tokens.get(m[1]);
  if (!userId) return null;
  return state.users.get(userId) || null;
}

module.exports = { register, authenticate, validateRegistration };
