"""Chiffrement AES (Fernet) des données sensibles — mots de passe Wi-Fi.

Stratégie :
  • Clé dérivée du mot de passe maître + sel (PBKDF2, 600k itérations)
  • Chaque champ sensible chiffré individuellement
  • Le sel est stocké sur disque (wifi_salt.bin)
  • Le mot de passe maître n'est JAMAIS stocké
"""
import base64
import getpass
import os
import sys
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


_fernet: Fernet | None = None
_master_pwd: str = ""

# Console Windows (cp1252) : tolérer les symboles Unicode (⚠, ✅, …)
for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        _stream.reconfigure(errors="replace")


# ==================================================================
#                        CLÉ & SEL
# ==================================================================
def _load_salt(salt_path: Path) -> bytes:
    """Charge le sel ou en crée un nouveau (16 bytes)."""
    if salt_path.exists():
        return salt_path.read_bytes()
    salt = os.urandom(16)
    salt_path.write_bytes(salt)
    try:
        os.chmod(salt_path, 0o600)
    except Exception:
        pass
    return salt


def _derive_key(password: str, salt: bytes) -> bytes:
    """PBKDF2-HMAC-SHA256 → 32 bytes base64 (Fernet key)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


# ==================================================================
#                        INIT
# ==================================================================
def init(master_password: str, salt_path: Path) -> None:
    """Initialise le module avec un mot de passe maître."""
    global _fernet, _master_pwd
    _master_pwd = master_password
    salt = _load_salt(salt_path)
    key = _derive_key(master_password, salt)
    _fernet = Fernet(key)


def is_ready() -> bool:
    return _fernet is not None


def reset() -> None:
    global _fernet, _master_pwd
    _fernet = None
    _master_pwd = ""


# ==================================================================
#                        ENCRYPT / DECRYPT
# ==================================================================
def encrypt(plaintext: str) -> str:
    """Chiffre une chaîne. Retourne un token base64 ou la chaîne vide."""
    if not plaintext:
        return ""
    if not _fernet:
        # Mode non chiffré (warning déjà loggé au démarrage)
        return plaintext
    token = _fernet.encrypt(plaintext.encode("utf-8"))
    return token.decode("ascii")


def decrypt(ciphertext: str) -> str:
    """Déchiffre un token. Tolère les chaînes non chiffrées (legacy)."""
    if not ciphertext:
        return ""
    if not _fernet:
        return ciphertext
    try:
        return _fernet.decrypt(ciphertext.encode("ascii")).decode("utf-8")
    except (InvalidToken, Exception):
        # Valeur legacy en clair → retourne tel quel
        return ciphertext


# ==================================================================
#                   PROMPT INTERACTIF
# ==================================================================
def prompt_password(confirm: bool = False) -> str:
    """Demande le mot de passe maître à l'utilisateur."""
    while True:
        try:
            pwd = getpass.getpass("🔐 Mot de passe maître : ")
        except (KeyboardInterrupt, EOFError):
            print("\nAnnulé.")
            sys.exit(1)
        if not pwd:
            print("  ⚠  Le mot de passe ne peut pas être vide.")
            continue
        if len(pwd) < 8:
            print("  ⚠  Minimum 8 caractères.")
            continue
        if confirm:
            try:
                pwd2 = getpass.getpass("🔐 Confirmer              : ")
            except (KeyboardInterrupt, EOFError):
                print("\nAnnulé.")
                sys.exit(1)
            if pwd != pwd2:
                print("  ⚠  Les mots de passe ne correspondent pas.")
                continue
        return pwd


def setup_from_env_or_prompt(salt_path: Path) -> bool:
    """
    Initialise le chiffrement :
      1. Depuis la variable d'env WIFI_MASTER_PASSWORD si définie
      2. Sinon, demande interactivement
      3. Sinon (mode non-interactif), désactive le chiffrement
    """
    from config import Config

    pwd = Config.MASTER_PASSWORD.strip()

    if pwd:
        init(pwd, salt_path)
        return True

    # Mode interactif ?
    if sys.stdin.isatty() and not Config.DEBUG:
        first_time = not Config.DB_PATH.exists()
        if first_time:
            print()
            print("=" * 60)
            print("  🔐  PREMIÈRE UTILISATION")
            print("=" * 60)
            print("  Choisissez un mot de passe maître pour chiffrer")
            print("  les mots de passe Wi-Fi stockés localement.")
            print("  ⚠  Si vous le perdez, les données seront illisibles.")
            print("=" * 60)
        pwd = prompt_password(confirm=first_time)
        init(pwd, salt_path)
        return True

    # Non-interactif sans mot de passe → mode non chiffré
    print("⚠  Mode NON CHIFFRÉ (WIFI_MASTER_PASSWORD non définie)")
    return False