# Player Care AI - Support System Design

![Project Banner](banner%20(1).png)

## What this is

A structured prototype for a Tier 1 customer support assistant, designed for gaming player care operations.

This project documents the design logic, decision rules, knowledge base, escalation framework, and evaluation criteria for a prompt-driven AI support assistant built on Claude (Anthropic). It includes a working Python classification engine for ticket triage.

Built by **Alexandros Alexakis**, Vendor Manager & L&D Lead at Scorewarrior.

---

## What this is not

- A deployed production system
- A live agent with tool access, account lookup, or transaction verification
- A trained ML model
- A system with memory between sessions
- A replacement for human agents

This is a **policy-driven support assistant prototype**. The assistant responds based on a structured system prompt, a knowledge base, and defined decision rules. It has no access to backend systems unless explicitly integrated.

---

## Architecture

```
Incoming ticket
      |
      v
 engine/classifier.py      # Intent + tone detection, confidence scoring
      |
      v
 engine/prioritizer.py     # Rules-based P1-P5 priority + SLA assignment
      |
      v
 engine/escalation.py      # Escalation decision + team routing
      |
      v
 engine/response_router.py # Response strategy for agent or LLM
      |
      v
 system-prompt.md          # Governs LLM response behavior
      |
      v
 knowledge-base/           # FAQ, policies, escalation rules, edge cases
```

The engine handles triage. The system prompt governs what the assistant says. The knowledge base defines what it knows. These three layers are intentionally separate so each can be updated independently.

---

## Scope

The assistant is scoped to **Tier 1 player support** only:

- Payment and purchase issues
- Account access and login problems
- In-game item or currency discrepancies
- Basic game mechanic questions
- Technical troubleshooting (crashes, connectivity)
- VIP player handling
- Escalation routing for out-of-scope issues

Out of scope at Tier 1: ban enforcement decisions, fraud investigation, legal and GDPR responses, account security breaches, refund approvals.

---

## Current Limitations

| Limitation | Detail |
|---|---|
| No account data access | The assistant cannot verify purchases, balances, or account history. It works only on player-provided information. |
| No session memory | Each conversation starts fresh. Prior contact history must be passed in as a parameter. |
| English only | Signal dictionaries and knowledge base are English. Multilingual support is not implemented. |
| Keyword-based classification | The classifier uses signal matching, not semantic understanding. Unusual phrasing reduces accuracy. |
| Confidence threshold gaps | Low-confidence tickets route to humans. This is correct but creates load on human agents during ambiguous volume spikes. |
| No incident detection across sessions | The system cannot detect that multiple players are reporting the same issue simultaneously without external aggregation. |
| Prototype system prompt | The system prompt has not been red-teamed or stress-tested at production volume. |

---

## What Productionization Would Require

1. **Account data integration** - API access to player account records, transaction history, and game event logs so the assistant can verify claims rather than accept them at face value.
2. **Session continuity** - Persistent conversation state so the assistant knows what was tried in prior contacts.
3. **Incident detection layer** - Cross-session signal aggregation to detect when multiple players report the same issue, triggering a proactive incident response.
4. **Multilingual support** - Either translated signal dictionaries or replacement of keyword classification with LLM-based intent detection.
5. **Red-teaming the system prompt** - Structured adversarial testing for prompt injection, policy bypass attempts, and edge case handling.
6. **Human review pipeline** - Formal workflow for tickets flagged as low confidence or requiring escalation, with SLA tracking.
7. **Metrics backend** - Live tracking of classification accuracy, escalation rate, CSAT by ticket type, and unknown intent rate. See `engine/metrics_spec.py`.
8. **QA sampling automation** - Automated flagging of interactions for human QA review based on confidence score and issue type.

---

## Repository Structure

```
engine/                        # Python triage engine
  classifier.py                # Intent + tone classification
  prioritizer.py               # Priority scoring
  escalation.py                # Escalation decisions
  response_router.py           # Response strategy
  pipeline.py                  # Orchestrator
  logging_config.py            # Structured JSON logging
  metrics_spec.py              # What to measure and why

tests/                         # Unit tests
  test_classifier.py
  test_prioritizer.py

evaluation/
  test-cases.md                # 30+ test scenarios
  failure-analysis.md          # Known failure modes and mitigations

knowledge-base/                # Operational knowledge
  faq-payments.md
  faq-account-access.md
  faq-game-mechanics.md
  faq-technical-issues.md
  escalation-rules.md
  decision-table.md            # Structured decision logic
  vip-player-handling.md
  seasonal-events-guide.md
  refund-policy-detail.md
  banned-account-faq.md
  gdpr-requests.md
  tos-violations-guide.md
  edge-cases.md                # Realistic edge case handling

operations/                    # Operational templates
sample-conversations/          # Style examples (not test evidence)
onboarding/                    # Agent training
qa/                            # QA framework

system-prompt.md               # Core assistant behavior rules
interaction-flow.md            # Decision flow
evaluation-criteria.md         # How performance is measured
tone-guide.md
agent-limitations.md
agent-versioning.md
prompt-engineering-notes.md
CHANGELOG.md
roadmap.md
CONTRIBUTING.md
```

---

## Running the engine

```bash
pip install -r requirements.txt
python example_run.py
```

## Running tests

```bash
pytest tests/
```

---

## Evaluation approach

See `evaluation-criteria.md` for full metrics definitions. Key measures:

- Escalation accuracy (target: >90% correctly routed)
- Scope compliance (target: >95%)
- Evidence collection completeness
- Hallucination avoidance
- CSAT by ticket complexity band (see `qa/ai-csat-bias-analysis.md`)

---

## Author

**Alexandros Alexakis**
Vendor Manager & L&D Lead | Player Care
Scorewarrior, Limassol, Cyprus
[LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/)

---

## Status

Prototype. Functional triage engine with unit tests. System prompt and knowledge base are design artifacts, not deployed configuration. See `roadmap.md` for what comes next.
