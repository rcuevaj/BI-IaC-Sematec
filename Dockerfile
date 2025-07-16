# Usa imagen base de Python
FROM python:3.9.6

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias y código fuente
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código ETL
COPY app/ .

# Comando que se ejecuta por defecto al iniciar el contenedor
CMD ["python", "ETL_migration_script.py"]
