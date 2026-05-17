# OWASP Top 10 — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.security`, `@nexusai.backend`, `@nexusai.qa`

OWASP Top 10 (2021 edition, current at write time). Quick-scan during code review + threat modeling.

---

## A01 — Broken Access Control

**Looks like**:
- `findById(id)` without checking ownership.
- Forced browsing: change `?id=1` to `?id=2` and see another tenant's data.
- Escalation via parameter tampering: `role=admin` accepted from request body.

**Fix**:
- AuthZ check at boundary (controller / middleware), not deep inside.
- Tenant scope from auth context, never from request input.
- 404 (not 403) for unauthorized access to existing resources (don't leak existence).
- Postgres RLS as defense in depth.

**Agency-critical**. Most-frequent breach pattern. Test it explicitly: client A tries to access client B's resource → must 404.

---

## A02 — Cryptographic Failures

**Looks like**:
- `md5(password)` or `sha256(password)`.
- Plaintext password storage.
- TLS optional / mixed content.
- API key in URL query string (logged in proxy / browser history).
- `Math.random()` for tokens / IDs (predictable).
- Encryption with hardcoded key.

**Fix**:
- Passwords: argon2id (or bcrypt cost ≥12).
- Random tokens: `secrets.token_urlsafe(32)` (Python), `crypto.randomBytes` (Node).
- TLS-only. HSTS header. No HTTP fallback.
- Secrets in vault, not config files, not env vars committed.
- AES-GCM for symmetric encryption (libsodium / cryptography lib — never roll-your-own).

---

## A03 — Injection

**Looks like**:
- String-concat SQL: `f"SELECT * WHERE name='{name}'"`.
- Shell exec from input: `os.system(f"convert {filename}")`.
- LDAP / NoSQL / XPath / template injection.
- Eval of user-supplied expression.

**Fix**:
- Parameterized queries always (`db.execute("WHERE name = %s", (name,))`).
- ORM with bind params (SQLAlchemy, Prisma) covers most SQL.
- `subprocess.run(["cmd", arg], shell=False)` — never `shell=True` with user input.
- Validate/whitelist allowed values; reject everything else.

---

## A04 — Insecure Design

**Looks like**:
- "We'll add auth later."
- Feature shipped without threat modeling.
- Trust-by-default for internal users.
- Forgot password flow that emails password (instead of reset token).

**Fix**:
- Threat-model BEFORE code (`knowledge/security/threat-modeling-stride.md`, `companies/nexusai/skills/security/threat-modeling.md`).
- Security AC mandatory for sensitive features.
- Default deny, explicitly grant.

---

## A05 — Security Misconfiguration

**Looks like**:
- `DEBUG = True` in prod.
- Default admin password unchanged.
- S3 bucket public.
- Verbose error messages exposing stack trace.
- CORS = `*`.
- Missing security headers (CSP, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security).

**Fix**:
- Hardening checklist + IaC review.
- Pre-prod security headers audit (`securityheaders.com`).
- CORS strict allowlist.
- Generic 500 responses ("Internal error, request_id: abc"), full detail in logs only.
- Cloud config audited (`tools/dep_audit.py`-equivalent for cloud is e.g. ScoutSuite, Prowler).

---

## A06 — Vulnerable / Outdated Components

**Looks like**:
- `requirements.txt` with versions from 3 years ago.
- Old jQuery / Lodash / Express with known CVEs.
- Container base image not refreshed for 6+ months.

**Fix**:
- Weekly `tools/dep_audit.py` (pip-audit / npm audit / GitHub Dependabot).
- Patch window: monthly minimum, immediate for critical.
- Pin to specific versions; avoid `^x.y.z` ranges in lockfile.
- Renovate / Dependabot bot to auto-PR updates.

---

## A07 — Identification and Authentication Failures

**Looks like**:
- Different responses for "wrong password" vs "user not found" (enumeration).
- No rate limit on login → brute force trivial.
- Session never expires.
- Password reset link valid forever / re-usable.
- No MFA option.

**Fix**:
- Generic error: "Invalid credentials" — same response, same timing.
- Rate-limit per username + per IP. Lock after N failures with progressive backoff.
- Session timeout (idle 30min, absolute 24h typical).
- Password reset: single-use, 30-min expiration, invalidates old sessions on success.
- MFA available; required for admin.

---

## A08 — Software and Data Integrity Failures

**Looks like**:
- Unsigned auto-update mechanism.
- Public CI cache that anyone can poison.
- Importing JS from sketchy CDN at runtime.
- `eval(downloaded_js)` patterns.

**Fix**:
- Signed releases. Verify signature before apply.
- SBOM (Software Bill of Materials) for every release.
- Pinned dep hashes (`requirements.txt` with `--hash=sha256:...`, or `pip-tools` `--generate-hashes`).
- Subresource Integrity (`<script integrity="sha384-..."`) for CDN scripts.

---

## A09 — Security Logging and Monitoring Failures

**Looks like**:
- No log of failed login attempts.
- No alert on auth-failure rate spike.
- Logs never reviewed.
- Logs contain credentials (negative case).

**Fix**:
- Log: every auth attempt (success + fail), every privileged action, every config change, every credential read from vault.
- Alert: brute-force, privilege escalation, mass data export, unusual hours.
- Review: weekly dashboard look. Quarterly audit.
- Reference: `knowledge/software/observability.md`.

---

## A10 — Server-Side Request Forgery (SSRF)

**Looks like**:
- Feature: "fetch URL preview". User supplies `http://169.254.169.254/...` (cloud metadata) or `http://internal-redis:6379/...`.
- Webhook URL from user, fetched server-side.
- File-import-from-URL feature.

**Fix**:
- Allowlist outbound hosts (strict; not "anything but private IPs").
- Block private/loopback/link-local IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16, ::1, fc00::/7).
- Resolve DNS once; verify resolved IP not private; then fetch from that IP (defeats DNS rebinding).
- Use a separate egress proxy with strict ACLs for user-driven fetches.

