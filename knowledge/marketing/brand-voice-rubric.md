# Brand Voice Rubric

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.copywriter`, `@brandflow.qa`, `@brandflow.cmo`, `@brandflow.designer`

---

## Why This Rubric

Voice is the single biggest agency-scale failure mode. One copywriter for 10 clients, one freelancer for 5 clients — without a structured voice rubric, content drifts toward a homogenized "agency-default" voice within 60 days. Clients notice. Retainers churn.

This file is the **canonical voice-capture template** used at client onboarding and as the QA reference for `tools/brand_voice_lint.py`.

---

## Voice ≠ Tone

- **Voice** is the brand's permanent personality. Doesn't change post-to-post. Captures things like: which brand archetype, what vocabulary register, what kind of metaphors, what POV.
- **Tone** is voice's contextual expression. Same voice sounds different in a celebration post vs a crisis post. Tone shifts; voice doesn't.

This rubric captures voice. Tone is then a per-piece adjustment within voice's allowable range.

---

## The 8 Voice Dimensions

Score each dimension 1-10 along the bipolar axis. The 8 numbers form the brand's voice fingerprint.

### 1. Formality (1=very informal · 10=very formal)
Casual chat / familiar / colloquial ←→ Polished / structured / professional

### 2. Seriousness (1=very playful · 10=very serious)
Jokes / puns / banter ←→ Earnest / weighty / measured

### 3. Boldness (1=reserved · 10=very bold)
Cautious / hedged / careful ←→ Provocative / opinion-leading / takes-stance

### 4. Warmth (1=cool · 10=very warm)
Detached / clinical / business-like ←→ Affectionate / familial / personal

### 5. Energy (1=calm · 10=intense)
Quiet / measured / paced ←→ Punchy / urgent / animated

### 6. Density (1=spare · 10=dense)
Short sentences / spacious ←→ Long sentences / packed / layered

### 7. Authority (1=peer · 10=expert)
On-the-same-level / "we're figuring this out together" ←→ Authority-from-expertise / "we know this"

### 8. Playfulness (1=straight · 10=very playful)
Direct / no-frills ←→ Witty / unexpected / culturally-coded humor

---

## Voice Profile Template (Canonical)

```
=========================================
VOICE PROFILE: <client name>
=========================================

[STATUS]
   Captured:                YYYY-MM-DD
   Last refreshed:          YYYY-MM-DD
   Captured by:             @brandflow.<role>
   Validated by client?:    Yes / No (date)

[ARCHETYPE]
   Primary:                 <Sage / Hero / Outlaw / Lover / Caregiver / Ruler / Innocent / Explorer / Magician / Jester / Everyman / Creator>
   Secondary (optional):    <archetype>

[8-DIMENSION FINGERPRINT]
   Formality:               <1-10>
   Seriousness:             <1-10>
   Boldness:                <1-10>
   Warmth:                  <1-10>
   Energy:                  <1-10>
   Density:                 <1-10>
   Authority:               <1-10>
   Playfulness:             <1-10>

[VOCABULARY — DO USE]
   Words/phrases this brand uses naturally:
     - "teman-teman" (preferred for IG/community)
     - "founder" / "operator" (B2B-leaning identity)
     - "data-driven" (only when actually backed by data)
     - "playbook" / "framework" / "pattern" (educational confidence)
     - <list 15-25 phrases>

