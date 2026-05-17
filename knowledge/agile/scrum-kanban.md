# Scrum vs Kanban — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.pm`, `@nexusai.ceo`

For the agency: solo founder + freelancers + ramping to 20–50 clients. Pure Scrum is overkill for that scale; pure laissez-faire is chaos. The right answer is usually a Kanban-flavored system with light Scrum ceremonies.

---

## TL;DR — When to Use What

| Pattern | Best when |
|---|---|
| **Pure Scrum** | Stable team ≥5, predictable backlog, value of forecast > cost of overhead. |
| **Pure Kanban** | Continuous flow, varied work types, support / ops mix. |
| **ScrumBan (hybrid)** | Most agency reality. Light cadence + flow-based execution. |
| **None / informal** | Solo founder + 1–2 contractors, daily verbal sync sufficient. |

NexusAI default at agency-scale: **ScrumBan**.

---

## Scrum — Core Concepts (Compressed)

| Element | Purpose |
|---|---|
| **Sprint** | Fixed time-box (1–4 weeks; default 2). Commit to a scope, ship at end. |
| **Sprint Goal** | One-sentence outcome the sprint serves. Don't have one = sprint is just a deadline, not a goal. |
| **Backlog** | Prioritized list of all work, refined ongoing. |
| **Sprint Backlog** | What was committed for this sprint. |
| **Daily Standup** | 15 min: what done / doing / blocked. Not a status report to manager — a sync among teammates. |
| **Sprint Review** | Demo what shipped. Stakeholder feedback. |
| **Retrospective** | What worked / what didn't / one change for next sprint. |
| **Velocity** | Average points completed per sprint. Forecasting input only — not performance metric. |

Anti-patterns common in misapplied Scrum:
- Sprint = "the deadline before the next deadline". No sprint goal.
- Daily standup = manager status report. Wastes 15min/person.
- Velocity used as performance metric. Gaming starts.
- Sprint commitments never met → either over-committing or interruption-heavy work mismatched with Scrum.

---

## Kanban — Core Concepts

| Element | Purpose |
|---|---|
| **Board** | Columns = workflow states (Backlog → Doing → Review → Done). |
| **WIP Limit** | Max items per column. Forces flow over multitasking. |
| **Pull system** | Worker pulls next item when capacity opens; not pushed. |
| **Cycle Time** | Time from "Doing" to "Done". Target: short + predictable. |
| **Lead Time** | Time from "Backlog" to "Done". User-facing latency. |
| **Cumulative Flow Diagram** | Visualization of WIP over time. Bumps = bottlenecks. |

Why Kanban fits agency reality:
- Mixed work types (client onboarding + bug fix + cold outreach config + reporting).
- Variable urgency (client asks "can we tweak X today?").
- Solo / small team → hard to plan-then-commit-then-ship in fixed sprints.
- Continuous client work doesn't pause every 2 weeks for ceremony.

---

## ScrumBan — NexusAI Recommended Pattern

Combine the best of both:

| From Scrum | From Kanban |
|---|---|
| Weekly sync (lightweight Sprint Review). | Pull-based work assignment. |
| Bi-weekly retro. | WIP limits per state + per person. |
| Defined goal per week ("ship the X dashboard"). | Cycle time + lead time tracking. |
| Quarterly OKR / strategic alignment. | No fixed sprint scope commitment. |

Cadence:
- **Daily**: optional async standup in chat (15-line update by each contributor when they start their day).
- **Weekly (Mon)**: 30-min team sync — review last week, frame this week's goal, raise blockers.
- **Bi-weekly**: retro (45 min) — what worked, what didn't, ONE change for next 2 weeks.
- **Monthly**: roadmap review with Fathur — strategic shift assessment.
- **Quarterly**: OKR refresh.

WIP limits (agency-context):
- Per person: max 2 active tasks. 3rd task = something must finish first.
- "Review" column: max 3. Backed-up reviews = blocker.
- "Blocked": no limit, but red-flagged on board.

---

## Ticket Discipline

Every ticket has:

```
[TITLE]         Outcome-oriented. "Add bulk DM scheduling" not "DM thing".
[CONTEXT]       Why this matters. Linked to what client / OKR.
[DONE = X]      Verifiable acceptance criteria.
[OUT OF SCOPE]  Explicit: what we're NOT doing here.
[OWNER]         One person.
[ESTIMATE]      Rough size (XS / S / M / L / XL or hours).
[DEPENDENCIES]  Blocking / blocked by.
[LINKS]         PR, design doc, related ticket.
```

For ticket sizing (agency-context):
- **XS** (<2h) — bug fix, copy edit, config change.
- **S** (2–8h) — small feature, small refactor.
- **M** (1–3 days) — sized feature.
- **L** (3–10 days) — sized epic/feature with multiple parts.
- **XL** (>10 days) — needs decomposition before starting.

XL never enters "Doing" — split first.

---

## Estimation — Realistic Approach

For a small agency:

- **Don't estimate XS/S tickets.** Just do them. Estimating costs more than the work.
- **Estimate M+ tickets** for planning. Use **rough buckets** (M / L / XL) not story points.
- **Track actual vs estimated** quarterly. Calibrate.
- **Don't measure individual velocity.** That's a metric headed for gaming.

Anti: hours-precise estimation. You're optimizing the wrong thing.

---

## Capacity Planning

Solo + 2 freelancers, 5-day work week:
- ~3 person-weeks of capacity per calendar week (rough).
- Reserve 30% for unplanned (bugs, client asks, ops). Plan to 70% (= ~2.1 person-weeks).
- Allocate by client: client_42 gets ~30% time → ~0.6 person-weeks/wk.

Guard rails:
- **WIP cap per client**: ≤2 active features per client.
- **Top 3 OKRs first**: anything not aligned waits unless P0.
- **Visible client allocation board**: who's working on which client this week.

---

## Common Anti-Patterns (Agency Context)

- **Sprint planning meeting > sprint work.** Scrum overhead exceeds value at small scale.
- **No retro.** Same mistakes repeat.
- **Retro lists 10 problems, fixes 0.** ONE change per retro, owned, due-dated.
- **Backlog grooming = nobody's job.** Items rot. Stalest item = signal: dead idea or just disorganized?
- **Estimating in hours, padding "just in case".** Padding becomes the new estimate. Estimate buckets, not hours.
- **No client-time visibility.** Two clients ask for "small thing today" simultaneously, both promised, both fail.
- **No defined "done"** per ticket. Ships whatever subset feels right.
- **Standup as status report.** Standup is for blockers + sync among peers, not status to manager.
- **Velocity worship.** Velocity is forecast input, not performance metric.

---

## When the Process Itself Is Wrong

Signals to change process (not work harder within it):

- Cycle time growing month-over-month.
- Blockers stuck in "Blocked" >3 days regularly.
- Same person always pulling next ticket → bus factor.
- Client surprises ("you said it'd be done last week!") frequently.
- Team feels overloaded but work doesn't ship.

Don't sprint harder. Stop. Diagnose. Adjust.

---

## Reference

- *Scrum Guide* (scrumguides.org) — canonical.
- *Kanban: Successful Evolutionary Change* — David J. Anderson.
- `knowledge/agile/agile-manifesto.md` — principles behind both.
- `companies/nexusai/agents/pm.md`
- `companies/nexusai/skills/qa/acceptance-criteria-templates.md` — DONE = X templates.
