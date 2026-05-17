---
name: seo
description: Keyword research, on-page SEO, content optimization, search intent matching for BrandFlow long-form output.
company: BrandFlow
used_by: ["@brandflow.seo", "@brandflow.copywriter", "@brandflow.writer"]
---

# SEO Skill — BrandFlow

Search optimization for long-form output (blog, article, landing page). Different from social — search rewards specific patterns.

Inherits BrandFlow SOUL. SEO is craft, not magic. We optimize for **search intent + structure**, not for keyword density.

## When to Use

- Keyword research for new article topic.
- On-page SEO audit / optimization.
- Search intent analysis.
- Title + meta description writing.
- URL structure decisions.
- Internal linking strategy.
- Blog post structure planning.

## Process

1. **Identify search intent.** Informational / Navigational / Transactional / Commercial.
2. **Pick primary keyword + 2-3 secondary.** Primary in title, H1, first 100 words. Secondary in H2/H3.
3. **Check competition.** Top-3 SERP results — what length, depth, format?
4. **Match or beat.** Article length and depth should match top results minimum.
5. **Structure for skim**: H2/H3 navigation, bullet points, short paragraphs.
6. **Internal links** to related content. **External links** to credible sources for fact claims.

## SEO Checklist (Per `knowledge/marketing/marketing-sop.md`)

For every blog article:
- [ ] Target keyword identified (1 primary + 2-3 secondary).
- [ ] Title contains primary keyword + benefit.
- [ ] Meta description: 150-160 chars, includes CTA.
- [ ] H1 = title; H2/H3 contain secondary keywords naturally.
- [ ] Article length matches top-3 SERP competitors.
- [ ] Internal links: minimum 2 to related articles.
- [ ] External links: to credible sources for any factual claim.
- [ ] Image alt text descriptive (not "image1.png").
- [ ] URL slug: short, lowercase, hyphenated.
- [ ] Mobile-readable (paragraph length, font size considerations).

## Rules

1. **Search intent first**, keyword second. A keyword without intent match won't rank.
2. **No keyword stuffing.** Modern search punishes this.
3. **Don't write for bots.** Write for humans, structure for crawlers.
4. **Cite primary sources** when claiming fact. Search and readers both reward this.
5. **Update is publishing too.** Re-optimize old articles — often higher ROI than new ones.
6. **Internal links > external links** for SEO juice flow within site.

## Output Format

For keyword research:
```
[TOPIC]         What we're considering writing about
[INTENT]        Informational / Navigational / Transactional / Commercial
[PRIMARY KW]    <keyword> + estimated volume / difficulty
[SECONDARY KWs] <2-3 keywords>
[COMPETITION]   Top-3 SERP summary (titles, lengths, format)
[OPPORTUNITY]   Where competitors are weak
[RECOMMENDATION] Write / skip / different angle
```

For on-page audit:
```
[URL]           The page being audited
[ISSUES]        By severity: Critical / Major / Minor
   - <issue>: <recommendation>
[OPPORTUNITIES] Quick wins
[REWRITE]       What sections need rewrite
[STRUCTURE]     Heading hierarchy + suggested changes
```

For blog post brief (handed to copywriter / writer):
```
[TITLE]         <primary keyword + benefit>
[META DESC]     150-160 chars, with CTA
[URL SLUG]      /short-lowercase-hyphenated
[PRIMARY KW]    <keyword>
[SECONDARY KWs] <2-3>
[INTENT]        <informational / etc>
[STRUCTURE]
   H1: <title>
   H2: <section 1>
     H3: <subsection if needed>
   H2: <section 2>
   ...
[INTERNAL LINKS] <2+ links to related articles>
[WORD COUNT]    Target range based on competitors
```

## Per-Channel Notes

- **Blog**: full SEO treatment.
- **LinkedIn long-form**: title and first 1-2 lines optimized; LinkedIn discovery > Google.
- **YouTube description**: keyword in first 100 chars.
- **Landing page**: SEO + conversion both, often conversion wins.

## Cross-Skill / Cross-Agent

- Long-form copy production → `@brandflow.copywriter` / `@brandflow.writer` + `skills/content`.
- Performance data (rankings, organic traffic) → `@brandflow.analytics`.
- Strategy for content investment → `@brandflow.cmo`.
- Technical SEO (sitemap, schema, redirects) → loop in `@nexusai.frontend` / `@nexusai.devops` + relevant skills.

## What This Skill Does NOT Cover

- Paid search (SEM, ads). Different domain — escalate to CMO for budget.
- Technical SEO infra (CDN, page speed) — coordinate with NexusAI.
- Social copy — uses `skills/content` instead.

## Reference

- `companies/brandflow/SOUL.md`
- `knowledge/marketing/marketing-sop.md` (SEO Checklist section)


---

## Senior Patterns (Deep Dive) — Update 11

The senior-SEO playbook for agency-context long-form work. Modern SEO = matching search intent, structuring for skim, and building topical authority — not gaming keyword density.

