# Task Logger Rules — AI Holding

Versi: 1.0
Update terakhir: 2026-05-17 (Update 8 — Task Logger JSONL implementation)
Berlaku untuk: Main Assistant + semua agent yang membuat / mengubah / membaca task

---

## Tujuan

Task Logger adalah **single source of truth** untuk task antar agent / antar perusahaan.
Dipakai untuk:

- Track work item yang Fathur (atau agent) delegate.
- State machine eksplisit (NEW → IN_PROGRESS → DONE / FAILED / CANCELLED).
- Audit trail yang resumable (kalau session crash, bisa lanjut dari last state).
- Cross-agent messaging yang durable (bukan basa-basi).

Bukan untuk: chat history, draft, scratch notes, basa-basi.

---

## File Structure (Per Company)

Setiap company punya folder `companies/<co>/tasks/` dengan **4 file JSONL**:

| File | Peran | Format |
|---|---|---|
| `inbox.jsonl` | **Single source of truth** untuk semua task. Status field membedakan, bukan file terpisah. | Task entry per line |
| `logs.jsonl` | **Append-only audit log** — setiap CREATE / UPDATE state transition tertulis di sini. | Audit entry per line |
| `messages.jsonl` | Agent-to-agent durable message (bukan task). | Message entry per line |
| `recap.jsonl` | Periodic summary — diisi oleh Recap Manager, **bukan** oleh task scripts. | Recap entry per line |

Catatan desain: kita **tidak** pakai pattern `inbox / active / done` 3-file move. Alasan:
- Lebih idempotent (rerun aman).
- Lebih mudah query (1 file, filter by status).
- Tidak ada race condition saat memindah file.

Holding-level task (mis. task yang menyangkut multi-company atau Main Assistant sendiri) ditulis ke `tasks/` di root, bukan ke company-specific folder.

---

## Schema Task (`inbox.jsonl`)

```json
{
  "id":         "T001",
  "company":    "nexusai",
  "from":       "USER",
  "to":         "@nexusai.backend",
  "task":       "Design REST API for user-service",
  "priority":   "HIGH",
  "status":     "NEW",
  "created_at": "2026-05-17T10:00:00Z",
  "updated_at": "2026-05-17T10:00:00Z",
  "context":    {}
}
```

| Field | Wajib | Validasi |
|---|---|---|
| `id` | ya | Format `T###` (auto-incremented per-company di `inbox.jsonl`). |
| `company` | ya | Slug perusahaan: `nexusai`, `brandflow`, `crypto-consultant`, atau `holding`. |
| `from` | ya | `USER`, `MAIN`, atau `@<company>.<agent>`. |
| `to` | ya | `@<company>` (untuk PM routing) atau `@<company>.<agent>` (direct). |
| `task` | ya | Min 8 karakter. Verb action + deliverable jelas. |
| `priority` | ya | `LOW` / `MEDIUM` / `HIGH` / `URGENT`. Default `MEDIUM`. |
| `status` | ya | Lihat State Machine. Awal selalu `NEW`. |
| `created_at` | ya | ISO-8601 UTC, auto. |
| `updated_at` | ya | ISO-8601 UTC, auto pada setiap transition. |
| `context` | ya | JSON object. Boleh `{}`. Diisi sprint, ref doc, history transitions, dll. |

ID space **per-company**: `nexusai/T001` dan `brandflow/T001` adalah dua task berbeda — boleh.

---

## Schema Audit (`logs.jsonl`)

```json
{
  "event":       "CREATE" | "UPDATE",
  "task_id":     "T001",
  "company":     "nexusai",
  "to":          "@nexusai.backend",
  "from":        "USER",
  "prev_status": null | "NEW" | "IN_PROGRESS" | ...,
  "new_status":  "NEW" | "IN_PROGRESS" | "DONE" | ...,
  "actor":       "MAIN" | "@nexusai.backend" | ...,
  "at":          "2026-05-17T10:00:00Z",
  "note":        "<optional free-form>"
}
```

`logs.jsonl` adalah **append-only** — tidak pernah dihapus / dirubah. Itu yang bikin audit valid.

---

## Schema Message (`messages.jsonl`)

