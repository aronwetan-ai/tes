# Tool Registry — AI Holding

Versi: 1.4
Update terakhir: 2026-05-17 (post Update 12 — Crypto Consultant deepening)
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
Declined-tools scope: lihat `knowledge/scope/declined-tools.md` untuk hal yang tidak dibangun.

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
| 013 | json_schema_check.py | Low     | Active   | Yes         | Auto            |
| 014 | markdown_lint.py     | Low     | Active   | Yes         | Auto            |
| 015 | dep_audit.py         | Low     | Active   | Yes         | Auto            |
| 016 | api_health.py        | Low     | Active   | Yes         | Auto            |
| 017 | prompt_eval.py       | Low     | Active   | Yes         | Auto            |
| 018 | cred_vault.py        | Medium  | Active   | Read-only sub-cmds | User confirm |
| 019 | secret_scanner.py    | Low     | Active   | Yes         | Auto            |
| 020 | exif_extract.py      | Low     | Active   | Yes         | Auto            |
| 021 | reverse_image_lookup.py | Low  | Active   | Yes (no `--open`) | Auto      |
| 022 | osint_lookup.py      | Low     | Active   | Yes         | Auto            |
| 028 | price_scraper.py     | Low     | Active   | Yes         | Auto            |
| 029 | news_scraper.py      | Low     | Active   | Yes         | Auto            |
| 030 | pattern_detector.py  | Low     | Active   | Yes         | Auto            |
| 031 | onchain_metrics.py   | Low     | Active   | Yes         | Auto            |
|| 032 | funding_rates.py     | Low     | Active   | Yes         | Auto            |
|| 033 | llm_client.py        | Medium  | Active   | No          | User confirm    |

