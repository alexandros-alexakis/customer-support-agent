# Responsibility Map

> Archived. Superseded by docs/ structure and issue templates.

When something goes wrong, this table tells you which file to open.

| Observed behavior | File to change |
|---|---|
| Agent misclassifies intent | `engine/classifier.py` - update INTENT_SIGNALS |
| Agent escalates incorrectly | `engine/escalation.py` - review triggers |
| Agent routes to wrong team | `engine/escalation.py` - update ROUTING_TABLE |
| Agent gives wrong information | `knowledge-base/` relevant file, then re-sync |
| Agent makes unauthorized promise | `system-prompt.md` - add to PROHIBITED ACTIONS |
| Agent uses wrong tone | `system-prompt.md` - tighten tone section |
| Priority score wrong | `engine/prioritizer.py` |
| RAG retrieves irrelevant content | `knowledge-base/` relevant file, re-sync |
| RAG returns nothing | Run `python rag/kb_sync.py` |
| Zendesk not getting internal notes | `integrations/zendesk_webhook.py`, check trigger and API token |

For issue reporting, use the GitHub issue templates (bug, kb-gap, escalation-misfire, scope-creep, feature-request, improvement).
