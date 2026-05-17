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

## Senior Patterns (Deep Dive)

### SaaS dashboard archetype (agency context)

NexusAI mostly builds **client-facing dashboards** for the agency. Default information architecture:

```
Top nav:    [Logo]  [Client switcher ▼]  [Account ▼]
Side nav:   Overview | Channels | Campaigns | Reports | Settings
Main:       Headline metric (1) → Supporting (3) → Trend (chart) → Actions
```

Per-screen rules:
- Headline metric is unambiguous. "47 new leads this week" not "Lead acquisition rate trending up".
- Trend chart shows last 4-12 periods, not 90 days of noise.
- Actions are scoped to the screen's intent. Don't put "Add team member" on the Reports screen.

### Client switcher pattern (multi-tenant UX)

- Dropdown in top nav, persistent across pages.
- Last-selected client persisted per user (cookie / settings).
- Switching clients clears any "draft" state safely with confirmation if data unsaved.
- URL reflects current client (`/dashboard/client-slug/...`) so links shareable.
- Accessible names: "Acme Corp · Marketing" not "ACME-2".

### Form patterns (agency reality — clients fill these)

| Form type | Pattern |
|---|---|
| Onboarding (long, multi-step) | Stepper with explicit steps + progress bar + save-and-resume. |
| Quick edit (single field) | Inline edit, autosave on blur, "saved" indicator. |
| Settings (medium) | Sectioned form, save per section, not whole-form submit. |
| Data import (CSV upload) | Drag-drop + sample download + preview before commit + dry-run report. |

Validation rules:
- **Inline on blur**, not on every keystroke (annoying) and not only on submit (frustrating).
- Error messages tell you what to do, not just what's wrong: "Email needs an @ — example: name@domain.com".
- Required fields marked, optional fields explicit. Don't assume which is which.

### Empty state hierarchy

A useful empty state has 3 layers:

1. **What's missing** — "No campaigns yet."
2. **Why this is good (or fine)** — "First campaign takes ~5 minutes to set up."
3. **CTA to fill it** — "Create your first campaign" button.

Anti-pattern: showing zero state with just "No data" — wastes pixels and confuses new users.

### Loading state patterns

| Wait time | Pattern |
|---|---|
| <100ms | No indicator, would feel jittery. |
| 100ms–1s | Spinner / skeleton in the affected region. |
| 1s–10s | Skeleton with structure (preview of layout). Optionally progressive reveal as data arrives. |
| >10s | Progress bar with realistic ETA. Allow cancel. |
| Background long-running | Toast: "Processing... we'll notify when done." Don't block UI. |

### Error UX

For every error a user might see:

- **Plain language**, no stack traces, no error codes alone.
- **Cause**: what went wrong (one sentence).
- **Action**: what to do (retry / fix input / contact support).
- **Recovery path**: don't lose user's work — preserve form input across refresh.

```
"We couldn't connect to your Instagram account.
This often happens when your IG session expires.
[Reconnect Instagram] · [Try later]"
```

### Accessibility baseline (must-have)

- All interactive elements keyboard-reachable (Tab) and operable (Enter/Space).
- Focus state visible (browser default ring or custom, never `outline: none` without replacement).
- Form labels via `<label>` or `aria-label`. Placeholder is not a label.
- Color is never the only signal (red/green also has icon/text).
- Body text contrast ≥ 4.5:1, large text ≥ 3:1.
- Image `alt`. Decorative `alt=""`. Icon buttons get `aria-label`.
- Live regions (`aria-live="polite"`) for async status updates.
- Skip-to-content link at top.

### Frontend state management — when to use what

| Need | Tool |
|---|---|
| Component-local UI state (open/closed, hover) | `useState` |
| Cross-component shared UI state (theme, sidebar) | Context API |
| Server data (fetch, cache, invalidate) | TanStack Query / SWR |
| Form state (large multi-step) | React Hook Form |
| URL state (filter / page / search) | URL search params (router) |
| Real-time / collaborative | WebSocket + reducer |
| Global app state across many features | Zustand / Redux Toolkit (only when others insufficient) |

Reference: `knowledge/software/frontend-state.md`.

### Component anti-patterns

- **Prop drilling > 3 levels deep.** Use context or composition.
- **State that mirrors server state.** Use server-state lib that handles staleness.
- **Imperative DOM manipulation in React.** Use refs only when necessary, prefer declarative.
- **All-in-one kitchen-sink components.** Split when component does >2 things.
- **Modal-in-modal.** UX nightmare. Re-design the flow.

### Design tokens (NexusAI dev tools / SaaS default)

- Spacing: 4-base scale (4, 8, 12, 16, 24, 32, 48, 64).
- Typography: 5 sizes max (xs, sm, base, lg, xl, 2xl). One sans family.
- Color: 1 brand color + 1 accent + neutral scale (50→900) + semantic (success / warn / error / info).
- Radius: 3 levels max (none, default, full).
- Shadow: 3 levels max (sm, md, lg).

Don't proliferate tokens — every additional design token is cognitive load on the team.

### Anti-patterns NexusAI rejects

- **"Pixel-perfect" pursuit on internal tools.** Ship usable, iterate on data.
- **Decorative elements without function.** Every UI element has a job.
- **Modals for routine forms.** Modal = blocking decision, not "where we put forms".
- **Toasts for errors.** Errors deserve sticky inline message, not 3-second toast.
- **Hover-only interactions.** Touch users + keyboard users left out.

## Reference

- `companies/nexusai/SOUL.md`
- `knowledge/software/software-development-sop.md`
- `knowledge/software/frontend-state.md`
