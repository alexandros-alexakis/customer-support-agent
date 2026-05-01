# Player Care AI - Support Operations Toolkit

![Project Banner](banner.png)

## What this is

A complete AI-powered customer support operations toolkit for gaming, built on Claude (Anthropic).

It covers the full support operations stack: automated ticket triage, LLM response generation, multilingual support, knowledge base retrieval, session memory, incident detection, QA scoring, agent coaching, training scenario generation, shift handover reporting, and team performance dashboards.

Built by **Alexandros Alexakis**, Vendor Manager & L&D Lead.

---

## What's included

| Layer | What it does |
|---|---|
| **Triage engine** | Classifies intent and tone, assigns P1–P5 priority, makes escalation decisions — fully deterministic |
| **RAG knowledge base** | Semantic search over policy and FAQ documents using ChromaDB |
| **LLM response generation** | Assembles full prompts and calls Claude API — or runs free in mock mode |
| **Multilingual support** | Detects player language, responds natively, translates KB content into 5 languages |
| **Session memory** | Persists conversation history per player across turns |
| **Player account context** | Injects account data (spend, tenure, VIP tier, device) into every prompt |
| **Incident detection** | Groups tickets by intent in rolling time windows and flags potential outages |
| **Zendesk & Helpshift** | Full webhook handlers — triage results written back as internal notes and tags |
| **Automated QA scoring** | Claude scores agent responses against a 100-point rubric |
| **Coaching report** | Turns QA scores into specific coaching plans per intent and team |
| **Training scenarios** | Graded practice scenarios (Easy / Medium / Hard) for onboarding and calibration |
| **Shift handover report** | End-of-shift summary: active incidents, critical flags, gaps, recommended actions |
| **Team performance dashboard** | QA scores, escalation accuracy, and volume aggregated by routing team |
| **Evaluation pipeline** | Synthetic ticket generation, batch evaluation, and markdown report generation |
| **Feedback loop** | Records wrong escalations, hallucinated policies, and tone failures for KB improvement |

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

**No API key needed.** The agent runs in mock mode by default — free, deterministic, no setup beyond installing dependencies.

See [QUICKSTART.md](QUICKSTART.md) for expected output and what the demo proves.

---

## Architecture

```
Incoming ticket
      |
      v
 player/account_provider.py    # Account context (spend, VIP tier, device, tenure)
      |
      v
 engine/classifier.py          # Intent + tone detection, confidence scoring
      |
      v
 engine/prioritizer.py         # Rules-based P1-P5 priority + SLA assignment
      |
      v
 engine/escalation.py          # Escalation decision + team routing
      |
      v
 engine/response_router.py     # Response strategy
      |
      v
 rag/retriever.py              # Semantic KB retrieval (ChromaDB)
      |
      v
 multilingual/language_handler.py  # Language detection + prompt modification
      |
      v
 memory/session_store.py       # Conversation history
      |
      v
 llm_client.py                 # LLM wrapper (mock or real Claude API)
      |
      v
 system-prompt.md + knowledge-base/   # Governs response behavior

Parallel:
 feedback/incident_detector.py     # Cross-ticket incident correlation
 qa/auto_scorer.py                 # Automated QA scoring
 operations/handover_report.py     # Shift handover generation
 operations/team_performance_dashboard.py  # Team metrics
 training/scenario_generator.py    # Agent training scenarios
```

The triage engine is entirely rules-based and deterministic. The LLM layer handles response generation only. These are intentionally separate so triage decisions are always auditable.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full component map and [HOW-IT-WORKS.md](HOW-IT-WORKS.md) for how each decision is made.

---

## Run modes

| Mode | Requires | Cost | Output |
|---|---|---|---|
| Mock | Nothing | Free | Deterministic pre-written responses |
| LLM | `ANTHROPIC_API_KEY` in `.env` | API credits | Real Claude responses |

```bash
# Mock mode (default - no API key needed)
python run_agent.py --demo

# With session memory
python run_agent.py --session --message "I was charged but didn't receive my coins"

# LLM mode
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

## Ops and L&D tools

```bash
# Generate agent training scenarios
python training/scenario_generator.py

# Generate coaching report from QA scores
python qa/coaching_report.py

# Generate shift handover report
python operations/handover_report.py

# Generate team performance dashboard
python operations/team_performance_dashboard.py
```

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
| [CONTRIBUTING.md](CONTRIBUTING.md) | Adapt this for your own company |
| [integrations/zendesk-integration-guide.md](integrations/zendesk-integration-guide.md) | Zendesk webhook setup |
| [integrations/helpshift/helpshift-integration-guide.md](integrations/helpshift/helpshift-integration-guide.md) | Helpshift webhook setup |

---

## Limitations

| Limitation | Detail |
|---|---|
| Keyword-based classification | Unusual phrasing reduces accuracy. RAG retrieval partially compensates. |
| English-biased classifier | `INTENT_SIGNALS` uses English keywords. Non-English input is translated at the response layer but classification remains English-first. |
| Player account backend is mocked | `player/account_provider.py` generates deterministic fake data. A real backend integration point is defined but not yet wired. |
| Prototype system prompt | Not red-teamed at production volume. |
| No live metrics backend | QA scores and dashboards are file-based. Production deployment would require a proper metrics store. |

See [LIMITATIONS.md](LIMITATIONS.md) for the complete list.

---

## Author

**Alexandros Alexakis**
Vendor Manager & L&D Lead | Player Care
[LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/)

---

## Status

Functional prototype. Triage engine with unit tests, semantic knowledge base, RAG retrieval, multilingual support, session memory, player account context, incident detection, Zendesk and Helpshift integrations, automated QA scoring, coaching reports, training scenario generator, shift handover reports, and team performance dashboard.

System prompt and knowledge base are design artifacts, not deployed configuration.

See [PRODUCTIONIZATION.md](PRODUCTIONIZATION.md) for the production deployment roadmap.
