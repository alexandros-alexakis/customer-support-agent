# Evaluation Criteria

## Overview

This document defines the metrics used to evaluate the performance 
of the Claude AI customer support agent. These criteria are based 
on standard customer support KPIs adapted for an AI-assisted 
Tier 1 operation in gaming support.

---

## Primary KPIs

| Metric | Definition | Target |
|---|---|---|
| First Contact Resolution (FCR) | Percentage of tickets resolved at Tier 1 without escalation | >75% |
| Average Handling Time (AHT) | Average time taken to resolve or escalate a ticket | Reduction vs. human baseline |
| Escalation Accuracy | Percentage of escalations that were correctly routed | >90% |
| Incorrect Escalation Rate | Tickets escalated unnecessarily or to wrong team | <10% |
| Player Satisfaction (CSAT) | Post-interaction satisfaction score from players | Maintained or improved vs. human Tier 1 |
| Policy Compliance Rate | Responses that correctly follow documented policies | >98% |

---

## Secondary KPIs

| Metric | Definition |
|---|---|
| Containment Rate | Percentage of contacts fully handled by agent without human involvement |
| Repeat Contact Rate | Players who contact support again within 7 days on same issue |
| Escalation Volume by Category | Breakdown of escalations by issue type to identify knowledge gaps |
| Response Consistency Score | Degree to which similar queries receive consistent responses |

---

## Evaluation Method

### Phase 1 - Prompt Testing (Pre-deployment)
- Run 50 simulated ticket scenarios covering all Tier 1 categories.
- Evaluate each response against tone, accuracy, policy compliance, 
  and escalation logic.
- Identify gaps in the knowledge base or system prompt and iterate.

### Phase 2 - Shadow Mode (Parallel running)
- Run the agent alongside human agents on live tickets.
- Compare agent responses to human responses on identical or similar issues.
- Score against primary KPIs without exposing agent responses to players.

### Phase 3 - Supervised Live Testing
- Allow agent to handle a controlled volume of real tickets.
- Human agent reviews all responses before they are sent.
- Collect CSAT data and compare to human Tier 1 baseline.

### Phase 4 - Independent Operation
- Agent handles Tier 1 tickets autonomously within defined scope.
- Human oversight maintained for escalations and edge cases.
- Weekly KPI review to identify drift or degradation in performance.

---

## Failure Conditions

The agent should be reviewed and retrained if any of the following occur:

- FCR drops below 65% for two consecutive weeks
- Incorrect escalation rate exceeds 15%
- CSAT drops more than 5 points below human Tier 1 baseline
- Policy compliance rate drops below 95%
- Any instance of the agent making commitments outside its defined scope

---

## Review Cadence

| Review Type | Frequency |
|
