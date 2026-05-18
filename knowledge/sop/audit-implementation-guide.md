# Post-Deployment Audit Implementation Guide

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** Operator (Main Assistant)  
**Purpose:** Step-by-step guide to implement and run post-deployment audits

---

## Quick Start (5 Minutes)

### For First-Time Setup

1. **Read the audit plan** (`knowledge/sop/post-deployment-audit-plan.md`)
2. **Copy the metrics dashboard** (`knowledge/sop/audit-metrics-dashboard.md`)
3. **Set up weekly audit schedule** (Every Friday, 2 hours)
4. **Assign audit owner** (typically Main Assistant or designated operator)
5. **Create audit log** in `memory/global.md` with `[AUDIT]` tag

### For Weekly Audit (2 Hours)

1. **Collect data** (30 min) — gather metrics from logs, files, feedback
2. **Analyze findings** (45 min) — compare against targets, identify issues
3. **Document results** (30 min) — update dashboard, log decisions
4. **Report & recommend** (15 min) — summarize for Fathur, propose actions

---

## Implementation Phases

### Phase 1: Setup (Week 1)

**Goal:** Establish audit infrastructure and baseline metrics.

**Tasks:**

- [ ] Create audit directory structure
  ```bash
  mkdir -p /home/fatur/ai-holding/audits/{2026-05,2026-06,2026-07}
  ```

- [ ] Copy audit templates
  ```bash
  cp knowledge/sop/post-deployment-audit-plan.md audits/AUDIT_PLAN.md
  cp knowledge/sop/audit-metrics-dashboard.md audits/METRICS_DASHBOARD.md
  ```

- [ ] Initialize audit log in `memory/global.md`
  ```
  [AUDIT] 2026-05-18 — Post-deployment audit framework initialized
  ```

- [ ] Schedule weekly audits (Friday 14:00 UTC)

- [ ] Assign audit owner and backup

- [ ] Create audit checklist in `COMMANDS.md`

**Deliverable:** Audit infrastructure ready, first baseline metrics collected

---

### Phase 2: Data Collection (Week 1-2)

**Goal:** Establish reliable data collection pipelines.

**Tasks:**

- [ ] Set up `tasks/logs.jsonl` monitoring
  - Verify all task executions logged
  - Check timestamp accuracy
  - Validate status field (success/failure)

- [ ] Set up memory monitoring
  - Track `MEMORY.md` file size
  - Track `memory/global.md` growth
  - Track company MEMORY.md sizes

- [ ] Set up tool usage tracking
  - Log all tool invocations
  - Capture tool errors
  - Track rate limit hits

- [ ] Set up response time tracking
  - Capture task received timestamp
  - Capture first response timestamp
  - Capture completion timestamp

- [ ] Set up error tracking
  - Capture all errors in logs
  - Categorize by type
  - Track escalations

- [ ] Set up feedback collection
  - Create feedback form/template
  - Establish feedback channel
  - Set collection frequency

**Deliverable:** All data sources feeding into audit dashboard

---

### Phase 3: Baseline Establishment (Week 2-3)

**Goal:** Establish baseline metrics for comparison.

**Tasks:**

- [ ] Run full 4-layer audit
  - Collect all metrics
  - Document current state
  - Identify gaps

- [ ] Establish targets
  - Review success criteria
  - Adjust targets if needed
  - Document rationale

- [ ] Create baseline report
  - Current state snapshot
  - Comparison to targets
  - Gap analysis

- [ ] Identify quick wins
  - Low-effort improvements
  - High-impact fixes
  - Priority ranking

**Deliverable:** Baseline metrics established, targets confirmed, quick wins identified

---

### Phase 4: Continuous Monitoring (Week 3+)

**Goal:** Establish sustainable weekly audit rhythm.

**Tasks:**

- [ ] Run weekly audits (every Friday)
  - Collect metrics
  - Compare to targets
  - Identify trends

- [ ] Update metrics dashboard
  - Fill in current values
  - Update status indicators
  - Note issues

- [ ] Log audit results
  - Record in `memory/global.md`
  - Tag with `[AUDIT]`
  - Include summary + recommendations

- [ ] Report to Fathur
  - Weekly summary
  - Critical issues
  - Recommended actions

- [ ] Execute approved actions
  - Implement fixes
  - Update framework
  - Document changes

**Deliverable:** Sustainable weekly audit cycle established

---

## Detailed Audit Execution Steps

### Step 1: Collect Data (30 minutes)

**1.1 Agent Behavior Data**

