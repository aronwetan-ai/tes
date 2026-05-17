# Cross-Company QA Routing

Version: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Scope: Automatic QA triggers when one company's output becomes another company's input

---

## Design Principle

> **QA follows the data, not the org chart.**

When Crypto Consultant research becomes BrandFlow content, *both* QA agents review — each for their own domain. This happens automatically via task logger entries. No manual coordination needed.

---

## Routing Rules

### Rule 1: Origin QA reviews derivative for ACCURACY

When Company A's output is used by Company B, Company A's QA automatically reviews Company B's derivative work for **factual fidelity**.

```
Crypto Consultant research → BrandFlow content
  └── @crypto.qa reviews BrandFlow draft for:
      - Data points match original report (number accuracy)
      - No distortion through simplification
      - Bear case preserved
      - Disclaimer present
      - No buy/sell language leaked in
      - Source attribution intact
```

### Rule 2: Destination QA reviews derivative for QUALITY

The receiving company's QA reviews for their own standards:

```
BrandFlow content (from Crypto research)
  └── @brandflow.qa reviews for:
      - Voice match (client profile)
      - Hook quality
      - Channel format compliance
      - No clichés / brand violations
      - CTA clarity
      - Hashtags / metadata present
```

### Rule 3: Both QA must PASS before delivery

```
Draft status flow:
  DRAFTED → @brandflow.qa review → @crypto.qa review → READY FOR APPROVAL
  
  If either QA FAILS:
    → Return to owning agent with fix guidance
    → After fix: re-submit to failing QA only (other QA pass is preserved)
```

---

## Trigger Mechanism

### How QA Gets Triggered (Automatic)

The system uses the task logger (`tasks/inbox.jsonl`) as the routing mechanism:

**Step 1:** When BrandFlow completes a draft derived from Crypto research:

```jsonl
{"task_id": "T-BF-2026-05-19-001", "type": "QA_REQUEST", "from": "@brandflow.copywriter", "to": "@brandflow.qa", "subject": "QA review: weekly crypto brief thread", "source_handoff": "FL-2026-05-17-001", "path": "tests/e2e-001/step-2-brandflow-content.md", "priority": "routine", "created": "2026-05-19T09:00:00Z"}
```

**Step 2:** Simultaneously, cross-company QA entry auto-generated:

```jsonl
{"task_id": "T-CC-2026-05-19-001", "type": "CROSS_QA_REQUEST", "from": "@brandflow.copywriter", "to": "@crypto.qa", "subject": "Cross-QA: verify factual accuracy of BrandFlow crypto content", "source_handoff": "FL-2026-05-17-001", "source_report": "step-1-crypto-research-report.md", "derivative": "step-2-brandflow-content.md", "checklist": "factual-accuracy", "priority": "routine", "created": "2026-05-19T09:00:00Z"}
```

**Rule:** The cross-QA entry is generated AUTOMATICALLY when:
- A draft is completed (status → DRAFTED)
- The draft has a `source_handoff` field pointing to another company's output

No manual triggering needed. The task logger pattern does it.

---

## QA Routing Matrix

| Source Company | Derivative Company | Origin QA Reviews For | Destination QA Reviews For |
|---|---|---|---|
| Crypto Consultant | BrandFlow | Factual accuracy, Boundary #4 compliance, bear case presence | Voice, brand, channel format, CTA, hooks |
| Crypto Consultant | NexusAI | Data mapping correctness, display rules compliance, disclaimer presence | Technical quality, states, a11y, performance, security |
| BrandFlow | NexusAI | Brand consistency in implementation, visual fidelity | Technical quality, responsive, accessible |
| NexusAI | Crypto Consultant | Tool output accuracy, API reliability | Research methodology compliance, 6-layer format |
| NexusAI | BrandFlow | Feature accuracy in marketing claims | Copy quality, audience match |

---

## QA Checklists (Per Routing Type)

### Checklist A: @crypto.qa reviewing BrandFlow content

```markdown
## Cross-QA: Crypto → BrandFlow Factual Review

Source report:    <path>
Derivative:       <path>
Forecast ID:      <FL-YYYY-MM-DD-NNN>

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 1 | All numbers in content match source report | | |
| 2 | No numbers invented that aren't in source | | |
| 3 | Bear case mentioned (not hidden/minimized) | | |
| 4 | No buy/sell language | | |
| 5 | Disclaimer present (marketing version acceptable) | | |
| 6 | Source attribution present | | |
| 7 | No deterministic language ("will", "pasti", "guaranteed") | | |
| 8 | Scenario framing uses ranges, not point targets | | |
| 9 | Risk/invalidation mentioned | | |
| 10 | Decay/expiry date stated or implied | | |

VERDICT: PASS / FAIL
If FAIL: <which items failed + fix guidance>
```

### Checklist B: @crypto.qa reviewing NexusAI data display

