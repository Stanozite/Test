# 🥩 ระบบแย่งกดบัตรคิว — ร้านสเต็กมหาสาร

ระบบ "แย่งกดบัตรคิว" สไตล์เดียวกับการกดบัตรคอนเสิร์ต (ที่นั่งจำกัด คนแย่งเยอะ)
สร้างด้วย **Node.js ล้วน ๆ ไม่มี dependency** รันได้ทันทีด้วยคำสั่งเดียว

ออกแบบเพื่อสาธิตสถาปัตยกรรมของ **reservation / virtual waiting room system**
ครบทั้งฝั่ง Client และ Server

---

## ▶️ วิธีรัน

```bash
node server/index.js
# เปิดเบราว์เซอร์ที่ http://localhost:3000
```

> เปิดหลาย ๆ แท็บ/หน้าต่าง (หรือ incognito หลายอัน) เพื่อจำลองสถานการณ์ "หลายคนแย่งกด" ได้

ค่าเริ่มต้น: ระบบจะ **เปิดให้กดบัตรในอีก 30 วินาที** หลังสตาร์ท (มีนับถอยหลัง)
อยากเปิดทันทีให้สั่ง `SALE_OPENS_IN_MS=0 node server/index.js`

---

## 🧩 องค์ประกอบที่ระบบนี้ครอบคลุม

### ฝั่ง Client (`public/`)
| องค์ประกอบ | ไฟล์ / ฟังก์ชัน | รายละเอียด |
|---|---|---|
| **Countdown timer** | `app.js → startSaleCountdown` | นับถอยหลังถึงเวลาเปิดขาย (sync เวลากับเซิร์ฟเวอร์ด้วย `serverOffset`) |
| **Queue waiting room** | `app.js → startQueuePolling / applyQueueStatus` | ห้องรอแสดงลำดับคิว + progress bar แบบเรียลไทม์ (poll ทุก 1.5 วิ) |
| **Authentication** | ฟอร์มลงทะเบียน → bearer token | ลงทะเบียนด้วยชื่อ+เบอร์ ได้ token ไว้เรียก API |
| **Form validation** | `app.js → validate` | ตรวจชื่อ/เบอร์ฝั่ง client ก่อนส่ง (เซิร์ฟเวอร์ตรวจซ้ำอีกชั้น) |
| **"Payment" / checkout flow** | `grabSlot → confirm` | hold ที่นั่ง → นับถอยหลัง → ยืนยันออกบัตร (จุดนี้เสียบ payment gateway ได้) |
| **Retry handling** | `app.js → api()` | retry อัตโนมัติแบบ exponential backoff เมื่อเจอ network error / 429 / 5xx |

### ฝั่ง Server (`server/`)
| องค์ประกอบ | ไฟล์ | รายละเอียด |
|---|---|---|
| **Rate limiting** | `rateLimit.js` | Token-bucket ต่อ IP กันการยิงถี่จากบอท → ตอบ `429 + Retry-After` |
| **Queue management** | `queue.js` | Virtual waiting room FIFO + admission control ปล่อยคนเข้าทีละชุด (`admitCapacity`) |
| **Inventory locking** | `inventory.js` | จองที่นั่งแบบ atomic, hold + หมดอายุคืนของอัตโนมัติ, กันขายเกิน (oversell) |
| **Distributed transactions** | `inventory.js` (hold→confirm) | รูปแบบ reserve-then-commit; ในระบบจริงคือ saga / 2-phase (ดูหัวข้อ Scaling) |
| **Anti-bot** | `antibot.js` | Proof-of-Work (Hashcash-style) บังคับก่อนเข้าคิว เพิ่มต้นทุนให้บอท |
| **CAPTCHA integration** | `antibot.js → verifyCaptcha` | จุดเสียบ provider จริง (reCAPTCHA / hCaptcha / Cloudflare Turnstile) |

---

## 🔄 Flow การทำงาน

```
นับถอยหลัง ──► ลงทะเบียน ──► [Anti-bot PoW] ──► เข้าห้องรอคิว
                                                      │  (admission control)
                                                      ▼
                                            ถึงคิว → เลือกรอบ ──► hold ที่นั่ง (ล็อก inventory)
                                                      │                │ มี countdown
                                                      ▼                ▼
                                            หมดเวลา = คืนสิทธิ์    ยืนยัน → ออกบัตรคิว 🎟️
```

