# Agent Versioning Guide

## Overview

This document defines how changes to the customer support agent are tracked, tested, and rolled back if needed. Versioning ensures that improvements can be made safely without breaking existing performance.

---

## Version Numbering

The agent uses semantic versioning: **MAJOR.MINOR.PATCH**

| Type | When to increment | Example |
|---|---|---|
| MAJOR | Fundamental redesign of the system prompt or scope | 1.0 to 2.0 |
| MINOR | New capability added or significant content expansion | 1.1 to 1.2 |
| PATCH | Small corrections, wording fixes, KB updates | 1.1.0 to 1.1.1 |

---

## Change Control Process

### Before making any change:

1. Document the reason for the change
2. Identify which file(s) will be affected
3. Assess the risk level (Low / Medium / High)
4. For High risk changes, test against sample conversations before deploying

### After making a change:

1. Update CHANGELOG.md with what changed and why
2. Increment the version number appropriately
3. Run QA review on at least 10 tickets to confirm no regression
4. Document any unexpected effects

---

## Risk Classification

| Risk Level | Examples | Approval Required |
|---|---|---|
| Low | Wording fix in KB, adding a new FAQ | Agent owner |
| Medium | New escalation trigger, tone adjustment | Team Lead |
| High | System prompt restructure, scope change | Management |

---

## Rollback Process

If a change causes performance degradation:

1. Identify the commit in GitHub that introduced the change
2. Revert to the previous version of the affected file(s)
3. Document the rollback in CHANGELOG.md
4. Investigate root cause before attempting the change again

GitHub commit history serves as the version control record. Every commit message should clearly describe what was changed to make rollbacks straightforward.

---

## Testing Before Deployment

For any Medium or High risk change, test against these standard scenarios before deploying:

- Payment issue (standard)
- Account access issue
- Angry player
- VIP complaint
- Immediate escalation trigger
- Out of scope request

If the agent handles all six correctly, the change is safe to deploy.
