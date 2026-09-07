# PROBE-1 · ลิสต์เป้าหมาย: บริษัทที่ขายแบบ Outcome-Based

> ประกอบ 2026-08-29 · **ตรวจชั้น T3 ครบแล้ว 2026-08-29** · ตารางทำงาน: [`templates/probe1-targets.csv`](templates/probe1-targets.csv)
> สถานะ: **ยังไม่ผ่านเกณฑ์ — 6 ราย จากที่ต้องการ 12**

---

## 🔴 ข้อค้นพบหลัก: "outcome-based" ถูกใช้กับสองอย่างที่ต่างกันคนละเรื่อง

การตรวจ T3 ทำให้เห็นว่านิยามที่เราใช้มาตลอดหลวมเกินไป และเมื่อรัดให้แน่น **ตลาดของ F1 หดลงมาก**

| | **(ก) Outcome-conditional** | **(ข) Per-unit-of-work** |
|---|---|---|
| คิดเงินเมื่อ | **สำเร็จเท่านั้น** — ล้มเหลว ไม่คิดเงิน | **ทุกครั้งที่ทำงาน** สำเร็จหรือไม่ก็คิด |
| ตัวอย่าง | Zendesk (ปิดเคสเองได้เท่านั้น) · Chargeflow 25% ของ dispute ที่ชนะ · Aurai 25% on wins · Anterior "ไม่คิดถ้าไม่มี measurable impact" | Prophet Security $10/investigation · eesel $0.40/ticket **ไม่ว่าจะแก้ได้หรือไม่** · Freshworks Freddy $0.10/session · Gorgias $0.90–1.00/interaction · CodaMetrix per-encounter |
| **มีข้อพิพาทเรื่อง "นับไหม"** | **มี → นี่คือตลาดของ F1** | **ไม่มี → ไม่มีอะไรให้เถียง ไม่ใช่ตลาดของ F1** |

ตลาดเองก็แยกสองอย่างนี้ออกแล้ว — บทวิเคราะห์เปรียบเทียบ vendor เขียนตรง ๆ ว่า:

> *"ราคาต่อหน่วยที่ถูกที่สุดไม่ใช่ราคาต่อ resolution — My AskAI และ eesel คิดเงินต่อ ticket ไม่ว่าจะแก้ปัญหาได้หรือไม่ · และ vendor แบบ custom ทุกรายคิดเงินคุณก่อนส่งมอบคุณค่า ผ่าน platform fee, implementation fee หรือ minimum — ซึ่งคือสิ่งที่ outcome pricing ควรกำจัดทิ้งพอดี"*

### ผลต่อ F1 — ต้องอ่านให้ชัด

ตัวเลข **~21.7% ของสัญญาองค์กรที่เราตื่นเต้นรอบก่อน น่าจะรวมแบบ (ข) และ hybrid เข้าไปด้วย** → **ห้ามอ่านเป็น TAM ของ F1**
TAM จริงของ F1 = แบบ (ก) เท่านั้น ซึ่งเล็กกว่ามาก และ**กระจุกใน CX หนักกว่าเดิม ไม่ใช่เบาลง**

---

## 🚨 สถานะเทียบเกณฑ์ — ไม่ผ่าน 2 ใน 3 ข้อ

| เกณฑ์ | สถานะ | รายละเอียด |
|---|---|---|
| ≥40 ราย | ✅ **46** | (ลดจาก 47 — Forethought ถูก Zendesk ซื้อไป มี.ค. 2026) |
| **≥12 รายนอก CX แบบ (ก)** | ❌ **6** | นับเข้มงวด · นับหลวมสุด (รวมที่ยังไม่ยืนยันและที่ทำได้ทั้งสองแบบ) ก็ได้แค่ **8** |
| ≥8 ราย verified จากเว็บบริษัทเอง | ⛔ **ตรวจไม่ได้** | ดูข้อจำกัดด้านล่าง |

