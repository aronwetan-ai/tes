# Step 1 — @crypto.research Weekly Market Synthesis

Issued by: @crypto.research (Research Lead)
Date: 2026-05-17 09:00 UTC
Type: Weekly Market Brief (Week of 2026-05-12 → 2026-05-17)
Skill loaded: `skills/research/SKILL.md` + `skills/pattern-recognition/SKILL.md`
Tools called: fear_greed.py, btc_price.py, pattern_detector.py, onchain_metrics.py, funding_rates.py

---

## SYNTHESIS — Crypto Consultant Research

Forecast ID: FL-2026-05-17-001
Issued: 2026-05-17 09:00 UTC
Decay window: 14 days (expires 2026-05-31)
Cycle phase read: Phase 3 — Markup post-halving (confidence: Medium)

---

### LENS READS

**Lens 1 — PRICE / TA** (via @crypto.market + pattern_detector.py)
- Reading: **Bullish-leaning sideways**
- Basis: BTC holding above 200D MA ($62,400). Weekly close sequence: higher lows since April 28. Mayer Multiple at 1.09 — neutral zone, not overheated. No Pi Cycle Top signal firing. RSI(14) daily at 58 — mid-range, room to run. Key resistance: $70,200 (Jan 2025 high retest). Key support: $64,800 (50D MA).
- Pattern: Wyckoff Phase C spring completed early May; now testing creek resistance.

**Lens 2 — ON-CHAIN** (via @crypto.onchain + onchain_metrics.py)
- Reading: **Mixed — cautiously bullish**
- Basis: LTH supply ratio increasing (accumulation signal). Exchange net outflows 7-day: -12,400 BTC (bullish). BUT: STH cost basis at $66,200 — current price near STH breakeven (risk of weak-hand selling on dips). MVRV-Z at 1.4 — mid-range, not overheated but not cheap. Stablecoin supply on exchanges up 8% WoW (dry powder available).
- Concern: Whale tier (T1, >10k BTC) flat — big players not adding aggressively.

**Lens 3 — DERIVATIVES** (via funding_rates.py)
- Reading: **Neutral-to-bullish**
- Basis: Funding rate 8h avg: +0.008% (slightly positive, not frothy). OI increased 6% WoW — new positions being built, not just leverage on existing. Binance + Bybit long/short ratio: 1.12 (slight long bias). No extreme crowding. Liquidation heatmap: heavy longs clustered at $63K; heavy shorts at $71K.
- Note: Derivatives NOT leading this move — spot-driven, which is healthier.

**Macro liquidity overlay** (via @crypto.macro)
- Regime: **Neutral-to-expanding**
- Basis: DXY at 103.8, down from 105.2 four weeks ago (dollar weakening = risk-on). Fed June meeting (2026-06-18): market pricing 72% hold. M2 global liquidity 12-week lag suggests mild tailwind arriving June-July. US 10Y at 4.28%, stable. No acute macro stress.

**Narrative overlay** (via news_scraper.py)
- Dominant story: ETF inflow re-acceleration ($340M net inflow this week across spot BTC ETFs).
- Secondary: Ethereum Pectra upgrade hype drawing attention to ETH, pulling some altcoin rotation.
- Sentiment: news_sentiment.py → 62% positive, 28% neutral, 10% negative (past 7 days).

---

### CONVERGENCE STATE

```
Price/TA:      Bullish-leaning sideways
On-chain:      Cautiously bullish (mixed)
Derivatives:   Neutral-to-bullish

Result: PARTIAL CONVERGENCE (2.5/3 bullish-leaning, on-chain has caveats)
Macro:         Supportive (neutral-to-expanding liquidity)
Narrative:     Supportive (ETF flows + weakening DXY)
```

---

### 6-LAYER OUTPUT

**[FACT]**
- BTC price: $68,420 (CoinGecko, 2026-05-17 09:00 UTC)
- BTC 7D change: +3.8%
- Fear & Greed Index: 71 (Greed) — 7D avg: 68
- Mayer Multiple: 1.09 (neutral)
- 200D MA: $62,400 — price well above
- Exchange net flow 7D: -12,400 BTC (outflows)
- LTH supply ratio: 72.1% (+0.4% WoW)
- STH cost basis: $66,200
- MVRV-Z: 1.4
- Stablecoin exchange supply: +8% WoW
- Funding rate 8h avg: +0.008%
- OI change WoW: +6%
- DXY: 103.8 (down from 105.2 four weeks ago)
- Fed June pricing: 72% hold
- BTC ETF net inflow (week): +$340M
- Hashrate: 618 EH/s (ATH)

