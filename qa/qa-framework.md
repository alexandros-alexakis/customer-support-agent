# QA Framework

## Overview

This document defines the quality assurance framework used to evaluate customer support interactions handled by both the AI agent and human agents. All interactions are scored against the same criteria to ensure consistency.

---

## Scoring Model

Each interaction is scored out of 100 points across five categories:

| Category | Weight | Max Points |
|---|---|---|
| Tone and Empathy | 20% | 20 |
| Accuracy and Policy Compliance | 30% | 30 |
| Resolution Quality | 25% | 25 |
| Communication Clarity | 15% | 15 |
| Escalation Handling | 10% | 10 |

---

## Category Breakdown

### 1. Tone and Empathy (20 points)

| Score | Criteria |
|---|---|
| 18-20 | Warm, professional, acknowledges player frustration, maintains tone throughout |
| 14-17 | Generally appropriate tone with minor lapses |
| 10-13 | Tone is neutral but lacks empathy or feels robotic |
| 5-9 | Tone is cold, dismissive, or inconsistent |
| 0-4 | Rude, argumentative, or completely inappropriate |

### 2. Accuracy and Policy Compliance (30 points)

| Score | Criteria |
|---|---|
| 27-30 | Fully accurate, no policy violations, no unauthorized promises |
| 22-26 | Minor inaccuracy that did not affect the outcome |
| 15-21 | Partial inaccuracy or unclear policy application |
| 8-14 | Significant inaccuracy or policy breach |
| 0-7 | Multiple errors or serious policy violation |

### 3. Resolution Quality (25 points)

| Score | Criteria |
|---|---|
| 23-25 | Issue fully resolved or correctly escalated with all steps followed |
| 18-22 | Issue mostly resolved with minor gaps |
| 12-17 | Partial resolution or incorrect escalation |
| 6-11 | Issue not resolved and escalation not triggered when required |
| 0-5 | No attempt to resolve or escalate |

### 4. Communication Clarity (15 points)

| Score | Criteria |
|---|---|
| 14-15 | Clear, concise, well-structured, easy to follow |
| 11-13 | Mostly clear with minor confusion |
| 7-10 | Some unclear or overly complex language |
| 3-6 | Difficult to follow or missing key information |
| 0-2 | Incomprehensible or missing response |

### 5. Escalation Handling (10 points)

| Score | Criteria |
|---|---|
| 9-10 | Escalation triggered correctly, all required info collected, player informed |
| 7-8 | Correct escalation with minor information gap |
| 4-6 | Escalation triggered but missing key information or player not informed |
| 1-3 | Incorrect escalation routing |
| 0 | Escalation required but not triggered, or unnecessary escalation |

---

## Performance Bands

| Score | Band | Action |
|---|---|---|
| 90-100 | Excellent | Positive recognition, use as benchmark example |
| 75-89 | Good | Standard performance, minor coaching |
| 60-74 | Needs Improvement | Coaching session required within 1 week |
| Below 60 | Critical | Immediate coaching, performance review |

---

## Fatal Errors

The following errors result in an automatic score of 0 regardless of other criteria:

- Agent asked player for their password
- Agent promised a refund or compensation without authorization
- Agent disclosed another player's account information
- Agent used abusive or discriminatory language
- Agent failed to escalate a security or fraud issue
