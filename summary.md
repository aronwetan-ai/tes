# AI Holding Project Summary

Tanggal: 17 Mei 2026 — Update 8
Owner: Fathur
Environment: WSL2 + Hermes + Telegram Bot + Online Provider API Key
Repository: aronwetan-ai/tes

---

## Update 8 — Task Logger JSONL Implementation (17 Mei 2026)

Branch: `feat/task-logger-jsonl`

### A. Tujuan

Sebelum Update 8:
- Schema task sudah didefinisi di `companies/nexusai/skills/automation/SKILL.md`, tapi **tidak ada implementasi**.
- 4 file JSONL per company (`inbox.jsonl`, `logs.jsonl`, `messages.jsonl`, `recap.jsonl`) **kosong semua**.
- Tidak ada cara konsisten untuk: buat task baru, transition status, list/filter, hand-off antar agent.
- SKILL.md menyebut struktur 3-file move (`inbox / active / done`) yang **tidak match** reality (4-file: inbox/logs/messages/recap).

Update 8 menyelesaikan empat hal:
1. **Implementasi production scripts** (Python) untuk full task lifecycle.
2. **Reconcile dokumentasi** dengan reality file structure.
3. **Tulis authoritative rules** untuk schema, state machine, filter rules, anti-pattern.
4. **Wire ke COMMANDS.md** sebagai natural commands Main Assistant.

### B. Yang Dieksekusi

**1. Production scripts di `bin/` (5 executable + 1 library):**

| File | Peran | Risk |
|---|---|---|
| `bin/log_task.py` | Buat task baru (auto ID `T###` per-company, validasi schema, append + audit) | Medium |
| `bin/update_task.py` | Transition status (state machine validated, audit) | Medium |
| `bin/list_tasks.py` | Filter & list (by company, agent, status, priority; format table/json/jsonl) | Low |
| `bin/log_message.py` | Append agent-to-agent durable message | Medium |
| `bin/log-task.sh` | Wrapper bash 3-arg ergonomis untuk `log_task.py` | Medium |
| `bin/task_logger.py` | Shared library — schema, validation, atomic I/O. Tidak dipanggil langsung. | N/A |

Karakteristik script:
- Read `AI_HOLDING_HOME` env var; default fallback walk-up dari script location.
- Append idempoten; `inbox.jsonl` rewrite atomic via `<file>.tmp` + `os.replace()`.
- `logs.jsonl` strict append-only — audit trail tidak pernah dimutasi.
- Validasi schema reject task < 8 char (filter rules: no basa-basi).
- State machine guard: transisi tidak valid (mis. `DONE → NEW`) ditolak dengan exit 2.
- Exit code 0 = OK, 2 = schema/transition/argument error, 3 = I/O error.

**2. Authoritative rules** — `knowledge/agent-design/task-logger-rules.md`:
- Tujuan + boundary task logger (apa yang masuk vs tidak).
- Schema lengkap untuk 3 entry type (task, audit, message).
- State machine + diagram transisi yang boleh.
- Filter rules — list eksplisit apa yang DILOG dan apa yang TIDAK.
- 3 workflow contoh end-to-end (delegate, recap, failed→retry).
- Anti-pattern + maintenance rules.
- Hubungan dengan memory (kapan task vs kapan memory).

**3. SKILL.md reconciliation** — `companies/nexusai/skills/automation/SKILL.md`:
- Tambah section "File Structure (Authoritative)" yang reflect reality 4-file.
- Tambah section "Implementasi (Production Scripts)" dengan tabel 6 script + workflow contoh.
- State machine diperjelas; DONE / CANCELLED disebut terminal eksplisit.

**4. Tool registry** — `knowledge/tools/tool-registry.md` versi 1.1:
- 5 entry baru: TOOL-005 sampai TOOL-009 (4 script + 1 library).
- Detail command, purpose, risk, status untuk tiap script.

**5. COMMANDS.md (root)** — natural commands baru:
- `cek task aktif <company>` → backed by `list_tasks.py --active-only`.
- `cek task <company> status <STATUS>` → filter by status.
- `log task untuk @company.agent: <desc> [priority HIGH]` → backed by `log_task.py`.
- `mulai task <ID>`, `tutup task <ID> sebagai DONE`, `batalkan task <ID>` → state transitions.
- `kirim pesan dari @x ke @y: <msg> [ref T001]` → backed by `log_message.py`.

**6. Memory updates**:
- `MEMORY.md` (root) versi 2.1: tambah strategic decision #9 (Task Logger model), update folder structure dengan 5 script baru di `bin/`.
- `memory/global.md` versi 2.1: 4 `[DECISION]` baru, 4 `[ARCH]` baru, 7 `[TOOL]` baru (script + library + wrapper), 2 `[NOTE]` updated dengan status terbaru.

### C. Smoke Test (12 cases lulus semua)

```
1. create task auto ID                    → OK (T001)
2. bash wrapper 3-arg                     → OK (T002)
3. create with --context JSON             → OK (T001 crypto-consultant, ID space per-company)
4. validation reject task <8 char         → exit 2 (filter rules enforced)
5. list tasks (table format)              → OK
6. NEW → IN_PROGRESS → DONE                → OK (history captured in context)
7. illegal transition DONE → NEW           → exit 2 (state machine guard)
8. filter --active-only                   → terminal hidden
9. filter --status DONE                   → match only DONE
10. log_message with --ref-task            → OK (durable hand-off)
11. update nonexistent task ID             → exit 2 (not found)
12. format jsonl machine-readable          → OK (single-line JSON each)
```

Audit log captured: 2 CREATE events + 2 UPDATE events dengan `prev_status`, `new_status`, `actor`, `at`, `note`. Test data direset ke kosong post-test.

### D. Total File Changes

```
Created:  bin/task_logger.py          (shared library, 350+ lines)
Created:  bin/log_task.py             (CLI create)
Created:  bin/update_task.py          (CLI transition)
Created:  bin/list_tasks.py           (CLI filter & list)
Created:  bin/log_message.py          (CLI agent-to-agent message)
Created:  bin/log-task.sh             (bash wrapper)
Created:  knowledge/agent-design/task-logger-rules.md  (authoritative rules)
Modified: companies/nexusai/skills/automation/SKILL.md (reconciled with reality)
Modified: knowledge/tools/tool-registry.md            (5 entries: TOOL-005..009)
Modified: COMMANDS.md                  (natural commands for task logger)
Modified: MEMORY.md                    (strategic decision #9 + folder layout)
Modified: memory/global.md             (4 DECISION + 4 ARCH + 7 TOOL + 2 NOTE)
Modified: summary.md                   (this section)
```

