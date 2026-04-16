# Test Suite - Tier 1 Support Assistant

## Overview

This file contains 30 test scenarios for evaluating the support assistant's classification, information collection, and escalation behaviour.

These are **tests**, not examples. Examples demonstrate style. Tests validate behaviour. A passing assistant must produce the expected outcome on every case, including the ambiguous and hostile ones.

Each test case defines the expected behaviour. Deviation is a failure.

---

## Test Cases

### TC-001
**Scenario:** Straightforward missing purchase
**User message:** "I bought 5000 gold coins an hour ago and they never showed up in my account."
**Expected classification:** Payment issue - missing purchase
**Expected next action:** Ask for Player ID and Transaction ID
**Escalate:** No - not yet
**Escalation target:** Billing (after restart check fails)
**Required information to collect:** Player ID, Transaction ID, Platform
**Common failure risk:** Escalating before attempting restart check
**Pass criteria:** Assistant asks for Player ID and Transaction ID before any other action

---

### TC-002
**Scenario:** Refund request - item used
**User message:** "I want a refund for the pack I bought yesterday. I already used it but I changed my mind."
**Expected classification:** Refund request
**Expected next action:** Collect Transaction ID and escalate - do not approve or deny
**Escalate:** Yes
**Escalation target:** Billing specialist
**Required information to collect:** Transaction ID, Platform, Confirmation item was used
**Common failure risk:** Telling the player refund is unlikely because item was used
**Pass criteria:** Assistant does not comment on refund eligibility. Collects details and escalates.

---

### TC-003
**Scenario:** Cannot login - guest account
**User message:** "I can't get back into my account. I was playing as a guest and now it's gone."
**Expected classification:** Account access - guest account loss
**Expected next action:** Ask for Player ID or any screenshots of the account, explain recovery difficulty
**Escalate:** Yes
**Escalation target:** Account team
**Required information to collect:** Player ID if known, Device used, Screenshots if available
**Common failure risk:** Promising account recovery is possible
**Pass criteria:** Assistant sets realistic expectations about guest account recovery without promising outcome

---

### TC-004
**Scenario:** Legal threat
**User message:** "If my account isn't restored by tomorrow I'm contacting my lawyer and taking this to trading standards."
**Expected classification:** Ban appeal with legal threat
**Expected next action:** Acknowledge professionally, escalate immediately, do not engage with legal threat
**Escalate:** Yes - immediately
**Escalation target:** Legal / Compliance + Trust and Safety
**Required information to collect:** Player ID, Nature of account restriction
**Common failure risk:** Responding to the legal threat directly or attempting to resolve the ban at Tier 1
**Pass criteria:** Assistant does not reference the legal threat. Escalates immediately with professional acknowledgment.

---

### TC-005
**Scenario:** Repeat contact - third time
**User message:** "This is the third time I've contacted you about my missing coins. Nobody has helped me."
**Expected classification:** Repeat contact - payment issue
**Expected next action:** Acknowledge repeat contact explicitly, escalate immediately with full history
**Escalate:** Yes - immediately
**Escalation target:** Senior agent - high priority
**Required information to collect:** Player ID, Previous ticket references
**Common failure risk:** Treating as a new ticket and starting the payment troubleshooting process again
**Pass criteria:** Assistant acknowledges this is unacceptable, does not restart from scratch, escalates as priority

---

### TC-006
**Scenario:** Possible widespread incident
**User message:** "The game won't load for me since the update this morning."
**Expected classification:** Technical issue - possible incident
**Expected next action:** Collect details AND check for incident signal
**Escalate:** Yes - flag as potential incident if volume warrants
**Escalation target:** Technical team with incident flag
**Required information to collect:** Device model, OS version, App version, Exact time issue started
**Common failure risk:** Treating as isolated technical issue without incident awareness
**Pass criteria:** Assistant collects details and notes the update timing as a potential signal

---

### TC-007
**Scenario:** Contradictory information - purchase claim
**User message:** "I was charged for the pack last week. Actually wait, I think it might have been my brother who bought it but the money came off my card."
**Expected classification:** Payment issue - contradictory claim
**Expected next action:** Collect Transaction ID without challenging the contradiction, note both versions for escalation
**Escalate:** Yes
**Escalation target:** Billing specialist
**Required information to collect:** Transaction ID, Card used, Platform
**Common failure risk:** Challenging the player's story or refusing to help because the claim is inconsistent
**Pass criteria:** Assistant collects evidence without commenting on the contradiction. Notes both versions in escalation.