**6 รายนอก CX ที่ผ่านแบบเข้มงวด**: Chargeflow · Aurai · Anterior · SmarterDx · Atomicwork · HubSpot Breeze prospecting
**+2 รายก้ำกึ่ง**: Adonis (ทำได้ทั้งสองแบบ ต้องถามว่าลูกค้าส่วนใหญ่เลือกอันไหน) · HighRadius (ประกาศ outcome-based แต่ไม่รู้ว่าเป็นแบบ ก จริงไหม)

### ⛔ ข้อจำกัดที่ต้องบอกตรง ๆ

**Session นี้ถูก network policy บล็อก egress ทั้งหมด** — WebFetch เข้าเว็บบริษัทไม่ได้เลย แม้แต่ `example.com` เหลือใช้ได้แค่ WebSearch ที่วิ่งผ่าน API ของ Anthropic

→ **เกณฑ์ "ยืนยันจากหน้าเว็บของบริษัทเอง" ทำจากที่นี่ไม่ได้** ต้องเปิดเองในเบราว์เซอร์ หรือรันในสภาพแวดล้อมที่เปิด egress
→ ผลตรวจทั้งหมดด้านล่างเป็น **หลักฐานชั้นรอง** แม้บางรายจะมาจากหน้า pricing ของบริษัทเองที่โผล่ในผลค้นหา (Atomicwork, Chargeflow)

---

## ผลตรวจรายบริษัท — 46 ราย

### ✅ (ก) Outcome-conditional · 15 ราย

**นอก CX — 6 ราย (นี่คือตัวเลขที่เกณฑ์วัด)**

| บริษัท | หมวด | หน่วย | หลักฐาน |
|---|---|---|---|
| **Chargeflow** | chargeback | 25% ของ dispute ที่ชนะ | ไม่ชนะไม่คิดเงิน · alert คิดเฉพาะที่กันได้สำเร็จ |
| **Aurai** | chargeback | 25% on wins | เริ่มฟรี จ่ายเฉพาะเคสที่ชนะ |
| **Anterior** | healthcare | measurable impact | **ไม่คิดเงินถ้าไม่มีผลกระทบที่วัดได้** |
| **SmarterDx** | healthcare RCM | contingency | ขึ้นค่า contingency ได้จนค่าเฉลี่ยสัญญาโตสามเท่า |
| **Atomicwork** | IT service desk | outcome | เสนอทางเลือก **"pay per outcome"** บนหน้า pricing ตัวเอง |
| **HubSpot Breeze** (prospecting) | sales | qualified lead ~$1.00 | outcome pricing สำหรับงานขาย รายแรก ๆ ในตลาด |

**ใน CX — 9 ราย**
Intercom Fin $0.99 · Zendesk $1.50–2.00 (ล้มเหลวไม่คิดเงินชัดเจน) · Salesforce Agentforce $2.00 · HubSpot Breeze Customer $0.50 · Lorikeet ~$0.80 · Quickchat ~$0.50–0.60 · Sierra / Decagon / Ada (custom ไม่เปิดราคา)

### 🟡 ก้ำกึ่ง · 2 ราย
- **Adonis** (healthcare RCM) — คิดได้ทั้ง *per claim processed* (แบบ ข) **หรือ** *% ของ denials ที่กู้คืน* (แบบ ก)
- **HighRadius** (order-to-cash) — ประกาศเลิก per-seat ไปใช้ outcome-based (ก.พ. 2026) แต่ไม่มีรายละเอียดว่าเป็นแบบ (ก) จริงไหม

### 🔵 (ข) Per-unit-of-work · 6 ราย — **ไม่ใช่ตลาดของ F1 แต่มีค่าเป็นกลุ่มเปรียบเทียบ**

| บริษัท | ราคา | ทำไมไม่ใช่ (ก) |
|---|---|---|
| **Gorgias** | $0.90–1.00/AI interaction **+ ค่า helpdesk ticket ซ้ำอีก $0.36–0.40** | คิดต่อ interaction ไม่ใช่ต่อ resolution · **ถูกบล็อกหลายเจ้าจัดว่าเป็น per-resolution ทั้งที่ไม่ใช่** |
| **Freshworks Freddy** | $0.10/session | คิดทุก session ไม่ว่าจะแก้ได้หรือไม่ |
| **eesel AI** | $0.40/ticket | คิดต่อ ticket ไม่ว่าจะแก้ได้หรือไม่ |
| **Prophet Security** | ~$10/investigation ($50k ต่อ 5,000) | คิดต่อการสอบสวน ไม่ใช่ต่อผลที่เจอ |
| **Dropzone AI** | ~$9/investigation (ถอนราคาแล้ว) | เหมือน Prophet |
| **CodaMetrix** | base fee + per-encounter | มี platform fee ก่อนส่งมอบคุณค่า |

