---
name: design
description: Visual concept, layout, type, color spec, format adaptation per channel. NOT product UI (that's NexusAI uiux).
company: BrandFlow
used_by: ["@brandflow.designer", "@brandflow.cmo"]
---

# Design Skill — BrandFlow

Visual craft for marketing output. Captions need visuals to land. Campaigns need a look. Brands need consistency.

Different from `@nexusai.skills/uiux` — that's product UX. This is **marketing visual**: campaigns, social, ads, landing imagery.

Inherits BrandFlow SOUL (creative-confident, slightly playful when it serves). I produce **specs**, not rendered files — Fathur or a tool renders.

## When to Use

- Visual concept for a campaign / post / ad.
- Layout spec (composition, hierarchy, spacing).
- Type spec (font, size, weight, line-height).
- Color spec (palette, contrast, brand alignment).
- Asset list (photos, illustrations, icons, charts needed).
- Format adaptation (IG square → IG story → LinkedIn banner → Twitter card).

## Default Approach

1. **Read copy + brief together.** Visual serves message, not the other way around.
2. **Identify the focal point.** What does the eye land on first?
3. **Build hierarchy.** Focal → secondary → tertiary. Three levels max.
4. **Strip.** Anything that doesn't earn its place is removed.
5. **Adapt per format.** What works on IG square fails on IG story. Spec both.
6. **Check accessibility.** Body text contrast > 4.5:1.

## Rules

1. **Less > more.** Crowded design is failed design.
2. **Whitespace is a design element.** Don't fill empty space "because it's empty".
3. **Type hierarchy is non-negotiable.** Three sizes (heading / body / caption) minimum.
4. **Color = role.** Each color has a job (primary action, accent, error, etc.) — not "this looks pretty".
5. **No "make logo bigger" or "add more text"** unless brief explicitly asks. Usually wrong.
6. **Brand consistency** > novelty. Recognition matters.

## Output Format

For visual concept:
```
[CAMPAIGN]      What this serves
[CHANNEL]       IG / LinkedIn / Email / etc
[FORMAT]        Square / story / banner / etc + dimensions
[VISUAL CONCEPT]
   - Focal point: <what eye lands on first>
   - Secondary: <where it leads>
   - Tertiary: <CTA / supporting>
[COMPOSITION]   Layout described (or sketched in text/ascii)
[TYPE]
   - Heading: <font, size, weight, color>
   - Body: <font, size>
   - CTA: <font, size, contrast>
[COLOR]
   - Primary: #HEX (role)
   - Accent: #HEX (role)
   - Background: #HEX (role)
[ASSETS NEEDED]
   - <photo / illustration / icon / chart>
   - Source: stock / commissioned / generated / existing
[ADAPTATIONS]   Brief notes for other formats
[CONSTRAINTS]   Brand guideline notes
```

For asset request (handed to Fathur or a renderer):
```
[ASSET]        What's needed
[PURPOSE]      What it serves
[STYLE]        Photo realism / illustration / icon / chart
[MOOD]         Emotional tone
[REFERENCE]    Similar examples (links if any)
[CONSTRAINTS]  Aspect ratio, color, must-include, must-avoid
```

For brand guideline update:
```
[ELEMENT]      What's being defined / updated
[OLD]          Previous spec (if any)
[NEW]          New spec
[RATIONALE]    Why this change
[ROLLOUT]      How existing assets get updated
```

## Channel Defaults

**Instagram square**: 1080x1080, focal point center or top-third.
**Instagram story**: 1080x1920, important content in middle 60% (avoid top/bottom UI).
**LinkedIn feed**: 1200x627 (link preview), 1080x1080 (image post).
**Twitter/X card**: 1600x900.
**Email header**: 600x300, dark-mode-aware (avoid pure white bg).

## Cross-Skill / Cross-Agent

- Copy that needs the visual → `@brandflow.copywriter` + `skills/content`.
- Where + when posted → `@brandflow.social`.
- Performance data on visual variants → `@brandflow.analytics`.
- Brand book / long-form guidelines → `@brandflow.writer`.
- Product UI (different domain entirely) → `@nexusai.frontend` + `skills/uiux`.

## What This Skill Does NOT Cover

- Actual PNG/JPG rendering (I produce specs; Fathur or a tool renders).
- Code-level UI (CSS, components) — that's `@nexusai.frontend`.
- Logo design from scratch — escalate to Fathur (brand identity decision).

## Reference

- `companies/brandflow/SOUL.md`
- `companies/brandflow/agents/designer.md`
- `knowledge/marketing/marketing-sop.md`


---

## Senior Patterns (Deep Dive) — Update 11

The senior-designer playbook for agency-context marketing visuals. Assumes the basics above are internalized; this is how you operate when one designer (or one freelancer) has to ship across 10 clients without breaking voice.

### 1. Visual Voice Profile Per Client

Parallel to the copy voice profile, each client has a **visual voice profile**:

```
companies/brandflow/clients/<client>/visual.md
```

Profile minimum:

```
[CLIENT]              <name>
[VISUAL ARCHETYPE]    Editorial / Documentary / Vibrant / Minimalist / Maximalist / Brutalist / Soft
[COLOR PALETTE]       Primary #HEX, secondary #HEX (×2-3), accent #HEX, neutral #HEX
[TYPOGRAPHY]          Heading family + weight, body family + weight
[GRID / LAYOUT]       12-col / 8-col / asymmetric / centered
[TREATMENT]           Photo style: stock / commissioned / illustrated / generated
[MOTIFS]              Recurring shapes, textures, compositional moves
[TABOOS]              Visual tropes the brand avoids (e.g. "no stock-photo handshake")
[REFERENCE BOARD]     5-10 of the brand's strongest past visuals
```

If the visual profile is missing, **escalate to `@brandflow.ceo`** for a brand kit session before producing. Designing without profile = inconsistency = the client notices the freelancer turnover.

### 2. Hierarchy: The 3-Level Rule

Every marketing visual has exactly three visual levels. Anything more = noise.

```
L1  Hero       — the focal point. Eye lands here first. ONE element.
L2  Support    — what the eye reads second. Connects L1 to action.
L3  Action     — CTA, logo, micro-info. Smallest, highest contrast color slot.
```

Test: cover any one of the three with your thumb. If the post still works at the other two levels, your hierarchy is solid. If covering L1 collapses the post, hierarchy is right (L1 is doing its job).

### 3. Composition Patterns by Format

| Format | Composition pattern | Why |
|---|---|---|
| IG square (1:1) | Center-anchor, headline top-third, CTA bottom-right | Mobile thumbnail readability |
| IG portrait (4:5) | Vertical stack, headline upper 40%, image middle, CTA bottom | Maximizes feed real estate |
| IG story / Reels cover (9:16) | Center middle 60%, top/bottom safe zones for UI | UI overlays eat top 250px and bottom 350px |
| LinkedIn feed (1.91:1) | Left-anchor headline, right-side imagery | Desktop-dominant audience reads left-to-right |
| LinkedIn carousel (1:1 or 4:5) | Slide 1 hooks; 2-N each = one idea; last slide = CTA | Carousel is a story, not a deck |
| Twitter/X card (1.91:1) | Bold headline left, brand mark right | Auto-cropped on mobile, ensure crop-safe |
| Email header (600×300) | Brand mark + 4-7 word headline. Dark-mode safe (no pure white bg) | Renders inconsistently across clients |
| YouTube thumbnail (16:9) | One face / object cropped tight + 3-5 word headline | Compete with 8 other thumbnails at small size |

### 4. Carousel Design Pattern (IG / LinkedIn)

The most-used agency format. Senior pattern:

```
Slide 1 — HOOK SLIDE
   Bold headline (≤8 words), high contrast, tease the payoff.
   No body text, no CTA on slide 1.

Slides 2-N — IDEA-PER-SLIDE
   One idea, one visual, one supporting caption.
   Numbered top-corner ("2/8") for orientation.
   Consistent template: same heading position, same color logic per slide.

Slide N-1 — SUMMARY / RECAP
   Single visual that consolidates the journey.
   Optional, recommended for educational carousels.

Slide N — CTA SLIDE
   Single CTA. Brand mark. No new info.
   Common patterns: "Save this post", "DM <keyword>", "Tap link in bio".
```

Common failure: 8 slides with 8 different layouts. Reader treats each as a separate post; thread breaks. **Lock layout in slide 2 and reuse through slide N-1.** Variation lives in content, not structure.

### 5. Color Roles (Not "Color Choices")

Each color in a layout has a *job*, not a *vibe*. Assign a role before placing pixels.

| Role | Slot | Contrast requirement |
|---|---|---|
| Primary action | CTA, primary button | ≥ 4.5:1 vs background |
| Brand identifier | Logo, brand mark, recurring accent | Recognizable across formats |
| Information layer | Headline text | ≥ 7:1 vs background (AAA) |
| Body text | Supporting copy | ≥ 4.5:1 vs background |
| Background | Surface | n/a (other roles measured against this) |
| Accent / decorative | Highlights, dividers, motifs | n/a (≤ 15% of total visual weight) |

If a designer adds a color without an assigned role, that color goes in the dustbin.

### 6. Typography Discipline

Three sizes minimum, max five. Anything more reads as a flyer, not a brand.

```
H1 / Headline       72-120pt    Heavy weight (700-900)
H2 / Subhead        36-48pt     Medium weight (500-600)
Body                18-24pt     Regular (400)
Caption / meta      12-14pt     Regular (400)
CTA / button        18-22pt     Bold (700), tracked +20-50
```

Line length:
- Headlines: 3-7 words / line, max 2 lines.
- Body: 45-75 characters / line.
- Mobile carousel body: 35-55 characters / line.

Pairing rules (when you must pick 2 typefaces):
- One serif + one sans = safe.
- Two sans of *clearly different proportions* = good (e.g. condensed display + humanist body).
- Two serifs = risky unless visibly different era.
- Display + script = wedding invitation territory; use only when brand archetype calls for it.

### 7. Accessibility as a Design Constraint (Not an Afterthought)

| Concern | Default |
|---|---|
| Body text contrast | ≥ 4.5:1 vs background |
| Headline contrast | ≥ 7:1 (AAA) for important headlines |
| Color-only signals | Banned — always pair with icon/text |
| Body text minimum size | 16px web / 18pt social-card |
| Animated content (Reels) | No flash > 3 Hz |
| Alt text for every published image | Mandatory; descriptive, not "image1.png" |

Mobile dark-mode check: open the visual on a phone, switch system to dark mode. Anything that becomes invisible (e.g. dark logo on now-dark background) gets fixed.

### 8. Asset Pipeline (Source → Derivative)

```
SOURCE (work surface)
   .fig / .ai / .psd / .key / .figma file
   Master file. Export-ready at multiple sizes.
   Lives in client folder, never in social scheduler directly.
        ↓
DERIVATIVES (per channel)
   IG square 1080×1080
   IG portrait 1080×1350
   IG story 1080×1920
   LinkedIn feed 1200×627
   LinkedIn carousel 1080×1080
   X card 1600×900
   ...
        ↓
PUBLISHED ASSETS
   .png / .jpg / .mp4
   Versioned filename: <client>-<campaign>-<format>-v<n>.png
```

Rule: **never edit a derivative directly.** Always go back to source, re-export. Otherwise drift between formats compounds.

### 9. The "Strip" Pass

Before submitting a visual, do a deletion pass:

1. Cover any non-L1 element with a square. Does the visual still work? If yes, that element is decorative — consider deleting.
2. Count total visual elements (text blocks, shapes, images, icons). If ≥ 7, you're probably crowded. Aim for 3-5.
3. For every element kept, you must articulate its role. "It looks nice" is not a role.

Senior visuals are **subtractive** — built by removing, not adding. Junior visuals are additive.

### 10. Layout Spec → Renderer Contract

Designer produces a **spec**, not a render. Renderer (Figma, Canva, generative tool, junior designer, freelancer) executes it. The spec must be unambiguous.

```
[ASSET]              brand-x-launch-ig-square-v1.png
[FORMAT]             1080×1080 px, RGB, sRGB profile
[BACKGROUND]         #0E1116 solid
[GRID]               24px margin, 8-col grid

[L1 — HEADLINE]
   Text:              "Cold email balik bukan karena copy."
   Font:              Inter Bold 96pt, tracking -2%
   Color:             #FFFFFF
   Position:          x=24, y=120, width=1032, max 2 lines

[L2 — SUPPORTING IMAGE]
   Source:            stock photo (Unsplash) — open laptop with notification
   Position:          centered horizontally, y=420, height=420
   Treatment:         duotone #2D6CDF / #0E1116, 0.85 opacity

[L3 — CTA + BRAND]
   CTA text:          "Read the breakdown →"
   CTA font:          Inter Medium 22pt
   CTA color:         #2D6CDF
   CTA position:      x=24, y=940
   Brand mark:        bottom-right, x=996-, y=996-, height=48

[ALT TEXT]            "Headline 'Cold email balik bukan karena copy' di atas foto laptop terbuka, dengan CTA 'Read the breakdown'."
```

Anything ambiguous = the renderer guesses, and the freelancer's guess is rarely the brand's guess. Tighten the spec.

### 11. Anti-Patterns Senior Designers Don't Ship

- **"Make logo bigger."** Almost always wrong; if you must enlarge, the layout is broken upstream.
- **Drop-shadow + outer-glow + inner-shadow on the same element.** Pick one effect, max.
- **Headline in 4 different colors.** Multi-color headline = no headline.
- **Text over busy photo with no overlay/scrim.** Always darken or scrim photos behind text.
- **Center-aligned everything.** Center is for short statements; left-align for body / lists.
- **"Pop" pursued via saturation.** Increasing saturation rarely helps; increasing contrast usually does.
- **Same visual recycled across 5 clients with logo swap.** Clients spot it. Treats your output as commodity. Bad business model.

### 12. Cross-Brand Senior Workflow (One Designer, Many Clients)

Pattern that scales for the agency:

1. **Master template per client** built once, locked.
2. **Variant slots** within the template (text, image, accent color) — those are all the freelancer touches.
3. **Output validator**: visual_lint check (spec-compliance) before publish.
4. **Voice + visual joint review** every Friday — designer + copywriter + QA review week's output cross-client to catch drift early.

### Reference

- `knowledge/marketing/social-platform-specs.md` — canonical dimensions and safe zones per channel.
- `knowledge/marketing/brand-voice-rubric.md` — visual voice capture parallels copy voice capture.
- `companies/brandflow/skills/designer/format-adaptation.md` (Update 11 deep skill).
- `tools/content_scheduler.py` — schedules pre-rendered assets, doesn't render them.
