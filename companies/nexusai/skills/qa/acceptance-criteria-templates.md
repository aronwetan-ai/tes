---
name: acceptance-criteria-templates
description: Battle-tested AC templates per feature type — agency context (multi-tenant, multi-account, OPSEC).
company: NexusAI
agent_specific: "@nexusai.qa"
parent_skill: qa
used_by: ["@nexusai.qa", "@nexusai.pm", "@nexusai.cto"]
---

# Acceptance Criteria Templates — NexusAI Deep Skill

Agent-specific extension of `skills/qa/SKILL.md`. Used by `@nexusai.qa` (and PM during scoping). AC template selection is a senior judgment call — picking the right template makes implicit requirements explicit.

Core principle: **AC must be falsifiable.** "User has good experience" is not AC. "Page loads in <2s on 3G" is.

---

## When to Use

- Picking up a new feature ticket from PM or Fathur.
- Reviewing PM-written AC before implementation starts.
- Writing AC for a feature you're QA'ing.
- Pushing back on under-specified asks.

---

## Template Picker

| Feature type | Template |
|---|---|
| User-facing CRUD endpoint | T1 (CRUD endpoint) |
| Form / data entry UI | T2 (Form UI) |
| Background job / cron | T3 (Background job) |
| External API integration | T4 (Third-party integration) |
| Multi-tenant feature (most agency work) | T5 (Multi-tenant feature) |
| AI agent feature | T6 (AI agent) |
| Migration / data backfill | T7 (Data migration) |
| Auth / security-sensitive | T8 (Auth/security) |
| Reporting / analytics | T9 (Reporting) |
| External outreach (DM / email send) | T10 (Outreach) |

Most agency features hit **T5 + one of the others** (e.g. T5 + T1 for a tenant-aware CRUD endpoint).

---

## T1 — CRUD Endpoint AC

```
GIVEN an authenticated user with role X
WHEN they POST /resource with valid body
THEN response is 201 with created resource id
AND resource is persisted correctly in DB
AND audit log records create event with user_id + timestamp

GIVEN an authenticated user with role X
WHEN they GET /resource/:id (their own)
THEN response is 200 with resource

GIVEN an authenticated user with role X
WHEN they GET /resource/:id (NOT their own / different tenant)
THEN response is 404 (not 403 — don't leak existence)

GIVEN an unauthenticated user
WHEN they hit any endpoint requiring auth
THEN response is 401 with no payload

GIVEN any user
WHEN they POST with malformed body
THEN response is 400 with structured error: {"code": "VALIDATION", "field": "...", "message": "..."}

GIVEN concurrent updates to the same resource
WHEN both submit edits within the same second
THEN one succeeds, the other gets 409 with current version
AND no data corruption (tested with version column / RLS)

PERFORMANCE
- p95 response time < 300ms under 50 RPS load
- DB query count < 5 per request
```

---

## T2 — Form UI AC

```
GIVEN the form is rendered fresh
WHEN user clicks each field tab order
THEN focus moves through fields in logical order
AND focus state is visible

GIVEN required fields are empty
WHEN user submits
THEN inline error appears under each empty field
AND submit button stays enabled (so user can retry after fix)

GIVEN field has invalid format
WHEN user blurs the field
THEN inline error appears with format hint (e.g. "name@domain.com")

GIVEN form is being submitted
WHEN request is in flight
THEN submit button is disabled
AND a loading indicator is visible
AND user cannot double-submit

GIVEN submit succeeds
WHEN response arrives
THEN form clears OR shows success state
AND a toast confirms ("Saved" / "Created")

GIVEN submit fails (network / 5xx)
WHEN response arrives
THEN form input is preserved
AND a sticky error message shows with actionable text
AND retry mechanism is available

ACCESSIBILITY
- All inputs have <label> or aria-label
- Errors announced via aria-live="polite"
- Color is not the only error signal (icon + text)
```

---

## T3 — Background Job AC

```
GIVEN the job is scheduled to run at time T
WHEN time T arrives
THEN job executes within 60s of T (cron drift acceptable)
AND completion is logged with start/end timestamp + outcome

GIVEN the job is in progress
WHEN it processes each item
THEN per-item outcome is logged
AND failures are routed to dead-letter queue (not lost)
AND backoff applied on transient errors (5 retries with exponential backoff)

GIVEN the job is killed mid-run (SIGTERM)
WHEN restarted
THEN it resumes from last completed item (idempotency / checkpoint)
AND no item is processed twice (deduplication via input hash)

GIVEN the job runs longer than expected (>2x typical duration)
WHEN duration exceeds threshold
THEN an alert fires
AND the job is killable safely

GIVEN the job is run twice with identical input (operator mistake)
WHEN both runs complete
THEN total side effect is identical to one run (idempotent)

OBSERVABILITY
- Heartbeat metric emitted every N minutes
- Per-run summary logged (items processed, duration, errors)
- Dead-letter queue has alert if non-empty for >1 hour
```

---

## T4 — Third-party Integration AC

