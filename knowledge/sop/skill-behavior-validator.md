# Skill: 3-Step Behavior Validation Loop

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** All agents, Operator  
**Trigger:** New SOUL section written, new behavior deployed, after UPGRADE  
**Frequency:** 2x/week (after new behavior, after upgrade)  
**Risk Level:** Low

---

## Purpose

Validate new agent behaviors through a 3-step iteration loop: small task → evaluate → correct permanently. Ensures behaviors are correct before they become habitual.

---

## Prerequisites

- New behavior written (SOUL.md section, skill file, or memory entry)
- Agent ready to execute tasks
- Evaluation criteria defined (5 dimensions)
- Access to SOUL.md, memory files, and skill directory

---

## Steps

### Step 1: Task Kecil Dulu (Start Small)

Begin with read-only or low-risk action. Build trust before high-stakes tasks.

**Low-risk task examples:**

```
Read-only:
  - Check balance / status
  - Read repository / logs
  - Summarize email / discussion
  - Research without action

Low-risk write:
  - Create draft (not publish)
  - Write to memory (not production config)
  - Generate report (internal only)
  - Test in staging (not production)
```

**Rule:** Don't give high-stakes tasks (money, public publish, irreversible) until behavior validated on safe tasks.

**Example for new agent:**

```
Task 1 (Day 1): Read NexusAI repository status
  → Expected: List repos, branches, recent commits
  → Risk: None (read-only)

Task 2 (Day 2): Summarize last week's Telegram messages
  → Expected: 3-5 key decisions, action items
  → Risk: Low (analysis only, no action)

Task 3 (Day 3): Draft a blog post (don't publish)
  → Expected: 500-word draft, ready for review
  → Risk: Low (draft only, not published)

Task 4 (Day 4): Create a GitHub branch and commit
  → Expected: Branch created, commit pushed to non-main
  → Risk: Low (non-main branch, reversible)

Task 5 (Day 5): Publish to staging environment
  → Expected: Deploy successful, no errors
  → Risk: Medium (staging only, not production)
```

---

### Step 2: Nilai Hasilnya (Evaluate Results)

Assess 5 dimensions of behavior:

| Dimension | What to Check | Good Sign | Bad Sign |
|-----------|---------------|-----------|----------|
| **Bahasa & Tone** | Register, emoji, formality | Matches context (aku/kamu for internal, formal for external) | Too formal/casual, wrong emoji, inconsistent |
| **Level Otonomi** | Does agent ask or just do? | Proceeds autonomously for Tier 1, asks for Tier 3 | Always asks for Tier 1, proceeds without asking for Tier 3 |
| **Tool Selection** | Does agent pick right tool? | Uses wallet tool for crypto, GitHub tool for code | Uses web search for wallet balance, wrong tool |
| **Verifikasi** | Does agent check results? | Verifies tx hash, build status, endpoint test | Says "should work", doesn't verify |
| **Error Handling** | How does agent handle failures? | Retries with backoff, escalates with info | Gives up silently, or retries infinitely |

**Evaluation checklist:**

```
Task: [task name]
Date: [YYYY-MM-DD]

Bahasa & Tone:
  ✓ Register appropriate for context
  ✓ Emoji usage (if any) appropriate
  ✓ Formality level matches expectation
  ✓ No unnecessary verbosity

Level Otonomi:
  ✓ Tier 1 tasks: proceeded without asking
  ✓ Tier 3 tasks: asked for confirmation
  ✓ Tier 2 tasks: logged decision + proceeded
  ✓ No over-caution (refusing Tier 1)
  ✓ No over-confidence (skipping Tier 3)

Tool Selection:
  ✓ Correct tool for task type
  ✓ Tool parameters correct
  ✓ Fallback tool used if primary unavailable
  ✓ No tool misuse

Verifikasi:
  ✓ Agent checked output before reporting
  ✓ Verification method appropriate
  ✓ Result matches expectation
  ✓ No "should work" without proof

Error Handling:
  ✓ Retry logic present (if applicable)
  ✓ Escalation clear and informative
  ✓ No infinite loops
  ✓ Fallback options tried before giving up

Overall: PASS / NEEDS_WORK
```

---

### Step 3: Koreksi Permanen (Save Corrections)

Every correction MUST be saved. Unsaved corrections repeat in next session.

**Save location depends on scope:**

```
General rule (applies everywhere):
  → Save to SOUL.md (Section 6: Default Disposition)
  → Example: "Asumsi user tahu apa yang dilakukan. Tanya konteks, jangan refuse."

Specific preference (this context only):
  → Save to memory (MEMORY.md or memory/global.md)
  → Example: "[BEHAVIOR] @nexusai.ceo prefers short answers, no preamble"

Workflow that works (5+ tool calls):
  → Save as skill file (companies/[co]/skills/[domain]/[skill].md)
  → Example: "Skill: Deploy to VPS" with 7 steps

Recurring pattern (same task 2+ times):
  → Save as skill file
  → Example: "Skill: Weekly system audit" with 4 layers
```

**Correction entry format:**

