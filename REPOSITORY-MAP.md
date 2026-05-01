# Repository Map

Every file and folder in the repository, what it does, and where to find things.

---

## Root level - start here

| File | What it is |
|---|---|
| `README.md` | Project overview, what it is and is not, architecture summary, status |
| `QUICKSTART.md` | Go from clone to first run in 5 minutes |
| `SETUP.md` | Full installation guide with venv, dependencies, validation steps |
| `ARCHITECTURE.md` | How components connect, what is rule-based vs model-based, component map |
| `HOW-IT-WORKS.md` | Operational explanation of every decision the system makes |
| `CONFIGURATION.md` | All environment variables, provider config, logging config |
| `TROUBLESHOOTING.md` | Symptom, cause, resolution for every common failure |
| `LIMITATIONS.md` | What the system cannot do, what is prototype-only, what is mocked |
| `PRODUCTIONIZATION.md` | 5-phase roadmap from prototype to live deployment |
| `GETTING_STARTED.md` | All runnable commands with expected output |
| `CONTRIBUTING.md` | How to adapt this for your own company, how to contribute |
| `EXTENDING.md` | How to safely add issue types, escalation rules, KB content, tests |
| `REPOSITORY-MAP.md` | This file |
| `VALIDATION-CHECKLIST.md` | Checklist to confirm setup is working correctly |
| `CHANGELOG.md` | Version history |
| `roadmap.md` | Planned improvements |
| `docs/operations/interaction-flow.md` | Step-by-step decision flow for any ticket |
| `evaluation-criteria.md` | How performance is measured, metrics with assessment methods |
| `system-prompt.md` | The LLM behavior contract: scope, rules, prohibited actions |
| `docs/operations/tone-guide.md` | Communication standards with good/bad examples |
| `agent-limitations.md` | What the AI agent can and cannot do |
| `agent-versioning.md` | How to track and roll back prompt and KB changes |
| `prompt-engineering-notes.md` | Design decisions behind the system prompt |
| `example_run.py` | Runnable demo: 4 tickets through the triage engine |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `.gitignore` | What is excluded from version control |

---

## `engine/` - The triage engine

All rule-based, deterministic Python. No LLM calls.

| File | What it does |
|---|---|
| `engine/__init__.py` | Package marker |
| `engine/classifier.py` | Intent detection, tone detection, confidence scoring, flag generation |
| `engine/prioritizer.py` | P1-P5 priority scoring and SLA assignment |
| `engine/escalation.py` | Escalation decisions, hard/soft triggers, team routing |
| `engine/response_router.py` | Response strategy: tone instruction, what to collect, what action to take |
| `engine/pipeline.py` | Orchestrates all four steps, structured logging at each stage |
| `engine/logging_config.py` | Configures structured JSON logging |
| `engine/metrics_spec.py` | Documents what should be measured in production and why |

---

## `rag/` - Semantic knowledge base retrieval

| File | What it does |
|---|---|
| `rag/kb_sync.py` | Reads KB markdown files, chunks by section, loads into ChromaDB |
| `rag/retriever.py` | Queries ChromaDB for semantically relevant chunks given a player message |
| `rag/example_rag.py` | Runnable demo showing retrieval on standard and non-standard phrasing |
| `rag/README.md` | RAG design decisions, why ChromaDB, limitations |
| `rag/chroma_store/` | Generated at runtime by `kb_sync.py`. Not committed. |

---

## `feedback/` - Gap tracking and correction loop

| File | What it does |
|---|---|
| `feedback/gap_tracker.py` | Records low-confidence tickets. Reviewed weekly to find KB gaps. |
| `feedback/feedback_store.py` | Records QA corrections with priority. Drives KB and prompt updates. |
| `feedback/README.md` | How gap tracking and feedback loop work, review process |
| `feedback/gaps.json` | Generated at runtime. Not committed. |
| `feedback/feedback.json` | Generated at runtime. Not committed. |

---

## `multilingual/` - Language detection and response

| File | What it does |
|---|---|
| `multilingual/language_handler.py` | Detects player language, adapts system prompt, generates response in player language |
| `multilingual/example_multilingual.py` | Runnable demo with Spanish, French, Turkish, Portuguese |
| `multilingual/README.md` | How multilingual works, supported languages, limitations |

---

## `integrations/` - Platform connectors

