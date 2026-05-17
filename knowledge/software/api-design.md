# API Design — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.backend`, `@nexusai.cto`, `@nexusai.frontend`

---

## REST vs gRPC vs GraphQL — When To Use What

| Style | Pick when | Avoid when |
|---|---|---|
| **REST** | Public API, third-party integrators, browser clients, simple CRUD-ish. | Real-time bidirectional, very chatty graphs of related data. |
| **gRPC** | Internal service-to-service, low-latency, strongly-typed contract. | Browser clients (needs gRPC-Web shim), public API for unknown consumers. |
| **GraphQL** | Aggregating many backends behind one client, frontend-driven schema, varied client needs. | Single backend with simple needs, public API where complexity must be limited, low-trust clients (query depth attacks). |

**Agency default**: REST for client-facing dashboards. gRPC if NexusAI grows internal microservices. GraphQL only if frontend genuinely benefits from schema-driven aggregation.

---

## URL Conventions (REST)

```
GET    /v1/clients                        # list
POST   /v1/clients                        # create
GET    /v1/clients/{id}                   # one
PATCH  /v1/clients/{id}                   # partial update
DELETE /v1/clients/{id}                   # remove
GET    /v1/clients/{id}/campaigns         # subresource list
POST   /v1/clients/{id}/campaigns:archive # action that doesn't fit CRUD
```

Rules:
- Plural nouns. Lowercase. Hyphen for word-split (`/ad-accounts`, not `/ad_accounts`).
- Version in path (`/v1/`) — bump only on breaking change.
- Actions get a `:verb` suffix (Google's convention). Don't pretend RPC is REST.
- Never use verbs in noun position (`/getClients` is wrong).

---

## HTTP Status Codes (the ones that matter)

| Code | When |
|---|---|
| 200 | Success with body. |
| 201 | Created. Include `Location` header pointing to the new resource. |
| 202 | Accepted (async); caller polls a status endpoint. |
| 204 | Success without body (DELETE typical). |
| 301 / 308 | Permanent redirect. Permalink change. |
| 400 | Client malformed input. Body contains `{code, field, message}`. |
| 401 | Not authenticated. |
| 403 | Authenticated but not authorized. |
| 404 | Not found — also use for unauthorized access to existing resource (don't leak existence). |
| 409 | Conflict (version mismatch, duplicate). |
| 410 | Gone (used to exist). |
| 422 | Unprocessable Entity — well-formed but fails business validation. |
| 429 | Rate limited. Include `Retry-After` header. |
| 500 | Server bug. Don't leak details. |
| 502 / 503 / 504 | Upstream / unavailable / timeout. |

---

## Response Envelope (NexusAI convention)

```json
// success
{ "success": true, "data": { ... }, "error": null, "meta": { "request_id": "..." } }

// error
{ "success": false, "data": null,
  "error": { "code": "VALIDATION", "field": "email", "message": "..." } }

// list
{ "success": true,
  "data": [ ... ],
  "error": null,
  "meta": { "next_cursor": "...", "has_more": true } }
```

Error `code` is **machine-readable** (UPPER_SNAKE), `message` is human-readable but English. Frontend localizes on display.

---

## Pagination

| Pattern | When |
|---|---|
| **Cursor-based** (`?cursor=abc&limit=50`) | Default. Stable under inserts. Scales to large lists. |
| **Offset** (`?page=3&size=50`) | Avoid for >10k rows; cliff after deep pages. OK for admin views. |
| **Keyset** (`?after_id=...&limit=50`) | When monotonic ID exists; cheaper than cursor. |

Cap `limit` server-side (e.g. max 100). Never trust client.

---

## Filtering & Sorting

```
GET /v1/campaigns?status=active&owner=alice&sort=-created_at&limit=50
```

- Explicit field names (`status=active`) — not generic DSL.
- `sort=field` ascending; `sort=-field` descending.
- Document allowed filter combinations + indexed columns.
- Reject unknown filter keys (don't silently ignore — caller may have a typo with consequences).

---

## Idempotency

Mutating endpoints (POST that creates) accept `Idempotency-Key` header:

```
POST /v1/campaigns
Idempotency-Key: 7e9c0f3a-...

→ Server stores (client_id, key) → response for 24h.
   Same key + same body within 24h = same response, no duplicate effect.
   Same key + different body = 422 conflict.
```

Critical for the agency: outreach send, payment trigger, third-party-API mutating call — all need idempotency.

---

## Versioning

| Change type | What to do |
|---|---|
| Add new optional field | No version bump. Document in changelog. |
| Add new endpoint | No version bump. |
| Change field type / rename / remove | Major version bump (`/v2/`). Run `/v1/` and `/v2/` parallel during sunset. |
| Change semantics of existing field (same name) | Major bump. Don't silently change. |

Sunset:
- 90-day notice minimum for paying clients.
- `Deprecation: true` and `Sunset: <RFC 2822 date>` headers per RFC 8594.
- Track usage to find clients still on old version; reach out before kill.

---

## Authentication Patterns

| Client | Pattern |
|---|---|
| Browser app, same origin | Session cookie (HttpOnly + Secure + SameSite=Lax) + CSRF token. |
| Browser SPA, cross origin | Short-lived JWT in memory; refresh via HttpOnly cookie. |
| Mobile app | Refresh token (long, secure storage) + access token (short, in memory). |
| Service-to-service | mTLS or signed JWT from internal IdP. |
| External API consumer | API key per client, scoped, rate-limited. |

See `knowledge/software/auth-patterns.md`.

---

## Rate Limiting

- Per-key budget (X requests / minute).
- 429 with `Retry-After` header on exceed.
- `X-RateLimit-Limit / -Remaining / -Reset` headers on every response.
- Different budget per endpoint class (read cheap, write expensive).
- Per-tenant separation: client A's spike doesn't deny client B (agency-critical).

---

## Webhooks (outbound)

When you call back into client systems:

- **Sign every payload**: `X-Signature: sha256=<hex>` over body using shared secret.
- **Timestamp + freshness window**: reject requests >5 min old to defeat replay.
- **Idempotency key in payload**: client must dedupe by `event_id`.
- **Retry with backoff**: 1m, 5m, 30m, 2h, 24h. Drop after.
- **At-least-once delivery**: receiver must be idempotent, not us.

---

## OpenAPI / Schema First

- Spec is source of truth — `openapi.yaml` lives in repo.
- Generate server stubs + client SDKs from spec (Stoplight, swagger-codegen, openapi-generator).
- CI checks: spec is valid + spec matches implementation (contract test).
- Versioned alongside code; PR that changes API must update spec.

---

## Anti-Patterns

- **Verbs in URL paths.** `GET /getClients` — wrong. `GET /clients`.
- **HTTP 200 for errors.** Frontend can't tell. Use proper status codes.
- **Stack traces in 500 responses.** Information disclosure. Log internally; return opaque error.
- **Filter via free-text JSON DSL.** Performance + security nightmare. Explicit fields.
- **Versioning by header for unknown public consumers.** Hard to discover. Keep version in path.
- **Mutating GET endpoints.** Breaks caching, retries, browser back-button.
- **Leaking tenant existence via 403.** Use 404 for unauthorized access to other tenants' data.
- **No `request_id` in responses.** Debugging impossible across logs.

---

## Reference

- `companies/nexusai/skills/coding/SKILL.md` (API design section).
- `knowledge/software/auth-patterns.md`
- `knowledge/software/twelve-factor.md` (config)
- Google Cloud API Design Guide (canonical reference; this file paraphrases for agency context).
