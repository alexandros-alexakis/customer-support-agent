# Gap Tracking and Feedback Loop

## Overview

Two mechanisms that close the loop between what the assistant does and what it should do.

---

## Gap Tracking

### What it is

A log of every case where the assistant could not handle a ticket confidently. When the classifier returns low confidence or RAG retrieval finds no relevant KB content, the ticket is flagged and the details recorded in `feedback/gaps.json`.

### Why it matters

Without gap tracking, KB improvement is guesswork. You do not know what questions the KB does not answer until a human QA reviewer happens to notice one. Gap tracking makes the unknown knowable: every week you can run `gap_tracker.get_gap_summary()` and see exactly which intent types and which question patterns are not covered.

### How it works

```python
from feedback.gap_tracker import record_gap, get_gaps, get_gap_summary

# Record a gap (called automatically by the pipeline)
record_gap(
    player_message="my purchase it not arrive in game",
    classification_intent="unknown",
    confidence=0.31,
    retrieval_scores=[0.28, 0.22],
    reason="low_confidence",
)

# Review gaps
gaps = get_gaps(limit=20)
summary = get_gap_summary()
```

### Weekly review process

1. Run `get_gap_summary()` to see which intents are most frequently below threshold
2. Review the actual player messages in those gaps
3. Identify patterns: is this a phrasing issue (classifier), a content issue (KB gap), or a genuinely ambiguous case?
4. If KB gap: add the content to the relevant KB file and re-sync ChromaDB
5. If classifier gap: add new signals to `engine/classifier.py`
6. If genuinely ambiguous: accept human escalation as correct behaviour

---

## Feedback Loop

### What it is

A correction mechanism. When a QA reviewer identifies that the assistant gave a wrong answer, made an incorrect escalation decision, or hallucinated policy, they record the correction in `feedback/feedback.json`.

### Why it matters

A system that cannot record its mistakes cannot improve. Without a feedback loop, the same wrong answer will be given to every player who asks the same question. Corrections are prioritised by severity so critical failures (hallucinated policy, wrong escalation) are reviewed and acted on before minor tone issues.

### How it works

```python
from feedback.feedback_store import record_feedback, get_feedback, get_feedback_summary

# Record a correction (called by QA reviewer after ticket review)
record_feedback(
    player_message="Can you tell me what section 4 of the TOS says?",
    agent_response="Section 4 states that refunds are available within 14 days...",
    issue_type="hallucinated_policy",
    priority="critical",
    correct_response="Direct the player to the TOS document link. Do not summarise TOS content.",
    reviewed_by="qa_reviewer",
    notes="Agent invented a 14-day refund window that does not exist in the KB.",
)

# Get critical issues first
critical = get_feedback(priority_filter="critical")
summary = get_feedback_summary()
```

### Feedback to action pipeline

Feedback records do not automatically update the system. They are inputs to a human review process:

| Issue Type | Action |
|---|---|
| hallucinated_policy | Add the correct policy explicitly to the KB. Tighten the system prompt prohibition. |
| wrong_escalation | Update the decision table escalation rule. Add a test case to the test suite. |
| incorrect_information | Update the relevant KB file. Re-sync ChromaDB. |
| tone_failure | Update `docs/operations/tone-guide.md`. Add to QA calibration session. |
| premature_closure | Review system prompt closure rules. |

This is intentional. Automatic prompt updates based on feedback without human review create a different class of risk. The loop is: detect -> record -> human reviews -> deliberate update.
