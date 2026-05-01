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

### How intent is detected

The classifier maintains a dictionary of keyword signals for each intent type:

```python
INTENT_SIGNALS = {
    Intent.PAYMENT_ISSUE: ["charged", "payment", "purchase", "didn't receive", ...],
    Intent.REFUND_REQUEST: ["refund", "money back", "want a refund", ...],
    Intent.BAN_APPEAL: ["banned", "suspended", "why was i banned", ...],
    ...
}
```

The player's message is lowercased and scanned against all signal lists simultaneously. Each match increments a score for that intent.

### How confidence is calculated

Confidence = signals matched by top intent / total signals matched across all intents.

If multiple intents score closely, confidence is dampened by 15%. This prevents a message that partially matches three intent types from being treated as high-confidence for any single one.

If no signals match at all: intent = UNKNOWN, confidence = 0.0.

### The confidence threshold

`CONFIDENCE_THRESHOLD = 0.65`

Below this: `requires_human = True`. The ticket goes to a senior agent rather than being handled autonomously. This is a deliberate conservative choice.

### How tone is detected

Separate signal lists for each tone level:

```python
TONE_SIGNALS = {
    Tone.THREATENING: ["lawyer", "lawsuit", "legal action", "sue", ...],
    Tone.ANGRY: ["unacceptable", "disgusting", "scam", "robbery", ...],
    Tone.FRUSTRATED: ["frustrated", "again", "still not", "useless", ...],
    Tone.DISTRESSED: ["please help", "desperate", "really need", ...],
}
```

Tone is checked in severity order. The first match wins.

### Flags

Flags are binary markers attached to a classification result:

| Flag | Trigger |
|---|---|
| `repeat_contact` | contact_count >= 3 |
| `second_contact` | contact_count == 2 |
| `vip_player` | is_vip == True |
| `legal_threat` | tone == THREATENING |
| `churn_risk` | intent == CHURN_RISK |
| `ban_appeal` | intent == BAN_APPEAL |
| `fraud_report` | intent == FRAUD_REPORT |

---

## Step 2: Prioritization

**File:** `engine/prioritizer.py`
**Type:** Rules-based, deterministic

Priority is assigned on a 1-5 scale using a rule table:

| Score | Label | SLA |
|---|---|---|
| 1 | Low | 72 hours |
| 2 | Standard | 24 hours |
| 3 | High | 8 hours |
| 4 | Urgent | 2 hours |
| 5 | Critical | 30 minutes |

Rules are applied additively - the score can only increase, never decrease:

- FRAUD_REPORT or CHURN_RISK intent: score >= 5
- PAYMENT_ISSUE, REFUND_REQUEST, ACCOUNT_ACCESS, BAN_APPEAL: score >= 3
- Threatening tone: score >= 5
- Angry tone: score >= 4
- Frustrated tone: score >= 3
- Repeat contact flag: score >= 4
- Second contact flag: score >= 3
- VIP player: score >= 4
- Low confidence (< 0.4): score >= 3

Priority is rules-based rather than ML-scored because rules are auditable and explainable to non-technical stakeholders.

---

## Step 3: Escalation

**File:** `engine/escalation.py`
**Type:** Rules-based, deterministic

### Hard escalation triggers (always escalate, no exceptions)

- Legal threat detected
- Intent is BAN_APPEAL or FRAUD_REPORT
- Repeat contact flag present
- VIP player flag present

### Soft escalation triggers (escalate if Tier 1 already tried)

- `prior_resolution_attempted == True` and confidence >= 0.65
- Confidence < 0.4 (extremely low signal)

### Routing table

```python
ROUTING_TABLE = {
    Intent.PAYMENT_ISSUE:    "billing",
    Intent.REFUND_REQUEST:   "billing",
    Intent.ACCOUNT_ACCESS:   "account_team",
    Intent.BAN_APPEAL:       "trust_and_safety",
    Intent.FRAUD_REPORT:     "trust_and_safety",
    Intent.BUG_REPORT:       "technical",
    Intent.TECHNICAL_ISSUE:  "technical",
    Intent.CHURN_RISK:       "player_relations",
    Intent.GAME_MECHANIC:    "tier1",
    Intent.UNKNOWN:          "senior_agent",
}
```

Overrides:
- Legal threat: always routes to `legal_compliance` regardless of intent
- VIP + payment/refund: routes to `player_relations` instead of `billing`

---

## Step 4: Response Strategy

**File:** `engine/response_router.py`
**Type:** Rules-based, deterministic

This step does not generate the player response. It generates instructions for whoever (or whatever) generates the response.

Outputs:
- **Tone instruction**: how to communicate based on player tone
- **Opening guidance**: how to start the response
- **Action**: what to do (troubleshoot steps vs escalate)
- **Collect**: which pieces of information to ask for

Example output for a payment issue with an angry player:
```
tone_instruction: "Lead with empathy. Acknowledge the frustration before any troubleshooting."
opening: "Acknowledge the frustration directly in the first sentence."
action: "Follow payment troubleshooting steps: restart app, verify transaction ID."
collect: ["Player ID", "Transaction ID", "Purchase date and amount", "Platform"]
```

---

## How tests map to intended behavior

The 30 test cases in `evaluation/test-cases.md` each target a specific behavior:

| Test range | What is tested |
|---|---|
| TC-001 to TC-010 | Straightforward cases, angry players, repeat contacts, VIP |
| TC-011 to TC-020 | GDPR, AI identity question, TOS, missing receipt, platform mismatch |
| TC-021 to TC-030 | Unclear intent, multiple identifiers, partial bug reports, legal threats, churn signals |

Every test specifies: expected classification, expected escalation, required info to collect, common failure risk, and pass criteria. Tests are not style examples - a passing assistant must produce the correct outcome on all 30.

---

## How the system decides to stop troubleshooting

The system stops Tier 1 resolution attempts and escalates when any of these is true:

1. Hard escalation trigger is present (checked before troubleshooting begins)
2. Standard Tier 1 steps have been attempted and failed (`prior_resolution_attempted = True`)
3. Confidence is too low to classify the issue type
4. The issue type is not in Tier 1 scope (escalation is the only action)

The system does not keep trying indefinitely. The interaction flow in `docs/operations/interaction-flow.md` defines the exact stopping points.

---

## How evidence is summarized for escalation

Before escalating, the pipeline compiles a handoff note containing:

1. Issue type (classification result)
2. Player-provided facts (labelled as: "player states...")
3. Steps already attempted at Tier 1
4. Reason for escalation
5. Priority level and SLA
6. Flags: VIP, repeat contact, legal threat, incident signal, contradictory info

Player claims and verified facts are kept separate. The specialist team knows what has been attempted and what has not.
