# UPGRADE.md — Hermes Auto-Upgrade Command Sheet

> **Cara pakai:** Kirim ke Hermes: **`jalankan upgrade dari UPGRADE.md`** atau **`run upgrade UPGRADE.md`**.
> Hermes baca file ini, jalankan setiap step urutan dari atas ke bawah, lalu lapor hasil.

---

## Tentang Upgrade Ini

**Source:** `update/v2/openclaw/` (SUPERAGENT v2 brain system)
**Strategy:** **Comprehensive Cherry-Pick** — ambil semua yang berguna sekarang + future-proof reference untuk yang belum dibutuhkan. Tidak replace existing system mana pun.
**Filosofi:** Sistem multi-company kita (Root SOUL → Tier 2 → Tier 3 + Boundary #4) **tetap autoritatif**. SUPERAGENT hanya memberi tools/SOPs/cookbook tambahan.

**Total: 13 step. Estimasi eksekusi: 12-18 menit.**

### Peta Step

```
TIER A — Generic SOP layer (4 steps)
  1. Reflection Loop
  2. Debug Protocol
  3. System Audit Protocol
  4. Strategic Thinking Protocol

TIER B — Infrastructure tools (2 steps)
  5. LLM Multi-Provider Client (m7) + API Integration Patterns (m6)
  6. HEARTBEAT.md v2.0

TIER C — Cookbooks & Future-Use (6 steps)
  7. DevOps Cookbook (m2 snippets — Nginx, Certbot, PM2)
  8. Automation Templates (m4 — Telegram bot, cron, FastAPI) ⭐ runnable code
  9. Data Analysis Protocol (m5)
  10. Artifact Generation Cookbook (m8)
  11. Marketing Landing Architecture (m9 — 8-section template untuk BrandFlow)
  12. Monetization Reference (m1 — for future business consulting work)

CLEANUP (1 step)
  13. Archive update/ folder + commit
```

---

## Pre-Flight Check (Wajib)

Hermes harus verify dulu sebelum mulai:

```bash
# 1. Pastikan di branch yang benar
git status
# Expected: clean working tree, on main (or feature branch from main)

# 2. Pastikan source file ada
test -d update/v2/openclaw && echo "source ok" || echo "source missing — abort"

# 3. Pastikan target dirs ada (akan dibuat kalau belum ada)
test -d knowledge/sop && echo "sop ok" || mkdir -p knowledge/sop
test -d knowledge/agent-design && echo "agent-design ok" || mkdir -p knowledge/agent-design
test -d tools && echo "tools ok" || mkdir -p tools
test -d knowledge/ml && echo "ml ok" || mkdir -p knowledge/ml
test -d knowledge/software && echo "software ok" || mkdir -p knowledge/software
test -d knowledge/marketing && echo "marketing ok" || mkdir -p knowledge/marketing
test -d knowledge/business && echo "business ok" || mkdir -p knowledge/business
test -d tools/templates && echo "templates ok" || mkdir -p tools/templates
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

## STEP 7 — DevOps Cookbook (Tier C — m2 snippets)

**File baru:** `knowledge/software/devops-cookbook.md`
**Source:** `update/v2/openclaw/skills/m2.md`
**Adapt:** Snippet library, BUKAN replace `companies/nexusai/skills/devops/SKILL.md`

Tulis file ini:

```markdown
# DevOps Cookbook — Snippet Library

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (`@nexusai.devops`) — referensi cookbook
Source: Adapted from SUPERAGENT v2 m2.md
Replaces: NOTHING — `companies/nexusai/skills/devops/SKILL.md` tetap autoritatif

---

## Purpose

Library bash snippets untuk infrastructure tasks yang sering muncul.
Snippet ini sudah tested, tinggal paste-adapt-run.

NexusAI devops SKILL.md tetap pegang kendali keputusan (when to deploy, what env, security review). Cookbook ini hanya implementation reference.

---

## A. Environment Bootstrap (Debian/Ubuntu)

```bash
# Update + essentials + firewall
apt update && apt upgrade -y
apt install -y curl wget git unzip nano htop ufw fail2ban
ufw allow 22 && ufw allow 80 && ufw allow 443 && ufw --force enable
```

---

## B. Node.js + PM2 Stack

```bash
# Node 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# PM2 + auto-start on reboot
npm install -g pm2
pm2 startup systemd
pm2 save
```

---

## C. Python venv Stack

```bash
apt install -y python3 python3-pip python3-venv
python3 -m venv /opt/venv
source /opt/venv/bin/activate
# pip install -r requirements.txt
```

---

## D. Nginx + Certbot SSL (Let's Encrypt)

```bash
# Install
apt install -y nginx certbot python3-certbot-nginx
systemctl enable nginx

# Free SSL cert (replace placeholders)
certbot --nginx -d <domain.tld> --non-interactive --agree-tos -m <email@domain.tld>
```

### Nginx reverse proxy template

```nginx
# /etc/nginx/sites-available/<app>
server {
    listen 80;
    server_name <domain.tld>;

    location / {
        proxy_pass http://localhost:<PORT>;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## E. Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com | bash
systemctl enable docker
usermod -aG docker $USER
# logout-login supaya group berlaku
```

---

## F. Deployment Sequences

### Node.js app

```bash
git clone <url> <dir>
cd <dir>
npm install --production
pm2 start index.js --name "<id>"
pm2 save
```

### Python ASGI (FastAPI/Starlette)

```bash
pm2 start "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000" \
  --name "<id>"
pm2 save
```

### Static site

```bash
cp -r dist/* /var/www/html/
nginx -t && systemctl reload nginx
```

---

## G. Instrumentation (Real-Time Diagnostics)

```bash
# Resource usage
htop
df -h

# PM2 process status
pm2 monit
pm2 logs <id>

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Network ports
netstat -tlnp
ss -tlnp

# System journal
journalctl -xe
journalctl -u nginx -f
```

---

## H. Common Recipe — Deploy Node.js App with HTTPS

```bash
# 1. Bootstrap (skip if already done)
apt update && apt install -y nginx certbot python3-certbot-nginx
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs && npm install -g pm2

# 2. Clone + install
git clone <repo-url> /opt/<app>
cd /opt/<app> && npm install --production

# 3. Run
pm2 start index.js --name "<app>"
pm2 startup systemd && pm2 save

# 4. Reverse proxy
cat > /etc/nginx/sites-available/<app> <<EOF
server {
    listen 80;
    server_name <domain.tld>;
    location / { proxy_pass http://localhost:3000; proxy_set_header Host \$host; }
}
EOF
ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 5. SSL
certbot --nginx -d <domain.tld> --non-interactive --agree-tos -m <email>
```

Total: ~5 minit untuk fresh server → live HTTPS app.

---

## Constraints

- Snippet ini reference, BUKAN SOP. Decisional authority tetap di `companies/nexusai/skills/devops/SKILL.md`.
- Production deploy = Tier 3 (butuh Fathur approval per `autonomous-boundaries.md`).
- Selalu test di staging dulu kalau bisa.
- `<placeholder>` di snippet = wajib diganti, bukan literal.

---

## Reference

- Source: `update/v2/openclaw/skills/m2.md`
- Authority: `companies/nexusai/skills/devops/SKILL.md`
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
- Debug: `knowledge/sop/debug-protocol.md`
```

**Verify:** `test -f knowledge/software/devops-cookbook.md && echo "step 7 ok"`

---

## STEP 8 — Automation Templates (Tier C — m4) ⭐

**Files baru:**
- `tools/templates/telegram_bot.js` (runnable Telegram bot)
- `tools/templates/cron_examples.txt` (crontab patterns)
- `tools/templates/fastapi_webhook.py` (FastAPI trigger receiver)
- `knowledge/software/automation-cookbook.md` (penjelasan + usage)

**Source:** `update/v2/openclaw/skills/m4.md`
**Adapt:** Production-ready dengan error handling + .env.example

### 8a. `tools/templates/telegram_bot.js`

```javascript
/**
 * Telegram Bot Template — Runnable
 *
 * Usage:
 *   1. cp .env.example .env
 *   2. Set TOKEN=... (get from @BotFather)
 *   3. npm install node-telegram-bot-api dotenv
 *   4. node tools/templates/telegram_bot.js
 *
 * For production: pm2 start tools/templates/telegram_bot.js --name <bot-name>
 *
 * Source: Adapted from SUPERAGENT v2 m4.md
 */

require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');

const TOKEN = process.env.TOKEN;
if (!TOKEN) {
  console.error('ERROR: TOKEN env var missing. Set in .env file.');
  process.exit(1);
}

const bot = new TelegramBot(TOKEN, { polling: true });

console.log('✅ Bot online. Polling for messages...');

// /start
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    '✅ Online.\n\nAvailable commands:\n/help — show all commands\n/status — system status'
  );
});

