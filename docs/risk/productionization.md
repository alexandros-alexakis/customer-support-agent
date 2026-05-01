# Productionization Roadmap

What is required to turn this prototype into a real deployed AI support system, organized by phase.

---

## Phase 1: Local Prototype (current state)

Rules-based triage engine, semantic KB with ChromaDB, system prompt, gap tracking, feedback loop, Zendesk webhook code, evaluation pipeline, 30-case test suite, multilingual support.

Limitations: no live LLM response loop, no real account data, no production infrastructure, synthetic data only.

---

## Phase 2: Internal Demo

Goal: show the system working end-to-end in a controlled environment.

Required: live LLM response loop, demo support platform (test Zendesk), logging infrastructure, VIP test data, human review workflow for AI triage decisions.

Estimated effort: 2-4 weeks for a small technical team.

---

## Phase 3: Controlled Pilot

Goal: run on a small slice of real traffic with full human oversight.

Required: real account data API, persistent case tracking, CSAT measurement, webhook authentication, rate limiting, rollback plan, real KB content, multilingual KB.

Estimated effort: 6-10 weeks including backend integration.

---

## Phase 4: Production Hardening

Goal: system is reliable enough for unsupervised Tier 1 handling.

Required: red-teaming, incident detection layer, live KB sync, model version pinning, audit trail, alerting (escalation rate spike, confidence drop, webhook errors), SLA tracking, QA automation.

Estimated effort: 8-16 weeks.

---

## Phase 5: Live Deployment

Goal: handles Tier 1 independently within defined scope, human escalation for everything else.

Required: agent assist mode first, performance baseline established, complexity-controlled CSAT, compliance review, data retention policy, vendor agreements, gradual rollout starting at 5-10% of volume.

Estimated effort: 12-20 weeks including compliance and legal review.

---

## Technology decisions for production

| Component | Prototype | Production recommendation |
|---|---|---|
| Vector store | ChromaDB local | Pinecone, Weaviate, or pgvector |
| Logging | stdout JSON | Datadog, CloudWatch, or ELK |
| Database | Local JSON files | PostgreSQL or equivalent |
| Deployment | Local | Kubernetes or ECS with auto-scaling |
| LLM provider | Anthropic Claude | Same, with model version pinning |
| Secrets | .env file | AWS Secrets Manager or Vault |
