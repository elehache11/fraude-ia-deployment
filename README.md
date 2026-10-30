# Sistema de detección de fraude con inteligencia artificial

## 1. Descripción del proyecto

Aplicación para identificar posibles transacciones fraudulentas mediante un modelo de inteligencia artificial Random Forest.

El proyecto reutiliza el modelo desarrollado durante la Actividad 6 y lo integra en una aplicación web con frontend Streamlit, backend FastAPI y contenedores Docker.

La solución recibe 30 variables de entrada, calcula una probabilidad estimada de fraude y clasifica la transacción utilizando un umbral de decisión de 0.17.

## 2. Arquitectura

La aplicación utiliza tres componentes principales:

| Componente | Tecnología    | Función                                                   |
| ---------- | ------------- | --------------------------------------------------------- |
| Frontend   | Streamlit     | Captura de datos y visualización de resultados            |
| Backend    | FastAPI       | Validación de solicitudes y procesamiento de predicciones |
| Modelo     | Random Forest | Estimación de probabilidad de fraude                      |

Los componentes se ejecutan mediante Docker Compose, utilizando dos contenedores independientes:

* `fraude-frontend:1.0`: interfaz Streamlit, puerto 8501.
* `fraude-backend:1.0`: API FastAPI, puerto 8000.

El frontend se comunica con el backend mediante solicitudes HTTP. Dentro de Docker Compose utiliza la dirección `http://backend:8000`.

El modelo se encuentra almacenado en `model/modelo_final_Random_Forest.joblib`. El umbral de clasificación se obtiene de `model/umbrales_seleccionados.csv`.

## 3. Tecnologías utilizadas

* Python 3.11
* scikit-learn 1.9.0
* FastAPI
* Streamlit
* Docker y Docker Compose
* pytest y httpx
* PowerShell
* Microsoft Azure Container Apps (estrategia de despliegue documentada)

## 4. Estructura del repositorio

```text
fraude-ia-deployment/
│
├── backend/
│   ├── main.py
│   ├── predictor.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── model/
│   ├── modelo_final_Random_Forest.joblib
│   └── umbrales_seleccionados.csv
│
├── tests/
│
├── docs/
│   ├── validacion_pruebas.md
│   ├── manual_despliegue.md
│   └── evidencias/
│
├── docker-compose.yml
├── requirements-local.txt
├── .gitignore
└── README.md
```

## 5. Instalación y ejecución

### Requisitos

Para ejecutar la aplicación mediante contenedores se requiere:

* Docker Desktop con soporte para contenedores Linux.
* Docker Compose.
* Imágenes Docker construidas localmente o acceso a un registro que las contenga.

### Construcción de imágenes

Desde PowerShell, situarse en la carpeta raíz del proyecto.

Construir el backend:

```powershell
docker build -t fraude-backend:1.0 -f backend/Dockerfile .
```

Construir el frontend:

```powershell
docker build -t fraude-frontend:1.0 -f frontend/Dockerfile .
```

### Iniciar la aplicación

Ejecutar:

```powershell
docker compose up -d
```

Comprobar los servicios:

```powershell
docker compose ps
```

Acceder a la interfaz:

`http://127.0.0.1:8501`

Consultar la documentación interactiva de FastAPI:

`http://127.0.0.1:8000/docs`

Verificar la disponibilidad del backend:

`http://127.0.0.1:8000/health`

### Detener los servicios

```powershell
docker compose stop
```

### Reactivar los servicios

```powershell
docker compose start
```

## 6. Contrato de la API

El backend expone tres endpoints:

| Endpoint      | Método | Función                          |
| ------------- | ------ | -------------------------------- |
| `/health`     | GET    | Consultar disponibilidad         |
| `/model-info` | GET    | Consultar información del modelo |
| `/predict`    | POST   | Generar predicciones             |

El endpoint `/predict` recibe un objeto JSON denominado `features`, que contiene las siguientes variables:

* `Time`
* `Amount`
* `V1` a `V28`

Las 30 variables deben contener valores numéricos finitos. Los valores de `Time` y `Amount` deben ser mayores o iguales a cero.

La respuesta incluye:

* `probabilidad_fraude`: probabilidad estimada por el modelo.
* `clasificacion`: 0 para transacción legítima y 1 para posible fraude.
* `resultado`: descripción de la clasificación.
* `umbral`: valor de decisión utilizado, actualmente 0.17.

Las variables `V1` a `V28` provienen de una transformación PCA y no corresponden directamente a atributos bancarios convencionales.

## 7. Pruebas y validación

La solución fue evaluada mediante pruebas funcionales, casos extremos y comprobaciones de consistencia.

Entre las validaciones realizadas se encuentran:

* Disponibilidad del backend.
* Generación de predicciones mediante API.
* Integración entre Streamlit y FastAPI.
* Ejecución de ambos componentes mediante Docker.
* Rechazo de solicitudes inválidas.
* Procesamiento técnico de valores extremos.
* Consistencia entre ejecuciones consecutivas.
* Consistencia entre Windows y Docker.
* Detención y recuperación de contenedores.

Las ocho pruebas adicionales ejecutadas obtuvieron resultados satisfactorios conforme a los criterios establecidos.

Para ejecutar las pruebas automatizadas desde el entorno local, instalar las dependencias correspondientes y utilizar:

```powershell
python -m pytest -v
```

Las pruebas automatizadas previamente ejecutadas finalizaron con dos pruebas aprobadas.

## 8. Estrategia de despliegue en la nube

Se diseñó una estrategia de despliegue en Microsoft Azure mediante Azure Container Apps.

La arquitectura propuesta contempla:

* Un frontend Streamlit accesible mediante HTTPS.
* Un backend FastAPI con acceso interno.
* Azure Container Registry para almacenar las imágenes.
* Comunicación entre servicios dentro del mismo entorno de Azure Container Apps.
* Controles de seguridad, monitoreo y recuperación.

## 9. Documentación adicional

Los siguientes documentos complementan la implementación:

* [Documento de validación y pruebas](docs/validacion_pruebas.md)
* [Manual y estrategia de despliegue en la nube](docs/manual_despliegue.md)

Las capturas de las pruebas se organizan en la carpeta `docs/evidencias/`.
