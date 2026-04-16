# Failure Analysis

## Overview

This document catalogues known failure modes for the Tier 1 support assistant. Each failure mode is defined, its likely cause identified, its operational impact quantified, and a mitigation proposed.

This is not a theoretical exercise. Every failure mode here has a real-world analogue in support operations. Identifying them in advance is how you design a system that fails predictably rather than catastrophically.

---

## Failure Mode 1: Over-escalation

**Description:** The assistant escalates tickets that could and should be resolved at Tier 1. Simple mechanic questions, routine payment delivery delays, and basic troubleshooting cases get routed to specialist teams unnecessarily.

**Likely cause:**
- Overly conservative confidence threshold
- Keyword signal matches a high-priority intent when the context is benign (e.g. "my account is running slow" triggering account compromise signals)
- System prompt escalation rules are too broad

**Operational impact:**
- Increases specialist team workload with tickets they should not be handling
- Increases response time for players with straightforward issues
- Inflates escalation rate metric, making it unreliable as a signal
- Creates frustration if players are passed between teams unnecessarily

**Mitigation:**
- Define minimum evidence required before escalation for each issue type (see decision table)
- Introduce a pre-escalation check: has Tier 1 resolution been attempted?
- Review false positive escalation rate weekly and adjust classifier signals
- Test specifically for TC-019 class scenarios (false positive escalation risk)

---

## Failure Mode 2: Under-escalation

**Description:** The assistant attempts to resolve a ticket at Tier 1 when it should have been escalated. A legal threat is missed. A VIP player is not identified. A repeat contact is treated as a new ticket.

**Likely cause:**
- Hard escalation triggers not comprehensive enough
- Legal language phrased in a way the classifier does not recognise (e.g. "I'll speak to my solicitor" instead of "lawyer")
- VIP flag not passed correctly from the support platform
- Contact history not available or not checked

**Operational impact:**
- Legal risk if threats are not escalated to compliance
- Player loss if churn risk signals are missed
- Repeat contacts deepen player frustration if not recognised and prioritised
- Potential reputational damage if VIP players feel they received standard treatment

**Mitigation:**
- Expand legal threat signal dictionary to cover jurisdiction-specific terminology
- Make VIP status a required parameter in the pipeline - fail loudly if missing rather than defaulting to non-VIP
- Implement mandatory contact history check before any Tier 1 resolution attempt
- Test specifically for TC-004, TC-020, TC-005 scenarios

---

## Failure Mode 3: Hallucinated Policy

**Description:** The assistant states a policy, rule, or outcome that does not exist in the knowledge base. It invents a refund window, confirms that a ban will be lifted, or speculates on a TOS clause.

**Likely cause:**
- System prompt does not sufficiently prohibit speculation
- LLM fills knowledge gaps with plausible-sounding information rather than acknowledging uncertainty
- Knowledge base has gaps that create pressure on the model to infer

**Operational impact:**
- Players may cite assistant statements in disputes
- Creates implied commitments the business cannot or will not honour
- Undermines player trust when the stated policy turns out to be wrong
- Potential legal liability in consumer protection jurisdictions

**Mitigation:**
- System prompt explicitly prohibits inventing policy (see current system-prompt.md)
- Knowledge base gaps should result in escalation, not inference
- Regular adversarial testing: ask the assistant about policies not in the knowledge base and verify it escalates rather than guesses
- QA review should specifically check for policy statements against the knowledge base

---

## Failure Mode 4: Insufficient Evidence Gathering

**Description:** The assistant escalates a ticket without collecting the information the specialist team needs. The ticket bounces back. The player has to be contacted again.

**Likely cause:**
- Escalation decision made too quickly before information collection is complete
- Information collection rules not enforced for the specific issue type
- Player is hostile and the assistant de-prioritises collection to avoid conflict

**Operational impact:**
- Increases average handling time
- Specialist teams receive incomplete tickets they cannot action
- Player is contacted multiple times for the same information
- FCR metric suffers

**Mitigation:**
- Information collection requirements defined per issue type in decision table
- System prompt mandates collection before escalation except for hard escalation triggers
- Escalation format requires a checklist confirming required fields are populated
- Track incomplete escalation rate as a QA metric

---

## Failure Mode 5: Wrong Issue Classification

**Description:** The assistant classifies the issue incorrectly and follows the wrong handling path. A compromised account is handled as a standard login issue. A churn risk signal is treated as a bug report.

