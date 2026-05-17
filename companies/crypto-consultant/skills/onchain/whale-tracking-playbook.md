---
name: whale-tracking-playbook
description: Forensic whale tracking — exchange flow forensics, cohort analysis, smart money attribution, Boundary #4 enforcement.
company: Crypto Consultant
agent_specific: "@crypto.onchain"
parent_skill: onchain
used_by: ["@crypto.onchain", "@crypto.research", "@crypto.qa"]
---

# Whale Tracking Playbook — Crypto Consultant Deep Skill

Agent-specific extension of `skills/onchain/SKILL.md`. Used by `@crypto.onchain` for any work involving large-wallet flows, smart-money cohorts, or entity attribution.

Inherits Crypto Consultant SOUL. **Boundary #4 is at MAXIMUM intensity here** — public attribution of wallets to real entities can damage real people if wrong. Tier discipline is non-negotiable.

Core principle: **flows are observable; intent is inferred; identity is high-stakes.** Senior whale tracking distinguishes all three layers.

---

## When to Use

- "Are whales accumulating / distributing?"
- "What is wallet X doing?"
- Exchange flow forensics (large deposits / withdrawals).
- Smart money cohort tracking (top-tier holders, named treasuries, fund wallets).
- ETF custody flow analysis (post-2024 BTC/ETH spot ETFs).
- Stablecoin issuer flow tracking (Tether, Circle large transfers).
- Pre-event positioning (whale moves before known catalysts).

---

## The Three Layers of Whale Reading

```
LAYER 1 — OBSERVED FLOW
  Specific transaction(s) with hash, block, timestamp, size.
  This is FACT. Verifiable on-chain.

LAYER 2 — INFERRED BEHAVIOR
  What the flow likely means in context.
  "Wallet X moved 1000 BTC to Coinbase deposit."
  Inference: "likely preparing to sell" — but could be:
    - Internal exchange wallet move
    - OTC desk routing
    - Custody change
    - Loan collateral repositioning
  State all alternatives.

LAYER 3 — ATTRIBUTED IDENTITY
  Who is the wallet?
  Highest stakes. Tier discipline (below) applies.
```

Senior whale tracking work outputs all three layers explicitly. Junior work conflates them.

---

## Wallet Tier Framework (Boundary #4 Critical)

For any attribution claim, state the tier:

| Tier | Basis | Public-facing OK? | Internal note |
|---|---|---|---|
| **T1 — Verified** | Self-disclosed by entity (e.g. exchange published address; treasury announced wallet) | Yes, with citation | Examples: Binance hot wallets per Binance disclosure; MicroStrategy treasury per their press release |
| **T2 — Strong public attribution** | Multiple reputable on-chain firms agree (Arkham, Nansen, Chainalysis, Glassnode); no contradiction | "as labeled by [source]" framing | Use cited attribution; don't claim independently verified |
| **T3 — Pattern-based inference** | Behavior matches known entity pattern (e.g. ETF custody flow timing matches Coinbase Custody handling iShares IBIT) | Internal only; OR "appears to be" framing for external (with `@crypto.ceo` review) | Pattern is suggestive but not proven |
| **T4 — Speculative** | Single-source claim, anonymous Twitter, "I think this is..." | **Never publish externally.** Internal-only with caveat | Treat as flag for further investigation, not as fact |

**Senior on-chain work that goes external never operates below Tier 2.** Tier 3 can go external only with explicit "appears to be" framing AND `@crypto.ceo` review.

---

## The Whale Cohort Framework

| Cohort | Wallet size | Cycle pattern |
|---|---|---|
| **Mega-whales** | >10,000 BTC | Often early to accumulate, late to distribute; counter-cyclical to retail |
| **Whales** | 1,000-10,000 BTC | Mixed — split between OG holders + institutions |
| **Sharks** | 100-1,000 BTC | Mid-tier — often follows whale lead |
| **Fish** | 10-100 BTC | Active mid-cycle; mixed sophistication |
| **Shrimp** | <10 BTC | Retail-dominated; FOMO at tops, capitulate at bottoms |

