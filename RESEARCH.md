# Research Report: Customer Search Repository

## 1. Current Functionality

The repository currently implements a local customer search capability (`customer-search`) developed following a Spec-Driven Development workflow.

### Core Features
- **Unified Single-Field Search (FR-01, SR-01)**:
  - Users provide a single search query that simultaneously queries both the customer's full name (`nombre`) and email address (`email`).
  - Search results represent the union of matches across both fields with deduplication based on unique customer identifier (`cliente_id`).
- **Substring Matching & Normalization (FR-02, FR-03, SR-02, SR-03)**:
  - Substring matching matches queries anywhere within target fields (not limited to prefix).
  - Search is case-insensitive and diacritic-insensitive. Normalization decomposes characters via Unicode NFKD and strips combining diacritical marks (`Mn` category), handling acute accents, graves, circumflexes, umlauts, and tildes (e.g., `José` / `jose` / `JOSÉ` return identical results).
- **Whitespace Handling (FR-04, SR-04)**:
  - Strips leading and trailing whitespace from the query.
  - Internal whitespace is preserved and included in substring comparisons.
- **Empty & Whitespace-Only Queries (FR-05, SR-05, EH-01)**:
  - Queries that are empty or contain only whitespace immediately return a structured empty result (`status = "EMPTY_QUERY"`, `items = []`, `total = 0`) without invoking the repository or raising exceptions.
  - A single non-whitespace character is a valid query (VR-02).
- **Zero-Match Results (FR-06, EH-02)**:
  - When no records match, the service returns `status = "NO_RESULTS"`, `items = []`, `total = 0`, and a predefined system message in Spanish (`NO_RESULTS_MESSAGE`):
    `"No se encontraron clientes que coincidan con la búsqueda. Por favor, revise o limpie el término de búsqueda."`
- **Result Truncation & Total Match Count (FR-07, SR-06, VR-03)**:
  - Limits returned items to a maximum of 50 records.
  - Always reports the true total count of matching records (`total`), even when matches exceed 50.
  - Truncation is direct; batch pagination or infinite scroll are not implemented (A-11).
- **Deterministic 3-Tier Ranking & Tie-Breaking (FR-08, SR-07)**:
  - Matches are sorted into three priority tiers:
    1. **Tier 1 (Exact Match)**: Normalized query exactly equals normalized name or normalized email.
    2. **Tier 2 (Prefix Match)**: Normalized name or normalized email starts with the normalized query.
    3. **Tier 3 (Substring Match)**: Normalized query is a substring anywhere within normalized name or normalized email.
  - Within each tier, ties are broken deterministically by:
    1. Alphabetical order of normalized name.
    2. Alphabetical order of raw name.
    3. Ascending order of `cliente_id`.
- **Security & Scope Boundary (FR-09, FR-10, SR-08, SR-09)**:
  - All users query the entire catalog without data partitioning or role-based filtering (FR-09 in single-scope mode).
  - Whitelist projection: Results expose strictly `cliente_id`, `nombre`, and `email` through `CustomerView`. No internal entity attributes are exposed.
- **Interfaces**:
  - Command-Line Interface (`customer_search.cli`) accepting an optional query argument and rendering human-readable outputs formatted by result status (`OK`, `EMPTY_QUERY`, `NO_RESULTS`).
  - Python programmatic API via `SearchService.search(query)`.

---

## 2. Current Architecture

The codebase follows a decoupled 3-tier architecture as detailed in `ARCHITECTURE.md`:

