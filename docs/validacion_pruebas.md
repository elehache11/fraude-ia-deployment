# Documento de validación y pruebas

## Sistema de detección de fraude mediante inteligencia artificial

### 1. Objetivo y alcance

El presente documento describe las actividades de validación técnica realizadas sobre una aplicación de detección de fraude financiero basada en el modelo Random Forest desarrollado durante la Actividad 6. El propósito es comprobar el funcionamiento de sus componentes, la comunicación entre frontend y backend, la ejecución mediante contenedores Docker y el comportamiento del sistema ante diferentes escenarios de prueba.

La solución utiliza FastAPI para exponer los servicios de predicción, Streamlit como interfaz gráfica y Docker Compose para administrar ambos componentes en contenedores independientes. El modelo utiliza 30 variables predictoras y un umbral de clasificación de 0.17.

El alcance comprende pruebas funcionales, validaciones de entradas, casos extremos, consistencia entre ejecuciones y recuperación de servicios. No incluye pruebas de carga, penetración, disponibilidad en la nube ni una nueva evaluación estadística del desempeño predictivo, dado que esta última fue desarrollada durante la Actividad 6.

### 2. Entorno técnico de validación

Las pruebas se realizaron en un entorno local con las siguientes características:

| Componente               | Tecnología o configuración         |
| ------------------------ | ---------------------------------- |
| Sistema operativo        | Windows 11, versión 26H2           |
| Lenguaje de programación | Python 3.11.6                      |
| Modelo predictivo        | Random Forest                      |
| Variables predictoras    | 30                                 |
| Umbral de clasificación  | 0.17                               |
| Backend                  | FastAPI                            |
| Frontend                 | Streamlit 1.66.1                   |
| Contenerización          | Docker Engine 29.9.2               |
| Orquestación             | Docker Compose 5.6.1               |
| Virtualización           | WSL 2                              |
| Herramientas de prueba   | Swagger, PowerShell, curl y pytest |
| Puerto del backend       | 8000                               |
| Puerto del frontend      | 8501                               |

La arquitectura implementada separa la interfaz de usuario del procesamiento predictivo. Streamlit captura las características de la transacción y las transmite mediante solicitudes HTTP al endpoint `/predict` de FastAPI. El backend valida los datos, ejecuta el modelo Random Forest y devuelve la probabilidad estimada de fraude y su clasificación.

La ejecución contenerizada utiliza dos imágenes independientes, administradas mediante Docker Compose. La comunicación entre servicios se establece a través de la red interna de Docker, utilizando el nombre del servicio `backend`.

### 3. Metodología de validación

La estrategia de pruebas se organizó en cuatro categorías principales:

**Pruebas funcionales.** Verificaron la disponibilidad de los servicios, el funcionamiento de los endpoints, la generación de predicciones y la integración entre los componentes.

**Pruebas negativas y casos extremos.** Evaluaron el comportamiento del sistema ante valores no numéricos, variables adicionales, estructuras incorrectas, solicitudes vacías e importes elevados.

**Pruebas de consistencia.** Comprobaron que una misma transacción produjera resultados idénticos en ejecuciones consecutivas y en los entornos de Windows y Docker.

**Pruebas operativas.** Verificaron la construcción de imágenes, ejecución de contenedores, comunicación entre servicios, detención controlada y recuperación posterior.

Para cada prueba se definieron las condiciones de ejecución, el resultado esperado y el comportamiento observado. Las evidencias se conservaron mediante capturas de pantalla identificadas individualmente.

### 4. Resultados de las pruebas

#### 4.1. Validaciones funcionales e integración

Durante las etapas previas se comprobaron las principales funcionalidades del sistema.

| Validación                        | Resultado obtenido                         | Estado   |
| --------------------------------- | ------------------------------------------ | -------- |
| Disponibilidad de FastAPI         | Endpoint `/health` respondió correctamente | Aprobada |
| Información del modelo            | 30 variables y umbral 0.17                 | Aprobada |
| Predicción mediante API           | Probabilidad y clasificación generadas     | Aprobada |
| Pruebas automatizadas con pytest  | 2 pruebas aprobadas                        | Aprobada |
| Ejecución de Streamlit            | Interfaz disponible                        | Aprobada |
| Integración frontend-backend      | Comunicación HTTP funcional                | Aprobada |
| Manejo de errores de conexión     | Mensaje controlado ante interrupción       | Aprobada |
| Recuperación de la comunicación   | Predicciones restablecidas                 | Aprobada |
| Construcción de imágenes Docker   | Backend y frontend construidos             | Aprobada |
| Ejecución mediante Docker Compose | Ambos contenedores funcionando             | Aprobada |
| Recuperación de contenedores      | Servicios reiniciados correctamente        | Aprobada |

Estas comprobaciones permitieron demostrar que la aplicación puede ejecutarse tanto directamente desde Windows como mediante contenedores Docker, conservando las funcionalidades principales.

#### 4.2. Validación automatizada del backend

Se realizó una comprobación desde PowerShell contra el endpoint `/health` del backend contenerizado.

El procedimiento verificó que la API respondiera correctamente y reportara la disponibilidad del modelo.

| Identificador | Resultado esperado              | Resultado obtenido          | Estado   |
| ------------- | ------------------------------- | --------------------------- | -------- |
| P-5.1         | Estado `ok` y modelo disponible | Ambas condiciones cumplidas | Aprobada |

**Evidencia:** `E32_Prueba_Automatizada_Docker.png`

#### 4.3. Pruebas de casos extremos

