# Professional Skill Study — ADA-07 
 
## Source 
Repository: skill incluida en este mismo proyecto, bajo `.agents/skills/code-review-and-quality/` (y su copia activa en `.claude/skills/code-review-and-quality/`).
Skill: `code-review-and-quality`
Version / commit: tal como está en el working tree actual del repo (no versionada por separado).
Installed path: `ada-05-spec-driven-feature/.agents/skills/code-review-and-quality/SKILL.md`
 
## Why this skill was selected 
Se seleccionó porque está disponible en el mismo entorno del curso, cubre el mismo tipo de tarea (revisión de un PR antes de mergear) que mi skill personalizada, y permite una comparación directa aplicando ambas sobre el mismo PR real del proyecto.
 
## Anatomy observations 
- Está organizada en cinco ejes fijos de revisión (correctness, readability, architecture, security, performance), cada uno con su propia lista de preguntas guía.
- Incluye "remedios estructurales" nombrados en vez de solo señalar el problema.
- Define un modelo de severidad por prefijos (Critical / sin prefijo = requerido / Nit / Optional-Consider / FYI) pensado para que el autor del PR sepa la urgencia del comentario.
- Tiene secciones sobre tamaño de cambio, mensajes de commit, disciplina de dependencias y hasta "racionalizaciones comunes" (excusas típicas para saltarse la revisión) y "red flags".
- Termina con un checklist de verificación y un veredicto final (Approve / Request changes).
- Está enfocada a revisiones mas generales, sin cerrarse solo a PR's, ya que tambien puede revisar merges, commits, codigo implementado, etc.
 
## Execution 
PR / diff reviewed: PR #3 del repositorio del proyecto (`JoseMurc/ada-05-spec-driven-feature`), rama `Feat/Controlador-interactivo` → `develop`/`main`, commit cabeza `2a76919`.
Prompt used: 

    Use the code-review-and-quality skill to review PR #3 
 
    Context: - Read repository requirements/specification when available. - Review the complete diff. - Inspect relevant tests and verification evidence. 
    
    Do not modify code yet. 
    Do not comment, approve, or merge on GitHub. 
    
    Produce the review locally in: 
    results/professional-skill-review.md 
    
    For every finding include: - severity - file / evidence - engineering rationale - recommended action

Artifacts produced: `results/professional-skill-review.md` (reporte completo de revisión con 4 hallazgos, verificación por mutation testing manual, y veredicto de aprobación).

 
## Findings unique to the professional skill 
1. Mediante mutation testing manual (invertir una condición y quitar un `.strip()` en el código), confirmó que las pruebas existentes realmente detectan esos errores — no solo que "existen pruebas".
2. Detectó una afirmación demasiado absoluta en `ARCHITECTURE.md` (dice que no se usa "monkeypatching global", pero una prueba específica sí lo hace a propósito para verificar el comportamiento por defecto).
 
## Findings unique to my skill 
1. Un commit del PR no referencia ningún ID de tarea de `TASKS.md`, lo cual incumple la regla C-06 de `AGENTS.md` sobre trazabilidad commit a tarea.
2. Un merge commit inesperado quedó incluido dentro del rango de commits del PR (la rama no se creó directamente desde `develop`), lo cual es ruido de historial que la skill profesional no revisó.

## Security / dependency audit 
Ninguna de las dos skills encontró hallazgos de seguridad o de dependencias en este PR, porque el cambio no agrega dependencias nuevas ni toca superficie de entrada externa (es una sesión interactiva de línea de comandos, mismo flujo de `SearchService` ya existente). La skill profesional sí tiene una lista de verificación de seguridad más explícita (dependencias de confianza, validación de input, licencias), pero en este caso concreto no encontró nada que reportar. No se ejecutó ningún `npm audit` ni equivalente porque el proyecto es Python y no tiene gestor de dependencias de terceros más allá de pytest.

 
## What I would adopt in v2 of my skill 
Adoptaría la técnica de mutation testing manual (invertir una condición del código nuevo y comprobar que al menos una prueba falla) como paso adicional dentro del workflow, y agregaría una sección explícita de seguridad y rendimiento con su propia checklist, en vez de dejarlas implícitas en `AGENTS.md`.
 
## Human conclusion 

La skill profesional es mas general que la skill personalizada y los motivos son claros, servir como un "comodin" para hacer revisiones en vez de centrarse en algo especifico, ganando mas utilidad general a cambio perder "especialidad" en actividades especificas, aunque igual ganando adaptabilidad con respecto a otras skills mientras que las personalizadas requeririan retrabajo para adaptarse a un ecosistema de skills complejo.

Para proyectos futuros una skill ya hecha puede ser mejor (se ahorra uno el trabajo previo de hacer una skill personalizada) pero se debe tener en cuenta la manera y el ambiente en que se trabaja, si el flujo de trabajo actual requiere una enfasis especial en algun aspecto del flujo (como revisiones a PR's) o un cambio relevante en alguna parte del mismo, se podria pensar en modificar la SKILL (aunque en Skills ya hechas, suelen estar acopladas a un ecosistema establecido y dificial de cambiar) o ya de plano, hacer una propia. 
 