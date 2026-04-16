# Edge Cases - Operational Handling Guide

## Overview

This document covers realistic support scenarios that fall outside standard FAQ handling. These are not hypothetical. They represent the cases that break a poorly designed system and expose gaps in classification, escalation, and policy.

Each case includes the scenario, what makes it difficult, and the correct handling approach.

---

## Case 1: Purchase claimed but no receipt

**Scenario:** Player insists they purchased an item but cannot provide any transaction evidence.

**Why it is difficult:** Without a transaction ID, the claim cannot be verified. Fulfilling without evidence creates a fraud vector. Refusing outright creates CSAT failure.

**Correct handling:**
1. Guide the player through receipt location steps: App Store purchase history, Google Play order history, bank statement, email search for store receipt.
2. If no receipt is found after these steps, escalate to billing with note that no receipt was located and steps attempted.
3. Do not fulfil the claim at Tier 1 without evidence.
4. Do not tell the player their claim will be rejected. That decision is for billing.

---

## Case 2: Receipt exists but item not delivered

**Scenario:** Player provides a valid transaction ID and the purchase is confirmed, but the item is not in their account.

**Why it is difficult:** The evidence is solid but resolution requires backend access the assistant does not have.

**Correct handling:**
1. Ask player to restart the app and check again - some delivery delays resolve with a session reset.
2. If still missing: escalate to billing immediately with transaction ID, platform, and confirmation that restart was attempted.
3. Do not speculate on why delivery failed. Do not promise restoration timeline.

---

## Case 3: Delayed store processing

**Scenario:** Player contacts support 15-20 minutes after a purchase and items have not appeared.

**Why it is difficult:** This is usually normal. Escalating every short-delay contact wastes billing team capacity.

**Correct handling:**
1. Inform player that store processing can take up to 30 minutes.
2. Ask player to restart the app.
3. Ask player to wait and recheck after 30 minutes.
4. Collect Transaction ID proactively so escalation is fast if needed.
5. If still missing after 1 hour: escalate to billing.

---

## Case 4: Platform mismatch

**Scenario:** Player purchased on iOS but is now playing on Android and cannot find their purchase.

**Why it is difficult:** Purchases on most platforms are tied to that platform's account and do not transfer. Player expects cross-platform availability.

**Correct handling:**
1. Explain that purchases are generally tied to the platform they were made on.
2. Do not promise cross-platform transfer is possible.
3. Escalate to billing with both platforms noted and transaction ID.
4. Billing team will confirm whether any transfer option exists - this is not a Tier 1 decision.

---

## Case 5: Guest account confusion

**Scenario:** Player was playing as a guest, did not link their account, and has lost access.

**Why it is difficult:** Guest accounts have no email or social login attached. Recovery depends entirely on device-specific data which may be gone.

**Correct handling:**
1. Ask if the player still has access to the original device.
2. Ask for any screenshots showing in-game username or Player ID.
3. Explain clearly that guest account recovery is not guaranteed without a Player ID or device.
4. Escalate to account team with everything collected.
5. Do not promise recovery. Set honest expectations before escalating.

---

## Case 6: Multiple possible account identifiers

**Scenario:** Player is unsure which email or username their account is under. They have multiple options.

**Why it is difficult:** Tier 1 cannot look up accounts. The account team needs identifiers to find the account.

**Correct handling:**
1. Collect all possible identifiers: every email the player might have used, in-game username, device type.
2. Do not ask the player to narrow it down - collect all of them.
3. Escalate to account team with all identifiers and a note that the correct one is unconfirmed.
4. Account team performs the lookup.

---

## Case 7: Partial bug report with weak reproduction steps

**Scenario:** Player reports "the game sometimes crashes" with no other detail.

**Why it is difficult:** Technical team cannot investigate without reproduction information. But asking too many questions at once causes the player to disengage.

**Correct handling:**
1. Ask for device model and OS version first - highest priority for the technical team.
2. In the same or next message, ask what the player was doing when the crash occurred.
3. Ask how frequently it happens.
4. Do not ask all questions at once.
5. Escalate to technical team with whatever detail was collected, noting what could not be obtained.

---

## Case 8: Repeat contact with prior unresolved history

**Scenario:** Player contacts for the third time. The previous two contacts resulted in escalations that were never followed up.

**Why it is difficult:** This is a process failure, not just a ticket. The player has been let down twice already.

**Correct handling:**
1. Acknowledge explicitly that this is their third contact and that this is not acceptable.
2. Do not restart from the beginning or ask them to re-explain the issue.
3. Pull all prior ticket history before responding.
4. Escalate immediately to senior agent with full history attached.
5. Tell the player specifically what will happen next and by when.
6. This interaction should generate a process review, not just a resolution.

---

## Case 9: User claim conflicts with available evidence

**Scenario:** Player claims they were charged twice. Transaction ID provided shows only one charge.

**Why it is difficult:** Either the player is mistaken, or there is a secondary transaction not captured in the reference provided.

**Correct handling:**
1. Do not tell the player they are wrong.
2. Ask if they have a second transaction reference or bank statement showing two charges.
3. Note both the player's claim and the single transaction ID in the escalation.
4. Escalate to billing with the discrepancy documented as: player states double charge / evidence provided shows single charge / bank statement not yet verified.
5. Billing team resolves the discrepancy.

---

## Case 10: Signs of a wider incident from similar reports

**Scenario:** Within 30 minutes, five players have reported that the game crashes when starting an Alliance War.

**Why it is difficult:** At the individual ticket level, each looks like a standard crash report. Collectively they signal an incident.

**Correct handling:**
1. Handle each ticket individually AND flag the pattern.
2. Notify team lead or use the incident reporting channel immediately.
3. Do not tell individual players there is a known issue unless confirmed by the technical team.
4. Use the approved holding response once an incident is declared.
5. Do not speculate on cause or fix timeline to players.

---

## Case 11: Abusive player with a valid support issue

**Scenario:** Player is using offensive language and making personal insults, but they also have a legitimate missing purchase.

**Why it is difficult:** The abuse is not acceptable, but the underlying issue is real and deserves resolution.

**Correct handling:**
1. Address the issue, not the language. Do not match hostility or refuse help because of tone.
2. Keep responses shorter and more factual than usual - do not over-engage.
3. Collect required information and escalate.
4. Note the abusive tone in the escalation record.
5. If the player directs threats at staff (not just general frustration), escalate to senior agent and note the threat.
6. Do not apologise for the player's behaviour or validate it. Simply proceed professionally.
