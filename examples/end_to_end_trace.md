# End-to-End Execution Trace

This document shows exactly what happens when a player message enters the system.
Every step is shown. Nothing is skipped.

---

## Input

```
Message:       "I bought gems but they never showed up in my account."
Contact count: 1
VIP:           False
```

Command used:
```bash
python run_agent.py --demo
```

---

## Step 1: Input received

The message is passed to `engine/pipeline.py` as a `TicketContext`:

```python
TicketContext(
    message="I bought gems but they never showed up in my account.",
    player_id="interactive_session",
    contact_count=1,
    is_vip=False,
)
```

---

## Step 2: Classification

**File:** `engine/classifier.py`
**Type:** Rules-based keyword matching. Deterministic. No LLM.

The message is lowercased and scanned against all intent signal lists.

Signals matched:
- `"bought"` → payment_issue signal
- `"never showed up"` → payment_issue signal ("not received" variant)

No other intent signals matched.

```
intent_scores = {
    payment_issue: 2,
    refund_request: 0,
    account_access: 0,
    ban_appeal: 0,
    ...
}
```

Confidence = 2 / 2 = 1.0 (all matched signals belong to one intent)

```
Intent:      payment_issue
Confidence:  1.0
Tone:        neutral     (no anger/frustration/threat signals found)
Flags:       []          (contact_count=1, not VIP, no legal language)
Requires human: True     (payment_issue always requires specialist review)
```

---

## Step 3: Immediate escalation check

**File:** `engine/escalation.py`
**Type:** Rules-based hard triggers. Deterministic.

Checked in order:
- Legal threat? No
- Ban appeal? No
- Fraud report? No
- Repeat contact (3+)? No (contact_count=1)
- VIP player? No
- GDPR request? No

No hard triggers fired.

Soft trigger check:
- `prior_resolution_attempted`? No (default False)
- Confidence < 0.4? No (confidence=1.0)

Result: **Escalate = True** because payment_issue is in `high_priority_intents` and `prior_resolution_attempted=False` means Tier 1 steps should be attempted first.

Actual decision:
```
Should escalate: True   (after Tier 1 steps - not immediate)
Team:            billing
Reason:          high-priority intent: payment_issue
```

---

## Step 4: Priority scoring

**File:** `engine/prioritizer.py`
**Type:** Rules-based scoring table. Deterministic.

Rules applied:
- payment_issue in high_priority_intents → score >= 3
- Tone = neutral → no escalation
- No VIP flag → no escalation
- No repeat contact → no escalation

```
Score:   3 (High)
Label:   High
SLA:     8.0 hours
Reason:  high-priority intent: payment_issue
```

---

## Step 5: Response strategy

**File:** `engine/response_router.py`
**Type:** Rules-based mapping. Deterministic.

```
Tone instruction: Professional and efficient. Get to the point without unnecessary padding.
Opening:          Standard professional greeting followed by acknowledgment of the issue.
Action:           Follow payment troubleshooting steps: restart app, verify transaction ID, check delivery.
Collect:          ['Player ID', 'Transaction ID', 'Purchase date and amount', 'Platform (iOS/Android/direct)']
```

---

## Step 6: RAG retrieval (optional)

**File:** `rag/retriever.py`
**Type:** Semantic similarity search. Near-deterministic.

If the KB has been synced (`python rag/kb_sync.py`), the message is embedded and the most similar KB sections are retrieved:

```
[0.847] faq-payments.md - Q1: A player was charged but did not receive their purchased items.
[0.731] faq-payments.md - Q2: A player's payment failed but they were charged.
```

If KB is not synced, this step is skipped and the LLM responds from the system prompt alone.

---

## Step 7: Prompt assembly

The full prompt sent to the LLM is assembled from four parts:

```
[PART 1 - SYSTEM PROMPT]
You are a Tier 1 customer support assistant for a mobile and PC strategy game.
You operate under strict rules...
[full system-prompt.md content]

[PART 2 - KNOWLEDGE BASE CONTEXT (if available)]
RELEVANT KNOWLEDGE BASE CONTENT:
[Source 1: faq-payments.md - Q1: A player was charged but did not receive...]
...content of the matching KB section...

[PART 3 - RESPONSE GUIDANCE]
Tone: Professional and efficient. Get to the point without unnecessary padding.
Action: Follow payment troubleshooting steps: restart app, verify transaction ID, check delivery.

[PART 4 - PLAYER MESSAGE]
I bought gems but they never showed up in my account.
```

