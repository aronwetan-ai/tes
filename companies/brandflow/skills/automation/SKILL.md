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


---

## Senior Patterns (Deep Dive) — Update 11

The senior marketing-ops playbook for agency-context automation. Marketing automation is mostly **content state machines + per-client compartmentalization + approval gates**, not infrastructure orchestration (which belongs to NexusAI).

### 1. Multi-Tenant Editorial Pipeline (Per-Client Compartmentalization)

The agency runs 20-50 active clients. Each has their own pipeline. The pipeline structure is uniform; the data is compartmentalized.

```
companies/brandflow/clients/<client>/
   voice.md
   visual.md
   personas.md
   pipeline/
     inbox.jsonl       (ideas — IDEA stage)
     active.jsonl      (in production — BRIEF/DRAFT/REVIEW/APPROVED stages)
     scheduled.jsonl   (queued — SCHEDULED stage)
     published.jsonl   (live + measurable — PUBLISHED/MEASURED stages)
     archive/<YYYY-MM>.jsonl   (older terminal entries)
   reports/
     weekly/<YYYY-WW>.md
     monthly/<YYYY-MM>.md
   credentials/
     (handled by NexusAI cred_vault, not stored here)
```

Rules:
- **Never** mix two clients' data in one file.
- **Always** include `client_id` in every JSONL row, even though the directory already implies it (defense in depth).
- **Always** scope reports to one client per file.
- Cross-client analytics requires explicit aggregation step (not "just read the files together"), because each client signed for separate reporting.

### 2. Editorial State Machine — Full

```
       IDEA
        │  (CMO / brainstorm)
        ▼
       BRIEF
        │  (CMO writes brief; auto-validate brief completeness)
        ▼
       DRAFT
        │  (Copywriter / Designer produce; voice_check + readability run)
        ▼
       REVIEW
        │  (QA reviews; can route to REVISION → DRAFT, or APPROVED, or KILLED)
        ▼
       APPROVED
        │  (CMO sign-off; eligible for SCHEDULED)
        ▼
       SCHEDULED
        │  (timed; awaits FATHUR APPROVAL gate per Boundary #4)
        ▼
       FATHUR-APPROVED        ← per-piece, never blanket
        │
        ▼
       PUBLISHED
        │  (auto-records published_at + native post_url; community + analytics begin)
        ▼
       MEASURED
        │  (after N days post-publish, performance data collected)
        ▼
       ARCHIVED               (after 90 days terminal)
```

Branching:

- Any non-terminal state → **KILLED** (with reason). Records to logs.
- REVIEW → **REVISION** → DRAFT (with reviewer notes inline).
- SCHEDULED → **UNSCHEDULED** (back to APPROVED) if Fathur or CMO pulls.

### 3. Pipeline JSONL Row — Canonical Schema

```json
{
  "id": "BF-<client>-<seq>",
  "client_id": "<client>",
  "campaign_id": "<campaign>",
  "company": "brandflow",
  "format": "carousel|caption|reels|thread|email|article|story|ad",
  "channel": "instagram|linkedin|x|tiktok|email|blog|whatsapp",
  "stage": "IDEA|BRIEF|DRAFT|REVIEW|APPROVED|SCHEDULED|FATHUR_APPROVED|PUBLISHED|MEASURED|KILLED|ARCHIVED",
  "owner": "@brandflow.<role>",
  "due": "YYYY-MM-DD",
  "scheduled_at": "YYYY-MM-DDTHH:MM:SSZ",
  "published_at": "YYYY-MM-DDTHH:MM:SSZ",
  "published_url": "https://...",
  "brief": {
    "audience": "...",
    "goal": "awareness|engagement|conversion|retention",
    "kpi": "...",
    "tone": "...",
    "constraint": "..."
  },
  "draft": {
    "copy": "...",
    "visual_spec_path": "..."
  },
  "review_notes": [
    {"reviewer": "@brandflow.qa", "at": "...", "severity": "blocker|major|minor|nit", "note": "..."}
  ],
  "approvals": [
    {"by": "@brandflow.cmo", "at": "...", "stage_advanced_to": "APPROVED"},
    {"by": "fathur", "at": "...", "stage_advanced_to": "FATHUR_APPROVED"}
  ],
  "metrics": {
    "impressions": 0,
    "engagements": 0,
    "saves": 0,
    "shares": 0,
    "clicks": 0,
    "comments": 0,
    "ctr": 0.0,
    "engagement_rate": 0.0
  },
  "utm": {
    "source": "...", "medium": "...", "campaign": "...", "content": "..."
  },
  "boundary_4_status": "draft_only|awaiting_fathur|fathur_approved|published",
  "version": 1
}
```

### 4. Approval Gate — Boundary #4 Hardcoded

The pipeline transition from `SCHEDULED → PUBLISHED` requires a `FATHUR_APPROVED` checkpoint **per piece**. This is hard-coded at the tooling layer, not a convention:

- Scheduler (`tools/content_scheduler.py`) refuses to release any piece to publishing unless `boundary_4_status == "fathur_approved"` and the approval signature matches.
- "Bulk approve" flag exists but is gated to a single client's same-campaign batch and emits an audit warning.
- Pre-approved categories (e.g. routine community replies) are scoped narrowly and signed off separately per client (not per piece).

### 5. Brief Validation (Refuse Incomplete Briefs)

Briefs without these fields fail validation and bounce back to CMO:

```
required_fields = {
  "audience",     # specific, not "everyone"
  "goal",         # one of: awareness / engagement / conversion / retention
  "channel",      # specific channel(s)
  "tone",         # explicit
  "format",       # specific format(s)
  "kpi",          # measurable
  "deadline"      # specific date
}
```

Optional but encouraged: `voice_profile_path`, `references`, `competitor_examples`, `constraint`.

The validator runs at `IDEA → BRIEF` transition. Briefs that fail = stuck at IDEA until fixed. This forces brief discipline upstream.

### 6. Cron / Scheduler Layer

Local scheduler driven by `content_scheduler.py`:

```
queue dimensions:
  - per-client
  - per-channel
  - per-time-window (publish hours per channel)

invariants:
  - no piece publishes without FATHUR_APPROVED
  - no overlapping publish for same channel within 30 min for same brand
  - per-channel cap (e.g. 3 IG posts/day per brand max — agency policy)
  - quiet hours per client (configured)

backoff:
  - if external scheduler API (Buffer/Hootsuite/native) returns error, retry with exponential backoff
  - hard fail to operator after 3 retries
```

Heavy infra (real cron daemon, real webhook server, multi-host queue) → escalate to `@nexusai.devops`. BrandFlow's scheduler is a local-first wrapper around external tools.

### 7. Performance Pipeline — From Publish to Report

```
PUBLISHED   (record published_at + post_url)
   │  (wait N days, default 7 for short-form, 30 for long-form)
   ▼
COLLECT     (social_monitor.py / native API pull → metrics object)
   │
   ▼
NORMALIZE   (per-channel metrics → unified schema with engagement_rate, ctr)
   │
   ▼
AGGREGATE   (per-campaign / per-client / per-period rollups)
   │
   ▼
REPORT      (auto-generated weekly/monthly client report from JSONL)
```

Rule: **anything that runs against a client's accounts produces structured logs that can be turned into a client dashboard or weekly report without re-instrumentation.** (This is the agency-context priority from SOUL.)

### 8. UTM Convention (Tracking Discipline)

Every tracked link uses `tools/utm_builder.py` with the agency-wide convention:

```
utm_source     = platform identifier (instagram | linkedin | tiktok | newsletter | x | tiktok | email | whatsapp | direct)
utm_medium     = format identifier (organic-post | organic-reel | paid-ad | dm | bio-link | story | email-body | email-cta)
utm_campaign   = <client>__<campaign-slug>__<YYYY-MM>
utm_content    = <piece-id> (ties back to BF-<client>-<seq>)
utm_term       = (paid only) targeting term / audience slice
```

Reference: `knowledge/marketing/utm-conventions.md`.

The convention is enforced by `utm_builder.py` validation. Custom formats are rejected to keep analytics joinable across the agency.

### 9. A/B Test Discipline

Marketing A/B testing in agency context is constrained by audience size. Don't pretend you have stat-sig at 1000 followers.

| Sample size | Test type | Decision rule |
|---|---|---|
| <500 reached | Don't A/B test. Pick by judgment + voice fit. | — |
| 500-5000 reached | Direction-only (>30% lift = signal) | Document, don't claim significance |
| 5000-50000 reached | Bayesian "this is likely better" framing | Decide after 7+ days |
| >50000 reached | Frequentist with proper test framework | Hand off to `@nexusai.ml` for analysis |

Senior pattern: **test format-against-format**, not micro-copy variants. "Carousel vs Reel for the same idea" yields useful directional learning. "Em-dash vs hyphen" doesn't.

### 10. Anti-Patterns Senior Marketing Ops Don't Ship

- **Mixed-tenant pipelines.** Combining two clients' state in one file. Eventually leaks one client's data into another's report.
- **Pipeline without owner per stage.** Pieces sit in "review" forever because no one claimed them.
- **Auto-publishing without per-piece Fathur approval.** Boundary #4 violation, hard-coded prevented.
- **Briefs allowed to enter production without KPI.** Unmeasurable = unjustifiable for retainer.
- **Custom UTM formats per campaign.** Breaks aggregation. Convention is the convention.
- **A/B tests claiming significance at n=200.** Statistically illiterate; invalidates the conclusion.
- **Performance pipeline that re-instruments per client.** Should be uniform schema; one report generator.

### Reference

- `knowledge/marketing/utm-conventions.md`.
- `knowledge/marketing/content-calendar-patterns.md`.
- `tools/content_scheduler.py` (Update 11 — pipeline state machine + approval gate enforcement).
- `tools/utm_builder.py` (Update 11 — convention-validated UTM strings).
- `tools/social_monitor.py` (Update 11 — performance + sentiment ingest).
- `companies/nexusai/skills/automation/SKILL.md` (heavy infra side; cron, daemon, queues).