// /help
bot.onText(/\/help/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    '*Commands:*\n' +
    '/start — bot greeting\n' +
    '/help — this menu\n' +
    '/status — current status\n' +
    '/run [cmd] — execute command',
    { parse_mode: 'Markdown' }
  );
});

// /status
bot.onText(/\/status/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    `📊 *Status*\nTime: ${new Date().toISOString()}\nUptime: ${process.uptime()}s`,
    { parse_mode: 'Markdown' }
  );
});

// /run <command>
bot.onText(/\/run (.+)/, (msg, match) => {
  const command = match[1];
  // PRODUCTION: validate user against allowlist before executing
  bot.sendMessage(msg.chat.id, `Received: \`${command}\``, { parse_mode: 'Markdown' });
});

// Generic message handler (non-commands)
bot.on('message', (msg) => {
  if (msg.text && !msg.text.startsWith('/')) {
    bot.sendMessage(msg.chat.id, `Echo: "${msg.text}"`);
  }
});

// Error handling
bot.on('polling_error', (err) => {
  console.error('Polling error:', err.message);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down bot...');
  bot.stopPolling();
  process.exit(0);
});
```

### 8b. `tools/templates/cron_examples.txt`

```
# Cron Patterns — Common Schedules
# Edit with: crontab -e
# Test syntax: crontab -l
#
# Format: minute hour day-of-month month day-of-week command
#         (0-59) (0-23) (1-31)       (1-12) (0-6, 0=Sun)
#
# Source: Adapted from SUPERAGENT v2 m4.md

# === DAILY SCHEDULES ===

# Every day at 08:00 — daily report
0 8 * * * /usr/bin/python3 /opt/run/daily.py >> /var/log/daily.log 2>&1

# Every day at 23:00 — backup
0 23 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

# === WEEKLY SCHEDULES ===

# Every Monday at 07:00 — weekly crypto brief (matches weekly-cadence.md)
0 7 * * 1 /opt/ai-holding/bin/run_weekly_brief.sh >> /var/log/weekly.log 2>&1

# Every Friday at 09:00 — weekly recap
0 9 * * 5 /opt/ai-holding/bin/run_weekly_recap.sh >> /var/log/recap.log 2>&1

# === HOURLY SCHEDULES ===

# Every hour — health check
0 * * * * /bin/bash /opt/run/health-check.sh

# Every 5 minutes — short-interval monitor
*/5 * * * * /usr/bin/node /opt/run/monitor.js

# === SPECIFIC TIMES (WIB-aware, server in UTC) ===

# Crypto tools refresh at 07:00 WIB = 00:00 UTC
0 0 * * * /opt/ai-holding/bin/run_crypto_tools.sh

# Approval reminder check at 13:00 WIB = 06:00 UTC
0 6 * * * /opt/ai-holding/bin/check_pending_approvals.sh

# === TIPS ===
# - Always redirect both stdout and stderr to log: >> /var/log/<name>.log 2>&1
# - Use absolute paths (cron PATH is minimal)
# - Test scripts manually first: bash -x /path/to/script.sh
# - Check cron is running: systemctl status cron
```

### 8c. `tools/templates/fastapi_webhook.py`

```python
#!/usr/bin/env python3
"""
FastAPI Webhook Receiver Template — Runnable

Usage:
    pip install fastapi uvicorn
    uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000

For production:
    pm2 start "uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000" \
        --name webhook-receiver

Test:
    curl -X POST http://localhost:8000/trigger \
      -H "Content-Type: application/json" \
      -d '{"type": "input.received", "payload": {"hello": "world"}}'

Source: Adapted from SUPERAGENT v2 m4.md
"""

import os
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Webhook Receiver", version="1.0")

# Optional: shared-secret signature verification
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


# === Event handlers ===

async def on_exchange_complete(data: dict):
    """Handle 'exchange.complete' events (e.g., payment confirmed)."""
    logger.info(f"Exchange complete: {data.get('payload')}")
    # ADD YOUR LOGIC HERE


async def on_input_received(data: dict):
    """Handle 'input.received' events (generic input trigger)."""
    logger.info(f"Input received: {data.get('payload')}")
    # ADD YOUR LOGIC HERE


async def on_unknown(data: dict):
    """Fallback for unmapped event types."""
    logger.warning(f"Unknown event type: {data.get('type')}")


# Event router
EVENT_HANDLERS = {
    "exchange.complete": on_exchange_complete,
    "input.received": on_input_received,
}