This is what Claude receives. The rules (Part 1) constrain behavior. The KB context (Part 2) grounds the response in actual policy. The strategy (Part 3) tells the LLM what to do. The message (Part 4) is what the player said.

---

## Step 8: LLM response

### Mock mode (no API key)

```
[MOCK MODE - deterministic pre-written response]

Thank you for reaching out. I'm sorry to hear your purchase didn't arrive.
Could you please share your Player ID and the transaction ID from your receipt?
Once I have those, I'll look into this right away.
```

### LLM mode (Anthropic Claude API)

Actual Claude response (non-deterministic, may vary):

```
Hi, thank you for contacting us. I'm sorry to hear your gems didn't arrive after your purchase -
that's frustrating and I want to help get this sorted.

Could you please provide:
1. Your Player ID or in-game username
2. The transaction ID from your purchase receipt
3. The date and approximate time of the purchase
4. Which platform you purchased on (iOS, Android, or directly through the game)

Once I have these details, I'll be able to look into what happened with your order.
```

---

## Full output (what you see in the terminal)

```
============================================================
 PLAYER CARE AI - EXECUTION TRACE
============================================================

Run mode:            MOCK MODE (no API key - deterministic output, no cost)
RAG context:         Available

------------------------------------------------------------
 STEP 1: INPUT
------------------------------------------------------------
Message:       I bought gems but they never showed up in my account.
Contact count: 1
VIP player:    False

------------------------------------------------------------
 STEP 2: CLASSIFICATION (rules-based, deterministic)
------------------------------------------------------------
Intent:        payment_issue
Confidence:    1.0
Tone:          neutral
Flags:         none
Requires human:True

------------------------------------------------------------
 STEP 3: PRIORITY (rules-based, deterministic)
------------------------------------------------------------
Score:         P3 - High
SLA:           8.0 hours
Reason:        high-priority intent: payment_issue

------------------------------------------------------------
 STEP 4: ESCALATION DECISION (rules-based, deterministic)
------------------------------------------------------------
Escalate:      True
Route to:      billing
Reason:        high-priority intent: payment_issue

------------------------------------------------------------
 STEP 5: RESPONSE STRATEGY (rules-based, deterministic)
------------------------------------------------------------
Tone guidance: Professional and efficient.
Opening:       Standard professional greeting followed by acknowledgment.
Action:        Follow payment troubleshooting steps: restart app, verify transaction ID.
Collect:       Player ID, Transaction ID, Purchase date and amount, Platform

------------------------------------------------------------
 STEP 6: PROMPT (assembled from system prompt + strategy + message)
------------------------------------------------------------
[prompt displayed here]

------------------------------------------------------------
 STEP 7: LLM RESPONSE [MOCK]
------------------------------------------------------------
NOTE: Mock mode active. This is a deterministic pre-written response.
      Set ANTHROPIC_API_KEY in .env to get real Claude responses.

Thank you for reaching out. I'm sorry to hear your purchase didn't arrive.
Could you please share your Player ID and the transaction ID from your receipt?
Once I have those, I'll look into this right away.

============================================================
 TRACE COMPLETE
============================================================
Processing time: 0.28ms (triage engine only, excludes LLM)
```

---

## What is code vs prompt vs assumption

| Step | Implemented in | Deterministic? |
|---|---|---|
| Intent classification | Python code (`classifier.py`) | Yes |
| Tone detection | Python code (`classifier.py`) | Yes |
| Confidence scoring | Python code (`classifier.py`) | Yes |
| Flag generation | Python code (`classifier.py`) | Yes |
| Priority scoring | Python code (`prioritizer.py`) | Yes |
| Escalation decision | Python code (`escalation.py`) | Yes |
| Team routing | Python code (`escalation.py`) | Yes |
| Response strategy | Python code (`response_router.py`) | Yes |
| KB retrieval | Embedding similarity (`retriever.py`) | Near-deterministic |
| Player-facing response | LLM via `llm_client.py` | No (non-deterministic) |

Everything above the LLM call is fully deterministic and auditable.
The LLM is constrained by the system prompt but its exact output varies.
