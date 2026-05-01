# How the Agent Works

An operational explanation of every decision the system makes, from input to output.

---

## Overview

The agent processes a player message through four sequential steps before any response is generated:

1. **Classify** - what is the issue, how angry is the player, how confident are we
2. **Prioritize** - how urgent is this, what is the SLA
3. **Escalate** - should a human specialist handle this, and who
4. **Route** - what should the response say and collect

Each step is independent. Each step's output is logged. Each step can be audited after the fact.

---

## Step 1: Classification

**File:** `engine/classifier.py`
**Type:** Rules-based, deterministic

The classifier scans for keyword signals across all intent types simultaneously. Confidence is calculated as signals matched by top intent / total signals matched. Below 0.65: `requires_human = True`.

Tone is checked in severity order: threatening, angry, frustrated, distressed. First match wins.

Flags are binary markers: `repeat_contact`, `vip_player`, `legal_threat`, `churn_risk`, `ban_appeal`, `fraud_report`.

---

## Step 2: Prioritization

**File:** `engine/prioritizer.py`
**Type:** Rules-based, deterministic

| Score | Label | SLA |
|---|---|---|
| 1 | Low | 72 hours |
| 2 | Standard | 24 hours |
| 3 | High | 8 hours |
| 4 | Urgent | 2 hours |
| 5 | Critical | 30 minutes |

Rules are additive. Score can only increase. VIP flag, legal threat, repeat contact, and churn risk all push toward P4 or P5.

---

## Step 3: Escalation

**File:** `engine/escalation.py`
**Type:** Rules-based, deterministic

Hard escalation triggers (always escalate, no exceptions): legal threat, ban appeal, fraud report, repeat contact, VIP player, GDPR request, account compromise.

Routing table: payment -> billing, account access -> account_team, ban appeal -> trust_and_safety, bug -> technical, churn risk -> player_relations, unknown -> senior_agent.

Overrides: legal threat always routes to legal_compliance. VIP + payment routes to player_relations instead of billing.

---

## Step 4: Response Strategy

**File:** `engine/response_router.py`
**Type:** Rules-based, deterministic

This step generates instructions for whoever drafts the response, not the response itself. Outputs: tone instruction, opening guidance, action, and list of information to collect.

---

## How evidence is compiled for escalation

Before escalating, the pipeline compiles a handoff note with: issue type, player-provided facts (labelled as player states...), steps already attempted, reason for escalation, priority level, and all active flags. Player claims and verified facts are kept separate. See [docs/operations/agent-handoff-template.md](../operations/agent-handoff-template.md).
