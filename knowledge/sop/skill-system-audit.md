# Skill: 4-Layer System Audit

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** Operator, Main Assistant  
**Trigger:** Friday 10:30 WIB or after major SOP/structure update  
**Frequency:** 1x/week (Friday after weekly recap)  
**Risk Level:** Medium

---

## Purpose

Conduct periodic 4-layer health check of entire AI Holding system. Catches drift, redundancy, and gaps that reflection loop and per-company QA miss. Tier 2 autonomous operation (log decision + propose fix, but don't auto-apply).

---

## Prerequisites

- Access to last 7 days of logs (tasks/logs.jsonl, memory/global.md)
- Access to test results (tests/integration/cross-company-smoke-test.md)
- Access to all company SKILLS.md files
- Access to all SOP files (knowledge/sop/)
- Understanding of system architecture (3 companies, cross-company handoffs, approval workflow)

---

## Steps

### Step 1: Layer 1 — Output Quality

Check if last week's outputs were immediately executable and effective.

**Questions to answer:**

```
1. Were last week's outputs immediately executable?
   → Check: Did any output require follow-up rounds to clarify?
   → Data source: tasks/logs.jsonl (last 7 days, all companies)

2. Did reflection loop catch all issues?
   → Check: Any issues that reflection loop missed but QA caught?
   → Data source: memory/global.md ([QA_HEALTH] entries)

3. Did QA agents catch issues reflection loop missed?
   → Check: Any FAIL verdicts that were unexpected?
   → Data source: memory/global.md ([QA_RESULT] entries)

4. Were SLAs met?
   → Check: Any QA requests that exceeded SLA?
   → Data source: memory/global.md ([SLA_MISS] entries)
```

**Findings format:**

```
[LAYER 1 — OUTPUT QUALITY]

Finding 1: BrandFlow content required 2 revision rounds (vs expected 1)
  Root cause: Handoff block from Crypto missing decay date
  Fix: Add decay date validation to handoff generator

Finding 2: NexusAI API endpoint test failed in smoke test
  Root cause: Endpoint timeout (>5s response time)
  Fix: Investigate endpoint performance, add caching if needed

Finding 3: All QA requests met SLA this week ✓
  Status: No action needed
```

---

### Step 2: Layer 2 — Module / Skill Coverage

Check if correct skills/agents activated per task, and identify gaps/redundancy.

**Questions to answer:**

```
1. Did correct skills/agents activate per task?
   → Check: Task routing decisions in tasks/messages.jsonl
   → Data source: companies/*/SKILLS.md (skill index)

2. Any gaps (task needed skill that doesn't exist)?
   → Check: Tasks that took longer than expected (skill missing?)
   → Data source: tasks/logs.jsonl (task duration)

3. Any redundancy (two skills doing same thing)?
   → Check: BrandFlow design vs NexusAI uiux, similar patterns
   → Data source: companies/*/skills/*/SKILL.md files

4. Any deprecated skill still loading?
   → Check: Skills marked deprecated but still referenced
   → Data source: companies/*/SKILLS.md (version history)
```

**Findings format:**

```
[LAYER 2 — MODULE / SKILL COVERAGE]

Finding 1: Skill gap detected — no skill for "credential rotation"
  Impact: Operator manually rotates credentials (should be automated)
  Fix: Create Skill #6: Credential Setup & Rotation Scheduler

Finding 2: Redundancy found — BrandFlow has 2 content-drafting skills
  Impact: Confusion about which skill to use
  Fix: Consolidate into 1 skill with variants

Finding 3: Deprecated skill "old-approval-format" still in SKILLS.md
  Impact: Agents might load outdated skill
  Fix: Remove from SKILLS.md, move to archive/

Finding 4: All active skills used this week ✓
  Status: No action needed
```

---

### Step 3: Layer 3 — Routing Precision

Check if handoffs, QA routing, and approval workflow respected.

**Questions to answer:**

```
1. Any false positives in routing (@x.y dispatched to wrong agent)?
   → Check: Task routing decisions vs expected routing
   → Data source: tasks/messages.jsonl (routing log)

2. Any handoff blocks malformed?
   → Check: Handoff blocks missing required fields
   → Data source: tasks/inbox.jsonl (handoff entries)

3. Any cross-company QA missed (skipped routing)?
   → Check: Derivative work without cross-QA entry
   → Data source: tasks/logs.jsonl (QA_REQUEST entries)

4. Approval workflow respected (no Tier 3 bypassed)?
   → Check: Any public publish without approval?
   → Data source: memory/global.md ([APPROVAL] entries)
```

**Findings format:**

```
[LAYER 3 — ROUTING PRECISION]

Finding 1: Handoff block missing decay date (1 instance)
  Impact: Content could stay live past expiry
  Fix: Add validation to handoff generator (Skill #3)

Finding 2: Cross-company QA skipped for 1 BrandFlow draft
  Impact: Factual accuracy not verified
  Fix: Enforce automatic QA trigger per cross-company-qa-routing.md

Finding 3: All Tier 3 decisions had approval before execution ✓
  Status: No action needed

Finding 4: Routing accuracy: 98% (1 false positive out of 50 tasks)
  Impact: Low (1 task re-routed, no delay)
  Fix: Review routing rules, update if needed
```

---

### Step 4: Layer 4 — Token / Context Efficiency

Check for bloat and optimization opportunities.

**Questions to answer:**

```
1. Any always-on content that could be conditional?
   → Check: File sizes of always-loaded files
   → Data source: SOUL.md, MAIN.md, MEMORY.md, COMMANDS.md (file sizes)

2. Which skills load more than needed?
   → Check: Skill file sizes, usage frequency
   → Data source: companies/*/skills/*/SKILL.md (file sizes)

3. What can be compressed without losing function?
   → Check: Redundant sections, verbose explanations
   → Data source: All knowledge files

4. Any MEMORY bloat (entries that should move to archive)?
   → Check: memory/global.md growth rate
   → Data source: memory/global.md (line count, age of entries)
```

**Findings format:**

```
[LAYER 4 — TOKEN / CONTEXT EFFICIENCY]

Finding 1: MEMORY.md grew 40% this week (200 → 280 lines)
  Impact: Context budget pressure
  Fix: Archive entries older than 30 days to memory/archive/

Finding 2: Skill file "content-drafting.md" is 500 lines (too large)
  Impact: Loads entire skill even for simple tasks
  Fix: Split into 3 smaller skills (thread / carousel / blog)

Finding 3: SOUL.md has 3 sections that could be conditional
  Impact: Always loaded even when not needed
  Fix: Move to separate file, load on-demand

Finding 4: Token efficiency stable this week ✓
  Status: No action needed
```

---

## Output Format

```markdown
[AUDIT — YYYY-MM-DD]

[FINDINGS]

Layer 1 (Output Quality):
  - <issue> → <fix>
  - <issue> → <fix>

Layer 2 (Skill Coverage):
  - <issue> → <fix>

Layer 3 (Routing Precision):
  - <issue> → <fix>

Layer 4 (Token Efficiency):
  - <issue> → <fix>

[PRIORITY]
1. <highest impact item>
2. <second>
3. <third>

[PROPOSED EDITS]

File: <path>
Change: <specific edit>
Rationale: <why>

File: <path>
Change: <specific edit>
Rationale: <why>

[STATUS]
[ ] Applied immediately (Tier 1 — config-only, no impact on running ops)
[ ] Awaiting Operator review (Tier 2 — affects multiple agents)
[ ] Awaiting Fathur approval (Tier 3 — affects Boundary #4 / strategic)

[NEXT AUDIT]
Scheduled: 2026-05-25 10:30 WIB
```

---

## Input Format

```json
{
  "audit_date": "2026-05-18",
  "period_start": "2026-05-11",
  "period_end": "2026-05-18",
  "data_sources": {
    "logs": "tasks/logs.jsonl",
    "memory": "memory/global.md",
    "test_results": "tests/integration/cross-company-smoke-test.md",
    "skills": "companies/*/SKILLS.md"
  }
}
```

---

## Output Format

```
[AUDIT COMPLETE — 2026-05-18]

Issues found: 4
Priority HIGH: 1
Priority MEDIUM: 2
Priority LOW: 1

Estimated effort to fix: 3 hours
Estimated impact: High (fixes 2 recurring issues)

Ready for review? Yes
```

---

## Critical Rule

**Never auto-apply system changes.** Audit produces findings + proposed edits. Operator (or Fathur for Tier 3) decides apply or revise.

After audit always close with:
> "Apply now or review first?"

---

## Common Errors & Recovery

| Error | Cause | Recovery |
|-------|-------|----------|
| Can't access logs | Permission denied or file missing | Check file paths. Verify access. Use fallback data if available. |
| Findings are vague | Insufficient data gathered | Re-run audit with more detailed log analysis. |
| Same issue found 2 weeks in a row | Fix not applied or ineffective | Escalate to Operator. Review why fix didn't work. |
| Too many findings (>10) | System has drifted significantly | Prioritize top 3. Schedule follow-up audit. |

---

## Verification

- [ ] All 4 layers analyzed
- [ ] Data sources checked (logs, memory, test results, skills)
- [ ] Findings specific (not vague)
- [ ] Proposed edits concrete (not "improve something")
- [ ] Priority ranking clear
- [ ] Status field filled (Tier 1/2/3)
- [ ] Never auto-applied changes

---

## Notes

- **Scheduled:** Every Friday 10:30 WIB (after weekly recap)
- **Triggered:** After major update (PR merge affecting SOP/structure)
- **Ad-hoc:** Operator request "run system audit"
- **Scope:** Entire AI Holding (all 3 companies, cross-company flows)
- **Output:** Findings + proposed edits, awaiting approval before apply

---

## Related Skills

- Skill: Approval Request Formatter (for Tier 3 audit findings)
- Skill: 6-Step Debug Protocol (for investigating audit findings)
- SOP: system-audit.md (full specification)
- SOP: weekly-cadence.md (Friday audit slot)
