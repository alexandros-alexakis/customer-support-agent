# Setup Guide

Full installation and configuration instructions for all operating systems.

---

## Before you start

**The Anthropic API key costs money.** The triage engine runs completely free with no API key. The API key is only needed for multilingual features and LLM response generation.

**The first sync will appear to hang.** When you run `python rag/kb_sync.py` for the first time, it downloads an 80MB machine learning model. This takes 1-2 minutes and shows no progress bar. This is normal.

**You must re-activate the virtual environment every session.** Every time you open a new terminal window, run the activate command again before running any Python commands. If you see `ModuleNotFoundError`, this is almost always the cause.

---

## Easiest setup (recommended)

**macOS / Linux:**
```bash
git clone https://github.com/alexandros-alexakis/ai-customer-support-agent.git
cd ai-customer-support-agent
bash setup.sh
```

**Windows (Command Prompt, not PowerShell):**
```
git clone https://github.com/alexandros-alexakis/ai-customer-support-agent.git
cd ai-customer-support-agent
setup.bat
```

The setup scripts handle everything and print clear next steps when done.

---

## Manual setup

### Prerequisites

| Requirement | Minimum version | How to check | Where to get it |
|---|---|---|---|
| Python | 3.10 | `python --version` | python.org/downloads |
| Git | Any | `git --version` | git-scm.com |
| Anthropic API key | Optional | — | console.anthropic.com |

### Step 1: Clone

```bash
git clone https://github.com/alexandros-alexakis/ai-customer-support-agent.git
cd ai-customer-support-agent
```

### Step 2: Create a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

```bash
cp .env.example .env   # macOS/Linux
copy .env.example .env # Windows
```

Open `.env` and add your API key if using LLM mode.

### Step 5: Sync the knowledge base

```bash
python rag/kb_sync.py
```

### Step 6: Validate

```bash
python run_agent.py --demo
pytest tests/ -v
python rag/example_rag.py
```

---

## Platform-specific notes

**Windows:** Use Command Prompt, not PowerShell. The Makefile does not work on Windows.

**macOS Apple Silicon:** If pip install fails with a torch error:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

---

See [troubleshooting.md](troubleshooting.md) for common failure modes.
