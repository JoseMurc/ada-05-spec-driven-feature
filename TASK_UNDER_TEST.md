# Task Under Test

Change ID: CR-001

## Goal
Add an optional email-domain filter to the existing customer search. When a domain value is entered with the search query, restrict the returned matches to customers whose email ends with that domain; when the domain filter is omitted or blank, search behavior must remain exactly as the actual system does.

## Requirements Covered
- FR-16
- AC-20

## Verification
- Automated tests proving that:
  - A query combined with a non-blank domain filter returns only customers whose normalized email ends with that domain.
  - The same query with the domain filter omitted or blank returns the same result set as before this change.
  - Domain comparison is case-insensitive and diacritic-insensitive, consistent with the existing normalization rules (FR-02, FR-03).

- Full existing test suite (`pytest -v`) must still pass with no regressions.

## Constraints
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.
