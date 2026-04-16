# Examples

Concrete input/output examples showing what the system actually does at each stage.

These are real outputs from the triage engine, not invented values.

---

## Example 1: Standard payment issue

### Input

```python
TicketContext(
    message="I was charged $9.99 for coins but they never appeared in my account. Transaction ID: TXN-884521",
    player_id="player_001",
    contact_count=1,
    is_vip=False,
)
```

### Classification result

```
Intent:     payment_issue
Confidence: 0.857
Tone:       neutral
Flags:      []
Requires human: True
```

### Priority result

```
Score:    3 (High)
SLA:      8.0 hours
Reason:   high-priority intent: payment_issue
```

### Escalation result

```
Should escalate: True
Team:            billing
Reason:          high-priority intent: payment_issue
Notes:           (none)
```

### Response strategy

```
Tone instruction: Professional and efficient. Get to the point without unnecessary padding.
Opening:          Standard professional greeting followed by acknowledgment of the issue.
Action:           Follow payment troubleshooting steps: restart app, verify transaction ID, check delivery.
Collect:          ['Player ID', 'Transaction ID', 'Purchase date and amount', 'Platform (iOS/Android/direct)']
```

### What the Zendesk internal note looks like

```
**AI Triage Result**
- Intent: payment_issue (confidence: 0.857)
- Tone: neutral
- Priority: High (P3) | SLA: 8.0h
- Escalate: Yes -> billing
- Reason: high-priority intent: payment_issue
- Flags: none

**Recommended action:** Follow payment troubleshooting steps: restart app, verify transaction ID, check delivery.
**Collect from player:** Player ID, Transaction ID, Purchase date and amount, Platform (iOS/Android/direct)
**Tone guidance:** Professional and efficient. Get to the point without unnecessary padding.

*Auto-generated. Review before acting. Processing time: 0.41ms*
```

---

## Example 2: Angry repeat contact with legal threat

### Input

```python
TicketContext(
    message="This is the THIRD time I've contacted you. If this isn't fixed I'm taking legal action.",
    player_id="player_002",
    contact_count=3,
    is_vip=False,
    prior_resolution_attempted=True,
)
```

### Classification result

```
Intent:     payment_issue
Confidence: 0.612
Tone:       threatening
Flags:      ['repeat_contact', 'legal_threat']
Requires human: True
```

### Priority result

```
Score:    5 (Critical)
SLA:      0.5 hours
Reason:   legal threat detected | third or more contact on same issue
```

### Escalation result

```
Should escalate: True
Team:            legal_compliance
Reason:          legal threat in message | third or more contact on unresolved issue
Notes:           Player mentioned legal action. Do not engage on legal specifics.
                 Player has contacted 3 times. Previous attempts did not resolve the issue.
```

### Response strategy

```
Tone instruction: Stay calm and professional. Do not engage with the legal threat directly.
                  Acknowledge the frustration and escalate immediately.
Opening:          Acknowledge the frustration directly in the first sentence. Do not open with a generic greeting.
Action:           Escalate to legal_compliance. Collect required information first.
                  Inform player of next steps and timeframe.
Collect:          ['Player ID', 'Transaction ID', 'Purchase date and amount', 'Platform']
```

---

## Example 3: VIP churn risk

### Input

```python
TicketContext(
    message="I'm done with this game. Uninstalling. Complete waste of money.",
    player_id="player_003",
    contact_count=1,
    is_vip=True,
)
```

### Classification result

```
Intent:     churn_risk
Confidence: 0.75
Tone:       angry
Flags:      ['vip_player', 'churn_risk']
Requires human: True
```

### Priority result

```
Score:    5 (Critical)
SLA:      0.5 hours
Reason:   critical intent: churn_risk | angry tone | VIP player
```

### Escalation result

```
Should escalate: True
Team:            player_relations
Reason:          critical intent: churn_risk | VIP player
Notes:           VIP player - prioritise response and follow up proactively after resolution.
```

---

## Example 4: Low confidence - routes to human

### Input

```python
TicketContext(
    message="Something is wrong with my account.",
    player_id="player_005",
    contact_count=1,
    is_vip=False,
)
```

### Classification result

```
Intent:     unknown
Confidence: 0.0
Tone:       neutral
Flags:      []
Requires human: True
```

### Priority result

```
Score:    2 (Standard)
SLA:      24.0 hours
Reason:   standard ticket
```

### Escalation result

```
Should escalate: True
Team:            senior_agent
Reason:          intent requires specialist: unknown
```

### Why this is correct behavior

A message with no classifiable signal goes to a human rather than receiving an automated response. The system does not guess. This is the confidence threshold working as designed.

---

## Example 5: RAG retrieval - non-standard phrasing

### Input query

```
"they took money from my account but nothing arrived"
```

### Keyword classifier result

```
Intent:     unknown
Confidence: 0.0
```

The keyword classifier finds no matches for "they took money" against its payment signals.

### RAG retrieval result

```
[0.724] faq-payments.md - Q1: A player was charged but did not receive their purchased items.
[0.681] faq-payments.md - Q2: A player's payment failed but they were charged.
[0.534] knowledge-base/refund-policy-detail.md - Refund Request Decision Tree
```

Despite zero keyword signal matches, the semantic retriever finds the correct KB content. This is why RAG complements the keyword classifier rather than replacing it entirely.

---

## Example 6: Test case mapping

How TC-004 from `evaluation/test-cases.md` maps to engine behavior:

**Test case:**
```
TC-004: Legal threat
User message: "If my account isn't restored by tomorrow I'm contacting my lawyer..."
Expected classification: ban_appeal with legal threat
Expected next action: Acknowledge professionally, escalate immediately
Should escalate: Yes - immediately
Escalation target: Legal/Compliance + Trust and Safety
```

**Actual engine output:**
```
Intent:     ban_appeal
Tone:       threatening
Flags:      ['ban_appeal', 'legal_threat']
Escalate:   True
Team:       legal_compliance  (legal_threat override applies)
Reason:     legal threat in message | intent requires specialist: ban_appeal
```

**Pass criteria met:** Assistant does not engage with legal threat. Escalates immediately to legal_compliance.
