"""Mise à jour automatique de Wifi Manager depuis GitHub.

Wifi Manager v1.2.0 — © 2026 Dane (manifest @2026)

Stratégie :
  • Interroge l'API GitHub pour la dernière release / version du dépôt
  • Compare avec la version locale (Config.APP_VERSION)
  • `git pull` si le dépôt est un clone git, sinon télécharge l'archive ZIP
    et remplace les fichiers applicatifs (DB, sel, logs, venv préservés)
  • Réinstalle les dépendances si requirements.txt a changé
"""
import io
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import config

GITHUB_API = "https://api.github.com/repos/Kraftdanilo/wifimanager-/commits/main"
RAW_MANIFEST = (
    "https://raw.githubusercontent.com/Kraftdanilo/wifimanager-/main/manifest.json"
)

# Fichiers/répertoires préservés lors d'une mise à jour par archive
PRESERVE = {".venv", "venv", "__pycache__", ".git", "data",
            "wifi_data.db", "wifi_salt.bin", "wifi_manager.log",
            ".env", "node_modules"}

# Fichiers applicatifs mis à jour
APP_FILES = ["app.py", "config.py", "crypto.py", "logging_config.py",
             "rate_limit.py", "update.py", "wifi_backend.py",
             "requirements.txt", "pytest.ini"]


def _fetch(url: str, timeout: int = 10) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "wifi-manager"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _parse_version(v: str) -> tuple:
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split("."))
    except Exception:
        return (0, 0, 0)


def check_latest() -> dict:
    """
    Vérifie la version distante.
    Ordre : manifest.json (raw) → dernier commit (date fallback).
    """
    local = config.Config.APP_VERSION

    # 1. manifest.json versionné dans le dépôt
    try:
        data = json.loads(_fetch(RAW_MANIFEST).decode("utf-8"))
        remote = str(data.get("version", "")).strip()
        if remote:
            return {
                "local_version": local,
                "remote_version": remote,
                "update_available": _parse_version(remote) > _parse_version(local),
                "notes": data.get("notes", ""),
                "source": "manifest",
            }
    except Exception:
        pass

    # 2. Fallback : date du dernier commit (gère le dépôt vide → HTTP 409)
    try:
        data = json.loads(_fetch(GITHUB_API).decode("utf-8"))
        sha = data.get("sha", "")[:8]
        date = data.get("commit", {}).get("committer", {}).get("date", "")
        return {
            "local_version": local,
            "remote_version": f"commit {sha}",
            "remote_date": date,
            "update_available": bool(date) and (
                date > getattr(config.Config, "_LAST_CHECK_DATE", "")),
            "source": "commit",
        }
    except Exception as e:
        msg = str(e)
        if "409" in msg:
            msg = "dépôt distant vide (aucun commit sur la branche main)"
        return {"error": msg, "update_available": False}


def _is_git_repo(root: Path) -> bool:
    return (root / ".git").exists()


def _git_available() -> bool:
    return shutil.which("git") is not None


def apply_update(root: Path | None = None) -> dict:
    """
    Applique la mise à jour :
      • git pull si clone git, sinon téléchargement de l'archive ZIP
    Retourne un rapport.
    """
    root = Path(root or Path(__file__).parent).resolve()
    report = {"ok": False, "method": "", "message": ""}

    latest = check_latest()
    if latest.get("error"):
        report["message"] = f"Impossible de vérifier : {latest['error']}"
        return report
    if not latest.get("update_available"):
        report["method"] = "none"
        report["message"] = (
            f"À jour (v{config.Config.APP_VERSION}). "
            f"Distant : {latest.get('remote_version')}")
        report["ok"] = True
        return report

    # --- Méthode git
    if _is_git_repo(root) and _git_available():
        try:
            r = subprocess.run(
                ["git", "pull", "--ff-only", "origin", "main"],
                cwd=root, capture_output=True, timeout=120,
            )
            out = (r.stdout + r.stderr).decode("utf-8", errors="replace")
            if r.returncode == 0:
                report.update(ok=True, method="git", message=out.strip())
            else:
                report.update(
                    method="git",
                    message=f"git pull a échoué : {out.strip()}")
                return report
        except Exception as e:
            report["message"] = f"git pull : {e}"
            return report

    # --- Méthode archive ZIP
    else:
        try:
            zip_url = config.Config.REPO_URL + "/archive/refs/heads/main.zip"
            blob = _fetch(zip_url, timeout=60)
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                names = z.namelist()
                prefix = names[0].split("/")[0] + "/"

                for member in names:
                    rel = member[len(prefix):]
                    if not rel or member.endswith("/"):
                        continue
                    # Ignore le venv, git, données et fichiers hors liste
                    if rel.split("/")[0] in PRESERVE:
                        continue
                    if len(rel.split("/")) > 1 and rel.split("/")[0] not in (
                            "templates", "static", "tests", ".github"):
                        continue
                    if not rel.endswith((".py", ".txt", ".ini", ".html",
                                         ".css", ".js", ".yml", ".md")):
                        continue

                    target = root / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(member) as src, \
                            open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)

            report.update(ok=True, method="archive",
                          message="Fichiers remplacés depuis l'archive ZIP")
        except Exception as e:
            report["message"] = f"Téléchargement : {e}"
            return report

    # --- Dépendances si requirements.txt présent
    req = root / "requirements.txt"
    if req.exists():
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r",
                 str(req), "--quiet"],
                cwd=root, capture_output=True, timeout=600,
            )
            report["deps"] = "pip install exécuté"
        except Exception as e:
            report["deps"] = f"pip install a échoué : {e}"

    report["restarted"] = False
    report["message"] += (
        " — redémarrez l'application pour appliquer la nouvelle version.")
    return report


# ==================================================================
#                        CLI
# ==================================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mise à jour Wifi Manager")
    parser.add_argument("--check", action="store_true",
                        help="Vérifie seulement la présence d'une mise à jour")
    parser.add_argument("--apply", action="store_true",
                        help="Applique la mise à jour")
    args = parser.parse_args()

    print("=" * 60)
    print(f"  WIFI MANAGER v{config.Config.APP_VERSION} — mise à jour")
    print(f"  {config.Config.APP_COPYRIGHT}")
    print("=" * 60)

    if args.check or not args.apply:
        info = check_latest()
        print(f"  Version locale  : {info.get('local_version', '?')}")
        print(f"  Version distante: {info.get('remote_version', '?')}")
        print(f"  Mise à jour dispo : "
              f"{'OUI ✅' if info.get('update_available') else 'non'}")
        if info.get("notes"):
            print(f"  Notes : {info['notes']}")

    if args.apply:
        print()
        print("  Application de la mise à jour...")
        result = apply_update()
        print(f"  Méthode : {result.get('method')}")
        print(f"  {result.get('message')}")
        if result.get("deps"):
            print(f"  Dépendances : {result['deps']}")
        if result.get("ok"):
            print("\n  → Redémarrez l'application.")
    sys.exit(0)
