# Usa la imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Establece variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia toda la aplicación al contenedor
COPY . .

# Expone el puerto en el que corre la aplicación
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=todo_app/run.py \
    FLASK_ENV=production

# Comando para ejecutar la aplicación
CMD ["python", "todo_app/run.py"]
