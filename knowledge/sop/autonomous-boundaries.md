# Autonomous Boundaries — What Runs Without Fathur

Version: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Scope: Entire AI Holding — governs decision autonomy across all 3 companies

---

## Design Principle

> **Default: autonomous. Exception: Fathur.**

The system is built to run without Fathur's intervention for routine operations. Fathur is only pulled in for decisions that are:
1. Irreversible (public publish, new commitments)
2. Expensive (budget, new tools, new clients)
3. Reputational (anything the public sees with Fathur's name)
4. Strategic (direction changes, company spawns, scope expansion)

Everything else runs on rails.

---

## Decision Classification Matrix

### TIER 1 — Fully Autonomous (No log needed beyond standard task logger)

These happen automatically as part of normal operations:

| Decision | Example | Companies |
|----------|---------|-----------|
| Run scheduled tools | fear_greed.py daily, price_scraper.py hourly | Crypto Consultant |
| Produce internal research | Weekly brief, ad-hoc analysis | Crypto Consultant |
| Internal cross-company handoff | Research → BrandFlow translation brief | All |
| Draft content (not publish) | Twitter thread draft, carousel script | BrandFlow |
| Produce design spec | Dashboard component spec, visual concept | BrandFlow, NexusAI |
| QA review (internal) | 7-Layer QA Pass, brand check | All |
| Update task logger | Log tasks, mark complete, recap | All |
| Write to company MEMORY.md | Decisions, architecture changes | All |
| Respond to Fathur's direct questions | Any analysis/research on request | All |
| Refresh dashboard data | Automated API calls per schedule | NexusAI |
| Internal code deploy (staging) | Push to staging environment | NexusAI |
| Update knowledge files | Framework revisions, glossary updates | All |
| Run weekly cadence tasks | Monday brief, Wednesday check, Friday recap | All |

### TIER 2 — Autonomous With Log (Must log decision + rationale to MEMORY.md)

These can proceed without Fathur but must be recorded for audit:

| Decision | Example | Trigger for logging |
|----------|---------|---------------------|
| Forecast Ledger entry | FL-2026-05-17-001 | Every entry logged to MEMORY.md |
| Cycle phase change call | "Phase 3 → Phase 4" | Significant market read change |
| Tool version update | Upgrading dependency | Any tool change |
| Content calendar adjustment | Moving post from Mon to Wed | Schedule deviation |
| QA FAIL on internal work | Blocking a report for revision | Quality issue detected |
| Cross-company routing decision | "This goes to NexusAI not BrandFlow" | Non-obvious routing |
| Crisis update (internal) | Market drops 10%, internal brief needed | Unusual event |
| Add/modify skill file | New pattern recognized, skill updated | Process evolution |
| Client voice profile update | Tone shift based on performance data | Client-facing change |

### TIER 3 — Requires Fathur (Must wait for explicit approval)

These CANNOT proceed without Fathur's explicit "yes":

| Decision | Example | Why |
|----------|---------|-----|
| **Publish to public surface** | Post tweet, publish blog, release report | Boundary #4 — reputational |
| **New client onboarding** | BrandFlow takes on new client | Scope + commitment |
| **New paid tool/service** | Subscribe to Glassnode Pro, new API | Budget |
| **Production deploy** | Ship to production (not staging) | Irreversible |
| **Spawn new company** | Create Company #4 | Strategic |
| **Change company focus/mission** | Pivot Crypto Consultant scope | Strategic |
| **External partnership/collab** | Respond to collab offer | Commitment |
| **Delete/archive significant work** | Remove a company, archive major content | Irreversible |
| **Public attribution of wallets** | Name real entity behind a wallet | Legal risk |
| **Crisis response (external)** | Public statement about market event | Reputational |
| **Budget allocation** | Spend money on anything | Financial |
| **Hire/fire equivalent** | Add permanent human or paid tool | Commitment |

---

## Approval Mechanism (Tier 3)

See `knowledge/sop/approval-workflow.md` for full detail.

Quick summary:
```
1. System produces [APPROVAL REQUEST] block
2. Sends via Telegram to Fathur
3. Fathur responds: "yes" / "no" / "revise: <feedback>"
4. System acts on response
5. If no response in 48h → reminder
6. If no response in 72h → log as "TIMED OUT, held" — do NOT proceed
```

---

## Boundary #4 Autonomous Interpretation

Boundary #4 (no unsupervised communication on Fathur's behalf) applies specifically to **public surfaces**:
- Social media posts
- Blog publications
- Email to external parties
- Dashboard visible to non-Fathur users
- Reports sent to clients/subscribers

It does NOT apply to:
- Internal analysis (Fathur is the only reader)
- Cross-company handoffs (internal routing)
- Draft production (drafts are not published)
- Tool execution (data gathering is not communication)
- Task logger entries (operational logging)

**Rule:** If the output could be read by someone other than Fathur → Tier 3 (requires approval).
If the output is only read by Fathur or the system internally → Tier 1 or 2 (autonomous).

---

## Escalation Triggers (System → Fathur)

Even within Tier 1/2 operations, certain conditions automatically escalate to Fathur:

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Fear & Greed extreme | F&G > 90 or F&G < 10 | Alert + crisis brief |
| BTC price move | >±10% in 24h | Alert + research update |
| Tool failure (critical) | Core tool down >4h | Alert + status report |
| QA FAIL on deliverable | Critical severity (Sev-1) | Alert + hold delivery |
| Cross-company conflict | Two companies disagree on approach | Escalate for tiebreak |
| Forecast Ledger miss | Forecast significantly wrong post-horizon | Alert + post-mortem |
| New request beyond scope | Client asks for something not in our charter | Escalate for scope decision |

---

## What "Autonomous" Means Operationally

For Hermes (the runtime):

1. **Monday 07:00 WIB** — Weekly cadence starts automatically. No prompt needed.
2. **Research runs tools** — fear_greed, price_scraper, etc. — outputs to structured format.
3. **Cross-company handoff happens** — research → BrandFlow brief auto-generated.
4. **BrandFlow drafts content** — using handoff block + client voice.
5. **QA chain runs** — both companies' QA review.
6. **Draft delivered to Fathur** — via Telegram with [APPROVAL REQUEST].
7. **System WAITS** — does not publish until Fathur says "yes".
8. **Post-approval** — schedules, publishes, logs.
9. **Weekly recap** — Friday summary of all actions taken.

Steps 1-6 and 8-9 are autonomous. Step 7 is the Fathur gate.

**Net result:** Fathur's only regular action is reviewing drafts and saying "yes" / "no" / "revise." Everything else runs on its own.

---

## Autonomy Evolution

As trust builds:
- Phase 1 (now): Fathur approves every public output individually.
- Phase 2 (future): Fathur approves a "content calendar" for the week; individual posts within the approved calendar ship without per-piece approval.
- Phase 3 (future): Fathur sets "standing rules" (e.g., "weekly crypto brief is always approved unless bear scenario >40%") and only reviews exceptions.

Current phase: **Phase 1.** Advance to Phase 2 only when Fathur explicitly says so.

---

## Reference

- `knowledge/sop/approval-workflow.md` — mechanism for Tier 3 approvals
- `knowledge/sop/cross-company-handoff.md` — handoff protocol
- `knowledge/sop/weekly-cadence.md` — autonomous rhythm
- `SOUL.md` — Root SOUL, Boundary #4 definition
- `MAIN.md` — Main Assistant operational rules
