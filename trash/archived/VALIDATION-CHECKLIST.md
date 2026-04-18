# Validation Checklist

> Archived. Moved to docs/setup/validation-checklist.md

Use this checklist to confirm the repository is set up correctly.

## Core checks

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] `pip install -r requirements.txt` completed without errors
- [ ] `.env` file exists with `ANTHROPIC_API_KEY` set
- [ ] `python example_run.py` completes and prints 4 ticket results
- [ ] `pytest tests/ -v` passes all tests
- [ ] `python rag/kb_sync.py` completes and creates `rag/chroma_store/`
- [ ] `python rag/example_rag.py` retrieves relevant content
- [ ] Evaluation pipeline runs and produces `evaluation/data/report.md`
- [ ] `.env` is not tracked by git (`git status` should not show it)
