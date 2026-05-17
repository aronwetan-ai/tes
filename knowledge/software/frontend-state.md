# Frontend State Management — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.frontend`, `@nexusai.cto`

NexusAI default stack: Next.js / React / TypeScript / Tailwind for SaaS dashboards. Vite + React for internal dev tools.

---

## Decision Tree — What State Lives Where

```
What kind of state?

├─ Server data (from API)
│    → TanStack Query (React Query) / SWR
│
├─ URL state (filter, page, search, selected tab)
│    → URL search params via Next router / useSearchParams
│
├─ Form state (multi-field, validated)
│    → React Hook Form
│
├─ UI state, single component (open/closed, hover, focused field)
│    → useState
│
├─ UI state, parent + a few children
│    → lift state to common parent + props
│
├─ UI state, deep tree, many components
│    → Context API (sparingly)
│
├─ App-wide UI state (theme, sidebar collapsed, toasts)
│    → Zustand (or Context if very small)
│
├─ Real-time / collaborative
│    → WebSocket + reducer + optimistic update
│
└─ Cross-tab / persistent
     → localStorage + Zustand persist middleware
```

Rule of thumb: **server state is not UI state**. Don't store API data in Zustand/Redux when React Query gives you cache + invalidation + dedup for free.

---

## Server State — TanStack Query Patterns

```typescript
// Query
const { data, isLoading, error } = useQuery({
  queryKey: ['campaigns', clientId],     // tenant-aware key
  queryFn: () => api.getCampaigns(clientId),
  staleTime: 60_000,                      // fresh for 1 min
});

// Mutation
const mut = useMutation({
  mutationFn: (input) => api.createCampaign(input),
  onSuccess: () => {
    qc.invalidateQueries({ queryKey: ['campaigns', clientId] });
  },
});
```

Key conventions:
- **Query key includes tenant** (`clientId`). Switching client invalidates correctly.
- **`staleTime`** prevents refetch-storm on remount. Tune per data: real-time → 0; settings → minutes.
- **Optimistic updates** for instant UX on mutations. Rollback on error.
- **`refetchOnWindowFocus: false`** if data is expensive to refetch.

Anti: storing `data` from `useQuery` into `useState` "to control it". Lose cache + dedup. Just use the query.

---

## URL State

For filter/sort/pagination/tabs — anything that should survive refresh + be shareable:

```typescript
const router = useRouter();
const params = useSearchParams();
const status = params.get('status') ?? 'all';

function setStatus(next: string) {
  const p = new URLSearchParams(params);
  p.set('status', next);
  router.push(`?${p}`);
}
```

Why URL state matters:
- Shareable links work.
- Browser back/forward works.
- Refresh preserves state.
- No need to sync state to URL manually.

---

## Form State — React Hook Form

For >2-field forms, especially multi-step:

```typescript
const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(campaignSchema),  // Zod for validation
});

<input {...register('name')} />
{errors.name && <p>{errors.name.message}</p>}
```

Wins:
- Uncontrolled inputs by default → fewer re-renders.
- Validation with Zod reuses backend schema (single source of truth).
- Simple async submit + error handling.
- Built-in dirty / touched tracking.

---

## When Context API, When Not

Use Context when:
- Truly app-wide (theme, current user, locale).
- Provider sits high enough that context value rarely changes.

Avoid Context when:
- Value updates frequently (causes all consumers to re-render).
- Used only by 2–3 components in same subtree → just lift state.

If frequent updates + many consumers: use Zustand instead. Selector subscriptions skip unrelated renders.

---

## Zustand Pattern (App-Wide UI)

```typescript
import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  toasts: Toast[];
  pushToast: (t: Toast) => void;
}

export const useUI = create<UIState>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  toasts: [],
  pushToast: (t) => set((s) => ({ toasts: [...s.toasts, t] })),
}));

// Component
const sidebarOpen = useUI((s) => s.sidebarOpen);  // selector — only re-renders on change
```

Why Zustand over Redux for agency-scale: less boilerplate, no provider, decent devtools, scales to ~50 stores fine.

---

## Optimistic Update Pattern

For "instant" UX on mutations:

```typescript
const mut = useMutation({
  mutationFn: (id: string) => api.toggleStar(id),
  onMutate: async (id) => {
    await qc.cancelQueries({ queryKey: ['items'] });
    const prev = qc.getQueryData(['items']);
    qc.setQueryData(['items'], (old) =>
      old.map((x) => (x.id === id ? { ...x, starred: !x.starred } : x))
    );
    return { prev };
  },
  onError: (err, id, ctx) => {
    qc.setQueryData(['items'], ctx?.prev);  // rollback
    toast.error('Update failed');
  },
  onSettled: () => qc.invalidateQueries({ queryKey: ['items'] }),
});
```

When to use: low-risk UI state (star, like, toggle). Don't use for critical operations (payment, send) — wait for confirmation.

---

## Real-Time Patterns

```typescript
// WebSocket → invalidate query
useEffect(() => {
  const ws = new WebSocket(url);
  ws.onmessage = (msg) => {
    const event = JSON.parse(msg.data);
    if (event.type === 'campaign.updated') {
      qc.invalidateQueries({ queryKey: ['campaigns', event.client_id] });
    }
  };
  return () => ws.close();
}, [url]);
```

For collaborative editing, consider Y.js / Liveblocks — handle CRDT for you.

---

## Multi-Tenant State Considerations

Agency-critical: switching clients must clear/invalidate all tenant-scoped state.

```typescript
function ClientSwitcher() {
  const setClient = useUI((s) => s.setCurrentClient);
  const qc = useQueryClient();

  function switchTo(clientId: string) {
    setClient(clientId);
    qc.removeQueries({ queryKey: ['campaigns'] });  // anything client-scoped
    qc.removeQueries({ queryKey: ['contacts'] });
    router.push(`/dashboard/${clientId}`);
  }
}
```

Test: switch from Client A to Client B, verify no Client A data flashes on Client B's screens.

---

## Performance — When to Memoize

`useMemo` / `useCallback` only when:
1. Profiler shows a measurable problem.
2. Memoized value is used as dep in `useEffect` / passed to memoized child.
3. Computation is genuinely expensive (>5ms).

Premature memoization adds noise without speed gain. React's reconciler is fast.

`React.memo` only for:
- Components that re-render often with same props.
- Children of frequently-updating parents.
- Props are referentially stable (objects/functions stabilized via `useMemo`/`useCallback`).

---

## Anti-Patterns

- **Putting server data in Redux/Zustand.** Use React Query/SWR instead.
- **Lifting state too high.** Causes parent re-render on every child interaction.
- **Prop drilling 3+ levels.** Use composition or context.
- **State that mirrors props.** `useState(props.value)` → state desync. Just use the prop.
- **`useEffect` to derive state.** Compute during render: `const x = derive(prop)`.
- **Imperative DOM manipulation.** Stick to declarative; refs only when essential.
- **Modal-in-modal.** UX nightmare. Re-design flow.
- **One giant `App` context with 20 fields.** Split or move to Zustand with selectors.
- **Storing tokens/secrets in localStorage.** XSS readable. Use HttpOnly cookies.

---

## Reference

- `companies/nexusai/skills/uiux/SKILL.md`
- `knowledge/software/api-design.md` (server contract)
- TanStack Query docs (canonical).
- Zustand docs (canonical).
