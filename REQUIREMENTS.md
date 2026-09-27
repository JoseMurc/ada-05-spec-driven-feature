# Requirements — Customer Search 
 
## User Story 
As a user, 
I want to search customers by name or email, 
so that I can quickly find the customer record I need. 
 
## Functional Requirements 
- FR-01: El sistema deberá exponer un único campo de búsqueda que consulta simultáneamente los atributos nombre y email del cliente al usuario, devolviendo la unión de coincidencias sin duplicados.
- FR-02: El sistema debe devolver coincidencias por subcadena, insensibles a mayúsculas/minúsculas y a diacríticos, aplicadas por igual sobre nombre y email.
- FR-03: El sistema deberá devolver el mismo conjunto de resultados, en el mismo orden, para términos de búsqueda que difieran únicamente en mayúsculas/minúsculas o en diacríticos (acentos agudos, graves, circunflejos y diéresis).
- FR-04: El sistema deberá devolver el mismo conjunto de resultados, en el mismo orden, para términos de búsqueda que difieran únicamente en caracteres de espacio en blanco al inicio o al final. 
- FR-05: El sistema deberá tratar una consulta compuesta únicamente por espacios como consulta vacía, devolviendo un resultado vacío con estado explícito, sin ejecutar búsqueda y sin error. 
- FR-06: El sistema deberá devolver una lista vacía, un código de estado de negocio NO_RESULTS y un mensaje fijo definido por el sistema cuando la búsqueda no tenga coincidencias.
- FR-07: La respuesta no contiene más de 50 elementos y siempre incluye el total de coincidencias; el exceso se trunca sin mecanismo de paginación.
- FR-08: El sistema ordena los resultados por coincidencia exacta, luego por posición del match, con desempate alfabético y por identificador de cliente.
- FR-09:  El sistema deberá devolver resultados según el alcance de datos autorizado para el usuario buscador; en esta entrega el alcance autorizado es el catálogo completo para todo usuario, sin particiones ni roles.
- FR-10: El sistema deberá devolver como respuesta únicamente los campos cliente_id, nombre y email; ningún otro campo del modelo de datos se expone en resultados.
 
## Non-Functional Requirements 
- NFR-01:El endpoint de búsqueda responde en ≤50 ms en el percentil 95 y ≤100 ms en el percentil 99, bajo una carga sostenida de 1 consultas por segundo, sobre un catálogo de 1000 clientes.
- NFR-02: No aplica en esta entrega — C-05 excluye sesión, autenticación y TLS en una ejecución local, mono-proceso y mono-usuario. Texto original, aplicable solo si el alcance cambia a un despliegue expuesto en red: "Todo acceso a la búsqueda ocurre sobre TLS 1.2+, requiere sesión autenticada y queda registrado en el log de auditoría con usuario, timestamp, término normalizado y cantidad de resultados, sin almacenar datos personales del cliente en el log."
- NFR-03: No aplica en esta entrega — C-05 excluye explícitamente la limitación de tasa en una ejecución local mono-usuario. Texto original, aplicable solo si el alcance cambia a un despliegue multiusuario expuesto en red: "El endpoint deberá aplicar limitación de tasa de 60 peticiones por minuto por usuario; al excederse responde HTTP 429 sin revelar información de clientes."
- NFR-04: No aplica en esta entrega — C-04 excluye toda interfaz web; no existe navegador, SO ni breakpoint que verificar. Texto original, aplicable solo si se agrega una interfaz web: "La interfaz de búsqueda es operable sin pérdida de funcionalidad ni scroll horizontal en los navegadores en cada combinación de navegador/SO/breakpoint."
- NFR-05: No aplica en esta entrega — C-04 excluye toda interfaz web; no existen componentes de UI que auditar por teclado o lector de pantalla. Texto original, aplicable solo si se agrega una interfaz web: "El campo de búsqueda es navegable por teclado, tiene etiqueta accesible y anuncia el número de resultados."

## Preguntas Abiertas 
- Q-01: ¿Qué estados de cliente son buscables?
  - Decisión: todos los registros del dataset son buscables; no se modelan estados de cliente (A-07). 
- Q-02: ¿Cómo se define el alcance de datos por rol/usuario (qué ve cada rol)?
  - Decisión: alcance único y total sobre el dataset local; no hay roles ni particiones (A-07, C-05). FR-09 se verifica con una matriz de un solo perfil.
- Q-03: ¿"Nombre" es un solo campo de texto libre o nombre/apellidos separados? ¿Se puede buscar por apellido solo?
  - Decisión: un único campo de texto libre con el nombre completo; al ser coincidencia por subcadena, buscar solo el apellido funciona sin campo dedicado (A-02, A-01).
- Q-04: ¿Qué tipo(s) de coincidencia parcial se soportan (prefijo, subcadena, por token, todos los tokens, difusa) y aplica igual a nombre y a email?
  - Decisión: subcadena en cualquier posición, insensible a mayúsculas/minúsculas y diacríticos, idéntica para nombre y email (A-01). No se soporta coincidencia difusa.
- Q-05: ¿La lista de resultados se actualiza mientras el usuario escribe o solo tras un envío explícito?
  - Decisión: solo tras envío explícito (comando o petición); no hay actualización incremental por pulsación (C-04).
- Q-06: ¿Se soportan operadores/comodines en la entrada, o todo el texto se trata siempre como literal?
  - Decisión: toda la entrada se trata como literal; no se soportan operadores, comodines ni expresiones regulares.
