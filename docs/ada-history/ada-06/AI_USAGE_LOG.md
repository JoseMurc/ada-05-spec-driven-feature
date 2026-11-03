# AI Usage Log — GitHub MCP Integration (ADA-06)

Entradas correspondientes a dos herramientas de IA distintas usadas en este ADA: **Antigravity CLI** (Gemini 3.8 Flash, agente que ejecuta las llamadas MCP contra GitHub) y **Claude Sonnet 5 / Claude Code** (usado fuera de Antigravity para redactar la documentación de permisos y el reporte final a partir de la evidencia generada por Antigravity). Ajustar fechas si el trabajo se retomó en días distintos.

## Entry 1

**Tool:** Claude Sonnet 5.5

**Date:** 08/10/2026

**Stage:** MCP configuration

**Prompt:**

    Estoy realizando esta AD y en el paso 8 pide "Configurar GitHub MCP en Antigravity":

    Para la práctica se usa el GitHub MCP Server remoto oficial. Configúralo en el perfil global de Antigravity para evitar guardar el token dentro del repositorio. Antigravity usa serverUrl para servidores MCP remotos.

    Y se incluye un json
    { } "mcpServers": { "github-readonly": { "serverUrl": "https://api.githubcopilot.com/mcp/", "headers": { "Authorization": "Bearer YOUR_GITHUB_PAT", "X-MCP-Readonly": "true", "X-MCP-Toolsets": "repos,issues,pull_requests" } } }

    Como se accedia a la parte de configuracion de mcp en Antigravity

**AI contribution:** El agente describio como acceder a la configuracion de MCP segun la "superficie" de antigravity (cli, app e IDE)

**Student decision:** Se decidio usar la configuracion mediante el archivo json desde el IDE.

**Impact:** Posteriormente, el servidor `github-readonly`  quedaria operativo desde el IDE.

---

## Entry 2

**Tool:** Antigravity CLI (Gemini 3.8 Flash)

**Date:** 09/10/2026

**Stage:** MCP configuration

**Prompt:**

    N/A — configuración manual del servidor MCP en el perfil global de Antigravity (`mcpServers.github-readonly`), no una conversación con el agente.

**AI contribution:** N/A (paso de configuración, no una sugerencia del agente).

**Student decision:** Se configuró el servidor remoto oficial `github-readonly` (`https://api.githubcopilot.com/mcp/`) con un fine-grained PAT limitado al repositorio `ada-05-spec-driven-feature`, permisos Contents/Issues/Pull requests en Read-only, expiración corta, y headers `X-MCP-Readonly: true` y `X-MCP-Toolsets: repos,issues,pull_requests` para acotar el servidor a solo esos tres toolsets.

**Impact:** Servidor `github-readonly` operativo; verificado con `/mcp` antes de usarlo (22 tools listadas, todas Read).

---

## Entry 3

**Tool:** Claude Sonnet 5.5

**Date:** 08/10/2026

**Stage:** Preparation

**Prompt:**

    Ahora en el paso 10 pide crear MCP_GITHUB_TOOL_INVENTORY.md e  incluir al menos la tabla de la imagen, dice que Los nombres exactos disponibles pueden variar con la versión del servidor. Registra los nombres que realmente muestre tu cliente.

    Por un lado puedes hacer el MD con la tabla, y como puedo ver los nombres exactos?
    Tengo el antigravity cli, la aplicacion de antigravity y el IDE. Puse el MCP desde el IDE y parece detectarlo desde el cli (/mcp) pero desde la app dde antigravity me dice github-readonly

**AI contribution:** El agente dio opciones para ver los nombres exactos de las herramientas disponibles, una es usando el cli y con /mcp "seleccionar" github-read-only y la otra es pedirselo directamente al agente como un prompt.   

**Student decision:** Se decidio usar un prompt 

**Impact:** Posteriormente, el servidor `github-readonly`  quedaria operativo desde el IDE.

---

## Entry 4

**Tool:** Antigravity CLI (Gemini 3.8 Flash)

**Date:** 09/10/2026

**Stage:** Repository analysis

**Prompt:**

    Using the GitHub MCP server, inspect repository: JoseMurc/ada-05-spec-driven-feature
    This is a READ-ONLY engineering analysis. Do not modify GitHub.
    Analyze: repository purpose, main directories, entry points, componentes, tests, documentación, áreas afectadas por el Issue/PR seleccionado.

