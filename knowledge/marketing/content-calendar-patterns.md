# Content Calendar Patterns

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.social`, `@brandflow.pm`, `@brandflow.cmo`, `@brandflow.copywriter`

---

## Why Calendar Patterns

Calendars serve two jobs:
1. **Cadence discipline** — promise the audience a rhythm, keep it.
2. **Theme variety** — same audience, different angles, no fatigue.

This file is the **agency-wide pattern library** for how to structure calendars at different brand maturities.

---

## Cadence vs Volume — Pick the Right Question

Junior teams ask "how often should we post?" — implying more = better.

Senior teams ask "what cadence can we hold for 12 weeks without quality drop?" The answer is usually **less than what's aspirationally claimed.**

The agency's default for most clients:

| Brand maturity | Sustainable cadence |
|---|---|
| New brand, single operator | 2-3 posts/week (1 channel) |
| Established, freelancer support | 4-5 posts/week (1-2 channels) |
| Mature, content team | 5-7 posts/week + repurposing across 3+ channels |
| Enterprise / agency-self | Variable per channel; orchestrated calendar |

If a client demands "daily" and you don't have the resources, push back. **3 strong posts/week beats 7 mediocre ones** in every metric except gross publication count.

---

## The 60/30/10 Mix

Standard agency calendar mix per client:

```
60% — EDUCATIONAL / VALUE-GIVING
   Tutorials, frameworks, breakdowns, insights, data, comparisons
   → Builds trust + saves + reach

30% — ENGAGEMENT / COMMUNITY
   Questions, polls, behind-the-scenes, controversy-light takes,
   responses to industry conversation, founder-personal stories
   → Builds relationship + comments + shares

10% — PROMOTIONAL / SALES
   Offers, launches, testimonials, case studies with sales hook,
   pricing transparency posts, limited-time pushes
   → Builds revenue
```

Clients who push for higher promotional % almost always over-rotate, exhaust the audience, then engagement collapses. Defend the 60/30/10 default with data when challenged.

---

## Pillar System (Topic Clustering)

Beyond mix, organize content by **pillars** — 3-5 topical territories the brand owns.

```
PILLAR 1 — <topic>          (e.g. "performance marketing for UMKM")
PILLAR 2 — <topic>          (e.g. "tools we actually use")
PILLAR 3 — <topic>          (e.g. "founder operations")
PILLAR 4 — <topic>          (e.g. "client wins / case studies")
```

Per pillar, decide:
- Which sub-themes recur (4-6 per pillar)
- Which formats are native (carousel? Reels? thread? long-form?)
- Posting frequency target per pillar
- Owner per pillar (who's source of truth?)

Posts are tagged by pillar in the pipeline. End-of-month review checks pillar balance.

Drift detection: if Pillar 4 (case studies) hasn't been posted in 6 weeks but Pillar 1 has 24 entries, the brand is over-rotating educational and under-leveraging proof.

---

## Day-of-Week / Hour-of-Day Patterns

Defaults; verify against each client's own analytics over time.

### Instagram (general consumer / lifestyle)
- Tue-Thu best engagement window.
- Sun also strong for some niches.
- Hours: 11:00-13:00 + 19:00-21:00 local.

### LinkedIn (B2B / professional)
- Tue-Thu strong; Mon and Fri also okay.
- Weekends weak.
- Hours: 08:00-10:00 + 12:00-13:00 local.

### Twitter / X
- Weekdays 09:00-11:00 + 14:00-15:00.
- Sun evening surprisingly strong for thinkpiece content.

### TikTok
- Evenings universally strong.
- Don't fight algorithm — it surfaces fresh content over old; cadence > timing.

### YouTube
- Thu-Sun for entertainment.
- Tue-Thu for educational.

These are starting points. After 30 days of analytics per client, override with **what works for that account.**

---

## Calendar Templates

### Template A — "Solo Founder, 1 Channel, 3 Posts/Week"

```
Mon morning      Educational (Pillar 1)
Wed morning      Engagement (poll / question / behind-the-scenes)
Fri morning      Educational (Pillar 2 or 3)

Bi-weekly:       Saturday: case study / case win
Monthly:         Promotional offer
```

Total ~13 posts/month: ~9 educational + ~3 engagement + ~1 promotional.

### Template B — "Established Brand, 2 Channels, 5 Posts/Week"

```
IG (3/week)
   Mon: Educational carousel
   Wed: Reel (behind-the-scenes / quick tip)
   Fri: Educational or case study

LinkedIn (2/week)
   Tue: Long-post (Pillar deep-dive)
   Thu: Repurposed insight from IG content this week
```

### Template C — "Multi-Channel Calendar, 8 Posts/Week"

```
IG (4/week)
   Mon: Educational carousel
   Wed: Reel
   Fri: Educational or community (UGC, Q&A)
   Sun: Story-led founder piece

LinkedIn (2/week)
   Tue: Long-post
   Thu: Article (longer, SEO-optimized)

TikTok (1-2/week)
   Wed/Sat: Trending-format short

