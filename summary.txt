# AI Holding Project Summary

Tanggal: 17 Mei 2026 — Update 2  
Owner: Fathur  
Environment: WSL2 + Hermes + Telegram Bot + Online Provider API Key

---

## 1. Tujuan Project

Project ini bertujuan membangun sistem **AI Holding Company** berbasis Hermes, di mana satu Main Assistant dapat mengatur beberapa perusahaan AI agent yang memiliki peran, memory, skill, tool, dan workflow masing-masing.

Target akhirnya:

- Satu bot Telegram sebagai pintu masuk utama.
- Main Assistant sebagai personal assistant dan router.
- Beberapa perusahaan AI agent dengan fokus berbeda.
- Setiap perusahaan memiliki agent/departemen sendiri.
- Task bisa dikirim ke perusahaan atau agent spesifik.
- Memory dan knowledge management tersusun rapi.
- Setup saat ini siap dimigrasikan ke opsi Telegram Topic di masa depan.

---

## 2. Arsitektur Saat Ini

Mode saat ini:

```text
Option A Portable
1 Telegram Bot
↓
Hermes Main Assistant
↓
AI Holding Workspace
↓
Companies / Agents / Tools / Knowledge
```

Workspace utama:

```text
/home/fatur/ai-holding
```

Struktur utama:

```text
ai-holding/
├── MAIN.md
├── SOUL.md
├── AGENTS.md
├── COMMANDS.md
├── MEMORY.md
├── HEARTBEAT.md
├── knowledge/
├── templates/
├── companies/
├── tasks/
├── memory/
├── tools/
└── bin/
```

---

## 3. Perusahaan yang Sudah Dibuat

### 3.1 NexusAI

Path:

```text
/home/fatur/ai-holding/companies/nexusai
```

Tipe:

```text
IT Software Company
```

Fokus:

```text
cloud, DevOps, AI agents, SaaS
```

Agent aktif:

- CEO
- CTO
- Project Manager
- Backend Engineer
- Frontend Engineer
- DevOps Engineer
- QA Engineer
- Technical Writer

Routing contoh:

```text
@nexusai.ceo buatkan strategi produk
@nexusai.cto buatkan arsitektur teknis
@nexusai.backend buatkan desain API
@nexusai.devops buatkan deployment plan
```

---

### 3.2 BrandFlow

Path:

```text
/home/fatur/ai-holding/companies/brandflow
```

Tipe:

```text
Marketing and Content Company
```

Fokus:

```text
branding, content, social media, campaign strategy
```

Agent aktif:

- CEO
- CMO
- Project Manager
- Copywriter
- Social Media
- SEO
- Analytics
- QA
- Writer

Routing contoh:

```text
@brandflow.cmo buatkan strategi campaign
@brandflow.copywriter buatkan caption
@brandflow.social buatkan kalender konten
@brandflow.analytics buatkan KPI campaign
```

---

### 3.3 Crypto Consultant

Path:

```text
/home/fatur/ai-holding/companies/crypto-consultant
```

Tipe:

```text
Crypto Research Company
```

Fokus:

```text
market research, cycle analysis, risk management, reporting
```

Agent aktif:

- CEO
- Research Lead
- Project Manager
- Market Analyst
- Risk Analyst
- Data Analyst
- QA
- Writer

Routing contoh:

```text
@crypto.research cek Fear & Greed Index hari ini
@crypto.market analisis trend BTC
@crypto.risk buatkan risk assessment
@crypto.report buatkan laporan market
```

---

## 4. Fitur yang Sudah Berhasil

### 4.1 Telegram Bot Berjalan

Hermes sudah berhasil berjalan melalui Telegram. Bot dapat menerima pesan dan membalas instruksi user.

### 4.2 Main Assistant Berjalan

Main Assistant sudah dapat:

- Membaca konteks AI Holding.
- Memahami perusahaan milik user.
- Menjawab status semua perusahaan.
- Melakukan routing ke perusahaan tertentu.
- Membaca file di `/home/fatur/ai-holding`.

### 4.3 Routing Perusahaan Berhasil

Format routing perusahaan:

```text
@nexusai <task>
@brandflow <task>
@crypto <task>
```

Contoh berhasil:

```text
@nexusai buatkan 3 ide produk SaaS untuk hackathon Google
```

### 4.4 Direct Agent Routing Berhasil

Format direct agent routing:

```text
@company.agent <task>
```

Contoh:

```text
@nexusai.ceo buatkan strategi produk
@crypto.research cek Fear & Greed Index
```

### 4.5 Company Generator Berhasil

Script generator perusahaan:

```text
/home/fatur/ai-holding/bin/create-company.sh
```

Fungsi:

- Membuat perusahaan baru dari template.
- Mengganti placeholder `{{COMPANY_NAME}}`, `{{COMPANY_TYPE}}`, dan `{{COMPANY_FOCUS}}`.
- Menambahkan perusahaan ke `company-index.jsonl`.

Index perusahaan:

```text
/home/fatur/ai-holding/tasks/company-index.jsonl
```

### 4.6 Tool Crypto Fear & Greed Berhasil

Tool dibuat di:

