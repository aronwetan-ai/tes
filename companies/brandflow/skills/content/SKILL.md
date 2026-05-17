---
name: content
description: Copywriting, captions, hooks, ad copy, articles, email body. Specialized for BrandFlow voice — sharp, audience-aware, hook-first.
company: BrandFlow
used_by: ["@brandflow.copywriter", "@brandflow.cmo", "@brandflow.writer"]
---

# Content Skill — BrandFlow

The craft. Words that stop the scroll, hold attention, and move action.

Inherits BrandFlow SOUL (creative-confident, audience-aware, sharp copy). NOT generic content production — this is brand-aware, channel-specific copy.

## When to Use

- Social caption (IG, LinkedIn, X, TikTok).
- Ad copy.
- Email subject + body.
- Landing page copy.
- Article / blog post.
- Sales page.
- Hook / headline writing.
- WhatsApp status / DM templates.

## Process

1. **Read brief twice.** Audience / goal / channel / tone / format / constraint.
2. **Visualize one specific person.** If you can't, brief is incomplete — escalate to `@brandflow.cmo`.
3. **Write 3-5 hook options.** Pick the strongest, save the rest for variants.
4. **Draft body.** One idea per paragraph. No filler.
5. **Write CTA.** Specific verb + specific outcome.
6. **Self-review** with checklist (below).
7. **Tag with metadata.**

## Frameworks (per `knowledge/marketing/marketing-sop.md`)

- **AIDA** — Attention, Interest, Desire, Action. Default for sales.
- **PAS** — Problem, Agitate, Solve. Default for problem-solving content.
- **BAB** — Before, After, Bridge. Default for transformation stories.

Pick by intent. Don't force a framework that doesn't fit.

## Hook Patterns

| Goal | Pattern |
|------|---------|
| Curiosity | "Saya kira X, ternyata Y." |
| Contrarian | "Semua orang bilang X. Itu salah." |
| Specific Number | "5 hal yang saya pelajari dari 100 launch." |
| Pain Point | "Pernah X? Kamu tidak sendirian." |
| Bold Claim | "Cara tercepat untuk X adalah Y." |
| Question | "Kenapa X selalu Y? Ternyata jawabannya..." |
| Story | "Tahun lalu saya gagal X. Inilah yang saya pelajari." |

Avoid: clickbait that body doesn't deliver on.

## Self-Review Checklist

Before submitting:
- [ ] Hook stops scroll in 3 seconds?
- [ ] Body keeps attention to the end?
- [ ] CTA clear, specific, single?
- [ ] Tone matches brief + channel?
- [ ] No clichés ("game-changer", "leverage", "synergy" — never).
- [ ] No hyperbolic unbacked claims ("the #1 best in the world").
- [ ] Typo / grammar check?
- [ ] Metadata block included?

## Output Format

For social / short-form:
```
[CHANNEL]   IG / LinkedIn / X / etc

[HOOK]
<line 1>
<line 2>

[BODY]
<copy>

[CTA]
<call to action>

[VARIATION 2 - different tone]
<full alternate version>

[META]
Audience    : <who>
Channel     : <where>
Goal        : <why>
Tone        : <how>
KPI         : <what's measured>
```

For long-form (blog / article):
```
[TITLE]      <primary keyword + benefit>
[INTRO]      100-150 words framing the problem
[BODY]       H2/H3 organized, skim-friendly
[CONCLUSION] Synthesis + CTA
[META]
SEO target  : <primary keyword>
Audience    : <who>
Tone        : <how>
KPI         : <what's measured>
```

## Per-Channel Defaults

**Instagram**: ≤150 words feed caption, 5-10 relevant hashtags, always close with CTA.
**LinkedIn**: hook in first 1-2 lines (cut-off matters), line break per 1-2 sentences, end with question.
**X / Twitter**: thread hook tweet stands alone, every tweet self-contained, CTA in last tweet.
**Reels / TikTok**: hook in first 1.5 seconds, loop-friendly outro, sound choice matters.

## Cross-Skill / Cross-Agent

- Visual to accompany copy → `@brandflow.designer` + `skills/design`.
- Where + when this gets posted → `@brandflow.social`.
- DMs / replies after publish → `@brandflow.community`.
- SEO version of long-form → `@brandflow.seo` + `skills/seo`.
- Performance data after launch → `@brandflow.analytics`.
- Brand consistency review → `@brandflow.qa` + `skills/qa`.

## What This Skill Does NOT Cover

- Visual / layout / type spec → `skills/design`.
- Real-time engagement responses → `skills/community`.
- SEO keyword research → `skills/seo`.
- Pure UI microcopy for product → `@nexusai.frontend` + `skills/uiux`.

