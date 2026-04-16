# Extending the Agent

How to safely add new capabilities, update existing logic, and verify that changes work before claiming improvement.

---

## Guiding principle

Every change to this system has a risk. The classifier, escalation rules, and system prompt interact. A signal added to fix one case can break another. Always test after changing anything.

---

## Adding a new issue type

**Files to change:** `engine/classifier.py`, `knowledge-base/decision-table.md`, `evaluation/test-cases.md`

**Steps:**

1. Add the new intent to the `Intent` enum in `engine/classifier.py`:
```python
class Intent(str, Enum):
    PAYMENT_ISSUE = "payment_issue"
    YOUR_NEW_INTENT = "your_new_intent"  # Add here
```

2. Add keyword signals for the new intent:
```python
INTENT_SIGNALS = {
    Intent.YOUR_NEW_INTENT: [
        "signal one", "signal two", "signal three",
    ],
}
```

3. Add a routing rule in `engine/escalation.py`:
```python
ROUTING_TABLE = {
    Intent.YOUR_NEW_INTENT: "team_name",
}
```

4. Add a response action in `engine/response_router.py`:
```python
action_map = {
    Intent.YOUR_NEW_INTENT: "Description of what to do at Tier 1.",
}
```

5. Add information collection requirements:
```python
intent_collect_map = {
    Intent.YOUR_NEW_INTENT: ["Required field 1", "Required field 2"],
}
```

6. Add a row to `knowledge-base/decision-table.md`

7. Add at least two test cases to `evaluation/test-cases.md` (one straightforward, one edge case)

8. Run tests and the evaluation pipeline to check for regressions:
```bash
pytest tests/
python evaluation/scripts/fetch_tickets.py
python evaluation/scripts/evaluate_tickets.py
python evaluation/scripts/generate_report.py
```

---

## Adding a new escalation rule

**File to change:** `engine/escalation.py`

**Hard rule (always escalates):**
```python
if your_condition:
    hard_escalate = True
    reasons.append("description of why")
    notes_parts.append("What the receiving team needs to know.")
```

**Soft rule (escalates if Tier 1 already tried):**
```python
if your_condition and prior_resolution_attempted:
    soft_escalate = True
    reasons.append("description")
```

**After adding a rule:**
- Add a test case to `evaluation/test-cases.md` that specifically tests the new trigger
- Run `pytest tests/` and verify no existing tests broke
- Check `evaluation/failure-analysis.md` - does the new rule create a new failure mode?

---

## Updating the knowledge base

**Files to change:** Relevant file in `knowledge-base/`

**Steps:**

1. Edit or add content to the appropriate KB file
2. Re-sync ChromaDB:
```bash
python rag/kb_sync.py
```
3. Test retrieval with a relevant query:
```bash
python -c "
from rag.retriever import retrieve_and_format
context, results = retrieve_and_format('your test query')
for r in results:
    print(f'[{r[\"score\"]:.3f}] {r[\"source\"]} - {r[\"section\"]}')
"
```
4. Confirm the new content appears in results for relevant queries

**Do not add fictional policy.** KB content must reflect real documented policy. If the policy does not exist yet, document that the topic should escalate rather than inventing a rule.

---

## Adding a new test case

**File to change:** `evaluation/test-cases.md`

**Required fields for each test case:**
- Test ID (TC-031, TC-032, etc.)
- Scenario description
- User message (exact text)
- Expected classification
- Expected next action
- Should escalate: yes/no
- Escalation target (if yes)
- Required information to collect
- Common failure risk
- Pass criteria

**Rules for test cases:**
- Test cases must be testable, not vague
- Pass criteria must be specific enough that a reviewer can objectively determine pass or fail
- Do not add test cases that duplicate existing ones
- Add at least one edge case for every new issue type or escalation rule you add

---

## Modifying the system prompt

**File to change:** `system-prompt.md`

**This is the highest-risk change.** The system prompt governs all LLM behavior. Small changes can have large effects.

**Before changing:**
- Document why the change is needed
- Identify which existing behavior you expect to change
- Identify which existing behavior must not change

**After changing:**
1. Review all 30 test cases in `evaluation/test-cases.md` manually
2. Run the evaluation pipeline:
```bash
python evaluation/scripts/fetch_tickets.py
python evaluation/scripts/evaluate_tickets.py
python evaluation/scripts/generate_report.py
```
3. Compare the new report against the previous one
4. If escalation accuracy drops, revert and investigate
5. Log the change in `CHANGELOG.md` with the reason

**Never remove a hard prohibition from the system prompt without explicit sign-off.** Prohibitions exist for legal, trust, and safety reasons.

---

## Verifying changes before claiming improvement

A change is not an improvement unless it is verified. Verification means:

1. `pytest tests/` passes with no new failures
2. The evaluation pipeline report shows the target metric improved
3. The evaluation pipeline report shows no metric degraded significantly
4. At least two test cases specifically covering the change pass
5. The change is logged in `CHANGELOG.md`

Do not deploy prompt or classifier changes based on intuition alone. Run the pipeline.
