/* ==========================================================
   WIFI MANAGER — Frontend v5
   i18n FR/EN · Dark mode · Notifs · Historique · Stats · PDF
   Cache 3 niveaux (mémoire / sessionStorage / localStorage)
   ========================================================== */

/* ==========================================================
                     TRADUCTIONS
   ========================================================== */
const I18N = {
  fr: {
    'nav.scan':'SCAN','nav.saved':'ENREGISTRÉS','nav.history':'HISTORIQUE',
    'nav.stats':'STATS','nav.share':'PARTAGER',
    'btn.refresh':'ACTUALISER','btn.reload':'RECHARGER','btn.retry':'RÉESSAYER',
    'btn.clear':'EFFACER','btn.close':'FERMER','btn.copy':'COPIER',
    'btn.connect':'CONNECTER','btn.disconnect':'DÉCONNECTER',
    'btn.diagnostic':'DIAGNOSTIC','btn.cancel':'ANNULER','btn.ok':'OK',
    'btn.qr':'QR','btn.export_pdf':'PDF',
    'common.loading':'CHARGEMENT…','common.empty':'AUCUN RÉSULTAT',
    'common.error':'ERREUR','common.yes':'OUI','common.no':'NON',
    'common.unknown':'INCONNU',
    'scan.filter':'FILTRER SSID','scan.scanning':'SCAN EN COURS…',
    'scan.empty':'AUCUN RÉSEAU TROUVÉ','scan.cache':'CACHE LOCAL',
    'scan.cacheoff':'HORS-LIGNE — CACHE AFFICHÉ',
    'scan.no_match':'AUCUN RÉSEAU CORRESPONDANT','scan.connected':'CONNECTÉ',
    'saved.empty':'AUCUN PROFIL ENREGISTRÉ','saved.open_network':'RÉSEAU OUVERT',
    'saved.password_saved':'MOT DE PASSE ENREGISTRÉ',
    'saved.no_password':'SANS MOT DE PASSE (OUVERT)',
    'saved.changed_banner':'MOT DE PASSE MODIFIÉ',
    'saved.new_first':'PREMIER ENREGISTREMENT','saved.networks_word':'réseaux',
    'history.filter.all':'TOUT','history.filter.changes':'CHANGEMENTS MDP',
    'history.filter.connections':'CONNEXIONS','history.empty':'AUCUN ÉVÉNEMENT',
    'history.changed':'MOT DE PASSE CHANGÉ','history.previous':'ANCIEN',
    'history.new':'NOUVEAU','history.connect':'CONNEXION',
    'history.disconnect':'DÉCONNEXION','history.success':'RÉUSSIE',
    'history.failed':'ÉCHOUÉE',
    'history.confirm_clear':'Effacer TOUT l\'historique des changements de mot de passe ?',
    'history.cleared':'HISTORIQUE EFFACÉ',
    'stats.title':'TABLEAU DE BORD','stats.total_scans':'SCANS TOTAUX',
    'stats.known':'RÉSEAUX CONNUS','stats.changes':'CHANGEMENTS MDP',
    'stats.connections':'CONNEXIONS','stats.favorites':'FAVORIS',
    'stats.recent_scans':'RÉSEAUX VUS PAR SCAN (10 DERNIERS)',
    'stats.band_dist':'RÉPARTITION PAR BANDE (SCAN ACTUEL)',
    'stats.top_networks':'TOP RÉSEAUX PAR FRÉQUENCE',
    'stats.success_rate':'TAUX DE RÉUSSITE DES CONNEXIONS',
    'stats.no_data':'PAS ENCORE ASSEZ DE DONNÉES',
    'stats.sub_networks':'réseau(x)','stats.sub_attempts':'tentative(s)',
    'stats.sub_records':'enregistrement(s)',
    'share.open_phone':'OUVRIR SUR VOTRE TÉLÉPHONE','share.copy_url':'COPIER L\'URL',
    'share.hint':'Assurez-vous que le téléphone est<br>sur le même réseau Wi-Fi.',
    'share.token_hint':'L\'URL contient un jeton d\'accès privé.',
    'modal.pwd_title':'MOT DE PASSE REQUIS','modal.pwd_network':'RÉSEAU',
    'modal.qr_share':'PARTAGER','modal.qr_hint':'Scannez avec l\'appareil photo<br>pour vous connecter',
    'modal.diag_title':'DIAGNOSTIC SYSTÈME',
    'diag.os':'SYSTÈME','diag.netsh':'NETSH','diag.nmcli':'NMCLI',
    'diag.airport':'AIRPORT','diag.adapter':'CARTE ACTIVE',
    'diag.location':'LOCALISATION','diag.networks':'RÉSEAUX VUS',
    'diag.raw':'SORTIE BRUTE DE LA COMMANDE','diag.missing':'MANQUANT',
    'diag.ok':'OK','diag.disabled':'DÉSACTIVÉE',
    'toast.connected':'CONNECTÉ : ','toast.connecting':'CONNEXION À ',
    'toast.disconnected':'DÉCONNECTÉ','toast.copied':'COPIÉ',
    'toast.copy_failed':'ÉCHEC DE COPIE','toast.failed':'ÉCHEC : ',
    'toast.diag_unavailable':'DIAGNOSTIC INDISPONIBLE : ',
    'toast.exported':'PDF EXPORTÉ','toast.theme':'THÈME : ',
    'toast.cache_cleared':'CACHE VIDÉ','toast.cache_ready':'CACHE PRÊT',
    'err.network':'ERREUR RÉSEAU','err.no_adapter':'AUCUNE CARTE WI-FI ACTIVE',
    'err.scan_blocked':'SCAN BLOQUÉ PAR WINDOWS','err.scan_failed':'SCAN IMPOSSIBLE',
    'err.location_fix':'FIX EN 10 SECONDES :',
    'err.location_link':'Paramètres de localisation',
    'err.location_step1':'1. Ouvre ce lien :',
    'err.location_step2':'2. Active « Localisation »',
    'err.location_step3':'3. Active « Autoriser les applications de bureau à accéder à votre emplacement »',
    'err.location_step4':'4. Reviens ici et clique RÉESSAYER',
  },
  en: {
    'nav.scan':'SCAN','nav.saved':'SAVED','nav.history':'HISTORY',
    'nav.stats':'STATS','nav.share':'SHARE',
    'btn.refresh':'REFRESH','btn.reload':'RELOAD','btn.retry':'RETRY',
    'btn.clear':'CLEAR','btn.close':'CLOSE','btn.copy':'COPY',
    'btn.connect':'CONNECT','btn.disconnect':'DISCONNECT',
    'btn.diagnostic':'DIAGNOSTIC','btn.cancel':'CANCEL','btn.ok':'OK',
    'btn.qr':'QR','btn.export_pdf':'PDF',
    'common.loading':'LOADING…','common.empty':'NO RESULT',
    'common.error':'ERROR','common.yes':'YES','common.no':'NO',
    'common.unknown':'UNKNOWN',
    'scan.filter':'FILTER SSID','scan.scanning':'SCANNING…',
    'scan.empty':'NO NETWORKS FOUND','scan.cache':'LOCAL CACHE',
    'scan.cacheoff':'OFFLINE — CACHE SHOWN',
    'scan.no_match':'NO MATCHING NETWORK','scan.connected':'CONNECTED',
    'saved.empty':'NO SAVED PROFILE','saved.open_network':'OPEN NETWORK',
    'saved.password_saved':'PASSWORD SAVED',
    'saved.no_password':'NO PASSWORD (OPEN)',
    'saved.changed_banner':'PASSWORD CHANGED',
    'saved.new_first':'FIRST SEEN','saved.networks_word':'networks',
    'history.filter.all':'ALL','history.filter.changes':'PASSWORD CHANGES',
    'history.filter.connections':'CONNECTIONS','history.empty':'NO EVENT',
    'history.changed':'PASSWORD CHANGED','history.previous':'PREVIOUS',
    'history.new':'NEW','history.connect':'CONNECT',
    'history.disconnect':'DISCONNECT','history.success':'SUCCESS',
    'history.failed':'FAILED',
    'history.confirm_clear':'Clear ALL password change history?',
    'history.cleared':'HISTORY CLEARED',
    'stats.title':'DASHBOARD','stats.total_scans':'TOTAL SCANS',
    'stats.known':'KNOWN NETWORKS','stats.changes':'PASSWORD CHANGES',
    'stats.connections':'CONNECTIONS','stats.favorites':'FAVORITES',
    'stats.recent_scans':'NETWORKS PER SCAN (LAST 10)',
    'stats.band_dist':'BAND DISTRIBUTION (CURRENT SCAN)',
    'stats.top_networks':'TOP NETWORKS BY FREQUENCY',
    'stats.success_rate':'CONNECTION SUCCESS RATE',
    'stats.no_data':'NOT ENOUGH DATA YET',
    'stats.sub_networks':'network(s)','stats.sub_attempts':'attempt(s)',
    'stats.sub_records':'record(s)',
    'share.open_phone':'OPEN ON YOUR PHONE','share.copy_url':'COPY URL',
    'share.hint':'Make sure your phone is<br>on the same Wi-Fi network.',
    'share.token_hint':'The URL contains a private access token.',
    'modal.pwd_title':'PASSWORD REQUIRED','modal.pwd_network':'NETWORK',
    'modal.qr_share':'SHARE','modal.qr_hint':'Scan with your phone camera<br>to auto-connect',
    'modal.diag_title':'SYSTEM DIAGNOSTIC',
    'diag.os':'OS','diag.netsh':'NETSH','diag.nmcli':'NMCLI',
    'diag.airport':'AIRPORT','diag.adapter':'ACTIVE ADAPTER',
    'diag.location':'LOCATION','diag.networks':'NETWORKS SEEN',
    'diag.raw':'RAW COMMAND OUTPUT','diag.missing':'MISSING',
    'diag.ok':'OK','diag.disabled':'DISABLED',
    'toast.connected':'CONNECTED: ','toast.connecting':'CONNECTING TO ',
    'toast.disconnected':'DISCONNECTED','toast.copied':'COPIED',
    'toast.copy_failed':'COPY FAILED','toast.failed':'FAILED: ',
    'toast.diag_unavailable':'DIAGNOSTIC UNAVAILABLE: ',
    'toast.exported':'PDF EXPORTED','toast.theme':'THEME: ',
    'toast.cache_cleared':'CACHE CLEARED','toast.cache_ready':'CACHE READY',
    'err.network':'NETWORK ERROR','err.no_adapter':'NO ACTIVE WI-FI ADAPTER',
    'err.scan_blocked':'SCAN BLOCKED BY WINDOWS','err.scan_failed':'SCAN FAILED',
    'err.location_fix':'QUICK FIX:',
    'err.location_link':'Location settings',
    'err.location_step1':'1. Open this link:',
    'err.location_step2':'2. Enable "Location"',
    'err.location_step3':'3. Enable "Allow desktop apps to access your location"',
    'err.location_step4':'4. Come back here and click RETRY',
  }
};

