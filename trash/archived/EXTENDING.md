# Extending the Agent

> Archived. Moved to docs/guides/extending.md

How to safely add new capabilities, update existing logic, and verify that changes work.

## Guiding principle

Every change has a risk. The classifier, escalation rules, and system prompt interact. Always test after changing anything.

## Adding a new issue type

Files to change: `engine/classifier.py`, `knowledge-base/decision-table.md`, `evaluation/test-cases.md`

Steps: add to Intent enum, add keyword signals, add routing rule, add response action, add collection requirements, add KB row, add test cases, run tests.

## Updating the knowledge base

Edit the relevant file in `knowledge-base/`, re-run `python rag/kb_sync.py`, test retrieval.

## Modifying the system prompt

Highest-risk change. Document why, identify what must and must not change, review all 30 test cases after, run evaluation pipeline, compare reports.

## Verifying changes

A change is not an improvement unless: pytest passes, evaluation pipeline shows target metric improved, no other metric degraded, change is logged in changelog.
