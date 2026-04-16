# Troubleshooting

Symptom, likely cause, and resolution for every common failure.

---

## Installation failures

### `ERROR: Could not find a version that satisfies the requirement chromadb`

**Likely cause:** Python version too old. ChromaDB requires Python 3.10+.

**Resolution:**
```bash
python --version
# Must be 3.10 or higher
# If not, install Python 3.10+ and recreate the venv
```

---

### `ERROR: Failed building wheel for sentence-transformers`

**Likely cause:** Missing build tools or incompatible torch version.

**Resolution (macOS Apple Silicon):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**Resolution (Linux):**
```bash
sudo apt-get install python3-dev build-essential
pip install -r requirements.txt
```

---

### `ModuleNotFoundError: No module named 'X'`

**Likely cause:** Virtual environment not activated, or requirements not installed.

**Resolution:**
```bash
# Activate venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

# Reinstall requirements
pip install -r requirements.txt
```

---

## Runtime failures

### `ValueError: Collection player_care_kb does not exist`

**Likely cause:** `rag/kb_sync.py` has not been run. ChromaDB has no data.

**Resolution:**
```bash
python rag/kb_sync.py
```

---

### `AuthenticationError: invalid x-api-key`

**Likely cause:** `ANTHROPIC_API_KEY` is not set or is incorrect.

**Resolution:**
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set it
export ANTHROPIC_API_KEY=your_key_here

# Or ensure .env is correct and load it
cat .env | grep ANTHROPIC
```

---

### `example_run.py` produces no output or crashes

**Likely cause:** Import error in engine module.

**Resolution:**
```bash
# Run with full traceback
python -v example_run.py

# Check you are in the project root
pwd
ls engine/
```

---

### Tests fail with `ModuleNotFoundError`

**Likely cause:** pytest is not finding the project root. Run pytest from the project root directory.

**Resolution:**
```bash
# Ensure you are in the project root
cd /path/to/customer-support-agent
pytest tests/ -v
```

---

### Tests fail with unexpected intent classification

**Likely cause:** Signal dictionary was modified and some signals now overlap more than expected.

**Resolution:**
1. Run the specific failing test with `-v` to see the actual vs expected output
2. Check `engine/classifier.py` for any recently added signals that might conflict
3. Run `python example_run.py` to see how real messages are classified

---

## Zendesk webhook issues

### Webhook returns `401 Unauthorized`

**Likely cause:** `WEBHOOK_SECRET` in `.env` does not match the signing secret in Zendesk.

**Resolution:**
1. Go to Zendesk Admin Center > Apps and Integrations > Webhooks
2. Open your webhook and check the signing secret
3. Copy it exactly into your `.env` as `WEBHOOK_SECRET`
4. Restart the webhook server

---

### Tickets are not getting internal notes

**Check in this order:**

1. Is the Zendesk trigger firing?
   - Admin Center > Objects and rules > Triggers
   - Click your trigger > check execution log

2. Is the webhook receiving the request?
   - Check server logs for `webhook_received` events
   - If nothing is logged, the trigger is not firing or the URL is wrong

3. Is the Zendesk API update succeeding?
   - Check logs for `zendesk_update_failed` or `403` errors
   - A 403 means your API token does not have write permission
   - Regenerate the token with full ticket access

---

### `ConnectionRefusedError` when running webhook server

**Likely cause:** Port 8000 is already in use.

**Resolution:**
```bash
# Find what is using port 8000
lsof -i :8000

# Change the port
PORT=8001 python integrations/zendesk_webhook.py
```

---

## RAG issues

### RAG retrieval returns empty results

**Likely causes and resolutions:**

1. KB not synced: `python rag/kb_sync.py`
2. Query has no semantic match above the minimum threshold (0.4): try a more specific query
3. ChromaDB store is corrupted: delete `rag/chroma_store/` and re-sync

```bash
rm -rf rag/chroma_store/
python rag/kb_sync.py
```

---

### Slow first run of RAG or multilingual

**Cause:** `sentence-transformers` model (~80MB) downloading on first use. This is normal.

**Resolution:** Wait for the download to complete. Subsequent runs use the cached model and are fast.

---

## Logic disagreements

### The classifier puts a ticket in the wrong intent category

**Cause:** The player used phrasing not in the signal dictionary.

**Resolution:**
1. Check what signals fired: add `print(intent_scores)` temporarily in `classifier.py`
2. If the correct intent has no signals matching the message, add the phrasing to `INTENT_SIGNALS`
3. Re-run tests to check for unintended side effects
4. If the system consistently fails on non-standard phrasing, this is a known limitation of keyword matching. The RAG layer handles this better for KB retrieval.

---

### The escalation decision seems wrong

**Resolution:**
1. Check `engine/escalation.py` hard trigger list
2. Check `engine/classifier.py` flags for the ticket
3. Run the ticket through `example_run.py` with the exact message to see the full pipeline output
4. Check `evaluation/failure-analysis.md` for the over/under-escalation failure modes

---

### Confusing output: confidence is 0.0

**Cause:** No keyword signals matched in the message at all. Intent = UNKNOWN.

**This is correct behavior.** The system routes to a human rather than guessing. If this is happening frequently, review the gap tracker:

```bash
python -c "from feedback.gap_tracker import get_gap_summary; import json; print(json.dumps(get_gap_summary(), indent=2))"
```
