# Debug Protocol — Standardized Fault Diagnosis

Versi: 1.0
Created: 2026-05-17
Owner: All agents (primarily NexusAI engineering, but applicable cross-company)
Source: Adapted from SUPERAGENT v2 x3.md

---

## Purpose

Sistematik 6-step debug protocol untuk diagnose & fix faults.
Reusable across companies (engineering bugs, content errors, data issues, tool failures).

Goal: **diagnose dulu sebelum prescribe**. Never "try this and see."

---

## The 6 Steps

### Step 1 — Gather (semua sekaligus)

Kumpulkan dalam satu pass:

```
- Exact error text (full, jangan paraphrase)
- Last action sebelum fault
- Environment: OS / runtime version / company / agent / tool versions
- Last known working state (kalau applicable)
- Recent changes (commits, config edits, deployments)
```

**Rule:** Jangan ask data piecemeal. Minta semua dalam satu message.

---

### Step 2 — Classify

Tentukan kategori fault:

```
syntax       → malformed instruction (markdown broken, code typo, JSON malformed)
runtime      → valid syntax, execution failure (script crashes, tool returns error)
logic        → runs clean, output salah (wrong calculation, wrong data routed)
environment  → missing var / wrong version / permission denied
network      → timeout / DNS / port / firewall / API rate limit
dependency   → missing module / version conflict / package broken
data         → input format wrong / source stale / schema mismatch
content      → factual error / brand violation / disclaimer missing
process      → SOP not followed / handoff block missing / approval skipped
```

---

### Step 3 — Diagnose

```
Root cause:  [specific line / config / step / data point]
Mechanism:   [satu kalimat: kenapa ini menyebabkan failure]
```

Diagnose dulu. Jangan langsung prescribe.

---

### Step 4 — Resolve

```bash
# Exact corrective action(s)
# Untuk code: command yang spesifik
# Untuk content: edit yang spesifik
# Untuk process: SOP step yang harus dijalankan
```

---

### Step 5 — Verify

```bash
# Command / check yang membuktikan fix bekerja
# Jangan skip ini — "should work" ≠ "verified work"
```

---

### Step 6 — Harden

```
# Config / SOP / test delta untuk prevent recurrence
# Kalau bug yang sama bisa muncul lagi → ada gap di system
```

---

## Output Format

```
[ROOT CAUSE]   → [specific]
[FIX]          → [exact commands / edits]
[VERIFY]       → [verification command / check]
[HARDEN]       → [prevention — SOP update, test added, monitoring added]
```

---

## Special Case: Cross-Company Fault

Kalau fault melibatkan handoff antar company:

1. Identify company tempat fault TERDETEKSI vs company tempat fault BERASAL.
2. Routing: SOP `cross-company-qa-routing.md` apply.
3. Both companies' QA review the fix sebelum hardening.

Contoh:
- BrandFlow content punya angka salah → root cause: handoff dari Crypto Consultant tidak include latest revision.
- Fix: bukan di BrandFlow, tapi di handoff protocol Crypto Consultant.
- Harden: tambah QA gate post-revision.

---

## Anti-Patterns (Jangan Lakukan)

❌ "Try this and see" — diagnose dulu.
❌ Skip Step 5 (Verify) — "should work" tidak cukup.
❌ Skip Step 6 (Harden) — bug yang sama bakal ulang.
❌ Tanya data piecemeal — minta semua dalam satu pass.
❌ Fix tanpa root cause — gejala hilang, penyakit tetap.
❌ Apply fix di production tanpa verify di staging.

---

## Reference

- Source: `update/v2/openclaw/skills/x3.md`
- Complementary: `knowledge/sop/cross-company-qa-routing.md`
- Tools: NexusAI `skills/devops/` untuk technical fixes
