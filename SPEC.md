# Customer Search Feature 
 
## Goal
Provide a local customer search by name or email via a single input field, returning normalized partial matches in a deterministic and bounded manner.

## Requirements Covered
- FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16
- NFR-01, NFR-02, NFR-03

NFR-02 and NFR-03 are marked as "Not applicable for this delivery" in REQUIREMENTS.md (C-05: single-user local execution). They are listed here because the scope of this increment explicitly defines their behavior—which is "none"—and this behavior is specified under "Error Handling."
## Scope

- A single search field that queries both name and email simultaneously (FR-01).
- Substring matching, case-insensitive and diacritic-insensitive (FR-02, FR-03).
- Trimming of leading and trailing whitespace; preservation of internal whitespace (FR-04).
- Queries that are empty or consist only of whitespace are treated as empty queries, with no search performed (FR-05).
- Explicit "no results" response when no matches are found (FR-06).
- Latency verification under sequential local load (NFR-01).
- Truncation to 50 results, with the total number of matches reported (FR-07).
- Deterministic sorting, with `customer_id` used as a tie-breaker (FR-08).
- A single data scope (the complete catalog) for any user performing a search (FR-09). - Whitelist of fields in the response: `cliente_id`, `nombre`, `email` (FR-10).
- Interactive session when the CLI is invoked without arguments, allowing repeated queries using the same search logic (FR-11).
- Welcome banner with instructions on how to exit (FR-12).
- Session persistence following an `EMPTY_QUERY` or `NO_RESULTS` outcome (FR-13).
- Session termination via `:salir`/`:exit`, or through terminal interruption/end-of-file (FR-14, A-12).
- Support for single-execution (one-shot) invocations with arguments (FR-15).
- Optional email-domain filter applied on top of the existing name/email match, with no effect when omitted or blank (FR-16).

## Out of Scope

- Session management, authentication, TLS, and audit logging (NFR-02 — not applicable, C-05).
- Rate limiting (NFR-03 — not applicable, C-05).
- Web interface, browser/OS/breakpoint compatibility matrix, and UI accessibility (NFR-04, NFR-05 — not applicable, C-04).
- Batch pagination or incremental scrolling (A-11: simple truncation with a total count provided).
- User roles and data partitioning (A-07; FR-09 is covered in its degenerate form—single scope).
- Fuzzy search, operators, and wildcards (Q-04, Q-06).

## Domain Model
Customer:
- `cliente_id`: str — a stable, unique identifier.
- `nombre`: str — free-text field for the full name (A-02).
- `email`: str — the customer's email address.
Storage: In-memory persistence or local JSON file (C-02). The indexing structure and internal normalization mechanism are technical decisions defined in `ARCHITECTURE.md`, not in this specification. ## Search Rules
- SR-01 [FR-01]: A query is compared simultaneously against `name` and `email`; the result is the union of matches from both fields, with no duplicates based on `client_id`.
- SR-02 [FR-02]: A match occurs when the normalized query appears as a substring anywhere within the normalized field (not just at the beginning).
- SR-03 [FR-03]: Before comparison, both the query and the indexed fields are normalized to lowercase, with all diacritics removed (e.g., á/à/â/ä → a, and similar).
- SR-04 [FR-04]: Leading and trailing spaces in the query are trimmed before normalization; internal spaces are preserved and included in the comparison.
- SR-05 [FR-05]: A query that is empty or consists solely of spaces is classified as an empty query and does not trigger a search.
- SR-06 [FR-07]: The result set is truncated to a maximum of 50 items; the response always includes the actual total number of matches, regardless of what that total may be.
- SR-07 [FR-08]: Ordering: (1) exact match, (2) match at the beginning of the field, (3) match at any position; within each group, results are sorted alphabetically by `name`, with `client_id` used as a tie-breaker.
- SR-08 [FR-09]: The authorized data scope is the entire catalog for any user performing a search; there are no partitions or roles in this increment (A-07).
- SR-09 [FR-10]: The response includes only `client_id`, `name`, and `email`; no other domain fields are included. 
- SR-10 [FR-11, FR-15]: If the CLI is invoked without arguments, an interactive session is initiated via the `InteractiveSession` controller, allowing for repeated queries using the existing search logic; if invoked with arguments (`python -m customer_search.cli "<query>"`), a single-execution (one-off) run is performed without starting an interactive session.
- SR-11 [FR-12]: Upon starting the interactive session, a welcome banner ("Welcome to the customer search tool") is displayed, along with instructions on the available exit commands (`:salir` and `:exit`).
- SR-12 [FR-11]: Each cycle of the interactive session prompts for a query using the fixed indicator `"Buscar cliente: "` and displays the retrieved results without terminating the session.
- SR-13 [FR-13]: For queries that result in `EMPTY_QUERY` or `NO_RESULTS`, the interactive session displays the corresponding message (FR-05, FR-06) and remains active, awaiting the next query.
- SR-14 [FR-14, A-12]: The interactive session terminates cleanly upon receiving an explicit exit command (`:salir` or `:exit`), without interpreting it as a search term or querying the repository.
- SR-15 [FR-16, A-13]: When a non-blank domain value is supplied, the result set from SR-01/SR-02 is further restricted to customers whose normalized email ends with the normalized domain; truncation (SR-06) and ordering (SR-07) are applied after this restriction.

## Validation Rules
- VR-01 [FR-01, FR-02]: Input is always treated as literal text; wildcards, operators, and regular expressions are not interpreted.
- VR-02 [FR-05]: There is no minimum query length other than the rule regarding empty queries (SR-05); a single non-empty character is a valid query and will be executed.
- VR-03 [FR-07]: The limit of 50 is not configurable by the caller; it is a fixed system value.
- VR-04 [FR-14, A-12]: A line entered during the interactive session is validated as an exit command if and only if, after trimming leading and trailing whitespace, it matches exactly ":salir" or ":exit" (case-insensitive); any other input is processed as a literal search term.
- VR-05 [FR-16, A-13]: A domain filter value that is empty or consists solely of spaces, after trimming, is treated as "no filter applied"; it never raises an error.