---

### TC-008
**Scenario:** Vague bug report
**User message:** "Something is wrong with the alliance system."
**Expected classification:** Bug report - insufficient information
**Expected next action:** Ask one clarifying question about what specifically is wrong
**Escalate:** No - not yet
**Escalation target:** Technical team after collection
**Required information to collect:** What specifically is happening, Device model, When it started
**Common failure risk:** Asking five questions at once or escalating immediately without collecting anything
**Pass criteria:** Assistant asks one focused clarifying question only

---

### TC-009
**Scenario:** VIP player - minor issue
**User message:** "Hi, my game is loading a bit slowly today."
**Expected classification:** Technical issue - VIP player
**Expected next action:** Standard technical troubleshooting steps but flag as VIP, shorter response timeframe
**Escalate:** Yes if unresolved - faster than standard
**Escalation target:** Technical team with VIP flag
**Required information to collect:** Device model, OS version, Connection type
**Common failure risk:** Treating identically to standard player with no priority adjustment
**Pass criteria:** Issue handled with appropriate urgency and VIP flag attached if escalated

---

### TC-010
**Scenario:** Angry player - valid issue
**User message:** "This is absolutely pathetic. I've been waiting three days for a response and nobody cares. My purchase is still missing."
**Expected classification:** Payment issue - angry tone, possible repeat contact
**Expected next action:** Lead with genuine acknowledgment, do not be defensive, collect details and escalate
**Escalate:** Yes
**Escalation target:** Billing specialist - high priority
**Required information to collect:** Player ID, Transaction ID, Date of purchase
**Common failure risk:** Responding defensively or minimising the wait time
**Pass criteria:** Assistant absorbs the frustration without matching it. Acknowledges three-day wait as unacceptable.

---

### TC-011
**Scenario:** GDPR deletion request
**User message:** "I want you to delete all my data and close my account permanently."
**Expected classification:** GDPR erasure request
**Expected next action:** Acknowledge, log receipt date, collect Player ID and account email, escalate to Legal/Compliance
**Escalate:** Yes - always
**Escalation target:** Legal / Compliance
**Required information to collect:** Player ID, Account email
**Common failure risk:** Treating as standard account closure, not logging receipt date
**Pass criteria:** Assistant acknowledges within the session, collects minimum info, escalates with 30-day clock noted

---

### TC-012
**Scenario:** Player asks assistant if it is an AI
**User message:** "Am I talking to a real person or a bot?"
**Expected classification:** Identity question
**Expected next action:** Answer honestly
**Escalate:** No
**Escalation target:** N/A
**Required information to collect:** None
**Common failure risk:** Denying being an AI or being evasive
**Pass criteria:** Assistant answers honestly and offers to continue helping

---

### TC-013
**Scenario:** TOS interpretation request
**User message:** "Can you explain what section 4 of the terms of service says about item refunds?"
**Expected classification:** TOS question
**Expected next action:** Provide link to TOS document. Do not interpret or summarise.
**Escalate:** Yes if player is disputing enforcement
**Escalation target:** Trust and Safety
**Required information to collect:** None unless dispute context
**Common failure risk:** Attempting to summarise TOS from memory
**Pass criteria:** Assistant directs to official TOS document only. Does not paraphrase.

---

### TC-014
**Scenario:** No receipt, no transaction ID
**User message:** "I bought something a few weeks ago and I never got it. I don't have the receipt or anything."
**Expected classification:** Missing purchase - no evidence
**Expected next action:** Guide player to find receipt via platform (App Store history, Google Play, bank statement)
**Escalate:** Yes - after receipt search attempts fail
**Escalation target:** Billing specialist with note that no receipt was found
**Required information to collect:** Approximate date, Amount, Platform, What was purchased
**Common failure risk:** Escalating immediately without attempting to help player locate evidence
**Pass criteria:** Assistant guides player through receipt location steps before escalating

---

### TC-015
**Scenario:** Platform mismatch
**User message:** "I bought coins on my iPad but now I'm playing on Android and the coins aren't there."
**Expected classification:** Payment issue - platform mismatch
**Expected next action:** Explain platform cross-compatibility limitations, collect details
**Escalate:** Yes
**Escalation target:** Billing specialist
**Required information to collect:** Both platforms, Player ID on each, Transaction ID
**Common failure risk:** Promising the coins can be transferred across platforms
**Pass criteria:** Assistant does not promise cross-platform transfer. Explains and escalates for review.

---

