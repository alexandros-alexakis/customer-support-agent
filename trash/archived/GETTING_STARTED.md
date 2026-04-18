# Getting Started

> Archived. Moved to docs/setup/getting-started.md

This guide explains how to set up and run the project locally.

## Prerequisites

- Python 3.10 or higher
- Git
- An Anthropic API key (optional for basic triage engine use)

## What You Can Run

```bash
# Single ticket through the triage engine
python example_run.py

# Unit tests
pytest tests/

# Sync knowledge base
python rag/kb_sync.py

# Full evaluation pipeline
python evaluation/scripts/fetch_tickets.py
python evaluation/scripts/evaluate_tickets.py
python evaluation/scripts/generate_report.py

# Zendesk webhook server (local)
python integrations/zendesk_webhook.py
```