7 file dibuat baru, 6 file dimodifikasi, 0 file dihapus.

### E. Dampak Operasional

Sebelum:
- Task antar agent hanya hidup di chat history — tidak resumable.
- Tidak ada audit trail — kalau ada dispute "task ini sudah selesai apa belum?", tidak ada source of truth.
- Hand-off antar agent informal — risiko terlewat.
- Schema task didefinisi tapi tidak di-enforce.

Sesudah:
- Task adalah **first-class durable entity** dengan ID, state, history, audit trail.
- State machine eksplisit & divalidasi script — tidak mungkin transisi liar.
- Audit trail di `logs.jsonl` immutable — siapa pindah status apa, kapan, dengan note apa.
- Hand-off via `messages.jsonl` durable — agent berikutnya melihatnya saat session start.
- Filter rules di-enforce by validation (min 8 char task; min 4 char message).
- Resumable: kalau session crash, state ada di file — agent berikutnya bisa lanjut tanpa kehilangan konteks.

### F. Yang Belum Selesai (untuk PR berikutnya — Tahap G)

1. **Tools tambahan** — `tools/btc_price.py` (CoinGecko), `tools/news_sentiment.py`. Sudah PLANNED di registry.
2. **Tier 3 SOULs untuk role sisa** (PM, QA, Writer, Frontend, SEO, Analytics, Data, Report) — on-demand saat Fathur mulai sering pakai.
3. **Whitelist tool read-only di Hermes** (Hermes hardening — supaya `fear_greed.py` + `list_tasks.py` bisa dipanggil tanpa konfirmasi).
4. **Recap Manager** — script yang otomatis generate `recap.jsonl` dari `inbox.jsonl` + `logs.jsonl`.
5. **Archival workflow** — pindah terminal tasks (`DONE`/`CANCELLED`) yang > 30 hari ke `tasks/archive/<YYYY-MM>.jsonl`.

---

## Update 7 — Fix Memory Reference + Restructure Memory Files (17 Mei 2026)

Branch: `chore/fix-memory-references`

### A. Tujuan

Sebelum Update 7:
- `MAIN.md` line 5 bilang baca `MEMORY.md` (root, format Update 2 era).
- `AGENTS.md` line 84 bilang baca `memory/global.md` (tagged log, post Update 3).
- Dua file memory dengan **peran tidak jelas** — overlap, duplikat, atau lengkap-lengkapan tidak terdefinisi.
- Company `MEMORY.md` masih boilerplate "None yet" tanpa link ke Tier 2 SOUL atau Update 5/6 changes.
- `memory-rules.md` Versi 1.0 belum reflect dual-file structure.

### B. Yang Dieksekusi

**1. Memory split eksplisit ditetapkan** (5 file di-rewrite):

| File | Sifat | Format |
|---|---|---|
| `MEMORY.md` (root) | Strategic / narrative — big picture | Paragraphs, struktur tabel |
| `memory/global.md` | Operational / tagged log — day-to-day | `[DECISION]`, `[TASK]`, `[ARCH]`, `[TOOL]`, `[INSIGHT]`, `[NOTE]` |
| `companies/<co>/MEMORY.md` × 3 | Company-scoped — both narrative + tagged | Mixed; identity narrative + tagged log |

**2. `MAIN.md` rewritten** untuk eksplisit baca **kedua** memory files saat session start (dengan urutan + alasan jelas).

**3. `AGENTS.md` rewritten** dengan section "Memory Reference Rules" yang explicit memisahkan strategic vs operational, plus update "Knowledge Reference Per Domain" agar konsisten dengan Tier 2/3 SOUL hierarchy + skill specialization (Update 6).

**4. `memory-rules.md` Versi 2.0**:
- Section "Struktur Memory di Holding" baru — 3 level scope (holding-level, company-level, agent-level).
- Tabel "Kapan Pakai File Mana" — decision tree write target.
- Section "Anti-Pattern" baru — list anti-pattern yang harus dihindari.

**5. Template `templates/company/MEMORY.md` rewritten**:
- Sekarang inherit dari Tier 2 SOUL pattern.
- Tambah section Active Projects, Architecture Notes, Cross-Company Collaboration Log.
- Tambah panduan format pendek vs panjang.
- Tambah anti-pattern reminder.

**6. Tiap company `MEMORY.md` rewritten** dengan reflect:
- Tier 2 SOUL inheritance.
- Update 5 role baru (security, ml, designer, community, onchain, macro).
- Update 6 skill specialization.
- Boundary #4 amplification untuk role rawan.
- Cross-company collaboration log section.

### C. Dampak Operasional

Sebelum:
- Agent baca `MEMORY.md` ATAU `memory/global.md` — tidak jelas which one when.
- Information yang sama bisa di kedua file dengan format beda.
- Strategic decision bisa hilang di tengah operational log.
- Company MEMORY.md generic, tidak link ke SOUL/skill changes.

Sesudah:
- Eksplisit: `MEMORY.md` = strategic narrative; `memory/global.md` = operational tagged log. Both read on session start.
- Format berbeda mencegah duplikasi: paragraph for narrative, tags for operational.
- Strategic decisions punya rumah jelas (root MEMORY.md), operational log punya rumah jelas (global.md), company-scoped punya rumah jelas (per-company MEMORY.md).
- Setiap company MEMORY.md sekarang menjadi snapshot active state per perusahaan, bukan boilerplate.

### D. Total File Changes

```
Modified: MAIN.md
Modified: AGENTS.md
Modified: MEMORY.md (root) — full rewrite, narrative format
Modified: memory/global.md — full rewrite, operational tagged log format
Modified: knowledge/agent-design/memory-rules.md — Versi 2.0
Modified: templates/company/MEMORY.md — Tier 2 inheritance pattern
Modified: companies/nexusai/MEMORY.md
Modified: companies/brandflow/MEMORY.md
Modified: companies/crypto-consultant/MEMORY.md
Modified: summary.md — Update 7 section
```

