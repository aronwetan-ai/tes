---
name: format-adaptation
description: Format-adaptation playbook for BrandFlow's designer — one master spec → all channel derivatives, brand-consistent.
company: BrandFlow
agent_specific: "@brandflow.designer"
parent_skill: design
used_by: ["@brandflow.designer", "@brandflow.cmo", "@brandflow.qa"]
---

# Format Adaptation — BrandFlow Deep Skill

Agent-specific extension of `skills/design/SKILL.md`. Used by `@brandflow.designer` whenever a piece needs to land on more than one channel — which is most pieces in agency work.

Inherits BrandFlow SOUL. **Repurposing is design, not export.** Junior designers re-export the same artwork at different sizes. Senior designers re-conceive composition per channel while preserving brand voice and the core message.

Core principle: **same idea, native execution.** A LinkedIn carousel is not a resized IG carousel. A Reels cover is not a cropped feed post. Every channel has a native grammar.

---

## When to Use

- A campaign ships across 2+ channels.
- A long-form blog needs social repurposing (carousel + Reels + thread).
- A client requests format expansion ("can we get this for LinkedIn too?").
- Onboarding a freelancer to the agency's adaptation method.
- Building a per-client master template kit.

---

## Master → Derivative Hierarchy

```
SOURCE (one per piece, work surface)
  Master Figma / AI / Sketch / Canva file
  Lives in: companies/brandflow/clients/<client>/assets/source/
        ↓
DERIVATIVES (per channel, exported for publish)
  Lives in: companies/brandflow/clients/<client>/assets/derivatives/<piece-id>/
  Files:
    ig-square-1080x1080.png
    ig-portrait-1080x1350.png
    ig-story-1080x1920.png
    linkedin-feed-1200x627.png
    linkedin-square-1080x1080.png
    x-card-1600x900.png
    youtube-thumb-1280x720.png
    blog-hero-1200x600.jpg
    email-header-600x300.png
    reels-cover-1080x1920.png
    ...
```

Rule: **never edit a derivative directly.** Always go back to source. Drift between formats compounds otherwise.

---

## Channel Spec Reference (Senior Defaults)

| Channel | Format | Dimensions (px) | Safe zone | Min font (body) | Notes |
|---|---|---|---|---|---|
| Instagram feed (square) | 1:1 | 1080×1080 | full canvas | 18pt | Most universal feed format |
| Instagram feed (portrait) | 4:5 | 1080×1350 | full canvas | 18pt | Maximum feed real-estate |
| Instagram story | 9:16 | 1080×1920 | center 60% (top 250 + bottom 350 = UI) | 24pt | UI eats edges; never put critical text there |
| Instagram Reels cover | 9:16 | 1080×1920 | center 60% | 36pt | Single hook word/phrase only |
| Instagram carousel slide | 1:1 or 4:5 | matches feed | full canvas | 18pt | Lock layout pattern across slides |
| LinkedIn feed image | 1.91:1 | 1200×627 | full canvas | 18pt | Desktop-first, left-anchored composition |
| LinkedIn square post | 1:1 | 1080×1080 | full canvas | 18pt | Increasingly common for slides |
| LinkedIn carousel slide | 1:1 or 4:5 | matches feed | full canvas | 18pt | Document-PDF format; readable on desktop |
| X / Twitter card | 1.91:1 | 1600×900 | center crop on mobile | 22pt | Auto-cropped; design crop-safe |
| TikTok video cover | 9:16 | 1080×1920 | center 60% (UI eats top + bottom) | 36pt | Single hook word/phrase |
| YouTube thumbnail | 16:9 | 1280×720 | center 80% (some clients show timestamp overlay) | 36pt | Compete with 8 thumbnails at small size |
| Email header | 2:1 | 600×300 | full canvas | 18pt | Dark-mode safe; no pure-white bg |
| Blog hero | 2:1 | 1200×600 | full canvas | 18pt | Loads first; CWV-conscious file size |
| Pinterest pin | 2:3 | 1000×1500 | full canvas | 18pt | Vertical-first; long-life pinning |
| WhatsApp Status | 9:16 | 1080×1920 | center 70% | 24pt | Status UI variant |

Reference cheatsheet: `knowledge/marketing/social-platform-specs.md`.

---

## The Adaptation Decision Tree

