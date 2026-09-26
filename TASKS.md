# Tasks 
 
## T-01 Project setup
- Goal: Crear la estructura del proyecto y el dataset semilla, sin lógica de negocio todavía.
- Files: `pyproject.toml` (o `setup.cfg`), `src/customer_search/__init__.py`, `tests/__init__.py`, `data/customers.json` (dataset semilla, ≤ 1 000 clientes, C-08).
- Acceptance: El paquete `customer_search` es importable; `data/customers.json` contiene registros válidos con `cliente_id`, `nombre`, `email`.
- Verification: `pytest -v` corre sin errores de recolección (0 tests aún es válido); `python -c "import customer_search"` no falla.
- Status: Completed

## T-02 Domain model
- Goal: Implementar la entidad `Customer` y el `CustomerRepository` (Domain Model e Interfaces de ARCHITECTURE.md), sin reglas de búsqueda.
- Files: `src/customer_search/models.py`, `src/customer_search/repository.py`, `tests/test_models.py`, `tests/test_repository.py`.
- Acceptance: `Customer` expone `cliente_id`, `nombre`, `email` (SPEC.md Domain Model). `CustomerRepository.find_all()` lee `data/customers.json` y devuelve todos los registros sin filtrar, ordenar ni normalizar.
- Verification: `pytest tests/test_models.py tests/test_repository.py -v`; el conteo de registros devueltos coincide con el dataset semilla.
- Status: Completed

## T-03 Search logic
- Goal: Implementar normalización y las reglas de coincidencia, orden, truncamiento y proyección de campos (SR-01, SR-02, SR-03, SR-04, SR-06, SR-07, SR-08, SR-09).
- Files: `src/customer_search/normalization.py`, `src/customer_search/search_service.py` (clases `SearchService`, `SearchResult`, `CustomerView`), `tests/test_normalization.py`, `tests/test_search_service.py`.
- Acceptance: AC-01, AC-02, AC-03, AC-04, AC-05, AC-09, AC-10, AC-12, AC-13 de SPEC.md pasan (unión sin duplicados, subcadena en cualquier posición, insensibilidad a mayúsculas/diacríticos, equivalencia por espacios, truncamiento a 50 con total correcto, orden determinista, proyección a la lista blanca).
- Verification: `pytest tests/test_normalization.py tests/test_search_service.py -v -k "not empty and not no_results"`; corresponde a TS-01, TS-02, TS-03, TS-04, TS-05, TS-09, TS-10, TS-12, TS-13.
- Status: Not started

## T-04 Validation and errors
- Goal: Implementar el manejo de consulta vacía y consulta sin resultados (SR-05, EH-01, EH-02), incluyendo el mensaje fijo de "sin resultados".
- Files: `src/customer_search/search_service.py` (rama `EMPTY_QUERY` / `NO_RESULTS`), `src/customer_search/messages.py` (mensaje fijo de "sin resultados"), `tests/test_search_service.py` (casos añadidos).
- Acceptance: AC-06 y AC-07 de SPEC.md pasan (consulta solo de espacios devuelve `EMPTY_QUERY` sin invocar al repositorio; consulta sin coincidencias devuelve `NO_RESULTS` con el mensaje definido); ningún caso lanza excepción.
- Verification: `pytest tests/test_search_service.py -v -k "empty or no_results"`; corresponde a TS-06, TS-07.
- Status: Not started

## T-05 Tests
- Goal: Completar la cobertura de pruebas: interfaz (CLI o API) y latencia (NFR-01), integrando lo construido en T-02 a T-04.
- Files: `src/customer_search/cli.py` (o `api.py`, según ARCHITECTURE.md), `tests/test_cli.py` (o `test_api.py`), `tests/test_latency.py`, `tests/conftest.py` (fixtures del dataset).
- Acceptance: AC-08 pasa (p95 ≤ 50 ms, p99 ≤ 100 ms sobre 1 000 clientes, carga secuencial); la interfaz traduce correctamente cada `status` (`OK`, `EMPTY_QUERY`, `NO_RESULTS`) a su salida; suite completa de SPEC.md (AC-01 a AC-13) pasa en verde.
- Verification: `pytest -v` (suite completa) sin fallos; `tests/test_latency.py` reporta p50/p95/p99 y valida el umbral; corresponde a TS-08 y a la verificación end-to-end de TS-01 a TS-13.
- Status: Not started

## T-06 Documentation
- Goal: Dejar trazabilidad y documentación de uso, sin modificar REQUIREMENTS.md, SPEC.md ni ARCHITECTURE.md.
- Files: `README.md` (cómo ejecutar la interfaz y los tests), tabla de trazabilidad (Requirement -> SPEC/AC -> Task -> Files -> Test -> Status; puede vivir en `README.md` o en un archivo aparte).
- Acceptance: La tabla de trazabilidad cubre FR-01 a FR-10 y NFR-01 a NFR-03, cada uno con su AC, tarea, archivo y estado de prueba; el checklist de revisión humana de la Fase 10 (¿cumple REQUIREMENTS/SPEC?, ¿SPEC referencia sin redefinir?, ¿se inventaron reglas?, ¿ARCHITECTURE coincide con el código?) queda respondido.
- Verification: Revisión manual contra el checklist de la Fase 10; `pytest -v` sigue en verde tras cualquier ajuste de documentación (no debe tocar código de producción).
- Status: Not started