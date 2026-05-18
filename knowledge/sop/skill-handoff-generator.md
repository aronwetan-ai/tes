# Skill: Cross-Company Handoff Block Generator

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** Crypto Consultant, BrandFlow, NexusAI  
**Trigger:** Output from one company becomes input for another  
**Frequency:** 3x/week (Mon research→BrandFlow, Mon research→NexusAI, ad-hoc)  
**Risk Level:** Medium

---

## Purpose

Generate structured handoff blocks when output from one company becomes input for another. Ensures data integrity, constraint compliance, and automatic QA triggering across company boundaries.

---

## Prerequisites

- Source output ready (research report, design spec, data spec, tool status, content request)
- Target company identified
- Handoff type determined (research-to-content / data-spec / design-direction / tool-status / content-request)
- Access to task logger (tasks/inbox.jsonl)
- Understanding of Boundary #4 constraints

---

## Steps

### Step 1: Identify Handoff Direction

Determine source → target company:

```
Crypto Consultant → BrandFlow    (research translated to social content)
Crypto Consultant → NexusAI      (data spec for dashboards / tools)
BrandFlow → NexusAI              (design direction for product UI)
NexusAI → Crypto Consultant      (tool status / API availability)
NexusAI → BrandFlow              (product updates for marketing)
BrandFlow → Crypto Consultant    (client content needs requiring research)
```

**Example:** Crypto research report → BrandFlow social content

---

### Step 2: Select Type-Specific Template

Choose template based on handoff type:

```
research-to-content    → Crypto → BrandFlow (research translated to social)
data-spec              → Crypto → NexusAI (data points for dashboard)
design-direction       → BrandFlow → NexusAI (visual identity for implementation)
tool-status            → NexusAI → others (tool change notification)
content-request        → BrandFlow → Crypto (client needs research)
```

---

### Step 3: Populate Handoff Block

Create structured block in source output file:

```markdown
## [HANDOFF → <RECEIVING_COMPANY>]

| Field | Value |
|-------|-------|
| From | @crypto.research |
| To | @brandflow.copywriter |
| Date | 2026-05-19 10:00 UTC |
| Source file | companies/crypto-consultant/tasks/research-2026-05-19.md |
| Type | research-to-content |
| Priority | routine |
| Decay | 2026-05-26 (7 days) |

### Payload

[Type-specific content per template below]

### Constraints

- NO buy/sell language — "levels to watch" only
- NO removing bear case from content
- NO price targets framed as predictions
- NO removing disclaimer
- Source attribution required

### QA Requirement

- @crypto.qa reviews BrandFlow draft for factual accuracy
- @brandflow.qa reviews for brand consistency
- Trigger: AUTOMATIC when BrandFlow draft is complete

### Acknowledgment

- [ ] Received by: @brandflow.copywriter
- [ ] Understood constraints: yes/no
- [ ] Questions: <none / listed>
```

---

### Step 4: Populate Type-Specific Payload

#### Type 1: Research → Content (Crypto → BrandFlow)

```markdown
### Payload

Key message:        BTC up 3.8% this week amid macro uncertainty
Simplification:     Can simplify technical analysis for general audience
Key numbers:        BTC +3.8%, Fear & Greed 65, funding rates neutral
Scenario summary:   Bull 40% / Side 45% / Bear 15%
Risk to mention:    Macro headwinds could reverse gains quickly
Source report:      companies/crypto-consultant/tasks/research-2026-05-19.md
Forecast ID:        FL-2026-05-19-001
Decay window:       7 days (content must expire by 2026-05-26)
```

#### Type 2: Research → Data Spec (Crypto → NexusAI)

```markdown
### Payload

Data points required:
  - BTC price | CoinGecko API | hourly | USD
  - Fear & Greed | Alternative.me | daily | 0-100 scale
  - Funding rates | Binance API | 8-hourly | percentage

Display rules:
  - Scenarios shown as RANGES, never single numbers
  - Cycle phase as text + confidence badge
  - All timestamps visible to end user

API mapping:
  - crypto_tools.py → /api/v1/market/btc
  - fear_greed.py → /api/v1/sentiment/fear-greed
  - funding_rates.py → /api/v1/derivatives/funding

Disclaimer requirement: Yes — visible in UI footer
```

#### Type 3: Design Direction (BrandFlow → NexusAI)

```markdown
### Payload

Visual identity:
  - Color palette: #1F2937 (dark), #3B82F6 (primary), #10B981 (accent)
  - Typography: Inter (sans-serif), 16px body, 24px heading
  - Spacing: 8px grid system
  - Component style: Rounded corners (8px), subtle shadows

Brand constraints:
  - Must include BrandFlow logo in header
  - Avoid competitor color schemes (red/orange)
  - Accessibility: contrast ≥ 4.5:1 for all text

Reference: companies/brandflow/design/system-2026.md
```

#### Type 4: Tool/API Status (NexusAI → Others)

```markdown
### Payload

Tool/Endpoint:     fear_greed.py
Status change:     active → deprecated
Effective:         2026-06-01
Impact:            Endpoint will return 410 Gone after 2026-06-01
Migration:         Use alternative.me API directly (see docs)
New capability:    N/A

### Constraints

- Crypto Consultant must not reference deprecated tool output after 2026-06-01
- BrandFlow must update any content referencing old data format
```

