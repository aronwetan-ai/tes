---
name: crisis-playbook
description: Tiered crisis response playbook for BrandFlow's community manager — escalation, holding statements, recovery arc.
company: BrandFlow
agent_specific: "@brandflow.community"
parent_skill: community
used_by: ["@brandflow.community", "@brandflow.cmo", "@brandflow.ceo"]
---

# Crisis Playbook — BrandFlow Deep Skill

Agent-specific extension of `skills/community/SKILL.md`. Used by `@brandflow.community` (and CMO + CEO during escalation) when sentiment turns or a public incident lands in front of an owned/client account.

Inherits BrandFlow SOUL with **Boundary #4 at maximum intensity**. In crisis, the community manager's job is to **buy time, hold the line, and feed information up — not to publicly counter-argue.**

Core principle: **the first hour decides the next two weeks.** Slow, deliberate, escalated > fast, reactive, public.

---

## When to Use

- A public complaint goes viral on an owned/client account.
- Negative sentiment cluster forms (3+ similar complaints in <2h).
- A competitor / influencer / journalist publicly criticizes the brand.
- An employee, freelancer, or partner makes a public statement that reflects on the brand.
- A platform action (suspension, shadowban, content takedown) hits an account.
- Misinformation about the brand spreads.
- A factual error in published content is identified post-publish.

---

## Severity Tiers

```
TIER 1 — WATCH
   Signal: 1-2 mentions, mild negative sentiment
   Volume: low, contained to original audience
   Action: monitor, draft response if escalation likely

TIER 2 — CONCERN
   Signal: cluster of 3-5 similar complaints, sentiment shifting
   Volume: spreading within original audience, not yet beyond
   Action: brief CMO, prepare holding statement, pause scheduled posts

TIER 3 — ALERT
   Signal: viral cycle starting, accounts beyond original audience engaging
   Volume: spreading beyond originating community
   Action: brief CMO + CEO, hold-all-replies, draft public statement, escalate to Fathur for client accounts

TIER 4 — CRISIS
   Signal: large account quoting, journalist asking, legal language used
   Volume: cross-platform spread, possible mainstream pickup
   Action: Fathur + CEO own response; community manager goes silent on public-facing replies until briefed
```

Tier transitions are not always sequential — a journalist DM jumps directly to T3-T4. Don't slow-walk a T4 just because it didn't pass through T2.

---

## The First Hour (T1-T3)

```
0-5 min     DETECT
   - Identify the originating post / DM / mention.
   - Screenshot. Capture URL. Capture timestamp. Capture poster's account history (volume, posting pattern, follower count).
   - Note: do this even if it looks small. Documentation is cheap; reconstruction is expensive.

5-15 min    TRIAGE
   - Tier 1 / 2 / 3 / 4?
   - Is the underlying claim true, partly true, or false? (Don't draft until you know.)
   - Is this a single-account issue or a real cluster?
   - Brief CMO with the facts above. ONE message, not a stream.

15-30 min   HOLD
   - Stop scheduled posts to this client (pause queue in content_scheduler.py).
   - Stop drafting new replies until tier confirmed.
   - If Tier 2+: draft a holding statement (see templates below).
   - DO NOT post anything publicly yet.

30-60 min   ESCALATE
   - If Tier 3+: CEO + Fathur briefed.
   - If Tier 4: Fathur owns the response from here.
   - Position the team for next 24h: who watches, who drafts, who approves, who sends.
```

---

## Holding Statement Templates

Holding statements buy time without committing. They acknowledge, signal that you're listening, and avoid making promises you'll regret.

### T1 — Owned account, mild complaint, public response

```
Halo [@user] — makasih udah kasih masukan. Boleh DM aku detail-nya?
Aku bantu lihat dari sisi kami juga.
```

Notes: warm, claim-aware, moves to private channel for substance. Generic and safe. Boundary #4: still requires per-message approval.

### T2 — Cluster forming, public-facing acknowledgment

