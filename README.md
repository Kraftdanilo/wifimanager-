# 📡 Wifi Manager

Application web locale pour gérer, analyser et partager vos réseaux Wi-Fi.

**Version 1.2.0** — © 2026 **Dane** — manifest @2026

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.2.0-orange.svg)
[![Tests](https://github.com/Kraftdanilo/wifimanager-/actions/workflows/test.yml/badge.svg)](https://github.com/Kraftdanilo/wifimanager-/actions/workflows/test.yml)

## ✨ Fonctionnalités

- 📡 **Scan** des réseaux à portée (2.4 / 5 / 6 GHz)
- 🔑 **Mots de passe** des réseaux déjà enregistrés
- 🔐 **Chiffrement AES** des données sensibles
- 📱 **QR codes** de partage Wi-Fi instantané
- 🌐 **Serveur web local** — consultation depuis téléphone
- 🔔 **Détection des changements** de mot de passe
- 📊 **Dashboard** statistique + export PDF
- 🗺 **Carte des canaux** 2.4 / 5 / 6 GHz
- 🌍 **Interface FR / EN**
- 🌙 **Thème clair / sombre automatique**
- 🔄 **Mise à jour automatique** depuis GitHub
- 🐳 **Support Docker**

## 🖥️ Prérequis

- Python 3.10+
- Windows 10/11, Linux ou macOS
- Carte Wi-Fi active

## 🚀 Installation

### Méthode classique

```bash
git clone https://github.com/Kraftdanilo/wifimanager-.git
cd wifimanager-

python -m venv .venv
# Windows : .venv\Scripts\activate
# Linux/macOS : source .venv/bin/activate

pip install -r requirements.txt
python app.py

## 🔄 Mise à jour automatique

### Depuis l'API

- `GET /api/update/check` → vérifie si une nouvelle version est disponible
- `POST /api/update/apply` → applique la mise à jour (désactivé en mode lecture seule)

### En ligne de commande

```bash
python update.py --check   # vérifier seulement
python update.py --apply   # appliquer la mise à jour
```

Comment ça marche :

1. Lit la version distante dans `manifest.json` sur GitHub (fallback : dernier commit)
2. Compare avec la version locale (`1.2.0`)
3. Fait `git pull` si le dépôt est un clone, sinon télécharge l'archive ZIP
   et remplace uniquement les fichiers applicatifs
4. **Préserve** : `.venv`, `.git`, `data/`, `wifi_data.db`, `wifi_salt.bin`,
   `wifi_manager.log`, `.env`
5. Réinstalle les dépendances si `requirements.txt` a changé
6. Demande un redémarrage de l'application pour appliquer la nouvelle version