```text
/home/fatur/ai-holding/tools/fear_greed.py
```

Fungsi:

- Mengambil data Crypto Fear & Greed Index dari Alternative.me API.
- Dipakai oleh Crypto Consultant untuk riset sentimen market.

Contoh command:

```bash
python3 /home/fatur/ai-holding/tools/fear_greed.py
```

### 4.7 Knowledge Management Berhasil

File knowledge berhasil dibuat dan dibaca oleh agent:
- /home/fatur/ai-holding/knowledge/tools/tool-registry.md
- /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
- /home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
- /home/fatur/ai-holding/knowledge/crypto/crypto-research-framework.md
- /home/fatur/ai-holding/memory/global.md

### 4.8 Format Output Standar Berhasil

- @crypto.research sudah mengikuti format 6 lapisan (FACT, SOURCE, TREND, INTERPRET, SCENARIO, RISK NOTE)
- @nexusai.backend sudah menghasilkan desain API terstruktur
- Disclaimer crypto muncul otomatis di setiap output laporan

### 4.9 COMMANDS.md Semua Perusahaan Diperbarui

- Format command diganti dari /slash menjadi @company keyword untuk menghindari konflik antar perusahaan
- Knowledge Loading Rules ditambahkan ke semua COMMANDS.md
- Setiap perusahaan kini punya command set sendiri yang tidak tabrakan:
  - @crypto <keyword>
  - @nexusai <keyword>
  - @brandflow <keyword>

### 4.10 Test Integrasi Berhasil

- @crypto.research berhasil jalankan fear_greed.py dan output format 6 lapisan
- @nexusai.backend berhasil buat desain API terstruktur
- @brandflow.copywriter berhasil buat caption Instagram dengan 2 variasi tone

---

## 5. Masalah yang Ditemukan

### 5.1 Slash Command Tidak Cocok

Format seperti ini tidak cocok:

```text
/nexusai
```

Karena dianggap native command oleh Hermes/Telegram.

Solusi:

Gunakan pseudo-mention:

```text
@nexusai
@brandflow
@crypto
```

### 5.2 Natural Command Perlu Diperkuat

Awalnya pesan:

```text
status semua perusahaan
```

dianggap sebagai perusahaan dunia nyata.

Solusi:

Sudah ditambahkan rule:

- Jika user berkata “perusahaan” tanpa konteks tambahan, artinya perusahaan AI Holding milik Fathur.
- Jika user berkata “perusahaan nyata”, “perusahaan publik”, atau “perusahaan di dunia”, baru artinya real-world company.

### 5.3 Agent Masih Perlu Knowledge Management

Kasus `@crypto.research` menunjukkan bahwa agent bisa routing, tetapi masih bisa bingung jika belum punya:

- SOP riset.
- Tool registry.
- Knowledge framework.
- Aturan kapan memakai tool.
- Format output standar.

### 5.4 Tool Execution Masih Butuh Approval

Hermes meminta approval saat menjalankan script lokal.

Ini aman untuk sekarang.

Ke depan bisa dibuat whitelist terbatas untuk tool read-only seperti:

```text
python3 /home/fatur/ai-holding/tools/fear_greed.py
```

---

## 6. Prinsip Project

Prinsip utama yang digunakan:

```text
Prompt is program.
Context is source code.
Memory is persistent state.
Skill is reusable module.
Tool is external capability.
Human remains supervisor.
```

Knowledge utama saat ini:

```text
/home/fatur/ai-holding/knowledge/karpathy.md
```

---

## 7. Yang Perlu Dilakukan Dalam Waktu Dekat

### Prioritas 1 — Bangun Knowledge Management

Buat struktur knowledge:

```text
/home/fatur/ai-holding/knowledge/
├── core/
├── agent-design/
├── crypto/
├── software/
├── marketing/
├── tools/
└── sop/
```

Tujuan:

- Agent tidak hanya punya role, tapi juga punya cara berpikir.
- Mengurangi jawaban random.
- Membuat agent tahu kapan harus pakai skill, memory, atau tool.

### Prioritas 2 — Buat Tool Registry

Buat file:

```text
/home/fatur/ai-holding/knowledge/tools/tool-registry.md
```

Isi minimal:

```text
Tool: fear_greed.py
Path: /home/fatur/ai-holding/tools/fear_greed.py
Purpose: Fetch Crypto Fear & Greed Index
Used by: @crypto.research, @crypto.market, @crypto.risk
Risk: Low, read-only
Status: Active
```

Tujuan:

- Agent tahu tool apa yang tersedia.
- Agent tidak langsung bilang tidak punya akses real-time.
- Tool bisa dikelola secara rapi.

### Prioritas 3 — Buat SOP Tool Usage

Buat file:

```text
/home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
```

Isi prinsip:

```text
Jika butuh data real-time:
1. Cek tool registry.
2. Jika tool tersedia, gunakan tool.
3. Jika tool tidak tersedia, jelaskan keterbatasan.
4. Jangan langsung bilang tidak bisa sebelum cek tool.
```

### Prioritas 4 — Buat SOP Crypto Research

Buat file:

```text
/home/fatur/ai-holding/knowledge/crypto/crypto-research-framework.md
```