let currentLang = 'fr';
function t(key) {
  const dict = I18N[currentLang] || I18N.fr;
  return dict[key] !== undefined ? dict[key] : key;
}


/* ==========================================================
              CACHE MANAGER (3 NIVEAUX)
   ==========================================================
   Niveau 1 : mémoire JS (le plus rapide)
   Niveau 2 : sessionStorage (survit au F5, perdu à la fermeture)
   Niveau 3 : localStorage (persistant)
   ========================================================== */

const CacheManager = (() => {
  const mem = new Map();          // Niveau 1
  const inflight = new Map();     // Déduplication
  const DEFAULT_TTL = 5 * 60 * 1000;   // 5 min
  const MAX_MEM_ENTRIES = 50;

  function memSet(key, value, ttl) {
    // Éviction LRU si trop d'entrées
    if (mem.size >= MAX_MEM_ENTRIES) {
      const firstKey = mem.keys().next().value;
      mem.delete(firstKey);
    }
    mem.set(key, {
      value,
      expires: Date.now() + ttl
    });
  }

  function memGet(key) {
    const e = mem.get(key);
    if (!e) return null;
    if (Date.now() > e.expires) {
      mem.delete(key);
      return null;
    }
    return e.value;
  }

  return {
    /** Écrit dans les 3 niveaux */
    set(key, value, ttl = DEFAULT_TTL) {
      memSet(key, value, ttl);
      const payload = JSON.stringify({
        v: value, e: Date.now() + ttl
      });
      try { sessionStorage.setItem(key, payload); } catch {}
      try { localStorage.setItem(key, payload); } catch {}
    },

    /** Lit en cascade (mémoire → session → local) */
    get(key) {
      let v = memGet(key);
      if (v !== null) return v;

      // sessionStorage
      try {
        const raw = sessionStorage.getItem(key);
        if (raw) {
          const o = JSON.parse(raw);
          if (o.e > Date.now()) {
            memSet(key, o.v, o.e - Date.now());
            return o.v;
          }
          sessionStorage.removeItem(key);
        }
      } catch {}

      // localStorage
      try {
        const raw = localStorage.getItem(key);
        if (raw) {
          const o = JSON.parse(raw);
          if (o.e > Date.now()) {
            const ttl = o.e - Date.now();
            memSet(key, o.v, ttl);
            try { sessionStorage.setItem(key, raw); } catch {}
            return o.v;
          }
          localStorage.removeItem(key);
        }
      } catch {}
      return null;
    },

    /** Récupère même si expiré (SWR : Stale-While-Revalidate) */
    getStale(key) {
      const v = memGet(key);
      if (v !== null) return { value: v, stale: false };

      for (const store of [sessionStorage, localStorage]) {
        try {
          const raw = store.getItem(key);
          if (raw) {
            const o = JSON.parse(raw);
            return { value: o.v, stale: Date.now() > o.e };
          }
        } catch {}
      }
      return null;
    },

    invalidate(key) {
      mem.delete(key);
      try { sessionStorage.removeItem(key); } catch {}
      try { localStorage.removeItem(key); } catch {}
    },

    invalidatePrefix(prefix) {
      const toDelete = [];
      mem.forEach((_, k) => {
        if (k.startsWith(prefix)) toDelete.push(k);
      });
      toDelete.forEach(k => mem.delete(k));

      [sessionStorage, localStorage].forEach(store => {
        try {
          const toRemove = [];
          for (let i = 0; i < store.length; i++) {
            const k = store.key(i);
            if (k && k.startsWith(prefix)) toRemove.push(k);
          }
          toRemove.forEach(k => store.removeItem(k));
        } catch {}
      });
    },

    clear() {
      mem.clear();
      try { sessionStorage.clear(); } catch {}
      // On ne vide QUE nos clés dans localStorage
      try {
        const toRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          if (k && k.startsWith('wifi_')) toRemove.push(k);
        }
        toRemove.forEach(k => localStorage.removeItem(k));
      } catch {}
    },

    /** Déduplique les appels réseau */
    async fetch(key, fetcher, ttl = DEFAULT_TTL) {
      // Si déjà en vol, on attend
      if (inflight.has(key)) return inflight.get(key);

      const promise = (async () => {
        try {
          const data = await fetcher();
          this.set(key, data, ttl);
          return data;
        } finally {
          inflight.delete(key);
        }
      })();

      inflight.set(key, promise);
      return promise;
    },

    /** SWR : renvoie le cache immédiatement, recharge en fond */
    async swr(key, fetcher, onFresh, ttl = DEFAULT_TTL) {
      // 1. Livre immédiatement le stale s'il existe
      const cached = this.getStale(key);
      if (cached) {
        onFresh(cached.value, { fromCache: true, stale: cached.stale });
        if (!cached.stale) return;   // Cache encore valide
      }

      // 2. Recharge en arrière-plan
      try {
        const fresh = await this.fetch(key, fetcher, ttl);
        onFresh(fresh, { fromCache: false, stale: false });
      } catch (e) {
        if (!cached) throw e;
        // Sinon on garde l'ancien
      }
    },

    stats() {
      return {
        memEntries: mem.size,
        inflight: inflight.size,
        sessionKeys: (() => {
          let n = 0;
          try {
            for (let i = 0; i < sessionStorage.length; i++) {
              const k = sessionStorage.key(i);
              if (k && k.startsWith('wifi_')) n++;
            }
          } catch {}
          return n;
        })(),
        localKeys: (() => {
          let n = 0;
          try {
            for (let i = 0; i < localStorage.length; i++) {
              const k = localStorage.key(i);
              if (k && k.startsWith('wifi_')) n++;
            }
          } catch {}
          return n;
        })()
      };
    }
  };
})();