9 file dimodifikasi, 0 file dihapus, 0 file dibuat baru.

### E. Yang Belum Selesai (untuk PR berikutnya)

1. **Task Logger JSONL implementation** — schema sudah didefinisi di `companies/nexusai/skills/automation/SKILL.md`, tinggal writer + filter.
2. **Tools tambahan** — `btc_price.py`, `news_sentiment.py`.
3. **Tier 3 untuk role sisa** — PM, QA, Writer, Frontend, SEO, Analytics, Data, Report. On-demand.
4. **Whitelist tool read-only** di Hermes (Hermes hardening).

---

## Update 6 — Specialize Skill Files Per Company (17 Mei 2026)

Branch: `feat/specialize-skills`

### A. Tujuan

Sebelum Update 6:
- Setiap perusahaan punya 8 folder skill yang **identik isinya** (boilerplate dari template lama).
- Skill yang tidak relevan tetap ada (mis. `devops/` di BrandFlow, `coding/` di Crypto Consultant).
- Skill files cuma 5-baris generic — tidak bawa identitas perusahaan, tidak terhubung ke Tier 2/3 SOUL atau knowledge SOP.

Update 6 menyelesaikan tiga hal:
1. **Buang skill folder yang tidak relevan** per perusahaan.
2. **Tulis ulang skill yang relevan** dengan konten spesifik per perusahaan, terhubung ke Tier 2/3 SOUL + knowledge SOP.
3. **Tambah skill baru** yang dibutuhkan (mengikuti role baru dari Update 5).

### B. Skill Set Final Per Perusahaan

#### NexusAI (7 skills, dari 8 generic → 7 specialized)
```
coding/        — Backend / API / database / refactor (NexusAI flavor)
devops/        — Deploy / CI/CD / observability / incident
security/      — Threat model + auth + OPSEC for offensive work (NEW)
ml-agent/      — AI agent design / prompts / evals (Karpathy-aligned, NEW)
automation/    — JSONL pipelines / scripts / multi-agent comm
qa/            — Code review / test plan / acceptance criteria
uiux/          — Product UX (SaaS dashboards, dev tools, agent surfaces)
```
Removed: content, research, business (tidak fit untuk engineering company).

#### BrandFlow (7 skills, dari 8 generic → 7 specialized)
```
content/       — Copy / hooks / captions / articles (BrandFlow voice)
design/        — Visual concept / layout / type spec (NEW)
community/     — Real-time DM/comment drafts (NEW)
seo/           — Keyword research / on-page SEO (NEW)
research/      — Audience / competitive / market research (commercial intel)
automation/    — Editorial pipeline / scheduler integration / brief routing
qa/            — Brand voice + accuracy + Boundary #4 review
```
Removed: coding, devops, business, uiux (tidak fit untuk marketing company).

#### Crypto Consultant (7 skills, dari 8 generic → 7 specialized)
```
research/      — Synthesis layer + 6-layer format
market-analysis/ — Technical / structure / cycle / dominance (NEW)
onchain/       — Wallet flows / smart money / supply (NEW)
macro/         — DXY / Fed / M2 / equity correlation (NEW)
risk/          — Drawdown / sizing / tail / counterparty (NEW)
reporting/     — Final assembly + mandatory disclaimer (NEW)
qa/            — Methodology + fact-check + Boundary #4 enforcement
```
Removed: coding, devops, content, automation, uiux, business (tidak fit untuk research company).

### C. Struktur Konsisten Tiap SKILL.md

Setiap SKILL.md baru pakai struktur 9-section:

1. Front-matter YAML (name, description, company, used_by)
2. When to Use (concrete trigger)
3. Default Approach / Process
4. Rules (numbered, non-negotiable)
5. Output Format (structured templates per task type)
6. Channel / Domain defaults (when relevant)
7. Cross-Skill / Cross-Agent Routing
8. What This Skill Does NOT Cover
9. Reference

### D. Index Files Baru (3 file)

```
companies/nexusai/SKILLS.md
companies/brandflow/SKILLS.md
companies/crypto-consultant/SKILLS.md
```

Setiap SKILLS.md adalah index resmi: daftar active skills + primary users + skill yang dihapus + alasan + cara nambah skill baru. Berfungsi sebagai pintu masuk ke skill folder.

### E. Template Update

`templates/company/SKILLS.md` ditulis ulang untuk panduan operator setelah `create-company.sh`:
- Cara review default skill set.
- Cara hapus yang tidak relevan.
- Cara specialize yang relevan.
- Cara add skill baru.
- Format front-matter standar.

### F. Dampak Operasional

Sebelum:
- `@brandflow.copywriter` baca `skills/content/SKILL.md` → dapat 5 baris generic, tidak match BrandFlow voice.
- `@nexusai.security` (role baru) tidak punya skill khusus.
- `@crypto.market` baca skill yang sama dengan `@nexusai.coding` (literally identik).

Sesudah:
- Setiap skill membawa **company DNA**: voice, framework, rules, output format spesifik domain.
- Skill terhubung ke Tier 3 SOUL (mention "Inherits", `used_by`).
- Skill terhubung ke knowledge SOP (referensi explicit).
- Cross-skill routing jelas — tidak ada overlap antara `skills/uiux` di NexusAI (product) vs `skills/design` di BrandFlow (marketing).

### G. Total File Changes

```
Removed:  16 generic SKILL.md (skills folders dihapus)
Added:    21 specialized SKILL.md (7 per company × 3)
Added:    3 SKILLS.md index files (per company)
Modified: 1 templates/company/SKILLS.md (operator guide)
```

### H. Yang Belum Selesai (untuk PR berikutnya)

1. **Fix memory reference** — `MAIN.md` baca `MEMORY.md`, `AGENTS.md` baca `memory/global.md`. Klarifikasi peran + update root MEMORY.md.
2. **Task Logger JSONL** — schema + writer + filter (skill `automation` di NexusAI sudah definisi schema, tinggal implementasi).
3. **Tools tambahan** — btc_price.py, news_sentiment.py.
4. **Tier 3 untuk role sisa** (PM, QA, Writer, Frontend, SEO, Analytics, Data, Report) — on-demand.

---

## Update 5 — Tier 3 Agent SOULs + New Specialist Roles (17 Mei 2026)

