# Agent Versioning Guide

> Archived. Moved to docs/roadmap/agent-versioning.md

This document defines how changes to the agent are tracked, tested, and rolled back if needed.

## Version Numbering

Semantic versioning: MAJOR.MINOR.PATCH

| Type | When to increment |
|---|---|
| MAJOR | Fundamental redesign of system prompt or scope |
| MINOR | New capability or significant content expansion |
| PATCH | Small corrections, wording fixes, KB updates |

## Change Control

Before any change: document the reason, identify affected files, assess risk level.
After any change: update changelog, increment version, run QA on at least 10 tickets.

## Risk levels

| Risk | Examples | Approval |
|---|---|---|
| Low | Wording fix, new FAQ | Agent owner |
| Medium | New escalation trigger, tone adjustment | Team Lead |
| High | System prompt restructure, scope change | Management |
