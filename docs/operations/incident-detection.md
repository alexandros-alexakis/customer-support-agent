# Incident Detection

How to identify when an individual player complaint is actually part of a wider issue affecting multiple players, and what to do when that happens.

---

## Why this matters

The triage engine processes each ticket in isolation. It cannot see that 200 players reported a tournament crash in the last two hours. Without an incident detection layer, an ops team is blind to emerging incidents until the volume becomes impossible to miss, by which time the queue is already overwhelmed and players have already had a poor experience.

Early detection changes the response from reactive to proactive.

---

## What to watch for

An incident is forming when you see a spike in tickets sharing:

- The same intent type (e.g. bug_report, lost_progress, payment_issue)
- The same platform or device type
- The same game feature or area
- A shared time window (all tickets reference something that happened in the last 2-4 hours)

None of these signals alone is sufficient. A spike in payment issues on a Friday afternoon may be noise. A spike in payment issues specifically on iOS, specifically mentioning the season pass, starting within 30 minutes of a game update, is a signal.

---

## Detection thresholds

Configure in `.env`:

```
INCIDENT_DETECTION_WINDOW_MINUTES=60
INCIDENT_DETECTION_THRESHOLD_COUNT=10
INCIDENT_DETECTION_INTENT=bug_report,lost_progress,payment_issue
```

Default: if 10 or more tickets with the same intent arrive within 60 minutes, an alert is triggered.

These thresholds should be calibrated against your normal ticket volume. A team handling 500 tickets per day has a different baseline than one handling 5,000.

---

## What happens when an incident is detected

1. Alert is surfaced to the ops team (Slack, email, or dashboard depending on your setup)
2. Ops confirms whether this is a real incident or noise
3. If confirmed: a new entry is created in [known-issues/](known-issues/README.md) with the issue ID, affected feature, platforms, and date range
4. The triage engine starts routing matching tickets as known issue hits
5. Compensation eligibility is set based on the [compensation matrix](compensation-matrix.md)
6. If proactive outreach is warranted: player relations is notified

---

## Prototype vs production

In this prototype, incident detection is not implemented as a live aggregation layer. The known issues directory must be updated manually when an incident is confirmed.

In production, this would be an aggregation query running on the ticket stream, checking for volume spikes on the intent + platform + time window combination every few minutes. The alert surfaces automatically. The human confirms.

See [docs/roadmap/roadmap.md](../roadmap/roadmap.md) for the planned implementation.

---

## Common false positives

- Scheduled maintenance windows (players report connection issues, this is expected)
- Major game updates (spike in bug reports and confusion questions is normal on update day)
- Seasonal events (payment issues spike when new content is released)
- Social media activity (a streamer posts about an issue and hundreds of players submit the same ticket)

Maintain a calendar of known high-volume events and cross-reference before confirming an incident. See [seasonal-risk-guide.md](seasonal-risk-guide.md).
