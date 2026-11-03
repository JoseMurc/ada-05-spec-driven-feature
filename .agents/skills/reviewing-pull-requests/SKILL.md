--- 
name: reviewing-pull-requests 
description: | 
  Reviews a Pull Request (or a local feature branch not yet opened as a PR) 
  for engineering readiness using the repository's requirements/specification/ 
  architecture docs, project rules (AGENTS.md), code changes, traceability 
  matrix and test evidence. Works equally against a GitHub PR or a local diff 
  when no remote PR exists yet. 
  Use when the user asks to review a PR, assess PR/branch readiness, 
  check a pull request or branch against requirements/spec, or produce a 
  readiness report before human review. 
  Do NOT use to implement issues, modify code, fix failing tests, 
  comment on GitHub, approve PRs, merge PRs, write changelogs/release 
  notes/commit summaries, or explain generic Git concepts. 
metadata:
  version: 1.0.0 
  owner: Jose Murcia 
  course: UADY-IS-AI 
--- 

# Reviewing Pull Requests 
 
## When to use

Use this skill for PR readiness reviews before human approval — including a 
local feature branch that has not been opened as an actual GitHub PR, reviewed 
entirely via `git log` / `git diff` / `git show` against the target branch. 

## Preconditions 

- Repository / PR / branch is accessible; read-only inspection is sufficient. 
  No GitHub access is required when the branch and its target base are 
  available locally. 
- `REQUIREMENTS.md`, `SPEC.md` and `ARCHITECTURE.md` exist and are used as 
  normative context when present. 
- `docs/Traceability.md` exists and maps requirements to code/tests; used to 
  verify coverage of every FR/AC touched by the diff. 
- `AGENTS.md` exists and defines project-level constraints (what must not be 
  modified, how tests must be treated); its rules apply during the review. 

## Workflow 

1. Identify the exact PR / branch / commit range to review: confirm it with 
   `git log`, `git diff <base>...<branch> --stat` and 
   `git merge-base <base> <branch>`. If the range is ambiguous (e.g. it 
   inherits a merge commit from another branch), fix the scope explicitly 
   instead of assuming it. 
2. Read `AGENTS.md` and the relevant `REQUIREMENTS.md` / `SPEC.md` / 
   `ARCHITECTURE.md` sections, and cross-check `docs/Traceability.md` for 
   coverage of every FR/AC touched by the diff. 
3. Inspect changed files and map them to the requested behavior. 
4. Identify and run the relevant tests (e.g. `pytest -v`); use the actual 
   pass/fail count as evidence, never a commit message or prior claim. 
5. Apply `references/review_checklist.md`. 
6. Classify findings using `references/severity_guide.md`, including branch/ 
   history hygiene issues (e.g. an unexpected merge commit inside the PR's 
   commit range) as SHOULD FIX. 
7. Create a draft report using `assets/review_report_template.md`. 
8. Run `scripts/validate_review_report.py` on the report. 
9. If validation fails, repair the report and validate again. 
10. Stop and present the report to the human reviewer. 

## Safety / Boundaries 

- Read-only review of GitHub/repository content. 
- Do not modify production code unless explicitly starting a new task. 
- Do not comment, approve or merge Pull Requests. 
- Do not weaken tests to remove findings, and flag any PR that already does so. 
- Do not treat a `REQUIREMENTS.md`/`SPEC.md` edit made to force tests to pass 
  as acceptable (AGENTS.md). 
- Do not produce changelogs, release notes or commit summaries — only the 
  structured readiness report. 
- Stop if `REQUIREMENTS.md` and `SPEC.md` conflict. 
- Stop and ask the human if the commit range of the PR/branch is ambiguous 
  rather than assuming its scope. 

## Output 

Create: 
results/pr-readiness-review.md 

The report must distinguish: 

- MUST FIX 
- SHOULD FIX 
- OPTIONAL 
- Human decision required