Branch: `feat/tier3-agent-souls`

### A. Tujuan

Sebelum Update 5:
- Tier 0/1/2 SOUL sudah ada, tapi setiap **agent individu** masih generic (warisan boilerplate).
- `@nexusai.backend` dan `@nexusai.frontend` punya jiwa yang sama persis (cuma role-nya beda).
- Beberapa role kritikal **belum ada** sama sekali: Security di NexusAI (padahal SaaS), Designer di BrandFlow, On-chain Analyst di Crypto.

Update 5 menyelesaikan dua hal sekaligus:
1. **Tier 3 SOUL** untuk 18 agent (6 per perusahaan, role yang paling sering dipanggil).
2. **Tambahan 6 role baru** untuk mengisi gap fungsional yang teridentifikasi dari analisis.

### B. Role Baru yang Ditambahkan

#### NexusAI (+2 role: 8 → 10 agent)
| Role | Slug | Alasan ditambahkan |
|---|---|---|
| Security Engineer | `@nexusai.security` | SaaS tanpa security = breach waiting to happen. Threat modeling, auth, OPSEC tidak fit ke backend atau devops. Juga handle offensive enablement (OPSEC untuk automation/multi-account work Fathur). |
| AI / ML Engineer | `@nexusai.ml` | Fokus perusahaan menyebut "AI agents". Tanpa role ini, agent design jatuh ke backend yang tidak punya konteks ML / prompt engineering / eval. |

#### BrandFlow (+2 role: 9 → 11 agent)
| Role | Slug | Alasan ditambahkan |
|---|---|---|
| Designer | `@brandflow.designer` | Marketing tanpa visual = incomplete. Copywriter handle copy, social handle calendar, tapi tidak ada yang own visual concept / layout / type / color spec. |
| Community Manager | `@brandflow.community` | Social plan kalender; tidak handle real-time DM, comments, mentions, sentiment monitoring, crisis early warning. Skill berbeda. |

#### Crypto Consultant (+2 role: 8 → 10 agent)
| Role | Slug | Alasan ditambahkan |
|---|---|---|
| On-chain Analyst | `@crypto.onchain` | `@crypto.data` generik (struktur data umum). On-chain itu skill spesifik: wallet flows, exchange flows, whale activity, smart money tracking, supply dynamics. |
| Macro Analyst | `@crypto.macro` | Cycle analysis butuh konteks DXY, Fed, M2, yields, equities — tidak fit ke market analyst yang fokus teknikal. Macro liquidity adalah primary cycle driver. |

### C. Tier 3 SOULs yang Dibuat (18 file)

Struktur: `companies/<company>/agents/<agent>.md`

```
NexusAI (6):
  agents/ceo.md, agents/cto.md, agents/backend.md
  agents/devops.md, agents/security.md (NEW), agents/ml.md (NEW)

BrandFlow (6):
  agents/ceo.md, agents/cmo.md, agents/copywriter.md
  agents/social.md, agents/designer.md (NEW), agents/community.md (NEW)

Crypto Consultant (6):
  agents/ceo.md, agents/research.md, agents/market.md
  agents/risk.md, agents/onchain.md (NEW), agents/macro.md (NEW)
```

Role lain (PM, QA, Writer, Frontend, SEO, Analytics, Data, Report) **belum** punya Tier 3 SOUL — mereka tetap inherit dari Tier 2 SOUL perusahaan dan SOP knowledge yang relevan. Ini standar; Tier 3 dibuat ketika role butuh spesifisitas tambahan.

### D. Struktur Konsisten Tiap Tier 3 SOUL

Setiap Tier 3 SOUL punya struktur 8-10 section:

1. Inheritance Note (eksplisit warisi Root SOUL → Company SOUL)
2. Identity (siapa agent ini, siapa BUKAN)
3. Voice (cara bicara, default style)
4. Specific Responsibilities (tugas konkret, bukan generic)
5. Decision Authority (boleh decide vs harus escalate)
6. Default Approach / Process (langkah default per task)
7. Output Format (structured templates per task type)
8. What I Do NOT Do (anti-pattern eksplisit)
9. Cross-Agent Routing (kapan delegate ke agent lain)
10. (Optional) Boundary reminders untuk role rawan (security, community, onchain, risk)

### E. Update File Lain

- **3× AGENTS.md** (per company) — daftar role lengkap, direct routing block dengan role baru, knowledge loading order updated, safety rules.
- **3× COMMANDS.md** (per company) — command baru untuk role baru, knowledge loading rule updated.
- **3× IDENTITY.md** (per company) — refresh active departments list, tambah inheritance note.

### F. Dampak Operasional

Sebelum:
- `@nexusai.backend buatkan API`, `@nexusai.frontend buatkan UI` → kedua agent jawab dengan persona yang sama.
- `@brandflow.copywriter` jawab dengan persona generic, sama dengan `@brandflow.cmo`.
- `@crypto.market` analisis chart pakai bahasa generic, tidak ada cycle awareness.
- Tidak ada agent untuk security review, designer brief, community management, on-chain forensics, atau macro overlay.

Sesudah:
- Setiap agent punya **voice, principles, decision authority, output format** yang khas peran.
- 6 role baru mengisi gap fungsional — tidak lagi ada task yang "jatuh" ke role yang salah.
- Boundary #4 diamplify spesifik di role rawan (community, onchain, risk).

### G. Yang Belum Selesai (untuk PR berikutnya)

1. **Tier 3 untuk role sisanya** — PM, QA, Writer, Frontend, SEO, Analytics, Data, Report. Bisa ditambahkan saat Fathur mulai sering pakai role-role ini dan butuh spesifisitas.
2. **Skill files specialization** — 23 dari 24 SKILL.md masih boilerplate. Sebaiknya hapus skill folder yang tidak relevan per perusahaan (mis. devops di brandflow).
3. **Fix memory reference** + update root MEMORY.md.
4. **Task Logger JSONL** — schema + writer + filter.
5. **Tools tambahan** — btc_price.py, news_sentiment.py.

---

## Update 4 — Tier 2 Company SOULs (17 Mei 2026)

Branch: `feat/tier2-company-souls`

### A. Tujuan

