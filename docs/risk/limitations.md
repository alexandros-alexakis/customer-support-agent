# Limitations

A direct list of what this system cannot do, does not do, and should not be claimed to do.

---

## What is prototype-only

| Capability | Status | Notes |
|---|---|---|
| Intent classification | Prototype, keyword matching | Breaks on non-standard phrasing. RAG partially compensates. |
| Live LLM response loop | Not wired into a live loop | System prompt and RAG are defined. The running agent loop is not implemented. |
| Incident detection | Not implemented | Each ticket is processed in isolation. Cross-session pattern detection requires an aggregation layer. |
| Persistent conversation state | Not implemented | Each ticket is stateless. Prior turns must be passed in explicitly. |
| Real account data access | Not implemented | Works on player-provided text only. Cannot verify purchases or game logs. |
| Production metrics backend | Not implemented | `engine/metrics_spec.py` documents what to measure. No live metrics system. |

---

## What is mocked or local-only

| Item | Reality |
|---|---|
| Ticket data | Synthetic. Realistic but fictional. |
| ChromaDB vector store | Local file storage. Not suitable for high-concurrency production. |
| Feedback and gap data | Local JSON files. No database, no multi-user access. |
| Zendesk integration | Requires your own Zendesk account. Untested against a live instance in this repo. |

---

## Known classifier limitations

- Keyword signals are English-only. Non-English phrasing scores zero on most intents.
- Signals can overlap between intent types, reducing confidence on ambiguous messages.
- Novel ticket types not in the signal dictionary always produce UNKNOWN intent.
- Confidence score is a proxy for reliability, not a statistical probability.

---

## Known system prompt limitations

- Not red-teamed at production volume.
- Adversarial inputs have not been systematically tested.
- LLM non-determinism means identical inputs can produce different outputs.
- Does not eliminate hallucination, reduces it significantly.

---

## What is missing for real-world deployment

| Missing | Why it matters |
|---|---|
| Webhook authentication | Anyone with the URL can POST to it unless WEBHOOK_SECRET is set |
| Rate limiting | No protection against request floods |
| Persistent case tracking | No database. State exists only in the support platform. |
| Human handoff workflow | No queue management or SLA tracking |
| Live KB synchronization | KB changes require manual re-sync |
| Audit log storage | Logs go to stdout only |
| Multi-language KB | KB is English. Responses in other languages are translated at generation time. |
| Incident detection at scale | Requires an aggregation layer not present here |

---

## Synthetic vs real-world data

All test cases are synthetic. Real player messages are messier, shorter, more emotionally unpredictable. Performance on synthetic data is not a reliable predictor of performance on live traffic.