/* ==========================================================
                    ÉTAT GLOBAL
   ========================================================== */
const state = {
  scan: [],
  saved: [],
  savedLoadedAt: 0,
  savedSignature: '',
  history: { changes: [], logs: [] },
  stats: null,
  activeTab: 'scan'
};

/* Clés du cache */
const CK = {
  SCAN:    'wifi_cache_scan',
  SAVED:   'wifi_cache_saved',
  HISTORY: 'wifi_cache_history',
  STATS:   'wifi_cache_stats',
  DIAG:    'wifi_cache_diag'
};

/* TTL par type de données */
const TTL = {
  SCAN:    30 * 1000,       // 30 s (change souvent)
  SAVED:   5 * 60 * 1000,   // 5 min
  HISTORY: 60 * 1000,       // 1 min
  STATS:   2 * 60 * 1000,   // 2 min
  DIAG:    10 * 60 * 1000   // 10 min
};


/* ==========================================================
                MÉMOIRE NAVIGATEUR (préférences)
   ========================================================== */
const MEM = {
  KEY: 'wifi_prefs',
  load() {
    try { return JSON.parse(localStorage.getItem(this.KEY) || '{}'); }
    catch { return {}; }
  },
  save(patch) {
    try {
      const cur = this.load();
      localStorage.setItem(this.KEY,
        JSON.stringify(Object.assign(cur, patch)));
    } catch {}
  },
  get(key, def) {
    const v = this.load()[key];
    return v === undefined ? def : v;
  },
  set(key, value) { this.save({ [key]: value }); }
};


/* ==========================================================
                     UTILITAIRES
   ========================================================== */
const $  = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

function toast(msg, isErr) {
  const el = $('#toast');
  if (!el) return;
  el.textContent = msg;
  el.classList.toggle('err', !!isErr);
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 2400);
}

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return r.json();
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;',
    '"': '&quot;', "'": '&#39;'
  }[c]));
}

function bandClass(band) {
  if (!band) return '';
  if (band.indexOf('2.4') >= 0) return 'b24';
  if (band.indexOf('6') >= 0)   return 'b6';
  if (band.indexOf('5') >= 0)   return 'b5';
  return '';
}

function isSecured(sec) {
  if (!sec) return false;
  return !/open|none|ouvert/i.test(sec);
}

function signalBars(pct) {
  const n = pct >= 75 ? 4 : pct >= 50 ? 3 : pct >= 25 ? 2 : pct > 0 ? 1 : 0;
  let html = '<span class="signal">';
  for (let i = 0; i < 4; i++) {
    html += '<i class="' + (i < n ? '' : 'off') + '"></i>';
  }
  return html + '</span>';
}

function fmtDateTime(iso) {
  if (!iso) return '';
  try {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    const pad = n => String(n).padStart(2, '0');
    return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' +
           d.getFullYear() + ' ' + pad(d.getHours()) + ':' +
           pad(d.getMinutes());
  } catch { return iso; }
}

function fmtDateOnly(iso) {
  if (!iso) return '';
  try {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    const days = currentLang === 'fr'
      ? ['DIMANCHE','LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI']
      : ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'];
    const pad = n => String(n).padStart(2, '0');
    return days[d.getDay()] + ' ' + pad(d.getDate()) + '/' +
           pad(d.getMonth() + 1) + '/' + d.getFullYear();
  } catch { return iso; }
}

function dateKey(iso) {
  try { return new Date(iso).toISOString().slice(0, 10); }
  catch { return 'unknown'; }
}

/* Signature rapide pour détecter si les données ont changé */
function signature(arr) {
  if (!Array.isArray(arr)) return '';
  return arr.map(x => x.ssid || '').sort().join('|');
}


/* ==========================================================
                     THÈME
   ========================================================== */
const THEME = {
  current: 'auto',
  init() {
    this.current = MEM.get('theme', 'auto');
    this.apply();
  },
  cycle() {
    const order = ['auto', 'light', 'dark'];
    const i = order.indexOf(this.current);
    this.current = order[(i + 1) % order.length];
    MEM.set('theme', this.current);
    this.apply();
    toast(t('toast.theme') + this.current.toUpperCase());
  },
  apply() {
    const html = document.documentElement;
    if (this.current === 'auto') {
      html.removeAttribute('data-theme');
    } else {
      html.setAttribute('data-theme', this.current);
    }
    this.updateIcon();
  },
  updateIcon() {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    const dark = this.current === 'dark'
      || (this.current === 'auto'
          && window.matchMedia('(prefers-color-scheme: dark)').matches);
    btn.textContent = dark ? '🌙' : '☀';
    btn.title = 'Thème : ' + this.current;
  }
};

window.matchMedia('(prefers-color-scheme: dark)')
  .addEventListener('change', () => {
    if (THEME.current === 'auto') THEME.apply();
  });


/* ==========================================================
                     NOTIFICATIONS
   ========================================================== */
const NOTIF = {
  KEY: 'wifi_notif_enabled',

  async requestPermission() {
    if (!('Notification' in window)) return false;
    if (Notification.permission === 'granted') return true;
    if (Notification.permission === 'denied') return false;
    const r = await Notification.requestPermission();
    return r === 'granted';
  },

  isEnabled() {
    return MEM.get(this.KEY, false)
      && 'Notification' in window
      && Notification.permission === 'granted';
  },

  async enable() {
    const ok = await this.requestPermission();
    if (ok) {
      MEM.set(this.KEY, true);
      try {
        new Notification('Notifications activées', {
          body: 'Vous serez alerté en cas de changement de mot de passe Wi-Fi.'
        });
      } catch {}
      return true;
    }
    return false;
  },

  notify(title, body, tag) {
    if (!this.isEnabled()) return;
    try {
      const n = new Notification(title, {
        body, tag: tag || 'wifi-manager',
        requireInteraction: true
      });
      n.onclick = () => { window.focus(); switchTab('saved'); n.close(); };
      setTimeout(() => n.close(), 30000);
    } catch {}
  },

  detectChanges(newSaved) {
    if (!Array.isArray(newSaved)) return [];
    const notified = MEM.get('notified_changes', {});
    const changes = [];
    newSaved.forEach(s => {
      if (!s.changed) return;
      const key = s.ssid + '|' + (s.previous_date || '');
      if (notified[key]) return;
      notified[key] = Date.now();
      changes.push(s);
    });
    const cutoff = Date.now() - 30 * 24 * 3600 * 1000;
    Object.keys(notified).forEach(k => {
      if (notified[k] < cutoff) delete notified[k];
    });
    MEM.set('notified_changes', notified);
    return changes;
  }
};


