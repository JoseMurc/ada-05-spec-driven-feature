# PR Review Checklist 
## Requirements / Specification 
- Changed behavior maps to an existing Requirement / Acceptance Criterion
- No undocumented business rule is introduced. 
- SPEC and implementation are consistent. 

## Code 
- Change is focused and understandable. 
- Error handling is appropriate. 
- No unrelated refactoring is mixed into the PR. 
- Dependencies are justified (AGENTS.md: no new dependency without justification). 

## Tests 
- The test suite was actually executed (e.g. `pytest -v`), not just inspected; the real pass/fail count is reported as evidence. 
- New behavior has automated evidence. 
- Important edge cases are covered. 
- Existing behavior is not weakened or deleted. 
- Tests verify behavior, not only implementation details.
 
## Architecture 
- Change respects documented boundaries. 
- ARCHITECTURE.md is updated if the design changed. 

## Traceability 
- `docs/Traceability.md` (or equivalent) is updated for every new/changed FR/AC touched by the diff. 
- Every changed requirement ID in REQUIREMENTS.md/SPEC.md maps to the files and tests that implement it. 

## Process 
- The branch was created from the expected base (e.g. `develop`), not from a branch that already merged a different PR. 
- The PR's commit range does not silently include an unrelated merge commit 
- Commits reference their task ID and are incremental per task (AGENTS.md, C-06). 

## Security 
- No secrets or credentials. 
- No unnecessary permissions. 
- External input is validated where required. 

## Evidence 
- Findings cite file/commit/test/requirement evidence, not general impressions. 