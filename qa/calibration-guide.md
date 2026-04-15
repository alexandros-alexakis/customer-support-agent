# QA Calibration Guide

## Overview

Calibration ensures all QA reviewers score interactions consistently. Without calibration, scores reflect the reviewer's personal standards rather than the team standard. This guide defines the calibration process.

---

## Why Calibration Matters

If two reviewers score the same ticket differently by more than 10 points, the QA score loses meaning. Agents cannot improve based on inconsistent feedback, and management cannot make reliable decisions from inconsistent data.

---

## Calibration Session Structure

Calibration sessions are held weekly and last 30-45 minutes.

### Step 1 - Select tickets
- Choose 3-5 tickets from the previous week
- Include at least one clear pass, one borderline case, and one clear fail
- Do not select tickets from agents who are present in the session

### Step 2 - Independent scoring
- Each reviewer scores all selected tickets independently before the session
- No discussion until all scores are submitted

### Step 3 - Compare scores
- Share scores simultaneously
- Identify any gaps greater than 10 points
- Discuss the reasoning behind each score

### Step 4 - Align on standard
- Agree on the correct score for each ticket
- Document the reasoning for future reference
- Update the calibration log

### Step 5 - Apply learnings
- Update QA guidance notes if a recurring ambiguity was identified
- Share calibration outcomes with the wider QA team

---

## Calibration Variance Targets

| Variance | Status |
|---|---|
| 0-5 points | Excellent alignment |
| 6-10 points | Acceptable, monitor |
| 11-15 points | Requires discussion and alignment |
| 16+ points | Serious misalignment, full calibration required |

---

## Common Calibration Disputes

### "The tone was fine, just a bit cold"
Default to the player's perspective. If a neutral observer would find the response cold, score accordingly.

### "The agent technically followed policy but the player wasn't helped"
Score resolution quality low. Policy compliance and resolution quality are separate categories.

### "The escalation info was incomplete but the specialist team still resolved it"
Still score escalation handling down. The process matters, not just the outcome.