/* ==========================================================
                     i18n
   ========================================================== */
function applyI18n() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-attr]').forEach(el => {
    const spec = el.dataset.i18nAttr;
    const parts = spec.split(':');
    if (parts.length === 2) el.setAttribute(parts[0], t(parts[1]));
  });
  document.documentElement.lang = currentLang;
}

function setLang(lang) {
  if (!I18N[lang]) lang = 'fr';
  currentLang = lang;
  MEM.set('lang', lang);
  applyI18n();
  reRenderActiveTab();
}

function reRenderActiveTab() {
  switch (state.activeTab) {
    case 'scan':    renderScan();    break;
    case 'saved':   renderSaved();   break;
    case 'history': renderHistory(); break;
    case 'stats':   renderStats();   break;
    case 'share':   loadShare();     break;
  }
}


/* ==========================================================
                     NAVIGATION
   ========================================================== */
function switchTab(name) {
  state.activeTab = name;
  MEM.set('activeTab', name);
  $$('.tab').forEach(el =>
    el.classList.toggle('active', el.id === 'tab-' + name));
  $$('nav button').forEach(b =>
    b.classList.toggle('active', b.dataset.tab === name));

  if (name === 'scan')    loadScan();
  if (name === 'saved')   loadSaved();
  if (name === 'history') loadHistory();
  if (name === 'stats')   loadStats();
  if (name === 'share')   loadShare();
}


/* ==========================================================
                       TAB SCAN
   ========================================================== */
async function loadScan(force = false) {
  const list = $('#scan-list');
  if (!list) return;

  // Affichage immédiat depuis cache (SWR)
  if (!state.scan.length) {
    const cached = CacheManager.get(CK.SCAN);
    if (cached && cached.networks && cached.networks.length) {
      state.scan = cached.networks;
      renderScan();
      list.insertAdjacentHTML('afterbegin',
        '<div style="padding:8px 14px;font-size:10px;'
        + 'letter-spacing:0.15em;color:var(--muted);'
        + 'text-transform:uppercase;border-bottom:2px solid var(--fg);'
        + 'background:var(--paper)">' + esc(t('scan.cache')) + '</div>');
    } else {
      list.innerHTML = '<div class="empty">'
                    + esc(t('scan.scanning')) + '</div>';
    }
  }

  const btn = $('#btn-scan');
  if (btn) btn.classList.add('loading');

  try {
    const res = await CacheManager.fetch(
      CK.SCAN,
      () => api('/api/scan'),
      TTL.SCAN
    );

    if (force) CacheManager.set(CK.SCAN, res, TTL.SCAN);

    state.scan = res.networks || [];

    if (res.error) { showScanError(list, res); return; }

    if (!state.scan.length) {
      list.innerHTML = ''
        + '<div class="empty">' + esc(t('scan.empty'))
        + '<br><br><button class="btn" onclick="loadScan(true)">'
        + esc(t('btn.retry')) + '</button></div>';
      return;
    }

    renderScan();
  } catch (e) {
    if (!state.scan.length) {
      list.innerHTML = ''
        + '<div class="empty err">' + esc(t('err.network')) + ' : '
        + esc(e.message)
        + '<br><br><button class="btn" onclick="loadScan(true)">'
        + esc(t('btn.retry')) + '</button></div>';
    } else {
      toast(t('scan.cacheoff'), true);
    }
  } finally {
    if (btn) btn.classList.remove('loading');
  }
}

function showScanError(list, res) {
  const isLocation = !!res.needs_location;
  const isAdapter  = res.adapter_ok === false;

  let title = t('err.scan_failed');
  if (isAdapter)       title = t('err.no_adapter');
  else if (isLocation) title = t('err.scan_blocked');

  let html = '<div class="empty err" style="text-align:left;'
           + 'letter-spacing:0.05em;line-height:1.9;padding:28px 24px;'
           + 'text-transform:none">';
  html += '<strong style="font-size:14px">❌ ' + esc(title) + '</strong>';
  html += '<div style="margin-top:14px;white-space:pre-wrap">'
        + esc(res.error) + '</div>';

  if (isLocation) {
    html += ''
      + '<div style="margin-top:18px;padding:14px;'
      + 'border:2px solid var(--danger);background:#ffe0e0;color:#0a0a0a;'
      + 'letter-spacing:0;line-height:1.7">'
      +   '<strong>' + t('err.location_fix') + '</strong><br><br>'
      +   t('err.location_step1') + ' '
      +     '<a href="ms-settings:privacy-location" '
      +     'style="color:#0033ee;text-decoration:underline">'
      +     t('err.location_link') + '</a><br>'
      +   t('err.location_step2') + '<br>'
      +   t('err.location_step3') + '<br>'
      +   t('err.location_step4')
      + '</div>';
  }

  html += '<div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap">'
        +   '<button class="btn" style="padding:10px 20px;border:2px solid var(--fg)" '
        +   'onclick="loadScan(true)">🔄 ' + esc(t('btn.retry')) + '</button>'
        +   '<button class="btn" style="padding:10px 20px;'
        +   'background:var(--paper);color:var(--fg);border:2px solid var(--fg)" '
        +   'onclick="showDiagnostics()">🔍 '
        +   esc(t('btn.diagnostic')) + '</button>'
        + '</div>';
  html += '</div>';
  list.innerHTML = html;
}

function renderScan() {
  const list = $('#scan-list');
  if (!list) return;
  const q = ($('#search')?.value || '').toLowerCase();

  const items = state.scan
    .filter(n => n.ssid.toLowerCase().indexOf(q) >= 0)
    .sort((a, b) => (b.connected - a.connected) || (b.signal - a.signal));

  if (!items.length) {
    list.innerHTML = '<div class="empty">' + esc(t('scan.no_match')) + '</div>';
    return;
  }

  list.innerHTML = items.map(n => {
    const badges = [];
    if (n.band) badges.push('<span class="badge '
      + bandClass(n.band) + '">' + esc(n.band) + '</span>');
    if (n.channel) badges.push('<span class="badge">CH '
      + esc(n.channel) + '</span>');
    if (n.security) {
      const open = !isSecured(n.security);
      badges.push('<span class="badge ' + (open ? 'open' : 'sec') + '">'
        + esc(n.security) + '</span>');
    }
    if (n.connected) badges.push('<span class="badge conn">'
      + esc(t('scan.connected')) + '</span>');

    const act = n.connected
      ? '<button class="danger" data-action="disconnect">'
        + esc(t('btn.disconnect')) + '</button>'
      : '<button class="primary" data-action="connect" data-ssid="'
        + esc(n.ssid) + '">' + esc(t('btn.connect')) + '</button>';

    return ''
      + '<div class="item ' + (n.connected ? 'connected' : '') + '">'
      +   '<div>'
      +     '<div class="ssid">' + esc(n.ssid) + '</div>'
      +     '<div class="meta">' + n.signal + '% &middot; '
      +       esc(n.bssid || '--') + '</div>'
      +     '<div class="badges">' + badges.join('') + '</div>'
      +   '</div>'
      +   '<div style="display:flex;align-items:center;gap:14px">'
      +     signalBars(n.signal)
      +     '<span class="actions">' + act + '</span>'
      +   '</div>'
      + '</div>';
  }).join('');
}


/* ==========================================================
                       CONNEXION
   ========================================================== */
