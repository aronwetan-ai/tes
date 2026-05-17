# Auth Patterns — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.security`, `@nexusai.backend`, `@nexusai.frontend`

Authentication = who you are. Authorization = what you're allowed. Don't conflate.

---

## Pattern Picker

| Client | Default pattern |
|---|---|
| Server-rendered web (Django/Rails/Next-SSR) | Session cookie (HttpOnly + Secure + SameSite=Lax) + CSRF token. |
| SPA on same origin | Session cookie. |
| SPA on different origin (cross-origin) | Short-lived JWT in memory + refresh via HttpOnly cookie. |
| Native mobile app | Refresh token (long, secure storage) + access token (short, in memory). |
| API consumer (third-party integrators) | API key per client, scoped, rate-limited. |
| Service-to-service inside infra | mTLS or signed JWT from internal IdP. |
| OAuth into 3rd-party (IG, Google, Meta) | Authorization Code + PKCE. Never implicit flow. |
| AI agent calling our API | Service token, scoped, audit-logged. |

---

## Session Cookie (Default for Web)

```
Set-Cookie: session_id=...;
            HttpOnly;          # JS can't read → XSS doesn't steal session
            Secure;            # HTTPS only
            SameSite=Lax;      # blocks most CSRF
            Path=/;
            Max-Age=86400      # 24h absolute expiry
```

CSRF: pair with double-submit token or `SameSite=Strict` for sensitive actions.

Storage: server-side (Redis / DB). Cookie is a key, not the data.

---

## JWT — Use Carefully

Pros: stateless verification, scales to many services.

Cons: revocation hard (must wait for expiry), bigger than session ID, easy to misuse.

Rules:
- **Short-lived access token** (5–15 min).
- **Refresh token** (longer, in HttpOnly cookie or secure mobile storage).
- **Never put PII / sensitive data in JWT** — base64 ≠ encrypted; client can read.
- **Include scope/role claim** for AuthZ.
- **Verify signature, issuer, audience, expiry** every time. Don't trust unverified.
- **Algorithm allowlist** — reject `alg: none`. Pin to RS256 or ES256.

Anti: long-lived JWT (24h+) with no revocation strategy.

---

## OAuth 2.0 (Connecting to 3rd-party)

For agency: this is how clients let you access their IG / Meta Ads / Google.

| Flow | Use |
|---|---|
| **Authorization Code + PKCE** | Default. SPA, web, mobile. |
| **Client Credentials** | Service-to-service (no user). |
| **Implicit** | Don't use. Deprecated. |
| **Resource Owner Password** | Don't use. Defeats OAuth. |
| **Device Code** | TVs, IoT, headless devices. |

Authorization Code + PKCE flow:

```
1. Frontend → IdP authorize URL (with PKCE challenge).
2. User authenticates + consents at IdP.
3. IdP redirects to our callback with code.
4. Backend exchanges code + PKCE verifier → access_token + refresh_token.
5. Backend stores tokens in cred_vault (per-client-encrypted).
6. Frontend never sees the tokens.
```

Critical:
- `state` param: random nonce, verify on callback (CSRF defense).
- PKCE verifier: random per request, never reused.
- Scope: minimum required. Reject overscoped tokens.
- Validate token at callback (issuer, audience, signature).

---

## Token Lifetime

| Token type | Typical lifetime |
|---|---|
| Session cookie | 24h–30d (sliding by activity). |
| JWT access token | 5–15 min. |
| JWT refresh token | 7–30 days; rotated on each use. |
| OAuth access token (3rd-party issued) | depends on provider; often 1h. |
| OAuth refresh token (3rd-party issued) | depends; often 30–60 days. |
| API key (client-managed) | rotation policy: 90 days routine. |
| Reset password token | 30 min, single-use. |
| Email verify token | 24h, single-use. |
| Magic link login | 15 min, single-use. |

---

## Multi-Factor (MFA)

| Factor | Strength |
|---|---|
| TOTP (authenticator app, RFC 6238) | Strong; default for general use. |
| WebAuthn / FIDO2 (hardware key) | Strongest; phishing-resistant. Required for admin / high-value accounts. |
| SMS OTP | Weakest (SIM swap risk). Use only as fallback. |
| Email OTP | Equivalent to "if you can read email". OK as recovery, not primary. |
| Push notification | Strong if app is signed + bound to device. |

