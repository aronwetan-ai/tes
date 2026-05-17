# Step 3 — @nexusai.frontend Dashboard Mockup Spec

Issued by: @nexusai.frontend (Frontend Engineer)
Date: 2026-05-17 13:00 UTC
Type: Component Spec — Weekly Crypto Dashboard Widget
Skills loaded: `skills/uiux/SKILL.md` + `skills/coding/SKILL.md`
Input: `step-1-crypto-research-report.md` [NEXUSAI HANDOFF] block

---

## Screen Flow

```
[SCREEN]      /dashboard/crypto-weekly
[ENTRY]       Sidebar nav → "Crypto Weekly" or direct link from BrandFlow embed
[DATA]        7 API calls (see Data Layer below)
[STATES]      Loading / Error / Success / Partial (some APIs fail) / Stale (data older than refresh window)
[INTERACTIONS] Hover tooltips on metrics, click scenario bar for detail, toggle between 7D/30D view
[EXIT]        External link to full research report (PDF/MD) or back to main dashboard
[EDGE CASES]  API timeout, stale data >24h, missing cycle phase (weekly refresh lag)
```

---

## Component Architecture

```
<WeeklyCryptoDashboard>
  ├── <DashboardHeader />          — title, report date, decay countdown
  ├── <MetricsGrid>
  │     ├── <MetricCard type="fear-greed" />
  │     ├── <MetricCard type="btc-price" />
  │     ├── <MetricCard type="funding-rate" />
  │     ├── <MetricCard type="etf-flow" />
  │     └── <MetricCard type="lth-supply" />
  ├── <CyclePhaseIndicator />      — text label + confidence badge
  ├── <ScenarioBar />              — bull/sideways/bear horizontal bar chart
  ├── <KeyLevelsRange />           — bull confirm / bear invalidate visual range
  ├── <SparklineChart />           — BTC 7D price chart
  └── <DisclaimerFooter />         — always visible, fixed bottom
```

---

## Component Specs

### 1. `<DashboardHeader />`

```
[COMPONENT]   DashboardHeader
[PROPS]       
  reportDate: string (ISO)      — "2026-05-17"
  decayDate: string (ISO)       — "2026-05-31"  
  forecastId: string            — "FL-2026-05-17-001"
[STATES]      
  success: shows title + dates + countdown
  stale: shows warning badge "Data may be outdated"
[BEHAVIOR]    
  - Countdown shows "Expires in X days" (calculated from decayDate - now)
  - If now > decayDate → red badge "EXPIRED — awaiting refresh"
[A11Y]        role="banner", aria-label="Weekly crypto dashboard header"
[CODE]        React + TypeScript (Next.js compatible)
```

### 2. `<MetricCard />`

```
[COMPONENT]   MetricCard
[PROPS]
  type: "fear-greed" | "btc-price" | "funding-rate" | "etf-flow" | "lth-supply"
  value: number
  label: string
  change: number (% change WoW)
  changeDirection: "up" | "down" | "flat"
  source: string
  timestamp: string (ISO)
  sparkline?: number[] (7 data points for mini chart)
[STATES]
  loading: skeleton pulse animation
  error: "—" with retry icon
  success: value + change arrow + sparkline
  stale: value shown with amber border + "Last updated: X hours ago"
[BEHAVIOR]
  - Hover: tooltip shows source + exact timestamp
  - Change arrow: green up / red down / gray flat
  - Sparkline: 7-point mini line chart (no axis labels, just shape)
[A11Y]        role="article", aria-label="{label}: {value}"
[USAGE]       5 instances in MetricsGrid
```

**Per-type configuration:**

| Type | Label | Format | Color coding | Source API |
|------|-------|--------|--------------|------------|
| fear-greed | Fear & Greed | 0-100 integer | 0-25 red, 26-45 orange, 46-55 gray, 56-75 green, 76-100 bright green | `/api/v1/fear-greed` |
| btc-price | BTC Price | $XX,XXX | green if change>0, red if <0 | `/api/v1/price/btc` |
| funding-rate | Funding Rate | 0.XXX% | green if <0.01%, yellow 0.01-0.05%, red >0.05% | `/api/v1/funding` |
| etf-flow | ETF Net Flow | $XXXM | green if positive, red if negative | `/api/v1/etf-flow` |
| lth-supply | LTH Supply | XX.X% | green if WoW change positive | `/api/v1/onchain/lth-supply` |

### 3. `<CyclePhaseIndicator />`

