"""Logs rotatifs — 5 fichiers de 2 Mo, 7 jours d'historique."""
import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path


def setup_logging(log_path: Path, level: str = "INFO") -> logging.Logger:
    """Configure le logger racine pour toute l'application."""
    logger = logging.getLogger("wifi_manager")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-7s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Fichier rotatif (2 Mo × 5 backups = 10 Mo max)
    try:
        fh = RotatingFileHandler(
            log_path, maxBytes=2 * 1024 * 1024,
            backupCount=5, encoding="utf-8",
        )
        fh.setFormatter(fmt)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
    except Exception as e:
        print(f"⚠  Impossible d'écrire les logs : {e}")

    # Console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.addHandler(ch)

    # Réduit le bruit de Flask/Werkzeug
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    return logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"wifi_manager.{name}")