**AI contribution:** Describió el propósito del repositorio (Customer Search Feature, SDD), la arquitectura de 3 capas, los puntos de entrada (`cli.py`), la organización de tests (65 tests, 100% pass) y las áreas afectadas por el PR #3.

**Student decision:** Al ejecutar la tool `get_file_contents`, el servidor devolvió inicialmente una interrupción inesperada. Se volvió a ejecutar el mismo prompt y, en el segundo intento, la herramienta se ejecutó sin interrupciones. Se decidió aceptar el análisis resultante solo después de confirmar que la segunda ejecución sí correspondía a una llamada MCP exitosa, no a una suposición del agente.

**Impact:** Sección "Repository Understanding" de `results/github-mcp-review.md`.

---

## Entry 5

**Tool:** Antigravity CLI (Gemini 3.8 Flash)

**Date:** 09/10/2026

**Stage:** Issue analysis

**Prompt:**

    Using GitHub MCP, read Issue #2 in JoseMurc/ada-05-spec-driven-feature.
    Do not modify the Issue. Analyze it as a software engineer: problema, comportamiento esperado, criterios de aceptación explícitos, ambigüedades, código/tests relacionados, riesgos, IDs de REQUIREMENTS.md/SPEC.md relacionados.

**AI contribution:** Leyó el Issue #2 vía la tool `issue_read` (MCP real, confirmado en el log como "Called 1 MCP tool"), separó hechos del Issue de inferencias de ingeniería, identificó 5 ambigüedades no explícitas (comandos de salida, señales de terminal, texto del prompt, comportamiento ante query vacía) y las vinculó a FR-11–FR-15 y SR-10–SR-14 de `SPEC.md`.

**Student decision:** Aceptado sin modificaciones; se confirmó que las ambigüedades señaladas coinciden con decisiones ya tomadas y documentadas en `SPEC.md` durante el ADA-05.

**Impact:** Sección "Issue Analysis" de `results/github-mcp-review.md`.

---

## Entry 6

**Tool:** Antigravity CLI (Gemini 3.8 Flash)

**Date:** 09/10/2026

**Stage:** Pull Request review

**Prompt:**

    Using GitHub MCP, inspect Pull Request #3 in JoseMurc/ada-05-spec-driven-feature.
    READ ONLY. Do not comment, approve, merge, edit or close the PR.
    Inspect título, archivos cambiados, diff, commits, tests. Clasificar hallazgos como OBSERVATION / RISK / QUESTION / POTENTIAL DEFECT.

**AI contribution:** Analizó los 6 commits y 12 archivos modificados del PR #3; clasificó 5 hallazgos, incluyendo un **[RISK]**: la rama `Feat/Controlador-interactivo` se creó desde `main` después del merge del PR #1 en vez de desde `develop`, por lo que el commit de merge `3a89bd5` queda incluido en el rango de commits del PR #3 contra `develop`.

**Student decision:** Se verificó personalmente la topología de git descrita (confirmado que la rama viene de `main`, no de `develop`). Se cuestionó si esa clasificación como `[RISK]` era proporcional o si debía quedar como una simple observación, dado que no genera conflicto de merge; se decidió mantener la clasificación `[RISK]` en el reporte porque afecta la limpieza del historial, aunque no bloquea el merge.

**Impact:** Sección "Pull Request Review" de `results/github-mcp-review.md`, incluyendo la nota de verificación manual del hallazgo.

---

## Entry 6

**Tool:** Antigravity CLI (Gemini 3.8 Flash)

**Date:** 09/10/2026

**Stage:** Permission boundary verification (Fase 7)

**Prompt:**

    Inspect the GitHub MCP capabilities available in this session. Do not execute any write action.
    Question: Could you create an Issue, comment on a Pull Request, or modify repository files using the currently exposed MCP tools? Explain your answer using the actual tools available. Do not attempt the write operation.

**AI contribution:** Inspeccionó el directorio local de configuración MCP y el listado de las 22 tools expuestas; concluyó explícitamente "No" y justificó por tool requerida (`create_issue`/`issue_write`, `pull_request_review_write`/`add_comment_to_pending_review`, `create_or_update_file`/`push_files`) que ninguna existe en el servidor `github-readonly`, sin intentar ejecutarlas.

**Student decision:** Aceptado. No se intentó ninguna acción de escritura, confirmando el límite read-only del laboratorio.

**Impact:** Confirma el control "read-only verificado" de la Definition of Done del ADA-06; evidencia usada en `docs/MCP_GITHUB_PERMISSION_REVIEW.md`.

---


