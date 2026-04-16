# Validation Checklist

Use this checklist to confirm that the repository is set up correctly and working as expected.

---

## 1. Environment setup

- [ ] Python 3.10 or higher is installed (`python --version`)
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated (terminal shows `(venv)`)
- [ ] Dependencies installed without errors (`pip install -r requirements.txt`)
- [ ] `.env` file exists (copied from `.env.example`)
- [ ] `ANTHROPIC_API_KEY` is set in `.env` (required for LLM features)

---

## 2. Basic engine run

Run: `python example_run.py`

- [ ] Command completes without error
- [ ] Four ticket results are printed
- [ ] Each result shows: Intent, Tone, Flags, Priority, Escalate, Team, Strategy, Collect, Processed time
- [ ] `player_001` (payment issue) shows `Escalate: True` and `Team: billing`
- [ ] `player_003` (VIP churn risk) shows `Flags: ['vip_player', 'churn_risk']` and `Priority: Critical`
- [ ] `player_004` (legal threat) shows `Flags: ['legal_threat']` and `Escalate: True`

---

## 3. Unit tests

Run: `pytest tests/ -v`

- [ ] All tests pass
- [ ] No import errors
- [ ] `test_payment_issue_detected` passes
- [ ] `test_threatening_tone_detected` passes
- [ ] `test_vip_always_requires_human` passes
- [ ] `test_fraud_report_is_critical` passes

---

## 4. RAG knowledge base

Run: `python rag/kb_sync.py`

- [ ] Command completes without error
- [ ] Output shows files processed and chunks created
- [ ] `rag/chroma_store/` directory is created
- [ ] At least 10 files processed, at least 40 chunks created

Run: `python rag/example_rag.py`

- [ ] Command completes without error
- [ ] Similarity scores are printed for each query
- [ ] Non-standard phrasing ("they took money from my account") retrieves payment-related content

---

## 5. Evaluation pipeline

Run in order:
```bash
python evaluation/scripts/fetch_tickets.py
python evaluation/scripts/evaluate_tickets.py
python evaluation/scripts/generate_report.py
```

- [ ] `evaluation/data/tickets.json` is created with 200 tickets
- [ ] `evaluation/data/results.json` is created
- [ ] `evaluation/data/report.md` is created
- [ ] Report shows escalation accuracy above 70% (expected range given keyword-based classifier)
- [ ] Report shows false negatives listed (tickets that should have escalated but did not)

---

## 6. Gap tracker and feedback (smoke test)

Run:
```bash
python -c "
from feedback.gap_tracker import record_gap, get_gap_summary
record_gap('test message', 'unknown', 0.2, [], 'low_confidence')
print(get_gap_summary())
"
```

- [ ] No errors
- [ ] Summary shows `total: 1` and `by_reason: {low_confidence: 1}`
- [ ] `feedback/gaps.json` is created

---

## 7. Multilingual (requires ANTHROPIC_API_KEY)

Run: `python multilingual/example_multilingual.py`

- [ ] Command completes without error
- [ ] Spanish message is detected as Spanish and receives a Spanish response
- [ ] French message is detected as French and receives a French response
- [ ] Response content addresses the payment issue, not just language

---

## 8. Configuration check

- [ ] `.env` is in `.gitignore` (run `git status` - `.env` should not appear as a tracked file)
- [ ] `rag/chroma_store/` is in `.gitignore`
- [ ] `feedback/gaps.json` is in `.gitignore`
- [ ] `evaluation/data/` is in `.gitignore`

---

## 9. Zendesk integration (optional - requires Zendesk account)

- [ ] All Zendesk variables are set in `.env`
- [ ] `python integrations/zendesk_webhook.py` starts without error
- [ ] `/health` endpoint returns `{"status": "ok"}` when curled
- [ ] Test ticket creates an internal note in Zendesk with AI triage result

---

## If a check fails

See `TROUBLESHOOTING.md` for symptom-by-symptom resolutions.

If the issue is not covered there, check:
1. Python version: `python --version` (must be 3.10+)
2. Virtual environment active: terminal shows `(venv)`
3. All dependencies installed: `pip list | grep chromadb`
4. Running from project root: `ls engine/` should show Python files
