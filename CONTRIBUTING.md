# Contributing Guide

## Overview

This repository is a complete AI-powered customer support operations toolkit for gaming — built for anyone who wants to understand, adapt, or build on it. Contributions, suggestions, and feedback are welcome.

---

## What this project actually contains

Before adapting, it helps to know the full scope of what's here:

| Layer | What it does |
|---|---|
| **Triage engine** | Classifies intent and tone, assigns priority, makes escalation decisions — all rules-based and deterministic |
| **RAG knowledge base** | Semantic search over your policy and FAQ documents using ChromaDB |
| **LLM response generation** | Assembles full prompts and calls Claude API (or runs in mock mode for free) |
| **Multilingual support** | Detects player language, responds natively, translates KB content into 5 languages |
| **Session memory** | Persists conversation history per player across turns |
| **Player account context** | Injects account data (spend, tenure, VIP tier, device) into every prompt |
| **Incident detection** | Groups tickets by intent in rolling time windows and flags potential outages |
| **Zendesk & Helpshift integration** | Full webhook handlers — triage results written back as internal notes and tags |
| **Automated QA scoring** | Claude scores agent responses against a 100-point rubric, results saved to `qa/scores.json` |
| **Coaching report** | Turns QA scores into specific coaching plans per intent and team |
| **Training scenario generator** | Produces graded practice scenarios (Easy / Medium / Hard) for onboarding and calibration |
| **Shift handover report** | End-of-shift summary: active incidents, critical flags, knowledge gaps, recommended actions |
| **Team performance dashboard** | QA scores, escalation accuracy, and volume aggregated by routing team |
| **Evaluation pipeline** | Synthetic ticket generation, batch evaluation, and markdown report generation |
| **Feedback loop** | Records wrong escalations, hallucinated policies, and tone failures for KB improvement |

---

## Adapting this for your own company

The core architecture is not gaming-specific. If you work in e-commerce, fintech, SaaS, travel, or any support-heavy domain, the engine, evaluation pipeline, and ops tools all transfer directly.

### What you need to replace

| Component | What to do |
|---|---|
| `knowledge-base/` | Replace markdown files with your own policies, FAQs, and escalation rules |
| `system-prompt.md` | Update tone, scope, and prohibited actions for your company |
| `engine/classifier.py` | Update `INTENT_SIGNALS` with vocabulary relevant to your domain |
| `knowledge-base/decision-table.md` | Rewrite issue types and escalation paths for your support model |
| `evaluation/scripts/fetch_tickets.py` | Replace synthetic tickets with your actual ticket patterns |
| `training/scenario_generator.py` | Replace scenario content with your own issue types and common mistakes |

### What you can keep as-is

- Full engine architecture (`engine/`)
- RAG pipeline (`rag/`)
- Session memory (`memory/`)
- Player account context layer (`player/`) — swap mock data for your own backend
- Incident detection (`feedback/incident_detector.py`)
- Multilingual handler (`multilingual/`) and KB translator (`rag/kb_translator.py`)
- Automated QA scoring (`qa/auto_scorer.py`) — rubric is editable in `qa/qa-framework.md`
- Coaching report generator (`qa/coaching_report.py`)
- Shift handover report (`operations/handover_report.py`)
- Team performance dashboard (`operations/team_performance_dashboard.py`)
- Evaluation pipeline (`evaluation/scripts/`)
- Zendesk and Helpshift webhook handlers (`integrations/`)
- `run_agent.py` and `llm_client.py`

### Steps to adapt

1. Clone the repository
2. Replace `knowledge-base/` content with your own policies
3. Update `system-prompt.md` with your company's rules and tone
4. Update intent signals in `engine/classifier.py` for your domain vocabulary
5. Run `python rag/kb_sync.py` to index your knowledge base
6. Run `python run_agent.py --demo` to test triage with a sample ticket
7. Run `python training/scenario_generator.py` to generate practice scenarios from your ticket patterns
8. Update `evaluation/scripts/fetch_tickets.py` with your ticket types and run the full evaluation pipeline
9. Wire up `integrations/zendesk_webhook.py` or `integrations/helpshift_webhook.py` to your support platform
10. Run `python operations/team_performance_dashboard.py` to see your first performance report

### What you will still need to build for production

- Connection to your customer account data API (the `player/account_provider.py` mock is the integration point)
- A metrics backend for live KPI tracking
- A human review workflow for escalated tickets
- Red-teaming and load testing of the system prompt at production volume

---

## How to contribute to this repo

### Reporting issues

1. Open an issue on GitHub
2. Describe the problem clearly
3. Suggest the correction or improvement if you have one

### Submitting changes

1. Fork the repository
2. Create a new branch for your changes
3. Make your edits
4. Submit a pull request with a clear description of what changed and why

---

## Content standards

- **No real company data** — all examples must be fictional
- **No player data** — all sample conversations use fictional player names and IDs
- **Consistent format** — follow the structure of existing documents
- **Plain language** — write for clarity, not complexity
- **Practical focus** — content should be usable in a real support operation

---

## Contact

For questions or discussions, connect via [LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/) or open an issue on GitHub.