async function doConnect(net) {
  let pwd = '';
  if (isSecured(net.security)) {
    const saved = state.saved.find(s => s.ssid === net.ssid);
    if (saved && saved.has_password) {
      pwd = saved.password;
    } else {
      const entered = await promptPassword(net.ssid);
      if (entered === null) return;
      pwd = entered;
    }
  }

  toast(t('toast.connecting') + net.ssid + '…');
  try {
    const r = await api('/api/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ssid: net.ssid, password: pwd })
    });
    if (r.ok) {
      toast(t('toast.connected') + net.ssid);
      // Invalide les caches concernés
      CacheManager.invalidate(CK.SCAN);
      CacheManager.invalidate(CK.SAVED);
      state.savedLoadedAt = 0;
      setTimeout(() => loadScan(true), 2200);
    } else {
      toast(t('toast.failed') + (r.message || '?'), true);
    }
  } catch (e) {
    toast(t('toast.failed') + e.message, true);
  }
}

async function doDisconnect() {
  try {
    await api('/api/disconnect', { method: 'POST' });
    toast(t('toast.disconnected'));
    CacheManager.invalidate(CK.SCAN);
    state.savedLoadedAt = 0;
    setTimeout(() => loadScan(true), 1500);
  } catch (e) {
    toast(t('toast.failed') + e.message, true);
  }
}


/* ==========================================================
                    TAB SAVED (CACHE INTELLIGENT)
   ========================================================== */
async function loadSaved(force = false) {
  const list = $('#saved-list');
  if (!list) return;

  const age = Date.now() - state.savedLoadedAt;
  const hasData = state.saved.length > 0;

  // Cache valide et pas de force → affichage instantané
  if (!force && hasData && age < TTL.SAVED) {
    renderSaved();
    updateSavedBadge();
    return;
  }

  // SWR : affiche immédiatement la version en cache
  if (!hasData) {
    const cached = CacheManager.getStale(CK.SAVED);
    if (cached && Array.isArray(cached.value) && cached.value.length) {
      state.saved = cached.value;
      state.savedLoadedAt = Date.now() - 1000; // marqueur
      renderSaved();
      updateSavedBadge();
    } else {
      list.innerHTML = ''
        + '<div class="skeleton"></div>'
        + '<div class="skeleton"></div>'
        + '<div class="skeleton"></div>'
        + '<div class="skeleton"></div>';
    }
  }

  const btn = $('#btn-saved');
  if (btn) btn.classList.add('loading');

  try {
    const saved = await CacheManager.fetch(
      CK.SAVED,
      () => api('/api/saved'),
      TTL.SAVED
    );

    if (force) CacheManager.set(CK.SAVED, saved, TTL.SAVED);

    // Détecte si les données ont vraiment changé
    const newSig = signature(saved) + '|' +
                   saved.map(s => s.has_password ? '1' : '0').join('');
    const hasChanged = newSig !== state.savedSignature;

    state.saved = saved;
    state.savedLoadedAt = Date.now();
    state.savedSignature = newSig;

    // Notifs pour changements
    const freshChanges = NOTIF.detectChanges(saved);
    freshChanges.forEach(s => {
      NOTIF.notify(
        '⚠  Mot de passe Wi-Fi modifié',
        'Réseau : ' + s.ssid + '\n'
        + 'Ancien : ' + (s.previous_password || '—') + '\n'
        + 'Nouveau : ' + (s.password || '—'),
        'wifi-pwd-' + s.ssid
      );
    });

    if (hasChanged || force) {
      renderSaved();
    }
    updateSavedBadge();
  } catch (e) {
    if (!state.saved.length) {
      list.innerHTML = ''
        + '<div class="empty err">' + esc(t('common.error')) + ' : '
        + esc(e.message)
        + '<br><br><button class="btn" onclick="loadSaved(true)">'
        + esc(t('btn.retry')) + '</button></div>';
    } else {
      toast('Cache affiché — hors-ligne', true);
    }
  } finally {
    if (btn) btn.classList.remove('loading');
  }
}


function updateSavedBadge() {
  const el = document.getElementById('saved-updated');
  if (!el) return;
  if (!state.savedLoadedAt) { el.textContent = ''; return; }

  const age = Date.now() - state.savedLoadedAt;
  const mins = Math.floor(age / 60000);

  let txt;
  if (age < 10000)         txt = currentLang === 'fr' ? 'À L\'INSTANT' : 'JUST NOW';
  else if (mins < 1)       txt = currentLang === 'fr' ? 'IL Y A < 1 MIN' : '< 1 MIN AGO';
  else if (mins === 1)     txt = currentLang === 'fr' ? 'IL Y A 1 MIN' : '1 MIN AGO';
  else if (mins < 60)      txt = (currentLang === 'fr' ? 'IL Y A ' : '') + mins + (currentLang === 'fr' ? ' MIN' : ' MIN AGO');
  else                     txt = (currentLang === 'fr' ? 'IL Y A ' : '') + Math.floor(mins/60) + (currentLang === 'fr' ? ' H' : ' H AGO');

  el.textContent = txt;
  el.classList.toggle('fresh', age < TTL.SAVED);
  el.classList.toggle('stale', age >= TTL.SAVED);
}

// Rafraîchit le badge toutes les 30 s
setInterval(() => {
  if (state.activeTab === 'saved' && state.savedLoadedAt) {
    updateSavedBadge();
  }
}, 30000);


function renderSaved() {
  const list = $('#saved-list');
  if (!list) return;
  const q = ($('#search-saved')?.value || '').toLowerCase();
  const items = state.saved.filter(s => s.ssid.toLowerCase().indexOf(q) >= 0);

  if (!items.length) {
    list.innerHTML = '<div class="empty">' + esc(t('saved.empty')) + '</div>';
    return;
  }

  const changed = items.filter(s => s.changed);
  let banner = '';
  if (changed.length) {
    banner = ''
      + '<div style="padding:12px 16px;background:#fff8e1;color:#0a0a0a;'
      + 'border-bottom:2px solid var(--warn);font-size:12px;'
      + 'letter-spacing:0.05em">'
      + '⚠  <strong>' + esc(t('saved.changed_banner')) + '</strong> — '
      + changed.length + ' ' + esc(t('saved.networks_word'))
      + ' : ' + changed.map(c => '« ' + esc(c.ssid) + ' »').join(', ')
      + '</div>';
  }

  list.innerHTML = banner + items.map(s => {
    let pwdHtml;
    if (s.has_password) {
      const dots = new Array(Math.min(s.password.length, 16) + 1).join('•');
      pwdHtml = '<span class="pwd" data-reveal data-pwd="'
              + esc(s.password) + '">' + dots + '</span>';
    } else {
      pwdHtml = '<span class="pwd empty">'
              + esc(t('saved.no_password')) + '</span>';
    }

    const dis = s.has_password ? '' : ' disabled';
    const cls = s.changed ? 'changed' : '';

    let meta = s.has_password
      ? t('saved.password_saved')
      : t('saved.open_network');
    if (s.changed) meta = '⚠  ' + t('saved.changed_banner');

    return ''
      + '<div class="item ' + cls + '">'
      +   '<div>'
      +     '<div class="ssid">' + esc(s.ssid) + '</div>'
      +     '<div class="meta">' + esc(meta) + '</div>'
      +     '<div style="margin-top:10px">' + pwdHtml + '</div>'
      +   '</div>'
      +   '<span class="actions">'
      +     '<button data-copy="' + esc(s.password) + '"' + dis + '>'
      +       esc(t('btn.copy')) + '</button>'
      +     '<button data-qr="' + esc(s.ssid) + '"' + dis + '>'
      +       esc(t('btn.qr')) + '</button>'
      +   '</span>'
      + '</div>';
  }).join('');

  // Reveal
  list.querySelectorAll('[data-reveal]').forEach(el => {
    el.addEventListener('click', () => {
      const real = el.dataset.pwd;
      const on = el.classList.toggle('revealed');
      el.textContent = on
        ? real
        : new Array(Math.min(real.length, 16) + 1).join('•');
    });
  });

  // Copy
  list.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', () => {
      navigator.clipboard.writeText(btn.dataset.copy)
        .then(() => toast(t('toast.copied')))
        .catch(() => toast(t('toast.copy_failed'), true));
    });
  });

  // QR
  list.querySelectorAll('[data-qr]').forEach(btn => {
    btn.addEventListener('click', () => showQR(btn.dataset.qr));
  });
}


