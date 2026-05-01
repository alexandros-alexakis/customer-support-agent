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
| **Zendesk & Helpshift integration** | Full webhook handlers |
| **Automated QA scoring** | Claude scores agent responses against a 100-point rubric |
| **Coaching report** | Turns QA scores into specific coaching plans per intent and team |
| **Training scenario generator** | Produces graded practice scenarios for onboarding and calibration |
| **Shift handover report** | End-of-shift summary of active incidents, critical flags, knowledge gaps |
| **Team performance dashboard** | QA scores, escalation accuracy, and volume aggregated by routing team |
| **Evaluation pipeline** | Synthetic ticket generation, batch evaluation, and markdown report generation |
| **Feedback loop** | Records wrong escalations, hallucinated policies, and tone failures for KB improvement |

---

## Adapting this for your own company

### What you need to replace

| Component | What to do |
|---|---|
| `knowledge-base/` | Replace markdown files with your own policies, FAQs, and escalation rules |
| `system-prompt.md` | Update tone, scope, and prohibited actions for your company |
| `engine/classifier.py` | Update `INTENT_SIGNALS` with vocabulary relevant to your domain |
| `knowledge-base/decision-table.md` | Rewrite issue types and escalation paths for your support model |
| `evaluation/scripts/fetch_tickets.py` | Replace synthetic tickets with your actual ticket patterns |
| `training/scenario_generator.py` | Replace scenario content with your own issue types and common mistakes |

### Steps to adapt

1. Clone the repository
2. Replace `knowledge-base/` content with your own policies
3. Update `system-prompt.md` with your company's rules and tone
4. Update intent signals in `engine/classifier.py` for your domain vocabulary
5. Run `python rag/kb_sync.py` to index your knowledge base
6. Run `python run_agent.py --demo` to test triage with a sample ticket
7. Wire up `integrations/zendesk_webhook.py` or `integrations/helpshift_webhook.py` to your support platform

---

## How to contribute to this repo

1. Fork the repository
2. Create a new branch for your changes
3. Make your edits
4. Submit a pull request with a clear description of what changed and why

---

## Contact

For questions or discussions, connect via [LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/) or open an issue on GitHub.