#### Type 5: Content Request (BrandFlow → Crypto)

```markdown
### Payload

Client:            CryptoInfluencer Inc
Content type:      weekly brief
Audience:          public (subscribers)
Deadline:          2026-05-24
Scope:             BTC + ETH + macro context
Depth:             full-research (not quick-read)
Special focus:     Regulatory developments this week

### Constraints

- Research output follows standard 6-layer format
- Boundary #4 applies (no unsupervised financial advice)
- Deadline is REQUEST — quality over speed
```

---

### Step 5: Validate Constraints

Checklist before sending handoff:

```
For research-to-content:
  ✓ No buy/sell language present
  ✓ Bear case included (not minimized)
  ✓ Disclaimer present
  ✓ Source attribution included
  ✓ Numbers match source report exactly
  ✓ No deterministic language ("will", "guaranteed")

For data-spec:
  ✓ Scenarios shown as ranges, not points
  ✓ Disclaimer requirement stated
  ✓ Stale data warning specified
  ✓ No automated trading triggers

For design-direction:
  ✓ Accessibility standards (4.5:1 contrast) included
  ✓ Brand elements specified
  ✓ Off-brand elements explicitly forbidden

For tool-status:
  ✓ Effective date clear
  ✓ Migration path documented
  ✓ Impact on dependent systems stated

For content-request:
  ✓ Deadline realistic
  ✓ Scope clear and bounded
  ✓ Audience specified
```

---

### Step 6: Generate Cross-Company QA Entry

Automatically create QA trigger in task logger:

```jsonl
{
  "task_id": "T-CC-2026-05-19-001",
  "type": "CROSS_QA_REQUEST",
  "from": "@brandflow.copywriter",
  "to": "@crypto.qa",
  "subject": "Cross-QA: verify factual accuracy of BrandFlow crypto content",
  "source_handoff": "FL-2026-05-19-001",
  "source_report": "companies/crypto-consultant/tasks/research-2026-05-19.md",
  "derivative": "companies/brandflow/tasks/content-2026-05-19.md",
  "checklist": "factual-accuracy",
  "priority": "routine",
  "created": "2026-05-19T10:00:00Z"
}
```

---

### Step 7: Log Handoff to Both Companies

Add entries to both companies' task logs:

```jsonl
{
  "task_id": "T-HANDOFF-2026-05-19-001",
  "type": "HANDOFF_SENT",
  "from": "@crypto.research",
  "to": "@brandflow.copywriter",
  "subject": "Research handoff: weekly crypto brief",
  "handoff_type": "research-to-content",
  "source_file": "companies/crypto-consultant/tasks/research-2026-05-19.md",
  "decay": "2026-05-26",
  "timestamp": "2026-05-19T10:00:00Z"
}
```

---

## Input Format

```json
{
  "source_company": "crypto-consultant",
  "source_agent": "@crypto.research",
  "target_company": "brandflow",
  "target_agent": "@brandflow.copywriter",
  "handoff_type": "research-to-content",
  "source_file": "companies/crypto-consultant/tasks/research-2026-05-19.md",
  "priority": "routine",
  "decay_days": 7,
  "payload": { "key_message": "...", "numbers": [...] }
}
```

---

## Output Format

```
✅ Handoff block generated
Type: research-to-content
From: @crypto.research
To: @brandflow.copywriter
Decay: 2026-05-26
QA trigger: AUTOMATIC (T-CC-2026-05-19-001)
Status: Ready for receiving company acknowledgment
```

---

## Common Errors & Recovery

| Error | Cause | Recovery |
|-------|-------|----------|
| Handoff block missing/malformed | Template not followed | Return to sender with HANDOFF_INCOMPLETE flag. Re-submit. |
| Constraints violated (e.g., buy/sell language present) | Sender didn't validate | QA catches. Return to sender. Fix constraints. Re-submit. |
| Decay date missing | Sender forgot to set expiry | Add decay date. Re-submit. |
| Receiver doesn't acknowledge within 24h | Receiver offline or missed message | Task logger timeout alert. Operator escalates or re-routes. |
| QA fails and blocks delivery | Quality issue detected | QA documents issue with fix guidance. Sender fixes. Re-submit to QA. |

---

## Verification

- [ ] Handoff block present in source output
- [ ] All required fields populated (From, To, Date, Type, Priority, Decay, Payload, Constraints, QA Requirement)
- [ ] Type-specific payload matches template
- [ ] Constraints validated (no violations)
- [ ] Cross-company QA entry generated in task logger
- [ ] Both companies' task logs updated
- [ ] Receiving company acknowledges receipt + constraints understood

---

## Notes

- **Decay window:** Content/data expires after decay date. Receiving company must re-verify or refresh.
- **Constraints travel with data:** Boundary #4 rules carry over to derivative work.
- **QA automatic:** Cross-company QA triggered automatically when derivative work completed.
- **Acknowledgment required:** Receiver must acknowledge receipt + confirm constraints understood before proceeding.
- **Handoff lifecycle:** Produce → Log → Route → ACK → Work → QA → Approve → Deliver → Archive

---

## Related Skills

- Skill: Cross-Company QA Routing & Checklist Execution (triggered by handoff)
- Skill: Approval Request Formatter (approval comes after QA passes)
- SOP: cross-company-handoff.md (full specification)
- SOP: cross-company-qa-routing.md (QA routing triggered by handoff)
