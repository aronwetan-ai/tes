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
