# VIP Tier Definitions

Replaces the binary VIP flag with a tiered system that reflects how different high-value player segments should be handled.

---

## Why tiers matter

A binary VIP flag treats a player who spent 50 euros last month the same as a player who has spent 2,000 euros over three years and has 50,000 followers on social media. The response strategy, compensation eligibility, and escalation path should differ between them.

Tiers also make the system honest. Not every player who contacts support is VIP. Calling everyone VIP devalues the designation and creates unrealistic expectations for agents.

---

## Tier definitions

### Tier 0: Standard player

No special handling. Standard SLA applies.

### Tier 1: Valued player

**Criteria:** Lifetime spend above threshold OR account age above threshold (set per game).

**Handling:**
- SLA: High (P3, 8 hours)
- Escalation: billing or technical team as normal
- Compensation: standard eligibility per compensation matrix
- Tone: warm and efficient

### Tier 2: High-value player

**Criteria:** Lifetime spend in top 10% of active players OR long-tenure player with consistent spend.

**Handling:**
- SLA: Urgent (P2, 4 hours)
- Escalation: routes to player relations for payment and account issues, not billing
- Compensation: elevated eligibility, lower approval threshold
- Tone: personalised, senior-voice
- Note: do not send a template without account context review

### Tier 3: VIP player

**Criteria:** Lifetime spend in top 1-2% OR content creator / competitive player with significant audience OR manually designated by player relations team.

**Handling:**
- SLA: Critical (P1, 30 minutes)
- Escalation: always to player relations, never to general billing or technical queue
- Compensation: maximum eligibility, senior agent or player relations approval required
- Tone: senior-voice only. Dedicated agent if possible.
- Churn risk: any negative signal triggers immediate escalation regardless of issue type
- Note: player relations must review account history before first contact

---

## Configuration

Tier thresholds are set per game in `.env` or a config file:

```
VIP_TIER1_LIFETIME_SPEND=50
VIP_TIER2_LIFETIME_SPEND=500
VIP_TIER3_LIFETIME_SPEND=2000
VIP_TIER1_ACCOUNT_AGE_DAYS=365
```

Manual tier overrides are set in the support platform player profile. Manual designations always take precedence over spend thresholds.

---

## How tiers interact with the triage engine

The engine checks VIP tier from the ticket context. Tier 2 and Tier 3 players trigger the elevated routing and SLA rules described above. Tier 1 players get the standard routing but the tone guidance shifts to warm and efficient.

Churn risk combined with any VIP tier always escalates to player relations at the tier's SLA.