# === Endpoints ===

@app.get("/")
async def root():
    return {"status": "ok", "service": "webhook-receiver", "ts": datetime.utcnow().isoformat()}


@app.get("/health")
async def health():
    return {"healthy": True, "ts": datetime.utcnow().isoformat()}


@app.post("/trigger")
async def trigger(
    request: Request,
    x_webhook_secret: Optional[str] = Header(None),
):
    """Main webhook receiver. Routes by event 'type' field."""

    # Optional secret verification
    if WEBHOOK_SECRET and x_webhook_secret != WEBHOOK_SECRET:
        logger.warning("Webhook called with invalid secret")
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    event_type = data.get("type")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing 'type' field")

    handler = EVENT_HANDLERS.get(event_type, on_unknown)
    try:
        await handler(data)
    except Exception as e:
        logger.exception(f"Handler error for {event_type}")
        raise HTTPException(status_code=500, detail=f"Handler error: {e}")

    return JSONResponse({"ack": True, "type": event_type, "ts": datetime.utcnow().isoformat()})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 8d. `knowledge/software/automation-cookbook.md`

```markdown
# Automation Cookbook — Runnable Templates

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (`@nexusai.automation` patterns)
Source: Adapted from SUPERAGENT v2 m4.md

---

## Purpose

Production-ready automation templates yang **paste-and-run**. Cocok untuk:
- Tier 1 autonomous execution layer (Hermes weekly cadence triggers)
- Telegram bot untuk approval workflow (`approval-workflow.md`)
- Webhook receivers untuk cross-company event routing
- Cron schedules untuk weekly cadence (`weekly-cadence.md`)

---

## Templates Tersedia

| Template | File | Use Case |
|----------|------|----------|
| Telegram Bot | `tools/templates/telegram_bot.js` | Approval flow, /status, /run commands |
| Cron Patterns | `tools/templates/cron_examples.txt` | Weekly cadence triggers, daily schedules |
| FastAPI Webhook | `tools/templates/fastapi_webhook.py` | Event-driven triggers, GitHub webhooks |

---

## Pattern A: Telegram Approval Bot

Mapping ke `approval-workflow.md`:
1. Hermes generate APPROVAL REQUEST
2. Bot kirim ke Fathur via Telegram
3. Fathur reply yes/no/revise
4. Bot capture response, return ke Hermes via shared file/state

Setup minimum:
```bash
npm install node-telegram-bot-api dotenv
echo "TOKEN=<from-botfather>" > .env
node tools/templates/telegram_bot.js
```

Production:
```bash
pm2 start tools/templates/telegram_bot.js --name approval-bot
pm2 save
```

---

## Pattern B: Weekly Cadence via Cron

Per `knowledge/sop/weekly-cadence.md`, schedule ini di server Hermes:

```bash
# crontab -e (server in UTC)

# Monday 07:00 WIB = 00:00 UTC — weekly crypto brief production
0 0 * * 1 /opt/ai-holding/bin/run_weekly_brief.sh >> /var/log/weekly.log 2>&1

# Friday 09:00 WIB = 02:00 UTC — weekly recap
0 2 * * 5 /opt/ai-holding/bin/run_weekly_recap.sh >> /var/log/recap.log 2>&1

# Daily 07:00 WIB — crypto tools refresh
0 0 * * * /opt/ai-holding/bin/run_crypto_tools.sh >> /var/log/tools.log 2>&1
```

---

## Pattern C: Webhook Receiver for Cross-Company Events

FastAPI receiver untuk handle:
- GitHub webhook (PR merged → trigger update on Hermes)
- External API callbacks
- Inter-company event triggers

Setup:
```bash
pip install fastapi uvicorn
uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000
```

Production:
```bash
pm2 start "uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000" \
  --name webhook-receiver
```

Reverse proxy via Nginx → Lihat `knowledge/software/devops-cookbook.md`.

---

## Distribution Pipeline Pattern

Untuk weekly content yang ada di BrandFlow:

```
QUEUE (BrandFlow tasks/inbox.jsonl)
   ↓
SCHEDULER (cron + queue worker)
   ↓
DELIVERY_LAYER (Telegram → Fathur approval → publish)
   ↓
CONFIRMATION + LOG (memory/global.md + tasks/logs.jsonl)
   ↑
GENERATOR (Crypto Consultant research → BrandFlow translation)
```

---

## Constraints

- Selalu pakai `.env` untuk secrets (jangan hardcode)
- Production deploy = Tier 3 (Fathur approval)
- Validate user authorization sebelum eksekusi command via bot
- Log semua trigger ke `tasks/logs.jsonl` per task-logger-rules
- Webhook receivers WAJIB signature verification (lihat fastapi_webhook.py optional secret)

---

## Reference

- Source: `update/v2/openclaw/skills/m4.md`
- Templates: `tools/templates/`
- DevOps: `knowledge/software/devops-cookbook.md`
- Approval: `knowledge/sop/approval-workflow.md`
- Cadence: `knowledge/sop/weekly-cadence.md`
```

**Verify:**
```bash
test -f tools/templates/telegram_bot.js && echo "8a ok"
test -f tools/templates/cron_examples.txt && echo "8b ok"
test -f tools/templates/fastapi_webhook.py && echo "8c ok"
test -f knowledge/software/automation-cookbook.md && echo "8d ok"
python -c "import ast; ast.parse(open('tools/templates/fastapi_webhook.py').read())" && echo "py syntax ok"
node -c "const fs = require('fs'); new Function(fs.readFileSync('tools/templates/telegram_bot.js', 'utf8'))" 2>/dev/null && echo "js syntax ok" || echo "js skip (node not available)"
```

---

## STEP 9 — Data Analysis Protocol (Tier C — m5)

**File baru:** `knowledge/sop/data-analysis-protocol.md`
**Source:** `update/v2/openclaw/skills/m5.md`
**Used by:** `@brandflow.analytics`, `@crypto.data`, ad-hoc cross-company reporting

Tulis file ini:

```markdown
# Data Analysis Protocol — SCOPE→PRESCRIBE Flow

Versi: 1.0
Created: 2026-05-17
Owner: `@brandflow.analytics` + `@crypto.data` + Operator
Source: Adapted from SUPERAGENT v2 m5.md

---

## Purpose

6-step protocol untuk transform raw data → actionable prescription.
Reusable cross-company. Setiap analysis output WAJIB akhiri dengan exactly 3 prescriptions.

---

## When To Use

- BrandFlow analytics weekly review (engagement metrics, content performance)
- Crypto Consultant data work (`@crypto.data` aggregations)
- Cross-company performance reporting (weekly recap data)
- Any "analyze this CSV/spreadsheet/log" request

NOT untuk:
- Crypto research synthesis (sudah ada 6-layer format)
- Real-time monitoring alerts (sudah ada threshold triggers)

---

## The 6 Steps

### Step 1 — SCOPE

```
Pertanyaan exact yang dijawab:
  → "What's the engagement rate trend WoW for crypto-influencer client?"
  → BUKAN: "Analyze the data"

