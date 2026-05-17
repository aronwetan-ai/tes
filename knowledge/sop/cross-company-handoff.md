# Cross-Company Handoff Protocol

Version: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Scope: All inter-company data/content/spec transfers within AI Holding

---

## Purpose

When output from Company A becomes input for Company B, the handoff must be **explicit, structured, and auditable**. No informal "just send it over" — every handoff has a block, a trigger, and a verification step.

This SOP ensures:
- Data integrity across company boundaries
- Boundary #4 compliance travels with the data
- QA knows what to review (see `cross-company-qa-routing.md`)
- The system can run autonomously without Fathur in the loop for routine handoffs

---

## Handoff Directions (Active)

| From | To | Use Case | Frequency |
|------|----|----------|-----------|
| Crypto Consultant → BrandFlow | Research translated to social content | Weekly (Monday brief) + ad-hoc |
| Crypto Consultant → NexusAI | Data spec for dashboards / tools | Weekly refresh + schema changes |
| BrandFlow → NexusAI | Design direction for product UI | Per campaign / per feature |
| NexusAI → Crypto Consultant | Tool status / API availability | On change |
| NexusAI → BrandFlow | Product updates for marketing | On release |
| BrandFlow → Crypto Consultant | Client content needs requiring research | On demand |

---

## Universal Handoff Block Format

Every handoff MUST include this structured block in the output file:

```markdown
## [HANDOFF → <RECEIVING_COMPANY>]

| Field | Value |
|-------|-------|
| From | @<company>.<agent> |
| To | @<company>.<agent> (primary receiver) |
| Date | YYYY-MM-DD HH:MM UTC |
| Source file | <path to originating document> |
| Type | research-to-content / data-spec / design-direction / tool-status / content-request |
| Priority | routine / urgent / blocking |
| Decay | YYYY-MM-DD (after this date, re-verify before using) |

### Payload
<The actual content being handed off — structured per type-specific template below>

### Constraints
- <What the receiver CANNOT do with this data>
- <Boundary #4 rules that carry over>
- <Simplification limits>

### QA Requirement
- <Which QA agent reviews the derivative work>
- <Trigger: automatic / on-request>

### Acknowledgment
- [ ] Received by: @<receiver>
- [ ] Understood constraints: yes/no
- [ ] Questions: <none / listed>
```

---

## Type-Specific Templates

### Type 1: Research → Content (Crypto Consultant → BrandFlow)

```markdown
### Payload
Key message:        <1-2 sentence synthesis — what the research says in plain language>
Simplification:     <What CAN be simplified for audience>
Key numbers:        <3-5 headline stats to use>
Scenario summary:   <Bull X% / Side Y% / Bear Z% — one line>
Risk to mention:    <Single biggest risk the content must include>
Source report:      <path to full report>
Forecast ID:       <FL-YYYY-MM-DD-NNN>
Decay window:       <N days — content must expire by this date>

### Constraints
- NO buy/sell language — "levels to watch" only
- NO removing bear case from content
- NO price targets framed as predictions
- NO removing disclaimer
- Source attribution required (min: "AI Holding Crypto Consultant, data as of YYYY-MM-DD")
- DO NOT invent numbers not in source report

### QA Requirement
- @crypto.qa reviews BrandFlow draft for factual accuracy
- @brandflow.qa reviews for brand consistency
- Trigger: AUTOMATIC when BrandFlow draft is complete (see cross-company-qa-routing.md)
```

### Type 2: Research → Data Spec (Crypto Consultant → NexusAI)

```markdown
### Payload
Data points required:
  - <metric name> | source tool | refresh frequency | format
  - <metric name> | source tool | refresh frequency | format
  - ...
Display rules:
  - <How data must be rendered — ranges not points, etc.>
  - <Color coding rules>
  - <Freshness indicator requirement>
API mapping:
  - <tool.py> → <suggested endpoint path>
  - ...
Disclaimer requirement: <yes — describe where it appears in UI>

### Constraints
- Scenarios shown as RANGES, never single numbers
- Cycle phase as text + confidence badge, never as "guaranteed" phase
- All timestamps visible to end user
- Stale data must show warning (age > refresh window)
- NO automated trading triggers from displayed data

### QA Requirement
- @nexusai.qa reviews technical implementation
- @crypto.qa reviews data accuracy post-integration
- Trigger: on API endpoint go-live + weekly spot-check
```

### Type 3: Design Direction (BrandFlow → NexusAI)

