---
name: coding
description: Backend / frontend / API implementation skill for NexusAI. Specialized for cloud / SaaS / DevOps / AI agent context.
company: NexusAI
used_by: ["@nexusai.backend", "@nexusai.frontend", "@nexusai.cto"]
---

# Coding Skill — NexusAI

NexusAI's craft. Use this for any task that produces code or technical design.

This skill inherits NexusAI SOUL (engineering-precise, pragmatic, zero fluff). It is NOT generic — it assumes SaaS / cloud / API context.

## When to Use

- API design (REST / GraphQL / gRPC).
- Database schema and queries.
- Backend business logic.
- Frontend UI implementation.
- Refactoring existing code.
- Debugging production issues.
- Code review.

## Process

1. **Read context first.** Existing code, existing patterns. No drive-by refactors.
2. **Clarify spec.** Input / output / contract / constraint.
3. **Pick approach.** State minimum 2 options + trade-off, choose with reasoning.
4. **Implement.** Working code beats perfect code.
5. **Validate.** Runs as written? Edge cases? Dependencies clear?
6. **Document inline + at handoff.**

## Rules

1. Identify root cause before fix. No symptom-patching.
2. Prefer boring tech (Postgres > new NoSQL, React > newest framework).
3. No hardcoded secrets. Ever. Loop in `@nexusai.security` for crypto / auth.
4. Handle errors that are realistic. Don't swallow exceptions.
5. Function names describe behavior; variable names describe content.
6. Tests are mandatory for shared code, optional for one-offs.

## Output Format

For implementation:
```
[GOAL]         What we're building
[APPROACH]     Chosen approach + why (1-2 lines)
[CODE]         Code block, language-tagged, with comments on tricky parts
[DEPENDENCIES] What needs to be installed / configured
[EDGE CASES]   What's handled, what's NOT (and why)
[NEXT STEP]    Test, deploy, integrate
```

For debugging:
```
[PROBLEM]      Observed behavior
[CAUSE]        Root cause (verified, not guessed)
[FIX]          Specific change
[VERIFICATION] How to confirm fix works
```

For API design:
```
[ENDPOINT]    METHOD /path
[PURPOSE]     One line
[INPUT]       Schema + example
[OUTPUT]      Schema + example (uses NexusAI standard envelope)
[ERRORS]      Possible codes + when fired
[AUTH]        Required level
[NOTES]       Edge cases, perf, deps
```

## API Standard (NexusAI)

Per `knowledge/software/software-development-sop.md`:

```json
// success
{ "success": true, "data": { ... }, "error": null, "meta": {...} }

// error
{ "success": false, "data": null, "error": { "code": "...", "message": "..." } }
```

## Cross-Skill / Cross-Agent

- Infra / deploy concerns → `@nexusai.devops` + `skills/devops`.
- Security review for auth / crypto → `@nexusai.security`.
- AI agent / prompt design → `@nexusai.ml`.
- Test plans → `@nexusai.qa` + `skills/qa`.
- UI components → `skills/uiux`.

## What This Skill Does NOT Cover

- Marketing copy. Use `@brandflow.copywriter`.
- Crypto research. Use `@crypto.*`.
- Pure infrastructure work. Use `skills/devops`.

## Senior Patterns (Deep Dive)

### Architecture decisions (decision tree)

```
New module / service?
├─ Belongs to existing bounded context? → extend existing service.
├─ Crosses 2+ existing contexts? → push back, redesign.
└─ New context? → new service.

Stateless vs stateful?
├─ Read-mostly + cacheable? → stateless + Redis.
├─ Write-heavy + transactional? → stateful + Postgres + careful tx boundary.
└─ Stream-of-events? → append-only log + projection.

Sync vs async?
├─ User waits for result? → sync (HTTP, gRPC).
├─ Result delivered later? → async (queue, webhook).
└─ Long-running with progress? → sync ack + status endpoint + WebSocket/poll.
```

Reference: `knowledge/software/clean-architecture.md`, `knowledge/software/ddd-cheatsheet.md`, `knowledge/software/cap-and-consistency.md`.

### Multi-tenant patterns (agency context — multiple clients)

