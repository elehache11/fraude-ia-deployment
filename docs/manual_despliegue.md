# Manual y estrategia de despliegue en la nube

## Sistema de detección de fraude mediante inteligencia artificial

### 1. Objetivo y alcance

Este manual describe la estrategia propuesta para desplegar en Microsoft Azure una aplicación de detección de fraude financiero basada en un modelo de inteligencia artificial Random Forest, desarrollado y evaluado durante la Actividad 6.

La aplicación utiliza FastAPI como backend para procesar solicitudes de predicción, Streamlit como interfaz gráfica y Docker para contenerizar ambos servicios. El modelo recibe 30 variables predictoras y utiliza un umbral de clasificación de 0.17.

El objetivo es definir un procedimiento técnicamente viable y reproducible para trasladar esta solución desde un entorno local hacia infraestructura de nube.

**Alcance:** se verificó el funcionamiento de las imágenes y contenedores en el entorno local, pero no se crearon recursos ni se ejecutaron despliegues reales en Azure. Las configuraciones de nube descritas representan una propuesta para una implementación futura.

### 2. Arquitectura y plataforma seleccionada

Se seleccionó **Microsoft Azure Container Apps** como servicio de referencia para ejecutar la aplicación.

Esta plataforma permite administrar aplicaciones contenerizadas sin gestionar directamente servidores o clústeres de Kubernetes.

La arquitectura propuesta contempla dos aplicaciones independientes dentro de un mismo entorno de Azure Container Apps.

| Componente           | Tecnología                       | Configuración propuesta                            |
| -------------------- | -------------------------------- | -------------------------------------------------- |
| Frontend             | Streamlit                        | Acceso externo mediante HTTPS, puerto interno 8501 |
| Backend              | FastAPI                          | Acceso interno, puerto 8000                        |
| Modelo predictivo    | Random Forest                    | Integrado en la imagen del backend                 |
| Registro de imágenes | Azure Container Registry         | Repositorios privados para ambas imágenes          |
| Entorno de ejecución | Azure Container Apps Environment | Red y configuración compartidas                    |

El usuario accede al frontend mediante HTTPS. Streamlit envía las solicitudes al backend utilizando la red interna de Azure Container Apps.

La decisión de mantener privado el backend busca reducir su exposición directa a internet.

La solución conserva la separación de responsabilidades implementada previamente mediante Docker Compose.

### 3. Requisitos técnicos

#### 3.1. Componentes disponibles

Durante el desarrollo local se verificaron los siguientes elementos:

| Elemento                             | Estado                        |
| ------------------------------------ | ----------------------------- |
| Código fuente del backend FastAPI    | Disponible                    |
| Código fuente del frontend Streamlit | Disponible                    |
| Modelo Random Forest serializado     | Disponible                    |
| Imagen `fraude-backend:1.0`          | Verificada                    |
| Imagen `fraude-frontend:1.0`         | Verificada                    |
| Sistema operativo de imágenes        | Linux                         |
| Arquitectura de imágenes             | amd64                         |
| Configuración Docker Compose         | Validada                      |
| Comunicación entre servicios         | Validada                      |
| Pruebas funcionales                  | Ejecutadas satisfactoriamente |

Las imágenes utilizan una arquitectura compatible con el entorno Linux propuesto, aunque su funcionamiento específico en Azure queda pendiente de validación.

#### 3.2. Recursos necesarios en Azure

Para ejecutar el despliegue se requieren los siguientes recursos:

| Recurso                    | Nombre ilustrativo | Función                                         |
| -------------------------- | ------------------ | ----------------------------------------------- |
| Resource Group             | `rg-fraude-ia`     | Administrar los recursos                        |
| Azure Container Registry   | `acrfraudeia`      | Almacenar imágenes                              |
| Container Apps Environment | `env-fraude-ia`    | Ejecutar los servicios en un entorno compartido |
| Container App Backend      | `fraude-backend`   | Ejecutar la API                                 |
| Container App Frontend     | `fraude-frontend`  | Ejecutar la interfaz                            |

