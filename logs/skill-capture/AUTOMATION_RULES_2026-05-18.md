# Skill Capture Automation Rules
**Date:** 2026-05-18 04:16 UTC

## Rule 1: Repeated Decision Pattern
- Trigger: Same decision made 3+ times in 7 days
- Action: Create skill draft
- Review: Fathur approval required
- Status: ACTIVE
- Example: API design decisions → `nexusai/skills/api-design-pattern`

## Rule 2: Workflow Completion Pattern
- Trigger: Workflow completed successfully 5+ times
- Action: Create skill draft
- Review: Fathur approval required
- Status: ACTIVE
- Example: Content production workflow → `brandflow/skills/content-production`

## Rule 3: Error Recovery Pattern
- Trigger: Same error resolved 3+ times
- Action: Create troubleshooting skill
- Review: Fathur approval required
- Status: ACTIVE
- Example: API timeout handling → `nexusai/skills/api-timeout-recovery`

## Rule 4: Tool Integration Pattern
- Trigger: Tool used 3+ times with same pattern
- Action: Create tool integration skill
- Review: Fathur approval required
- Status: ACTIVE
- Example: Figma design workflow → `brandflow/skills/figma-workflow`

## Rule 5: Decision Authority Pattern
- Trigger: 3+ decisions in same category
- Action: Create decision framework skill
- Review: Fathur approval required
- Status: ACTIVE
- Example: Market analysis decisions → `crypto/skills/market-analysis-framework`

## Rule 6: Escalation Pattern
- Trigger: 3+ escalations with same root cause
- Action: Create escalation handling skill
- Review: Fathur approval required
- Status: ACTIVE
- Example: Budget escalations → `nexusai/skills/budget-escalation-handling`

## Automation Status
- All rules: ACTIVE
- Monitoring: ENABLED
- Logging: ENABLED
- Approval workflow: ENABLED
- Publication: ENABLED

## Performance Targets
- Detection latency: <1 hour
- Draft creation: <5 minutes
- Approval turnaround: <24 hours
- Publication: <1 hour after approval

## Next check: 2026-05-19 04:16 UTC