```
Given a master concept, for each target channel:

1. AUDIENCE BEHAVIOR ON THIS CHANNEL?
   - Skim while commuting? (mobile vertical, ≤2s read)
   - Deep read at desk? (horizontal, longer copy block)
   - Sound-on / sound-off? (caption + visual self-sufficient)

2. NATIVE GRAMMAR?
   - IG feed: thumb stops on visual; text supports.
   - LinkedIn feed: headline-led; visual supports text.
   - Reels/TikTok: hook word + visual motion; caption secondary.
   - Email: brand mark + 4-7 word headline; image as accent.
   - Blog hero: atmospheric; less prescriptive; loads with article.

3. WHAT CARRIES THE HOOK?
   - Visual element (photo / illustration / chart)?
   - Headline text (typographic hook)?
   - Combination (photo + overlay)?

4. WHAT CAN BE CUT?
   Each derivative cuts something the master had. Decide what.

5. WHAT MUST BE ADDED?
   Each derivative may need something the master lacked
   (e.g., Reels cover needs a single hook word; blog hero may need atmosphere not data).
```

---

## Six Adaptation Patterns

### Pattern 1: Crop with Recomposition

Source: 1080×1080 IG feed.
Derivative target: 1200×627 LinkedIn feed.

NOT: stretch / squeeze / center-crop.
DO: re-anchor focal point to the left third (LinkedIn reads left-to-right on desktop), reduce visual elements (more whitespace), re-size headline up (LinkedIn audience reads at desk-distance).

### Pattern 2: Carousel → Reels Script

Source: 8-slide LinkedIn carousel, 1 idea per slide.
Derivative target: 30s Reels.

DO:
- Slide 1 hook → 1.5s opening visual + spoken hook.
- Slides 2-6 ideas → 5-6s each, on-screen text + voiceover.
- Slide 7 summary → optional; consider removing if pacing tight.
- Slide 8 CTA → final 3s; CTA on screen + spoken.

Result: same idea, native motion grammar.

### Pattern 3: Long-form blog → IG Carousel

Source: 1500-word article with 5 H2 sections.
Derivative target: 8-slide IG carousel.