/* ==========================================================
                    TAB HISTORY
   ========================================================== */
async function loadHistory(force = false) {
  const list = $('#history-list');
  if (!list) return;

  if (!state.history.changes.length && !state.history.logs.length) {
    const cached = CacheManager.get(CK.HISTORY);
    if (cached && cached.changes) {
      state.history = cached;
      renderHistory();
    } else {
      list.innerHTML = '<div class="empty">'
                    + esc(t('common.loading')) + '</div>';
    }
  }

  try {
    const data = await CacheManager.fetch(
      CK.HISTORY,
      async () => {
        const changes = await api('/api/history');
        const logs    = await api('/api/logs?limit=200');
        return { changes, logs };
      },
      TTL.HISTORY
    );

    if (force) CacheManager.set(CK.HISTORY, data, TTL.HISTORY);

    state.history = data;
    renderHistory();
  } catch (e) {
    if (!state.history.changes.length) {
      list.innerHTML = ''
        + '<div class="empty err">' + esc(t('common.error')) + ' : '
        + esc(e.message)
        + '<br><br><button class="btn" onclick="loadHistory(true)">'
        + esc(t('btn.retry')) + '</button></div>';
    }
  }
}

function renderHistory() {
  const list = $('#history-list');
  if (!list) return;
  const filter = ($('#history-filter')?.value || 'all');

  const events = [];

  if (filter === 'all' || filter === 'changes') {
    (state.history.changes || []).forEach(c => {
      events.push({
        type: 'change', ssid: c.ssid, ts: c.changed_at,
        old: c.previous_password || '', nw: c.password || '',
      });
    });
  }

  if (filter === 'all' || filter === 'connections') {
    (state.history.logs || []).forEach(l => {
      events.push({
        type: l.action === 'disconnect' ? 'disconnect' : 'connect',
        ssid: l.ssid, ts: l.timestamp,
        success: !!l.success, message: l.message || '',
      });
    });
  }

  if (!events.length) {
    list.innerHTML = '<div class="empty">' + esc(t('history.empty')) + '</div>';
    return;
  }

  events.sort((a, b) => (b.ts || '').localeCompare(a.ts || ''));

  const groups = {};
  events.forEach(ev => {
    const k = dateKey(ev.ts);
    if (!groups[k]) groups[k] = [];
    groups[k].push(ev);
  });

  let html = '';
  Object.keys(groups).sort().reverse().forEach(day => {
    html += '<div class="history-day">'
          + esc(fmtDateOnly(groups[day][0].ts)) + '</div>';
    groups[day].forEach(ev => { html += renderHistoryRow(ev); });
  });

  list.innerHTML = html;
}

function renderHistoryRow(ev) {
  const timeStr = fmtDateTime(ev.ts);
  if (ev.type === 'change') {
    return ''
      + '<div class="hist-row" style="box-shadow:inset 4px 0 0 var(--warn)">'
      +   '<div class="hist-head">'
      +     '<span class="hist-ssid">' + esc(ev.ssid) + '</span>'
      +     '<span class="hist-time">' + esc(timeStr) + '</span>'
      +   '</div>'
      +   '<div class="hist-detail">'
      +     '<span>🔑 ' + esc(t('history.changed')) + '</span>'
      +     (ev.old ? '<span>' + esc(t('history.previous')) + ' : '
                + '<code class="pwd-old">' + esc(ev.old) + '</code></span>' : '')
      +     (ev.nw  ? '<span>' + esc(t('history.new')) + ' : '
                + '<code class="pwd-new">' + esc(ev.nw) + '</code></span>' : '')
      +   '</div>'
      + '</div>';
  }

  const ok = ev.success;
  const col = ok ? 'var(--ok)' : 'var(--danger)';
  const label = ev.type === 'disconnect'
    ? t('history.disconnect') : t('history.connect');
  const status = ok ? t('history.success') : t('history.failed');

  return ''
    + '<div class="hist-row" style="box-shadow:inset 4px 0 0 ' + col + '">'
    +   '<div class="hist-head">'
    +     '<span class="hist-ssid">' + esc(ev.ssid) + '</span>'
    +     '<span class="hist-time">' + esc(timeStr) + '</span>'
    +   '</div>'
    +   '<div class="hist-detail">'
    +     '<span>' + (ok ? '✓' : '✗') + ' ' + esc(label) + ' — '
    +       esc(status) + '</span>'
    +     (ev.message ? '<span>' + esc(ev.message.slice(0, 120)) + '</span>' : '')
    +   '</div>'
    + '</div>';
}

async function clearHistory() {
  if (!confirm(t('history.confirm_clear'))) return;
  try {
    await api('/api/history', { method: 'DELETE' });
    CacheManager.invalidate(CK.HISTORY);
    state.history = { changes: [], logs: [] };
    toast(t('history.cleared'));
    loadHistory(true);
  } catch (e) {
    toast(t('common.error') + ' : ' + e.message, true);
  }
}


/* ==========================================================
                    TAB STATS
   ========================================================== */
async function loadStats(force = false) {
  const box = $('#stats-content');
  if (!box) return;

  if (!state.stats) {
    const cached = CacheManager.get(CK.STATS);
    if (cached) {
      state.stats = cached;
      renderStats();
    } else {
      box.innerHTML = '<div class="empty">' + esc(t('common.loading')) + '</div>';
    }
  }

  try {
    const stats = await CacheManager.fetch(
      CK.STATS, () => api('/api/stats'), TTL.STATS);
    if (force) CacheManager.set(CK.STATS, stats, TTL.STATS);
    state.stats = stats;
    renderStats();
  } catch (e) {
    if (!state.stats) {
      box.innerHTML = ''
        + '<div class="empty err">' + esc(t('common.error')) + ' : '
        + esc(e.message)
        + '<br><br><button class="btn" onclick="loadStats(true)">'
        + esc(t('btn.retry')) + '</button></div>';
    }
  }
}

function statCard(label, value, sub, cls) {
  return ''
    + '<div class="stat-card ' + cls + '">'
    +   '<div class="stat-label">' + esc(label) + '</div>'
    +   '<div class="stat-value">' + esc(String(value)) + '</div>'
    +   (sub ? '<div class="stat-sub">' + esc(sub) + '</div>' : '')
    + '</div>';
}

