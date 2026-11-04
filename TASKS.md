# Tasks 
 
## T-01 Project setup
- Goal: Create the project structure and the seed dataset, without any business logic yet.
- Files: `pyproject.toml` (or `setup.cfg`), `src/customer_search/__init__.py`, `tests/__init__.py`, `data/customers.json` (seed dataset, ≤ 1,000 customers, C-08).
- Acceptance: The `customer_search` package is importable; `data/customers.json` contains valid records with `cliente_id`, `nombre`, and `email`.
- Verification: `pytest -v` runs without collection errors (0 tests is still acceptable); `python -c "import customer_search"` does not fail.
- Status: Completed

## T-02 Domain model
- Goal: Implement the `Customer` entity and the `CustomerRepository` (Domain Model and Interfaces from ARCHITECTURE.md), without any search rules.
- Files: `src/customer_search/models.py`, `src/customer_search/repository.py`, `tests/test_models.py`, `tests/test_repository.py`.
- Acceptance: `Customer` exposes `cliente_id`, `nombre`, and `email` (SPEC.md Domain Model). `CustomerRepository.find_all()` reads `data/customers.json` and returns all records without filtering, sorting, or normalizing.
- Verification: `pytest tests/test_models.py tests/test_repository.py -v`; the count of returned records matches the seed dataset.
- Status: Completed

## T-03 Search logic
- Goal: Implement normalization and rules for matching, ordering, truncation, and field projection (SR-01, SR-02, SR-03, SR-04, SR-06, SR-07, SR-08, SR-09).
- Files: `src/customer_search/normalization.py`, `src/customer_search/search_service.py` (classes `SearchService`, `SearchResult`, `CustomerView`), `tests/test_normalization.py`, `tests/test_search_service.py`.
- Acceptance: AC-01, AC-02, AC-03, AC-04, AC-05, AC-09, AC-10, AC-12, and AC-13 from `SPEC.md` are met (union without duplicates, substring matching at any position, case/diacritic insensitivity, equivalence regarding spaces, truncation to 50 characters with an accurate total count, deterministic ordering, and projection based on an allowlist).
- Verification: `pytest tests/test_normalization.py tests/test_search_service.py -v -k "not empty and not no_results"`; corresponds to TS-01, TS-02, TS-03, TS-04, TS-05, TS-09, TS-10, TS-12, and TS-13.
- Status: Completed

## T-04 Validation and errors
- Goal: Implement normalization and rules for matching, ordering, truncation, and field projection (SR-01, SR-02, SR-03, SR-04, SR-06, SR-07, SR-08, SR-09).
- Files: `src/customer_search/normalization.py`, `src/customer_search/search_service.py` (classes `SearchService`, `SearchResult`, `CustomerView`), `tests/test_normalization.py`, `tests/test_search_service.py`.
- Acceptance: AC-01, AC-02, AC-03, AC-04, AC-05, AC-09, AC-10, AC-12, and AC-13 from `SPEC.md` are met (union without duplicates, substring matching at any position, case/diacritic insensitivity, equivalence regarding spaces, truncation to 50 characters with an accurate total count, deterministic ordering, and projection based on an allowlist).
- Verification: `pytest tests/test_normalization.py tests/test_search_service.py -v -k "not empty and not no_results"`; corresponds to TS-01, TS-02, TS-03, TS-04, TS-05, TS-09, TS-10, TS-12, and TS-13.
- Status: Completed

## T-05 Tests

- Goal: Complete test coverage for the interface (CLI or API) and latency (NFR-01), integrating the components built in T-02 through T-04.
- Files: `src/customer_search/cli.py` (or `api.py`, as per ARCHITECTURE.md), `tests/test_cli.py` (or `test_api.py`), `tests/test_latency.py`, `tests/conftest.py` (dataset fixtures).
- Acceptance: AC-08 is met (p95 ≤ 50 ms, p99 ≤ 100 ms for 1,000 customers, sequential load); the interface correctly maps each `status` (`OK`, `EMPTY_QUERY`, `NO_RESULTS`) to its corresponding output; the full test suite defined in SPEC.md (AC-01 through AC-13) passes.
- Verification: `pytest -v` (full suite) runs with no failures; `tests/test_latency.py` reports p50/p95/p99 metrics and validates against the defined thresholds; corresponds to TS-08 and the end-to-end verification for TS-01 through TS-13.
- Status: Completed

