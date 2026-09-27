

## (Traceability Matrix)

| Requisito | Regla SPEC / AC / TS | Tarea | Archivos de Código | Archivos de Prueba | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** (Unión nombre/email sin duplicados) | SR-01, AC-01, AC-02, TS-01, TS-02 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac01_name_and_email_match`, `test_ac02_deduplication`) | **Implementado & Probado** |
| **FR-02** (Coincidencia por subcadena insensible a caso/diacríticos) | SR-02, SR-03, AC-03, TS-03 | T-03 | `src/customer_search/normalization.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac03_substring_match`)<br>`tests/test_normalization.py` | **Implementado & Probado** |
| **FR-03** (Equivalencia ante mayúsculas/diacríticos) | SR-03, AC-04, TS-04 | T-03 | `src/customer_search/normalization.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac04_case_and_diacritics_equivalence`)<br>`tests/test_normalization.py` | **Implementado & Probado** |
| **FR-04** (Trim de espacios inicio/fin preservando internos) | SR-04, AC-05, TS-05 | T-03 | `src/customer_search/normalization.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac05_whitespace_equivalence`)<br>`tests/test_normalization.py` | **Implementado & Probado** |
| **FR-05** (Consulta vacía / solo espacios → EMPTY_QUERY) | SR-05, EH-01, AC-06, TS-06 | T-04 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac06_empty_query_does_not_call_repository`) | **Implementado & Probado** |
| **FR-06** (Sin coincidencias → NO_RESULTS con mensaje fijo) | EH-02, AC-07, TS-07 | T-04 | `src/customer_search/messages.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac07_no_results_returns_empty_list_and_fixed_message`) | **Implementado & Probado** |
| **FR-07** (Truncamiento a 50 con total real) | SR-06, VR-03, AC-09, TS-09 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac09_truncation_to_50_with_real_total`) | **Implementado & Probado** |
| **FR-08** (Orden exacto > prefijo > subcadena, desempate alfabético y cliente_id) | SR-07, AC-10, AC-13, TS-10, TS-13 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac10_deterministic_order`, `test_ac13_ranking_and_tie_breaking`) | **Implementado & Probado** |
| **FR-09** (Alcance de catálogo completo para todo usuario) | SR-08, AC-11, TS-11 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac11_user_scope_unrestricted`) | **Implementado & Probado** |
| **FR-10** (Lista blanca: cliente_id, nombre, email) | SR-09, AC-12, TS-12 | T-03 | `src/customer_search/search_service.py` (`CustomerView`) | `tests/test_search_service.py` (`test_ac12_field_projection_whitelist`) | **Implementado & Probado** |
| **NFR-01** (Latencia p95 ≤ 50 ms, p99 ≤ 100 ms en 1 000 clientes) | AC-08, TS-08 | T-05 | `src/customer_search/search_service.py` | `tests/test_latency.py` (`test_search_latency_nfr01`) | **Implementado & Probado** (p95: ~5.5 ms, p99: ~7.7 ms) |
| **NFR-02** (TLS, sesión, auditoría) | EH-03 | N/A | Ninguno | Ninguno | **Fuera de alcance** (C-05: ejecución local mono-usuario) |
| **NFR-03** (Rate limiting) | EH-04 | N/A | Ninguno | Ninguno | **Fuera de alcance** (C-05: ejecución local mono-usuario) |
| **NFR-04** (Interfaz web, matriz navegador/SO/breakpoint) | Out of Scope | N/A | Ninguno | Ninguno | **Fuera de alcance** (C-04: no existe interfaz web) |
| **NFR-05** (Accesibilidad de teclado/UI) | Out of Scope | N/A | Ninguno | Ninguno | **Fuera de alcance** (C-04: no existe interfaz web) |
 

