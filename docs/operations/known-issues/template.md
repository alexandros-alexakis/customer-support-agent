# Known Issue Template

Copy this file, rename it using the `ISSUE-YYYY-MM-DD-SHORT-DESCRIPTION.md` format, and fill in all fields.

---

## Issue ID

`ISSUE-YYYY-MM-DD-SHORT-DESCRIPTION`

## Title

One sentence describing the issue.

## Status

`ongoing` or `resolved`

## Reported date

Date the issue was first confirmed internally.

## Affected feature

The specific game feature, system, or flow affected. Be specific: "gem purchase delivery" not "purchases".

## Affected platforms

List all affected platforms. Example: iOS 17.x, Android 13+, all platforms.

## Affected date range

The window during which players could have been affected.

Start: YYYY-MM-DD
End: YYYY-MM-DD (or "ongoing")

## Symptoms

What the player experiences. Written from the player's perspective.

Example:
- Player completes a gem purchase, charge appears on their payment method, gems do not appear in account
- Issue occurs on first purchase attempt only, retry succeeds

## Verification method

How to confirm a specific player was affected. This must be answerable with available data.

Example:
- Check purchase logs for a completed transaction between [start date] and [end date] with no corresponding inventory credit
- Confirm player is on iOS 17.x
- Confirm the transaction was not already manually credited

## Compensation eligible

`yes` or `no`

If yes, which tier? See [../compensation-matrix.md](../compensation-matrix.md).

## Compensation tier

`tier-1` / `tier-2` / `tier-3` / `manual-review`

## Who approves compensation

Role or team name. Example: billing team, senior agent, player relations.

## Proactive outreach required

`yes` or `no`

If yes, which players should be contacted and by when?

## Resolution notes

What fixed the issue and when. Leave blank if ongoing.

## Related tickets

Ticket IDs or patterns that led to this issue being identified.
