# GitHub MCP Engineering Review — ADA-06

## 1. Repository

Owner / Repo: `JoseMurc/ada-05-spec-driven-feature`
Visibility: publico
Branch / reference analyzed: `Feat/Controlador-interactivo` (PR #3 --> `develop`), commits `7db07fc` a `2a76919`

## 2. MCP Connection

Server: `github-readonly` (`https://api.githubcopilot.com/mcp/`)
Mode: READ-ONLY (`X-MCP-Readonly: true`)
Toolsets:
- repos
- issues
- pull_requests

Total de tools expuestas y confirmadas en `/mcp`: 22, todas con operación Read (detalle completo en `docs/MCP_GITHUB_TOOL_INVENTORY.md`).

## 3. Repository Understanding

**Purpose:** Customer Search Feature desarrollada con Spec-Driven Development (SDD) para el curso de Ingeniería de Software asistida por IA (ADA-05): búsqueda local, determinista y acotada de clientes por nombre/email sobre un catálogo de hasta 1,000 registros, con objetivo de latencia p95 ≤ 50 ms / p99 ≤ 100 ms.

**Architecture summary:** Arquitectura de 3 capas:
- *Capa de presentación*: `cli.py` (dispatcher de un solo disparo vs. interactivo), `session.py` (`InteractiveSession`, REPL), `formatting.py` (`format_output`, compartido entre ambos modos).
- *Capa de logica de negocios*: `search_service.py` (`SearchService`: unión nombre/email, normalización, deduplicación, ranking determinista de 3 niveles, truncamiento a 50, proyección de campos), `normalization.py`, `messages.py`.
- *Capa de acceso de datos*: `repository.py` (`CustomerRepository.find_all()`) leyendo `data/customers.json`.

**Important files:** `pyproject.toml`, `REQUIREMENTS.md` (FR-01–FR-15, NFR-01–NFR-05, C-01–C-08, Q-01–Q-16), `SPEC.md` (SR-01–SR-14, VR-01–VR-04, EH-01–EH-05, AC-01–AC-19), `ARCHITECTURE.md`, `TASKS.md` (T-01–T-09), `docs/Traceability.md`.

**Tests:** `pytest`, organizados por criterio de aceptación (`conftest.py`, `test_models.py`, `test_repository.py`, `test_normalization.py`, `test_search_service.py`, `test_latency.py`, `test_cli.py`, `test_session.py`). Estado al momento del análisis: **65 tests, 100% pass, 0.71 s**.

## 4. Issue Analysis

**Issue:** #2 — "Añadir un controlador interactivo para buscador" (autor: `JoseMurc`, estado: open). Leída vía MCP real (`issue_read` ejecutada con éxito contra `github-readonly`).

**Facts from Issue:**
- Limitación actual: el programa solo se ejecuta en un solo disparo con el query como argumento (`python -m customer_search.cli "carlos"`).
- Solicitud: agregar un controlador interactivo / clase "session" que permita entrar a una interfaz inicial, hacer múltiples búsquedas en la misma terminal, mostrar resultados por cada búsqueda, y salir con comandos específicos.
- Debe preservarse el modo de un solo disparo original.

**Ambiguities (no explícitas en el Issue, resueltas luego en SPEC.md):**
- Comandos de salida exactos no definidos (resuelto como `:salir`/`:exit`, insensible a mayúsculas, con trim — `SPEC.md` VR-04, A-12).
- Manejo de `Ctrl+C`/`Ctrl+D` (`KeyboardInterrupt`/`EOFError`) no mencionado (resuelto en `SPEC.md` EH-05).
- Texto del prompt/banner no especificado (resuelto como `"Buscar cliente: "` — `SPEC.md` SR-11/SR-12).
- Comportamiento ante query vacía o sin resultados dentro de la sesión no especificado (resuelto: la sesión permanece activa — `SPEC.md` SR-13).

**Related requirements/spec:** FR-11 a FR-15 (`REQUIREMENTS.md`), SR-10 a SR-14, VR-04, EH-05, AC-14 a AC-19 (`SPEC.md`), T-07/T-08/T-09 (`TASKS.md`).

**Related code:** `cli.py` (`build_parser`, `main`), `session.py` (`InteractiveSession`), `formatting.py`. `search_service.py` se reutiliza sin cambios.

**Related tests:** `test_cli.py` (dispatcher: `test_build_parser_query_defaults_to_none`, `test_ac14_main_without_args_starts_interactive_session`, `test_ac14_main_with_args_runs_one_shot_without_session`, `test_ac14_main_with_whitespace_arg_stays_one_shot`, `test_ac14_main_with_explicit_empty_arg_stays_one_shot`), `test_session.py` (`test_ac15_*`, `test_ac16_*`, `test_ac17_*`, `test_ac18_*`, `test_ac19_*`).

## 5. Pull Request Review

**PR:** #3 — "Feat/controlador interactivo" (autor: `JoseMurc`, rama `Feat/Controlador-interactivo` --> `develop`, estado: open, 0 comentarios). Inspeccionada vía MCP / análisis de git log de los commits del PR, **sin comentar, aprobar, mergear ni cerrar**.

**Changed behavior:**
- Invocación sin argumentos ya no busca string vacío: inicia una sesión REPL persistente.
- Banner de bienvenida + prompt `"Buscar cliente: "` repetido hasta comando de salida.
- Terminación limpia con `:salir`/`:exit` (insensible a mayúsculas/espacios) o señales (`KeyboardInterrupt`/`EOFError`), sin stack traces.
- Modo de un solo disparo con argumento preservado sin cambios.

**Changed files (12 archivos, +948/-54):** código de presentación (`session.py` +82/-0, `cli.py` +17/-25, `formatting.py` +26/-0), tests (`test_session.py` +338/-0, `test_cli.py` +106/-0), y documentación/spec (`ARCHITECTURE.md`, `SPEC.md`, `REQUIREMENTS.md`, `TASKS.md`, `Traceability.md`, `README.md`, `RESEARCH.md`).

**Tests:** 38 tests nuevos/afectados específicos de este comportamiento (32 en `test_session.py`, 6 en `test_cli.py`); suite total 65/65 pasando.

**Observations / Risks / Questions / Potential defects:**

- **[OBSERVATION]** Separación limpia de responsabilidades: `format_output` se extrajo a `formatting.py` para evitar dependencia circular entre `cli.py` y `session.py`.
- **[OBSERVATION]** `InteractiveSession` acepta `input_fn`/`output_fn` inyectables, lo que permite testear sin parchear stdin/stdout globales.
- **[RISK]** La rama `Feat/Controlador-interactivo` se creó desde `main` después de mergear el PR #1, en vez de desde `develop`; el commit de merge `3a89bd5` queda incluido en el rango de commits del PR #3 contra `develop`, generando historial solapado (git lo resuelve sin conflicto, pero conviene revisar la topología antes de mergear).
- **[QUESTION]** ¿Debería `RESEARCH.md` (agregado en la raíz, +232 líneas) moverse a `docs/` junto con `Traceability.md`? No fue pedido explícitamente por el Issue #2.
- **[QUESTION]** La descripción del PR no incluye `Closes #2`/`Fixes #2`; el merge no cerrará automáticamente el Issue.
- **[POTENTIAL DEFECT]** Ninguno identificado: los 65 tests pasan, la lógica de negocio (`search_service.py`) permanece sin modificar, y los casos borde (falsos positivos de `:salir`/`:exit` en queries legítimas, señales de terminal, espacios) están cubiertos por tests dedicados.

**What a human reviewer should verify manually:**
1. Ergonomía real del REPL ejecutando `python -m customer_search.cli` en una terminal nativa (PowerShell/cmd/bash) y probando `Ctrl+C`/`Ctrl+D` interactivamente.
2. Topología de git: si `develop` debería estar sincronizada/rebaseada antes de mergear el PR #3.
3. Si el Issue #2 debe cerrarse manualmente o vincularse explícitamente en la descripción del PR.

## 6. Traceability — Issue → Requirement/Spec → PR → Code → Test

| Issue / Need | Requirement/Spec | PR | Code / Files | Test / Evidence | Estado |
|---|---|---|---|---|---|
| #2 — Controlador interactivo con búsquedas repetidas | FR-11, SR-10/SR-12 | PR #3 | `src/customer_search/cli.py`, `src/customer_search/session.py` | `tests/test_cli.py::test_ac14_main_without_args_starts_interactive_session`, `tests/test_session.py::test_ac16_multiple_consecutive_searches` | Covered |
| #2 — Banner de bienvenida con instrucciones de salida | FR-12, SR-11 | PR #3 | `src/customer_search/session.py` (`WELCOME_BANNER`) | `tests/test_session.py::test_ac15_banner_printed_on_run` | Covered |
| #2 — Sesión permanece activa ante query vacía / sin resultados | FR-13, SR-13 | PR #3 | `src/customer_search/session.py` | `tests/test_session.py::test_ac17_empty_query_keeps_session_active`, `test_ac17_no_results_keeps_session_active` | Covered |
| #2 — Salida por `:salir`/`:exit` o interrupción/EOF | FR-14, VR-04, EH-05, A-12 | PR #3 | `src/customer_search/session.py` (`EXIT_COMMANDS`, `is_exit_command`) | `tests/test_session.py::test_ac18_exit_commands_terminate_session`, `test_ac19_eof_error_terminates_gracefully`, `test_ac19_keyboard_interrupt_terminates_gracefully` | Covered |
| #2 — Modo de un solo disparo preservado | FR-15, SR-10 | PR #3 | `src/customer_search/cli.py` | `tests/test_cli.py::test_ac14_main_with_args_runs_one_shot_without_session` | Covered |
| _(inferencia, no explícita en el Issue)_ Prevenir acoplamiento `cli.py` ↔ `session.py` | _no tiene ID de requiremiento — decisión de diseño_ | PR #3 | `src/customer_search/formatting.py` | Cubierto indirectamente por `test_cli.py` y `test_session.py` (ambos usan `format_output`) | Covered (inferencia del agente, no un hecho del Issue) |

## 7. Permission Review

Ver detalle completo en `docs/MCP_GITHUB_PERMISSION_REVIEW.md`. Resumen:

- **Authentication:** Fine-grained PAT de la cuenta `JoseMurc`, repositorio único.
- **GitHub token permissions:** Contents / Issues / Pull requests en Read-only.
- **MCP read-only:** Confirmado — 22 tools expuestas, ninguna de escritura (`create_*`, `update_*`, `delete_*`, `merge_*`, `push_*` ausentes).
- **Enabled toolsets:** `repos`, `issues`, `pull_requests`.
- **Write capabilities exposed:** Ninguna (verificado explícitamente en la Fase 7: el agente concluyó que no podía crear Issues, comentar PRs ni modificar archivos con las tools disponibles).
- **Hallazgo adicional:** `get_file_contents` (toolset `repos`) está en el catálogo pero fue rechazada en tiempo de ejecución durante esta sesión — ver nota de "tool availability vs policy".

## 8. Security Notes

- **Credential exposure:** Ningún PAT fue versionado, capturado en pantalla ni incluido en este log.
- **Prompt injection:** El contenido del Issue #2 y del PR #3 se trató como datos a analizar (separando "facts" de "engineering inferences"), no como instrucciones ejecutables.
- **Excess permissions:** Ninguno detectado; PAT y toolsets acotados al mínimo necesario.
- **Repository scope:** Mitigado nombrando `OWNER/REPOSITORY` explícitamente en cada prompt, dado que `search_code`/`search_repositories` operan sobre todo GitHub.
- **Tool availability ≠ runtime policy:** Ver `docs/MCP_GITHUB_PERMISSION_REVIEW.md` — una tool listada no garantiza que se ejecute; el fallback a datos locales debe declararse, no asumirse como equivalente a MCP.

## 9. Human Review

**What did you verify yourself?**

Se verifico un error inicial que hubo al utilizar un la herramienta del MCP de `get_file_contents`, que se trato de una interrupcion inesperada y se volvio a ejecutar el prompt para que se re-utilizara esta herramienta esta vez sin interrupciones. 

Se probaron los comandos que se integraron junto con la funcion de controlador interactivo como `Ctrl+C`, `Ctrl+Enter+Z`, `:exit` y `:salida`, para comprobar que funcionaran como comandos de salida.

De igual manera se verifico una observacion que estaba en [RISK] que consistia en que la rama y por ende el PR de la modificacion, estaba hecho desde main y no desde develop (aunque estuvieran igualados), esto hace que el merge commit se incluya en el PR ante develop.

**What AI conclusions did you reject or modify?**

Como tal no fue una modificacion pero se tuvo que volver a usar  el prompt para usar la herramienta de MCP `get_file_contents` y en la clasificacion de hallazgos que dio el agente, cuestiono si el riesgo donde el merge commit aparecia en el PR ante develop sea un riesgo palpable o solo una observacion que seria mejor evitar. No se hicieron modificaciones significativas al trabajo del agente.

## 10. Conclusion

**What did MCP add to the engineering workflow?**

MCP permitió que el agente consultara el estado real del Issue #2 y del PR #3 directamente desde GitHub (autor, estado, descripción, commits, archivos modificados) sin que el estudiante copiara manualmente ese contenido al prompt, reduciendo el riesgo de transcripción incompleta o desactualizada. El ejercicio también expuso, de forma práctica y no simulada, la diferencia entre lo que un PAT autoriza (capa de GitHub), lo que un servidor MCP anuncia como disponible (catálogo de tools) y lo que realmente deja ejecutar en una sesión concreta (policy de runtime), las tres capas no son intercambiables, y confiar solo en el catálogo de tools habría ocultado que la Fase 2 terminó dependiendo parcialmente de una fuente no-MCP.
