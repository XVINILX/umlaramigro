# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar dependências de build
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar tudo que é necessário para instalar o pacote
COPY pyproject.toml README.md ./
COPY app ./app 

# Instalar o pacote
RUN pip install --no-cache-dir --user .

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar pacote instalado do builder
COPY --from=builder /root/.local /root/.local

# Copiar o resto dos arquivos
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY run.py .
COPY .env* ./

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "run.py"]