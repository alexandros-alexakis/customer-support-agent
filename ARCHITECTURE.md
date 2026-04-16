# Architecture

How the system is structured and how the components interact.

---

## What this system is

A **policy-driven, rules-based triage engine** combined with a **prompt-governed LLM response layer**, connected to a **semantic knowledge base** via RAG.

These three layers are intentionally separate:
- The triage engine makes decisions (rules, deterministic)
- The system prompt governs what the LLM says (prompt, non-deterministic)
- The knowledge base provides what the LLM knows (documents, static until synced)

---

## Component map

```
┌─────────────────────────────────────────────────────────────┐
│                      INCOMING TICKET                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   TRIAGE ENGINE (Python)                    │
│                                                             │
│  classifier.py      Intent + tone detection                 │
│                     Confidence scoring                      │
│                     Flag generation                         │
│                                                             │
│  prioritizer.py     P1-P5 priority scoring                  │
│                     SLA assignment                          │
│                                                             │
│  escalation.py      Hard/soft escalation rules              │
│                     Team routing                            │
│                                                             │
│  response_router.py Response strategy generation            │
│                                                             │
│  pipeline.py        Orchestrates all steps                  │
│                     Structured logging                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐   ┌───────────────────────────────────────┐
│   RAG LAYER     │   │           LLM LAYER (Claude)           │
│                 │   │                                        │
│  kb_sync.py     │   │  system-prompt.md  Behavior rules      │
│  Loads KB into  │   │  Retrieved KB      Injected context    │
│  ChromaDB       │   │  Response strategy From pipeline       │
│                 │   │                                        │
│  retriever.py   │   │  Output: Player-facing response        │
│  Semantic       │   │                                        │
│  search at      │   │  NOTE: LLM integration is the          │
│  query time     │   │  boundary between this prototype       │
└─────────────────┘   │  and a deployed agent. The system      │
                      │  prompt + RAG context define what      │
                      │  the LLM can and cannot do.            │
                      └───────────────────────────────────────┘
```

---

## What is rule-based vs model-based

| Component | Type | Deterministic? | File |
|---|---|---|---|
| Intent classification | Rule-based (keyword signals) | Yes | `engine/classifier.py` |
| Tone detection | Rule-based (keyword signals) | Yes | `engine/classifier.py` |
| Confidence scoring | Deterministic calculation | Yes | `engine/classifier.py` |
| Priority scoring | Rules-based decision table | Yes | `engine/prioritizer.py` |
| Escalation decision | Rules-based, hard triggers | Yes | `engine/escalation.py` |
| Team routing | Lookup table | Yes | `engine/escalation.py` |
| Response strategy | Rules-based mapping | Yes | `engine/response_router.py` |
| KB retrieval | Semantic similarity (embedding model) | Near-deterministic | `rag/retriever.py` |
| Player-facing response | LLM (Claude) | Non-deterministic | `system-prompt.md` + API call |
| Language detection | LLM (Claude) | Non-deterministic | `multilingual/language_handler.py` |

---

## What happens during a single request

### In the triage engine (implemented, runnable)

1. `TicketContext` is constructed with: message text, player ID, contact count, VIP flag
2. `classifier.py` scans for keyword signals, calculates intent scores, scores tone, generates flags
3. A confidence score is produced. Below 0.65: `requires_human = True` immediately
4. `prioritizer.py` applies rules to produce a P1-P5 score and SLA target
5. `escalation.py` checks hard triggers first (legal threat, VIP, ban appeal, repeat contact), then soft triggers (low confidence, prior resolution failed)
6. `response_router.py` maps intent + escalation decision to a response strategy (tone instruction, what to collect, what action to take)
7. All steps are logged as structured JSON events

### In the LLM layer (design complete, integration boundary)

8. Retrieved KB chunks are injected as context (via `rag/retriever.py`)
9. System prompt + context + player message + response strategy are assembled into a prompt
10. Claude generates the player-facing response
11. Language detection runs if needed (via `multilingual/language_handler.py`)

Steps 8-11 are implemented as standalone modules but are not wired into a live agent loop. The integration point is where your support platform (e.g. Zendesk) calls the pipeline and sends the generated response.

---

## File responsibilities

| File | Responsibility |
|---|---|
| `engine/classifier.py` | Converts raw message text into a structured `ClassificationResult` |
| `engine/prioritizer.py` | Converts classification into a priority score and SLA |
| `engine/escalation.py` | Decides whether to escalate, where, and why |
| `engine/response_router.py` | Produces a `ResponseStrategy` for the agent or LLM |
| `engine/pipeline.py` | Runs all four steps, logs each, returns `PipelineResult` |
| `engine/logging_config.py` | Configures structured JSON logging |
| `engine/metrics_spec.py` | Documents what should be measured in production |
| `rag/kb_sync.py` | Reads KB markdown files, chunks by section, loads into ChromaDB |
| `rag/retriever.py` | Queries ChromaDB for relevant chunks given a player message |
| `multilingual/language_handler.py` | Detects language, adapts system prompt |
| `feedback/gap_tracker.py` | Records low-confidence cases for KB review |
| `feedback/feedback_store.py` | Records QA corrections with priority |
| `integrations/zendesk_webhook.py` | Flask webhook server for Zendesk integration |
| `integrations/zendesk_client.py` | Zendesk API calls (fetch ticket, update ticket, get user) |
| `system-prompt.md` | The LLM behavior contract: scope, rules, prohibited actions |
| `knowledge-base/decision-table.md` | Operational decision logic by issue type |
| `interaction-flow.md` | Step-by-step decision flow for any ticket |
| `evaluation/test-cases.md` | 30 test scenarios covering edge cases |
| `evaluation/failure-analysis.md` | Known failure modes with causes and mitigations |
| `evaluation/scripts/` | Ticket generator, evaluator, report generator |
| `tests/` | Unit tests for classifier and prioritizer |