```
GIVEN a valid client credential is configured
WHEN we call the third-party API
THEN response is parsed correctly
AND on success, our DB reflects the result

GIVEN the third-party API returns 401 (token expired)
WHEN we receive the response
THEN we attempt token refresh once
AND on refresh success, retry the original request
AND on refresh failure, mark client.connection_status="disconnected" + notify

GIVEN the third-party API returns 429 (rate limit)
WHEN we receive the response
THEN we honor Retry-After header
AND back off with exponential delay
AND do not exceed N retries per request

GIVEN the third-party API is down (5xx / timeout)
WHEN we hit the failure budget for this client
THEN we circuit-break for 5 minutes for that client
AND return graceful degradation to user
AND alert if circuit stays open >15 min

GIVEN third-party deprecates an endpoint
WHEN our calls return deprecation warnings
THEN warning is logged with severity=warn
AND we file follow-up issue to migrate

CREDENTIAL HANDLING
- Token stored only in cred_vault.py
- Never logged in any log line
- Rotated on freelancer offboarding event
- Audit log on every read of token

CONTRACT
- We pin to API version X.Y in code
- Schema changes detected via contract test (mock vs spec) in CI
```

---

## T5 — Multi-tenant Feature AC

```
GIVEN client A and client B both exist in the system
WHEN client A's user performs any action
THEN action ONLY affects client A's data
AND no row from client B is read, written, or returned

GIVEN tenant isolation is enforced via row-level security policy
WHEN a query is run without explicit client_id filter
THEN the query returns 0 rows (RLS denies, defense-in-depth)
AND test exists that proves this (regression test)

GIVEN client A's user attempts to access /api/resource/:id where id belongs to client B
WHEN request is processed
THEN response is 404 (don't leak existence)
AND audit log records cross-tenant access attempt

GIVEN client switcher is used in UI
WHEN a user with multi-client access switches from A to B
THEN session state is updated server-side, not just client-side
AND any cached data is invalidated
AND URL reflects current client

GIVEN per-client rate limit is configured
WHEN client A's traffic spikes
THEN client A is throttled
AND client B is unaffected (no shared budget exhaustion)

OBSERVABILITY
- Every log line + metric has client_id label
- Reports can be filtered/sliced by client
- Cross-tenant queries (legitimate, e.g. internal dashboards) are explicitly tagged
```

---

## T6 — AI Agent AC

```
GIVEN the agent has a defined eval set (≥20 cases)
WHEN we run the eval against the current prompt + model
THEN pass rate ≥ baseline
AND no category regresses by >2pp
AND avg cost-per-call ≤ budget threshold

GIVEN typical user input
WHEN agent processes it
THEN output matches expected schema
AND output is in expected language (e.g. id-ID for Indonesian client)

GIVEN adversarial input (prompt injection attempt)
WHEN agent processes it
THEN agent does NOT execute the injected instruction
AND output remains within original task scope
AND a flag is logged (input_flag="injection_suspected")

GIVEN out-of-scope input
WHEN agent processes it
THEN agent refuses politely with referral to correct path

GIVEN agent calls a tool
WHEN tool returns malformed output
THEN agent does NOT propagate raw tool output to user
AND falls back to "couldn't complete that, try again" or similar

COST + LATENCY
- p95 latency ≤ N seconds
- Per-call cost ≤ $X
- Daily cost cap enforced; alert at 80%, hard-stop at 100%

OBSERVABILITY
- Every call logs: input hash, prompt version, model, tool calls, tokens in/out, cost, latency, outcome
- Eval re-run on every prompt/tool/model change (CI)
```

Reference: `skills/ml-agent/prompt-eval.md`.

---

## T7 — Data Migration AC

```
GIVEN production data and migration script
WHEN script is executed
THEN row counts are reported pre/post (sanity check)
AND no data is silently lost (orphan check)

GIVEN script is executed on a copy of prod first
WHEN comparing source and destination
THEN every source row maps to either:
  - a destination row (transformed correctly)
  - a documented exclusion (with reason logged)

GIVEN script is interrupted mid-run
WHEN restarted
THEN it resumes from checkpoint
AND no row is migrated twice (idempotency)

GIVEN migration produces unexpected exclusions or warnings
WHEN over threshold (e.g. >1% of rows)
THEN script halts and reports
AND operator must explicitly continue

ROLLBACK
- Pre-migration backup taken (DB dump)
- Rollback script tested on copy of prod
- Window after migration where rollback is acceptable, with confirmation needed

TIMING
- Run on low-traffic window
- Estimated duration documented (with margin)
- If >2x estimate, alert + decide continue/abort
```

---

## T8 — Auth / Security-Sensitive AC