Sebelum Update 4, ketiga `companies/*/SOUL.md` masih copy-paste boilerplate dari template lama — agent NexusAI, BrandFlow, dan Crypto Consultant punya "jiwa" yang identik. Update ini memberi setiap perusahaan **kepribadian, prinsip, dan decision authority** yang spesifik untuk domainnya.

### B. Yang Dieksekusi

3 file SOUL ditulis ulang dari nol dengan struktur Tier-2 yang konsisten:

```
companies/nexusai/SOUL.md
  Nuansa: engineering-precise, pragmatic, zero fluff.
  - 7 engineering principles (working code beats perfect, boring tech, dst).
  - 7-step operating behavior untuk setiap task.
  - Decision authority eksplisit: CEO / CTO / PM / Specialist (boleh decide vs harus escalate).
  - Cross-company collaboration: kapan loop in BrandFlow / Crypto.

companies/brandflow/SOUL.md
  Nuansa: creative-confident, audience-aware, sharp copy, slightly playful.
  - 7 marketing principles (audience first, hook earns the read, dst).
  - 6-step operating behavior dengan emphasis pada KPI.
  - Decision authority + Boundary #4 reminder (BrandFlow paling sering brush dengan rule "tidak bicara atas nama Fathur di publik").
  - Memory discipline: hanya simpan campaign decisions, bukan setiap draft.

companies/crypto-consultant/SOUL.md
  Nuansa: analyst-cautious, data-first, skeptical, bedakan fakta vs opini.
  - 7 research principles (fact > interpretation > scenario, no determinism, source everything).
  - Decision authority + Boundary #4 amplified (financial advice posture).
  - Wajib disclaimer pada @crypto.report output.
  - Time-stamp & source citation non-negotiable.
```

### C. Struktur Konsisten Tiap SOUL

Setiap Tier-2 SOUL punya 14 section dengan urutan sama:

1. Inheritance Note (eksplisit warisi Root SOUL)
2. Identity (siapa perusahaan ini, siapa BUKAN)
3. Culture & Tone (bagaimana suara perusahaan, bagaimana TIDAK)
4. Principles (non-negotiable)
5. Operating Behavior (langkah default per task)
6. Decision Authority (boleh decide vs harus escalate ke Fathur)
7. Boundary Reminder (jika domain rawan)
8. Memory Discipline
9. Tool Discipline
10. Knowledge Loading (mandatory file order)
11. What This Company Is NOT
12. Cross-Company Collaboration
13. Loyalty Reminder (diulang agar tidak drift)

### D. Dampak Operasional

Sebelum:
- @nexusai.ceo dan @brandflow.ceo dan @crypto.ceo menjawab dengan tone yang sama.
- Tidak ada kejelasan kapan CEO boleh decide sendiri vs harus tanya Fathur.
- Tidak ada kejelasan boundary spesifik per domain (mis. financial advice di Crypto).

Sesudah:
- Setiap perusahaan punya tone, principles, dan rules sendiri yang spesifik.
- Decision authority terstruktur: CEO / VP / PM / Specialist masing-masing tahu otoritas dan escalation path.
- Boundary #4 dari Root SOUL diamplify khusus di BrandFlow & Crypto (domain paling rawan).
- Cross-company collaboration jelas: NexusAI tidak bikin copy, BrandFlow tidak invent fakta crypto, dst.

### E. Yang Belum Selesai (untuk PR berikutnya)

1. **Tier 3 Agent SOULs** — minimal untuk role utama (CEO, CTO/CMO/Research, dan 1 spesialis per company).
2. **Specialize skill files** — 23 dari 24 SKILL.md masih boilerplate.
3. **Fix memory reference inkonsistensi** + update root MEMORY.md.
4. **Task Logger JSONL** — schema + writer + filter.
5. **Tools tambahan** — btc_price.py, news_sentiment.py.

---

## Update 3 — Audit Repository & Quick Wins (17 Mei 2026)

Section ini ditambahkan setelah audit menyeluruh terhadap repository dan eksekusi
"Quick Wins" pada branch `chore/quickwins-cleanup-and-knowledge-fix`.

### A. Hasil Audit Repository

Audit menyoroti tujuh area dengan status berbeda:

| Area                       | Status sebelum audit | Catatan |
|----------------------------|----------------------|---------|
| Top-level governance       | 95% baik             | SOUL.md, MAIN_SOUL.md, MAIN.md sudah Tier 0/1 yang benar |
| Knowledge (root)           | 60% baik             | Hanya 3 dari 7 folder yang dirujuk benar-benar ada |
| SOUL hierarchy             | 50% baik             | Tier 0/1 selesai; Tier 2/3 masih boilerplate generik |
| Companies (struktur)       | 90% baik             | Struktur folder lengkap |
| Companies (depth)          | 30% baik             | Isi 80% generik copy-paste dari template |
| Templates                  | 40% baik             | Belum reflect Tier-2 design + tidak ada Direct Routing |
| Skills                     | 20% baik             | 23 dari 24 SKILL.md identik (boilerplate) |
| Tools                      | 25% baik             | 1 active dari 4 entry registry |
| Task logger                | 5% baik              | Semua JSONL kosong, tidak ada writer |
| Kebersihan repo            | 70% baik             | 13 file sampah (.bak + Zone.Identifier + duplikat) |

### B. Gap Kritis yang Ditemukan

1. **Broken knowledge references.** `MAIN.md`, `AGENTS.md`, `companies/nexusai/COMMANDS.md`,
   dan `companies/brandflow/COMMANDS.md` menunjuk ke folder/file yang belum dibuat:
   - `knowledge/core/`
   - `knowledge/software/software-development-sop.md`
   - `knowledge/marketing/marketing-sop.md`
   - `knowledge/sop/`
2. **Template tidak reflect desain terbaru.** Generator perusahaan akan menghasilkan
   company tanpa Direct Agent Routing, tanpa Knowledge Loading rules, dan tanpa
   inheritance dari Root SOUL.
3. **File sampah Windows + backup.** 9 file `.bak/.bak2/.bak3`, 2 Zone.Identifier
   stream, dan 1 duplikat `summary.txt`.
4. **Skill files generik.** 23 dari 24 file SKILL.md identik dengan template — agent
   tidak benar-benar mendapat skill yang spesifik untuk perannya.
