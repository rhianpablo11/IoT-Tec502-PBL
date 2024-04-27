# Use a imagem oficial do Python
FROM python:3.12-bullseye

COPY . ./app
# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o código-fonte para o diretório de trabalho


# Exponha as portas TCP, UDP e HTTP
EXPOSE 8080
EXPOSE 8081/udp
EXPOSE 8082

# Comando para iniciar o aplicativo
CMD ["python", "server.py"]
