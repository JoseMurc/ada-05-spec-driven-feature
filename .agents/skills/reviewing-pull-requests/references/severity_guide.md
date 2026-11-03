# Finding Severity Guide 

## MUST FIX 
Use when the change: 
- Violates a Requirement or Acceptance Criterion. 
- Introduces a regression. 
- Breaks tests required by the specification. 
- Creates a security or data integrity problem. 
- Violates an explicit AGENTS.md rule (e.g. REQUIREMENTS.md/SPEC.md edited to force tests to pass, a test deleted or weakened to remove a failure). 
- Makes the PR unsafe to approve. 

## SHOULD FIX 
Use when the feature works but there is a significant 
maintainability, testability, architecture or clarity problem. 

## OPTIONAL 
Use for non-blocking improvements that do not affect 
the approved behavior or safety. 