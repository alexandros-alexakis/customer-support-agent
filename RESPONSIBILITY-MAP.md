# Responsibility Map

When something goes wrong or needs changing, this table tells you exactly which file to open.

---

## Behavior to file mapping

| Observed behavior | Root cause | File to change | Extra step |
|---|---|---|---|
| Agent misclassifies an intent | Missing or weak keyword signals | `engine/classifier.py` - update `INTENT_SIGNALS` | Run `pytest tests/` after |
| Agent escalates when it should not | Over-broad escalation rule | `engine/escalation.py` - review hard/soft triggers | Add a test case to `evaluation/test-cases.md` |
| Agent fails to escalate when it should | Missing escalation trigger | `engine/escalation.py` - add hard trigger | Add a test case to `evaluation/test-cases.md` |
| Agent routes to the wrong team | Incorrect routing table entry | `engine/escalation.py` - update `ROUTING_TABLE` | Re-run evaluation pipeline |
| Agent gives wrong information to player | KB content is missing or incorrect | Relevant file in `knowledge-base/` | Re-run `python rag/kb_sync.py` |
| Agent makes an unauthorized promise | System prompt prohibition missing | `system-prompt.md` - add to PROHIBITED ACTIONS | Review all 30 test cases manually |
| Agent uses the wrong tone | Tone rules too loose | `system-prompt.md` - tighten tone section | Check `docs/operations/tone-guide.md` for consistency |
| Priority score seems wrong | Priority rule missing or miscalibrated | `engine/prioritizer.py` - update priority rules | Run `tests/test_prioritizer.py` |
| Mock response is unhelpful or wrong | Mock dictionary entry | `llm_client.py` - update `MOCK_RESPONSES` for that intent | Run `python run_agent.py --demo` to verify |
| RAG retrieves irrelevant content | KB section is poorly written or misplaced | Relevant file in `knowledge-base/` | Re-run `python rag/kb_sync.py` and test with `python rag/example_rag.py` |
| RAG returns nothing | KB not synced | Run `python rag/kb_sync.py` | - |
| Confidence score is always low | Signals too sparse or overlapping | `engine/classifier.py` - review `INTENT_SIGNALS` | Check gap tracker: `make gaps` |
| New issue type not handled | Intent not defined | `engine/classifier.py`, `engine/escalation.py`, `engine/response_router.py` | Follow `EXTENDING.md` step by step |
| Feedback not being recorded | Gap tracker or feedback store not called | `feedback/gap_tracker.py` or `feedback/feedback_store.py` | Check `feedback/gaps.json` exists |
| Zendesk ticket not getting internal note | Webhook, trigger, or API token issue | `integrations/zendesk_webhook.py` | Follow troubleshooting in `integrations/zendesk-integration-guide.md` |

---

## What each layer owns

| Layer | What it controls | What it does not control |
|---|---|---|
| `engine/classifier.py` | Intent type, tone, confidence, flags | What the agent says |
| `engine/prioritizer.py` | Priority score, SLA | Who handles the ticket |
| `engine/escalation.py` | Whether to escalate, which team | Response content |
| `engine/response_router.py` | Tone guidance, what to collect, action | Actual response wording |
| `system-prompt.md` | LLM behavior, prohibitions, scope | Triage decisions (those are in the engine) |
| `knowledge-base/` | What the agent knows | How the agent decides |
| `llm_client.py` | Mock responses, API call | Classification or escalation logic |
| `rag/retriever.py` | Which KB sections are retrieved | What the LLM does with them |

---

## Decision ownership: code vs prompt vs KB

| Decision | Made by |
|---|---|
| Is this a payment issue? | Code (`classifier.py`) |
| How urgent is it? | Code (`prioritizer.py`) |
| Should it escalate? | Code (`escalation.py`) |
| Which team gets it? | Code (`escalation.py`) |
| What tone should the response use? | Code (`response_router.py`) informs → LLM executes |
| What should the response say? | LLM, constrained by `system-prompt.md` |
| What policy does the response reference? | KB content retrieved by RAG |
| Can the agent promise a refund? | `system-prompt.md` (prohibited) |
