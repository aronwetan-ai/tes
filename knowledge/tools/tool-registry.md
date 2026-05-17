# Tool Registry — AI Holding

Versi: 1.2
Update terakhir: 2026-05-17 (post Update 9 — Tahap G complete)
Dikelola oleh: Main Assistant

---

## Aturan Penggunaan Registry Ini

Setiap agent WAJIB membaca file ini sebelum menyatakan "tidak bisa mengambil data real-time" atau "tidak punya akses ke X".

Urutan pengecekan:
1. Cek registry ini.
2. Jika tool tersedia → gunakan tool.
3. Jika tool tidak tersedia → jelaskan keterbatasan dengan jujur.
4. JANGAN langsung bilang tidak bisa sebelum cek registry.

Whitelist policy: lihat `knowledge/tools/hermes-whitelist.md` untuk aturan auto-approval Hermes.

---

## Quick Reference

| ID  | Tool                  | Risk    | Status   | Whitelisted | Approval        |
|-----|----------------------|---------|----------|-------------|-----------------|
| 001 | fear_greed.py        | Low     | Active   | Yes         | Auto            |
| 002 | btc_price.py         | Low     | Active   | Yes         | Auto            |
| 003 | news_sentiment.py    | Low     | Active   | Yes         | Auto            |
| 004 | create-company.sh    | Medium  | Active   | No          | User confirm    |
| 005 | log_task.py          | Medium  | Active   | No          | User confirm    |
| 006 | update_task.py       | Medium  | Active   | No          | User confirm    |
| 007 | list_tasks.py        | Low     | Active   | Yes         | Auto            |
| 008 | log_message.py       | Medium  | Active   | No          | User confirm    |
| 009 | task_logger.py       | N/A lib | Active   | N/A         | Not invoked     |
| 010 | archive_tasks.py     | Medium  | Active   | Dry-run only| User confirm    |
| 011 | archive_messages.py  | Medium  | Active   | Dry-run only| User confirm    |
| 012 | recap_manager.py     | Medium  | Active   | Dry-run only| User confirm    |

---

## Daftar Tool Aktif

---

### TOOL-001 — Fear & Greed Index
Name        : fear_greed.py
Path        : /home/fatur/ai-holding/tools/fear_greed.py
Command     : python3 /home/fatur/ai-holding/tools/fear_greed.py
Purpose     : Mengambil Crypto Fear & Greed Index dari Alternative.me API
Output      : Nilai index (0-100) + label (Extreme Fear / Fear / Neutral / Greed / Extreme Greed)
Used by     : @crypto.research, @crypto.market, @crypto.risk, @crypto.report
Risk        : Low — read-only, tidak ada data sensitif
Status      : Active
Whitelisted : Yes — read-only HTTP GET to public API
Approval    : Auto (whitelisted)
Depends on  : Internet connection, Alternative.me API (free, no key)

Contoh output:
Fear & Greed Index: 72 — Greed
Timestamp: 2026-05-17

---

### TOOL-002 — BTC Price Fetcher
Name        : btc_price.py
Path        : /home/fatur/ai-holding/tools/btc_price.py
Command     : python3 /home/fatur/ai-holding/tools/btc_price.py [--currency usd|idr|eur] [--json]
Purpose     : Mengambil harga BTC + 24h change dari CoinGecko public API
Output      : Harga BTC, change %, market cap, volume, last-updated, source
Used by     : @crypto.market, @crypto.risk, @crypto.report
Risk        : Low — read-only public API
Status      : Active (post Update 9)
Whitelisted : Yes — read-only HTTP GET, no key, no mutation
Approval    : Auto (whitelisted)
Depends on  : Internet, CoinGecko API (free, no key)

Contoh output:
BTC price: 67,234.50 USD  ↑ +2.34% (24h)
Market cap: 1,324,567,890,000 USD
Volume 24h: 45,123,456,789 USD
Last updated: 2026-05-17T11:45:00Z (source: CoinGecko)

---

### TOOL-003 — News Sentiment Fetcher
Name        : news_sentiment.py
Path        : /home/fatur/ai-holding/tools/news_sentiment.py
Command     : python3 /home/fatur/ai-holding/tools/news_sentiment.py [--limit N] [--kind news|media] [--json]
Purpose     : Headline scan + naive keyword-based sentiment classifier from CryptoPanic public feed
Output      : Headlines + per-item sentiment (positive/negative/neutral) + summary skew
Used by     : @crypto.research, @crypto.market, @brandflow.analytics (audience trends)
Risk        : Low — read-only public API
Status      : Active (post Update 9)
Whitelisted : Yes — read-only HTTP GET, no key
Approval    : Auto (whitelisted)
Depends on  : Internet, CryptoPanic public API (free)

