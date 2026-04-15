# Capacity Planning Guide

## Overview

This document outlines how to forecast staffing needs for the customer support team based on historical ticket volume, seasonal patterns, and planned game events.

---

## Key Metrics for Capacity Planning

| Metric | Definition |
|---|---|
| Average Handling Time (AHT) | Average time to resolve one ticket from first contact to close |
| Tickets Per Agent Per Hour | How many tickets one agent can handle in one hour |
| Occupancy Rate | Percentage of time agents spend actively handling tickets |
| Shrinkage | Time lost to breaks, training, meetings, absence (typically 25-35%) |
| Service Level Target | % of tickets responded to within target time (e.g. 80% within 4 hours) |

---

## Staffing Formula

```
Agents Required = (Forecasted Ticket Volume x AHT) / (Available Minutes Per Agent x Target Occupancy)
```

Always add shrinkage on top of the base calculation:

```
Final Headcount = Agents Required / (1 - Shrinkage %)
```

---

## Seasonal Volume Patterns

Gaming support ticket volumes follow predictable patterns:

| Period | Volume Impact | Reason |
|---|---|---|
| Game update releases | +40 to +100% | New bugs, feature confusion |
| In-game seasonal events | +30 to +60% | Event item issues, confusion |
| Holiday periods | +20 to +40% | New players, gifting issues |
| Weekend vs weekday | +15 to +25% on weekends | Higher player activity |
| Server maintenance windows | +20% post-maintenance | Issues discovered after downtime |

---

## Planning Horizons

| Horizon | Purpose | Owner |
|---|---|---|
| Daily | Intraday staffing adjustments | Team Lead |
| Weekly | Schedule planning for next week | Vendor Manager |
| Monthly | Headcount review and BPO coordination | Vendor Manager / L&D Lead |
| Quarterly | Strategic headcount and hiring plan | Management |

---

## BPO Coordination

When working with BPO partners:

- Provide volume forecasts at least 2 weeks in advance
- Agree on flex capacity thresholds (e.g. BPO can scale up to 20% within 48 hours)
- Define escalation paths if BPO capacity is exceeded
- Review BPO performance weekly against agreed KPIs
