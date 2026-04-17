# Case Studies — Support Operational Walkthroughs

This document walks through eight realistic player support scenarios. Each one shows how the system handles the case and, more importantly, the operational reasoning behind every decision.

This is not documentation of code. It is documentation of how a senior support professional thinks through escalation, priority, tone, and agent guidance — and how that thinking is encoded into a system.

---

## How to read these case studies

Each case shows:

- **The player message** — as received, before any human reads it
- **What the system detects** — urgency, tone, intent, flags
- **Priority and SLA** — how urgent this is and what the response window is
- **Where it goes** — which team, and why
- **What the agent is told** — tone guidance, what to collect, what not to say
- **Operational reasoning** — the support logic behind the decision, explained plainly

---

## Case 1: "You charged me but nothing arrived"

**Player message:**
> "I was charged £9.99 for coins but they never appeared in my account. Transaction ID: TXN-884521"

**What the system detects:**
- Issue type: payment problem with failed delivery
- Urgency signals: confirmed charge, specific transaction ID provided
- Tone: neutral — frustrated but not aggressive
- Flags: none

**Priority and SLA:**
- P3 — High
- 8-hour response window

**Where it goes:**
- Billing team
- Reason: a confirmed charge with a transaction ID is a financial dispute. Tier 1 cannot verify or reverse this. It goes to billing immediately.

**What the agent is told:**
- Collect: Player ID, transaction ID, purchase date and amount, platform (iOS / Android / web)
- Tone: professional, efficient — the player has already done the work of providing the transaction ID. Acknowledge that and move.
- Do not: suggest the refund will happen before verification. Do not ask for information the player has already given.

**Operational reasoning:**
This is one of the highest-volume, highest-sensitivity ticket types in gaming support. The player is owed money or items — that is not a question. The question is verification. Getting this wrong in either direction — promising too much, or appearing to dismiss it — damages trust. The right move is a fast, professional acknowledgement that confirms the right team is on it.

---

## Case 2: "All my progress is gone after the update"

**Player message:**
> "I logged in this morning and everything from the last two weeks is gone. My level, my items, my purchases. It happened right after yesterday's update."

**What the system detects:**
- Issue type: lost progress, possible data corruption or failed sync
- Urgency signals: recent update as a trigger, scope of loss is significant
- Tone: distressed — not angry yet, but upset
- Flags: possible wider incident if other players report the same

**Priority and SLA:**
- P3 — High
- 8-hour response window

**Where it goes:**
- Technical support
- Reason: progress loss tied to an update is a technical investigation, not an agent-resolvable issue. If multiple players report the same thing, this becomes an incident.

**What the agent is told:**
- Collect: Player ID, platform, game version, last login before the issue, whether cloud save is enabled
- Tone: empathetic and specific — acknowledge what was lost, not just that "something went wrong"
- Do not: promise data recovery. Recovery may not be possible. Raising that expectation and then failing it is worse than not raising it.

**Operational reasoning:**
Lost progress is emotionally significant. Players invest real time and often real money into their accounts. A response that treats this as routine will increase frustration. The agent's job in the first contact is to validate the experience, gather what is needed, and give an honest expectation of what comes next — not to fix it in one interaction.

---

## Case 3: VIP player threatening to quit

**Player message:**
> "I'm done. Uninstalling right now. I've spent a lot of money on this game and this is the thanks I get."

**What the system detects:**
- Issue type: churn risk — intent to leave
- Urgency signals: VIP flag active, frustration about money spent, no specific issue stated
- Tone: angry, resigned
- Flags: VIP player, churn risk

**Priority and SLA:**
- P1 — Critical
- 30-minute response window

**Where it goes:**
- Player relations
- Reason: VIP churn is a revenue and relationship event. A templated first-contact response makes this worse. This needs a personalised, senior-voice response from someone who has the player's account history in front of them.

**What the agent is told:**
- Before responding: review the player's recent support history and purchase history. Understand what has happened before the first word is written.
- Tone: personalised, warm, not defensive
- Do not: send a template. Do not respond without knowing the account context. Do not treat this as a standard complaint.

**Operational reasoning:**
When a high-value player expresses intent to leave, the underlying issue is rarely stated clearly in the message. Something built up over time. The agent's job is to find out what it was and address it — not to respond to the surface-level message. The 30-minute SLA is not about speed for its own sake. It is about catching the player before the decision solidifies.

---

## Case 4: "I'll do a chargeback if this isn't fixed"

**Player message:**
> "I've been waiting four days for a response about my missing items. If I don't hear back today I'm disputing the charge with my bank."

**What the system detects:**
- Issue type: unresolved payment issue with chargeback threat
- Urgency signals: four-day wait, financial threat, no prior resolution
- Tone: threatening
- Flags: chargeback threat, repeat contact on unresolved issue

**Priority and SLA:**
- P1 — Critical
- 1-hour response window

**Where it goes:**
- Billing team + senior agent flag
- Reason: a chargeback threat is a financial and reputational risk. If the chargeback proceeds, it costs the business more than the original transaction. This needs resolution, not a holding response.

**What the agent is told:**
- Collect: original ticket reference, transaction ID if not already held, platform
- Tone: calm, direct, solution-focused — the player is frustrated by a wait, not by the original issue alone. Acknowledge the wait explicitly.
- Do not: lecture the player about chargeback policy. Do not make them feel like a threat. Find the original issue and resolve it.

**Operational reasoning:**
Chargebacks are expensive and avoidable in most cases. When a player threatens one, they have usually already tried to resolve the issue through normal channels and been failed. The escalation here is not because the player is difficult — it is because the system previously failed them. The agent needs to own that and move fast.

---

