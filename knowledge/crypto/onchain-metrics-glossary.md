# On-Chain Metrics Glossary — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.onchain`, `@crypto.research`, `@crypto.market`

---

## Why This File

On-chain metrics are crypto's exclusive analytical edge over TradFi. The blockchain is a public ledger; you can read positioning that's invisible in equities markets. This file is the **canonical glossary** for the major on-chain metrics — definitions, mechanisms, interpretations, and limitations.

---

## Section 1 — Network Health Metrics

### Hashrate
**Definition**: Total computational power securing the network (BTC: TH/s, EH/s).

**Read**:
- Rising = miner confidence; network growing
- Sustained ATH = healthy bull regime
- 15%+ drop in 30 days = miner capitulation (often near cycle bottoms)

**Tool**: `onchain_metrics.py --metric hashrate`.

### Difficulty
**Definition**: Network adjustment that targets ~10-min block time (BTC); adjusts every 2,016 blocks.

**Read**: difficulty rising = hashrate rising = miners committing capital.

### Active Addresses
**Definition**: Unique addresses that participated in at least one transaction within a window.

**Read**:
- Rising = network usage growing
- Falling = waning interest
- Caveat: privacy-conscious users use new addresses per tx; metric noisy

### Transaction Count
**Definition**: Number of on-chain transactions per period.

**Read**: persistent high tx volume = strong demand for blockspace.

### Mempool Size
**Definition**: Pending tx queue waiting for confirmation.

**Read**:
- Rising = demand exceeding throughput; fee market active
- Persistent high = network congestion (bullish for fee revenue)

**Tool**: `onchain_metrics.py --metric mempool` (BTC).

### Fees
**Definition**: Total fees paid in a window; or median fee per tx.

**Read**: high fees = network in demand; sustainable security budget post-halving.

---

## Section 2 — Supply Dynamics

### Realized Cap
**Definition**: Sum of value of each UTXO at the price when it last moved.

**Read**: aggregate cost basis of network. Useful in MVRV calculation.

### Realized Price
**Definition**: Realized Cap ÷ supply.

**Read**: average cost basis. Price below realized = aggregate holders underwater (capitulation zone).

### Liquid Supply
**Definition**: Coins held in wallets that have moved recently (high spendability).

**Read**: high liquid supply = potential sell pressure.

### Illiquid Supply
**Definition**: Coins held in wallets with no spending history (long-term hold).

**Read**: rising illiquid supply = strong holding behavior; bullish.

### LTH Supply (Long-Term Holders)
**Definition**: Coins held >155 days (Glassnode threshold).

**Read**:
- Rising in Phase 1-2 = accumulation, bullish
- Falling in Phase 3-4 = distribution, late-cycle warning
- Rising again in Phase 5 = re-accumulation, bottom signal

**Tool**: paid Glassnode for precise LTH; our `onchain_metrics.py` uses approximation.

### STH Supply (Short-Term Holders)
**Definition**: Coins held <155 days.

**Read**: STH supply rising rapidly = retail FOMO inflow.

### Exchange Supply
**Definition**: BTC/ETH/etc held in exchange wallet addresses.

**Read**:
- Falling = coins moving to self-custody = bullish (less sell pressure)
- Rising = coins moving to exchanges = potential sell pressure

**Tool**: `onchain_metrics.py --metric exchange-balance`.

---

## Section 3 — Cohort / Holder Distribution

### Whale Distribution
**Definition**: Distribution of supply by wallet size cohort.

| Cohort | Wallet size (BTC) |
|---|---|
| Mega-whales | >10,000 |
| Whales | 1,000-10,000 |
| Sharks | 100-1,000 |
| Fish | 10-100 |
| Shrimp | <10 (retail) |

**Read**: cohort divergence at cycle inflections (mega-whales accumulate, shrimp capitulate at bottoms; reverse at tops).

### HODL Waves
**Definition**: Visualization of supply by age (1d, 1w, 1m, 6m, 1y, 2y+).

**Read**:
- Old supply waking up (>1y bands shrinking) = distribution
- Old supply growing (>1y bands expanding) = accumulation

### Dormancy
**Definition**: Average age of coins that moved.

**Read**:
- Rising dormancy = older coins moving = LTH distribution risk
- Low dormancy = recent coins moving = STH dominated activity

---

## Section 4 — Valuation Metrics

### MVRV (Market Value to Realized Value)
**Definition**: Market Cap ÷ Realized Cap.

**Read**:
- <1 = aggregate underwater (capitulation)
- 1-3 = recovery / fair value
- 3-5 = overvalued (warning)
- >5 = euphoria (cycle top zone)

### MVRV-Z Score
**Definition**: (Market Cap - Realized Cap) ÷ stdev(Market Cap).

**Read** (BTC reference):
- <0 = capitulation (cycle bottoms)
- >7 = euphoria (cycle tops)

See `cycle-indicators.md` for full reference.

### NUPL (Net Unrealized Profit/Loss)
**Definition**: (Market Cap - Realized Cap) ÷ Market Cap.