```
[COMPONENT]   CyclePhaseIndicator
[PROPS]
  phase: "accumulation" | "markup" | "distribution" | "markdown"
  confidence: "high" | "medium" | "low"
  description: string           — "Phase 3 — Markup post-halving"
  lastUpdated: string (ISO)
[STATES]
  loading: skeleton
  success: phase label + confidence badge + timeline visual
  stale: amber border, "Updated X days ago" warning
[BEHAVIOR]
  - Visual: 4-phase horizontal timeline, current phase highlighted
  - Confidence badge: H=green, M=yellow, L=orange
  - Tooltip on hover: shows basis for cycle phase read
[A11Y]        role="status", aria-live="polite"
```

### 4. `<ScenarioBar />`

```
[COMPONENT]   ScenarioBar
[PROPS]
  bull: { pct: number, label: string, levels: string }
  sideways: { pct: number, label: string, levels: string }
  bear: { pct: number, label: string, levels: string }
[STATES]
  loading: skeleton bar
  success: three-segment horizontal bar (green/yellow/red) with percentages
[BEHAVIOR]
  - Bar rendered left-to-right: Bear (red) | Sideways (yellow) | Bull (green)
  - NOTE: Bear rendered FIRST (left) to match Crypto Consultant "bear first" convention
  - Click/tap segment → expands detail panel with levels + conditions
  - Percentages shown inside bar if segment wide enough, above if narrow
[A11Y]        role="img", aria-label="Scenario distribution: Bear {X}%, Sideways {Y}%, Bull {Z}%"
```

### 5. `<KeyLevelsRange />`

```
[COMPONENT]   KeyLevelsRange
[PROPS]
  currentPrice: number
  bullLevel: number             — confirmation level
  bearLevel: number             — invalidation level
  bullLabel: string             — "Bull confirm"
  bearLabel: string             — "Bear invalidate"
[STATES]
  loading: skeleton
  success: horizontal range bar with current price marker
[BEHAVIOR]
  - Visual: horizontal bar from bearLevel to bullLevel
  - Current price shown as a dot/marker on the bar
  - Color gradient: red (left/bear) → yellow (middle) → green (right/bull)
  - Labels at each end
  - NEVER shows as "target" — labels say "level to watch"
[A11Y]        aria-label="Price range: bear below ${bearLevel}, bull above ${bullLevel}, current ${currentPrice}"
```

### 6. `<SparklineChart />`

```
[COMPONENT]   SparklineChart
[PROPS]
  data: { date: string, price: number }[] (7 days)
  height: number (default 120px)
  showAxis: boolean (default false for compact, true for expanded)
[STATES]
  loading: skeleton rectangle
  error: "Chart unavailable" text
  success: line chart with gradient fill
[BEHAVIOR]
  - Default: compact sparkline (no axes) in MetricsGrid area
  - Expanded: click to see with date axis + price axis
  - Line color: green if last > first, red if last < first
  - Tooltip on hover: shows date + exact price
[A11Y]        role="img", aria-label="BTC price chart, 7-day trend: {direction}"
```

### 7. `<DisclaimerFooter />`

```
[COMPONENT]   DisclaimerFooter
[PROPS]
  decayDays: number
  source: string                — "AI Holding Crypto Consultant"
  reportDate: string
[STATES]
  always visible (no loading/error state — static content)
[BEHAVIOR]
  - Fixed position at bottom of dashboard widget
  - Always visible regardless of scroll
  - Text: "Not financial advice. Data as of {reportDate}. Forecast decay: {decayDays} days. Source: {source}. DYOR."
  - Cannot be hidden/dismissed by user
[A11Y]        role="contentinfo", aria-label="Disclaimer"
```

---

## Data Layer

### API Contract Requirements (→ escalate to @nexusai.backend)

| Endpoint | Method | Response shape | Refresh | Source tool |
|----------|--------|---------------|---------|-------------|
| `/api/v1/fear-greed` | GET | `{ value: number, classification: string, timestamp: string, history_7d: number[] }` | Every 4h | fear_greed.py |
| `/api/v1/price/btc` | GET | `{ price: number, change_24h: number, change_7d: number, market_cap: number, history_7d: {date,price}[] }` | Every 1h | price_scraper.py |
| `/api/v1/funding` | GET | `{ rate_8h: number, avg_7d: number, oi_change_7d: number, exchange: string }` | Every 8h | funding_rates.py |
| `/api/v1/onchain/lth-supply` | GET | `{ ratio: number, change_7d: number, timestamp: string }` | Daily | onchain_metrics.py |
| `/api/v1/etf-flow` | GET | `{ net_flow_weekly: number, cumulative: number, timestamp: string }` | Daily | ⚠️ NO TOOL EXISTS |
| `/api/v1/cycle-phase` | GET | `{ phase: string, confidence: string, description: string, updated: string }` | Weekly | pattern_detector.py |
| `/api/v1/scenarios` | GET | `{ bull: {pct,levels}, sideways: {pct,levels}, bear: {pct,levels}, forecast_id: string, decay: string }` | Weekly | ⚠️ MANUAL — from research report |