También se requiere una suscripción de Azure, permisos suficientes para crear recursos y mecanismos de autenticación para publicar y recuperar las imágenes.

Los nombres definitivos y las capacidades de cómputo deben validarse antes de una implementación real.

### 4. Procedimiento propuesto de despliegue

El despliegue se organiza en seis actividades secuenciales.

#### Paso 1. Crear el grupo de recursos

Desde Azure Portal o Azure CLI se crea un grupo de recursos denominado, por ejemplo, `rg-fraude-ia`.

Este recurso permite administrar de manera conjunta los componentes del proyecto, incluyendo sus configuraciones, permisos y costos.

Se selecciona una región compatible con Azure Container Apps y con los requisitos de residencia de datos aplicables.

#### Paso 2. Crear Azure Container Registry

Se configura un registro privado de contenedores para almacenar las imágenes del backend y frontend.

El registro permite que Azure Container Apps obtenga las imágenes necesarias para ejecutar los servicios.

El acceso se controla mediante identidades y permisos específicos.

#### Paso 3. Etiquetar y publicar las imágenes

Las imágenes existentes se etiquetan utilizando la dirección asignada al registro de Azure.

Como ejemplo, suponiendo que el registro se denomina `acrfraudeia`, se utilizan los siguientes comandos:

**Backend:**

`docker tag fraude-backend:1.0 acrfraudeia.azurecr.io/fraude-backend:1.0`

`docker push acrfraudeia.azurecr.io/fraude-backend:1.0`

**Frontend:**

`docker tag fraude-frontend:1.0 acrfraudeia.azurecr.io/fraude-frontend:1.0`

`docker push acrfraudeia.azurecr.io/fraude-frontend:1.0`

Antes de la publicación es necesario autenticarse en el registro con los permisos correspondientes.

#### Paso 4. Crear el entorno de Azure Container Apps

Se crea un entorno denominado `env-fraude-ia`.

Este recurso proporciona el contexto compartido para ejecutar ambas aplicaciones y permitir su comunicación interna.

Durante la configuración se definen los recursos de cómputo, las opciones de red y los mecanismos de observabilidad.

#### Paso 5. Desplegar el backend FastAPI

Se crea una aplicación de contenedor denominada `fraude-backend`, utilizando la imagen almacenada en Azure Container Registry.

La configuración propuesta es:

| Parámetro               | Valor                     |
| ----------------------- | ------------------------- |
| Imagen                  | `fraude-backend:1.0`      |
| Puerto de aplicación    | 8000                      |
| Ingreso                 | Interno                   |
| Protocolo de aplicación | HTTP                      |
| Acceso desde internet   | No permitido directamente |

Se establece una verificación de disponibilidad mediante el endpoint `/health`.

Una vez iniciado el servicio, se comprueba que el modelo esté disponible y que el endpoint `/model-info` devuelve la configuración esperada.

#### Paso 6. Desplegar el frontend Streamlit

Se crea una segunda aplicación denominada `fraude-frontend`.

La configuración propuesta es:

| Parámetro            | Valor                           |
| -------------------- | ------------------------------- |
| Imagen               | `fraude-frontend:1.0`           |
| Puerto de aplicación | 8501                            |
| Ingreso              | Externo                         |
| Acceso de usuarios   | HTTPS                           |
| Variable de entorno  | `API_URL=http://fraude-backend` |

La dirección interna utilizada para `API_URL` permite que Streamlit envíe solicitudes al backend dentro del mismo entorno de Azure Container Apps.

### 5. Estrategia de validación del despliegue

Una vez publicados ambos servicios, se ejecuta una secuencia de pruebas para comprobar su funcionamiento.

