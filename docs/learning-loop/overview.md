# Learning Loop: Escalate Instead of Hallucinate, Learn from Agent Replies

Two connected behaviours that together form the learning loop: how the system handles unknown questions, and how it builds toward answering them over time.

---

## The problem this solves

AI systems in support fail in two main ways. Overconfidence: the system gives a fluent, plausible-sounding answer to a question it has no business answering. Stagnation: the system keeps escalating the same questions indefinitely because nobody captures the answers.

The learning loop addresses both.

---

## Part 1: Escalate instead of hallucinate

Before generating any response, the system runs two checks:

1. **Classification confidence.** If intent cannot be classified above 0.65, ticket is flagged `requires_human` immediately.
2. **KB retrieval confidence.** If the top KB retrieval result falls below the similarity threshold (hardcoded at 0.4 in `rag/retriever.py`), the system escalates rather than generating a response from general knowledge.

If the system does not know the answer, it says so and passes the ticket to a human. It does not guess.

In gaming support, a hallucinated answer is often worse than no answer. The cost of over-escalating is low. The cost of hallucinating is high: false expectations, an agent who has to fix what the AI broke, and a CSAT hit.

Both thresholds are hardcoded in the current prototype. Calibrate these values against real tickets before going live.

---

## Part 2: Learn from agent replies

When the system escalates because it did not know the answer, the agent who resolves it does know. The learning loop captures it.

The cycle:

1. Player asks something the KB does not cover.
2. System escalates, logs the gap to `feedback/gap_tracker.py`.
3. Agent resolves the ticket. Their reply is captured alongside the original question.
4. The pair enters a pending KB candidates pool in `feedback/feedback_store.py`.
5. If the same pattern appears multiple times with consistent resolutions, confidence builds.
6. Once the pattern crosses the promotion threshold, it is surfaced as a suggested KB update.
7. A human approves or rejects it. Approved entries are added to the KB.
8. On the next KB sync, the system can answer that question directly.

**This is not automatic KB updating.** Every candidate goes through human review before anything is added. One agent reply might be inconsistent with policy. The approval step is where quality control happens.

Default promotion threshold: 3 consistent resolutions before surfacing for review. This is hardcoded in `feedback/incident_detector.py` in the current prototype.

---

## What the feedback files do

| File | Role |
|---|---|
| `feedback/gap_tracker.py` | Logs escalations caused by low confidence or KB miss |
| `feedback/feedback_store.py` | Stores agent reply pairs, tracks pattern frequency, surfaces candidates |

See [kb-maintenance.md](kb-maintenance.md) for the KB review process.
