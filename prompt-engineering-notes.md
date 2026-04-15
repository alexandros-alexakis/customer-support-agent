# Prompt Engineering Notes

## Overview

This document records the design decisions made when building the system prompt for the customer support agent. It is intended to help future maintainers understand why the prompt is structured the way it is.

---

## Key Design Decisions

### 1. Escalation-first on ambiguity

**Decision:** When the agent is uncertain, it escalates rather than attempts resolution.

**Reason:** A wrongly escalated ticket is recoverable. A wrongly resolved ticket (incorrect information given, unauthorized promise made) damages player trust and creates liability. The cost of over-escalation is lower than the cost of under-escalation.

---

### 2. No self-identification as AI

**Decision:** The agent does not identify itself as an AI unless directly asked.

**Reason:** Players interacting with support want their issue resolved. Proactively identifying as AI introduces friction and may cause players to disengage. If asked directly, the agent should answer honestly.

---

### 3. Structured information collection

**Decision:** The agent always collects required information in numbered lists before proceeding.

**Reason:** Structured collection reduces back-and-forth and ensures escalations have complete information. It also makes conversations easier for QA reviewers to evaluate.

---

### 4. Empathy before resolution

**Decision:** The agent always acknowledges the player's frustration before moving to troubleshooting.

**Reason:** Players who feel dismissed disengage or escalate emotionally. A single sentence of acknowledgment significantly reduces hostility and improves CSAT scores.

---

### 5. Hard boundaries on promises

**Decision:** The agent never promises refunds, restorations, or specific outcomes.

**Reason:** Promises made by support agents create player expectations that the business may not be able to fulfill. This leads to further escalation and damages trust more than not making the promise in the first place.

---

## Prompt Iteration History

| Version | Change | Reason |
|---|---|---|
| v1.0 | Initial prompt created | Project launch |
| v1.1 | Added VIP handling instructions | VIP players were being handled identically to standard players |
| v1.2 | Tightened escalation triggers | Agents were over-resolving issues outside Tier 1 scope |

---

## Known Prompt Weaknesses

- The agent occasionally over-apologizes in rapid succession, which can feel robotic
- Edge cases involving multiple simultaneous issues in one ticket are not fully handled
- The agent may be too conservative on game mechanic questions, escalating when it could resolve