Output: 1 sentence question.
```

Salah scope = analysis useless.

---

### Step 2 — ACQUIRE

```
Required inputs:    [list]
Available inputs:   [list]
Gap:                [missing data + plan to fill or work-around]
```

Identify gap dulu. Don't proceed dengan asumsi.

---

### Step 3 — NORMALIZE

```
Steps:
- Deduplicate
- Reformat (consistent units, datetime, currency)
- Handle nulls (drop / impute / flag)
- Outlier handling (cap / remove / investigate)
```

Show work. Reproducibility matters.

---

### Step 4 — PROCESS

```
Patterns:    [trend, seasonality, correlation]
Anomalies:   [outliers, breaks]
Segments:    [groupby analysis]
Deltas:      [period-over-period change %]
```

**Rule:** Always include delta/trend. Snapshot alone is insufficient.

---

### Step 5 — RENDER

```
Visualization:  chart / table / sparkline (per appropriate)
Summary:       narrative paragraph (3-5 sentences)
Output file:   actual artifact (CSV/XLSX/MD), not inline preview
Path:          companies/<company>/tasks/analysis-YYYY-MM-DD.<ext>
```

Reference template (Python/pandas):

```python
import pandas as pd

df = pd.read_csv('input.csv')
print(df.describe(), df.isnull().sum())

# Aggregate per segment
out = df.groupby('segment')['value'].agg(
    total='sum',
    avg='mean',
    n='count',
)

# Multi-sheet output
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as w:
    out.to_excel(w, sheet_name='Summary')
    df.to_excel(w, sheet_name='Source', index=False)

print("✅ output.xlsx ready")
```

---

### Step 6 — PRESCRIBE

**Always exactly 3 prescriptions.** Specific, executable, owned.

```
[PRESCRIPTION 1]
  What:   <action>
  Owner:  <agent>
  When:   <by date>
  Expected impact: <metric → target>

[PRESCRIPTION 2] ...
[PRESCRIPTION 3] ...
```

3 = enough untuk prioritization, tidak overwhelming.

---

## Performance Indicators (Quick Reference)

```
throughput:   total + period-over-period delta %
activity:     active + new + lapsed units
efficiency:   input → qualified → converted %
acquisition:  cost per new unit
retention:    lifetime yield per unit
return:       output / input ratio %
```

Pick 3-5 yang relevan untuk question. Don't dump all 6.

---

## Output Format

```
[ANALYSIS — YYYY-MM-DD]
Question: <1 sentence>
Period:   <date range>
Source:   <data origin>

[KEY FACTS]
- <data point + delta>
- <data point + delta>

[PATTERNS]
- <observation>

[ANOMALIES]
- <if any>

[3 PRESCRIPTIONS]
1. <action> — owner — by date — impact
2. <action> — owner — by date — impact
3. <action> — owner — by date — impact

[ARTIFACT]
Path: <output file>

[CAVEATS]
- <data limitations>
- <interpretation caveats>
```

---

## Boundary #4 Awareness

Kalau analysis hasilnya akan dipublish/share keluar:
- Tier 3 → butuh Fathur approval
- Tetap perlu disclaimer kalau data finansial

Internal-only analysis (Fathur reads, no publish) → Tier 1/2.

---

## Anti-Patterns (Jangan Lakukan)

❌ Skip Step 1 (scope) — gampang answer wrong question.
❌ Snapshot tanpa delta — current state tidak useful tanpa trend.
❌ More than 3 prescriptions — focus dilution.
❌ Inline-only output — actual file artifact required untuk reproduceability.
❌ Skip caveats — lebih baik hedge yang fair daripada confident-and-wrong.
❌ Mix factual + speculative — separate jelas.

---

## Reference

- Source: `update/v2/openclaw/skills/m5.md`
- Used by: `@brandflow.analytics`, `@crypto.data`
- Complementary: `companies/crypto-consultant/skills/research/SKILL.md` (untuk crypto research synthesis berbeda)
- Tools: `tools/llm_client.py` untuk text-heavy analysis
```

**Verify:** `test -f knowledge/sop/data-analysis-protocol.md && echo "step 9 ok"`

---

## STEP 10 — Artifact Generation Cookbook (Tier C — m8)

**File baru:** `knowledge/software/artifact-generation-cookbook.md`
**Source:** `update/v2/openclaw/skills/m8.md`

Tulis file ini:

```markdown
# Artifact Generation Cookbook — File Output Templates

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (technical) + cross-company (template usage)
Source: Adapted from SUPERAGENT v2 m8.md

---

## Purpose

Reference cookbook untuk render output ke berbagai format file.
Reusable saat ada client work, external delivery, atau Fathur butuh artifact konkret.

---

## Render Targets

| Format | Use Case | Method | Library |
|--------|----------|--------|---------|
| `.md` | Specs, reports, prompts | Direct emit | none |
| `.docx` | Proposals, contracts, briefs | python-docx | `pip install python-docx` |
| `.xlsx` | Trackers, models, budgets | openpyxl | `pip install openpyxl` |
| `.pptx` | Decks, pitches | python-pptx | `pip install python-pptx` |
| `.pdf` | Final delivery, invoices | reportlab | `pip install reportlab` |
| `.json/.yaml` | Config, schemas | Direct emit | yaml: `pip install pyyaml` |
| `.py/.js/.sh` | Executable scripts | Direct emit | none |

---

## Templates Struktural

### A. Proposal (Client / Pitch)

```
1. Summary             — 1 paragraph, what + why now
2. Problem             — 1-2 paragraphs articulating friction
3. Solution            — 2-3 paragraphs, our approach
4. Timeline            — phases + dates
5. Investment          — pricing tiers (3 tiers usually)
6. Proof               — testimonials / case studies / metrics
7. Next step           — single specific action
```

### B. Technical Spec

```
# [ID] — [name]
## Capabilities
## Requirements
## Setup
## Usage
## Reference
```

### C. Insight Report

```
1. Executive summary   — 1 paragraph
2. Method              — how data was gathered
3. Findings            — patterns + facts
4. Analysis            — what it means
5. Prescriptions       — exactly 3 (per data-analysis-protocol)
6. Appendix            — sources, methodology details
```

---

## Quick Render Examples

### DOCX — Proposal (python-docx)

```python
from docx import Document
from docx.shared import Pt, Inches