```bash
# Count Tier 1/2/3 actions
grep -c '"tier": "1"' tasks/logs.jsonl
grep -c '"tier": "2"' tasks/logs.jsonl
grep -c '"tier": "3"' tasks/logs.jsonl

# Count Tier 2 logs
grep -c '\[AUTO-LOG' memory/global.md

# Count escalations
grep -c '"escalated": true' tasks/logs.jsonl

# Count tool invocations
grep -c '"tool_used"' tasks/logs.jsonl

# Count tool errors
grep -c '"tool_error"' tasks/logs.jsonl
```

**1.2 Framework Adoption Data**

```bash
# Check SOUL tier coverage
find companies/*/agents -name "*.md" | wc -l

# Check memory file sizes
wc -c MEMORY.md memory/global.md companies/*/MEMORY.md

# Check knowledge file sizes
du -sh knowledge/

# Count memory entries
grep -c '^\[' memory/global.md
```

**1.3 Performance Data**

```bash
# Extract response times from logs
jq '.response_time_ms' tasks/logs.jsonl | sort -n

# Calculate percentiles
jq '.response_time_ms' tasks/logs.jsonl | sort -n | tail -5

# Count timeouts
grep -c '"timeout": true' tasks/logs.jsonl

# Count failures
grep -c '"status": "failed"' tasks/logs.jsonl
```

**1.4 Quality Data**

```bash
# Count outputs with issues
grep -c 'TODO\|PLACEHOLDER' tasks/logs.jsonl

# Count boundary violations
grep -c 'boundary_violation' tasks/logs.jsonl

# Count user feedback
grep -c 'feedback' memory/global.md
```

---

### Step 2: Analyze Findings (45 minutes)

**2.1 Compare to Targets**

For each metric:
1. Get current value
2. Compare to target
3. Determine status (✓ pass, ⚠ warning, ✗ fail)
4. Calculate variance

**2.2 Identify Trends**

For each metric:
1. Get last 4 weeks of data
2. Plot trend (↑ improving, → stable, ↓ degrading)
3. Extrapolate if trend continues
4. Flag if trend is concerning

**2.3 Root Cause Analysis**

For each failing metric:
1. What is the issue?
2. Why is it happening?
3. What is the impact?
4. What are possible fixes?

**2.4 Prioritize Issues**

1. Separate by severity (critical/medium/low)
2. Separate by impact (high/medium/low)
3. Separate by effort (easy/medium/hard)
4. Create priority matrix

---

### Step 3: Document Results (30 minutes)

**3.1 Update Metrics Dashboard**

```markdown
[AUDIT — 2026-05-18]

[LAYER 1: AGENT BEHAVIOR]
Autonomy Tier Compliance:
  - Tier 1 auto-execution rate: 96% (target 95%+) ✓
  - Tier 2 logging compliance: 100% (target 100%) ✓
  - Tier 3 confirmation rate: 100% (target 100%) ✓
  - False Tier 3 escalations: 2% (target <5%) ✓
  - Tier misclassification: 0% (target 0%) ✓

[LAYER 2: FRAMEWORK ADOPTION]
...

[LAYER 3: PERFORMANCE]
...

[LAYER 4: QUALITY]
...

[SUMMARY]
Overall health: 🟢 Green
Critical issues: 0
Medium issues: 1
Low issues: 2
```

**3.2 Log in Memory**

```markdown
[AUDIT] 2026-05-18 — Weekly audit complete
Status: Green (all layers passing)
Issues: 1 medium (memory growth rate 52 lines/week, target <50)
Recommendations: Archive old entries from memory/global.md
```

**3.3 Create Audit Report**

```markdown
# Audit Report — 2026-05-18

## Executive Summary
All systems operating within acceptable parameters. One minor issue identified.

## Metrics Summary
- Agent Behavior: ✓ Pass
- Framework Adoption: ⚠ Warning (memory growth)
- Performance: ✓ Pass
- Quality: ✓ Pass

## Issues Found
1. Memory growth rate 52 lines/week (target <50)
   - Cause: Increased task logging
   - Impact: Minor (still <500KB)
   - Fix: Archive entries >30 days old

## Recommendations
1. Archive memory/global.md entries from April
2. Continue monitoring memory growth
3. No other actions needed

## Next Audit
2026-05-25 (Friday)
```

---

### Step 4: Report & Recommend (15 minutes)

**4.1 Prepare Summary for Fathur**

```
Weekly Audit Summary — 2026-05-18

Status: 🟢 Green (all systems healthy)

Key Metrics:
- Tier 1 auto-execution: 96% ✓
- Tier 2 logging: 100% ✓
- Tier 3 confirmation: 100% ✓
- Response time: 1.8m avg ✓
- Error rate: 1.2% ✓
- Output quality: 96% ✓
- Boundary compliance: 100% ✓

Issues: 1 minor
- Memory growth slightly above target (52 vs 50 lines/week)
- Action: Archive old entries

Recommendations:
1. Archive memory/global.md entries from April
2. Continue current trajectory
3. Next audit: 2026-05-25
```