> ⚠️ **กรณี Gorgias คือหลักฐานตรง ๆ ว่าตลาดสับสนเรื่องนิยามนี้จริง** — ซึ่งเป็นทั้งความเสี่ยงและโอกาสของ F1 (ดูท้ายไฟล์)

### ❌ ตกรอบ · 9 ราย
| บริษัท | โมเดลจริง |
|---|---|
| Moveworks | ต่อหัวพนักงานทั้งบริษัท ($150/user/ปี) ไม่ใช่ต่อ ticket |
| Espressive | ต่อหัวพนักงาน (ต่ำกว่า Moveworks 10–20%) |
| Aisera | enterprise license จาก $200K/ปี |
| Intezer | ต่อ endpoint |
| Radiant Security | flat rate unlimited — **กลุ่มควบคุม** |
| Kustomer | $89–139/user/เดือน |
| Aissist | $0.09 ต่อ**ข้อความ** |
| 11x | flat $3,750/เดือน |
| Artisan | usage ตามงานที่ทำ ไม่ผูกผลลัพธ์ |

### ⛔ ตัดออก — ไม่มีตัวตนแล้ว
**Forethought** — ถูก **Zendesk ซื้อไป มี.ค. 2026** (โมเดลเดิมคิดตาม ticket volume/usage อยู่แล้ว จึงไม่ผ่านทั้งสองทาง)

### ⬜ ตรวจไม่ได้ · 13 ราย
Gradient Labs · Crescendo · Maven AGI · Thena · Macha AI · Sobot · AnyReach · PolyAI · Cognigy · Redo · 7AI · AiSDR · EvenUp

ส่วนใหญ่คือ **"custom quote ไม่เปิดราคา"** ซึ่ง**เป็นข้อมูลในตัวมันเอง**: ขายผ่าน sales เท่านั้น = เข้าถึงยาก = ICP คนละแบบกับที่ probe ออกแบบไว้ (ยิงอีเมลเย็นแล้วได้คุยใน 2 สัปดาห์)

### 🔴 ฝ่ายค้าน · 1 ราย
**Parloa** — ลง Forbes (ม.ค. 2026) เรียก outcome pricing ว่า "กับดักที่สวยงาม" เชียร์ per-minute · **ยังเป็นเป้าหมายคุยอันดับต้น ๆ** เพราะคนที่ค้านดังที่สุดมักอธิบายกลไกได้ดีที่สุด

---

## สิ่งที่ควรทำต่อในสัปดาห์ที่ 1

`03-decision-rubric.md` ห้ามแก้ kill criteria หลังเริ่ม probe — **จึงไม่เสนอให้แก้เกณฑ์อีก** ใช้เวลาที่เหลือแบบนี้แทน:

1. **ขยายไปหมวดที่ยังไม่แตะ** — จัดซื้อ · แปลและ localization · recruiting · ทวงหนี้ · voice agent · ตรวจสอบเนื้อหา · logistics claims
   → หมวดพวกนี้มีวัฒนธรรม contingency อยู่ก่อนแล้ว **โอกาสเจอแบบ (ก) สูงกว่าหมวดที่สแกนไปแล้วมาก**
2. **ปิด 13 รายที่ตรวจไม่ได้** — ต้องเปิดเว็บเอง session ทำแทนไม่ได้
3. **ถ้าครบสัปดาห์แล้วยังไม่ถึง 12 → ฆ่า F1 ตามกติกา** เลื่อน F2/F3 ขึ้นมาแทน **อย่ายืดเวลา**