**Read** (color zones):
- <0 capitulation (red)
- 0-0.25 hope/fear (orange)
- 0.25-0.5 optimism (yellow)
- 0.5-0.75 belief (green)
- >0.75 euphoria (blue)

### Realized Profit / Loss
**Definition**: Profit (or loss) realized when coins move (priced at realized vs current).

**Read**:
- Realized profit spike = active distribution (selling)
- Realized loss spike = capitulation event

### SOPR (Spent Output Profit Ratio)
**Definition**: Average of (price sold) ÷ (price acquired) for spent UTXOs.

**Read**:
- >1 = market in profit (selling at gain on average)
- <1 = market in loss (capitulation territory)
- 1.0 in bull = important support test (resets)

---

## Section 5 — Flow Metrics

### Exchange Net Flow
**Definition**: Inflow - outflow on exchange wallets.

**Read**:
- Negative (net outflow) = coins leaving exchanges (bullish, less sell pressure)
- Positive (net inflow) = coins arriving at exchanges (potential sell)

**Caveat**: must decompose by source (miner / whale / retail / internal exchange moves) for senior read. See `whale-tracking-playbook.md`.

### Stablecoin Issuance / Burn
**Definition**: New mints (or burns) of USDT, USDC, DAI, etc.

**Read**:
- Net mint = new dry powder entering system (bullish)
- Net burn = capital leaving stablecoins back to fiat (bearish)
- Pace matters: $500M+ in a day is significant

**Tool**: `onchain_metrics.py --metric stablecoin-mint`.

### Stablecoin Supply Ratio (SSR)
**Definition**: BTC market cap ÷ stablecoin supply.

**Read**: lower SSR = more dry powder relative to BTC value (bullish potential).

### Miner Outflow
**Definition**: Coins moving from miner-attributed wallets to exchanges or other addresses.

**Read**: large miner sell flow = sell pressure pipeline; especially relevant post-halving when revenue drops.

---

## Section 6 — DeFi-Specific

### TVL (Total Value Locked)
**Definition**: Aggregate USD value of assets deposited in DeFi protocols.

**Read**:
- Rising TVL = capital deployment, risk-on within crypto
- Falling TVL = capital exiting DeFi (often risk-off)

**Source**: DefiLlama (free, comprehensive).

**Tool**: `onchain_metrics.py --metric tvl --protocol <name>`.

### Lending Utilization
**Definition**: Borrowed / supplied ratio in lending protocols.

**Read**: high utilization = strong borrow demand; can signal leverage build-up.

### Liquidation Volume
**Definition**: Total value liquidated in DeFi or perp markets.

**Read**: liquidation cascades = leverage flush events; often near short-term reversals.

### DEX Volume / CEX Volume Ratio
**Definition**: DEX trading volume relative to CEX.

**Read**: rising ratio = preference shift toward self-custody trading (post-FTX trend).

### Bridge Flows
**Definition**: Capital moving between L1/L2 chains via bridges.

**Read**: flow direction shows which chain is gaining/losing capital share.

---

## Section 7 — Tool Sources

| Tool | Free? | Coverage |
|---|---|---|
| Etherscan / Blockchain.com | Free | Block explorer, basic metrics |
| Mempool.space | Free | BTC mempool + fee data |
| DefiLlama | Free | TVL, protocol-level data |
| Dune Analytics | Free + paid | Custom queries on Ethereum |
| Coin Metrics | Free + paid | Network data, valuation metrics |
| Glassnode | Paid | Most comprehensive on-chain (LTH, MVRV-Z full, RHODL, etc.) |
| Nansen | Paid | Smart money labels, wallet attribution |
| Arkham | Paid | Entity labels, attribution |
| Santiment | Paid | Sentiment + on-chain |
| `onchain_metrics.py` | Local | Aggregates free APIs (mempool.space, DefiLlama, blockchain.info) |

For paid data not available: state the limitation; do not fabricate.

---

## Anti-Patterns

- **Quoting net exchange flow without decomposition**: Decompose into miner / whale / retail / internal.
- **Treating MVRV / Mayer / NUPL as triggers**: They're zones.
- **Ignoring approximation caveats**: Our tools use proxies for paid metrics; state this.
- **Citing Whale Alert as primary source**: Verify on-chain independently.
- **Conflating liquid supply with sell pressure**: Liquid supply is potential, not actual.
- **Confusing realized cap with market cap**: They're fundamentally different — one is cost basis aggregate, one is current value.
- **Single-metric reads**: Convergence required.

---

## Reference

- `companies/crypto-consultant/skills/onchain/SKILL.md` (parent skill).
- `companies/crypto-consultant/skills/onchain/whale-tracking-playbook.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — valuation metrics in cycle context).
- `tools/onchain_metrics.py` (Update 12).
- This file paraphrases standard on-chain metric definitions (Glassnode, Coin Metrics, DefiLlama documentation tradition); content rephrased for licensing compliance.