**4.2 Propose Actions**

For each issue:
1. State the issue clearly
2. Propose specific action
3. Estimate effort (hours)
4. Estimate impact (high/medium/low)
5. Recommend priority (now/this week/this month)

**4.3 Get Approval**

- [ ] Fathur reviews summary
- [ ] Fathur approves recommended actions
- [ ] Operator executes approved actions
- [ ] Log execution in memory

---

## Audit Checklist Template

Use this for each weekly audit:

```
[AUDIT CHECKLIST — 2026-05-18]

PRE-AUDIT (5 min)
- [ ] Gather all data sources
- [ ] Open metrics dashboard
- [ ] Review last week's issues

LAYER 1: AGENT BEHAVIOR (10 min)
- [ ] Autonomy tier compliance
- [ ] Escalation patterns
- [ ] Tool usage compliance
- [ ] Issues found: ___

LAYER 2: FRAMEWORK ADOPTION (10 min)
- [ ] SOUL compliance
- [ ] Memory discipline
- [ ] Knowledge loading
- [ ] Issues found: ___

LAYER 3: PERFORMANCE (10 min)
- [ ] Response time
- [ ] Error rates
- [ ] Resource usage
- [ ] Issues found: ___

LAYER 4: QUALITY (10 min)
- [ ] Output quality
- [ ] Safety boundaries
- [ ] User satisfaction
- [ ] Issues found: ___

ANALYSIS (15 min)
- [ ] Identify trends
- [ ] Root cause analysis
- [ ] Prioritize issues
- [ ] Prepare recommendations

DOCUMENTATION (10 min)
- [ ] Update dashboard
- [ ] Log in memory
- [ ] Create report
- [ ] Prepare summary

REPORTING (5 min)
- [ ] Send to Fathur
- [ ] Get approval
- [ ] Execute actions
- [ ] Close audit

TOTAL TIME: ~75 minutes
```

---

## Tools & Scripts

### Audit Data Collection Script

Create `/home/fatur/ai-holding/bin/audit-collect.sh`:

```bash
#!/bin/bash
# Collect audit metrics

AUDIT_DATE=$(date +%Y-%m-%d)
AUDIT_DIR="audits/$AUDIT_DATE"
mkdir -p "$AUDIT_DIR"

echo "Collecting audit data for $AUDIT_DATE..."

# Agent behavior
echo "=== AGENT BEHAVIOR ===" > "$AUDIT_DIR/metrics.txt"
echo "Tier 1 count: $(grep -c '"tier": "1"' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"
echo "Tier 2 count: $(grep -c '"tier": "2"' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"
echo "Tier 3 count: $(grep -c '"tier": "3"' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"
echo "Escalations: $(grep -c '"escalated": true' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"

# Framework adoption
echo "" >> "$AUDIT_DIR/metrics.txt"
echo "=== FRAMEWORK ADOPTION ===" >> "$AUDIT_DIR/metrics.txt"
echo "SOUL files: $(find companies/*/agents -name "*.md" | wc -l)" >> "$AUDIT_DIR/metrics.txt"
echo "MEMORY.md size: $(wc -c < MEMORY.md) bytes" >> "$AUDIT_DIR/metrics.txt"
echo "memory/global.md size: $(wc -c < memory/global.md) bytes" >> "$AUDIT_DIR/metrics.txt"

# Performance
echo "" >> "$AUDIT_DIR/metrics.txt"
echo "=== PERFORMANCE ===" >> "$AUDIT_DIR/metrics.txt"
echo "Total tasks: $(wc -l < tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"
echo "Failed tasks: $(grep -c '"status": "failed"' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"
echo "Tool errors: $(grep -c '"tool_error"' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"

# Quality
echo "" >> "$AUDIT_DIR/metrics.txt"
echo "=== QUALITY ===" >> "$AUDIT_DIR/metrics.txt"
echo "Outputs with TODO: $(grep -c 'TODO' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"
echo "Boundary violations: $(grep -c 'boundary_violation' tasks/logs.jsonl)" >> "$AUDIT_DIR/metrics.txt"

echo "Data collected to $AUDIT_DIR/metrics.txt"
cat "$AUDIT_DIR/metrics.txt"
```

### Audit Report Generator

Create `/home/fatur/ai-holding/bin/audit-report.py`:

