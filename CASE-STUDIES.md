# Case Studies — Support Operational Walkthroughs

This document walks through eight realistic player support scenarios, showing the operational logic behind each triage decision. These are not just code outputs — they represent how a senior support professional thinks about each case: what matters, why, what happens next, and what the agent needs to do.

---

## How to read these case studies

Each case shows:

- **Incoming issue** — the player message as received
- **Classification** — intent, tone, confidence, and flags
- **Priority and SLA** — urgency level and expected response window
- **Escalation path** — where the ticket goes and why
- **Response strategy** — what the agent (or AI-assisted agent) should do
- **Operational reasoning** — why these decisions were made

---

## Case 1: Refund request — within policy window

**Incoming issue:**
> "I accidentally bought the wrong pack. I want a refund. It was 10 minutes ago."

**Classification:**
- Intent: `refund_request`
- Confidence: 0.89
- Tone: neutral
- Flags: none

**Priority and SLA:**
- P3 — High
- SLA: 8 hours

**Escalation path:**
- Route to: `billing`
- Reason: refund requests require billing team review; agent cannot approve unilaterally

**Response strategy:**
- Collect: Player ID, transaction ID, purchase date, platform
- Action: Acknowledge request, confirm the purchase details, advise the player that the request is being reviewed
- Tone: Professional, efficient. Do not pre-approve or deny the refund in the initial response.

**Operational reasoning:**
Refund requests within a short window are legitimate service interactions, not complaints. Routing to billing protects both the player and the business — the agent acknowledges quickly without creating a false expectation of approval. What the agent should *not* do: delay the acknowledgement, make a unilateral decision, or ask for information that is unnecessary at this stage.

---

## Case 2: Payment issue — charged but no delivery

**Incoming issue:**
> "I was charged £9.99 for coins but they never appeared in my account. Transaction ID: TXN-884521"

**Classification:**
- Intent: `payment_issue`
- Confidence: 0.86
- Tone: neutral
- Flags: none

**Priority and SLA:**
- P3 — High
- SLA: 8 hours

**Escalation path:**
- Route to: `billing`
- Reason: payment issues with a transaction ID are high priority and require backend verification

**Response strategy:**
- Collect: Player ID, transaction ID, purchase date and amount, platform (iOS/Android/direct)
- Action: Acknowledge, thank the player for providing the transaction ID, explain next steps
- Tone: Professional. Do not suggest the charge will be reversed before verification.

**Operational reasoning:**
This is one of the most common high-priority ticket types in gaming support. The player has already done the right thing by providing a transaction ID — the response should acknowledge that and move efficiently toward resolution. Delays here damage trust. The AI flags this for billing immediately rather than trying to resolve it through FAQ content.

---

## Case 3: Lost progress — account rollback

**Incoming issue:**
> "I logged in this morning and all my progress from the last two weeks is gone. My level, my items, everything."

**Classification:**
- Intent: `lost_progress`
- Confidence: 0.80
- Tone: distressed
- Flags: none

**Priority and SLA:**
- P3 — High
- SLA: 8 hours

**Escalation path:**
- Route to: `technical_support`
- Reason: progress loss may indicate a backend sync issue, account data corruption, or a wider incident

**Response strategy:**
- Collect: Player ID, platform, last login date before the issue, whether they use cloud save
- Action: Acknowledge the loss clearly (do not minimise it), confirm the team will investigate
- Tone: Empathetic but factual. Avoid vague reassurances. Do not promise data recovery.

**Operational reasoning:**
Lost progress is emotionally significant to players — it often represents real time and money. The agent's job in the first response is to validate that concern, collect what is needed to investigate, and not raise false hopes about recovery. If multiple players report the same issue in a short window, this may be an incident — the system flags low-confidence or unusual-volume cases for human review.

---

## Case 4: Account compromise — security concern

**Incoming issue:**
> "Someone has been in my account. There are purchases I didn't make and my email has been changed."

**Classification:**
- Intent: `account_compromise`
- Confidence: 0.91
- Tone: urgent
- Flags: `security_flag`, `requires_human`

**Priority and SLA:**
- P1 — Critical
- SLA: 1 hour

**Escalation path:**
- Route to: `trust_and_safety`
- Reason: account compromise with unauthorised purchases requires identity verification and account lockdown before any other action

**Response strategy:**
- Collect: Do not collect sensitive information over chat. Direct the player to the secure account recovery flow.
- Action: Acknowledge immediately, advise the player to change their password if they still have access, confirm the case has been escalated to the security team
- Tone: Calm, reassuring, clear. Do not ask for passwords or payment details.

**Operational reasoning:**
This case cannot be handled by Tier 1 under any circumstances. Identity verification must happen through a secure channel before anything is disclosed or changed on the account. The AI's job here is to act fast, escalate, and ensure the first-contact response does not make things worse — for example, by disclosing account information to someone who may be the attacker.

---

## Case 5: Abusive player

**Incoming issue:**
> "You are all completely useless. I've been waiting 3 days. Fix this NOW or I'll make sure everyone knows how terrible you are."