## Case 5: "This is the third time I've contacted you" — legal threat

**Player message:**
> "This is the THIRD time. I am done being ignored. If my account is not restored by tomorrow I am contacting my solicitor."

**What the system detects:**
- Issue type: unresolved account issue, repeat contact
- Urgency signals: third contact, legal threat, prior resolution failure
- Tone: threatening
- Flags: legal threat, repeat contact, prior resolution failed

**Priority and SLA:**
- P1 — Critical
- 30-minute response window

**Where it goes:**
- Legal compliance team
- Secondary: senior agent for account investigation
- Reason: a legal threat overrides all other routing. The response must be reviewed before it goes out.

**What the agent is told:**
- Tone: formal, calm, no engagement with the legal threat at all
- Opening: acknowledge the number of contacts directly. Do not open with a generic greeting.
- Do not: mention the legal threat. Do not discuss what legal action would or would not achieve. Do not make commitments. Inform the player their case has been escalated and they will receive a formal response.
- Collect: nothing in this response. That happens in the investigation.

**Operational reasoning:**
When a player mentions legal action, the job of the first response changes. It is no longer about resolving the issue — it is about not making the situation worse. Anything said here may be quoted. The response needs to be short, professional, and focused only on confirming escalation. The investigation happens in parallel, not in the reply thread.

---

## Case 6: "My account was hacked"

**Player message:**
> "Someone has accessed my account. There are purchases I did not make and my email address has been changed to one I don't recognise."

**What the system detects:**
- Issue type: account compromise — unauthorised access and purchases
- Urgency signals: email changed by third party, unauthorised transactions
- Tone: urgent, alarmed
- Flags: security flag, requires immediate human review

**Priority and SLA:**
- P1 — Critical
- 1-hour response window

**Where it goes:**
- Trust & Safety
- Reason: this is a security incident. Account actions, information disclosure, and any recovery steps must go through identity verification — not a Tier 1 chat exchange.

**What the agent is told:**
- Tone: calm and reassuring — the player is alarmed
- Action: direct the player to the secure account recovery flow. Do not attempt to process this in chat.
- Do not: ask for passwords, payment details, or personal identification in chat. Do not confirm or deny any account information to the person contacting — you cannot verify their identity yet. Do not take any account actions until identity is confirmed.

**Operational reasoning:**
Account compromise cases carry real risk in both directions. If the person contacting is the legitimate account holder, they need fast, calm help. If the person contacting is the attacker, any information disclosed makes the situation worse. The first response must do both: reassure and redirect without revealing anything. Identity verification through a secure channel is non-negotiable before anything else happens.

---

## Case 7: "My ban was unfair" — ban appeal

**Player message:**
> "My account was banned but I didn't do anything wrong. I've spent hundreds of pounds on this game. I want this reviewed immediately."

**What the system detects:**
- Issue type: ban appeal
- Urgency signals: financial investment mentioned, demand for immediate review
- Tone: indignant
- Flags: ban appeal — out of scope for Tier 1

**Priority and SLA:**
- P2 — Urgent
- 4-hour response window

**Where it goes:**
- Trust & Safety — ban review team
- Reason: ban appeals require access to account history, moderation logs, and enforcement policy. Tier 1 agents cannot and should not make decisions about enforcement.

**What the agent is told:**
- Tone: professional, neutral — not sympathetic in a way that implies the ban was wrong before it has been reviewed
- Action: acknowledge the appeal, confirm it has been escalated to the review team, provide a realistic timeframe
- Do not: comment on whether the ban seems fair. Do not ask the player to explain what they did. Do not imply the ban will be overturned. Do not let the mention of money spent influence the tone.

**Operational reasoning:**
Ban appeals are sensitive because both outcomes are possible — the ban may have been correct, or it may have been a false positive. The first-contact response cannot presuppose either. The agent's job is to confirm the appeal is being reviewed fairly and that the player will receive a proper answer. Anything beyond that creates expectations that the review team may not be able to meet.

---

## Case 8: Crash on a specific feature — bug report

**Player message:**
> "Every time I try to open the tournament mode the game crashes. It's been happening since the update yesterday. iPhone 13, iOS 17.2, game version 4.1.1."

**What the system detects:**
- Issue type: reproducible crash, possible regression from recent update
- Urgency signals: tied to a specific update, specific device and version information provided
- Tone: neutral — informative, not angry
- Flags: none

**Priority and SLA:**
- P3 — High
- 8-hour response window

**Where it goes:**
- Technical support
- Reason: a reproducible crash with device and version data is a bug report that needs to reach the technical team. If other players are reporting the same issue on the same update, this could be a widespread regression.

**What the agent is told:**
- Tone: efficient and appreciative — this player gave detailed, useful information. Acknowledge that.
- Collect: steps to reproduce, whether a reinstall or restart temporarily resolved it, any error message displayed
- Action: check the knowledge base for a known workaround. If one exists, provide it. Either way, log the report formally so the technical team can identify if this is affecting multiple players.
- Do not: suggest this is a device problem before investigation. Do not ask for information the player has already provided.

**Operational reasoning:**
A player who submits a detailed bug report with device specs and version numbers is doing the technical team a favour. The response should reflect that. Treating them like a standard complaint rather than a useful reporter damages the relationship and reduces the chance they will report the next issue they find. Internally, this case should be cross-referenced against other recent reports from the same game version.

---

## What these cases have in common

Across all eight scenarios, the system is doing the same thing: reading the incoming message, detecting what matters most about it, and making sure the right human has the right information before they respond.

The triage logic here — when to escalate, what to collect, what tone to take, what not to say in a first response — comes from direct experience managing player care operations. That is what this project is built to demonstrate.
