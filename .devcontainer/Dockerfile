# Base image com Python 3.11
FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências nativas do Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
      libdbus-1-3 libcups2 libxcomposite1 libxdamage1 \
      libxfixes3 libasound2 libgbm1 libpango-1.0-0 \
      libcairo2 libxkbcommon0 libatspi2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /workspace

# Copia arquivos de código
COPY . .

# Expõe porta padrão do Streamlit
EXPOSE 5000

# Comando padrão ao abrir o Codespace
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