### 1. Search Intent Classification (The Foundation)

Before keyword volume, classify **intent**. The wrong-intent article doesn't rank no matter how good the copy is.

| Intent | What the searcher wants | Right format | Wrong response |
|---|---|---|---|
| Informational | Definition, how-to, explanation | Article, guide, video | Sales page |
| Navigational | A specific site / brand / page | Brand page, login | Generic article |
| Commercial Investigation | Compare, "best of", review | Comparison, review, listicle | One-product pitch |
| Transactional | Buy, sign up, download | Product page, pricing, signup | Long-form blog |

Test: search the keyword. Top 3 results' format = the dominant intent. Match it. If 3/3 are listicles, your essay won't rank — Google has decided "listicle" is the answer.

Reference: `knowledge/marketing/search-intent.md`.

### 2. Topical Authority > Single Article

Single article ≠ ranking. Cluster of articles around a topic = ranking.

```
PILLAR PAGE (broad, comprehensive, ~3000-5000 words)
  └─ CLUSTER POST 1 (specific subtopic, ~1500 words)
  └─ CLUSTER POST 2 (specific subtopic, ~1500 words)
  └─ CLUSTER POST 3 (specific subtopic, ~1500 words)
  └─ CLUSTER POST 4 (long-tail variant, ~1200 words)
```

Internal links flow:
- Every cluster post links UP to the pillar.
- Pillar links DOWN to every cluster post.
- Clusters link laterally to 1-2 related clusters when contextually natural.

This signals to search: "this site owns this topic." A single great article without a cluster ranks for a week, then gets out-competed.

### 3. Keyword Tier System for Agency Clients

Pick keywords by **tier**, not by volume alone:

| Tier | Volume | Difficulty | Use for |
|---|---|---|---|
| T1 — Big-money | 10k+/mo | Hard | Pillar page, long-term investment (6-12mo to rank) |
| T2 — Validation | 1-10k/mo | Medium | Cluster posts, expected ranking 3-6mo |
| T3 — Long-tail | 100-1k/mo | Easy | Quick wins, expected ranking 1-3mo |
| T4 — Hyper-niche | 10-100/mo | Very easy | Conversion-heavy ("agency [city] [niche]") |

Most clients oversize T1. Senior SEO output for a new client: **80% T3 + T4 wins first, 15% T2 mid-term, 5% T1 long-term play.** This builds compound traffic + authority. Going all-T1 = 6 months of zero traffic.

### 4. SERP Reverse-Engineering (Before Writing)

Senior workflow: don't write, then check. **Check first, then write.**

```
1. Search the target keyword.
2. Open top 5 results in tabs.
3. Note for each:
   - Title structure (question / listicle / how-to / comparison)
   - Word count
   - H2 hierarchy (extract their TOC)
   - Above-fold elements (definition / TOC / video / image)
   - Schema markup (article / FAQ / how-to / product)
   - Last updated date
   - Backlink count (Ahrefs/SEMrush if available)
4. Common patterns across all 5 = required.
5. Gaps across all 5 = your differentiation.
```