X (1-2/week)
   Mon/Thu: Thread — repurposed from LinkedIn long-post
```

This template requires content team or fully delegated production.

### Template D — "Agency-Self Calendar"

For BrandFlow's own marketing (showcasing agency capability):

```
LinkedIn (3/week)              # primary B2B channel
   Mon: Educational long-post
   Wed: Case study (anonymized client win)
   Fri: Founder-led perspective post

IG (2/week)                    # visual showcase
   Tue: Carousel (case study or tutorial)
   Sat: Reel (work-process / behind-the-scenes)

Newsletter (1/week)            # owned audience
   Thu: Weekly recap + curated insights
```

---

## Campaign Layering Over Cadence

Calendars host both the **always-on cadence** and **campaign overlays**. They coexist:

```
Always-on cadence:   3-5 posts/week per pillar mix (60/30/10)
                  +
Campaign overlay:    Time-bound, theme-focused, may add 2-5 extra pieces
                     across the campaign window
```

Avoid: a 4-week campaign that 100% replaces always-on. Audience expects the rhythm.

Senior pattern:
- Campaign weeks: ~70% campaign content + ~30% always-on (keeps the rhythm).
- Non-campaign weeks: 100% always-on.
- Never go more than 2 weeks without an always-on Pillar 4 (case-study) post — proof bank thins.

---

## Editorial Calendar JSONL Format (Agency Standard)

The pipeline (see `companies/brandflow/skills/automation/SKILL.md` Senior Patterns §3) holds the canonical schema. Calendar view is a slice of the pipeline filtered to `stage IN (DRAFT, REVIEW, APPROVED, SCHEDULED)`.

Calendar-view fields surfaced for quick review:

```
date           |  client     |  channel   |  format    |  pillar  |  hook (≤80c)  |  owner             |  stage
2026-05-20 09  |  acme       |  IG        |  carousel  |  P1      |  "Pricing..."  |  @brandflow.copy   |  DRAFT
2026-05-20 14  |  kopi-x     |  LinkedIn  |  long-post |  P2      |  "Cold..."     |  @brandflow.writer |  APPROVED
...
```

Quick sanity checks at calendar review:
- Is each client hitting their committed cadence?
- Is the 60/30/10 mix balanced this week?
- Is each pillar represented this month?
- Are there approval bottlenecks (pieces stuck >48h in REVIEW)?

---

## Holiday + Event Calendar

Layer over editorial calendar:

- Major Indonesia holidays (Idul Fitri, Natal, Imlek, Independence Day, etc.) — plan content 2-3 weeks ahead.
- Industry-specific events relevant to client (conferences, trade shows, launches).
- Cultural moments where brand archetype invites participation.

Don't force participation. Brands that "can't shut up about the holiday" exhaust audiences. **Acknowledge once, well, then return to programming.**

---

## Trend Layering

When a trend hits, decide fast (≤12 hours from detection):

```
Q1. On-brand for archetype?       No → skip
Q2. On-curve?                      Late → skip; Early/Mainstream → consider
Q3. Audience cares?                No → skip
Q4. Can we add an angle?           Generic → skip
Q5. Effort vs window?              Mismatched → skip
```

Reference: `companies/brandflow/skills/research/SKILL.md` Senior Patterns §6 trend triage.

If it passes: add 1 piece of trend-specific content. Don't replace the whole week's calendar.

---

## Cross-Posting vs Repurposing

Cross-posting = same content, multiple channels. Bad. Audiences notice; algorithms penalize duplicate.

Repurposing = same idea, native execution per channel. Good. See:
- `companies/brandflow/skills/content/SKILL.md` Senior Patterns §9 (copy side).
- `companies/brandflow/skills/design/format-adaptation.md` (visual side).

Calendar-level rule: when an idea ships to channel A, schedule its natively-adapted version to channel B at least 48 hours later (if at all). Same-day same-content cross-posts read lazy.

---

## Anti-Patterns

- **Daily posting promise without resources.** Promised 7/week, sustainable 3/week → quality collapse → audience leaves.
- **100% promotional during launches.** Audience exhaustion + algorithm penalty.
- **No pillar discipline.** Random topics; brand feels unfocused; audience can't form an image.
- **Calendar that ignores client cadence reality.** Pretty grid in Notion, real shipped output is half.
- **Same-day cross-posting.** Penalized by every algorithm.
- **No campaign overlay system.** Either always-on dies during campaigns or campaigns dilute always-on.
- **Calendar without owners per slot.** Pieces sit unclaimed.
- **No approval-time buffer.** Schedule for Mon morning with no Friday review = Sunday-night chaos.

---

## Reference

- `companies/brandflow/skills/social/SKILL.md` — channel strategy.
- `companies/brandflow/skills/automation/SKILL.md` — pipeline + scheduler.
- `companies/brandflow/skills/content/SKILL.md` — repurposing discipline.
- `knowledge/marketing/social-platform-specs.md` — per-channel timing defaults.
- `tools/content_scheduler.py` (Update 11) — pipeline-aware scheduler with approval gates.
