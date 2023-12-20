FROM python:3.11.5

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY ../requirements.txt .

ENV DEBUG 0

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código-fonte da aplicação para o contêiner
COPY . .

# Execute as migrações do Django
WORKDIR /app/distro
RUN python manage.py migrate

# Exponha a porta em que o Gunicorn estará em execução
EXPOSE 8000
