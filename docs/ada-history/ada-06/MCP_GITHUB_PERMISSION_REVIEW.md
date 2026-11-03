# MCP GitHub Permission Review — ADA-06

## 1. Contexto

| Campo | Valor |
|---|---|
| Repositorio analizado | `JoseMurc/ada-05-spec-driven-feature` |
| MCP Host | Antigravity CLI |
| Servidor | `github-readonly` (`https://api.githubcopilot.com/mcp/`) |
| Modo | READ-ONLY (`X-MCP-Readonly: true`) |
| Toolsets declarados | `repos`, `issues`, `pull_requests` |
| PAT | Fine-grained, repositorio único, permisos Contents/Issues/Pull requests en Read-only, expiración corta |

## 2. Fase 6 — Permission Review

| Capability | Needed | Granted | Control | Decision |
|---|---|---|---|---|
| Read repository contents | Yes | Yes (PAT) / **No en runtime** | PAT `Contents: Read`; pero la tool `get_file_contents` fue rechazada por el servidor en esta sesión (`tool get_file_contents is not allowed for server github-readonly`) | Keep el permiso del PAT; **investigar** por qué la tool no se ejecutó (ver nota abajo) |
| Read Issues | Yes | Yes | PAT `Issues: Read`; `issue_read` ejecutada con éxito vía MCP | Keep |
| Read Pull Requests | Yes | Yes | PAT `Pull requests: Read`; herramientas `pull_request_read` / `list_pull_requests` expuestas y usadas | Keep |
| Create/edit Issue | No | No | MCP read-only (ninguna tool `create_issue`/`issue_write` en el listado de 22 tools) | Block |
| Comment on PR | No | No | MCP read-only (ninguna tool `pull_request_review_write`/`add_comment_to_pending_review`) | Block |
| Push files / branch | No | No | MCP read-only + PAT solo lectura (ninguna tool `create_or_update_file`/`push_files`) | Block |
| Other repositories | No | No | Fine-grained PAT limitado a `ada-05-spec-driven-feature`; `search_code`/`search_repositories` sí operan sobre todo GitHub, pero los prompts nombraron `OWNER/REPOSITORY` explícitamente en cada fase | Block (mitigado por disciplina de prompt, no por el token) |

### Nota: tool availability ≠ policy (hallazgo real de la sesión)

Durante la Fase 2 (Repository Understanding), el agente intentó usar `get_file_contents` — una tool que **sí aparece listada** en el inventario de 22 tools expuestas (ver `MCP_GITHUB_TOOL_INVENTORY.md`). Sin embargo, al ejecutarla, el servidor respondió que la tool no estaba permitida en ese contexto (`server github-readonly is not allowed in this context`). El agente, sin pedir confirmación, cayó de vuelta a inspeccionar el clon local del repositorio para completar el análisis.

Esto demuestra en la práctica la diferencia entre las tres capas del modelo mental del ADA:

- **Tool availability** (lo que el catálogo del servidor anuncia que existe) no es lo mismo que **runtime policy** (lo que el servidor realmente deja ejecutar en una sesión concreta). Una tool puede figurar en el listado y aun así estar bloqueada por una política adicional del lado del servidor.
- Esto **no fue un fallo de autorización del PAT** (el token sí tiene `Contents: Read`), sino una restricción aplicada por el servidor/cliente MCP en ese contexto específico.
- Consecuencia práctica para el ADA: la Fase 2 **no se completó 100% "exclusivamente vía MCP"** como pide la regla del laboratorio — se completó con una mezcla de intento de MCP (fallido) + inspección local de archivos. Esto debe declararse explícitamente en el reporte final (ver `results/github-mcp-review.md`, sección 9), no ocultarse, porque la regla académica del ADA exige poder explicar qué vino realmente de GitHub vía MCP y qué no.

### Tres capas distintas (aplicadas a este caso concreto)

| Capa | Pregunta | Evidencia en este ADA |
|---|---|---|
| **AUTHENTICATION** | ¿Quién es el usuario? | El PAT fine-grained identifica a la cuenta `JoseMurc` frente a GitHub. |
| **AUTHORIZATION** | ¿Qué permite el token en GitHub? | Contents/Issues/Pull requests en Read-only, sobre un único repositorio. |
| **MCP TOOL EXPOSURE / POLICY** | ¿Qué herramientas pone el servidor a disposición del agente, y cuáles realmente deja ejecutar? | 22 tools listadas, todas Read; pero `get_file_contents` fue bloqueada en runtime pese a estar en el listado — la policy del servidor fue más restrictiva que el catálogo anunciado. |

