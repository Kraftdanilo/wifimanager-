"""Wifi Manager - Flask backend v2.

Nouveautés :
  • Chiffrement AES des mots de passe (crypto.py)
  • Configuration centralisée (config.py)
  • Logs rotatifs (logging_config.py)
  • Rate limiting (rate_limit.py)
  • /api/health pour monitoring
  • Mode lecture seule (--readonly)
  • Gestion du mot de passe maître
"""
import io
import ipaddress
import json
import secrets
import socket
import sqlite3
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from flask import (Flask, jsonify, render_template, request,
                   send_file, abort)

import crypto
import wifi_backend as wb
from config import Config
from logging_config import setup_logging, get_logger
from rate_limit import RateLimiter


# ==================================================================
#                        INITIALISATION
# ==================================================================
Config.validate()
log = setup_logging(Config.LOG_PATH, Config.LOG_LEVEL)
log.info("=" * 60)
log.info("WIFI MANAGER — démarrage")
log.info("=" * 60)

# Chiffrement
encryption_active = crypto.setup_from_env_or_prompt(Config.SALT_PATH)
if encryption_active:
    log.info("🔐 Chiffrement AES activé")
else:
    log.warning("⚠  Mode NON CHIFFRÉ — données en clair dans la DB")

# Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
SHARE_TOKEN = secrets.token_urlsafe(16)

# Rate limiter (par défaut : 60 req/min par IP + endpoint)
limiter = RateLimiter(max_per_minute=Config.RATE_LIMIT_PER_MIN)

# QR optionnel
try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False
    log.warning("qrcode non installé — partage QR désactivé")


