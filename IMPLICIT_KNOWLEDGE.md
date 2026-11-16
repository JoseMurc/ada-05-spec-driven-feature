# Implicit Knowledge Found 

## IK-01
What:
README.md (part 4) already documents the canonical way to run the suite (`pytest -v`, plus specific subset commands for revelant modules) and during the CR-001 implementation, the agent ran `python -m pytest -q 2>&1 | tail -20` instead, not the one the project documents have because it validated against `pyproject.toml` and habit rather than reading README.md (part 4) first.

How was it discovered:
Noticed on review of the CR-001 session transcript, comparing the commands actually run against README.md.

Should this remain implicit?
NO

Where should it become explicit?
AGENTS.md should point directly at the topic 4 of README.md (or restate the exact command) under "Validation", so agents reuse the documented invocation instead of improvising an equivalent one.

## IK-02
What:
The path given to the agent as the working directory is the outer container, not the project root. The actual project (`pyproject.toml`, `src/`, `tests/`, `AGENTS.md`, `docs/`, etc.) lives one level deeper, in a same-named nested subfolder (`ada-05-spec-driven-feature/ada-05-spec-driven-feature/`), beacause te folder was created first and the the repository was cloned inside of it.

How was it discovered:
The agent's first `Read` calls (REQUIREMENTS.md, SPEC.md) failed with "File does not exist" at the given working directory; it then ran `find . -maxdepth 2 ...` to locate the real project folder before any file could be opened.

Should this remain implicit?
NO

Where should it become explicit?
A root-level note (or AGENTS.md) stating the real project path, so agents don't spend a round-trip discovering the nesting via failed reads.

## IK-03
What:
REQUIREMENTS.md and SPEC.md already fully specified FR-16/AC-20/SR-15/VR-05 (the email-domain filter) before TASKS.md had any corresponding task entry and before the code implemented it. Nothing marks a requirement as "specified but not yet built" vs. "specified and implemented" , TASK_UNDER_TEST.md itself didn't say which case applied.

How was it discovered:
The agent had to grep the whole repo (`domain|dominio|FR-16|AC-20|SR-15|VR-05`) across docs, source, and tests to determine implementation status, since no single document stated it directly.

Should this remain implicit?
NO

Where should it become explicit?
TASKS.md should carry a "Pending" task entry the moment a requirement is added to REQUIREMENTS.md/SPEC.md, so spec that are ahead of the already implemented code are visible without a searching the whole repository.