5. **Tier 2 dan Tier 3 SOUL belum ada.** Ketiga `companies/*/SOUL.md` masih copy-paste
   generik, tidak menyebut inheritance dari Root SOUL.

### C. Quick Wins yang Sudah Dieksekusi

Branch: `chore/quickwins-cleanup-and-knowledge-fix`

#### C.1 Cleanup (13 file dihapus)

```
SOUL.md.bak
COMMANDS.md.bak
summary.txt
summary.md:Zone.Identifier
summary - Copy.md:Zone.Identifier
companies/brandflow/AGENTS.md.bak
companies/nexusai/AGENTS.md.bak
companies/crypto-consultant/AGENTS.md.bak
companies/crypto-consultant/AGENTS.md.bak2
companies/crypto-consultant/AGENTS.md.bak3
companies/crypto-consultant/MEMORY.md.bak
companies/crypto-consultant/TOOLS.md.bak
companies/crypto-consultant/skills/research/SKILL.md.bak
```

#### C.2 Knowledge Files Baru (4 file)

```
knowledge/core/principles.md
  → Cara berpikir umum + hierarchy SOUL/knowledge.
  → Wajib dibaca oleh semua agent saat sesi baru.

knowledge/software/software-development-sop.md
  → SOP untuk @nexusai.* — API design, code review, deployment,
    output formats, internal routing.

knowledge/marketing/marketing-sop.md
  → SOP untuk @brandflow.* — copywriting framework (AIDA/PAS/BAB),
    hook patterns, per-channel standards, KPI tables.

knowledge/sop/README.md
  → Skill library reusable lintas perusahaan, planned skill list.
```

Setelah perubahan ini, semua referensi dari `MAIN.md`, `AGENTS.md`, dan
`companies/*/COMMANDS.md` mengarah ke file yang **ada**.

#### C.3 Template Update (3 file)

```
templates/company/AGENTS.md (rewritten)
  → Tambah Core Roles dengan deskripsi lebih jelas.
  → Tambah Direct Agent Routing block dengan format @{{COMPANY_SLUG}}.<agent>.
  → Tambah Knowledge Loading block (7 file mandatory).
  → Tambah Memory Rules + Safety Rules.
  → Tambah catatan untuk operator setelah create-company.

templates/company/COMMANDS.md (rewritten)
  → Replace /slash commands dengan @company keyword namespacing.
  → Tambah Knowledge Loading Rules block.
  → Tambah Direct Agent Routing block.
  → Tambah Domain Commands placeholder yang tinggal di-customize.

templates/company/SOUL.md (rewritten - Tier 2 design)
  → Header eksplisit: "Inherits Root SOUL".
  → Identity tied to {{COMPANY_NAME}} + {{COMPANY_TYPE}} + {{COMPANY_FOCUS}}.
  → Section Culture & Tone (default + customization guidance).
  → Operating Behavior 6-step flow.
  → Decision Authority — CEO bisa decide vs must escalate ke Fathur.
  → Memory & Tool discipline pointing to root knowledge files.
  → Loyalty Reminder repeated supaya tidak terlupa.
```

#### C.4 Generator Script Update

```
bin/create-company.sh
  → Tambah substitusi {{COMPANY_SLUG}} → $SLUG.
  → Sebelumnya hanya substitusi {{COMPANY_NAME}} / {{COMPANY_TYPE}} / {{COMPANY_FOCUS}}.
```

### D. Yang Belum Selesai (untuk sesi berikutnya)

Quick Wins selesai. Yang berikutnya berdasarkan urutan dampak:

1. **Tier 2 — Company SOULs** untuk NexusAI, BrandFlow, Crypto Consultant.
   Saat ini ketiga `companies/*/SOUL.md` masih copy-paste generik.
2. **Tier 3 — Agent SOULs** minimal untuk role yang paling sering dipanggil
   (CEO, CTO/CMO/Research, dan 1 specialist per company).
3. **Specialize skill files** — buang yang tidak relevan, perdalam yang relevan.
4. **Fix inkonsistensi memory reference** — `MAIN.md` baca `MEMORY.md`,
   `AGENTS.md` baca `memory/global.md`. Perlu klarifikasi peran.
5. **Update `MEMORY.md` (root)** — belum reflect keputusan SOUL hierarchy
   dan knowledge management terbaru (hanya `memory/global.md` yang di-update).
6. **Task Logger JSONL** — schema + writer + filter.
7. **Tools tambahan** — `btc_price.py`, `news_sentiment.py` (sudah PLANNED di registry).

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

Struktur utama (post Update 3):

```text
ai-holding/
├── SOUL.md           ← Tier 0 (Root constitution)
├── MAIN_SOUL.md      ← Tier 1 (Main Assistant personality)
├── MAIN.md           ← Loader (urutan baca file)
├── AGENTS.md         ← Routing rules
├── COMMANDS.md       ← Command surface
├── MEMORY.md         ← Durable memory root
├── HEARTBEAT.md      ← Self-check loop
├── knowledge/
│   ├── core/         ← principles.md
│   ├── agent-design/ ← memory-rules.md, tool-use-rules.md
│   ├── tools/        ← tool-registry.md
│   ├── software/     ← software-development-sop.md (NexusAI)
│   ├── marketing/    ← marketing-sop.md (BrandFlow)
│   ├── crypto/       ← crypto-research-framework.md
│   ├── sop/          ← skill library reusable
│   └── karpathy.md
├── templates/
│   └── company/      ← updated to Tier-2 design
├── companies/
│   ├── nexusai/
│   ├── brandflow/
│   └── crypto-consultant/
├── tasks/
├── memory/
├── tools/
└── bin/
```

### Hierarki SOUL (Inheritance)

```
Tier 0: SOUL.md                                    ← konstitusi global (semua entitas)
        ↓
Tier 1: MAIN_SOUL.md                               ← Main Assistant personality
        ↓
Tier 2: companies/<co>/SOUL.md                     ← per perusahaan (3 perusahaan, post Update 4)
        ↓
Tier 3: companies/<co>/agents/<role>.md            ← per agent (18 file, post Update 5)
```

---

## 3. Perusahaan yang Sudah Dibuat

### 3.1 NexusAI

Path: `/home/fatur/ai-holding/companies/nexusai`
Tipe: IT Software Company
Fokus: cloud, DevOps, AI agents, SaaS

