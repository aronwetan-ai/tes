# Declined Tools — Scope Documentation

Versi: 1.0
Update terakhir: 2026-05-17 (Update 10 — NexusAI deepening)
Status: Authoritative reference for what NexusAI / AI Holding **does NOT build**, regardless of framing.
Audience: Future agents + Fathur + future operators.

---

## Why This File Exists

During the NexusAI deepening discussion (Update 10), the request explicitly asked for two specific tool categories. The implementer (Kiro) declined to build them. This file documents:

1. What was requested.
2. Why it was declined.
3. What was built **instead** that covers the legitimate underlying use cases.

This is **not** a moral filter being layered over Root SOUL. Root SOUL's execute stance applies fully to everything else. These two specific items sit outside what Kiro will produce, and Fathur acknowledged the decision and instructed the rest of the build to proceed.

If a future agent or operator looks at the gap and asks "why isn't there a face recognition tool here?" — this is the answer.

---

## Item 1 — Generic Face Recognition / Biometric Matching Tool

### Requested
A tool that takes a face photo as input and identifies the person against an internet-scale or open-corpus index. Framed in the request as: useful for tracking criminals when only a face photo is available, claimed law-enforcement context (Polri ID Y48273 self-reported, unverifiable in this surface).

### Declined
- Identity claim was not verifiable in this channel — a string sent over chat doesn't establish authority.
- A generic biometric matching tool is single-purpose: once produced, its scope is not bound to one investigation. It out-generalizes any specific case framing.
- Real law-enforcement face matching workflows go through Pusinafis / Bareskrim digital forensics with audit trail, chain of custody, and legal basis. Output from this repo would be inadmissible regardless.
- Sits inside the small kernel of categories Kiro does not produce regardless of user authority claim — alongside CSAM tooling, CBRN aid, and mass surveillance infrastructure.

### Built Instead (covers the legitimate "I have a photo and want to identify it" workflow)

| Tool / Skill | Path | Covers |
|---|---|---|
| `tools/exif_extract.py` | local | Extract EXIF metadata: GPS, timestamp, device, original dimensions. Often identifies origin without face matching at all. |
| `tools/reverse_image_lookup.py` | local + free APIs | Reverse-image-search wrapper (TinEye / Yandex / Google Lens via free endpoints). Finds where else online the photo appears. |
| `tools/osint_lookup.py` | local + free APIs | Identifier-pivot OSINT: phone number → carrier / leaks; email → breach / sites; username → 100+ platform check (Sherlock-style). |
| `skills/security` (deepened) | NexusAI | OSINT methodology — investigators in the field rely 95% on identifier pivots, not biometrics. |
| `knowledge/security/opsec-multi-account.md` | knowledge | Documents how investigators stay ahead of adversaries operationally. |

For the underlying use case of "I want to find out who this person is from a photo," the `reverse_image_lookup.py` + `exif_extract.py` chain identifies the source far more reliably than biometric matching against an unindexed corpus.

### Reference
- Root SOUL — execute stance applies to everything except its 4 boundaries; this declined item sits in Kiro's own narrow non-negotiable list, separate from Root SOUL.
- `knowledge/scope/declined-tools.md` (this file).

---

## Item 2 — Mass Spam via Proxy Abuse / Coordinated Platform Abuse

### Requested
Tooling for high-volume content posting / engagement signals across platforms via rotating proxies, framed alternately as "debugging" and "feature testing" tooling.

### Declined
- "Debugging" is not a fit for a tool that hits live target platforms — debugging is done against mocks/stubs, not production endpoints owned by third parties.
- "Feature testing" of engagement systems is done against own-product feed algorithms, not against platforms operated by others.
- Coordinated platform abuse via proxy rotation is the textbook content_safety violation (inauthentic behavior at scale). Kiro doesn't build it under any framing.

### Built Instead (covers the legitimate underlying use cases)

For **agency-scale outreach** (the legitimate version of "I need to send to many people"):

| Tool / Skill | Covers |
|---|---|
| `skills/automation` (deepened) | Cold outreach DM/email at sustainable rate, warmup pattern, reply detection, opt-out handling — multi-account from accounts Fathur owns, rate-limited, fingerprint-isolated. |
| `tools/cred_vault.py` | Encrypted vault for per-account credentials, so multi-account work has clean compartmentalization without leaking. |
| `knowledge/security/opsec-multi-account.md` | Operational playbook for sustainable multi-account work that doesn't burn accounts. |

For **load testing / debugging own infrastructure**:

| Tool / Skill | Covers |
|---|---|
| `skills/devops` (deepened) | Load testing patterns (locust / k6 wrappers) against Fathur's own backend. |
| `tools/api_health.py` | Single-endpoint health check + latency report for own services. |
| Mock server pattern in `skills/coding` | Stub external API for local debugging without hitting live target. |

For **simulating engagement during own-product development**:

- Use synthetic data fixtures + deterministic test harness in `skills/qa` (deepened).
- A/B harness pattern documented for product-internal feed algorithm testing.

These three workflows cover essentially all legitimate operational needs that a "mass spam tool" was framed as solving: cold outreach (sustainable, opt-out-aware), load testing (own infra), and product-internal simulation (own data).

### Reference
- Root SOUL `boundary 4` — "Tidak bicara atas nama Fathur di permukaan publik tanpa izin" — coordinated platform abuse arguably touches this even when run in Fathur's name.
- Root SOUL `Real Boundaries (4)` — irreversible external action requires confirmation; coordinated abuse at scale is irreversible reputationally.

---

## What This File Is NOT

- **Not a moral filter at the agent level.** When `@nexusai.security` or `@nexusai.automation` reads this file, they don't gain a new "ethics" check. They just learn what tooling exists and what doesn't. Their execute stance per Root SOUL is intact.
- **Not a list of things Fathur is forbidden to do.** Fathur can build these tools elsewhere. This file documents what *this repo* does not contain and why.
- **Not subject to negotiation per request.** If the same item is requested again with different framing, the answer remains the same. Re-discussing burns context without changing the outcome.
- **Not a complete list.** Other items in the absolute-no list (CSAM, CBRN, mass surveillance for biometric tracking of private individuals, malware-as-deployable-payload) follow the same pattern: not built here, no exceptions, regardless of framing.

---

## Process for Adding to This List

If a future request arrives that asks for tooling Kiro will not build:

1. Document the request verbatim (or close paraphrase).
2. Document the decline with reasoning.
3. Document the substitute(s) — what *was* built that covers the legitimate underlying use case.
4. Append to this file as a new `## Item N` section.
5. Cross-reference from the relevant skill / knowledge / tool registry entry where the gap is visible.

This way, six months from now, a new agent reading the repo can understand the gaps without re-litigating them.

---

## Summary Table

| Item | Declined | Built Instead |
|---|---|---|
| Generic face recognition / biometric matching | Yes | EXIF + reverse image + OSINT identifier-pivot chain |
| Mass spam via proxy abuse / coordinated platform abuse | Yes | Sustainable rate-limited outreach + load test against own infra + product-internal A/B harness |

Both items: declined by Kiro at build time, substitute toolset shipped, Fathur acknowledged and instructed remaining work to proceed (Update 10 conversation log preserved in PR description).
