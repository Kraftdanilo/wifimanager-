# 📄 Version 1.2.1

## 🎉 Nouveautés

### 🔐 Sécurité

- Chiffrement AES (Fernet) des mots de passe
- Mot de passe maître (PBKDF2, 600k itérations)
- Rate limiting 60 req/min
- Mode lecture seule (`WIFI_READONLY=1`)

### 🧪 Tests

- 25 tests pytest
- CI GitHub Actions (Windows + Linux + macOS × Python 3.10-3.12)

### 🐳 Déploiement

- Support Docker + docker-compose
- Healthcheck `/api/health`

### 📊 Améliorations

- Logs rotatifs (10 Mo max)
- Configuration centralisée (env vars)
- README professionnel

## 📦 Installation

```bash
git clone https://github.com/Kraftdanilo/wifimanager-.git
cd wifimanager-
pip install -r requirements.txt
python app.py
```
