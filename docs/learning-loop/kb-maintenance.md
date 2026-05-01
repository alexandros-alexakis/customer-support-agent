# Knowledge Base Maintenance Guide

The KB is what the AI knows. If it goes stale, the AI goes stale.

---

## Who owns the KB

This is the most important decision before going live. The KB is not a technical artifact. It is a living document of your support policy and it needs an owner who understands that policy.

The KB owner should be a senior support ops person or team lead, not a developer. Someone with access to the policy team. Someone who is part of incident review so they know when policy changes.

If nobody owns the KB, it will drift. Agents will start noticing the AI gives outdated answers. They will stop trusting it.

---

## What is in the KB

The KB lives in `knowledge-base/`. Each file covers a topic: payment FAQ, refund policy, escalation rules, edge cases. Written in plain markdown. No developer needed to update it.

---

## What triggers a review

**Scheduled:** Monthly at minimum. Check that refund policies, escalation paths, FAQ answers, and gameplay-related content are still current.

**Event-triggered:**
- A game update that changes how purchases, items, or accounts work
- A policy change from payments, legal, or compliance
- An incident where the AI gave wrong answers at scale
- A change to team structure or escalation paths
- A new issue type appearing in the queue the KB does not cover

**Learning loop candidates:** When the loop surfaces a KB candidate for review, that is also a trigger. See [overview.md](overview.md).

---

## The review process for learning loop candidates

1. **Is the answer accurate?** Does it match current policy?
2. **Is the answer complete?** Does it cover the edge cases in the original question?
3. **Is the answer general enough?** Can it handle slight variations in phrasing?
4. **Who owns this entry?** Someone needs to be responsible for keeping it updated.

---

## How to add a KB entry

1. Create or edit a file in `knowledge-base/`
2. Write the content in plain markdown. Use clear headings.
3. Run `python rag/kb_sync.py` to re-index
4. Test with `python run_agent.py --message "[question the entry should answer]"`
5. Confirm the retrieval score improved

---

## Signs the KB is degrading

- Escalation rate climbing without a corresponding increase in ticket volume
- Gap tracker logging the same question repeatedly without a KB update
- Agents manually correcting AI responses on the same topic repeatedly
- CSAT dropping on a specific ticket type

Any of these is a signal to review the KB, not just the next scheduled date.