| Prueba | Validación                 | Criterio de aceptación                                                                  |
| ------ | -------------------------- | --------------------------------------------------------------------------------------- |
| VD01   | Disponibilidad del backend | Respuesta correcta de `/health`                                                         |
| VD02   | Configuración del modelo   | 30 variables y umbral 0.17                                                              |
| VD03   | Acceso al frontend         | Interfaz disponible mediante HTTPS                                                      |
| VD04   | Integración de servicios   | Streamlit recibe predicciones de FastAPI                                                |
| VD05   | Consistencia predictiva    | Resultados equivalentes a los obtenidos localmente para las transacciones de referencia |
| VD06   | Manejo de errores          | Solicitudes inválidas rechazadas de forma controlada                                    |
| VD07   | Recuperación               | Restablecimiento del servicio ante una interrupción simulada                            |

Estas pruebas retoman los criterios y procedimientos utilizados durante la validación local.

### 6. Seguridad, monitoreo y recuperación

#### 6.1. Seguridad

La estrategia de seguridad contempla restringir el acceso al backend, mantener privado el registro de imágenes y utilizar HTTPS para el frontend.

Asimismo, antes de trabajar con información financiera real, es necesario incorporar autenticación, autorización, gestión segura de secretos y controles de protección de datos.

También deben establecerse mecanismos de actualización y revisión de vulnerabilidades de las imágenes Docker.

#### 6.2. Monitoreo

Para supervisar el funcionamiento de la aplicación se propone utilizar las capacidades de observabilidad de Azure Container Apps y sus integraciones con Azure Monitor.

Los indicadores principales serían:

| Indicador                   | Propósito                       |
| --------------------------- | ------------------------------- |
| Disponibilidad del servicio | Identificar interrupciones      |
| Errores HTTP 5xx            | Detectar fallas internas        |
| Solicitudes HTTP 4xx        | Identificar entradas rechazadas |
| Tiempo de respuesta         | Evaluar rendimiento             |
| CPU y memoria               | Detectar saturación             |
| Reinicios de contenedores   | Identificar inestabilidad       |

Se deben definir umbrales de alerta y responsables de atención.

#### 6.3. Recuperación

La estrategia contempla utilizar los mecanismos de administración de instancias de Azure Container Apps para recuperar servicios afectados por interrupciones.

También se propone conservar revisiones previamente validadas que permitan revertir actualizaciones defectuosas.

Como antecedente local, se verificó que ambos contenedores Docker utilizan la política `unless-stopped` y que los servicios pueden recuperarse después de detenerse y reiniciarse.

### 7. Documentación, limitaciones y conclusiones

#### 7.1. Herramientas utilizadas

La preparación técnica del proyecto consideró herramientas de desarrollo, contenerización y documentación:

| Herramienta             | Utilización                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| Python                  | Desarrollo y ejecución de componentes                                               |
| FastAPI                 | Implementación del servicio de predicción                                           |
| Streamlit               | Desarrollo de la interfaz                                                           |
| Docker y Docker Compose | Construcción y ejecución de contenedores                                            |
| PowerShell              | Validaciones y pruebas locales                                                      |
| GitHub                  | Repositorio previsto para el código y documentación                                 |
| IA generativa           | Apoyo en la estructuración de procedimientos, explicaciones y documentación técnica |

#### 7.2. Limitaciones

El despliegue en Microsoft Azure fue diseñado y documentado, pero no ejecutado.

Siendo así, no se cuenta con disponibilidad pública, conectividad real entre servicios de Azure, métricas de rendimiento en nube ni costos efectivos de operación.

Tampoco se realizaron pruebas de penetración, carga o resistencia sobre infraestructura remota.

#### 7.3. Conclusión

La estrategia desarrollada demuestra cómo una aplicación de detección de fraude basada en inteligencia artificial puede prepararse para migrar desde una ejecución local hacia una arquitectura contenerizada en Microsoft Azure.

La propuesta aprovecha las imágenes Docker existentes y mantiene la separación entre frontend, backend y modelo predictivo, reduciendo la necesidad de modificar el código de la aplicación.

Las pruebas locales respaldan la funcionalidad e integración de los componentes. Por su parte, el procedimiento documentado establece los recursos, configuraciones y verificaciones que serían necesarios para realizar un despliegue posterior.