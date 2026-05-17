# UPGRADE.md — Hermes Auto-Upgrade Command Sheet

> **Cara pakai:** Kirim ke Hermes: **`jalankan upgrade dari UPGRADE.md`** atau **`run upgrade UPGRADE.md`**.
> Hermes baca file ini, jalankan setiap step urutan dari atas ke bawah, lalu lapor hasil.

---

## Tentang Upgrade Ini

**Source:** `update/v2/openclaw/` (SUPERAGENT v2 brain system)
**Strategy:** **Cherry-pick** — hanya ambil yang kita belum punya atau yang lebih baik dari milik kita. Tidak replace existing system.
**Filosofi:** Sistem multi-company kita (Root SOUL → Tier 2 → Tier 3 + Boundary #4) **tetap autoritatif**. SUPERAGENT hanya memberi tools/SOPs tambahan.

---

## Pre-Flight Check (Wajib)

Hermes harus verify dulu sebelum mulai:

```bash
# 1. Pastikan di branch yang benar
git status
# Expected: clean working tree, on main (or feature branch from main)

# 2. Pastikan source file ada
test -d update/v2/openclaw && echo "source ok" || echo "source missing — abort"

# 3. Pastikan target dirs ada
test -d knowledge/sop && echo "sop ok"
test -d knowledge/agent-design && echo "agent-design ok"
test -d tools && echo "tools ok"
test -d knowledge/ml && echo "ml ok" || mkdir -p knowledge/ml
```

Kalau ada yang fail → **STOP**, lapor ke operator.

---

## STEP 1 — Adopt Reflection Loop (Tier A)

**File baru:** `knowledge/agent-design/reflection-loop.md`
**Source:** `update/v2/openclaw/skills/m0.md` (REFLECTION LOOP section)
**Adapt:** +1 question untuk Boundary #4 awareness

Tulis file ini:

```markdown
# Reflection Loop — Lightweight Self-Check

Versi: 1.0
Created: 2026-05-17
Owner: All agents (Tier 1, 2, 3)
Source: Adapted from SUPERAGENT v2 m0.md

---

## Purpose

A 5-question silent check yang dijalankan **setiap agent** sebelum mengirim output.
Lightweight quality gate — catches obvious issues BEFORE heavyweight QA.

NOT a replacement untuk QA agents. Ini di layer agent-individual, QA tetap di layer cross-checking.

---

## The 5 Questions

Setelah draft output ready, agent melakukan check ini secara silent:

```
✅ Q1. Immediately executable / usable as-is?
       (Tidak ada placeholder, tidak ada "TODO", tidak ada referensi yang belum ada)

✅ Q2. Anything missing the user/next-agent will need next?
       (Konteks, sumber, decay date, handoff block lengkap)

✅ Q3. Generic advice avoided?
       (Spesifik untuk konteks ini, bukan boilerplate)

✅ Q4. Faster or cleaner path missed?
       (Apakah ada cara yang lebih efisien yang terlewat?)

✅ Q5. Boundary #4 honored?
       (Kalau output ini menyentuh public surface → ada flag "needs Fathur approval"?
        Kalau output ini financial → ada disclaimer + bear case?
        Kalau output ini cross-company → ada handoff block?)
```

**Jika ada 1 jawaban "tidak" → revise sebelum output.**
**Jika semua "ya" → ship.**

---

## Penambahan Optional: Upgrade Note

Jika ada upgrade path yang relevan (cara lebih baik, refactor opportunity), append:

```
🔧 Upgrade path: [satu baris saja]
```

Tidak wajib. Hanya ketika benar-benar relevan.

---

## Yang Bukan Bagian dari Reflection Loop

❌ Bukan pengganti QA agents (`@crypto.qa`, `@brandflow.qa`, `@nexusai.qa`).
❌ Bukan tempat untuk full content review — itu QA's job.
❌ Bukan tempat untuk debate persona / tone.

Reflection loop = self-check 30 detik, bukan review 30 menit.

---

## Reference

- Source: `update/v2/openclaw/skills/m0.md`
- Complementary: `knowledge/sop/cross-company-qa-routing.md` (heavyweight QA)
- Complementary: `companies/*/skills/qa/SKILL.md` (per-company QA)
- Boundary #4: `SOUL.md` root
```

**Verify:** `test -f knowledge/agent-design/reflection-loop.md && echo "step 1 ok"`

---

## STEP 2 — Adopt Debug Protocol (Tier A)

**File baru:** `knowledge/sop/debug-protocol.md`
**Source:** `update/v2/openclaw/skills/x3.md`
**Adapt:** Format generalisasi untuk semua company (bukan hanya engineering)

Tulis file ini:

```markdown
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
```

**Verify:** `test -f knowledge/sop/debug-protocol.md && echo "step 2 ok"`

---

## STEP 3 — Adopt System Audit Protocol (Tier A)

**File baru:** `knowledge/sop/system-audit.md`
**Source:** `update/v2/openclaw/skills/x1.md`
**Adapt:** Schedule mingguan (Friday) di weekly-cadence.md sebagai automated trigger

Tulis file ini:

```markdown
# System Audit Protocol — Periodic Health Check

Versi: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Schedule: Weekly (Friday, after weekly recap) + ad-hoc when triggered
Source: Adapted from SUPERAGENT v2 x1.md

---

## Purpose

Periodic 4-layer audit untuk health check seluruh AI Holding system.
Catches drift, redundancy, dan gaps yang reflection loop / per-company QA miss.

Tier 2 dari `autonomous-boundaries.md` — autonomous tapi log decision + propose fix.

---

## When To Run

- **Scheduled:** Setiap Jumat sebagai bagian dari weekly recap (`weekly-cadence.md` Step 4)
- **Triggered:** Setelah major update (PR merge yang affect SOP / structure)
- **Ad-hoc:** Operator request "run system audit"

---

## The 4 Layers

### Layer 1 — Output Quality

```
Pertanyaan:
- Were last week's outputs immediately executable?
- Did any cause unnecessary follow-up rounds?
- Did reflection loop catch all issues?
- Did QA agents catch issues reflection loop missed?

Data source:
- tasks/logs.jsonl (last 7 days, all companies)
- memory/global.md (last week's [APPROVAL] / [QA_HEALTH] entries)
- tests/integration/cross-company-smoke-test.md (Friday run results)
```

### Layer 2 — Module / Skill Coverage

```
Pertanyaan:
- Did correct skills/agents activate per task?
- Any gaps (task needed skill yang belum ada)?
- Any redundancy between skills (BrandFlow design vs NexusAI uiux, dll)?
- Any deprecated skill yang masih ke-load?

Data source:
- companies/*/SKILLS.md
- knowledge/sop/* (cross-cutting SOPs)
- Recent task routing decisions
```

### Layer 3 — Routing Precision

```
Pertanyaan:
- Any false positives in pseudo-mention routing (@x.y dispatched ke wrong agent)?
- Any handoff blocks malformed?
- Any cross-company QA missed (skipped routing)?
- Approval workflow respected (no Tier 3 bypassed)?

Data source:
- tasks/inbox.jsonl (handoff entries)
- tasks/messages.jsonl (cross-agent routing)
- memory/global.md (approval log)
```

### Layer 4 — Token / Context Efficiency

```
Pertanyaan:
- Any always-on content yang bisa dijadikan conditional?
- Which skills load more than needed?
- What can be compressed without losing function?
- Any MEMORY bloat (entries yang seharusnya pindah ke archive)?

Data source:
- File size of always-loaded files (SOUL.md, MAIN.md, MEMORY.md, COMMANDS.md)
- Skill file sizes
- memory/global.md growth rate
```

---

## Output Format

```
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

[STATUS]
[ ] Applied immediately (Tier 1 — config-only, no impact on running ops)
[ ] Awaiting Operator review (Tier 2 — affects multiple agents)
[ ] Awaiting Fathur approval (Tier 3 — affects Boundary #4 / strategic)
```

---

## Critical Rule

**Never auto-apply system changes.** Audit produces findings + proposed edits.
Operator (or Fathur untuk Tier 3) decides apply or revise.

After audit always close with:
> "Apply now or review first?"

---

## Reference

- Source: `update/v2/openclaw/skills/x1.md`
- Schedule: `knowledge/sop/weekly-cadence.md` (Friday slot)
- Complementary: `tests/integration/cross-company-smoke-test.md`
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
```

**Verify:** `test -f knowledge/sop/system-audit.md && echo "step 3 ok"`

---

## STEP 4 — Adopt Strategic Thinking Protocol (Tier A)

**File baru:** `knowledge/sop/strategic-thinking.md`
**Source:** `update/v2/openclaw/skills/x2.md`
**Adapt:** Reusable untuk semua company CEOs untuk multi-step decisions

Tulis file ini:

```markdown
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
```

**Verify:** `test -f knowledge/sop/strategic-thinking.md && echo "step 4 ok"`

---

## STEP 5 — Build LLM Multi-Provider Client (Tier B)

**File baru:** `tools/llm_client.py` + `knowledge/ml/llm-providers.md`
**Source:** `update/v2/openclaw/skills/m7.md` (Universal Python Wrapper section)
**Adapt:** Production-grade dengan error handling + retry + log + register di tool registry

### 5a. Buat `tools/llm_client.py`

```python
#!/usr/bin/env python3
"""
TOOL-033 — LLM Multi-Provider Client
====================================

Unified client untuk 5 LLM providers: Anthropic, OpenAI, Groq, Kimi, DeepSeek.
Adapted from SUPERAGENT v2 m7.md.

Usage (CLI):
    python tools/llm_client.py --provider anthropic --message "Halo"
    python tools/llm_client.py --provider groq --system "Anda asisten Indonesia" --message "Apa kabar?"

Usage (import):
    from tools.llm_client import call_llm
    result = call_llm("Halo", provider="anthropic")
    print(result)

Env vars (set yang dipakai saja):
    ANTHROPIC_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, KIMI_API_KEY, DEEPSEEK_API_KEY

Risk: Medium (network call to external API, requires API key)
"""

import os
import sys
import json
import argparse
import time
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library missing. Install: pip install requests", file=sys.stderr)
    sys.exit(1)


# Provider config registry
PROVIDERS = {
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "key_env": "ANTHROPIC_API_KEY",
        "default_model": "claude-sonnet-4-20250514",
        "auth_style": "anthropic",  # x-api-key + anthropic-version
    },
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "default_model": "anthropic/claude-sonnet-4-20250514",
        "auth_style": "bearer",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4o",
        "auth_style": "bearer",
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "key_env": "GROQ_API_KEY",
        "default_model": "llama-3.1-70b-versatile",
        "auth_style": "bearer",
    },
    "kimi": {
        "url": "https://api.moonshot.cn/v1/chat/completions",
        "key_env": "KIMI_API_KEY",
        "default_model": "moonshot-v1-128k",
        "auth_style": "bearer",
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key_env": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
        "auth_style": "bearer",
    },
}


def call_llm(
    message: str,
    system: str = "You are a helpful assistant.",
    provider: str = "anthropic",
    model: Optional[str] = None,
    max_tokens: int = 1024,
    timeout: int = 60,
    max_retries: int = 2,
) -> str:
    """
    Call an LLM provider with unified interface.

    Returns: response text (string).
    Raises: RuntimeError on failure after retries.
    """
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(PROVIDERS.keys())}")

    cfg = PROVIDERS[provider]
    api_key = os.getenv(cfg["key_env"])
    if not api_key:
        raise RuntimeError(f"Missing env var: {cfg['key_env']}")

    use_model = model or cfg["default_model"]

    # Build headers + body per auth style
    if cfg["auth_style"] == "anthropic":
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
        body = {
            "model": use_model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": message}],
        }
    else:  # bearer (OpenAI-compatible)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body = {
            "model": use_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            "max_tokens": max_tokens,
        }

    # Retry loop
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(cfg["url"], json=body, headers=headers, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            # Parse per provider response shape
            if cfg["auth_style"] == "anthropic":
                return data["content"][0]["text"]
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            raise RuntimeError(f"LLM call failed after {max_retries + 1} attempts: {e}") from e

    raise RuntimeError(f"Unreachable: {last_error}")


def main():
    parser = argparse.ArgumentParser(description="LLM Multi-Provider Client")
    parser.add_argument("--provider", default="anthropic",
                        choices=list(PROVIDERS.keys()),
                        help="LLM provider to use")
    parser.add_argument("--model", help="Model name (override default)")
    parser.add_argument("--system", default="You are a helpful assistant.",
                        help="System prompt")
    parser.add_argument("--message", required=True, help="User message")
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of plain text")
    args = parser.parse_args()

    try:
        result = call_llm(
            message=args.message,
            system=args.system,
            provider=args.provider,
            model=args.model,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        if args.json:
            print(json.dumps({"provider": args.provider, "ok": True, "output": result}))
        else:
            print(result)
    except Exception as e:
        if args.json:
            print(json.dumps({"provider": args.provider, "ok": False, "error": str(e)}))
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 5b. Buat `knowledge/ml/llm-providers.md` (provider selection guide)

```markdown
# LLM Provider Selection Guide

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (`@nexusai.ml`) + Operator
Source: Adapted from SUPERAGENT v2 m7.md
Tool: `tools/llm_client.py` (TOOL-033)

---

## Purpose

Guide untuk memilih LLM provider berdasarkan use case di AI Holding.
Multi-provider supaya tidak lock-in ke 1 vendor + bisa optimize cost vs quality per task.

---

## Provider Comparison

| Provider | Best For | Speed | Cost | Context | Risk Level |
|----------|----------|-------|------|---------|-----------|
| **Anthropic (Claude)** | Research synthesis, nuanced reasoning, content polish | Medium | High | 200k | Low |
| **OpenAI (GPT-4o)** | Multimodal (image+text), structured output | Medium | High | 128k | Low |
| **Groq (Llama 3.1)** | Real-time classification, fast routing decisions | Ultra-fast | Low | 128k | Medium |
| **Kimi (Moonshot)** | Long document analysis, large file processing | Slow | Medium | 128k+ | Medium (CN-based) |
| **DeepSeek** | Bulk content generation, coding tasks | Fast | Very Low | 64k | Medium |
| **OpenRouter** | Multi-model gateway (access semua via 1 key) | Variable | Variable | Variable | Low |

---

## Use Case → Provider Mapping (Per Company)

### Crypto Consultant
| Task | Provider | Reason |
|------|----------|--------|
| Research synthesis (6-layer) | Anthropic Claude | Best reasoning, nuanced output |
| News scan / sentiment | Groq | Fast, bulk processing |
| Long-form methodology docs | Kimi | Long context (literature review) |
| Forecast Ledger entry generation | DeepSeek | Cheap, structured |

### BrandFlow
| Task | Provider | Reason |
|------|----------|--------|
| Hook generation (variations) | Anthropic Claude | Voice nuance |
| Bulk caption variants | DeepSeek | Cheap, volume |
| Brand voice linting | Groq | Fast classification |
| Long-form blog drafts | Kimi | Long context for SEO research |

### NexusAI
| Task | Provider | Reason |
|------|----------|--------|
| Code generation | DeepSeek (coder) | Specialist, cheap |
| Architecture review | Anthropic Claude | Nuanced reasoning |
| Bug triage / classification | Groq | Fast routing |
| API doc generation | DeepSeek | Cheap, structured |

---

## Tool Usage

### CLI

```bash
# Quick test (Claude default)
python tools/llm_client.py --message "Halo, jelaskan Boundary #4 dengan singkat"

# Pakai Groq untuk speed
python tools/llm_client.py --provider groq --message "Klasifikasikan: BTC turun 5%"

# Pakai system prompt
python tools/llm_client.py --provider deepseek \
  --system "Anda adalah copywriter BrandFlow, voice bold tapi data-first" \
  --message "Tulis 3 hook untuk Twitter tentang ETF inflow $340M"

# JSON output (untuk pipeline)
python tools/llm_client.py --provider groq --message "Halo" --json
```

### Import dari Python script

```python
from tools.llm_client import call_llm

result = call_llm(
    message="Translate to Indonesian: Bear case first",
    system="You are a precise translator. Output only the translation.",
    provider="groq",
)
print(result)
```

---

## Cost-Aware Routing Pattern

Default approach untuk autonomous operations:

```python
def smart_route(task_type, content):
    """Cost-aware provider selection."""
    if task_type == "classify":
        return call_llm(content, provider="groq")  # fast + cheap
    if task_type == "research_synthesis":
        return call_llm(content, provider="anthropic")  # quality
    if task_type == "bulk_content":
        return call_llm(content, provider="deepseek")  # cheap
    if task_type == "long_doc":
        return call_llm(content, provider="kimi")  # context
    return call_llm(content, provider="anthropic")  # default
```

---

## Setup

### Environment variables

Tambahkan ke `.env` (jangan commit):

```bash
# Pilih yang dipakai saja, tidak perlu semua
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
KIMI_API_KEY=...
DEEPSEEK_API_KEY=...
```

### Dependencies

```bash
pip install requests  # only dependency
```

### Smoke test

```bash
python tools/llm_client.py --provider groq --message "ping"
# Expected: short response, exit 0
```

---

## Rules

1. **Never hardcode API keys.** Selalu via env var.
2. **Never bypass cost-aware routing untuk bulk tasks.** Pakai cheap provider.
3. **Always set timeout.** Default 60s, lower untuk routing decisions.
4. **Log usage.** Untuk track cost per company per task (future: tools/llm_usage_logger.py).
5. **Boundary #4 awareness.** Output dari LLM yang akan publish ke public surface tetap perlu Fathur approval. LLM call itself = Tier 1 autonomous.

---

## Reference

- Source: `update/v2/openclaw/skills/m7.md`
- Tool: `tools/llm_client.py` (TOOL-033)
- Tool registry: `knowledge/tools/tool-registry.md`
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
```

### 5c. Update `knowledge/tools/tool-registry.md`

Append entry di bagian active tools:

```
TOOL-033 | tools/llm_client.py | LLM multi-provider client (Anthropic/OpenAI/Groq/Kimi/DeepSeek/OpenRouter) | Active | Risk: Medium (external API calls, requires API key) | Owner: @nexusai.ml | Doc: knowledge/ml/llm-providers.md
```

**Verify:**
```bash
test -f tools/llm_client.py && echo "5a ok"
test -f knowledge/ml/llm-providers.md && echo "5b ok"
grep -q "TOOL-033" knowledge/tools/tool-registry.md && echo "5c ok"
python -c "import ast; ast.parse(open('tools/llm_client.py').read())" && echo "syntax ok"
```

---

## STEP 6 — Update HEARTBEAT.md (Tier B)

**Source pattern:** `update/v2/openclaw/HEARTBEAT.md`
**Adapt:** Tambahkan reference ke skill registry + reflection loop

Tulis ulang `HEARTBEAT.md`:

```markdown
# HEARTBEAT.md — Pre-Session Checklist

Versi: 2.0
Updated: 2026-05-17 (post upgrade dari SUPERAGENT v2 patterns)

> Keep SHORT. Runs every heartbeat. Token burn is real.

---

## On Session Start

```
[ ] Read MAIN_SOUL.md (always-on identity)
[ ] Read MEMORY.md (holding strategic state)
[ ] Read memory/[YYYY-MM-DD].md (today's tagged log) jika ada
[ ] Identify routing: pseudo-mention (@x.y) atau natural command
[ ] Load relevant skill(s) on demand — bukan full company on session start
[ ] Apply Reflection Loop sebelum output (knowledge/agent-design/reflection-loop.md)
```

## Resume Logic

- Notify operator if: task pending > 24h tanpa update
- Resume context if: session continues from previous (cek `memory/global.md` last 24h)

## Boundary #4 Reminder

Setiap session:
- Public surface output → Tier 3 (Fathur approval)
- Internal/Fathur-only → Tier 1/2 (autonomous)
- Cek `knowledge/sop/autonomous-boundaries.md` saat ragu

## Reference

- Adapted from: `update/v2/openclaw/HEARTBEAT.md`
- Reflection loop: `knowledge/agent-design/reflection-loop.md`
- Routing: `MAIN.md` + `COMMANDS.md`
```

**Verify:** `head -5 HEARTBEAT.md | grep -q "Versi: 2.0" && echo "step 6 ok"`

---

## STEP 7 — Cleanup (Final)

Setelah semua step di atas verified:

### 7a. Pindahkan source folder ke archive

```bash
mkdir -p docs/external-references
git mv update docs/external-references/superagent-v2
```

### 7b. Update commit message untuk audit trail

```bash
git add -A
git commit -m "feat: cherry-pick SUPERAGENT v2 patterns

Tier A — Adopted (4 files):
- knowledge/agent-design/reflection-loop.md (5-Q self-check + Boundary #4)
- knowledge/sop/debug-protocol.md (6-step diagnose+fix+harden)
- knowledge/sop/system-audit.md (4-layer weekly audit)
- knowledge/sop/strategic-thinking.md (5-step decomposition)

Tier B — Adopted (3 files):
- tools/llm_client.py (TOOL-033, 5 providers)
- knowledge/ml/llm-providers.md (selection guide + use cases)
- HEARTBEAT.md (v2.0 with skill registry + reflection ref)

NOT adopted (incompatible with Boundary #4 / inferior):
- Flexibility Doctrine, IDENTITY rebrand, keyword router, single-brain arch

Source archived: docs/external-references/superagent-v2/
Original analysis: docs/external-references/superagent-v2/ANALYSIS.md"
```

---

## Final Verification Checklist

Hermes lapor di akhir:

```
✅ Step 1: knowledge/agent-design/reflection-loop.md created
✅ Step 2: knowledge/sop/debug-protocol.md created
✅ Step 3: knowledge/sop/system-audit.md created
✅ Step 4: knowledge/sop/strategic-thinking.md created
✅ Step 5a: tools/llm_client.py created (syntax valid)
✅ Step 5b: knowledge/ml/llm-providers.md created
✅ Step 5c: knowledge/tools/tool-registry.md updated (TOOL-033 added)
✅ Step 6: HEARTBEAT.md updated to v2.0
✅ Step 7a: update/ moved to docs/external-references/superagent-v2/
✅ Step 7b: committed

Total files added: 6
Total files modified: 2 (HEARTBEAT.md, tool-registry.md)
Total files relocated: 22 (update/v2/openclaw/* → docs/external-references/superagent-v2/v2/openclaw/*)

Branch: feat/upgrade-cherry-pick-superagent
Ready to push + PR: yes
```

---

## What Was NOT Adopted (For Audit Trail)

Hermes harus aware bahwa item-item ini SENGAJA tidak diadopsi:

| Item | Source | Reason |
|------|--------|--------|
| Flexibility Doctrine | `update/v2/openclaw/SOUL.md` | Bertabrakan dengan Boundary #4 |
| IDENTITY rebrand ke "SUPERAGENT" | `update/v2/openclaw/IDENTITY.md` | Identity per-company kita lebih kuat |
| Keyword router | `update/v2/openclaw/AGENTS.md` | Inferior to pseudo-mention `@company.agent` |
| Single MEMORY format | `update/v2/openclaw/MEMORY.md` | Kita punya layered memory (holding + global + 3× company) |
| m1 (Monetization) | `update/v2/openclaw/skills/m1.md` | Out of scope untuk AI Holding |
| m2 (VPS/DevOps) | `update/v2/openclaw/skills/m2.md` | NexusAI `skills/devops/` lebih dalam |
| m3 (Content) | `update/v2/openclaw/skills/m3.md` | BrandFlow `skills/content/` lebih dalam |
| m4 (Automation) | `update/v2/openclaw/skills/m4.md` | NexusAI handles, akan terbangun di Tier 1 autonomous execution work |
| m5 (Data) | `update/v2/openclaw/skills/m5.md` | Crypto Consultant `skills/research` punya pieces |
| m6 (API integration) | `update/v2/openclaw/skills/m6.md` | NexusAI handle ad-hoc |
| m8 (File generation) | `update/v2/openclaw/skills/m8.md` | Ad-hoc per company |
| m9 (Frontend) | `update/v2/openclaw/skills/m9.md` | NexusAI `skills/uiux/` lebih dalam |

---

## Stop Conditions

Hermes harus STOP dan lapor operator KALAU:

- Pre-flight check fail (source missing, target dir tidak bisa dibuat)
- Step 5a: Python syntax error di llm_client.py
- Step 7a: `git mv` fail (uncommitted changes di update/)
- Verifikasi step apapun fail
- Conflict dengan existing file (kecuali HEARTBEAT.md yang memang di-overwrite)

Format laporan stop:
```
🛑 UPGRADE STOPPED at Step <N>
Reason: <specific>
Action needed: <what operator should do>
Recovery: <how to resume after fix>
```

---

## Post-Upgrade

Setelah PR merged:

1. Pull di Hermes mesin: `git pull origin main`
2. Test smoke: `python tools/llm_client.py --provider groq --message "ping"` (perlu env GROQ_API_KEY)
3. Schedule di weekly cadence: System Audit Friday slot sudah otomatis aktif via reference di `weekly-cadence.md` (no edit needed — already mentions Friday recap)
4. Update PR description dengan link ke `docs/external-references/superagent-v2/ANALYSIS.md` untuk audit trail

---

**END OF UPGRADE.md**

Total estimated execution time untuk Hermes: ~5-8 minit.
Total file impact: 6 added, 2 modified, 22 relocated.
