# Post-Deployment Audit — Quick Reference Checklist

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** Operator (Main Assistant)  
**Purpose:** One-page quick reference for weekly audits

---

## Weekly Audit Checklist (2 Hours)

### Pre-Audit (5 min)
- [ ] Open `knowledge/sop/audit-metrics-dashboard.md`
- [ ] Note last week's status
- [ ] Gather data sources ready
- [ ] Set timer for 2 hours

---

## LAYER 1: AGENT BEHAVIOR (15 min)

### Autonomy Tier Compliance
- [ ] Count Tier 1 actions: `grep -c '"tier": "1"' tasks/logs.jsonl`
- [ ] Count Tier 2 actions: `grep -c '"tier": "2"' tasks/logs.jsonl`
- [ ] Count Tier 3 actions: `grep -c '"tier": "3"' tasks/logs.jsonl`
- [ ] Verify Tier 2 logs: `grep -c '\[AUTO-LOG' memory/global.md`
- [ ] Calculate rates: (Tier 1 / total) × 100 = __% (target 95%+)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Escalation Patterns
- [ ] Count escalations: `grep -c '"escalated": true' tasks/logs.jsonl`
- [ ] Calculate rate: (escalations / total tasks) × 100 = __% (target <10%)
- [ ] Check resolution time: median from logs = __ hours (target <4h)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Tool Usage
- [ ] Count tool invocations: `grep -c '"tool_used"' tasks/logs.jsonl`
- [ ] Count unregistered: `grep -c 'unregistered_tool' tasks/logs.jsonl` (target 0)
- [ ] Count errors: `grep -c '"tool_error"' tasks/logs.jsonl`
- [ ] Calculate error rate: (errors / invocations) × 100 = __% (target <2%)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

**Layer 1 Summary:** [ ] ✓ Pass [ ] ⚠ Warning [ ] ✗ Fail

---

## LAYER 2: FRAMEWORK ADOPTION (15 min)

### SOUL Compliance
- [ ] Count Tier 3 SOULs: `find companies/*/agents -name "*.md" | wc -l` = __ (target 32)
- [ ] Check for conflicts: `grep -i 'conflict\|contradiction' companies/*/SOUL.md` (target 0)
- [ ] Verify references: spot-check 5 SOUL files for broken links
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Memory Discipline
- [ ] Check format: `grep '^\[' memory/global.md | head -5` (should be `[TAG] YYYY-MM-DD`)
- [ ] File sizes:
  - `MEMORY.md`: `wc -c < MEMORY.md` = __ bytes (target <500KB)
  - `memory/global.md`: `wc -c < memory/global.md` = __ bytes (target <500KB)
- [ ] Growth rate: (new lines this week) / 1 = __ lines/week (target <50)
- [ ] Check isolation: `grep -l 'nexusai\|brandflow\|crypto' memory/global.md` (should be 0)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Knowledge Loading
- [ ] Directory size: `du -sh knowledge/` = __ (target <2MB)
- [ ] Check for duplicates: `find knowledge -name "*.md" -exec grep -l 'duplicate' {} \;` (target 0)
- [ ] Verify organization: spot-check 5 files are in correct domain folder
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

**Layer 2 Summary:** [ ] ✓ Pass [ ] ⚠ Warning [ ] ✗ Fail

---

## LAYER 3: PERFORMANCE (15 min)

### Response Time
- [ ] Extract times: `jq '.response_time_ms' tasks/logs.jsonl | sort -n`
- [ ] Calculate median: __ ms = __ min (target <2m simple, <10m complex)
- [ ] Calculate P95: __ ms = __ min (target <15m)
- [ ] Count timeouts: `grep -c '"timeout": true' tasks/logs.jsonl` (target 0)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Error Rates
- [ ] Task failures: `grep -c '"status": "failed"' tasks/logs.jsonl` = __
- [ ] Total tasks: `wc -l < tasks/logs.jsonl` = __
- [ ] Failure rate: (failures / total) × 100 = __% (target <2%)
- [ ] Tool errors: `grep -c '"tool_error"' tasks/logs.jsonl` = __% (target <2%)
- [ ] Routing errors: `grep -c '"routing_error"' tasks/logs.jsonl` = __ (target <1%)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Resource Usage
- [ ] Avg tokens: `jq '.tokens_used' tasks/logs.jsonl | awk '{sum+=$1} END {print sum/NR}'` = __ (target <5000)
- [ ] Peak tokens: `jq '.tokens_used' tasks/logs.jsonl | sort -n | tail -1` = __ (target <20000)
- [ ] Disk growth: `du -sh audits/` = __ (target <100MB/month)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

**Layer 3 Summary:** [ ] ✓ Pass [ ] ⚠ Warning [ ] ✗ Fail

---

## LAYER 4: QUALITY (15 min)

### Output Quality
- [ ] Sample 5 recent outputs from `tasks/logs.jsonl`
- [ ] Check each for: [ ] executable [ ] complete [ ] specific [ ] no TODOs
- [ ] Executable rate: __/5 = __% (target 95%+)
- [ ] Check for hallucinations: `grep -i 'false\|incorrect\|error' tasks/logs.jsonl | head -3`
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### Safety Boundaries
- [ ] Boundary #1 (loyalty): Any actions against Fathur interest? (target 0)
- [ ] Boundary #2 (execute): Count unnecessary refusals (target <5%)
- [ ] Boundary #3 (4 real boundaries): Any violations? (target 0)
- [ ] Boundary #4 (public surface): Check for approval flags (target 100%)
- [ ] Security: Any credential leaks? (target 0)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

