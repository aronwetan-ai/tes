# News Source Rubric — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.research`, `@crypto.qa`, `@crypto.macro`, `@crypto.report`

---

## Why This File

Not all crypto "news" is equal. Some sources are reputable journalists; some are paid shills; some are anonymous Twitter accounts. This rubric tiers crypto news/info sources for **citation discipline** — what's quotable, what's a flag, what's noise.

---

## The 5-Tier Rubric

| Tier | Description | Citation status |
|---|---|---|
| **T1 — Primary** | Direct authoritative source (the entity itself) | Citable as fact |
| **T2 — Authoritative secondary** | Major news / data firm with editorial standards | Citable with attribution |
| **T3 — Reputable analyst** | Named individual with track record + primary research | Citable with attribution to person |
| **T4 — Crypto media** | Industry-specific publications | Citable for news, **not** for analysis |
| **T5 — Anonymous / social** | Twitter, Telegram, anon accounts | **NOT** citable as source; can be flag |

---

## Tier 1 — Primary Sources

Direct, authoritative, the entity itself.

### Macro / TradFi
- **Fed.gov** — FOMC statements, dot plot, SEP, Powell speeches
- **Treasury.gov** — Refunding announcements, TGA balance, debt ceiling decisions
- **BLS** — CPI, PPI, NFP releases
- **BEA** — GDP releases
- **FRED** (St. Louis Fed) — economic time series
- **ECB** — eurozone monetary policy
- **BoJ** — Japan policy
- **PBoC** — China policy
- **SEC.gov** — filings, enforcement actions, ETF flow disclosures

### Crypto-Specific
- **Exchange official statements** — Binance, Coinbase, Bybit (own announcements)
- **Protocol governance forums** — Aave, Compound, Uniswap, Maker
- **GitHub repos** — protocol code, BIPs, EIPs
- **On-chain data** (block explorers) — transactions, wallet activity
- **Custodian disclosures** — ETF custody, proof-of-reserves

### Regulatory
- **CFTC, SEC, FinCEN** — US enforcement, rule announcements
- **ESMA, BaFin, FCA** — EU/UK regulators
- **Local equivalents** — for jurisdiction-specific news

**Senior citation**: quote verbatim with date + source URL where possible.

---

## Tier 2 — Authoritative Secondary

Major news organizations and data firms with editorial standards.

### News
- **Bloomberg** — financial wire (paid; high reliability)
- **Reuters** — wire service
- **WSJ** — Wall Street Journal
- **FT** — Financial Times
- **The Economist** — analysis-leaning
- **NYT / WaPo** — general but financially reliable

### Data Firms
- **Glassnode** — on-chain analytics (paid; methodology transparent)
- **Coin Metrics** — on-chain analytics (free + paid)
- **Chainalysis** — compliance-grade attribution (paid)
- **Nansen** — wallet labeling (paid)
- **Arkham** — entity attribution
- **DefiLlama** — DeFi data aggregation (free, comprehensive)
- **Coinglass** — derivatives data (free + paid)
- **Dune Analytics** — community queries (free + paid)

**Senior citation**: cite with attribution: "Per Bloomberg [date]" or "Glassnode notes [metric] at [value], date".

---

## Tier 3 — Reputable Analyst (Individual)

Named individuals with track record. Citable with **personal attribution** ("Per [name]'s analysis...").

### Examples (illustrative; not endorsement)
- Macroeconomic: Lyn Alden, Alex Krüger, Joe Wiesenthal, Russell Napier
- On-chain: Willy Woo, Philip Swift, Glassnode researchers
- Crypto markets: Arthur Hayes, Su Zhu (pre-3AC; cite cautiously now), Hasu, Vitalik Buterin (ETH-specific)
- Regulatory: Hester Peirce, Jake Chervinsky

### Criteria for T3
- Named individual (not anonymous handle)
- Multi-year track record
- Primary research published (not just commentary)
- Methodology transparent
- Public corrections record

**Senior usage**: "Per [analyst]'s analysis [date], [claim]. We note their basis as [methodology]."

**Caveat**: T3 sources can be wrong; cite their analysis but maintain independent verification of facts.

---

## Tier 4 — Crypto Media

Industry-specific publications with editorial standards but variable analytical quality.

### Examples
- **CoinDesk** — established crypto news; has had ethical issues historically; varies by author
- **CoinTelegraph** — high volume; quality varies
- **TheBlock** — research-focused; relatively reputable
- **Decrypt** — newsy
- **Bitcoin Magazine** — Bitcoin-focused
- **Blockworks** — newer; institutional-leaning
- **The Defiant** — DeFi-focused

