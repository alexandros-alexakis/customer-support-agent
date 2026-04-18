# Response Quality Rubric

A structured scoring guide for QA review of AI-assisted support interactions. Not just whether the response sounded good, but whether it did the right things.

---

## How to use this rubric

Score each interaction across six dimensions. Each dimension scores 0, 1, or 2. Maximum score is 12.

Use this rubric for:
- Regular QA sampling of AI-assisted tickets (recommended: random sample of 5-10% weekly)
- Calibration sessions with agents to align on quality standards
- Identifying patterns in AI failure modes to feed back into the learning loop

---

## Scoring dimensions

### 1. Correct routing (0-2)

**2:** Ticket went to the right team for the right reason.
**1:** Ticket went to an acceptable team but not the optimal one, or routing was correct but reasoning was unclear.
**0:** Ticket went to the wrong team, or should have escalated and did not, or escalated unnecessarily.

Notes:

---

### 2. Information collection (0-2)

**2:** All required information for this issue type was collected. No unnecessary information was requested. Player was not asked for something they already provided.
**1:** Most required information collected, or one unnecessary ask, or one piece of required information missed.
**0:** Key information missing that would prevent resolution, or player was asked to repeat themselves.

Notes:

---

### 3. Tone appropriateness (0-2)

**2:** Tone matched the player's emotional state appropriately. Empathy shown where needed. Professional throughout.
**1:** Tone was acceptable but missed an opportunity to acknowledge distress or frustration, or was slightly too formal / informal for the situation.
**0:** Tone was inappropriate: too cold for a distressed player, too casual for a legal threat, or defensive with an angry player.

Notes:

---

### 4. Scope compliance (0-2)

**2:** System stayed within T1 scope. Did not attempt to resolve out-of-scope issues. Escalated correctly when needed.
**1:** Minor scope boundary question, or escalated something that could have been resolved at T1.
**0:** System attempted to resolve an out-of-scope issue, or gave information it should not have given (account data, policy specifics beyond its knowledge).

Notes:

---

### 5. Accuracy (0-2)

**2:** All information provided was accurate and consistent with current policy and KB content.
**1:** Minor inaccuracy or outdated information that would not mislead the player.
**0:** Factually incorrect information, hallucinated policy, or a response that contradicts current policy.

Notes:

---

### 6. Player experience (0-2)

**2:** Response was clear, appropriately concise, and would leave the player feeling heard and informed about next steps.
**1:** Response was acceptable but overly long, or unclear on next steps, or missed an opportunity to reassure.
**0:** Response was confusing, generic, dismissive, or would likely increase the player's frustration.

Notes:

---

## Score interpretation

| Score | Assessment |
|---|---|
| 11-12 | Excellent. No action needed. |
| 9-10 | Good. Minor improvement opportunity. |
| 7-8 | Acceptable. Pattern to monitor. |
| 5-6 | Below standard. Review and log issue type. |
| 0-4 | Failing. Escalate for immediate review. Flag in issue tracker. |

---

## What to do with results

For any score below 7: log the failure mode using the appropriate issue template (bug, KB gap, escalation misfire, or scope creep).

For patterns across multiple tickets: bring to the weekly ops review. If the same dimension is failing consistently, that is a systemic issue, not a one-off.

For accuracy failures specifically: immediate KB review required. Do not wait for the next scheduled review.
