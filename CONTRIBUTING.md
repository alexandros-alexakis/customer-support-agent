# Contributing Guide

## Overview

This repository documents the design and ongoing development of an AI-powered customer support agent for gaming operations. Contributions, suggestions, and feedback are welcome.

---

## Adapting This for Your Own Company

This project is designed to be domain-adaptable. The core engine, decision logic, and evaluation pipeline are not gaming-specific. If you work in e-commerce, fintech, SaaS, or any other support-heavy industry, you can adapt this for your own use.

### What you need to replace

| Component | What to do |
|---|---|
| `knowledge-base/` | Replace all markdown files with your own company's policies, FAQs, and escalation rules |
| `system-prompt.md` | Update tone, scope, and prohibited actions to match your company's policies |
| `engine/classifier.py` | Update `INTENT_SIGNALS` with vocabulary relevant to your domain |
| `knowledge-base/decision-table.md` | Rewrite issue types and escalation paths for your support model |
| `evaluation/scripts/fetch_tickets.py` | Replace synthetic tickets with examples from your actual ticket types |

### What you can keep as-is

- The full engine architecture (`engine/`)
- The RAG pipeline (`rag/`)
- The gap tracking and feedback loop (`feedback/`)
- The evaluation pipeline structure (`evaluation/scripts/`)
- The multilingual handler (`multilingual/`)
- The QA framework and scoring templates (`qa/`)
- `run_agent.py` and `llm_client.py`

### Steps to adapt

1. Clone the repository
2. Replace `knowledge-base/` content with your own policies
3. Update `system-prompt.md` with your company's rules
4. Update intent signals in `engine/classifier.py` for your domain vocabulary
5. Run `python rag/kb_sync.py` to load your knowledge base into the vector store
6. Run `python run_agent.py --demo` to test with example tickets
7. Update `evaluation/scripts/fetch_tickets.py` with your ticket patterns
8. Run the full evaluation pipeline to measure performance

### What you will still need to build for production

- Integration with your live support platform (Zendesk, Freshdesk, Intercom, etc.)
- Connection to your customer account data API for claim verification
- A front-end interface or chat widget
- A human review workflow for escalated tickets
- A metrics backend for live KPI tracking

The gap between a working local prototype and a live production system is real. This project gives you the decision logic, knowledge layer, and evaluation framework. Platform integration is a separate engineering project.

---

## How to Contribute to This Repo

### Reporting Issues

1. Open an Issue on GitHub
2. Describe the problem clearly
3. Suggest the correction or improvement if you have one

### Submitting Changes

1. Fork the repository
2. Create a new branch for your changes
3. Make your edits
4. Submit a pull request with a clear description of what you changed and why

---

## Content Standards

- **No real company data** - all examples must be fictional
- **No player data** - all sample conversations use fictional player names and IDs
- **Consistent format** - follow the structure of existing documents
- **Plain language** - write for clarity, not complexity
- **Practical focus** - content should be usable in a real support operation

---

## Contact

For questions or discussions, connect via [LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/).

Repository: [github.com/alexandros-alexakis/ai-customer-support-agent](https://github.com/alexandros-alexakis/ai-customer-support-agent)