Format standar output crypto:

```text
1. Fact
2. Source
3. Trend
4. Interpretation
5. Scenario
6. Risk note
```

Tujuan:

- Crypto Consultant lebih konsisten.
- Tidak memberi sinyal palsu.
- Selalu memisahkan fakta, interpretasi, dan risiko.

### Prioritas 5 — Buat Memory Rules

Buat file:

```text
/home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
```

Rule:

```text
Catat:
- Task nyata
- Project baru
- Keputusan penting
- Tool baru
- Perubahan arsitektur

Jangan catat:
- Basa-basi
- Ucapan terima kasih
- Klarifikasi ringan
- Chat santai
- Jawaban tanpa keputusan
```

### Prioritas 6 — Buat Task Logger JSONL

Target:

Ketika user memberi task penting, task dicatat ke:

```text
/home/fatur/ai-holding/companies/<company>/tasks/inbox.jsonl
```

Contoh:

```json
{"id":"NX-001","company":"nexusai","agent":"ceo","task":"Buat strategi produk SmartBill Pro","priority":"HIGH","status":"NEW","created_at":"2026-05-17"}
```

Namun task logger harus memakai filter agar chat basa-basi tidak dicatat.

### Prioritas 7 — Update Template Perusahaan

Karena direct agent routing sudah ditambahkan ke perusahaan yang ada, template juga harus diperbarui:

```text
/home/fatur/ai-holding/templates/company/AGENTS.md
/home/fatur/ai-holding/templates/company/COMMANDS.md
```

Tujuannya:

- Perusahaan baru otomatis punya direct agent routing.
- Tidak perlu update manual setelah create-company.

### Prioritas 8 — Perkuat Service Hermes

Hermes sekarang sudah berjalan sebagai user service:

```text
hermes-gateway.service
```

Command penting:

```bash
systemctl --user status hermes-gateway
systemctl --user restart hermes-gateway
journalctl --user -u hermes-gateway -f
```

Perlu dicek:

- Warning service sudah bersih.
- Tidak ada proses Hermes dobel.
- Restart service membaca konfigurasi terbaru.

---

## 8. Roadmap Pendek

### Tahap A — Stabilkan Main Assistant

- Pastikan natural command stabil.
- Pastikan `status semua perusahaan` selalu memakai AI Holding context.
- Pastikan pseudo-mention routing konsisten.
- Pastikan direct agent routing konsisten.

### Tahap B — Bangun Knowledge Management

- Buat folder knowledge yang rapi.
- Buat SOP per domain.
- Buat tool registry.
- Buat memory rules.

### Tahap C — Buat Task Logger

- Buat format task JSONL.
- Buat rule pencatatan task.
- Hindari mencatat basa-basi.
- Simpan task ke inbox perusahaan.

### Tahap D — Tambah Tool

Tool awal:

- Fear & Greed Index.
- BTC price fetcher.
- News sentiment fetcher.
- Google Trends jika memungkinkan.
- Simple web research helper.

### Tahap E — Siapkan Migrasi Option C

Nanti jika sudah stabil:

```text
Telegram Group / Forum Topics
├── Main Assistant
├── NexusAI
├── BrandFlow
└── Crypto Consultant
```

Mapping folder:

```text
Topic NexusAI → /home/fatur/ai-holding/companies/nexusai
Topic BrandFlow → /home/fatur/ai-holding/companies/brandflow
Topic Crypto Consultant → /home/fatur/ai-holding/companies/crypto-consultant
```

---

## 9. Status Terakhir

Status project:

```text
Usable Prototype
```

Yang sudah siap:

```text
- Hermes Telegram bot
- Main Assistant
- AI Holding workspace
- Company generator
- 3 perusahaan awal (NexusAI, BrandFlow, Crypto Consultant)
- Direct agent routing (@company.agent)
- Crypto Fear & Greed tool
- Knowledge management (5 file knowledge)
- COMMANDS.md per perusahaan dengan namespace @company keyword
- Test integrasi semua perusahaan berhasil
```

```text
- SOP software development lengkap (knowledge/software/)
- SOP marketing lengkap (knowledge/marketing/)
- Task logger JSONL
- Template update untuk direct routing
- Whitelist tool read-only
- btc_price.py (PLANNED)
- news_sentiment.py (PLANNED)
```

---

## 10. Next Immediate Action

Langkah paling dekat yang harus dilakukan:

```text
1. Buat folder knowledge management.
2. Buat tool-registry.md.
3. Buat tool-use-rules.md.
4. Buat crypto-research-framework.md.
5. Buat memory-rules.md.
6. Update Main Assistant agar membaca knowledge sesuai kebutuhan.
```

Setelah itu, baru lanjut ke:

```text
Task Logger JSONL
```

---

## 11. Prompt untuk Melanjutkan Setup

Gunakan prompt ini ke Hermes jika ingin melanjutkan dari ringkasan:

```text
Baca /home/fatur/ai-holding/summary.md lalu lanjutkan setup dari bagian Next Immediate Action. Kerjakan pelan-pelan, satu tahap dulu. Jangan mengubah file penting tanpa backup.
```
