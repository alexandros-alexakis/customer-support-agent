# Troubleshooting

Symptom, likely cause, and resolution for every common failure.

---

## Installation

### `Could not find a version that satisfies the requirement chromadb`
Python version too old. ChromaDB requires Python 3.10+.
```bash
python --version
```

### `Failed building wheel for sentence-transformers`
**macOS Apple Silicon:**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```
**Linux:**
```bash
sudo apt-get install python3-dev build-essential
pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'X'`
Virtual environment not activated.
```bash
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Runtime

### `ValueError: Collection player_care_kb does not exist`
KB not synced yet.
```bash
python rag/kb_sync.py
```

### `AuthenticationError: invalid x-api-key`
```bash
echo $ANTHROPIC_API_KEY
cat .env | grep ANTHROPIC
```

### Tests fail with `ModuleNotFoundError`
Run pytest from the project root directory.
```bash
cd /path/to/ai-customer-support-agent
pytest tests/ -v
```

### Tests fail with unexpected intent classification
Run the specific test with `-v`, check `engine/classifier.py` for overlapping signals.

---

## Zendesk

### Webhook returns `401 Unauthorized`
`WEBHOOK_SECRET` in `.env` does not match the signing secret in Zendesk. Go to Admin Center > Apps and Integrations > Webhooks, copy the signing secret, paste into `.env`, restart the server.

### Tickets not getting internal notes
1. Check the Zendesk trigger is firing (Admin Center > Objects and rules > Triggers)
2. Check server logs for `webhook_received` events
3. Check for `zendesk_update_failed` or `403` — a 403 means your token lacks write permission

### `ConnectionRefusedError` on webhook server
Port 8000 already in use.
```bash
lsof -i :8000
PORT=8001 python integrations/zendesk_webhook.py
```

---

## RAG

### Empty retrieval results
1. Run `python rag/kb_sync.py`
2. Try a more specific query (minimum similarity threshold: 0.4)
3. Delete and re-sync: `rm -rf rag/chroma_store/ && python rag/kb_sync.py`

### Slow first run
Normal. `sentence-transformers` model (~80MB) downloading on first use.

---

## Classification

### Wrong intent category
Check signals in `engine/classifier.py`. Add missing phrasing to `INTENT_SIGNALS`. Re-run tests.

### Confidence is 0.0
No keyword signals matched. Intent = UNKNOWN. This is correct — routes to human instead of guessing. If frequent, review the gap tracker:
```bash
python -c "from feedback.gap_tracker import get_gap_summary; import json; print(json.dumps(get_gap_summary(), indent=2))"
```
