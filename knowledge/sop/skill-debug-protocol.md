# Skill: 6-Step Debug Protocol

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** All QA agents, NexusAI DevOps, Operator  
**Trigger:** Any fault reported (syntax, runtime, logic, environment, network, dependency, data, content, process)  
**Frequency:** 10x/month (cross-company fault diagnosis)  
**Risk Level:** Medium

---

## Purpose

Systematically diagnose and fix faults using a standardized 6-step protocol. Ensures root cause is identified before prescribing fixes, preventing symptom-only patches.

---

## Prerequisites

- Access to error logs and system state
- Understanding of the affected system (code, config, data, process)
- Ability to run verification commands
- Access to relevant SOP files (especially cross-company-qa-routing.md for cross-company faults)

---

## Steps

### Step 1: Gather (Semua Sekaligus)

Collect ALL information in one pass. Don't ask piecemeal.

**Required fields:**

```
Exact error text:        [full error, not paraphrase]
Last action before fault: [what was happening when it broke]
Environment:            [OS, runtime version, company, agent, tool versions]
Last known working state: [when did this last work?]
Recent changes:         [commits, config edits, deployments in last 24h]
Affected scope:         [single user, one company, all companies?]
Reproducibility:        [always fails, intermittent, one-time?]
```

**Example:**

```
Exact error text: "TypeError: Cannot read property 'price' of undefined at line 42 of price_scraper.py"
Last action: Ran daily crypto tools refresh at 07:00 WIB
Environment: Python 3.9, Ubuntu 20.04, Crypto Consultant, price_scraper v2.1
Last known working: Yesterday 07:00 WIB (same time, same script)
Recent changes: Deployed price_scraper v2.1 yesterday 18:00 UTC (12 hours ago)
Affected scope: Crypto Consultant only
Reproducibility: Always fails at 07:00 WIB
```

---

### Step 2: Classify

Determine fault category:

```
syntax       → malformed instruction (markdown broken, code typo, JSON malformed)
runtime      → valid syntax, execution failure (script crashes, tool returns error)
logic        → runs clean, output wrong (wrong calculation, wrong data routed)
environment  → missing var, wrong version, permission denied
network      → timeout, DNS, port, firewall, API rate limit
dependency   → missing module, version conflict, package broken
data         → input format wrong, source stale, schema mismatch
content      → factual error, brand violation, disclaimer missing
process      → SOP not followed, handoff block missing, approval skipped
```

**Example:** "runtime — script crashes with TypeError"

---

### Step 3: Diagnose

Identify root cause and mechanism:

```
Root cause:  [specific line / config / step / data point]
Mechanism:   [one sentence: why this causes failure]
```

**Example:**

```
Root cause:  price_scraper v2.1 line 42: accessing response['price'] without checking if 'price' key exists
Mechanism:   API response format changed (v2.1 expects 'price' but API now returns 'current_price'), causing KeyError
```

**Rule:** Diagnose first. Don't prescribe yet.

---

### Step 4: Resolve

Exact corrective action(s):

```bash
# For code: specific command or edit
# For config: specific setting change
# For process: specific SOP step to execute
```

**Example:**

```bash
# Fix: Update price_scraper.py line 42
# OLD: price = response['price']
# NEW: price = response.get('price') or response.get('current_price')

# Then test:
python3 price_scraper.py --test
```

---

### Step 5: Verify

Run verification command to prove fix works:

```bash
# Command that proves fix is effective
# Don't skip this — "should work" ≠ "verified work"
```

**Example:**

```bash
# Run the script that was failing
python3 bin/run_crypto_tools.sh

# Check logs for success
tail -20 logs/crypto-tools-*.log | grep "price_scraper.*SUCCESS"

# Verify data was written
ls -la companies/crypto-consultant/tasks/data-*.jsonl | tail -1
```

**Rule:** If verification fails, go back to Step 3 (diagnose again). Don't patch symptoms.

---

### Step 6: Harden

Add config/SOP/test to prevent recurrence:

```
# Config change: add validation
# SOP update: add pre-flight check
# Test added: unit test for this scenario
# Monitoring: alert if this error happens again
```

**Example:**

```
# Add to price_scraper.py:
def validate_response(response):
    required_keys = ['price', 'current_price', 'last_price']
    if not any(k in response for k in required_keys):
        raise ValueError(f"Response missing price field. Got: {response.keys()}")
    return response.get('price') or response.get('current_price')

# Add unit test:
def test_price_scraper_handles_api_format_change():
    response_old = {'price': 100}
    response_new = {'current_price': 100}
    assert validate_response(response_old) == 100
    assert validate_response(response_new) == 100

# Add to monitoring:
- Alert if price_scraper fails 2+ times in 1 hour
```

---

## Input Format

```json
{
  "error_text": "full error message",
  "last_action": "what was happening",
  "environment": "OS, versions, company, agent",
  "last_working": "when did this last work",
  "recent_changes": "commits, config edits, deployments",
  "affected_scope": "single user / company / all",
  "reproducibility": "always / intermittent / one-time"
}
```

---

## Output Format

```
[ROOT CAUSE]
<specific line / config / step / data point>

[MECHANISM]
<one sentence: why this causes failure>

[FIX]
<exact commands / edits / SOP steps>

[VERIFY]
<verification command / check>

[HARDEN]
<prevention — config update, test added, monitoring added>
```

---

## Special Case: Cross-Company Fault

If fault involves handoff between companies:

1. **Identify:** Where was fault DETECTED vs where did it ORIGINATE?
   - Example: BrandFlow content has wrong number (detected in BrandFlow) but source is Crypto research (originated in Crypto)

2. **Routing:** Apply cross-company-qa-routing.md
   - Fix is not in BrandFlow, but in Crypto Consultant's handoff protocol
   - Both companies' QA review the fix before hardening

3. **Harden:** Update handoff SOP to prevent recurrence
   - Example: Add QA gate post-revision in Crypto Consultant

---

## Common Errors & Recovery

| Error | Cause | Recovery |
|-------|-------|----------|
| Can't reproduce the fault | Environment difference or intermittent issue | Ask for more details. Try in exact same environment. Check logs for pattern. |
| Multiple possible root causes | Insufficient data gathered | Go back to Step 1. Gather more information. Don't guess. |
| Fix works in staging but fails in production | Environment difference | Verify production environment matches staging. Check config differences. |
| Same fault recurs after fix | Hardening step skipped | Add test / monitoring / config to prevent recurrence. |
| Cross-company fault, unclear ownership | Handoff ambiguous | Escalate to Operator. Both companies' QA review. |

---

## Verification

- [ ] All 7 information fields gathered (Step 1)
- [ ] Fault classified into one category (Step 2)
- [ ] Root cause identified (not symptom) (Step 3)
- [ ] Fix is specific and executable (Step 4)
- [ ] Verification command proves fix works (Step 5)
- [ ] Hardening prevents recurrence (Step 6)
- [ ] No "try this and see" — diagnosis before prescription

---

## Notes

- **Diagnosis first:** Never prescribe without understanding root cause.
- **Verification mandatory:** "Should work" is not acceptable. Prove it works.
- **Hardening required:** If same bug can recur, there's a gap in the system.
- **Cross-company:** If fault crosses company boundaries, both QA agents review.
- **Anti-pattern:** Patching symptoms without fixing root cause leads to recurring bugs.

---

## Related Skills

- Skill: Cross-Company QA Routing & Checklist Execution (routes cross-company faults)
- Skill: System Audit (detects recurring fault patterns)
- SOP: debug-protocol.md (full specification)
- SOP: cross-company-qa-routing.md (cross-company fault routing)
