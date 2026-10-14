"""Backend Wi-Fi cross-platform — version universelle corrigée.

Corrections incluses :
  • Décodage robuste (UTF-8 / CP850 / CP1252 / CP437 / latin-1)
  • Parser universel des profils (FR / EN / ES / DE / IT / ...)
  • Nettoyage espaces insécables et BOM
  • Fallback scan multi-stratégies
  • Détection localisation Windows via registre
  • Fallback "au moins la connexion active"
"""
import os
import re
import platform
import subprocess
import shutil
from dataclasses import dataclass


# ==================================================================
#                            MODÈLES
# ==================================================================
@dataclass
class WifiNetwork:
    ssid: str
    signal: int
    security: str = ""
    channel: str = ""
    bssid: str = ""
    band: str = ""
    connected: bool = False


@dataclass
class ScanResult:
    networks: list
    error: str = ""
    raw_output: str = ""
    adapter_ok: bool = True
    needs_location: bool = False
    connected_ssid: str = ""


# ==================================================================
#                   BANDE DEPUIS CANAL
# ==================================================================
def channel_to_band(channel) -> str:
    if channel is None or channel == "":
        return ""
    try:
        ch = int(str(channel).strip())
    except (ValueError, TypeError):
        return ""
    if 1 <= ch <= 14:
        return "2.4 GHz"
    if 32 <= ch <= 177:
        return "5 GHz"
    if 181 <= ch <= 233:
        return "6 GHz"
    return ""


def _cflags():
    return subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0


# ==================================================================
#              DÉCODAGE ROBUSTE + NETTOYAGE
# ==================================================================
def _decode(raw: bytes) -> str:
    """Teste plusieurs encodages Windows jusqu'à trouver le bon."""
    if not raw:
        return ""
    for enc in ("utf-8", "cp850", "cp1252", "cp437", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _clean_netsh_line(line: str) -> str:
    """Supprime le BOM ; remplace NBSP / narrow NBSP / figure space par espace."""
    line = line.lstrip("\ufeff")
    for ch in ("\u00a0", "\u202f", "\u2007"):
        line = line.replace(ch, " ")
    return line.replace("\t", "    ")


def _run(cmd: list, timeout: int = 15) -> tuple:
    """Exécute une commande, retourne (code, stdout, stderr) bien décodés."""
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            creationflags=_cflags(),
        )
        return r.returncode, _decode(r.stdout), _decode(r.stderr)
    except FileNotFoundError:
        return -1, "", "Commande introuvable : " + cmd[0]
    except subprocess.TimeoutExpired:
        return -2, "", "Timeout (>%ds)" % timeout
    except Exception as e:
        return -3, "", str(e)


# ==================================================================
#              LOCALISATION WINDOWS (registre)
# ==================================================================
def _check_location_services() -> str:
    """Retourne 'Allow', 'Deny' ou 'Unknown'."""
    if platform.system() != "Windows":
        return "Unknown"
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion"
            r"\CapabilityAccessManager\ConsentStore\location",
        )
        val, _ = winreg.QueryValueEx(key, "Value")
        winreg.CloseKey(key)
        return val
    except Exception:
        return "Unknown"


