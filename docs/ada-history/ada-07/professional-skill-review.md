# Code Review: PR #3 — Interactive CLI Session (FR-11 to FR-15)

**Reviewer skill applied:** `code-review-and-quality` (five-axis review: correctness, readability, architecture, security, performance)
**Branch:** `pr-3` (GitHub PR #3) → base `main` / `develop` (identical merge-base)
**Head commit:** `2a76919` "FIX: Solution of 'should fix' fixes delivered by the agend on the 'Test' phase"
**Diff size:** 12 files changed, 948 insertions(+), 54 deletions(-) (≈650 lines excluding `RESEARCH.md`, which is a new research artifact, not a behavior change)

## Context

The PR implements an interactive REPL mode for the customer-search CLI (`FR-11`–`FR-15`): running `python -m customer_search.cli` with no arguments now starts a session (`InteractiveSession`) that repeatedly prompts for a query, reuses the existing `SearchService`, and exits on `:salir`/`:exit`, `Ctrl+C`, or EOF. The existing one-shot invocation (`python -m customer_search.cli "<query>"`) is preserved unchanged (`FR-15`). `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `docs/Traceability.md`, and `README.md` were updated in lockstep, with an explicit justification (`T-09` note) for touching spec files that an earlier task (`T-06`) had frozen.

New production code: `src/customer_search/session.py` (82 lines) and `src/customer_search/formatting.py` (26 lines, extracted from `cli.py`). `cli.py` was reduced by extracting `format_output` and adding a dispatch branch.

## Verification performed

- Checked out the PR head into an isolated worktree and ran `pytest -v`: **65/65 tests pass** (28 pre-existing + 37 new/modified), confirming the author's verification story.
- Read every changed line in the diff (code, tests, and spec/doc files), not just the stat summary.
- Mutation-tested `session.py`'s control flow by hand:
  - Inverted the loop's exit condition (`if not self.handle_input(...)` → `if self.handle_input(...)`): **13 tests failed**, correctly catching the mutant.
  - Weakened `is_exit_command` by dropping `.strip()`: **4 tests failed** (the whitespace-padded exit-command cases), correctly catching the mutant.
- Traced `FR-11`–`FR-15` through `SPEC.md` → `ARCHITECTURE.md` → `docs/Traceability.md` → test names to confirm every AC (`AC-14`–`AC-19`) has a corresponding assertion, and that the traceability table's file/test references match what's actually in the diff.
- Inspected commit history (`git log origin/main..pr-3`): the head commit shows this PR already went through one internal review/fix round (extracting `formatting.py`, adding the `A-12`/missing-test fixes) before being opened — the version reviewed here is the result of that round.

## Findings

### 1. Nit — Commit message violates the project's own change-description convention
- **Severity:** Nit (non-blocking, process hygiene)
- **Evidence:** Head commit `2a76919`: `"FIX: Solution of 'should fix' fixes delivered by the agend on the 'Test' phase"`
- **Engineering rationale:** This is close to the textbook anti-pattern example ("Fix bug") called out by this project's own review standard: it says nothing about *what* changed or *why*, isn't imperative/standalone, and contains a typo ("agend" → "agent"). Someone searching `git log` later for why `formatting.py` was extracted gets no signal from this message — they'd have to open the diff. The four other commits on this branch (`T-07`, `T-08`, `T-09`, and the I/O-defaults fix) follow a much better convention (task ID + concrete description).
- **Recommended action:** Not worth a rebase/amend at this point (the content is fine and tests pass), but ask the author to use descriptive, task-referencing messages for the *next* fix-up commit rather than "FIX: ...". No action required to merge.

### 2. Low — Architecture doc overclaims "no global monkeypatching" in the test strategy
- **Severity:** Low (documentation accuracy, not a functional defect)
- **Evidence:** `ARCHITECTURE.md` testing strategy section states: *"pruebas unitarias aisladas inyectando simulaciones de `input_fn` y `output_fn` (**sin monkeypatching global**)"*. However, `tests/test_session.py::test_default_session_uses_real_builtin_input` does exactly that:
  ```python
  monkeypatch.setattr("builtins.input", fake_input)
  session = InteractiveSession()
  session.run()
  ```
- **Engineering rationale:** The claim is true for the bulk of `test_session.py` (which does inject `input_fn`/`output_fn` per the DI design), but it is not true for the whole file — one test deliberately monkeypatches `builtins.input` to verify the default-wiring path (that `InteractiveSession()` with no args really falls back to the real `input`/`print`, per the "resolved at construction time, not at def time" fix from commit `b88ac1b`). That test is valuable and correctly placed; the documentation sentence is just slightly too absolute.
- **Recommended action:** Soften the sentence in `ARCHITECTURE.md`, e.g. "...inyectando simulaciones de `input_fn`/`output_fn` para la mayoría de los casos, salvo una prueba dedicada que verifica el cableado por defecto contra `builtins.input`." Cosmetic; does not block merge.

### 3. Informational — Unhandled exceptions from `SearchService.search()` inside the REPL loop are not caught
- **Severity:** FYI / informational (explicitly out of current spec scope, flagging as a residual risk, not a required fix)
- **Evidence:** `src/customer_search/session.py`, `run()`:
  ```python
  try:
      raw_input = self.input_fn(PROMPT)
  except (EOFError, KeyboardInterrupt):
      break
  if not self.handle_input(raw_input):
      break
  ```
  `handle_input` calls `self.service.search(raw_input)` outside any `try`/`except`. `EH-05` only specifies clean handling of `KeyboardInterrupt`/`EOFError` at the *input* prompt; it says nothing about exceptions raised by the service layer (e.g., a corrupted `data/customers.json` read mid-session).
- **Engineering rationale:** This matches the spec and architecture exactly as written (`ARCHITECTURE.md`: *"la lógica de negocio y validación de consultas vive en Search Service"* — error handling for data/business failures is explicitly out of this component's charter), so it is **not a defect against the current requirements**. It's worth recording because a REPL that crashes on an unexpected I/O error mid-session (instead of printing an error and continuing) is a rougher UX than a one-shot CLI that exits immediately either way. Flagging now avoids relitigating it as a "regression" later.
- **Recommended action:** No action required for this PR. If a future increment wants the interactive session to be resilient to backend failures (not currently a requirement), file it as a new FR/AC rather than retrofitting it silently.

### 4. Nit — `EXIT_COMMANDS` declared as mutable `set` rather than `frozenset`
- **Severity:** Nit
- **Evidence:** `src/customer_search/session.py`: `EXIT_COMMANDS: set[str] = {":salir", ":exit"}`
- **Engineering rationale:** It's used read-only (`in EXIT_COMMANDS`) everywhere in the diff and in tests, so there's no live bug. A `frozenset` would make the "this is a fixed constant" intent explicit and immune to accidental mutation by a future caller, consistent with it being declared as a module-level constant (upper-case naming already signals that intent).
- **Recommended action:** Optional; change to `frozenset({":salir", ":exit"})` at the author's discretion. Not required to merge.

## What I verified and found correct (no issues)

- **Spec traceability:** every new FR (`FR-11`–`FR-15`) maps to SR/VR/EH/AC entries in `SPEC.md`, and every AC (`AC-14`–`AC-19`) has at least one passing test; `docs/Traceability.md` was updated to match. No invented business rules found (`AGENTS.md` constraint honored).
- **One-shot path regression safety (FR-15):** `build_parser()`'s `query` default changed from `""` to `None`; `test_ac14_main_with_explicit_empty_arg_stays_one_shot` specifically distinguishes "no argument" (→ session) from "explicit empty-string argument" (→ one-shot `EMPTY_QUERY`), which is the correct, non-obvious edge case to pin down given the default changed.
- **Exit-command matching (`VR-04`, `A-12`):** `is_exit_command` strips and case-folds before an exact-match check against `{":salir", ":exit"}`. Tests cover case-insensitivity, surrounding whitespace, substrings that merely *contain* "exit"/"salir" (correctly treated as literal queries, including an email address and a name), and near-miss strings (`"::exit"`, `":exit:"`, `": salir"`) that must NOT match. This is a well-designed boundary with good negative-test coverage, and it exercises exactly the ambiguity the spec's `A-12` assumption was written to resolve.
- **No repository access on exit:** `test_ac18_exit_commands_terminate_session` asserts `spy_service.repository.find_all_calls == 0`, directly verifying `SR-14`'s "sin consultar el repositorio" requirement rather than just the session's exit behavior.
- **Signal handling (`EH-05`, `AC-19`):** `KeyboardInterrupt`/`EOFError` are caught at the single point they can occur (the `input_fn` call) and cause a clean `break`; both are tested independently.
- **Dependency injection correctness:** `input_fn`/`output_fn`/`service` defaults are resolved in `__init__` (not as mutable default arguments or module-load-time bindings), which was itself the subject of a prior fix commit (`b88ac1b`) and is now covered by `test_default_session_initialization` and `test_default_session_uses_real_builtin_input`.
- **Architecture fit:** Extracting `format_output` into `formatting.py` is the right move — it removes what would otherwise be a duplicated formatter between `cli.py` and `session.py`, and keeps `InteractiveSession` from depending on `cli.py` (avoids a layering inversion). `InteractiveSession` has zero business logic of its own; it only orchestrates I/O and delegates to the existing `SearchService`, consistent with the three-layer design and FR-09/FR-10's existing guarantees (which this PR does not touch or weaken).
- **Security:** No new external input surface beyond what the CLI already exposes (same `SearchService.search(str)` call); no secrets, no new dependencies, no injection vectors. Local, single-user, stdin/stdout only, consistent with `C-04`/`C-05`.
- **Performance:** No change to `SearchService` or `CustomerRepository`; `test_latency.py` (NFR-01) is untouched by this diff and was confirmed still green in the full run. The REPL loop does one `search()` call per line of input — no N+1, no unbounded loop beyond the user's own typing.
- **Change size:** ~650 lines of actual code/test diff (excluding the new `RESEARCH.md`) is on the large side of "acceptable" for a single logical change, but it is genuinely one cohesive feature (interactive mode) with its tests and documentation, not a mix of refactor + unrelated feature work, so splitting further would mostly fragment one coherent unit.

## Verdict

**Approve.** No Critical or Required issues found. All four findings above are Nit/Low/Informational and do not block merge; they are opportunities for incremental cleanup (commit message convention going forward, a documentation wording tweak, and an optional `frozenset`). The feature is correctly scoped to its spec, the test suite demonstrates real behavioral coverage (confirmed via targeted mutation testing, not just "tests exist"), and the refactor (`formatting.py` extraction) measurably reduces duplication rather than relocating it.

### Review checklist

- [x] Change matches spec/task requirements (FR-11–FR-15, SR-10–SR-14, VR-04, EH-05, AC-14–AC-19 all traced and tested)
- [x] Edge cases handled (empty arg vs. no arg, whitespace-padded/case-varied exit commands, substrings containing "exit"/"salir")
- [x] Error paths handled (EOFError, KeyboardInterrupt) — service-layer exceptions correctly left to service-layer scope (see Finding 3)
- [x] Tests cover the change adequately (mutation-tested two independent control-flow paths; both caught)
- [x] Names clear, logic straightforward, no unnecessary complexity
- [x] Follows existing patterns (DI for I/O, shared formatter, no business logic in presentation layer)
- [x] No secrets, no injection surface, no auth concerns (N/A for this scope)
- [x] No N+1/unbounded operations; NFR-01 unaffected
- [x] Tests pass (65/65), build succeeds, verification story documented and independently reproduced