```json
{
  "company":    "nexusai",
  "from":       "@nexusai.backend",
  "to":         "@nexusai.devops",
  "message":    "user-service API ready, please deploy to staging",
  "ref_task":   "T001",
  "created_at": "2026-05-17T10:00:00Z"
}
```

Pakai untuk hand-off antar agent, status report yang bukan task baru, atau notifikasi yang harus terlihat oleh agent penerima saat session berikutnya. Min 4 karakter — tidak boleh basa-basi.

---

## State Machine

```
                    ┌─────────────────────┐
                    │                     ▼
   NEW ──► IN_PROGRESS ──► DONE   (terminal)
    │           │
    │           ├──► FAILED ──► RETRY ──► IN_PROGRESS
    │           │
    └──► CANCELLED (terminal)
                │
                └─► (only from any non-terminal state)
```

Transisi yang **boleh**:

| Dari | Ke |
|---|---|
| `NEW` | `IN_PROGRESS`, `CANCELLED` |
| `IN_PROGRESS` | `DONE`, `FAILED`, `CANCELLED` |
| `FAILED` | `RETRY`, `CANCELLED` |
| `RETRY` | `IN_PROGRESS`, `CANCELLED` |
| `DONE` | (terminal — tidak ada) |
| `CANCELLED` | (terminal — tidak ada) |

Transisi tidak valid (mis. `DONE → NEW`) ditolak oleh `update_task.py` dengan exit code 2.

Kalau task DONE perlu dikerjakan ulang: buat task baru dengan reference ke ID lama di `context.parent_id`.

---

## Filter Rules — Apa yang DILOG, Apa yang TIDAK

### Wajib di-log sebagai task

- Task konkret dengan deliverable jelas (`task` ≥ 8 karakter, ada verb action).
- Decision yang menghasilkan kerja lanjutan (berbeda dengan `[DECISION]` di memory yang sekedar mencatat keputusan).
- Multi-step work yang akan dieksekusi lintas turn / lintas hari.
- Kerja yang state-nya perlu dilacak (siapa yang pegang, kapan selesai).

### Tidak boleh di-log sebagai task

- **Basa-basi** — "ok", "siap", "thanks", "sip" — masuk ke chat, bukan task.
- **Konfirmasi ringan** — "ya, lanjutkan", "betul" — tidak ada kerja, tidak ada state.
- **Pertanyaan yang langsung dijawab dalam 1 turn** — itu Q&A, bukan task.
- **Auto-generated heartbeat** — `HEARTBEAT.md` punya tempat sendiri.
- **Draft / scratch / brainstorming** — pakai memory atau scratch file, bukan task logger.
- **Klarifikasi tanpa keputusan** — tidak ada delivery commitment.

### Apa yang dilog di `messages.jsonl` vs di-skip

- Log: hand-off antar agent, status report durable, notifikasi yang harus persist.
- Skip: setiap interaksi chat, ack ringan, basa-basi, pertanyaan klarifikasi.

Aturan praktis: **kalau Fathur (atau agent) tidak akan pernah baca lagi entry ini, jangan log.**

---

## Tools (Scripts)

Semua di `bin/`. Detail: `knowledge/tools/tool-registry.md`.

| Tool | Pakai untuk |
|---|---|
| `bin/log_task.py` | Buat task baru (auto ID, validasi schema, append + audit). |
| `bin/log-task.sh` | Wrapper bash ergonomis untuk `log_task.py` (3 arg minimal). |
| `bin/update_task.py` | Transition status existing task (validasi state machine, audit). |
| `bin/list_tasks.py` | Filter & list (by company, agent, status, priority, format). |
| `bin/log_message.py` | Append agent-to-agent durable message ke `messages.jsonl`. |

Semua script:
- Read `AI_HOLDING_HOME` env var; default fallback ke walk-up dari script location.
- Append idempoten; rerun tidak membuat duplikat (kecuali sengaja diberi ID yang sudah ada — itu error).
- Exit code 0 = OK, 2 = schema/argument/transition error, 3 = I/O error.

---

## Workflow Contoh

### Skenario 1 — User delegate task ke agent