```
+-----------------------------------------------------------+
|               CLI / Entry Point Layer                     |
|              (customer_search.cli)                        |
+-----------------------------------------------------------+
                            |
                            | calls search(query)
                            v
+-----------------------------------------------------------+
|              Domain & Search Service Layer                |
|          (customer_search.search_service)                 |
|   - Normalization (customer_search.normalization)         |
|   - Fixed Messages (customer_search.messages)             |
|   - Ranking, Tiering, Deduplication, Truncation           |
|   - Data Projection (Customer -> CustomerView)            |
+-----------------------------------------------------------+
                            |
                            | calls find_all()
                            v
+-----------------------------------------------------------+
|                 Repository Layer                          |
|             (customer_search.repository)                  |
|   - Reads raw storage without filter, sort, or normalize  |
+-----------------------------------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|                 Persistence Layer                         |
|               (data/customers.json)                       |
+-----------------------------------------------------------+
```

### Component Roles & Responsibilities
1. **Presentation Layer (`customer_search.cli`)**:
   - Parses CLI arguments (`argparse`).
   - Delegates to `SearchService.search(query)`.
   - Formats user-facing output according to the result status (`format_output`).
   - Contains zero search or business logic.
2. **Business / Service Layer (`customer_search.search_service`, `normalization`, `messages`)**:
   - Concentrates all business rules (SR-01 to SR-09) and error-handling decisions (EH-01, EH-02).
   - Sanitizes and normalizes input queries via `normalization.py`.
   - Directly intercepts empty/whitespace queries before data access.
   - Executes multi-field matching, deduplication, tiering, sorting, truncation, and field projection.
   - Emits standardized data contracts (`SearchResult`, `CustomerView`).
3. **Data Access Layer (`customer_search.repository`, `models`)**:
   - Defines the raw domain entity `Customer` (`models.py`).
   - `CustomerRepository` encapsulates JSON file loading (`data/customers.json`).
   - `find_all()` retrieves the entire dataset without filtering, sorting, or normalizing.
   - Supports dependency injection of custom file paths for isolated testing.
4. **Data Layer (`data/customers.json`)**:
   - Flat JSON file containing 1,000 customer records.

---

## 3. Relevant Files

### Specification & Guidance Documentation
- `REQUIREMENTS.md`: Foundational source of truth defining functional requirements (FR-01 to FR-10), non-functional requirements (NFR-01 to NFR-05), open questions resolved (Q-01 to Q-16), constraints (C-01 to C-08), and assumptions (A-01 to A-11).
- `SPEC.md`: Technical specification detailing scope, out-of-scope boundaries, domain models, search rules (SR-01 to SR-09), validation rules (VR-01 to VR-03), error handling (EH-01 to EH-04), acceptance criteria (AC-01 to AC-13), and test scenario mappings (TS-01 to TS-13).
- `ARCHITECTURE.md`: High-level system design, layer responsibilities, data flow, interfaces, error handling strategy, testing strategy, design decisions, and architectural trade-offs.
- `TASKS.md`: Task breakdown covering T-01 through T-06 with goals, affected files, acceptance criteria, verification commands, and status.
- `AGENTS.md`: Operational instructions and guardrails for coding agents (strict prohibition on inventing business requirements, altering requirements/spec files to pass tests, modifying fixture data, or weakening tests).
- `README.md`: Project overview, architecture summary, installation guide, CLI usage guide, test execution instructions, and Phase 10 human review checklist.
- `docs/Traceability.md`: Traceability matrix linking requirements to spec rules, tasks, implementation files, test cases, and completion statuses.
- `results/agent-report.md`: Historical execution report and verification benchmarks.

### Source Code (`src/customer_search/`)
- `src/customer_search/__init__.py`: Package initialization; exposes `__version__ = "0.1.0"`.
- `src/customer_search/models.py`: Domain entity `Customer` with `cliente_id`, `nombre`, and `email`.
- `src/customer_search/messages.py`: User-facing message constant `NO_RESULTS_MESSAGE`.
- `src/customer_search/normalization.py`: Utility functions `remove_diacritics`, `normalize_text`, and `normalize_query`.
- `src/customer_search/repository.py`: `CustomerRepository` implementation and `DEFAULT_DATA_PATH`.
- `src/customer_search/search_service.py`: Core logic: `SearchService`, `SearchResult`, and `CustomerView`.
- `src/customer_search/cli.py`: CLI entry point (`main`, `build_parser`, `format_output`).

