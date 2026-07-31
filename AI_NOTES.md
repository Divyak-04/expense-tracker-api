# AI Notes

<!--
DRAFT — Divya, replace the bracketed parts with what's actually true
once you've read through the code and run it yourself. See the note
at the end of this file for why that matters.
-->

## 1. What was AI-generated vs. written by me

- The overall structure (FastAPI app in `src/main.py`, Pydantic
  models in `src/models.py`, JSON-file storage in `src/storage.py`,
  and the test suite in `tests/test_expenses.py`) was scaffolded with
  AI assistance (Claude).
- [Describe what you personally changed, added, or rewrote —
  e.g. renamed variables, changed an endpoint's response shape,
  added/removed a test case, fixed something that didn't match your
  understanding of the requirements, adjusted error handling, etc.
  Be specific — this is the part reviewers weight most heavily.]

## 2. What I validated or tested, and why

- Ran `pytest tests/ -v` locally — all 11 tests pass. [Confirm this
  yourself on your machine and note the actual result.]
- Started the server with `uvicorn src.main:app --reload` and manually
  exercised each endpoint with `curl` / the `/docs` Swagger UI:
  adding an expense, listing/filtering by category, checking totals,
  checking the monthly summary, and deleting an expense.
- [Add anything specific you checked — e.g. "confirmed a negative
  amount is rejected with a 422", "confirmed deleting a non-existent
  id returns 404", "restarted the server and confirmed expenses.json
  persisted the data" — and say *why* you checked it, e.g. because
  the spec calls it out explicitly, or because it's an edge case AI
  output commonly gets wrong.]

## 3. AI suggestions I didn't use, and why

- [If you asked for or were offered alternatives — e.g. a different
  storage approach (SQLite vs. JSON file), UUID vs. integer ids, a
  different validation strategy — note what you didn't take and your
  reasoning. If nothing was offered/declined, say so honestly rather
  than inventing something.]

---
**Note to self before submitting:** this section is explicitly graded,
and a generic or copy-pasted AI_NOTES.md costs marks even with solid
code. Fill it in only with things you actually did — read the three
source files end to end, run the server and the tests yourself, and
write down what you genuinely checked and changed. If something in
the code doesn't make sense to you, that's worth fixing or asking
about before you submit, not glossing over.
