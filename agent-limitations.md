# Agent Limitations

## Overview

This document provides an honest assessment of what the AI customer support agent can and cannot do. Understanding these limitations is essential for deciding when human oversight is required.

---

## What the Agent Does Well

- Handling high-volume, repetitive Tier 1 queries consistently
- Applying escalation rules without emotional bias
- Collecting required information in a structured way
- Maintaining consistent tone across all interactions
- Responding instantly without queue delays
- Referencing the knowledge base accurately

---

## Current Limitations

### 1. No real-time data access
The agent cannot look up live player account data, transaction records, or game logs. It relies entirely on information provided by the player. All verification requires human or system-level access.

### 2. No memory between sessions
The agent does not retain context from previous conversations with the same player. Each session starts fresh. Repeat contacts must re-provide their information.

### 3. Limited judgment on edge cases
The agent applies rules as defined in the system prompt and knowledge base. Novel situations not covered by documentation require human judgment.

### 4. Tone calibration
While the agent maintains professional tone, it may occasionally miss subtle emotional cues that an experienced human agent would pick up on.

### 5. Language handling
The agent is optimized for English. Performance in other languages depends on the quality of the underlying model and may be inconsistent.

### 6. Cannot take direct action
The agent cannot issue refunds, restore items, modify accounts, or take any action in the game backend. All actions require human execution.

---

## Human Oversight Requirements

Human review is always required for:
- VIP player complaints
- Any interaction involving financial disputes above a defined threshold
- Security or fraud reports
- Legal or regulatory inquiries
- Any case where the agent flags uncertainty
- QA review sample (minimum 10% of all interactions weekly)

---

## Improvement Process

When a limitation causes a failure:
1. Document the failure case
2. Identify whether it was a knowledge base gap or a system prompt gap
3. Update the relevant document
4. Re-test against the same scenario
5. Log the update in CHANGELOG.md