Senior pattern: at cycle inflection points, **mega-whale supply diverges from shrimp supply**. Mega-whales accumulating + shrimp capitulating = classic bottom signal. Reverse = classic top signal.

Tooling: cohort splits without paid Glassnode are approximations — derive from chain data with caveats. State this in output.

---

## Exchange Flow Forensics — Senior Decomposition

Net exchange flow alone is misleading. Senior decomposition:

```
GROSS INFLOW           total coins arriving on exchanges
  Decompose:
    - Miner inflow      sell pressure pipeline
    - Whale inflow      potential distribution
    - Retail inflow     panic selling or routine
    - Internal moves    exchange wallet rebalancing (NOT economic)

GROSS OUTFLOW          total coins leaving exchanges
  Decompose:
    - To cold storage   long-term hold accumulation
    - To self-custody   shift to hodl mode
    - To DeFi           collateral / yield
    - To OTC            large block sale (still economic exit)
    - Internal moves    NOT economic

NET FLOW              inflow - outflow (least informative alone)
```

Real read = decomposed flow + cohort identification + size context.

Example (senior):
> "Net inflow: +5,200 BTC over 24h. Decomposed: ~3,800 BTC from 5 distinct large wallets (likely OTC routing per pattern); ~1,100 BTC from miner-attributed addresses (per Glassnode community labels); ~300 BTC from distributed retail. Internal exchange moves excluded. Net read: distribution pipeline activity moderate, not retail capitulation."

vs junior:
> "Net inflow 5,200 BTC = bearish."

---

## Specific Wallet Patterns to Watch

### ETF Custody Flow (post-2024)
- iShares IBIT custodian: Coinbase Custody
- Fidelity FBTC custodian: Fidelity Digital Assets
- ARK ARKB custodian: Coinbase Custody
- Bitwise BITB: Coinbase Custody
- Etc.

ETF custody addresses have public attribution via SEC filings + custodian disclosure. T1-T2 tier.

ETF flow patterns:
- Net positive inflow days = institutional buying
- Net outflow days = institutional selling or rebalancing
- Volume spike + custody flow spike = ETF-driven move

Tool: `onchain_metrics.py --metric etf-flow` (approximation).

### MicroStrategy / Saylor Treasury
- Public treasury per company filings.
- Pattern: large purchases announced; verified on-chain.
- T1 tier.

### Binance Hot/Cold
- Binance has published hot wallet addresses per their proof-of-reserves.
- T1-T2 tier.

### Tether/Circle Issuance Wallets
- Mint/burn wallet addresses are well-known.
- T1 tier.

### "Satoshi" Wallets
- Genesis-era wallets; no movement since 2009-2010.
- Any movement = significant signal.
- T1 attribution to "early miner" cohort; **never** attribute to specific person.

### Mt. Gox Trustee Distribution
- Trustee wallet addresses public.
- Distribution events known catalyst.
- T1 tier.

---

## The "Whale Alert" Trap

Twitter accounts like Whale Alert, Lookonchain, etc. publish large transfers. Senior pattern:

```
[ ] Verify the transaction independently (block explorer link)
[ ] Check if wallet is exchange-internal (often is — false signal)
[ ] Check cohort context (is this routine or anomalous for this wallet?)
[ ] Don't quote whale alert as primary source — quote the on-chain data
```

Whale Alert is a flag, not a source. Misuse: agent posts "Whale moved 5000 BTC to Binance!" without checking it's an internal Binance hot wallet rebalance. Common failure.

---

## Stablecoin Whale Patterns

Tether/USDC mint and burn patterns are leading indicator:

```
LARGE MINT (>$100M USDT/USDC)        = buy-side dry powder created
  Watch: where does it flow next? CEX inflow = imminent buy.

LARGE BURN (>$100M)                   = capital exiting stablecoins
  Watch: redemption to fiat = risk-off.

ROUTINE (<$50M)                       = noise; ignore.

PATTERN (sustained mints over 7 days) = trend; watch for cumulative.
```

Tool: `onchain_metrics.py --metric stablecoin-mint`.

---

## Pre-Event Positioning Read

