# Seasonal and Event Risk Guide

Gaming support has predictable high-risk moments. This guide covers how to prepare the system and the team before they happen.

---

## High-risk event types

### Major game updates

**Why they are high-risk:** Updates change how features work, introduce new bugs, sometimes break things that were working. Players who experience issues immediately after an update are more likely to blame the game than their own setup.

**What to expect:** Spike in bug reports, technical issues, and "something changed" complaints within 2-6 hours of release. If a payment feature was changed, expect payment issues.

**Preparation checklist:**
- KB review 48 hours before: update any content that will be affected by the patch notes
- Lower the incident detection threshold for the 24 hours post-update
- Pre-brief agents on what changed so they have context before tickets arrive
- Have a known issue entry template ready to fill in immediately if a bug is confirmed
- Confirm escalation paths are current (team names, availability)

---

### Season launches and battle pass releases

**Why they are high-risk:** New content drives purchases. Purchase issues, delivery failures, and "I bought X but got Y" tickets spike. Players who spend money on launch day and have a bad experience are among the most vocal.

**What to expect:** Payment issues, missing item reports, refund requests. VIP players spending on launch day and encountering issues are a churn risk.

**Preparation checklist:**
- Confirm payment KB is current (refund policy, delivery troubleshooting)
- Brief player relations on new VIP content so they have context for high-value player contacts
- Increase QA sampling rate for the first 48 hours
- Set a lower compensation matrix approval threshold for known launch day issues if leadership approves

---

### Holiday sales and limited-time events

**Why they are high-risk:** Volume spikes across all categories. Players who do not normally contact support come in. Event-specific questions the KB may not cover.

**What to expect:** General volume increase 2-3x normal. Event mechanic questions. FOMO-driven frustration if something does not work during a limited window.

**Preparation checklist:**
- Add event-specific FAQ to the KB at least 24 hours before the event starts
- Increase staffing or extend coverage hours for the event window
- Prepare a response strategy for "I missed the event because of a bug" - this is common and sensitive
- Set clear policy before the event on whether missed event rewards will be compensated

---

### Tournament and competitive windows

**Why they are high-risk:** Competitive players have high expectations and low tolerance for issues. A bug during a tournament match carries real stakes for the player. Responses need to be fast and accurate.

**What to expect:** Bug reports with detailed reproduction steps (good), ban appeals from players who believe they were incorrectly penalised for behaviour caused by a bug (complex), frustration at high intensity.

**Preparation checklist:**
- Confirm tournament rules and ban appeal process is in the KB
- Brief Trust & Safety on the tournament window so they can prioritise ban appeal reviews
- Lower the VIP threshold temporarily if competitive players are not already tiered as VIP
- Have a fast-track escalation path for confirmed bugs during live tournament windows

---

## Adjusting the triage system for high-risk periods

**Lower incident detection threshold:** Reduce the count needed to trigger an incident alert during high-risk windows. A 10-ticket threshold on a normal day might be 5 during a launch.

```
INCIDENT_DETECTION_THRESHOLD_COUNT=5
```

**Increase escalation sensitivity:** During a major update, consider temporarily lowering the confidence threshold so more tickets go to human review rather than automated response.

```
CLASSIFICATION_CONFIDENCE_THRESHOLD=0.75
```

**Pre-load KB content:** Run `python rag/kb_sync.py` after any pre-event KB updates so the content is indexed before tickets arrive.

**Brief the team:** Agents who know what changed perform better. A 15-minute pre-brief before a major launch is worth more than any configuration change.

---

## Post-event review

After every major event or update, run a brief review:

- What issue types spiked that the KB did not cover? Log KB gaps.
- Did the incident detection trigger? Was it accurate or a false positive?
- Were any compensation decisions made that should update the compensation matrix?
- What would have made the team better prepared?

This review feeds directly into preparation for the next event.
