---
name: automation
description: Use for workflow automation, JSONL task systems, scripts, scheduled jobs, routing, and multi-agent communication.
---

# Automation Skill

Use this skill for:
- JSONL workflows
- Agent task routing
- Scripts
- Repeated processes
- File-based automation
- Multi-agent communication
- Company generator

Rules:
1. Use simple file formats first.
2. Prefer JSONL for logs, tasks, and messages.
3. Make workflows resumable.
4. Include status fields.
5. Avoid over-engineering.

Default JSONL task format:
{"id":"T001","company":"company-name","from":"USER","to":"CEO","task":"Describe task","priority":"HIGH","status":"NEW","created_at":"ISO_DATE"}

Output format:
- Goal
- Workflow
- File structure
- Script/command
- Verification
