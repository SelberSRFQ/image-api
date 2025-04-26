FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libtesseract-dev \
    libleptonica-dev \
    libgl1 \
    libglib2.0-0 \
    libjpeg62-turbo \
    && apt-get clean

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o app
COPY app2.py .

# Expor a porta
EXPOSE 10000

# Comando de inicialização
CMD gunicorn app2:app --bind 0.0.0.0:$PORT --workers 1 --threads 1 --access-logfile - --error-logfile -

