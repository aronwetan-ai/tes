# Strategic Thinking Protocol — Decomposition & Sequencing

Versi: 1.0
Created: 2026-05-17
Owner: Used by all CEO agents (`@nexusai.ceo`, `@brandflow.ceo`, `@crypto.ceo`) + Operator
Source: Adapted from SUPERAGENT v2 x2.md

---

## Purpose

5-step protocol untuk break down complex multi-step decisions / strategy / architecture.
Reusable across companies — Tier 2 / Tier 3 SOULs pakai protocol yang sama untuk konsistensi.

NOT untuk routine tasks — itu pakai standard agent flow.

---

## When To Use

- Multi-step strategic decision (e.g., "should we spawn Company #4?")
- Architecture choice (e.g., "embed dashboard vs standalone product?")
- "Help me think through [X]"
- Operator atau CEO menghadapi keputusan dengan trade-off non-trivial

NOT untuk:
- Routine content production
- Standard research/analysis (sudah ada framework)
- Single-step questions

---

## The 5 Steps

### Step 1 — Reframe

```
Pertanyaan:
- Apa actual problem? (sering ≠ stated problem)
- Apa ultimate objective?
- Apa real constraints vs assumed constraints?

Output: 1-2 paragraf clarification.
```

Reframe seringkali change everything. "How do I scale BrandFlow?" mungkin sebenarnya "How do I avoid burnout during scale?"

---

### Step 2 — Decompose

```
Pertanyaan:
- Apa sub-problems?
- Apa yang HARUS true supaya ini sukses?
- Dependencies di antara sub-problems?
- Critical path?

Output: list sub-problems + dependency graph (text-based ok).
```

---

### Step 3 — Options Matrix

Untuk setiap viable path:

```
| Path | Upside | Downside | Risk | Speed | Cost |
|------|--------|----------|------|-------|------|
| A    | ...    | ...      | low  | 2w    | $X   |
| B    | ...    | ...      | high | 6w    | $Y   |
| C    | ...    | ...      | med  | 3w    | $Z   |
```

Be specific. "Risk: medium" tidak cukup. "Risk: 30% chance brand voice drift if QA gate skipped" lebih baik.

---

### Step 4 — Recommend

```
Primary recommendation:  [option]
  Because:               [reason]
  Confidence:            [H/M/L]

Fallback:                [option]
  Trigger:               [if X happens, switch to fallback]

Avoid:                   [option]
  Because:               [specific risk]
```

---

### Step 5 — First Move

Always close dengan:

```
First concrete action dalam 24 jam:
  → [specific action, owner, deliverable]
```

Strategy tanpa first move = wishful thinking. Always make next step concrete.

---

## Output Format

Short structured output. Headers + bullets. Long thinking → compressed output.

Show internal chain of thought hanya ketika explicitly asked. Default: hasil saja.

---

## Anti-Patterns (Jangan Lakukan)

❌ Skip Step 1 (Reframe) — gampang solve wrong problem.
❌ Options matrix tanpa specifics — "low risk" / "fast" tidak useful.
❌ Skip Step 5 (First Move) — strategy tanpa action item.
❌ Show all chain of thought — operator butuh result, bukan transcript.
❌ Rekomendasi tanpa fallback — apa kalau primary fail?
❌ Lupa Boundary #4 — strategy yang affect public surface harus flag for Fathur approval.

---

## Reference

- Source: `update/v2/openclaw/skills/x2.md`
- Complementary: `knowledge/sop/autonomous-boundaries.md` (decide tier of resulting decision)
- Used by: All CEO agents + Operator
