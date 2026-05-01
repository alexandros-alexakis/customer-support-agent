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
| `ANTHROPIC_API_KEY` | Yes (for LLM features) | None | Authenticates requests to the Claude API. Required for multilingual support and any LLM-generated response. Not required to run the triage engine alone. |

Get your key at: https://console.anthropic.com

**Security:** Never hardcode this in any Python file. Never log it. Never commit it. Load it only from the environment.

---

### Zendesk Integration

Only required if you are running the Zendesk webhook integration. The triage engine runs without these.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `ZENDESK_SUBDOMAIN` | Zendesk only | None | Your Zendesk URL prefix. If your URL is `yourcompany.zendesk.com`, enter `yourcompany` |
| `ZENDESK_EMAIL` | Zendesk only | None | Admin email address registered in Zendesk |
| `ZENDESK_API_TOKEN` | Zendesk only | None | Zendesk API token. Generate in Admin Center > Apps and Integrations > APIs |
| `WEBHOOK_SECRET` | Zendesk only | None | HMAC signing secret for verifying webhook requests. Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |

**Security note on `WEBHOOK_SECRET`:** If this is not set, webhook signature verification is disabled and any HTTP client can call your endpoint. Always set this in production.

---

### Server

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `PORT` | No | `8000` | Port the Flask webhook server listens on |

---

## Model and provider configuration

The project uses **Claude** (Anthropic) as the LLM provider.

Model used: `claude-sonnet-4-20250514`

This is set directly in:
- `multilingual/language_handler.py` - for language detection and multilingual response

To change the model, edit the `model=` parameter in those files. Available models are listed at https://docs.anthropic.com

**Note:** The triage engine (`engine/`) does not make any LLM calls. It is entirely rules-based and requires no API key to run.

---

## Where the LLM integration boundary sits

The project currently uses the Anthropic API in two places:

1. `multilingual/language_handler.py` - detects language and generates multilingual responses
2. The system prompt in `system-prompt.md` defines LLM behavior but is not called by the engine directly

A full LLM integration (where Claude generates the player-facing response using the pipeline output + RAG context) would require wiring `rag/retriever.py` output and `engine/pipeline.py` output into a Claude API call. This integration point is documented but not implemented as a live loop.

---

## Logging

Logging level is controlled in code via `configure_logging(level="INFO")` in `engine/logging_config.py`.

Valid levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

All logs are emitted as structured JSON to stdout.

---

## ChromaDB configuration

ChromaDB stores vector embeddings locally at `rag/chroma_store/`. This path is defined in `rag/kb_sync.py`.

The embedding model is `all-MiniLM-L6-v2`, downloaded from Hugging Face on first use (~80MB).
