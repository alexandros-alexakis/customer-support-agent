# Interaction Flow

The decision flow the assistant follows for every ticket. This is the operational logic that the system prompt enforces and the engine implements.

---

## Flow

```
START
  |
  v
1. RECEIVE MESSAGE
   Read the player message. Note contact count, VIP status, prior history.

  |
  v
2. CHECK IMMEDIATE ESCALATION CONDITIONS
   Legal threat -> Legal/Compliance immediately
   Ban or suspension mentioned -> Trust and Safety immediately
   Fraud or cheating report -> Trust and Safety immediately
   Third or more contact -> Senior Agent immediately
   VIP player confirmed -> Flag VIP, continue with elevated priority
   GDPR / privacy request -> Legal/Compliance immediately
   Compromised account signals -> Security immediately
   Threatening behaviour -> Senior Agent immediately

   IF any of the above: go to ESCALATE (step 6)
   IF none: continue to step 3

  |
  v
3. CLASSIFY ISSUE TYPE
   IF confidence < 0.65: ask ONE clarifying question.
   IF still unclear: go to ESCALATE

  |
  v
4. COLLECT MINIMUM REQUIRED INFORMATION
   Ask for one piece of information at a time.
   Do not ask for what you do not need.
   If player provides contradictory information, collect both versions without challenging.

  |
  v
5. ATTEMPT TIER 1 RESOLUTION (if in scope)
   IF issue resolved: confirm and close.
   IF unresolved after Tier 1 steps: go to ESCALATE
   IF out of scope: go to ESCALATE

  |
  v
6. ESCALATE
   Compile handoff note. Inform player of escalation, team, and timeframe.
   Do NOT promise an outcome.

  |
  v
7. CLOSE OR HAND OFF
   IF resolved at Tier 1: confirm with player, ask if anything else, close.
   IF escalated: ticket stays open. Human agent takes ownership.

END
```

---

## Key rules

Step 2 runs before everything else. Hard triggers are not a fallback.

Uncertainty defaults to escalation, not guessing.

Evidence collection happens before resolution attempts.

Tier 1 resolution is time-boxed. Do not keep troubleshooting indefinitely.

Escalation is not closure. A ticket is open until the issue is resolved.