- Q-07: ¿Cuáles son los criterios de ordenamiento y su prioridad (coincidencia exacta, posición del match, estado, recencia, alfabético)?
  - Decisión: coincidencia exacta, luego coincidencia al inicio del campo, luego coincidencia en cualquier posición; dentro de cada grupo, alfabético por nombre y desempate por cliente_id (A-04, FR-08). No se usan estado ni recencia por A-07.
- Q-08: ¿Cuál es el límite máximo de resultados por respuesta (<N>)?
  - Decisión: N = 50, acompañado del total de coincidencias (A-05, FR-07).
- Q-09: ¿Qué mecanismo de acceso al resto de resultados se usa: paginación, scroll incremental u otro?
  - Decisión: truncamiento simple a N con total informado; sin paginación por lotes ni scroll incremental (A-11).
- Q-10: ¿Qué campos del cliente son visibles en los resultados (lista blanca) y cuáles se consideran sensibles?
  - Decisión: lista blanca = {cliente_id, nombre, email}; el modelo de dominio no incluye campos sensibles (A-06). 
- Q-11: ¿Cuál es el texto exacto (por idioma) del mensaje de "sin resultados" y qué acción ofrece?
  - Decisión: texto fijo en un único idioma (español), sin catálogo ni i18n; el mensaje sugiere revisar o limpiar el término de búsqueda (A-08, FR-06).
- Q-12: ¿Qué comportamiento tiene la pantalla con consulta vacía: en blanco, listado por defecto, u otro?
  - Decisión: no se ejecuta búsqueda; se devuelve resultado vacío con estado explícito y sin error (A-03, FR-05). 
- Q-13: ¿Cuál es el umbral de latencia aceptable (p95/p99) y bajo qué carga (QPS) y volumen de clientes (<V>)?
  - Decisión: p95 ≤ 50 ms, p99 ≤ 100 ms, medidos de forma local y secuencial (1 consulta por segundo) sobre 1 000 clientes en memoria (NFR-01, C-08, A-09). No hay carga concurrente declarada.
- Q-14: ¿Cuál es el límite de tasa por usuario (<R> peticiones/minuto) antes de bloquear la búsqueda?
  - Decisión: R = 60 como valor de referencia; no se implementa en esta entrega por C-05 (NFR-03).
- Q-15: ¿Qué controles de auditoría se requieren sobre las búsquedas realizadas (retención de logs, anonimización)?
  - Decisión: no aplica en esta entrega; C-05 excluye sesión y usuario identificable, por lo que no hay log de auditoría que definir (NFR-02).
- Q-16: ¿Cuál es la matriz oficial de navegadores, sistemas operativos y breakpoints soportados (<matriz>)?
  - Decisión: no aplica; la feature se entrega como CLI/API local sin interfaz web (C-04, NFR-04, NFR-05).
 
## Restricciones
- C-01: La solución se implementa en Python 3.11+ con pytest como único framework de pruebas.
- C-02: La persistencia se limita a memoria o a un archivo JSON local; no se usa motor de base de datos.
- C-03: No se usan servicios, APIs o modelos de pago; las dependencias se restringen a la librería estándar más pytest, y cualquier dependencia adicional requiere justificación explícita.
- C-04: La feature se entrega como interfaz local (CLI o API HTTP local); no existe interfaz web ni cliente móvil, por lo que no aplica matriz de navegadores, breakpoints ni accesibilidad de UI.
- C-05: La ejecución es local, mono-proceso y mono-usuario; no hay sesión, autenticación, autorización por rol, TLS ni limitación de tasa.
- C-06: El control de versiones es Git, con commits incrementales por tarea.
- C-07: El código es producido por un coding agent y debe ser revisado y validado por el desarrollador antes de integrarse.
- C-08: El conjunto de datos de trabajo es un dataset local acotado (≤ 1 000 clientes), suficiente para pruebas funcionales y de latencia, pero no para pruebas de carga concurrente.

## Suposiciones
- A-01: Coincidencia parcial se interpreta como subcadena en cualquier posición, insensible a mayúsculas/minúsculas y a diacríticos, aplicada por igual a nombre y a correo electrónico.
- A-02: El nombre del cliente es un único campo de texto libre que contiene el nombre completo; No se modelan nombre y apellidos como campos separados.
- A-03: Una consulta vacía o compuesta solo por espacios no ejecuta búsqueda y devuelve un resultado vacío con estado explícito, sin error.
- A-04: El orden de resultados es: coincidencia exacta, luego coincidencia al inicio del campo, luego coincidencia en cualquier posición; dentro de cada grupo, orden alfabético por nombre y desempate por identificador de cliente.
- A-05: El límite máximo de resultados por respuesta es 50, acompañado del total de coincidencias.
- A-06: Los campos expuestos en los resultados son identificador, nombre y correo electrónico; el modelo de dominio no incluye campos clasificados como sensibles.
- A-07: Todos los clientes del conjunto de datos son buscables; no se modelan estados de cliente (activo, inactivo, eliminado) ni particiones de datos por alcance de usuario.
- A-08: Los mensajes al usuario se emiten en un único idioma con texto fijo; no se implementa catálogo de textos ni internacionalización.
- A-09: El umbral de rendimiento se verifica de forma local y secuencial sobre el dataset acotado, sin carga concurrente declarada.
- A-10: A-01 a A-09 y A-11 son decisiones tomadas por el desarrollador, que asume el rol de responsable del producto a falta de uno externo, y quedan registradas como tales; un cambio en cualquiera de ellas obliga a revisar los requisitos afectados antes de la especificación y las pruebas.
- A-11: El mecanismo de acceso a resultados más allá del límite de FR-07 es truncamiento simple con total informado; no se implementa paginación por lotes ni scroll incremental.



Nota: REQUIREMENTS.md es la fuente de la verdad para FR/NFR