---
name: uiux
description: UI flow / component design / UX decisions for NexusAI products (SaaS dashboards, agent control surfaces, dev tools).
company: NexusAI
used_by: ["@nexusai.frontend", "@nexusai.cto"]
---

# UI/UX Skill — NexusAI

Frontend craft for SaaS / dev tools / agent control surfaces. Different from BrandFlow's `designer` — this is about **functional product UX**, not marketing visuals.

Inherits NexusAI SOUL (engineering-precise, pragmatic). Clarity > decoration.

## When to Use

- SaaS app screen design.
- Dashboard / admin panel UX.
- Agent control / monitoring UI.
- Form design (data entry, settings).
- Navigation flow.
- Component-level decisions (states, edge cases).
- Empty / loading / error states.

## Rules

1. **Clarity over cleverness.** A familiar pattern beats a novel one.
2. **Minimize decisions per screen.** One primary action; secondary ones de-emphasized.
3. **Show state.** Loading, empty, error, success — all need explicit states.
4. **Mobile-first only if mobile is primary use case.** Otherwise design desktop-first for SaaS.
5. **Accessibility**: contrast > 4.5:1 for body text, keyboard nav for all interactive elements.
6. **Component states**: default, hover, active, disabled, focus, error.

## Output Format

For UX flow:
```
[FLOW]        Name + goal of the flow
[STEPS]       1, 2, 3 with screens/actions
[STATES]      Loading / empty / error / success per screen
[EDGE CASES]  What if user has no data, no permission, etc.
[CTA]         Primary action per screen
```

For component spec:
```
[COMPONENT]   Name + purpose
[VARIANTS]    Default / hover / active / disabled / loading / error
[BEHAVIOR]    Click / focus / keyboard
[A11Y]        ARIA labels, role, keyboard nav
[PROPS]       Required + optional + defaults
```

For UX problem analysis:
```
[PROBLEM]     What user struggle exists
[ROOT CAUSE]  Why (not just what)
[OPTIONS]     2-3 paths
[DECISION]    Chosen approach + reasoning
[VALIDATION]  How we'll know it's better
```

## Standard Patterns

- **Forms**: label above input. Inline validation. Disable submit while loading.
- **Tables**: sortable headers, pagination if > 50 rows, clear empty state.
- **Toasts**: 3-5 second auto-dismiss for success; sticky for errors.
- **Modals**: only for confirmation / blocking decisions; not for forms with > 5 fields.
- **Empty states**: explain what + CTA to populate.
- **Errors**: actionable ("retry" / "fix") not just "something went wrong".

## Cross-Skill / Cross-Agent

- Backend API for the UI → `@nexusai.backend` + `skills/coding`.
- Test plans for the UX → `@nexusai.qa` + `skills/qa`.
- Marketing landing page (different from product UI) → `@brandflow.designer`.
- Product positioning → `@nexusai.ceo`.

## What This Skill Does NOT Cover

- Marketing visuals (banners, ads, social). Use `@brandflow.designer`.
- Brand identity / logo / palette. Use `@brandflow.designer`.
- Crypto-specific dashboards beyond generic UI patterns. Pair with `@crypto.*` for content.

## Reference

- `companies/nexusai/SOUL.md`
- `knowledge/software/software-development-sop.md`