```
Kami baca semua masukan yang masuk. Tim sedang review minggu ini.
Update menyusul. Sementara waktu, kalau ada kasus spesifik — DM kami,
detail-nya kami pegang langsung.
```

Notes: acknowledges plurality, signals review without committing to outcome, opens private channel.

### T3 — Public statement, broader audience watching

```
Kami menerima masukan dari sebagian audiens minggu ini soal [topik singkat].
Beberapa hal yang valid kami catat dan kami review internal. Beberapa hal
lain perlu kami clarify dengan data, dan itu sedang kami siapkan.

Update menyusul dalam 48 jam.
```

Notes: acknowledges the issue exists, separates valid feedback from claims-needing-clarification, sets a return time. **Never longer than 48h on the timer** — unkept promises compound.

### T4 — Crisis-level, owned by Fathur/CEO

Don't draft. Hand to Fathur. The community manager's role is research support, not authorship.

---

## Apology Anatomy (When an Apology Is Owed)

Apologies are sometimes the right move and sometimes a trap. Senior judgment:

| Owed | Not owed |
|---|---|
| Factual error in published content | Mild dissatisfaction with subjective opinion |
| Process broken (delayed delivery, missed reply) | Audience didn't like the take |
| Insensitive language unintentional | Politically charged demand for stance |
| Real harm caused (financial, reputational, time) | Trolls performing offense |

Anatomy of a senior apology:

```
1. ACKNOWLEDGE THE SPECIFIC THING
   "Kami salah saat menulis [exact claim]. Yang benar adalah [correct claim]."

2. WHY IT HAPPENED (concise, no excuses)
   "Salah cek source, kami tidak verifikasi sebelum publish."

3. WHAT WE DID
   "Post sudah kami koreksi pukul 14:32. Catatan koreksi muncul di body."

4. WHAT WE'RE CHANGING
   "Mulai minggu depan setiap claim numerik melewati double-check QA."

5. (OPTIONAL) GENUINE THANK-YOU TO THE PERSON WHO FLAGGED
   "Terima kasih [@user] yang catch ini lebih dulu."
```

Anti-pattern apologies (avoid):
- **"Sorry if anyone was offended."** Not an apology — shifts blame to reader's reaction.
- **"We apologize for the confusion."** Avoids ownership of the cause.
- **Apology + counter-attack.** "Sorry, BUT actually..." erases the apology.
- **Repeated apology.** Over-apologizing reads as unstable. Once, clearly, then move.

---

## Misinformation / False-Claim Response

When a false claim about the brand circulates:

```
1. DON'T AMPLIFY
   Quote-replying with "this is wrong" boosts the false claim's reach.
   Reply directly only on the originating post; respond to the false claim everywhere else with a positive, fact-led counter-message that doesn't quote the lie.

2. CORRECT CALMLY
   "Faktual: [our position with evidence]. Kalau ada pertanyaan spesifik, DM kami."

3. DOCUMENT THE SPREAD
   Track which accounts amplified. Note for record. Don't engage them directly unless they ARE the source.

4. CONSIDER NOT RESPONDING
   Some lies die fastest in silence. If the originating account has <500 followers and the claim isn't spreading, ignoring is the strongest move.
```

Reference: `community/SKILL.md §5 — Drop the Rope Pattern.`

---

## Platform Action Response (Suspension, Shadowban, Takedown)

When a client account hits a platform-side restriction:

```
1. IDENTIFY
   - Which platform? Which action? (suspension / restriction / takedown / shadowban / appeal-required)
   - Which post / behavior triggered it?
   - When did it start?

2. DON'T POST FROM THAT ACCOUNT
   - Even normal-looking posts during a shadowban worsen it.
   - Pause scheduled posts immediately.

3. APPEAL VIA OFFICIAL CHANNEL
   - Use platform's appeal/support flow.
   - One concise appeal — don't spam.

4. PUBLIC SILENCE FROM THAT ACCOUNT
   - Don't address platform action publicly from the affected account.
   - If a public statement is needed, use a different owned account or website.

5. INFORM CLIENT (for client accounts)
   - Brief CMO immediately.
   - CMO briefs client, not community manager.

6. REVIEW WHAT TRIGGERED IT
   - Hashtag use, content pattern, posting cadence, third-party tool.
   - Document so the same trigger isn't repeated on other accounts.
```