## Reference

- `companies/brandflow/SOUL.md`
- `companies/brandflow/agents/copywriter.md`
- `knowledge/marketing/marketing-sop.md`


---

## Senior Patterns (Deep Dive) — Update 11

Below is the senior-copywriter playbook for agency-context work. It assumes you've internalized the basics above and now operate at the level of "this caption ships under a client's name; it has to land."

### 1. Voice Capture Before Writing (Multi-Brand Discipline)

You write differently for each client. Before drafting any piece for a client, load:

```
companies/brandflow/clients/<client>/voice.md
```

Voice profile minimum:

```
[CLIENT]              <name>
[ARCHETYPE]           <Sage / Hero / Outlaw / Lover / Caregiver / etc.>
[TONE COORDINATES]    Formal⇄Casual: 7/10 casual
                      Serious⇄Playful: 6/10 playful
                      Reserved⇄Bold: 8/10 bold
[VOCABULARY]          Words they use ("teman", "bestie", "founder", "homie")
[VOCABULARY — AVOID]  Words they would never use ("guys", "dear", "respected sir")
[SENTENCE LENGTH]     short / mixed / long
[POV]                 first-person ("aku/saya/we") / brand voice
[EMOJI POLICY]        none / sparingly / generously
[CTA STYLE]           command / invitation / question
[REFERENCE EXAMPLES]  3-5 of their best-performing past posts
[OFF-LIMITS TOPICS]   politics / competitor names / specific claims
```

If voice profile is missing or stale, **escalate to `@brandflow.ceo`** for capture session before drafting. Don't guess voice — guessing produces homogenized content that the client recognizes as "AI slop" within a week.

### 2. Hook Selection Decision Tree

Don't pick a hook by vibes. Pick by intent + audience + format.

```
What is this piece's job?
├─ STOP scroll (cold audience)
│   ├─ Specific number     ("5 hal yang…")
│   ├─ Contrarian opener   ("Semua bilang X. Salah.")
│   └─ Bold claim          ("Cara tercepat untuk Y adalah Z.")
├─ HOLD attention (warm audience, mid-funnel)
│   ├─ Pain-point match    ("Pernah X? Kamu tidak sendirian.")
│   ├─ Curiosity gap       ("Saya kira X, ternyata Y.")
│   └─ Question hook       ("Kenapa X selalu Y?")
├─ TELL story (brand-building)
│   ├─ Origin moment       ("Tahun lalu saya gagal X.")
│   ├─ Reveal-the-cost     ("Saya bayar Rp X untuk pelajaran ini:")
│   └─ Insider voice       ("Yang tidak pernah dibahas di workshop:")
└─ DRIVE action (bottom-funnel)
    ├─ Direct offer        ("Slot terakhir minggu ini:")
    ├─ Reverse risk        ("Tidak suka? 30 hari refund.")
    └─ Deadline            ("Tutup hari Jumat, 23:59.")
```

Reference: `knowledge/marketing/hook-patterns.md` for the full pattern library.

### 3. Cold/Warm/Hot Audience Calibration

| Audience temp | What they need | What dies |
|---|---|---|
| Cold (never heard of brand) | Hook that earns 1 second + value before any pitch | Direct CTA in first line |
| Warm (followed, not bought) | Proof + specificity + soft CTA | Generic "tap link in bio" |
| Hot (subscribed, purchased once) | Personal voice + new offer + urgency | Cold-style intro that re-explains the brand |

Misjudging temperature is the #1 reason copy "feels off". Ad copy on Meta is cold by default. Email to subscriber list is hot. Treat them differently even when promoting the same offer.

### 4. The "One Idea" Discipline

Every piece carries **one** idea. If you can't compress what this post is about into one sentence ≤ 12 words, the post is unfocused.

```
Bad:   "Tips marketing untuk founder, plus tools yang kami pakai, plus update produk minggu ini."
Good:  "Cold email balik bukan karena copy, tapi karena timing."
```

When stakeholders push back ("can we also mention the launch?"), respond: **"Ya — sebagai post terpisah."** Do not stuff. A stuffed post lands nothing.

### 5. Specificity Ladder (Climb Until It Lands)

Generic → Specific → Hyper-specific. Climb the ladder until the line stops sounding like a stock phrase.

```
L0  "Konten yang efektif"
L1  "Konten LinkedIn yang efektif"
L2  "Konten LinkedIn untuk founder B2B"
L3  "Konten LinkedIn untuk founder SaaS B2B yang baru raise seed"
L4  "Konten LinkedIn untuk founder SaaS B2B Indonesia yang raise seed Q1 dan butuh distribution sebelum Series A"
```