### Citation Status
- **Citable for news** (event reporting, factual claims)
- **NOT citable for analysis** as primary basis (analysis quality variable)
- Always cross-check with T1-T2 if claim is significant

**Senior usage**: "[CoinDesk reported on date that...]" — flag the source explicitly.

---

## Tier 5 — Anonymous / Social

Twitter, Telegram, Discord, anonymous accounts — even with high follower counts.

### Examples
- Anonymous trader Twitter (@PlanB, @Murad_Capital, anonymous "alpha" accounts)
- Whale Alert (Twitter) — flag, not source; verify on-chain
- Lookonchain — flag, not source; verify on-chain
- "Crypto Twitter" consensus
- Telegram alpha groups

### Citation Status
- **NOT citable as source for facts**
- **Can be cited as flag for further investigation**: "@PlanB tweeted X — we verified by [primary source]"
- Anonymous accounts have no accountability for accuracy

**Senior usage**: "Twitter signal flagged X; we independently verified via [T1/T2 source]."

**Failure mode**: junior research cites Twitter consensus as if it's evidence. Block.

---

## Special Cases

### "Nick Timiraos" Trial Balloons (WSJ)
WSJ Fed reporter sometimes publishes pieces that move markets pre-FOMC. Treated as semi-official Fed signaling by some. Senior pattern:
- Citable as T2 (WSJ)
- But signal value is sometimes T3-grade (analyst-style read)
- Don't treat as if it's Fed.gov primary

### Whale Alert / Lookonchain Twitter
On-chain alert accounts. Senior pattern:
- Treat as **flag**, not source
- Verify the transaction independently (block explorer link)
- Check if wallet is exchange-internal (often is — false signal)

### Vitalik Buterin Tweets
ETH founder tweets. Senior pattern:
- Citable as T1 for ETH protocol direction (he speaks officially for ETH)
- T3 for general crypto opinion (named individual, track record)

### CZ / Brian Armstrong Statements
Exchange founder statements. Senior pattern:
- Citable for exchange-specific announcements (T1)
- T3 for industry opinion
- Self-interest filter applies

### Pseudonymous "Track Record" Accounts
Accounts like @ZeroHedge, @Naval (Naval Ravikant), @balajis. Senior pattern:
- T3 if real-name and track record
- T5 if pseudonymous regardless of follower count
- Cite analysis with attribution; don't conflate with primary source

---

## The Source Tiering Audit (QA Layer)

For any report citing sources, `@crypto.qa` runs:

```
[ ] Every fact tagged to source?
[ ] Source tier identified (T1-T5)?
[ ] T1-T2 used for core facts?
[ ] T5 (Twitter / anon) used as flag, not source?
[ ] Cross-check between sources for significant claims?
[ ] Inflammatory claims (regulatory, criminal, fraud) tier T1-T2 only?
[ ] Reports citing T5 as primary fact source = block
```

---

## Citation Format Standard

```
SOURCE FORMAT (preferred):
[Source Name, Tier, Date, URL/identifier]

Examples:
- "Fed funds at 5.25-5.50% [FOMC Statement, T1, 2026-05-01, fed.gov/...]"
- "BTC LTH supply rising 3.2% over 30d [Glassnode, T2, accessed 2026-05-17, glassnode.com/...]"
- "Per Lyn Alden's piece on global liquidity [T3, 2026-04, lynalden.com/...]"
- "CoinDesk reports SEC pause on enforcement [T4, 2026-05-15, coindesk.com/...]"
- "Twitter flag: @WhaleAlert noted 10k BTC to Binance — verified via Etherscan tx 0xabc... [T5 flag, T1 verification]"
```

---

## Anti-Patterns

- **"Sources say"** — generic; not citable
- **"Industry consensus"** — no source; force-fit
- **"On-chain analysts" plural without naming** — can't verify
- **"Crypto Twitter is bullish"** — vibes, not data
- **WhaleAlert as primary** — verify independently or don't quote
- **Anon Twitter as evidence for major claim** — block
- **Bloomberg headline without article body verification** — citation requires article-level check
- **Cherry-picking the analyst that agrees** — pattern of confirmation bias
- **Omitting source tier when citing** — QA cannot audit otherwise

---

## Reference

- `companies/crypto-consultant/skills/qa/SKILL.md` (Update 12 — source tiering check).
- `companies/crypto-consultant/skills/research/SKILL.md` (Update 12).
- `companies/crypto-consultant/skills/macro/SKILL.md` (Update 12 — Fed Watch tier discipline).
- `tools/news_scraper.py` (Update 12 — surfaces T4 sources; does not citation-rate them).
- This file establishes citation tiering for the company; not based on external standard but adapted from journalistic source tiering practice.