| File | What it does |
|---|---|
| `integrations/__init__.py` | Package marker |
| `integrations/zendesk_webhook.py` | Flask webhook server: receives Zendesk events, runs pipeline, updates ticket |
| `integrations/zendesk_client.py` | Zendesk API calls: fetch ticket, fetch user, get contact count, update ticket |
| `integrations/zendesk-integration-guide.md` | Complete 10-part Zendesk setup guide |

---

## `evaluation/` - Testing and evaluation

| File | What it does |
|---|---|
| `evaluation/test-cases.md` | 30 test scenarios: straightforward, ambiguous, hostile, edge cases |
| `evaluation/failure-analysis.md` | 10 failure modes with causes, impacts, mitigations |
| `evaluation/scripts/fetch_tickets.py` | Generates 200 synthetic support tickets |
| `evaluation/scripts/evaluate_tickets.py` | Runs tickets through the engine, compares expected vs actual |
| `evaluation/scripts/generate_report.py` | Produces markdown report: accuracy, false negatives, false positives |
| `evaluation/data/` | Generated by evaluation pipeline. Not committed. |

---

## `tests/` - Unit tests

| File | What it tests |
|---|---|
| `tests/test_classifier.py` | Intent classification, tone detection, escalation flags, confidence threshold |
| `tests/test_prioritizer.py` | Priority scoring for critical intents, hostile tones, VIP, repeat contacts |

---

## `knowledge-base/` - Policy and FAQ documents

| File | Coverage |
|---|---|
| `faq-payments.md` | Payment issues, missing purchases, duplicate charges |
| `faq-account-access.md` | Login failures, password reset, guest accounts |
| `faq-game-mechanics.md` | In-game feature questions |
| `faq-technical-issues.md` | Crashes, connectivity, device issues |
| `escalation-rules.md` | When and how to escalate |
| `decision-table.md` | Structured decision logic for all 15 issue types |
| `vip-player-handling.md` | Differentiated handling for high-value players |
| `seasonal-events-guide.md` | Event-related ticket spikes |
| `refund-policy-detail.md` | Refund decision tree and platform-specific notes |
| `banned-account-faq.md` | Ban and suspension handling |
| `gdpr-requests.md` | GDPR data access, deletion, and privacy requests |
| `tos-violations-guide.md` | TOS agent handling: quote directly or escalate |
| `edge-cases.md` | 11 realistic difficult scenarios with correct handling |

---

## `operations/` - Operational templates

| File | What it is |
|---|---|
| `shift-handover-template.md` | End-of-shift handover structure |
| `incident-response-playbook.md` | P1-P5 incident response steps |
| `capacity-planning-guide.md` | Staffing forecasting methodology |
| `weekly-reporting-template.md` | Weekly KPI report for management |
| `agent-performance-review-template.md` | Monthly/quarterly agent review |

---

## `qa/` - Quality assurance framework

| File | What it is |
|---|---|
| `qa-framework.md` | 100-point scoring system across 5 categories |
| `calibration-guide.md` | How QA reviewers align on scoring standards |
| `coaching-template.md` | Post-QA feedback session structure |
| `common-failure-patterns.md` | Most frequent agent mistakes and corrections |
| `ai-csat-bias-analysis.md` | Why aggregate AI vs human CSAT comparisons are misleading |

---

## `onboarding/` - Agent training

| File | What it is |
|---|---|
| `agent-training-guide.md` | Week-by-week onboarding plan |
| `new-agent-checklist.md` | Day 1 through month 1 milestones |
| `certification-criteria.md` | What qualifies an agent as fully trained |
| `qa-scorecard.md` | Per-ticket QA evaluation form |

---

## `sample-conversations/` - Style examples

Illustrative interaction examples showing correct tone and structure. These are **not test evidence**. They demonstrate style, not validated behavior.

| File | Scenario |
|---|---|
| `payment-issue-example.md` | Standard payment handled ticket |
| `escalation-example.md` | Immediate escalation |
| `angry-player-example.md` | De-escalation |
| `vip-complaint-example.md` | VIP player handling |
| `technical-issue-example.md` | Device and crash troubleshooting |
| `repeat-contact-example.md` | Second contact handling |
| `fraud-suspicion-example.md` | Player reporting suspected cheating |
| `language-barrier-example.md` | Non-native English speaker |