```markdown
### Payload
Visual identity:
  - Color palette: <hex values + roles>
  - Typography: <font family, sizes, weights>
  - Spacing: <system — 4px/8px grid?>
  - Component style: <rounded/sharp, shadow/flat, etc.>
Brand constraints:
  - <What must be present — logo, colors, etc.>
  - <What must be avoided — competitor styles, etc.>
Reference:         <link to design spec or brandflow/designer output>

### Constraints
- NexusAI implements the direction, does not redesign
- Changes to brand direction must go back through @brandflow.designer
- Accessibility standards (contrast 4.5:1+) override visual preference

### QA Requirement
- @brandflow.qa visual review post-implementation
- Trigger: on deploy to staging
```

### Type 4: Tool/API Status (NexusAI → Crypto Consultant / BrandFlow)

```markdown
### Payload
Tool/Endpoint:     <name>
Status change:     <active → deprecated / new / breaking change / downtime>
Effective:         <YYYY-MM-DD>
Impact:            <What breaks / what's new / what changes>
Migration:         <Steps if breaking change>
New capability:    <What's now possible that wasn't before>

### Constraints
- Crypto Consultant must not reference deprecated tool output after effective date
- BrandFlow must update any content referencing old data format

### QA Requirement
- Receiving company QA verifies their workflows still function
- Trigger: AUTOMATIC on status change
```

### Type 5: Content Request (BrandFlow → Crypto Consultant)

```markdown
### Payload
Client:            <client name or ID>
Content type:      <weekly brief / ad-hoc analysis / specific topic>
Audience:          <who will see this — public / subscriber / private>
Deadline:          <YYYY-MM-DD>
Scope:             <BTC only / multi-asset / specific topic>
Depth:             <quick-read / full-research / deep-dive>
Special focus:     <Any specific angles client wants>

### Constraints
- Research output follows standard 6-layer format regardless of request
- Boundary #4 applies regardless of client audience
- Deadline is a REQUEST — quality over speed, but flag if impossible

### QA Requirement
- @crypto.qa reviews research output (standard)
- @brandflow.qa reviews final translated content
- Trigger: standard pipeline
```

---

## Handoff Lifecycle

```
1. PRODUCE    — Source company creates output with handoff block
2. LOG        — Task logger entry in BOTH companies (see task-logger-rules.md)
3. ROUTE      — Receiving company's inbox gets entry (automatic — see weekly-cadence.md)
4. ACK        — Receiver acknowledges receipt + constraints understood
5. WORK       — Receiver produces derivative work
6. QA         — Cross-company QA triggered (see cross-company-qa-routing.md)
7. APPROVE    — Per approval-workflow.md (autonomous for routine, Fathur for public)
8. DELIVER    — Final output ships
9. ARCHIVE    — After decay date, handoff is marked expired
```

---

## Autonomous vs Fathur-Required Handoffs

| Handoff Type | Autonomous? | Reason |
|---|---|---|
| Crypto → BrandFlow (internal client brief) | ✅ Yes | Routine weekly workflow |
| Crypto → BrandFlow (public publish) | ❌ Fathur approves final | Boundary #4 — public financial content |
| Crypto → NexusAI (data spec) | ✅ Yes | Internal infrastructure |
| BrandFlow → NexusAI (design direction) | ✅ Yes | Internal infrastructure |
| NexusAI → others (tool status) | ✅ Yes | Operational notification |
| BrandFlow → Crypto (new client research request) | ⚠️ Fathur if new client | Scope decision |
| Any → public surface | ❌ Fathur approves | Boundary #4 always |

Detail: see `knowledge/sop/autonomous-boundaries.md`.

---

## Failure Modes + Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Handoff block missing/malformed | Receiving QA rejects | Return to sender with "HANDOFF_INCOMPLETE" flag |
| Factual distortion in translation | Cross-company QA catches (see routing SOP) | BrandFlow revises, re-submit to @crypto.qa |
| Decay expired, content still live | Weekly cadence check (see weekly-cadence.md) | Archive/remove/refresh — whichever applies |
| Receiver doesn't ACK within 24h | Task logger timeout alert | Operator escalates or re-routes |
| QA fails and blocks delivery | QA documents issue with fix guidance | Fix → re-submit → QA re-check |

---

## Reference

- `knowledge/sop/approval-workflow.md` — decision authority matrix
- `knowledge/sop/cross-company-qa-routing.md` — QA trigger mechanism
- `knowledge/sop/weekly-cadence.md` — timing of routine handoffs
- `knowledge/sop/autonomous-boundaries.md` — what runs without Fathur
- `knowledge/agent-design/task-logger-rules.md` — logging entries
- `companies/crypto-consultant/skills/reporting/SKILL.md` — original handoff templates
- `COMMANDS.md` — natural language triggers
