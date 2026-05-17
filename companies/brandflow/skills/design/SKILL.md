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
