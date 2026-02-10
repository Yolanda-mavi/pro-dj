#FROM python:3.13-bookworm

#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1

#WORKDIR /app

#COPY requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#segunda opcion
FROM python:3.13-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# UID/GID del usuario del host (yolanda-mv suele ser 1000)
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID appuser \
    && useradd -u $UID -g appuser -m appuser

# Dependencias como root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Permisos
RUN chown -R appuser:appuser /app

# Usuario no-root
USER appuser

# Código
COPY --chown=appuser:appuser . .
