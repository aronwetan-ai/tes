# E2E Test #001 — Weekly Crypto Brief for Crypto Influencer Client

Test ID: E2E-001
Date: 2026-05-17
Tested by: Operator (Kiro)
Status: IN PROGRESS

---

## Scenario

**Client:** A crypto influencer who is a BrandFlow client. They need a weekly market update translated into social media content (Twitter thread + IG carousel) backed by real research, plus a dashboard mockup to display weekly numbers to their audience.

**Flow:**
```
Crypto Consultant (research)
        ↓ [HANDOFF: research report]
BrandFlow (copywriter + designer + social)
        ↓ [HANDOFF: data spec]
NexusAI (frontend dashboard mockup)
        ↓
QA chain (all 3 companies)
        ↓
Gap analysis
```

---

## Steps

### Step 1 — @crypto.research produces Weekly Market Report

**Input:** "Produce a weekly crypto market brief for week of 2026-05-12 to 2026-05-17. BTC-focused. Use 3-Lens Convergence Test + Forecast Ledger entry."

**Expected Output:**
- Senior synthesis with 3-Lens reads (Price/TA, On-chain, Derivatives)
- Macro + narrative overlay
- Convergence state labeled
- 6-layer format (FACT → SOURCE → TREND → INTERPRET → SCENARIO → RISK NOTE)
- Forecast Ledger entry (FL-2026-05-17-001)
- Bear case first in scenarios
- Disclaimer present

**Agent chain:** `@crypto.research` → pulls `@crypto.market` + `@crypto.onchain` + `@crypto.macro` + `@crypto.risk` → hands to `@crypto.report`

---

### Step 2 — @brandflow.copywriter translates to Twitter Thread + IG Carousel

**Input:** The research report from Step 1 + a BrandFlow handoff block.

**Expected Output:**
- Twitter/X thread (5-7 tweets): hook tweet stands alone, each tweet self-contained, CTA last tweet
- IG carousel script (6-8 slides): 1 idea per slide, hook slide, CTA slide
- Voice adapted to crypto-influencer client (bold, direct, slightly edgy)
- Disclaimer maintained (marketing version)
- No buy/sell language (Boundary #4 carried through)

**Agent chain:** `@brandflow.copywriter` + `@brandflow.designer` (visual spec) + `@brandflow.social` (calendar slot)

---

### Step 3 — @nexusai.frontend produces Dashboard Mockup Spec

**Input:** Data spec from Crypto Consultant (F&G + BTC price + funding rates + cycle phase) + BrandFlow design direction.

**Expected Output:**
- Component spec: weekly-crypto-dashboard
- States: loading / error / success / partial
- Data requirements: API endpoints, refresh frequency
- Visual hierarchy: what the eye sees first
- Mobile-responsive consideration

**Agent chain:** `@nexusai.frontend` (component spec) + references `@nexusai.backend` (API contract)

---

### Step 4 — QA Chain

Each company's QA reviews its own output:
- `@crypto.qa` → 7-Layer QA Pass on research report
- `@brandflow.qa` → brand consistency + no Boundary #4 violation on copy
- `@nexusai.qa` → technical review on dashboard spec

---

### Step 5 — Gap Analysis

Document:
- Missing handoff formats / templates
- Missing tools
- Missing skills
- Boundary discipline issues
- Process friction points
- Cross-company communication gaps

---

## Success Criteria

1. Research report follows 6-layer + senior synthesis template perfectly
2. BrandFlow output maintains factual accuracy from research (no distortion)
3. NexusAI spec is implementable from the data available
4. QA catches at least 1 issue per company (proves QA is working)
5. Handoff between companies is smooth with defined format
6. Boundary #4 respected end-to-end (no buy/sell, disclaimer present everywhere)

---

## Gaps Found (filled during test)

_To be documented in Step 5._
