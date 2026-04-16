# Makefile
# Common commands for setting up, running, and testing the project.
# Run any command with: make <command>
# Example: make setup

.PHONY: help setup test run agent agent-demo agent-interactive sync-kb rag-example eval feedback gaps webhook lint clean

# Default target - show available commands
help:
	@echo ""
	@echo "Player Care AI - Available commands:"
	@echo ""
	@echo "  SETUP"
	@echo "  make setup              Create venv, install dependencies, copy .env.example"
	@echo ""
	@echo "  RUNNING THE AGENT"
	@echo "  make agent-demo         Run agent with preset demo message (quickest start)"
	@echo "  make agent-interactive  Run agent with interactive input prompts"
	@echo "  make agent-interactive m='your message here'  Run with a specific message"
	@echo ""
	@echo "  TRIAGE ENGINE (no LLM)"
	@echo "  make run                Run the triage engine example (4 preset tickets)"
	@echo ""
	@echo "  KNOWLEDGE BASE"
	@echo "  make sync-kb            Sync knowledge base into ChromaDB vector store"
	@echo "  make rag-example        Run RAG retrieval demo"
	@echo ""
	@echo "  TESTING"
	@echo "  make test               Run unit tests"
	@echo "  make eval               Run full evaluation pipeline (generates report)"
	@echo ""
	@echo "  FEEDBACK"
	@echo "  make feedback           Show feedback summary"
	@echo "  make gaps               Show knowledge gap summary"
	@echo ""
	@echo "  ZENDESK"
	@echo "  make webhook            Start Zendesk webhook server (local)"
	@echo ""
	@echo "  CLEANUP"
	@echo "  make clean              Remove generated files (chroma_store, evaluation data)"
	@echo ""

# First-time setup
setup:
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "Installing dependencies..."
	./venv/bin/pip install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env && echo ".env created from .env.example - fill in your values"; fi
	@echo ""
	@echo "Setup complete. Next steps:"
	@echo "  1. Activate venv: source venv/bin/activate"
	@echo "  2. Edit .env (API key optional - works in mock mode without it)"
	@echo "  3. Run: make agent-demo"

# Run the full agent (with LLM or mock)
agent-demo:
	python run_agent.py --demo

agent-interactive:
	python run_agent.py

# Run agent with a specific message
# Usage: make agent m="I was charged but didn't receive my coins"
agent:
	python run_agent.py --message "$(m)"

# Run the triage engine only (no LLM, no prompt)
run:
	python example_run.py

# Run unit tests
test:
	pytest tests/ -v

# Sync knowledge base into ChromaDB
sync-kb:
	python rag/kb_sync.py

# Run RAG retrieval demo
rag-example:
	python rag/example_rag.py

# Run full evaluation pipeline
eval:
	@echo "Step 1: Generating synthetic tickets..."
	python evaluation/scripts/fetch_tickets.py
	@echo "Step 2: Evaluating tickets through pipeline..."
	python evaluation/scripts/evaluate_tickets.py
	@echo "Step 3: Generating report..."
	python evaluation/scripts/generate_report.py
	@echo ""
	@echo "Report saved to evaluation/data/report.md"

# Show feedback summary
feedback:
	python -c "from feedback.feedback_store import get_feedback_summary; import json; print(json.dumps(get_feedback_summary(), indent=2))"

# Show knowledge gap summary
gaps:
	python -c "from feedback.gap_tracker import get_gap_summary; import json; print(json.dumps(get_gap_summary(), indent=2))"

# Start Zendesk webhook server
webhook:
	python integrations/zendesk_webhook.py

# Clean generated files
clean:
	rm -rf rag/chroma_store/
	rm -rf evaluation/data/
	rm -f feedback/gaps.json
	rm -f feedback/feedback.json
	@echo "Cleaned generated files. Run make sync-kb to rebuild ChromaDB."
