# Step 4 — QA Chain Review (All 3 Companies)

Date: 2026-05-17 15:00 UTC
Type: Cross-company QA chain — each company reviews its own output

---

## QA-A: @crypto.qa — Research Report Review

**Reviewing:** `step-1-crypto-research-report.md`
**Skill loaded:** `skills/qa/SKILL.md` (7-Layer QA Pass)

### 7-Layer QA Pass Results

| Layer | Check | Result | Notes |
|-------|-------|--------|-------|
| 1. Format compliance | 6-layer present + ordered? | ✅ PASS | FACT→SOURCE→TREND→INTERPRET→SCENARIO→RISK NOTE all present in order |
| 2. Source verification | Every fact has source + timestamp? | ⚠️ PARTIAL | 14/16 facts sourced. **Issue:** "Wyckoff Phase C spring completed early May" — no source/timestamp. "ETF inflow $340M" — source is Farside Investors but no URL. |
| 3. Determinism scrub | Any "will" / "pasti" / "dijamin" language? | ✅ PASS | All probabilistic. "Boring bullish" is interpretation, acceptable. |
| 4. Bear-first check | Bear case stated before bull? | ✅ PASS | Bear (20%) → Sideways (35%) → Bull (45%). Correct order. |
| 5. Disclaimer present | Full bilingual disclaimer with decay window? | ✅ PASS | Present, includes decay (14 days), bilingual. |
| 6. Forecast Ledger entry | ID + horizon + invalidation + decay? | ✅ PASS | FL-2026-05-17-001, 14d horizon, invalidation specific ("weekly close <$66K with exchange net inflows >8K BTC/day for 5 days"). |
| 7. Calibration audit | Probabilities sum to 100%? Ranges, not points? | ✅ PASS | 45+35+20=100. Levels given as thresholds ($70.2K, $64.8K), not point targets. |

### Additional Checks (Senior QA — Update 12)

| Check | Result | Notes |
|-------|--------|-------|
| Pattern-recognition audit (force-fit detection) | ⚠️ FLAG | "Wyckoff Phase C spring completed" — this is stated as fact but Wyckoff identification is interpretive. Should be in [INTERPRET] layer, not implied in lens-read basis. Mild force-fit risk. |
| Source-tiering | ⚠️ FLAG | STH cost basis cited as "Glassnode public tier" — Glassnode public tier does NOT provide STH cost basis. That's a paid (Professional) metric. Source tier claim is inaccurate. |
| Wallet attribution tier | ✅ PASS | No specific wallets attributed to entities. Only aggregate tiers (T1 >10k BTC) mentioned. |
| Setup math check | ✅ PASS | Mayer Multiple 1.09 = price/200DMA = 68420/62400 ≈ 1.096. Checks out. |
| "If Wrong, So What?" audit | ✅ PASS | Each scenario has clear consequence. Risk Note mentions position sizing. |

### @crypto.qa Verdict

```
VERDICT:        CONDITIONAL PASS
SEVERITY:       2 × Medium, 1 × Low
BLOCKING:       No (none are Severity 1 / Critical)

ISSUES TO FIX BEFORE EXTERNAL PUBLISH:
  [MED-001] Wyckoff Phase C claim needs source or move to [INTERPRET] with caveat
  [MED-002] STH cost basis source tier incorrect — cannot claim "public tier" for paid metric.
            Fix: either cite alternative free source OR flag as "estimated from public data"
  [LOW-001] ETF flow citation missing URL — add Farside Investors link

PASS CONDITION: Fix MED-001 + MED-002 before external publish.
                Internal use (Fathur-only) → acceptable as-is with annotations.
```

---

## QA-B: @brandflow.qa — Content Review

