"""Tests du module de chiffrement."""
import pytest


def test_encrypt_decrypt_roundtrip(crypto_ready):
    original = "MonMotDePasseWiFi!2026"
    encrypted = crypto_ready.encrypt(original)
    assert encrypted != original
    assert crypto_ready.decrypt(encrypted) == original


def test_encrypt_empty(crypto_ready):
    assert crypto_ready.encrypt("") == ""
    assert crypto_ready.decrypt("") == ""


def test_decrypt_legacy_plaintext(crypto_ready):
    """Les anciennes valeurs non chiffrées doivent passer sans erreur."""
    assert crypto_ready.decrypt("not_encrypted_legacy") == "not_encrypted_legacy"


def test_encrypt_deterministic_not(crypto_ready):
    """Fernet doit produire un résultat différent à chaque appel."""
    a = crypto_ready.encrypt("hello")
    b = crypto_ready.encrypt("hello")
    assert a != b


def test_wrong_password_fails(temp_dir):
    """Avec un mauvais mot de passe, decrypt renvoie le ciphertext brut."""
    import crypto
    crypto.init("good-password-111", temp_dir / "salt1.bin")
    encrypted = crypto.encrypt("secret")

    # Nouveau module avec mauvais mdp + même sel
    crypto.reset()
    crypto.init("wrong-password-222", temp_dir / "salt1.bin")
    # Doit retourner le ciphertext tel quel (legacy fallback)
    assert crypto.decrypt(encrypted) != "secret"