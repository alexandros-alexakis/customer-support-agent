# Limitations

A direct list of what this system cannot do, does not do, and should not be claimed to do.

---

## What is prototype-only

| Capability | Status | Notes |
|---|---|---|
| Intent classification | Prototype - keyword matching | Breaks on non-standard phrasing. Semantic matching via RAG retrieval partially compensates but does not fully replace |
| Live LLM response generation | Not wired into a live loop | System prompt and RAG context are defined. The integration call that sends them to Claude and returns a response to the player is not implemented as a running agent |
| Incident detection across sessions | Not implemented | The engine processes each ticket in isolation. Detecting that multiple players are reporting the same issue requires external aggregation |
| Persistent conversation state | Not implemented | Each ticket is stateless. Prior conversation turns must be passed in explicitly |
| Real account data access | Not implemented | The engine works on player-provided text only. It cannot verify purchases, account history, or game logs |
| Production metrics backend | Not implemented | `engine/metrics_spec.py` documents what should be measured. No live metrics system is wired up |

---

## What is mocked or local-only

| Item | Reality |
|---|---|
| Ticket data | Synthetic. `evaluation/scripts/fetch_tickets.py` generates realistic but fictional tickets |
| ChromaDB vector store | Local file storage. Not suitable for high-concurrency production workloads |
| Feedback and gap data | Local JSON files. No database, no multi-user access |
| Zendesk integration | Requires your own Zendesk account and credentials. The code is correct but untested against a live Zendesk instance in this repo |

---

## Known limitations of the classifier

- Keyword signals are English-only. Non-English phrasing scores zero on most intents
- Signals can overlap between intent types, reducing confidence in ambiguous messages
- Novel ticket types not in the signal dictionary always produce UNKNOWN intent
- A player who describes their issue without using any expected vocabulary will be mis-classified or produce UNKNOWN
- The confidence score is a proxy for classification reliability, not a probability in the statistical sense

---

## Known limitations of the system prompt

- The system prompt has not been red-teamed at production volume
- Adversarial inputs (prompt injection, policy bypass attempts) have not been systematically tested
- Non-determinism in LLM responses means identical inputs can produce different outputs across runs
- The system prompt cannot prevent all hallucination - it reduces it significantly but does not eliminate it

---

## What is not present for real-world deployment

| Missing element | Why it matters |
|---|---|
| Authentication layer on the webhook | Anyone with the URL can POST to it unless WEBHOOK_SECRET is set |
| Rate limiting | No protection against request floods |
| Persistent case tracking | No database. Ticket state exists only in the support platform |
| Human handoff workflow | No queue management, assignment, or SLA tracking system |
| Live KB synchronization | KB changes require a manual re-sync. No watch for file changes |
| Auditability log storage | Logs go to stdout only. No persistent audit trail |
| Multi-language KB | KB content is English. Responses in other languages are translated at generation time, not from translated source content |
| Incident detection at scale | Cross-session pattern detection requires an aggregation layer not present here |
| Model version pinning | Model updates from Anthropic may change response behavior without warning |

---

## Synthetic vs real-world data

All test cases and evaluation tickets are synthetic. They are realistic but:

- Real player messages are messier, shorter, more abbreviated, and more emotionally unpredictable
- Real ticket volume creates patterns (e.g. incident spikes) that synthetic data does not represent
- Performance on synthetic data is not a reliable predictor of performance on live traffic

The evaluation pipeline exists to make testing structured and repeatable, not to claim production accuracy.

---

## Prompt sensitivity

Small changes to `system-prompt.md` can produce large changes in LLM behavior. There is no automated regression test for prompt changes. Any prompt modification should be followed by:

1. Manual review against the 30 test cases in `evaluation/test-cases.md`
2. A run of the evaluation pipeline
3. Human review of a sample of outputs before deploying