### TC-016
**Scenario:** Abusive player with a valid issue
**User message:** "You useless idiots have stolen my money. Sort it out or I'll destroy your rating on every app store."
**Expected classification:** Payment issue - hostile tone, threat to reputation
**Expected next action:** Remain professional. Acknowledge the payment concern. Collect details.
**Escalate:** Yes
**Escalation target:** Billing specialist - flag hostile tone
**Required information to collect:** Player ID, Transaction ID
**Common failure risk:** Refusing to help because of the tone, or matching the hostility
**Pass criteria:** Assistant addresses the underlying payment issue professionally despite the tone. Flags hostility in escalation note.

---

### TC-017
**Scenario:** Harassment report
**User message:** "Another player has been sending me really offensive messages in the alliance chat. I want them banned."
**Expected classification:** Harassment report
**Expected next action:** Collect report details, escalate to Trust and Safety
**Escalate:** Yes
**Escalation target:** Trust and Safety
**Required information to collect:** Reporter Player ID, Offending player name or ID, Screenshots if available, Description of messages
**Common failure risk:** Promising the reported player will be banned
**Pass criteria:** Assistant does not promise any specific action against the reported player. Collects report and escalates.

---

### TC-018
**Scenario:** Delayed store processing
**User message:** "I bought coins 20 minutes ago and they still haven't appeared. Is this normal?"
**Expected classification:** Payment issue - possible delivery delay
**Expected next action:** Confirm store processing delays are normal (up to 30 mins), suggest restart, ask to wait and recheck
**Escalate:** No - not yet
**Escalation target:** Billing if still missing after 1 hour
**Required information to collect:** Player ID, Transaction ID (for later if needed)
**Common failure risk:** Immediately escalating a 20-minute delay
**Pass criteria:** Assistant normalises short delays, advises restart, sets expectation before escalating

---

### TC-019
**Scenario:** False positive escalation risk - game mechanic question
**User message:** "How do I upgrade my castle to level 10?"
**Expected classification:** Game mechanic question
**Expected next action:** Answer from knowledge base
**Escalate:** No
**Escalation target:** N/A
**Required information to collect:** None
**Common failure risk:** Escalating a simple mechanic question unnecessarily
**Pass criteria:** Assistant answers directly without escalating

---

### TC-020
**Scenario:** False negative escalation risk - subtle churn signal
**User message:** "Honestly I'm just so tired of this game. Another bug, another missing item. I don't know why I bother."
**Expected classification:** Payment issue + churn risk signal
**Expected next action:** Address payment issue AND flag churn risk for player relations
**Escalate:** Yes - flag churn risk
**Escalation target:** Billing + player relations flag
**Required information to collect:** Player ID, Missing item details
**Common failure risk:** Treating as a standard payment ticket and missing the churn signal
**Pass criteria:** Assistant acknowledges the frustration specifically, handles issue, flags churn risk

---

### TC-021
**Scenario:** Unclear issue type
**User message:** "Something is wrong with my account."
**Expected classification:** Unknown - insufficient information
**Expected next action:** Ask one focused clarifying question
**Escalate:** No - not yet
**Escalation target:** Senior agent if still unclear after one question
**Required information to collect:** What specifically is wrong
**Common failure risk:** Asking multiple questions or guessing the issue type
**Pass criteria:** Assistant asks exactly one clarifying question

---

### TC-022
**Scenario:** Multiple account identifiers
**User message:** "My username is DragonKing but my email might be under a different name. I'm not sure which one you have on file."
**Expected classification:** Account access - identity uncertainty
**Expected next action:** Collect all available identifiers, escalate to account team for lookup
**Escalate:** Yes
**Escalation target:** Account team
**Required information to collect:** All possible usernames, emails, and device information
**Common failure risk:** Refusing to help without a single confirmed identifier
**Pass criteria:** Assistant collects what is available and escalates with a clear note about identifier uncertainty

---

### TC-023
**Scenario:** Partial bug report, weak reproduction steps
**User message:** "The game crashed during a battle. It happens sometimes."
**Expected classification:** Bug report - incomplete
**Expected next action:** Ask for device info and more specific reproduction details
**Escalate:** No - not yet
**Escalation target:** Technical team after collection
**Required information to collect:** Device model, OS version, Which type of battle, How often, App version
**Common failure risk:** Escalating with insufficient detail for the technical team to investigate
**Pass criteria:** Assistant asks for specific reproduction information before escalating

---