**[SOURCE]**
- BTC price: CoinGecko via price_scraper.py (2026-05-17 09:00 UTC)
- F&G: Alternative.me via fear_greed.py (2026-05-17 09:00 UTC)
- Mayer Multiple: pattern_detector.py calculation (2026-05-17 09:00 UTC)
- Exchange flows: CryptoQuant via onchain_metrics.py (2026-05-17 08:00 UTC, 1h lag)
- LTH/STH data: Glassnode public tier via onchain_metrics.py (2026-05-16 close)
- MVRV-Z: Glassnode public tier via onchain_metrics.py (2026-05-16 close)
- Stablecoin supply: DefiLlama via onchain_metrics.py (2026-05-17 06:00 UTC)
- Funding/OI: Binance + Bybit via funding_rates.py (2026-05-17 08:00 UTC)
- DXY: TradingView (2026-05-16 NY close)
- Fed pricing: CME FedWatch (2026-05-16)
- ETF flows: Farside Investors (2026-05-16 close)
- Hashrate: blockchain.com via onchain_metrics.py (2026-05-17 06:00 UTC)

**[TREND]**
- 7D: BTC grinding higher, low-volatility uptrend. F&G stable in Greed (65-72 range all week).
- 30D: Recovery from $61K low (April 20) to current $68.4K. +12% in 4 weeks.
- 90D: Post-halving markup underway. Classic Phase 3 pattern: slow grind, low retail attention, institutional accumulation via ETFs.
- On-chain: LTH accumulating, exchanges draining, but whale tier flat — big players watching, not chasing.
- Derivatives: Healthy — spot-leading, not leverage-leading. Funding mild. No froth signals.
- Macro: DXY retreating slowly. Global liquidity 12-week lag model suggests June-July tailwind.

**[INTERPRET]**
- The three lenses partially converge on a constructive setup. Price structure is healthy (higher lows, above key MAs, no froth indicators). On-chain supports accumulation thesis but whale passivity is a caution flag — the move lacks "big conviction" from largest holders.
- Derivatives confirm this isn't a leverage-driven pump — it's organic/spot. This makes the trend more durable but slower.
- Macro is neutral-to-supportive. DXY decline + liquidity model suggest the wind is at BTC's back for the next 4-8 weeks. Key macro risk: CPI surprise or hawkish Fed June surprise.
- Narrative is supportive (ETF flows). But ETF flows are lagging indicators — they follow price, not lead it.
- Net read: **Constructive setup with limited downside protection below $64.8K.** Not euphoric, not cheap. "Boring bullish."
- The signal I'd weight most: exchange outflows + LTH accumulation + spot-driven move. The signal I'd weight least: F&G (lagging sentiment indicator).

**[SCENARIO]**

Bear case (20% likelihood):
- Trigger: CPI hot print → Fed June hawkish surprise → DXY reversal above 106 → risk-off.
- Path: BTC loses $64.8K (50D MA) → triggers STH selling (cost basis $66.2K, now underwater) → cascade to $58K-$60K support band.
- Timeframe: If triggered, plays out in 1-2 weeks.
- Invalidation of bear: BTC holds $64.8K on retest with volume.

Sideways case (35% likelihood):
- Trigger: Market waits for Fed June clarity + ETH rotation absorbs attention.
- Path: BTC ranges $65K-$70K for 2-4 weeks. Low volatility. Boring.
- Timeframe: Through June 18 (Fed meeting).
- Invalidation of sideways: Breakout above $70.2K with >$2B daily spot volume.

Bull case (45% likelihood):
- Trigger: DXY continues weakening + ETF inflows sustain $300M+/week + $70.2K resistance breaks.
- Path: BTC clears $70.2K → psychological $72K → next major target $76K-$78K (measured move from April low).
- Timeframe: If $70.2K breaks, 2-4 week move to $76K zone.
- Invalidation of bull: Weekly close below $66K.

**[RISK NOTE]**
- Primary risk: Fed June meeting (2026-06-18). If dot plot shifts hawkish, entire bullish thesis pauses.
- Secondary risk: Whale tier passive — if big players don't confirm accumulation within 2 weeks, grind could stall.
- Structural risk: STH cost basis at $66.2K = potential air pocket. A dip below that triggers mechanical selling.
- Unknown: Geopolitical event risk (unmodeled).
- Position sizing note: cycle Phase 3 posture per `risk-sizing-methods.md` = moderate allocation (50-70% target), not max exposure.

---

### FORECAST LEDGER ENTRY

```
[FORECAST LEDGER ENTRY]
ID:               FL-2026-05-17-001
Issued:           2026-05-17 09:00 UTC
Issuer:           @crypto.research
Horizon:          14 days (decay 2026-05-31)
Cycle phase:      Phase 3 — Markup post-halving (confidence: Medium)
Lens convergence: PARTIAL — price+derivatives bullish-leaning, on-chain mixed
View summary:     Bull 45% / Sideways 35% / Bear 20%
Key levels:       BTC bull confirm >$70.2K; bear invalidate <$64.8K
Key catalysts:    Fed June meeting (06-18); ETF flow continuation; DXY trajectory
Invalidation:     Weekly close <$66K with exchange net inflows >8K BTC/day for 5 days
Refresh trigger:  Fed June statement; BTC closes above $70.2K or below $64.8K
Reviewed at:      Post-event refresh required after Fed June
```

