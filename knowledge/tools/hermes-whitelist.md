# Hermes Whitelist — Tool Auto-Approval Policy

Versi: 1.0
Update terakhir: 2026-05-17 (Update 9 — Hermes hardening)
Owner: Fathur (config) + Main Assistant (registry tracking)

---

## Purpose

Hermes safety default = ask approval before running every script. That's correct for `Risk: High` and `Risk: Medium` tools, but creates friction for `Risk: Low` (read-only) tools that should be auto-runnable.

This document defines:
1. **Which tools are eligible** for whitelisting (auto-run without confirmation).
2. **Which are NOT eligible** (must always confirm).
3. **How to apply** the whitelist in Hermes config.
4. **Audit + revocation** rules.

---

## Whitelist Eligibility Rules

A tool may be whitelisted **only if all of the following are true**:

1. `Risk: Low` in `knowledge/tools/tool-registry.md`.
2. **Read-only**: it does not write, modify, delete, or move files in the workspace, and does not send any external request that mutates state.
3. **No secrets**: it does not read API keys, tokens, passwords, or `.env` files.
4. **No external mutation**: it does not POST/PUT/PATCH/DELETE to any external API.
5. **Bounded cost**: it does not trigger paid API calls (e.g., Glassnode, Bloomberg, OpenAI billable).
6. **Deterministic side effects**: re-running it 100 times produces no observable change in the system.
7. **Observable**: its output goes to stdout / a log file you can audit.

If any one fails → **NOT whitelistable**. Period.

---

## Current Whitelist (Recommendation)

Based on `tool-registry.md` Versi 1.2 (post Update 9):

| Tool | Risk | Whitelist? | Reason |
|---|---|---|---|
| `tools/fear_greed.py` | Low | ✅ Yes | Read-only HTTP GET to Alternative.me public API. |
| `tools/btc_price.py` | Low | ✅ Yes | Read-only HTTP GET to CoinGecko public API. |
| `tools/news_sentiment.py` | Low | ✅ Yes | Read-only HTTP GET to CryptoPanic public feed. |
| `bin/list_tasks.py` | Low | ✅ Yes | Read-only — only reads `inbox.jsonl`, never writes. |
| `bin/recap_manager.py --dry-run` | Low | ✅ Yes (dry-run only) | Read-only when `--dry-run` set. |
| `bin/archive_tasks.py --dry-run` | Low | ✅ Yes (dry-run only) | Read-only when `--dry-run` set. |
| `bin/archive_messages.py --dry-run` | Low | ✅ Yes (dry-run only) | Read-only when `--dry-run` set. |
| `bin/log_task.py` | Medium | ❌ No | Writes to `inbox.jsonl` + `logs.jsonl`. |
| `bin/update_task.py` | Medium | ❌ No | Mutates `inbox.jsonl` + appends `logs.jsonl`. |
| `bin/log_message.py` | Medium | ❌ No | Writes to `messages.jsonl`. |
| `bin/log-task.sh` | Medium | ❌ No | Wrapper for `log_task.py` (writes). |
| `bin/recap_manager.py` (no `--dry-run`) | Medium | ❌ No | Writes to `recap.jsonl`. |
| `bin/archive_tasks.py` (no `--dry-run`) | Medium | ❌ No | Mutates `inbox.jsonl` + writes to `archive/`. |
| `bin/archive_messages.py` (no `--dry-run`) | Medium | ❌ No | Mutates `messages.jsonl` + writes to `messages-archive/`. |
| `bin/create-company.sh` | Medium | ❌ No | Creates folder structure + appends to `company-index.jsonl`. |

Result: **7 entries whitelisted** (4 read-only + 3 dry-run-only). Everything that mutates state — including the task logger writers — stays gated.

---

## Hermes Config Application

The actual whitelist file lives in your Hermes installation, not in this repo. Typical path (depends on your Hermes setup):

- `~/.config/hermes/tools.yaml`
- or `/etc/hermes/tools.yaml`
- or via Hermes admin UI under "Tool Permissions"

### Recommended config shape (YAML, illustrative)

