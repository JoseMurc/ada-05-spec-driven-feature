# Third-Party Skill Pre-Install Audit 
 
Repository: https://github.com/addyosmani/agent-skills 
Selected skill: code-review-and-quality 
Version / commit inspected: docs(code-review): answer the regression question with a mutation
Date: 26/09/2026
 
## Purpose 

Conduct multi-axis code review to assess code quality across multiple dimensions before it enters the main branch. The axis that amke the base for this skill are correctness, readability, architecture, security, and performance

This skill is intended to be used for code reviews (made by a human or an agent) that are prefered when making new implementations, before merges, changes, evaluations and  bugfixes.

## Trigger / Description 

It is triggered when a request is made to review a code change before a merge, whether it is your own code, code from another agent, or code from a human—including diffs or Pull Requests, or even code pasted directly into the chat.

The SKILL.md file does not include an explicit "do not use for..." section. There are no anti-triggers defined in the frontmatter.


## Supporting References 

The skill mentions—but does NOT include in this file—the following:
- `../../references/security-checklist.md`
- `../../references/performance-checklist.md`

It also recommends supplementing this with other skills from the same repository: `security-and-hardening`, `performance-optimization`, and `constraint-driven-development` (the latter for project-level mutation scores).

## Tools / Commands / Permissions 

It does not define custom scripts in `scripts/`. Instead, it instructs the agent to execute project-related commands:
- It runs the test suite (both before and after any changes to dependencies).
- It performs manual mutation testing: it inverts a condition, runs the tests, and then restores the original file.
- It suggests running `npm audit` to check for vulnerabilities in dependencies.

It neither requests nor requires any credentials. It does not interact with GitHub (it does not post comments, approve pull requests, or perform merges), it only examines local code or diffs.

## Potential Risks 
 
- It relies on external files (`security-checklist.md`, `rendimiento-checklist.md`) that are not included in this `SKILL.md`; if the full collection is not installed, the workflow may remain incomplete.
- It executes commands on the repository (tests, mutation testing, `npm audit`). Although these are limited to read-only/validation tasks, they do trigger processes on machine or within the CI environment, they are not 100% passive, unlike simply reading a file.
- It is an extensive and opinionated Skill: it may consume more context , and its criteria (e.g., "approx. 1000 lines is too large") might not be equally applicable to every project.
- It does not explicitly state the boundaries, these constraints are merely implied by the workflow description rather than being defined as an explicit rule.

## Decision 
[X] Install 
[ ] Do not install 
