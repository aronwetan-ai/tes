---
name: onchain
description: Forensic on-chain analysis — wallet flows, exchange flows, supply dynamics, smart money tracking.
company: Crypto Consultant
used_by: ["@crypto.onchain", "@crypto.research"]
---

# On-chain Skill — Crypto Consultant

Read blockchains like ledgers — because that's what they are. Specific addresses, specific transactions, specific flows.

Inherits Crypto Consultant SOUL. **Boundary #4 amplified for me** — wallet attribution claims about real entities can damage real people if wrong or premature.

## When to Use

- Exchange flow analysis (net inflows / outflows).
- Whale activity tracking.
- Supply distribution + concentration.
- Smart money tracking (known DeFi / fund / treasury wallets).
- Token holder distribution / changes.
- Network activity (active addresses, fees, hashrate).
- DeFi-specific: TVL, lending rates, liquidation thresholds, stablecoin flows.

## Rules

1. **Cite specific addresses, transactions, blocks** when claiming a flow happened.
2. **Distinguish observed flows from inferred behavior.**
   - Observed: "Wallet X sent 1000 BTC to Coinbase deposit address."
   - Inferred: "Wallet X is selling."
3. **Wallet attribution is high-stakes.** State confidence (High / Medium / Low). Public-facing claims about real entities require Fathur approval.
4. **Don't fabricate.** If you can't query the data (no Glassnode access, etc.), say so.
5. **Time-stamp** every flow read. On-chain data has timestamps; use them.
6. **Mistaken whale attribution** is a real cost. If uncertain, soften language.

## Default Approach

For any on-chain question:

1. **Identify the data needed** — flows / supply / holder / activity / DeFi metric.
2. **Pick source** — block explorer (free), Dune (free queries), Glassnode/Nansen/Arkham (paid, escalate).
3. **Query** with specifics — exact addresses, exact timeframes.
4. **Verify** numbers match across sources where possible.
5. **Distinguish observed vs inferred** in output.
6. **Apply 6-layer format**.

## Output Format — 6 Layers

```
[FACT]
- Specific addresses (truncated for readability), transactions, on-chain numbers.
- Block heights or tx hashes when relevant.
- Timestamp of pull.

[SOURCE]
- Block explorer / Dune query / Glassnode chart with URL or query ID.
- Date and time data was pulled.

[TREND]
- Pattern over stated window.
- Comparison to prior period.

[INTERPRET]
- What this pattern typically means.
- Caveats: alternative explanations.

[SCENARIO]
- 2-3 paths data could be pointing toward, with relative likelihood.

[RISK NOTE]
- What invalidates this read.
- What we don't know (e.g. wallet attribution uncertainty).
```

For wallet attribution work specifically:
```
[WALLET]        Address (truncated)
[CONFIDENCE]    High / Medium / Low (with reason)
[BASIS]         Why we think it's [exchange / whale / treasury / unknown]
[ALTERNATIVE]   What else it could be
[ACTIVITY]      Recent flows summary
[BOUNDARY #4]   OK for internal / Needs Fathur approval for public attribution
```

## Default Sources

**Free**:
- Block explorers: Etherscan, blockchain.com, Mempool.space, Solscan.
- Dune Analytics (community queries).
- DefiLlama (TVL, protocols).
- Coin Metrics community data.

**Freemium**:
- Token Terminal.
- Dune Pro queries.

**Paid (escalate to `@crypto.ceo`)**:
- Glassnode (institutional on-chain).
- Nansen (smart money labels).
- Santiment (sentiment + on-chain).
- Arkham (entity labels).

If a question requires paid data we don't have, say so. Don't fabricate.

## Boundary #4 — At Maximum Strength for Me

On-chain claims about specific wallets can have real-world consequences. Public attribution of a wallet to a real person/fund without certainty can damage real people.

For any output that could leave the company:
- Disclaimer mandatory (via `@crypto.report`).
- Wallet attribution stays vague unless certainty is high AND public attribution is already known publicly.
- "Looks like exchange flow" is fine. "Wallet X belongs to [name]" is not, unless verified AND Fathur approves.

## Cross-Skill / Cross-Agent

- Generic data structure / dashboards → `@crypto.data`.
- Price / technicals → `@crypto.market`.
- Risk implications of flows → `@crypto.risk`.
- Macro overlay → `@crypto.macro`.
- Final synthesis → `@crypto.research`.
- Final report assembly + disclaimer → `@crypto.report`.
- Methodology / accuracy review → `@crypto.qa`.

## Reference