DO:
- Slide 1: hook (article's strongest single claim).
- Slides 2-6: one H2 = one slide, distilled to a single insight per slide.
- Slide 7: summary visual (recap framework / list / before-after).
- Slide 8: CTA → "Read the full breakdown" (link in bio).

Don't:
- Try to fit all 5 H2 sections in 1 slide.
- Use blog headline verbatim as slide 1 (often too long for visual).
- Skip the visual recap (slide 7) — it's the save-bait.

### Pattern 4: Tweet thread → IG Story Series

Source: 7-tweet thread.
Derivative target: 7 IG story frames.

DO:
- Each tweet = one story frame.
- Add interaction stickers (poll / question / quiz) on 2-3 frames to break monotony.
- Final frame: CTA → "Tap link in bio for the full thread."

### Pattern 5: Customer Testimonial → 3 Channel Variants

Source: long testimonial quote.
Derivative targets: IG square, LinkedIn feed, X card.

| Channel | Visual treatment |
|---|---|
| IG square | Quote + headshot + brand frame; 1080×1080 |
| LinkedIn feed | Quote left-anchored, brand mark right; 1200×627 |
| X card | Punchline-only headline + small attribution; 1600×900 |

Same testimonial, three native compositions, one cohesive campaign.

### Pattern 6: Single Photo → Multi-Channel Cover

Source: photoshoot output (1 strong image).
Derivative targets: 5 channels.

DO:
- IG square: full image.
- IG portrait: extend top/bottom with brand-color bands.
- IG story: image center, top + bottom UI-safe.
- LinkedIn feed: crop horizontal, headline overlay left.
- X card: tight crop on subject's face/object, headline.

Rule: never over-stretch a photo. If the source image lacks horizontal real estate for a 1.91:1 crop, add intentional brand-color band; don't distort.

---

## Brand-Consistent Adaptation Rules

| Element | Hold across all derivatives | Allowed to vary per derivative |
|---|---|---|
| Brand color palette | Yes | No |
| Brand typography (heading + body family) | Yes | Size scales per format |
| Logo/brand mark | Yes (always present) | Position adapts to safe zones |
| Visual archetype (per `visual.md`) | Yes | No |
| Specific visual elements (photo / illustration) | Concept yes | Crop / re-frame yes |
| Headline copy | Yes (verbatim if possible) | Length-tightening allowed for shortest formats |
| CTA text | Concept yes | Phrasing adapts to channel norm |
| Composition | Concept yes | Re-anchored per channel grammar |

If you're varying things in the "Yes" column, you're drifting from brand kit. Reload `visual.md` and recheck.

---

## Adaptation Spec Template

When designing a multi-channel piece, the spec covers all derivatives:

```
[CAMPAIGN]              <campaign-id>
[PIECE]                 <piece-id>
[CLIENT]                <client>
[CORE IDEA]             1-line summary, ≤12 words
[VISUAL VOICE FILE]     companies/brandflow/clients/<client>/visual.md
[BRAND COLORS USED]     <list>
[BRAND TYPE USED]       <list>

[MASTER COMPOSITION]
   <describe the full master file at design-time grid>

[DERIVATIVES]

  [IG-SQUARE-1080×1080]
     L1 (hero): <element>
     L2 (support): <element>
     L3 (CTA): <element>
     headline: "<verbatim text>"
     CTA: "<verbatim text>"
     alt-text: "..."

  [IG-PORTRAIT-1080×1350]
     <same fields>

  [IG-STORY-1080×1920]
     <same fields, with safe-zone notes>

  [LINKEDIN-1200×627]
     <same fields, with horizontal recompose notes>

  ... per channel ...

[ASSETS NEEDED]
  - Photo: <description / source>
  - Icon set: <description>
  - Custom illustration: <description>

[DELIVERY DEADLINE]     <date>
[OWNER]                 @brandflow.designer
[REVIEW]                @brandflow.qa  (voice + brand alignment per visual.md)
```

The spec is what the renderer (Figma operator, Canva freelancer, generative tool) executes against. Anything ambiguous in the spec = the renderer guesses, and the freelancer's guess is rarely the brand's guess.

---

## Repurpose vs Re-Concept Decision

Not every channel needs the master idea adapted. Sometimes it's better to ship a *new* concept on the second channel.

```
REPURPOSE if:
  - Same audience consumes both channels
  - Idea has visual core (a photo, chart, visual moment) that travels well
  - Both channels share grammar (e.g., IG feed + LinkedIn feed both static-image-led)
  - Time/budget is tight

RE-CONCEPT if:
  - Audience differs significantly per channel (LinkedIn audience ≠ TikTok audience)
  - Source format's grammar doesn't translate (text-heavy article → 30s video)
  - Time/budget allows
  - The piece is high-investment (campaign launch, hero asset)
```

Senior judgment: don't auto-repurpose to all 5 channels because the brief said "publish everywhere." Some channels deserve native re-concept; others get repurposed. Document the decision per piece.

---

## QA Pass for Adaptations

Before shipping a multi-derivative piece, run the cross-channel check:

```
[ ] Open all derivatives side by side at preview size.
[ ] Confirm visual cohesion: at thumbnail size, do they read as the same campaign?
[ ] Confirm brand consistency: colors, type, logo treatment match across all.
[ ] Confirm headline parity: same idea expressed natively per channel.
[ ] Confirm CTA parity: equivalent action requested per channel.
[ ] Confirm safe zones: no critical text in UI-overlaid regions.
[ ] Confirm dark mode: open derivatives on dark-mode device; nothing disappears.
[ ] Confirm legibility: body text minimum size hit; contrast ≥ 4.5:1.
[ ] Confirm alt text: every derivative has descriptive alt text.
```

Reference: `companies/brandflow/skills/qa/SKILL.md` Senior Patterns — visual layer.

---

## Anti-Patterns Senior Format Adaptation Avoids

- **Stretch / squeeze to fit.** Always recompose; never distort.
- **Same composition exported at 5 sizes.** That's export, not adaptation.
- **Critical text in UI safe zones.** Story top/bottom or YouTube thumbnail edge.
- **Headline that fits IG square but breaks LinkedIn.** Plan headline length around the constraint format up front.
- **Inconsistent CTA across derivatives.** Same campaign, different action requested = audience confusion.
- **Brand mark scaling without re-balancing.** Logo at 5% on big canvas can look like 15% on small canvas — recheck post-adaptation.
- **Forgetting Reels/TikTok cover.** Cover is the thumbnail in feed; if it's blank or auto-grabbed, format underperforms.
- **Adapting the master before the master is approved.** Wastes work — adaptations should always follow approved master.

---

## Reference

- `companies/brandflow/skills/design/SKILL.md` (parent skill, especially §3 Composition Patterns by Format).
- `knowledge/marketing/social-platform-specs.md` (Update 11 — full canonical spec sheet).
- `companies/brandflow/skills/content/SKILL.md` (Repurposing Discipline §9 — copy-side parallel).
- `companies/brandflow/agents/designer.md` (agent SOUL).
