'use strict';

// ===========================================================================
// Frontend client สำหรับระบบแย่งกดบัตรคิวร้านสเต็กมหาสาร
// ครอบคลุม: countdown timer, ลงทะเบียน+validation, anti-bot PoW,
//           ห้องรอคิว (poll), เลือกรอบ, hold→confirm, retry แบบ backoff
// ===========================================================================

const App = {
  token: null,            // auth bearer token
  userName: null,
  queueToken: null,
  config: null,
  hold: null,             // { holdId, slotId, expiresAt }
  serverOffset: 0,        // serverNow - clientNow เพื่อให้ countdown ตรงกับเซิร์ฟเวอร์
  pollTimer: null,
  countdownTimer: null,
};

const $ = (sel) => document.querySelector(sel);
const fmt = (sec) => {
  sec = Math.max(0, Math.floor(sec));
  const h = String(Math.floor(sec / 3600)).padStart(2, '0');
  const m = String(Math.floor((sec % 3600) / 60)).padStart(2, '0');
  const s = String(sec % 60).padStart(2, '0');
  return h === '00' ? `${m}:${s}` : `${h}:${m}:${s}`;
};
const serverNow = () => Date.now() + App.serverOffset;

function showStep(id) {
  ['countdown', 'queue', 'grab', 'confirm', 'ticket'].forEach((s) => {
    $(`#step-${s}`).classList.toggle('hidden', s !== id);
  });
}

function banner(msg, kind = 'info', autohideMs = 0) {
  const el = $('#banner');
  el.textContent = msg;
  el.className = `banner ${kind}`;
  if (autohideMs) setTimeout(() => el.classList.add('hidden'), autohideMs);
}

