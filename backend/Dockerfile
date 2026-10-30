#1. Imagen base con Python
FROM python:3.11-slim

#2. Directorio de trabajo dentro del contenedor
WORKDIR /app

#3. Evitar archivos temporales de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#4. Copiar archivo de dependencias
COPY backend/requirements.txt /app/requirements.txt

#5. Instalar bibliotecas necesarias
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

#6. Copiar código del backend
COPY backend/ /app/backend/

#7. Copiar modelo entrenado
COPY model/ /app/model/

#8. Documentar el puerto de la API
EXPOSE 8000

#9. Iniciar FastAPI
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
