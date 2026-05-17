# Risk Sizing Methods — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.risk`, `@crypto.research`

---

## Why This File

Crypto downside is asymmetric. -90% drawdowns are normal. Recoveries take cycles. This file is the **canonical reference** for position-sizing math, capital allocation methods, and survival-first risk frameworks.

Senior risk work uses these formulas with explicit drawdown floors and correlation cluster caps — never gut-feel sizing.

---

## Section 1 — The Survival-First Frame

```
SIZING PRIORITY ORDER:

1. Capital survival under tail event       (mandatory floor)
2. Cycle drawdown survival                 (must survive cycle bear)
3. Correlation cluster cap                 (don't overweight one driver)
4. Per-trade risk %                        (granular sizing)
5. Expected return / Kelly                 (last; not first)
```

Junior sizing leads with Kelly / expected return. Senior sizing leads with **survival**.

---

## Section 2 — Drawdown Floors by Asset Class

Assume on entry; size to survive these:

| Position type | Drawdown floor | Recovery time |
|---|---|---|
| BTC long (cycle hold) | -85% from cycle top | 1-3 cycles |
| ETH long (cycle hold) | -90% from cycle top | 1-3 cycles |
| Top-10 alt long | -95% from cycle top | Often >1 cycle; some never |
| Mid-cap alt long | -98% from cycle top | Often never recovers |
| Small-cap / new alt | -99-100% (effectively zero) | Most go to zero |
| LP / DeFi yield | -100% (smart contract risk) | Total loss possible |
| Stablecoin yield | -10% (peg break) + protocol risk | Variable |
| Centralized exchange custody | -100% (counterparty risk) | FTX precedent |
| Memecoin | -100% (likely) | Don't expect recovery |

**Rule**: Position size that does not survive its own drawdown floor is the **wrong size**. Always.

---

## Section 3 — Per-Trade Risk %

Standard frame:

```
Per-position risk = capital × per-trade risk %

Per-trade risk %:
  Conservative (cycle-trading)    1-2%
  Standard (active swing)         2-3%
  Aggressive (high-conviction)    up to 5%
  NEVER                           above 5% on single position
```

**Rationale**: At 5% per trade, 4 consecutive max losses = -20% of capital, recoverable. At 10%, same scenario = -40%, harder to recover psychologically and mathematically.

---

## Section 4 — Position Sizing Formula

```
Position size = (capital × per-trade risk %) ÷ (entry - stop) × 1/leverage

Example:
  Capital:           $100,000
  Per-trade risk %:  2%
  Entry:             $70,000
  Stop:              $66,000 (5.7% below entry)
  Leverage:          1x (spot)

  Risk dollars:      $100,000 × 0.02 = $2,000
  Stop distance:     $70,000 - $66,000 = $4,000
  Coins to buy:      $2,000 ÷ $4,000 = 0.5 BTC
  Position value:    0.5 × $70,000 = $35,000
```

This says: "If stop hits, lose exactly $2,000 (2% of capital)."

---

## Section 5 — Kelly Criterion (Capped)

The Kelly formula gives optimal sizing for known edge:

```
Kelly fraction = (W × R - L) / R

  W = win probability
  R = win/loss ratio (avg win / avg loss)
  L = loss probability (1 - W)
```

**Example**: 60% win rate, 2:1 win/loss ratio:
- Kelly = (0.60 × 2 - 0.40) / 2 = 0.4 = 40% of capital per trade

