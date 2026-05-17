# KPI Cheatsheet — Marketing

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.analytics`, `@brandflow.cmo`, `@brandflow.ceo`, `@brandflow.copywriter`

---

## Why KPI Discipline

"Measure or it didn't happen." Every campaign, every piece, needs a KPI defined **before** it ships. Post-hoc metric-shopping is fiction.

This file is the **agency-wide reference** for metric definitions, formulas, and which to use for which goal.

---

## Metric Hierarchy

```
GOAL                  →  PRIMARY METRIC      →  SECONDARY METRICS
                         (the headline)         (supporting context)

Awareness             →  Reach / Impressions →  Branded search volume, Brand mentions
Engagement            →  Engagement Rate     →  Saves, Shares, Comments
Conversion            →  CTR / Conv. Rate    →  Cost per Conversion, Conv. Volume
Retention             →  Repeat engagement   →  Newsletter open rate, Returning traffic
Authority             →  Backlinks / mentions→  Comment quality, Citation depth
```

Pick ONE primary per piece / per campaign. Junior teams pick five and report the one that improved.

---

## Engagement Metrics

### Engagement Rate (ER)

Definition: total engagements ÷ reach (or impressions or followers, depending on platform convention).

Formulas (canonical):
- ER (by reach):       `(likes + comments + saves + shares) / reach × 100%`
- ER (by impressions): `(likes + comments + saves + shares) / impressions × 100%`
- ER (by followers):   `(likes + comments + saves + shares) / followers × 100%`

Use `by reach` when reach data is available — it's the truest engagement signal.

Healthy ranges (post-2024 rough averages):

| Channel | Average ER | Strong ER |
|---|---|---|
| Instagram (organic feed) | 0.8-1.5% | >2.5% |
| Instagram (Reels) | 1.5-3% | >5% |
| LinkedIn (organic post) | 1-3% | >5% |
| LinkedIn (B2B niche) | 2-5% | >7% |
| TikTok | 4-10% | >15% |
| Twitter/X | 0.4-0.8% | >1.5% |

These shift quarterly. Always benchmark against the **client's peer set**, not industry averages.

### Saves

Modern algorithm signal of value. Often more correlated with reach growth than likes.

Save rate: `saves / reach × 100%`

For carousels and educational content, saves are the primary engagement metric — not likes.

### Shares

Strongest viral signal. Share rate: `shares / reach × 100%`

For Reels / TikTok / threads, shares matter more than saves.

### Comments

Comment volume × comment quality both matter. A 3-comment post with substantive replies > a 30-comment post with "🔥🔥🔥" responses.

For QA: review the actual content of comments quarterly. Comment quality drift signals audience drift.

---

## Awareness Metrics

### Reach

Unique accounts that saw the content. The denominator for engagement rate.

### Impressions

Total times content was displayed (one account can register multiple impressions). Always ≥ reach.

Reach < impressions = healthy (rewatchable / re-served content).
Reach = impressions = unusual (only on first-time shares without re-display).

### Branded Search Volume

Number of searches that include the brand name as keyword. Track via Google Search Console (queries containing brand name).

Strong leading indicator: brand search up 30% over baseline = audience awareness genuinely growing.

### Share of Voice (SoV)

Brand's mentions ÷ total mentions in category (over a defined period).

Used for competitive benchmarking. Requires social listening tool.

### Profile Visits

Source of follower growth. Reach without profile-visit ratio = content getting seen but not driving exploration.

`profile-visit rate = profile visits / reach × 100%`

---

## Conversion Metrics

### Click-Through Rate (CTR)

`clicks / impressions × 100%`

Measures how compelling the CTA is. Strong CTR ≠ strong conversion (the landing page does the second job).

### Conversion Rate

`conversions / clicks × 100%`

Where the funnel reveals truth. CTR can be high but if conversion is low, the landing page or offer is the issue.

Define **conversion explicitly**:
- Newsletter signup
- Free trial signup
- Demo booked
- Purchase completed
- DM sent with intent keyword
- WhatsApp click-to-chat opened

### Cost per Conversion (CPC for paid; effective CPC for organic)

`spend / conversions` (paid)
For organic, calculate effective CPC by dividing time-cost or retainer-share by conversions; useful for ROI conversations with clients.

### Lead Quality Score

Beyond conversion volume — are leads from this campaign closing? Score 1-5 based on:
- Qualification (fits ICP?)
- Sales-cycle progression
- Eventual close rate by source

Track per source / campaign over 60-90 days.

---

## Retention Metrics

### Repeat Engagement Rate

`accounts that engaged 2+ times in N days / unique-engaging-accounts × 100%`

Higher = audience returning, brand becoming a habit.

### Newsletter Open Rate

`opens / delivered × 100%`

Healthy ranges:
- Industry-average: 20-25%
- Engaged niche newsletter: 35-50%
- Highly-personal newsletter: 50-70%

Industry numbers fluctuate (Apple Mail Privacy Protection inflates apparent opens). Trust trend lines, not absolute numbers.

### Newsletter Click Rate

`clicks / delivered × 100%`

More signal than opens (can't be triggered by anti-tracking).

Industry-average: 2-5%. Strong: >7%.

### Returning Traffic %

`returning visitors / total visitors × 100%`

Strong leading indicator of brand-as-habit.

---

## Authority Metrics

### Backlinks (referring domains)

Different domains linking to the site. Track via Ahrefs / SEMrush / GSC.

Quality > quantity. 1 link from a respected industry source > 50 links from generic blog farms.

### Brand Mentions (unlinked + linked)

Mentions of the brand name across the web — including social, podcasts, articles, communities. Tracked via social listening.

Strong indicator: brand mentions growing organically without paid amplification.

### Comment Quality

Subjective but trackable. Quarterly QA pass: are top-comment threads showing substantive engagement vs surface reactions?

---

## Calendar / Content Production Metrics

These measure agency execution health, not campaign outcome:

### Pipeline Velocity

`pieces published / pieces planned × 100%` per week

Below 80%: bottleneck investigation needed. Where are pieces stuck?

### Approval Cycle Time

Median time from `DRAFT → APPROVED`.

Healthy: <24 hours. Above 48h = bottleneck (usually CMO or Fathur approval lag, sometimes QA over-blocking).

### Pillar Balance

Posts per pillar per month. Drift = brand losing focus.

### Mix Adherence

Actual 60/30/10 vs planned. Drift = client requests over-rotating to promo, or educational pillar starving.

---

## Per-Goal KPI Anchors (Defaults)

For new clients, these are reasonable starting targets in the first 90 days. Calibrate to peer benchmark after 30 days of analytics.

| Goal | KPI | 90-day target (typical UMKM-tier client) |
|---|---|---|
| Awareness | Reach growth | +30-60% baseline |
| Awareness | Branded search volume | +20-40% |
| Engagement | Engagement rate | At or above peer benchmark |
| Engagement | Save rate | >1.5% on educational pieces |
| Conversion | CTR | 1-3% on bio/CTA links |
| Conversion | Conversion rate | Defined per offer; usually 2-8% |
| Retention | Repeat engagement | 25-40% of engagers return within 14 days |
| Authority | Backlinks | +5-15 referring domains in 90d |

Bigger / mature clients calibrate higher. Stage-zero clients calibrate lower.

---

## Reporting Cadences

| Cadence | Audience | Content |
|---|---|---|
| Daily | Internal (community manager) | Sentiment + flag-watch |
| Weekly | Internal + lightweight client | Pipeline velocity, top performers, anomalies |
| Monthly | Client retainer report | Full mix: awareness, engagement, conversion, authority + narrative |
| Quarterly | Client + agency leadership | Trend lines, pillar drift, persona refresh, strategy adjust |
| Annual | Client + retention review | Year-over-year, ROI, retainer renewal conversation |

---

## Reporting Anti-Patterns

- **Vanity metrics dressed as outcomes.** Reach without engagement / engagement without conversion / followers without retention.
- **Comparing to industry average instead of peer set.** Industry averages mix small + huge brands; peer set is the right reference.
- **Cherry-picking the metric that improved.** Define KPI before launch; report it whether it improved or not.
- **No baseline.** "Reach grew 40%" — from what? Always show baseline.
- **No baseline → no significance.** A 40% jump on tiny baseline can be one strong post; not a trend.
- **Reporting without recommendation.** Numbers without "so what / now what" wastes the reader's time.
- **Mixing window definitions across reports.** Last week vs last 7 days vs last business week — pick one and lock.

---

## What "Improvement" Actually Means

A senior analytics report distinguishes:

- **Statistically meaningful improvement** vs **noise** (high-volume client may need 4-8 weeks of data; small client may never reach significance — direction-only is appropriate there).
- **Sustained improvement** vs **single-data-point spike** (one viral post ≠ system improvement).
- **Improvement on the chosen KPI** vs **improvement on adjacent metric while KPI stayed flat**.
- **Causal improvement** vs **correlated improvement** (always interrogate "what else happened?").

---

## Reference

- `companies/brandflow/skills/automation/SKILL.md` — Senior Patterns §9 A/B test discipline.
- `companies/brandflow/skills/research/SKILL.md` — Senior Patterns §7 channel benchmark research.
- `knowledge/marketing/utm-conventions.md` — without UTM convention, attribution dies.
- `knowledge/marketing/marketing-sop.md` — KPI defaults section.
- `tools/social_monitor.py` (Update 11) — metric ingest from social platforms.
