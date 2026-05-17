# Crypto Consultant Skill Index

Versi: 1.1
Last updated: 2026-05-17 (post Update 12 — Crypto Consultant deepening)

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → Crypto Consultant SOUL.

---

## Active Skills (8 parent + 3 agent-specific deep skills = 11 total)

### Parent Skills (used by multiple agents)

| Skill | Path | Primary Users |
|---|---|---|
| research | `skills/research/SKILL.md` | @crypto.research, @crypto.ceo, @crypto.report |
| market-analysis | `skills/market-analysis/SKILL.md` | @crypto.market, @crypto.research |
| onchain | `skills/onchain/SKILL.md` | @crypto.onchain, @crypto.research |
| macro | `skills/macro/SKILL.md` | @crypto.macro, @crypto.research |
| risk | `skills/risk/SKILL.md` | @crypto.risk, @crypto.research |
| reporting | `skills/reporting/SKILL.md` | @crypto.report, @crypto.writer, @crypto.ceo |
| qa | `skills/qa/SKILL.md` | @crypto.qa, @crypto.report, @crypto.ceo |
| **pattern-recognition** (NEW Update 12) | `skills/pattern-recognition/SKILL.md` | @crypto.market, @crypto.onchain, @crypto.macro, @crypto.research, @crypto.risk |

### Agent-Specific Deep Skills (Update 12)

These extend a parent skill with depth that's primarily owned by one agent. They're loaded in addition to (not instead of) the parent skill.

| Skill | Path | Owner | Parent |
|---|---|---|---|
| cycle-models | `skills/pattern-recognition/cycle-models.md` | @crypto.market | pattern-recognition |
| whale-tracking-playbook | `skills/onchain/whale-tracking-playbook.md` | @crypto.onchain | onchain |
| global-liquidity | `skills/macro/global-liquidity.md` | @crypto.macro | macro |

---

## What Was Deepened in Update 12

Each parent skill now has a **Senior Patterns (Deep Dive)** section appended. Highlights:

- **research** — 3-Lens Convergence Test (price + on-chain + derivatives) with macro overlay; Forecast Ledger discipline; Brier-style calibration; senior synthesis output template; anti-stitching-disagreeing-lenses.
- **market-analysis** — Top-down workflow (cycle phase → macro regime → 1M → 1W → 1D → 4H → tactical); cycle-anchored pattern library; volume-confirmed structure; dominance + rotation reading; derivatives overlay; multi-timeframe conflict resolution.
- **onchain** — 5-level on-chain hierarchy (network health → supply → flow → cohort → entity); exchange flow forensic decomposition; cohort behavior patterns; MVRV/Mayer/NUPL bands; T1-T4 wallet tier framework; stablecoin flow read; hashrate / difficulty / miner health.
- **macro** — Liquidity-first mental model; 5 macro drivers ranked; Fed Watch tier discipline (T1-T4); macro calendar discipline; cross-asset correlation regime; DXY cheat sheet.
- **risk** — Drawdown-floor table by asset class; survivability calculator; correlation-cluster sizing; tail scenario library (7 categories); cycle-phase risk posture; position lifecycle; counterparty-risk quarterly review; "stop means stop" rule.
- **reporting** — Report tier discipline (5 tiers); expanded mandatory disclaimer with decay window; "Bear First" rendering; source-citation standard; "what's-new" filter; crisis update discipline; external-publish gate (per-piece Fathur authorization); cross-company handoff templates.
- **qa** — 7-Layer QA Pass; severity calibration crypto-specific; pattern-recognition audit (force-fit detection); calibration audit (Brier scoring post-horizon); source-tiering check; wallet-attribution-tier audit; setup math check; "If Wrong, So What?" audit.

### Pattern-Recognition (New Parent Skill — Update 12)

A new parent skill that turns the 4-year cycle, on-chain bands, and recurring formations from "story" into operational pattern detection backed by base rates and invalidation conditions.

**Core discipline**: 3 Guards
1. Pattern has a **name and a source** (literature reference)
2. **Base rate stated** (sample size, hit rate, failure rate, time to resolution)
3. **Invalidation stated before confirmation**

**Pattern libraries** organized in 4 domains:
- Cycle (Pi top, MVRV-Z extremes, Mayer, 200W MA, NUPL, RHODL, halving timing)
- Structural (Wyckoff schematics, range tests, classical TA)
- On-chain (LTH/STH supply, exchange flow, stablecoin issuance, hashrate)
- Macro (yield curve, DXY, M2, Fed pivot, real yield rollover)

**Convergence logic**: 4-level confidence framework + macro overlay; disagreement among indicators is the read.

---

## Removed Skills (Not Relevant for This Company)

These were boilerplate from the original template; removed because Crypto Consultant doesn't ship code, design, or content — it produces research:

- `coding` — engineering → NexusAI.
- `devops` — infrastructure → NexusAI.
- `content` — marketing copy → BrandFlow.
- `automation` — pipelines → NexusAI handles infra; tools used by Crypto Consultant come from `tools/`.
- `uiux` — product UI → NexusAI.
- `business` — business / SOP → CEO + identity files.

---

## Tools Available to Crypto Consultant Agents (post Update 12)

All entries in `knowledge/tools/tool-registry.md`.

**Update 12 crypto-specific tools (5 new, all Risk=Low):**
- `tools/price_scraper.py` (TOOL-028) — multi-asset OHLCV from CoinGecko.
- `tools/news_scraper.py` (TOOL-029) — multi-source crypto RSS + sentiment heuristic.
- `tools/pattern_detector.py` (TOOL-030) — pi_top / btc_bottom / mayer / cross / mvrv_zone / cycle_phase detection over OHLCV.
- `tools/onchain_metrics.py` (TOOL-031) — hashrate / mempool / TVL / stablecoin from public APIs.
- `tools/funding_rates.py` (TOOL-032) — Binance + Bybit perp funding history + OI.

