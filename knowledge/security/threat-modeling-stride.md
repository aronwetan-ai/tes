# Threat Modeling — STRIDE Reference

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.security`, `@nexusai.cto`, `@nexusai.backend`

Quick reference for STRIDE-based threat modeling. Companion to `companies/nexusai/skills/security/threat-modeling.md` (which has methodology). This file = lookups + concrete examples.

---

## STRIDE Recap

| Letter | Threat | Property violated |
|---|---|---|
| **S** | Spoofing | Authenticity |
| **T** | Tampering | Integrity |
| **R** | Repudiation | Non-repudiation |
| **I** | Info Disclosure | Confidentiality |
| **D** | DoS | Availability |
| **E** | Elevation of Privilege | Authorization |

Apply per component / per data flow.

---

## S — Spoofing (Pretending to Be Someone)

| Asset / Surface | Concrete attack | Mitigation |
|---|---|---|
| User account | Stuffing (leaked creds from other site). | MFA, per-user breach detection, rate limit. |
| Service-to-service | Forged JWT via stolen signing key. | Short-lived tokens, key rotation, signature verify, mTLS. |
| External webhook | Attacker calls our webhook endpoint posing as Meta. | Signature verify (HMAC), timestamp + nonce. |
| Email / domain | Phishing pretending to be us. | SPF + DKIM + DMARC. |
| Operator / freelancer | Stolen SSH key / GitHub token. | Hardware key (FIDO2), session bind to device, audit. |
| Client account hijack | Stolen IG cookie used to manipulate client's account in our system. | Session bind to fingerprint, anomaly detection. |

---

## T — Tampering (Modifying Data)

| Asset / Surface | Concrete attack | Mitigation |
|---|---|---|
| Data in transit | MITM modifies HTTP. | TLS only. HSTS. Cert pinning for mobile. |
| Data at rest | Attacker writes to DB via SQL injection. | Parameterized queries. Read-only DB user where possible. |
| File integrity | Container layer swapped on registry. | Image signing (cosign), verify before pull. |
| Webhook payload | Attacker forges webhook body. | HMAC signature in header. |
| Config / state | Attacker writes to config file. | File permissions, audit log, signed config. |
| Audit log | Attacker erases trail. | Append-only log. Off-host archive. |

---

## R — Repudiation (Denying Action)

| Asset / Surface | Concrete attack | Mitigation |
|---|---|---|
| Privileged action | "I never deleted that data." | Audit log: who, when, what, IP, UA. Immutable. |
| Outreach send | Client claims "you spammed me without consent." | Per-recipient consent record + send log + opt-out trail. |
| Payment trigger | "You charged me twice." | Idempotency key + transaction ID + receipt. |
| Code change | "I never approved that PR." | Signed commits + review log + branch protection. |
| Credential read | "Someone else accessed the vault." | `cred_vault.py` access log, per-credential. |

Audit log discipline:
- Immutable (append-only, separate storage).
- Reviewed quarterly even when no incident.
- Retained per policy (typically ≥1 year).

---

## I — Info Disclosure (Reading What You Shouldn't)

| Asset / Surface | Concrete attack | Mitigation |
|---|---|---|
| Cross-tenant data | Tenant A's query returns Tenant B's row (broken access control). | Tenant filter at boundary + RLS. |
| Error messages | Stack trace exposes internal paths, queries, dep versions. | Generic 5xx; full detail in logs. |
| Logs | Token / password / PII in log. | Field-level redaction. Pre-deploy log review. |
| Backups | Snapshot in public S3 bucket. | Bucket policy review. KMS encryption. |
| Cache | Cached response served to wrong user (cache key missed user_id). | Cache key includes tenant + user. |
| Browser DevTools | Sensitive in client-side state, accessible via console. | Don't ship secrets to client. Server-side only. |
| Side channel | Timing attack reveals which field is wrong on login. | Constant-time compare. |
| Prompt injection extracting prior context | Adversarial input in scraped content asks AI to leak system prompt. | Capability segregation + output validation. See `skills/ml-agent/prompt-eval.md`. |

---

## D — Denial of Service (Blocking Legitimate Use)

| Asset / Surface | Concrete attack | Mitigation |
|---|---|---|
| API endpoint | Attacker floods with requests. | Rate limit per key + per IP. WAF. |
| Compute resource | Slow-loris / Slowloris / Slowdown attacks holding connections. | Connection timeout + max-conn per IP. Reverse proxy front. |
| Database | Expensive query (no LIMIT, table scan) repeated. | Query timeout. Slow-query log. RBAC restrict. |
| Disk | Attacker uploads huge files until disk full. | Per-user quota. Pre-flight content-length check. |
| Cost | Attacker triggers expensive LLM calls in loop. | Per-user / per-tenant cost cap. Hard daily ceiling. |
| External API | Attacker burns our shared rate limit on Meta API. | Per-tenant budget. Circuit breaker. |
| Email reputation | Bot-driven account creation triggers spam complaints. | CAPTCHA on signup. Email verification before activation. |
| Account lockout DoS | Attacker triggers lockout on victim by repeated wrong passwords. | Combine rate limit with secondary signal (CAPTCHA, MFA). |

---

## E — Elevation of Privilege (Gaining Capabilities)

| Asset / Surface | Concrete attack | Mitigation |
|---|---|---|
| Vertical (user → admin) | Body parameter `role=admin` accepted on signup. | Role assigned server-side only. |
| Horizontal (user → other user) | Forced browsing or IDOR. | AuthZ check on every action. |
| Cross-tenant | Tenant A user becomes Tenant B admin. | Tenant scope derived from auth context, never client. |
| OAuth scope | Token granted scope X used to access scope Y. | Scope-validate on every action. |
| RCE | File upload with exec name → exec path. | Disallow exec extensions, isolate uploads (separate dir, no exec mount). |
| Container escape | RCE → escape to host. | Drop CAPS, read-only root, seccomp profile, no `--privileged`. |
| Internal service unauthenticated | Internal API assumed safe; no auth. Network breached → game over. | mTLS or JWT on every internal call. Zero-trust. |
| Dependency confusion | Public package with same name as internal one fetched. | Scope packages, lock file, private registry first. |

---

## Trust Boundary Checklist (per data flow)

When drawing the data-flow diagram, mark every boundary:

```
[ ] External user → public app    (untrusted in)
[ ] Public app → internal service (semi-trusted, authN/authZ)
[ ] Service → DB                  (trusted, but authZ scoped)
[ ] App → external API            (outbound; their response is untrusted)
[ ] Operator → infra              (human factor: phishing, mistake)
[ ] Freelancer → repo / vault     (scoped trust; minimal privilege)
[ ] AI agent → user input         (untrusted; capability segregation)
[ ] AI agent → tool calls         (validated input/output schema)
```

Threats cluster at boundaries.

---

## Multi-Tenant SaaS — Common Threats Quick-Reference

(Pulled from `companies/nexusai/skills/security/threat-modeling.md`.)

1. **Cross-tenant data leak** (I) — `findById` skips client filter.
2. **Credential leak via log** (I) — exception logger dumps body with token.
3. **Webhook replay** (T / R) — capture+replay external signal.
4. **Token reuse after rotation** (S / E) — old token still works.
5. **OAuth scope overreach** (E) — accept token with surplus scope.
6. **Freelancer offboarding gap** (E / I) — access not revoked.
7. **CSV injection** (T / I) — `=HYPERLINK` formula in cell, opened in Excel.
8. **SSRF** (E / I) — fetch arbitrary URL → cloud metadata endpoint.
9. **Prompt injection** (T / E) — adversarial scraped content steers AI.

---

## Workflow

1. Draw data-flow diagram with trust boundaries.
2. For each component / flow, walk through STRIDE.
3. List concrete threats (not abstract: "an attacker could spoof identity"; concrete: "attacker submits forged JWT with admin role").
4. For each threat: likelihood + impact + existing controls + proposed mitigation.
5. DREAD-rank if list is long.
6. Document. Re-review when system changes.

---

## Reference

- Microsoft STRIDE original docs (canonical).
- *Threat Modeling: Designing for Security* — Adam Shostack.
- `companies/nexusai/skills/security/threat-modeling.md` (methodology + worked examples).
- `knowledge/security/owasp-top10.md` (overlapping concrete threats).
- `companies/nexusai/skills/security/SKILL.md`.