## Error Handling
- EH-01 [FR-05]: Empty query → no search is performed; the defined empty-query status is returned (without execution), and no error is thrown. - EH-02 [FR-06]: A query with no matches results in an empty list, a business status of `NO_RESULTS`, and a predefined fixed message; no error is thrown.
- EH-03 [NFR-02]: N/A — there is no session, authentication, or TLS channel in the single-user local scope (C-05); therefore, there are no authentication or transport errors to handle.
- EH-04 [NFR-03]: N/A — there is no rate limiting in the single-user local scope (C-05); therefore, there are no blocking responses (HTTP 429 or equivalent) to handle.
- EH-05 [FR-14]: A keyboard interrupt (`KeyboardInterrupt` / Ctrl+C) or end-of-file signal (`EOFError` / Ctrl+D / Ctrl+Z) at the interactive session prompt is handled gracefully, terminating the session without displaying exception stack traces or unhandled errors.

## Acceptance Criteria
- AC-01 [FR-01]: A query that matches only by name and a query that matches only by email each return the corresponding client.
- AC-02 [FR-01]: A client whose name and email both match the same query appears exactly once in the results.
- AC-03 [FR-02]: A query that matches within the middle or at the end of a field (not just at the beginning) returns the corresponding client.
- AC-04 [FR-03]: The queries "JOSÉ", "jose", and "José" all return the same set of results.
- AC-05 [FR-04]: The queries "ana" and " ana " return the same set of results, in the same order.
- AC-06 [FR-05]: A query consisting solely of spaces returns an "empty query" status, without performing a search and without triggering an error. - AC-07 [FR-06]: A query with no matches returns an empty list, a `NO_RESULTS` status, and the defined message.
- AC-08 [NFR-01]: Given a catalog of 1,000 clients, with a sequential load of 1 query per second, the observed latency is ≤ 50 ms at the p95 percentile and ≤ 100 ms at the p99 percentile.
- AC-09 [FR-07]: When there are more than 50 matches, the response contains exactly 50 items and the actual total number of matches.
- AC-10 [FR-08]: Executing the same query multiple times always yields the same order of results.
- AC-11 [FR-09]: Any user who executes the same query receives the same set of results.
- AC-12 [FR-10]: Each client object in the response contains only the keys `cliente_id`, `nombre`, and `email`.
- AC-13 [FR-08]: Given a set containing exact matches, prefix matches (matches at the beginning), and internal matches, the results are returned in that order, with ties broken alphabetically and by `cliente_id`.
- AC-14 [FR-11, FR-15]: Running the CLI without arguments launches an interactive session; running the CLI with arguments performs a one-off search without launching an interactive session.
- AC-15 [FR-12]: Upon launching the interactive session, a welcome banner ("Welcome to the client search tool") is displayed, along with instructions for the available exit commands (`:salir` and `:exit`).
- AC-16 [FR-11]: The interactive session prompts for queries using the fixed prompt "Buscar cliente: ", executing successive searches and displaying their corresponding results. 
- AC-17 [FR-13]: An empty query or one with no matches within an interactive session displays the expected message (EMPTY_QUERY or NO_RESULTS) and keeps the session active for the next search.
- AC-18 [FR-14, A-12]: The commands ":salir" and ":exit" (with or without leading/trailing spaces, and case-insensitive) terminate the interactive session without querying the repository; valid search terms containing the words "salir" or "exit" are executed as standard searches.
- AC-19 [FR-14]: Upon receiving a `KeyboardInterrupt` or `EOFError` during the interactive session prompt, the process terminates cleanly without outputting exceptions to the console.
- AC-20 [FR-16]: Given a query and a non-blank domain filter, only customers whose email domain matches it (case-insensitive, diacritic-insensitive) are returned; given the same query with the domain filter omitted or blank, the result set is identical to the one obtained before FR-16 existed.

## Test Scenarios
- TS-01 -> AC-01
- TS-02 -> AC-02
- TS-03 -> AC-03
- TS-04 -> AC-04
- TS-05 -> AC-05
- TS-06 -> AC-06
- TS-07 -> AC-07
- TS-08 -> AC-08 (latency measurement; not a unit test)
- TS-09 -> AC-09
- TS-10 -> AC-10
- TS-11 -> AC-11
- TS-12 -> AC-12
- TS-13 -> AC-13
- TS-14 -> AC-14
- TS-15 -> AC-15
- TS-16 -> AC-16
- TS-17 -> AC-17
- TS-18 -> AC-18
- TS-19 -> AC-19
- TS-20 -> AC-20

## Constraints
- C-01, C-02, C-03: Define the stack, persistence, and permitted dependencies for the entire implementation of this specification.
- C-05: Justifies why EH-03 and EH-04 are marked as N/A (as the implementation does not involve sessions, TLS, or rate limiting).
- C-08: Limits the dataset used in AC-08/TS-08 to ≤ 1,000 clients.
- C-04: Limits delivery to a local interface (CLI or local HTTP API); justifies why NFR-04 and NFR-05 do not apply. 

## Open Questions
N/A — all decisions required for FR-01–FR-16 and NFR-01–NFR-03 have already been addressed in REQUIREMENTS.md (Q-01 through Q-17, plus A-12 regarding interactive session exit commands and A-13 regarding the email-domain filter). There are no remaining open questions within the scope of this increment.