Las tres capas fueron coherentes en lo esencial (ninguna permitió escritura), pero el caso de `get_file_contents` muestra que **"la tool aparece disponible" no es garantía de "la tool se ejecutará"**: siempre hay que verificar el resultado real de la invocación, no solo el catálogo.

## 3. Fase 8 — Security Analysis

| Riesgo | Ejemplo | Mitigación |
|---|---|---|
| Over-permissioned token | Token con acceso a todos los repos o permisos write | Fine-grained PAT + repositorio único (`ada-05-spec-driven-feature`) + Read-only |
| Credential leakage | PAT en commit, captura o AI log | No se versionó el token; no aparece en `mcp_config.json` entregado, capturas ni `AI_USAGE_LOG.md` |
| Prompt injection | Issue/PR contiene instrucciones maliciosas dirigidas al agente | Contenido de Issue #2 y PR #3 se trató como datos a analizar, no como instrucciones; ningún prompt delegó decisiones de escritura al contenido leído |
| Unnecessary tools | Habilitar `actions`/`security`/`admin` sin necesitarlos | Header `X-MCP-Toolsets: repos,issues,pull_requests`; confirmado que las 22 tools observadas pertenecen solo a esos 3 toolsets |
| Scope confusion | Agente analiza otro repositorio | `search_code`/`search_repositories` operan sobre todo GitHub; mitigado nombrando `OWNER/REPOSITORY` explícitamente en cada prompt |
| **Tool availability vs runtime policy** (hallazgo propio) | `get_file_contents` listada como disponible pero rechazada al ejecutarse (`not allowed in this context`), forzando fallback silencioso a datos locales | No asumir que el catálogo de tools refleja lo ejecutable; verificar el resultado de cada invocación; si el agente cae a una fuente no-MCP (clon local), debe **declararlo explícitamente** en vez de mezclar silenciosamente evidencia remota y local |

### Lockdown Mode del GitHub MCP Server

El GitHub MCP Server oficial incluye un **Lockdown Mode**: en repositorios públicos, cuando está activado, filtra el contenido que el servidor devuelve al agente limitándolo a elementos (issues, comentarios, etc.) cuyos autores tienen permiso de `push` sobre el repositorio. El objetivo es reducir el riesgo de que contenido de bajo privilegio (un comentario o Issue de un usuario externo) inyecte instrucciones maliciosas que el agente interprete como órdenes legítimas.

Es, sin embargo, una mitigación **best-effort** y no un sustituto de la frontera de autorización, por varias razones:

- Es un filtro de **contenido visible**, no un control de **qué puede hacer** el agente. La verdadera frontera de lo que el agente puede ejecutar sigue siendo el PAT (autorización) + el toolset/read-only (policy de tools), no el Lockdown Mode.
- Solo se aplica a repos públicos y a la señal "el autor tiene push access"; no garantiza que todo contenido malicioso quede filtrado (un colaborador con push access podría igualmente insertar contenido malicioso, o el filtro podría tener falsos negativos).
- El propio mecanismo ha tenido fallos de implementación: por ejemplo, una vulnerabilidad reportada (CVE-2026-48529) en versiones del servidor en modo HTTP permitió que, con Lockdown Mode activo, una caché compartida mezclara credenciales entre usuarios distintos — es decir, el propio control de seguridad introdujo un riesgo nuevo si no se audita.
- Por eso, en este ADA, la defensa principal sigue siendo: **read-only real al nivel del servidor + PAT de mínimo privilegio + tratar todo contenido de Issues/PRs como datos no confiables en el prompt**, y el Lockdown Mode (si estuviera disponible y activado) se consideraría una capa adicional, no un reemplazo de ninguna de las anteriores.

Fuentes consultadas: [GitHub Changelog — tool-specific configuration and lockdown](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more), [Reducing Prompt Injection Risk with GitHub MCP Lockdown Mode (Classmethod)](https://dev.classmethod.jp/en/articles/github-mcp-lockdown-verification/), [CVE-2026-48529](https://cvefeed.io/vuln/detail/CVE-2026-48529), [Researchers warn of prompt injection vulnerability in GitHub MCP (DevClass)](https://devclass.com/2025/05/27/researchers-warn-of-prompt-injection-vulnerability-in-github-mcp-with-no-obvious-fix/).
