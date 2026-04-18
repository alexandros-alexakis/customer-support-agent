# Risk Register: Gaming-Specific AI Support Risks

Known risks specific to deploying an AI support agent in a gaming player care environment. Each entry includes the risk, why it is specific to gaming, the likelihood, the impact, and the mitigation.

---

## R01: Players learn to phrase messages to avoid escalation

**Risk:** Players in gaming communities share information quickly. If players discover that certain phrasings result in faster resolutions or compensation, they will use them. The AI's confidence in a given classification can be gamed by anyone who knows the keyword signals.

**Why gaming-specific:** Gaming communities are organised and communicative. Reddit threads, Discord servers, and content creators mean that information about support behaviours spreads faster than in most industries.

**Likelihood:** Medium. Requires motivated players and a pattern to exploit.
**Impact:** Medium. Increases misclassification rate and unjustified compensation claims.

**Mitigation:**
- Rotate and expand keyword signals periodically
- Use semantic search (RAG) as a complement to keyword matching
- Require verification before compensation, not just classification
- Monitor for unusual spikes in specific intent classifications

---

## R02: AI gives wrong refund or policy information with confidence

**Risk:** The AI generates a plausible-sounding answer to a refund or policy question that contradicts current policy. The player acts on it. The agent then has to walk it back.

**Why gaming-specific:** Refund policies, in-game currency rules, and platform-specific purchase terms are complex and change frequently. Gaming companies often have different policies per platform (iOS vs Android vs direct) which creates contradiction risk.

**Likelihood:** Medium without mitigation. Low with KB confidence thresholds enforced.
**Impact:** High. Creates false expectations, damages trust, and generates additional contact.

**Mitigation:**
- Enforce RAG similarity threshold: if KB match is below 0.70, escalate rather than answer
- Keep refund policy KB entries current and reviewed after every policy change
- System prompt explicitly prohibits speculating on policy
- QA rubric includes accuracy as a scored dimension

---

## R03: VIP misidentification

**Risk:** A high-value player is not flagged as VIP, receives standard handling, and churns. Or a standard player is incorrectly flagged as VIP and receives elevated handling that sets an expectation that cannot be sustained.

**Why gaming-specific:** VIP status in gaming is often tied to in-game spend which fluctuates, and whales can represent a disproportionate share of revenue. A single VIP churn event can have outsized financial impact.

**Likelihood:** Low if VIP tier configuration is maintained. Medium if spend thresholds are not updated.
**Impact:** High for false negatives (missed VIP). Low for false positives.

**Mitigation:**
- Use VIP tier definitions with configurable spend thresholds (see [vip-tiers.md](vip-tiers.md))
- Allow manual VIP override in the support platform
- Review tier thresholds quarterly against current revenue distribution
- Alert when a player near VIP threshold contacts support

---

## R04: False positive on legal threat detection triggers unnecessary escalation

**Risk:** A player uses legal-sounding language casually ("I'm going to sue" as an expression of frustration, not a genuine legal threat) and the system escalates to legal compliance unnecessarily.

**Why gaming-specific:** Hyperbolic language is common in gaming culture. Players express frustration more dramatically than in other support contexts.

**Likelihood:** Medium. Legal-sounding language is not rare in gaming support queues.
**Impact:** Low operationally, but legal compliance resources are finite.

**Mitigation:**
- Over-escalation is safer than under-escalation for legal signals. Accept the false positives.
- Train agents to distinguish genuine legal threats from frustrated hyperbole in their review
- Track false positive rate and tune signals if it becomes operationally disruptive

---

## R05: AI confidently handles an account compromise that it should not touch

**Risk:** A player reporting account compromise receives an automated response that discloses account information or takes an action before identity is verified. If the person contacting is the attacker, this makes the situation worse.

**Why gaming-specific:** Account theft is common in gaming, particularly for accounts with rare items, high competitive rank, or significant spend history. Accounts are traded and sold on third-party markets.

**Likelihood:** Low if hard escalation triggers are correctly configured.
**Impact:** Critical. Account data disclosure to an attacker is a security incident.

**Mitigation:**
- Account compromise is a hard escalation trigger. No automated handling under any circumstances.
- System prompt explicitly prohibits disclosing any account information in response to compromise reports
- Identity verification through secure channel is mandatory before any account action
- This risk should be in every agent training session

---

## R06: Incident not detected, queue overwhelmed before ops responds

**Risk:** A widespread bug causes hundreds of players to contact support simultaneously. The triage engine processes each ticket as an individual complaint. No alert fires. The queue is overwhelmed before ops is aware there is an incident.

**Why gaming-specific:** Game updates, server outages, and competitive events create sudden volume spikes that are unique to gaming environments.

**Likelihood:** Medium without incident detection. Low with monitoring in place.
**Impact:** High. Overwhelmed queue, player frustration, CSAT damage.

**Mitigation:**
- Implement incident detection layer (see [incident-detection.md](incident-detection.md))
- Lower detection thresholds during high-risk windows (see [seasonal-risk-guide.md](seasonal-risk-guide.md))
- Have a known issue template ready to fill in immediately when an incident is confirmed
- Pre-plan communication for common incident types

---

## R07: KB degrades over time without anyone noticing

**Risk:** The KB is accurate at launch but gradually becomes outdated as game features, policies, and escalation paths change. The AI continues to answer questions with stale information. Agents start noticing but do not have a formal way to flag it.

**Likelihood:** High without ownership and a maintenance process.
**Impact:** Medium. Gradual CSAT decline, increasing escalation rate on topics the AI should handle.

**Mitigation:**
- Assign a named KB owner before go-live (see [docs/learning-loop/kb-maintenance.md](../learning-loop/kb-maintenance.md))
- Scheduled monthly review
- Event-triggered reviews for updates and policy changes
- Monitor escalation rate by intent type as an early signal of KB degradation
