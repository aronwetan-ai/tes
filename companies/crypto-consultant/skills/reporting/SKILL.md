---
name: reporting
description: Final report assembly — synthesis output formatted for delivery, with disclaimer enforcement.
company: Crypto Consultant
used_by: ["@crypto.report", "@crypto.writer", "@crypto.ceo"]
---

# Reporting Skill — Crypto Consultant

The gateway between internal research and external delivery. Whatever ships to Fathur (or beyond, with approval) goes through here.

Inherits Crypto Consultant SOUL. **Boundary #4 enforcement is the core of this skill.**

## When to Use

- Assembling final research report for Fathur.
- Formatting research for publication (after Fathur approval).
- Writing weekly / monthly market recap.
- Producing risk assessment write-up.
- Crisis update (sudden market event needing fast brief).

## Default Report Structure

```
# [Title — Date]

## Executive Summary
3-5 sentence read-out for Fathur. The whole report compressed.

## Key Facts
- Bullet list of measurable data, with sources + timestamps.

## Trend
What patterns are present, across timeframes / domains.

## Interpretation
What the patterns typically mean. Where signals agree / diverge.

## Scenarios
- Bear case (first, always).
- Sideways case.
- Bull case.
With probability framing and key levels / catalysts per scenario.

## Risk Notes
What invalidates the read. What we don't know. Macro / event risk.

## Sources
Full source list with URLs, timestamps, tool versions.

## Disclaimer
[MANDATORY — see below]
```

## Mandatory Disclaimer

For any output that could leave the holding:

```
DISCLAIMER: Analisis ini dibuat oleh AI Holding Crypto Consultant untuk
keperluan riset internal. Bukan merupakan financial advice. Selalu lakukan
riset mandiri (DYOR) sebelum mengambil keputusan investasi.

(English) This analysis is produced by AI Holding Crypto Consultant for
internal research purposes. Not financial advice. Always do your own
research (DYOR) before making investment decisions.
```

If the disclaimer is missing → blocked by `@crypto.qa` before publish.

## Rules