**Existing tools relevant to Crypto Consultant:**
- `tools/fear_greed.py` (TOOL-001) — Crypto Fear & Greed Index.
- `tools/btc_price.py` (TOOL-002) — BTC price / change / market cap.
- `tools/news_sentiment.py` (TOOL-003) — CryptoPanic headline scan.
- `tools/api_health.py` (TOOL-016) — endpoint health probes.
- Task logger system (TOOL-005..012) — shared across companies.

What Crypto Consultant does NOT build: see `knowledge/scope/declined-tools.md` Item 5 (automated guaranteed-signal / auto-trading bot).

---

## Knowledge References (post Update 12)

Domain knowledge files relevant to Crypto Consultant agents. See `companies/crypto-consultant/SOUL.md` for the per-task loading guidance.

**Crypto cheatsheets (10 files in `knowledge/crypto/`):**
- `crypto-research-framework.md` (foundational SOP — pre-existing)
- `four-year-cycle.md` (5-phase model + halving table + cycle compression)
- `cycle-indicators.md` (Tier A/B/C/D library: 200W MA, Mayer, MVRV-Z, NUPL, RHODL, Pi cycle, etc.)
- `wyckoff-method.md` (3 laws + accumulation/distribution schematics + crypto application)
- `onchain-metrics-glossary.md` (~30 metrics across network / supply / cohort / valuation / flow / DeFi)
- `derivatives-glossary.md` (perps / futures / options / cycle signatures)
- `global-liquidity.md` (liquidity hierarchy + 12-week lag + 5 drivers + Fed Watch tiers)
- `risk-sizing-methods.md` (drawdown floors + Kelly capped + correlation clusters + cycle posture)
- `scenario-modeling.md` (3+2 scenarios + probability discipline + range required)
- `news-source-rubric.md` (T1-T5 source tiering + citation format)
- `forecast-evaluation.md` (Forecast Ledger + Brier scoring + post-mortem template)

**Cross-cutting:**
- `knowledge/scope/declined-tools.md` — Item 5 is Crypto-specific (auto-trading bot decline).
- `knowledge/agent-design/memory-rules.md`, `tool-use-rules.md`, `task-logger-rules.md`.

---

## How To Use

Agents call skills by reference, not duplication. When a task arrives:

1. Identify which skill(s) apply (parent skill + agent-specific deep skill if you own one).
2. Read the skill file for process + output format.
3. Apply the skill's rules to the task.
4. Use the skill's output template.
5. Load relevant `knowledge/crypto/*` cheatsheets per the skill's References section.

If a skill conflicts with the agent's Tier 3 SOUL, the SOUL wins (it's more specific). If a skill conflicts with the company's Tier 2 SOUL, the SOUL wins. Root SOUL always wins above all.

---

## Boundary #4 — Maximum Strength for Crypto

Crypto research has **financial consequences**. Every skill here treats output that could leave the holding as gated:

- **research, market-analysis, onchain, macro, risk, pattern-recognition** — produce internal analysis with 6-layer format.
- **reporting** — final assembly + mandatory disclaimer (with decay window per Update 12).
- **qa** — 7-Layer QA Pass with hardcoded enforcement; checks disclaimer + risk-language compliance + ledger entry before ship.

Public-facing output requires explicit Fathur per-piece approval (via `@crypto.ceo`). Internal use ships after `@crypto.qa` review.

The new pattern-recognition skill explicitly forbids buy/sell calls per its 3-Guard discipline; pattern firing = signal to investigate, never directive to act.

---

## 6-Layer Format (Cross-Skill Standard)

All analytical skills produce output in 6 layers:

```
[FACT]       — measurable data with timestamp
[SOURCE]     — where data came from + when (T1-T5 tier when applicable)
[TREND]      — pattern in the data
[INTERPRET]  — what the pattern typically means
[SCENARIO]   — bull / sideways / bear (BEAR FIRST) with relative likelihood + ranges
[RISK NOTE]  — what could invalidate the read
```

Update 12 additions:
- Forecast ledger entry for any multi-week-horizon view
- Decay window stated explicitly
- Source tier (T1-T5) noted per fact
- Invalidation conditions specific and observable

Mandated by `knowledge/crypto/crypto-research-framework.md` + `companies/crypto-consultant/SOUL.md` Prediction Discipline.

---

## Adding New Skills

When a behavior pattern emerges that's used by 2+ agents and isn't covered:

1. Decide if it should be **company-specific** (here) or **cross-company** (`knowledge/sop/`).
2. Decide if it's a **parent skill** (multi-agent, broad) or an **agent-specific deep skill** (extends a parent, owned by one agent).
3. Create file:
   - Parent: `skills/<skill-name>/SKILL.md`
   - Deep: `skills/<parent-skill-name>/<deep-skill-name>.md`
4. Use the standard front-matter:
   ```yaml
   ---
   name: skill-name
   description: One-line description.
   company: Crypto Consultant
   used_by: ["@crypto.role1", "@crypto.role2"]
   # for deep skills also include:
   # agent_specific: "@crypto.<role>"
   # parent_skill: <parent-skill-name>
   ---
   ```
5. Update this index.
6. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference

- `companies/crypto-consultant/SOUL.md` (Tier 2 — company personality, Prediction Discipline, knowledge loading order).
- `companies/crypto-consultant/AGENTS.md` (role roster).
- `knowledge/crypto/crypto-research-framework.md` (foundational domain SOP).
- `knowledge/scope/declined-tools.md` (scope boundaries; Item 5 Crypto-specific).
- `knowledge/tools/tool-registry.md` (full tool registry, 32 entries post Update 12).
