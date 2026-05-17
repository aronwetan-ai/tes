---
name: research
description: Audience research, competitive analysis, market research, trend analysis for BrandFlow campaigns.
company: BrandFlow
used_by: ["@brandflow.cmo", "@brandflow.copywriter", "@brandflow.analytics"]
---

# Research Skill — BrandFlow

Marketing research — understanding audience, competition, and market context before campaigns ship.

Different from `@crypto.research` (crypto market research) and from a generic "fact check" — this is **commercial intelligence** for marketing strategy.

## When to Use

- Audience persona development.
- Competitive content audit.
- Market trend analysis.
- Channel benchmark research.
- Voice / tone reference research.
- Hashtag / trend research.
- Brand sentiment baseline.

## Rules

1. **Verify with primary sources** when possible. Linked example > "I heard somewhere".
2. **Separate fact from inference.** "Brand X has 1M followers" ≠ "Brand X has loyal audience".
3. **Recent over old.** Marketing trends move fast. 2-year-old benchmark may be stale.
4. **Competitor inspiration** is fine. Competitor copy is not. Note the line.
5. **Audience research** focuses on real behavior (what they do) over claimed preferences (what they say in surveys).

## Output Format

For audience persona:
```
[NAME / SEGMENT]   "Sarah the SaaS Founder"
[DEMOGRAPHICS]     Age, location, role, company size
[GOALS]            What they're trying to achieve
[PAIN POINTS]      What's blocking them
[CHANNELS]         Where they spend attention
[VOICE THEY TRUST] Whose content they consume
[OBJECTIONS]       Why they wouldn't buy / engage
[MESSAGE FRAME]    How to talk to them
```

For competitive audit:
```
[COMPETITOR]    Name + URL
[POSITIONING]   How they describe themselves
[VOICE]         Tone characteristics
[CONTENT MIX]   Educational / promotional / engagement %
[STRENGTHS]     What they do well
[WEAKNESSES]    Where they're vulnerable
[OPPORTUNITY]   Where we can differentiate
[NOTES]         Recent changes, campaigns, signals
```

For trend research:
```
[TREND]        What's happening
[EVIDENCE]     Sources confirming the trend
[TIMING]       Early / mainstream / late stage?
[FIT]          Does it match BrandFlow brand and audience?
[RECOMMENDATION] Ride / observe / skip
[ACTION]       If ride: what specific content adapts
```

## Sources / Approach

**Free**:
- Manual SERP analysis.
- Social listening (search hashtags, mentions).
- Competitor's own owned channels.
- Google Trends.
- Industry blogs / newsletters.

**Freemium**:
- BuzzSumo (limited free).
- SimilarWeb (limited free).
- Ahrefs / SEMrush (paid trial).

**Paid (escalate to CEO)**:
- Brandwatch / Meltwater for full social listening.
- Custom audience surveys.

## Cross-Skill / Cross-Agent

- Insights become campaign brief → `@brandflow.cmo`.
- Voice reference → `@brandflow.copywriter` + `skills/content`.
- Visual reference / mood board → `@brandflow.designer` + `skills/design`.
- Hashtag / trend → `@brandflow.social`.
- Performance baseline → `@brandflow.analytics`.

## What This Skill Does NOT Cover

- Crypto market research → `@crypto.research`.
- Technical research (libraries, APIs) → `@nexusai.cto`.
- Internal performance data — that's analytics, not research.

## Reference

- `companies/brandflow/SOUL.md`
- `knowledge/marketing/marketing-sop.md`


---

## Senior Patterns (Deep Dive) — Update 11

The senior marketing-research playbook for agency-context work. Research at the agency feeds three buckets: **client onboarding** (voice + persona + competitive baseline), **campaign briefs** (audience + angle + channel mix), and **performance interpretation** (why did this work / not work).

### 1. Three Research Modes — Don't Mix Them

| Mode | Purpose | Output | Time budget |
|---|---|---|---|
| Discovery | "We don't know enough yet." | Hypotheses, questions, signal map | 2-8 hours, batched |
| Validation | "We have a hypothesis; is it right?" | Confirmed/refuted with evidence | 1-3 hours, focused |
| Reporting | "What just happened?" | Causal narrative + recommended action | 0.5-2 hours, post-campaign |

Mixing modes = endless rabbit holes. State the mode at the top of every research note.

### 2. Audience Persona — From Demographic to Psychographic to Behavioral