**Likely cause:**
- Keyword signals overlap between issue types
- Player describes issue in an unusual way that does not match any signal
- Confidence score is above threshold but classification is still wrong

**Operational impact:**
- Wrong information is collected
- Wrong team receives the escalation
- Resolution path is inappropriate for the actual issue
- Player frustration increases when handling is visibly wrong

**Mitigation:**
- Confidence threshold acts as a safety valve - low confidence routes to human
- Classification is logged at every step for audit
- Weekly review of misclassification cases from QA sampling
- Expand test suite with overlapping-signal cases

---

## Failure Mode 6: Over-questioning

**Description:** The assistant asks too many questions before taking any action. The player provides their issue, and the assistant responds with five clarifying questions before acknowledging the problem.

**Likely cause:**
- System prompt asks for too much information upfront
- Information collection rules not ordered by priority
- No constraint on number of questions per turn

**Operational impact:**
- Players abandon the interaction
- CSAT drops even when the issue is eventually resolved
- Interaction feels bureaucratic rather than helpful

**Mitigation:**
- System prompt mandates one question per turn when clarification is needed
- Information collection is ordered: ask for the most critical item first
- QA checklist includes unnecessary follow-up rate as a metric
- Test specifically for TC-008 and TC-021 scenarios

---

## Failure Mode 7: Premature Closure

**Description:** The assistant closes or marks a ticket as resolved before confirming the player's issue is actually resolved.

**Likely cause:**
- No mandatory confirmation step before closure
- Escalation is treated as resolution
- Player says "ok thanks" and the assistant interprets this as resolution

**Operational impact:**
- Player recontacts, increasing repeat contact rate
- FCR metric is artificially inflated
- Player frustration when they have to re-explain the issue

**Mitigation:**
- System prompt requires ending every interaction with a clear next step or confirmation question
- Escalation is not closure - the ticket remains open until the specialist team confirms resolution
- Player saying "ok" or "thanks" should not trigger automatic closure

---

## Failure Mode 8: Failure to Detect Incident Pattern

**Description:** Multiple players report the same issue in a short window. The assistant handles each ticket individually and never flags the pattern as a potential incident.

**Likely cause:**
- No cross-session signal aggregation
- Each ticket is processed in isolation
- No incident detection threshold defined

**Operational impact:**
- Incident response is delayed
- Players receive individual troubleshooting steps for a problem that requires a backend fix
- Support volume spikes while the root cause goes unaddressed
- Potential SLA breaches across many tickets simultaneously

**Mitigation:**
- Incident detection requires external aggregation (see roadmap - this is a known limitation)
- At Tier 1, agents are trained to manually flag when they see multiple identical reports
- Volume spike monitoring should be in place at the platform level
- Test case TC-025 and TC-006 specifically probe this failure mode

---

## Failure Mode 9: Emotional De-escalation Failure

**Description:** An angry or distressed player becomes more hostile during the interaction because the assistant's responses feel dismissive, robotic, or defensive.

**Likely cause:**
- Tone rules in the system prompt are followed technically but feel formulaic
- Standard troubleshooting steps are delivered without acknowledging the emotional context first
- Response is too long and structured when a short, human acknowledgment is needed

**Operational impact:**
- Escalation becomes necessary for tickets that could have been resolved at Tier 1
- Player sentiment worsens - CSAT is lower than it would have been with a human agent
- Negative reviews or public complaints are more likely

**Mitigation:**
- Tone instructions mandate acknowledgment before any troubleshooting
- QA specifically scores emotional de-escalation as a category
- Sample conversations include hostile player examples for style reference
- Common failure patterns document (qa/common-failure-patterns.md) covers this explicitly

---

## Failure Mode 10: Inconsistency Across Similar Cases

**Description:** Two players with identical issues receive different responses. One is told to wait 24-48 hours. Another is told the issue will be reviewed within the week. One receives an apology. Another receives a factual response with no acknowledgment.

**Likely cause:**
- LLM response generation is non-deterministic
- System prompt rules are not specific enough to constrain variation
- Knowledge base is ambiguous on specific policy points

**Operational impact:**
- Players compare responses (especially in community forums) and lose trust when they see discrepancies
- Creates implied policy differences that do not exist
- Undermines the entire purpose of a standardised support system

**Mitigation:**
- Timeframe commitments should come from the decision table, not the LLM
- System prompt provides exact language for escalation acknowledgments
- Consistency testing: run identical inputs multiple times and compare outputs
- QA calibration sessions specifically check for consistency across similar ticket types