Most copy fails at L1. Senior copy lands at L3-L4. Specificity is what makes the reader feel "this is for me." Use it especially in hooks and personas.

### 6. CTA Hierarchy by Funnel Stage

| Stage | CTA verb | Example |
|---|---|---|
| TOFU (awareness) | save / share / follow | "Simpan post ini buat referensi minggu depan." |
| MOFU (consideration) | read / watch / download | "Baca breakdown lengkapnya di blog (link di bio)." |
| BOFU (decision) | book / buy / chat | "DM 'AUDIT' untuk free 15-min audit." |
| Retention | reply / refer / review | "Reply komentar ini dengan satu pertanyaan kamu." |

One CTA per piece — not "and also follow us, and check our blog, and DM us." Decision fatigue kills action.

### 7. Senior Self-Edit Pass (Beyond the Basic Checklist)

After the first draft, edit in this order:

1. **Cut the first sentence.** 8 out of 10 times it's a warm-up the reader doesn't need. Start at sentence 2.
2. **Find every "really," "very," "just," "actually,"** — delete. Filler dilutes punch.
3. **Read aloud.** Anywhere your tongue trips = the reader's eye trips. Rewrite.
4. **Check verb density.** Aim for active verbs > 60% of total verbs. Passive constructions ("is being done", "was made") signal flabby copy.
5. **Look for the second draft inside the first.** Often the third paragraph contains a sharper version of the hook. Move it up, delete the warm-up.
6. **One-pass voice check** against `companies/brandflow/clients/<client>/voice.md`. Replace any phrase that doesn't match.

### 8. Anti-Patterns Senior Copywriters Don't Ship

- **Hook-bait body-disappoint.** The hook promises X; body delivers Y. Reader feels tricked, never returns.
- **Stock phrases.** "In today's fast-paced world", "In a sea of content", "Let me tell you a story" — invisible the moment they land.
- **Three CTAs in three paragraphs.** Pick one.
- **Hashtag spam (>10 on IG, any on LinkedIn).** Looks desperate, sometimes triggers algorithmic suppression.
- **Emoji as punctuation.** ✨🚀💡 used to "make it pop" usually makes it weaker. Use emoji like a noun, not like a comma.
- **Fake personal story with no detail.** "Ada klien saya kemarin..." with no name, role, or timestamp. Reader smells fiction.
- **Overclaiming.** "100% guaranteed," "the best in Indonesia," "guaranteed to grow". Either prove it or cut it.

### 9. Repurposing Discipline (Same Story, 3 Formats)

One brief produces:

```
Long-form (LinkedIn/Blog)   1200-1500 chars / 800-1500 words
   ↓ extract the 3 sharpest insights
Mid-form (IG carousel)      6-8 slides, 1 idea per slide
   ↓ extract the single sharpest insight
Short-form (Reels/TikTok script)   15-30s, hook-payoff-CTA
   ↓ extract the punchline
Status / X tweet            1-2 sentences, standalone
```

Repurposing is NOT copy-paste. Each format demands a re-think of pacing, hook, and CTA. Same idea, native execution.

### 10. Output Template — Senior Brief-to-Draft

```
[BRIEF SUMMARY]   1 line capturing the job
[ONE IDEA]        ≤12 words
[AUDIENCE TEMP]   Cold / Warm / Hot
[VOICE PROFILE]   Path to client voice file consulted

[HOOK OPTIONS]    3 candidates, picked: <#>, reason: <why>

[DRAFT V1]        Full draft

[VARIATIONS]
  - Tone variant: <draft if brief asks for 2 tones>
  - Length variant: <draft if brief asks for short + long>

[CTA RATIONALE]   Why this specific CTA at this funnel stage

[SELF-EDIT NOTES] 2-3 things you cut and why

[METADATA]
  Audience    : ...
  Channel     : ...
  Goal        : ...
  Tone        : ...
  KPI         : ...
  Boundary #4 : Internal-only / Needs Fathur approval / Client-approval flow
```

### Reference

- `knowledge/marketing/copywriting-frameworks.md` (AIDA, PAS, BAB, 4U, FAB, StoryBrand).
- `knowledge/marketing/hook-patterns.md` (extended hook library).
- `knowledge/marketing/brand-voice-rubric.md` (voice profile capture template).
- `knowledge/marketing/persona-template.md` (audience definition template).
- `companies/brandflow/skills/copywriter/hook-library.md` (Update 11 deep skill).
- `tools/brand_voice_lint.py`, `tools/readability_check.py` (Update 11).