```yaml
# Hermes tool permissions for AI Holding workspace
# Generated 2026-05-17 — review before applying
workspace: /home/fatur/ai-holding

auto_approve:
  # --- Read-only tools (full auto-run) ---
  - command: python3 /home/fatur/ai-holding/tools/fear_greed.py
    risk: low
    reason: "Read-only public API (Alternative.me)"

  - command: python3 /home/fatur/ai-holding/tools/btc_price.py
    risk: low
    reason: "Read-only public API (CoinGecko)"
    args_pattern: "^(--currency \\w+|--json)?$"

  - command: python3 /home/fatur/ai-holding/tools/news_sentiment.py
    risk: low
    reason: "Read-only public API (CryptoPanic)"
    args_pattern: "^(--limit \\d+|--kind (news|media)|--json)*$"

  - command: python3 /home/fatur/ai-holding/bin/list_tasks.py
    risk: low
    reason: "Read-only — reads inbox.jsonl only"

  # --- Dry-run only (auto-run only when --dry-run is present) ---
  - command: python3 /home/fatur/ai-holding/bin/recap_manager.py
    risk: low
    require_args: ["--dry-run"]
    reason: "Read-only with --dry-run"

  - command: python3 /home/fatur/ai-holding/bin/archive_tasks.py
    risk: low
    require_args: ["--dry-run"]
    reason: "Read-only with --dry-run"

  - command: python3 /home/fatur/ai-holding/bin/archive_messages.py
    risk: low
    require_args: ["--dry-run"]
    reason: "Read-only with --dry-run"

require_confirm:
  # Everything else — explicit list discourages "approve all"
  - command: python3 /home/fatur/ai-holding/bin/log_task.py
  - command: python3 /home/fatur/ai-holding/bin/update_task.py
  - command: python3 /home/fatur/ai-holding/bin/log_message.py
  - command: bash    /home/fatur/ai-holding/bin/log-task.sh
  - command: python3 /home/fatur/ai-holding/bin/recap_manager.py   # without --dry-run
  - command: python3 /home/fatur/ai-holding/bin/archive_tasks.py   # without --dry-run
  - command: python3 /home/fatur/ai-holding/bin/archive_messages.py # without --dry-run
  - command: bash    /home/fatur/ai-holding/bin/create-company.sh

deny:
  # Catch-all: anything not listed above falls through to deny + ask
  default: ask
```

> **Important**: the YAML shape above is illustrative. Your actual Hermes might use JSON, a different field naming, or a UI form. Read your Hermes docs and translate the structure; don't copy-paste blindly.

### Per-tool argument constraints

For tools with mode flags (e.g., `--dry-run`), enforce the constraint at config level:

- `recap_manager.py` whitelisted **only** if `--dry-run` is in argv.
- `archive_tasks.py` whitelisted **only** if `--dry-run` is in argv.
- `archive_messages.py` whitelisted **only** if `--dry-run` is in argv.

If your Hermes can't enforce arg patterns, **don't** whitelist the dry-run-only tools. Keep them in `require_confirm`.

---

## Audit Trail

Whitelist activity should be logged. Recommended:

1. Hermes log file (`~/.local/share/hermes/tool-runs.log`) records every auto-run with timestamp + command + exit code.
2. **Once a week**: run `bin/list_tasks.py` against the audit log to review what auto-ran.
3. **If anything looks unexpected**: revoke the whitelist entry, debug, re-add only after fix verified.

The repo's own `logs.jsonl` only logs task lifecycle events, not Hermes tool runs. Those are different audit trails living in different places.

---

## When to Add a New Tool to the Whitelist

1. Tool is added to `tool-registry.md` with `Risk: Low` + Active.
2. Verify all 7 eligibility rules above.
3. Run the tool **manually** ≥ 5 times. Confirm:
   - Output stable and predictable.
   - No file writes (check `inotifywait` or similar if unsure).
   - No outbound mutation requests (check with `tcpdump` or your Hermes network log if paranoid).
4. Add a row to the whitelist YAML.
5. Update this file (`hermes-whitelist.md`) with the new entry + reason.
6. Update `tool-registry.md` `Whitelisted` column to `yes`.

If any of those fail, the tool stays gated.

---

## Revocation

Revoke whitelist entry **immediately** if:

- Tool's source code changes — re-evaluate eligibility before re-whitelisting.
- Tool starts hitting a different (mutating) endpoint.
- Tool starts reading secrets / env files.
- Tool starts producing observable side effects beyond stdout.
- Hermes audit log shows unexpected runs.
- API at the other end starts charging (free → paid).

After revocation: the tool falls back to `require_confirm`. Re-whitelist only after fix + re-verification.

---

## What This Document Is Not

- This is **not** a list of tools that are "safe to ignore". Every tool — whitelisted or not — is still your responsibility to audit periodically.
- This is **not** a permission system that protects against malicious code. If `fear_greed.py` itself were tampered with, Hermes would still auto-run it. Source code review is upstream of whitelist policy.
- This is **not** a substitute for `tool-use-rules.md`. Agents must still consult the registry before claiming "I can't do X".

---

## Reference

- `knowledge/tools/tool-registry.md` — canonical registry with risk levels.
- `knowledge/agent-design/tool-use-rules.md` — agent behavior when invoking tools.
- `knowledge/agent-design/task-logger-rules.md` — context for task-logger script risks.
- `knowledge/core/principles.md` — overall safety stance.
