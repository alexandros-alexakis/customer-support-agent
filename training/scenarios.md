# Agent Training Scenarios

Generated: 2026-04-17 13:17 UTC
Scenarios: 12

Use these scenarios for onboarding practice, team calibration sessions, or coaching.
Each scenario includes the expected handling approach and common mistakes.

**Difficulty guide:** Easy = Tier 1 standard · Medium = requires judgement · Hard = edge case / emotional

## Summary

| Difficulty | Count |
|---|---|
| Easy | 6 |
| Medium | 3 |
| Hard | 3 |

---

### Scenario 1: [Easy]

**Player message:**
> "I bought 5000 gold coins and they never appeared in my account."

**Context:** First contact

**Expected classification:** Intent: `payment_issue` | Tone: `neutral` | Escalate: Yes → billing

**Correct approach:**
Acknowledge the issue. Collect Player ID and transaction ID. Check if the payment shows in platform receipts. Escalate to billing with full details.

**Common mistakes to avoid:**
  - Promising a refund without authorisation
  - Asking the player to repurchase
  - Not collecting the transaction ID before escalating

---

### Scenario 2: [Medium]

**Player message:**
> "This is the THIRD time I have contacted you about a missing purchase. Nobody ever helps me."

**Context:** Contact #3 from this player

**Expected classification:** Intent: `payment_issue` | Tone: `angry` | Escalate: Yes → billing

**Correct approach:**
Lead with empathy and acknowledge this is not their first contact. Take ownership. Do not ask them to repeat information already given. Escalate with urgent flag and full contact history.

**Common mistakes to avoid:**
  - Starting with a generic greeting
  - Asking for information they may have already provided
  - Matching the player's frustration
  - Saying 'unfortunately'

---

### Scenario 3: [Easy]

**Player message:**
> "I can't log into my account. I tried resetting my password but the email never arrived."

**Context:** First contact

**Expected classification:** Intent: `account_access` | Tone: `frustrated` | Escalate: Yes → account_team

**Correct approach:**
Collect login method (email, Google, Apple, Facebook, guest). Ask them to check spam folder. If still no email, escalate to account team with the login method confirmed.

**Common mistakes to avoid:**
  - Assuming the login method without asking
  - Telling them to 'try again later'
  - Not checking if the reset email is in spam

---

### Scenario 4: [Medium]

**Player message:**
> "My account was banned. I have never cheated in my life. This is completely unfair."

**Context:** First contact

**Expected classification:** Intent: `ban_appeal` | Tone: `angry` | Escalate: Yes → trust_and_safety

**Correct approach:**
Acknowledge frustration without confirming or denying the ban reason. Do not share any information about what triggered the restriction. Collect Player ID and date ban was noticed. Escalate to Trust & Safety.

**Common mistakes to avoid:**
  - Saying 'I understand you didn't cheat'
  - Explaining what caused the ban
  - Promising the ban will be reversed
  - Asking for screenshots of gameplay

---

### Scenario 5: [Easy]

**Player message:**
> "I want a refund for the pack I bought yesterday. I didn't mean to buy it."

**Context:** First contact

**Expected classification:** Intent: `refund_request` | Tone: `neutral` | Escalate: Yes → billing

**Correct approach:**
Acknowledge the request without confirming a refund is possible. Collect Player ID, transaction ID, platform, and whether items were used. Escalate to billing for review.

**Common mistakes to avoid:**
  - Saying 'refunds are not available'
  - Promising a refund will be issued
  - Not checking whether items were used before escalating

---

### Scenario 6: [Easy]

**Player message:**
> "There is a player in my server using an obvious speed hack. I have video proof."

**Context:** First contact

**Expected classification:** Intent: `fraud_report` | Tone: `neutral` | Escalate: Yes → trust_and_safety

**Correct approach:**
Thank the player for reporting. Collect: reported player's username, date and description of incident, and ask them to send screenshots or video via the link. Escalate to Trust & Safety.

**Common mistakes to avoid:**
  - Promising the reported player will be banned
  - Asking for the reported player's Player ID (they won't have it)
  - Telling the player the outcome of the investigation

