# Requirements — Customer Search 
 
## User Story 
As a user, 
I want to search customers by name or email, 
so that I can quickly find the customer record I need. 
 
## Functional Requirements
- FR-01: The system shall provide a single search field that queries both the customer's name and email attributes simultaneously, returning the union of all matches with duplicates removed.
- FR-02: The system must return substring matches that are case-insensitive and diacritic-insensitive, applied equally to both the name and email fields.
- FR-03: The system shall return the same set of results, in the same order, for search terms that differ only in terms of case or diacritics (acute, grave, and circumflex accents, as well as diaereses).
- FR-04: The system shall return the same set of results, in the same order, for search terms that differ only by the presence of whitespace characters at the beginning or end.
- FR-05: The system shall treat a query consisting solely of whitespace as an empty query, returning an empty result set with an explicit status, without performing a search and without triggering an error.
- FR-06: The system shall return an empty list, a business status code of `NO_RESULTS`, and a fixed, system-defined message when no matches are found.
- FR-07: The response shall contain no more than 50 items and must always include the total number of matches; any excess results are truncated, with no pagination mechanism provided.
- FR-08: The system shall sort results based on exact matches, followed by the position of the match, with ties broken alphabetically and then by customer identifier.
- FR-09: The system shall return results based on the data scope authorized for the user performing the search; for this release, the authorized scope is the complete catalog for all users, with no partitioning or role-based restrictions.
- FR-10: The system shall return only the `cliente_id`, `nombre`, and `email` fields in the response; no other fields from the data model shall be exposed in the results. - FR-11: When the CLI is executed without arguments, the system shall initiate an interactive session that repeatedly prompts for search terms, processes each term using the existing search logic (FR-01 through FR-10), and outputs the results.
- FR-12: Upon starting the interactive session, the system shall display a welcome message along with instructions on how to exit.
- FR-13: The interactive session shall remain active following a query that results in an `EMPTY_QUERY` or `NO_RESULTS` state, displaying the corresponding outcome (FR-05, FR-06).
- FR-14: The system shall allow the interactive session to be terminated via explicit exit commands or through terminal interruption/end-of-file (EOF) signals, without interpreting these actions as search terms.
- FR-15: A single-execution invocation with arguments (e.g., `python -m customer_search.cli "<query>"`) shall maintain its current behavior.
- FR-16: The system shall support an optional email-domain filter. When a domain value is supplied alongside the query, the result set shall be restricted to customers whose normalized email ends with that domain; when the domain filter is omitted or blank, search behavior is unchanged from FR-01 through FR-10.

## Non-Functional Requirements
- NFR-01: The search endpoint shall respond in ≤50 ms at the 95th percentile and ≤100 ms at the 99th percentile, under a sustained load of 1 query per second, against a catalog of 1,000 customers.
- NFR-02: Not applicable to this release — C-05 excludes session management, authentication, and TLS for a local, single-process, single-user execution. (Original text, applicable only if the scope expands to a network-exposed deployment: "All access to the search function must occur over TLS 1.2+, require an authenticated session, and be recorded in an audit log—capturing the user, timestamp, normalized search term, and number of results—without storing the customer's personal data in the log.")
- NFR-03: Not applicable to this release — C-05 explicitly excludes rate limiting for a local, single-user execution. Original text, applicable only if the scope changes to a multi-user deployment exposed over a network: "The endpoint must implement rate limiting of 60 requests per minute per user; if exceeded, it shall respond with an HTTP 429 status code without revealing client information."
- NFR-04: Not applicable to this delivery — C-04 excludes any web interface; there are no browsers, operating systems, or breakpoints to verify. Original text, applicable only if a web interface is added: "The search interface must be operable without loss of functionality or horizontal scrolling across all browser/OS/breakpoint combinations."
- NFR-05: Not applicable to this delivery — C-04 excludes any web interface; there are no UI components to audit for keyboard or screen reader accessibility. Original text, applicable only if a web interface is added: "The search field must be keyboard-navigable, include an accessible label, and announce the number of results."

## Open Questions
- Q-01: Which client statuses are searchable? 
  - Decision: All records in the dataset are searchable; client statuses are not modeled (A-07).
- Q-02: How is the data scope defined by role/user (i.e., what does each role see)? 
  - Decision: A single, full-access scope over the local dataset; there are no roles or partitions (A-07, C-05). FR-09 is verified using a single-profile matrix.
- Q-03: Is "Name" a single free-text field, or are first and last names separate? Is it possible to search by last name only?
  - Decision: a single free-text field for the full name; since matching is based on substrings, searching by surname alone works without the need for a dedicated field (A-02, A-01).
- Q-04: What type(s) of partial matching are supported (prefix, substring, per-token, all-tokens, fuzzy), and do they apply equally to both name and email? 
  - Decision: Substring matching at any position; case-insensitive and diacritic-insensitive; identical logic for both name and email (A-01). Fuzzy matching is not supported.
- Q-05: Does the list of results update as the user types, or only after an explicit submission? 
  - Decision: Only after an explicit submission (command or request); there is no incremental update per keystroke (C-04).
- Q-06: Are operators or wildcards supported in the input, or is all text treated strictly as a literal string? 
  - Decision: All input is treated as a literal string; operators, wildcards, and regular expressions are not supported.
