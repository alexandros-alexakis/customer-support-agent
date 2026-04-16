# Getting Started

This guide explains how to set up and run the project locally. You do not need to be a developer to understand what each step does.

---

## Prerequisites

- Python 3.10 or higher
- An Anthropic API key (for multilingual support and future LLM integration)
- Git (to clone the repository)

To check your Python version:
```bash
python --version
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/alexandros-alexakis/customer-support-agent.git
cd customer-support-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `chromadb` - local vector database for RAG
- `sentence-transformers` - local embedding model for semantic search
- `pytest` - test runner

**3. Set your API key (required for multilingual example only)**
```bash
export ANTHROPIC_API_KEY=your_key_here
```

---

## What You Can Run

### 1. Single ticket through the triage engine

Runs four example tickets through the classifier, prioritizer, and escalation engine and prints the results.

```bash
python example_run.py
```

What you will see: intent classification, confidence score, priority level, escalation decision, and which team it routes to.

---

### 2. Unit tests

Runs the test suite for the classifier and prioritizer.

```bash
pytest tests/
```

What you will see: which tests passed, which failed, and a summary. All tests should pass on a clean install.

---

### 3. Sync the knowledge base into the vector store (RAG)

Loads all markdown files from `knowledge-base/` into ChromaDB so the retriever can perform semantic search.

```bash
python rag/kb_sync.py
```

What you will see: each file being processed, how many chunks were created, and a sync summary. This creates a `rag/chroma_store/` folder locally.

Run this once before using the RAG retriever. Re-run it any time you update the knowledge base.

---

### 4. RAG retrieval example

Demonstrates how the semantic retriever finds relevant knowledge base content for player messages, including non-standard phrasing that keyword matching would miss.

```bash
python rag/example_rag.py
```

Requires: `rag/kb_sync.py` to have been run first.

What you will see: for each example message, the top matching KB sections and their similarity scores.

---

### 5. Full evaluation pipeline

Tests the triage engine against 200 synthetic support tickets and produces an accuracy report.

Run the three scripts in order:

```bash
# Step 1: Generate 200 synthetic tickets
python evaluation/scripts/fetch_tickets.py

# Step 2: Run all tickets through the engine and compare results
python evaluation/scripts/evaluate_tickets.py

# Step 3: Generate a markdown report with statistics
python evaluation/scripts/generate_report.py
```

What you will see after step 3:
- Overall pass rate
- Intent classification accuracy
- Escalation accuracy
- False negatives (tickets that should have escalated but did not)
- False positives (tickets that escalated unnecessarily)
- Failures broken down by intent type

The report is saved to `evaluation/data/report.md`.

---

### 6. Multilingual support example

Demonstrates language detection and multilingual response generation.

```bash
python multilingual/example_multilingual.py
```

Requires: `ANTHROPIC_API_KEY` to be set.

What you will see: the same payment issue described in Spanish, French, Turkish, and Portuguese - each detected and responded to in the player's language.

---

## Folder Structure at a Glance

| Folder / File | What it is |
|---|---|
| `engine/` | Python triage engine (classifier, prioritizer, escalation, pipeline) |
| `rag/` | Semantic search layer (KB sync, retriever, vector store) |
| `feedback/` | Gap tracking and correction recording |
| `multilingual/` | Language detection and multilingual response |
| `evaluation/` | Test suite, evaluation scripts, and report generator |
| `tests/` | Unit tests for the engine |
| `knowledge-base/` | Markdown policy and FAQ documents |
| `operations/` | Operational templates (handover, reporting, incident response) |
| `qa/` | QA framework and scoring tools |
| `onboarding/` | Agent training and certification documents |
| `sample-conversations/` | Illustrative interaction examples (not test evidence) |
| `system-prompt.md` | Core assistant behavior rules |
| `interaction-flow.md` | Step-by-step decision flow |
| `evaluation-criteria.md` | How performance is measured |
| `failure-analysis.md` | Known failure modes and mitigations |

---

## Common Issues

**`ModuleNotFoundError: No module named 'chromadb'`**
Run `pip install -r requirements.txt`

**`ValueError: Collection player_care_kb does not exist`**
Run `python rag/kb_sync.py` first to populate the vector store.

**`AuthenticationError` from Anthropic**
Make sure `ANTHROPIC_API_KEY` is set in your environment.

**Slow first run of RAG or multilingual**
The `sentence-transformers` model (~80MB) downloads on first use. Subsequent runs are fast.
