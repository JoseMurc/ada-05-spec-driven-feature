## Skill Iteration 

Version: 1.0.0 (the skill version doesn't change)

### Observed failure:
Ran the execution test from step 15 in the ADA document (prompt below) in a fresh coding-agent session, with no explicit mention of the Skill's path:

```
Revisa el PR n# 3 e indica si está listo para una revisión humana.

Utiliza los requisitos/especificaciones del repositorio y las evidencias de las pruebas.
No realices ninguna publicación en GitHub.
Genera la revisión de forma local en:
results/pr-readiness-review.md
```

The agent did not discover the `reviewing-pull-requests` Skill or the `.agents/skills/` folder. It produced a `results/pr-readiness-review.md` that ignored `assets/review_report_template.md` (wrong structure, missing the MUST FIX/SHOULD FIX/OPTIONAL split), never applied `references/review_checklist.md` or `references/severity_guide.md`, omitted test evidence that the real workflow would have surfaced, and added unrequested content that was outside the Skill's declared scope. That output was discarded.

After the agent's failure to generate the `results/pr-readiness-review.md`, a second fresh session was asked directly "do you detect the `reviewing-pull-requests` skill?" — it answered yes and located `SKILL.md` on its own, so the Skill folder itself was not broken. A third fresh session was then given the **same original prompt** plus one added sentence making the path explicit:

> "Toda la info relacionada con la skill que se necesitará está en `.agents/skills/reviewing-pull-requests`, como `SKILL.md` y en el resto de directorios también."

With that addition, the third session found and used the Skill correctly and produced a structurally valid `results/pr-readiness-review.md` (verified below).

### Root cause:
**Boundary:** the failure was an inconsistent auto-discovery of `.agents/skills/` across coding-agent sessions/tools. `SKILL.md`'s `description` only helps once the Skill is in the candidate set; here it sometimes never reached that set. The one file every session in this project reliably reads is `AGENTS.md` (per the course's own convention), so that's the most appropiate place to put anything that we need the agent to see always.

### Change:
Added two line to `AGENTS.md` → Project Rules:

-  *"For PR/branch readiness reviews (before human approval), use the `reviewing-pull-requests` Skill: read `.agents/skills/reviewing-pull-requests/SKILL.md` first, before improvising a review."* This gives any session, even one whose host tool doesn't auto-index `.agents/skills/`,  a reliable, always-read pointer to the Skill before it attempts to improvise a review from scratch.

-  *"Check the `.agents/skills` folder for any skill that could be used according to the prompt made."* This gives any session a reliable, always-read pointer to the skill folder (`.agents/skills/`), avoiding  any mistake caused by not detecting the folder,

### Evidence after change:
The `results/pr-readiness-review.md` produced by the third (successful) session was validated against `scripts/validate_review_report.py`:

```
$ python .agents/skills/reviewing-pull-requests/scripts/validate_review_report.py results/pr-readiness-review.md
VALID: PR readiness review structure is complete.
exit code: 0
```

It correctly follows the template structure, cites `pytest -v` output (65/65 passed) as test evidence, applies the severity guide and ends with `Human decision required: YES` without approving, commenting on, or merging anything.

Result:
PASS for the Skill's own content and workflow (confirmed structurally valid, scope-respecting output once discovered), change already applied to `AGENTS.md` and already verified ith a cold start prompt. 

### NOTE:

The change made was applied to AGENTS.md to allow any agent to locate the skill, the skill itself wasn't changed, therefore the skill version remains the same 