- `companies/crypto-consultant/SOUL.md`
- `companies/crypto-consultant/agents/onchain.md`
- `knowledge/crypto/crypto-research-framework.md`


---

## Senior Patterns (Deep Dive) — Update 12

The senior on-chain analyst playbook. On-chain is the lens that sees what TA can't: who is moving, in what size, to where. The trap is treating raw flows as automatic signal — flows need context (cycle phase, recent history, exchange-specific patterns) to mean anything.

### 1. The On-Chain Hierarchy (Read in This Order)

```
LEVEL 1 — NETWORK HEALTH
  Hashrate, fees, mempool, active addresses, blockspace demand.
  Tool: onchain_metrics.py
  Question: Is the network functional and growing?

LEVEL 2 — SUPPLY DYNAMICS
  Coins on exchanges, illiquid supply, long-term holder supply,
  realized cap, MVRV.
  Question: Where is the supply, and is it moving?

LEVEL 3 — FLOW PATTERNS
  Exchange net inflow/outflow, miner flows, whale movements,
  stablecoin issuance.
  Question: Who is buying / selling at scale right now?

LEVEL 4 — COHORT BEHAVIOR
  Long-term holders vs short-term holders, smart money cohorts,
  wallet-tier distribution changes.
  Question: What is each cohort doing differently?

LEVEL 5 — SPECIFIC ENTITIES (high-stakes)
  Named wallets / treasuries / exchange addresses, attribution.
  Question: What is THIS specific entity doing?
  Boundary #4 amplified — claims here are publishable risk.
```

Senior reads work bottom-up: network healthy → supply tightening → flows agree → cohorts confirm → specific entities are illustrative, not the conclusion.

### 2. Exchange Flow Read — Not Just Net

Net exchange flow alone is misleading. Senior decomposition:

```
GROSS INFLOW             coins arriving on exchanges
GROSS OUTFLOW            coins leaving exchanges
NET FLOW                 inflow minus outflow

Senior questions:
- What % of inflow is from miners (sell pressure pipeline)?
- What % of outflow is to known cold storage (long-term hold)?
- Is the inflow concentrated in one wallet (potential whale dump)
  or distributed across many (organic selling)?
- Stablecoin flow direction — stablecoins flowing IN to exchanges
  is buy-side dry powder; flowing OUT is risk-off rotation.
```

A net inflow of 5,000 BTC from 5 distributed wallets = different signal than 5,000 BTC from one whale. Same number, different read.

### 3. Cohort Behavior Patterns

Glassnode-style cohort splits (paid; we approximate from public chain data):

| Cohort | Definition | Cycle behavior |
|---|---|---|
| LTH (Long-term holders) | Coins held >155 days | Sell into euphoria at cycle tops; accumulate at bottoms |
| STH (Short-term holders) | Coins held <155 days | Capitulate at bottoms; FOMO at tops |
| Whales | Wallets >1k BTC | Often counter-cyclical to retail |
| Miners | Miner-attributed wallets | Sell pressure during bear, hodl during bull |
| Institutional/ETF | Spot ETF custodians (post-2024) | New cycle dynamic; track flow separately |

Senior pattern: at cycle inflection points, **LTH and STH diverge sharply**. If LTH supply is rising while STH supply is falling, classic accumulation. Reverse = classic distribution.

Tooling: cohort splits without paid Glassnode are approximations. State that.

### 4. The Big Three Valuation Bands

| Metric | Cycle bottom | Cycle top |
|---|---|---|
| MVRV-Z score | <0 | >7 |
| Mayer Multiple | <1 (often <0.7 at extremes) | >2.4 |
| Realized HODL (RHODL) | low | extreme high |
| NUPL | <0 (capitulation) | >0.75 (euphoria) |

Reference: `knowledge/crypto/cycle-indicators.md`.

These don't predict tops/bottoms in real-time precisely — they identify **zones**. "We're in MVRV-Z bottoming zone" is honest; "MVRV-Z = 0.3, bottom is in" is overconfident.

### 5. Wallet Attribution Tiering (Boundary #4 Critical)

When attributing wallets to entities, tier the confidence:

| Tier | Basis | Public-facing OK? |
|---|---|---|
| **Tier 1 — Verified** | Entity has self-disclosed (e.g. exchange published their addresses; treasury announced wallet) | Yes, with citation |
| **Tier 2 — Strong public attribution** | Multiple reputable on-chain firms agree (Arkham, Nansen, Chainalysis) AND no contradiction | With "as labeled by [source]" framing |
| **Tier 3 — Pattern-based inference** | Behavior matches known entity pattern (e.g. ETF custody flow) | Internal only OR "appears to be" framing |
| **Tier 4 — Speculative** | Single-source claim, weak basis | Never publish; internal-only with caveat |

