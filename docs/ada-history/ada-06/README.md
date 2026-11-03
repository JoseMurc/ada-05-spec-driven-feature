# ADA-06 — MCP Tool Integration with GitHub (Read-Only)

Laboratorio de integración de un coding agent con GitHub mediante **Model Context Protocol (MCP)**, en modo **read-only**, usando como repositorio objeto de análisis `JoseMurc/ada-05-spec-driven-feature` (la *Customer Search Feature* del ADA-05).

> Este README pertenece a la entrega del **ADA-06**, no a la del ADA-05. El README de la feature (instalación, uso de la CLI, tests) es un documento distinto y no debe mezclarse con este.

---

## 1. Objetivo del laboratorio

Conectar un MCP Host (Antigravity) al GitHub MCP Server oficial para leer código, Issues y Pull Requests de un repositorio real, usar esa información en una revisión de ingeniería de software, y evaluar explícitamente autenticación, autorización, exposición de herramientas (tool availability) y policy de ejecución — sin realizar ninguna acción de escritura sobre GitHub.

## 2. Repositorio analizado

| Campo | Valor |
|---|---|
| Owner / Repo | `JoseMurc/ada-05-spec-driven-feature` |
| Issue analizado | #2 — "Añadir un controlador interactivo para buscador" |
| Pull Request analizado | #3 — "Feat/controlador interactivo" |
| Rama / commits | `Feat/Controlador-interactivo` (`7db07fc`…`2a76919`) → `develop` |

## 3. Configuración MCP

- **MCP Host:** Antigravity (CLI + IDE).
- **Servidor:** `github-readonly`, GitHub MCP Server remoto oficial (`https://api.githubcopilot.com/mcp/`).
- **Modo:** READ-ONLY (`X-MCP-Readonly: true`).
- **Toolsets habilitados:** `repos`, `issues`, `pull_requests` (`X-MCP-Toolsets`).
- **Credencial:** Fine-grained Personal Access Token, acotado a este único repositorio, con permisos Contents / Issues / Pull requests en **Read-only** y expiración corta.

El token **no está incluido** en esta entrega (ni en `mcp_config.json`, ni en capturas, ni en los logs). Si necesitas reproducir la conexión, créalo siguiendo la sección 7 del PDF del ADA-06 y configúralo en el perfil global de Antigravity, nunca dentro del repositorio.

## 4. Qué se hizo (fases del ADA)

| Fase | Resultado | Dónde consultarlo |
|---|---|---|
| 1 — Tool Inventory | 22 tools expuestas, todas Read, mapeadas al catálogo esperado del ADA | `docs/MCP_GITHUB_TOOL_INVENTORY.md` |
| 2 — Repository Understanding | Arquitectura de 3 capas, puntos de entrada, tests (65/65 passing) | `results/github-mcp-review.md` §3 |
| 3 — Issue Analysis | Issue #2 leído vía MCP (`issue_read`); hechos separados de inferencias | `results/github-mcp-review.md` §4 |
| 4 — Pull Request Review | PR #3 analizado (12 archivos, 6 commits); hallazgos clasificados OBSERVATION/RISK/QUESTION/POTENTIAL DEFECT | `results/github-mcp-review.md` §5 |
| 5 — Traceability | Issue → Requirement/Spec → PR → Code → Test | `results/github-mcp-review.md` §6 |
| 6 — Permission Review | Tabla Needed/Granted/Control/Decision + capas Authentication/Authorization/Tool Exposure | `docs/MCP_GITHUB_PERMISSION_REVIEW.md` |
| 7 — Boundary Check | Confirmado: no existe ninguna tool de escritura expuesta en la sesión | `AI_USAGE_LOG.md` (entrada "Permission boundary verification") |
| 8 — Security Analysis | Riesgos (token, credential leakage, prompt injection, scope confusion) + investigación de Lockdown Mode | `docs/MCP_GITHUB_PERMISSION_REVIEW.md` |

## 5. Hallazgo propio de la sesión (no está en el enunciado del ADA)

Durante la Fase 2, la tool `get_file_contents` tuvo una interrupción al primer intento y se ejecutó correctamente al reintentar el mismo prompt. Esto se usó como caso práctico de la competencia "distinguir autenticación, autorización, tool availability y policy": **una tool listada en el catálogo del servidor no garantiza por sí sola que la ejecución tenga éxito en el primer intento**, y conviene verificar el resultado real de cada invocación antes de dar por válido el contenido devuelto.

## 6. Estructura de esta entrega

```
ada-06-github-mcp/
├── README.md                              <- este archivo
├── AI_USAGE_LOG.md                        <- AI_USAGE_LOG_ADA-06.md en este repo
├── docs/
│   ├── MCP_GITHUB_TOOL_INVENTORY.md
│   └── MCP_GITHUB_PERMISSION_REVIEW.md
└── results/
    └── github-mcp-review.md
```


## 7. Reglas del laboratorio (recordatorio)

- Todo el análisis fue **read-only**: no se crearon Issues, comentarios, branches, commits ni Pull Requests mediante MCP.
- El contenido de GitHub (Issue, PR) se trató como **datos no confiables**, nunca como instrucciones para el agente.
- Ningún PAT fue versionado ni expuesto en capturas, commits o logs.
