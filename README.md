# Player Care AI Engine

![Project Banner](banner%20(1).png)

## What this is

A domain-specific AI engine for Tier 1 gaming customer support, built on top of Claude AI (Anthropic).

This is not a generic chatbot wrapper. It is a modular processing pipeline designed around the actual operational constraints of player support at scale: high ticket volume, multilingual teams, variable player value, and the need for consistent escalation decisions under pressure.

Built and documented by **Alexandros Alexakis**, Vendor Manager & L&D Lead at Scorewarrior.

---

## The problem this solves

Support teams handling large game titles deal with a predictable but high-volume mix of Tier 1 issues: payment failures, account access, bugs, and player frustration. The challenge is not answering these questions - it is doing so consistently, at scale, without burning out agents on repetitive work or letting complex cases slip through.

The specific failure modes this engine addresses:

- **Inconsistent escalation decisions** - whether a ticket gets escalated depends too much on which agent handles it
- **Poor prioritisation** - urgent tickets (churn risk, VIP complaints, legal threats) sit in the same queue as mechanic questions
- **No early warning on player sentiment** - by the time frustration becomes a visible problem, the player is already churning
- **CSAT measurement bias** - AI handles easy tickets, agents handle hard ones, and the comparison tells you nothing useful (see `qa/ai-csat-bias-analysis.md`)

---

## Architecture

```
Incoming ticket
      |
      v
 classifier.py       # Intent and tone detection with confidence scoring
      |
      v
 prioritizer.py      # Rules-based priority scoring (P1-P5) with SLA targets
      |
      v
 escalation.py       # Escalation decision and team routing
      |
      v
 response_router.py  # Translate decisions into agent response strategy
      |
      v
 pipeline.py         # Orchestrates all steps with structured logging
```

Each module has a single responsibility. This is deliberate. When escalation logic changes (and it will), you edit one file. When routing rules change, you edit one file. Nothing is entangled.

---

## Key design decisions

**Rules-based classification, not ML**

The intent classifier uses keyword signal matching rather than a trained model. This is a deliberate tradeoff. Rules are auditable, explainable to non-technical stakeholders, and adjustable without retraining. The downside is lower recall on unusual phrasing. The mitigation is a confidence threshold below which the system defers to human review rather than guessing.

**Confidence threshold at 0.65**

Below 65% confidence, the system does not act autonomously. It routes to a human. This is conservative by design. A wrong autonomous response damages player trust more than a slight delay from human review.

**Hard escalation rules are non-negotiable**

Certain conditions always escalate regardless of confidence: legal threats, ban appeals, fraud reports, VIP players, repeat contacts. These are not configurable at runtime. Operational decisions that bypass these rules require a code change, not a config tweak - making the decision visible and deliberate.

**Priority is rules-based, not ML-scored**

Priority scoring uses a deterministic rules engine. The inputs are intent, tone, VIP status, and contact history. This produces a score of 1-5 with an attached SLA target. Rules-based priority is faster, more auditable, and easier to explain to operations teams than a black-box score.

**Structured logging at every step**

Every pipeline stage emits a structured JSON log event. Classification decisions, escalation triggers, and processing times are all logged with player context. This makes it possible to audit why a ticket was handled a specific way after the fact.

---

## Tradeoffs and limitations

**No real-time account data access**
The classifier has no access to player account records, transaction history, or game data. It works only on the text of the message. This limits its ability to verify claims (e.g. confirming a transaction actually exists before routing to billing).

**Keyword matching misses paraphrase**
A player who says "took my money" instead of "charged" will score lower on payment intent. The confidence threshold catches the worst cases, but recall is imperfect. This is acceptable at prototype stage and would be addressed with LLM-based classification in production.

**No session memory**
The pipeline processes each ticket independently. It does not know what was said in previous turns of the same conversation. Contact count is passed in as a parameter from the support platform, not inferred.

**English only**
The signal dictionaries are in English. Multilingual support requires translated signal sets or replacement with an LLM-based classifier.

---

## Repository structure

```
engine/
  classifier.py          # Intent and tone classification
  prioritizer.py         # Priority scoring and SLA assignment
  escalation.py          # Escalation decisions and team routing
  response_router.py     # Response strategy generation
  pipeline.py            # Full pipeline orchestrator
  logging_config.py      # Structured JSON logging
  metrics_spec.py        # What to measure and why

tests/
  test_classifier.py     # Unit tests for classification logic
  test_prioritizer.py    # Unit tests for priority scoring

knowledge-base/          # FAQ and policy documents for agent reference
operations/              # Operational templates and playbooks
qa/                      # QA framework and evaluation tools
onboarding/              # Agent training and certification
sample-conversations/    # Annotated example interactions
```

---

## Running the example

```bash
pip install -r requirements.txt
python example_run.py
```

---

## Running tests

```bash
pip install pytest
pytest tests/
```

---

## Author

**Alexandros Alexakis**
Vendor Manager & L&D Lead | Player Care
Scorewarrior, Limassol, Cyprus
[LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/)

---

## Status

Prototype stage. The engine is functional and tested. Production deployment would require integration with a live support platform webhook, account data API, and a metrics backend. See `roadmap.md` for planned improvements.