**Classification:**
- Intent: `payment_issue` (inferred from context)
- Confidence: 0.55
- Tone: aggressive
- Flags: `repeat_contact`, `abusive_language`

**Priority and SLA:**
- P4 — Urgent
- SLA: 4 hours

**Escalation path:**
- Route to: `senior_agent`
- Reason: abusive tone + repeat contact + low confidence on underlying issue requires experienced handling

**Response strategy:**
- Collect: Do not demand information in the opening response. Acknowledge the wait first.
- Action: De-escalate. Acknowledge the delay directly. Do not apologise in a way that implies fault without knowing the facts. Request the information needed to investigate.
- Tone: Calm, professional, non-defensive. Do not match the player's tone. Do not threaten or warn the player in the first response.

**Operational reasoning:**
This is a case where the AI correctly routes to a senior agent rather than generating an automated response. The underlying issue is unclear, the player is agitated, and a poorly worded response here can inflame the situation further. The AI's value is in getting this to the right person quickly and providing the agent with context — not in attempting to resolve it autonomously.

---

## Case 6: VIP churn risk

**Incoming issue:**
> "I'm done. Uninstalling. This is a waste of money and the support is a joke."

**Classification:**
- Intent: `churn_risk`
- Confidence: 0.75
- Tone: angry
- Flags: `vip_player`, `churn_risk`

**Priority and SLA:**
- P1 — Critical
- SLA: 30 minutes

**Escalation path:**
- Route to: `player_relations`
- Reason: VIP player expressing intent to leave requires proactive, personalised outreach — not a templated response

**Response strategy:**
- Collect: Identify the underlying issue from the contact history before responding
- Action: Escalate immediately to player_relations. Do not send an automated response. Ensure the assigned agent has the player's account history before making contact.
- Tone: Personalised, senior-voice. Generic apologies will make this worse.

**Operational reasoning:**
VIP churn is a revenue and relationship issue, not just a support ticket. The system flags this at P1 regardless of whether the underlying complaint is resolved, because the churn signal is itself the priority. A 30-minute SLA means a human is assigned quickly — the AI's role is to make sure that human has everything they need when they pick it up.

---

## Case 7: Bug report — reproducible crash

**Incoming issue:**
> "Every time I try to open the tournament mode the game crashes. It's been happening since the update yesterday. iPhone 13, iOS 17."

**Classification:**
- Intent: `bug_report`
- Confidence: 0.83
- Tone: neutral
- Flags: none

**Priority and SLA:**
- P3 — High
- SLA: 8 hours

**Escalation path:**
- Route to: `technical_support`
- Reason: reproducible crash with specific device and version data should be logged and passed to the technical team

**Response strategy:**
- Collect: Device model, OS version, game version, steps to reproduce, frequency, whether a restart resolved it temporarily
- Action: Acknowledge, thank the player for the detail they have already provided, confirm the issue will be investigated, provide a workaround if one exists in the knowledge base
- Tone: Helpful and methodical. Players who submit detailed bug reports are engaged users — treat them accordingly.

**Operational reasoning:**
A well-reported bug is an asset. The response should acknowledge the quality of the report and make it easy for the player to provide any missing information. Internally, this should be logged in a way that allows the technical team to identify if other players are reporting the same issue.

---

## Case 8: Ban appeal

**Incoming issue:**
> "My account was banned but I didn't do anything wrong. I've spent hundreds of pounds on this game and this is how I get treated? If my account isn't restored I'm contacting my lawyer."

**Classification:**
- Intent: `ban_appeal`
- Confidence: 0.88
- Tone: threatening
- Flags: `ban_appeal`, `legal_threat`

**Priority and SLA:**
- P1 — Critical
- SLA: 30 minutes

**Escalation path:**
- Route to: `legal_compliance` (legal_threat override)
- Secondary: `trust_and_safety` for ban review
- Reason: legal threat triggers immediate escalation regardless of the underlying ban status

**Response strategy:**
- Action: Acknowledge receipt of the appeal. Do not discuss the ban details, the reason for it, or respond to the legal threat directly. Inform the player that their case has been escalated and they will receive a formal response.
- Collect: Nothing in this response. Evidence collection happens in the escalated review.
- Tone: Formal, calm, non-confrontational. Do not engage with the legal threat.

**Operational reasoning:**
Ban appeals are out of scope for Tier 1 regardless of the circumstances. When a legal threat is also present, the case must go to legal_compliance before any substantive response is written. The first-contact response should be minimal: acknowledge, escalate, confirm a timeline. Saying too much here creates liability. Saying nothing creates the appearance of ignoring the player. The goal is a brief, professional holding response that moves the case to the right team immediately.

---

## What these cases demonstrate

Across these eight scenarios, the pattern is consistent: the AI engine's job is to **classify, prioritise, and route** — not to resolve. Resolution requires human judgment in almost every case above. The system is designed to make sure the right human has the right context at the right time, not to replace them.

The support logic reflected here — when to escalate, how to collect information without alienating the player, how to handle tone, what not to say in a first response — comes from direct experience managing player care operations, not from engineering documentation.