doc = Document()
doc.add_heading('Proposal: <Client Name>', 0)

doc.add_heading('Summary', level=1)
doc.add_paragraph('We propose...')

doc.add_heading('Investment', level=1)
table = doc.add_table(rows=4, cols=3)
table.style = 'Light Grid'
table.cell(0, 0).text = 'Tier'
table.cell(0, 1).text = 'Includes'
table.cell(0, 2).text = 'Investment'
# ... fill rows ...

doc.save('proposal-clientname-2026-05-17.docx')
print("✅ proposal saved")
```

### XLSX — Multi-Sheet Tracker (openpyxl)

```python
import pandas as pd

summary_df = pd.DataFrame({...})
detail_df = pd.DataFrame({...})

with pd.ExcelWriter('tracker.xlsx', engine='openpyxl') as w:
    summary_df.to_excel(w, sheet_name='Summary', index=False)
    detail_df.to_excel(w, sheet_name='Detail', index=False)

print("✅ tracker.xlsx saved")
```

### PDF — Simple Invoice (reportlab)

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas('invoice-001.pdf', pagesize=A4)
c.setFont('Helvetica-Bold', 16)
c.drawString(50, 800, 'INVOICE')
c.setFont('Helvetica', 11)
c.drawString(50, 770, 'To: <Client>')
c.drawString(50, 750, 'Date: 2026-05-17')
c.drawString(50, 720, 'Total: IDR <amount>')
c.save()

print("✅ invoice saved")
```

### PPTX — Pitch Deck (python-pptx)

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])  # title slide
slide.shapes.title.text = '<Project Name>'
slide.placeholders[1].text = '<Tagline>'

slide2 = prs.slides.add_slide(prs.slide_layouts[1])  # title + content
slide2.shapes.title.text = 'The Problem'
slide2.placeholders[1].text = '...'

prs.save('deck-2026-05-17.pptx')
print("✅ deck saved")
```

---

## Render Protocol

1. Confirm scope (max 1 clarifying exchange)
2. Generate artifact (actual file, not preview)
3. Save to descriptive path: `<context>-<topic>-<YYYY-MM-DD>.<ext>`
4. Deliver path/link
5. Offer one specific next edit

**Rules:**
- Filename descriptif: `q3-analysis.xlsx` BUKAN `output.xlsx`
- Always actual file, never inline-only
- Always offer next edit option

---

## Naming Convention

```
<context>-<topic>-<date>.<ext>

Examples:
  brandflow-weekly-recap-2026-05-17.docx
  crypto-research-FL-2026-05-17-001.pdf
  nexusai-spec-dashboard-2026-05-17.md
  proposal-newclient-2026-05-17.docx
```

---

## Output Path Convention

| Type | Path |
|------|------|
| Company internal artifact | `companies/<company>/tasks/<filename>` |
| Cross-company deliverable | `tests/integration/<filename>` or `memory/global-<date>.md` |
| Client deliverable (post-approval) | `companies/<company>/clients/<client>/<filename>` |

---

## Boundary #4 Awareness

- Internal artifact (Fathur reads) → Tier 1, generate freely
- External delivery (client/public) → Tier 3, butuh Fathur approval sebelum kirim
- Disclaimer wajib di artifact financial (lihat `companies/crypto-consultant/skills/reporting/SKILL.md`)

---

## Constraints

- Always render actual artifact — preview tidak qualify
- Descriptive filenames — generic name ditolak
- One specific edit offer setelah delivery
- Test artifact opens correctly sebelum send (DOCX corrupt = failed delivery)

---

## Reference

- Source: `update/v2/openclaw/skills/m8.md`
- Companion: `knowledge/sop/data-analysis-protocol.md` (m5)
- Tool: `tools/llm_client.py` untuk content generation
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
```

**Verify:** `test -f knowledge/software/artifact-generation-cookbook.md && echo "step 10 ok"`

---

## STEP 11 — Marketing Landing Architecture (Tier C — m9)

**File baru:** `knowledge/marketing/landing-page-architecture.md`
**Source:** `update/v2/openclaw/skills/m9.md` (Conversion Surface section)
**Used by:** `@brandflow.designer` + `@nexusai.frontend` (cross-company)

Tulis file ini:

```markdown
# Landing Page Architecture — 8-Section Conversion Template

Versi: 1.0
Created: 2026-05-17
Owner: BrandFlow (`@brandflow.designer`) + NexusAI (`@nexusai.frontend`) cross-company
Source: Adapted from SUPERAGENT v2 m9.md
Replaces: NOTHING — reference template untuk handoff BrandFlow → NexusAI

---

## Purpose

Standardized 8-section conversion landing page architecture untuk:
- Marketing landing page (BrandFlow drives, NexusAI implements)
- Client-facing product page
- Sales conversion page

NexusAI `skills/uiux/SKILL.md` tetap pegang **product UI** (dashboard, internal tools, app screens). Cookbook ini fokus **marketing landing**.

---

## The 8 Sections

```
┌─────────────────────────────────────────┐
│  1. INTERRUPT     (above fold)         │
│     - headline + value prop + CTA      │
├─────────────────────────────────────────┤
│  2. PROOF                              │
│     - logos / testimonials / metrics   │
├─────────────────────────────────────────┤
│  3. PROBLEM                            │
│     - articulate the friction          │
├─────────────────────────────────────────┤
│  4. RESOLUTION                         │
│     - product/service presentation     │
├─────────────────────────────────────────┤
│  5. CAPABILITY                         │
│     - 3-6 key outcomes                 │
├─────────────────────────────────────────┤
│  6. EXCHANGE                           │
│     - 3 tiers (anchor on premium)      │
├─────────────────────────────────────────┤
│  7. OBJECTION                          │
│     - FAQ handling                     │
├─────────────────────────────────────────┤
│  8. FINAL SIGNAL                       │
│     - urgency + action directive       │
└─────────────────────────────────────────┘
```

---

## Section Specs

### 1. INTERRUPT (Above Fold)

```
Headline:     [Big bold problem-solution statement]
              Max 12 words, specific, outcome-focused
              ❌ "Welcome to our company"
              ✅ "Stop losing customers to slow checkouts"

Subheadline:  [Value proposition expansion]
              Max 25 words, who + what + why-now

CTA:          [Single primary action]
              Verb-led, specific outcome
              ✅ "Book free 15-min audit"
              ❌ "Learn more"

