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

## Documentation

| Guide | What it covers |
|---|---|
| [QUICKSTART.md](QUICKSTART.md) | Clone to first run in 5 minutes |
| [SETUP.md](SETUP.md) | Full installation: venv, dependencies, validation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Component map, rule-based vs model-based, request flow |
| [HOW-IT-WORKS.md](HOW-IT-WORKS.md) | How every decision is made, operationally explained |
| [CONFIGURATION.md](CONFIGURATION.md) | All environment variables and provider config |
| [EXAMPLES.md](EXAMPLES.md) | Real input/output examples from the triage engine |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Symptom, cause, resolution for common failures |
| [EXTENDING.md](EXTENDING.md) | How to add issue types, rules, KB content safely |
| [LIMITATIONS.md](LIMITATIONS.md) | What is prototype-only, mocked, or missing |
| [PRODUCTIONIZATION.md](PRODUCTIONIZATION.md) | 5-phase roadmap to production deployment |
| [REPOSITORY-MAP.md](REPOSITORY-MAP.md) | Every file explained in one place |
| [VALIDATION-CHECKLIST.md](VALIDATION-CHECKLIST.md) | Confirm setup is working correctly |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Adapt this for your own company |
| [GETTING_STARTED.md](GETTING_STARTED.md) | All runnable commands with expected output |
| [integrations/zendesk-integration-guide.md](integrations/zendesk-integration-guide.md) | Complete Zendesk webhook setup |

---

## Quickstart

```bash
git clone https://github.com/alexandros-alexakis/ai-customer-support-agent.git
cd ai-customer-support-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run_agent.py --demo
```

Or with Make:

```bash
make setup
source venv/bin/activate
make agent-demo
```

See [QUICKSTART.md](QUICKSTART.md) for expected output and what the demo proves.

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
 llm_client.py             # LLM wrapper (mock or real Claude API)
      |
      v
 system-prompt.md          # Governs LLM response behavior
      |
      v
 knowledge-base/           # FAQ, policies, escalation rules, edge cases
```

The engine is entirely rules-based and deterministic. The system prompt governs non-deterministic LLM behavior. The knowledge base is loaded into ChromaDB for semantic retrieval. These three layers are intentionally separate.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full component map and [HOW-IT-WORKS.md](HOW-IT-WORKS.md) for how each decision is made.

---

## Run modes

| Mode | Requires | Cost | Output |
|---|---|---|
| Mock | Nothing | Free | Deterministic pre-written responses |
| LLM | `ANTHROPIC_API_KEY` in `.env` | API credits | Real Claude responses |

```bash
# Mock mode (default - no API key needed)
python run_agent.py --demo

# LLM mode (add key to .env first)
python run_agent.py --message "I was charged but didn't receive my coins"
```

---

## Scope

The assistant handles **Tier 1 player support** only:

- Payment and purchase issues
- Account access and login problems
- In-game item or currency discrepancies
- Basic game mechanic questions
- Technical troubleshooting (crashes, connectivity)
- VIP player handling
- Escalation routing for out-of-scope issues

Out of scope at Tier 1: ban enforcement, fraud investigation, legal and GDPR responses, refund approvals.

---

## Current Limitations

| Limitation | Detail |
|---|---|
| No account data access | Works only on player-provided text. Cannot verify purchases or account history. |
| No session memory | Each ticket is stateless. Prior contact history is passed in as a parameter. |
| Keyword-based classification | Unusual phrasing reduces accuracy. RAG retrieval partially compensates. |
| No incident detection | Cannot detect multiple players reporting the same issue across sessions. |
| Prototype system prompt | Not red-teamed at production volume. |

See [LIMITATIONS.md](LIMITATIONS.md) for the complete list.

---

## Running tests

```bash
pytest tests/ -v
```

## Running the evaluation pipeline

```bash
make eval
```

---

## Evaluation approach

- Escalation accuracy (target: >90% correctly routed)
- Scope compliance (target: >95%)
- Evidence collection completeness
- Hallucination avoidance
- CSAT by ticket complexity band

See [evaluation-criteria.md](evaluation-criteria.md) for full metric definitions and [evaluation/failure-analysis.md](evaluation/failure-analysis.md) for known failure modes.

---

## Author

**Alexandros Alexakis**
Vendor Manager & L&D Lead | Player Care
Scorewarrior, Limassol, Cyprus
[LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/)

---

## Status

Prototype. Functional triage engine with unit tests, semantic knowledge base, gap tracking, feedback loop, multilingual support, evaluation pipeline, and Zendesk integration guide. System prompt and knowledge base are design artifacts, not deployed configuration.

See [PRODUCTIONIZATION.md](PRODUCTIONIZATION.md) for what is required to deploy this in production.