Before known catalysts (FOMC, CPI, ETF approval decisions, halving), watch whale cohort behavior:

```
Pre-event whale flow patterns:
  Inflow rising into event       = de-risking, expecting downside
  Outflow rising into event      = accumulating, expecting upside
  Stable                         = neutral or hedged

Caveat: pre-event flows may be hedging, not directional bets.
        Combine with funding rate read for confirmation.
```

---

## Output Format — Senior Whale Tracking Read

```
[WHALE TRACKING READ]
Issued:                  YYYY-MM-DD HH:MM TZ
Network:                 BTC / ETH / SOL / etc
Source coverage:         public-only / public+paid

[OBSERVED FLOW (LAYER 1 — FACT)]
  Time window:           <range>
  Notable transactions:  
    - Hash: <truncated>, Block: <N>, Size: <X>, From: <wallet truncated>, To: <wallet truncated>
    - ...
  Aggregate metrics:
    Net exchange flow:   <signed amount>
    Decomposed:          <breakdown if available>

[INFERRED BEHAVIOR (LAYER 2)]
  Most likely interpretation:
    <interpretation>
  Alternative explanations:
    - <alt 1>
    - <alt 2>
  Confidence:            High / Medium / Low

[ATTRIBUTED IDENTITY (LAYER 3)]
  Wallets identified:
    - Wallet <truncated>: tier <T1-T4>, attribution: <entity or "unknown">, basis: <source>
    - ...
  Tier breakdown:
    T1: <count>, T2: <count>, T3: <count>, T4: <count>

[COHORT CONTEXT]
  Mega-whales:           <accumulating / distributing / neutral>
  Whales:                <state>
  Sharks:                <state>
  Retail (shrimp):       <state>
  Divergence note:       <if cohorts diverge, that IS the signal>

[INTERPRET]
  What the flows + attribution + cohort behavior suggest.
  Cycle context.

[SCENARIO]
  Bear: <if flows are warning signal>
  Sideways: <if flows are routine>
  Bull: <if flows confirm accumulation>

[RISK NOTE]
  What invalidates this read.
  What we don't know (attribution gaps, paid-data gaps).

[BOUNDARY #4 STATUS]
  Internal-only / Tier 2+ external OK / Tier 3+ requires Fathur approval
```

---

## Anti-Patterns Senior Whale Trackers Avoid

- **Naming wallets in public output without Tier 1-2 confidence.** Real-world reputational damage to misattributed entities. Lawsuit risk.
- **Quoting Whale Alert as primary source.** Verify independently or don't quote.
- **Treating internal exchange moves as economic flow.** False signal.
- **Confusing OTC routing with retail selling.** Different cohort, different signal.
- **Ignoring cohort divergence.** When mega-whales go one way and shrimp go the other, the divergence is the entire signal.
- **Headline whale tracking ("biggest single move ever").** Drama for clicks; not analysis.
- **Skipping the three-layer separation.** Conflating observed flow with inferred behavior with attributed identity is the most common subtle failure.
- **Promoting "Satoshi moved!" without verification.** Genesis-era wallet moves are dramatic but rarely Satoshi.
- **Asserting whale intent from a single transaction.** Need pattern, not point.

---

## Cross-Skill / Cross-Agent

- Generic on-chain reads → `skills/onchain` (parent skill).
- Pattern recognition (Pi top, MVRV bands) → `skills/pattern-recognition`.
- Macro overlay on whale activity → `@crypto.macro`.
- Risk implications of distribution → `@crypto.risk`.
- Final synthesis → `@crypto.research`.
- Wallet attribution audit (force-fit detection) → `@crypto.qa`.
- Tool execution → `onchain_metrics.py`, public block explorers.

---

## Reference

- `companies/crypto-consultant/skills/onchain/SKILL.md` (parent skill).
- `knowledge/crypto/onchain-metrics-glossary.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — cohort dynamics at cycle inflections).
- `knowledge/scope/declined-tools.md` (Update 12 — Item 5 forbids guaranteed-signal automation).
- `tools/onchain_metrics.py` (Update 12).
- Root SOUL — Boundary #4.