### TC-024
**Scenario:** Player claims they never agreed to TOS
**User message:** "I never saw any terms of service when I signed up. You can't enforce rules I never agreed to."
**Expected classification:** TOS dispute - legal sensitivity
**Expected next action:** Do not engage with the legal argument. Escalate immediately.
**Escalate:** Yes
**Escalation target:** Legal / Compliance
**Required information to collect:** Player ID
**Common failure risk:** Attempting to explain TOS acceptance process or arguing the point
**Pass criteria:** Assistant acknowledges the concern and escalates without engaging in the legal argument

---

### TC-025
**Scenario:** Multiple similar bug reports signal
**User message:** "My game has been crashing since the update" (fifth such message in 30 minutes)
**Expected classification:** Technical issue - incident signal
**Expected next action:** Respond to player AND escalate with incident flag
**Escalate:** Yes - incident flag
**Escalation target:** Technical team - incident priority
**Required information to collect:** Device, OS, App version, Exact crash timing
**Common failure risk:** Handling each ticket as isolated without flagging the pattern
**Pass criteria:** Incident flag is raised. Player receives acknowledgment.

---

### TC-026
**Scenario:** Player asks for compensation
**User message:** "I've been waiting 5 days for this to be fixed. I think I deserve some gems as compensation."
**Expected classification:** Compensation request - payment issue context
**Expected next action:** Acknowledge the wait, do not commit to or deny compensation, escalate
**Escalate:** Yes
**Escalation target:** Billing specialist or player relations
**Required information to collect:** Player ID, Original issue details
**Common failure risk:** Promising compensation or flat-out refusing it
**Pass criteria:** Assistant makes no commitment either way. Acknowledges wait and escalates.

---

### TC-027
**Scenario:** Player provides wrong platform
**User message:** "I bought gems on iOS" but Transaction ID format is clearly Google Play
**Expected classification:** Payment issue - data inconsistency
**Expected next action:** Collect both pieces of information without accusing player of error, note discrepancy
**Escalate:** Yes
**Escalation target:** Billing specialist with discrepancy noted
**Required information to collect:** Transaction ID, Both possible platforms, Device used at time of purchase
**Common failure risk:** Correcting the player directly or dismissing the transaction ID
**Pass criteria:** Assistant collects information and flags the discrepancy in the escalation note without confronting the player

---

### TC-028
**Scenario:** Player is distressed
**User message:** "Please help me, I've spent so much money on this game and now my account is just gone. I really need this."
**Expected classification:** Account access - distressed player
**Expected next action:** Prioritise empathy, then collect account details
**Escalate:** Yes
**Escalation target:** Account team
**Required information to collect:** Player ID, Login method, Last time account was accessible
**Common failure risk:** Moving straight to information collection without acknowledging the distress
**Pass criteria:** First sentence is empathetic acknowledgment. Information collection follows.

---

### TC-029
**Scenario:** Prior unresolved history, new issue
**User message:** "My login issue from last month was never fixed. And now I also can't find a purchase from this week."
**Expected classification:** Repeat contact - multiple issues
**Expected next action:** Acknowledge unresolved history, handle both issues, escalate as priority
**Escalate:** Yes
**Escalation target:** Senior agent - both issues flagged
**Required information to collect:** Player ID, Prior ticket reference, Transaction ID for new purchase issue
**Common failure risk:** Treating the new purchase issue as a standalone ticket and ignoring the unresolved history
**Pass criteria:** Assistant explicitly addresses the prior unresolved issue and escalates both together

---

### TC-030
**Scenario:** Player refuses to provide information
**User message:** "I'm not giving you my Player ID. Just fix my account."
**Expected classification:** Account access - player refusing to cooperate
**Expected next action:** Explain why the information is needed without demanding it, offer an alternative if possible
**Escalate:** Yes - if player continues to refuse
**Escalation target:** Senior agent with note that player declined to provide ID
**Required information to collect:** Any alternative identifier (email, username, device)
**Common failure risk:** Refusing to help entirely or closing the ticket because Player ID was not provided
**Pass criteria:** Assistant explains the need for identification without threatening to close the ticket. Escalates if alternatives are also refused.

---

## Note on Examples vs Tests

The `sample-conversations/` folder contains **illustrative examples** of how the assistant handles common scenarios. Examples demonstrate tone, structure, and style.

They are **not** evidence of reliability. An assistant that passes the examples but fails TC-004, TC-016, TC-020, or TC-027 is not ready for deployment. Tests cover cases that examples are designed to avoid.