---

## Bonus — Recently Promoted Concerns

### Insecure Deserialization (A08-related)
- Don't `pickle.loads()` on user-supplied bytes.
- Don't accept arbitrary YAML (`yaml.safe_load` only).
- JSON is safest; if you must accept binary, sign and verify.

### XXE (XML External Entities)
- If you must parse XML: disable external entities + DTDs (`defusedxml` in Python).
- Prefer JSON over XML for new APIs.

### Dependency Confusion
- Private packages: scope correctly, register the public name even if unused (squat).
- Use lockfiles + hash verification.

---

## Quick Code Review Pass (use during PR review)

```
[ ] A01: Tenant filter present? AuthZ at boundary?
[ ] A02: Passwords hashed? Tokens random? TLS only?
[ ] A03: Parameterized queries? No string concat to SQL/shell?
[ ] A05: DEBUG off? Sensitive info not in error responses?
[ ] A06: Deps reasonably current? No known-vulnerable version?
[ ] A07: Login rate-limited? Generic error responses?
[ ] A09: New error path logged? Sensitive ops audit-logged?
[ ] A10: User-supplied URL? Allowlisted? IP-validated?
```

---

## Anti-Patterns (Beyond Top 10)

- **"Security is the security team's job."** Every developer is responsible. Security team is force multiplier.
- **"We're too small to be targeted."** Wrong. Small + valuable = soft target.
- **"Compliance = security."** Compliance is the floor, not the ceiling.
- **"We'll fix the deps next sprint."** No, you won't. Schedule the patch window.
- **"Just use a WAF."** WAF is one layer. Don't outsource thinking.

---

## Reference

- OWASP Top 10 (2021) — owasp.org/www-project-top-ten/
- `companies/nexusai/skills/security/SKILL.md`
- `companies/nexusai/skills/security/threat-modeling.md`
- `knowledge/security/threat-modeling-stride.md`
- `knowledge/security/incident-runbook.md`
- `knowledge/software/auth-patterns.md`
