# Quickstart

Get from clone to first successful run in under 5 minutes.

---

## Step 1: Clone and enter the project

```bash
git clone https://github.com/alexandros-alexakis/customer-support-agent.git
cd customer-support-agent
```

## Step 2: Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

## Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the example

```bash
python example_run.py
```

## Expected output

You should see four ticket results printed to the terminal. Each looks like this:

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

## What this proves

The triage engine is working. It classified the intent, scored a confidence level, assigned priority and SLA, made an escalation decision, determined the routing team, and specified what information to collect.

## What this does not prove

- This is not a live agent. No message was sent to any player.
- The engine is not connected to Zendesk or any support platform.
- No LLM was called in this run. The classifier is rules-based.
- The system prompt in `system-prompt.md` governs LLM behavior but is not invoked by `example_run.py`.

See `GETTING_STARTED.md` for all available commands including RAG, evaluation pipeline, and Zendesk integration.
