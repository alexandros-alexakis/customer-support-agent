# Roadmap

---

## In progress

- Full docs/ folder restructure
- Learning loop: escalate instead of hallucinate, learn from agent replies
- Known issues directory with incident logging
- VIP tier definitions
- Compensation matrix (keyed to known issues + VIP tier)
- Incident detection layer
- Agent handoff template
- Response quality rubric
- Seasonal and event risk guide
- 6 GitHub issue templates

---

## Short term

**Live account data integration**
Connect to live player account data so the system can verify purchases and account status without human lookup. Biggest current limitation.

**CSAT survey integration**
Automatically trigger a CSAT survey after ticket closure. Enables proper measurement segmented by ticket complexity.

**Confidence threshold calibration guide**
A structured process for calibrating the 0.65 classification threshold and 0.70 RAG similarity threshold against real ticket samples before going live.

---

## Medium term

**Proactive outreach for known issues**
When a confirmed incident is logged in the known issues directory, automatically notify affected players before they contact support. Requires incident detection and a player notification system.

**Agent assist mode**
AI runs in parallel with human agents, suggesting responses rather than sending them. The step before full automation.

**Cross-session incident detection**
Real-time aggregation layer that watches for volume spikes on the same intent + platform + time window and surfaces an alert to ops.

---

## Long term

**Full Tier 1 autonomy**
Agent handles Tier 1 tickets end-to-end without human review, with oversight only for escalations and QA sampling. Requires proven performance baseline and stakeholder approval.

**Predictive volume forecasting**
Use historical ticket data to predict volume spikes and automatically adjust staffing recommendations.