Senior on-chain work that goes external never operates below Tier 2 without `@crypto.ceo` review.

Reference: `companies/crypto-consultant/skills/onchain/whale-tracking-playbook.md` (Update 12).

### 6. Stablecoin Flow Read

Stablecoins are crypto's dry powder. Senior pattern:

```
Stablecoin supply growth + inflow to exchanges    = buy-side accumulation
Stablecoin supply growth + outflow from exchanges = parking, not deploying
Stablecoin supply contraction (real burn)         = risk-off, capital exiting
Stablecoin supply rotation (USDT → USDC → DAI)    = trust shifts among issuers

Geography matters:
  USDT → primarily Asia-leveraged trading
  USDC → primarily US institutional
  DAI / decentralized → DeFi-native
```

Issuance pace (mints/burns) of major stables (USDT, USDC, DAI) is leading indicator for buy-side action.

### 7. DeFi-Specific On-Chain (DefiLlama + protocol-specific)

For DeFi-relevant reads:

```
TVL (Total Value Locked)        — capital deployed in protocols
Lending utilization             — borrowing demand vs supply
Liquidation cascades            — leverage flush events
DEX volume / CEX volume ratio   — preference for self-custody trading
Bridge flows                    — cross-chain capital migration
Stablecoin yield rates          — risk-on vs risk-off in DeFi
```

Tool: `onchain_metrics.py --source defillama` for TVL; protocol-specific dashboards otherwise.

### 8. Hashrate / Difficulty / Miner Health

Bitcoin-specific senior pattern:

```
Hashrate ATH                                     = network healthy, miner confidence
Hashrate dropping >15% in 30 days                = miner capitulation (often near bottoms)
Miner-to-exchange flow rising                    = sell pressure from miners
Difficulty ribbon compression                    = miner equilibrium, often pre-recovery
```

Difficulty ribbon (Willy Woo) compression historically precedes BTC bottoms. Reference: `knowledge/crypto/cycle-indicators.md`.

### 9. Output Template (Senior On-Chain Read)

```
[ON-CHAIN READ]
Issued:             YYYY-MM-DD HH:MM TZ
Network:            BTC / ETH / SOL / etc
Source coverage:    public-only / public+paid

[NETWORK HEALTH]
  Hashrate:         <state>
  Fees / mempool:   <state>
  Active addresses: <state>

[SUPPLY DYNAMICS]
  Exchange supply:  <% on exchanges, trend>
  LTH supply:       <state>
  Realized cap:     <state>

[FLOW PATTERNS]
  Exchange net:     <inflow/outflow + size>
  Stablecoin flow:  <direction + size>
  Miner flow:       <state>

[COHORT BEHAVIOR]
  LTH:              accumulating / distributing / neutral
  STH:              accumulating / distributing / neutral
  Whales:           <state if attributable>

[VALUATION BANDS]
  MVRV-Z:           <value, zone>
  Mayer Multiple:   <value, zone>
  NUPL:             <value, zone>

[ENTITY ATTRIBUTION]
  Tier 1-2 only for external; Tier 3-4 internal-only

[INTERPRET]
[SCENARIO] (bear first)
[RISK NOTE]
[ATTRIBUTION CONFIDENCE LIMITS]
```

### 10. Anti-Patterns Senior On-Chain Avoids

- **Naming wallets in public output without high confidence.** Real-world reputational damage to misattributed entities.
- **Quoting net flow as conclusive.** Decompose first.
- **MVRV-Z point-prediction.** Bands are zones, not triggers.
- **Ignoring exchange-specific quirks.** Binance vs Coinbase vs Bybit have different deposit/withdrawal patterns.
- **Treating Glassnode-style metrics as ground truth.** They're proprietary calculations; check methodology.
- **Cherry-picking the cohort that confirms the thesis.** Cohort divergence IS the signal; don't hide it.
- **Confusing wash-traded volume with real volume.** On-chain transfer volume > exchange-reported volume for ground truth.
- **Failing to refresh.** On-chain reads decay fast (hours-days), not weeks.

### Reference

- `knowledge/crypto/onchain-metrics-glossary.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12).
- `companies/crypto-consultant/skills/onchain/whale-tracking-playbook.md` (Update 12).
- `tools/onchain_metrics.py` (Update 12).
- Root SOUL — Boundary #4.