### Data Fetching Strategy

```typescript
// React Query / TanStack Query pattern
const STALE_TIMES = {
  'fear-greed': 4 * 60 * 60 * 1000,   // 4h
  'btc-price': 1 * 60 * 60 * 1000,    // 1h
  'funding': 8 * 60 * 60 * 1000,      // 8h
  'lth-supply': 24 * 60 * 60 * 1000,  // 24h
  'etf-flow': 24 * 60 * 60 * 1000,    // 24h
  'cycle-phase': 7 * 24 * 60 * 60 * 1000, // 7d
  'scenarios': 7 * 24 * 60 * 60 * 1000,   // 7d (manual)
};

// Partial state handling:
// If 5/7 APIs succeed, show those 5 cards + error state on 2 failed cards.
// Never block entire dashboard for a single API failure.
```

---

## Responsive Design

| Breakpoint | Layout |
|------------|--------|
| Desktop (>1024px) | MetricsGrid: 5 cards in 1 row. ScenarioBar full width below. |
| Tablet (768-1024px) | MetricsGrid: 3+2 rows. Everything else stacks. |
| Mobile (<768px) | MetricsGrid: 1 card per row (scrollable). ScenarioBar vertical. |

---

## Visual Design Reference

Per @brandflow.designer spec from Step 2:
- BG: #0D1117 (dark)
- Accent green: #00D26A
- Accent red: #FF4757
- Accent yellow: #FFA502
- Text: #FFFFFF / #A0AEC0
- Font: Inter (system fallback: -apple-system, sans-serif)

---

## Tech Stack Assumptions

Per NexusAI SOUL + CTO guidance:
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript (strict)
- **State**: TanStack Query for server state
- **Styling**: Tailwind CSS
- **Charts**: lightweight — recharts or custom SVG (no heavy D3 for sparklines)
- **Deployment**: Vercel or self-hosted (per DevOps)

---

## Implementation Estimate

| Component | Complexity | Estimated hours |
|-----------|-----------|-----------------|
| MetricCard (generic) | Medium | 3h |
| DashboardHeader | Low | 1h |
| CyclePhaseIndicator | Medium | 2h |
| ScenarioBar | Medium | 3h |
| KeyLevelsRange | Medium | 2h |
| SparklineChart | Low-Medium | 2h |
| DisclaimerFooter | Low | 0.5h |
| Data layer (hooks + error handling) | Medium | 3h |
| Responsive layout | Low | 2h |
| **Total** | | **~18.5h** |

Backend API layer (7 endpoints wrapping Python tools) estimated separately by @nexusai.backend.

---

## E2E TEST NOTES — Step 3 Observations

### What Worked Well
1. **Handoff block from Crypto Consultant → spec** was smooth — data requirements clearly mapped to API endpoints.
2. **Component decomposition is clean** — single responsibility per component, composable.
3. **States fully defined** — loading, error, success, stale, partial all covered (per frontend.md mandate).
4. **Disclaimer non-dismissible** — Boundary #4 enforced at UI level.
5. **Bear-first convention carried to UI** — ScenarioBar renders bear on left.
6. **Decay countdown in header** — makes stale-data risk visible to end-user.

### Gaps Identified
1. **❌ No ETF flow tool exists** — `/api/v1/etf-flow` references data that no Python tool provides. Need TOOL-033 (etf_flow_scraper.py) or manual input. **Blocked.**
2. **❌ Scenarios endpoint is MANUAL** — `/api/v1/scenarios` requires @crypto.research to produce a report first. There's no automation. This is a human-in-the-loop dependency with no fallback if research is late.
3. **⚠️ No backend API spec exists** — @nexusai.backend hasn't produced OpenAPI spec for these 7 endpoints. Frontend is speccing without confirmed contract. Risk of mismatch.
4. **⚠️ Auth/access unclear** — Is this dashboard public (embed on influencer's site)? Or private (Fathur-only)? Access control not defined. Affects Boundary #4 significantly.
5. **⚠️ No design system documented** — Color palette from @brandflow.designer is referenced but NexusAI has no formal design tokens file. Should be `knowledge/software/design-tokens.md` or similar.
6. **⚠️ Embed vs standalone unclear** — Is this a full page (/dashboard/crypto-weekly) or an embeddable widget for the influencer's own site? Architecture differs significantly.
7. **⚠️ No error monitoring** — What happens when APIs fail? Alert to @nexusai.devops? Log to task logger? Undefined.
