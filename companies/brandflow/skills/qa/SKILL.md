---
name: qa
description: Content review for brand voice, accuracy, KPI fit, channel appropriateness — before publish.
company: BrandFlow
used_by: ["@brandflow.qa", "@brandflow.cmo", "@brandflow.community"]
---

# QA Skill — BrandFlow

Last-line review before content goes public. Different from product QA — this is editorial / brand QA.

Inherits BrandFlow SOUL. Boundary #4 awareness — this is the final check before content can reach Fathur for publish approval.

## When to Use

- Reviewing copy before submit to CMO.
- Reviewing visual + copy combo before scheduling.
- Reviewing community reply drafts.
- Reviewing campaign launch package.
- Reviewing brand-sensitive output.

## Review Checklist

**Brand voice**:
- [ ] Tone matches BrandFlow + client brand voice?
- [ ] Vocabulary appropriate for audience + channel?
- [ ] Doesn't sound like AI-generated cliché ("game-changer", "leverage", "synergy")?

**Accuracy**:
- [ ] Factual claims have sources?
- [ ] Numbers / statistics verifiable?
- [ ] Spelling / grammar / punctuation clean?
- [ ] Names / titles / dates correct?

**Channel fit**:
- [ ] Length appropriate for channel?
- [ ] Hashtag count reasonable for platform?
- [ ] Format works on target device (mobile vs desktop)?

**Strategic fit**:
- [ ] Hook earns the read?
- [ ] CTA clear, single, actionable?
- [ ] Audience targeting reflected in copy?
- [ ] KPI defined?

**Risk check**:
- [ ] No hyperbolic unbacked claims?
- [ ] No unintended controversy / sensitive language?
- [ ] No promises Fathur can't keep?
- [ ] Boundary #4: marked as "needs Fathur approval" if going public?

## Rules

1. **Distinguish blockers from nits.** Don't make every comment a blocker.
2. **State severity.** Blocker / Major / Minor / Suggestion.
3. **Suggest fix.** Don't just say "this is wrong" — propose specific replacement.
4. **Loop in domain owner** for issues outside editorial expertise (legal, technical, financial claims).
5. **Approve fast** once issues are addressed. Don't re-litigate.

## Output Format

For content review:
```
[VERDICT]      Approve / Approve with changes / Reject
[STRENGTHS]    What's solid (briefly)
[ISSUES]       Numbered, with severity:
   1. [Blocker] <issue> — <suggested fix>
   2. [Major] ...
   3. [Minor] ...
   4. [Nit] ...
[BRAND VOICE]  On-brand / off-brand / mixed (with example)
[BOUNDARY #4]  Internal / Needs Fathur approval before publish
[NEXT STEP]    Author revises / Send to CMO / Block for Fathur
```

For campaign launch QA:
```
[CAMPAIGN]     Name + scope
[ASSETS]       List of pieces being reviewed
[ISSUES PER ASSET]
   <asset 1>: <findings>
   <asset 2>: ...
[SYSTEMIC ISSUES]   Cross-asset patterns
[VERDICT]      Ready / Needs revision / Hold
```

For community reply review:
```
[REPLY]        Original draft
[CONTEXT]      Incoming message + sentiment
[ISSUES]       Tone / accuracy / Boundary #4
[REVISED DRAFT] Suggested rewrite (if needed)
[OK TO SEND?]  After Fathur per-message approval
```

## Cross-Skill / Cross-Agent