function renderStats() {
  const box = $('#stats-content');
  if (!box) return;
  const s = state.stats;
  if (!s) {
    box.innerHTML = '<div class="empty">' + esc(t('common.loading')) + '</div>';
    return;
  }

  const successPct = s.connections > 0
    ? Math.round(100 * s.connections_ok / s.connections) : 0;

  let html = '';

  html += '<div class="stats-grid">';
  html += statCard(t('stats.total_scans'), s.total_scans,
                   t('stats.sub_records'), 'c-blue');
  html += statCard(t('stats.known'), s.known_networks,
                   t('stats.sub_networks'), 'c-green');
  html += statCard(t('stats.changes'), s.password_changes,
                   t('stats.sub_records'), 'c-orange');
  html += statCard(t('stats.connections'), s.connections,
                   t('stats.sub_attempts'), 'c-purple');
  html += statCard(t('stats.favorites'), s.favorites || 0, '', 'c-red');
  html += '</div>';

  html += '<div class="stats-section">';
  html += '<h3>' + esc(t('stats.recent_scans')) + '</h3>';
  const scans = (s.recent_scans || []).slice().reverse();
  if (scans.length) {
    const max = Math.max(...scans.map(x => x.network_count), 1);
    html += '<div class="bar-chart">';
    scans.forEach(sc => {
      const pct = Math.round(100 * sc.network_count / max);
      const label = (sc.timestamp || '').slice(11, 16);
      html += '<div class="bar-col">'
            +   '<div class="bar-val">' + sc.network_count + '</div>'
            +   '<div class="bar-fill" style="height:' + pct + '%"></div>'
            +   '<div class="bar-label">' + esc(label) + '</div>'
            + '</div>';
    });
    html += '</div>';
  } else {
    html += '<div style="color:var(--muted);font-size:12px">'
          + esc(t('stats.no_data')) + '</div>';
  }
  html += '</div>';

  html += '<div class="stats-section">';
  html += '<h3>' + esc(t('stats.band_dist')) + '</h3>';
  const last = s.last_scan || { '2.4 GHz': 0, '5 GHz': 0, '6 GHz': 0 };
  const totalBands = (last['2.4 GHz'] || 0) + (last['5 GHz'] || 0)
                   + (last['6 GHz'] || 0);
  if (totalBands > 0) {
    html += '<div class="band-dist">';
    ['2.4 GHz', '5 GHz', '6 GHz'].forEach(b => {
      const n = last[b] || 0;
      if (!n) return;
      const cls = b.indexOf('2.4') >= 0 ? 'b24'
                : b.indexOf('6') >= 0 ? 'b6' : 'b5';
      const pct = Math.round(100 * n / totalBands);
      html += '<div class="band-seg ' + cls + '" style="flex-grow:' + n + '">'
            + (pct >= 8 ? n + ' · ' + pct + '%' : n)
            + '</div>';
    });
    html += '</div>';
    html += '<div class="band-legend">';
    ['2.4 GHz', '5 GHz', '6 GHz'].forEach(b => {
      const n = last[b] || 0;
      if (!n) return;
      const color = b.indexOf('2.4') >= 0 ? 'var(--b24)'
                  : b.indexOf('6') >= 0 ? 'var(--b6)' : 'var(--b5)';
      html += '<span><i style="background:' + color + '"></i>'
            + esc(b) + ' : ' + n + '</span>';
    });
    html += '</div>';
  } else {
    html += '<div style="color:var(--muted);font-size:12px">'
          + esc(t('stats.no_data')) + '</div>';
  }
  html += '</div>';

  html += '<div class="stats-section">';
  html += '<h3>' + esc(t('stats.top_networks')) + '</h3>';
  const top = s.top_networks || [];
  if (top.length) {
    top.forEach(x => {
      html += '<div class="hbar-row">'
            +   '<div class="hbar-name">' + esc(x.ssid) + '</div>'
            +   '<div class="hbar-count">' + x.count + '×</div>'
            + '</div>';
    });
  } else {
    html += '<div style="color:var(--muted);font-size:12px">'
          + esc(t('stats.no_data')) + '</div>';
  }
  html += '</div>';

  html += '<div class="stats-section">';
  html += '<h3>' + esc(t('stats.success_rate')) + '</h3>';
  const col = successPct >= 75 ? 'var(--ok)'
            : successPct >= 50 ? 'var(--warn)' : 'var(--danger)';
  html += '<div class="success-rate">'
        +   '<div class="success-bar">'
        +     '<div class="success-fill" style="width:' + successPct + '%">'
        +     '</div>'
        +   '</div>'
        +   '<div class="success-pct" style="color:' + col + '">'
        +     successPct + '%'
        +   '</div>'
        + '</div>'
        + '<div style="margin-top:10px;font-size:11px;color:var(--muted)">'
        +   s.connections_ok + ' / ' + s.connections + ' '
        +   esc(t('stats.sub_attempts'))
        + '</div>';
  html += '</div>';

  box.innerHTML = html;
}


/* ==========================================================
                    TAB SHARE
   ========================================================== */
async function loadShare() {
  const box = $('#share-content');
  if (!box) return;
  box.innerHTML = '<div class="empty">' + esc(t('common.loading')) + '</div>';
  try {
    const info = await api('/api/share-info');
    box.innerHTML = ''
      + '<div class="qr-panel">'
      +   '<h2>' + esc(t('share.open_phone')) + '</h2>'
      +   '<img src="/api/share-qr" alt="QR">'
      +   '<div class="url-line">' + esc(info.url) + '</div>'
      +   '<button class="btn-copy" id="copy-share-url">'
      +     esc(t('share.copy_url')) + '</button>'
      +   '<div class="hint">' + t('share.hint') + '<br>'
      +     esc(t('share.token_hint')) + '</div>'
      + '</div>';

    const copyBtn = document.getElementById('copy-share-url');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(info.url)
          .then(() => toast(t('toast.copied')))
          .catch(() => toast(t('toast.copy_failed'), true));
      });
    }
  } catch (e) {
    box.innerHTML = ''
      + '<div class="empty err">' + esc(t('common.error')) + ' : '
      + esc(e.message)
      + '<br><br><button class="btn" onclick="loadShare()">'
      + esc(t('btn.retry')) + '</button></div>';
  }
}


/* ==========================================================
                     MODALES
   ========================================================== */
function promptPassword(ssid) {
  return new Promise(resolve => {
    const bg = document.createElement('div');
    bg.className = 'modal-bg';
    bg.innerHTML = ''
      + '<div class="modal">'
      +   '<h2>' + esc(t('modal.pwd_title')) + '</h2>'
      +   '<div class="body">'
      +     '<p>' + esc(t('modal.pwd_network')) + ' &middot; <strong>'
      +       esc(ssid) + '</strong></p>'
      +     '<input type="password" id="pw" autocomplete="off" autofocus>'
      +   '</div>'
      +   '<div class="foot">'
      +     '<button data-act="cancel">' + esc(t('btn.cancel')) + '</button>'
      +     '<button data-act="ok" class="primary">'
      +       esc(t('btn.connect')) + '</button>'
      +   '</div>'
      + '</div>';
    document.body.appendChild(bg);

    const inp = bg.querySelector('#pw');
    inp.focus();

    const close = val => { bg.remove(); resolve(val); };
    bg.querySelector('[data-act="cancel"]').onclick = () => close(null);
    bg.querySelector('[data-act="ok"]').onclick     = () => close(inp.value);
    inp.addEventListener('keydown', e => {
      if (e.key === 'Enter')  close(inp.value);
      if (e.key === 'Escape') close(null);
    });
    bg.addEventListener('click', e => { if (e.target === bg) close(null); });
  });
}

function showQR(ssid) {
  const bg = document.createElement('div');
  bg.className = 'modal-bg';
  bg.innerHTML = ''
    + '<div class="modal" style="max-width:520px">'
    +   '<h2>' + esc(t('modal.qr_share')) + ' ' + esc(ssid) + '</h2>'
    +   '<div class="body">'
    +     '<div class="qr-panel">'
    +       '<img src="/api/qr/' + encodeURIComponent(ssid) + '" alt="QR">'
    +       '<div class="hint">' + t('modal.qr_hint') + '</div>'
    +     '</div>'
    +   '</div>'
    +   '<div class="foot">'
    +     '<button data-act="close" class="primary">'
    +       esc(t('btn.close')) + '</button>'
    +   '</div>'
    + '</div>';
  document.body.appendChild(bg);

  bg.querySelector('[data-act="close"]').onclick = () => bg.remove();
  bg.addEventListener('click', e => { if (e.target === bg) bg.remove(); });
}

