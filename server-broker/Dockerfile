# Use a imagem oficial do Python
FROM python:3.12-bullseye

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

COPY . ./app
# Defina o diretório de trabalho
WORKDIR /app

# Exponha as portas TCP, UDP e HTTP


# Comando para iniciar o aplicativo
CMD ["python", "server.py"]
