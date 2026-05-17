# Search Intent Cheatsheet

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.seo`, `@brandflow.copywriter`, `@brandflow.writer`

---

## Why Intent Matters More Than Keyword

Modern search is intent-led. A page that targets the right keyword but the wrong intent will not rank — and even if it ranks briefly, won't convert.

A page that targets the right intent with adjacent keywords often outranks the keyword-matched but intent-mismatched competitor.

**Pick intent first. Pick keyword second.**

---

## Four Intent Types

### 1. Informational
**What the searcher wants:** definition, explanation, how-to, list, comparison-by-criteria.

**Query patterns:** "what is X" / "how to X" / "X examples" / "X vs Y" / "why X" / "X for beginners" / "X explained"

**Right format:** article, guide, tutorial, video, FAQ.

**Wrong format:** sales page, product detail page.

**Conversion potential:** low at first touch; build subscriber/follower; nurture downstream.

### 2. Navigational
**What the searcher wants:** a specific brand, site, or page.

**Query patterns:** "X login" / "X official" / "X brand name" / "X website"

**Right format:** brand homepage, login page, branded landing.

**Wrong format:** generic article on the topic — they wanted *the brand*, not info about the topic.

**Conversion potential:** mostly low (already a known seeker); rank protection matters.

### 3. Commercial Investigation
**What the searcher wants:** to compare options before deciding. Pre-purchase research.

**Query patterns:** "best X" / "X review" / "X vs Y" / "top X for Y" / "X alternatives" / "X pros and cons"

**Right format:** comparison post, listicle, review, alternatives breakdown.

**Wrong format:** single-product pitch (they're not ready to buy *yet*).

**Conversion potential:** medium-high; affiliate / lead-gen / soft-CTA performs well.

### 4. Transactional
**What the searcher wants:** to buy, sign up, download, take action.

**Query patterns:** "buy X" / "X price" / "X for sale" / "X subscription" / "X discount" / "X near me" / branded buy-intent

**Right format:** product page, pricing page, sign-up form, checkout-leading content.

**Wrong format:** long-form blog (slows decision; loses momentum).

**Conversion potential:** highest; direct CTA appropriate.

---

## Intent Identification Method

```
1. Search the keyword on Google (incognito + relevant region).
2. Look at the top 5 organic results' formats.
3. Pattern majority wins:
   - All blog/article = Informational
   - All listicle/comparison = Commercial Investigation
   - All product/pricing = Transactional
   - Brand-name + login + homepage = Navigational
4. If split (e.g. 3 articles + 2 product pages):
   - Mixed intent. Decide which 60% slice you want; design for that intent.
   - Don't try to serve both with one page.
5. Check SERP features:
   - Featured snippet → Informational + question-format opportunity
   - "People also ask" → Informational, FAQ schema bonus
   - Product carousel → Transactional dominates
   - Map pack → Local intent, often transactional
   - Video thumbnails dominant → Informational with video preference