Required = table stakes (you must include or you're not competing). Differentiation = where you win.

### 5. On-Page Structure for Modern SEO

```
TITLE                 50-60 chars; primary keyword + benefit/year/specificity
                      e.g. "Cold Email Templates for B2B SaaS (2026 Update)"

META DESC             150-160 chars; primary kw + value + CTA
                      e.g. "12 cold email templates with 30%+ reply rate, with breakdowns of why each works. Updated for 2026 deliverability rules."

URL SLUG              /short-keyword-only-no-stopwords
                      Bad: /how-to-write-cold-emails-in-2026
                      Good: /cold-email-templates-b2b

H1                    Mirrors title. ONE H1 per page. Contains primary keyword.

INTRO (≤150 words)
  - Hook: the searcher's pain in their words
  - Promise: what this article delivers
  - Credibility: why trust this source (1 line)
  - Path: brief TOC mention

H2 TOC (skim path)
  - 5-8 H2s for typical 1500-word post
  - 8-12 H2s for pillar
  - Each H2 contains a secondary or LSI keyword naturally
  - Order H2s in the way the searcher's mind progresses

PARAGRAPH RHYTHM
  - 1-3 sentences per paragraph (mobile readability)
  - Mix paragraph length: 1 short, 1 medium, 1 short, 1 medium...
  - Bullet lists every 200-400 words (skim anchors)
  - Subheading every ~300 words

INTERNAL LINKS (≥3 per article)
  - 1 to pillar (if cluster post)
  - 1-2 to lateral cluster posts
  - 1 to a high-converting page (if natural)

EXTERNAL LINKS (1-3 per article)
  - To primary sources for any factual claim
  - Open in new tab

SCHEMA MARKUP
  - Article schema: always
  - FAQ schema: when 3+ Q&As exist
  - HowTo schema: when steps exist
  - Author schema: bio + credibility signals

CONCLUSION (≤200 words)
  - Synthesize 3-5 takeaways
  - One CTA, specific
  - Optional: "next read" pointing to related cluster
```

### 6. E-E-A-T (Experience, Expertise, Authoritativeness, Trust)

Google's modern ranking lens. Every article needs:

| Signal | How to provide |
|---|---|
| Experience | First-person ("we ran 200 cold emails", "in our agency we found"), specific numbers, screenshots of real outcomes |
| Expertise | Author byline with credentials, published-elsewhere links, technical depth that goes past surface-level |
| Authoritativeness | Citations of other authoritative sources, reciprocal recognition (mentions in industry pubs) |
| Trust | Source links, dated content, transparent methodology, clear contact / about / disclosure pages |

Articles that read as "ChatGPT generic regurgitation" fail E-E-A-T regardless of keyword optimization. Senior SEO output is **brand-voiced, specific, sourced**.

### 7. Refresh / Re-optimize Pattern (Often Higher ROI Than New)

Existing articles that ranked positions 4-15 are gold. They're already half-ranked; refreshing nudges them into top 3.

Refresh checklist:

```
[ ] Updated title (year, currency of facts)
[ ] Updated stats and examples (drop anything older than 2 years)
[ ] Added H2 sections that competitors have but we don't
[ ] Tightened intro to current style
[ ] Added FAQ section (FAQ schema bonus)
[ ] Added 1-2 new internal links from recently published cluster posts
[ ] Updated images / regenerated alt text
[ ] Updated published date (or use modified date) — be transparent
```

Rule of thumb: **2 hours of refresh on a 4th-position article > 8 hours of new article from scratch.** Audit existing articles quarterly; refresh 3-5 per quarter.

### 8. AI Overviews / SGE Optimization

Generative search (Google's AI Overviews, Bing chat, Perplexity, ChatGPT browsing) increasingly intercepts traffic before it reaches your page. Compete by being the **citable source**:

- **Lead with the direct answer** in the first 100 words. AI overviews extract answer-style passages.
- **Bullet structure**: AI cites bullet lists more than prose paragraphs.
- **Discrete factual claims** with sources. Vague prose doesn't get cited.
- **FAQ section** with question-format H2/H3. Often quoted verbatim.
- **Update frequency**: AI overviews favor recently updated content.

This is a directional bet, not a guarantee. Track citations as a new metric class beyond clicks.

### 9. Technical SEO Coordination Points (Loop in NexusAI)

These belong to NexusAI but the SEO specialist surfaces them:

- Page speed (Core Web Vitals: LCP, INP, CLS).
- Mobile responsiveness.
- HTTPS + HSTS.
- Sitemap.xml generation + robots.txt sanity.
- Structured data validation.
- 301 redirect strategy (when URLs change).
- Canonical tags (when content is syndicated).
- Indexability check (no accidental noindex).
- JS rendering (SPA → SSR/SSG decision for any new client site).

When SEO finds technical debt → file ticket to `@nexusai.devops` or `@nexusai.frontend` with specifics. Don't try to "patch" it in copy.

### 10. KPI Stack for SEO Work

| Layer | Metric | Tool |
|---|---|---|
| Visibility | Average position, impressions | GSC |
| Acquisition | Organic clicks, CTR | GSC |
| Engagement | Bounce, time-on-page, scroll depth | GA4 |
| Conversion | Goal completion, signups, sales attributed | GA4 / CRM |
| Authority | Backlinks, referring domains, brand mentions | Ahrefs / SEMrush |

Report what matters to the client tier:
- Small agency clients (T3/T4 keywords) → clicks + conversions.
- Mid-tier clients → clicks + position-improvement deltas.
- Big retainer clients → full stack + competitor share-of-voice.

### 11. Anti-Patterns Senior SEO Doesn't Ship

- **Keyword stuffing.** Modern algos punish this; humans hate reading it.
- **Writing for crawlers.** Bots that mattered in 2008 don't matter now. Write for humans, structure for crawlers.
- **Targeting only T1 keywords for new clients.** 6 months of zero traffic = client churn.
- **Single-article strategy without clusters.** No topical authority = no ranking.
- **Skipping E-E-A-T.** Generic AI-tasting prose is now actively de-ranked.
- **"SEO copywriter" mode that ignores hook + body discipline.** SEO content still has to be readable.
- **Ignoring SGE / AI Overviews.** Even if traffic looks fine today, the trend matters.
- **Promising rankings.** "We'll get you to position 1 in 30 days" is a lie. Senior SEO promises **process + leading indicators**, not outcomes outside of one's control.

### Reference

- `knowledge/marketing/search-intent.md` (Update 11 cheatsheet).
- `knowledge/marketing/copywriting-frameworks.md` (for SEO long-form structure).
- `tools/readability_check.py` (Update 11 — Flesch / sentence length / structure scan).
- `knowledge/marketing/marketing-sop.md` — SEO Checklist section.