### Test Suite (`tests/`)
- `tests/__init__.py`: Test package initialization.
- `tests/conftest.py`: Shared pytest fixtures (`seed_dataset_path`, `seed_customers`, `search_service`, `sample_customers`).
- `tests/test_models.py`: Unit tests for `Customer` dataclass initialization, equality, and validation.
- `tests/test_repository.py`: Unit tests for `CustomerRepository` against seed data, empty datasets, and preservation of raw data.
- `tests/test_normalization.py`: Unit tests for text normalization, diacritic stripping, and query trimming.
- `tests/test_search_service.py`: Unit tests verifying acceptance criteria AC-01 to AC-07 and AC-09 to AC-13.
- `tests/test_cli.py`: Integration tests for CLI parsing, output formatting, and exit codes across status branches.
- `tests/test_latency.py`: Performance benchmark validating latency threshold on 1,000 customers (p95 <= 50 ms, p99 <= 100 ms).

### Data & Configuration
- `data/customers.json`: Seed dataset consisting of 1,000 customer objects (`cliente_id`, `nombre`, `email`).
- `pyproject.toml`: Build system configuration using `setuptools`, Python requirement `>=3.11`, and pytest settings (`pythonpath = ["src"]`, `testpaths = ["tests"]`).

---

## 4. Existing Task Data Model

### A. Domain Entities & Data Contracts
The domain and contract structures are implemented as Python dataclasses:

1. **`Customer` (`customer_search.models`)**:
   ```python
   @dataclass
   class Customer:
       cliente_id: str  # Stable unique identifier (e.g., "CUST-0001")
       nombre: str      # Full name as free text (unsplit name/surname)
       email: str       # Customer email address
   ```

2. **`CustomerView` (`customer_search.search_service`)**:
   ```python
   @dataclass
   class CustomerView:
       cliente_id: str  # Exposed identifier
       nombre: str      # Customer full name
       email: str       # Customer email address
   ```
   *Purpose: Strict whitelist projection ensuring no extraneous domain or persistence attributes escape to consumers (FR-10, SR-09).*

3. **`SearchResult` (`customer_search.search_service`)**:
   ```python
   @dataclass
   class SearchResult:
       items: list[CustomerView]   # Truncated list of results (max 50)
       total: int                  # Actual total match count before truncation
       status: str                 # "OK" | "EMPTY_QUERY" | "NO_RESULTS"
       message: Optional[str] = None  # Populated with NO_RESULTS_MESSAGE on NO_RESULTS
   ```

4. **Persistence Structure (`data/customers.json`)**:
   A JSON array of 1,000 objects:
   ```json
   [
     {
       "cliente_id": "CUST-0001",
       "nombre": "José García",
       "email": "jose.garcia@example.com"
     }, ...
   ]
   ```

### B. Task Model Structure (`TASKS.md`)
The project utilizes a structured task definition pattern for engineering activities:
- **Task Identifier**: `T-XX <Name>`
- **Goal**: Functional and technical objective of the task.
- **Files**: Specific files created or modified.
- **Acceptance**: Specification rules and acceptance criteria to be fulfilled.
- **Verification**: Exact test executions or CLI commands required to validate completion.
- **Status**: Lifecycle state (`Completed`).

---

## 5. Existing Tests

The repository maintains an automated test suite executed with `pytest`. All 28 tests pass in ~0.75 seconds.

### Test Breakdown by Module

