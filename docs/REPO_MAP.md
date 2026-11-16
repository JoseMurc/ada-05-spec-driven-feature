# Repository Map

## Entry Points
- `src/customer_search/cli.py` — dispatcher: parses args; with a query runs a one-off search, without args starts the interactive session (FR-11, FR-15)
- `src/customer_search/session.py` — `InteractiveSession`, the REPL loop for interactive mode 
- `src/customer_search/search_service.py` — `SearchService`, the only component with business logic (normalization, matching, ordering, truncation, projection)
- `src/customer_search/repository.py` — `CustomerRepository`, exposes the raw customer catalog (`find_all()`), no filtering/sorting
- `src/customer_search/formatting.py` — `format_output`, renders a `SearchResult` as text; shared by CLI and `InteractiveSession`
- `src/customer_search/models.py` — data types: `Customer`, `CustomerView`, `SearchResult`
- `src/customer_search/normalization.py` — text normalization helpers (diacritics/case) used by the Search Service
- `src/customer_search/messages.py` — fixed user-facing message constants (e.g. `NO_RESULTS`)
- `data/customers.json` — fixture customer data backing the repository; do not modify outside 

## Tests
- `tests/test_search_service.py` — normalization, matching, dedup, truncation, sorting, projection 
- `tests/test_repository.py` — repository read behavior, empty dataset, dataset at the C-08 limit
- `tests/test_session.py` — `InteractiveSession` unit tests with injected `input_fn`/`output_fn` mocks (banner, exit commands, EMPTY_QUERY/NO_RESULTS handling, EOFError/KeyboardInterrupt)
- `tests/test_cli.py` — integration: no-args triggers interactive mode, args trigger single-shot mode
- `tests/test_models.py` — data model behavior
- `tests/test_normalization.py` — normalization unit tests
- `tests/test_latency.py` — non-unit latency test (p95/p99) over 1,000 clients

## Change Guide
If changing search/CLI behavior:
1. Check `REQUIREMENTS.md` / `SPEC.md` — requirements and verifiable behavior live only there
2. Read `ARCHITECTURE.md` before any architectural boundary change
3. Update `src/customer_search/search_service.py` for business-rule changes, `src/customer_search/cli.py` or `session.py` for presentation/flow changes, `repository.py` only for data-access changes
4. Add or update tests under `tests/` (do not weaken existing tests)
5. Run `./scripts/verify_repo.sh` (runs `pytest -v`, `ruff check .`, `scripts/check_repo_contract.py`)
6. Follow `TASKS.md` and commit referencing the task ID (C-06)

## Do Not Edit Directly
- `data/customers.json` — fixture data, outside T-01 (per `AGENTS.md`)
- `REQUIREMENTS.md` / `SPEC.md` — to make tests pass (sources of truth, not test-fitting targets)
- `src/customer_search.egg-info/` — generated packaging metadata
- `.pytest_cache/`, `.ruff_cache/`, `**/__pycache__/` — generated caches
