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

## Reference

- `companies/nexusai/agents/ml.md`
- `knowledge/karpathy.md`
- `knowledge/agent-design/tool-use-rules.md`
- `companies/nexusai/SOUL.md`