# ==================================================================
#                      DIAGNOSTIC
# ==================================================================
def diagnostics() -> dict:
    s = platform.system()
    info = {
        "os": s,
        "netsh": bool(shutil.which("netsh")) if s == "Windows" else None,
        "nmcli": bool(shutil.which("nmcli")) if s == "Linux" else None,
        "airport": False,
        "adapter_active": False,
        "location_service": None,
        "sample_output": "",
        "error": "",
        "networks_visible": 0,
    }

    if s == "Windows":
        loc = _check_location_services()
        info["location_service"] = (loc == "Allow")

        code, out, err = _run(["netsh", "wlan", "show", "interfaces"])
        if code == 0 and re.search(r"(?im)^\s*(Name|Nom)\s*:", out):
            info["adapter_active"] = True
        info["sample_output"] = out[:800]

        code2, out2, err2 = _run(["netsh", "wlan", "show", "networks"])
        if code2 == 0:
            n = len(re.findall(r"^SSID \d+ :", out2, re.MULTILINE))
            info["networks_visible"] = n
            if n == 0 and not info["adapter_active"]:
                info["error"] = "Aucune carte Wi-Fi active."
            elif n == 0 and info["location_service"] is False:
                info["error"] = (
                    "Windows refuse de lister les réseaux car la "
                    "LOCALISATION est désactivée.\n\n"
                    "Fix : Paramètres → Confidentialité → Localisation."
                )
            elif n == 0:
                info["error"] = (
                    "netsh renvoie 0 réseau malgré un adaptateur actif.\n"
                    "Cause possible : pilote Intel ancien + Windows 11.\n\n"
                    "→ Mets à jour le pilote Wi-Fi Intel.\n"
                    "→ Ou utilise l'onglet SAVED (profils enregistrés)."
                )

    elif s == "Linux":
        code, out, err = _run(
            ["nmcli", "-t", "-f", "DEVICE,TYPE,STATE", "device", "status"])
        if code == 0 and "wifi" in out.lower():
            info["adapter_active"] = True
        info["sample_output"] = out[:800]

    elif s == "Darwin":
        path = ("/System/Library/PrivateFrameworks/Apple80211.framework/"
                "Versions/Current/Resources/airport")
        info["airport"] = os.path.exists(path)

    return info


# ==================================================================
#              PARSER UNIVERSEL — toutes langues
# ==================================================================
def _parse_profiles_windows(out: str) -> list:
    """
    Parser universel pour 'netsh wlan show profiles'.
    Garde uniquement les lignes INDENTÉES contenant ':' avec valeur.
    """
    profiles = []

    forbidden_in_key = (
        "interface", "interfaz", "schnittstelle",
        "groupe", "group", "grupo", "gruppe", "gruppo", "grupp",
        "gpo", "policy", "politique", "política", "politik",
    )

    placeholders = (
        "<aucun>", "<none>", "<ninguno>", "<keine>",
        "<nessuno>", "<nenhum>", "<geen>", "<нет>", "<无>", "<なし>",
        "aucun", "none",
    )

    for raw in out.splitlines():
        line = _clean_netsh_line(raw)

        if not line.strip():
            continue
        if not line[:1].isspace():
            continue
        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        if not value:
            continue
        if value.lower() in placeholders:
            continue
        if not key:
            continue

        key_l = key.lower()
        if any(fw in key_l for fw in forbidden_in_key):
            continue

        profiles.append(value)

    seen, result = set(), []
    for p in profiles:
        if p and p not in seen:
            seen.add(p)
            result.append(p)
    return result


