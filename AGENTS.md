# Agent Instructions 

## Before you start
Make sure your terminal/editor is open directly in this folder (the one that contains this `AGENTS.md` file and `pyproject.toml`), not in a parent folder with the same name. If your first file reads fail with "file not found", that is almost always the reason — stop and open the correct folder instead of guessing with `find`/`ls`.

## Read First 
1. REQUIREMENTS.md 
2. SPEC.md 
3. ARCHITECTURE.md 
4. TASKS.md 
5. docs/REPO_MAP.md 

# Sources of Truth 
- Requirements live only in REQUIREMENTS.md. 
- Verifiable behavior lives in SPEC.md. 
- Do not change requirements/spec merely to make tests pass. 

# Repository Map 
- src/                  implementation 
- tests/                automated tests
- docs/                 architecture and operational context 
- docs/ada-history      architecture and operational context for past activities
- scripts/              deterministic checks 
- results/              generated evidence 
 
 ## Standard Commands 
- Install: `pip install -e .` 
- Run (single search): `python -m customer_search.cli "<term>"` 
- Run (interactive mode): `python -m customer_search.cli` 
- Test: use the exact commands from README.md, section 4 ("Ejecución de Pruebas"), do not improvise an equivalent command. Full suite: `pytest -v`. 
- Lint: ruff check .
- Verify: ./scripts/verify_repo.sh 

# Change Rules 
- Keep changes scoped to the requested task. 
- Do not weaken existing tests. 
- Do not introduce new dependencies without justification. 
- Do not modify secrets or generated files. 

## Stop Conditions 
Stop and ask for human input when: 
- requirements conflict, 
- a destructive action is required, 
- an architecture boundary must change, 
- a required external system is unavailable. 

## Project Rules 
- Read REQUIREMENTS.md before implementing. 
- Read SPEC.md before implementing. 
- Read ARCHITECTURE.md before architectural changes. 
- Follow TASKS.md. 
- For PR/branch readiness reviews (before human approval), use the `reviewing-pull-requests` Skill: read `.agents/skills/reviewing-pull-requests/SKILL.md` first, before improvising a review. 
- Prefer small, focused changes. 
- Do not invent business requirements. 
- Do not modify REQUIREMENTS.md or SPEC.md to make tests pass. 
- Do not delete or weaken tests. 
- Do not add dependencies without justification. 
- Do not implement behavior for NFR-02 or NFR-03 (authentication, TLS, audit log, rate limiting): they are explicitly out of scope in this delivery (C-05).
- Do not modify `data/customers.json` outside T-01; it is fixture data, not a place to patch failing tests.
- Commit after each completed task, referencing the task ID (C-06).
- Check the `.agents/skills` folder for any skill that could be used according to the prompt made.
 
## Validation 
- Run the pytest commands documented in README.md, section 4, before and after changes, use those commands as written instead of a different one that happens to cover the same tests. 
- Run `./scripts/verify_repo.sh ` (it runs `pytest -v`, `ruff check .`, ` scripts/check_repo_contract.py ` )
- Add tests for new behavior. 
- Report changed files and test results. 
- Stop and ask for clarification if requirements conflict. 
 
## Definition of Done 
- Relevant tests pass. 
- Acceptance criteria are covered. 
- No unrelated files are changed. 
- Documentation reflects final behavior. 