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

## Senior Patterns (Deep Dive)

### Agency-scale automation patterns

NexusAI's automation skill exists primarily to support the agency's operational reality: 20–50 active clients, multi-platform (IG / Twitter / LinkedIn / TikTok / email / ads), per-client credentials, sustainable rate. Default patterns:

#### Multi-account orchestration

```
For each client:
  For each platform account they own (or grant access):
    Load credentials from cred_vault[client_id][platform][account]
    Spawn isolated browser profile / session
    Apply per-account fingerprint (UA, viewport, timezone, locale)
    Route through assigned proxy (residential for IG/LI, datacenter for less hostile)
    Execute task with human-paced jitter (mean ± 30%)
    Log every action: {client, account, platform, action, ts, outcome}
    On failure: classify (rate-limit / auth / shadow-ban / network) and route to handler
```

Implementation hints:
- One browser profile dir per account, never shared.
- Proxy assignment is sticky per account, not per session.
- Action queue is per-account (don't fire all clients in parallel — that's the obvious abuse pattern platforms detect).
- Daily action budget per account, enforced in code, not just intent.

Reference: `knowledge/security/opsec-multi-account.md`.

#### Cold outreach pipeline (DM / email)

Architecture:

```
prospects.jsonl  →  enrichment  →  personalization  →  send queue  →  reply detector
                                       (LLM)             (rate-limited       ↓
                                                          per account)    inbox.jsonl
                                                                              ↓
                                                                          intent classifier
                                                                              ↓
                                                                          (positive / negative / neutral / oos)
```

Rules for sustainable outreach:

| Layer | Rule |
|---|---|
| Account warmup | New account: 7–14 days low-activity (scroll, like) before any DM. |
| Daily cap | 20–40 cold DMs/day max per IG account. 50–80 cold emails/day per email account (after warmup). |
| Pacing | Spread across 6–10 hours. Not bursty. Skip overnight in target's timezone. |
| Personalization | Profile-extracted variable fill (name, company, recent post, mutual interest). At least 2 variables, real, verified. Generic blasts get reported, faster than slow. |
| Reply detection | Within 5 minutes. Pause sequence on reply, route to human / classifier. |
| Opt-out | Every message includes opt-out path. Honor immediately. Track in `opt_out.jsonl` per client. Never DM same prospect from same client twice. |
| Failure response | Account flagged → quarantine 24–48h → if still flagged, retire account + do not reuse same fingerprint pattern. |

#### Scraping pipeline

```
target_list.jsonl  →  fetcher (rate-limited, fingerprinted)
                          ↓
                  parser (extract structured fields)
                          ↓
                  validator (drop malformed, dedupe)
                          ↓
                  output.jsonl (one row per result, schema-validated)
```

Sources by sensitivity:

| Source | Approach |
|---|---|
| Public web (no login) | Plain HTTP, polite User-Agent, robots.txt respected as long as legally meaningful in target jurisdiction. |
| Public API (open) | Use official client, respect rate limit, pin API version. |
| Public API (key-required) | Per-client API key in cred_vault. |
| Authenticated with own session cookie / token | Headless browser w/ persistent profile OR direct API call w/ valid cookie jar. Per `declined-tools.md`, only own/authorized session — not third-party harvested. |
| Public profile data on social platform (logged in) | Each scrape account on its own fingerprint + proxy, low daily quota, jittered. |

#### Pipeline reliability patterns

- **Idempotency**: every step keys outputs by `(input_hash, step_name)`. Re-running = no duplicate output.
- **Resume from checkpoint**: pipeline state in `.state/<pipeline>/<run_id>.json`. Crash = resume from last completed step.
- **Dead letter queue**: failed items → `dlq.jsonl` with error reason. Don't lose data on transient failure.
- **Backoff**: exponential with jitter on 429 / 503. Cap retries (typically 5).
- **Circuit breaker**: after N failures in M seconds, halt that target for cool-down period.

### Cron / scheduled job patterns

```
0 */4 * * *   /home/fatur/ai-holding/bin/scrape_run.sh competitor_posts
30 9 * * *    /home/fatur/ai-holding/bin/dm_outreach_run.sh client_a "morning_batch"
0  6 * * 0    /home/fatur/ai-holding/bin/recap_manager.py --window weekly --quiet
```

Discipline:
- Each cron job logs to `cron/<job>/<date>.log` for last 30 days.
- Each cron job emits a heartbeat after success → if heartbeat misses, alert.
- Each cron job has a `--dry-run` flag.
- Long-running jobs (>10min) should be background workers, not cron.

### Inter-agent / inter-process communication

For NexusAI's own coordination (agent → agent, script → script):

| Pattern | When |
|---|---|
| Shared JSONL inbox (current task logger) | Asynchronous, durable, single-host. |
| HTTP / gRPC service | Real-time, multi-host, structured. |
| Redis Streams | Real-time, multi-consumer, replay-able. |
| Postgres `LISTEN/NOTIFY` | If you already have Postgres, free, no new infra. |
| Filesystem watch | Local-only, simple jobs. |

Default for agency-internal: JSONL + cron, until proven insufficient. Don't reach for Kafka.

### Anti-patterns

- **Burst-fire automation that gets accounts banned within a week.** Sustainable rate beats heroic rate.
- **Shared browser profile across multiple accounts on the same platform.** Cluster-detection guarantee.
- **Hardcoded credentials in scripts.** Use `cred_vault.py` always.
- **Logging full request/response with PII.** Redact at log-write time.
- **No idempotency.** Re-run after crash = duplicate DMs / charges / posts.
- **No dead-letter queue.** Failed items disappear silently.
- **Cron job that doesn't exit cleanly when killed.** Trap signals, drain, exit.

## Reference

- `knowledge/agent-design/tool-use-rules.md`
- `knowledge/agent-design/task-logger-rules.md` — schema, state machine, filter rules untuk Task Logger.
- `knowledge/tools/tool-registry.md` — TOOL-005..009 untuk script Task Logger; TOOL-013..022 untuk Update 10 tools.
- `knowledge/security/opsec-multi-account.md` — operational hygiene for multi-account work.
- `knowledge/scope/declined-tools.md` — boundary on what automation will NOT do.
- `bin/create-company.sh` (existing example).
- `bin/log_task.py` / `bin/update_task.py` / `bin/list_tasks.py` / `bin/log_message.py`.
- `tools/cred_vault.py`, `tools/secret_scanner.py` (Update 10 — agency-context).