NexusAI defaults:
- All staff: WebAuthn primary, TOTP fallback.
- Client end-users: TOTP primary, optional.
- Admin actions: WebAuthn required.

---

## Authorization Models

| Model | When |
|---|---|
| **RBAC** (role-based) | Default. Few well-defined roles (admin, member, viewer). |
| **ABAC** (attribute-based) | Complex rules (resource attributes + user attributes + context). |
| **ReBAC** (relationship-based) | Per-resource sharing — "Alice can edit doc X because doc X is in folder Y owned by Alice's team". |
| **Per-tenant role** (agency-critical) | RBAC scoped to client_id — same user is admin in client_42, viewer in client_43. |

Implementation pattern (RBAC + tenant):

```python
class AuthCtx:
    user_id: UUID
    client_id: UUID  # current client context
    role: Role       # user's role within this client

def require(permission: str):
    def deps(ctx: AuthCtx = Depends(auth)):
        if not ctx.role.has(permission):
            raise HTTPException(403)
        return ctx
    return deps

@app.delete("/campaigns/{id}")
def delete_campaign(id: UUID, ctx = Depends(require("campaign:delete"))):
    ...
```

Anti: AuthZ check missing ("forgot one endpoint"). Use middleware/decorator/route-level enforcement so it's hard to forget.

---

## Login Anti-Enumeration

Same response regardless of which step failed:

| What | Response |
|---|---|
| User doesn't exist | "Invalid credentials." |
| User exists, wrong password | "Invalid credentials." |
| User exists, right password, MFA wrong | "Invalid credentials." |
| Account locked | "Invalid credentials. Try again later." |

Same response time too — use constant-time compare to prevent timing-based enumeration.

For password reset / signup: same trick. "If an account exists for that email, we've sent a reset link" — even if no account.

---

## Rate Limiting Auth Endpoints

```
/login                 5 per minute per IP, 10 per hour per username.
/register              5 per hour per IP.
/password-reset        3 per hour per email.
/verify-mfa            10 per minute per session.
```

After threshold: progressive backoff (1m, 5m, 30m, 1h). Add CAPTCHA at moderate threshold; full lock + email alert at high.

---

## Session Revocation

- Logout invalidates server-side session immediately (delete from store).
- Logout-all-sessions option: invalidate all of user's sessions.
- Force-logout on password change, email change, suspected compromise.
- Periodic re-auth for sensitive actions (re-enter password before deletion of important data).

---

## Cookies + Cross-Site

| SameSite | Behavior | Use |
|---|---|---|
| `Strict` | Cookie not sent on any cross-site request. | High-sensitivity flows (banking, settings). |
| `Lax` | Cookie sent on top-level navigation, not on iframe/POST/AJAX cross-site. | Default for sessions. |
| `None` | Cookie sent on all cross-site requests. Requires `Secure`. | API for third-party origins (SSO, embeds). |

Rule: pick the strictest that works for your use case.

---

## Anti-Patterns

- **MD5/SHA hashing of passwords.** Use argon2id or bcrypt cost ≥12.
- **Plain JWT in localStorage.** XSS readable. Use HttpOnly cookies for the long-lived token.
- **Long-lived JWT with no revocation plan.** Compromise = persistent access until expiry.
- **`alg: none` accepted.** Reject. Allowlist algorithms.
- **AuthZ check at deep call instead of boundary.** Forget one path = bypass.
- **Tenant scope from request body.** Forge it = cross-tenant.
- **CORS = `*`.** Anyone can fetch user's data via their browser.
- **No rate limit on login.** Brute force trivial.
- **OAuth without `state` param.** CSRF on the callback.
- **OAuth implicit flow.** Token in URL fragment, leaks to referer / browser history.
- **Trusting client-side role check.** Client-side is hint; server enforces.

---

## Reference

- `companies/nexusai/skills/security/SKILL.md`
- `knowledge/security/owasp-top10.md` (A01, A02, A07).
- `knowledge/security/threat-modeling-stride.md` (S = spoofing).
- OWASP Authentication Cheat Sheet (canonical).
- RFC 6749 (OAuth 2.0), RFC 7636 (PKCE), RFC 6238 (TOTP).