```

---

## Mixed-Intent Keywords (How to Decide)

Some keywords are inherently mixed. Senior strategy:

| Pattern | Decision |
|---|---|
| 60% one intent, 40% other | Build for the 60% intent; address 40% in a brief section. |
| 50/50 split | Build TWO pages (separate URL each) — one per intent. |
| Top 3 same intent, positions 4-10 other intent | The top 3 have decided the dominant intent; build for that. |
| All 10 results are mixed but each individually one intent | Build for the format you can do best (your differentiation). |

---

## Intent → Page Structure

### Informational article structure

```
TITLE             "What is X" / "How to X" / "X explained"
INTRO             Direct answer in first 100 words (snippet-bait)
TOC               (long-form) Skim path
SECTIONS          H2 per major sub-question; H3 for nested
EXAMPLES          Concrete, with screenshots or data
CONCLUSION        Synthesis + soft CTA (subscribe, related read)
SCHEMA            Article + FAQ if applicable
```

### Commercial investigation structure

```
TITLE             "Best X for Y" / "X vs Y" / "X alternatives"
INTRO             Frame the comparison criteria
COMPARISON TABLE  At-a-glance scoreboard (most-wanted feature in modern search)
OPTION 1-N        Each: pitch + pros + cons + best-for + price/access
DECISION HELPER   "If you need X, pick A. If Y, pick B."
CONCLUSION        Recommendation + CTA to chosen option
SCHEMA            Article + Product / Review schema
```

### Transactional page structure

```
HERO              Headline + benefit + primary CTA
SOCIAL PROOF      Logos / testimonials / numbers
FEATURE × BENEFIT 3-5 max; FAB framework
PRICING           Visible, transparent, with comparison
FAQ               Top 5-8 objections preempted
CTA REPEAT        Bottom of page; sticky on mobile if appropriate
SCHEMA            Product + FAQ
```

### Navigational structure
Less variable. Brand homepage / branded landing. The job is being findable + signaling brand correctness.

---

## Intent + Funnel Match

| Intent | Funnel stage | Content type |
|---|---|---|
| Informational | TOFU | Educational article, video, podcast |
| Commercial Investigation | MOFU | Comparison, review, listicle, case study |
| Transactional | BOFU | Product page, pricing, signup form |
| Navigational | Brand-aware | Brand pages |

The funnel match is **why intent matters**. A TOFU visitor on a BOFU page doesn't convert; a BOFU visitor on a TOFU page bounces back to compare.

---

## Common Intent Mismatches (And Why They Fail)

| Wrote for | Actually serves | Why it fails |
|---|---|---|
| Sales page on "what is X" keyword | Informational searcher | Wants info, not pitch; bounces |
| Long article on "buy X" keyword | Transactional searcher | Wants to buy NOW; long article slows them |
| Generic article on "X login" keyword | Navigational searcher | Wants the actual login page; doesn't rank |
| Single-product pitch on "best X" keyword | Commercial Investigation searcher | Wants comparison; one option ≠ comparison |
| Listicle on "what is X" keyword | Informational searcher | Wants definition; listicle answers different question |

---

## SERP Feature Optimization (By Intent)

### Featured snippet (Informational)
- Provide direct answer in 40-60 words right after H1.
- Use list or paragraph format depending on what's currently winning the snippet.
- Question-format H2 increases capture chance.

### People Also Ask (Informational)
- Add FAQ section with 4-8 question-format H3s.
- Apply FAQ schema markup.
- Each answer self-contained in 50-100 words.

### Image / Video pack
- Strong cover image / thumbnail with alt text.
- Embed video with transcript on the page.
- Schema: VideoObject if applicable.

### Product carousel (Transactional)
- Schema: Product, Offer, Review.
- Pricing visible.
- Reviews/ratings visible.

### Map pack (Local)
- Google Business Profile claimed + populated.
- Consistent NAP (name/address/phone) across web.

---

## AI Overviews / Generative Search Behavior

Generative search (Google AI Overviews, Bing chat, Perplexity, ChatGPT browsing) increasingly intercepts traffic before it reaches a page. Compete by being the **citable source**:

- **Lead with direct answer** in first 100 words. AI overviews extract answer-style passages.
- **Bullet structure**: AI cites bullet lists more than prose paragraphs.
- **Discrete factual claims with sources**. Vague prose doesn't get cited.
- **FAQ section** with question-format H2/H3. Often quoted verbatim.
- **Recently updated content**: AI overviews favor freshness.

This is a directional bet, not a guarantee. Track AI citations as a separate metric from organic clicks.

---

## Anti-Patterns

- **Picking keyword by volume only.** Volume × wrong-intent = zero ranking.
- **Targeting "best X" with single-product page.** Misreads commercial-investigation intent.
- **One page targeting 5 intents.** Be one thing well, not five things badly.
- **Ignoring SERP features.** The SERP is the brief.
- **Writing for a 2008 algo.** Keyword-density + meta-keywords + exact-match URL: dead.
- **Generic AI-tasting prose.** E-E-A-T penalty; doesn't rank.
- **Forgetting the funnel match.** Right intent + wrong funnel stage = mismatch.

---

## Reference

- `companies/brandflow/skills/seo/SKILL.md` — full SEO skill including SERP reverse-engineering.
- `knowledge/marketing/marketing-sop.md` — SEO Checklist section.
- `knowledge/marketing/copywriting-frameworks.md` — frameworks for each intent type's content.
- This file paraphrases SEO industry consensus on intent classification (Google QRG-aligned). Content rephrased for licensing compliance.
