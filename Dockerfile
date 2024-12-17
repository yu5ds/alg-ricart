# Usar una imagen base con Python 3.10
FROM python:3.10

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Ejecutar la aplicación
CMD ["python", "app.py"]