**Senior application**:
- Full Kelly assumes perfect knowledge of probabilities (you don't have)
- Crypto edges are noisy; estimates have wide error bars
- Use **Half-Kelly or Quarter-Kelly** in practice
- Never exceed 5% per trade regardless of Kelly output

**Why Kelly capping**:
- Underestimating loss probability by 10% can flip Kelly from positive to ruinous
- Crypto's fat-tail distribution makes Kelly assumptions optimistic
- Survival > optimization

---

## Section 6 — Fixed-Fractional Sizing

Simpler than Kelly, more robust:

```
Position size = capital × fixed fraction

E.g.:
  Capital × 2%  per trade (standard)
  Capital × 5%  for high conviction (rare)
  Capital × 10% for cycle-anchor positions like BTC core (long horizon)
```

**Advantage**: doesn't require probability estimation; simple to implement; consistent.

**Disadvantage**: doesn't account for varying setup quality.

---

## Section 7 — Volatility-Targeted Sizing

Size positions to target equal **portfolio volatility contribution**:

```
Position size = (target portfolio vol × portfolio value) / (asset vol × correlation)
```

**Use case**: portfolio with mixed assets where you want each to contribute equally to risk, not equally to dollar value.

**Crypto-specific challenge**: most crypto correlates highly to BTC; vol-targeting often results in BTC dominating allocation.

---

## Section 8 — Correlation Cluster Sizing

Crypto correlates. Treat correlated assets as **one position** for risk purposes:

```
CLUSTER 1 — Bitcoin proxy
  BTC, BTC ETF (IBIT/FBTC), MicroStrategy (MSTR — equity proxy)
  Sized as one position

CLUSTER 2 — Ethereum proxy
  ETH, ETH ETF, ETH-correlated L2 tokens
  Sized as one position

CLUSTER 3 — High-beta L1
  SOL, AVAX, ADA, DOT — all high-beta to ETH/BTC
  Sized as one cluster

CLUSTER 4 — DeFi blue-chip
  AAVE, UNI, LDO, MKR
  Sized as one cluster

CLUSTER 5 — Memecoin
  Treat the whole memecoin allocation as one position cap

CLUSTER 6 — Stablecoin yield
  Treat by protocol, not by asset
```

**Senior portfolio defaults**:
- Cluster cap typically 20% of crypto allocation per cluster
- BTC + ETH allowed up to 40% combined
- Single-asset cap typically 25% of crypto allocation

---

## Section 9 — Cycle-Phase-Aware Sizing

Risk posture changes with cycle phase:

| Cycle phase | Default posture | Per-trade risk % | Cash buffer |
|---|---|---|---|
| Phase 1 (Accumulation) | Aggressive accumulation | 3-5% | 5-15% |
| Phase 2 (Pre-halving markup) | Standard | 2-3% | 10-20% |
| Phase 3 (Post-halving markup) | Standard with trim | 2-3% | 15-25% |
| Phase 4 (Distribution / top) | Defensive | 1-2% | 30-50% |
| Phase 5 (Markdown / bear) | Capital preservation | 0.5-1% | 50-80% |

**Why**: bull market = more risk OK. Bear market = capital preservation. Reverse this and the cycle eats you.

---

## Section 10 — Tail Scenario Library

Senior risk maintains a permanent library of tail scenarios with sizing implications:

| Scenario | Probability over 12mo | Portfolio impact | Mitigation |
|---|---|---|---|
| Major exchange insolvency (FTX-class) | ~5-10% in any 12mo | -20-40% if exposed | Self-custody primary holdings; spread CEX exposure |
| Regulatory enforcement (US/EU) | ~15-30% | -10-30% sector-specific | Limit exposure to regulatory-target sectors |
| BTC ETF flow reversal | ~20% | -15-25% on BTC | Watch flow data; position trim |
| Stablecoin de-peg (USDT/USDC) | ~3-5% | catastrophic if held in stables | Diversify stables; some self-custody |
| Smart contract exploit (top-10 protocol) | ~10% in any 12mo | -100% on exposed allocation | Cap LP/DeFi positions; prefer audited protocols |
| Macro shock (rate panic, geo event) | ~25% in any 12mo | -20-50% all-asset | Maintain cash buffer 15-25% |
| 51% attack on minor chain | ~varies | -100% on that chain | Don't hold significant on small-network L1s |

These are **estimates**, not predictions. The point is **sizing such that any one of them happening doesn't ruin the portfolio**.

---

## Section 11 — Stop Loss Discipline

```
RULE 1: Stop level defined BEFORE entry
RULE 2: Stop placed AT entry (never "I'll watch")
RULE 3: Mental stops fail under stress; written/programmed stops survive
RULE 4: When stop hits, EXIT — no exceptions
RULE 5: Trailing stops trail; never move them backward
RULE 6: Slippage in fast markets is real; pre-stop is preferred
```

**Senior risk produces setups assuming mechanical execution**. If Fathur won't execute mechanically, position size must drop further to compensate.

---

## Section 12 — The Three-Question Pre-Size Test

Before sizing any setup, three questions:

```
Q1. If this goes to drawdown floor, can capital recover within
    the time horizon I care about?

Q2. If I'm wrong about the cycle phase, how much extra do I lose?

Q3. If a tail event hits (exchange insolvency, regulation, hack),
    what happens to this position?
```

Any "I don't know" or "doesn't matter" answer = block the trade.

---

## Section 13 — Capital Allocation Tiers

For overall portfolio:

```
CORE (50-70%)        Long-term BTC + ETH self-custody
                     Don't trade actively; ride cycles

SATELLITE (20-30%)   Active swing trades, alt rotations
                     Tactical exposure

YIELD (5-15%)        Stablecoin yield, low-risk DeFi
                     Income, not speculation

CASH (5-25%)         Cycle-phase-dependent buffer
                     Dry powder + safety
```

Adjustments by cycle phase per Section 9.

---

## Anti-Patterns

- **Position sizing on conviction**: Conviction ≠ correctness. Size on math, not feelings.
- **Ignoring correlation**: "I have 8 positions" but they all correlate to BTC = 1 position.
- **No invalidation level**: "I'll know when it's wrong" = no plan.
- **Moving stops against the trade**: Inviting catastrophic loss.
- **Catching falling knives in markdown phase**: Phase 5 risk posture exists for a reason.
- **Over-leveraging in late-cycle euphoria**: Highest-risk regime, not lowest.
- **Single-exchange concentration**: FTX cured many of this; some forgot.
- **No tail scenario library**: Tail events are recurring features, not one-offs.
- **Personalized advice language**: "You should buy" — never. "Position sizing math suggests X%" — yes.
- **Full Kelly**: Crypto's fat tails make full Kelly often catastrophic.

---

## Reference

- `companies/crypto-consultant/skills/risk/SKILL.md` (parent skill).
- `knowledge/crypto/four-year-cycle.md` (Update 12 — phase-posture table).
- `knowledge/crypto/scenario-modeling.md` (Update 12 — tail / scenario construction).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — for cycle-phase identification).
- This file paraphrases standard risk-management literature (Tharp, Faith, Vince) applied to crypto context; content rephrased for licensing compliance.
