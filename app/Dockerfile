# Imagen base con Python
FROM python:3.9.6

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY requirements.txt .
COPY encrypt_yml.py .
COPY credential.yml .
COPY supabase_connection.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Variable de entorno
#ENV AES_SECRET_KEY="AES_SEMATIC_PROJECT_SECRET_KEY_A"

# Ejecutar el script al iniciar el contenedor
CMD ["python", "supabase_connection.py"]
