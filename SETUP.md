# Setup Guide

Full installation and configuration instructions for all operating systems.

---

## Before you start - important notes

**The Anthropic API key costs money.** The triage engine (`example_run.py`, `pytest`) runs completely free with no API key. The API key is only needed for the multilingual features and LLM response generation. The free tier at console.anthropic.com has usage limits. For basic setup and testing you may not need it at all.

**The first sync will appear to hang.** When you run `python rag/kb_sync.py` for the first time, it downloads an 80MB machine learning model. This takes 1-2 minutes and shows no progress bar. This is normal. Do not close the terminal.

**You must re-activate the virtual environment every session.** Every time you open a new terminal window, you need to run the activate command again before running any Python commands. If you see `ModuleNotFoundError`, this is almost always the cause.

---

## Easiest setup (recommended for non-developers)

**macOS / Linux:**
```bash
git clone https://github.com/your-username/ai-customer-support-agent.git
cd ai-customer-support-agent
bash setup.sh
```

**Windows (Command Prompt, not PowerShell):**
```
git clone https://github.com/your-username/ai-customer-support-agent.git
cd ai-customer-support-agent
setup.bat
```

The setup scripts handle everything and print clear next steps when done.

---

## Manual setup

### Prerequisites

| Requirement | Minimum version | How to check | Where to get it |
|---|---|---|---|
| Python | 3.10 | `python --version` or `python3 --version` | python.org/downloads |
| Git | Any | `git --version` | git-scm.com |
| Anthropic API key | Optional for basic use | - | console.anthropic.com |

**Windows note:** During Python installation, check the box **"Add Python to PATH"**. Without this, `python` will not be recognized as a command.

---

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/ai-customer-support-agent.git
cd ai-customer-support-agent
```

---

### Step 2: Create a virtual environment

A virtual environment keeps this project's dependencies separate from your system Python. Always use one.

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```
python -m venv venv
venv\Scripts\activate
```

After activation your terminal prompt changes to show `(venv)` at the start.

**Every time you open a new terminal, run the activate command again before using Python.**

To deactivate when done:
```bash
deactivate
```

---

### Step 3: Install dependencies

With the venv active:

```bash
pip install -r requirements.txt
```

This takes 2-5 minutes. You will see many lines of output - this is normal.

| Package | Purpose |
|---|---|
| `anthropic` | Claude API client |
| `chromadb` | Local vector database for RAG |
| `sentence-transformers` | Local embeddings (~80MB download on first sync) |
| `flask` | Web server for Zendesk webhook |
| `gunicorn` | Production server |
| `python-dotenv` | Reads `.env` file |
| `requests` | HTTP client for Zendesk API |
| `pytest` | Test runner |

---

### Step 4: Configure environment variables

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Open `.env` in any text editor and fill in:

```
ANTHROPIC_API_KEY=your_key_here
```

Leave the Zendesk variables blank unless you are setting up the Zendesk integration.

**Where to get your Anthropic API key:**
1. Go to console.anthropic.com
2. Sign up or log in
3. Click "API Keys" in the left menu
4. Click "Create Key"
5. Copy the key and paste it into `.env`

**Note:** You do not need this key to run `run_agent.py --demo` or `pytest`. The agent runs in mock mode without it.

---

### Step 5: Sync the knowledge base

```bash
python rag/kb_sync.py
```

**First run warning:** This downloads an ~80MB model. It will appear to hang for 1-2 minutes. Wait for it.

---

### Step 6: Validate the setup

```bash
# Check 1: Full agent run (no API key needed)
python run_agent.py --demo

# Check 2: Unit tests pass
pytest tests/ -v

# Check 3: RAG retrieval works
python rag/example_rag.py
```

If all three pass, the setup is complete.

---

## Platform-specific notes

### Windows
- Use Command Prompt (`cmd.exe`), not PowerShell
- Activation command: `venv\Scripts\activate`
- The `Makefile` does not work on Windows - use `setup.bat` and run commands manually

### macOS with Apple Silicon (M1/M2/M3)

If `pip install -r requirements.txt` fails with a torch error:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Python version conflicts

If `python --version` shows Python 2.x, use `python3` and `pip3` instead.

---

## Common issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate venv: `source venv/bin/activate` |
| `python: command not found` | Use `python3` instead |
| `kb_sync.py` appears frozen | Wait 1-2 minutes - model is downloading |
| `AuthenticationError` | Check `ANTHROPIC_API_KEY` in `.env` |
| Tests fail with import error | Make sure you are in the project root directory |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for full coverage.