async function showDiagnostics() {
  let diag;
  try {
    diag = await CacheManager.fetch(
      CK.DIAG, () => api('/api/diagnostics'), TTL.DIAG);
  } catch (e) {
    toast(t('toast.diag_unavailable') + e.message, true);
    return;
  }

  const rows = [
    [t('diag.os'),       diag.os || '?'],
    [t('diag.netsh'),    diag.netsh    === null ? '—'
                          : (diag.netsh ? t('diag.ok') : t('diag.missing'))],
    [t('diag.nmcli'),    diag.nmcli    === null ? '—'
                          : (diag.nmcli ? t('diag.ok') : t('diag.missing'))],
    [t('diag.airport'),  diag.airport  === null ? '—'
                          : (diag.airport ? t('diag.ok') : t('diag.missing'))],
    [t('diag.adapter'),  diag.adapter_active ? t('common.yes') : t('common.no')],
    [t('diag.location'), diag.location_service === null ? '—'
                          : (diag.location_service ? t('diag.ok') : t('diag.disabled'))],
    [t('diag.networks'), diag.networks_visible !== undefined
                          ? diag.networks_visible : '?'],
  ];

  const rowsHtml = rows.map(([k, v]) =>
    '<div style="display:flex;justify-content:space-between;'
    + 'padding:8px 0;border-bottom:1px solid var(--muted)">'
    + '<strong style="letter-spacing:0.1em">' + esc(k) + '</strong>'
    + '<span>' + esc(String(v)) + '</span>'
    + '</div>'
  ).join('');

  const bg = document.createElement('div');
  bg.className = 'modal-bg';
  bg.innerHTML = ''
    + '<div class="modal" style="max-width:560px">'
    +   '<h2>' + esc(t('modal.diag_title')) + '</h2>'
    +   '<div class="body">'
    +     '<div style="text-transform:none;letter-spacing:0">' + rowsHtml + '</div>'
    +     (diag.error
          ? '<div style="margin-top:16px;padding:12px;'
            + 'border:2px solid var(--danger);background:#ffe0e0;color:#0a0a0a;'
            + 'text-transform:none;letter-spacing:0;white-space:pre-wrap">'
            + esc(diag.error) + '</div>'
          : '')
    +     (diag.sample_output
          ? '<details style="margin-top:16px">'
            + '<summary style="cursor:pointer;text-transform:uppercase;'
            + 'letter-spacing:0.15em;font-size:11px;font-weight:700">'
            + esc(t('diag.raw')) + '</summary>'
            + '<pre style="margin-top:10px;padding:10px;background:#efeee7;'
            + 'color:#0a0a0a;border:1.5px solid var(--fg);overflow:auto;'
            + 'max-height:200px;font-size:11px;text-transform:none;'
            + 'letter-spacing:0">' + esc(diag.sample_output) + '</pre>'
            + '</details>'
          : '')
    +   '</div>'
    +   '<div class="foot">'
    +     '<button data-act="close" class="primary">'
    +       esc(t('btn.close')) + '</button>'
    +   '</div>'
    + '</div>';

  document.body.appendChild(bg);
  bg.querySelector('[data-act="close"]').onclick = () => bg.remove();
  bg.addEventListener('click', e => { if (e.target === bg) bg.remove(); });
}


/* ==========================================================
                EXPORT PDF
   ========================================================== */
async function exportPDF() {
  const btn = document.getElementById('btn-export-pdf');
  if (btn) { btn.disabled = true; btn.textContent = '⏳'; }
  try {
    const r = await fetch('/api/export/pdf');
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-');
    a.download = 'wifi-dashboard-' + stamp + '.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    toast(t('toast.exported'));
  } catch (e) {
    toast('Erreur export : ' + e.message, true);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '📤 <span data-i18n="btn.export_pdf">'
                    + esc(t('btn.export_pdf')) + '</span>';
    }
  }
}


/* ==========================================================
                       BOOT
   ========================================================== */
window.loadScan        = loadScan;
window.loadSaved       = loadSaved;
window.loadHistory     = loadHistory;
window.loadStats       = loadStats;
window.loadShare       = loadShare;
window.showDiagnostics = showDiagnostics;
window.switchTab       = switchTab;
window.exportPDF       = exportPDF;

document.addEventListener('DOMContentLoaded', () => {
  // ---- Thème
  THEME.init();
  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', () => THEME.cycle());

  // ---- Langue
  currentLang = MEM.get('lang', 'fr');
  const langSel = $('#lang-switch');
  if (langSel) {
    langSel.value = currentLang;
    langSel.addEventListener('change', e => setLang(e.target.value));
  }
  applyI18n();

  // ---- Injection du badge "dernière MAJ" dans SAVED
  const savedToolbar = document.querySelector('#tab-saved .toolbar');
  if (savedToolbar && !document.getElementById('saved-updated')) {
    const badge = document.createElement('span');
    badge.id = 'saved-updated';
    badge.className = 'updated-badge';
    badge.textContent = '';
    const reloadBtn = savedToolbar.querySelector('.btn');
    if (reloadBtn) savedToolbar.insertBefore(badge, reloadBtn);
    else savedToolbar.appendChild(badge);
  }

  // ---- Notifications (demande une fois)
  if (('Notification' in window)
      && Notification.permission === 'default'
      && MEM.get('notif_asked', false) === false) {
    setTimeout(() => {
      MEM.set('notif_asked', true);
      const prompt = currentLang === 'fr'
        ? 'Activer les notifications pour être alerté des changements de mot de passe Wi-Fi ?'
        : 'Enable notifications to be alerted of Wi-Fi password changes?';
      if (confirm(prompt)) NOTIF.enable();
    }, 3000);
  }

  // ---- Boutons
  const btnScan    = $('#btn-scan');
  const btnSaved   = $('#btn-saved');
  const btnHistory = $('#btn-history');
  const btnStats   = $('#btn-stats');
  const btnClear   = $('#btn-history-clear');
  const btnPdf     = $('#btn-export-pdf');

  if (btnScan)    btnScan.addEventListener('click', () => loadScan(true));
  if (btnSaved)   btnSaved.addEventListener('click', () => loadSaved(true));
  if (btnHistory) btnHistory.addEventListener('click', () => loadHistory(true));
  if (btnStats)   btnStats.addEventListener('click', () => loadStats(true));
  if (btnClear)   btnClear.addEventListener('click', clearHistory);
  if (btnPdf)     btnPdf.addEventListener('click', exportPDF);

  // ---- Filtres
  const s1 = $('#search');
  const s2 = $('#search-saved');
  const hf = $('#history-filter');

  if (s1) s1.addEventListener('input', renderScan);
  if (s2) s2.addEventListener('input', renderSaved);
  if (hf) hf.addEventListener('change', renderHistory);

  const sq = MEM.get('search', '');
  if (sq && s1) s1.value = sq;
  const sqs = MEM.get('searchSaved', '');
  if (sqs && s2) s2.value = sqs;

  if (s1) s1.addEventListener('input',
    e => MEM.set('search', e.target.value));
  if (s2) s2.addEventListener('input',
    e => MEM.set('searchSaved', e.target.value));

  // ---- Navigation
  $$('nav button').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });

  // ---- Délégation liste scan
  const scanList = $('#scan-list');
  if (scanList) {
    scanList.addEventListener('click', e => {
      const btn = e.target.closest('button[data-action]');
      if (!btn) return;
      if (btn.dataset.action === 'disconnect') doDisconnect();
      else if (btn.dataset.action === 'connect') {
        const net = state.scan.find(n => n.ssid === btn.dataset.ssid);
        if (net) doConnect(net);
      }
    });
  }

  // ---- Onglet initial
  switchTab(MEM.get('activeTab', 'scan'));

  // ---- Journal du cache en console (utile pour debug)
  console.log('[WifiManager] Cache:', CacheManager.stats());
});