Reference: `companies/nexusai/skills/security/SKILL.md` and `knowledge/security/opsec-multi-account.md` for prevention/account-hygiene patterns.

---

## The Recovery Arc (Days 1-30 Post-Crisis)

Crisis ≠ death. Most crises follow a recoverable arc if managed:

```
Day 0     Acknowledgment / holding statement.
Day 1-3   First substantive response: facts, change committed.
Day 4-7   Resume normal cadence, NOT victory-lap content.
              Keep it boring, useful, on-brand. Let the news cycle move on.
Day 8-14  Quiet improvement: ship the change you committed to.
Day 15-30 Casual reference (in passing) to what you learned, not as marketing.
Day 30+   Document internally: post-mortem in MEMORY.md. What
              triggered? What changed? What patterns to detect earlier?
```

Avoid:
- Day 1 hot-take retribution against critics.
- Day 4 gloating that "we're past it."
- Day 7 boost-spending on positive content (transparent, backfires).
- Day 30 promotional campaign that uses the crisis as origin story (cringe-y; reads as opportunism).

---

## Memory & Post-Mortem

After Tier 2+ crises, file a post-mortem in `companies/brandflow/MEMORY.md`:

```
[CRISIS]              Short title (e.g. "2026-05-14 false-claim about pricing")
[TIER]                T2 / T3 / T4
[TRIGGER]             What set it off
[FIRST DETECT]        When the team noticed
[ESCALATION TIMELINE] Hour-by-hour action
[STATEMENTS ISSUED]   Drafts + final published versions
[OUTCOMES]            What worked. What didn't.
[CHANGES MADE]        Process / content / tooling change since
[DETECTION SIGNAL]    What signal we'd watch for next time
[REFERENCE]           Screenshots / archived links
```

Six months later, this file is the senior-team's only honest record. Don't sanitize it.

---

## Communication Channels (Internal)

During a Tier 2+ crisis:

```
T1   Async note in #brandflow channel + flag CMO.
T2   Sync brief CMO. Async update CEO. Pause queue.
T3   Sync brief CMO + CEO. Schedule 30-min check-ins. Hold-all queue.
T4   Sync brief Fathur. CEO + CMO + Fathur own response from here.
     Community manager moves to information-support role.
```

Don't escalate to Fathur in 6 messages of incremental detail. Bundle: situation, severity, options, recommendation, what you need.

---

## Anti-Patterns During Crisis

- **First-hour public statement.** Almost always too early. Hold first; speak after triage.
- **Apologizing reflexively.** Don't apologize for things you weren't wrong about — sets a precedent that critics can extract apologies.
- **Counter-arguing in public.** No public arguments win the public. They feed it.
- **Silence past 48h with no holding statement.** Audience reads silence as guilt.
- **Mixed-message replies.** Two replies from the same account contradicting each other = blood in water.
- **Letting freelancers reply during a crisis.** Lock all reply access to one approver.
- **Treating the crisis as a content opportunity.** "Use this to grow our followers" — readers smell it.
- **Skipping the post-mortem.** Same crisis happens again in 4 months.

---

## Reference

- `companies/brandflow/skills/community/SKILL.md` (parent skill).
- `knowledge/marketing/crisis-comms-playbook.md` (Update 11 — broader strategic framing).
- `knowledge/marketing/brand-voice-rubric.md` (voice in crisis stays on-brand even when somber).
- Root SOUL — Boundary #4.
- `tools/social_monitor.py` (Update 11 — sentiment + cluster detection signals).
