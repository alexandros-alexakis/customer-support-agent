# Architecture

> **Moved.** This file has been superseded by [docs/guides/architecture.md](../docs/guides/architecture.md). The content below is preserved for reference.

---

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
│  prioritizer.py     P1-P5 priority scoring                  │
│  escalation.py      Hard/soft escalation rules              │
│  response_router.py Response strategy generation            │
│  pipeline.py        Orchestrates all steps                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐   ┌───────────────────────────────────────┐
│   RAG LAYER     │   │           LLM LAYER (Claude)           │
│  kb_sync.py     │   │  system-prompt.md  Behavior rules      │
│  retriever.py   │   │  Retrieved KB      Injected context    │
└─────────────────┘   └───────────────────────────────────────┘
```