Se ejecutaron cinco pruebas orientadas a evaluar el comportamiento de la API ante entradas incorrectas o poco habituales.

| ID   | Escenario                        | Resultado esperado   | Resultado obtenido | Estado                | Evidencia |
| ---- | -------------------------------- | -------------------- | ------------------ | --------------------- | --------- |
| CE01 | Variable con valor no numérico   | HTTP 422             | HTTP 422           | Aprobada              | E33       |
| CE02 | Variable adicional no reconocida | Rechazo controlado   | HTTP 422           | Aprobada              | E34       |
| CE03 | Estructura JSON incorrecta       | HTTP 422             | HTTP 422           | Aprobada              | E35       |
| CE04 | Importe extremadamente elevado   | Respuesta controlada | HTTP 200           | Aprobada técnicamente | E36       |
| CE05 | Solicitud sin contenido          | HTTP 422             | HTTP 422           | Aprobada              | E37       |

En CE01, la API rechazó un valor de texto introducido en una variable numérica.

En CE02, identificó correctamente la variable `Variable_Extra`, indicando que no existían variables faltantes, pero sí un campo adicional no reconocido.

En CE03, detectó la ausencia del objeto obligatorio `features` y devolvió un mensaje de campo requerido.

En CE04, procesó una transacción con importe de 1,000,000 y devolvió una probabilidad estimada de fraude de 0, clasificación legítima y umbral de 0.17. La prueba confirma que el sistema puede procesar ese valor sin errores, pero no demuestra que la predicción sea confiable para importes fuera de la distribución de entrenamiento.

Finalmente, en CE05, FastAPI rechazó una solicitud POST sin contenido, devolviendo HTTP 422 y un mensaje que identificaba la ausencia del cuerpo de la solicitud.

Las cinco pruebas produjeron respuestas acordes con los criterios técnicos establecidos.

#### 4.4. Pruebas de consistencia

Se realizaron dos pruebas para comprobar la reproducibilidad de las predicciones.

| ID   | Escenario                                                 | Resultado obtenido        | Estado   | Evidencia |
| ---- | --------------------------------------------------------- | ------------------------- | -------- | --------- |
| PC01 | Tres ejecuciones consecutivas de una transacción idéntica | Tres respuestas idénticas | Aprobada | E38       |
| PC02 | Comparación de predicciones entre Windows y Docker        | Resultados coincidentes   | Aprobada | E39       |

Para ambas pruebas se utilizó una transacción sintética con `Time = 0`, `Amount = 100` y las variables `V1–V28` iguales a cero.

Los resultados obtenidos fueron:

| Parámetro                       | Resultado                |
| ------------------------------- | ------------------------ |
| Probabilidad estimada de fraude | 0                        |
| Clasificación                   | 0 — Transacción legítima |
| Umbral utilizado                | 0.17                     |

La prueba PC01 confirmó la consistencia de tres respuestas consecutivas del backend contenerizado.

La prueba PC02 confirmó que la ejecución directa mediante Python en Windows y la ejecución dentro de Docker devolvieron la misma respuesta.

Estos resultados respaldan la consistencia funcional para la entrada evaluada. No permiten generalizar esa equivalencia a todas las transacciones posibles sin realizar pruebas adicionales.

### 5. Hallazgos y limitaciones

Las pruebas identificaron los siguientes aspectos relevantes.

**Integración funcional.** La comunicación entre frontend, backend y modelo predictivo funciona correctamente. La arquitectura permite separar la presentación de información del procesamiento de predicciones.

**Portabilidad.** La aplicación pudo ejecutarse mediante contenedores Docker, manteniendo los resultados observados en el entorno local para las transacciones evaluadas. Esto respalda la viabilidad técnica de trasladar la solución a otros entornos compatibles.

**Validación de entradas.** La API rechazó solicitudes con datos no numéricos, variables adicionales, estructuras incorrectas y cuerpos vacíos. Estas verificaciones constituyen controles básicos para proteger la integridad de las solicitudes.

**Continuidad operativa.** Las pruebas confirmaron que los contenedores pueden detenerse y reiniciarse, recuperando posteriormente la comunicación y la capacidad de generar predicciones.

**Valores extremos.** El procesamiento exitoso de un importe elevado no garantiza que el modelo produzca estimaciones confiables fuera de los rangos observados durante el entrenamiento. Es recomendable, en ejercicios posteriores, incorporar controles de valores atípicos y monitoreo de la distribución de datos.

Los resultados de precisión, recall, F1-score y ROC-AUC del modelo corresponden a la Actividad 6 y no fueron recalculados durante esta etapa.

### 6. Conclusiones

Las actividades de validación permitieron comprobar satisfactoriamente el funcionamiento técnico de la aplicación de detección de fraude basada en Random Forest. La solución integra una interfaz Streamlit, una API FastAPI y un modelo previamente entrenado, utilizando Docker y Docker Compose para facilitar su ejecución local.

Las ocho pruebas realizadas durante esta etapa produjeron resultados satisfactorios conforme a los criterios establecidos. Las validaciones de etapas anteriores complementan esta evidencia al demostrar la construcción de imágenes, integración entre servicios, generación de predicciones y recuperación operativa.

En conjunto, los resultados permiten concluir que la aplicación cuenta con una base técnica funcional y portable para preparar su despliegue en la nube. Sin embargo, antes de considerarla apta para un entorno productivo, sería necesario ampliar las pruebas de seguridad, rendimiento, disponibilidad, monitoreo y comportamiento predictivo ante datos no representados adecuadamente durante el entrenamiento.

Por lo tanto, **la solución se considera técnicamente validada para un entorno local de demostración**.