---

### CONTRIBUTORS

- @crypto.research — synthesis, convergence test, ledger entry
- @crypto.market — price/TA lens, Wyckoff read, key levels
- @crypto.onchain — exchange flows, LTH/STH, whale tier, stablecoin supply
- @crypto.macro — DXY, Fed Watch, liquidity model, M2 lag
- @crypto.risk — scenario probability framing, position sizing note, invalidation levels

---

### METHODOLOGY

Per `knowledge/crypto/crypto-research-framework.md` — 6-layer format.
Senior synthesis per `skills/research/SKILL.md` — 3-Lens Convergence Test.
Pattern recognition per `skills/pattern-recognition/SKILL.md`.

---

### DISCLAIMER

DISCLAIMER

Analisis ini dibuat oleh AI Holding Crypto Consultant untuk keperluan
riset internal. Bukan merupakan financial advice.

Probabilitas yang disebutkan di laporan ini adalah estimasi berbasis data
saat ini, bukan prediksi pasti. Skenario dan range harga adalah kerangka
berpikir, bukan target eksekusi.

Crypto market moves fast. Read decay window: 14 days. Setelah window
ini, baca ulang sebelum dipakai.

Selalu lakukan riset mandiri (DYOR) sebelum mengambil keputusan investasi.
Position sizing keputusan pribadi.

(English) This analysis is produced by AI Holding Crypto Consultant for
internal research purposes. Not financial advice. Probabilities stated
are estimates based on current data, not certain predictions. Scenarios
and price ranges are thinking frameworks, not execution targets. Forecast
decay: 14 days. Always do your own research (DYOR).

---

### HANDOFF — FOR BRANDFLOW

```
[BRANDFLOW HANDOFF]
Original research:       tests/e2e-001-weekly-crypto-brief/step-1-crypto-research-report.md
Translation guidance:    
  - Key message: "BTC in constructive-boring-bullish setup. Higher lows, ETF inflows, spot-driven."
  - Simplify 3-lens to: "price healthy, wallets accumulating, no leverage froth"
  - Key number to highlight: +3.8% week, F&G 71, $340M ETF inflows
  - Scenario summary: "mostly up (45%), maybe flat (35%), small chance dip (20%)"
  - Risk to mention: Fed June meeting could change everything
Off-limits framing:
  - NO "buy now" / "this is your chance" / "guaranteed gains"
  - NO specific price targets as "predictions" — always frame as "levels to watch"
  - NO removing the disclaimer
  - NO oversimplifying bear case (must mention it)
Disclaimer requirement: Yes — marketing-adapted version required in thread/carousel
Source citation:         At minimum mention "AI Holding Crypto Consultant research" + data date
Review on draft:         @crypto.qa reviews factual accuracy before publish
```

### HANDOFF — FOR NEXUSAI

```
[NEXUSAI HANDOFF]
Data spec required:
  - Fear & Greed Index (current + 7D sparkline)
  - BTC price (current + 7D chart)
  - Funding rate (current + 7D avg)
  - Cycle phase indicator (text: "Phase 3 — Markup")
  - Scenario widget (bear/side/bull percentages as bar)
  - Key levels (bull >$70.2K / bear <$64.8K as range indicator)
  - ETF net flow (weekly number)
  - LTH supply ratio (current + trend arrow)
Refresh frequency: Daily (except cycle phase = weekly)
Display rules:
  - Scenarios shown as ranges, NEVER single number targets
  - Cycle phase as text label with confidence badge (H/M/L)
  - F&G shown with color coding (green/yellow/red)
  - All numbers show source + freshness timestamp
Disclaimer in product: Required — fixed footer element, always visible
API sources:
  - fear_greed.py → /api/v1/fear-greed
  - price_scraper.py → /api/v1/price/btc
  - funding_rates.py → /api/v1/funding
  - onchain_metrics.py → /api/v1/onchain/lth-supply
  - pattern_detector.py → /api/v1/cycle-phase (weekly refresh)
```

---

## E2E TEST NOTES — Step 1 Observations

### What Worked Well
- 6-layer format applied cleanly
- 3-Lens Convergence Test produced a nuanced read (not forced bullish)
- Forecast Ledger entry has specific invalidation criteria
- Bear case stated first with clear trigger
- All data sourced with timestamps
- Both handoff blocks (BrandFlow + NexusAI) produced

### Potential Gaps Identified (Preliminary)
1. **No actual tool execution** — tools referenced but this is simulated data. In production, tools would need to actually run and return real values.
2. **No client voice profile** — BrandFlow handoff doesn't reference a `clients/<crypto-influencer>/voice.md` file. That file doesn't exist yet.
3. **Handoff format is ad-hoc** — reporting SKILL.md has a template, but it's the first time actually used. Might need standardization.
4. **No task logger entry** — this research task wasn't logged to `tasks/inbox.jsonl` as protocol requires.
5. **STH cost basis source** — cited "Glassnode public tier" but public tier may not have this metric. Source verification needed.
