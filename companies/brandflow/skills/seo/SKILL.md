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
