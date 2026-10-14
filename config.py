"""Configuration centralisée — variables d'environnement + valeurs par défaut.

Wifi Manager v1.2.0 — © 2026 Dane (manifest @2026)
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


def _bool(key: str, default: bool = False) -> bool:
    v = os.environ.get(key, "").lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    return default


class Config:
    # --- Identité
    APP_NAME = "Wifi Manager"
    APP_VERSION = "1.2.0"
    APP_AUTHOR = "Dane"
    APP_COPYRIGHT = "© 2026 Dane — manifest @2026"
    REPO_URL = "https://github.com/Kraftdanilo/wifimanager-"

    # --- Serveur
    HOST = os.environ.get("WIFI_HOST", "0.0.0.0")
    PORT = int(os.environ.get("WIFI_PORT", "5000"))
    DEBUG = _bool("WIFI_DEBUG", False)

    # --- Chemins
    BASE_DIR = BASE_DIR
    DB_PATH = Path(os.environ.get("WIFI_DB_PATH",
                                  str(BASE_DIR / "wifi_data.db")))
    SALT_PATH = Path(os.environ.get("WIFI_SALT_PATH",
                                    str(BASE_DIR / "wifi_salt.bin")))
    LOG_PATH = Path(os.environ.get("WIFI_LOG_PATH",
                                   str(BASE_DIR / "wifi_manager.log")))

    # --- Sécurité
    # Si non définie, on demande interactivement au démarrage
    MASTER_PASSWORD = os.environ.get("WIFI_MASTER_PASSWORD", "")
    # Mode lecture seule : désactive connect/disconnect
    READONLY = _bool("WIFI_READONLY", False)
    # Rate limiting : max requêtes par minute sur endpoints sensibles
    RATE_LIMIT_PER_MIN = int(os.environ.get("WIFI_RATE_LIMIT", "60"))

    # --- Fonctionnalités
    ENABLE_PDF = _bool("WIFI_ENABLE_PDF", True)
    ENABLE_QR = _bool("WIFI_ENABLE_QR", True)
    LOG_LEVEL = os.environ.get("WIFI_LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        """Vérifie la cohérence de la config."""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.SALT_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        return cls