[VOCABULARY — DON'T USE]
   Words/phrases this brand never uses:
     - "guys" (too male-coded for this audience)
     - "dear" / "respected sir" (over-formal)
     - "literally" (overused)
     - "hustle" / "grind" (off-archetype)
     - "we'll be honest with you" (filler, condescending)
     - <list 10-20 phrases>

[POV]
   First-person plural ("we / kami") · First-person singular ("I / saya")
   · Brand voice ("BrandX believes")?
   Mixed — if mixed, when to use which:
     <rule>

[SENTENCE LENGTH PATTERN]
   Mostly short (8-15 words) · mixed · long (20+ words)
   Rhythm preference:
     <e.g. "alternate short and medium; rare long sentences for emphasis">

[EMOJI POLICY]
   None / sparingly (≤1 per post) / generously / channel-dependent
   Specific allowed: <list>
   Specific banned: <list>

[PUNCTUATION QUIRKS]
   Em-dashes:               yes / no / preferred for emphasis
   Ellipses:                yes / no / sparingly
   Exclamation:              <max per post>
   ALL CAPS:                 yes / no / single-word emphasis only
   Title case vs sentence case in headlines: <preference>

[CTA STYLE]
   Pattern preference:
     - Command ("Save this post.")
     - Invitation ("Save kalau berguna.")
     - Question ("Resonate? Comment 1 thing kamu coba.")
     - Direct offer ("DM 'AUDIT' for free 15-min.")
   Preferred:                <pattern>
   Off-limits:               <patterns>

[METAPHOR / ANALOGY VOCABULARY]
   Categories the brand naturally reaches for:
     - sports / athletic
     - cooking / kitchen
     - building / construction
     - nature / weather
     - tech / software
   Preferred:                <list>
   Off-limits:               <list>

[CULTURAL / LOCAL REFERENCES]
   Bahasa Indonesia / Bahasa campur English /
   English-only / Region-specific (Jakarta-leaning / nasional / etc.)?
   Preferred:                <pattern>
   Off-limits:               <regions/cultures the brand doesn't speak to>

[OFF-LIMITS TOPICS]
   - politics
   - religion
   - <competitor names>
   - <specific claims the brand can't legally make>
   - <other>

[REFERENCE EXAMPLES — STRONG]
   3-5 of the brand's best past posts (links + reasons):
     1. <link> — why it's strong: <reason>
     2. <link> — why it's strong: <reason>
     ...

[REFERENCE EXAMPLES — OFF-VOICE]
   2-3 examples of past posts that drifted off-voice (links + what was wrong):
     1. <link> — drift: <reason>
     ...

[VOICE TEST PROMPTS]
   Sample prompts to verify voice consistency. Pass = output reads like the
   brand. Fail = drift detected.

   Prompt 1: "Write a 2-line caption for IG announcing a free webinar."
     Reference output: <text>

   Prompt 2: "Write a LinkedIn post hook about [topic]."
     Reference output: <text>

   Prompt 3: "Draft a DM reply to a complaint about pricing."
     Reference output: <text>

[BOUNDARY #4 STATUS]
   This voice profile reflects which entity?
     - This client (publishing under client's name) ✓
     - Fathur personal voice (publishing under Fathur's name)
     - BrandFlow agency voice (publishing under BrandFlow)
   Approval-path implication:
     <e.g. "All output requires client per-piece approval">
```

---

## Voice Capture Process (How to Fill This Out)

### Step 1: Source materials
Gather:
- Last 30-50 of the brand's published posts (across channels).
- 5-10 of the brand's strongest performers (by engagement / save / share).
- 3-5 of the brand's weaker / off-voice performers.
- Founder interview transcript (if available).
- Existing brand book / style guide (if any).

### Step 2: Quantify
Score the 8 dimensions on the brand's strongest performers. Average if needed.

### Step 3: Extract vocabulary
Read 30 posts. Highlight every recurring phrase / word the brand favors. Cluster. Top 15-25 = "do use." Inverse (words conspicuously absent in their voice but common in industry) = "don't use."

### Step 4: Founder validation
Send the draft profile to the founder / brand owner. They confirm or correct. **Voice profile without founder validation is a hypothesis, not a profile.**

### Step 5: Write 3 voice-test reference outputs
Use the voice profile to write 3 small drafts. These become the regression-test references for `brand_voice_lint.py`.

### Step 6: Lock + version
Save to `companies/brandflow/clients/<client>/voice.md`. Refresh quarterly minimum.

---

## Voice Drift Detection

Voice drift is the most common, most insidious editorial failure across agencies. Detection signals:

| Signal | Implies |
|---|---|
| 30+ posts with same opening phrase | Pattern collapse → drift toward template |
| Vocabulary outside "do use" list appearing | Drift toward writer's own voice |
| Sentence length pattern shifting | Density fingerprint drifting |
| POV slipping ("we" → "I" inconsistently) | Voice inconsistency |
| Engagement rate falling on previously-strong format | Audience may be sensing drift |
| Freelancer turnover correlated with voice shift | New writer hasn't internalized profile |

`tools/brand_voice_lint.py` scores drafts against the locked voice profile and flags drift early. Reference: `companies/brandflow/skills/qa/SKILL.md` Senior Patterns §3.

---

## Visual Voice Parallel

Voice profile (this file) covers copy. **Visual profile** is a parallel concept covering type / color / composition / archetype on the visual side. Both live per client:

```
companies/brandflow/clients/<client>/
   voice.md       ← copy voice (this rubric)
   visual.md      ← visual voice (companies/brandflow/skills/design/SKILL.md §1)
   personas.md    ← audience side
```

Voice and visual must align — a Sage-archetype voice with Outlaw-archetype visuals = brand confusion.

---

## Common Voice Failures

- **Founder voice ≠ brand voice.** Founder talks one way casually but the brand's audience-facing voice is different. Capture brand voice from brand-channel posts, not from founder DMs.
- **Aspirational voice.** Profile reflects what the founder *wants* to sound like, not what works for the audience. Run an A/B; let the audience decide.
- **Voice without verbatim phrases.** "Casual but professional" is meaningless without specific phrases.
- **One profile, many sub-brands.** Each sub-brand needs its own profile.
- **Voice profile that contradicts brand archetype.** Pick archetype first, derive voice from it.
- **No off-limits list.** Without it, freelancers drift into territory the brand avoids.
- **No refresh.** Brand voices evolve; profiles must too.

---

## Reference

- `companies/brandflow/skills/content/SKILL.md` — voice capture is step 1 in copy production.
- `companies/brandflow/skills/qa/SKILL.md` — Senior Patterns §3 voice drift detection.
- `companies/brandflow/skills/design/SKILL.md` — visual voice profile parallel.
- `knowledge/marketing/persona-template.md` — audience-side fingerprint (used jointly with voice).
- `tools/brand_voice_lint.py` (Update 11) — automated voice-drift scoring against locked profile.
- This rubric integrates established brand-voice-thinking traditions (archetype work, voice scorecard methods). Content paraphrased for licensing compliance.
