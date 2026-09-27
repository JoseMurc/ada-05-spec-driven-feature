# AI Usage Log — Customer Search (ADA-05)
 
Todas las entradas corresponden a una misma sesión de trabajo. Ajustar las fechas si el trabajo se retomó en días distintos.
 
 
## Entry 1

**Tool:** Claude Sonnet 5

**Date:** 24/09/2026

**Stage:**Requirements analysis

**Prompt:** 

    Para el caso de los requisitos no funcionales, no sería más conveniente a este punto rescribir esa parte? (dejando los no diferidos, reemplazando/rescribiendo los diferidos). Aunque no se que tan apropiado sea en el contexto de las ADAS y de lo enseñado en las diapositivas. Aunque parece que se tiene que hacer por que de otro modo queda raro que 4 de 5 NFR estén diferidos.

**Student decision:** Aceptado.

**AI contribution:** Recomendó reescribir NFR-02 a NFR-05 con "No aplica en esta entrega" como declaración principal y la constraint que lo justifica, dejando el texto original entre paréntesis solo como referencia, mismo criterio usado para reescribir requisitos (no anotarlos) cuando existe una decisión.

**Student decision:** Aceptado.

**Impact:** NFR-02 a NFR-05 reescritos en REQUIREMENTS.md; Q-14, Q-15 y Q-16 de Open Questions alineadas al mismo lenguaje ("No aplica").
 

 
## Entry 2

**Tool:** Claude Sonnet 5

**Date:** 24/09/2026

**Stage:** Specification

**Prompt:** 

    Ahora sigue el SPEC.md

    SPEC.md es la fuente de verdad del comportamiento verificable de la feature. Parte de REQUIREMENTS.md y transforma los requisitos en alcance, reglas, validaciones, criterios de aceptación y escenarios de prueba. No redefine FR/NFR. No dejes secciones vacías. Si no aplica, escribe N/A y justifica. Los IDs incluidos en Requirements Covered deben existir en REQUIREMENTS.md.

**AI contribution:** Redactó SPEC.md completo: Scope/Out of Scope, Domain Model, Search Rules (SR-01–SR-05), Validation Rules, Error Handling (EH-03/EH-04 marcados N/A por C-05), Acceptance Criteria (AC-01–AC-08) y Test Scenarios (TS-01–TS-08), referenciando cada FR/NFR por ID sin redefinirlo.

**Student decision:** Aceptado.

**Impact:** SPEC.md v1 creado.
 
 
## Entry 3

**Tool:** Claude Sonnet 5

**Date:** 25/09/2026

**Stage:** Architecture

**Prompt:** 
    
    Genera ARCHITECTURE.md con la estructura del ADA-05 (Overview, Components, Responsibilities, Data Flow, Interfaces, Error Handling, Testing Strategy, Dependencies, Design Decisions, Trade-offs), incluyendo diagrama Mermaid o ASCII. (Se adjunto el ejemplo de las diapositivas)

**AI contribution:** Propuso arquitectura de tres capas (CLI/API, Search Service, Repository, Customer Data) con diagrama Mermaid; asignó cada regla de SPEC.md (SR-01–SR-09, EH-01/EH-02) a un componente concreto; documentó decisiones de diseño para FR-09 (sin filtrado, punto de extensión señalado) y FR-10 (proyección de campos en Search Service, no en la interfaz).

**Student decision:** Aceptado.

**Impact:** ARCHITECTURE.md creado.
 
## Entry 4

**Tool:** Claude Sonnet 5

**Date:** 25/09/2026

**Stage:** Tasks

**Prompt:**
    
    Continua con TASKS.md con la estructura del ADA-05: T-01 Project setup, T-02 Domain modal , T-03 Search logic, T-04 Validation and errors, T-05 Tests, T-06 Documentation (each one with Goal, files, acceptance and verification subtopics).

**AI contribution:** Dividió el trabajo en T-01 a T-06 (setup, domain model, search logic, validation and errors, tests, documentation), cada una con Goal/Files/Acceptance/Verification/Status, mapeando cada tarea a los AC-XX y TS-XX específicos de SPEC.md sin introducir requisitos nuevos.