## T-06 Documentation
- Goal: Establish traceability and usage documentation, without modifying `REQUIREMENTS.md`, `SPEC.md`, or `ARCHITECTURE.md`.
- Files: `README.md` (instructions on how to run the interface and tests), and a traceability matrix (Requirement -> SPEC/AC -> Task -> Files -> Test -> Status; this may reside in `README.md` or a separate file).
- Acceptance: The traceability matrix covers FR-01 through FR-10 and NFR-01 through NFR-03, with each entry including its corresponding acceptance criteria (AC), task, file, and test status. The human-review checklist from Phase 10, addressing questions such as "Does it meet the requirements/specifications?", "Does the specification reference items without redefining them?", "Were any rules invented?", and "Does the architecture align with the code?", must be completed.
- Verification: Manual review against the Phase 10 checklist; `pytest -v` must remain "green" (passing) following any documentation updates (production code must not be altered).
- Status: Completed

## T-07 Interactive session controller
- Goal: Implement the `InteractiveSession` class in `src/customer_search/session.py`, including the constants `WELCOME_BANNER` and `EXIT_COMMANDS`, and the methods `is_exit_command`, `handle_input`, and `run()`. The implementation must support dependency injection for `service`, `input_fn`, and `output_fn`.
- Files: `src/customer_search/session.py`, `tests/test_session.py`.
- Acceptance: Complies with SR-11, SR-12, SR-13, SR-14, VR-04, and EH-05; covers AC-15, AC-16, AC-17, AC-18, and AC-19 from `SPEC.md`. The banner displays "Welcome to the customer search tool" along with exit instructions (`:salir` and `:exit`). A persistent prompt, `"Buscar cliente: "`, repeatedly requests search terms. Valid queries trigger a search and display formatted results. In the event of an `EMPTY_QUERY` or `NO_RESULTS`, the appropriate message is displayed, and the session remains active. The commands `:salir` and `:exit` (case-insensitive and allowing for optional whitespace) terminate the session without querying the repository. `KeyboardInterrupt` and `EOFError` are handled gracefully, preventing unhandled exceptions.
- Verification: `pytest tests/test_session.py -v` passes with 100% coverage; corresponds to TS-15, TS-16, TS-17, TS-18, and TS-19.
- Status: Completed

## T-08 CLI dispatcher integration
- Goal: Modify `src/customer_search/cli.py` to distinguish between invocations with arguments and those without, delegating to `InteractiveSession` when no arguments are provided.
- Files: `src/customer_search/cli.py`, `tests/test_cli.py`.
- Acceptance: Satisfies SR-10, FR-11, and FR-15, and covers AC-14 from `SPEC.md`. `build_parser()` configures the `query` argument with `default=None`. When `main()` is called without arguments (`args.query is None`), it instantiates and executes `InteractiveSession(service=search_service).run()`. When `main(["<query>"])` is called with an argument, it preserves the existing single-execution behavior.
- Verification: `pytest tests/test_cli.py -v` passes 100%; this corresponds to TS-14 and covers regression testing for existing CLI use cases.
- Status: Completed

## T-09 Traceability and documentation update
- Goal: Update the documentation and the traceability matrix to record the new requirements (FR-11 through FR-15) and their corresponding test coverage and tasks.
- Note: The restriction from T-06 ("do not modify REQUIREMENTS.md, SPEC.md, or ARCHITECTURE.md") applied to the FR-01–FR-10 increment. This increment introduces new requirements (FR-11 through FR-15); therefore, T-09 explicitly updates these documents. The updates are limited to adding the new requirements, rules, and components, without redefining existing ones.
- Files: `docs/Traceability.md`, `README.md`, `ARCHITECTURE.md`, `REQUIREMENTS.md`, `RESEARCH.md`, `SPEC.md`, and `TASKS.md`.
- Acceptance: The traceability matrix in `docs/Traceability.md` includes FR-11 through FR-15, linked to SR-10–SR-14, VR-04, EH-05, AC-14–AC-19, T-07, and T-08. `README.md` documents the interactive use of the CLI without arguments.
- Verification: Manual consistency review across `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `docs/Traceability.md`, and `README.md`; the full `pytest -v` test suite passes.
- Status: Completed