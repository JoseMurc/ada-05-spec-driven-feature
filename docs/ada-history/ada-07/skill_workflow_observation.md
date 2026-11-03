# Workflow Observation

## Trigger
¿Cuándo debería utilizarse este workflow?
- Cuando existe un PR o un conjunto de commits en una rama de feature (en este caso `Feat/Controlador-interactivo`, abierta como PR pero no fusionada a `develop`) que implementa una historia de usuario spec-driven, y se necesita determinar si está lista para revisión humana antes de fusionar.
- No se activa para: implementar código nuevo, corregir los hallazgos encontrados, aprobar/fusionar el PR, comentar en GitHub, ni explicar conceptos genéricos de Git.

## Inputs
¿Qué necesita para iniciar?
- Identificador del PR/rama/diff a revisar (rama, rango de commits o número de PR).
- `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md` del repositorio como fuente normativa.
- `AGENTS.md` (reglas del proyecto: qué no modificar, qué no implementar, límites de alcance).
- `docs/Traceability.md`.
- Acceso de solo lectura al repositorio Git local (`log`, `diff`, `show`, `branch`) y capacidad de ejecutar `pytest`.
- Hallazgos previos ya documentados (si existen) de una revisión anterior, para reutilizar y reclasificar en lugar de repetir el análisis desde cero.

## Steps Performed
1. Seleccioné el conjunto de cambios a revisar: rama `Feat/Controlador-interactivo`, acotada a los 5 commits más recientes relevantes a la feature interactiva (`7db07fc`, `b88ac1b`, `d971ae7`, `98c0734`, `2a76919`), confirmados con `git log --oneline -15` y `git branch -a`.
2. Leí íntegros `REQUIREMENTS.md`, `SPEC.md` y `ARCHITECTURE.md` como contexto normativo, identificando que el incremento revisado cubre FR-11 a FR-15 (sesión interactiva) y su arquitectura asociada (`InteractiveSession`, `formatting.py`, dispatcher en `cli.py`).
3. Inspeccioné el diff y los archivos modificados con `git diff develop...HEAD --stat` y `git log --stat b88ac1b^..2a76919 --reverse`, y leí el contenido final de `src/customer_search/session.py`, `cli.py` y `formatting.py`, además del diff puntual del commit `FIX` (`git show 2a76919 -- ...`) para entender exactamente qué problema corrigió.
4. Identifiqué los tests relevantes: `tests/test_session.py` (nuevo, ~20 casos cubriendo AC-15 a AC-19) y `tests/test_cli.py` (ampliado con los casos AC-14), y confirmé que `tests/test_search_service.py`, `test_repository.py`, `test_normalization.py`, `test_models.py` y `test_latency.py` no deberían verse afectados por tratarse de un cambio aislado a la capa de presentación.
5. Ejecuté `python -m pytest -v --tb=short`: **65/65 tests pasaron en 0.69 s**, confirmando la nota "DEFECTO POTENCIAL: Ninguno identificado" de una revisión previa.
6. Clasifiqué los hallazgos recopilados (propios y los de una revisión previa adjunta como comentario al final de este archivo) en **MUST FIX / SHOULD FIX / OPTIONAL** — ver sección Decisions.
7. Consolidé el resultado como reporte para revisión humana, preservando la revisión anterior como evidencia cruda en lugar de descartarla.

## Decisions
¿Qué decisiones requieren criterio del LLM?
- **Delimitar el rango de commits del PR**: el historial por sí solo no distingue qué commits pertenecen "a la feature" frente a los heredados del merge previo del PR #1. 
- **Clasificación de severidad de cada hallazgo** (no es mecánico; requiere juicio de ingeniería sobre impacto):
  - **MUST FIX**: Ninguno. Ningún FR/AC se viola, no hay regresión (65/65 tests pasan) y no hay riesgo de seguridad o integridad de datos en el diff revisado.
  - **SHOULD FIX**: Divergencia de historial de Git — `Feat/Controlador-interactivo` se creó desde `main` *después* del merge del PR #1 (`3a89bd5`), en vez de crearse directamente desde `develop`. Confirmado con `git log --graph --oneline --all`: el commit de merge `3a89bd5` queda dentro del rango de commits del PR contra `develop`. No rompe nada funcionalmente, pero genera un historial superpuesto al fusionar contra `develop` — es un problema de mantenibilidad/higiene de control de versiones, no de comportamiento del sistema.
  - **OPTIONAL**: (a) Ubicación de `RESEARCH.md` (raíz del repo vs. `docs/`, junto a `Traceability.md`) — decisión de organización sin impacto funcional. (b) Vincular el PR al cierre automático del Issue #2 (`Closes #2` en la descripción) — mejora de trazabilidad de proceso, no bloqueante para el merge.
- **Validar que el fix del commit `2a76919` es real y no cosmético**: requirió leer el diff puntual para confirmar que `formatting.py` resuelve una dependencia circular efectiva (`cli.py` importaba `format_output` definido en sí mismo y `session.py` lo importaba de `cli.py`, mientras `cli.py` importaba `InteractiveSession` de `session.py` de forma diferida/local para evitar el ciclo). Esto es relevante para decidir si el hallazgo "separación de responsabilidades limpia" de la revisión previa era un acierto de diseño correctivo y no solo una refactorización decorativa.
- **Verificar que la documentación (ARCHITECTURE.md, SPEC.md, Traceability.md) refleja fielmente el código final**: se cruzó `docs/Traceability.md` (FR-11 a FR-15 mapeados a T-07/T-08 y a los archivos/tests concretos) contra el código real, en lugar de confiar en que el mensaje del commit T-09 ("documentation update") garantiza esa consistencia por sí solo.

