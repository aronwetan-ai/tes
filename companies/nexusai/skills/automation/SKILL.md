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
- `bin/create-company.sh` (existing example)
