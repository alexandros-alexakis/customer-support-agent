# Roadmap

---

## Completed

- docs/ folder restructure with subfolders (setup/, guides/, operations/, risk/, learning-loop/, roadmap/)
- Learning loop: agent escalates instead of hallucinating, learns from agent replies, requires human approval before KB updates
- Known issues directory with incident logging template
- VIP tier definitions
- Compensation matrix (keyed to known issues and VIP tier)
- Incident detection layer
- Agent handoff template
- Response quality rubric
- Seasonal and event risk guide
- 6 GitHub issue templates (bug, kb-gap, escalation-misfire, scope-creep, feature-request, improvement)
- Zendesk and Helpshift webhook integrations
- Automated QA scoring and coaching reports
- Training scenario generator
- Shift handover report
- Team performance dashboard
- Multilingual support across 5 languages
- RAG retrieval with ChromaDB
- Session memory per player
- Player account context injection

---

## Short term

**Live account data integration**
Connect to live player account data so the system can verify purchases and account status without human lookup. Currently the account context layer uses mock data. This is the biggest remaining limitation.

**CSAT survey integration**
Automatically trigger a CSAT survey after ticket closure. Enables proper CSAT measurement segmented by ticket complexity band.

**Confidence threshold calibration guide**
A structured process for calibrating the 0.65 classification threshold and 0.70 RAG similarity threshold against real ticket samples before going live. Thresholds set in a prototype are guesses until validated against real volume.

---

## Medium term

**Proactive outreach for known issues**
When a confirmed incident is logged in the known issues directory, automatically notify affected players before they contact support. Requires incident detection and a player notification system.

**Agent assist mode**
AI runs in parallel with human agents, suggesting responses rather than sending them. The step before full automation.

**Cross-session incident detection**
Real-time aggregation layer that watches for volume spikes on the same intent and platform within a time window and surfaces an alert to ops.

---

## Long term

**Full Tier 1 autonomy**
Agent handles Tier 1 tickets end-to-end without human review, with oversight only for escalations and QA sampling. Requires proven performance baseline and stakeholder approval. Not a starting point.

**Predictive volume forecasting**
Use historical ticket data to predict volume spikes and automatically adjust staffing recommendations.