**หัวใจของระบบแบบคอนเสิร์ต** คือ *virtual waiting room*: ทุกคนต่อคิว FIFO ก่อน
เซิร์ฟเวอร์ค่อย ๆ "ปล่อย" คนเข้าโซนกดบัตรครั้งละไม่เกิน `admitCapacity` คน
เพื่อไม่ให้ backend ล่มตอนคนแห่เข้าพร้อมกัน และทำให้การแย่งของยุติธรรมตามลำดับ

---

## ⚙️ ตัวแปรปรับแต่ง (ENV)

| ENV | ดีฟอลต์ | ความหมาย |
|---|---|---|
| `PORT` | `3000` | พอร์ต |
| `SALE_OPENS_IN_MS` | `30000` | เปิดขายในอีกกี่ ms (ตั้ง `0` = เปิดทันที) |
| `SALE_OPENS_AT` | – | กำหนดเวลาเปิดเป็น epoch ms ตรง ๆ |
| `ADMIT_CAPACITY` | `5` | จำนวนคนที่เข้าโซนกดบัตรได้พร้อมกัน |
| `ADMIT_TTL_MS` | `60000` | เข้าคิวแล้วเงียบเกินนี้ = สละสิทธิ์ |
| `HOLD_TTL_MS` | `45000` | hold ที่นั่งได้นานแค่ไหนก่อนต้องยืนยัน |
| `RATE_CAPACITY` / `RATE_REFILL` | `30` / `10` | ขนาดถัง / อัตราเติม ของ rate limiter |
| `POW_DIFFICULTY` | `4` | ความยากของ proof-of-work (จำนวนเลข 0 นำหน้า hash) |
| `CAPTCHA_ENABLED` | `false` | บังคับ CAPTCHA หรือไม่ |

ตัวอย่างจำลองงานเดือด: `ADMIT_CAPACITY=3 SALE_OPENS_IN_MS=10000 node server/index.js`

---

## 📈 การ Scale ขึ้น production (จากเดโม → ของจริง)

ระบบนี้เก็บ state ใน memory ของโปรเซสเดียวเพื่อให้รันง่าย จุดที่ต้องเปลี่ยนเมื่อขึ้นจริง:

- **Queue + inventory** → ย้ายไป **Redis** (atomic `DECR`, `WATCH/MULTI`) หรือ DB ที่มี
  `SELECT ... FOR UPDATE` เพื่อ lock ข้ามหลายเซิร์ฟเวอร์ ไม่ให้ขายเกิน
- **Distributed transaction** → ใช้รูปแบบ **saga** หรือ outbox pattern เชื่อม
  inventory ↔ payment ↔ การออกบัตร ให้ทำสำเร็จหรือ rollback พร้อมกัน
- **Rate limiting** → ใช้ Redis-based limiter ที่แชร์ทุก instance + WAF ขอบนอก
- **CAPTCHA** → เติม secret ใน `antibot.verifyCaptcha` แล้วเรียก siteverify ของ provider
- **Auth** → เปลี่ยนเป็น OTP ทาง SMS / OAuth + JWT แทน token ในหน่วยความจำ
- **Waiting room realtime** → เปลี่ยน polling เป็น WebSocket / SSE เพื่อ push ลำดับคิว

---

## 🗂️ โครงสร้างโปรเจกต์

```
server/
  index.js      HTTP server + routing + เสิร์ฟไฟล์ static
  config.js     ค่าคอนฟิกทั้งหมด (ปรับผ่าน ENV ได้)
  store.js      in-memory store กลาง
  auth.js       ลงทะเบียน + ตรวจ token + validation
  queue.js      virtual waiting room + admission control
  inventory.js  จองที่นั่ง (hold/confirm) + กันขายเกิน
  rateLimit.js  token-bucket rate limiter
  antibot.js    proof-of-work + จุดเสียบ CAPTCHA
public/
  index.html    UI ทุกขั้นตอน (countdown → คิว → กดบัตร → บัตรคิว)
  styles.css    ธีมร้านสเต็ก
  app.js        ตรรกะฝั่ง client ทั้งหมด
```