# ==================================================================
#                      BASE DE DONNÉES
# ==================================================================
def _db_init():
    with sqlite3.connect(Config.DB_PATH) as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS password_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssid TEXT NOT NULL,
            pwd_hash TEXT NOT NULL,
            password TEXT,
            previous_hash TEXT,
            previous_password TEXT,
            changed_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_pwd_ssid
            ON password_history(ssid);

        CREATE TABLE IF NOT EXISTS known_networks (
            ssid TEXT PRIMARY KEY,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            last_password_hash TEXT,
            favorite INTEGER DEFAULT 0,
            notes TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS connection_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssid TEXT NOT NULL,
            action TEXT NOT NULL,
            success INTEGER NOT NULL,
            message TEXT,
            timestamp TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_log_ts
            ON connection_log(timestamp DESC);

        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            network_count INTEGER NOT NULL,
            ssids_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_scan_ts
            ON scan_history(timestamp DESC);

        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """)


@contextmanager
def db():
    conn = sqlite3.connect(Config.DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _hash(s: str) -> str:
    import hashlib
    if not s:
        return ""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


# ==================================================================
#              CHIFFREMENT : HELPERS
# ==================================================================
def _enc(p: str) -> str:
    """Chiffre si le module est prêt, sinon laisse en clair."""
    if not p:
        return ""
    return crypto.encrypt(p)


def _dec(p: str) -> str:
    """Déchiffre ; tolère les legacy en clair."""
    if not p:
        return ""
    return crypto.decrypt(p)


# ==================================================================
#              SUIVI DES MOTS DE PASSE
# ==================================================================
def record_password(ssid: str, pwd: str) -> dict:
    result = {
        "changed": False,
        "previous_password": "",
        "previous_date": "",
        "first_seen": False,
    }
    pwd_hash = _hash(pwd)
    now = _now()

    with db() as c:
        row = c.execute(
            "SELECT * FROM known_networks WHERE ssid = ?", (ssid,)
        ).fetchone()

        if row is None:
            c.execute(
                "INSERT INTO known_networks "
                "(ssid, first_seen, last_seen, last_password_hash) "
                "VALUES (?, ?, ?, ?)",
                (ssid, now, now, pwd_hash),
            )
            result["first_seen"] = True
            return result

        old_hash = row["last_password_hash"] or ""
        c.execute(
            "UPDATE known_networks SET last_seen = ? WHERE ssid = ?",
            (now, ssid),
        )

        if old_hash and pwd_hash and old_hash != pwd_hash:
            prev = c.execute(
                "SELECT password, changed_at FROM password_history "
                "WHERE ssid = ? ORDER BY id DESC LIMIT 1",
                (ssid,),
            ).fetchone()

            prev_pwd = _dec(prev["password"]) if prev else ""
            prev_date = prev["changed_at"] if prev else ""

            c.execute(
                "INSERT INTO password_history "
                "(ssid, pwd_hash, password, previous_hash, "
                " previous_password, changed_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (ssid, pwd_hash, _enc(pwd), old_hash,
                 _enc(prev_pwd) if prev_pwd else "", now),
            )
            c.execute(
                "UPDATE known_networks SET last_password_hash = ? "
                "WHERE ssid = ?",
                (pwd_hash, ssid),
            )
            result["changed"] = True
            result["previous_password"] = prev_pwd
            result["previous_date"] = prev_date

    return result


# ==================================================================
#                          UTILS
# ==================================================================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _is_local(req):
    addr = req.remote_addr or ""
    if addr in ("127.0.0.1", "::1", "localhost"):
        return True
    try:
        ip = ipaddress.ip_address(addr)
        return ip.is_loopback or ip.is_private
    except ValueError:
        return False


def _current_port():
    host = request.host or f"127.0.0.1:{Config.PORT}"
    return host.split(":")[-1] if ":" in host else str(Config.PORT)


def _log_connection(ssid: str, action: str, success: bool, msg: str = ""):
    try:
        with db() as c:
            c.execute(
                "INSERT INTO connection_log "
                "(ssid, action, success, message, timestamp) "
                "VALUES (?, ?, ?, ?, ?)",
                (ssid, action, 1 if success else 0, msg[:200], _now()),
            )
        log.info(f"[{action}] {ssid} — {'OK' if success else 'FAIL'}")
    except Exception as e:
        log.error(f"log_connection: {e}")


# ==================================================================
#                    SÉCURITÉ (token + rate limit)
# ==================================================================
@app.before_request
def _check_access():
    # 1. Rate limiting global (par IP+endpoint)
    key = f"{request.remote_addr}:{request.endpoint}"
    allowed, wait = limiter.check(key)
    if not allowed:
        log.warning(f"Rate limit dépassé : {key}")
        abort(429, description=f"Trop de requêtes. Réessayez dans {wait} s.")

    # 2. Token obligatoire hors LAN
    if _is_local(request):
        return
    token = (request.args.get("t")
             or request.headers.get("X-Token")
             or "")
    if token != SHARE_TOKEN:
        abort(403)


@app.errorhandler(429)
def _err_429(e):
    return jsonify({"error": "rate_limit", "message": str(e.description)}), 429


# ==================================================================
#                          ROUTES
# ==================================================================
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- HEALTH ----------------
@app.route("/api/health")
def api_health():
    """Endpoint de monitoring léger."""
    try:
        with db() as c:
            c.execute("SELECT 1").fetchone()
        db_ok = True
    except Exception as e:
        log.error(f"health db: {e}")
        db_ok = False

    return jsonify({
        "status": "ok" if db_ok else "degraded",
        "version": Config.APP_VERSION,
        "encryption": crypto.is_ready(),
        "readonly": Config.READONLY,
        "db": db_ok,
        "rate_limit": limiter.stats(),
        "uptime_since": str(datetime.now().isoformat(timespec="seconds")),
    })


# ---------------- SCAN ----------------
@app.route("/api/scan")
def api_scan():
    result = wb.scan_all()

    if result.networks:
        try:
            with db() as c:
                ssids = [n.ssid for n in result.networks]
                c.execute(
                    "INSERT INTO scan_history "
                    "(timestamp, network_count, ssids_json) "
                    "VALUES (?, ?, ?)",
                    (_now(), len(ssids),
                     json.dumps(ssids, ensure_ascii=False)),
                )
                c.execute(
                    "DELETE FROM scan_history WHERE id NOT IN "
                    "(SELECT id FROM scan_history ORDER BY id DESC LIMIT 100)"
                )
        except Exception as e:
            log.error(f"scan_history: {e}")

    return jsonify({
        "networks": [
            {
                "ssid": n.ssid,
                "signal": n.signal,
                "security": n.security,
                "channel": n.channel,
                "bssid": n.bssid,
                "band": n.band,
                "connected": n.connected,
            }
            for n in result.networks
        ],
        "error": result.error,
        "adapter_ok": result.adapter_ok,
        "needs_location": result.needs_location,
        "connected_ssid": result.connected_ssid,
    })


# ---------------- DIAGNOSTICS ----------------
@app.route("/api/diagnostics")
def api_diag():
    return jsonify(wb.diagnostics())


@app.route("/api/profiles-raw")
def api_profiles_raw():
    return jsonify({
        "os": wb.platform.system(),
        "raw": wb.profiles_raw(),
        "parsed": wb.list_saved_profiles(),
        "count": len(wb.list_saved_profiles()),
    })


# ---------------- PROFILS + MDP ----------------
@app.route("/api/saved")
def api_saved():
    out = []
    for ssid in wb.list_saved_profiles():
        try:
            ok, pwd_or_err = wb.get_saved_password(ssid)
        except Exception as e:
            log.error(f"saved: {ssid} — {e}")
            out.append({
                "ssid": ssid, "password": "", "has_password": False,
                "note": "Erreur : " + str(e),
                "changed": False, "previous_password": "",
                "previous_date": "", "first_seen": False,
            })
            continue

        entry = {
            "ssid": ssid,
            "password": pwd_or_err if ok else "",
            "has_password": bool(ok),
            "note": "" if ok else str(pwd_or_err),
            "changed": False,
            "previous_password": "",
            "previous_date": "",
            "first_seen": False,
        }

        if ok:
            try:
                info = record_password(ssid, pwd_or_err)
                entry["changed"] = info["changed"]
                entry["previous_password"] = info["previous_password"]
                entry["previous_date"] = info["previous_date"]
                entry["first_seen"] = info["first_seen"]
            except Exception as e:
                entry["note"] = "DB error: " + str(e)

        out.append(entry)

    return jsonify(out)


# ---------------- HISTORIQUE ----------------
@app.route("/api/history")
def api_history_all():
    with db() as c:
        rows = c.execute(
            "SELECT ssid, password, previous_password, "
            "changed_at FROM password_history "
            "ORDER BY changed_at DESC LIMIT 200"
        ).fetchall()
    # Déchiffre avant envoi
    return jsonify([
        {
            "ssid": r["ssid"],
            "password": _dec(r["password"]),
            "previous_password": _dec(r["previous_password"]),
            "changed_at": r["changed_at"],
        }
        for r in rows
    ])


@app.route("/api/history", methods=["DELETE"])
def api_history_clear():
    with db() as c:
        c.execute("DELETE FROM password_history")
    log.info("Historique MDP effacé")
    return jsonify({"ok": True})


# ---------------- RÉSEAUX CONNUS ----------------
@app.route("/api/known")
def api_known():
    with db() as c:
        rows = c.execute(
            "SELECT ssid, first_seen, last_seen, favorite, notes "
            "FROM known_networks ORDER BY last_seen DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/known/<path:ssid>", methods=["POST"])
def api_known_update(ssid):
    data = request.get_json(silent=True) or {}
    with db() as c:
        row = c.execute(
            "SELECT ssid FROM known_networks WHERE ssid = ?", (ssid,)
        ).fetchone()
        if not row:
            return jsonify({"ok": False, "error": "Inconnu"}), 404

        if "notes" in data:
            c.execute("UPDATE known_networks SET notes = ? WHERE ssid = ?",
                      (str(data["notes"])[:500], ssid))
        if "favorite" in data:
            c.execute("UPDATE known_networks SET favorite = ? WHERE ssid = ?",
                      (1 if data["favorite"] else 0, ssid))
    return jsonify({"ok": True})


# ---------------- JOURNAL ----------------
@app.route("/api/logs")
def api_logs():
    limit = min(int(request.args.get("limit", 100)), 500)
    with db() as c:
        rows = c.execute(
            "SELECT ssid, action, success, message, timestamp "
            "FROM connection_log ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/logs", methods=["DELETE"])
def api_logs_clear():
    with db() as c:
        c.execute("DELETE FROM connection_log")
    return jsonify({"ok": True})


# ---------------- PRÉFÉRENCES ----------------
@app.route("/api/preferences", methods=["GET"])
def api_prefs_get():
    with db() as c:
        rows = c.execute("SELECT key, value FROM preferences").fetchall()
    return jsonify({r["key"]: json.loads(r["value"]) for r in rows})


@app.route("/api/preferences", methods=["POST"])
def api_prefs_set():
    data = request.get_json(silent=True) or {}
    with db() as c:
        for k, v in data.items():
            c.execute(
                "INSERT OR REPLACE INTO preferences (key, value) "
                "VALUES (?, ?)",
                (str(k)[:50], json.dumps(v, ensure_ascii=False)),
            )
    return jsonify({"ok": True})


# ---------------- STATS ----------------
@app.route("/api/stats")
def api_stats():
    with db() as c:
        n_scans = c.execute(
            "SELECT COUNT(*) FROM scan_history").fetchone()[0]
        n_known = c.execute(
            "SELECT COUNT(*) FROM known_networks").fetchone()[0]
        n_changes = c.execute(
            "SELECT COUNT(*) FROM password_history").fetchone()[0]
        n_conn = c.execute(
            "SELECT COUNT(*) FROM connection_log "
            "WHERE action='connect'").fetchone()[0]
        n_conn_ok = c.execute(
            "SELECT COUNT(*) FROM connection_log "
            "WHERE action='connect' AND success=1").fetchone()[0]
        n_favs = c.execute(
            "SELECT COUNT(*) FROM known_networks "
            "WHERE favorite=1").fetchone()[0]

        recent_scans = c.execute(
            "SELECT timestamp, network_count FROM scan_history "
            "ORDER BY id DESC LIMIT 10"
        ).fetchall()

        all_rows = c.execute(
            "SELECT ssids_json FROM scan_history LIMIT 200"
        ).fetchall()

    from collections import Counter
    freq = Counter()
    for row in all_rows:
        try:
            for s in json.loads(row["ssids_json"]):
                freq[s] += 1
        except Exception:
            pass
    top = [{"ssid": k, "count": v} for k, v in freq.most_common(5)]

    last_bands = {"2.4 GHz": 0, "5 GHz": 0, "6 GHz": 0}
    try:
        scan_now = wb.scan_all()
        for n in scan_now.networks:
            if n.band in last_bands:
                last_bands[n.band] += 1
    except Exception:
        pass

    return jsonify({
        "total_scans":      n_scans,
        "known_networks":   n_known,
        "password_changes": n_changes,
        "connections":      n_conn,
        "connections_ok":   n_conn_ok,
        "favorites":        n_favs,
        "recent_scans":     [dict(r) for r in recent_scans],
        "top_networks":     top,
        "last_scan":        last_bands,
    })


# ---------------- EXPORT PDF ----------------
@app.route("/api/export/pdf")
def api_export_pdf():
    if not Config.ENABLE_PDF:
        return jsonify({"ok": False, "error": "PDF désactivé"}), 503

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak
        )
    except ImportError:
        return jsonify({
            "ok": False,
            "error": "reportlab non installé. → pip install reportlab"
        }), 500

    with db() as c:
        known = [dict(r) for r in c.execute(
            "SELECT ssid, first_seen, last_seen, favorite, notes "
            "FROM known_networks ORDER BY ssid"
        ).fetchall()]

        changes_raw = [dict(r) for r in c.execute(
            "SELECT ssid, password, previous_password, changed_at "
            "FROM password_history ORDER BY changed_at DESC LIMIT 100"
        ).fetchall()]

        logs = [dict(r) for r in c.execute(
            "SELECT ssid, action, success, message, timestamp "
            "FROM connection_log ORDER BY timestamp DESC LIMIT 100"
        ).fetchall()]

        recent_scans = [dict(r) for r in c.execute(
            "SELECT timestamp, network_count FROM scan_history "
            "ORDER BY id DESC LIMIT 20"
        ).fetchall()]

    # Déchiffre les changements
    changes = [
        {
            "ssid": c["ssid"],
            "password": _dec(c["password"]),
            "previous_password": _dec(c["previous_password"]),
            "changed_at": c["changed_at"],
        }
        for c in changes_raw
    ]

    scan_now = wb.scan_all()
    bands = {"2.4 GHz": 0, "5 GHz": 0, "6 GHz": 0}
    for n in scan_now.networks:
        if n.band in bands:
            bands[n.band] += 1

    n_conn_ok = sum(1 for l in logs
                    if l["action"] == "connect" and l["success"])
    n_conn = sum(1 for l in logs if l["action"] == "connect")
    success_pct = int(100 * n_conn_ok / n_conn) if n_conn else 0

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"],
                        textColor=colors.HexColor("#0a0a0a"),
                        fontName="Helvetica-Bold", fontSize=22)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"],
                        textColor=colors.HexColor("#0033ee"),
                        fontName="Helvetica-Bold", fontSize=14,
                        spaceBefore=14, spaceAfter=8)
    body = ParagraphStyle("body", parent=styles["Normal"],
                          fontName="Helvetica", fontSize=10)
    small = ParagraphStyle("small", parent=styles["Normal"],
                           fontName="Helvetica-Oblique", fontSize=8,
                           textColor=colors.HexColor("#666666"))
    warn = ParagraphStyle("warn", parent=styles["Normal"],
                          fontName="Helvetica-Bold", fontSize=10,
                          textColor=colors.HexColor("#c0392b"))
    big = ParagraphStyle("big", fontSize=18, fontName="Helvetica-Bold")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm,
        title="Wifi Manager Dashboard",
        author="Wifi Manager",
    )

    story = []
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    story.append(Paragraph("📡  WIFI MANAGER", h1))
    story.append(Paragraph(
        "Tableau de bord — généré le " + now_str
        + ("  🔐 chiffré" if crypto.is_ready() else "  ⚠ non chiffré"),
        body))
    story.append(Spacer(1, 8*mm))

    stats_table_data = [
        [Paragraph("<b>SCANS</b>", small),
         Paragraph("<b>RÉSEAUX CONNUS</b>", small),
         Paragraph("<b>CHANGEMENTS MDP</b>", small),
         Paragraph("<b>CONNEXIONS</b>", small)],
        [Paragraph("<b>" + str(len(recent_scans)) + "</b>", big),
         Paragraph("<b>" + str(len(known)) + "</b>", big),
         Paragraph("<b>" + str(len(changes)) + "</b>", big),
         Paragraph("<b>" + str(n_conn) + "</b>", big)],
    ]
    t = Table(stats_table_data, colWidths=[42*mm]*4)
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#dfe6e9")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dfe6e9")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5f6fa")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Répartition par bande (scan actuel)", h2))
    total_bands = sum(bands.values()) or 1
    band_rows = [["Bande", "Nombre", "Pourcentage"]]
    for b, n in bands.items():
        band_rows.append([b, str(n), f"{int(100*n/total_bands)} %"])
    bt = Table(band_rows, colWidths=[60*mm, 40*mm, 40*mm])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dfe6e9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(bt)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        f"Taux de réussite connexions : <b>{success_pct} %</b> "
        f"({n_conn_ok} / {n_conn})", body))

    story.append(PageBreak())

    story.append(Paragraph(
        f"Historique changements ({len(changes)})", h2))
    if changes:
        ch_rows = [["SSID", "Ancien mdp", "Nouveau mdp", "Date"]]
        for c in changes[:50]:
            ch_rows.append([
                c["ssid"][:30],
                (c["previous_password"] or "—")[:25],
                (c["password"] or "—")[:25],
                (c["changed_at"] or "")[:16].replace("T", " "),
            ])
        ct = Table(ch_rows, colWidths=[45*mm, 45*mm, 45*mm, 35*mm],
                   repeatRows=1)
        ct.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#b35900")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dfe6e9")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#fff8e1")]),
        ]))
        story.append(ct)
    else:
        story.append(Paragraph("Aucun changement enregistré.", body))

    story.append(Spacer(1, 6*mm))

    story.append(Paragraph(f"Réseaux connus ({len(known)})", h2))
    if known:
        k_rows = [["SSID", "1ère vue", "Dernière vue", "★"]]
        for k in known[:80]:
            k_rows.append([
                k["ssid"][:40],
                (k["first_seen"] or "")[:10],
                (k["last_seen"] or "")[:10],
                "★" if k["favorite"] else "",
            ])
        kt = Table(k_rows, colWidths=[80*mm, 30*mm, 30*mm, 10*mm],
                   repeatRows=1)
        kt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#27ae60")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dfe6e9")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f8f9fa")]),
        ]))
        story.append(kt)

    story.append(PageBreak())

    story.append(Paragraph(f"Journal connexions ({len(logs)})", h2))
    if logs:
        l_rows = [["SSID", "Action", "Résultat", "Date", "Message"]]
        for l in logs[:60]:
            l_rows.append([
                l["ssid"][:25],
                l["action"],
                "OK" if l["success"] else "ÉCHEC",
                (l["timestamp"] or "")[:16].replace("T", " "),
                (l["message"] or "")[:40],
            ])
        lt = Table(l_rows, colWidths=[45*mm, 22*mm, 20*mm, 30*mm, 48*mm],
                   repeatRows=1)
        lt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dfe6e9")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f8f9fa")]),
        ]))
        story.append(lt)
    else:
        story.append(Paragraph("Aucune connexion enregistrée.", body))

    story.append(Spacer(1, 10*mm))
    story.append(Paragraph(
        "⚠  Ce document contient des mots de passe en clair. "
        "Ne pas diffuser.", warn))

    doc.build(story)
    buf.seek(0)

    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    return send_file(
        buf, mimetype="application/pdf",
        as_attachment=True,
        download_name=f"wifi-dashboard-{stamp}.pdf",
    )


# ---------------- CONNEXION ----------------
@app.route("/api/connect", methods=["POST"])
def api_connect():
    if Config.READONLY:
        return jsonify({
            "ok": False,
            "message": "Mode lecture seule activé (WIFI_READONLY=1)."
        }), 403

    data = request.get_json(silent=True) or {}
    ssid = (data.get("ssid") or "").strip()
    pwd = data.get("password") or ""
    if not ssid:
        return jsonify({"ok": False, "message": "SSID requis"}), 400

    ok, msg = wb.connect_to(ssid, pwd)
    _log_connection(ssid, "connect", ok, msg)
    return jsonify({"ok": bool(ok), "message": msg})


@app.route("/api/disconnect", methods=["POST"])
def api_disconnect():
    if Config.READONLY:
        return jsonify({"ok": False, "message": "Lecture seule."}), 403

    data = request.get_json(silent=True) or {}
    ssid = data.get("ssid", "(current)")
    wb.disconnect_current()
    _log_connection(ssid, "disconnect", True, "")
    return jsonify({"ok": True})


# ---------------- MISE À JOUR ----------------
@app.route("/api/update/check")
def api_update_check():
    """Vérifie si une mise à jour est disponible sur GitHub."""
    try:
        import update
    except ImportError:
        return jsonify({
            "ok": False,
            "error": "module de mise à jour non installé (update.py absent)",
            "update_available": False,
        }), 503
    return jsonify(update.check_latest())


@app.route("/api/update/apply", methods=["POST"])
def api_update_apply():
    """Applique la mise à jour (désactivé en mode lecture seule)."""
    if Config.READONLY:
        return jsonify({"ok": False, "message": "Lecture seule."}), 403
    try:
        import update
    except ImportError:
        return jsonify({
            "ok": False,
            "error": "module de mise à jour non installé (update.py absent)",
        }), 503
    return jsonify(update.apply_update())


# ---------------- QR ----------------
@app.route("/api/qr/<path:ssid>")
def api_qr(ssid):
    if not HAS_QR:
        abort(503)
    ok, pwd = wb.get_saved_password(ssid)
    if not ok:
        abort(404)
    text = f"WIFI:T:WPA;S:{ssid};P:{pwd};;"
    img = qrcode.make(text, box_size=8, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/api/share-info")
def api_share_info():
    ip = get_local_ip()
    port = _current_port()
    url = f"http://{ip}:{port}/?t={SHARE_TOKEN}"
    return jsonify({"url": url, "ip": ip, "token": SHARE_TOKEN,
                    "port": port})


@app.route("/api/share-qr")
def api_share_qr():
    if not HAS_QR:
        abort(503)
    ip = get_local_ip()
    port = _current_port()
    url = f"http://{ip}:{port}/?t={SHARE_TOKEN}"
    img = qrcode.make(url, box_size=8, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


# ==================================================================
#                          DÉMARRAGE
# ==================================================================
_db_init()
log.info(f"Base de données : {Config.DB_PATH}")

if __name__ == "__main__":
    print()
    print("=" * 62)
    print("                     WIFI MANAGER")
    print("=" * 62)
    print(f"  Local : http://127.0.0.1:{Config.PORT}")
    print(f"  LAN   : http://{get_local_ip()}:{Config.PORT}/?t={SHARE_TOKEN}")
    print("=" * 62)
    print(f"  Base de données : {Config.DB_PATH}")
    print(f"  Chiffrement     : {'✅ AES activé' if crypto.is_ready() else '⚠ NON chiffré'}")
    print(f"  Mode            : {'READONLY' if Config.READONLY else 'Normal'}")
    print(f"  Rate limit      : {Config.RATE_LIMIT_PER_MIN}/min")
    print("=" * 62)
    print("  Ctrl+C pour arrêter")
    print()

    try:
        app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG,
                threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        log.info("Arrêt demandé")
        sys.exit(0)