Note on numbering: TOOL-023 through TOOL-027 are reserved for Update 11 (BrandFlow — utm_builder, readability_check, brand_voice_lint, content_scheduler, social_monitor; PR #8 pending merge to main). Update 12 (Crypto Consultant) takes 028-032. Update 13 (SUPERAGENT v2 cherry-pick) takes 033. When PR #8 merges, the table sections will conflict-merge cleanly.

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

### TOOL-013 — JSON Schema Validator
Name        : json_schema_check.py
Path        : /home/fatur/ai-holding/tools/json_schema_check.py
Command     : python3 /home/fatur/ai-holding/tools/json_schema_check.py --schema schema.json --data data.json [--recursive] [--stdin] [--quiet]
Purpose     : Validate JSON files against a JSON Schema. Stdlib fallback when `jsonschema` lib unavailable.
Output      : Per-file PASS/FAIL with error detail; summary count.
Used by     : `@nexusai.qa`, `@nexusai.backend`, `@nexusai.ml` (validate agent JSON output), task logger contract checks.
Risk        : Low — read-only local FS, no network.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto

Exit code: 0 = all valid; 1 = at least one invalid; 2 = arg/IO error.

---

### TOOL-014 — Markdown Linter
Name        : markdown_lint.py
Path        : /home/fatur/ai-holding/tools/markdown_lint.py
Command     : python3 /home/fatur/ai-holding/tools/markdown_lint.py [paths] [--max-line N] [--root .] [--fail-on info|warning|error] [--quiet]
Purpose     : Lint Markdown for doc quality (heading hierarchy, broken internal links, trailing whitespace, tabs, unclosed code fences, blank-line runs, line length).
Output      : Per-issue line `path:line [level] msg`; summary count.
Used by     : `@nexusai.writer`, `@nexusai.qa`, doc reviewers, CI.
Risk        : Low — read-only local FS, no network.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto

---

### TOOL-015 — Dependency Audit
Name        : dep_audit.py
Path        : /home/fatur/ai-holding/tools/dep_audit.py
Command     : python3 /home/fatur/ai-holding/tools/dep_audit.py [--workdir DIR] [--only python|node] [--json]
Purpose     : Wrap pip / npm dep auditors. Surface outdated + vulnerable. Read-only.
Output      : Human report (default) or JSON; lists outdated packages + vulnerability counts.
Used by     : `@nexusai.devops`, `@nexusai.security`, weekly cron, pre-release.
Risk        : Low — auditors only inspect lockfiles, never modify.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto

Notes:
- Falls back gracefully if `pip-audit` not installed.
- Skips `node` audit if no `package.json` in workdir.
- Exit 0 = no issues, 1 = issues found, 2 = arg error.

---

### TOOL-016 — API Health Check
Name        : api_health.py
Path        : /home/fatur/ai-holding/tools/api_health.py
Command     : python3 /home/fatur/ai-holding/tools/api_health.py URL [--expect-status N] [--expect-substring S] [--max-latency-ms N] [--header 'Name: Value'] [--runs N] [--timeout S] [--json]
Purpose     : Single-endpoint GET probe. Reports status, p50/p95/max latency over N runs.
Output      : Human report or JSON; nonzero exit if expectations fail.
Used by     : `@nexusai.devops`, `@nexusai.qa`, post-deploy smoke test.
Risk        : Low — single GET to user-supplied URL, no write.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto
Depends on  : Python 3 stdlib only (urllib).

---

### TOOL-017 — Prompt Eval Runner
Name        : prompt_eval.py
Path        : /home/fatur/ai-holding/tools/prompt_eval.py
Command     : python3 /home/fatur/ai-holding/tools/prompt_eval.py --cases cases.yaml --outputs outputs.json [--baseline baseline.json] [--regression-threshold 0.02] [--json]
Purpose     : Run deterministic graders against AI agent outputs to compute eval pass rate. Detects regression vs baseline.
Output      : Per-category pass rate, regression flag, list of failing cases.
Used by     : `@nexusai.ml`, `@nexusai.qa`, CI on prompt-change PR.
Risk        : Low — local FS only, NO LLM calls (you produce outputs separately).
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto

10 grader types: regex, regex_must_not, must_contain, must_not_contain, must_not_contain_any, length_max, length_min, json_valid, json_has_keys, exact.

Reference: `companies/nexusai/skills/ml-agent/prompt-eval.md`, `knowledge/ml/eval-methodology.md`.

---

### TOOL-018 — Credential Vault
Name        : cred_vault.py
Path        : /home/fatur/ai-holding/tools/cred_vault.py
Command     : python3 /home/fatur/ai-holding/tools/cred_vault.py {keygen|init|set|get|list|delete|rotate|audit|export} ...
Purpose     : Encrypted per-client credential vault (AES-256-GCM via `cryptography` lib). Audit-logs every read.
Output      : Per subcommand; `get` prints plaintext value to stdout for piping.
Used by     : `@nexusai.security`, all automation that touches client credentials.
Risk        : Medium — writes encrypted vault file + audit log; never logs plaintext.
Status      : Active (post Update 10)
Whitelisted : Read-only sub-commands (`list`, `audit`, `keygen`) yes; mutating sub-commands (`init`, `set`, `delete`, `rotate`, `export`, `get`) require user confirm.
Approval    : Mixed per sub-command
Depends on  : `cryptography` package; `AI_VAULT_KEY` env var (or `AI_VAULT_KEY_FILE`).

Subcommand risk profile:
- `keygen`        — Low (prints, never persists). Whitelistable.
- `list` / `audit` — Low (read-only). Whitelistable.
- `init` / `set` / `delete` / `rotate` — Medium (writes vault). Confirm.
- `get` — Medium (reads + appends audit; secret printed to stdout). Confirm.
- `export` — Medium (encrypted blob, but exposes scope). Confirm.

Reference: `knowledge/security/opsec-multi-account.md`.

---

### TOOL-019 — Secret Scanner
Name        : secret_scanner.py
Path        : /home/fatur/ai-holding/tools/secret_scanner.py
Command     : python3 /home/fatur/ai-holding/tools/secret_scanner.py [paths] [--staged] [--since rev..rev] [--json] [--quiet]
Purpose     : Scan files for credential / secret leak patterns (AWS, GCP, GitHub, Slack, Stripe, Anthropic, OpenAI, Meta, JWT, private keys, generic high-entropy).
Output      : Per-finding line `path:line [pattern] desc: snippet`; summary count.
Used by     : `@nexusai.security`, pre-commit hook, CI on every PR.
Risk        : Low — read-only local FS / git inspection, no network.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto

Annotations:
- Add `# secret-scanner: ignore` or `# pragma: allowlist secret` on a line to skip.
- Exit 0 = no findings, 1 = findings present (CI block).

Reference: `knowledge/security/opsec-multi-account.md`, `knowledge/security/owasp-top10.md` (A02).

---

### TOOL-020 — EXIF Extractor
Name        : exif_extract.py
Path        : /home/fatur/ai-holding/tools/exif_extract.py
Command     : python3 /home/fatur/ai-holding/tools/exif_extract.py FILE [FILE...] [--json]
Purpose     : Extract EXIF metadata from image files. GPS DMS→decimal conversion; Pillow preferred, stdlib JPEG fallback.
Output      : Human or JSON; common tags + GPS lat/lon + size + format.
Used by     : `@nexusai.security`, OSINT investigations, agency due-diligence on uploaded images.
Risk        : Low — read-only local FS, no network.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto
Depends on  : Pillow (preferred) or stdlib only (limited to JPEG basic tags).

Reference: `knowledge/scope/declined-tools.md` (substitute for face recognition).

---

### TOOL-021 — Reverse Image Lookup URL Builder
Name        : reverse_image_lookup.py
Path        : /home/fatur/ai-holding/tools/reverse_image_lookup.py
Command     : python3 /home/fatur/ai-holding/tools/reverse_image_lookup.py {--url URL | --file PATH} [--engines list] [--open] [--json]
Purpose     : Build reverse-image-search URLs for Google Lens / Yandex / TinEye / Bing / SauceNAO. For local files: prints upload pages + sha256/sha1/md5 fingerprint.
Output      : Per-engine URL; with `--open`, opens browser tab.
Used by     : `@nexusai.security`, OSINT investigations.
Risk        : Low — generates URLs and optionally opens browser; no scraping.
Status      : Active (post Update 10)
Whitelisted : Yes when no `--open` flag (plain URL generation = read-only). With `--open` requires confirm (browser action is user-visible side effect).
Approval    : Auto for URL generation; confirm if `--open`.

Reference: `knowledge/scope/declined-tools.md` (substitute for face recognition).

---

### TOOL-022 — OSINT Identifier Lookup
Name        : osint_lookup.py
Path        : /home/fatur/ai-holding/tools/osint_lookup.py
Command     : python3 /home/fatur/ai-holding/tools/osint_lookup.py {--phone N | --email E | --username U} [--probe] [--probe-timeout S] [--json]
Purpose     : Build OSINT lookup URLs for phone / email / username; for username, optionally HEAD-probe ~30 platforms (Sherlock-style).
Output      : Per-source URL; with `--probe`, list of platforms where username exists.
Used by     : `@nexusai.security`, agency due-diligence, investigations.
Risk        : Low — URL generation + HEAD probes against public profile URLs.
Status      : Active (post Update 10)
Whitelisted : Yes
Approval    : Auto
Depends on  : Python 3 stdlib only (urllib, ThreadPoolExecutor).

Reference: `knowledge/scope/declined-tools.md` (substitute for face recognition).

---

### TOOL-028 — Multi-Asset Price Scraper

Name        : price_scraper.py
Path        : /home/fatur/ai-holding/tools/price_scraper.py
Command     : python3 /home/fatur/ai-holding/tools/price_scraper.py --coin <ids> [--days N] [--vs usd|idr|eur] [--ohlc] [--output FILE] [--json]
Purpose     : Multi-asset OHLCV history from CoinGecko public API. Outputs price + market cap + volume per timestamp; or true OHLC candles via --ohlc.
Output      : Human summary (default), JSON via --json, or CSV/JSON file via --output.
Used by     : `@crypto.market`, `@crypto.research`, `@crypto.onchain` (input to pattern_detector.py).
Risk        : Low — read-only HTTP GET to public API; no key, no mutation.
Status      : Active (post Update 12)
Whitelisted : Yes — read-only, bounded cost
Approval    : Auto
Depends on  : Internet, CoinGecko API (free tier, ~10-30 calls/min limit; tool sleeps 1.5s between multi-coin calls).

Notes:
- Max ~365 days on free tier; tool clamps and warns if exceeded.
- Multi-coin: comma-separated, e.g. `--coin bitcoin,ethereum,solana`.
- For pattern detection requiring 1400 bars (200W MA), accumulate multiple scrapes or use OHLC weekly endpoints.

Reference: `knowledge/crypto/cycle-indicators.md`, `companies/crypto-consultant/skills/pattern-recognition/SKILL.md`.

---

### TOOL-029 — Crypto News Scraper

Name        : news_scraper.py
Path        : /home/fatur/ai-holding/tools/news_scraper.py
Command     : python3 /home/fatur/ai-holding/tools/news_scraper.py [--source slugs] [--keyword kw1,kw2] [--since YYYY-MM-DD] [--limit N] [--sentiment-only X] [--json]
Purpose     : Multi-source crypto news RSS aggregator with keyword filter + naive sentiment classification (positive/neutral/negative/critical). Sources: CoinDesk, CoinTelegraph, Decrypt, TheBlock, Bitcoin Magazine.
Output      : Per-headline date + source + title + sentiment marker + summary stats. JSON for full payload.
Used by     : `@crypto.research` (narrative scan), `@crypto.macro` (event flagging), `@crypto.report` (citation candidates with T4 source tier disclaimer).
Risk        : Low — read-only HTTP GET to public RSS feeds; no key.
Status      : Active (post Update 12)
Whitelisted : Yes
Approval    : Auto
Depends on  : Internet, public RSS feeds (subject to feed availability).

Notes:
- Sentiment is **keyword heuristic, directional only** — explicit disclaimer in output. Pair with human review.
- News sources are **tier T4** per `knowledge/crypto/news-source-rubric.md` — citable for news, NOT for primary analytical claims.
- Keyword filter is OR-match across title+summary.

Reference: `knowledge/crypto/news-source-rubric.md`, `companies/crypto-consultant/skills/research/SKILL.md`.

---

### TOOL-030 — Pattern Detector (OHLCV)

Name        : pattern_detector.py
Path        : /home/fatur/ai-holding/tools/pattern_detector.py
Command     : python3 /home/fatur/ai-holding/tools/pattern_detector.py --input FILE --pattern <name> [--json] [--fail-on-fire]
Purpose     : Detect cycle / structural patterns over OHLCV time series. Patterns: pi_top, btc_bottom, mayer_low, mayer_high, golden_cross, death_cross, mvrv_zone (proxy), cycle_phase (aggregate), all.
Output      : Per-pattern read with current state, threshold, firing/not, base rate, invalidation, tier, reference.
Used by     : `@crypto.market`, `@crypto.research`, `@crypto.onchain` (consumes price_scraper.py output).
Risk        : Low — read-only local file processing; no network.
Status      : Active (post Update 12)
Whitelisted : Yes
Approval    : Auto
Depends on  : Python 3 stdlib only; price_scraper.py JSON or CSV.

Notes:
- Patterns are PROBABILISTIC; sample sizes small (N=3-4 cycles). Pattern firing = signal to investigate, not directive to act.
- MVRV-Z is **proxy** (price/200D MA z-score); true MVRV-Z requires Glassnode realized-cap data — disclaimer in output.
- 200W MA (btc_bottom) requires ~1400 daily bars; falls back to INSUFFICIENT_DATA for shorter scrapes.
- Senior interpretation per `companies/crypto-consultant/skills/pattern-recognition/SKILL.md` required.

Reference: `knowledge/crypto/cycle-indicators.md`, `companies/crypto-consultant/skills/pattern-recognition/cycle-models.md`.

---

### TOOL-031 — On-Chain Metrics Aggregator

Name        : onchain_metrics.py
Path        : /home/fatur/ai-holding/tools/onchain_metrics.py
Command     : python3 /home/fatur/ai-holding/tools/onchain_metrics.py --metric <name> [--protocol slug] [--chain name] [--json]
Purpose     : Public on-chain metric aggregator. Metrics: hashrate (BTC, blockchain.info), mempool (BTC, mempool.space), blockchain (BTC stats), tvl (DefiLlama; total/protocol/chain), stablecoin (DefiLlama), all.
Output      : Per-metric snapshot with source + interpretation hint + timestamp.
Used by     : `@crypto.onchain` (network health, DeFi reads), `@crypto.research`, `@crypto.market`.
Risk        : Low — read-only HTTP GET to public APIs; no key.
Status      : Active (post Update 12)
Whitelisted : Yes
Approval    : Auto
Depends on  : Internet, blockchain.info / mempool.space / DefiLlama (free APIs).

Notes:
- Free APIs only. **Whale-level / cohort-level** metrics require paid data (Glassnode, Nansen) — tool surfaces this in disclaimer.
- See `companies/crypto-consultant/skills/onchain/whale-tracking-playbook.md` for paid-data substitution patterns.
- TVL: `--protocol aave` for protocol-specific; `--chain ethereum` for chain-specific; no flag for total.

Reference: `knowledge/crypto/onchain-metrics-glossary.md`, `companies/crypto-consultant/skills/onchain/SKILL.md`.

---

### TOOL-032 — Perp Funding Rates + Open Interest

Name        : funding_rates.py
Path        : /home/fatur/ai-holding/tools/funding_rates.py
Command     : python3 /home/fatur/ai-holding/tools/funding_rates.py [--symbol BTCUSDT] [--exchanges binance,bybit] [--limit N] [--include-oi] [--json]
Purpose     : Perpetual futures funding rate history + open-interest snapshot from Binance Futures + Bybit public APIs. Annotates each exchange with funding-zone label per derivatives-glossary.md.
Output      : Per-exchange summary (latest funding, mean/max/min, zone label), full history, optional OI snapshot, live mark/index price.
Used by     : `@crypto.market` (derivatives lens), `@crypto.research` (3-lens convergence), `@crypto.risk` (positioning context).
Risk        : Low — read-only HTTP GET to public exchange APIs; no positions, no orders, no key.
Status      : Active (post Update 12)
Whitelisted : Yes
Approval    : Auto
Depends on  : Internet, Binance Futures + Bybit public endpoints.

Notes:
- Default symbol BTCUSDT; common alternatives: ETHUSDT, SOLUSDT.
- Default --limit 30 (~10 days of 8h funding intervals).
- Sustained funding extremes ≠ immediate reversal — combine with other lenses.
- Zone labels per `knowledge/crypto/derivatives-glossary.md`.

Reference: `knowledge/crypto/derivatives-glossary.md`, `companies/crypto-consultant/skills/market-analysis/SKILL.md` Senior Patterns (derivatives overlay).

---

### TOOL-033 — LLM Multi-Provider Client

Name        : llm_client.py
Path        : /home/fatur/ai-holding/tools/llm_client.py
Command     : python3 /home/fatur/ai-holding/tools/llm_client.py --provider <name> --message "..." [--system "..."] [--model override] [--json]
Purpose     : Unified client untuk 6 LLM providers (Anthropic, OpenAI, Groq, Kimi, DeepSeek, OpenRouter)
Output      : LLM response text (default) atau JSON dengan metadata
Used by     : @nexusai.ml, @nexusai.backend, @brandflow.copywriter, @crypto.research, all agents needing inference
Risk        : Medium — network call to external API, requires API key, token cost
Status      : Active (post Update 13 — SUPERAGENT v2 cherry-pick)
Whitelisted : No — external API call, requires user confirm + API key setup
Approval    : User confirm (first time setup); auto after env vars configured
Depends on  : Internet, requests library, API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, KIMI_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY)

Providers:
- anthropic: Claude Sonnet 4 (best reasoning)
- openai: GPT-4o (general purpose)
- groq: Llama 3.1 70B (ultra-fast)
- deepseek: DeepSeek Chat (cost-effective)
- kimi: Moonshot v1 128k (long context)
- openrouter: Multi-model gateway (flexibility)

Setup:
```bash
# Create .env in workspace root
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GROQ_API_KEY=gsk_...
# etc.
```

CLI examples:
```bash
python tools/llm_client.py --provider anthropic --message "Halo"
python tools/llm_client.py --provider groq --system "Anda asisten Indonesia" --message "Apa kabar?"
python tools/llm_client.py --provider deepseek --message "..." --json
```

Python import:
```python
from tools.llm_client import call_llm
result = call_llm("Halo", provider="anthropic")
```

Reference: `knowledge/ml/llm-providers.md` (provider selection guide), `update/v2/openclaw/skills/m7.md` (source).

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
