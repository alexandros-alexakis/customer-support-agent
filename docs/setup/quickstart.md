# Quickstart

Get from clone to a running demo in under 5 minutes.

---

## Fastest path

**macOS / Linux:**
```bash
git clone https://github.com/alexandros-alexakis/ai-customer-support-agent.git
cd ai-customer-support-agent
bash setup.sh
source venv/bin/activate
python run_agent.py --demo
```

**Windows (Command Prompt):**
```
git clone https://github.com/alexandros-alexakis/ai-customer-support-agent.git
cd ai-customer-support-agent
setup.bat
venv\Scripts\activate
python run_agent.py --demo
```

**No API key needed.** The agent runs in mock mode by default — free, deterministic, no setup beyond installing dependencies.

---

## What `run_agent.py --demo` does

Runs this message through the complete pipeline:

```
"I bought gems but they never showed up in my account."
```

And prints a full execution trace showing intent classification, priority scoring, escalation decision, response strategy, and the assembled prompt.

---

## Run modes

| Mode | Requires | Cost | Output |
|---|---|---|---|
| Mock | Nothing | Free | Deterministic pre-written responses |
| LLM | `ANTHROPIC_API_KEY` in `.env` | API credits | Real Claude responses |

To switch to LLM mode, add your key to `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

---

## Other ways to run

```bash
# Your own message
python run_agent.py --message "I can't log into my account"

# With contact history and VIP flag
python run_agent.py --message "still not fixed" --contact-count 3 --vip

# Interactive prompts
python run_agent.py
```

---

## Next steps

```bash
# Sync knowledge base for semantic search
python rag/kb_sync.py
python run_agent.py --demo

# Run unit tests
pytest tests/ -v

# Run full evaluation pipeline
make eval
```

See [setup.md](setup.md) for full installation details.
See [configuration.md](configuration.md) for environment variables.