## Deterministic Work
¿Qué pasos deberían ser scripts/comandos?
- `git status`, `git branch -a`, `git log --oneline -N` — identificar el PR/rama y su estado actual.
- `git merge-base <base> <rama>` + `git log --graph --oneline --all` — detectar divergencias de historial (candidato a regla automatizable: "¿el merge-base de la rama con `develop` coincide con el punto de creación esperado, o pasa por un merge commit intermedio?").
- `git diff <base>...<HEAD> --stat` y `git show --stat <commit>` por cada commit del rango — enumerar archivos y líneas modificadas; no requiere juicio humano.
- `python -m pytest -v --tb=short` — evidencia de pruebas; el conteo pass/fail y el exit code son 100% deterministas.
- Verificación de cobertura en `docs/Traceability.md`: por cada FR-ID nuevo o modificado en el diff de `REQUIREMENTS.md`/`SPEC.md`, comprobar que exista una fila correspondiente en la matriz (scripteable con una comparación de IDs por expresión regular).
- Validación de estructura del reporte final (secciones MUST FIX/SHOULD FIX/OPTIONAL, resumen, "Human decision required") — exactamente el rol que cumplirá `scripts/validate_review_report.py` en la Skill.

## Reference Knowledge
¿Qué checklist, criterios o convenciones se consultaron?
- `REQUIREMENTS.md` (FR-01 a FR-15, NFR-01 a NFR-05, Restricciones C-01 a C-08) como fuente de verdad.
- `SPEC.md` (Search Rules, Validation Rules, Error Handling, Acceptance Criteria, Test Scenarios) para verificar que el código cumple reglas concretas y no solo la intención general del requisito.
- `ARCHITECTURE.md` (Components, Responsibilities, Data Flow, Testing Strategy, Design Decisions) para evaluar si el cambio respeta las fronteras documentadas (p. ej., que `InteractiveSession` no dependa de `cli.py`, y que `formatting.py` sea el punto de desacoplo).
- `docs/Traceability.md` como checklist de cobertura requisito → código → test.
- `AGENTS.md` (reglas del proyecto: no modificar `REQUIREMENTS.md`/`SPEC.md` para hacer pasar tests, no debilitar tests, commitear por tarea referenciando su ID) como criterio de límites y seguridad del proceso.
- Hallazgos de una revisión previa (clasificada como OBSERVACIÓN / RIESGO / PREGUNTA / DEFECTO POTENCIAL, adjuntos como comentario HTML al final de este archivo) reutilizados como insumo directo para la clasificación de severidad de este reporte.

## Output
¿Qué artefacto produce?
- Este documento (`docs/skill_workflow_observation.md`) con el workflow capturado paso a paso.
- Un reporte de disposición para revisión humana (equivalente al formato `results/pr-readiness-review.md` que producirá la Skill final), con hallazgos clasificados MUST FIX / SHOULD FIX / OPTIONAL, cada uno con evidencia (archivo/commit/test) y acción recomendada — nunca una aprobación, comentario o merge sobre el PR.

## Stop Conditions
¿Cuándo debe detenerse y pedir intervención humana?
- Si `REQUIREMENTS.md` y `SPEC.md` se contradicen entre sí (no ocurrió aquí: `docs/Traceability.md` confirma alineación FR ↔ SR ↔ AC ↔ Test).
- Si `pytest` reporta fallos (no ocurrió: 65/65 passed).
- Si se detecta un hallazgo MUST FIX (violación de FR/AC, regresión, problema de seguridad o integridad de datos) — no se detectó ninguno en este rango de commits.
- Si se pide ejecutar una acción fuera de alcance (comentar, aprobar o fusionar el PR en GitHub) — el workflow se detiene y entrega el reporte únicamente en local.
- Si el historial de Git presenta una ambigüedad que afecta el alcance de la revisión (p. ej., qué commits pertenecen realmente al PR frente a un merge heredado), se detuvo brevemente para fijar explícitamente el rango `7db07fc..2a76919` antes de continuar, en lugar de asumirlo.


<!--
### [OBSERVACIÓN]

1. Separación de responsabilidades limpia: En el commit 2a76919, el formateo de presentación se desacopló en formatting.py. Esto evita dependencias circulares entre cli.py y session.py.
2. Diseño de REPL testeable: InteractiveSession acepta callables inyectables input_fn y output_fn. Esto permite probar unitariamente flujos de entrada de múltiples pasos sin parchear los streams estándar globales.
3. Trazabilidad rigurosa de especificaciones: Todos los documentos de especificación (REQUIREMENTS.md, SPEC.md, ARCHITECTURE.md, TASKS.md, Traceability.md) se actualizaron de forma concurrente con el código.

### [RIESGO]

1. Divergencia de rama / historial de merges: La rama de feature Feat/Controlador-interactivo se creó desde main después de que se hizo merge del PR #1, en lugar de crearse directamente desde develop. Como resultado, el merge commit 3a89bd5 queda incluido en el rango de commits del PR contra develop. Aunque git resuelve el contenido sin conflictos, hacer merge de esto de vuelta a develop genera un historial superpuesto.

### [PREGUNTA]

1. Ubicación de RESEARCH.md: ¿Debería RESEARCH.md permanecer en la raíz del repositorio o moverse a docs/ junto a Traceability.md?
2. Cierre automático del Issue #2: ¿Debería actualizarse la descripción del PR para incluir Closes #2 antes de hacer merge?

### [DEFECTO POTENCIAL]

• Ninguno identificado. Los 65 tests unitarios y de integración pasan, la lógica de negocio en search_service.py no se ve afectada, y los casos borde (comandos de salida falsos positivos, señales, espacios en blanco) están manejados y probados.
-->