```
GIVEN a new user signs up
WHEN they submit credentials
THEN password is hashed with argon2 (or bcrypt cost ≥ 12) before storage
AND password is never logged anywhere

GIVEN a user logs in
WHEN credentials are correct
THEN session token is issued (HttpOnly + Secure + SameSite=Lax cookie)
AND session expires after N hours of inactivity

GIVEN a user logs in with WRONG password
WHEN response is returned
THEN response is identical to "user does not exist" (no enumeration)
AND login attempts are rate-limited per IP + per username

GIVEN MFA is enabled for the account
WHEN user logs in
THEN MFA challenge is required
AND MFA secret is stored encrypted

GIVEN a session token is leaked
WHEN we discover the leak
THEN that token can be revoked server-side
AND user is logged out

GIVEN user requests password reset
WHEN reset link is sent
THEN link expires in 30 minutes
AND link is single-use
AND old session tokens are invalidated after successful reset

OWASP CHECK
- A03 (Injection): all user input parameterized
- A05 (Misconfig): debug=False in prod, headers (HSTS, CSP, X-Frame-Options) set
- A07 (ID/Auth fail): generic error messages, rate-limit, lockout
- A09 (Logging): auth failures logged + alerted at threshold
```

Reference: `knowledge/security/owasp-top10.md`, `knowledge/software/auth-patterns.md`.

---

## T9 — Reporting / Analytics AC

```
GIVEN report config (date range, metrics, filters)
WHEN report is generated
THEN numbers match source-of-truth queries (verified via spot-check)
AND each metric has a defined formula (no implicit "what does X mean")

GIVEN client viewing their report
WHEN they apply filters
THEN data refreshes correctly
AND only their tenant's data is included (T5 also applies)

GIVEN report is exported (CSV / PDF)
WHEN export is generated
THEN content matches on-screen view
AND CSV cells are escaped against formula injection (=, +, -, @)

GIVEN data is aggregated across multiple sources (e.g. IG + Meta Ads + GA)
WHEN sources have different time zones / latency
THEN report normalizes timestamps to client's TZ
AND staleness per source is shown ("Meta Ads as of 2h ago")

PERFORMANCE
- Report renders in <3s for typical client (1 month, 5 channels)
- Heavy reports (12 months) cached or background-generated with download link
```

---

## T10 — Outreach (DM / Email Send) AC

```
GIVEN sender account is in cred_vault and warmed up
WHEN we initiate a send batch
THEN sends respect rate limit (configurable; default 30/day per IG account, 60/day per email)
AND sends are spread across configured time window with jitter
AND no two messages are identical (template + variable fill ensures variation)

GIVEN recipient is on opt-out list for this client
WHEN we attempt to send
THEN send is skipped
AND attempt is logged for compliance audit

GIVEN target platform returns rate-limit error
WHEN we receive it
THEN account is paused for cool-down period (default 24h)
AND alert fires
AND remaining recipients are routed to alternative account (if available)

GIVEN a recipient replies
WHEN reply arrives
THEN sequence pauses for that recipient
AND reply is classified (positive / negative / neutral / oos)
AND positive replies are surfaced for human handoff

GIVEN account flagged / shadowbanned
WHEN we detect (no replies in N days, action error rate up)
THEN account is quarantined
AND we do NOT continue sending from same fingerprint pattern
AND incident is logged for OPSEC review

COMPLIANCE
- Every outbound message includes opt-out path
- Opt-out is honored immediately and persisted
- Audit log contains recipient + content hash + timestamp + outcome
- For email: SPF/DKIM/DMARC pass; bounce handling; spam complaint monitoring
```

Reference: `knowledge/security/opsec-multi-account.md`, `skills/security/threat-modeling.md`.

---

## Cross-Cutting AC (apply to ALL features)

```
OBSERVABILITY
- Every error path logged with structured context (request_id, user_id, client_id)
- Every external call logged (target, latency, outcome)
- Health check endpoint exists and reflects real health, not "200 always"

DOCUMENTATION
- README updated for new endpoint / config / env var
- ADR (knowledge/software/adr-format.md) for any architecture decision
- Runbook entry for any new ops procedure

TESTING
- Unit tests for pure logic
- Integration test for tenant-isolation paths
- E2E test for critical user journey (only)
- Load test result attached if performance-sensitive

DEPLOY
- Migration script (if DB schema changed)
- Rollback plan documented
- Deployed to staging first; smoke-tested ≥15 min before prod
```

---

## Anti-Patterns

- **AC written after implementation.** That's verification, not acceptance. Write AC at scoping.
- **AC = "feature works".** Falsifiable means specific. "Works" doesn't qualify.
- **No tenant-isolation AC on multi-tenant features.** Most-frequent agency-context bug source.
- **No empty-state AC.** First-day client experiences = empty state. Don't ship apps that crash on it.
- **No failure-mode AC.** External APIs go down. AC must say what happens then.
- **AC without observability.** If you can't tell whether AC is met in prod, it's vapor.

---

## Reference

- `companies/nexusai/skills/qa/SKILL.md` (parent skill).
- `knowledge/software/code-review-checklist.md`
- `knowledge/security/owasp-top10.md`
- `knowledge/security/opsec-multi-account.md`
- `knowledge/ml/eval-methodology.md`
- `companies/nexusai/skills/ml-agent/prompt-eval.md`
- `companies/nexusai/skills/security/threat-modeling.md`
