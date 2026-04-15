# AI CSAT Bias Analysis

## Overview

This document addresses a known measurement problem in AI-assisted customer support: when AI handles simple tickets and human agents handle complex ones, comparing their CSAT scores produces a misleading picture that favours AI and unfairly penalises agents.

This is not a theoretical concern. It is an observable pattern in operations that have deployed AI without controlling for ticket complexity in their measurement framework.

---

## The Problem

### How it happens

AI agents are typically deployed to handle Tier 1 scope: straightforward, repetitive queries with clear resolutions. Players asking basic questions receive fast, consistent answers and rate the interaction positively.

Human agents, by contrast, increasingly handle what is left: escalations, billing disputes, ban appeals, frustrated repeat contacts, complex technical issues. These interactions are inherently harder to resolve satisfactorily regardless of agent quality.

The result is a CSAT comparison that looks like this:

| Handler | Ticket Type | Average CSAT |
|---|---|---|
| AI agent | Simple, fast-resolution queries | High |
| Human agents | Complex, emotionally charged, unresolved issues | Low |

This comparison tells you nothing useful about the performance of either the AI or the human agents. It tells you that easy tickets get better ratings than hard ones - which was always true.

---

## Why This Matters

Organisations making resourcing decisions based on this data will:

- Overestimate AI capability and expand AI scope prematurely
- Underestimate human agent performance and make incorrect staffing or training decisions
- Potentially reduce human headcount based on flawed benchmarks
- Damage player experience when AI is given tickets it cannot handle well
- Erode agent morale when their scores reflect ticket difficulty rather than their actual performance

---

## The Root Cause

The measurement framework is not controlling for the variable that matters most: **ticket complexity**.

A fair comparison requires that AI and human agents are evaluated on equivalent ticket types. Without this control, the comparison is structurally biased from the start.

---

## Proposed Solution: Complexity-Controlled Measurement

### Step 1: Define a ticket complexity score

Score each ticket at the point of routing based on objective criteria:

| Factor | Low Complexity (1) | Medium Complexity (2) | High Complexity (3) |
|---|---|---|---|
| Resolution type | Standard FAQ answer | Requires investigation | Requires specialist action |
| Emotional intensity | Neutral | Frustrated | Angry or distressed |
| Contact history | First contact | Second contact | Three or more contacts |
| Financial impact | None | Minor | Significant |
| Policy sensitivity | Standard | Gray area | Exception required |

Total score range: 5 (simplest) to 15 (most complex)

---

### Step 2: Segment CSAT by complexity band

Rather than one aggregate CSAT figure, report CSAT within complexity bands:

| Complexity Band | Score Range | Description |
|---|---|---|
| Simple | 5-7 | Standard queries, clear resolution available |
| Moderate | 8-11 | Requires investigation or judgment |
| Complex | 12-15 | High sensitivity, specialist involvement likely |

---

### Step 3: Compare like-for-like

Only compare AI and human CSAT scores within the same complexity band.

| Complexity Band | AI CSAT | Human CSAT | Valid Comparison |
|---|---|---|---|
| Simple | Measurable | Measurable | Yes |
| Moderate | Measurable (if in scope) | Measurable | Yes |
| Complex | Not applicable | Measurable | No comparison |

This immediately reveals whether AI is actually performing well on simple tickets, or whether its high CSAT is simply a function of ticket selection.

---

### Step 4: Report separately, not in aggregate

Stop reporting a single CSAT figure that combines AI and human interactions. Report:

- AI CSAT for tickets within AI scope
- Human CSAT by complexity band
- Overall CSAT as a blended metric with clear methodology notes

---

## What Good Measurement Looks Like

A well-designed measurement framework produces honest answers to these questions:

- Is the AI actually resolving simple tickets well, or just fast?
- Are human agents performing well on the complex tickets they are given?
- Is the AI being given tickets that are too complex for its current capabilities?
- Where is the complexity threshold at which AI performance drops?

---

## Implications for This Project

The customer support agent documented in this repository is scoped to Tier 1 tickets deliberately. Before expanding that scope:

1. Establish a complexity baseline for current Tier 1 tickets
2. Measure CSAT within that complexity band only
3. Compare against human agent CSAT on equivalent tickets
4. Only expand AI scope if performance holds at the next complexity level

Expanding AI scope based on inflated simple-ticket CSAT is a measurement error, not a performance signal.

---

## Further Reading

This problem is related to broader issues in performance measurement:

- Simpson's Paradox: aggregate statistics that reverse when data is segmented
- Selection bias in AI evaluation benchmarks
- Goodhart's Law: when a measure becomes a target, it ceases to be a good measure