Visual:       [Hero image / video / animation]
              Shows the outcome OR product hero shot
```

### 2. PROOF (Trust)

Pilih minimum 1, maksimum 2:
- Client logos (>5 = credibility, <3 = jangan tampilkan)
- Testimonial (1-3 max, dengan nama + role + photo)
- Metrics ("Used by 500+ companies", "$2M revenue managed")

### 3. PROBLEM (Articulation)

```
Format:       1-2 paragraphs
Tone:         Empathetic, specific
Goal:         Reader thinks "yes, that's me"
Anti-pattern: Generic ("Many businesses struggle with...")
Better:       Specific ("Your team spends 8 hours/week on manual reports...")
```

### 4. RESOLUTION (Product)

```
Format:       1-2 paragraphs + visual
Goal:         Show how problem solves
Pattern:      Before / After / Bridge (BAB framework)
              "Before: chaos → After: clarity → Bridge: our solution"
```

### 5. CAPABILITY (Outcomes)

```
Format:       3-6 cards/list items
Goal:         Specific outcomes user will get
Pattern:      Verb + Specific outcome + Quantified benefit (if possible)

Example:
  ✅ "Generate weekly reports automatically — save 6h/week"
  ❌ "Powerful reporting features"
```

### 6. EXCHANGE (Pricing)

```
3 tiers always — anchor on PREMIUM (middle), not lowest

Layout:
┌──────────┬──────────┬──────────┐
│   Entry  │ Premium★ │   Pro    │
│  $29/mo  │ $99/mo   │  $299/mo │
│  Basic   │ Most     │  Custom  │
│  features│ popular  │  features│
└──────────┴──────────┴──────────┘

Premium star/highlight = drives 60-70% of selections.
```

### 7. OBJECTION (FAQ)

```
Format:       5-8 FAQ items, accordion or list
Pattern:      Address actual objection, not vanity question

Common objections to address:
- Price ("Why so expensive?")
- Trust ("How do I know this works?")
- Switching ("I already use [competitor]")
- Cancellation ("What if I want to cancel?")
- Timing ("I'll think about it")
```

### 8. FINAL SIGNAL (Closing CTA)

```
Headline:     Echo of #1 headline (variation OK)
Urgency:      Specific reason to act now (not fake urgency)
              ✅ "Cohort closes May 31, next opens August"
              ❌ "Limited time only!" (no specifics)
CTA:          Same as #1 (consistency)
```

---

## Implementation Stack (NexusAI handoff)

| Use Case | Stack | Reason |
|----------|-------|--------|
| Static marketing landing | HTML + Tailwind + Alpine.js | Fastest delivery, SEO-ready |
| Conversion-optimized | HTML + Tailwind + AOS.js | Scroll triggers for engagement |
| Application/SaaS landing | Next.js + Tailwind | SSR, dynamic content, app integration |
| Indonesian market | + Midtrans payment binding | Regional checkout |

---

## Performance Protocol (Mandatory)

```
✅ Assets:        WebP, lazy-loaded, dimensioned
✅ Typography:    System-ui or max 2 web fonts, preloaded
✅ Styles:        Tailwind purge enabled
✅ Scripts:       Defer/async, minimal payload
✅ Responsive:    Verified at 375px (mobile-first)
✅ Discovery:     Meta title + description + OG tags
✅ Speed:         < 3s first paint target
✅ Accessibility: Contrast 4.5:1 minimum, alt text on all images
```

---

## Mobile-First Always

Desktop = secondary viewport.

Build flow:
1. Mobile design first (375px width as canvas)
2. Tablet enhancement (768px)
3. Desktop expansion (1024px+)

NEVER reverse this. Mobile-as-afterthought = poor mobile UX.

---

## Quick Start HTML Template

Lihat `knowledge/software/devops-cookbook.md` untuk full deploy.
HTML+Tailwind starter:

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title — Primary Keyword]</title>
  <meta name="description" content="[Value prop in 150 chars]">
  <meta property="og:title" content="[Same as title]">
  <meta property="og:description" content="[Same as meta description]">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-gray-900 font-sans">

  <!-- Section 1: INTERRUPT -->
  <section class="min-h-screen flex items-center justify-center px-6">
    <div class="max-w-3xl text-center">
      <h1 class="text-4xl md:text-6xl font-bold mb-6">[Headline]</h1>
      <p class="text-lg text-gray-600 mb-8">[Subheadline]</p>
      <a href="#cta" class="bg-black text-white px-8 py-4 rounded-lg text-lg hover:bg-gray-800 transition">
        [CTA verb]
      </a>
    </div>
  </section>

  <!-- Sections 2-7 follow same pattern, varied layouts -->

  <!-- Section 8: FINAL SIGNAL -->
  <section id="cta" class="bg-gray-900 text-white py-20 px-6">
    <div class="max-w-3xl mx-auto text-center">
      <h2 class="text-3xl md:text-5xl font-bold mb-6">[Echo of headline]</h2>
      <p class="text-lg mb-8 opacity-90">[Urgency line — specific]</p>
      <a href="[link]" class="bg-white text-black px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition">
        [Same CTA verb]
      </a>
    </div>
  </section>

</body>
</html>
```

---

## Cross-Company Workflow

```
@brandflow.cmo        — strategy: who, why, message
@brandflow.copywriter — copy for each section (per skills/content/SKILL.md)
@brandflow.designer   — visual direction (color, type, hierarchy)
       ↓ HANDOFF
@nexusai.frontend     — implementation (this template + per nexusai/skills/uiux/)
@nexusai.devops       — deployment (per devops-cookbook.md)
       ↓ QA
@brandflow.qa         — visual brand check
@nexusai.qa           — technical quality (states, perf, a11y)
       ↓
APPROVAL              — Fathur (Tier 3, public surface = Boundary #4)
       ↓
LIVE
```

---

## Boundary #4 Awareness

Public-facing landing = ALWAYS Tier 3. Setiap perubahan content yang ke audience publik butuh Fathur approval per-piece (atau standing approval kalau Phase 2 active).

---

## Reference

- Source: `update/v2/openclaw/skills/m9.md`
- BrandFlow content: `companies/brandflow/skills/content/SKILL.md`
- BrandFlow design: `companies/brandflow/skills/design/SKILL.md`
- NexusAI uiux: `companies/nexusai/skills/uiux/SKILL.md` (product UI authority)
- DevOps deploy: `knowledge/software/devops-cookbook.md`
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
```

**Verify:** `test -f knowledge/marketing/landing-page-architecture.md && echo "step 11 ok"`

---

## STEP 12 — Monetization Reference (Tier C — m1, future-use)

**File baru:** `knowledge/business/monetization-reference.md`
**Source:** `update/v2/openclaw/skills/m1.md`
**Status:** Reference untuk masa depan (kalau Company #4 fokus business consulting, atau kalau ada client work yang butuh monetization framework)

Tulis file ini:

```markdown
# Monetization Reference — Value Generation & Exchange Framework