- Copy under review → `@brandflow.copywriter` (revisor).
- Visual under review → `@brandflow.designer` (revisor).
- Strategic fit question → `@brandflow.cmo`.
- Brand voice question → `@brandflow.ceo`.
- Community reply → `@brandflow.community`.
- Final publish approval → escalate to Fathur (Boundary #4).

## Reference

- `companies/brandflow/SOUL.md`
- `knowledge/marketing/marketing-sop.md`


---

## Senior Patterns (Deep Dive) — Update 11

The senior editorial-QA playbook for agency-context content review. Editorial QA at the agency reviews 40-100 pieces per week across 10+ clients. The hard part is **detecting drift early** — voice drift, factual drift, brand-cluster drift — before it lands in front of a client's audience.

### 1. Review Layers (Don't Skip)

Senior QA passes a piece through 5 layers in this order. Each layer is short; layers compound.

```
LAYER 1 — VOICE
   Does it sound like THIS client (per voice.md), not BrandFlow's house voice?
   Tools: brand_voice_lint.py + manual ear

LAYER 2 — FACTS
   Are all factual claims sourced or owned-knowledge?
   Are numbers verifiable? Names spelled correctly? Dates accurate?

LAYER 3 — BRAND
   Visual aligns with visual.md? Logo placement, color, type all per brand kit?
   No off-limits topic / vocab violations?

LAYER 4 — STRATEGY
   Hook earns the read? CTA single + clear?
   KPI defined? Audience targeting reflected in copy?
   Format right for the channel?

LAYER 5 — RISK
   No hyperbolic unbacked claims?
   No unintended controversy / sensitive language?
   No promises Fathur or client can't keep?
   Boundary #4 status set correctly?
```

Failure at Layer 1-2 = blocker. Failure at Layer 3-4 = major or minor depending on impact. Failure at Layer 5 = blocker until risk is owned by CMO/CEO.

### 2. Severity Calibration (Stop Treating Everything as Blocker)

Junior reviewers blocker-everything. Senior reviewers calibrate:

| Severity | Definition | Action |
|---|---|---|
| **BLOCKER** | Wrong client voice / factual error / brand-kit violation / Boundary #4 unmet / risky claim | Cannot ship. Author revises. |
| **MAJOR** | Strategy weakness (hook weak, CTA muddled), structural issue, voice drift on one phrase | Strongly recommend fix; document if shipped without |
| **MINOR** | Style nit, mild grammar, suboptimal but functional | Optional fix |
| **NIT** | Personal preference, not brand-supported | Mention, do not push |
| **SUGGESTION** | Idea for next piece, not this one | Document for future |

If everything is blocker, the team learns to ignore QA. Over-blocking = capability collapse.

### 3. Voice Drift Detection — Concrete Method

Voice drift is the most common, most insidious editorial failure across agencies.

Senior QA pass for voice:

```
1. Read the draft once, fast.
2. Read the last 5 published pieces from this client, fast.
3. Read the draft a second time. What jumps as inconsistent?
   - Vocabulary register shift (formal where it should be casual, etc.)
   - Sentence-length rhythm shift
   - POV shift ("we" vs "saya" vs brand voice)
   - Emoji density shift
   - CTA-style shift
4. Run brand_voice_lint.py — pulls automated drift scoring.
5. If drift is detected, point to the specific phrases. Don't say "feels off."
```

Drift on isolated phrases = MAJOR (fixable). Drift across the whole piece = BLOCKER (rewrite or push back to copywriter).

### 4. Fact-Checking Hierarchy

Per claim:

```
TIER 1 — Owned-knowledge (the brand's own data, directly verifiable)
   → Confirm with client / internal data. No external citation needed.

TIER 2 — Industry stats / public data
   → Required: source URL, source date, authority.
   → Reject vague "studies show", "experts say", "research suggests" without specific sources.

TIER 3 — Influencer / personality / public-figure quotes
   → Required: verbatim accuracy. Misquoting = legal + reputation risk.

TIER 4 — Predictive / forward-looking claims
   → Required: framed as opinion, prediction, or "we believe", not as fact.

TIER 5 — Numbers
   → Required: math checks. ("Revenue grew 300%" — from what to what?)
   → No ambiguity ("up to" / "as much as" must be backed; vague claims rejected).
```

Senior QA sniffs for unsourceable claims by reading every numeric or comparative phrase.

### 5. Cluster Drift Detection (Cross-Piece Patterns)

Reviewing one piece at a time misses cluster patterns. Weekly cross-piece review catches:

| Pattern | What it indicates |
|---|---|
| 5/10 weekly pieces start with same hook structure | Hook variety collapsing |
| 8/10 weekly pieces tag same audience phrase | Persona narrowing too far |
| Visual consistency drifting across last 14 days | Designer/freelancer turnover signal |
| Engagement rate falling on similar formats | Audience fatigue with format |
| 3+ pieces with similar fact pattern that may overlap legally | Compliance risk cluster |

QA conducts a Friday cross-cluster review per client (~30 min/client) and flags drift to CMO + author. This is **higher leverage** than per-piece nitpicking.

### 6. Approval-Path Discipline (Boundary #4)

Each piece's `boundary_4_status` is QA's responsibility to set correctly:

| Path | When |
|---|---|
| `draft_only` | Internal artifact; never goes public. |
| `awaiting_fathur` | Will publish under Fathur's name; needs Fathur per-piece approval. |
| `awaiting_client` | Will publish under a client's name; needs client per-piece approval (or pre-approved category). |
| `pre_approved_category` | Routine, signed-off category like "thank-you reply"; ship subject to category bounds. |
| `published` | Already live. (Set post-fact, not by QA.) |

QA REJECTS any piece where `boundary_4_status` doesn't match its destination. Mismatched status = high-risk pipeline state.

### 7. Senior QA Output Templates

For per-piece review:

```
[VERDICT]              Approve / Approve-with-changes / Reject

[STRENGTHS]            What's solid (briefly — 1-3 lines max)

[ISSUES]               Numbered with severity:
   1. [BLOCKER] Voice drift in line 4 ("guys" — client voice profile excludes this).
      Suggested: "teman-teman" (matches voice profile line 12).
   2. [MAJOR] Hook is generic ("Berikut tips marketing"). Suggest using L3+ specificity.
   3. [MINOR] Em-dash spacing inconsistent in line 8.
   4. [NIT] Could shorten paragraph 3.

[VOICE CHECK]          Pass / Drift on phrase X / Fail
[FACT CHECK]           All sourced / Missing source on claim X / Numerical error in line N
[BRAND ALIGNMENT]      On-kit / Drift on element X / Off-kit
[BOUNDARY #4]          draft_only / awaiting_fathur / awaiting_client / pre_approved_category
[NEXT STEP]            Author revises / Send to CMO / Block for Fathur
```

For weekly cross-piece review:

```
[CLIENT]               <client>
[PERIOD]               Mon DD - Sun DD
[PIECES REVIEWED]      <count>
[CLUSTER PATTERNS]
   - Hook variety: <observation>
   - Persona drift: <observation>
   - Visual consistency: <observation>
   - Format mix: <observation>
[STRENGTHS]
[CONCERNS]
[RECOMMENDATIONS]      For author / CMO / Fathur
```

For freelancer review (when external designer / writer ships):

```
[FREELANCER]           Name + scope
[ASSIGNMENT]           What they shipped
[QUALITY VS BRIEF]     Met / Partial / Off-brief (with examples)
[VOICE / VISUAL FIT]   On-brand / Drifted (specific examples)
[REVISION REQUESTS]    Numbered, blockers vs nits split
[FUTURE GUIDANCE]      Patterns to internalize for next assignment
[VERDICT]              Pay-and-iterate / Pay / Hold-until-revise / Reject
```

### 8. Common Editorial Failures (Senior-Eye Patterns)

Things that escape junior review:

- **Hook-bait, body-disappoint.** Hook promises specific, body delivers generic.
- **Fake personal story.** "Klien saya bilang..." with no specifics. Reader smells fiction.
- **Stat without context.** "47% improvement" — from what baseline, over what period?
- **Comparison without naming.** "Unlike most agencies..." — which agencies, what specifically?
- **Vague CTA dressed as specific.** "Learn more" / "Find out" — what does the reader actually do?
- **Off-brand vocabulary buried in middle paragraph.** Voice consistent at start + end, drifts in middle 200 words.
- **Visual focal point disagrees with copy hook.** Eye lands on one thing, copy talks about another.
- **Carousel where slide 1 hook doesn't promise what slide 8 CTA delivers.** Mid-funnel mismatch.

### 9. Approval Speed Discipline

Senior QA approves fast when issues are addressed. Don't re-litigate:

```
First review:  Be thorough. List blockers + majors + minors.
Second review (after revision): Check ONLY blockers + majors from first review. Don't add new minor critique unless severity blocker. Approve.
Third review (rare): Should never happen except for stage-skipping major changes.
```

Re-litigating each round = bottleneck = team learns to bypass QA. Bad.

### 10. Brand-Aware Approval Tier Per Client

Not every client's content needs the same QA depth. Tiering:

| Client tier | QA depth | Cycle time target |
|---|---|---|
| New (first 30 days) | Full 5-layer review per piece + cross-cluster weekly | 4h turnaround |
| Established (60+ days) | Full review per piece, lighter cluster review | 2h turnaround |
| High-trust (proven authors + voice locked) | Spot review (1 of every 3 pieces) + cluster weekly | 1h turnaround |
| Crisis-watch (post-incident) | Full review + double-sign-off (QA + CMO) | Scheduled around approval window |

CEO calibrates tier per client. QA executes per tier.

### 11. Anti-Patterns Senior QA Doesn't Ship

- **Approve-everything (no value-add).** Team learns QA is rubber-stamp.
- **Block-everything (false urgency).** Team learns to bypass QA.
- **Issue without suggested fix.** "This is wrong" without a path forward = friction without value.
- **Mixing personal preference with blocker.** "I'd say it differently" ≠ "this is broken."
- **Re-litigating fixed issues.** Once resolved, drop it.
- **Surface-level reads.** Skimming a 2000-word article in 60 seconds = missed drift.
- **Skipping cross-cluster review.** Per-piece review alone misses pattern-level drift.
- **Letting Boundary #4 status drift.** Most-frequent serious mistake — QA's job to enforce.

### Reference

- `knowledge/marketing/brand-voice-rubric.md` (voice profile structure).
- `knowledge/marketing/copywriting-frameworks.md` (strategic-fit reference).
- `tools/brand_voice_lint.py` (Update 11 — automated voice-drift scoring).
- `tools/readability_check.py` (Update 11 — readability + sentence rhythm).
- `companies/brandflow/skills/content/SKILL.md` Senior Patterns (the ideals being QA'd against).