```python
#!/usr/bin/env python3
"""Generate audit report from collected metrics."""

import json
import sys
from datetime import datetime
from pathlib import Path

def load_metrics(audit_dir):
    """Load metrics from audit directory."""
    metrics_file = Path(audit_dir) / "metrics.txt"
    metrics = {}
    
    with open(metrics_file) as f:
        section = None
        for line in f:
            line = line.strip()
            if line.startswith("==="):
                section = line.strip("=").strip()
                metrics[section] = {}
            elif line and section:
                key, value = line.split(": ", 1)
                metrics[section][key] = value
    
    return metrics

def compare_to_targets(metrics):
    """Compare metrics to targets."""
    targets = {
        "AGENT BEHAVIOR": {
            "Tier 1 count": (">", 0),
            "Tier 2 count": (">", 0),
            "Tier 3 count": (">", 0),
        },
        "FRAMEWORK ADOPTION": {
            "SOUL files": ("==", 32),
        },
        "PERFORMANCE": {
            "Failed tasks": ("<", 2),
        },
    }
    
    results = {}
    for section, section_metrics in metrics.items():
        results[section] = {}
        for key, value in section_metrics.items():
            if section in targets and key in targets[section]:
                op, target = targets[section][key]
                val = int(value.split()[0])
                
                if op == ">" and val > target:
                    status = "✓"
                elif op == "<" and val < target:
                    status = "✓"
                elif op == "==" and val == target:
                    status = "✓"
                else:
                    status = "✗"
                
                results[section][key] = (value, target, status)
    
    return results

def generate_report(audit_date, metrics, results):
    """Generate audit report."""
    report = f"""# Audit Report — {audit_date}

## Executive Summary
Audit completed on {audit_date}.

## Metrics

"""
    
    for section, section_results in results.items():
        report += f"### {section}\n\n"
        for key, (value, target, status) in section_results.items():
            report += f"- {key}: {value} (target: {target}) {status}\n"
        report += "\n"
    
    return report

if __name__ == "__main__":
    audit_date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    audit_dir = f"audits/{audit_date}"
    
    metrics = load_metrics(audit_dir)
    results = compare_to_targets(metrics)
    report = generate_report(audit_date, metrics, results)
    
    print(report)
    
    # Save report
    report_file = Path(audit_dir) / "report.md"
    report_file.write_text(report)
    print(f"\nReport saved to {report_file}")
```

---

## Integration with Existing Systems

### Update COMMANDS.md

Add audit commands:

```markdown
## Audit Commands

### Run Weekly Audit
```
@main audit-weekly
```
Runs full 4-layer audit, updates dashboard, generates report.

### Collect Audit Data
```
@main audit-collect
```
Collects raw metrics from logs and files.

### Generate Audit Report
```
@main audit-report [DATE]
```
Generates formatted report from collected metrics.

### View Audit Dashboard
```
@main audit-dashboard
```
Shows current metrics dashboard.
```

### Update HEARTBEAT.md

Add audit check:

```markdown
## System Audit (Weekly)

Every Friday (or ad-hoc after major update):

Run 4-layer audit:
- **Layer 1** — Agent Behavior (autonomy, escalation, tools)
- **Layer 2** — Framework Adoption (SOUL, memory, knowledge)
- **Layer 3** — Performance (response time, errors, resources)
- **Layer 4** — Quality (output, boundaries, satisfaction)

Output findings + proposed edits. **Never auto-apply.** Always ask: "Apply now or review first?"

Reference: `knowledge/sop/post-deployment-audit-plan.md`
```

### Update memory/global.md

Add audit entries:

```markdown
[AUDIT] 2026-05-18 — Post-deployment audit framework initialized
[AUDIT] 2026-05-25 — Weekly audit: Green status, 1 minor issue (memory growth)
```

---

## Success Metrics for Audit Implementation

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Audit completion rate | 100% | Count: (audits completed) / (scheduled audits) |
| Audit on-time rate | 95%+ | Count: (audits on schedule) / (total audits) |
| Issue identification rate | 95%+ | Manual review: issues found vs actual issues |
| Action execution rate | 90%+ | Count: (approved actions executed) / (total approved) |
| Audit quality | 95%+ | Manual review: audit thoroughness + accuracy |

---

## Troubleshooting

### Issue: Missing data in logs

**Solution:**
- Verify `tasks/logs.jsonl` is being written to
- Check file permissions
- Ensure all agents are logging correctly

### Issue: Metrics don't match reality

**Solution:**
- Verify data collection script is correct
- Check for data corruption
- Re-run collection manually

### Issue: Audit takes too long

**Solution:**
- Parallelize data collection
- Use sampling for large datasets
- Automate metric calculations

### Issue: Trends are unclear

**Solution:**
- Collect more historical data
- Use moving averages
- Visualize trends graphically

---

## References

- `knowledge/sop/post-deployment-audit-plan.md` — full audit plan
- `knowledge/sop/audit-metrics-dashboard.md` — metrics dashboard
- `knowledge/sop/system-audit.md` — audit protocol
- `HEARTBEAT.md` — reflection loop
- `MEMORY.md` — strategic memory
