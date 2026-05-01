# Player Care AI: Support Operations Prototype

![Project Banner](banner.png)

---

> **This project reflects my professional background in support operations, escalation design, quality assurance, and team training. It explores how AI can assist these workflows in a gaming player care environment, and where it cannot.**
>
> This is not a software engineering project. It is a support operations design project that uses code to make the logic runnable and testable.
>
> **Alexandros Alexakis**, Vendor Manager and L&D Lead, Player Care

---

## Part of a two-repo toolkit

This repo handles the **intake layer**: triage, escalation, routing, and response strategy.

The companion repo handles **what comes after**: scoring interactions, analysing CSAT, and generating coaching output.

| Repo | What it does |
|---|---|
| [ai-customer-support-agent](https://github.com/alexandros-alexakis/ai-customer-support-agent) (this repo) | Detects urgency, identifies VIP players, routes to the right team, generates response strategy |
| [ai-customer-support-qa](https://github.com/alexandros-alexakis/ai-customer-support-qa) | Scores interactions, analyses low CSAT, assigns responsibility, generates coaching notes |

The agent produces the interaction. The QA system evaluates it.

---

## What this is

A working prototype for a Tier 1 player support assistant in a gaming environment.

The system detects urgency, identifies VIP players, reads negative sentiment, spots legal threats, and routes tickets to the right team: billing, technical support, trust and safety, player relations, or legal compliance, before any human has to read the message.

It includes:
- A rules-based triage engine that runs without an API key
- A knowledge base covering common player issues, refund policies, and escalation rules
- A system prompt that governs how the AI responds when Claude is connected
- Session memory that persists conversation history per player across turns
- Player account context injected into every prompt (spend, VIP tier, device, tenure)
- Multilingual support: detects player language and responds natively in 5 languages
- Incident detection that groups tickets by intent and flags potential outages in real time
- Automated QA scoring of agent responses against a 100-point rubric
- Coaching reports, training scenario generators, shift handover reports, and team performance dashboards
- A feedback loop that learns from agent replies and builds toward KB updates over time
- Zendesk and Helpshift webhook integrations

Built by a support operations professional with a background in player care and vendor management.

---

## What this is not

- A deployed production system
- A live agent with account lookup, purchase verification, or backend access
- A trained machine learning model
- A system with memory between conversations
- A replacement for human agents

This is a **policy-driven prototype**. Every decision it makes is a recommendation for a human to review, not an action it takes on its own.

---

## What a support team would actually use this for

When a player contacts support, the agent currently has to read the message, decide how urgent it is, figure out who should handle it, and work out what information to collect, before writing a single word of response. On a busy queue, that cognitive load compounds across hundreds of tickets a day.

This system handles the intake layer:

| What the system does | Example |
|---|---|
| Detects urgency and assigns a priority level | Angry VIP with a failed payment -> P1, 30-minute SLA |
| Identifies threatening or distressed tone | "I'm taking legal action" -> flags immediately, routes to compliance |
| Recognises VIP players and raises priority | VIP expressing churn intent -> escalates to player relations before a generic reply goes out |
| Spots known high-risk patterns | Third contact on an unresolved issue -> flags for senior agent, not Tier 1 |
| Routes to the right team without manual reading | Account compromise -> Trust & Safety, not billing |
| Tells the agent what to collect before they ask | Payment issue -> collect transaction ID, platform, purchase date |
| Suggests a response tone and opening | Legal threat -> calm, formal, no engagement with the threat |
| Escalates instead of guessing | No KB match found -> ticket goes to a human, no hallucinated answer |

The agent opens the ticket and already knows: urgency, team, what to ask, and how to open. That is the operational value.

---

## Human-in-the-loop review

Good AI support design is not about maximising automation. It is about knowing exactly where automation helps and where it causes harm.

### What the AI can handle without human review

- Reading the message and detecting urgency level
- Identifying VIP status from the ticket context
- Recognising tone: neutral, frustrated, angry, threatening, distressed
- Routing to the correct team based on issue type
- Generating a list of information to collect
- Suggesting a response tone and opening approach
- Flagging low-confidence cases before they go anywhere

### What must always be reviewed by a human before action

| Trigger | Why human review is required |
|---|---|
| Any payment or refund action | The system cannot verify purchases. A human must check before any credit or reversal. |
| VIP churn risk | A personalised, senior-voice response is required. Templates make this worse. |
| Repeat contact (3+) on same issue | A human needs to understand why previous resolutions failed before responding again. |
| Low-confidence classification | If the system is not sure what the player wants, it does not guess. It sends the ticket to a human. |
| First response to an abusive player | Tone management here requires human judgment. Automated de-escalation often inflames. |
| Account compromise suspected | Identity must be verified through a secure channel before any information is disclosed. |

### What is never automated in this design

- Responses to legal threats
- Ban enforcement or ban appeals
- Fraud investigation
- Identity verification
- GDPR or data subject requests
- Refund approvals
- Any response where being wrong creates legal, financial, or safety risk

The AI does not send messages to players. It prepares a recommendation: triage result, suggested response, information to collect, and a human agent reviews it before anything reaches the player.

---

## Real support scenarios this system handles

See [CASE-STUDIES.md](CASE-STUDIES.md) for full operational walkthroughs.

| Scenario | What the system does |
|---|---|
| Player was charged but items never arrived | Detects payment issue, routes to billing, collects transaction ID |
| Player lost all progress after an update | Detects distress, routes to technical support, flags for possible incident |
| VIP player says they are quitting | Detects churn risk + VIP flag, escalates to player relations at P1 in 30 minutes |
| Player threatens a chargeback | Detects financial threat, routes to billing + flags for senior agent |
| Player claims their ban was unfair | Detects ban appeal, routes to Trust & Safety, holds from Tier 1 |
| Player's account was accessed by someone else | Detects security flag, routes to Trust & Safety at P1, does not disclose account info |
| Angry player contacts for the third time | Detects repeat contact + frustration, routes to senior agent, flags that previous resolutions failed |
| Crash on a specific feature after an update | Detects bug report, routes to technical, collects device and version info |

---

## Documentation

**Getting started**
- [Quickstart](QUICKSTART.md)
- [Setup](SETUP.md)
- [Configuration](CONFIGURATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)

**Understanding the system**
- [How it works](docs/guides/how-it-works.md)
- [Architecture](docs/guides/architecture.md)
- [Extending](EXTENDING.md)

**Operations and cases**
- [Case studies](CASE-STUDIES.md)
- [Interaction flow](docs/operations/interaction-flow.md)
- [Tone guide](docs/operations/tone-guide.md)

**Learning loop**
- [How the learning loop works](docs/learning-loop/overview.md)
- [KB maintenance guide](docs/learning-loop/kb-maintenance.md)

**Risks and limits**
- [Limitations](docs/risk/limitations.md)
- [Productionization roadmap](docs/risk/productionization.md)
- [Risk register](docs/risk/risk-register.md)

**Contributing**
- [Contributing](CONTRIBUTING.md)
- [Roadmap](docs/roadmap/roadmap.md)

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

No API key needed for the demo. See [QUICKSTART.md](QUICKSTART.md) for expected output.

---

## How the system works

```
Player message arrives
      |
      v
Detect urgency, intent, and tone          # Is this angry? Threatening? A payment issue? A bug?
      |
      v
Identify VIP status and contact history   # Is this a VIP? Is this their third contact on the same problem?
      |
      v
Check knowledge base for a match          # Does the KB cover this? If not, escalate. Do not guess.
      |
      v
Assign priority level and SLA             # P1 = 30 min. P5 = 72 hours. Based on issue + signals.
      |
      v
Decide escalation path                    # Billing? Technical? Trust & Safety? Legal? Senior agent?
      |
      v
Generate response strategy                # What tone. What to collect. What not to say.
      |
      v
Assemble prompt for Claude (if connected) # System prompt + knowledge base + strategy + player message
      |
      v
Human agent reviews triage result         # Before anything reaches the player
      |
      v
Interaction evaluated by QA system        # See ai-customer-support-qa
```

The triage logic is entirely rules-based and runs without an API key. Claude is only involved in drafting the player-facing response. Those are intentionally separate.

---

## Run modes

| Mode | Requires | Cost | What you get |
|---|---|---|---|
| Mock | Nothing | Free | Deterministic triage output with a pre-written response |
| LLM | `ANTHROPIC_API_KEY` in `.env` | API credits | Real Claude response grounded in the knowledge base |

```bash
# Mock mode (no API key needed)
python run_agent.py --demo

# LLM mode
python run_agent.py --message "I was charged but didn't receive my coins"
```

---

## Scope

Tier 1 player support only:

- Payment and purchase issues
- Account access and login problems
- Missing in-game items or currency
- Basic gameplay questions
- Technical issues: crashes, connectivity, platform-specific bugs
- VIP player handling and escalation

Not in scope at Tier 1: ban enforcement, fraud investigation, legal and GDPR responses, refund approvals.

---

## Current limitations

| Limitation | What this means in practice |
|---|---|
| No live account data access | The system reads the player's message. The account context layer uses mock data — a real backend integration point is defined but not yet wired. |
| Keyword-based intent detection | Unusual phrasing reduces accuracy. The semantic search layer partially compensates. |
| English-biased classifier | Intent signals use English keywords. Non-English input is translated at the response layer but classification remains English-first. |
| System prompt not red-teamed | Tested on representative cases, not adversarial volume. |
| No live metrics backend | QA scores and dashboards are file-based. Production deployment would require a proper metrics store. |

See [docs/risk/limitations.md](docs/risk/limitations.md) for the complete list.

---

## What I would do differently with a real team

- **Agent assist first, never automation first.** The AI suggests. A human approves. You earn the right to increase automation by proving quality at every stage.
- **Build the knowledge base from real tickets.** Synthetic examples are useful for prototyping. Real edge cases only come from actual support data.
- **Calibrate confidence thresholds against real volume.** A threshold set in a prototype is a guess. Set it by reviewing a sample of real tickets and measuring where the AI gets it wrong.
- **Sample every queue from day one.** Automated random sampling with a QA rubric, not manual selection. Manual selection introduces bias.
- **Track escalation rate as the primary health signal.** Too high means the AI is not helping. Too low means it is being overconfident. Either is a problem.
- **Train the team before rollout.** Agents need to understand what the AI is flagging, why it sometimes gets it wrong, and how to correct it. Without this, they will either over-trust it or ignore it.
- **Legal and compliance review before any live use.** Data processing agreements, AI-generated customer communication review, jurisdiction-specific requirements. Not optional.

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

## Evaluation

- Escalation accuracy (target: >90% correctly routed)
- Scope compliance (target: >95%)
- Evidence collection completeness
- Hallucination avoidance
- CSAT segmented by ticket complexity band

See [evaluation-criteria.md](evaluation-criteria.md) for metric definitions and [evaluation/failure-analysis.md](evaluation/failure-analysis.md) for known failure modes.

---

## Reporting issues

Use the issue templates in this repo:

- **Bug** - the engine does something it should not
- **KB gap** - the knowledge base is missing a scenario
- **Escalation misfire** - a ticket routed to the wrong team
- **Scope creep** - the system answered something it should have deflected
- **Feature request** - something new to add
- **Improvement** - something that works but could work better

---

## Author

**Alexandros Alexakis**
Vendor Manager and L&D Lead | Player Care
[LinkedIn](https://www.linkedin.com/in/alexandros-alexakis/)

---

## Status

Functional prototype. Triage engine with unit tests, semantic knowledge base, RAG retrieval, session memory, player account context, multilingual support across 5 languages, incident detection, automated QA scoring, coaching reports, training scenario generator, shift handover reports, team performance dashboard, evaluation pipeline, feedback loop, and Zendesk and Helpshift integrations.

See [docs/risk/productionization.md](docs/risk/productionization.md) for what a real deployment would require.
