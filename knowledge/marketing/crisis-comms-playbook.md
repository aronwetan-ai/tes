# Crisis Communications Playbook

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.cmo`, `@brandflow.community`, `@brandflow.ceo`, `@brandflow.qa`

---

## Why This File

Crisis comms is the highest-stakes, lowest-frequency work the agency does. Most months, nothing. Some quarters, one. When it happens, the first hour decides the next two weeks.

This file is the **strategic playbook**. The community-manager-level operational version lives at `companies/brandflow/skills/community/crisis-playbook.md`. They're complementary — read both before anything serious lands.

Core principle: **slow, deliberate, escalated > fast, reactive, public.** The instinct to "respond fast" usually compounds the crisis.

---

## What Counts as a Crisis

| Tier | Description | Examples |
|---|---|---|
| 1 — Watch | Single complaint, low spread, easily addressable | One DM about pricing confusion, one bad review |
| 2 — Concern | Cluster forming, sentiment shifting | 5 similar complaints in a day; mention volume up 3× |
| 3 — Alert | Viral cycle starting, beyond-original-audience accounts engaging | Mid-size account quote-tweets critically; thread gets 100+ engagements |
| 4 — Crisis | Cross-platform spread, mainstream-pickup possible, legal/reputation stakes | Journalist DM; influencer with 100k+ followers leading critique; legal language used |

Tier transitions are not always sequential. Journalist DM jumps directly to T3-T4. Don't slow-walk a T4 just because it didn't pass through T2.

---

## Decision Authority by Tier

| Tier | Who decides response | Who drafts | Who approves before send |
|---|---|---|---|
| T1 | `@brandflow.community` | community | CMO (per-message or batch) |
| T2 | `@brandflow.cmo` | community + CMO | CMO + Fathur |
| T3 | `@brandflow.ceo` + Fathur | CMO drafts; CEO refines | Fathur (mandatory) |
| T4 | Fathur owns; CEO supports | Fathur drafts; CEO + CMO support | Fathur (mandatory, per-message) |

Boundary #4 applies absolutely: nothing goes public on Fathur's name without explicit per-piece approval. Even a holding statement.

---

## The Crisis Framework — Five Stages

### Stage 1: Detect

```
Time-to-detect target:
   T1: <4h business hours
   T2: <2h business hours
   T3: <1h any time
   T4: <30min any time

Sources:
   - Native platform notifications
   - social_monitor.py sentiment scan (cluster + volume thresholds)
   - Mention searches (brand name, founder name, key product names)
   - Community manager observation
   - Inbound from Fathur / client / partner

Action:
   - Screenshot. Capture URL. Capture timestamps.
   - Identify originating account. Account history.
   - Identify spread vector (who amplified, when).
```

Documentation is cheap; reconstruction post-fact is expensive.

### Stage 2: Triage

```
Within first 30 minutes:

Q1. What is the underlying claim?
    - True / Partly true / False / Opinion-not-fact?

Q2. Is there harm to the brand or to a customer?
    - To brand: reputation / sales / partnership-relationship / platform standing?
    - To customer: financial / time / wellbeing / safety?

Q3. Who is the spreader?
    - Owned-channel critic (existing audience)
    - Bad-faith account (history of trolling / spam)
    - Competitor / poacher
    - Influencer / journalist
    - Coordinated cluster (multiple accounts, similar talking points)

Q4. What's the realistic spread trajectory?
    - Low: <500 immediate audience, no boost potential
    - Medium: 5k+ initial reach, possibility of mid-tier amplifier picking up
    - High: already amplified by 10k+ account or showing viral signals
    - Critical: mainstream / cross-platform / mass-media interest

Q5. Tier classification:
    - Q1+Q2+Q3+Q4 → tier number → escalate per authority table.
```

### Stage 3: Hold

```
Within first hour:

