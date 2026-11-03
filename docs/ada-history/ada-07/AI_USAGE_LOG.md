# AI Usage Log — GitHub MCP Integration (ADA-06)

Entradas correspondientes a la herramienta de IA usada en este ADA: **Claude Sonnet 5 / Claude Code** (usado fuera de Antigravity para redactar la documentación de permisos y el reporte final a partir de la evidencia generada por Antigravity). Ajustar fechas si el trabajo se retomó en días distintos.

## Entry 1

**Tool:** Claude Sonnet 5.5

**Date:** 25/10/2026

**Stage:** Workflow observation

**Prompt:**

        Necesito que documentes el workflow del sistema actual con el fin de diseñar una skill (en el documento anexo esta en el paso 6):

        1. Selecciona un PR o conjunto de cambios. (actualmente en el repositorio hay un PR de la rama en la que estamos: "Feat/Controlador-interactivo" pero no fue mergeado a develop, pero sigue ahi por propositos de las ada's)
        2. Lee @ada-05-spec-driven-feature/REQUIREMENTS.md  / @ada-05-spec-driven-feature/SPEC.md  / @ada-05-spec-driven-feature/ARCHITECTURE.md . 
        3. Inspecciona el diff y los archivos modificados (los commits en dicho PR fueron los 5 ultimos registrados: el FIX, los 2 de T-07, el commit de T-08 y T-09)
        4. Identifica los tests relevantes. 
        5. Ejecuta o inspecciona evidencia de pruebas. 
        6. Clasifica hallazgos como MUST FIX, SHOULD FIX u OPTIONAL. Hace un tiempo un agente recopilo hallazgos segun OBSERVACION/RIESGO/DEFECTO POTENCIA Y PREGUNTA. Los adjunto como comentario en @ada-05-spec-driven-feature/skill_workflow_observation.md  
        7. Genera un reporte para revisión humana (ya esta el documento en @ada-05-spec-driven-feature/skill_workflow_observation.md  con la estructura ya definida )

        Como en el ADA-07 dice, el objetivo es capturar un workflow que ya demostró valor.  

**AI contribution:** El agente genero lo necesario en el archivo de skill_workfloe_validation, incluyendo los pasos del workflow actual:
 - Seleccion de cambios
 - Lectura de documentacion (`REQUIREMENTS.md`, `SPEC.md` y `ARCHITECTURE.md`)
 - Inspeccion de cambios realizados en el PR (mediante `git diff` y `git log`)
 - Identificacion de test relevantes
 - Ejecucion de tests 
 - Clasificacion de hallazgos relevantes
 - Creacion del reporte

**Student decision:** Se mantuvo sin cambios el workflow actual, si bien se dudo si la identificacion y ejecucion de tests podia juntarse en un paso, al final se decidio dejarlo asi para evitar una carga de trabajo mayor en un solo paso.

**Impact:** `skill_workflow_observation.md creado`.

---

## Entry 2

**Tool:** Claude Sonnet 5.5

**Date:** 27/10/2026

**Stage:** Skill authoring

**Prompt:**

        En @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/SKILL.md  existe una skill redactada con su nombre, descripcion, metadatos y una seccion que describe cuando se usa, sus precondiciones, workflow, seguridad/limites y SALIDA.

        De momento lo que tiene son aspectos algo genericos. considerando que ya existe @ada-05-spec-driven-feature/skill_workflow_observation.md  y @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/evals/trigger_cases.json  , podrias en base a eso sugerir que se podria añadir a la @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/SKILL.md para que sea mas de acorde a lo que se ha hecho.

**AI contribution:** El agente enlisto y aplico cambios a SKILL.md, entre dichos cambios estaban:
- La distincion de que el PR puede ser local y no fusionado (como es el caso) en lugar de un PR ya mergeado
- Adicion de 2 anti-triggers en la descripcion
- Mencion al resto de documentacion del proyecto (`ARCHITECTURE`, `AGENTS.md` y `Traceability.md`)
- Especificacion de que se debe revisar el rango de commits en el workflow utilizando diversos comandos, ya que en otras revisiones se tuvo que especificar
- Adicion de las "capturas" de SHOULD FIX
- Especificacion de que se deben verificar lo resultados de los tests
- Mencion de AGENTS.md como documentacion respetable
- Adicion de Stop condition: que se detenga si el rango de commits en amiguo en vez de asumirlo

**Student decision:** Se recibieron los cambios hechos por el agente, se elimino texto redundante o demasiado tecnico (tambien se llego a simplificar/parafrasear)

**Impact:** `SKILL.md modificado`.

---

## Entry 3

**Tool:** Claude Sonnet 5.5

**Date:** 27/10/2026

**Stage:** Script design

**Prompt:**

        Ahora revisa @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/references/review_checklist.md , @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/references/severity_guide.md y @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/assets/review_report_template.md 

        Se tienen plantillas genericas que parecen funcionar pero revisalas ya agrega o elimina lo que veas necesario y enlista los cambios para una revision posterior. 

        Ademas, Implementa `scripts/validate_review_report.py`. El script NO debe juzgar la calidad del código; debe verificar 
        aspectos deterministas del artefacto.  Debe comprobar como mínimo:
        
        ● El archivo existe. 
        ● Incluye Review Context. 
        ● Incluye Requirements / Acceptance Criteria Reviewed. 
        ● Incluye Test Evidence. 
        ● Incluye secciones MUST FIX, SHOULD FIX y OPTIONAL. 
        ● Incluye Final Review Summary. 
        ● Incluye la línea Human decision required. 
        ● Devuelve exit code 0 cuando el formato es válido y distinto de 0 cuando falta una sección.
        python .agents/skills/reviewing_pull_requests/scripts/validate_review_report.py   
        results/pr-readiness-review.md 
        
        # Expected 
        VALID: PR readiness review structure is complete. 
        exit code: 0

**AI contribution:** El agente enlisto y aplico cambios a `review_checklist.md`, `severity_guide.md`, `review_report_template.md` y creo `validate_review_report.py`. Por cada documento:
- `review_checklist.md`
  - Se añadio la seccion de "Traceability" para verificar que se actualiara ese doc
  - Se añadio la seccion de "Process" para verificar que la rama este limpia de commits "ocultos" y tenga una raiz "adecuada" (develop)
  - Se agrego que los test DEBEN ser ejecutados
  - Se agrego `AGENTS.md`en la seccion de Code y commit en evidence
- `severity_guide`
  - Se agrego un nuevo "caso" de MUST FIX: Si se viola una regla de AGENTS.md
- `review_report_template.md`
  - Se agrego commit range para evitar la amiguedad en el rango de commits abarcados en el PR
  - Se agregaron comentarios en el documento para denotar la plantilla que cada hallazgo debe tener y recalcar que SIEMPRE se requiere intervencion humana
- `validate_review_report.py`
  - Verifica existencia del archivo y las 7 secciones/línea requeridas por regex sobre encabezados ##, sin juzgar contenido.
  - Da Exit 0 si todo está completo; exit 1 listando cada MISSING: <sección> si falta algo y exit 2 si el uso de CLI es incorrecto.


**Student decision:** Se recibieron los cambios y adiciones de archivos realizadas por el agente, se eliminaron ejemplos innecesarios y se parafrasearon partes de informacion para aumentar la claridad de los documentos (en el caso de los markdown). Para el script se conservo como esta

**Impact:** `review_checklist.md`, `severity_guide.md` y `review_report_template.md` modificados y `validate_review_report.py`

---

## Entry 4

**Tool:** Claude Sonnet 5

**Date:** 28/10/2026

**Stage:** Evaluation/refinement/Test run

**Prompt:**

  Revisa el PR n# 3 e indica si está listo para una revisión humana. 
 
  Utiliza los requisitos/especificaciones del repositorio y las evidencias de las pruebas. 
  No realices ninguna publicación en GitHub. 
  Genera la revisión de forma local en: 
  results/pr-readiness-review.md

**AI contribution:** La IA genero el archivo de pr-readiness-review.md pero sin usar el skill y las plantillas provistas, por lo que este documento era incorrecto en estructra e informacion; Al no usar la skill no consulto las templates e incluyo en el documento cosas fuera de scope como jerarquias de archivos en el programa.

**Student decision:** Se descarto el documento generrado y se rehizo el prompt esta vez especificando ñla ruta del skill.

**Impact:** Primera version de `pr-readiness-review` eliminada.

---

## Entry 5

**Tool:** Claude Sonnet 5

**Date:** 28/10/2026

**Stage:** Evaluation/refinement/Test run

**Prompt:**

  Revisa el PR n# 3 e indica si está listo para una revisión humana. 
  
  Utiliza los requisitos/especificaciones del repositorio y las evidencias de las pruebas. 
  No realices ninguna publicación en GitHub. 
  Genera la revisión de forma local en: 
  results/pr-readiness-review.md
  Toda la info relacionada con la skill que se necesitara esta en @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests, como @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/SKILL.md y en el resto de directorios tambien

**AI contribution:** La IA genero el archivo de pr-readiness-review.md y redacto un resumen final de la revisom de PR #3, detectando 2 cambios en should fix.

**Student decision:** Se acepto el documento generado

**Impact:** Segunda version de `pr-readiness-review` aceptada.

---

## Entry 5

**Tool:** Claude Sonnet 5

**Date:** 29/10/2026

**Stage:** MCP configuration

**Prompt:**

  En el caso del paso 16, ya existe un @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/evals/execution_cases.json , pero son los casos que ya venian en el ADA, puedes agregar mas para que sean 5 casos (si ves pertinente reemplazar uno, aunque dudo que sea necesario, hazlo). 

  Para el paso 17 se pide ejecutar los casos de prueba Si la Skill falla, modifica primero la pieza correcta en lugar de agregar instrucciones indiscriminadamente. 

  Cuando hice una ejecucion de prueba (paso 15) se dio un error y es que el agente no detecto el skill (ni la carpetas donde estaba) asi que cuando hizo el pr-readiness-review, lo hizo sin seguir los templates, sin tomar en cuenta los trigger cases y el severity guide, por ende, omitio informacion critica y añadio informacion no solicitada, incluso saliendose del scope.

  La prompt donde surgio el error fue esta:
  Revisa el PR n# 3 e indica si está listo para una revisión humana. 
  
  Utiliza los requisitos/especificaciones del repositorio y las evidencias de las pruebas. 
  No realices ninguna publicación en GitHub. 
  Genera la revisión de forma local en: 
  results/pr-readiness-review.md
  Despues de ver que no genero el documento con la estructura adecuada, mande a la papelera al docuemnto, abri otra instacia del agente y pregunte que si detectaba la skill, esa oinstancia respondio que si y hata ubico el @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/SKILL.md . Luego abro una tercera instancia donde envie el mismo prompt con un agregado:

  Toda la info relacionada con la skill que se necesitara esta en @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests, como @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/SKILL.md y en el resto de directorios tambien

  Y esta vez si pudo detectar las skills pero por siento que fue por la info extra.

  Añade los casos de prueba que sean necesarios para que sean 5 y si puedes ejecutarlos, hazlo y documenta una iteracion (el pdf no dice donde asi que de mienttras nombra al md: skill_iteration y ponl en la segunda carpeta anidad de ada-05-spec-driven-development)

**AI contribution:** La IA genero 2 casos de pruebas extra en `execution_cases.md`: 
- execution_03: abarca las adiciones de `SKILL.md` que se encargan de revisar el rango de commits antes de asumir el alcance.
- insert_02: indica que el agente debe usar la skill y no salirse del alcance la misma (evitando el error anterior).

Tambien se genero un bosquejo de `skill_iteration.md` y se añadio 1 linea a la seccion "Project rules" de `AGENTS.md`.

**Student decision:** Se aceptaron los casos extras en `execution_cases.md`, las regla de proyecto extra en `AGENTS.md` y el archivo de la iteracion (`skill_iteration.md`). Se modifico `skill_iteration.md` para aclarar que la verion de la skill se mantiene igual (ya que la modificacion fue para `AGENTS.md`), se modifico parte del texto para hacer enfasis que el fallo fue el NO descubrimiento de la skill, se añadio una nota aclarando que `AGENTS.md` fue lo que se cambio y se añadio un cambio extra (una regla mas) que se añadio a `AGENTS.md`.

De igual manera, se añadio una regla adicional a `AGENTS.md` para que el agente pueda localizar la carpeta de skills (ya que la regla añadida por el agente fue dirigida a la skill de reviewing pull requests).

**Impact:** `execution_cases.md`, `AGENTS.md` (con cambios)y `skill_iteration.md` aceptados.

---

## Entry 6

**Tool:** Claude Sonnet 5

**Date:** 30/10/2026

**Stage:** Third party audit

**Prompt:**

  Estoy haciendo esta ADA y voy por el paso II.2, quiero instalar la skill de code-review-and-quality del repositorio de https://github.com/addyosmani/agent-skills.git
  Considerando que estamos en la extension de claude para vs code, como podria instalar la skill en el proyecto (y ando viendo si se tiene que instalar mejor todas las skills ya que segun los riesgos documentados en @ada-05-spec-driven-feature/docs/third_party_skill_audit.md, podria tener ciertas dependencia a otras skills)

  Igual si ves la manera de instalarlo en el proyecto, procura que no genere "cambios" pendientes en el repositorio (que es la segunda carpta anidada de ada-05-spec-driven-feature)  ya que los documentos que se pide en el entrega del ada 07 los movere a otro repositorio.


**AI contribution:** El agente recomendo (y corroboro) la opcion de isntalar el "paquete de skills" entero para evitar problemas de dependencias, ademas de preguntar donde se instalaba a coleccion de skills para no "ensuciar" el repositorio. Posteriormente instalo la coleccion de skills.

**Student decision:** Se decidio que el paquete de skills estaria dentro de la carpeta del repositorio y usando un .gitignore, se evitaria que se considere este cambio en el repositorio del ada 05 (que se sigue usando de base para las otras ADAS).

**Impact:** Modificacion de .gitignore y descarga de skills externas.

---

## Entry 6

**Tool:** Claude Sonnet 5

**Date:** 30/10/2026

**Stage:** Professional skill comparisson

**Prompt:**

  Siguiendo con el @ADA-07_Build_an_Agent_Skill_Ingenieria_Software.pdf , en el  paso  II.5  se debe comparra la skill personalizada (la de la carpeta @ada-05-spec-driven-feature/.agents/skills/reviewing-pull-requests/SKILL.md  ) y la Skill de terceros/profesional ( @ada-05-spec-driven-feature/.agents/skills/code-review-and-quality/SKILL.md  ).

  El archivo @ada-05-spec-driven-feature/results/pr-readiness-review.md es el resultado de la skill personalizada, mientras que @ada-05-spec-driven-feature/results/professional-skill-review.md es el resultado de la Skill de code-review-and-quality (el skill profesional)

  Podrias hacer el results/skill-comparison.md, que compare la skill personalizada con la profesional  (ver imagen adjunta) y responde estas preguntas.


**AI contribution:** El genero el archivo de skill-comparison.md (solo la tabla).

**Student decision:** Se hicieron cambios menores en la redaccion del contenido de la tabla, parafraseando algunas partes y eliminando otras, posteriormente se agregaron las preguntas y sus respuestas.

**Impact:** skill-comparison.md creado con la tabla (y posteriormente con las preguntas). Ya desde un punto de vista de aprendizaje, se noto que la skill profesional era mas "generica" y adaptable a todo tipo de revisiones y ecosistemas de skills,mientras que la skill personalizada tendia a ser mas centrada en algo especifico, lo cual puede ayudar a que no se desvie en otras responsabilidades, pero la hace mas rigida a la hora de adpatrala a otros contextos.