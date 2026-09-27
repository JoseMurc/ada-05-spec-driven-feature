# Customer Search Feature 
 
## Goal 
Proveer una búsqueda local de clientes por nombre o email, mediante un único campo de entrada, que devuelva coincidencias parciales normalizadas de forma determinista y acotada.
 
## Requirements Covered  
- FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-10
- NFR-01, NFR-02, NFR-03

NFR-02 y NFR-03 están marcados como "No aplica en esta entrega" en REQUIREMENTS.md (C-05: ejecución local mono-usuario). Se listan aquí porque el alcance de este incremento sí decide explícitamente qué comportamiento tienen — ninguno — y ese comportamiento se especifica en Error Handling.
## Scope 
 
- Un único campo de búsqueda que consulta nombre y email simultáneamente (FR-01).
- Coincidencia por subcadena, insensible a mayúsculas/minúsculas y diacríticos (FR-02, FR-03).
- Recorte de espacios al inicio/fin de la entrada; preservación de espacios internos (FR-04).
- Clasificación de consulta vacía o solo espacios como consulta vacía, sin ejecutar búsqueda (FR-05).
- Respuesta explícita de "sin resultados" cuando no hay coincidencias (FR-06).
- Verificación de latencia bajo carga local secuencial (NFR-01).
- Truncamiento a 50 resultados con total de coincidencias informado (FR-07).
- Ordenamiento determinista con desempate por cliente_id (FR-08).
- Alcance de datos único (catálogo completo) para cualquier usuario buscador (FR-09).
- Lista blanca de campos en la respuesta: cliente_id, nombre, email (FR-10).

## Out of Scope 

- Sesión, autenticación, TLS y log de auditoría (NFR-02 — no aplica, C-05).
- Limitación de tasa (NFR-03 — no aplica, C-05).
- Interfaz web, matriz de navegador/SO/breakpoint y accesibilidad de UI (NFR-04, NFR-05 — no aplica, C-04).
- Paginación por lotes o scroll incremental (A-11: truncamiento simple con total informado).
- Roles y particiones de datos por usuario (A-07; FR-09 se cubre en su forma degenerada, alcance único).
- Búsqueda difusa, operadores y comodines (Q-04, Q-06).

 
## Domain Model 
Customer:
- cliente_id: str — identificador estable y único.
- nombre: str — texto libre, nombre completo (A-02).
- email: str — dirección de correo del cliente.
Storage: persistencia en memoria o archivo JSON local (C-02). La estructura de indexado y el mecanismo de normalización interna son decisiones técnicas de ARCHITECTURE.md, no de esta especificación.

## Search Rules 
- SR-01 [FR-01]: Una consulta se compara simultáneamente contra `nombre` y `email`; el resultado es la unión de las coincidencias de ambos campos, sin duplicados por `cliente_id`.
- SR-02 [FR-02]: Existe coincidencia cuando la consulta normalizada aparece como subcadena en cualquier posición del campo normalizado (no solo al inicio).
- SR-03 [FR-03]: Antes de comparar, tanto la consulta como los campos indexados se normalizan a minúsculas y sin diacríticos (á/à/â/ä → a, y análogos).
- SR-04 [FR-04]: Los espacios al inicio y al final de la consulta se recortan antes de normalizar; los espacios internos se preservan y participan en la comparación.
- SR-05 [FR-05]: Una consulta vacía o compuesta únicamente por espacios se clasifica como consulta vacía y no dispara búsqueda.
- SR-06 [FR-07]: El resultado se trunca a un máximo de 50 elementos; la respuesta siempre incluye el total real de coincidencias, sea cual sea ese total.
- SR-07 [FR-08]: Orden: (1) coincidencia exacta, (2) coincidencia al inicio del campo, (3) coincidencia en cualquier posición; dentro de cada grupo, alfabético por nombre, desempate por cliente_id.
- SR-08 [FR-09]: El alcance de datos autorizado es el catálogo completo para cualquier usuario buscador; no existen particiones ni roles en este incremento (A-07).
- SR-09 [FR-10]: La respuesta expone únicamente cliente_id, nombre y email; ningún otro campo del dominio se incluye.
 
