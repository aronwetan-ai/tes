# Agile Manifesto — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.pm`, `@nexusai.ceo`, `@nexusai.cto`

---

## The 4 Values (Original Text, 2001)

> We are uncovering better ways of developing software by doing it and helping others do it.
> Through this work we have come to value:
>
> - **Individuals and interactions** over processes and tools
> - **Working software** over comprehensive documentation
> - **Customer collaboration** over contract negotiation
> - **Responding to change** over following a plan
>
> That is, while there is value in the items on the right, we value the items on the left more.

The "over" is critical — it's not "instead of". You still need processes, documentation, contracts, plans. They're just not the goal.

---

## What This Means at Agency Scale

For a digital agency (Fathur's context):

| Value | Practical version |
|---|---|
| Individuals & interactions | Talk to your client and your freelancers daily. Don't manage by Trello card alone. |
| Working software | Ship what your client can actually use this week, even if rough. |
| Customer collaboration | Treat scope as a conversation, not a 30-page SOW. |
| Responding to change | Client pivots are normal. Plan in 2-week horizons, not quarters. |

---

## The 12 Principles (Compressed)

1. **Satisfy the customer through early & continuous delivery.**
   → Ship something useful in week 1, not month 3.

2. **Welcome changing requirements, even late.**
   → Don't penalize the client for learning. Estimate cost, but accept change.

3. **Deliver working software frequently** (weeks, not months).
   → Default cadence: weekly demoable progress.

4. **Business and developers work together daily.**
   → For agency: founder, account manager, and engineer should not work in isolation.

5. **Build projects around motivated individuals.**
   → Trust + tools + decision authority. Don't micromanage.

6. **Face-to-face conversation is the most efficient.**
   → For remote: synchronous video for hard problems, async for status.

7. **Working software is the primary measure of progress.**
   → Not lines of code, not tickets closed, not hours billed. What works.

8. **Sustainable pace.**
   → 60-hour weeks burn the team and the work. Predictable 40-hour pace.

9. **Continuous attention to technical excellence.**
   → Tech debt is interest-bearing. Pay it down.

10. **Simplicity — maximizing the work not done.**
    → YAGNI. Cut features that don't earn their keep.

11. **Self-organizing teams.**
    → For agency: freelancers given context + outcomes, not micro-tasked.

12. **Reflect & adjust regularly** (retrospectives).
    → Bi-weekly retros, ONE change actioned.

---

## Where Agile Fails (Be Honest)

1. **In small/solo teams**, full ceremony is overhead. Use light Kanban (`scrum-kanban.md`).
2. **Without a real PO/customer**, "responding to change" becomes "no plan ever".
3. **Without retros**, the same mistakes repeat.
4. **Without working software at the end of each sprint**, sprint = artificial deadline.
5. **Velocity worship** turns the team into a feature factory ignoring quality + product fit.
6. **"Agile" used to skip documentation entirely** — eventually no one knows why anything was decided. Use ADRs.

---

## Anti-Patterns (Misapplied Agile)

- **"We're agile, so we don't write specs."** Wrong. Agile values working software *over* comprehensive documentation; it doesn't say "no documentation".
- **"Agile means we don't have to plan."** Wrong. Plan in shorter horizons. Don't stop planning.
- **"Velocity is up, ship more!"** Velocity is forecasting input, not performance metric.
- **"Daily standup is a status meeting for the manager."** No. It's peer sync about blockers.
- **Retro lists 10 problems, fixes 0.** ONE actionable change per retro, owned, due-dated.
- **Sprint = "the deadline before the next deadline".** No goal = no agile.
- **Cargo-culting Spotify model / SAFe / LeSS for a 5-person team.** These are scale-out models for orgs of hundreds.

---

## Lightweight Agile for the Agency (Practical)

For Fathur's solo + 2 freelancers + 5–10 clients setup:

- **Weekly sync** (Mon, 30 min): review last week's outcomes, pick this week's goal.
- **Async standup** (chat, not meeting): each morning, contributor posts 3 lines: did / doing / blocked.
- **Bi-weekly retro** (Fri, 45 min): what worked, what didn't, ONE change.
- **Ticket has DONE = X**: see `companies/nexusai/skills/qa/acceptance-criteria-templates.md`.
- **Quarterly OKR refresh** with Fathur — not micromanagement, strategy alignment.
- **No sprint commitment** in the Scrum sense — pull-based work via Kanban WIP limits.

When agency grows past ~10 people: revisit. May want firmer Scrum.

---

## Reference

- agilemanifesto.org (canonical text).
- *Manifesto for Agile Software Development* (4 values, 12 principles).
- `knowledge/agile/scrum-kanban.md` — practical execution patterns.
- *Agile Estimating and Planning* — Mike Cohn.
- `companies/nexusai/agents/pm.md`
