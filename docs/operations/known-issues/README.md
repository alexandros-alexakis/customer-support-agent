# Known Issues Directory

This directory contains confirmed incidents that have a player impact. The triage engine checks incoming tickets against these entries to identify known issue hits rather than treating them as new unknown complaints.

---

## When to log a known issue

Log an entry here when all three of the following are true:

1. The issue is confirmed by the technical team, not just suspected
2. Players are reporting it or are likely to report it
3. You have a way to verify whether a specific player is affected

Do not log speculation. An entry in this directory activates compensation eligibility and changes how tickets are routed. It needs to be accurate.

---

## File naming

```
ISSUE-YYYY-MM-DD-SHORT-DESCRIPTION.md
```

Examples:
- `ISSUE-2024-03-15-gem-purchase-not-delivered.md`
- `ISSUE-2024-04-02-tournament-crash-ios17.md`
- `ISSUE-2024-04-10-season-pass-progress-reset.md`

---

## How the triage engine uses this directory

When a ticket comes in, the engine checks:
1. Does the intent match a known issue category?
2. Does the player's reported date fall within the issue's affected date range?
3. Does the player's platform match the affected platforms?

If all three match, the ticket is flagged as a known issue hit. This changes the triage result: the response strategy references the known issue, the agent is told whether compensation applies, and the handoff note includes the issue ID for the specialist team.

---

## Verification is required before compensation

A known issue match in triage is a flag, not a confirmation. The agent or specialist team still needs to verify the player was actually affected before any compensation is approved.

Verification methods vary by issue type and are defined in each issue file. Common methods: checking purchase logs against the affected time window, confirming platform and version, cross-referencing account activity.

See [../compensation-matrix.md](../compensation-matrix.md) for compensation rules.

---

## Closing an issue

When the issue is resolved, update the status field to `resolved` and add resolution notes. Do not delete the file. Historical entries are useful for pattern analysis and any delayed compensation reviews.