```markdown
## [BEHAVIOR CORRECTION — YYYY-MM-DD]

**Agent:** @company.agent  
**Task:** [task name]  
**Finding:** [what was wrong]  
**Root Cause:** [why it happened]  
**Fix:** [what to change]  
**Scope:** [general rule / specific context / workflow / pattern]  
**Saved To:** [SOUL.md / memory / skill file]

### Before
[old behavior]

### After
[new behavior]

### Verification
[how to verify fix works]
```

**Example:**

```markdown
## [BEHAVIOR CORRECTION — 2026-05-18]

**Agent:** @nexusai.ceo  
**Task:** Read repository status  
**Finding:** Agent provided 3-paragraph explanation when 1 sentence would suffice  
**Root Cause:** No rule about answer length in SOUL.md  
**Fix:** Add "Default Disposition" section with: "Answer concisely. Short answers > long explanations. No preamble."  
**Scope:** General rule (applies to all tasks)  
**Saved To:** companies/nexusai/SOUL.md (Section 6)

### Before
"The NexusAI repository contains multiple branches organized by feature. The main branch is the production branch. We have develop, staging, and several feature branches. Recent commits include..."

### After
"NexusAI repo: main (prod), develop, staging, 3 feature branches. Latest: merged auth-refactor (2h ago)."

### Verification
Next task: ask agent to summarize same info. Should be 1-2 sentences.
```

---

## Behavior Pathology — Tanda Perlu Diperbaiki

### Terlalu Pasif (Too Passive)

**Gejala:** Agent always asks for permission, even for Tier 1 tasks.

**Root Cause:** SOUL.md says "wajib izin" without explaining when to proceed autonomously.

**Fix:** Add "Fully autonomous" section with explicit examples:
```
Fully autonomous (no permission needed):
  - Read any file / check status
  - Summarize information
  - Draft content (not publish)
  - Create branch (not main)
  - Test in staging (not production)
```

---

### Terlalu Agresif (Too Aggressive)

**Gejala:** Agent proceeds without confirmation for Tier 3 tasks.

**Root Cause:** SOUL.md doesn't explain when to ask.

**Fix:** Add "Wajib konfirmasi" section with explicit examples:
```
Wajib konfirmasi (always ask first):
  - Publish to public surface
  - Transfer money to new address
  - Delete files / force push
  - Change production config
  - New client / partnership
```

---

### Terlalu Verbose (Too Wordy)

**Gejala:** Long explanations for simple questions.

**Root Cause:** No rule about answer length.

**Fix:** Add to Default Disposition:
```
Answer length:
  - Simple question → 1-2 sentences
  - Complex question → 3-5 sentences + code/examples
  - No preamble ("Let me explain..."), no filler
```

---

### Salah Konteks (Wrong Context)

**Gejala:** Agent brings context from different project/company.

**Root Cause:** SOUL.md too generic, no domain boundary.

**Fix:** Add domain-specific rules or memory per project:
```
[CONTEXT] NexusAI agents focus on: software, DevOps, infrastructure
[CONTEXT] BrandFlow agents focus on: marketing, content, brand
[CONTEXT] Crypto agents focus on: research, analysis, market data
```

---

### Over-Cautious (Refuse/Lecture)

**Gejala:** Agent refuses requests or gives warning paragraphs.

**Root Cause:** No Default Disposition in SOUL.md.

**Fix:** Add:
```
Default Disposition:
  - Assume user knows what they're doing
  - Ask context if request seems odd, don't refuse
  - One clarifying question > one warning paragraph
  - Push back on bad ideas with technical reasons, not moral judgment
```

---

## Iteration Cadence

| Phase | Duration | Focus | Frequency |
|-------|----------|-------|-----------|
| **Onboard** | 3-5 days | Task kecil, koreksi intensif, simpan banyak | Daily tasks + evaluation |
| **Stabilize** | 1-2 weeks | Task normal, koreksi berkurang, behavior menetap | 2-3x per week |
| **Mature** | Ongoing | Koreksi jarang, mostly upgrade/expand | 1x per week or on-demand |

---

## When To Run Testing

- [ ] After SOUL.md baru ditulis atau di-update major
- [ ] After credential/akses baru diberikan
- [ ] After behavior baru ditulis (dari template)
- [ ] After upgrade (UPGRADE.md / UPGRADE2.md)
- [ ] After bug yang terkait agent behavior
- [ ] Onboarding new agent (3-5 day cycle)

---

## Verification

- [ ] Task kecil executed successfully
- [ ] All 5 dimensions evaluated
- [ ] Findings documented
- [ ] Corrections saved to appropriate location (SOUL/memory/skill)
- [ ] Correction verified in next task
- [ ] No corrections left unsaved

---

## Notes

- **Corrections must be saved:** Unsaved corrections repeat in next session.
- **Build trust gradually:** Small tasks first, high-stakes tasks after validation.
- **Pathology diagnosis:** If behavior is wrong, diagnose root cause before fixing.
- **Scope matters:** General rules go to SOUL.md, specific prefs to memory, workflows to skills.
- **Iteration is normal:** Agent behavior improves through repeated correction cycles.

---

## Related Skills

- Skill: System Audit (detects behavior drift across all agents)
- SOP: testing-iteration.md (full specification)
- SOP: autonomy-tiers.md (Tier 1/2/3 definitions)
- Template: soul-section-template.md (standardized SOUL structure)