Versi: 1.0 (REFERENCE — not actively used)
Created: 2026-05-17
Owner: Future business-strategy work (Company #4 candidate, atau ad-hoc client engagement)
Source: Adapted from SUPERAGENT v2 m1.md

---

## Status

🟡 **REFERENCE ONLY.** Belum aktif digunakan.

AI Holding sekarang fokus: Crypto research (Crypto Consultant), Marketing (BrandFlow), Engineering (NexusAI). Monetization advisory bukan service yang dijalankan.

File ini disimpan sebagai **future-proof reference** untuk:
1. Company #4 yang fokus business consulting
2. BrandFlow client engagement yang butuh pricing framework
3. NexusAI productization (kalau salah satu tool jadi SaaS)
4. Operator (Fathur) personal business decisions

---

## Opportunity Evaluation Framework

5 dimensi scoring (1-10 each):

```
signal_strength:    Apakah demand signal jelas dan specific?
                    1 = vague hunch | 10 = specific paying audience identified

exchange_pool:      Siapa yang sudah bayar untuk solve problem ini?
                    1 = nobody | 10 = saturated market with proven willingness-to-pay

differentiation:    Apa yang bikin offer ini distinct?
                    1 = me-too | 10 = unique angle / IP / capability

operator_fit:       Bisa orang ini execute delivery?
                    1 = skill gap besar | 10 = perfect fit, sudah ada track record

activation_time:    Berapa hari ke first successful exchange?
                    1 = months+ | 10 = days
```

Threshold: Jangan pursue kalau total score < 30/50.

---

## Pipeline Architecture

```
SIGNAL      → Awareness channel (content / search / referral)
     ↓
CAPTURE     → Conversion asset (free tool / demo / sample / lead magnet)
     ↓
CONVERT     → Decision trigger (sales page / direct DM / call)
     ↓
EXCHANGE    → Fulfillment (checkout / invoice / link)
     ↓
COMPOUND    → Retention loop (upsell / renewal / referral)
```

Each layer needs:
- Specific channel
- Owner
- Conversion metric
- Drop-off recovery (what if leak?)

---

## Pricing Logic

Core formula:

```
RATE = (Perceived Outcome × Urgency) / (Friction × Risk)
```

Implications:
- Rate on **outcome delivered**, never on **input cost**
- Always 3 tiers — anchor on **premium tier first** (psychological anchor)
- Installment option for high-friction price points
- Currency context matters (IDR has different psychology than USD)

3-tier pattern:

```
ENTRY        — Lowest barrier, validates fit
              ~30% of buyers, low margin per sale
CORE         — Sweet spot, sustainable margin
              ~50% of buyers, primary revenue driver
PREMIUM      — Anchor + best margin
              ~20% of buyers, highest LTV
```

---

## Fast Activation Paths (5 Patterns)

### 1. Operator-as-Service (IDR 500k–5jt per engagement)

You-as-deliverable. Lowest barrier, fastest activation.
- Examples: 1-on-1 audit, done-for-you, hourly consulting
- Risk: doesn't scale, capped at your hours

### 2. Distribution Resale (30-60% margin)

Resell existing tools/services dengan added value.
- Examples: white-label SaaS, agency reseller, affiliate+service combo
- Risk: dependent on upstream

### 3. Leverage Arbitrage (Premium rate via AI-acceleration)

You charge senior rate, AI does production work, you do quality control + relationship.
- Examples: AI-generated content with human editing, AI-spec'd code with senior review
- Risk: client perceives as "just AI" if positioning weak

### 4. Template Distribution (Passive after build)

Build once, sell many.
- Examples: Notion templates, code starters, prompt libraries
- Risk: needs distribution muscle (audience or platform)

### 5. Audience-to-Affiliate (Compound via referrals)

Build audience → recommend tools → affiliate revenue.
- Examples: niche newsletter + affiliate stack
- Risk: audience-building is slow

---

## Output Structure (Saat Aktif Digunakan)

Untuk setiap monetization analysis, output mandatory:

```
[OPPORTUNITY EVALUATION]
  signal_strength:    X/10 — basis
  exchange_pool:      X/10 — basis
  differentiation:    X/10 — basis
  operator_fit:       X/10 — basis
  activation_time:    X/10 — basis
  TOTAL:              XX/50

[RECOMMENDATION]
  Pursue:             yes / no / iterate
  Reasoning:          1-2 sentences

[PRIMARY EXCHANGE MODEL]
  Type:               <one of 5 fast paths>
  Tier 1 (Entry):     IDR <amount> / <what's included>
  Tier 2 (Core):      IDR <amount> / <what's included>
  Tier 3 (Premium):   IDR <amount> / <what's included>

[2-3 EXPANSION PATHS]
  Path A: <description>
  Path B: <description>

[ACQUISITION PLAN — first 10 exchanges]
  Channel:            <where leads come from>
  Capture asset:      <what makes them give contact>
  Conversion:         <how they decide>
  Timeline:           <X days to first 10>

[FIRST ACTIVATION STEP — 24 HOURS]
  → <single specific action>
```

---

## Boundary #4 Awareness

Monetization advice yang affect decisions besar (price changes, business model pivots) untuk personal Fathur stuff = Tier 2 (autonomous with log) — biasanya output untuk Fathur read.

Untuk client work via BrandFlow/future Company #4 → standard public-content gate (Tier 3 saat ada deliverable yang dipublikasikan).

---

## When To Activate This Skill

Trigger conditions untuk load this reference:
- Operator menanyakan pricing / business model question
- BrandFlow client engagement membutuhkan rate sheet
- NexusAI productize tool jadi SaaS (perlu pricing strategy)
- Spawn Company #4 yang fokus business advisory

NOT:
- Routine content/research/engineering tasks (out of scope)
- Tactical execution (this is strategy layer)

---

## Reference

- Source: `update/v2/openclaw/skills/m1.md`
- Companion strategic thinking: `knowledge/sop/strategic-thinking.md`
- Companion data analysis: `knowledge/sop/data-analysis-protocol.md`
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
```

**Verify:** `test -f knowledge/business/monetization-reference.md && echo "step 12 ok"`

---

## STEP 13 — Cleanup & Commit (Final)

Setelah semua step di atas verified:

### 13a. Pindahkan source folder ke archive

```bash
mkdir -p docs/external-references
git mv update docs/external-references/superagent-v2
```

### 13b. Update commit message untuk audit trail

```bash
git add -A
git commit -m "feat: comprehensive cherry-pick from SUPERAGENT v2 — 12 patterns adopted

Tier A — Generic SOPs (4 files):
- knowledge/agent-design/reflection-loop.md (5-Q self-check + Boundary #4)
- knowledge/sop/debug-protocol.md (6-step diagnose+fix+harden)
- knowledge/sop/system-audit.md (4-layer weekly audit)
- knowledge/sop/strategic-thinking.md (5-step decomposition)

Tier B — Infrastructure (4 files):
- tools/llm_client.py (TOOL-033, 5 providers with retry/backoff)
- knowledge/ml/llm-providers.md (selection guide + use cases)
- knowledge/tools/tool-registry.md (TOOL-033 registered)
- HEARTBEAT.md (v2.0 with skill registry + reflection ref)

Tier C — Cookbooks & Future-Use (9 files):
- knowledge/software/devops-cookbook.md (m2 — Nginx/Certbot/PM2 snippets)
- tools/templates/telegram_bot.js (m4 — runnable bot)
- tools/templates/cron_examples.txt (m4 — schedule patterns)
- tools/templates/fastapi_webhook.py (m4 — webhook receiver)
- knowledge/software/automation-cookbook.md (m4 — patterns + usage)
- knowledge/sop/data-analysis-protocol.md (m5 — SCOPE→PRESCRIBE flow)
- knowledge/software/artifact-generation-cookbook.md (m8 — DOCX/XLSX/PDF/PPTX)
- knowledge/marketing/landing-page-architecture.md (m9 — 8-section template)
- knowledge/business/monetization-reference.md (m1 — future-use reference)

NOT adopted (incompatible with Boundary #4 / inferior):
- Flexibility Doctrine (bertabrakan Boundary #4)
- IDENTITY rebrand ke 'SUPERAGENT' (per-company identity kita lebih kuat)
- Keyword router (pseudo-mention @company.agent lebih baik)
- Single MEMORY format (kita layered: holding + global + 3× company)
- m3 (Content) — BrandFlow skills/content/ + Update 11 senior patterns lebih dalam

Source archived: docs/external-references/superagent-v2/
Original analysis: docs/external-references/superagent-v2/ANALYSIS.md"
```

---

## Final Verification Checklist

Hermes lapor di akhir:

```
=== TIER A — Generic SOPs ===
✅ Step 1:  knowledge/agent-design/reflection-loop.md created
✅ Step 2:  knowledge/sop/debug-protocol.md created
✅ Step 3:  knowledge/sop/system-audit.md created
✅ Step 4:  knowledge/sop/strategic-thinking.md created

=== TIER B — Infrastructure ===
✅ Step 5a: tools/llm_client.py created (syntax valid)
✅ Step 5b: knowledge/ml/llm-providers.md created
✅ Step 5c: knowledge/tools/tool-registry.md updated (TOOL-033)
✅ Step 6:  HEARTBEAT.md updated to v2.0

=== TIER C — Cookbooks & Future-Use ===
✅ Step 7:  knowledge/software/devops-cookbook.md (m2 snippets)
✅ Step 8a: tools/templates/telegram_bot.js (runnable)
✅ Step 8b: tools/templates/cron_examples.txt
✅ Step 8c: tools/templates/fastapi_webhook.py (syntax valid)
✅ Step 8d: knowledge/software/automation-cookbook.md
✅ Step 9:  knowledge/sop/data-analysis-protocol.md (m5)
✅ Step 10: knowledge/software/artifact-generation-cookbook.md (m8)
✅ Step 11: knowledge/marketing/landing-page-architecture.md (m9)
✅ Step 12: knowledge/business/monetization-reference.md (m1)

=== CLEANUP ===
✅ Step 13a: update/ moved to docs/external-references/superagent-v2/
✅ Step 13b: committed

=== TOTALS ===
Files added:        17 (4 Tier A + 4 Tier B + 9 Tier C)
Files modified:     2 (HEARTBEAT.md, tool-registry.md)
Files relocated:    22 (update/v2/openclaw/* → docs/external-references/superagent-v2/v2/openclaw/*)

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
| m3 (Content) — full skill | `update/v2/openclaw/skills/m3.md` | BrandFlow `skills/content/` + Update 11 senior patterns lebih dalam |

**Yang DIADOPT (revisi dari draft sebelumnya):**

| Item | Step | Reason adopted |
|------|------|----------------|
| m1 (Monetization) | Step 12 | Future-proof reference untuk masa depan |
| m2 (DevOps snippets) | Step 7 | Cookbook reference — NexusAI SKILL.md tetap autoritatif |
| m4 (Automation) | Step 8 | ⭐ Runnable code untuk Tier 1 autonomous execution |
| m5 (Data analysis) | Step 9 | Generic protocol berguna untuk @brandflow.analytics + @crypto.data |
| m6 (API patterns) | Step 5 (in llm_client) | Retry/backoff pattern integrated |
| m7 (LLM multi-provider) | Step 5 | Gap nyata, jadi tools/llm_client.py |
| m8 (File rendering) | Step 10 | Cookbook untuk DOCX/XLSX/PDF/PPTX kalau butuh |
| m9 (Landing arch) | Step 11 | 8-section template untuk BrandFlow→NexusAI marketing landing |

---

## Stop Conditions

Hermes harus STOP dan lapor operator KALAU:

- Pre-flight check fail (source missing, target dir tidak bisa dibuat)
- Step 5a: Python syntax error di `llm_client.py`
- Step 8c: Python syntax error di `fastapi_webhook.py`
- Step 13a: `git mv` fail (uncommitted changes di update/)
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
2. Test smoke LLM: `python tools/llm_client.py --provider groq --message "ping"` (perlu env GROQ_API_KEY)
3. Test smoke FastAPI: `pip install fastapi uvicorn && python -m uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000` lalu `curl http://localhost:8000/health`
4. Test smoke Telegram bot (jika bot token tersedia): `npm install node-telegram-bot-api dotenv && node tools/templates/telegram_bot.js`
5. Schedule di weekly cadence: System Audit Friday slot sudah otomatis aktif via reference di `weekly-cadence.md` (no edit needed — already mentions Friday recap)
6. Update PR description dengan link ke `docs/external-references/superagent-v2/ANALYSIS.md` untuk audit trail

---

**END OF UPGRADE.md**

Total estimated execution time untuk Hermes: ~12-18 menit.
Total file impact: 17 added, 2 modified, 22 relocated.