def profiles_raw() -> str:
    """Sortie brute de 'netsh wlan show profiles' (debug)."""
    s = platform.system()
    if s == "Windows":
        code, out, err = _run(["netsh", "wlan", "show", "profiles"])
        return out if code == 0 else ("ERREUR : " + (err or str(code)))
    if s == "Linux":
        code, out, err = _run(
            ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"])
        return out if code == 0 else ("ERREUR : " + (err or str(code)))
    return "(non disponible)"


def list_saved_profiles():
    """Retourne la liste des SSID enregistrés (universel)."""
    s = platform.system()
    out_list = []

    if s == "Windows":
        code, out, err = _run(["netsh", "wlan", "show", "profiles"])
        if code == 0:
            out_list = _parse_profiles_windows(out)

        if not out_list:
            for iface in (
                "Wi-Fi", "WiFi", "WiFi 2", "WiFi 3",
                "Wireless Network Connection",
                "Connexion réseau sans fil",
                "WLAN", "wlan0", "wlan1",
            ):
                code, out, err = _run(
                    ["netsh", "wlan", "show", "profiles",
                     "interface=" + iface])
                if code == 0:
                    parsed = _parse_profiles_windows(out)
                    if parsed:
                        out_list = parsed
                        break

        if not out_list:
            code, out, err = _run(["netsh", "wlan", "show", "interfaces"])
            if code == 0:
                for line in out.splitlines():
                    s_line = _clean_netsh_line(line).strip()
                    m = re.match(r"^SSID\s*:\s*(.+)$", s_line)
                    if m:
                        ssid = m.group(1).strip()
                        if ssid:
                            out_list.append(ssid)
                            break

    elif s == "Linux":
        code, out, err = _run(
            ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"])
        if code == 0:
            for line in out.splitlines():
                name, _, typ = line.rpartition(":")
                if "wireless" in typ:
                    out_list.append(name.replace("\\:", ":"))

    elif s == "Darwin":
        plist = ("/Library/Preferences/SystemConfiguration/"
                 "com.apple.airport.preferences.plist")
        if os.path.exists(plist):
            try:
                code, out, err = _run(["defaults", "read", plist])
                for m in re.finditer(r"SSID_STR\s*=\s*\"([^\"]+)\"", out):
                    out_list.append(m.group(1))
            except Exception:
                pass

    seen, uniq = set(), []
    for p in out_list:
        if p and p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


# ==================================================================
#                     SCAN WINDOWS
# ==================================================================
def _parse_netsh_networks(out: str) -> list:
    nets, cur = [], None
    for raw in out.splitlines():
        line = _clean_netsh_line(raw).strip()
        m = re.match(r"^SSID\s+\d+\s*:\s*(.*)$", line)
        if m:
            if cur:
                if not cur.band:
                    cur.band = channel_to_band(cur.channel)
                nets.append(cur)
            cur = WifiNetwork(ssid=m.group(1).strip(), signal=0)
            continue
        if cur is None:
            continue
        if line.startswith(("Authentication", "Authentification")):
            cur.security = line.split(":", 1)[1].strip()
        elif line.startswith("Signal"):
            try:
                cur.signal = int(
                    line.split(":", 1)[1].strip().replace("%", ""))
            except ValueError:
                pass
        elif line.startswith(("Channel", "Canal")):
            if not cur.channel:
                cur.channel = line.split(":", 1)[1].strip()
        elif line.startswith("BSSID") and not cur.bssid:
            cur.bssid = line.split(":", 1)[1].strip()
        elif line.startswith(("Band", "Bande")):
            if not cur.band:
                cur.band = line.split(":", 1)[1].strip()

    if cur:
        if not cur.band:
            cur.band = channel_to_band(cur.channel)
        nets.append(cur)
    return nets


def _parse_netsh_interfaces(out: str) -> dict:
    info = {"ssid": "", "signal": 0, "channel": "", "bssid": "",
            "security": "", "connected": False}

    if not re.search(r"(?im)^\s*SSID\s*:", out):
        return info
    if not re.search(r"(?im)(état|state)\s*:\s*connect", out):
        return info

    for raw in out.splitlines():
        s = _clean_netsh_line(raw).strip()
        if re.match(r"^SSID\s*:", s):
            info["ssid"] = s.split(":", 1)[1].strip()
        elif re.match(r"^BSSID\s*:", s):
            info["bssid"] = s.split(":", 1)[1].strip()
        elif re.match(r"^Signal\s*:", s):
            try:
                info["signal"] = int(
                    s.split(":", 1)[1].strip().replace("%", ""))
            except ValueError:
                pass
        elif re.match(r"^(Canal|Channel)\s*:", s):
            info["channel"] = s.split(":", 1)[1].strip()
        elif re.match(r"^(Authentification|Authentication)\s*:", s):
            info["security"] = s.split(":", 1)[1].strip()

    if info["ssid"]:
        info["connected"] = True
    return info


def _scan_windows() -> ScanResult:
    code, out_if, err = _run(["netsh", "wlan", "show", "interfaces"])
    if code != 0:
        return ScanResult(
            networks=[],
            error="netsh wlan show interfaces a échoué : " + err,
            adapter_ok=False,
        )

    active = _parse_netsh_interfaces(out_if)
    adapter_ok = bool(re.search(r"(?im)^\s*(Name|Nom)\s*:", out_if))

    if not adapter_ok:
        return ScanResult(
            networks=[],
            error=("Aucune carte Wi-Fi active détectée.\n"
                   "Vérifie que le Wi-Fi est bien activé."),
            adapter_ok=False,
            raw_output=out_if[:600],
        )

    strategies = [
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        ["netsh", "wlan", "show", "networks"],
    ]

    all_nets = []
    last_raw = ""
    for cmd in strategies:
        code, out, err = _run(cmd, timeout=10)
        last_raw = out[:800]
        if code == 0:
            nets = _parse_netsh_networks(out)
            if nets:
                all_nets = nets
                break

    if not all_nets and active["connected"]:
        fallback = WifiNetwork(
            ssid=active["ssid"],
            signal=active["signal"] or 100,
            security=active["security"] or "WPA2-Personnel",
            channel=active["channel"] or "",
            bssid=active["bssid"] or "",
            band=channel_to_band(active["channel"]),
            connected=True,
        )
        return ScanResult(
            networks=[fallback],
            error=("Windows ne liste QUE le réseau auquel tu es connecté.\n\n"
                   "La liste des réseaux VOISINS est bloquée par Windows "
                   "(bug connu sur certains pilotes Intel + Windows 11).\n\n"
                   "➜ Alternative : utilise l'onglet SAVED."),
            adapter_ok=True,
            connected_ssid=active["ssid"],
        )

    if active["connected"]:
        for n in all_nets:
            if n.ssid == active["ssid"]:
                n.connected = True

    if not all_nets:
        loc = _check_location_services()
        if loc == "Deny":
            msg = ("Windows bloque la liste Wi-Fi : la LOCALISATION "
                   "est désactivée.\n\n"
                   "Fix : ouvre ms-settings:privacy-location.")
            return ScanResult(
                networks=[], error=msg, adapter_ok=True,
                needs_location=True, raw_output=last_raw,
            )
        return ScanResult(
            networks=[],
            error=("Aucun réseau détecté malgré un adaptateur actif.\n"
                   "→ Mets à jour le pilote Wi-Fi Intel.\n"
                   "→ Ou utilise l'onglet SAVED."),
            adapter_ok=True, raw_output=last_raw,
        )

    return ScanResult(networks=all_nets, adapter_ok=True)


# ==================================================================
#                     SCAN LINUX
# ==================================================================
def _scan_linux() -> ScanResult:
    if not shutil.which("nmcli"):
        return ScanResult(
            networks=[], error="nmcli introuvable.", adapter_ok=False)

    _run(["nmcli", "dev", "wifi", "rescan"], timeout=10)
    code, out, err = _run([
        "nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY,CHAN,BSSID",
        "dev", "wifi", "list",
    ])
    if code != 0:
        return ScanResult(networks=[], error="nmcli : " + err)

    nets = []
    for line in out.splitlines():
        parts = re.split(r"(?<!\\):", line)
        if len(parts) < 6:
            continue
        ssid = parts[1].replace("\\:", ":").strip()
        if not ssid:
            continue
        try:
            signal = int(parts[2])
        except ValueError:
            signal = 0
        ch = parts[4]
        nets.append(WifiNetwork(
            ssid=ssid, signal=signal,
            security=parts[3] or "Open",
            channel=ch, bssid=parts[5].strip(),
            band=channel_to_band(ch),
            connected=(parts[0].strip() == "*"),
        ))
    return ScanResult(networks=nets)


# ==================================================================
#                     SCAN MACOS
# ==================================================================
def _scan_macos() -> ScanResult:
    airport = ("/System/Library/PrivateFrameworks/Apple80211.framework/"
               "Versions/Current/Resources/airport")
    if not os.path.exists(airport):
        return ScanResult(
            networks=[], error="airport introuvable (macOS 14+).",
            adapter_ok=False,
        )
    code, out, err = _run([airport, "-s"])
    if code != 0:
        return ScanResult(networks=[], error=err or "airport a échoué")

    nets = []
    for line in out.splitlines()[1:]:
        m = re.match(r"^(.*?)\s+([0-9a-f:]{17})\s+(-?\d+)\s+(\d+)\s+", line)
        if not m:
            continue
        rssi = int(m.group(3))
        signal = max(0, min(100, 2 * (rssi + 100)))
        ch = m.group(4)
        nets.append(WifiNetwork(
            ssid=m.group(1).strip(), signal=signal,
            security="", channel=ch, bssid=m.group(2),
            band=channel_to_band(ch),
        ))
    return ScanResult(networks=nets)


def scan_all() -> ScanResult:
    s = platform.system()
    if s == "Windows":
        return _scan_windows()
    if s == "Linux":
        return _scan_linux()
    if s == "Darwin":
        return _scan_macos()
    return ScanResult(networks=[], error="OS non supporté : " + s)


# ==================================================================
#              MOTS DE PASSE ENREGISTRÉS
# ==================================================================
def get_saved_password(ssid):
    """Retourne (ok, mot_de_passe_ou_raison)."""
    s = platform.system()

    if s == "Windows":
        code, out, err = _run(
            ["netsh", "wlan", "show", "profile",
             "name=" + ssid, "key=clear"])
        if code != 0:
            return False, "Profil non trouvé."
        for raw in out.splitlines():
            line = _clean_netsh_line(raw).strip()
            if "Key Content" in line or "Contenu de la cl" in line:
                pwd = line.split(":", 1)[1].strip()
                if pwd:
                    return True, pwd
        return False, "Réseau ouvert (pas de mot de passe)."

    if s == "Linux":
        try:
            out = subprocess.check_output(
                ["nmcli", "-s", "-g", "802-11-wireless-security.psk",
                 "connection", "show", ssid],
                encoding="utf-8", errors="ignore",
            ).strip()
            if out:
                return True, out
        except Exception:
            pass
        for path in (
            "/etc/NetworkManager/system-connections/" + ssid + ".nmconnection",
            "/etc/NetworkManager/system-connections/" + ssid,
        ):
            try:
                with open(path) as f:
                    for line in f:
                        if line.startswith("psk="):
                            return True, line.split("=", 1)[1].strip()
            except Exception:
                continue
        return False, "Accès refusé (root requis)."

    if s == "Darwin":
        code, out, err = _run(
            ["security", "find-generic-password", "-wa", ssid])
        if code == 0 and out.strip():
            return True, out.strip()
        return False, "Mot de passe introuvable."

    return False, "OS non supporté."


# ==================================================================
#                   CONNEXION
# ==================================================================
def connect_to(ssid, password=""):
    s = platform.system()
    try:
        if s == "Windows":
            profile = (
                '<?xml version="1.0"?>\n'
                '<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">\n'
                '  <name>' + ssid + '</name>\n'
                '  <SSIDConfig><SSID><name>' + ssid + '</name></SSID></SSIDConfig>\n'
                '  <connectionType>ESS</connectionType>\n'
                '  <connectionMode>auto</connectionMode>\n'
                '  <MSM><security>\n'
                '    <authEncryption><authentication>WPA2PSK</authentication>\n'
                '    <encryption>AES</encryption><useOneX>false</useOneX></authEncryption>\n'
                '    <sharedKey><keyType>passPhrase</keyType>\n'
                '    <protected>false</protected><keyMaterial>' + password + '</keyMaterial></sharedKey>\n'
                '  </security></MSM>\n'
                '</WLANProfile>'
            )
            tmp = os.path.join(
                os.environ.get("TEMP", "."), "wifi_profile.xml")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(profile)
            _run(["netsh", "wlan", "add", "profile", "filename=" + tmp])
            _run(["netsh", "wlan", "connect", "name=" + ssid])
            return True, "Connexion lancée."

        if s == "Linux":
            cmd = ["nmcli", "dev", "wifi", "connect", ssid]
            if password:
                cmd += ["password", password]
            code, out, err = _run(cmd)
            return code == 0, (out + err).strip()

        if s == "Darwin":
            code, out, err = _run(
                ["networksetup", "-setairportnetwork",
                 "en0", ssid, password])
            return code == 0, (out + err).strip()
    except Exception as e:
        return False, str(e)
    return False, "OS non supporté."


def disconnect_current():
    s = platform.system()
    if s == "Windows":
        _run(["netsh", "wlan", "disconnect"])
    elif s == "Linux":
        _run(["nmcli", "dev", "disconnect", "wlan0"])
    elif s == "Darwin":
        _run(["networksetup", "-setairportpower", "en0", "off"])
        _run(["networksetup", "-setairportpower", "en0", "on"])