**Student decision:** Aceptado.
**Impact:** TASKS.md creado.
 
---
 
## Entry 5

**Tool:** Claude Sonnet 5

**Date:** 25/09/2026

**Stage:** Cross-artifact review

**Prompt:** 

    Aqui estan todos los documentos que pertencen a la baseline del ADA. Puedes revisarlos y ver si hay inconsistencias entre ellos, por ejemplo, ahorita en REQUIREMENTS, falta el FR-09 que podria integrar de vuelta, aunque revisando cual es:

    FR-09: El sistema deberá devolver resultados según el alcance autorizado para el usuario buscador definido en la matriz de autorización RN-06.

    Ando viendo si se debe incluir o debe haber una modificacion en el md y en otros con respecto, ya que SPEC tambien menciona el FR-09.

Se adjuntaron documentos: ARCHITECHTURE.md, SPEC.md, TASKS.md, AGENTS.md, REQUIREMENTS.md

**AI contribution:** Detectó una contradicción crítica en SPEC.md (FR-07–FR-10 listados simultáneamente en Requirements Covered y en Out of Scope); recomendó no restaurar el FR-09 original porque citaba RN-06, un ID ya inexistente en el resto del baseline, y propuso una redacción alternativa que instancia la decisión ya tomada; detectó contradicción entre FR-06 y A-08 sobre "catálogo de textos"; detectó inconsistencia en el nombre del campo identificador (`id` / "identificador de cliente" / `cliente_id`); señaló encabezados en español que rompían la consistencia con el resto de archivos.

**Student decision:** Aceptado.

**Impact:** SPEC.md corregido (Scope/Out of Scope); REQUIREMENTS.md corregido (FR-06, FR-09, FR-10, encabezados de sección).
 
 
## Entry 6

**Tool:** Claude Sonnet 5

**Date:** 25/09/2026

**Stage:** Cross-artifact review

**Prompt:** 

    Puedes hacer una ultima revision de los archivos antes de subir la baseline? Se realizaron modificaciones para mantener coherencias, revisa si esta se mantuvo.

Se adjuntaron documentos: ARCHITECHTURE.md, SPEC.md, TASKS.md, AGENTS.md, REQUIREMENTS.md

**AI contribution:** Detectó que `SearchResult` en ARCHITECTURE.md no tenía campo para transportar el mensaje fijo exigido por FR-06/AC-07; detectó que AC-13/TS-13 no estaban asignados a ninguna tarea en TASKS.md; detectó que "catálogo de mensajes fijos" había reaparecido en T-04 pese a haberse corregido en REQUIREMENTS.md; detectó referencias al material del curso dentro de TASKS.md (T-06); señaló que C-06 (commits incrementales por tarea) no estaba reflejado en AGENTS.md.

**Student decision:** Aceptado.

**Impact:** ARCHITECTURE.md (campo `message` agregado a `SearchResult`); TASKS.md (T-03, T-05, T-06 corregidas); AGENTS.md (regla de commits añadida); REQUIREMENTS.md (NFR-01, Q-02, Q-15 corregidos).
 
 
## Entry 7

**Tool:** Claude Sonnet 5

**Date:** 25/09/2026

**Stage:** Traceability

**Prompt:**

    Preguntó si la matriz de trazabilidad estaba bien construida, señalando que debía conectar REQUIREMENTS.md → SPEC.md → implementación; después compartió el `Traceability.md` ya creado (movido del README a un archivo aparte) para revisión.

**AI contribution:** Advirtió que la plantilla del PDF solo cubre 9 de los 15 requisitos reales del proyecto. Al revisar el archivo real, detectó 3 problemas: faltaban las filas de NFR-04 y NFR-05; la fila de FR-09 listaba dos tareas (T-03 y T-05) sin justificar la segunda; faltaba el ID de Test Scenario (TS-XX) en casi todas las filas. Además advirtió que el estado "Implementado & Probado" es una afirmación verificable que debe confirmarse con una corrida real de `pytest` antes de la Fase 10, no darse por hecho.

**Student decision:** Aceptado;

**Impact:** `Traceability.md` regenerado: NFR-04/NFR-05 añadidos, TS-XX añadido a cada fila, FR-09 simplificado a T-03.