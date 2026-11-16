# Repository Readiness Audit

## BEFORE

| Dimension | Score 0-5 | Weighted | Evidence | Main Gap |
|---|---:|---:|---|---|
| Entry Point & Navigation | 4 | 12/15 | El README explica la arquitectura, la instalación y los comandos de uso, y enlaza a REQUIREMENTS, SPEC, ARCHITECTURE y TASKS. AGENTS.md indica qué leer antes de trabajar. | No existe un único punto de entrada que reúna todos los documentos juntos; hay que revisar varios archivos para armar el panorama completo. |
| Agent Instructions | 4 | 12/15 | AGENTS.md define reglas claras del proyecto, archivos que no se deben tocar, alcance fuera de límite y una Definition of Done concreta. | Las reglas están escritas en texto pero nada verifica de forma automática que se cumplan antes de aceptar un cambio. |
| Build / Run / Test | 4 | 12/15 | El README incluye comandos exactos de instalación y de ejecución de pruebas, incluyendo pruebas específicas por archivo, sin dependencias externas. | No hay un solo comando que corra todo el proceso de validación de punta a punta ni evidencia de que se ejecuta de forma automática. |
| Architecture Boundaries | 4 | 8/10 | ARCHITECTURE.md describe cada componente, su responsabilidad, el flujo de datos y las decisiones de diseño con mucho detalle. | Los límites están bien explicados pero dependen de que la persona o el agente los lea; nada impide en automático una modificación fuera de esos límites. |
| Requirements & Traceability | 4 | 8/10 | La matriz de trazabilidad conecta cada requisito con sus reglas, tareas, archivos de código y archivos de prueba usando IDs consistentes. | La matriz se mantiene a mano, por lo que puede desactualizarse si se cambia el código sin actualizarla al mismo tiempo. |
| Automation & Guardrails | 1 | 2/10 | Existe una configuración básica de pytest y los comandos para correrlo están documentados. | No hay integración continua, ni lint, ni hooks que conviertan las reglas de AGENTS.md en verificaciones automáticas; todo depende de que alguien las recuerde y las aplique a mano. |
| Testability & Evidence | 4 | 12/15 | Hay pruebas para cada capa (modelos, normalización, repositorio, servicio, CLI, sesión interactiva) y una prueba de latencia con resultados medidos documentados. | No existe un reporte de cobertura ni un umbral mínimo exigido, por lo que no hay forma rápida de ver qué tan completas son las pruebas. |
| Safety & Permissions | 2 | 4/10 | AGENTS.md menciona algunos límites, como no modificar el archivo de datos fuera de una tarea específica y no implementar autenticación ni límites de uso en esta entrega. | No hay una sección dedicada a seguridad que hable de secretos, operaciones destructivas o acciones externas; los límites que existen están repartidos y son parciales. |

TOTAL BEFORE: 70 / 100

Top 3 friction points:
1. No hay automatización (integración continua, lint o hooks) que convierta las reglas de AGENTS.md y los resultados de las pruebas en verificaciones obligatorias; todo depende de que la persona o el agente las ejecute y las respete por su cuenta.
2. No existe una sección clara de seguridad y permisos que reúna en un solo lugar qué no se puede tocar, qué operaciones son riesgosas y qué acciones externas están permitidas.
3. La documentación de requisitos, arquitectura y trazabilidad es muy completa pero se mantiene a mano, así que con el tiempo puede desalinearse del código si no se actualiza junto con cada cambio.
