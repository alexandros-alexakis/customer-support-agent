# Evaluation Criteria

## Overview

This document defines the key performance indicators (KPIs) used 
to measure the effectiveness of the AI customer support agent. 
These metrics mirror the standards used to evaluate human Tier 1 
agents in gaming support operations.

---

## Primary KPIs

### 1. First Contact Resolution (FCR)

**Definition:** The percentage of tickets resolved without requiring 
escalation or a follow-up contact from the player.

**Target:** >75% for issues within Tier 1 scope

**How to measure:**
- Tag each conversation as resolved or escalated
- Calculate: (Resolved tickets / Total tickets) x 100
- Exclude out-of-scope tickets from the denominator

---

### 2. Average Handling Time (AHT)

**Definition:** The average time taken from first player message 
to ticket closure or escalation.

**Target:** Reduction vs. human Tier 1 baseline

**How to measure:**
- Record timestamp of first player message and ticket close
- Calculate average across a sample of at least 50 tickets
- Compare against human agent AHT benchmark

---

### 3. Escalation Accuracy

**Definition:** The percentage of escalations that were correctly 
routed to the right specialist team with sufficient information.

**Target:** >90% correctly routed escalations

**How to measure:**
- Review escalated tickets with specialist teams weekly
- Flag incorrectly routed or incomplete escalations
- Calculate: (Correct escalations / Total escalations) x 100

---

### 4. Player Satisfaction (CSAT)

**Definition:** Player-reported satisfaction score collected via 
post-interaction survey.

**Target:** Maintained or improved vs. human Tier 1 baseline

**How to measure:**
- Deploy a 1-5 star or thumbs up/down survey after ticket closure
- Calculate average score across all rated interactions
- Track weekly and flag drops of more than 0.3 points

---

### 5. Policy Compliance Rate

**Definition:** The percentage of responses that correctly followed 
defined policies (no unauthorized promises, correct escalation 
triggers, appropriate tone).

**Target:** >95%

**How to measure:**
- Conduct weekly QA review of a random sample of tickets (10%)
- Score each ticket against the compliance checklist below
- Calculate: (Compliant tickets / Reviewed tickets) x 100

---

## QA Compliance Checklist

For each reviewed ticket, verify:

| Check | Pass / Fail |
|---|---|
| Agent did not ask for player password | |
| Agent did not promise refunds or compensation without authorization | |
| Agent escalated correctly when required | |
| Agent collected required information before escalating | |
| Tone was professional and empathetic throughout | |
| Response was concise and clear | |
| Player was informed of next steps | |

---

## Review Cadence

| Review Type | Frequency |
|---|---|
| KPI dashboard review | Weekly |
| QA ticket sampling | Weekly |
| Escalation accuracy audit | Weekly |
| Full performance review | Monthly |

---

## Iteration Process

When KPIs fall below target:

1. Identify the ticket categories where failures occurred.
2. Review whether the system prompt or FAQ content is insufficient.
3. Update the relevant knowledge base file or system prompt rule.
4. Re-test against the same ticket category.
5. Document the change and the reason in the repository commit history.