Agent aktif (10 role, post Update 5):
- CEO, CTO, Project Manager, Backend, Frontend, DevOps, **Security (NEW)**, **ML (NEW)**, QA, Technical Writer

Tier 3 SOULs ada untuk: ceo, cto, backend, devops, security, ml.

Routing contoh:
```
@nexusai.ceo buatkan strategi produk
@nexusai.cto buatkan arsitektur teknis
@nexusai.backend buatkan desain API
@nexusai.security review auth flow                (NEW)
@nexusai.ml design prompt untuk agent             (NEW)
```

Knowledge domain: `knowledge/software/software-development-sop.md` (Update 3)

### 3.2 BrandFlow

Path: `/home/fatur/ai-holding/companies/brandflow`
Tipe: Marketing and Content Company
Fokus: branding, content, social media, campaign strategy

Agent aktif (11 role, post Update 5):
- CEO, CMO, Project Manager, Copywriter, Social, **Community (NEW)**, **Designer (NEW)**, SEO, Analytics, QA, Writer

Tier 3 SOULs ada untuk: ceo, cmo, copywriter, social, community, designer.

Routing contoh:
```
@brandflow.cmo buatkan strategi campaign
@brandflow.copywriter buatkan caption
@brandflow.designer buatkan visual concept       (NEW)
@brandflow.community draft reply DM ini          (NEW)
```

Knowledge domain: `knowledge/marketing/marketing-sop.md` (Update 3)

### 3.3 Crypto Consultant

Path: `/home/fatur/ai-holding/companies/crypto-consultant`
Tipe: Crypto Research Company
Fokus: market research, cycle analysis, risk management, reporting

Agent aktif (11 role, post Update 5):
- CEO, Research Lead, Project Manager, Market, Risk, **On-chain (NEW)**, **Macro (NEW)**, Data, QA, Report, Writer

Tier 3 SOULs ada untuk: ceo, research, market, risk, onchain, macro.

Routing contoh:
```
@crypto.research cek Fear & Greed Index hari ini
@crypto.market analisis trend BTC weekly
@crypto.onchain trace exchange flows BTC          (NEW)
@crypto.macro overlay DXY + Fed posture           (NEW)
@crypto.risk buatkan risk assessment
```

Knowledge domain: `knowledge/crypto/crypto-research-framework.md`

---

## 4. Fitur yang Sudah Berhasil

### 4.1 Telegram Bot Berjalan
Hermes sudah berjalan via Telegram. Bot dapat menerima dan membalas instruksi user.

### 4.2 Main Assistant Berjalan
Membaca konteks AI Holding, memahami perusahaan milik Fathur, routing, baca file
di workspace.

### 4.3 Routing Perusahaan & Direct Agent Routing
Format `@company` dan `@company.agent` keduanya berjalan.

### 4.4 Company Generator
`bin/create-company.sh` — sekarang juga mensubstitusi `{{COMPANY_SLUG}}` (Update 3).

### 4.5 Tool Crypto Fear & Greed
`tools/fear_greed.py` — production-grade dengan error handling.

### 4.6 SOUL Hierarchy Tier 0 + Tier 1
- `SOUL.md` (Root) — loyalty + execute stance + 4 boundaries.
- `MAIN_SOUL.md` — personality Main Assistant + routing rules + decision authority.

### 4.7 Knowledge Management (post Update 3)
8 file knowledge aktif:
```
knowledge/core/principles.md                     (NEW)
knowledge/agent-design/memory-rules.md
knowledge/agent-design/tool-use-rules.md
knowledge/tools/tool-registry.md
knowledge/software/software-development-sop.md   (NEW)
knowledge/marketing/marketing-sop.md             (NEW)
knowledge/crypto/crypto-research-framework.md
knowledge/sop/README.md                          (NEW)
knowledge/karpathy.md
```

### 4.8 Format Output Standar
- @crypto.research mengikuti format 6 lapisan (FACT, SOURCE, TREND, INTERPRET, SCENARIO, RISK NOTE).
- Disclaimer crypto otomatis di setiap output laporan.

### 4.9 Template Perusahaan (post Update 3)
Template di `templates/company/` sudah:
- AGENTS.md punya Direct Agent Routing block.
- COMMANDS.md pakai `@company keyword` namespacing.
- SOUL.md pakai Tier-2 inheritance design.

### 4.10 Tier 2 Company SOULs (post Update 4)
Setiap perusahaan punya SOUL.md spesifik dengan:
- Identity, culture & tone unik per domain.
- Principles non-negotiable per perusahaan.
- Decision authority eksplisit (CEO/VP/PM/Specialist).
- Boundary reminder spesifik domain (terutama BrandFlow & Crypto).

### 4.11 Tier 3 Agent SOULs + 6 Role Baru (post Update 5)
- 18 Tier 3 SOULs (6 per perusahaan, role utama).
- 6 role baru ditambahkan: `@nexusai.security`, `@nexusai.ml`, `@brandflow.designer`, `@brandflow.community`, `@crypto.onchain`, `@crypto.macro`.
- Setiap Tier 3 SOUL punya voice, principles, decision authority, output format yang spesifik per role.
- AGENTS.md, COMMANDS.md, IDENTITY.md per company di-update untuk reflect role baru.

### 4.12 Test Integrasi Berhasil
- @crypto.research jalankan fear_greed.py + output 6 lapisan.
- @nexusai.backend buat desain API terstruktur.
- @brandflow.copywriter buat caption Instagram dengan 2 variasi tone.

---

## 5. Masalah yang Sudah Diselesaikan

### 5.1 Slash Command Tidak Cocok → Pseudo-Mention
Format `/nexusai` dianggap native command oleh Hermes/Telegram.
Solusi: pakai `@nexusai`, `@brandflow`, `@crypto`.

### 5.2 Natural Command Diperkuat
Rule:
- "perusahaan" tanpa konteks → AI Holding milik Fathur.
- "perusahaan nyata / publik / di dunia" → real-world company.

### 5.3 Knowledge Management → Sudah Lengkap (Update 3)
Sebelumnya broken references. Sekarang semua knowledge yang dirujuk ada.

### 5.4 Tool Execution Approval
Hermes meminta approval saat menjalankan script lokal — aman untuk sekarang.
Whitelist read-only untuk masa depan.

---

## 6. Prinsip Project

