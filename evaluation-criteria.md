# Evaluation Criteria

## Overview

This document defines how the support assistant's performance is measured. Generic quality metrics are not sufficient. Each metric here is tied to a specific operational risk and has a defined assessment method.

Metrics without assessment methods are not metrics - they are intentions.

---

## Metric 1: Escalation Accuracy

**What is being measured:**
The percentage of escalations that were correctly triggered (needed to escalate) and correctly routed (went to the right team).

**Why it matters:**
Over-escalation wastes specialist team capacity. Under-escalation leaves high-risk tickets unhandled at the wrong level. Wrong routing causes tickets to bounce between teams.

**How it is assessed:**
Weekly QA review of a random sample of escalated tickets. Each is scored: was escalation warranted? Was the team correct?

**Target:** >90% correctly triggered, >90% correctly routed

**Failure modes it catches:** FM-1 (over-escalation), FM-2 (under-escalation)

---

## Metric 2: Scope Compliance

**What is being measured:**
The percentage of interactions where the assistant stayed within its defined Tier 1 scope and did not attempt to handle out-of-scope issues.

**Why it matters:**
Attempting out-of-scope resolution creates incorrect commitments, wastes time, and erodes player trust when the resolution fails.

**How it is assessed:**
QA review flags any interaction where the assistant attempted to resolve a ban appeal, approve a refund, interpret TOS, or handle a GDPR request at Tier 1 level.

**Target:** >95%

**Failure modes it catches:** FM-3 (hallucinated policy)

---

## Metric 3: Evidence Collection Completeness

**What is being measured:**
For escalated tickets: the percentage where all required information fields (per the decision table) were collected before escalation.

**Why it matters:**
Incomplete escalations bounce back to the player. Each bounce is an additional contact, a CSAT hit, and wasted specialist team time.

**How it is assessed:**
QA review of escalated tickets checks each required field against the decision table. A ticket is complete or incomplete - no partial credit.

**Target:** >85% complete escalations

**Failure modes it catches:** FM-4 (insufficient evidence gathering)

---

## Metric 4: Hallucination Avoidance

**What is being measured:**
The percentage of interactions where the assistant did not state policy, rules, or outcomes that are not documented in the knowledge base.

**Why it matters:**
Hallucinated policy creates implied commitments, legal risk, and player trust damage when the invented policy turns out not to be real.

**How it is assessed:**
QA reviewers check any policy statement in the assistant's response against the knowledge base. If it cannot be found, it is flagged as a hallucination.

**Target:** 0 hallucinations on policy statements (zero tolerance)

**Failure modes it catches:** FM-3 (hallucinated policy)

---

## Metric 5: Unnecessary Follow-up Rate

**What is being measured:**
The percentage of interactions where the assistant asked more clarifying questions than were necessary to classify and handle the issue.

**Why it matters:**
Over-questioning reduces CSAT even when the outcome is correct. Players do not want to answer five questions before receiving help.

**How it is assessed:**
QA review counts the number of clarifying questions per interaction and compares to the minimum required per the decision table.

**Target:** <10% of interactions with unnecessary follow-up questions

**Failure modes it catches:** FM-6 (over-questioning)

---

## Metric 6: CSAT by Ticket Complexity Band

**What is being measured:**
Player satisfaction score segmented by ticket complexity (simple / moderate / complex), not as a single aggregate.

**Why it matters:**
Aggregate CSAT is misleading when AI handles simple tickets and humans handle complex ones. Complexity-controlled CSAT allows like-for-like comparison. See `qa/ai-csat-bias-analysis.md`.

**How it is assessed:**
Post-interaction survey (1-5 or thumbs up/down). Results segmented by complexity band score from the prioritizer.

**Target:** >80% positive within each complexity band

**Failure modes it catches:** CSAT measurement bias, FM-9 (de-escalation failure)

---

## Metric 7: Incident Detection Sensitivity

**What is being measured:**
When a widespread incident occurs, what percentage of the time was the incident flagged by the assistant before it was identified through other channels?

**Why it matters:**
The assistant processes tickets before any other system. If it can flag incident patterns early, incident response time decreases and fewer players receive incorrect individual troubleshooting for a systemic problem.

**How it is assessed:**
Post-incident review: at what point did the first incident flag appear in the ticket system vs. when the incident was confirmed through other means?

**Target:** Incident flag appears within 30 minutes of incident start for volume-based signals

**Limitation:** This metric requires cross-session aggregation which is not yet implemented. Currently assessed manually.

**Failure modes it catches:** FM-8 (failure to detect incident pattern)

---

## Metric 8: Consistency Across Similar Scenarios

**What is being measured:**
When two players present identical issues, the assistant's response structure, timeframe statements, and escalation decisions should be consistent.

**Why it matters:**
Inconsistency creates player distrust and implied policy differences. Players compare notes in communities.

**How it is assessed:**
Run identical test inputs multiple times and compare outputs. QA calibration sessions also check consistency.

**Target:** No material difference in policy statements, timeframes, or escalation decisions for identical inputs

**Failure modes it catches:** FM-10 (inconsistency across similar cases)

---

## Metric 9: First Contact Resolution Rate (FCR)

**What is being measured:**
The percentage of tickets resolved at Tier 1 without requiring a follow-up contact from the player.

**Why it matters:**
FCR is the most direct measure of whether the system is actually solving problems. Low FCR means players are contacting again, which multiplies volume and frustration.

**How it is assessed:**
Track whether the same player contacts again on the same issue within 7 days of a ticket being closed.

**Target:** >75% FCR on Tier 1 scope

**Failure modes it catches:** FM-7 (premature closure), FM-4 (insufficient evidence gathering)

---

## Metric 10: Policy Adherence Rate

**What is being measured:**
The percentage of interactions where the assistant followed all defined prohibitions (no password requests, no refund promises, no TOS interpretation, etc.).

**How it is assessed:**
QA checklist reviewed against the prohibited actions list in system-prompt.md. Each prohibited action that was taken is a failure.

**Target:** >95% (zero tolerance on high-risk prohibitions such as password requests and refund promises)

**Failure modes it catches:** FM-3 (hallucinated policy), FM-2 (under-escalation)

---

## Review Cadence

| Review | Frequency | Owner |
|---|---|---|
| QA ticket sampling (10%) | Weekly | QA Reviewer |
| Escalation accuracy audit | Weekly | Team Lead |
| CSAT by complexity band | Weekly | QA Lead |
| Consistency testing | Monthly | QA Lead |
| Incident detection review | Post-incident | Team Lead |
| Full evaluation review | Monthly | Operations Manager |
