FROM python:3.12-slim

LABEL maintainer="Wifi Manager"
LABEL description="Gestionnaire Wi-Fi local avec interface web"

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    network-manager \
    && rm -rf /var/lib/apt/lists/*

# Python deps (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

# Utilisateur non-root
RUN useradd -m -u 1000 wifi && chown -R wifi:wifi /app
USER wifi

# Volume pour la DB et les logs
VOLUME ["/app/data"]
ENV WIFI_DB_PATH=/app/data/wifi_data.db \
    WIFI_SALT_PATH=/app/data/wifi_salt.bin \
    WIFI_LOG_PATH=/app/data/wifi_manager.log \
    WIFI_HOST=0.0.0.0 \
    WIFI_PORT=5000

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

CMD ["python", "app.py"]
