# Landing Page Architecture — 8-Section Conversion Template

Versi: 1.0
Created: 2026-05-17
Owner: BrandFlow (`@brandflow.designer`) + NexusAI (`@nexusai.frontend`) cross-company
Source: Adapted from SUPERAGENT v2 m9.md
Replaces: NOTHING — reference template untuk handoff BrandFlow → NexusAI

---

## Purpose

Standardized 8-section conversion landing page architecture untuk:
- Marketing landing page (BrandFlow drives, NexusAI implements)
- Client-facing product page
- Sales conversion page

NexusAI `skills/uiux/SKILL.md` tetap pegang **product UI** (dashboard, internal tools, app screens). Cookbook ini fokus **marketing landing**.

---

## The 8 Sections

```
┌─────────────────────────────────────────┐
│  1. INTERRUPT     (above fold)         │
│     - headline + value prop + CTA      │
├─────────────────────────────────────────┤
│  2. PROOF                              │
│     - logos / testimonials / metrics   │
├─────────────────────────────────────────┤
│  3. PROBLEM                            │
│     - articulate the friction          │
├─────────────────────────────────────────┤
│  4. RESOLUTION                         │
│     - product/service presentation     │
├─────────────────────────────────────────┤
│  5. CAPABILITY                         │
│     - 3-6 key outcomes                 │
├─────────────────────────────────────────┤
│  6. EXCHANGE                           │
│     - 3 tiers (anchor on premium)      │
├─────────────────────────────────────────┤
│  7. OBJECTION                          │
│     - FAQ handling                     │
├─────────────────────────────────────────┤
│  8. FINAL SIGNAL                       │
│     - urgency + action directive       │
└─────────────────────────────────────────┘
```

---

## Section Specs

### 1. INTERRUPT (Above Fold)

```
Headline:     [Big bold problem-solution statement]
              Max 12 words, specific, outcome-focused
              ❌ "Welcome to our company"
              ✅ "Stop losing customers to slow checkouts"

Subheadline:  [Value proposition expansion]
              Max 25 words, who + what + why-now

CTA:          [Single primary action]
              Verb-led, specific outcome
              ✅ "Book free 15-min audit"
              ❌ "Learn more"

Visual:       [Hero image / video / animation]
              Shows the outcome OR product hero shot
```

### 2. PROOF (Trust)

Pilih minimum 1, maksimum 2:
- Client logos (>5 = credibility, <3 = jangan tampilkan)
- Testimonial (1-3 max, dengan nama + role + photo)
- Metrics ("Used by 500+ companies", "$2M revenue managed")

### 3. PROBLEM (Articulation)

```
Format:       1-2 paragraphs
Tone:         Empathetic, specific
Goal:         Reader thinks "yes, that's me"
Anti-pattern: Generic ("Many businesses struggle with...")
Better:       Specific ("Your team spends 8 hours/week on manual reports...")
```

### 4. RESOLUTION (Product)

```
Format:       1-2 paragraphs + visual
Goal:         Show how problem solves
Pattern:      Before / After / Bridge (BAB framework)
              "Before: chaos → After: clarity → Bridge: our solution"
```

### 5. CAPABILITY (Outcomes)

```
Format:       3-6 cards/list items
Goal:         Specific outcomes user will get
Pattern:      Verb + Specific outcome + Quantified benefit (if possible)

Example:
  ✅ "Generate weekly reports automatically — save 6h/week"
  ❌ "Powerful reporting features"
```

### 6. EXCHANGE (Pricing)

```
3 tiers always — anchor on PREMIUM (middle), not lowest

Layout:
┌──────────┬──────────┬──────────┐
│   Entry  │ Premium★ │   Pro    │
│  $29/mo  │ $99/mo   │  $299/mo │
│  Basic   │ Most     │  Custom  │
│  features│ popular  │  features│
└──────────┴──────────┴──────────┘

Premium star/highlight = drives 60-70% of selections.
```

### 7. OBJECTION (FAQ)

```
Format:       5-8 FAQ items, accordion or list
Pattern:      Address actual objection, not vanity question

Common objections to address:
- Price ("Why so expensive?")
- Trust ("How do I know this works?")
- Switching ("I already use [competitor]")
- Cancellation ("What if I want to cancel?")
- Timing ("I'll think about it")
```

### 8. FINAL SIGNAL (Closing CTA)

```
Headline:     Echo of #1 headline (variation OK)
Urgency:      Specific reason to act now (not fake urgency)
              ✅ "Cohort closes May 31, next opens August"
              ❌ "Limited time only!" (no specifics)
CTA:          Same as #1 (consistency)
```

---

## Implementation Stack (NexusAI handoff)

| Use Case | Stack | Reason |
|----------|-------|--------|
| Static marketing landing | HTML + Tailwind + Alpine.js | Fastest delivery, SEO-ready |
| Conversion-optimized | HTML + Tailwind + AOS.js | Scroll triggers for engagement |
| Application/SaaS landing | Next.js + Tailwind | SSR, dynamic content, app integration |
| Indonesian market | + Midtrans payment binding | Regional checkout |

---

## Performance Protocol (Mandatory)

```
✅ Assets:        WebP, lazy-loaded, dimensioned
✅ Typography:    System-ui or max 2 web fonts, preloaded
✅ Styles:        Tailwind purge enabled
✅ Scripts:       Defer/async, minimal payload
✅ Responsive:    Verified at 375px (mobile-first)
✅ Discovery:     Meta title + description + OG tags
✅ Speed:         < 3s first paint target
✅ Accessibility: Contrast 4.5:1 minimum, alt text on all images
```

---

## Mobile-First Always

Desktop = secondary viewport.

Build flow:
1. Mobile design first (375px width as canvas)
2. Tablet enhancement (768px)
3. Desktop expansion (1024px+)

NEVER reverse this. Mobile-as-afterthought = poor mobile UX.

---

## Reference

- Source: `update/v2/openclaw/skills/m9.md`
- Used by: `@brandflow.designer`, `@nexusai.frontend`
- Authority: `companies/nexusai/skills/uiux/SKILL.md` (product UI)