```markdown
## Cross-QA: Crypto → NexusAI Data Display Review

Source spec:      <path>
Implementation:   <path or endpoint>
Data points:      <list>

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 1 | Data values match tool output (no transformation errors) | | |
| 2 | Scenarios shown as ranges, not point targets | | |
| 3 | Disclaimer visible and non-dismissible | | |
| 4 | Stale data shows warning (beyond refresh window) | | |
| 5 | Source + timestamp visible per data point | | |
| 6 | No "prediction" framing — "levels to watch" only | | |
| 7 | Bear case not hidden in UI (rendered first or equally) | | |
| 8 | Color coding doesn't imply recommendation | | |

VERDICT: PASS / FAIL
```

### Checklist C: @brandflow.qa reviewing NexusAI implementation

```markdown
## Cross-QA: BrandFlow → NexusAI Visual Review

Design spec:      <path>
Implementation:   <path or screenshot>

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 1 | Color palette matches spec (within 1 shade tolerance) | | |
| 2 | Typography matches (family, size hierarchy, weight) | | |
| 3 | Visual hierarchy preserved (focal → secondary → tertiary) | | |
| 4 | Brand elements present where required | | |
| 5 | No off-brand elements introduced | | |
| 6 | Responsive behavior preserves brand intent | | |
| 7 | Accessibility maintained (contrast ≥ 4.5:1 for text) | | |

VERDICT: PASS / FAIL
```

---

## SLA (Service Level Agreement)

| QA Type | Expected turnaround | Escalation if exceeded |
|---------|--------------------|-----------------------|
| Same-company QA (routine) | 4 hours | Alert to company CEO agent |
| Cross-company QA (routine) | 8 hours | Alert to Operator |
| Same-company QA (urgent) | 1 hour | Alert immediately |
| Cross-company QA (urgent) | 2 hours | Alert to Operator + company CEOs |

**If QA doesn't respond within SLA:**
1. Auto-reminder sent to QA agent
2. If still no response after 2x SLA: Operator manually reviews OR escalates to Fathur

---

## QA Result Logging

Every QA pass/fail logged to the respective company's `tasks/logs.jsonl`:

```jsonl
{"task_id": "T-CC-2026-05-19-001", "type": "CROSS_QA_RESULT", "reviewer": "@crypto.qa", "subject": "BrandFlow weekly crypto thread", "verdict": "PASS", "issues": [], "timestamp": "2026-05-19T12:00:00Z"}
```

Or on failure:
```jsonl
{"task_id": "T-CC-2026-05-19-001", "type": "CROSS_QA_RESULT", "reviewer": "@crypto.qa", "subject": "BrandFlow weekly crypto thread", "verdict": "FAIL", "issues": [{"id": "MED-001", "severity": "medium", "description": "Tweet 3 states 12,500 BTC but source says 12,400", "fix": "Change to 12,400"}], "timestamp": "2026-05-19T12:00:00Z"}
```

---

## Bypass Rules (When Cross-QA Can Be Skipped)

Cross-company QA can be skipped ONLY when:

1. **Purely internal, Fathur-only audience** — no public surface, no client delivery
2. **Tool status notification** — NexusAI notifying others of a tool change (informational, not content)
3. **Identical re-publish** — same content, already QA'd, no changes, within decay window

Cross-company QA CANNOT be skipped when:
- Content goes to any public surface (even internal re-share that might leak)
- Data is displayed in a product/dashboard
- Client-facing in any way
- Contains financial data/scenarios

---

## Conflict Resolution

If origin QA and destination QA disagree:

```
Example: @crypto.qa says "this simplification distorts the research"
         @brandflow.qa says "this simplification is necessary for the audience"

Resolution path:
1. Both QA agents state their position with specific reasoning
2. Route to Operator for initial mediation
3. If unresolved: escalate to both company CEOs
4. If still unresolved: Fathur decides

Principle: ACCURACY wins over SIMPLIFICATION for financial content.
           If it can't be simplified without distortion, it's better to not include that point.
```

---

## Weekly QA Health Check

Every Friday, Operator verifies:
- [ ] All cross-QA requests from this week were responded to within SLA
- [ ] No FAIL verdicts left unresolved
- [ ] No bypasses used inappropriately
- [ ] Checklists used (not just rubber-stamp "PASS")

Logged to `memory/global.md` as `[QA_HEALTH]` entry.

---

## Reference

- `knowledge/sop/cross-company-handoff.md` — triggers handoff that triggers QA
- `knowledge/sop/approval-workflow.md` — QA must pass BEFORE approval request sent
- `knowledge/sop/autonomous-boundaries.md` — QA is Tier 1 (fully autonomous)
- `knowledge/agent-design/task-logger-rules.md` — inbox.jsonl format
- `companies/crypto-consultant/skills/qa/SKILL.md` — 7-Layer QA Pass
- `companies/brandflow/skills/qa/SKILL.md` — brand QA checklist
