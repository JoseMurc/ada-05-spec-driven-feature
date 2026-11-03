# MCP GitHub Tool Inventory — ADA-06

## 1. Contexto

| Campo | Valor |
|---|---|
| MCP Host | Antigravity (IDE / CLI) |
| Servidor | `github-readonly` |
| Endpoint | `https://api.githubcopilot.com/mcp/` |
| Modo | READ-ONLY (`X-MCP-Readonly: true`) |
| Toolsets | `repos`, `issues`, `pull_requests` |
| Fecha de verificación | YYYY-MM-DD |
| Cliente usado para verificar | Antigravity CLI (`/mcp`) |

## 2. Inventario esperado (referencia del ADA)

| Tool / capacidad | Toolset | Read/Write | Uso en el ADA | Riesgo |
|---|---|---|---|---|
| get_file_contents / lectura de archivos | repos | Read | Leer código y docs | Bajo |
| search / búsqueda de código o repos | repos | Read | Localizar implementación | Bajo |
| issue_read / lectura de Issue | issues | Read | Comprender solicitud/bug | Medio: contenido no confiable |
| pull_request_read / lectura de PR | pull_requests | Read | Analizar cambio y diff | Medio: contenido no confiable |
| Write tools | — | No disponibles | No deben aparecer por read-only | Alto si estuvieran habilitadas |

## 3. Inventario observado (nombres reales del cliente)

Método de obtención: Antigravity CLI, servidor `github-readonly` (`/mcp` y listado de tools).
Total de tools expuestas: **22**. Todas con operación **Read**.

> La columna Toolset es inferida (el CLI no la muestra). Para `get_label` y `list_repository_collaborators` es la menos segura.

| Nombre exacto observado | Toolset (inferido) | Read/Write | Descripción | Riesgo | Se usó en el ADA |
|---|---|---|---|---|---|
| `get_file_contents` | repos | Read | Obtiene el contenido de un archivo o directorio del repositorio | Bajo | ☑ |
| `search_code` | repos | Read | Búsqueda de código (símbolos, funciones, clases, patrones) en GitHub | Bajo | ☐ |
| `search_repositories` | repos | Read | Busca repositorios por nombre, descripción, README, topics o metadatos | Bajo | ☑ |
| `list_branches` | repos | Read | Lista las branches del repositorio | Bajo | ☐ |
| `list_commits` | repos | Read | Lista los commits de una branch (paginado) | Bajo | ☐ |
| `get_commit` | repos | Read | Detalle de un commit | Bajo | ☑ |
| `search_commits` | repos | Read | Busca commits (solo en la branch por defecto) | Bajo | ☐ |
| `list_tags` | repos | Read | Lista los tags de git | Bajo | ☐ |
| `get_tag` | repos | Read | Detalle de un tag de git | Bajo | ☐ |
| `list_releases` | repos | Read | Lista los releases del repositorio | Bajo | ☐ |
| `get_latest_release` | repos | Read | Obtiene el release más reciente | Bajo | ☐ |
| `get_release_by_tag` | repos | Read | Obtiene un release por nombre de tag | Bajo | ☐ |
| `list_repository_collaborators` | repos | Read | Lista colaboradores del repositorio (paginado) | Bajo: expone usuarios | ☐ |
| `issue_read` | issues | Read | Información de un Issue específico | Medio: contenido no confiable |☑ | Read | Lista Issues del repositorio (paginado con cursor) | Medio: contenido no confiable | ☑ |
| `search_issues` | issues | Read | Búsqueda semántica de Issues (ya acotada a `is:issue`) | Medio: contenido no confiable | ☑ |
| `list_issue_types` | issues | Read | Tipos de Issue soportados por el repo u organización | Bajo | ☐ |
| `list_issue_fields` | issues | Read | Definiciones de campos de Issue (nombre, tipo, opciones) | Bajo | ☐ |
| `get_label` | issues | Read | Obtiene una label específica del repositorio | Bajo | ☐ |
| `pull_request_read` | pull_requests | Read | Información de un Pull Request específico | Medio: contenido no confiable | ☑ |
| `list_pull_requests` | pull_requests | Read | Lista Pull Requests del repositorio | Medio: contenido no confiable | ☐ |
| `search_pull_requests` | pull_requests | Read | Busca PRs con sintaxis de búsqueda, acotada a `is:pr` | Medio: contenido no confiable | ☑ |

### Verificación de ausencia de write tools

- [x] Las 22 tools observadas tienen operación Read en la salida del CLI.
- [x] No aparece ninguna tool `create_*`, `update_*`, `delete_*`, `add_*`, `merge_*`, `push_*` o `fork_*`.
- [x] No aparecen tools de otros toolsets (`actions`, `code_security`, `users`, `orgs`).

Resultado: **PASS**

### Diferencias frente al inventario esperado del ADA

- `search` del ADA corresponde a tres tools: `search_code`, `search_repositories` y `search_commits`.
- `get_file_contents`, `issue_read` y `pull_request_read` coinciden por nombre exacto.
- Hay tools adicionales de lectura no previstas (commits, tags, releases, branches, labels, tipos y campos de Issue, colaboradores, búsqueda de Issues y PRs).
- `search_code` y `search_repositories` operan sobre **todo GitHub**, no solo el repo del ADA. Por eso los prompts deben nombrar `OWNER/REPOSITORY` explícitamente (scope confusion, Fase 8).

## 6. Evidencia

- Captura de `/mcp` mostrando `github-readonly` conectado (sin token visible): `docs/evidence/...`
