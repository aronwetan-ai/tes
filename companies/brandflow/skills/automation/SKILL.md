---
name: automation
description: Editorial calendar automation, social scheduler integration, JSONL task pipelines for BrandFlow campaigns.
company: BrandFlow
used_by: ["@brandflow.pm", "@brandflow.social", "@brandflow.analytics"]
---

# Automation Skill — BrandFlow

Repeatable workflows for marketing operations. Calendar slotting, scheduler queue, performance pipeline, brief routing.

Less infrastructure-heavy than NexusAI's automation. Marketing automation is mostly about **workflow + content state machines**.

## When to Use

- Editorial calendar pipeline (idea → brief → draft → review → schedule → published → measured).
- Social scheduler integration (Buffer, Hootsuite, Later, etc.).
- Performance data pipeline (post → engagement metrics → analysis).
- Brief routing automation (CMO writes brief → goes to Copywriter + Designer in parallel).
- A/B test execution and tracking.
- Recurring campaign templates.

## Default Editorial Pipeline (JSONL)

```json
{
  "id": "BF-001",
  "company": "brandflow",
  "campaign": "campaign-name",
  "format": "carousel",
  "channel": "instagram",
  "stage": "DRAFT",
  "owner": "@brandflow.copywriter",
  "due": "2026-05-20",
  "brief": {...},
  "draft": {...},
  "review_notes": [],
  "scheduled_at": null,
  "published_at": null,
  "metrics": null
}
```

Stage transitions:
```
IDEA → BRIEF → DRAFT → REVIEW → APPROVED → SCHEDULED → PUBLISHED → MEASURED → ARCHIVED
```

Branching:
- REVIEW → REVISION (back to DRAFT) → REVIEW
- Any stage → KILLED (with reason)

## Rules

1. **One source of truth per piece.** Don't duplicate state across files.
2. **Status field always present.** Never NULL — at least DRAFT.
3. **Owner field always present.** Someone is responsible at each stage.
4. **Due date always present.** Even if it's "this sprint".
5. **Resumable**: piece can be picked up at any stage by reading its current state.
6. **Approval gate**: PUBLISHED stage requires Fathur approval marker (Boundary #4).

## Output Format

For pipeline design:
```
[GOAL]          What the pipeline automates
[STAGES]        Stage 1 → Stage 2 → ... → Done
[FILE STRUCTURE]
   inbox.jsonl     — new ideas
   active.jsonl    — in production
   scheduled.jsonl — approved, queued
   published.jsonl — live + measured
[OWNERS PER STAGE] Who advances each stage
[GATES]         Where approval is required
[ROLLBACK]      How to revert / kill
```

For one-shot script:
```
[PURPOSE]   What it does
[INPUT]     Args / env / files needed
[OUTPUT]    Files / state changes
[USAGE]     Exact command
[ROLLBACK]  How to undo
```

For scheduler integration:
```
[TOOL]          Buffer / Hootsuite / Later / etc
[AUTH]          API key location (vault — never in script)
[TRIGGER]       Stage = SCHEDULED → call API
[FAILURE MODE]  What if API down, retries, manual fallback
[VERIFICATION]  How to confirm post is queued
```

## Cross-Skill / Cross-Agent

- Heavy infra (cron, daemon, webhook server) → `@nexusai.devops` + `skills/automation`.
- Performance metric collection from social platforms → `@brandflow.analytics`.
- Content production within pipeline → `@brandflow.copywriter` / `.designer`.
- Calendar strategy / mix → `@brandflow.social`.

## What This Skill Does NOT Cover

- Server / container orchestration → use NexusAI.
- AI-driven content generation pipelines (hybrid) → coordinate with `@nexusai.ml`.
- Crypto data pipelines → `@crypto.*`.

## Reference

- `companies/brandflow/SOUL.md`
- `knowledge/marketing/marketing-sop.md` (Content Calendar Template section)