| File | Number of Tests | Focus / Target |
| :--- | :---: | :--- |
| `tests/test_models.py` | 3 | Creation, dataclass equality, missing mandatory field validation. |
| `tests/test_repository.py` | 3 | Full dataset reading (1,000 records), empty file handling, strict preservation of raw order and characters (no sorting/normalization). |
| `tests/test_normalization.py` | 3 | Diacritics stripping (acute, grave, circumflex, umlaut, tilde), text lowercasing, whitespace trimming with internal space preservation. |
| `tests/test_search_service.py` | 13 | Business rules & Acceptance Criteria:<br>- `test_ac01_name_and_email_match` (FR-01 / AC-01)<br>- `test_ac02_deduplication` (FR-01 / AC-02)<br>- `test_ac03_substring_match` (FR-02 / AC-03)<br>- `test_ac04_case_and_diacritics_equivalence` (FR-03 / AC-04)<br>- `test_ac05_whitespace_equivalence` (FR-04 / AC-05)<br>- `test_ac06_empty_query_does_not_call_repository` (FR-05 / AC-06, EH-01)<br>- `test_ac07_no_results_returns_empty_list_and_fixed_message` (FR-06 / AC-07, EH-02)<br>- `test_ac09_truncation_to_50_with_real_total` (FR-07 / AC-09)<br>- `test_ac10_deterministic_order` (FR-08 / AC-10)<br>- `test_ac11_user_scope_unrestricted` (FR-09 / AC-11)<br>- `test_ac12_field_projection_whitelist` (FR-10 / AC-12)<br>- `test_ac13_ranking_and_tie_breaking` (FR-08 / AC-13) |
| `tests/test_cli.py` | 6 | Formatting and status translation for `OK`, `EMPTY_QUERY`, and `NO_RESULTS`; execution of `main()` with standard output capture. |
| `tests/test_latency.py` | 1 | Non-functional benchmark (NFR-01 / AC-08): Executes 100 sequential searches across 10 query variants over the 1,000-customer dataset. Asserts p95 <= 50.0 ms (observed: ~5.5 ms) and p99 <= 100.0 ms (observed: ~7.7 ms). |

---

## 6. Potential Constraints

### Technical & Environmental Constraints
- **Runtime Environment (C-01)**: Must run on Python 3.11+. The testing framework must be strictly `pytest`.
- **Zero Third-Party Production Dependencies (C-03)**: Only Python standard library modules (`dataclasses`, `unicodedata`, `json`, `pathlib`, `argparse`, `statistics`, `time`) are permitted. External libraries require formal justification.
- **Persistence Constraints (C-02)**: Storage is constrained to local memory or local JSON files (`data/customers.json`). No external database engine (SQL, NoSQL, SQLite) is allowed.
- **Interface Constraints (C-04)**: Interfaces are strictly local (CLI or local HTTP API). Web UIs, frontend frameworks, cross-browser compatibility, and web accessibility standards (NFR-04, NFR-05) are out of scope.
- **Execution Model (C-05)**: Single-process, single-user execution. Authentication, TLS encryption, audit logging, and rate limiting (NFR-02, NFR-03) are explicitly excluded.
- **Dataset Size & Scalability Bounds (C-08, NFR-01)**: The dataset is bounded to <= 1,000 customers. Because `CustomerRepository.find_all()` loads the full dataset into memory on every query and linear scans are performed, any new feature modifying data handling must maintain the p95 <= 50 ms latency threshold.

### Process & Agent Governance Constraints
- **Spec-Driven Governance (`AGENTS.md`)**:
  - `REQUIREMENTS.md` is the single source of truth for functional and non-functional requirements.
  - No business rules may be invented outside the specification.
  - `REQUIREMENTS.md` and `SPEC.md` must never be modified to force failing tests to pass.
  - Existing tests must not be deleted, disabled, or weakened.
  - `data/customers.json` is a fixed seed/fixture dataset and must not be altered to patch test failures.
- **Version Control Constraints (C-06)**: Git commits must be incremental and explicitly reference corresponding task IDs.
- **Contract Stability**: External consumers depend on `SearchResult` and `CustomerView` shapes. Changes to these contracts affect both the service layer and the presentation layer.
