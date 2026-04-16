# Quickstart

Get from clone to first successful run as fast as possible.

---

## Fastest path (recommended)

**macOS / Linux:**
```bash
git clone https://github.com/alexandros-alexakis/customer-support-agent.git
cd customer-support-agent
bash setup.sh
```

**Windows (Command Prompt - not PowerShell):**
```
git clone https://github.com/alexandros-alexakis/customer-support-agent.git
cd customer-support-agent
setup.bat
```

The setup script installs everything and prints exactly what to do next.

---

## After setup: run the example

Activate your virtual environment first:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Then run:

```bash
python example_run.py
```

**You must activate the venv every time you open a new terminal.** If you see `ModuleNotFoundError`, this is why.

---

## Expected output

```
============================================================
Player: player_001
Message: I was charged $9.99 for coins but they never appeared...
Contact count: 1 | VIP: False
------------------------------------------------------------
Intent:      payment_issue (confidence: 0.857)
Tone:        neutral
Flags:       []
Priority:    High (P3) - SLA: 8.0h
Escalate:    True -> billing
Reason:      high-priority intent: payment_issue
Strategy:    Follow payment troubleshooting steps...
Collect:     ['Player ID', 'Transaction ID', 'Purchase date and amount', 'Platform']
Processed:   0.31ms
```

You should see four results like this, one for each example ticket.

---

## What this proves

The triage engine is working. It classified the player's intent, scored confidence, assigned priority and SLA, made an escalation decision, routed to the correct team, and specified what information to collect.

## What this does not prove

- No message was sent to any player
- The engine is not connected to Zendesk or any live platform
- No LLM was called - the classifier is entirely rules-based
- The system prompt in `system-prompt.md` governs LLM behavior but is not invoked here

---

## No API key needed for this

`example_run.py` and `pytest tests/` run completely free with no Anthropic API key.

The API key is only needed for:
- `python multilingual/example_multilingual.py`
- Any feature that calls Claude to generate a player-facing response

---

## Next steps

```bash
# Run unit tests
pytest tests/ -v

# Sync knowledge base for semantic search
python rag/kb_sync.py
# Note: first run downloads ~80MB model, takes 1-2 minutes - do not close terminal

# Test semantic retrieval
python rag/example_rag.py

# Run full evaluation pipeline
python evaluation/scripts/fetch_tickets.py
python evaluation/scripts/evaluate_tickets.py
python evaluation/scripts/generate_report.py
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for all available commands.
See [SETUP.md](SETUP.md) for full installation details and troubleshooting.
