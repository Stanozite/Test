'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const { state, config } = require('./store');
const rateLimit = require('./rateLimit');
const antibot = require('./antibot');
const auth = require('./auth');
const queue = require('./queue');
const inventory = require('./inventory');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');

// ---------------------------------------------------------------------------
// helpers
// ---------------------------------------------------------------------------
function send(res, status, body, headers = {}) {
  const data = typeof body === 'string' ? body : JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': typeof body === 'string' ? 'text/plain; charset=utf-8' : 'application/json; charset=utf-8',
    ...headers,
  });
  res.end(data);
}

function clientKey(req) {
  // ใน production ที่อยู่หลัง proxy ให้ใช้ X-Forwarded-For อย่างระมัดระวัง
  return (req.headers['x-forwarded-for'] || '').split(',')[0].trim() ||
    req.socket.remoteAddress || 'unknown';
}

function readJson(req) {
  return new Promise((resolve) => {
    let raw = '';
    req.on('data', (c) => {
      raw += c;
      if (raw.length > 1e6) req.destroy(); // กัน payload ใหญ่เกิน
    });
    req.on('end', () => {
      if (!raw) return resolve({});
      try { resolve(JSON.parse(raw)); } catch { resolve(null); }
    });
  });
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

function serveStatic(req, res) {
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  if (urlPath === '/') urlPath = '/index.html';
  const filePath = path.normalize(path.join(PUBLIC_DIR, urlPath));
  if (!filePath.startsWith(PUBLIC_DIR)) return send(res, 403, 'forbidden'); // กัน path traversal
  fs.readFile(filePath, (err, buf) => {
    if (err) return send(res, 404, 'ไม่พบหน้าที่ต้องการ');
    res.writeHead(200, { 'Content-Type': MIME[path.extname(filePath)] || 'application/octet-stream' });
    res.end(buf);
  });
}

// ---------------------------------------------------------------------------
// API routing
// ---------------------------------------------------------------------------
async function handleApi(req, res, url) {
  // rate limit ทุก endpoint ของ API
  const rl = rateLimit.allow(clientKey(req));
  if (!rl.ok) {
    return send(res, 429, { error: 'rate_limited', message: 'กดถี่เกินไป กรุณารอสักครู่', retryAfterSec: rl.retryAfterSec }, {
      'Retry-After': String(rl.retryAfterSec),
    });
  }

  const route = `${req.method} ${url.pathname}`;

  // ---- ข้อมูลสาธารณะของการเปิดขาย ----
  if (route === 'GET /api/config') {
    return send(res, 200, {
      restaurant: config.restaurant,
      opensAt: state.opensAt,
      serverNow: Date.now(),
      saleOpen: queue.saleOpen(),
      slots: inventory.listSlots(),
      pow: { difficulty: config.pow.difficulty },
      captchaEnabled: config.captcha.enabled,
    });
  }

  // ---- Anti-bot: ขอโจทย์ proof-of-work ----
  if (route === 'GET /api/challenge') {
    return send(res, 200, antibot.issueChallenge());
  }

  // ---- Auth: ลงทะเบียน/เข้าสู่ระบบ ----
  if (route === 'POST /api/auth/register') {
    const body = await readJson(req);
    if (!body) return send(res, 400, { error: 'bad_json' });
    const result = auth.register(body);
    if (!result.ok) return send(res, 422, { error: 'validation', fields: result.errors });
    return send(res, 200, { token: result.token, userId: result.userId, name: result.name });
  }

  // ตั้งแต่นี้ต้องล็อกอิน
  const user = auth.authenticate(req);
  const needsAuth = url.pathname.startsWith('/api/queue') || url.pathname.startsWith('/api/grab');
  if (needsAuth && !user) {
    return send(res, 401, { error: 'unauthorized', message: 'กรุณาลงทะเบียนก่อน' });
  }

  // ---- เข้าคิว (ต้องผ่าน PoW + CAPTCHA) ----
  if (route === 'POST /api/queue/join') {
    const body = await readJson(req);
    if (!body) return send(res, 400, { error: 'bad_json' });

    const cap = await antibot.verifyCaptcha(body.captchaToken);
    if (!cap.ok) return send(res, 403, { error: 'captcha_failed', message: 'ยืนยัน CAPTCHA ไม่ผ่าน' });

    const pow = antibot.verifyPow(body.nonce, body.counter);
    if (!pow.ok) return send(res, 403, { error: pow.error, message: 'ตรวจสอบ proof-of-work ไม่ผ่าน' });

    const entry = queue.join(user.id);
    return send(res, 200, { queueToken: entry.queueToken, ...queue.status(entry.queueToken) });
  }

  // ---- สถานะคิว (poll ถี่ ๆ ได้) ----
  if (route === 'GET /api/queue/status') {
    const queueToken = url.searchParams.get('token');
    const st = queue.status(queueToken);
    if (!st.found) return send(res, 404, { error: 'queue_not_found' });
    return send(res, 200, { queueToken, ...st });
  }

  // ---- ออกจากคิว ----
  if (route === 'POST /api/queue/leave') {
    const body = await readJson(req);
    if (body && body.queueToken) queue.leave(body.queueToken);
    return send(res, 200, { ok: true });
  }

  // ---- จองที่นั่งค้างไว้ (hold) — ต้องได้รับ admit แล้วเท่านั้น ----
  if (route === 'POST /api/grab/hold') {
    const body = await readJson(req);
    if (!body) return send(res, 400, { error: 'bad_json' });
    if (!queue.isAdmitted(body.queueToken, user.id)) {
      return send(res, 403, { error: 'not_admitted', message: 'ยังไม่ถึงคิวของคุณ' });
    }
    const result = inventory.hold({ userId: user.id, slotId: body.slotId, queueToken: body.queueToken });
    if (!result.ok) {
      const code = result.error === 'sold_out' ? 409 : 400;
      return send(res, code, result);
    }
    return send(res, 200, result);
  }

  // ---- ยกเลิก hold ----
  if (route === 'POST /api/grab/release') {
    const body = await readJson(req);
    if (!body || !body.holdId) return send(res, 400, { error: 'bad_request' });
    return send(res, 200, inventory.releaseHold(body.holdId, user.id));
  }

  // ---- ยืนยันออกบัตรคิว ----
  if (route === 'POST /api/grab/confirm') {
    const body = await readJson(req);
    if (!body || !body.holdId) return send(res, 400, { error: 'bad_request' });
    const result = inventory.confirm({ holdId: body.holdId, userId: user.id });
    if (!result.ok) {
      const code = result.error === 'hold_expired' ? 410 : 400;
      return send(res, code, result);
    }
    if (body.queueToken) queue.markDone(body.queueToken); // ออกจากคิว คืน slot ให้คนถัดไป
    return send(res, 200, result);
  }

  // ---- บัตรของฉัน ----
  if (route === 'GET /api/me/ticket') {
    if (!user) return send(res, 401, { error: 'unauthorized' });
    const ticket = inventory.ticketFor(user.id);
    return send(res, 200, { ticket });
  }

  return send(res, 404, { error: 'not_found' });
}

// ---------------------------------------------------------------------------
const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    if (url.pathname.startsWith('/api/')) return await handleApi(req, res, url);
    return serveStatic(req, res);
  } catch (err) {
    console.error(err);
    send(res, 500, { error: 'internal_error' });
  }
});

server.listen(config.PORT, () => {
  const opensIn = Math.max(0, Math.round((state.opensAt - Date.now()) / 1000));
  console.log(`🥩 ${config.restaurant.name} — ระบบกดบัตรคิว`);
  console.log(`   เปิดที่ http://localhost:${config.PORT}`);
  console.log(`   เปิดให้กดบัตรในอีก ${opensIn} วินาที (admitCapacity=${config.admitCapacity})`);
});

module.exports = server;
