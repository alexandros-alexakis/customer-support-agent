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
Incoming ticket
      |
      v
engine/classifier.py      Intent + tone detection, confidence scoring
      |
      v
engine/prioritizer.py     P1-P5 priority + SLA assignment
      |
      v
engine/escalation.py      Escalation decision + team routing
      |
      v
engine/response_router.py Response strategy generation
      |
      v
rag/retriever.py          Semantic KB search
      |
      v
llm_client.py             Claude API call (or mock)
      |
      v
Human agent reviews       Before anything reaches the player
```

---

## What is rule-based vs model-based

| Component | Type | Deterministic? |
|---|---|---|
| Intent classification | Rule-based keyword signals | Yes |
| Tone detection | Rule-based keyword signals | Yes |
| Priority scoring | Rules-based decision table | Yes |
| Escalation decision | Rules-based, hard triggers | Yes |
| KB retrieval | Semantic similarity | Near-deterministic |
| Player-facing response | LLM (Claude) | No |

---

## File responsibilities

| File | Responsibility |
|---|---|
| `engine/classifier.py` | Intent, tone, confidence, flags |
| `engine/prioritizer.py` | Priority score and SLA |
| `engine/escalation.py` | Escalation decision and routing |
| `engine/response_router.py` | Response strategy |
| `engine/pipeline.py` | Orchestrates all steps |
| `rag/kb_sync.py` | Loads KB into ChromaDB |
| `rag/retriever.py` | Semantic search at query time |
| `feedback/gap_tracker.py` | Logs low-confidence escalations |
| `feedback/feedback_store.py` | Stores agent reply pairs |
| `integrations/zendesk_webhook.py` | Zendesk webhook server |
