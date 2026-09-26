# Agent Instructions 
 
## Project Rules 
- Read REQUIREMENTS.md before implementing. 
- Read SPEC.md before implementing. 
- Read ARCHITECTURE.md before architectural changes. 
- Follow TASKS.md. 
- Prefer small, focused changes. 
- Do not invent business requirements. 
- Do not modify REQUIREMENTS.md or SPEC.md to make tests pass. 
- Do not delete or weaken tests. 
- Do not add dependencies without justification. 
- Do not implement behavior for NFR-02 or NFR-03 (authentication, TLS, audit log, rate limiting): they are explicitly out of scope in this delivery (C-05).
- Do not modify `data/customers.json` outside T-01; it is fixture data, not a place to patch failing tests.
- Commit after each completed task, referencing the task ID (C-06).
 
## Validation 
- Run pytest before and after changes. 
- Add tests for new behavior. 
- Report changed files and test results. 
- Stop and ask for clarification if requirements conflict. 
 
## Definition of Done 
- Relevant tests pass. 
- Acceptance criteria are covered. 
- No unrelated files are changed. 
- Documentation reflects final behavior. 