# Productionization Roadmap

What is required to turn this prototype into a real deployed AI support system, organized by phase.

---

## Phase 1: Local Prototype (current state)

**What exists:**
- Rules-based triage engine with intent, tone, priority, and escalation logic
- Semantic knowledge base with ChromaDB and sentence-transformers
- System prompt defining LLM behavior
- Gap tracking and feedback loop (local JSON files)
- Zendesk webhook server (code complete, requires your own Zendesk account)
- Evaluation pipeline with synthetic tickets
- 30-case test suite
- Multilingual support via Claude API

**Limitations at this phase:**
- No live LLM response loop
- No real account data
- No production infrastructure
- Synthetic data only

---

## Phase 2: Internal Demo

**Goal:** Show the system working end-to-end in a controlled environment.

**Required additions:**

| Item | Detail |
|---|---|
| Live LLM response loop | Wire `rag/retriever.py` + `engine/pipeline.py` output into a Claude API call that generates the player-facing response |
| Demo support platform | Connect to a test Zendesk instance with real (internal) test tickets |
| Logging infrastructure | Redirect structured logs to a searchable store (e.g. Datadog, CloudWatch, or even a local ELK stack) |
| VIP test data | Create internal test accounts tagged as VIP to validate VIP handling |
| Human review workflow | Define how a human reviews and overrides AI triage decisions |

**Estimated effort:** 2-4 weeks for a small technical team.

---

## Phase 3: Controlled Pilot

**Goal:** Run on a small slice of real traffic with full human oversight.

**Required additions:**

| Item | Detail |
|---|---|
| Real account data API | Integration with game backend to verify purchases, account status, and contact history |
| Persistent case tracking | Database to store triage decisions, escalation history, and outcomes per ticket |
| CSAT measurement | Post-interaction survey connected to ticket platform, segmented by complexity band |
| Authentication | Webhook endpoint protected beyond HMAC signature (IP allowlist or mTLS) |
| Rate limiting | Protect the webhook server from request floods |
| Rollback plan | Ability to disable the AI layer instantly and revert to 100% human handling |
| Real KB content | Replace fictional knowledge base with actual company policies |
| Multilingual KB | Translate or author KB content in top player languages |

**Estimated effort:** 6-10 weeks including backend integration.

---

## Phase 4: Production Hardening

**Goal:** System is reliable enough for unsupervised Tier 1 handling.

**Required additions:**

| Item | Detail |
|---|---|
| Red-teaming | Systematic adversarial testing of the system prompt for injection, policy bypass, and edge cases |
| Incident detection layer | Cross-session aggregation to detect volume spikes indicating a widespread issue |
| Live KB sync | Automatic re-indexing when KB files are updated, without manual intervention |
| Model version pinning | Lock to a specific Claude model version. Define a process for testing and approving model updates |
| Audit trail | Persistent, tamper-evident log of every triage decision and LLM response |
| Alerting | Automated alerts for: escalation rate spike, unknown intent rate spike, confidence drop, webhook errors |
| SLA tracking | Automated monitoring that tickets are picked up within their SLA window |
| QA automation | Automated sampling of interactions for QA review, replacing manual selection |

**Estimated effort:** 8-16 weeks.

---

## Phase 5: Live Deployment

**Goal:** System handles Tier 1 independently within defined scope, with human escalation for everything else.

**Required additions:**

| Item | Detail |
|---|---|
| Agent assist mode | AI runs in parallel with human agents, suggesting responses rather than sending autonomously, before full autonomy is granted |
| Performance baseline | Establish human Tier 1 CSAT and FCR baselines before AI deployment for fair comparison |
| Complexity-controlled CSAT | CSAT segmented by ticket complexity band (see `qa/ai-csat-bias-analysis.md`) to prevent misleading comparisons |
| Compliance review | Legal review of AI-generated customer communication in all operating jurisdictions |
| Data retention policy | Define how long ticket data, triage logs, and LLM inputs/outputs are stored |
| Vendor agreements | Confirm data processing agreements with Anthropic and any other providers |
| Gradual rollout | Start at 5-10% of ticket volume. Increase only after CSAT and FCR targets are met at each level |

**Estimated effort:** 12-20 weeks including compliance and legal review.

---

## Technology decisions for production

| Component | Prototype | Production recommendation |
|---|---|---|
| Vector store | ChromaDB (local) | Pinecone, Weaviate, or pgvector on managed Postgres |
| Embeddings | sentence-transformers local | Same model or fine-tuned variant, served via API |
| Logging | stdout JSON | Datadog, CloudWatch, or ELK |
| Database | Local JSON files | PostgreSQL or equivalent |
| Deployment | Local / Railway | Kubernetes, ECS, or equivalent with auto-scaling |
| LLM provider | Anthropic Claude | Same, with model version pinning and fallback |
| Monitoring | None | Datadog APM or equivalent |
| Secrets management | .env file | AWS Secrets Manager, Vault, or equivalent |
