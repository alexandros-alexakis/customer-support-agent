# Configuration Guide

All environment variables, their purpose, whether they are required, and safe defaults.

---

## Setup

Copy the example file and edit it:
```bash
cp .env.example .env
```

Never commit `.env`. It is in `.gitignore`.

---

## Variables

### Core

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes (for LLM features) | None | Authenticates requests to the Claude API. Not required to run the triage engine alone. |

Get your key at: https://console.anthropic.com

**Security:** Never hardcode this in any Python file. Never log it. Never commit it.

---

### Zendesk Integration

Only required if running the Zendesk webhook integration.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `ZENDESK_SUBDOMAIN` | Zendesk only | None | Your Zendesk URL prefix |
| `ZENDESK_EMAIL` | Zendesk only | None | Admin email registered in Zendesk |
| `ZENDESK_API_TOKEN` | Zendesk only | None | Zendesk API token |
| `WEBHOOK_SECRET` | Zendesk only | None | HMAC signing secret for verifying webhook requests |
| `PORT` | No | `8000` | Port the Flask webhook server listens on |

---

## Model configuration

The project uses Claude (Anthropic) as the LLM provider. Model is set in `multilingual/language_handler.py`. The triage engine (`engine/`) makes no LLM calls and requires no API key.

---

## ChromaDB

Vector embeddings stored locally at `rag/chroma_store/`. Path defined in `rag/kb_sync.py`. Embedding model: `all-MiniLM-L6-v2` (~80MB, downloaded from Hugging Face on first use).

---

## Logging

Level controlled via `configure_logging(level="INFO")` in `engine/logging_config.py`. Valid levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`. All logs emit as structured JSON to stdout.