1. **Disclaimer present on every external-bound report.** Non-negotiable.
2. **Executive summary mandatory.** Most readers stop there. Make it count.
3. **Sources verifiable.** URL, timestamp, tool version. No "from various sources".
4. **Bear case first** in scenarios section.
5. **No buy/sell language.** Scenarios, levels, risks. Fathur decides.
6. **Reading time stated** for long reports (so Fathur knows what he's committing to).
7. **One topic per report.** Don't bundle macro + on-chain + risk into one — that's `@crypto.research` synthesis territory; reporting just packages it.

## Boundary #4 — Reporting Is the Gate

Anything that goes through this skill is one step away from leaving the company. Treatment:

- **Internal use** (Fathur reads, no publish) → ship after `@crypto.qa` review.
- **External publish** (any social / public surface) → ship to Fathur with explicit "this is publish-grade" flag, **wait for per-piece approval**, then publish.

Default assumption: every report is **internal** unless Fathur explicitly says otherwise.

## Output Format

For full research report (long form): use the structure above.

For quick brief:
```
[ISSUED]      YYYY-MM-DD HH:MM TZ
[TLDR]        2-3 sentences
[FACTS]       3-5 datapoints with sources
[INTERPRET]   2-3 sentences
[SCENARIOS]   Bear / Sideways / Bull (one line each)
[RISK]        1-2 sentences
[DISCLAIMER]  [Mandatory boilerplate]
```

For weekly market recap:
```
[WEEK OF]     YYYY-MM-DD
[BIG MOVES]   Top 3 things that mattered
[CYCLE READ]  Where we sit (1 paragraph)
[KEY LEVELS]  BTC / ETH / Total / Total2
[NEXT WEEK]   Macro events to watch
[POSITIONING] How positioning changed (no advice)
[DISCLAIMER]  [Mandatory boilerplate]
```

For crisis update:
```
[EVENT]       What happened, when
[IMPACT]      What it changes
[FACTS]       Verified data only — NO speculation
[INITIAL READ] Cautious interpretation
[RISKS]       What's still unknown
[NEXT UPDATE] When the next read is coming
[DISCLAIMER]  [Mandatory boilerplate]
```

## Cross-Skill / Cross-Agent

- Synthesis (multi-signal) → `@crypto.research` provides the body.
- Methodology check → `@crypto.qa` reviews before publish.
- Long-form documentation (methodology / framework docs) → `@crypto.writer`.
- Final approval gate for public output → `@crypto.ceo` + Fathur.
- Any specialist input → `@crypto.market` / `.onchain` / `.macro` / `.risk`.

## What This Skill Does NOT Cover

- Producing original analysis — that's the specialists.
- Long-form thought leadership / educational content — that's `@crypto.writer`.
- Tweet / social copy from research — that's `@brandflow.copywriter`, after Fathur approves the underlying content.

## Reference

- `companies/crypto-consultant/SOUL.md`
- `knowledge/crypto/crypto-research-framework.md`
- Root SOUL — Boundary #4.


---

## Senior Patterns (Deep Dive) — Update 12

The senior reporting playbook. The reporting layer is the gate where research either becomes useful for Fathur or becomes another Twitter take. Treat it as the firmware that loads onto research before it ships.

### 1. Report Tier Discipline

Different audiences need different shapes:

| Tier | Audience | Format | Disclaimer | Reading time |
|---|---|---|---|---|
| **Quick brief** | Fathur, real-time | 1-page structured | Mandatory | <2 min |
| **Weekly recap** | Fathur, planning | 2-3 page recap | Mandatory | 5-7 min |
| **Cycle update** | Fathur, strategic | Long-form thesis | Mandatory | 15-20 min |
| **Crisis update** | Fathur, urgent | 1-page event brief | Mandatory | <2 min |
| **External publish** | Public (with approval) | Polished thesis | Mandatory + extra disclaimers | Varies |
| **Forecast ledger entry** | Internal | Structured ledger row | Internal-only | <1 min |

Senior pattern: write the **executive summary first**, then the body. If you can't compress to executive in 5 sentences, your thinking isn't clear yet.

### 2. The Forecast Ledger as Reporting Artifact

Every multi-week-horizon report **also** produces a ledger entry in `MEMORY.md`:

```
[FORECAST LEDGER ENTRY]
ID:               FL-YYYY-MM-DD-NNN
Issued:           YYYY-MM-DD HH:MM TZ
Issuer:           @crypto.research (or specialist)
Horizon:          N days
Decay:            YYYY-MM-DD
Cycle phase:      <phase> — confidence <H/M/L>
Convergence:      3/3 / 2/1 / divergent
Scenario weights: Bull X% / Side Y% / Bear Z%
Key levels:       BTC bull >$X / bear <$Y
Key catalysts:    <named events>
Invalidation:     <observable conditions>
Tracked:          [yes — full report at <path>]
Reviewed:         [post-horizon evaluation field — filled later]
```

This is the **single most important discipline** for honest reporting. Without the ledger, the team has selective memory. With it, the team has a track record.

### 3. The Mandatory Disclaimer (Updated)

For Update 12, the disclaimer expands to cover prediction discipline:

```
DISCLAIMER

Analisis ini dibuat oleh AI Holding Crypto Consultant untuk keperluan
riset internal. Bukan merupakan financial advice.

Probabilitas yang disebutkan di laporan ini adalah estimasi berbasis data
saat ini, bukan prediksi pasti. Skenario dan range harga adalah kerangka
berpikir, bukan target eksekusi.

Crypto market moves fast. Read decay window: <N days>. Setelah window
ini, baca ulang sebelum dipakai.

Selalu lakukan riset mandiri (DYOR) sebelum mengambil keputusan investasi.
Position sizing keputusan pribadi.

(English) This analysis is produced by AI Holding Crypto Consultant for
internal research purposes. Not financial advice. Probabilities stated
are estimates based on current data, not certain predictions. Scenarios
and price ranges are thinking frameworks, not execution targets. Forecast
decay: <N days>. Always do your own research (DYOR).
```

`@crypto.qa` blocks publish if disclaimer is missing OR doesn't include the decay window.

### 4. The "Bear First" Rendering

Senior reports state the **bear case first** in scenarios — not because we're bearish, but because:

1. Bear cases are systematically under-weighted by writers and readers (psychological bias).
2. Survival depends on bear case being honest.
3. If bear case is plausible, sizing changes immediately regardless of base case.

Rendering rule:

```
[SCENARIOS]

Bear case (X% likelihood):
  <Conditions, levels, time horizon, what happens>

Sideways case (Y% likelihood):
  <Conditions, range, what catalyzes break>

Bull case (Z% likelihood):
  <Conditions, levels, time horizon, what happens>

Sum to 100%. Internal-only reports may omit precise %; external-publish
reports must show probability framing.
```

### 5. Source Citation Standard

Every fact in the body cites:

```
"BTC at $68,400 [CoinGecko 2026-05-17 09:00 UTC]"
"Hashrate ATH 612 EH/s [blockchain.com 2026-05-17 09:00 UTC]"
"F&G = 72 [Alternative.me 2026-05-17 09:00 UTC, via fear_greed.py]"
"Fed funds 5.25-5.50% [FOMC statement 2026-05-01]"
```

Not:
- ❌ "Some sources say BTC is at $68K"
- ❌ "Hashrate is high right now"
- ❌ "Fear & Greed is in greed territory"

### 6. The "What's New, What's Different" Filter

Senior weekly reports start with a "what's actually new" filter — not a recap of unchanged conditions:

```
[WHAT'S NEW THIS WEEK]
  - Fed minutes more dovish than expected (2026-05-XX)
  - BTC ETF inflow re-accelerated to $X
  - On-chain LTH supply began rising again

[WHAT'S UNCHANGED]
  - Cycle phase: still Phase 3 markup
  - Macro regime: still neutral liquidity
  - Major levels intact

[WHAT TO WATCH NEXT WEEK]
  - Powell speech 2026-05-XX
  - CPI 2026-05-XX
  - BTC test of $X resistance
```

Weeks where nothing changed get a 1-paragraph brief, not a forced full recap.

### 7. Crisis Update Discipline

When sudden events hit (hack, exchange failure, regulatory shock, macro surprise), produce a crisis update fast:

```
[CRISIS UPDATE]
Issued:             YYYY-MM-DD HH:MM TZ (within 2 hours of event ideal)
Event:              <what happened, when, where>
Verified facts:     <only what's confirmed>
Unverified claims:  <flagged as such, NOT speculation>

[INITIAL READ]
  Cautious interpretation. Avoid hot takes.

[KNOWN UNKNOWNS]
  What we don't know yet (most of the picture, often).

[POSITIONING IMPACT]
  How this changes the standing read (without buy/sell calls).

[NEXT UPDATE]
  When the next read is coming. Stick to it.

[DISCLAIMER]
  Mandatory. Crisis-specific decay window often 24-48h.
```

Anti-pattern: hot-take crisis updates that age badly within hours.

### 8. External Publish — The Gate Is Per-Piece

For reports that go to public surfaces (Twitter, blog, podcast):

```
[PUBLISH AUTHORIZATION]
  Submitted by:        @crypto.report
  Reviewed by:         @crypto.qa
  Methodology check:   passed
  Disclaimer:          present
  Boundary #4 status:  awaiting Fathur
  Submitted to Fathur: YYYY-MM-DD HH:MM
  Approved by Fathur:  [yes/no, with timestamp]
  Approved for which surface: [Twitter / blog / podcast / other]
```

Default = internal-only. External publish needs the authorization block filled.

### 9. Cross-Company Handoff Templates

When research feeds BrandFlow (for marketing) or NexusAI (for product):

```
[BRANDFLOW HANDOFF]
  Original research:       <path>
  Translation guidance:    What can be simplified, what cannot
  Off-limits framing:      <e.g. don't make it sound like advice>
  Disclaimer requirement:  Yes, marketing version included
  Source citation:         Required even in social copy
  Review on draft:         @crypto.qa before publish

[NEXUSAI HANDOFF]
  Data spec required:      <e.g. F&G + BTC + funding for dashboard>
  Refresh frequency:       <hourly / daily>
  Display rules:           <ranges as ranges, not single numbers>
  Disclaimer in product:   <required UI element>
```

Senior reporters keep the analytical truth intact across the handoff.

### 10. Anti-Patterns Senior Reporting Avoids

- **Single-number price targets in body text.** Range required.
- **"BTC will" / "ETH will" deterministic phrasing.** Block.
- **Disclaimer skipped because "internal only".** Disclaimers cost nothing; build the habit.
- **Burying the bear case at the end.** Bear first.
- **Recapping unchanged conditions weekly.** Filter for new vs old.
- **Hot-take crisis updates.** Cautious-and-late > confident-and-wrong.
- **Forecast ledger skipped.** No ledger = no track record = selective memory.
- **External publish without per-piece Fathur approval.** Boundary #4.
- **Source-thin facts.** Every fact tagged with source + timestamp.
- **Ledger entries with vague invalidation.** "If conditions change" isn't observable; specify.

### Reference

- `knowledge/crypto/forecast-evaluation.md` (Update 12).
- `knowledge/crypto/scenario-modeling.md` (Update 12).
- `companies/crypto-consultant/skills/qa/SKILL.md` (gate enforcement).
- Root SOUL — Boundary #4.