Junior personas: age + gender + city + job title. Useless for marketing; everyone in the segment looks identical.

Senior personas climb 3 layers:

```
LAYER 1 — DEMOGRAPHIC (basic identification)
  Age range, location, role, company size, income range

LAYER 2 — PSYCHOGRAPHIC (what they care about)
  Goals (next 6 months)
  Fears (what's keeping them up)
  Identity statements ("I'm the kind of person who...")
  Status concerns (peer perception they care about)
  Trusted voices (whose content they consume)

LAYER 3 — BEHAVIORAL (what they actually do)
  Where they spend attention (specific platforms, hours)
  How they research before buying
  What triggered past buy/sign-up decisions
  Objections that stopped past purchases
  Words they use for their own problem (their language, not industry jargon)
```

Layer 3 is where copy lands. Without Layer 3, the persona is fiction. Reference: `knowledge/marketing/persona-template.md`.

### 3. Persona Source Hierarchy

| Source | Quality | Cost |
|---|---|---|
| 1. 1:1 conversations with 5-7 actual customers | Highest | High (1-2 weeks, scheduling) |
| 2. Sales / support transcripts (real complaints, real questions) | High | Low |
| 3. Existing customer reviews (theirs + competitors') | High | Low |
| 4. Social listening on hashtags + relevant communities | Medium | Low |
| 5. Search queries (Answer the Public, Reddit, Quora) | Medium | Low |
| 6. Surveys (claimed preferences) | Low-Medium | Medium |
| 7. Pure demographic data | Low | Low |

Senior workflow: blend top 3 into the persona; treat 4-5 as triangulation; use 6-7 only when nothing better exists. Never rely on 6-7 alone — claimed behavior ≠ real behavior.

### 4. Voice-of-Customer Mining (Concrete Method)

Instead of "what do customers want?", senior research mines **the literal phrases**:

```
1. Pull last 100 reviews / DMs / support tickets / sales call transcripts.
2. Highlight every phrase a customer uses to describe:
   - Their problem ("I keep getting stuck at...")
   - Their goal ("I just want to...")
   - Their fear ("What if I...")
   - Their before-state ("I was tired of...")
   - Their after-state ("Now I can...")
3. Cluster phrases. Frequency = signal.
4. Top 10-15 phrases become **the brief's source of language** for hooks and body copy.
```

Senior copy uses customer phrases verbatim wherever credible. Example:
- Bad: "Streamline your workflow with our productivity solution."
- Good: "Setiap senin saya buang 2 jam cuma rapat status." (taken from real DM)

### 5. Competitive Audit — Two Kinds

**Direct competitor audit** = what the brand competes with for the same buy decision.
**Adjacent inspiration** = brands the audience admires that are NOT competitors.

Adjacent often beats direct for inspiration. A SaaS may compete with another SaaS but the audience admires Patagonia or Glossier — borrowing voice/visual moves from adjacent brands feels fresh; copying direct feels derivative.

Audit dimensions per competitor:

```
[POSITIONING]       Their one-line claim (in their words)
[VOICE]             Tone characteristics (3-5 adjectives + 1 line example)
[CONTENT MIX]       Education / promo / engagement / community %
[CADENCE]           Posts per week per channel
[FORMATS]           Carousel / Reels / long-form / short-form distribution
[ENGAGEMENT]        Avg likes / comments / saves on top 10 posts
[STRENGTHS]         What they do well
[WEAKNESSES]        Where they're vulnerable
[OPPORTUNITY]       Where we differentiate
[RECENT MOVES]      Campaigns / pivots in last 90 days
```

Cap the audit at 5-7 competitors. Bigger = analysis paralysis.

### 6. Trend Triage — Should We Ride It?

Trends arrive constantly. Most should be skipped.

```
Q1. Does the trend match the brand archetype?
    No  → SKIP. Forced trends look desperate.
    Yes → continue.

Q2. Where is the trend on the curve?
    Early    → Strong opportunity, light effort to capitalize.
    Mainstream → Decision: ride if angle is unique, else skip.
    Late     → SKIP. Riding late = derivative.

Q3. Does the audience care?
    Audience-channel match? If trend lives on TikTok and audience is on LinkedIn → SKIP for that brand.

Q4. Can we add an angle?
    "Same trend, with our domain twist" → ride.
    "Same trend, generic" → skip. Crowd already has it.

Q5. Effort vs window?
    Trend window <2 weeks + production effort >2 days → SKIP.
    Trend window 4+ weeks + lightweight format → ride.
```

Document the decision. "We skipped the X trend because Y" is useful when the same trend resurfaces.

### 7. Channel Benchmark Research

Before promising a KPI to a client, benchmark against their realistic peer set, not against industry-leading outliers.

Benchmark dimensions:

| Dimension | Source |
|---|---|
| Engagement rate (peers, same size, same niche, same channel) | Manual sample of 8-12 peer accounts |
| Posting cadence (what's normal, what's the floor, what's the ceiling) | Same sample |
| Content mix proportions | Same sample |
| Reach-to-follower ratio | Native analytics if accessible |
| CPC / CPM benchmarks (paid) | Industry reports + own past data |

Report to client: "Your peers run at X engagement. Top quartile in your peer set hits Y. Realistic 3-month target: Y/2." Beats promising "we'll 10× your engagement."

### 8. Hashtag / Community Research (Per-Channel Specifics)

Not "generic hashtag research." Modern hashtag research = community discovery.

```
Per relevant tag (~20-30 candidates):
  - Volume of posts (active community vs ghost town)
  - Recency (top posts from last 7 days vs 6 months)
  - Audience overlap with brand audience (manual scan: who's posting?)
  - Spam ratio (% obvious bots / promo)
  - Engagement quality (real comments vs follower-buy patterns)

Output: 8-15 tags per brand:
  - 3-5 mid-volume (10k-100k posts) for discovery
  - 5-8 niche (1k-10k posts) for relevance
  - 2-3 brand/campaign-specific (low volume, high signal)
  - 0 mass-volume (>1M posts) — they don't reach anyone
```

### 9. Research Output Templates

For onboarding research (full client kickoff):

```
[CLIENT]                  Name + tier
[BUSINESS]                What they do, who pays them, how
[CURRENT POSITIONING]     Their one-line claim (verified with founder)
[3-LAYER PERSONA]         (Layer 1, 2, 3 above) for primary segment
[VOICE PROFILE]           See knowledge/marketing/brand-voice-rubric.md
[VOICE-OF-CUSTOMER]       Top 10-15 phrases from sources
[COMPETITIVE AUDIT]       Top 5 competitors + 2-3 adjacent inspirations
[CHANNEL BENCHMARK]       Peer-set realistic ranges
[OPPORTUNITY MAP]         Where we play, where we don't
[KPI ANCHORS]             Realistic 3 / 6 / 12-month targets
```

For campaign-level research (pre-brief):

```
[CAMPAIGN]                Name + scope
[OBJECTIVE]               Awareness / engagement / conversion / retention
[AUDIENCE FOCUS]          Slice of persona for this campaign
[INSIGHTS]                Top 3 things research surfaces
[ANGLES]                  3-5 angles to test
[RECOMMENDED ANGLE]       Pick + reason
[CHANNEL MIX]             Recommended weights
[KPI]                     What we measure
[RISKS]                   What could miss
```

For post-campaign learning report:

```
[CAMPAIGN]                Name
[PLAN VS ACTUAL]          Side-by-side: planned KPI vs delivered
[WHAT WORKED]             Patterns ≥2 pieces of evidence
[WHAT DIDN'T]             Same standard
[NEW HYPOTHESES]          Things to test next
[RECOMMENDATIONS]         For next campaign / refresh
[MEMORY]                  Save to brandflow MEMORY.md
```

### 10. Anti-Patterns Senior Researchers Don't Ship

- **"Findings" without sources.** Every claim has a source.
- **Survey-only personas.** Claimed behavior is unreliable.
- **Mode-mixing.** Discovery sliding into validation sliding into reporting = no useful output.
- **Industry-average benchmarks dressed as peer benchmarks.** Wrong reference set.
- **Trend FOMO.** Riding trends just because they're trending.
- **5-month research project for a campaign that ships in 2 weeks.** Time-box research to the decision it informs.
- **Treating competitor audit as "what to copy."** Audit informs differentiation, not imitation.
- **Single-source insights.** One review or one DM is anecdote, not signal. Need ≥3 occurrences before treating as pattern.

### Reference

- `knowledge/marketing/persona-template.md` (Update 11).
- `knowledge/marketing/brand-voice-rubric.md` (Update 11).
- `knowledge/marketing/copywriting-frameworks.md` (research → framework selection).
- `companies/brandflow/skills/content/SKILL.md` (Senior Patterns — uses voice-of-customer phrases verbatim).