- Q-07: What are the sorting criteria and their order of priority (e.g., exact match, match position, status, recency, alphabetical)? 
  - Decision: Exact match first, followed by a match at the beginning of the field, then a match at any position. Within each group, results are sorted alphabetically by name, with `client_id` used as a tie-breaker (A-04, FR-08). Status and recency are not used (A-07).
- Q-08: What is the maximum number of results per response (<N>)? 
  - Decision: N = 50, accompanied by the total number of matches (A-05, FR-07).
- Q-09: What mechanism is used to access the remaining results (e.g., pagination, incremental scrolling, etc.)? 
  - Decision: Simple truncation at N, with the total count provided; no batch pagination or incremental scrolling (A-11). 
- Q-10: Which customer fields are visible in the results (allowlist), and which are considered sensitive? 
  - Decision: allowlist = {customer_id, name, email}; the domain model does not include sensitive fields (A-06).
- Q-11: What is the exact text (per language) for the "no results" message, and what action does it offer? 
  - Decision: fixed text in a single language (Spanish), with no localization/i18n; the message suggests reviewing or clearing the search term (A-08, FR-06).
- Q-12: How does the screen behave when the query is empty—does it appear blank, show a default list, or something else? 
  - Decision: no search is executed; an empty result is returned with an explicit status and no error (A-03, FR-05).
- Q-13: What is the acceptable latency threshold (p95/p99), and under what load (QPS) and customer volume (<V>)? 
  - Decision: p95 ≤ 50 ms, p99 ≤ 100 ms, measured locally and sequentially (1 query per second) with 1,000 customers in memory (NFR-01, C-08, A-09). No concurrent load is specified.
- Q-14: What is the rate limit per user (<R> requests/minute) before blocking search access? 
  - Decision: R = 60 as a reference value; not implemented in this release per C-05 (NFR-03).
- Q-15: What audit controls are required for searches performed (log retention, anonymization)? 
  - Decision: not applicable to this release; C-05 excludes sessions and identifiable users; therefore, no audit log needs to be defined (NFR-02).
- Q-16: What is the official matrix of supported browsers, operating systems, and breakpoints (<matrix>)? 
  - Decision: Not applicable; the feature is delivered as a local CLI/API without a web interface (C-04, NFR-04, NFR-05).
- Q-17: How should the optional email-domain filter (FR-16) be compared, and what happens with an empty or whitespace-only domain value?
  - Decision: The domain comparison reuses the existing normalization rules (case-insensitive, diacritic-insensitive, FR-02/FR-03) and checks that the normalized email ends with the normalized domain. A domain value that is empty or consists solely of spaces is treated as "no filter applied" (A-13).

## Constraints
- C-01: The solution is implemented in Python 3.11+ using `pytest` as the sole testing framework.
- C-02: Data persistence is limited to memory or a local JSON file; no database engine is used.
- C-03: No paid services, APIs, or models are used; dependencies are restricted to the standard library plus `pytest`. Any additional dependency requires explicit justification.
- C-04: The feature is delivered as a local interface (CLI or local HTTP API); there is no web interface or mobile client, so the matrix for browsers, breakpoints, and UI accessibility does not apply.
- C-05: Execution is local, single-process, and single-user; there are no sessions, authentication, role-based authorization, TLS, or rate limiting.
- C-06: Version control is managed via Git, with incremental commits for each task.
- C-07: The code is generated by a coding agent and must be reviewed and validated by the developer before integration.
- C-08: The working dataset is a limited local dataset (≤ 1,000 clients), sufficient for functional and latency testing, but not for concurrent load testing. ## Assumptions
- A-01: A partial match is interpreted as a substring found at any position; it is case-insensitive and diacritic-insensitive, and applies equally to both the name and the email address.
- A-02: The customer name is a single free-text field containing the full name; first and last names are not modeled as separate fields.
- A-03: An empty query—or one consisting solely of spaces—does not trigger a search; instead, it returns an empty result set with an explicit status, without an error.
- A-04: The order of results is: exact match, followed by a match at the beginning of the field, followed by a match in any position; within each group, results are sorted alphabetically by name, with the customer identifier used as a tie-breaker.
- A-05: The maximum number of results per response is 50, accompanied by the total number of matches.
- A-06: The fields exposed in the results are identifier, name, and email; the domain model does not include fields classified as sensitive.
- A-07: All customers in the dataset are searchable; customer states (active, inactive, deleted) and data partitioning based on user scope are not modeled.
- A-08: User messages are provided in a single language using fixed text; no text catalog or internationalization is implemented.
- A-09: The performance threshold is verified locally and sequentially on the scoped dataset, with no concurrent load specified.
- A-10: A-01 through A-09 and A-11 are decisions made by the developer—who assumes the role of product owner in the absence of an external one—and are documented as such; any change to these decisions requires a review of the affected requirements prior to specification and testing.
- A-11: The mechanism for accessing results beyond the limit defined in FR-07 is simple truncation, with the total count provided; neither batch-based pagination nor incremental scrolling is implemented.
- A-12: A line entered during an interactive session is interpreted as an exit command only if, after trimming leading and trailing whitespace, it is exactly `:salir` or `:exit` (case-insensitive); any other text—even if it contains these strings—is treated as a search term. Commands are not considered valid search terms.
- A-13: The email-domain filter (FR-16) is applied after the existing name/email substring match (FR-01, FR-02), using the same normalization pipeline; an omitted or blank domain value leaves current search behavior unchanged.

Note: REQUIREMENTS.md is the source of truth for FR/NFR (functional/non-functional requirements).