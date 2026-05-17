# Tool Registry — AI Holding

Versi: 1.1
Update terakhir: 2026-05-17 (post Update 8 — Task Logger JSONL)
Dikelola oleh: Main Assistant  

---

## Aturan Penggunaan Registry Ini

Setiap agent WAJIB membaca file ini sebelum menyatakan "tidak bisa mengambil data real-time" atau "tidak punya akses ke X".

Urutan pengecekan:
1. Cek registry ini.
2. Jika tool tersedia → gunakan tool.
3. Jika tool tidak tersedia → jelaskan keterbatasan dengan jujur.
4. JANGAN langsung bilang tidak bisa sebelum cek registry.

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
Approval    : Tidak perlu approval khusus (read-only)
Depends on  : Internet connection, Alternative.me API (free, no key)

Contoh output:
Fear & Greed Index: 72 — Greed
Timestamp: 2026-05-17

---

### TOOL-002 — [PLANNED] BTC Price Fetcher
Name        : btc_price.py
Path        : /home/fatur/ai-holding/tools/btc_price.py
Command     : python3 /home/fatur/ai-holding/tools/btc_price.py
Purpose     : Mengambil harga BTC real-time dari CoinGecko API
Output      : Harga BTC dalam USD + perubahan 24 jam
Used by     : @crypto.market, @crypto.risk, @crypto.report
Risk        : Low — read-only
Status      : PLANNED — belum dibuat
Approval    : Tidak perlu

---

### TOOL-003 — [PLANNED] News Sentiment Fetcher
Name        : news_sentiment.py
Path        : /home/fatur/ai-holding/tools/news_sentiment.py
Purpose     : Mengambil berita crypto terbaru + analisis sentimen sederhana
Output      : Daftar headline + label sentimen (positive/neutral/negative)
Used by     : @crypto.research, @brandflow.analytics
Risk        : Low — read-only
Status      : PLANNED — belum dibuat
Approval    : Tidak perlu

---

### TOOL-004 — Company Generator Script
Name        : create-company.sh
Path        : /home/fatur/ai-holding/bin/create-company.sh
Command     : bash /home/fatur/ai-holding/bin/create-company.sh
Purpose     : Membuat perusahaan baru dari template
Output      : Folder perusahaan baru di /home/fatur/ai-holding/companies/
Used by     : Main Assistant
Risk        : Medium — membuat file/folder baru
Status      : Active
Approval    : Perlu konfirmasi user sebelum dijalankan

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
Approval    : Tidak perlu (filter rules sudah di-enforce di script)
Depends on  : Python 3, AI_HOLDING_HOME (optional env)

Wrapper:
- bin/log-task.sh — bash wrapper 3-arg ergonomis (untuk path standar).

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
Approval    : Tidak perlu (state machine guards)

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
Approval    : Tidak perlu

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
Approval    : Tidak perlu (min 4-char filter)

---

### TOOL-009 — Task Logger: Shared Library
Name        : task_logger.py
Path        : /home/fatur/ai-holding/bin/task_logger.py
Command     : (tidak dipanggil langsung)
Purpose     : Shared schema, validation, I/O untuk TOOL-005..008
Used by     : log_task.py, update_task.py, list_tasks.py, log_message.py
Risk        : N/A (library)
Status      : Active

Reference: knowledge/agent-design/task-logger-rules.md untuk schema, state machine, filter rules.

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
Approval    : Perlu / Tidak perlu
Depends on  : Dependency eksternal jika ada

Risk level:
- **Low** — read-only, tidak ada efek samping
- **Medium** — membuat/mengubah file lokal
- **High** — akses ke sistem eksternal, mengirim data, atau menghapus file

---

## Catatan Maintenance

- Setiap tool baru harus didaftarkan di sini sebelum dipakai agent.
- Tool dengan status PLANNED tidak boleh dijalankan agent.
- Tool dengan Risk High wajib konfirmasi user.
- Update versi file setiap kali ada perubahan.
