---
name: automation
description: Workflow automation, JSONL task systems, scripts, scheduled jobs, multi-agent communication for NexusAI.
company: NexusAI
used_by: ["@nexusai.devops", "@nexusai.backend", "@nexusai.ml"]
---

# Automation Skill — NexusAI

Build the plumbing. Use for workflow automation, scripts, scheduled jobs, JSONL pipelines, and multi-agent communication.

Inherits NexusAI SOUL (engineering-precise, pragmatic). Boring tech. Resumable. Observable.

## When to Use

- JSONL task pipelines (inbox / processing / done).
- Cron / scheduled jobs.
- Multi-agent message routing.
- File-based state machines.
- One-shot scripts that may become recurring.
- Generators (like `bin/create-company.sh`).

## Rules

1. **File formats**: JSONL for logs / tasks / messages. Markdown for human-edited config. JSON for structured data needing parser.
2. **Resumable**: every workflow can stop and resume from last completed step.
3. **Status fields**: NEW / IN_PROGRESS / DONE / FAILED / RETRY.
4. **Idempotent**: re-running with same input = same end state.
5. **Logged**: every step writes to a log line. No silent failures.
6. **Avoid over-engineering**: if a 50-line script works, don't reach for Airflow.

## File Structure (Authoritative)

Reality di repo (lihat `companies/<co>/tasks/`):

| File | Peran | Format |
|---|---|---|
| `inbox.jsonl` | **Single source of truth** — semua task. Status field membedakan. | Task entry per line |
| `logs.jsonl` | **Append-only audit log** — setiap CREATE / UPDATE state transition. | Audit entry per line |
| `messages.jsonl` | Agent-to-agent durable message. | Message entry per line |
| `recap.jsonl` | Periodic summary — diisi Recap Manager. | Recap entry per line |

Tidak pakai pattern `inbox / active / done` 3-file move. Alasan: idempoten + tidak ada race condition.

## Default JSONL Task Schema

```json
{
  "id": "T001",
  "company": "nexusai",
  "from": "USER",
  "to": "@nexusai.backend",
  "task": "Describe the task in one line",
  "priority": "HIGH",
  "status": "NEW",
  "created_at": "2026-05-17T10:00:00Z",
  "updated_at": "2026-05-17T10:00:00Z",
  "context": {}
}
```

Status transitions:
- NEW → IN_PROGRESS → DONE
- NEW → IN_PROGRESS → FAILED → RETRY → IN_PROGRESS → DONE
- NEW → CANCELLED (with reason)

State machine validated by `bin/update_task.py`. DONE / CANCELLED adalah terminal — kalau task perlu dikerjakan ulang, buat task baru dengan `context.parent_id`.

## Implementasi (Production Scripts)

Semua script di `bin/`. Detail rules: `knowledge/agent-design/task-logger-rules.md`.

| Script | Pakai untuk |
|---|---|
| `bin/log_task.py` | Buat task baru. Auto ID `T###` per-company, append ke `inbox.jsonl` + audit ke `logs.jsonl`. |
| `bin/log-task.sh` | Wrapper bash 3-arg ergonomis di atas `log_task.py`. |
| `bin/update_task.py` | Transition status (validasi state machine + audit). |
| `bin/list_tasks.py` | Filter & list (by company, agent, status, priority, format: table/json/jsonl). |
| `bin/log_message.py` | Append agent-to-agent message ke `messages.jsonl`. |
| `bin/task_logger.py` | Shared library — schema, validation, I/O. **Tidak dipanggil langsung.** |

Workflow standard NexusAI:

```bash
# Fathur delegasi ke @nexusai.backend
bin/log-task.sh nexusai @nexusai.backend "Design REST API for user-service" HIGH

# Backend pull list
bin/list_tasks.py --company nexusai --agent @nexusai.backend --active-only

# Backend mulai
bin/update_task.py --company nexusai --id T001 --status IN_PROGRESS --actor @nexusai.backend

# Selesai + hand-off
bin/update_task.py --company nexusai --id T001 --status DONE --actor @nexusai.backend --note "PR #12 merged"
bin/log_message.py --company nexusai --from @nexusai.backend --to @nexusai.devops \
  --message "user-service ready, deploy staging" --ref-task T001
```

Semua script:
- Read `AI_HOLDING_HOME` env var; default fallback walk-up dari script location.
- Exit code 0 = OK, 2 = schema/transition error, 3 = I/O error.
- Append idempoten; logs.jsonl immutable / append-only.

## Output Format

For workflow design:
```
[GOAL]          What the automation does
[WORKFLOW]      Step-by-step (numbered)
[FILE STRUCTURE]
   inbox.jsonl     — new tasks
   active.jsonl    — being processed
   done.jsonl      — completed
   logs.jsonl      — append-only audit
[SCRIPT/COMMAND] Concrete code or command
[VERIFICATION]   How to confirm it works
[FAILURE MODE]   What breaks first, how to recover
```

For one-shot script:
```
[PURPOSE]   What it does, in one line
[INPUT]     Args / env / files needed
[OUTPUT]    Files created / lines logged / state changed
[USAGE]     Exact command line
[ROLLBACK]  How to undo (if applicable)
```

## Cross-Skill / Cross-Agent

- Automation that ships to production → `@nexusai.devops` + `skills/devops`.
- Automation that drives an AI agent → `@nexusai.ml`.
- Automation security (secrets, escalated privileges) → `@nexusai.security`.

## Reference

- `knowledge/agent-design/tool-use-rules.md`
- `knowledge/agent-design/task-logger-rules.md` — schema, state machine, filter rules untuk Task Logger.
- `knowledge/tools/tool-registry.md` — TOOL-005..009 untuk script Task Logger.
- `bin/create-company.sh` (existing example).
- `bin/log_task.py` / `bin/update_task.py` / `bin/list_tasks.py` / `bin/log_message.py`.