## Validation Rules 
- VR-01 [FR-01, FR-02]: La entrada se trata siempre como texto literal; no se interpretan comodines, operadores ni expresiones regulares.
- VR-02 [FR-05]: No hay longitud mínima de consulta distinta de la regla de consulta vacía (SR-05); una consulta de un solo carácter no vacío es válida y se ejecuta.
- VR-03 [FR-07]: El límite de 50 no es configurable por quien llama; es un valor fijo del sistema.
 
## Error Handling 
- EH-01 [FR-05]: Consulta vacía → no se ejecuta búsqueda; se devuelve el estado de consulta vacía definido (sin ejecutar), sin lanzar error.
- EH-02 [FR-06]: Consulta sin coincidencias → se devuelve lista vacía, estado de negocio `NO_RESULTS` y el mensaje fijo definido, sin lanzar error.
- EH-03 [NFR-02]: N/A — no existe sesión, autenticación ni canal TLS en el alcance local mono-usuario (C-05); no hay error de autenticación/transporte que manejar.
- EH-04 [NFR-03]: N/A — no existe limitación de tasa en el alcance local mono-usuario (C-05); no hay respuesta de bloqueo (HTTP 429 o equivalente) que manejar.
 
## Acceptance Criteria 
- AC-01 [FR-01]: Una consulta que coincide solo por nombre y otra que coincide solo por email devuelven cada una al cliente correspondiente.
- AC-02 [FR-01]: Un cliente cuyo nombre y email coinciden con la misma consulta aparece exactamente una vez en el resultado.
- AC-03 [FR-02]: Una consulta que coincide en medio o al final de un campo (no al inicio) devuelve al cliente correspondiente.
- AC-04 [FR-03]: Las consultas "JOSÉ", "jose" y "José" devuelven el mismo conjunto de resultados.
- AC-05 [FR-04]: Las consultas "ana" y " ana " devuelven el mismo conjunto de resultados, en el mismo orden.
- AC-06 [FR-05]: Una consulta compuesta solo de espacios devuelve el estado de consulta vacía, sin ejecutar búsqueda y sin error.
- AC-07 [FR-06]: Una consulta sin coincidencias devuelve lista vacía, estado `NO_RESULTS` y el mensaje definido.
- AC-08 [NFR-01]: Sobre un catálogo de 1 000 clientes, con carga secuencial de 1 consulta por segundo, la latencia observada es ≤ 50 ms en p95 y ≤ 100 ms en p99.
- AC-09 [FR-07]: Con más de 50 coincidencias, la respuesta contiene exactamente 50 elementos y el total real de coincidencias.
- AC-10 [FR-08]: Ejecutar la misma consulta varias veces produce siempre el mismo orden de resultados.
- AC-11 [FR-09]: Cualquier usuario que ejecute la misma consulta recibe el mismo conjunto de resultados.
- AC-12 [FR-10]: Cada objeto cliente en la respuesta contiene únicamente las claves cliente_id, nombre y email.
- AC-13 [FR-08]: Dado un conjunto con coincidencia exacta, coincidencia al inicio y coincidencia interna, el resultado las devuelve en ese orden, con desempate alfabético y por cliente_id.

## Test Scenarios 
- TS-01 -> AC-01
- TS-02 -> AC-02
- TS-03 -> AC-03
- TS-04 -> AC-04
- TS-05 -> AC-05
- TS-06 -> AC-06
- TS-07 -> AC-07
- TS-08 -> AC-08 (medición de latencia, no unitario)
- TS-09 -> AC-09
- TS-10 -> AC-10
- TS-11 -> AC-11
- TS-12 -> AC-12
- TS-13 -> AC-13
 
## Constraints 
- C-01, C-02, C-03: stack, persistencia y dependencias permitidas para toda la implementación de esta spec.
- C-05: justifica que EH-03 y EH-04 sean N/A (no aplica sesión, TLS ni rate limiting).
- C-08: acota el dataset a ≤ 1 000 clientes usado en AC-08/TS-08.
- C-04: limita la entrega a interfaz local (CLI o API HTTP local); justifica que NFR-04 y NFR-05 no apliquen.
 
## Open Questions 
N/A — todas las decisiones necesarias para FR-01–FR-10 y NFR-01–NFR-03 ya están resueltas en REQUIREMENTS.md (Q-01 a Q-16). No quedan preguntas abiertas dentro del alcance de este incremento.