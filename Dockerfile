# Usa una imagen oficial de Python (slim) como base
FROM python:3.10-slim

# Instala dependencias del sistema: Chrome, Chromedriver, utilidades
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias Python primero (para aprovechar caché)
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente (src, archive, etc.)
COPY . .

# Expone el puerto que usa la aplicación Flask (5000)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "src/main.py"]
