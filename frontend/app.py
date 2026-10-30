import os
import requests

import streamlit as st

#1. CONFIGURACIÓN GENERAL
st.set_page_config(
    page_title = "Detección de Fraude con IA",
    page_icon = "🔍",
    layout = "centered"
)

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

#2. ENCABEZADO
st.title("Sistema de Detección de Fraude")

st.write(
    "Aplicación de inteligencia artificial para evaluar "
    "transacciones financieras mediante un modelo Random Forest."
)

st.info(
    "Modelo desarrollado en la Actividad 6. "
    "Umbral de clasificación: 0.17."
)

st.divider()

#3. FORMULARIO DE TRANSACCIÓN
st.subheader("Datos de la transacción")

st.write(
    "Introduce las características de la transacción "
    "que deseas evaluar."
)

with st.form("formulario_transaccion"):

    time = st.number_input(
        "Tiempo de la transacción (Time)",
        min_value = 0.0,
        value = 0.0
    )

    amount = st.number_input(
        "Importe de la transacción (Amount)",
        min_value = 0.0,
        value = 100.0
    )

    st.write("Variables anonimizadas (V1–V28)")

    with st.expander("Mostrar variables V1–V28"):

        variables = {}

        for i in range(1, 29):

            variables[f"V{i}"] = st.number_input(
                f"V{i}",
                value = 0.0,
                format = "%.6f"
            )

    enviar = st.form_submit_button(
        "Evaluar transacción",
        type = "primary"
    )

#4. COMUNICACIÓN CON FASTAPI
if enviar:

    datos = {
        "Time": time,
        "Amount": amount
    }

    datos.update(variables)

    solicitud = {
        "features": datos
    }

    try:

        respuesta = requests.post(
            f"{API_URL}/predict",
            json = solicitud,
            timeout = 30
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

        #5. PRESENTACIÓN DEL RESULTADO
        st.divider()

        st.subheader("Resultado de la evaluación")

        probabilidad = resultado["probabilidad_fraude"]

        clasificacion = resultado["clasificacion"]

        umbral = resultado["umbral"]

        st.metric(
            "Probabilidad estimada de fraude",
            f"{probabilidad * 100:.2f}%"
        )

        st.write(
            f"Umbral de clasificación: {umbral:.2f}"
        )

        if clasificacion == 1:

            st.error(
                "Transacción clasificada como potencialmente fraudulenta."
            )

        else:

            st.success(
                "Transacción clasificada como legítima."
            )

        st.caption(
            "El resultado corresponde a una estimación del modelo "
            "y no constituye una confirmación de fraude."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "No fue posible conectar con FastAPI. "
            "Verifica que el backend esté ejecutándose."
        )

    except requests.exceptions.Timeout:

        st.error(
            "La solicitud excedió el tiempo máximo de espera."
        )

    except requests.exceptions.HTTPError as error:

        st.error(
            f"El servidor rechazó la solicitud: {error}"
        )

    except (ValueError, KeyError, TypeError):

        st.error(
            "El servidor devolvió una respuesta con formato inesperado."
        )
