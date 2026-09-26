# Customer Search Feature (`ada-05-spec-driven-feature`)

Implementación local de la funcionalidad de búsqueda de clientes por nombre o correo electrónico, desarrollada con arquitectura guiada por especificación (Spec-Driven Development).

---

## 1. Descripción y Arquitectura

El sistema implementa una arquitectura desacoplada de tres capas conforme a [ARCHITECTURE.md](file:///C:/Users/ItzKe/Documents/9no_Semestre/Ingenieria%20asistida%20con%20IA/ada-05-spec-driven-feature/ada-05-spec-driven-feature/ARCHITECTURE.md):

```mermaid
flowchart LR
    A["CLI (Interfaz Local)<br/>customer_search.cli"] --> B["Search Service<br/>customer_search.search_service"]
    B --> C["Repository<br/>customer_search.repository"]
    C --> D[("Customer Data<br/>data/customers.json")]
```

- **CLI (`customer_search.cli`)**: Punto de entrada de línea de comandos. Parsea argumentos de entrada y formatea la salida de resultados y estados (`OK`, `EMPTY_QUERY`, `NO_RESULTS`).
- **Search Service (`customer_search.search_service`)**: Concentra toda la lógica de negocio:
  - Normalización de texto y eliminación de diacríticos (`customer_search.normalization`).
  - Búsqueda simultánea sobre nombre y email con coincidencia por subcadena sin duplicados (FR-01, FR-02).
  - Truncamiento a 50 resultados con reporte del total real (FR-07).
  - Ordenamiento determinista en 3 niveles de coincidencia con desempate alfabético e ID (FR-08).
  - Proyección de resultados a la lista blanca (`CustomerView`: `cliente_id`, `nombre`, `email`) (FR-10).
  - Manejo de consultas vacías y sin resultados con mensajes fijos (FR-05, FR-06).
- **Customer Repository (`customer_search.repository`)**: Abstrae la lectura de los clientes desde almacenamiento JSON (`data/customers.json`) sin aplicar filtros, orden ni normalización.

---

## 2. Instalación

Requiere **Python 3.11+** y `pytest`.

```powershell
# Clonar o ubicarse en la raíz del repositorio
# Instalar el paquete en modo editable
pip install -e .
```

---

## 3. Uso de la Interfaz (CLI)

Ejecutar la interfaz de línea de comandos mediante el módulo `customer_search.cli`:

```powershell
# 1. Búsqueda por coincidencia parcial en nombre
python -m customer_search.cli "carlos"

# 2. Búsqueda insensible a mayúsculas y diacríticos (á, é, í, ó, ú, ü, etc.)
python -m customer_search.cli "JOSÉ"
python -m customer_search.cli "jose"

# 3. Búsqueda por coincidencia en correo electrónico
python -m customer_search.cli "special"

# 4. Búsqueda con espacios al inicio y final (recortados automáticamente)
python -m customer_search.cli "   ana   "

# 5. Consulta vacía o solo espacios (devuelve estado EMPTY_QUERY sin ejecutar búsqueda)
python -m customer_search.cli "   "

# 6. Búsqueda sin coincidencias (devuelve estado NO_RESULTS con mensaje fijo)
python -m customer_search.cli "termino_inexistente"
```

---

## 4. Ejecución de Pruebas

La suite de pruebas automatizadas está construida con `pytest`:

```powershell
# Ejecutar todas las pruebas unitarias y de integración
pytest -v

# Ejecutar únicamente la prueba de latencia con reporte en consola (NFR-01 / AC-08)
pytest tests/test_latency.py -v -s

# Ejecutar pruebas específicas de normalización y servicio
pytest tests/test_normalization.py tests/test_search_service.py -v

# Ejecutar pruebas de la CLI
pytest tests/test_cli.py -v
```

---

## 5. Tabla de Trazabilidad (Traceability Matrix)

| Requisito | Regla SPEC / AC | Tarea | Archivos de Código | Archivos de Prueba | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** (Unión nombre/email sin duplicados) | SR-01, AC-01, AC-02 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac01_name_and_email_match`, `test_ac02_deduplication`) | **Implementado & Probado** |
| **FR-02** (Coincidencia por subcadena insensible a caso/diacríticos) | SR-02, SR-03, AC-03 | T-03 | `src/customer_search/normalization.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac03_substring_match`)<br>`tests/test_normalization.py` | **Implementado & Probado** |
| **FR-03** (Equivalencia ante mayúsculas/diacríticos) | SR-03, AC-04 | T-03 | `src/customer_search/normalization.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac04_case_and_diacritics_equivalence`)<br>`tests/test_normalization.py` | **Implementado & Probado** |
| **FR-04** (Trim de espacios inicio/fin preservando internos) | SR-04, AC-05 | T-03 | `src/customer_search/normalization.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac05_whitespace_equivalence`)<br>`tests/test_normalization.py` | **Implementado & Probado** |
| **FR-05** (Consulta vacía / solo espacios → EMPTY_QUERY) | SR-05, EH-01, AC-06 | T-04 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac06_empty_query_does_not_call_repository`) | **Implementado & Probado** |
| **FR-06** (Sin coincidencias → NO_RESULTS con mensaje fijo) | EH-02, AC-07 | T-04 | `src/customer_search/messages.py`<br>`src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac07_no_results_returns_empty_list_and_fixed_message`) | **Implementado & Probado** |
| **FR-07** (Truncamiento a 50 con total real) | SR-06, AC-09 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac09_truncation_to_50_with_real_total`) | **Implementado & Probado** |
| **FR-08** (Orden exacto > prefijo > subcadena, desempate alfabético y cliente_id) | SR-07, AC-10, AC-13 | T-03 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac10_deterministic_order`, `test_ac13_ranking_and_tie_breaking`) | **Implementado & Probado** |
| **FR-09** (Alcance de catálogo completo para todo usuario) | SR-08, AC-11 | T-03, T-05 | `src/customer_search/search_service.py` | `tests/test_search_service.py` (`test_ac11_user_scope_unrestricted`) | **Implementado & Probado** |
| **FR-10** (Lista blanca: cliente_id, nombre, email) | SR-09, AC-12 | T-03 | `src/customer_search/search_service.py` (`CustomerView`) | `tests/test_search_service.py` (`test_ac12_field_projection_whitelist`) | **Implementado & Probado** |
| **NFR-01** (Latencia p95 ≤ 50 ms, p99 ≤ 100 ms en 1 000 clientes) | AC-08, TS-08 | T-05 | `src/customer_search/search_service.py` | `tests/test_latency.py` (`test_search_latency_nfr01`) | **Implementado & Probado** (p95: ~5.5 ms, p99: ~7.7 ms) |
| **NFR-02** (TLS, sesión, auditoría) | EH-03 | N/A | Ninguno | Ninguno | **Fuera de alcance** (C-05: ejecución local mono-usuario) |
| **NFR-03** (Rate limiting) | EH-04 | N/A | Ninguno | Ninguno | **Fuera de alcance** (C-05: ejecución local mono-usuario) |

---

## 6. Checklist de Revisión Humana (Fase 10)

- **¿El código cumple con REQUIREMENTS.md y SPEC.md?**
  **Sí.** Se verificaron todos los requisitos funcionales FR-01 a FR-10 y el requisito no funcional NFR-01 mediante pruebas automatizadas (AC-01 a AC-13). NFR-02 y NFR-03 quedaron explícitamente fuera de alcance según C-05.
- **¿SPEC.md referencia sin redefinir requisitos?**
  **Sí.** SPEC.md toma las definiciones exactas de REQUIREMENTS.md sin alterar su semántica ni inventar nuevos comportamientos.
- **¿Se inventaron reglas de negocio fuera de la especificación?**
  **No.** Todas las reglas implementadas (SR-01 a SR-09, EH-01 y EH-02) provienen de SPEC.md y las decisiones documentadas en REQUIREMENTS.md (Q-01 a Q-16).
- **¿ARCHITECTURE.md coincide con el código implementado?**
  **Sí.** La separación en tres capas (CLI local, SearchService, CustomerRepository y JSON fixture) y las interfaces (`Customer`, `CustomerView`, `SearchResult`, `CustomerRepository`, `SearchService`) coinciden exactamente con la arquitectura diseñada.