"""Fixtures pytest partagées."""
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ajoute la racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir():
    # ignore_cleanup_errors : sur Windows, les handles SQLite/log peuvent
    # être libérés après le début du cleanup → on ignore ces erreurs.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        yield Path(d)


@pytest.fixture
def crypto_ready(temp_dir):
    """Initialise le module crypto avec un mot de passe de test."""
    import crypto
    crypto.init("test-password-12345", temp_dir / "salt.bin")
    yield crypto
    crypto.reset()


@pytest.fixture
def app_client(temp_dir, crypto_ready):
    """Client Flask avec DB temporaire."""
    os.environ["WIFI_DB_PATH"] = str(temp_dir / "test.db")
    os.environ["WIFI_SALT_PATH"] = str(temp_dir / "salt.bin")
    os.environ["WIFI_LOG_PATH"] = str(temp_dir / "test.log")
    os.environ["WIFI_MASTER_PASSWORD"] = "test-password-12345"

    # Recharge les modules avec la nouvelle config
    import importlib
    import config
    importlib.reload(config)

    import app as app_module
    importlib.reload(app_module)

    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client