Notes:
- Sentiment is **keyword-based heuristic**, not full NLP. Output explicitly disclaims this. Treat as headline scan, not analytical truth.
- @crypto.qa flags any research that cites this tool's sentiment as ground truth without further verification.

---

### TOOL-004 — Company Generator Script
Name        : create-company.sh
Path        : /home/fatur/ai-holding/bin/create-company.sh
Command     : bash /home/fatur/ai-holding/bin/create-company.sh "Name" "Type" "Focus"
Purpose     : Membuat perusahaan baru dari template
Output      : Folder perusahaan baru di /home/fatur/ai-holding/companies/<slug>
Used by     : Main Assistant
Risk        : Medium — membuat file/folder baru + appends to company-index.jsonl
Status      : Active
Whitelisted : No — mutates filesystem
Approval    : User confirm before running

---

### TOOL-005 — Task Logger: Create Task
Name        : log_task.py
Path        : /home/fatur/ai-holding/bin/log_task.py
Command     : python3 /home/fatur/ai-holding/bin/log_task.py --company <slug> --to <@agent> --task "<desc>" [--priority HIGH] [--context '{}']
Purpose     : Append task baru ke companies/<co>/tasks/inbox.jsonl + audit log
Output      : Task entry JSON (id, status NEW, timestamps UTC) atau error code 2/3
Used by     : Main Assistant, semua agent yang membuat task delegasi
Risk        : Medium — menulis ke inbox.jsonl + logs.jsonl
Status      : Active
Whitelisted : No — mutates state
Approval    : User confirm
Depends on  : Python 3, AI_HOLDING_HOME (optional env)

Wrapper:
- bin/log-task.sh — bash wrapper 3-arg ergonomis (also Risk: Medium, also gated).

---

### TOOL-006 — Task Logger: Update Status
Name        : update_task.py
Path        : /home/fatur/ai-holding/bin/update_task.py
Command     : python3 /home/fatur/ai-holding/bin/update_task.py --company <slug> --id T001 --status <STATUS> [--actor <@agent>] [--note "..."]
Purpose     : Transition status existing task (state machine validated) + audit
Output      : Updated task entry JSON atau error code 2 (illegal transition / not found)
Used by     : Agent yang mengerjakan / menutup task
Risk        : Medium — rewrites inbox.jsonl atomically + appends to logs.jsonl
Status      : Active
Whitelisted : No — mutates state
Approval    : User confirm

State machine:
  NEW → IN_PROGRESS → DONE
  NEW → IN_PROGRESS → FAILED → RETRY → IN_PROGRESS → DONE
  NEW / IN_PROGRESS / FAILED / RETRY → CANCELLED

---

### TOOL-007 — Task Logger: List & Filter
Name        : list_tasks.py
Path        : /home/fatur/ai-holding/bin/list_tasks.py
Command     : python3 /home/fatur/ai-holding/bin/list_tasks.py --company <slug> [--status X] [--agent @x] [--priority HIGH] [--active-only] [--format table|json|jsonl]
Purpose     : Filter & list tasks dari inbox.jsonl
Output      : Table (default) / JSON array / JSONL stream
Used by     : Main Assistant (recap, status check), agent inbox pull
Risk        : Low — read-only
Status      : Active
Whitelisted : Yes — never writes
Approval    : Auto (whitelisted)

---

### TOOL-008 — Task Logger: Agent Message
Name        : log_message.py
Path        : /home/fatur/ai-holding/bin/log_message.py
Command     : python3 /home/fatur/ai-holding/bin/log_message.py --company <slug> --from <@agent> --to <@agent> --message "..." [--ref-task T001]
Purpose     : Append agent-to-agent durable message ke messages.jsonl
Output      : Message entry JSON
Used by     : Agent yang hand-off / status report durable antar agent
Risk        : Medium — menulis ke messages.jsonl
Status      : Active
Whitelisted : No — mutates state
Approval    : User confirm

---

### TOOL-009 — Task Logger: Shared Library
Name        : task_logger.py
Path        : /home/fatur/ai-holding/bin/task_logger.py
Command     : (tidak dipanggil langsung)
Purpose     : Shared schema, validation, I/O untuk TOOL-005..008, TOOL-010..012
Used by     : log_task.py, update_task.py, list_tasks.py, log_message.py, archive_tasks.py, archive_messages.py, recap_manager.py
Risk        : N/A (library)
Status      : Active
Whitelisted : N/A
Approval    : N/A