For any service that handles multiple clients (most of NexusAI's output):

| Isolation level | When to use | Tradeoff |
|---|---|---|
| Row-level (`client_id` column + filter) | Default. Cheap. Fast. | One bug = data leak across clients. Test rigorously. |
| Schema-level (one Postgres schema per client) | Sensitive client data, regulated workloads. | Migration overhead × N. |
| Database-level (one DB per client) | Compliance / SLA differentiation. | Operational overhead high. |

**Default for agency work**: row-level + middleware that enforces `client_id` from auth context, never from request body. Add a Postgres RLS policy as defense-in-depth.

```python
# WRONG — client_id from body, attacker can forge
@app.post("/contacts")
def create(req): return db.insert("contacts", client_id=req.client_id, ...)

# RIGHT — client_id from authenticated context
@app.post("/contacts")
def create(req, ctx: AuthContext = Depends(auth)):
    return db.insert("contacts", client_id=ctx.client_id, ...)
```

### Error handling patterns

Three categories — handle differently:

1. **Programmer errors** (logic bug, type error, null deref). → Crash loud. Don't catch. Let monitoring see.
2. **Operational errors** (network down, DB unavailable, rate limit). → Catch, retry with backoff, circuit-break, surface to user as 5xx with stable error code.
3. **Business errors** (invalid input, not authorized, conflict). → Return 4xx with clear message and `error.code` machine-readable.

```python
# DON'T catch-all
try: do_thing()
except Exception: pass  # silent swallowing — bug guaranteed

# DO let it bubble unless handling is meaningful
try: external_api.call()
except RequestTimeout: return retry_with_backoff()  # operational
except ValidationError as e: return error_response(400, "VALIDATION", e.detail)  # business
```

### Database transaction patterns

- **Read your writes**: stick to a single connection across a request when consistency matters; explicit `BEGIN`/`COMMIT`.
- **Avoid open transactions across HTTP calls**. Locks held during external I/O = lock storm.
- **Idempotency keys** for any mutation that the client might retry (per `knowledge/software/api-design.md`).
- **Optimistic concurrency** (`version` column) for low-contention edits. Pessimistic lock only for high-contention hot rows.
- Reference: `knowledge/software/postgres-prod.md`.

### API contract patterns

- **Versioning**: `/v1/...` in path. Bump on breaking change only. Additive changes don't bump.
- **Deprecation**: `Deprecation` header + `Sunset` header per RFC 8594. Document in CHANGELOG. 90-day notice minimum for paying clients.
- **Pagination**: cursor-based (`?cursor=...&limit=50`) > offset (deep pagination performance cliff).
- **Filtering**: explicit fields (`?status=active&owner=...`) > generic query DSL (security + perf nightmare).
- **Idempotency**: `Idempotency-Key` header on POST that mutates. Server stores result keyed by `(client_id, idempotency_key)` for 24h.
- Reference: `knowledge/software/api-design.md`.

### Boring tech baseline (NexusAI defaults)

| Concern | Default | When to deviate |
|---|---|---|
| RDBMS | Postgres 15+ | Need full-text + spatial → still Postgres. Need >100k writes/sec → only then consider alternatives. |
| Cache | Redis | Need persistent KV with replication SLA → KeyDB, but rarely. |
| Queue | Postgres `LISTEN/NOTIFY` for <1k/s; Redis Streams for higher | Kafka only when >50k events/sec sustained. |
| Auth | Session cookie + CSRF for browser; JWT (short-lived) + refresh for SPA/mobile | Per `knowledge/software/auth-patterns.md`. |
| Backend lang | Python (FastAPI) or TypeScript (Node, Hono) | Match team skill. |
| Frontend | Next.js + Tailwind for SaaS | Plain Vite + React for dev tools. |
| Container runtime | Docker Compose dev / single-VM prod with systemd | K8s only when scaling team beyond 10 services. |
| Observability | OpenTelemetry → Grafana stack OR Datadog | Per `knowledge/software/observability.md`. |

### Anti-patterns NexusAI explicitly rejects

- **Premature microservice split.** Start as a monolith. Split only along bounded contexts that have proven independent change rate.
- **ORM-only data access for hot paths.** ORM for CRUD; raw SQL for reports / aggregates / hot loops.
- **Sync HTTP cascade.** Service A → B → C → D in one request = latency multiplier. Async fan-out or denormalize.
- **Universal `BaseException` catch.** Hides bugs, kills observability.
- **God objects / 500-line classes.** Refactor at 200 lines / 5 responsibilities.
- **Leaking abstractions.** Repository returns ORM model, controller returns ORM model — now your API contract is your DB schema. Map at the boundary.

## Reference

- `knowledge/software/software-development-sop.md`
- `knowledge/software/clean-architecture.md`
- `knowledge/software/ddd-cheatsheet.md`
- `knowledge/software/api-design.md`
- `knowledge/software/postgres-prod.md`
- `knowledge/software/auth-patterns.md`
- `knowledge/software/cap-and-consistency.md`
- `knowledge/software/code-review-checklist.md`
- `companies/nexusai/SOUL.md`
- `companies/nexusai/agents/backend.md`, `agents/cto.md`
