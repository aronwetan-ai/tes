# Approval Workflow — Fathur Decision Gate

Version: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Scope: All Tier 3 decisions requiring Fathur's explicit approval

---

## Purpose

Define HOW Fathur approves things. The system runs autonomously for routine work (see `autonomous-boundaries.md`). When something requires Fathur, this SOP defines the exact mechanism.

---

## Channel

**Primary:** Telegram (Hermes bot → Fathur)
**Fallback:** None currently. If Telegram is down, system holds all Tier 3 decisions until channel is restored.

---

## Approval Request Format

When the system needs Fathur's approval, it sends this structured message:

```
🔒 APPROVAL REQUEST

Type:       <publish / new-client / budget / deploy / strategic / other>
From:       @<company>.<agent>
Priority:   routine / time-sensitive / urgent
Deadline:   <YYYY-MM-DD or "no deadline">

SUMMARY:
<2-3 sentences: what is being requested and why>

PREVIEW:
<For content: first 3-5 lines of the content>
<For decisions: the options with recommendation>

RISK:
<What happens if approved — what's the downside>

ATTACHED:
<Full draft available at: <path> or "see next message">

---
Reply with:
✅ "yes" — approve as-is
✏️ "revise: <feedback>" — approve with changes
❌ "no" — reject (with optional reason)
⏸️ "hold" — not now, ask again later
```

---

## Response Handling

| Fathur says | System does |
|---|---|
| "yes" / ✅ / "ok" / "lanjut" / "go" / "approved" | Execute immediately. Log: `[APPROVED] YYYY-MM-DD by Fathur` |
| "revise: <feedback>" / "ubah: <feedback>" | Route feedback to owning agent. Agent revises. Re-submit for approval. |
| "no" / ❌ / "jangan" / "cancel" | Cancel execution. Log: `[REJECTED] YYYY-MM-DD by Fathur. Reason: <reason>` |
| "hold" / "nanti" / "later" | Park in queue. Re-ask after 48h. |
| No response | See timeout handling below. |

---

## Timeout Handling

```
T+0h:     Request sent
T+24h:    No response → gentle reminder: "Reminder: approval pending for <summary>"
T+48h:    No response → second reminder: "⏰ Still waiting on: <summary>. Reply or say 'hold'."
T+72h:    No response → log: [TIMED OUT] — held indefinitely. Do NOT proceed.
           Exception: if Priority=urgent, escalate with: "🚨 URGENT: <summary> is blocking. Please respond."
```

**Critical rule:** The system NEVER proceeds without approval on Tier 3 decisions. Silence ≠ consent.

---

## Priority Definitions

| Priority | Meaning | Timeout before first reminder |
|----------|---------|-------------------------------|
| Routine | Normal weekly flow (e.g., approve Monday brief) | 24h |
| Time-sensitive | Has a deadline (e.g., publish before market opens) | 6h |
| Urgent | Blocking critical operations or crisis response | 2h |

---

## Batch Approval (Efficiency Mode)

For weekly routine, the system can batch multiple approvals into one message:

```
🔒 WEEKLY APPROVAL BATCH (Week of 2026-05-19)

Items requiring approval:

1. [CONTENT] Weekly crypto brief Twitter thread (7 tweets)
   Preview: "BTC +3.8% this week and nobody's talking about it..."
   Risk: Standard — public financial content with disclaimer
   
2. [CONTENT] Weekly crypto brief IG carousel (8 slides)
   Preview: Slide 1 — "BTC +3.8% this week. Zero hype."
   Risk: Standard — public financial content with disclaimer

3. [CONTENT] IG story teaser (3 slides)
   Preview: Key metrics highlight
   Risk: Low — derivative of approved carousel

---
Reply options:
✅ "all yes" — approve all items
✅ "1,2 yes, 3 no" — selective approval
✏️ "revise 1: <feedback>" — approve others, revise specified
❌ "all no" — reject batch
```

---

## Approval Types & Typical Items

### Content Publish (Most Common)
- Weekly crypto brief → social media
- Blog posts
- Dashboard made visible to non-Fathur users
- Any external communication

### New Client
- BrandFlow onboarding new client
- Crypto Consultant providing research to new party

### Budget
- New paid tool subscription
- Infrastructure cost increase
- Paid API access

### Production Deploy
- New features going live (staging → production)
- API endpoint changes affecting external users

### Strategic
- New company spawn
- Mission/scope changes
- Major architectural decisions

---

## Autonomous Pre-Processing

Before sending approval request, the system MUST have:
1. ✅ Completed all QA checks (don't send broken work for approval)
2. ✅ Applied all Boundary #4 constraints (disclaimer, bear case, no buy/sell)
3. ✅ Cross-company QA complete (if applicable)
4. ✅ Full draft ready (not "will write after approval")

Fathur reviews finished work, not plans.

---

## Logging

Every approval interaction logged to `memory/global.md`:

```
[APPROVAL] 2026-05-17 — Type: content-publish
  Request: Weekly crypto brief thread (7 tweets)
  Submitted: 2026-05-17 10:00 UTC
  Approved: 2026-05-17 12:30 UTC
  Published: 2026-05-19 01:00 UTC (Monday 08:00 WIB)
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Fathur approves but content has decayed | Re-verify data before publish. If stale, produce fresh version. |
| Fathur approves with revision but revision changes data | Full QA re-run on revised version. |
| Multiple conflicting approval requests pending | Present as batch; let Fathur prioritize. |
| Fathur says "approved for next 4 weeks" (Phase 2 intent) | Log as standing approval. Still verify each piece passes QA before publish. Mark in MEMORY.md as Phase 2 pilot. |
| Crisis event happens while waiting for approval | Send urgent alert. Produce internal brief immediately (Tier 1). Hold public response for Tier 3 approval. |

---

## Reference

- `knowledge/sop/autonomous-boundaries.md` — what's Tier 1/2/3
- `knowledge/sop/cross-company-handoff.md` — handoff protocol
- `knowledge/sop/cross-company-qa-routing.md` — QA gates before approval
- `SOUL.md` — Boundary #4 (root authority)
- `MAIN.md` — Main Assistant operational layer