**Reviewing:** `step-2-brandflow-content.md`
**Skill loaded:** `skills/qa/SKILL.md` (brand consistency + Boundary #4)

### Brand Consistency Check

| Check | Result | Notes |
|-------|--------|-------|
| Voice match | ⚠️ PARTIAL | No formal voice.md exists. Assumed voice used. Cannot confirm voice match without baseline. **GAP.** |
| Hook quality | ✅ PASS | Tweet 1 hook is specific, numbers-driven, contrarian-angle. Stops scroll. |
| One-idea-per-piece | ✅ PASS | Thread: weekly market read. Carousel: weekly market read. Single topic. |
| CTA clarity | ✅ PASS | "Save this thread. Revisit in 2 weeks." — specific, single, actionable. |
| No clichés | ✅ PASS | No "game-changer", "leverage", "synergy", "to the moon". Clean. |
| Channel format compliance | ✅ PASS | Thread: each tweet standalone. Carousel: 1 idea/slide. Story: 3-slide teaser. |
| Hashtags | ❌ FAIL | IG carousel has ZERO hashtags. Per channel norms, 5-10 required. Missing. |

### Boundary #4 Check (Financial Content)

| Check | Result | Notes |
|-------|--------|-------|
| No buy/sell language | ✅ PASS | "Levels to watch" framing used consistently. No directives. |
| Bear case preserved | ✅ PASS | Tweet 6 + Slide 6 both present bear case with specific levels. |
| Disclaimer present | ✅ PASS | Final tweet + final slide both carry disclaimer. |
| Source attribution | ✅ PASS | "Research by AI Holding Crypto Consultant" + date stated. |
| No price targets as predictions | ✅ PASS | "$70.2K" framed as "level to watch", not "target". |
| No over-simplification of risk | ✅ PASS | "If $64.8K breaks, the picture changes. Respect the levels." — risk conveyed. |

### Factual Accuracy Cross-Check (vs Step 1 report)

| Data point in content | Matches research report? | Result |
|---|---|---|
| "+3.8% week" | Step 1: "BTC 7D change: +3.8%" | ✅ Match |
| "F&G 71" | Step 1: "Fear & Greed Index: 71" | ✅ Match |
| "$340M ETF inflows" | Step 1: "BTC ETF net inflow (week): +$340M" | ✅ Match |
| "12,400 BTC left exchanges" | Step 1: "Exchange net flow 7D: -12,400 BTC" | ✅ Match |
| "LTH 72.1%" | Step 1: "LTH supply ratio: 72.1%" | ✅ Match |
| "Funding +0.008%" | Step 1: "Funding rate 8h avg: +0.008%" | ✅ Match |
| "DXY 103.8" | Step 1: "DXY: 103.8" | ✅ Match |
| "Bull 45% / Sideways 35% / Bear 20%" | Step 1: same | ✅ Match |
| "$70.2K bull / $64.8K bear" | Step 1: same | ✅ Match |
| "Stablecoins +8%" | Step 1: "Stablecoin exchange supply: +8% WoW" | ✅ Match |

**Factual accuracy: 10/10 data points match.** No distortion in translation.

### @brandflow.qa Verdict

```
VERDICT:        CONDITIONAL PASS
SEVERITY:       1 × Medium, 1 × Low
BLOCKING:       No

ISSUES TO FIX:
  [MED-003] No client voice profile — copywriter operated without verified voice.md.
            Cannot guarantee voice match. Escalate to @brandflow.ceo for voice capture.
  [LOW-002] IG carousel missing 5-10 hashtags. @brandflow.social should append before scheduling.

FACTUAL ACCURACY: 10/10 ✅ (no distortion from research to content)

BOUNDARY #4: COMPLIANT — no buy/sell, disclaimer present, bear case included, source cited.

PASS CONDITION: Add hashtags (LOW-002) before publish.
                Voice profile creation (MED-003) needed for ongoing client work, not blocking this single piece.
```

---

## QA-C: @nexusai.qa — Dashboard Spec Review

**Reviewing:** `step-3-nexusai-dashboard-spec.md`
**Skill loaded:** `skills/qa/SKILL.md` (technical review)

### Technical Spec Review

| Check | Result | Notes |
|-------|--------|-------|
| All states defined (loading/error/success) | ✅ PASS | Every component has loading + error + success. Plus: stale + partial states. Exceeds minimum. |
| Props typed | ✅ PASS | All props have TypeScript-style type annotations. |
| Accessibility | ✅ PASS | Every component has ARIA roles + labels. Keyboard nav noted in SparklineChart. |
| Responsive breakpoints | ✅ PASS | 3 breakpoints defined (desktop/tablet/mobile). |
| Data fetching strategy | ✅ PASS | Stale times per endpoint. Partial-success handling defined. |
| Error boundary | ⚠️ PARTIAL | Individual card errors handled. No top-level error boundary defined for full-page crash. |
| Security / auth | ❌ FAIL | Zero auth specification. Is this public or private? Who can access? Major gap for a financial data dashboard. |
| Performance | ✅ PASS | Lightweight chart lib (recharts/SVG), stale-while-revalidate pattern, no heavy D3. |

### Boundary #4 Check (Financial Data Display)

| Check | Result | Notes |
|-------|--------|-------|
| Disclaimer non-dismissible | ✅ PASS | DisclaimerFooter is fixed, always visible, cannot be hidden. |
| No price targets as predictions | ✅ PASS | KeyLevelsRange uses "level to watch" labels. |
| Scenarios shown as ranges | ✅ PASS | ScenarioBar shows percentage distribution, not single-number calls. |
| Bear-first rendering | ✅ PASS | Bear rendered left (first) in ScenarioBar. Convention preserved from research. |
| Source + freshness visible | ✅ PASS | MetricCard hover shows source + timestamp. DashboardHeader shows decay countdown. |

### Dependency/Blocker Check

| Dependency | Status | Blocking? |
|---|---|---|
| `/api/v1/etf-flow` — no Python tool exists | ❌ MISSING | **YES** — cannot build this endpoint without data source |
| `/api/v1/scenarios` — manual input from research | ⚠️ HUMAN-IN-LOOP | Partial — works if report exists, fails if late |
| Backend OpenAPI spec | ❌ MISSING | Non-blocking for spec, but blocks implementation |
| Design tokens file | ❌ MISSING | Non-blocking for spec, blocks pixel-perfect implementation |
| Auth/access control decision | ❌ MISSING | **YES** — architecture fundamentally differs for public vs private |

### @nexusai.qa Verdict

```
VERDICT:        CONDITIONAL PASS (spec quality)
                BLOCKED (implementation readiness)
SEVERITY:       2 × Critical (blocking), 2 × Medium
BLOCKING:       YES — cannot begin implementation without auth decision + ETF tool

ISSUES:
  [CRIT-001] Auth/access undefined. Public dashboard vs Fathur-only vs embed. 
             Architecture changes based on answer. BLOCKS IMPLEMENTATION.
  [CRIT-002] ETF flow data source missing. No tool in registry. BLOCKS one endpoint.
  [MED-004]  No top-level error boundary defined. Add React ErrorBoundary wrapper.
  [MED-005]  Backend OpenAPI spec needed before implementation starts.

SPEC QUALITY: HIGH — comprehensive, all states defined, accessible, responsive.
              Ready to implement once blockers resolved.

PASS CONDITION: Resolve CRIT-001 (Fathur decision) + CRIT-002 (build TOOL-033 or manual fallback).
```

---

## QA Chain Summary

| Company | Verdict | Issues | Blocking? |
|---------|---------|--------|-----------|
| Crypto Consultant | CONDITIONAL PASS | 2 Medium, 1 Low | No (internal use OK) |
| BrandFlow | CONDITIONAL PASS | 1 Medium, 1 Low | No (hashtags easy fix) |
| NexusAI | CONDITIONAL PASS (spec) / BLOCKED (impl) | 2 Critical, 2 Medium | **YES** |

### Cross-Company QA Observations

1. **Factual accuracy preserved end-to-end** ✅ — BrandFlow content matches research report 10/10 data points. No distortion in translation.
2. **Boundary #4 maintained end-to-end** ✅ — no buy/sell language at any stage, disclaimer present in all three outputs.
3. **Bear case preserved end-to-end** ✅ — research states it first, content includes it (tweet 6, slide 6), dashboard renders it first (left side of bar).
4. **No formal cross-company review routing exists** ⚠️ — @crypto.qa is supposed to review BrandFlow content for factual accuracy, but there's no mechanism to trigger this. Manual hand-waving only.
5. **Approval flow (Fathur) undefined** ⚠️ — every step says "needs Fathur approval" but there's no defined channel/mechanism/SLA for that approval.

---

## Issues Registry (All Steps Combined)

| ID | Severity | Company | Issue | Fix |
|----|----------|---------|-------|-----|
| MED-001 | Medium | Crypto | Wyckoff claim unsourced | Add source or move to INTERPRET |
| MED-002 | Medium | Crypto | STH cost basis source tier wrong | Fix source attribution |
| LOW-001 | Low | Crypto | ETF citation missing URL | Add Farside Investors URL |
| MED-003 | Medium | BrandFlow | No client voice profile | Create voice.md |
| LOW-002 | Low | BrandFlow | IG carousel missing hashtags | Add 5-10 hashtags |
| CRIT-001 | Critical | NexusAI | Auth/access undefined | Fathur decision needed |
| CRIT-002 | Critical | NexusAI | ETF flow tool missing | Build TOOL-033 |
| MED-004 | Medium | NexusAI | No error boundary | Add ErrorBoundary wrapper |
| MED-005 | Medium | NexusAI | No backend OpenAPI spec | @nexusai.backend to produce |