// ---------------------------------------------------------------------------
// fetch + retry แบบ exponential backoff (ดีเลย์ 0.5s, 1s, 2s, 4s)
// retry เฉพาะ network error และ 5xx/429 เท่านั้น; 4xx อื่น ๆ ส่งกลับให้ caller จัดการ
// ---------------------------------------------------------------------------
async function api(pathname, { method = 'GET', body, auth = true, retries = 4 } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (auth && App.token) headers['Authorization'] = `Bearer ${App.token}`;

  let attempt = 0;
  for (;;) {
    try {
      const res = await fetch(pathname, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });
      const data = await res.json().catch(() => ({}));

      if (res.status === 429 && attempt < retries) {
        const wait = (data.retryAfterSec || 1) * 1000;
        banner(`ระบบกำลังหนาแน่น กำลังลองใหม่ใน ${Math.ceil(wait / 1000)} วิ…`, 'warn', wait);
        await sleep(wait);
        attempt++;
        continue;
      }
      if (res.status >= 500 && attempt < retries) {
        await sleep(backoff(attempt));
        attempt++;
        continue;
      }
      return { status: res.status, ok: res.ok, data };
    } catch (err) {
      // network error → retry
      if (attempt < retries) {
        banner('การเชื่อมต่อขัดข้อง กำลังลองใหม่…', 'warn', backoff(attempt));
        await sleep(backoff(attempt));
        attempt++;
        continue;
      }
      return { status: 0, ok: false, data: { error: 'network_error' } };
    }
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const backoff = (n) => Math.min(500 * 2 ** n, 8000);

// ---------------------------------------------------------------------------
// Anti-bot: แก้ proof-of-work ในเบราว์เซอร์ด้วย Web Crypto (SHA-256)
// หา counter ที่ทำให้ hash ขึ้นต้นด้วย '0' * difficulty
// ---------------------------------------------------------------------------
async function solvePow(nonce, difficulty) {
  const prefix = '0'.repeat(difficulty);
  const enc = new TextEncoder();
  for (let counter = 0; ; counter++) {
    const buf = await crypto.subtle.digest('SHA-256', enc.encode(`${nonce}:${counter}`));
    const hex = [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
    if (hex.startsWith(prefix)) return counter;
    if (counter % 5000 === 0) await sleep(0); // ปล่อยให้ UI หายใจ
  }
}

// ===========================================================================
// STEP 0: โหลด config + เริ่ม countdown
// ===========================================================================
async function init() {
  const { data } = await api('/api/config', { auth: false });
  App.config = data;
  App.serverOffset = data.serverNow - Date.now();
  $('#restaurantName').textContent = data.restaurant.name;
  $('#tagline').textContent = data.restaurant.tagline;
  renderSlots(data.slots);
  startSaleCountdown();
}

function startSaleCountdown() {
  clearInterval(App.countdownTimer);
  App.countdownTimer = setInterval(() => {
    const remain = (App.config.opensAt - serverNow()) / 1000;
    $('#countdown').textContent = fmt(remain);
    if (remain <= 0) {
      $('#countdown').textContent = 'เปิดแล้ว!';
      $('#registerBtn').textContent = 'ลงทะเบียน & เข้าคิวเลย';
      clearInterval(App.countdownTimer);
    }
  }, 250);
}

// ===========================================================================
// STEP 1: ลงทะเบียน (client-side validation ก่อนส่ง)
// ===========================================================================
function validate({ name, phone }) {
  const errors = {};
  if (!name || name.trim().length < 2) errors.name = 'กรุณากรอกชื่ออย่างน้อย 2 ตัวอักษร';
  const p = (phone || '').replace(/[\s-]/g, '');
  if (!/^0\d{8,9}$/.test(p)) errors.phone = 'เบอร์โทรไม่ถูกต้อง (เช่น 0812345678)';
  return errors;
}

function showFieldErrors(errors) {
  document.querySelectorAll('.field-error').forEach((el) => {
    el.textContent = errors[el.dataset.for] || '';
  });
}

$('#registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = $('#name').value;
  const phone = $('#phone').value;
  const errors = validate({ name, phone });
  showFieldErrors(errors);
  if (Object.keys(errors).length) return;

  const btn = $('#registerBtn');
  btn.disabled = true;
  btn.textContent = 'กำลังลงทะเบียน…';

  const reg = await api('/api/auth/register', { method: 'POST', auth: false, body: { name, phone } });
  if (!reg.ok) {
    if (reg.data.fields) showFieldErrors(reg.data.fields);
    else banner('ลงทะเบียนไม่สำเร็จ ลองใหม่อีกครั้ง', 'error', 4000);
    btn.disabled = false;
    btn.textContent = 'ลงทะเบียน';
    return;
  }
  App.token = reg.data.token;
  App.userName = reg.data.name;

  await joinQueue();
  btn.disabled = false;
  btn.textContent = 'ลงทะเบียน';
});

// ===========================================================================
// STEP 2: เข้าคิว — ทำ PoW (+ CAPTCHA) ก่อน แล้วเข้าห้องรอ
// ===========================================================================
async function joinQueue() {
  banner('🛡️ กำลังพิสูจน์ว่าไม่ใช่บอท (proof-of-work)…', 'info');
  const ch = await api('/api/challenge', { auth: false });
  const counter = await solvePow(ch.data.nonce, ch.data.difficulty);

  // จุดเสียบ CAPTCHA จริง: ถ้าเปิดใช้ ให้ดึง token จาก widget แล้วส่งมาด้วย
  const captchaToken = App.config.captchaEnabled ? 'dev-captcha-ok' : undefined;

  banner('🚪 กำลังเข้าห้องรอคิว…', 'info');
  const res = await api('/api/queue/join', {
    method: 'POST',
    body: { nonce: ch.data.nonce, counter, captchaToken },
  });
  if (!res.ok) {
    banner(res.data.message || 'เข้าคิวไม่สำเร็จ ลองใหม่', 'error', 5000);
    return;
  }
  App.queueToken = res.data.queueToken;
  $('#banner').classList.add('hidden');
  showStep('queue');
  applyQueueStatus(res.data);
  startQueuePolling();
}

function startQueuePolling() {
  clearInterval(App.pollTimer);
  const poll = async () => {
    const res = await api(`/api/queue/status?token=${encodeURIComponent(App.queueToken)}`);
    if (res.ok) applyQueueStatus(res.data);
  };
  App.pollTimer = setInterval(poll, 1500);
  poll();
}

function applyQueueStatus(st) {
  if (st.status === 'admitted') {
    clearInterval(App.pollTimer);
    enterGrabZone(st);
    return;
  }
  if (st.status === 'expired' || st.status === 'done') {
    clearInterval(App.pollTimer);
    banner('สิทธิ์ในคิวหมดอายุ กรุณาเข้าคิวใหม่', 'error');
    showStep('countdown');
    return;
  }
  // ยัง waiting
  $('#queuePosition').textContent = st.position;
  $('#queueWait').textContent = st.estimatedWaitSec > 0 ? `~${fmt(st.estimatedWaitSec)}` : 'ใกล้แล้ว';
  $('#queueStatusPill').textContent = st.saleOpen ? 'กำลังเลื่อนคิว' : 'รอเปิดขาย';
  // progress: ยิ่ง position น้อยยิ่งเต็ม (อิงจากจำนวนคนข้างหน้าตอนเริ่ม)
  const start = App._startPos || (App._startPos = st.position);
  const pct = Math.min(100, Math.max(2, ((start - st.position + 1) / start) * 100));
  $('#queueProgress').style.width = `${pct}%`;
}

$('#leaveQueueBtn').addEventListener('click', async () => {
  clearInterval(App.pollTimer);
  await api('/api/queue/leave', { method: 'POST', body: { queueToken: App.queueToken } });
  App.queueToken = null;
  App._startPos = null;
  showStep('countdown');
});

// ===========================================================================
// STEP 3: โซนกดบัตร — เลือกรอบ พร้อม countdown สิทธิ์ admit
// ===========================================================================
let admitTimer = null;
function enterGrabZone(st) {
  banner('🎉 ถึงคิวคุณแล้ว! รีบเลือกรอบ', 'ok', 3000);
  showStep('grab');
  refreshSlots();

  clearInterval(admitTimer);
  admitTimer = setInterval(() => {
    const remain = (st.admitExpiresAt - serverNow()) / 1000;
    $('#admitCountdown').textContent = fmt(remain);
    if (remain <= 0) {
      clearInterval(admitTimer);
      banner('หมดเวลาเลือกรอบ ระบบคืนสิทธิ์ให้คิวถัดไป', 'error');
      showStep('countdown');
    }
  }, 250);
}

async function refreshSlots() {
  const { data } = await api('/api/config', { auth: false });
  renderSlots(data.slots, true);
}

function renderSlots(slots, grabbable = false) {
  const list = $('#slotList');
  if (!list) return;
  list.innerHTML = '';
  slots.forEach((s) => {
    const div = document.createElement('div');
    div.className = `slot ${s.soldOut ? 'soldout' : ''}`;
    const low = !s.soldOut && s.remaining <= 5;
    div.innerHTML = `
      <div>
        <div class="slot-label">${s.label}</div>
        <div class="slot-remain ${low ? 'low' : ''}">${s.soldOut ? 'เต็มแล้ว' : `เหลือ ${s.remaining} ที่`}</div>
      </div>`;
    if (grabbable && !s.soldOut) {
      const btn = document.createElement('button');
      btn.className = 'btn primary';
      btn.textContent = 'กดจอง';
      btn.onclick = () => grabSlot(s.id, s.label, btn);
      div.appendChild(btn);
    }
    list.appendChild(div);
  });
}

// ===========================================================================
// STEP 4: hold → confirm (inventory locking + checkout countdown)
// ===========================================================================
let holdTimer = null;
async function grabSlot(slotId, slotLabel, btn) {
  btn.disabled = true;
  btn.textContent = 'กำลังจอง…';
  const res = await api('/api/grab/hold', { method: 'POST', body: { slotId, queueToken: App.queueToken } });

  if (!res.ok) {
    if (res.data.error === 'sold_out') {
      banner('รอบนี้เต็มแล้ว ลองรอบอื่น', 'error', 3000);
      refreshSlots();
    } else if (res.data.error === 'not_admitted') {
      banner('สิทธิ์หมดอายุ กรุณาเข้าคิวใหม่', 'error');
      showStep('countdown');
    } else {
      banner('จองไม่สำเร็จ ลองใหม่', 'error', 3000);
      btn.disabled = false;
      btn.textContent = 'กดจอง';
    }
    return;
  }

  clearInterval(admitTimer);
  App.hold = res.data;
  $('#confirmSlotLabel').textContent = slotLabel;
  showStep('confirm');

  clearInterval(holdTimer);
  holdTimer = setInterval(() => {
    const remain = (App.hold.expiresAt - serverNow()) / 1000;
    $('#holdCountdown').textContent = fmt(remain);
    if (remain <= 0) {
      clearInterval(holdTimer);
      banner('หมดเวลายืนยัน ที่นั่งถูกปล่อยคืน', 'error');
      App.hold = null;
      showStep('countdown');
    }
  }, 250);
}

$('#confirmBtn').addEventListener('click', async () => {
  if (!App.hold) return;
  const btn = $('#confirmBtn');
  btn.disabled = true;
  btn.textContent = 'กำลังยืนยัน…';
  const res = await api('/api/grab/confirm', {
    method: 'POST',
    body: { holdId: App.hold.holdId, queueToken: App.queueToken },
  });
  btn.disabled = false;
  btn.textContent = 'ยืนยันรับบัตรคิว';

  if (!res.ok) {
    banner(res.data.error === 'hold_expired' ? 'หมดเวลายืนยันแล้ว' : 'ยืนยันไม่สำเร็จ', 'error', 4000);
    if (res.data.error === 'hold_expired') showStep('countdown');
    return;
  }
  clearInterval(holdTimer);
  showTicket(res.data.ticket);
});

$('#cancelHoldBtn').addEventListener('click', async () => {
  if (App.hold) await api('/api/grab/release', { method: 'POST', body: { holdId: App.hold.holdId } });
  clearInterval(holdTimer);
  App.hold = null;
  showStep('grab');
  refreshSlots();
});

// ===========================================================================
// STEP 5: แสดงบัตรคิว
// ===========================================================================
function showTicket(t) {
  $('#ticketNumber').textContent = t.cardNumber;
  $('#ticketName').textContent = t.name;
  $('#ticketSlot').textContent = t.slotLabel;
  $('#ticketTime').textContent = new Date(t.issuedAt).toLocaleTimeString('th-TH');
  $('#banner').classList.add('hidden');
  showStep('ticket');
}

init();
