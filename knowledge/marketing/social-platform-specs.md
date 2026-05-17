# Social Platform Specs Cheatsheet

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.designer`, `@brandflow.copywriter`, `@brandflow.social`, `@brandflow.qa`

---

## Why This File

Canonical spec sheet for the channels BrandFlow ships content to. Specs change at platform whim; treat this file as **the agency's frozen reference**, updated quarterly and on visible change. Always verify against the platform's own current docs before high-stakes campaigns.

This file paraphrases publicly-documented platform specs for the agency's working context. Content was rephrased for compliance with licensing restrictions.

---

## Instagram

### Feed image (square)
- Dimensions: 1080×1080 px
- Aspect: 1:1
- File: JPG/PNG, ≤30 MB
- Caption: up to ~2,200 chars; first ~125-140 chars visible before "more"
- Hashtags: up to 30 (use 5-10 relevant)
- Best post hours (general rule): 11:00-13:00 + 19:00-21:00 local time

### Feed image (portrait)
- Dimensions: 1080×1350 px
- Aspect: 4:5
- Same caption / hashtag constraints as square
- Tends to outperform square in feed reach (more vertical real estate)

### Feed image (landscape)
- Dimensions: 1080×566 px
- Aspect: 1.91:1
- Same caption / hashtag rules
- Less common; weaker reach than portrait/square

### Story
- Dimensions: 1080×1920 px
- Aspect: 9:16
- Safe zone: middle ~60% (top ~250 px and bottom ~350 px reserved for UI overlays — handle, profile sticker, reply box, share/CTA buttons)
- Duration: 15s per frame; longer videos auto-split
- Stickers (poll, question, quiz, location, hashtag, mention): use sparingly, 1-2 per frame max
- Lifespan: 24 hours unless saved as Highlight

### Reels
- Dimensions: 1080×1920 px
- Aspect: 9:16
- Cover image: critical; auto-generates if not set, often poor — always set custom cover
- Duration: 15-90 seconds typical; up to 90s gets full algorithmic treatment
- Hook: first 1-1.5 seconds decide retention curve
- Loop-friendly outro: rewatch boosts ranking
- Caption: 2,200 chars (same as feed); first ~75 chars visible

### Carousel
- Slides: 2-10
- Each slide: 1080×1080 (square) or 1080×1350 (portrait)
- Lock layout pattern across slides for visual cohesion
- Slide 1 = hook; slides 2-N = ideas; slide N = CTA
- Save rate is the carousel's success metric (not likes)

### Profile
- Profile picture: 320×320 px (rendered at smaller size)
- Bio: 150 chars
- Link: 1 (use Linktree-style hub if multi-link)

---

## LinkedIn

### Feed image post
- Dimensions: 1200×627 px (landscape) — used in link previews
- For native post images: 1200×1200 (square) or 1200×1500 (4:5 portrait) often perform better
- File: JPG/PNG, ≤5 MB
- Post text: up to 3,000 chars; first ~210 chars visible before "see more"
- Hashtags: 3-5 relevant (more dilutes; LinkedIn favors fewer than Instagram)
- Best post hours: weekdays 08:00-10:00 + 12:00-13:00 local time; weekends underperform

### Feed video
- Dimensions: 1920×1080 (16:9) or 1080×1080 (1:1) or 1080×1350 (4:5)
- Duration: up to 10 min (short-form 15-90s consistently outperforms)
- Captions: native captions strongly recommended (sound-off viewing dominates)

### Document carousel (PDF post)
- Dimensions per page: 1080×1080 (square) or 1080×1350 (4:5)
- Pages: up to ~300 (practical sweet spot 8-12)
- File: PDF only, ≤100 MB
- Often outperforms image post in B2B (saves + dwell)

### Article (LinkedIn long-form)
- Cover image: 1920×1080 px
- Length: 800-2,500 words typical; 1,200-1,500 sweet spot
- Distinct from posts; lives at /pulse/<slug>

### Profile
- Profile picture: 400×400 px
- Cover photo: 1584×396 px
- Headline: 220 chars
- About: 2,600 chars

---

## Twitter / X

### Tweet (text)
- Length: 280 chars (free); longer for paid Premium accounts
- Threads: chain via reply; first tweet must stand alone *and* tease the thread
- Hashtags: 1-2 max (more dilutes; ≥3 reads as spam)
- Best post hours: weekdays 09:00-11:00 + 14:00-15:00 local time; weekends slower

### Tweet (image)
- Single image: 1600×900 (1.91:1, mobile crop-safe) or 1080×1080 (1:1)
- Multi-image (up to 4): platform composes a grid; design crop-aware
- Alt-text: required field

### Tweet (video)
- Dimensions: 1280×720 (16:9) or 1080×1080 (1:1) or 1080×1920 (9:16)
- Duration: up to 2:20 (free) / longer (Premium)
- File: MP4, ≤512 MB

### Profile
- Profile picture: 400×400 px
- Header: 1500×500 px
- Bio: 160 chars

---

## TikTok

### Video
- Dimensions: 1080×1920 px
- Aspect: 9:16
- Safe zone: middle ~70% (top ~150 px and bottom ~480 px reserved for UI: handle, caption, hashtags, comment/share/like buttons, music ticker, follow button)
- Duration: 9-180 seconds (up to 10 min available; <60s typical for organic)
- Hook: first 1-1.5 seconds determine retention curve
- Caption: 2,200 chars; first ~75 chars visible
- Hashtags: 3-5 typical (more is fine; relevance > volume)
- Cover: critical; thumbnail-first scroll behavior

### Profile
- Profile picture: 200×200 px
- Bio: 80 chars

---

## YouTube

### Long-form video
- Dimensions: 1920×1080 (16:9 standard) or 3840×2160 (4K)
- Duration: 30s-12 hours (sweet spot for retention varies by genre)
- Title: ≤100 chars (first ~60 chars visible in most surfaces)
- Description: ≤5,000 chars; first 2-3 lines drive expand-rate
- Tags: ≤500 chars total
- Custom thumbnail: critical, 1280×720 px
- End screens / cards: drive retention to next video

### Shorts
- Dimensions: 1080×1920 px (9:16)
- Duration: ≤60 seconds
- Title + description: as long-form
- Vertical-only

### Channel
- Channel art: 2560×1440 px (safe zone 1546×423 px)
- Profile picture: 800×800 px

---

## Email (general best practice across major MTAs)

### Subject line
- Length: 35-50 chars optimal (mobile preview)
- Avoid: all-caps, multiple exclamations, excessive emoji (deliverability impact)
- Personalization: first-name token outperforms generic ~10-25% open rate (varies by list)

### Preheader
- Length: 50-90 chars
- Treat as extension of subject; not a generic "view in browser" line

### Body
- Length: 80-300 words (transactional / promo); up to 1,500 (newsletter)
- Width: 600 px desktop email-safe canvas
- Single CTA primary; secondary CTAs allowed but de-emphasized
- Dark-mode safe: avoid pure white BG, ensure logo legibility on dark surfaces
- Image-only emails: high spam risk; always pair with text

### Sender name + reply-to
- Sender name: brand or person; consistency matters more than cleverness
- Reply-to: monitored inbox (don't use no-reply if avoidable; reduces engagement)

---

## WhatsApp (status + business)

### Status
- Dimensions: 1080×1920 px
- Aspect: 9:16
- Safe zone: middle ~70%
- Duration: 30s per frame (text/image); video up to 30s per status
- Lifespan: 24 hours

### Business profile
- Profile picture: 640×640 px
- Catalog images: 1:1, 1024×1024 px

---

## Pinterest

### Pin (standard)
- Dimensions: 1000×1500 px
- Aspect: 2:3
- Vertical-first; horizontal pins underperform
- Title: ≤100 chars; description ≤500 chars
- Click-through to source URL (drives outbound traffic — pin economy is built on this)

### Idea pin (multi-page)
- Dimensions: 1080×1920 (9:16)
- Pages: up to 20
- More social, less outbound; weaker for traffic

---

## Blog (canonical SEO surfaces)

### Hero image
- Dimensions: 1200×600 px (2:1) or 1920×1080 (16:9)
- File: optimized JPG/WebP, ≤200 KB ideal (CWV impact)
- Alt text: descriptive, keyword-aware but not stuffed

### In-post images
- Width: 800-1200 px common; let CSS scale rather than embedding 4K assets
- Alt text + caption: both for accessibility + SEO

### Open Graph (preview when shared)
- og:image: 1200×627 px (1.91:1)
- og:title: ≤60 chars
- og:description: ≤155 chars

---

## Crop-Safe Composition Reference

For visuals shared across platforms with different aspect crops:

```
Compose to a 1080×1080 "core" canvas.
Add ±270 px top/bottom = 1080×1620 portrait-safe expansion.
Add ±300 px left/right = 1680×1080 landscape-safe expansion.

Critical content stays inside the 1080×1080 core.
Backgrounds/atmosphere extend to the expansion zones.
```

Result: one master file crops cleanly to 1:1 (IG square), 4:5 (IG portrait), 9:16 (Story/Reels/TikTok), 1.91:1 (LinkedIn / X card / OG), 16:9 (YouTube thumbnail) — all without distortion.

---

## Update Cadence

This cheatsheet is reviewed quarterly. On a verified visible change to a platform's feed/format/algorithm, update sooner.

Sources to verify against (when checking before a campaign):
- Each platform's own creator/business help center.
- Reputable industry trackers (search query specific to current quarter).
- Sample of 5+ peer-account current posts to verify reality matches docs.

---

## Reference

- `companies/brandflow/skills/design/SKILL.md` — composition patterns by format.
- `companies/brandflow/skills/design/format-adaptation.md` — master→derivative adaptation patterns.
- `companies/brandflow/skills/content/SKILL.md` — per-channel copy length defaults.
- `knowledge/marketing/marketing-sop.md` — channel-default voice/tone.
- This file paraphrases publicly-documented platform specs. Content was rephrased for compliance with licensing restrictions; verify against current platform documentation before high-stakes campaigns.
