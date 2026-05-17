# Cross-Company Integration Smoke Test

Test ID: INTEGRATION-001
Version: 1.0
Created: 2026-05-17
Run frequency: Weekly (Friday, as part of recap)
Duration: ~5 minutes (checklist-based, no full content production)

---

## Purpose

Quick verification that cross-company integration infrastructure is functional. This is NOT an E2E test (that's `tests/e2e-001-weekly-crypto-brief/`). This checks that the **plumbing works** — handoff formats are findable, QA routing triggers, approval flow is reachable.

---

## When To Run

- Every Friday as part of weekly recap (see `knowledge/sop/weekly-cadence.md`)
- After any SOP change in `knowledge/sop/`
- After adding/removing a company
- After major structural refactor

---

## Checklist

### A. Handoff Protocol Integrity

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| A1 | `knowledge/sop/cross-company-handoff.md` exists and is readable | | |
| A2 | All 5 handoff types documented (research→content, research→data, design-direction, tool-status, content-request) | | |
| A3 | Universal handoff block format has all required fields (From, To, Date, Source, Type, Priority, Decay, Payload, Constraints, QA, Ack) | | |
| A4 | Each active company MEMORY.md references the handoff SOP | | |

### B. QA Routing Integrity

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| B1 | `knowledge/sop/cross-company-qa-routing.md` exists | | |
| B2 | Routing matrix covers all active company pairs | | |
| B3 | Checklists A, B, C all present with specific items | | |
| B4 | SLA defined (4h same-company, 8h cross-company) | | |
| B5 | Conflict resolution path defined (QA → Operator → CEOs → Fathur) | | |

### C. Approval Workflow Integrity

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| C1 | `knowledge/sop/approval-workflow.md` exists | | |
| C2 | Approval request format defined with all fields | | |
| C3 | Response handling covers: yes / revise / no / hold / timeout | | |
| C4 | Timeout SLA defined (24h routine, 6h time-sensitive, 2h urgent) | | |
| C5 | Batch approval format documented | | |

### D. Autonomous Boundaries Integrity

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| D1 | `knowledge/sop/autonomous-boundaries.md` exists | | |
| D2 | Tier 1 (fully autonomous) list present | | |
| D3 | Tier 2 (autonomous with log) list present | | |
| D4 | Tier 3 (requires Fathur) list present | | |
| D5 | Escalation triggers defined with thresholds | | |
| D6 | Boundary #4 interpretation documented (public = Tier 3, internal = Tier 1/2) | | |

### E. Weekly Cadence Integrity

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| E1 | `knowledge/sop/weekly-cadence.md` exists | | |
| E2 | Monday-Friday timeline present with specific times (WIB) | | |
| E3 | Each action tagged with company + agent + autonomous tier | | |
| E4 | Daily tool execution schedule present | | |
| E5 | Trigger conditions (override) defined | | |
| E6 | Late/missed handling defined for each critical step | | |
| E7 | Fathur minimum commitment stated (<15 min/week target) | | |

### F. Cross-Company Commands

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| F1 | `COMMANDS.md` has "Cross-Company Commands" section | | |
| F2 | `weekly brief` command documented | | |
| F3 | `handoff crypto ke brandflow` command documented | | |
| F4 | `cross-qa status` command documented | | |
| F5 | `approval status` command documented | | |
| F6 | `weekly recap` command documented | | |
| F7 | `cadence status` command documented | | |

### G. Client Infrastructure

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| G1 | At least 1 client voice profile exists in `companies/brandflow/clients/` | | |
| G2 | Voice profile has all required fields (archetype, tone coordinates, vocabulary, emoji policy, CTA style) | | |
| G3 | Client voice profile is referenced in BrandFlow MEMORY.md | | |

### H. Company Memory Cross-References

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| H1 | `companies/crypto-consultant/MEMORY.md` has "Cross-Company Collaboration Protocol" section | | |
| H2 | `companies/brandflow/MEMORY.md` has "Cross-Company Collaboration Protocol" section | | |
| H3 | `companies/nexusai/MEMORY.md` has "Cross-Company Collaboration Protocol" section | | |
| H4 | Each section references the 5 SOP files | | |
| H5 | Each section describes the company's role in cross-company workflow | | |

---

## Scoring

- **ALL PASS (32/32):** Integration infrastructure healthy. No action needed.
- **28-31 PASS:** Minor drift. Log which items failed + schedule fix.
- **<28 PASS:** Significant gap. Escalate to Operator for immediate fix before next Monday.

---

## Result Log

_Append results here each time the test runs:_

```
[RUN] YYYY-MM-DD — Score: XX/32 — Notes: <any failures>
```

---

## Reference

- `knowledge/sop/weekly-cadence.md` — when this test runs (Friday)
- `tests/e2e-001-weekly-crypto-brief/` — full E2E test (more comprehensive)
- `knowledge/sop/autonomous-boundaries.md` — this test is Tier 1 (fully autonomous)
