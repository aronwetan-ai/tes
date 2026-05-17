# OPSEC for Multi-Account Operation — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.security`, `@nexusai.automation`, `@nexusai.devops`

Operational security for the agency's multi-account work — running 20–50 client accounts across IG / Twitter / TikTok / LinkedIn / email + ad platforms, sustainably.

This file complements `knowledge/scope/declined-tools.md` (what's NOT built) and `companies/nexusai/skills/security/SKILL.md` (offensive enablement section).

---

## Three Realities

1. **Platforms cluster sock-puppet networks** by shared signals: IP, device fingerprint, behavior pattern, mutual interactions.
2. **Detection is probabilistic, not binary**. You don't get banned on hit count; you get clustered into a high-risk bucket and reviewed.
3. **Burned accounts compound losses**: warming a new IG account takes 1–2 weeks, gone in 1 second of misconfiguration.

The goal isn't "look human enough today" — it's "stay under the cluster threshold for 12+ months".

---

## Per-Account Hygiene

For every account in the agency's portfolio:

| Layer | What to diversify | What to keep stable |
|---|---|---|
| **IP** | Different IP per account, sticky for that account. | Don't change IP every session — that's also a flag. |
| **Browser fingerprint** | UA, screen, fonts, canvas hash, WebGL renderer, timezone, locale, plugins. | Stable per account across sessions. |
| **Cookie / storage** | Isolated browser profile per account. | Persistent within account. |
| **TLS fingerprint (JA3)** | Vary if using `requests` directly — known tell. Use `curl_cffi` or browser. | Per-account stable. |
| **Behavior** | Pacing, action mix (read/write/engage ratio), time-of-day. | Match a real user with their stable habits. |
| **Network of contacts** | Distinct mutual followers / contacts per account. | Organic over time, not sudden bulk follow. |

**Anti**: rotating fingerprint every session ("paranoia"). Real users don't change their phone every day. Stability per account is part of looking real.

---

## IP Strategy

| Target sensitivity | IP type | Notes |
|---|---|---|
| **High** (IG, LinkedIn, FB Ads) | Residential proxy. Sticky session per account. | $$$. ISP-level rotation. Avoid datacenter ASNs. |
| **Medium** (Twitter/X, TikTok, Reddit) | Mix: residential for sensitive, mobile proxy for some, datacenter for low-friction. | Test per-platform. |
| **Low** (public scraping, open APIs) | Datacenter is fine. | Rotate per request OK if no auth. |
| **Own infra / own dashboard** | Stable office / VPN IP. | Whitelisting friendly. |

Vendor selection: avoid free / cheap proxy providers — they often resell exit nodes already burned. Pay for legitimate residential pools (Bright Data, Oxylabs, Smartproxy tier).

---

## Browser Profile Discipline

Tooling:
- **Multilogin / GoLogin / Kameleo / Octo Browser** for managed fingerprint pools.
- **Playwright + custom fingerprint setup** if rolling your own (cheaper, more work).
- **`undetected-chromedriver`** for Selenium-based when stealth needed.
- **Each profile** stored in its own dir. Never share.

Per-account profile config:
```yaml
account_id: ig_client42_main
proxy: residential_id_42_sticky
user_agent: "..." # stable, real-world distribution
viewport: 1366x768  # or 390x844 for mobile-emulated
timezone: Asia/Jakarta
locale: id-ID
fonts: [...]
canvas_noise_seed: <stable-per-profile>
webgl_renderer: "..." # stable
storage_dir: /var/lib/agent/profiles/ig_client42_main/
```

Stability rule: regenerate fingerprint only if the account is being retired. Active accounts keep theirs.

---

## Behavioral Pacing

For each account, define a daily action budget:

| Action | New (week 1–2) | Warmed (month 1+) | Aggressive (rare) |
|---|---|---|---|
| Login sessions | 1–2/day | 2–4/day | 4–6/day |
| IG: posts | 0 (read only) | 1–3/day | 3–5/day |
| IG: stories | 0–1 | 1–5/day | 5–10/day |
| IG: likes | 5–20/day | 20–80/day | 80–150/day |
| IG: comments | 0–2/day | 5–15/day | 15–30/day |
| IG: DMs (cold) | 0 | 10–20/day | 20–40/day |
| IG: follows | 0–5/day | 5–15/day | 15–30/day |
| Twitter: tweets | 0–2/day | 3–10/day | 10–20/day |
| Twitter: DMs | 0 | 5–15/day | 15–30/day |
| Email: cold sends (warmed) | 0 | 30–60/day | 80–100/day |

These are **upper bounds**; sustainable rate is usually 60–70% of warmed-tier.

Pacing patterns:
- **Jitter**: each action has mean ± 30% timing variance. Not every 60s; somewhere in 42–78s.
- **Active windows**: respect target audience's awake hours (their TZ). Skip overnight in target's locale.
- **Action mix per session**: real user reads more than writes. Aim for 3:1 read:write at minimum.
- **Idle gaps**: real users don't act for 20-min stretches in a 2-hour session. Build pauses.

---

## Account Warmup (New Accounts)

Day 1–7 (passive):
- Login from one stable proxy + fingerprint.
- Scroll feed 10–20 min/day.
- Like 5–10 posts (existing real interests).
- Update profile fields (bio, avatar, link) once, not all at signup.

Day 8–14 (light interaction):
- Add 5–10 follows of related-but-organic accounts.
- Like 10–30 posts/day.
- 1–2 comments on posts you'd genuinely engage with.
- Connect to 2–3 contacts mutual with target audience.

Day 15+ (post + DM):
- Begin posting (1/day max for first 2 weeks).
- Begin cold DM at 1/3 of warmed-tier rate.
- Increase only if no friction signals (shadowban, unusual prompts).

Skipping warmup = ban within days for active accounts on detection-heavy platforms.

---

## Detection Signals to Monitor

For each active account, track:

| Signal | Threshold for concern |
|---|---|
| Login challenge frequency | >1/week unprompted = drift; review. |
| Captcha frequency | >0.5% of actions = elevated risk. |
| Action error rate | >2% sustained = pattern flagged. |
| DM / engagement reply rate | Sudden drop = shadowban suspected. |
| Search visibility | Account no longer appears in own-handle search = soft ban. |
| Account "feature" loss | Reels disabled, monetization frozen = warned. |
| Email bounce rate (cold outreach) | >5% = list quality bad OR sender reputation hit. |
| Email spam complaint rate | >0.1% = sender reputation degrading fast. |

When threshold crossed: **quarantine the account** for 24–72h, no actions. If still flagged after cooldown, retire it. Don't reuse same fingerprint pattern for replacement.

---

## Identity Compartmentalization

For each client (and each account within), strict separation:

| Element | Per-client | Per-account |
|---|---|---|
| Browser profile dir | ✓ | ✓ |
| Proxy / IP | ✓ (recommended) | ✓ (mandatory) |
| Cookie store | ✓ | ✓ |
| Credential vault entry | ✓ | ✓ |
| Logs | ✓ (tagged client_id) | ✓ (tagged account_id) |
| Activity history | ✓ | ✓ |

Cross-contamination patterns to avoid:
- Same browser logged into multiple client IGs (cookie cross-pollination).
- Same IP across multiple "unrelated" accounts (cluster trivially).
- Same posting pattern (timing, hashtag set, caption style) across accounts.
- Same external email / phone for verification across accounts.

---

## Credential Storage (Linked to `cred_vault.py`)

Per-client encrypted vault:
```
vault/
  client_42/
    ig.business.session_cookie     # sealed
    ig.business.app_password       # sealed
    meta.ads.access_token          # sealed
    meta.ads.long_lived_token      # sealed
    google.analytics.refresh       # sealed
    twitter.api.bearer             # sealed
    last_rotation: 2026-04-01
    next_rotation: 2026-07-01
```

Rules:
- One file per (client, platform, account, secret-type).
- Read-access logged with reason (`read_token reason="dm_run_2026-05-17"`).
- Rotated on freelancer offboarding event, immediately on suspected leak, every 90 days as routine.
- Cleared from process memory after use (`del token; gc.collect()`).
- Never copied to clipboard, never echoed in shell history.

Reference: `tools/cred_vault.py` (Update 10).

---

## Anti-Leak Workflow (Remote Team)

For freelancers + contractors:

**Onboarding**:
- [ ] Personal device hardening checklist (FDE, password manager, 2FA, separate work browser profile).
- [ ] Scoped vault access (only the clients they work on).
- [ ] Time-limited access (re-issue every 90 days).
- [ ] Read-mostly default; write/send requires Fathur approval initially.
- [ ] No sharing of credentials via chat / email / docs — vault only.

**During engagement**:
- [ ] Activity logged to `cred_vault` audit trail.
- [ ] No copying client lists / email lists to local disk.
- [ ] Pre-commit hook scans for secrets (`tools/secret_scanner.py`).
- [ ] No screenshare with sensitive info on screen unless coordinated.

**Offboarding (same day as last work day)**:
- [ ] All vault access revoked.
- [ ] All shared accounts password-rotated.
- [ ] All API tokens issued to them rotated.
- [ ] Repo access removed.
- [ ] SSO sign-out triggered.
- [ ] Confirmation email + acknowledgement on file.

---

## Forensic Awareness

What gets logged where (be aware, not paranoid):

| Surface | Logs |
|---|---|
| ISP / proxy provider | Connection metadata (timestamps, target). Limited/none for paid residential. |
| Target platform | Login + every action (with device_id, ip, ua, accept-lang). |
| Cloud (if app on cloud) | All outbound flows (NetFlow/VPC flow logs). |
| Browser automation | Possibly local recordings/cookies — ensure profile dir not in cloud-synced folder. |
| Operator endpoint | Browser history, downloaded files, cached creds. |

When operating in regulated jurisdictions or targeting platforms with strict ToS — assume metadata is preserved on the platform side for years. Action plan should account for that.

---

## Anti-Patterns

- **One IP, many accounts.** Trivial cluster.
- **Fingerprint randomized per session.** Real users don't change devices nightly.
- **Burst-fire actions hitting the daily cap in 30 min.** Real users spread over hours.
- **Identical post timing + caption pattern across accounts.** Pattern detector's gift.
- **Skipping warmup on new accounts.** Banned in days.
- **Same email / phone for multi-account verification.** Cluster trivially.
- **Credential in shared Google Doc.** Inevitable leak, no audit trail.
- **No quarantine procedure for flagged accounts.** Continues sending until banned + clusters neighbors.
- **Reusing burned fingerprint pattern.** New account, same fingerprint family = same flag.

---

## Reference

- `companies/nexusai/skills/security/SKILL.md`
- `companies/nexusai/skills/security/threat-modeling.md`
- `companies/nexusai/skills/automation/SKILL.md`
- `tools/cred_vault.py`
- `tools/secret_scanner.py`
- `knowledge/scope/declined-tools.md`