---

### Scenario 7: [Hard]

**Player message:**
> "I'm completely done with this game. I've spent €200 and it keeps crashing. I'm uninstalling."

**Context:** First contact

**Expected classification:** Intent: `churn_risk` | Tone: `angry` | Escalate: Yes → player_relations

**Correct approach:**
Lead with genuine empathy — do not jump to troubleshooting. Acknowledge the spend and the frustration. Escalate immediately to player relations as a churn risk. Collect Player ID. Do not offer refunds or compensation without authorisation.

**Common mistakes to avoid:**
  - Opening with technical troubleshooting steps
  - Offering a refund or bonus without authorisation
  - Minimising the player's frustration
  - Saying 'I understand your frustration but...'

---

### Scenario 8: [Medium]

**Player message:**
> "The game crashed during my alliance war battle and I lost all my troops. Can you restore them?"

**Context:** First contact

**Expected classification:** Intent: `technical_issue` | Tone: `frustrated` | Escalate: No (handle at Tier 1)

**Correct approach:**
Acknowledge the frustration. Collect device model, OS version, app version, and exact timing of the crash. Check if this is an isolated issue or part of a wider incident. Do not promise troop restoration — that requires billing team review.

**Common mistakes to avoid:**
  - Promising troop restoration
  - Escalating immediately without gathering device info
  - Dismissing the loss as 'normal game behaviour'

---

### Scenario 9: [Hard]

**Player message:**
> "I want to delete my account and all my data. GDPR."

**Context:** First contact

**Expected classification:** Intent: `unknown` | Tone: `neutral` | Escalate: Yes → senior_agent

**Correct approach:**
Treat this as a formal GDPR data deletion request. Do not attempt to handle at Tier 1. Collect Player ID and the email address on the account. Escalate to the data privacy team (senior agent route) and inform the player of the 30-day statutory response window.

**Common mistakes to avoid:**
  - Attempting to process the deletion yourself
  - Asking the player to 'just uninstall the game'
  - Promising deletion within a specific short timeframe
  - Not informing the player of the statutory response window

---

### Scenario 10: [Hard]

**Player message:**
> "If this issue isn't resolved today I will be taking legal action and posting on every review site."

**Context:** Contact #2 from this player

**Expected classification:** Intent: `ban_appeal` | Tone: `threatening` | Escalate: Yes → trust_and_safety

**Correct approach:**
Stay calm and professional. Do not engage with the legal threat directly. Do not escalate the tone. Acknowledge the frustration briefly and state that the case is being escalated. Collect Player ID. Pass 'legal_threat' flag to the receiving team.

**Common mistakes to avoid:**
  - Saying 'please calm down'
  - Responding to the legal threat directly ('we have done nothing wrong')
  - Promising an outcome to avoid escalation
  - Matching the urgency or emotion of the player

---

### Scenario 11: [Easy]

**Player message:**
> "I accidentally bought the wrong pack. Can I swap it for a different one?"

**Context:** First contact

**Expected classification:** Intent: `refund_request` | Tone: `neutral` | Escalate: Yes → billing

**Correct approach:**
Acknowledge the request. Collect Player ID, transaction ID, platform, pack name purchased, and pack name wanted. Check item usage. Escalate to billing — swaps are treated the same as refunds.

**Common mistakes to avoid:**
  - Approving the swap yourself
  - Telling the player swaps are 'not possible'
  - Not asking whether the items in the wrong pack were used

---

### Scenario 12: [Easy]

**Player message:**
> "The app won't open at all since this morning's update."

**Context:** First contact

**Expected classification:** Intent: `technical_issue` | Tone: `frustrated` | Escalate: No (handle at Tier 1)

**Correct approach:**
Acknowledge the timing (post-update). Check whether this is a known incident. Collect device model, OS version, app version. Ask them to try: force-close, clear cache, reinstall. If multiple players are reporting the same issue after an update, flag as a potential incident.

**Common mistakes to avoid:**
  - Immediately telling the player to reinstall without troubleshooting
  - Not noting the update timing as a relevant signal
  - Escalating without gathering basic device info first