> ⛔ **สิ่งที่ต้องไม่ทำ**: อย่าลดนิยามกลับไปนับแบบ (ข) เพื่อให้ครบ 12
> นั่นคือการโกงตัวเองแบบที่ `03-decision-rubric.md` §anti-checklist เขียนเตือนไว้พอดี — และถ้านับแบบ (ข) เข้ามา ธุรกิจที่ได้จะไม่มีข้อพิพาทให้ตัดสิน ซึ่งแปลว่าไม่มีสินค้า

---

## 🎯 ทางที่ผลตรวจนี้เปิดให้ — อาจดีกว่า F1 เดิม

หลักฐานที่เจอระหว่างตรวจ:
- **Gorgias** ถูกจัดว่า per-resolution ทั้งที่คิดต่อ interaction และคิดค่า ticket ซ้ำอีกชั้น
- **eesel / Freshworks** คิดต่อ ticket/session ไม่ว่าจะแก้ได้หรือไม่ แต่ถูกจัดกลุ่มรวมกับ per-resolution
- **vendor แบบ custom ทุกราย** คิด platform fee ก่อนส่งมอบคุณค่า
- ตลาดเรียกทั้ง (ก) และ (ข) ว่า "outcome-based" เหมือนกันหมด

→ **ปัญหาที่พิสูจน์แล้วว่ามีจริงวันนี้ ไม่ใช่ "outcome นับไหม" แต่คือ "ราคาที่โฆษณาว่า outcome-based จริง ๆ คิดเงินยังไง"**
→ ผู้ซื้อคือ **ฝั่งที่กำลังจะซื้อ agent** — ตรงกับที่ Parloa บ่นใน Forbes พอดี
→ ทำเป็น free wedge ได้ทันที (ตรงกับ `99-quick-wins.md` QW-4) และเป็น distribution ให้ F1 ตัวจริง

**ยังไม่เสนอให้เปลี่ยนไปทำ** — บันทึกเป็นผู้สมัครใหม่ในสแกน (`D6`) และเอาไปถามใน probe

---

## แหล่งอ้างอิงเพิ่มจากรอบตรวจ

- ITSD — [Moveworks pricing (eesel)](https://www.eesel.ai/blog/moveworks-pricing) · [Moveworks vs Aisera (Rezolve)](https://www.rezolve.ai/blog/moveworks-vs-aisera) · [Atomicwork pricing](https://www.atomicwork.com/pricing)
- Healthcare — [SmarterDx contingency (Flare Capital)](https://www.flarecapital.com/insight/from-seed-to-hyperscale-in-3-years-how-smarterdx-is-cracking-the-healthcare-ai-code-2/) · [Anterior (AlleyWatch)](https://www.alleywatch.com/2026/03/anterior-health-insurance-clinical-ai-platform-prior-authorization-payer-workflow-administrative-efficiency-abdel-mahmoud/) · [Adonis Series C](https://adonis.io/resources/adonis-raises-40m-series-c-to-equip-healthcare-providers-with-ai-driven-revenue-cycle-operations) · [CodaMetrix review](https://medaiverdict.com/tools/codametrix)
- Security — [Prophet Security pricing](https://www.trustradius.com/products/prophet-security/pricing) · [Intezer vs Prophet](https://intezer.com/guides/soc-as-a-service/prophet-security)
- Chargeback — [Aurai vs Chargeflow](https://aurai.dev/vs/chargeflow)
- CX — [Gorgias AI agent costs (Macha)](https://www.getmacha.com/blog/gorgias-ai-agent-explained) · [Aissist pricing (eesel)](https://www.eesel.ai/blog/aissist-io-pricing) · [Maven AGI pricing (eesel)](https://www.eesel.ai/blog/maven-agi-pricing) · [Forethought reviews (Maven AGI)](https://www.mavenagi.com/blog/forethought-reviews)
- Sales — [AI SDR pricing index (Cleanlist)](https://www.cleanlist.ai/blog/2026-07-23-ai-sdr-pricing-statistics) · [AI SDR pricing (Formanorden)](https://formanorden.com/blog/ai-sdr-pricing/)
- Legal — [EvenUp review (AI Vortex)](https://www.aivortex.io/legal/ai-tools/evenup/)
