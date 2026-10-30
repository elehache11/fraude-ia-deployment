#1. Imagen base
FROM python:3.11-slim

#2. Directorio de trabajo
WORKDIR /app

#3. Configuración de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#4. Copiar dependencias
COPY frontend/requirements.txt /app/requirements.txt

#5. Instalar dependencias
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

#6. Copiar código de Streamlit
COPY frontend/ /app/frontend/

#7. Documentar puerto de Streamlit
EXPOSE 8501

#8. Ejecutar aplicación
CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