Action:
   1. Pause scheduled publishing for affected accounts (use content_scheduler.py)
   2. Pause community manager from drafting public-facing replies
   3. Designate reply-control owner (one person; not a committee)
   4. Brief decision-maker (per tier)
   5. If T2+: draft a holding statement (templates below)
   6. DO NOT post anything publicly yet

Why hold:
   - Bought time for accurate triage
   - Avoids contradictions if first reply turns out wrong
   - Signals to internal team that this is being handled, not improvised
```

### Stage 4: Respond

```
After triage + holding decision:

1. CHOOSE LEVEL OF RESPONSE
   - No public response (some crises die fastest in silence — typically T1, sometimes T2)
   - Quiet correction (DM the originating account, address privately)
   - Holding statement (acknowledge, signal review, set return time)
   - Substantive statement (acknowledge + facts + actions + change committed)
   - Apology (only when owed; see Apology Anatomy below)

2. DRAFT (per authority table)
3. INTERNAL APPROVAL
4. PUBLISH (per Boundary #4 — Fathur per-piece sign-off)
5. MONITOR (every 30-60 min for next 6 hours; every 2-4 hours for next 24)
```

### Stage 5: Recover

The recovery arc is days 1-30 post-crisis. See `companies/brandflow/skills/community/crisis-playbook.md` §Recovery Arc.

```
Day 0     Acknowledgment / holding statement
Day 1-3   Substantive response: facts, change committed
Day 4-7   Resume normal cadence; NOT victory-lap content
Day 8-14  Quiet improvement; ship the change committed to
Day 15-30 Casual reference (in passing) to what was learned
Day 30+   Internal post-mortem in MEMORY.md
```

---

## Holding Statement Templates

### T1 — Single complaint, public response

```
Halo [@user] — makasih udah kasih masukan. Boleh DM aku detail-nya?
Aku bantu lihat dari sisi kami juga.
```

Notes: warm, claim-aware, moves to private channel for substance.

### T2 — Cluster forming

```
Kami baca semua masukan yang masuk. Tim sedang review minggu ini.
Update menyusul. Sementara waktu, kalau ada kasus spesifik — DM kami,
detail-nya kami pegang langsung.
```

### T3 — Public statement, broader audience watching

```
Kami menerima masukan dari sebagian audiens minggu ini soal [topik singkat].
Beberapa hal yang valid kami catat dan kami review internal. Beberapa hal
lain perlu kami clarify dengan data, dan itu sedang kami siapkan.

Update menyusul dalam 48 jam.
```

**Never longer than 48h** on the timer. Unkept promises compound.

### T4 — Crisis-level

Don't draft as community/CMO. Hand to Fathur. Fathur owns voice + decision.

---

## Apology Anatomy

Apologies are sometimes right and sometimes a trap. Senior judgment:

### When apology IS owed
- Factual error in published content.
- Process broken (delayed delivery, missed reply, billing error).
- Insensitive language unintentionally used.
- Real harm caused (financial, reputational, time).

### When apology IS NOT owed
- Mild dissatisfaction with subjective opinion.
- Audience didn't like the take.
- Politically charged demand for stance.
- Trolls performing offense.

### Apology structure (when owed)

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

### Apology anti-patterns

- **"Sorry if anyone was offended."** Shifts blame to reader's reaction; not an apology.
- **"We apologize for the confusion."** Avoids ownership of cause.
- **Apology + counter-attack.** "Sorry, BUT actually..." — erases the apology.
- **Repeat apology.** Over-apologizing reads as unstable. Once, clearly, then move forward.

---

## Misinformation Response

When a false claim about the brand circulates:

```
1. DON'T AMPLIFY
   Quote-replying with "this is wrong" boosts the false claim's reach.
   Reply directly only on the originating post; respond to the false claim
   everywhere else with a positive, fact-led counter-message that doesn't
   quote the lie.

2. CORRECT CALMLY
   "Faktual: [our position with evidence]. Kalau ada pertanyaan spesifik, DM kami."

3. DOCUMENT THE SPREAD
   Track which accounts amplified. Note for record. Don't engage them
   directly unless they ARE the source.

4. CONSIDER NOT RESPONDING
   Some lies die fastest in silence. If the originating account has
   <500 followers and the claim isn't spreading, ignoring is the strongest move.
```

---

## Platform Action Response

When an owned/client account hits a platform-side restriction (suspension, shadowban, takedown):

```
1. IDENTIFY
   Which platform? Which action? Which post / behavior triggered it? When?

2. DON'T POST FROM THAT ACCOUNT
   Even normal-looking posts during a shadowban worsen it.
   Pause scheduled posts immediately.

3. APPEAL VIA OFFICIAL CHANNEL
   Use platform's appeal/support flow. One concise appeal — don't spam.

4. PUBLIC SILENCE FROM THAT ACCOUNT
   Don't address platform action publicly from the affected account.
   If a public statement is needed, use a different owned account or website.

5. INFORM CLIENT (for client accounts)
   Brief CMO immediately. CMO briefs client, not community manager.

6. REVIEW WHAT TRIGGERED IT
   Hashtag use, content pattern, posting cadence, third-party tool.
   Document so the same trigger isn't repeated on other accounts.
```

Reference: `companies/nexusai/skills/security/SKILL.md` and `knowledge/security/opsec-multi-account.md` for prevention/account-hygiene patterns.

---

## Communication Channels During Crisis

```
T1   Async note in #brandflow channel + flag CMO.
T2   Sync brief CMO. Async update CEO. Pause queue.
T3   Sync brief CMO + CEO. Schedule 30-min check-ins. Hold-all queue.
T4   Sync brief Fathur. CEO + CMO + Fathur own response from here.
     Community manager moves to information-support role.
```

Don't escalate to Fathur in 6 messages of incremental detail. Bundle: situation, severity, options, recommendation, what you need.

---

## Post-Mortem (Mandatory After Tier 2+)

File in `companies/brandflow/MEMORY.md` (or company `summary.md`):

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

## Anti-Patterns During Crisis

- **First-hour public statement.** Almost always too early. Hold first; speak after triage.
- **Apologizing reflexively.** Don't apologize for things you weren't wrong about — sets a precedent.
- **Counter-arguing in public.** No public arguments win the public. They feed it.
- **Silence past 48h with no holding statement.** Audience reads silence as guilt.
- **Mixed-message replies.** Two replies from the same account contradicting each other = blood in water.
- **Letting freelancers reply during crisis.** Lock all reply access to one approver.
- **Treating the crisis as content opportunity.** "Use this to grow our followers" — readers smell it.
- **Skipping the post-mortem.** Same crisis happens again in 4 months.
- **Public statement defending against bad-faith critique.** Drop the rope (see community/SKILL.md §5).

---

## Pre-Crisis Preparation (Best Done Before You Need It)

Quarterly hygiene that pays back during a crisis:

- [ ] Crisis decision-tree printed; team familiar with severity tiers.
- [ ] Holding statement templates approved at T2-T3 levels for quick use.
- [ ] Approval chain documented (who approves what during a Saturday afternoon T3?).
- [ ] Communication channels for Fathur during a crisis confirmed.
- [ ] Last 30 days of social monitoring — is sentiment baseline understood?
- [ ] Account hygiene status (cred_vault audit, freelancer access audit).
- [ ] Each high-stakes client has crisis contact + after-hours protocol.

---

## Reference

- `companies/brandflow/skills/community/crisis-playbook.md` — operational community-manager-level detail.
- `companies/brandflow/skills/community/SKILL.md` — Senior Patterns §6 crisis early warning signals.
- `companies/brandflow/skills/qa/SKILL.md` — Boundary #4 enforcement at QA layer.
- Root SOUL — Boundary #4.
- `tools/social_monitor.py` (Update 11) — sentiment + cluster + spread detection signals.
- This playbook integrates established crisis-comms thinking (Image Repair Theory, Situational Crisis Communication Theory). Content paraphrased for licensing compliance.
