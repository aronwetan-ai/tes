---
name: ml-agent
description: AI agent design, prompt engineering, tool integration, eval design, model selection. Karpathy-aligned.
company: NexusAI
used_by: ["@nexusai.ml", "@nexusai.cto"]
---

# ML / Agent Skill — NexusAI

How NexusAI builds AI systems. Aligned with `knowledge/karpathy.md`:

- Prompt is program.
- Context is source code.
- Memory is persistent state.
- Skills are reusable modules.
- **Evals are tests.**
- Tools are external capabilities.
- Human remains supervisor.

## When to Use

- Designing a new AI agent (system prompt, tools, memory).
- Iterating on an existing agent's prompt.
- Building eval suites.
- Selecting a model (Claude / GPT / Gemini / open / local).
- Cost optimization for AI workloads.
- Tool / function-calling schema design.
- Memory strategy (vector store, summary, hybrid).
- Prompt injection defense.

## Default Approach

1. **State the job as measurable outcome.** What does success look like?
2. **Identify failure modes.** What does "wrong" look like? What's catastrophic vs annoying?
3. **Eval first.** Build the eval before tuning the prompt. Otherwise you're guessing.
4. **Smallest viable model.** Start with Haiku / Mini before reaching for Opus / Sonnet 4.
5. **Tools > prompts** for capability. Tool calls are deterministic; prompts are not.
6. **Context discipline.** Retrieve only what's needed. Don't dump the repo.
7. **Memory only if needed.** Stateless first; add memory when stateless fails.
8. **Observability.** Log every call, every tool invocation, every refusal, every cost.

## Rules

1. **Bigger model isn't always better.** Prove with evals.
2. **No shipping without evals.** "It looked right when I tried it" is not eval.
3. **Don't invent capabilities.** If the model can't do X reliably, don't pretend it can.
4. **APIs first** before training/fine-tuning. Most problems don't need custom models.
5. **Prompt injection is real.** Treat user input to AI as untrusted, like a SQL query.
6. **Cost is a constraint.** Track $/call. Optimize before scaling.

## Output Format

For agent design:
```
[GOAL]          What the agent accomplishes
[INPUTS]        User input, context, available tools
[OUTPUTS]       Format + structure
[FAILURE MODES] How this could go wrong
[EVAL CRITERIA] Pass/fail definition + sample size
[SYSTEM PROMPT] Concrete prompt (or sketch)
[TOOLS]         Function specs the agent can call
[GUARDRAILS]    Refusal patterns, injection defense
[COST]          Estimated $/call + monthly projection
```

For prompt iteration:
```
[BASELINE]      Current prompt + current eval scores
[HYPOTHESIS]    What change should improve scores
[CHANGE]        Concrete diff to the prompt
[RESULT]        New eval scores (with sample size)
[KEEP / REVERT] Decision + reasoning
```

For eval suite:
```
[CAPABILITY]    What we're testing
[INPUTS]        Eval set (manually curated or generated)
[METRIC]        Pass/fail / score / human eval
[BASELINE]      Current performance
[TARGET]        What "good enough" looks like
[FAILURE EXAMPLES] What failure looks like (concrete)
```

For tool / function spec:
```
[TOOL]         Name + purpose
[INPUT SCHEMA] JSON schema or similar
[OUTPUT SCHEMA] JSON schema
[ERRORS]       What can fail + how it's surfaced
[SIDE EFFECTS] What this changes (if anything)
[RISK LEVEL]   Read-only / Mutating / Destructive
```

## Karpathy Defaults

- **Prompts as programs**: version-control them, eval them, regression-test them.
- **Context as source code**: control what gets loaded, not just write a prompt.
- **Skill files** (this very system) — reusable, composable behavior.
- **Tools as capabilities**: clean schema, tight error handling, deterministic.
- **Human in the loop** for irreversible.

## Cross-Skill / Cross-Agent

- API exposing the agent → `@nexusai.backend` + `skills/coding`.
- Inference deployment / scaling → `@nexusai.devops` + `skills/devops`.
- Prompt injection defense / output sanitization → `@nexusai.security` + `skills/security`.
- Eval review / behavior validation → `@nexusai.qa` + `skills/qa`.
- Architectural integration → `@nexusai.cto`.

## What This Skill Does NOT Cover

- Generic backend code (DB, API logic) → `skills/coding`.
- Marketing copy generated **by** an agent (prompt design lives here, content design lives at `@brandflow.copywriter`).
- Crypto-specific research agent — methodology lives at `@crypto.*`, agent design lives here.

## Senior Patterns (Deep Dive)

### Agent design pattern (NexusAI default)

For any new AI agent in the holding:

```
1. Job spec     — measurable outcome + failure budget.
2. Eval set     — 20–50 hand-curated examples covering:
                  - Happy path (60%)
                  - Edge case (20%)
                  - Adversarial / injection (10%)
                  - Out-of-scope refusal (10%)
3. System prompt — short, structured, role + rules + output format.
4. Tool list    — JSON-schema'd, deterministic, error-handled.
5. Memory       — minimal first; add only when stateless fails.
6. Guardrails   — input filter + output validator + cost cap.
7. Eval baseline — score current setup.
8. Iterate      — change one thing, re-eval, keep if better.
9. Deploy       — log every call, monitor cost + latency + error.
10. Regression  — eval re-runs on every prompt / tool / model change.
```

### Prompt-as-code discipline