```bash
# Fathur: "buatkan REST API user-service di NexusAI"
bin/log-task.sh nexusai @nexusai.backend "Design REST API for user-service" HIGH
# → T001 NEW

# @nexusai.backend pulls task
bin/list_tasks.py --company nexusai --agent @nexusai.backend --active-only

# @nexusai.backend mulai kerja
bin/update_task.py --company nexusai --id T001 --status IN_PROGRESS --actor @nexusai.backend

# Selesai
bin/update_task.py --company nexusai --id T001 --status DONE \
  --actor @nexusai.backend --note "merged in PR #12"

# Hand-off ke @nexusai.devops
bin/log_message.py --company nexusai --from @nexusai.backend --to @nexusai.devops \
  --message "user-service API ready, deploy to staging" --ref-task T001
```

### Skenario 2 — Recap

```bash
# Lihat semua task aktif Crypto Consultant
bin/list_tasks.py --company crypto-consultant --active-only

# Lihat semua HIGH priority lintas status
bin/list_tasks.py --company nexusai --priority HIGH

# Export untuk laporan
bin/list_tasks.py --company brandflow --format jsonl > /tmp/brandflow-tasks.jsonl
```

### Skenario 3 — Failed → Retry

```bash
bin/update_task.py --company nexusai --id T002 --status FAILED \
  --actor @nexusai.devops --note "deploy gagal: missing secret"
bin/update_task.py --company nexusai --id T002 --status RETRY \
  --actor @nexusai.devops --note "secret added, retrying"
bin/update_task.py --company nexusai --id T002 --status IN_PROGRESS --actor @nexusai.devops
bin/update_task.py --company nexusai --id T002 --status DONE --actor @nexusai.devops
```

History tersimpan di `context.history[]` per task + audit trail di `logs.jsonl`.

---

## Maintenance

- File `inbox.jsonl` boleh besar — filter pakai `list_tasks.py`, jangan baca manual.
- Saat `inbox.jsonl` company > ~500 baris, arsipkan terminal tasks (`DONE`/`CANCELLED`/`FAILED` tanpa retry) ke `tasks/archive/<YYYY-MM>.jsonl`. Pertahankan task aktif di `inbox.jsonl`.
- `logs.jsonl` jangan diarsipkan tanpa konfirmasi user — ini compliance/audit trail.
- `messages.jsonl` lama (> 30 hari, sudah dibaca) boleh diarsipkan ke `messages-archive.jsonl`.

---

## Anti-Pattern

- ❌ Manually edit `inbox.jsonl` / `logs.jsonl`. Pakai script.
- ❌ Reuse task ID antar transition (mis. mengubah T001 jadi T001-v2). Kalau task fundamental berubah, buat task baru.
- ❌ Log basa-basi sebagai task supaya "kelihatan kerja". Filter rules melarang.
- ❌ Skip audit log dengan langsung append ke `inbox.jsonl`. Selalu lewat script.
- ❌ Mencampur company task di file lain (mis. NexusAI task di `crypto-consultant/tasks/`).
- ❌ Mengubah `logs.jsonl` (append-only, immutable).

---

## Reference

- `companies/nexusai/skills/automation/SKILL.md` — schema asal, NexusAI automation flavor.
- `bin/task_logger.py` — implementasi shared library.
- `knowledge/tools/tool-registry.md` — entry registry untuk 4 script ini.
- `knowledge/agent-design/memory-rules.md` — perbedaan task (di tasks/) vs memory (di memory/).

---

## Hubungan dengan Memory

Task logger TIDAK menggantikan memory:

| Domain | Tempat |
|---|---|
| Work item yang sedang berjalan dengan state machine | `tasks/inbox.jsonl` |
| Keputusan strategis durable | `MEMORY.md` (root) |
| Operational tagged log (`[DECISION]`, `[ARCH]`, `[INSIGHT]`) | `memory/global.md` |
| Company-scoped state | `companies/<co>/MEMORY.md` |
| Audit trail state transition task | `tasks/logs.jsonl` |
| Hand-off antar agent | `tasks/messages.jsonl` |

Task yang selesai (`DONE`) yang punya impact strategis: catat **juga** sebagai `[DONE]` di memory yang relevan. Task yang sekadar selesai tidak perlu masuk memory.