Prinsip utama:
```text
Prompt is program.
Context is source code.
Memory is persistent state.
Skill is reusable module.
Tool is external capability.
Human remains supervisor.
```

Knowledge:
- `knowledge/karpathy.md` — Karpathy-inspired principles.
- `knowledge/core/principles.md` — operational version untuk semua agent (Update 3).

---

## 7. Yang Perlu Dilakukan Dalam Waktu Dekat (Updated)

### Prioritas 1 — Task Logger JSONL Implementation (NEXT)
Schema sudah didefinisi di `companies/nexusai/skills/automation/SKILL.md`. Tinggal:
- Writer script (`bin/log-task.sh` atau Python).
- Filter rule (apa yang masuk inbox.jsonl, apa yang tidak — basa-basi out).
- Wire ke Main Assistant routing flow.

### Prioritas 2 — Tools Tambahan
- `btc_price.py` (PLANNED di registry — CoinGecko API, low risk).
- `news_sentiment.py` (PLANNED di registry — perlu pilih source).

### Prioritas 3 — Tier 3 untuk Role Sisanya
Saat ini 18 dari ~32 agent punya Tier 3 SOUL. Yang belum:
- NexusAI: pm, frontend, qa, writer
- BrandFlow: pm, seo, analytics, qa, writer
- Crypto: pm, data, qa, report, writer

Tambah Tier 3 untuk role yang sering dipanggil oleh Fathur, on-demand.

### Prioritas 4 — Hermes Service Hardening
- Cek `hermes-gateway.service` warning bersih, no double process.
- Whitelist tool read-only (mis. `fear_greed.py`) supaya tidak butuh approval setiap kali.

### Prioritas 5 — Migration Prep (Option C)
Mulai siapkan migrasi ke Telegram Group Topics setelah semua di atas stabil.

---

## 8. Roadmap Pendek

### Tahap A — Stabilkan Main Assistant ✓
Done — natural command, routing, pseudo-mention konsisten.

### Tahap B — Bangun Knowledge Management ✓ (Update 3)
Done — folder lengkap, SOP per domain, tool registry, memory rules.

### Tahap C — Buat Tier 2/3 SOULs ✓ (Update 4 + 5)
Tier 2 done. Tier 3 — 18 agent untuk role utama; sisanya on-demand.

### Tahap D — Specialize Skills ✓ (Update 6)
Done — 21 skill files specialized per company, 3 SKILLS.md index, 16 boilerplate dihapus.

### Tahap E — Memory Reference Fix ✓ (Update 7)
Done — `MEMORY.md` (strategic) vs `memory/global.md` (operational) split eksplisit.

### Tahap F — Task Logger (NEXT)
Belum — schema sudah definisi di `skills/automation`, tinggal writer + filter.

### Tahap G — Tools Tambahan
1 dari 4 active. 3 PLANNED (`btc_price.py`, `news_sentiment.py`, lainnya).

### Tahap H — Hermes Hardening
Service warnings cleanup + whitelist read-only tools.

### Tahap I — Migrasi Option C (Telegram Topic)
Nanti setelah F–H stabil.

---

## 9. Status Terakhir

Status project: **Usable Prototype with Specialized Layers + Coherent Memory**

Yang sudah siap:
```
- Hermes Telegram bot
- Main Assistant
- AI Holding workspace
- Company generator (sudah handle SLUG substitution)
- 3 perusahaan awal (32 total agents: 10 + 11 + 11)
- Direct agent routing (@company.agent)
- Crypto Fear & Greed tool
- SOUL Tier 0 + Tier 1
- SOUL Tier 2 (semua 3 perusahaan, Update 4)
- SOUL Tier 3 (18 agent role utama, Update 5)
- 6 role baru: security, ml, designer, community, onchain, macro
- Skill files specialized per company (21 file, Update 6)
- 3 SKILLS.md index files (Update 6)
- Knowledge management lengkap (8 file aktif)
- Memory reference rapi: MEMORY.md (strategic) vs memory/global.md (operational), Update 7
- Per-company MEMORY.md ter-update dengan Tier 2 inheritance
- memory-rules.md Versi 2.0 dengan dual-file structure eksplisit
- Template Tier-2 + skill template + memory template ready
- Repo bersih (no .bak, no Zone.Identifier)
```

Yang belum:
```
- Tier 3 untuk role sisa (PM, QA, Writer, Frontend, SEO, Analytics, Data, Report)
- Task logger JSONL writer (schema ready, implementation pending)
- btc_price.py
- news_sentiment.py
- Whitelist tool read-only (Hermes hardening)
```

---

## 10. Next Immediate Action

Setelah Update 7 (Memory Reference Fix) selesai, langkah berikutnya:

```
1. Task logger JSONL implementation — schema ready di skills/automation,
   tinggal writer + filter.
2. Tools tambahan: btc_price.py, news_sentiment.py.
3. Tier 3 untuk role sisa (on-demand).
4. Hermes hardening — whitelist read-only tools.
```

---

## 11. Prompt untuk Melanjutkan Setup

Gunakan prompt ini ke Hermes / Kiro jika ingin melanjutkan:

```text
Baca summary.md (Update 7 section terbaru) lalu lanjutkan dari "Next Immediate Action".
Mulai dari Task Logger JSONL implementation.
Pelan-pelan, satu tahap per response, tunggu konfirmasi sebelum lanjut.
```

---

## 12. Catatan Branch & Commit

| Branch                                          | Status   | Isi |
|-------------------------------------------------|----------|-----|
| `main`                                          | base     | Update 3 + 4 + 5 + 6 sudah merged |
| `chore/quickwins-cleanup-and-knowledge-fix`     | merged   | Update 3 — cleanup + knowledge + template (PR #1) |
| `feat/tier2-company-souls`                      | merged   | Update 4 — Tier 2 SOULs untuk 3 perusahaan (PR #2) |
| `feat/tier3-agent-souls`                        | merged   | Update 5 — Tier 3 SOULs (18) + 6 role baru (PR #3) |
| `feat/specialize-skills`                        | merged   | Update 6 — Specialize skill files (PR #4) |
| `chore/fix-memory-references`                   | active   | Update 7 — Memory reference fix + restructure |

Setelah branch ini di-merge, lanjut ke task logger atau tools tambahan.
