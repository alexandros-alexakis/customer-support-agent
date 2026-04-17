# Getting Started

This guide explains how to set up and run the project locally. You do not need to be a developer to understand what each step does.

---

## Prerequisites

- Python 3.10 or higher
- An Anthropic API key
- Git (to clone the repository)

To check your Python version:
```bash
python --version
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/ai-customer-support-agent.git
cd ai-customer-support-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `chromadb` - local vector database for RAG
- `sentence-transformers` - local embedding model for semantic search
- `flask` - web server for the Zendesk webhook
- `gunicorn` - production server
- `python-dotenv` - loads environment variables from `.env`
- `requests` - HTTP client for Zendesk API calls
- `pytest` - test runner

**3. Set up your environment variables**

Copy the example file and fill in your values:
```bash
cp .env.example .env
```

Open `.env` and fill in:
- `ANTHROPIC_API_KEY` - from console.anthropic.com
- Zendesk credentials (only needed for the Zendesk integration)

---

## What You Can Run

### 1. Single ticket through the triage engine

Runs four example tickets through the classifier, prioritizer, and escalation engine.

```bash
python example_run.py
```

What you will see: intent classification, confidence score, priority level, escalation decision, and which team it routes to.

---

### 2. Unit tests

```bash
pytest tests/
```

All tests should pass on a clean install.

---

### 3. Sync the knowledge base into the vector store (RAG)

Loads all markdown files from `knowledge-base/` into ChromaDB for semantic search.

```bash
python rag/kb_sync.py
```

Run this once before using the RAG retriever. Re-run it any time you update knowledge base files.

---

### 4. RAG retrieval example

Shows how semantic search finds relevant KB content even when a player uses non-standard phrasing.

```bash
python rag/example_rag.py
```

Requires: `rag/kb_sync.py` to have been run first.

---

### 5. Full evaluation pipeline

Tests the triage engine against 200 synthetic tickets and produces an accuracy report.

```bash
# Step 1: Generate synthetic tickets
python evaluation/scripts/fetch_tickets.py

# Step 2: Run tickets through the engine
python evaluation/scripts/evaluate_tickets.py

# Step 3: Generate the report
python evaluation/scripts/generate_report.py
```

Report is saved to `evaluation/data/report.md`. Shows intent accuracy, escalation accuracy, false negatives, and false positives.

---

### 6. Multilingual support example

```bash
python multilingual/example_multilingual.py
```

Requires: `ANTHROPIC_API_KEY` to be set.

---

### 7. Gap tracker - see what the KB is missing

After tickets have been processed, review which questions the system could not confidently answer:

```bash
python -c "
from feedback.gap_tracker import get_gap_summary
import json
print(json.dumps(get_gap_summary(), indent=2))
"
```

---

### 8. Feedback summary - review QA corrections

```bash
python -c "
from feedback.feedback_store import get_feedback_summary
import json
print(json.dumps(get_feedback_summary(), indent=2))
"
```

---

### 9. Zendesk webhook server (local testing)

Run the webhook server locally:

```bash
python integrations/zendesk_webhook.py
```

To expose it publicly for Zendesk to reach during testing, use ngrok:

```bash
# In terminal 1
python integrations/zendesk_webhook.py

# In terminal 2
ngrok http 8000
```

Copy the `https://` URL from ngrok and use it as your Zendesk webhook endpoint.

For full Zendesk setup instructions see: `integrations/zendesk-integration-guide.md`

---

### 10. Zendesk webhook server (production)

```bash
gunicorn integrations.zendesk_webhook:app --bind 0.0.0.0:8000 --workers 2
```

---

## Folder Structure at a Glance

| Folder / File | What it is |
|---|---|
| `engine/` | Triage engine: classifier, prioritizer, escalation, pipeline |
| `rag/` | Semantic search: KB sync, retriever, ChromaDB vector store |
| `feedback/` | Gap tracking and QA correction recording |
| `multilingual/` | Language detection and multilingual response |
| `integrations/` | Zendesk webhook server and API client |
| `evaluation/` | Test suite, evaluation scripts, report generator |
| `tests/` | Unit tests |
| `knowledge-base/` | Markdown policy and FAQ documents |
| `operations/` | Operational templates |
| `qa/` | QA framework and scoring tools |
| `onboarding/` | Agent training and certification |
| `sample-conversations/` | Illustrative examples (not test evidence) |
| `system-prompt.md` | Core assistant behavior rules |
| `interaction-flow.md` | Step-by-step decision flow |
| `evaluation-criteria.md` | How performance is measured |
| `evaluation/failure-analysis.md` | Known failure modes and mitigations |
| `CONTRIBUTING.md` | How to adapt this for your own company |
| `integrations/zendesk-integration-guide.md` | Full Zendesk setup guide |

---

## Common Issues

**`ModuleNotFoundError: No module named 'chromadb'`**
Run `pip install -r requirements.txt`

**`ValueError: Collection player_care_kb does not exist`**
Run `python rag/kb_sync.py` first.

**`AuthenticationError` from Anthropic**
Make sure `ANTHROPIC_API_KEY` is set in your `.env` file.

**`ModuleNotFoundError: No module named 'dotenv'`**
Run `pip install python-dotenv`

**Slow first run of RAG or multilingual**
The `sentence-transformers` model (~80MB) downloads on first use. Subsequent runs are fast.

**Zendesk webhook returns 401**
Check that `WEBHOOK_SECRET` in your `.env` matches the signing secret in Zendesk exactly.

**Tickets not getting internal notes in Zendesk**
Check in order: (1) Is the Zendesk trigger firing? (2) Is the webhook receiving the request? Check server logs. (3) Is the API token correct and has ticket write permission?