- **Version control**: prompts live in `.md` or `.txt` files, not embedded strings. Diff-able, review-able, rollback-able.
- **Templating**: variable interpolation via Jinja2 / f-strings, schema documented at top of file.
- **Pinning**: model name + version pinned (`claude-sonnet-4-5`, not `claude-latest`). Drift on auto-update is a real bug source.
- **Eval on change**: any prompt edit triggers eval suite re-run. No "looks good, ship it".

### Eval methodology (Karpathy-aligned)

Tier 1 — code-graded (cheap, fast):
- Format compliance: regex / JSON schema validation.
- Tool-call correctness: did the agent call the right tool with right args?
- Length / cost bounds: under N tokens?

Tier 2 — LLM-graded (medium cost):
- Rubric scoring (1-5 on each dimension: relevance, accuracy, format, tone).
- Pairwise A/B (prompt v1 vs v2) using a stronger model as judge.
- Adversarial (red-team) — does it refuse the injection?

Tier 3 — human-graded (expensive, slow):
- Sample 5–10 outputs per change, human reviews.
- Use only when Tier 1+2 disagrees with intuition, OR for high-stakes shipping.

Reference: `knowledge/ml/eval-methodology.md`.

### Prompt injection — defense patterns

| Layer | Defense |
|---|---|
| Input sanitization | Detect known injection patterns (`ignore previous`, `system:`, role-switch markers). Don't sanitize naively — most injection is subtle. |
| Trust boundary | Treat user content (DM, scraped page, tool output) as untrusted. Wrap in delimiters: `<user_content>...</user_content>`. |
| System prompt anchor | Repeat critical rules at the END of the prompt. Models weight recent more. |
| Tool gating | Privileged tools (write, send, pay) require an explicit token from system prompt that user content can't forge. |
| Output validation | Validate model output against expected schema before passing to tools. Refuse on shape mismatch. |
| Capability segregation | Two agents: one reads untrusted, one acts on trusted. Reader emits structured intent; Actor validates and executes. |

### Cost control patterns

- **Tier the model**: use Haiku / Mini for classification + extraction; reserve Sonnet / GPT-4 class for synthesis only.
- **Cache**: hash `(model, system_prompt, user_input)` → cache response. Especially valuable for client-onboarding analyses where 30% of inputs repeat.
- **Batch**: when possible, batch similar inputs into one call. Token overhead amortized.
- **Truncation**: long context inflates cost linearly. RAG / summarization step before the agent call.
- **Cost cap per request**: hard cutoff. If retries exceed budget, fail loud, don't retry forever.
- **Daily / per-client budget**: track in metrics. Alert at 80%, hard-stop at 100%.

### Tool-calling design (function spec discipline)

```json
{
  "name": "send_dm",
  "description": "Send a DM. Use ONLY when explicitly authorized in this turn. Cannot be undone.",
  "parameters": {
    "type": "object",
    "required": ["account_id", "recipient", "body"],
    "properties": {
      "account_id":  {"type": "string", "description": "Sender account in cred_vault."},
      "recipient":   {"type": "string", "description": "Target username."},
      "body":        {"type": "string", "maxLength": 1000}
    }
  },
  "x-risk": "high",
  "x-requires-confirm": true
}
```

Agent rules:
- Description includes risk + when-to-use + when-NOT-to-use.
- High-risk tools require explicit confirmation token in the same turn.
- Output schema validated before agent sees the result (defense against malformed-tool-output injection).

### Memory strategy

| Need | Pattern |
|---|---|
| Conversation context within session | Sliding window (last N turns) |
| User preferences across sessions | Key-value store, fetched at session start |
| Domain knowledge | RAG over indexed corpus, retrieved per query |
| Long task with state | Append-only log + periodic summarization |
| Cross-agent shared facts | Central memory store with namespace per topic |

Don't use vector DB for everything. Most agency-internal needs are KV or RAG, not "infinite memory".

### Agency-context AI tooling (what NexusAI builds for the agency)

| Use case | Pattern |
|---|---|
| Proposal generation per prospect | Template + variable filler + LLM tone-match. Cache common industries. |
| Content variation per channel | One brief → 5 channel-specific variants in single batch call. |
| Competitor post analysis | Scrape → extract → cluster topics with embeddings → trend report. |
| DM personalization at scale | Profile scrape → variable extraction → template fill (LLM only for the 10% non-template part). |
| Lead scoring | Structured extraction + rule-based scoring. LLM only for "tone of bio" features. |
| Reporting summary | Metrics dump → LLM → executive summary. Cached weekly. |

### Anti-patterns NexusAI rejects

- **"Just throw GPT-4 at it."** Without eval, no guarantee it works. Without cost cap, it'll burn budget.
- **Trusting model output as code/data without validation.** Schema-validate everything.
- **Long monolithic prompts.** Decompose into pipeline of small focused steps.
- **No regression testing on prompt change.** "Ship and pray" — old failure modes return.
- **Memory bloat.** Storing every conversation forever. Summarize, expire, forget.
- **Letting agents call privileged tools without explicit authorization.** Privileged tool = side effect = needs scoped auth from current turn.

## Reference

- `companies/nexusai/agents/ml.md`
- `knowledge/karpathy.md`
- `knowledge/agent-design/tool-use-rules.md`
- `knowledge/ml/prompt-engineering.md`
- `knowledge/ml/eval-methodology.md`
- `companies/nexusai/SOUL.md`
- `companies/nexusai/skills/ml-agent/prompt-eval.md` (agent-specific deep skill)