Reference: knowledge/agent-design/task-logger-rules.md untuk schema, state machine, filter rules.

---

### TOOL-010 — Task Archival
Name        : archive_tasks.py
Path        : /home/fatur/ai-holding/bin/archive_tasks.py
Command     : python3 /home/fatur/ai-holding/bin/archive_tasks.py [--company <slug>] [--older-than 30] [--dry-run] [--quiet]
Purpose     : Move terminal tasks (DONE / CANCELLED) older than N days from inbox.jsonl to archive/<YYYY-MM>.jsonl
Output      : Per-company report kept/archived counts; appends ARCHIVE event to logs.jsonl
Used by     : Main Assistant (operator), `@nexusai.devops` (cron)
Risk        : Medium — mutates inbox.jsonl + writes archive bucket files
Status      : Active (post Update 9)
Whitelisted : Dry-run only (`--dry-run` is read-only and auto-runnable)
Approval    : User confirm for actual archival; dry-run is auto

Notes:
- FAILED is NOT auto-archived (might be retried).
- logs.jsonl is NEVER archived (audit trail).
- Idempotent: rerun safe; archive bucket dedupes by ID.
- Recommended cadence: weekly cron, or manual when inbox > 200 rows.

---

### TOOL-011 — Message Archival
Name        : archive_messages.py
Path        : /home/fatur/ai-holding/bin/archive_messages.py
Command     : python3 /home/fatur/ai-holding/bin/archive_messages.py [--company <slug>] [--older-than 30] [--dry-run] [--quiet]
Purpose     : Move messages older than N days from messages.jsonl to messages-archive/<YYYY-MM>.jsonl
Output      : Per-company report kept/archived counts
Used by     : Main Assistant (operator)
Risk        : Medium — mutates messages.jsonl + writes archive bucket files
Status      : Active (post Update 9)
Whitelisted : Dry-run only
Approval    : User confirm for actual archival; dry-run is auto

---

### TOOL-012 — Recap Manager
Name        : recap_manager.py
Path        : /home/fatur/ai-holding/bin/recap_manager.py
Command     : python3 /home/fatur/ai-holding/bin/recap_manager.py [--company <slug>] [--window daily|weekly|monthly|custom] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--dry-run] [--quiet]
Purpose     : Generate periodic recap entry from logs.jsonl + inbox.jsonl into recap.jsonl
Output      : Per-company recap (counts created / completed / cancelled / failed / active, top agents, priority distribution)
Used by     : Main Assistant (Recap Manager role), Fathur (status checks)
Risk        : Medium — appends to recap.jsonl (does NOT mutate inbox/logs/messages)
Status      : Active (post Update 9)
Whitelisted : Dry-run only
Approval    : User confirm for actual append; dry-run is auto

Windows:
  daily    last 24h
  weekly   last 7d (default)
  monthly  last 30d
  custom   --since + --until

---

## Cara Menambah Tool Baru

Tambahkan entry baru dengan format:
TOOL-XXX — Nama Tool
Name        : nama_file.py
Path        : /home/fatur/ai-holding/tools/nama_file.py
Command     : perintah untuk menjalankan
Purpose     : Apa yang dilakukan tool ini
Output      : Format output
Used by     : @company.agent yang memakai
Risk        : Low / Medium / High
Status      : Active / Planned / Deprecated
Whitelisted : Yes / No / Dry-run only / N/A
Approval    : Auto / User confirm / Always confirm
Depends on  : Dependency eksternal jika ada

Risk level:
- **Low** — read-only, tidak ada efek samping
- **Medium** — membuat/mengubah file lokal
- **High** — akses ke sistem eksternal mutating, mengirim data, atau menghapus file

Whitelist eligibility (lihat `knowledge/tools/hermes-whitelist.md` untuk aturan lengkap):
- Yes hanya bila Risk=Low DAN read-only DAN no-secrets DAN no-external-mutation DAN bounded-cost.
- Dry-run only bila tool punya flag yang membuat eksekusi pure read-only saat di-set.

---

## Catatan Maintenance

- Setiap tool baru harus didaftarkan di sini sebelum dipakai agent.
- Tool dengan status PLANNED tidak boleh dijalankan agent.
- Tool dengan Risk High wajib konfirmasi user (tidak boleh whitelist).
- Update versi file setiap kali ada perubahan tool.
- Whitelist sync: setiap kali registry berubah, periksa `hermes-whitelist.md` untuk konsistensi.
