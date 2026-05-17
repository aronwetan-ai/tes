# Derivatives Glossary — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.market`, `@crypto.research`, `@crypto.risk`

---

## Why This File

Crypto derivatives (perps, futures, options) account for the majority of crypto trading volume. Reading derivatives **positioning** is the third lens (alongside price and on-chain) for any senior view. This cheatsheet is the canonical glossary for the metrics that matter.

---

## Section 1 — Perpetual Futures (Perps)

### Funding Rate
**Definition**: Periodic payment between perp longs and shorts; mechanism to keep perp price aligned with spot.

**Calculation** (simplified): based on premium of perp price vs spot index.
- Positive funding = longs pay shorts (perp trades at premium; longs are crowded).
- Negative funding = shorts pay longs (perp trades at discount; shorts are crowded).

**Frequency**: typically every 8 hours (Binance, Bybit) or 1 hour (FTX legacy, dYdX).

**Reference levels** (8h periods, Binance BTC perp):
| Funding | State | Implication |
|---|---|---|
| <-0.05% | Extreme negative | Short-side crowded; squeeze potential |
| -0.05% to 0% | Mild bear positioning | |
| 0% to 0.01% | Neutral | |
| 0.01% to 0.05% | Mild bull positioning | |
| 0.05% to 0.1% | Bull-leaning | Watch |
| >0.1% sustained | Extreme positive | Long-side crowded; flush risk |

**Read**:
- Sustained extreme funding = positioning crowded = mean-reversion / liquidation cascade risk
- Funding flips during ranges = volatility incoming

**Tool**: `funding_rates.py`.

### Open Interest (OI)
**Definition**: Total notional value of open perp/futures positions.

**Read** (matrix):

| Funding | OI rising | OI falling | Implication |
|---|---|---|---|
| High positive | New longs piling in | Longs closing | Top risk if sustained |
| Low/negative | New shorts piling in | Shorts closing | Squeeze potential if low |
| Neutral | Healthy market | Position flush | Continuation likely |

**Tool**: `funding_rates.py --include-oi`.

### Liquidations
**Definition**: Forced position closure when margin insufficient.

**Read**:
- Long liquidation cascade = price flush down
- Short liquidation cascade = price squeeze up
- Both can mark short-term reversals

**Source**: Coinglass (free), exchange APIs.

### Premium / Basis
**Definition**: (Perp price - Spot price) ÷ Spot price.

**Read**:
- Positive premium = bullish positioning (longs crowded)
- Negative premium = bearish positioning (shorts crowded)
- Highly correlated with funding rate

---

## Section 2 — Quarterly Futures

### Annualized Basis
**Definition**: Annualized premium of dated futures (e.g. 90-day) over spot.

**Read**:
- Bull market: basis often 5-15% annualized
- Bear market: basis can flip negative (rare; signals stress)
- Cycle tops: basis often >20% annualized (extreme contango)

**Why it matters**: cash-and-carry traders arb basis; high basis = high speculative demand for leveraged longs.

### Term Structure
**Definition**: Comparison of basis across different futures expiries (1mo, 3mo, 6mo).

**Read**:
- Steep upward = strong bull positioning (more bullish further out)
- Flat or inverted = positioning uncertainty / bear

---

## Section 3 — Options

### Implied Volatility (IV)
**Definition**: Option-implied future volatility annualized.

**Read**:
- Rising IV = market pricing in larger moves (uncertainty)
- Falling IV = consolidation / complacency

**Source**: Deribit (BTC/ETH options market leader), Greeks.live.

### Put/Call Ratio
**Definition**: Open interest in puts ÷ open interest in calls.

**Read**:
- High (>1) = defensive positioning (puts dominant)
- Low (<0.5) = bullish positioning (calls dominant)
- Extreme readings often contrarian indicators

### Skew (25-Delta Risk Reversal)
**Definition**: IV of 25-delta puts minus IV of 25-delta calls.

**Read**:
- Positive skew = puts more expensive than calls (downside protection demand)
- Negative skew = calls more expensive than puts (upside speculation)
- Crypto historically negative skew during euphoria

### Gamma Exposure (GEX)
**Definition**: Aggregate dealer gamma positioning.

**Read**: large GEX clusters at strikes can cause magnetic price action (gamma squeeze / pin).

**Source**: Greeks.live, Genesis Volatility (paid).

---

## Section 4 — Cross-Asset Derivatives Reads

### Cumulative Volume Delta (CVD)
**Definition**: Cumulative buy-volume minus sell-volume.

**Read**: divergence between price and CVD = warning of trend exhaustion.

### Long/Short Ratio
**Definition**: Ratio of accounts long vs short on a given exchange.

**Read** (caveat: noisy, retail-heavy on most public APIs):
- Extreme one-sided positioning often contrarian
- Per-exchange variation important (Binance vs Bybit may differ)

### Smart Money Long/Short
**Definition**: Long/short ratio for top-tier accounts (large positions).

**Read**: contrast vs retail ratio. Smart money often counter-positioned to retail at extremes.

**Source**: Binance / Bybit account category data, Coinglass.

---

## Section 5 — Derivatives Cycle Patterns

### Cycle Top Derivatives Signature
- Funding rate sustained >0.1% per 8h
- OI at ATH
- Annualized basis >20%
- Smart money short / retail long (divergence)
- Skew positive (call-buying dominant)

### Cycle Bottom Derivatives Signature
- Funding rate negative for sustained period
- OI at multi-month low
- Annualized basis flat or negative
- Smart money long / retail short (divergence)
- Skew negative (put-buying dominant)

### Squeeze Signatures
- Negative funding + price holding above support = short squeeze setup
- Positive extreme funding + price stalling = long flush setup

---

## Section 6 — Tool Sources

| Source | Free? | Best for |
|---|---|---|
| Coinglass | Free + paid | Funding, OI, liquidations, long/short |
| Binance / Bybit / OKX APIs | Free | Direct exchange data |
| Deribit | Free | Options data |
| Greeks.live | Free + paid | Options analytics |
| Genesis Volatility | Paid | Pro options analytics |
| `funding_rates.py` | Local | Aggregates Binance/Bybit funding + OI |

---

## Anti-Patterns

- **Quoting funding without timeframe**: 0.01% per 8h ≠ 0.01% per 1h.
- **Single-exchange reads**: Binance perp ≠ Bybit perp ≠ OKX perp; aggregate or note exchange.
- **Ignoring spot/perp divergence**: spot bid + perp shorted = whale offloading; spot dump + perp bid = leveraged longs only.
- **Treating long/short ratio as fact**: retail-heavy data; smart money data needs different source.
- **Funding extremes treated as immediate reversal**: extremes can persist; combine with other lenses.
- **Ignoring options for major moves**: large gamma walls, expiry events shape price action.
- **Forgetting OI context**: high funding with rising OI ≠ high funding with falling OI.

---

## Reference

- `companies/crypto-consultant/skills/market-analysis/SKILL.md` (parent skill — derivatives overlay).
- `companies/crypto-consultant/skills/risk/SKILL.md` (Update 12 — leverage / liquidation context).
- `tools/funding_rates.py` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — derivatives signatures by cycle phase).
- This file paraphrases derivatives market terminology from exchange documentation and standard derivatives literature; content rephrased for licensing compliance.