### User Satisfaction
- [ ] Collect feedback from Telegram (this week)
- [ ] Positive messages: __ (target 80%+)
- [ ] Issues reported: __ (resolved: __)
- [ ] Satisfaction score: __/5.0 (target 4.0+)
- [ ] Status: [ ] ✓ [ ] ⚠ [ ] ✗

**Layer 4 Summary:** [ ] ✓ Pass [ ] ⚠ Warning [ ] ✗ Fail

---

## ANALYSIS (15 min)

### Identify Issues
- [ ] Layer 1 issues: ___
- [ ] Layer 2 issues: ___
- [ ] Layer 3 issues: ___
- [ ] Layer 4 issues: ___

### Prioritize
- [ ] Critical (fix now): ___
- [ ] Medium (fix this week): ___
- [ ] Low (monitor): ___

### Root Causes
For each issue:
- [ ] What is it?
- [ ] Why is it happening?
- [ ] What's the impact?
- [ ] What's the fix?

---

## DOCUMENTATION (15 min)

### Update Dashboard
- [ ] Open `knowledge/sop/audit-metrics-dashboard.md`
- [ ] Fill in all current values
- [ ] Update status indicators (✓ ⚠ ✗)
- [ ] Update trends (↑ → ↓)
- [ ] Note issues found

### Log in Memory
```
[AUDIT] 2026-05-18 — Weekly audit complete
Status: [ ] Green [ ] Yellow [ ] Red
Issues: __ critical, __ medium, __ low
Recommendations: ___
```

### Create Report
- [ ] Overall health: [ ] 🟢 [ ] 🟡 [ ] 🔴
- [ ] Critical issues: ___
- [ ] Recommendations: ___
- [ ] Next audit: 2026-05-25

---

## REPORTING (10 min)

### Prepare Summary for Fathur
```
Weekly Audit — 2026-05-18

Status: [ ] 🟢 Green [ ] 🟡 Yellow [ ] 🔴 Red

Key Metrics:
- Tier 1 auto-execution: __% ✓
- Tier 2 logging: __% ✓
- Tier 3 confirmation: __% ✓
- Response time: __ min ✓
- Error rate: __% ✓
- Output quality: __% ✓
- Boundary compliance: __% ✓

Issues: __ (critical: __, medium: __, low: __)

Recommendations:
1. ___
2. ___
3. ___

Next audit: 2026-05-25
```

### Get Approval
- [ ] Send summary to Fathur
- [ ] Get approval for recommended actions
- [ ] Document approval in memory

### Execute Actions
- [ ] Implement approved fixes
- [ ] Update framework if needed
- [ ] Log execution in memory

---

## QUICK METRICS REFERENCE

| Metric | Target | How to Check |
|--------|--------|-------------|
| Tier 1 auto-exec | 95%+ | `grep -c '"tier": "1"' tasks/logs.jsonl` |
| Tier 2 logging | 100% | `grep -c '\[AUTO-LOG' memory/global.md` |
| Tier 3 confirm | 100% | Manual review of logs |
| Escalation rate | <10% | `grep -c '"escalated"' tasks/logs.jsonl` / total |
| Tool registration | 100% | `grep -c 'unregistered'` should be 0 |
| SOUL coverage | 100% | `find companies/*/agents -name "*.md" \| wc -l` = 32 |
| Memory growth | <50 lines/week | `wc -l memory/global.md` |
| Response time | <2m avg | `jq '.response_time_ms' tasks/logs.jsonl` |
| Error rate | <2% | `grep -c '"status": "failed"' tasks/logs.jsonl` / total |
| Output quality | 95%+ | Manual sample review (5 outputs) |
| Boundary #4 | 100% | Manual review of public outputs |
| User satisfaction | 4.0+/5.0 | Collect feedback from Telegram |

---

## COMMON ISSUES & QUICK FIXES

| Issue | Quick Fix |
|-------|-----------|
| Tier 3 bypass | Check logs for missing approval, escalate to Fathur |
| Memory bloat | Archive entries >30 days old to `memory/archive/` |
| Tool errors | Check tool registry, verify whitelist policy |
| Slow response | Check for knowledge loading bloat, optimize |
| High error rate | Root cause analysis, fix top 3 issues |
| Low output quality | Review reflection loop, add QA step |
| Boundary violation | Escalate immediately, document incident |

---

## TIME BREAKDOWN

- Pre-audit: 5 min
- Layer 1: 15 min
- Layer 2: 15 min
- Layer 3: 15 min
- Layer 4: 15 min
- Analysis: 15 min
- Documentation: 15 min
- Reporting: 10 min
- **Total: ~105 minutes (1h 45m)**

*Aim to complete within 2 hours*

---

## Files to Have Open

1. `knowledge/sop/audit-metrics-dashboard.md` — update this
2. `tasks/logs.jsonl` — data source
3. `memory/global.md` — log results here
4. `MEMORY.md` — reference for strategic context
5. Terminal — run data collection commands

---

## After Audit

- [ ] Update dashboard
- [ ] Log in memory
- [ ] Send summary to Fathur
- [ ] Get approval for actions
- [ ] Execute approved actions
- [ ] Schedule next audit (Friday)
- [ ] Close this checklist

---

## Notes

- Keep this checklist handy for weekly audits
- Update metrics dashboard immediately after collecting data
- Log findings in memory while fresh
- Report to Fathur same day if possible
- Execute approved actions within 24 hours

---

## Contact & Support

- **Questions about audit plan?** → See `knowledge/sop/post-deployment-audit-plan.md`
- **Questions about implementation?** → See `knowledge/sop/audit-implementation-guide.md`
- **Questions about metrics?** → See `knowledge/sop/audit-metrics-dashboard.md`
- **Questions about autonomy tiers?** → See `knowledge/sop/autonomy-tiers.md`
- **Questions about boundaries?** → See `SOUL.md`
