# Interaction Flow

## Overview

This document defines the decision flow the assistant follows for every ticket. This is not code. It is the operational logic that the system prompt enforces and the engine implements.

Anyone reviewing this project should be able to trace any interaction through this flow and identify where a failure occurred.

---

## Flow

```
START
  |
  v
1. RECEIVE MESSAGE
   Read the player's message.
   Note: contact count, VIP status, prior history (if passed in).

  |
  v
2. CHECK IMMEDIATE ESCALATION CONDITIONS
   Before anything else, check:

   - Legal threat detected?          -> Escalate to Legal/Compliance immediately
   - Ban or suspension mentioned?    -> Escalate to Trust and Safety immediately
   - Fraud or cheating report?       -> Escalate to Trust and Safety immediately
   - Third or more contact?          -> Escalate to Senior Agent immediately
   - VIP player confirmed?           -> Flag VIP, continue with elevated priority
   - GDPR / privacy request?         -> Escalate to Legal/Compliance immediately
   - Compromised account signals?    -> Escalate to Security immediately
   - Threatening behaviour?          -> Escalate to Senior Agent immediately

   IF any of the above: go to ESCALATE (step 6)
   IF none: continue to step 3

  |
  v
3. CLASSIFY ISSUE TYPE
   Identify the primary issue from the message.

   Possible classifications:
   - Payment issue
   - Missing purchase
   - Account access
   - Bug report
   - Technical issue
   - Game mechanic question
   - Refund request
   - Harassment report
   - Unclear / mixed

   IF classification confidence is low (< 0.65):
     Ask ONE clarifying question.
     IF still unclear after response: go to ESCALATE

  |
  v
4. COLLECT MINIMUM REQUIRED INFORMATION
   Refer to the decision table for required fields by issue type.

   Rules:
   - Ask for one piece of information at a time.
   - Do not ask for information you do not need.
   - If player refuses to provide required information, note this and continue.
   - If player provides contradictory information, collect both versions without challenging.

  |
  v
5. ATTEMPT TIER 1 RESOLUTION (if allowed)
   Check the decision table: is this issue type allowed at Tier 1?

   IF yes:
     Follow the defined troubleshooting steps.
     IF issue resolved: confirm with player and close.
     IF issue unresolved after Tier 1 steps: go to ESCALATE

   IF no (issue is out of Tier 1 scope):
     Go to ESCALATE

  |
  v
6. ESCALATE
   Determine the correct escalation target from the decision table.

   Before escalating, compile the handoff note:

   - Issue type
   - Facts provided by player (labelled as: player states...)
   - Steps already attempted
   - Reason for escalation
   - Priority level
   - Flags: VIP / repeat contact / legal threat / incident signal / contradictory info

   Inform the player:
   - That their case is being escalated
   - Which team is handling it (generic description, not staff names)
   - Realistic timeframe (from decision table SLA)
   - Do NOT promise an outcome

  |
  v
7. CLOSE OR HAND OFF
   IF resolved at Tier 1:
     Confirm resolution with player.
     Ask if there is anything else.
     Close only after player confirms or does not respond.

   IF escalated:
     Ticket remains open.
     Human agent or specialist team takes ownership.
     Do not close on the AI side.

END
```

---

## Notes on This Flow

**Step 2 runs before everything else.** Hard escalation triggers are not a fallback - they are the first check. An angry player with a legal threat does not go through troubleshooting first.

**Uncertainty defaults to escalation, not guessing.** If the issue type cannot be determined after one clarifying question, escalate. Do not attempt resolution on an unknown classification.

**Collection happens before resolution.** Evidence is gathered before any troubleshooting step. Escalating without evidence is a failure (see failure-analysis.md, Failure Mode 4).

**Tier 1 resolution is time-boxed.** If standard steps do not resolve the issue, escalate. Do not keep troubleshooting indefinitely.

**Escalation is not closure.** A ticket is open until the player's issue is resolved, not just until it is handed off.
