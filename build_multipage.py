#!/usr/bin/env python3
"""
Builds uk.html, schengen.html, and index.html from the existing bundle.
"""
import json, base64, gzip, re, os

PROMO_CODES = [
    "1BC8BO99","XSXPA5S6","GYYHMKDL","1FL4J218","BG75BX8M","1APDNR8A","01UYIY5S",
    "GETQ2CJC","8R02U4F8","NMI544QI","Z20F02YF","TCN96F2B","5WRTJCDA","CFCS67U0",
    "XV44AZCL","AEAA6CPF","7HB296TT","0LMEH0JQ","0TQ9H4DE","UIMJY7X9","Z9FHW1IW",
    "9NLOATHO","SZ7N356G","XPQ1XXM5","ZE8LLTOL","FPI2LBBS","F7KBOTS6","QLP2SF23",
    "U1K8J8VR","Q1WRNMM5",
]

# ─── helpers ─────────────────────────────────────────────────────────────────

def pack(text: str) -> str:
    compressed = gzip.compress(text.encode('utf-8'), compresslevel=9)
    return base64.b64encode(compressed).decode('ascii')

def pack_binary(path: str) -> str:
    with open(path, 'rb') as f:
        data = f.read()
    compressed = gzip.compress(data, compresslevel=9)
    return base64.b64encode(compressed).decode('ascii')

def unpack(b64: str) -> str:
    data = base64.b64decode(b64)
    try:
        return gzip.decompress(data).decode('utf-8')
    except Exception:
        return data.decode('utf-8')

def load_bundle(path: str):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    mline = lines[176]
    start = mline.index('>') + 1
    end   = mline.rindex('<')
    manifest = json.loads(mline[start:end])
    return lines, manifest

def write_bundle(lines, manifest, out_path: str, title: str, *,
                 page_js: str = '', ext_resources=None, favicon_uuid=None):
    """Serialize manifest back and write the output HTML file."""
    import copy
    new_lines = copy.copy(lines)

    # Update manifest line
    mline_prefix = lines[176][:lines[176].index('>')+1]
    mline_suffix = lines[176][lines[176].rindex('<'):]
    new_lines[176] = mline_prefix + json.dumps(manifest, ensure_ascii=False) + mline_suffix

    # Update ext_resources line (line 179)
    if ext_resources is not None:
        new_lines[179] = json.dumps(ext_resources, ensure_ascii=False) + '\n'

    # Update template (line 182) – re-encode with </script> escaping
    tline = lines[182]
    tstart = tline.index('>') + 1
    tend   = tline.rindex('<')
    raw_json = tline[tstart:tend]
    template_str = json.loads(raw_json)

    # Inject favicon link in <head>
    if favicon_uuid:
        favicon_link = f'<link rel="icon" type="image/png" href="{favicon_uuid}">'
        template_str = template_str.replace('</head>', favicon_link + '</head>', 1)

    # Inject optional page-level JS into template
    if page_js:
        template_str = template_str.replace('</body>', page_js + '</body>')

    new_tline = (
        tline[:tstart]
        + json.dumps(template_str, ensure_ascii=False).replace('</', '<\\/')
        + tline[tend:]
    )
    new_lines[182] = new_tline

    # Update <title>
    result = ''.join(new_lines)
    result = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', result)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f'Written: {out_path}')

# ─── asset UUIDs ─────────────────────────────────────────────────────────────

UUID_WORDMARK    = '60627151-0cab-4b34-b9d9-9c81934b6a67'
UUID_APP         = '774abb2e-b7d0-47e2-9652-6e2780b11610'
UUID_HEADER      = '4066f641-663c-423e-bcee-9f971347a05e'
UUID_FOOTER      = 'f19335ce-1355-4d50-810d-a16b9efb659b'
UUID_HERO        = 'd8b75256-d161-4203-a466-a96659caa0e7'
UUID_ABOUT       = 'afcfe05f-048b-413e-9060-b183e4dc0578'
UUID_MAP         = '44cc7cd7-30a7-4ae5-b112-9943037e47e5'
UUID_SERVICES    = '072e9989-17ac-4031-8550-5080c67b7c43'
UUID_CONSULT     = '4ccf8b6e-9863-4ccf-8411-475d3a657df9'
UUID_BIGBEN      = '923327bd-a28b-4eec-adfa-df4133dd71ae'
UUID_TOWERBRIDGE = '64080515-00ba-4554-bd9e-a1347b6b18a4'
UUID_UKMAP       = 'a609367f-1eee-422f-a3fa-3ee82fdf5b36'

UUID_PARIS       = 'd28c82df-3882-4689-9cf7-ab9cfa7d14fa'
UUID_SCHENGENMAP = '3e88f09c-f95e-4559-a125-c0660ba0bcdc'
UUID_BANNER      = '767b4a73-49fb-40ab-a65a-f17933927039'
UUID_FAVICON     = '61e43071-9d06-41cd-b224-ad084081abca'

ASSET_DIR = '/home/user/ukvisa'

# ─── updated wordmark SVG ─────────────────────────────────────────────────────

WORDMARK_SVG = """<svg width="320" height="72" viewBox="0 0 320 72" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Royal Visas">
  <defs>
    <linearGradient id="wRoyal" x1="8" y1="12" x2="60" y2="60" gradientUnits="userSpaceOnUse">
      <stop stop-color="#3f2b5e"></stop>
      <stop offset="0.52" stop-color="#6f345c"></stop>
      <stop offset="1" stop-color="#956786"></stop>
    </linearGradient>
    <linearGradient id="wEdge" x1="12" y1="12" x2="32" y2="60" gradientUnits="userSpaceOnUse">
      <stop stop-color="#ffffff" stop-opacity="0.7"></stop>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.12"></stop>
    </linearGradient>
    <radialGradient id="wSpec" cx="0.32" cy="0.18" r="0.6">
      <stop stop-color="#ffffff" stop-opacity="0.5"></stop>
      <stop offset="0.5" stop-color="#ffffff" stop-opacity="0"></stop>
    </radialGradient>
  </defs>
  <rect x="8" y="12" width="48" height="48" rx="15" fill="url(#wRoyal)"></rect>
  <rect x="8.75" y="12.75" width="46.5" height="46.5" rx="14.25" fill="none" stroke="url(#wEdge)" stroke-width="1.2"></rect>
  <rect x="8" y="12" width="48" height="48" rx="15" fill="url(#wSpec)"></rect>
  <path d="M21 42 L19 30 L25.6 35.4 L32 27 L38.4 35.4 L45 30 L43 42 Z" fill="#ffffff" fill-opacity="0.96"></path>
  <rect x="21" y="44" width="22" height="3.2" rx="1.6" fill="#ffffff" fill-opacity="0.96"></rect>
  <text x="72" y="44" font-family="Geist, -apple-system, Segoe UI, sans-serif" font-size="23" font-weight="600" letter-spacing="-0.02em" fill="#ffffff">Royal Visas</text>
</svg>"""

# ─── component sources ───────────────────────────────────────────────────────

HEADER_JS = r"""/* global React */
function Header({ onOpenMenu, onOpenConsult }) {
  const { Button } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [scrolled, setScrolled] = React.useState(false);

  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const links = [
    { href: 'uk.html', label: 'Виза UK' },
    { href: 'schengen.html', label: 'Виза ЕС' },
  ];

  return (
    <header style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 50,
      transition: 'background .3s ease, box-shadow .3s ease, border-color .3s ease',
      background: scrolled ? 'var(--glass-fill-solid)' : 'transparent',
      backdropFilter: scrolled ? 'var(--glass-blur)' : 'none',
      WebkitBackdropFilter: scrolled ? 'var(--glass-blur)' : 'none',
      borderBottom: `1px solid ${scrolled ? 'var(--glass-edge-faint)' : 'transparent'}`,
      boxShadow: scrolled ? 'var(--elev-1)' : 'none',
    }}>
      <div className="rv-container" style={{ height: 72, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 24 }}>
        <a href="index.html" style={{ display: 'flex', alignItems: 'center', flex: 'none' }}>
          <img src={window.__rv('wordmark', 'assets/logo/royal-visa-wordmark.svg')} alt="Royal Visas" style={{ height: 40 }} />
        </a>

        {/* desktop nav */}
        <nav className="rv-desktop-nav" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          {links.map((l) => (
            <a key={l.href} href={l.href} style={{
              padding: '9px 16px', borderRadius: 'var(--r-pill)', fontSize: 'var(--t-sm)',
              fontWeight: 'var(--w-medium)', color: 'var(--text-body)', transition: 'color .15s, background .15s',
              textDecoration: 'none',
            }}
              onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--text-strong)'; e.currentTarget.style.background = 'var(--glass-fill)'; }}
              onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-body)'; e.currentTarget.style.background = 'transparent'; }}
            >{l.label}</a>
          ))}
          <div style={{ marginLeft: 10 }}>
            <Button variant="primary" size="sm" onClick={onOpenConsult}>Бесплатная консультация</Button>
          </div>
        </nav>

        {/* mobile hamburger */}
        <button className="rv-burger" aria-label="Меню" onClick={onOpenMenu} style={{
          display: 'none', width: 46, height: 46, flex: 'none', cursor: 'pointer',
          alignItems: 'center', justifyContent: 'center',
          borderRadius: 'var(--r-md)', background: 'var(--glass-fill)',
          border: '1px solid var(--glass-edge)', boxShadow: 'var(--glass-inner-soft)',
          backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
        }}>
          <i data-lucide="menu" style={{ width: 22, height: 22, color: 'var(--text-strong)' }}></i>
        </button>
      </div>
    </header>
  );
}

function MobileMenu({ open, onClose, onOpenConsult }) {
  const links = [
    { href: 'uk.html', label: 'Виза UK' },
    { href: 'schengen.html', label: 'Виза ЕС' },
  ];

  return (
    <div aria-hidden={!open} style={{
      position: 'fixed', inset: 0, zIndex: 60,
      pointerEvents: open ? 'auto' : 'none',
    }}>
      <div onClick={onClose} style={{
        position: 'absolute', inset: 0,
        background: 'rgba(8,7,13,0.62)',
        backdropFilter: open ? 'blur(28px) saturate(140%)' : 'blur(0px)',
        WebkitBackdropFilter: open ? 'blur(28px) saturate(140%)' : 'blur(0px)',
        opacity: open ? 1 : 0, transition: 'opacity .32s ease, backdrop-filter .32s ease',
      }} />

      <button aria-label="Закрыть" onClick={onClose} style={{
        position: 'absolute', top: 18, right: 18, zIndex: 2,
        width: 48, height: 48, cursor: 'pointer', borderRadius: '50%',
        background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
        backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        opacity: open ? 1 : 0, transition: 'opacity .3s ease',
      }}>
        <i data-lucide="x" style={{ width: 22, height: 22, color: 'var(--text-strong)' }}></i>
      </button>

      <nav style={{
        position: 'absolute', inset: 0, zIndex: 1,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        gap: 34, padding: 24,
        opacity: open ? 1 : 0,
        transform: open ? 'translateY(0)' : 'translateY(12px)',
        transition: 'opacity .32s ease, transform .4s cubic-bezier(.2,.8,.2,1)',
        pointerEvents: open ? 'auto' : 'none',
      }}>
        {links.map((l) => (
          <a key={l.href} href={l.href} onClick={onClose} style={{
            fontSize: 30, fontWeight: 'var(--w-semibold)', letterSpacing: '-0.02em',
            color: 'var(--text-strong)', textDecoration: 'none',
          }}>{l.label}</a>
        ))}
        <button onClick={() => { onClose(); setTimeout(onOpenConsult, 240); }} style={{
          marginTop: 8, padding: '16px 34px', borderRadius: 'var(--r-pill)',
          background: 'var(--grad-royal)', color: '#fff',
          fontSize: 19, fontWeight: 'var(--w-semibold)',
          border: '1px solid rgba(255,255,255,0.18)',
          boxShadow: 'var(--glow-mauve), var(--glass-inner)',
          cursor: 'pointer',
        }}>Бесплатная консультация</button>
      </nav>
    </div>
  );
}

Object.assign(window, { Header, MobileMenu });
"""

FOOTER_JS = r"""/* global React */
function Footer() {
  const links = [
    ['uk.html', 'Виза UK'],
    ['schengen.html', 'Виза ЕС'],
    ['#consult', 'Консультация'],
  ];
  return (
    <footer style={{ paddingTop: 56, paddingBottom: 40 }}>
      <div className="rv-container">
        <div style={{
          padding: 32, borderRadius: 'var(--r-2xl)',
          background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
          boxShadow: 'var(--glass-shadow), var(--glass-inner)',
        }}>
          <div className="rv-footer-top" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 24, flexWrap: 'wrap' }}>
            <img src={window.__rv('wordmark', 'assets/logo/royal-visa-wordmark.svg')} alt="Royal Visas" style={{ height: 40 }} />
            <nav style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {links.map(([h, l]) => (
                <a key={h} href={h}
                  onClick={h === '#consult' ? (e) => { e.preventDefault(); if (window.__openConsult) window.__openConsult(); } : undefined}
                  onMouseEnter={(e) => { e.currentTarget.style.background = 'var(--glass-fill)'; e.currentTarget.style.color = 'var(--text-strong)'; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--text-body)'; }}
                  style={{ padding: '8px 14px', borderRadius: 'var(--r-pill)', fontSize: 'var(--t-sm)', color: 'var(--text-body)', textDecoration: 'none', transition: 'background .15s, color .15s' }}>{l}</a>
              ))}
            </nav>
            <div style={{ display: 'flex', gap: 10 }}>
              {(() => {
                const MSG = 'Здравствуйте! Интересует виза';
                const contacts = [
                  ['message-circle', 'WhatsApp', 'https://wa.me/447342193316?text=' + encodeURIComponent(MSG)],
                  ['send', 'Telegram', 'https://t.me/paulderbush'],
                  ['mail', 'E-mail', 'mailto:paul.derbush@icloud.com?subject=' + encodeURIComponent('Виза') + '&body=' + encodeURIComponent(MSG)],
                ];
                return contacts.map(([ic, t, href]) => (
                  <a key={t} href={href} target="_blank" rel="noopener noreferrer" aria-label={t}
                    onMouseEnter={(e) => { e.currentTarget.style.background = 'var(--glass-fill-strong)'; e.currentTarget.style.borderColor = 'rgba(182,166,214,0.5)'; e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = 'var(--glow-violet), var(--glass-inner)'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.background = 'var(--glass-fill)'; e.currentTarget.style.borderColor = 'var(--glass-edge)'; e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = 'none'; }}
                    style={{
                    width: 42, height: 42, borderRadius: 'var(--r-md)', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
                    transition: 'background .18s, border-color .18s, transform .18s, box-shadow .18s',
                  }}>
                    <i data-lucide={ic} style={{ width: 18, height: 18, color: 'var(--accent-violet)' }}></i>
                  </a>
                ));
              })()}
            </div>
          </div>
          <div style={{ height: 1, background: 'var(--glass-edge-faint)', margin: '24px 0' }}></div>
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap' }}>
            <p style={{ margin: 0, fontSize: 'var(--t-sm)', color: 'var(--text-muted)', maxWidth: 560, lineHeight: 1.5 }}>
              Royal Visas&nbsp;- частный визовый сервис. Мы не являемся государственным
              органом и не аффилированы с UK Visas&nbsp;&amp; Immigration или посольствами. Решение по визе
              принимает консульство.
            </p>
            <p style={{ margin: 0, fontSize: 'var(--t-sm)', color: 'var(--ink-3)' }}>© 2026 Royal Visas</p>
          </div>
        </div>
      </div>
    </footer>
  );
}

Object.assign(window, { Footer });
"""

APP_JS = r"""/* global React */
function ConsultModal({ open, onClose }) {
  const TG_TOKEN = '8677081622:AAHAvOYbY50uCZnx9QimTXDO98CYJnMnvxA';
  const TG_CHAT_ID = '-5235367527';
  const VISA_LABEL = typeof window.__consultLabel === 'string' ? window.__consultLabel : '📋 Новая заявка - Royal Visas';
  const PROMO_DISCOUNT = 5000;
  const PROMO_CODES_LIST = typeof window.__promoCodes === 'object' ? window.__promoCodes : [];

  const { Button, Input, Switch } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [channel, setChannel] = React.useState('whatsapp');
  const [sent, setSent] = React.useState(false);
  const [name, setName] = React.useState('');
  const [contact, setContact] = React.useState('');
  const [promo, setPromo] = React.useState('');
  const [promoInfo, setPromoInfo] = React.useState(null);
  const [sending, setSending] = React.useState(false);
  const [error, setError] = React.useState('');
  const [opts, setOpts] = React.useState({ weekdays: false, hours: false, anytime: true, urgent: false });

  React.useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  React.useEffect(() => {
    if (open) document.body.style.overflow = 'hidden';
    else document.body.style.overflow = '';
    return () => { document.body.style.overflow = ''; };
  }, [open]);

  React.useEffect(() => {
    if (open && window.lucide) setTimeout(() => window.lucide.createIcons(), 30);
  }, [open]);

  const validatePromo = (code) => {
    if (!code || !code.trim()) return null;
    const upper = code.trim().toUpperCase();
    if (upper === 'KRISKISS') {
      return new Date() < new Date('2026-10-01')
        ? { valid: true, discount: PROMO_DISCOUNT }
        : { valid: false, msg: 'Промокод истёк' };
    }
    if (PROMO_CODES_LIST.includes(upper)) {
      try {
        const used = JSON.parse(localStorage.getItem('rv_used_promos') || '[]');
        if (used.includes(upper)) return { valid: false, msg: 'Этот промокод уже был использован' };
      } catch(e) {}
      return { valid: true, discount: PROMO_DISCOUNT };
    }
    return { valid: false, msg: 'Промокод не найден' };
  };

  const handlePromoChange = (e) => {
    const val = e.target.value;
    setPromo(val);
    if (!val.trim()) { setPromoInfo(null); return; }
    if (val.trim().length >= 6) setPromoInfo(validatePromo(val));
    else setPromoInfo(null);
  };

  const setOpt = (k, v) => setOpts((p) => {
    const next = { ...p, [k]: v };
    if (k === 'anytime' && v) { next.weekdays = false; next.hours = false; }
    if ((k === 'weekdays' || k === 'hours') && v) next.anytime = false;
    return next;
  });

  const submit = async (e) => {
    e.preventDefault();
    setError(''); setSending(true);
    try {
      const when = [];
      if (opts.weekdays) when.push('только будни');
      if (opts.hours) when.push('рабочие часы (до 18:00)');
      if (opts.anytime) when.push('в любое время');
      const promoResult = promo.trim() ? validatePromo(promo) : null;
      const promoLine = promoResult?.valid
        ? 'Промокод: ' + promo.trim().toUpperCase() + ' (-' + PROMO_DISCOUNT.toLocaleString('ru') + ' руб.)'
        : promo.trim() ? 'Промокод: ' + promo.trim() + ' (недействителен)' : null;
      const text = [
        VISA_LABEL,
        'Имя: ' + (name || '-'),
        'Канал: ' + (channel === 'whatsapp' ? 'WhatsApp' : 'Telegram'),
        'Контакт: ' + (contact || '-'),
        'Когда писать: ' + (when.join(', ') || '-'),
        promoLine,
        opts.urgent ? '⚡ Виза нужна СРОЧНО' : null,
      ].filter(Boolean).join('\n');
      const resp = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: TG_CHAT_ID, text }),
      });
      const jr = await resp.json();
      if (!jr.ok) throw new Error(jr.description || 'send failed');
      if (promoResult?.valid && promo.trim().toUpperCase() !== 'KRISKISS') {
        try {
          const used = JSON.parse(localStorage.getItem('rv_used_promos') || '[]');
          used.push(promo.trim().toUpperCase());
          localStorage.setItem('rv_used_promos', JSON.stringify(used));
        } catch(e) {}
      }
      setSent(true);
    } catch (err) {
      setError('Не удалось отправить заявку. Напишите нам напрямую в WhatsApp или Telegram - кнопки в подвале.');
    } finally {
      setSending(false);
    }
  };

  const switches = [
    { key: 'weekdays', label: 'Писать только в будние дни', icon: 'calendar-days' },
    { key: 'hours', label: 'Писать только в рабочие часы (до 18:00)', icon: 'clock' },
    { key: 'anytime', label: 'Писать в любое время', icon: 'infinity' },
    { key: 'urgent', label: 'Виза нужна срочно', icon: 'zap' },
  ];

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 200,
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20,
      pointerEvents: open ? 'auto' : 'none',
    }}>
      <div onClick={onClose} style={{
        position: 'absolute', inset: 0, background: 'rgba(8,7,13,0.65)',
        backdropFilter: open ? 'blur(24px) saturate(140%)' : 'blur(0)',
        WebkitBackdropFilter: open ? 'blur(24px) saturate(140%)' : 'blur(0)',
        opacity: open ? 1 : 0, transition: 'opacity .28s ease',
      }} />
      <div role="dialog" aria-modal="true" style={{
        position: 'relative', width: '100%', maxWidth: 960,
        maxHeight: '90vh', overflowY: 'auto',
        borderRadius: 'var(--r-2xl)',
        background: 'var(--glass-fill-strong)',
        border: '1px solid var(--glass-edge-strong)',
        backdropFilter: 'var(--glass-blur-heavy)', WebkitBackdropFilter: 'var(--glass-blur-heavy)',
        boxShadow: 'var(--elev-4), var(--glass-inner)',
        transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.97)',
        opacity: open ? 1 : 0,
        transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease',
      }}>
        <button aria-label="Закрыть" onClick={onClose} style={{
          position: 'absolute', top: 16, right: 16, zIndex: 10,
          width: 36, height: 36, cursor: 'pointer',
          borderRadius: 'var(--r-sm)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <i data-lucide="x" style={{ width: 18, height: 18, color: 'var(--text-strong)' }}></i>
        </button>

        <div style={{ padding: '32px 8px 8px' }}>
          <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 32px' }}>
            <span className="rv-eyebrow">Бесплатная консультация</span>
            <h2 style={{ fontSize: 'var(--t-h2)', marginTop: 14 }}>Оставьте заявку - ответим в мессенджере</h2>
            <p style={{ marginTop: 12, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
              Расскажем, какая виза подходит именно вам, и как быстро её получить.
            </p>
          </div>

          <div style={{ padding: 8 }}>
            <div className="rv-form-grid" style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: 8 }}>
              <div style={{ padding: 28 }}>
                {sent ? (
                  <div style={{ height: '100%', minHeight: 300, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: 14 }}>
                    <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'var(--success-soft)', border: '1px solid rgba(111,174,143,0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <i data-lucide="check" style={{ width: 30, height: 30, color: 'var(--success)' }}></i>
                    </div>
                    <h3 style={{ fontSize: 'var(--t-h3)' }}>Заявка отправлена</h3>
                    <p style={{ color: 'var(--text-muted)', maxWidth: 320 }}>Свяжемся с вами в {channel === 'whatsapp' ? 'WhatsApp' : 'Telegram'} в ближайшее время.</p>
                    <Button variant="ghost" size="sm" onClick={() => { setSent(false); setName(''); setContact(''); setPromo(''); setPromoInfo(null); }}>Отправить ещё одну</Button>
                  </div>
                ) : (
                  <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
                    <Input label="Имя" placeholder="Как к вам обращаться" required value={name} onChange={(e) => setName(e.target.value)} icon={<i data-lucide="user-round" style={{ width: 17, height: 17 }}></i>} />
                    <div>
                      <div style={{ fontSize: 'var(--t-sm)', fontWeight: 500, color: 'var(--text-body)', marginBottom: 8 }}>Куда вам написать</div>
                      <div style={{ display: 'flex', gap: 10 }}>
                        {['whatsapp', 'telegram'].map((ch) => (
                          <button key={ch} type="button" onClick={() => { setChannel(ch); setContact(''); setError(''); }} style={{
                            flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 9,
                            height: 48, cursor: 'pointer', borderRadius: 'var(--r-md)',
                            fontFamily: 'var(--font-sans)', fontSize: 'var(--t-body)', fontWeight: 600,
                            color: channel === ch ? '#fff' : 'var(--text-body)',
                            background: channel === ch ? 'var(--grad-twilight)' : 'var(--glass-fill)',
                            border: `1px solid ${channel === ch ? 'rgba(255,255,255,0.2)' : 'var(--glass-edge)'}`,
                            boxShadow: channel === ch ? 'var(--glow-steel), var(--glass-inner)' : 'var(--glass-inner-soft)',
                            backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                            transition: 'all .2s ease',
                          }}>
                            <i data-lucide={ch === 'whatsapp' ? 'message-circle' : 'send'} style={{ width: 19, height: 19 }}></i>
                            {ch === 'whatsapp' ? 'WhatsApp' : 'Telegram'}
                          </button>
                        ))}
                      </div>
                    </div>
                    {channel === 'whatsapp'
                      ? <Input key="wa" label="Номер телефона" type="tel" required value={contact} onChange={(e) => setContact(e.target.value)} placeholder="+7 900 000-00-00" icon={<i data-lucide="phone" style={{ width: 17, height: 17 }}></i>} />
                      : <Input key="tg" label="Ваш @никнейм" required value={contact} onChange={(e) => setContact(e.target.value)} placeholder="@username" icon={<i data-lucide="at-sign" style={{ width: 17, height: 17 }}></i>} />}
                    <div>
                      <Input label="Промокод (необязательно)" placeholder="Введите промокод" value={promo} onChange={handlePromoChange} icon={<i data-lucide="tag" style={{ width: 17, height: 17 }}></i>} />
                      {promoInfo && (
                        <div style={{ marginTop: 8, padding: '8px 12px', borderRadius: 'var(--r-md)', display: 'flex', alignItems: 'center', gap: 8, background: promoInfo.valid ? 'rgba(86,160,84,0.12)' : 'var(--danger-soft)', border: `1px solid ${promoInfo.valid ? 'rgba(86,160,84,0.3)' : 'rgba(201,122,130,0.35)'}` }}>
                          <i data-lucide={promoInfo.valid ? 'circle-check' : 'circle-x'} style={{ width: 15, height: 15, flex: 'none', color: promoInfo.valid ? 'var(--success)' : 'var(--danger)' }}></i>
                          <span style={{ fontSize: 'var(--t-sm)', color: 'var(--text-body)' }}>{promoInfo.valid ? 'Скидка 5 000 руб. применена' : promoInfo.msg}</span>
                        </div>
                      )}
                    </div>
                    {error && (
                      <div style={{ display: 'flex', gap: 9, alignItems: 'flex-start', padding: '12px 14px', borderRadius: 'var(--r-md)', background: 'var(--danger-soft)', border: '1px solid rgba(201,122,130,0.35)' }}>
                        <i data-lucide="triangle-alert" style={{ width: 17, height: 17, marginTop: 1, flex: 'none', color: 'var(--danger)' }}></i>
                        <span style={{ fontSize: 'var(--t-sm)', color: 'var(--text-body)', lineHeight: 1.45 }}>{error}</span>
                      </div>
                    )}
                    <div style={{ marginTop: 4 }}>
                      <Button type="submit" variant="primary" size="lg" fullWidth disabled={sending} iconRight={!sending && <i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>}>
                        {sending ? 'Отправляем...' : 'Отправить заявку'}
                      </Button>
                    </div>
                  </form>
                )}
              </div>

              <div style={{ padding: 28, borderRadius: 'var(--r-xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge-faint)' }}>
                <div style={{ fontSize: 'var(--t-sm)', fontWeight: 600, letterSpacing: 'var(--track-eyebrow)', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 18 }}>Когда удобно</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  {switches.map((s) => {
                    const on = opts[s.key];
                    return (
                      <div key={s.key} style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '12px 8px', borderRadius: 'var(--r-md)', background: on ? 'var(--glass-fill)' : 'transparent', transition: 'background .2s ease' }}>
                        <i data-lucide={s.icon} style={{ width: 18, height: 18, flex: 'none', color: on ? (s.key === 'urgent' ? 'var(--warning)' : 'var(--accent-violet)') : 'var(--ink-3)' }}></i>
                        <span style={{ flex: 1, fontSize: 'var(--t-body)', color: on ? 'var(--text-strong)' : 'var(--text-body)' }}>{s.label}</span>
                        <Switch checked={on} onChange={(v) => setOpt(s.key, v)} size="sm" accent={s.key === 'urgent' ? 'var(--grad-royal)' : 'var(--grad-twilight)'} />
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [consultOpen, setConsultOpen] = React.useState(false);

  const openConsult = React.useCallback(() => setConsultOpen(true), []);

  React.useEffect(() => {
    window.__openConsult = openConsult;
    return () => { delete window.__openConsult; };
  }, [openConsult]);

  React.useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });

  React.useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : '';
  }, [menuOpen]);

  return (
    <React.Fragment>
      <Header onOpenMenu={() => setMenuOpen(true)} onOpenConsult={openConsult} />
      <MobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} onOpenConsult={openConsult} />
      <ConsultModal open={consultOpen} onClose={() => setConsultOpen(false)} />
      <main>
        <Hero />
        <AboutVisa />
        <UKMap />
        <Services />
        <ConsultForm />
      </main>
      <Footer />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
setTimeout(() => window.lucide && window.lucide.createIcons(), 80);
"""

CONSULT_FORM_UK = r"""/* global React */
function ChannelButton({ active, icon, label, onClick }) {
  return (
    <button type="button" onClick={onClick} style={{
      flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 9,
      height: 48, cursor: 'pointer', borderRadius: 'var(--r-md)',
      fontFamily: 'var(--font-sans)', fontSize: 'var(--t-body)', fontWeight: 600,
      color: active ? '#fff' : 'var(--text-body)',
      background: active ? 'var(--grad-twilight)' : 'var(--glass-fill)',
      border: `1px solid ${active ? 'rgba(255,255,255,0.2)' : 'var(--glass-edge)'}`,
      boxShadow: active ? 'var(--glow-steel), var(--glass-inner)' : 'var(--glass-inner-soft)',
      backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
      transition: 'all .2s ease',
    }}>
      <i data-lucide={icon} style={{ width: 19, height: 19 }}></i>
      {label}
    </button>
  );
}

function ConsultForm() {
  const { Button, Input, Switch } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [channel, setChannel] = React.useState('whatsapp');
  const [sent, setSent] = React.useState(false);
  const [name, setName] = React.useState('');
  const [contact, setContact] = React.useState('');
  const [promo, setPromo] = React.useState('');
  const [promoInfo, setPromoInfo] = React.useState(null);
  const [sending, setSending] = React.useState(false);
  const [error, setError] = React.useState('');
  const [opts, setOpts] = React.useState({ weekdays: false, hours: false, anytime: true, urgent: false });

  const TG_TOKEN = '8677081622:AAHAvOYbY50uCZnx9QimTXDO98CYJnMnvxA';
  const TG_CHAT_ID = '-5235367527';
  const VISA_LABEL = '🇬🇧 Новая заявка - Royal Visas';
  const PROMO_DISCOUNT = 5000;
  const PROMO_CODES_LIST = __PROMO_CODES__;

  const validatePromo = (code) => {
    if (!code || !code.trim()) return null;
    const upper = code.trim().toUpperCase();
    if (upper === 'KRISKISS') {
      return new Date() < new Date('2026-10-01')
        ? { valid: true, discount: PROMO_DISCOUNT }
        : { valid: false, msg: 'Промокод истёк' };
    }
    if (PROMO_CODES_LIST.includes(upper)) {
      try {
        const used = JSON.parse(localStorage.getItem('rv_used_promos') || '[]');
        if (used.includes(upper)) return { valid: false, msg: 'Этот промокод уже был использован' };
      } catch(e) {}
      return { valid: true, discount: PROMO_DISCOUNT };
    }
    return { valid: false, msg: 'Промокод не найден' };
  };

  const handlePromoChange = (e) => {
    const val = e.target.value;
    setPromo(val);
    if (!val.trim()) { setPromoInfo(null); return; }
    if (val.trim().length >= 6) setPromoInfo(validatePromo(val));
    else setPromoInfo(null);
  };

  const resolveChatId = async () => {
    if (TG_CHAT_ID) return TG_CHAT_ID;
    const r = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/getUpdates');
    const j = await r.json();
    const ups = j.result || [];
    for (let i = ups.length - 1; i >= 0; i--) {
      const m = ups[i].message || ups[i].my_chat_member || ups[i].edited_message;
      if (m && m.chat && m.chat.id) return m.chat.id;
    }
    throw new Error('chat id not found');
  };

  const switchChannel = (c) => { setChannel(c); setContact(''); setError(''); };

  const submit = async (e) => {
    e.preventDefault();
    setError(''); setSending(true);
    try {
      const chatId = await resolveChatId();
      const when = [];
      if (opts.weekdays) when.push('только будни');
      if (opts.hours) when.push('рабочие часы (до 18:00)');
      if (opts.anytime) when.push('в любое время');
      const promoResult = promo.trim() ? validatePromo(promo) : null;
      const promoLine = promoResult?.valid
        ? 'Промокод: ' + promo.trim().toUpperCase() + ' (-' + PROMO_DISCOUNT.toLocaleString('ru') + ' руб.)'
        : promo.trim() ? 'Промокод: ' + promo.trim() + ' (недействителен)' : null;
      const text = [
        VISA_LABEL,
        'Имя: ' + (name || '-'),
        'Канал: ' + (channel === 'whatsapp' ? 'WhatsApp' : 'Telegram'),
        'Контакт: ' + (contact || '-'),
        'Когда писать: ' + (when.join(', ') || '-'),
        promoLine,
        opts.urgent ? '⚡ Виза нужна СРОЧНО' : null,
      ].filter(Boolean).join('\n');
      const resp = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text }),
      });
      const jr = await resp.json();
      if (!jr.ok) throw new Error(jr.description || 'send failed');
      if (promoResult?.valid && promo.trim().toUpperCase() !== 'KRISKISS') {
        try {
          const used = JSON.parse(localStorage.getItem('rv_used_promos') || '[]');
          used.push(promo.trim().toUpperCase());
          localStorage.setItem('rv_used_promos', JSON.stringify(used));
        } catch(e) {}
      }
      setSent(true);
    } catch (err) {
      setError('Не удалось отправить заявку. Напишите нам напрямую в WhatsApp или Telegram - кнопки в подвале.');
    } finally {
      setSending(false);
    }
  };

  const setOpt = (k, v) => setOpts((p) => {
    const next = { ...p, [k]: v };
    if (k === 'anytime' && v) { next.weekdays = false; next.hours = false; }
    if ((k === 'weekdays' || k === 'hours') && v) next.anytime = false;
    return next;
  });

  const switches = [
    { key: 'weekdays', label: 'Писать только в будние дни', icon: 'calendar-days' },
    { key: 'hours', label: 'Писать только в рабочие часы (до 18:00)', icon: 'clock' },
    { key: 'anytime', label: 'Писать в любое время', icon: 'infinity' },
    { key: 'urgent', label: 'Виза нужна срочно', icon: 'zap' },
  ];

  return (
    <section id="consult" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">Бесплатная консультация</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Оставьте заявку - ответим в мессенджере</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            Расскажем, какая виза подходит именно вам, и как быстро её получить.
          </p>
        </div>

        <div style={{
          maxWidth: 940, margin: '0 auto', padding: 8, borderRadius: 'var(--r-2xl)',
          background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
          boxShadow: 'var(--elev-3), var(--glass-inner)',
        }}>
          <div className="rv-form-grid" style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: 8 }}>
            <div style={{ padding: 28 }}>
              {sent ? (
                <div style={{ height: '100%', minHeight: 320, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: 14 }}>
                  <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'var(--success-soft)', border: '1px solid rgba(111,174,143,0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <i data-lucide="check" style={{ width: 30, height: 30, color: 'var(--success)' }}></i>
                  </div>
                  <h3 style={{ fontSize: 'var(--t-h3)' }}>Заявка отправлена</h3>
                  <p style={{ color: 'var(--text-muted)', maxWidth: 320 }}>Свяжемся с вами в {channel === 'whatsapp' ? 'WhatsApp' : 'Telegram'} в ближайшее время.</p>
                  <Button variant="ghost" size="sm" onClick={() => { setSent(false); setName(''); setContact(''); setPromo(''); setPromoInfo(null); }}>Отправить ещё одну</Button>
                </div>
              ) : (
                <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
                  <Input label="Имя" placeholder="Как к вам обращаться" required value={name} onChange={(e) => setName(e.target.value)} icon={<i data-lucide="user-round" style={{ width: 17, height: 17 }}></i>} />

                  <div>
                    <div style={{ fontSize: 'var(--t-sm)', fontWeight: 500, color: 'var(--text-body)', marginBottom: 8 }}>Куда вам написать</div>
                    <div style={{ display: 'flex', gap: 10 }}>
                      <ChannelButton active={channel === 'whatsapp'} icon="message-circle" label="WhatsApp" onClick={() => switchChannel('whatsapp')} />
                      <ChannelButton active={channel === 'telegram'} icon="send" label="Telegram" onClick={() => switchChannel('telegram')} />
                    </div>
                  </div>

                  {channel === 'whatsapp'
                    ? <Input key="wa" label="Номер телефона" type="tel" required value={contact} onChange={(e) => setContact(e.target.value)} placeholder="+7 900 000-00-00" icon={<i data-lucide="phone" style={{ width: 17, height: 17 }}></i>} />
                    : <Input key="tg" label="Ваш @никнейм" required value={contact} onChange={(e) => setContact(e.target.value)} placeholder="@username" icon={<i data-lucide="at-sign" style={{ width: 17, height: 17 }}></i>} />}

                  <div>
                    <Input
                      label="Промокод (необязательно)"
                      placeholder="Введите промокод"
                      value={promo}
                      onChange={handlePromoChange}
                      icon={<i data-lucide="tag" style={{ width: 17, height: 17 }}></i>}
                    />
                    {promoInfo && (
                      <div style={{
                        marginTop: 8, padding: '8px 12px', borderRadius: 'var(--r-md)',
                        display: 'flex', alignItems: 'center', gap: 8,
                        background: promoInfo.valid ? 'rgba(86,160,84,0.12)' : 'var(--danger-soft)',
                        border: `1px solid ${promoInfo.valid ? 'rgba(86,160,84,0.3)' : 'rgba(201,122,130,0.35)'}`,
                      }}>
                        <i data-lucide={promoInfo.valid ? 'circle-check' : 'circle-x'} style={{ width: 15, height: 15, flex: 'none', color: promoInfo.valid ? 'var(--success)' : 'var(--danger)' }}></i>
                        <span style={{ fontSize: 'var(--t-sm)', color: 'var(--text-body)' }}>
                          {promoInfo.valid ? 'Скидка 5 000 руб. применена' : promoInfo.msg}
                        </span>
                      </div>
                    )}
                  </div>

                  {error && (
                    <div style={{ display: 'flex', gap: 9, alignItems: 'flex-start', padding: '12px 14px', borderRadius: 'var(--r-md)', background: 'var(--danger-soft)', border: '1px solid rgba(201,122,130,0.35)' }}>
                      <i data-lucide="triangle-alert" style={{ width: 17, height: 17, marginTop: 1, flex: 'none', color: 'var(--danger)' }}></i>
                      <span style={{ fontSize: 'var(--t-sm)', color: 'var(--text-body)', lineHeight: 1.45 }}>{error}</span>
                    </div>
                  )}

                  <div style={{ marginTop: 4 }}>
                    <Button type="submit" variant="primary" size="lg" fullWidth disabled={sending} iconRight={!sending && <i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>}>
                      {sending ? 'Отправляем...' : 'Отправить заявку'}
                    </Button>
                  </div>
                </form>
              )}
            </div>

            <div style={{
              padding: 28, borderRadius: 'var(--r-xl)',
              background: 'var(--glass-fill)', border: '1px solid var(--glass-edge-faint)',
            }}>
              <div style={{ fontSize: 'var(--t-sm)', fontWeight: 600, letterSpacing: 'var(--track-eyebrow)', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 18 }}>
                Когда удобно
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {switches.map((s) => {
                  const on = opts[s.key];
                  return (
                    <div key={s.key} style={{
                      display: 'flex', alignItems: 'center', gap: 14, padding: '12px 8px',
                      borderRadius: 'var(--r-md)',
                      background: on ? 'var(--glass-fill)' : 'transparent',
                      transition: 'background .2s ease',
                    }}>
                      <i data-lucide={s.icon} style={{ width: 18, height: 18, flex: 'none', color: on ? (s.key === 'urgent' ? 'var(--warning)' : 'var(--accent-violet)') : 'var(--ink-3)' }}></i>
                      <span style={{ flex: 1, fontSize: 'var(--t-body)', color: on ? 'var(--text-strong)' : 'var(--text-body)' }}>{s.label}</span>
                      <Switch checked={on} onChange={(v) => setOpt(s.key, v)} size="sm"
                        accent={s.key === 'urgent' ? 'var(--grad-royal)' : 'var(--grad-twilight)'} />
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { ConsultForm });
"""

SERVICES_29990 = r"""/* global React */
const CONSULAR_FEES = [
  { label: 'Туристическая виза на 6 месяцев', price: '150 £' },
  { label: 'Туристическая виза на 2 года', price: '550 £' },
  { label: 'Туристическая виза на 5 лет', price: '980 £' },
  { label: 'Туристическая виза на 10 лет', price: '1250 £' },
];

function FeeLink({ onOpen }) {
  return (
    <button onClick={onOpen} style={{
      display: 'inline-flex', alignItems: 'center', gap: 5, padding: 0,
      background: 'none', border: 'none', cursor: 'pointer', font: 'inherit',
      color: 'var(--accent-sky)', fontWeight: 600,
      textDecoration: 'underline', textUnderlineOffset: 3, textDecorationColor: 'rgba(185,210,230,0.45)',
    }}>
      консульский сбор
      <i data-lucide="info" style={{ width: 14, height: 14 }}></i>
    </button>
  );
}

function FeeModal({ open, onClose }) {
  React.useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  return (
    <div aria-hidden={!open} style={{
      position: 'fixed', inset: 0, zIndex: 80,
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20,
      pointerEvents: open ? 'auto' : 'none',
    }}>
      <div onClick={onClose} style={{
        position: 'absolute', inset: 0, background: 'rgba(8,7,13,0.55)',
        backdropFilter: open ? 'blur(20px) saturate(140%)' : 'blur(0)',
        WebkitBackdropFilter: open ? 'blur(20px) saturate(140%)' : 'blur(0)',
        opacity: open ? 1 : 0, transition: 'opacity .28s ease, backdrop-filter .28s ease',
      }} />
      <div role="dialog" aria-modal="true" style={{
        position: 'relative', width: '100%', maxWidth: 480, padding: 28,
        borderRadius: 'var(--r-2xl)',
        background: 'var(--glass-fill-strong)',
        border: '1px solid var(--glass-edge-strong)',
        backdropFilter: 'var(--glass-blur-heavy)', WebkitBackdropFilter: 'var(--glass-blur-heavy)',
        boxShadow: 'var(--elev-4), var(--glass-inner)',
        transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.96)',
        opacity: open ? 1 : 0, transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease',
      }}>
        <span style={{ position: 'absolute', inset: 0, borderRadius: 'inherit', background: 'var(--glass-specular)', pointerEvents: 'none' }}></span>
        <button aria-label="Закрыть" onClick={onClose} style={{
          position: 'absolute', top: 16, right: 16, width: 36, height: 36, cursor: 'pointer',
          borderRadius: 'var(--r-sm)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <i data-lucide="x" style={{ width: 18, height: 18, color: 'var(--text-strong)' }}></i>
        </button>

        <div style={{ position: 'relative' }}>
          <div style={{
            width: 46, height: 46, borderRadius: 'var(--r-md)', marginBottom: 16,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'var(--glass-tint-sky)', border: '1px solid var(--glass-edge)',
          }}>
            <i data-lucide="credit-card" style={{ width: 22, height: 22, color: 'var(--accent-sky)' }}></i>
          </div>
          <p style={{ margin: 0, fontSize: 'var(--t-lg)', color: 'var(--text-strong)', lineHeight: 1.45, fontWeight: 500 }}>
            Консульский сбор оплачивается зарубежной банковской картой. Если у вас такой нет - мы поможем оплатить.
          </p>

          <div style={{ marginTop: 22, display: 'flex', flexDirection: 'column', gap: 2 }}>
            {CONSULAR_FEES.map((f, i) => (
              <div key={f.label} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16,
                padding: '14px 4px',
                borderTop: i === 0 ? 'none' : '1px solid var(--glass-edge-faint)',
              }}>
                <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)' }}>{f.label}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--t-lg)', fontWeight: 600, color: 'var(--text-strong)', whiteSpace: 'nowrap' }}>{f.price}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function TariffCard({ data, featured, onOpenFee }) {
  const { Button, Badge } = window.RoyalVisaUKDesignSystem_ccc97c;
  return (
    <div style={{
      position: 'relative', padding: 30, borderRadius: 'var(--r-xl)',
      background: featured ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
      border: `1px solid ${featured ? 'rgba(182,166,214,0.4)' : 'var(--glass-edge)'}`,
      backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: featured ? 'var(--elev-3), var(--glass-inner), var(--glow-violet)' : 'var(--glass-shadow), var(--glass-inner)',
      display: 'flex', flexDirection: 'column',
    }}>
      <h3 className="rv-tariff-name" style={{ fontSize: 'var(--t-h3)' }}>{data.name}</h3>
      <p className="rv-tariff-tagline" style={{ marginTop: 8, color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>{data.tagline}</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 22, marginBottom: 24 }}>
        {data.features.map((f) => (
          <div key={f.text} style={{ display: 'flex', gap: 11, alignItems: 'flex-start' }}>
            <i data-lucide={f.you ? 'user-round' : 'check'} style={{ width: 18, height: 18, marginTop: 2, flex: 'none', color: f.you ? 'var(--accent-violet)' : 'var(--success)' }}></i>
            <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)', lineHeight: 1.45 }}>{f.text}</span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 'auto', paddingTop: 20, borderTop: '1px solid var(--glass-edge-faint)' }}>
        <div className="rv-tariff-price" style={{ display: 'flex', alignItems: 'baseline', gap: 8, flexWrap: 'wrap' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 34, fontWeight: 600, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{data.price}</span>
          <span style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>руб.</span>
        </div>
        <div className="rv-tariff-fee" style={{ marginTop: 6, fontSize: 'var(--t-sm)', color: 'var(--text-muted)' }}>
          + <FeeLink onOpen={onOpenFee} />
        </div>
        <div style={{ marginTop: 22 }}>
          <Button variant={featured ? 'primary' : 'secondary'} fullWidth size="lg"
            iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>}
            onClick={() => { if (window.__openConsult) window.__openConsult(); }}>
            Записаться на консультацию
          </Button>
        </div>
      </div>
    </div>
  );
}

function Services() {
  const [feeOpen, setFeeOpen] = React.useState(false);
  const tariff = {
    name: 'Всё включено',
    tagline: 'Берём весь процесс на себя - от анкеты до подачи.',
    price: '29 990',
    features: [
      { text: 'Заполняем анкету за вас' },
      { text: 'Готовим полный пакет документов' },
      { text: 'Помогаем поймать слот в визовый центр на подачу документов' },
    ],
  };

  return (
    <section id="services" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">Стоимость</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Всё включено</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            Берём весь процесс на себя - вам остаётся только прийти на подачу.
          </p>
        </div>
        <div style={{ maxWidth: 760, margin: '0 auto' }}>
          <TariffCard data={tariff} featured={false} onOpenFee={() => setFeeOpen(true)} />
        </div>
      </div>
      <FeeModal open={feeOpen} onClose={() => setFeeOpen(false)} />
    </section>
  );
}

Object.assign(window, { Services });
"""

SCHENGEN_HERO = r"""/* global React */
function Hero() {
  const { Button, Badge } = window.RoyalVisaUKDesignSystem_ccc97c;
  const go = (e, href) => {
    e.preventDefault();
    const el = document.querySelector(href);
    if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 84, behavior: 'smooth' });
  };

  return (
    <section id="top" style={{ position: 'relative', paddingTop: 132, paddingBottom: 96 }}>
      <div className="rv-container">
        <div className="rv-hero-grid" style={{ display: 'grid', gridTemplateColumns: '1.05fr 0.95fr', gap: 56, alignItems: 'center' }}>
          <div className="rv-hero-copy">
            <div style={{ marginBottom: 22 }}>
              <Badge tone="accent" dot>Шенгенские визы · с 2022 года</Badge>
            </div>
            <h1 style={{ fontSize: 'var(--t-display)', letterSpacing: 'var(--track-tight)', lineHeight: 1.02 }}>
              Шенген в 2026 -<br />
              <span style={{
                background: 'var(--grad-royal)', WebkitBackgroundClip: 'text',
                backgroundClip: 'text', color: 'transparent',
              }}>это реально</span>
            </h1>
            <p className="rv-hero-lead" style={{ marginTop: 22, fontSize: 'var(--t-lg)', color: 'var(--text-body)', maxWidth: 520, lineHeight: 'var(--lh-relaxed)' }}>
              Получить шенген сложнее, чем раньше, но реально. Поможем оформить визу в Европу под ключ.
            </p>
            <div className="rv-hero-actions" style={{ marginTop: 32, display: 'flex', gap: 14, flexWrap: 'wrap' }}>
              <Button variant="primary" size="lg" iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>} onClick={() => { if (window.__openConsult) window.__openConsult(); }}>
                Бесплатная консультация
              </Button>
              <Button variant="secondary" size="lg" onClick={(e) => go(e, '#services')}>Стоимость</Button>
            </div>
            <div className="rv-hero-stats" style={{ marginTop: 40, display: 'flex', gap: 36, flexWrap: 'wrap' }}>
              {[['≈ 70%', 'Одобрений виз'], ['до 2 лет', 'Срок визы'], ['3-4 нед.', 'Решение по заявке']].map(([v, l]) => (
                <div key={l}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: 28, fontWeight: 500, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{v}</div>
                  <div style={{ fontSize: 'var(--t-sm)', color: 'var(--text-muted)', marginTop: 2 }}>{l}</div>
                </div>
              ))}
            </div>
          </div>

          <div style={{ position: 'relative' }}>
            <div style={{
              position: 'absolute', inset: -30, borderRadius: '50%',
              background: 'var(--grad-royal)', filter: 'blur(60px)', opacity: 0.42, zIndex: 0,
            }} />
            <div style={{
              position: 'relative', zIndex: 1, padding: 12, borderRadius: 'var(--r-2xl)',
              background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
              boxShadow: 'var(--elev-3), var(--glass-inner)',
              backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
            }}>
              <img
                src={window.__rv('paris', 'assets/photos/paris.jpg')}
                alt="Эйфелева башня, Париж"
                style={{ display: 'block', width: '100%', height: 'auto', borderRadius: 24 }}
              />
              <div style={{
                position: 'absolute', left: 26, bottom: 26,
                display: 'inline-flex', alignItems: 'center', gap: 10,
                padding: '12px 16px', borderRadius: 'var(--r-pill)',
                background: 'var(--glass-fill-solid)', border: '1px solid var(--glass-edge)',
                backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                boxShadow: 'var(--glass-inner)',
              }}>
                <i data-lucide="map-pin" style={{ width: 16, height: 16, color: 'var(--accent-violet)' }}></i>
                <span style={{ fontSize: 'var(--t-sm)', color: 'var(--text-strong)', fontWeight: 500 }}>Эйфелева башня, Париж</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { Hero });
"""

SCHENGEN_ABOUT = r"""/* global React */
function AboutVisa() {
  const { Badge } = window.RoyalVisaUKDesignSystem_ccc97c;
  const points = [
    { icon: 'calendar-check', title: 'Выдают даже на 2 года', text: 'В 2026 году есть случаи выдачи шенгена на 2 года с многократным въездом - для 2026 года это из области фантастики.' },
    { icon: 'globe', title: '27 стран по одной визе', text: 'Германия, Франция, Италия, Испания и ещё 23 страны - все по одному разрешению без дополнительных сборов.' },
    { icon: 'shield-check', title: 'Помогаем даже в сложных случаях', text: 'Знаем актуальные требования консульств и собираем убедительный пакет документов.' },
  ];
  return (
    <section id="about" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div className="rv-about-grid" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 48, alignItems: 'center' }}>
          <div className="rv-about-copy">
            <div style={{ marginBottom: 18 }}>
              <span className="rv-eyebrow">О визе</span>
            </div>
            <h2 style={{ fontSize: 'var(--t-h2)' }}>Европа открыта - в наше время</h2>
            <p style={{ marginTop: 18, fontSize: 'var(--t-lg)', color: 'var(--text-body)', lineHeight: 'var(--lh-relaxed)' }}>
              Шенген получить сложнее, чем раньше, но путешествовать по Европе в 2026 году -
              это реально. Правильно собранный пакет документов значительно повышает шансы на одобрение.
            </p>
            <div className="rv-about-points" style={{ marginTop: 28, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12 }}>
              {points.map((p) => (
                <div key={p.title} style={{
                  display: 'flex', gap: 16, padding: 18, borderRadius: 'var(--r-lg)',
                  background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
                  backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                  boxShadow: 'var(--glass-inner-soft)',
                }}>
                  <div style={{
                    flex: 'none', width: 44, height: 44, borderRadius: 'var(--r-md)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    background: 'var(--glass-tint-violet)', border: '1px solid var(--glass-edge)',
                  }}>
                    <i data-lucide={p.icon} style={{ width: 21, height: 21, color: 'var(--accent-violet)' }}></i>
                  </div>
                  <div>
                    <div style={{ color: 'var(--text-strong)', fontWeight: 600, fontSize: 'var(--t-lg)' }}>{p.title}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)', marginTop: 3, lineHeight: 1.55 }}>{p.text}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { AboutVisa });
"""

SCHENGEN_MAP = r"""/* global React */
var SCHENGEN_GEO_GROUPS = [
  { label: 'Западная Европа', countries: [
    { id: 'fr', name: 'Франция', flag: '🇫🇷', capital: 'Париж' },
    { id: 'de', name: 'Германия', flag: '🇩🇪', capital: 'Берлин' },
    { id: 'nl', name: 'Нидерланды', flag: '🇳🇱', capital: 'Амстердам' },
    { id: 'be', name: 'Бельгия', flag: '🇧🇪', capital: 'Брюссель' },
    { id: 'lu', name: 'Люксембург', flag: '🇱🇺', capital: 'Люксембург' },
    { id: 'at', name: 'Австрия', flag: '🇦🇹', capital: 'Вена' },
    { id: 'ch', name: 'Швейцария', flag: '🇨🇭', capital: 'Берн' },
    { id: 'li', name: 'Лихтенштейн', flag: '🇱🇮', capital: 'Вадуц' },
    { id: 'pt', name: 'Португалия', flag: '🇵🇹', capital: 'Лиссабон' },
  ]},
  { label: 'Южная Европа', countries: [
    { id: 'it', name: 'Италия', flag: '🇮🇹', capital: 'Рим' },
    { id: 'es', name: 'Испания', flag: '🇪🇸', capital: 'Мадрид' },
    { id: 'gr', name: 'Греция', flag: '🇬🇷', capital: 'Афины' },
    { id: 'hr', name: 'Хорватия', flag: '🇭🇷', capital: 'Загреб' },
    { id: 'si', name: 'Словения', flag: '🇸🇮', capital: 'Любляна' },
    { id: 'mt', name: 'Мальта', flag: '🇲🇹', capital: 'Валлетта' },
  ]},
  { label: 'Центральная и Восточная Европа', countries: [
    { id: 'pl', name: 'Польша', flag: '🇵🇱', capital: 'Варшава' },
    { id: 'cz', name: 'Чехия', flag: '🇨🇿', capital: 'Прага' },
    { id: 'sk', name: 'Словакия', flag: '🇸🇰', capital: 'Братислава' },
    { id: 'hu', name: 'Венгрия', flag: '🇭🇺', capital: 'Будапешт' },
    { id: 'ro', name: 'Румыния', flag: '🇷🇴', capital: 'Бухарест' },
    { id: 'bg', name: 'Болгария', flag: '🇧🇬', capital: 'София' },
  ]},
  { label: 'Северная Европа', countries: [
    { id: 'se', name: 'Швеция', flag: '🇸🇪', capital: 'Стокгольм' },
    { id: 'no', name: 'Норвегия', flag: '🇳🇴', capital: 'Осло' },
    { id: 'dk', name: 'Дания', flag: '🇩🇰', capital: 'Копенгаген' },
    { id: 'fi', name: 'Финляндия', flag: '🇫🇮', capital: 'Хельсинки' },
    { id: 'is', name: 'Исландия', flag: '🇮🇸', capital: 'Рейкьявик' },
  ]},
  { label: 'Прибалтика', countries: [
    { id: 'ee', name: 'Эстония', flag: '🇪🇪', capital: 'Таллин' },
    { id: 'lv', name: 'Латвия', flag: '🇱🇻', capital: 'Рига' },
    { id: 'lt', name: 'Литва', flag: '🇱🇹', capital: 'Вильнюс' },
  ]},
];

function UKMap() {
  var [hoveredId, setHoveredId] = React.useState(null);
  return (
    <section id="map" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 680, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">{'Шенгенская зона'}</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>{'Одна виза - вся Европа'}</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            {'29 стран шенгенской зоны. Одна виза даёт доступ ко всем — без отдельных разрешений.'}
          </p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
          {SCHENGEN_GEO_GROUPS.map(function(geo) {
            return (
              <div key={geo.label}>
                <div style={{ fontSize: 'var(--t-sm)', fontWeight: 600, letterSpacing: 'var(--track-eyebrow)', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 14 }}>
                  {geo.label}
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {geo.countries.map(function(c) {
                    var on = hoveredId === c.id;
                    return (
                      <div
                        key={c.id}
                        onMouseEnter={function() { setHoveredId(c.id); }}
                        onMouseLeave={function() { setHoveredId(null); }}
                        style={{
                          padding: '10px 16px', borderRadius: 'var(--r-lg)',
                          display: 'flex', alignItems: 'center', gap: 10,
                          background: on ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
                          border: ('1px solid ' + (on ? 'rgba(182,166,214,0.5)' : 'var(--glass-edge)')),
                          backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                          boxShadow: on ? 'var(--glow-violet), var(--glass-inner)' : 'var(--glass-inner-soft)',
                          transform: on ? 'translateY(-2px)' : 'none',
                          cursor: 'default',
                          transition: 'all .18s ease',
                        }}
                      >
                        <span style={{ fontSize: 20, lineHeight: 1 }}>{c.flag}</span>
                        <div>
                          <div style={{ fontSize: 'var(--t-sm)', fontWeight: on ? 600 : 500, color: on ? 'var(--text-strong)' : 'var(--text-body)', lineHeight: 1.2 }}>{c.name}</div>
                          <div style={{ fontSize: 'var(--t-xs)', color: 'var(--text-muted)', marginTop: 2 }}>{c.capital}</div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { UKMap });
"""

_SCHENGEN_MAP_OLD = r"""UNUSED_var SCHENGEN_COLOR_GROUPS = [
  { key: 'purple',       ref: [182,154,202], accent: 'rgba(210,180,240,0.85)',
    countries: [{id:'fr',name:'Франция',flag:'🇫🇷'},{id:'es',name:'Испания',flag:'🇪🇸'},{id:'hr',name:'Хорватия',flag:'🇭🇷'}] },
  { key: 'yellow-lime',  ref: [217,224,34],  accent: 'rgba(230,240,80,0.85)',
    countries: [{id:'de',name:'Германия',flag:'🇩🇪'},{id:'pt',name:'Португалия',flag:'🇵🇹'},{id:'it',name:'Италия',flag:'🇮🇹'},{id:'at',name:'Австрия',flag:'🇦🇹'},{id:'ch',name:'Швейцария',flag:'🇨🇭'},{id:'cz',name:'Чехия',flag:'🇨🇿'},{id:'si',name:'Словения',flag:'🇸🇮'},{id:'li',name:'Лихтенштейн',flag:'🇱🇮'}] },
  { key: 'green',        ref: [140,198,63],  accent: 'rgba(160,220,80,0.85)',
    countries: [{id:'fi',name:'Финляндия',flag:'🇫🇮'},{id:'ee',name:'Эстония',flag:'🇪🇪'}] },
  { key: 'sky',          ref: [133,187,223], accent: 'rgba(160,210,240,0.85)',
    countries: [{id:'se',name:'Швеция',flag:'🇸🇪'},{id:'hu',name:'Венгрия',flag:'🇭🇺'},{id:'lu',name:'Люксембург',flag:'🇱🇺'},{id:'ro',name:'Румыния',flag:'🇷🇴'},{id:'mt',name:'Мальта',flag:'🇲🇹'},{id:'be',name:'Бельгия',flag:'🇧🇪'},{id:'nl',name:'Нидерланды',flag:'🇳🇱'}] },
  { key: 'blue-violet',  ref: [154,153,255], accent: 'rgba(180,178,255,0.85)',
    countries: [{id:'pl',name:'Польша',flag:'🇵🇱'},{id:'sk',name:'Словакия',flag:'🇸🇰'},{id:'lt',name:'Литва',flag:'🇱🇹'},{id:'lv',name:'Латвия',flag:'🇱🇻'}] },
  { key: 'bright-yellow',ref: [255,255,104], accent: 'rgba(255,255,140,0.85)',
    countries: [{id:'dk',name:'Дания',flag:'🇩🇰'},{id:'no',name:'Норвегия',flag:'🇳🇴'},{id:'gr',name:'Греция',flag:'🇬🇷'},{id:'bg',name:'Болгария',flag:'🇧🇬'},{id:'is',name:'Исландия',flag:'🇮🇸'}] },
];

var GEO_GROUPS = [
  { label: 'Западная Европа', ids: ['fr','de','nl','be','lu','at','ch','li','pt'] },
  { label: 'Южная Европа', ids: ['it','es','hr','si','gr','mt','bg'] },
  { label: 'Центральная/Восточная Европа', ids: ['pl','cz','sk','hu','ro'] },
  { label: 'Северная Европа', ids: ['se','no','dk','fi','is'] },
  { label: 'Прибалтика', ids: ['ee','lv','lt'] },
];

var ALL_BY_ID = {};
SCHENGEN_COLOR_GROUPS.forEach(function(g) { g.countries.forEach(function(c) { ALL_BY_ID[c.id] = { country: c, group: g }; }); });

function schColorDist(r,g,b,ref) { var dr=r-ref[0],dg=g-ref[1],db=b-ref[2]; return dr*dr+dg*dg+db*db; }

function getSchGroupKey(r,g,b,a) {
  if (a < 128) return null;
  var best=null, bestD=9000;
  for (var i=0;i<SCHENGEN_COLOR_GROUPS.length;i++) {
    var d=schColorDist(r,g,b,SCHENGEN_COLOR_GROUPS[i].ref);
    if (d<bestD) { bestD=d; best=SCHENGEN_COLOR_GROUPS[i].key; }
  }
  return bestD < 4000 ? best : null;
}

function UKMap() {
  var imgRef = React.useRef(null);
  var overlayCanvasRef = React.useRef(null);
  var hiddenCanvasRef = React.useRef(null);
  var masksRef = React.useRef(null);
  var imgDataRef = React.useRef(null);
  var activeGroupRef = React.useRef(null);
  var [activeGroup, setActiveGroup] = React.useState(null);
  var mapUrl = window.__rv('schengenmap', 'assets/maps/map.jpg');

  React.useEffect(function() {
    var img = new Image();
    img.onload = function() {
      var hc = hiddenCanvasRef.current;
      if (!hc) return;
      hc.width = img.naturalWidth; hc.height = img.naturalHeight;
      var ctx = hc.getContext('2d');
      ctx.drawImage(img, 0, 0);
      var imgData = ctx.getImageData(0, 0, hc.width, hc.height);
      imgDataRef.current = imgData;
      var data = imgData.data, w = imgData.width, h = imgData.height;
      var masks = {};
      SCHENGEN_COLOR_GROUPS.forEach(function(g) { masks[g.key] = new Uint8ClampedArray(data.length); });
      for (var i=0;i<data.length;i+=4) {
        var key = getSchGroupKey(data[i],data[i+1],data[i+2],data[i+3]);
        if (key) { masks[key][i]=data[i]; masks[key][i+1]=data[i+1]; masks[key][i+2]=data[i+2]; masks[key][i+3]=255; }
      }
      var stored = {};
      SCHENGEN_COLOR_GROUPS.forEach(function(g) { stored[g.key] = new ImageData(masks[g.key], w, h); });
      masksRef.current = stored;
    };
    img.src = mapUrl;
  }, [mapUrl]);

  var drawOverlay = React.useCallback(function(key) {
    var oc = overlayCanvasRef.current;
    if (!oc || !imgDataRef.current) return;
    oc.width = imgDataRef.current.width; oc.height = imgDataRef.current.height;
    var ctx = oc.getContext('2d');
    ctx.clearRect(0, 0, oc.width, oc.height);
    if (key && masksRef.current && masksRef.current[key]) ctx.putImageData(masksRef.current[key], 0, 0);
  }, []);

  var handleMouseMove = React.useCallback(function(e) {
    if (!imgDataRef.current) return;
    var rect = e.currentTarget.getBoundingClientRect();
    var sx = imgDataRef.current.width / rect.width, sy = imgDataRef.current.height / rect.height;
    var px = Math.floor((e.clientX-rect.left)*sx), py = Math.floor((e.clientY-rect.top)*sy);
    var data = imgDataRef.current.data, w = imgDataRef.current.width, h = imgDataRef.current.height;
    if (px<0||py<0||px>=w||py>=h) return;
    var i=(py*w+px)*4;
    var key = getSchGroupKey(data[i],data[i+1],data[i+2],data[i+3]);
    if (key !== activeGroupRef.current) { activeGroupRef.current = key; setActiveGroup(key); drawOverlay(key); }
  }, [drawOverlay]);

  var handleMouseLeave = React.useCallback(function() {
    activeGroupRef.current = null; setActiveGroup(null); drawOverlay(null);
  }, [drawOverlay]);

  var activeGroupObj = activeGroup ? SCHENGEN_COLOR_GROUPS.find(function(g) { return g.key === activeGroup; }) : null;

  return (
    <section id="map" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 680, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">{'Шенгенская зона'}</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>{'Одна виза - вся Европа'}</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            {'29 стран шенгенской зоны. Одна виза даёт доступ ко всем — без отдельных разрешений.'}
          </p>
        </div>

        <div className="rv-map-grid" style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: 32, alignItems: 'start' }}>
          <div style={{ position: 'relative', borderRadius: 'var(--r-xl)', overflow: 'hidden', background: '#08060f', boxShadow: 'var(--elev-2), var(--glass-inner)' }}>
            <canvas ref={hiddenCanvasRef} style={{ display: 'none' }} />
            <img
              ref={imgRef}
              src={mapUrl}
              alt=""
              style={{ width: '100%', display: 'block', filter: activeGroup ? 'brightness(0.42) saturate(0.7)' : 'none', transition: 'filter .25s ease' }}
            />
            <canvas
              ref={overlayCanvasRef}
              style={{
                position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none',
                filter: activeGroupObj ? ('drop-shadow(0 0 14px ' + activeGroupObj.accent + ')') : 'none',
                transition: 'filter .25s ease',
              }}
            />
            <div onMouseMove={handleMouseMove} onMouseLeave={handleMouseLeave} style={{ position: 'absolute', inset: 0, cursor: 'crosshair' }} />
            {activeGroupObj && (
              <div style={{
                position: 'absolute', bottom: 14, left: 14, right: 14,
                padding: '10px 14px', borderRadius: 'var(--r-lg)',
                background: 'rgba(10,8,18,0.78)',
                backdropFilter: 'blur(16px) saturate(140%)', WebkitBackdropFilter: 'blur(16px) saturate(140%)',
                border: '1px solid rgba(255,255,255,0.12)',
                display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center',
              }}>
                {activeGroupObj.countries.map(function(c) {
                  return (
                    <span key={c.id} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 'var(--t-sm)', color: '#fff' }}>
                      <span>{c.flag}</span><span>{c.name}</span>
                    </span>
                  );
                })}
              </div>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 22 }}>
            {GEO_GROUPS.map(function(geo) {
              return (
                <div key={geo.label}>
                  <div style={{ fontSize: 'var(--t-xs)', fontWeight: 600, letterSpacing: 'var(--track-eyebrow)', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 10 }}>
                    {geo.label}
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {geo.ids.map(function(id) {
                      var entry = ALL_BY_ID[id];
                      if (!entry) return null;
                      var on = activeGroup === entry.group.key;
                      return (
                        <div
                          key={id}
                          onMouseEnter={function() { setActiveGroup(entry.group.key); activeGroupRef.current = entry.group.key; drawOverlay(entry.group.key); }}
                          onMouseLeave={function() { setActiveGroup(null); activeGroupRef.current = null; drawOverlay(null); }}
                          style={{
                            padding: '6px 12px', borderRadius: 'var(--r-lg)',
                            display: 'flex', alignItems: 'center', gap: 6,
                            background: on ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
                            border: ('1px solid ' + (on ? 'rgba(182,166,214,0.5)' : 'var(--glass-edge)')),
                            backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                            boxShadow: on ? 'var(--glow-violet), var(--glass-inner)' : 'var(--glass-inner-soft)',
                            transform: on ? 'translateY(-1px)' : 'none',
                            cursor: 'default', transition: 'all .18s ease',
                          }}
                        >
                          <span style={{ fontSize: 15 }}>{entry.country.flag}</span>
                          <span style={{ fontSize: 'var(--t-sm)', fontWeight: on ? 600 : 400, color: on ? 'var(--text-strong)' : 'var(--text-body)', whiteSpace: 'nowrap' }}>{entry.country.name}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { UKMap });
"""

SCHENGEN_SERVICES = r"""/* global React */
const SCHENGEN_CONSULAR_FEES = [
  { label: 'Краткосрочная шенгенская виза (стандарт)', price: '90 €' },
  { label: 'Дети до 6 лет', price: 'Бесплатно' },
  { label: 'Дети 6-12 лет', price: '45 €' },
];

function FeeLink({ onOpen }) {
  return (
    <button onClick={onOpen} style={{
      display: 'inline-flex', alignItems: 'center', gap: 5, padding: 0,
      background: 'none', border: 'none', cursor: 'pointer', font: 'inherit',
      color: 'var(--accent-sky)', fontWeight: 600,
      textDecoration: 'underline', textUnderlineOffset: 3, textDecorationColor: 'rgba(185,210,230,0.45)',
    }}>
      консульский сбор
      <i data-lucide="info" style={{ width: 14, height: 14 }}></i>
    </button>
  );
}

function FeeModal({ open, onClose }) {
  React.useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  return (
    <div aria-hidden={!open} style={{
      position: 'fixed', inset: 0, zIndex: 80,
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20,
      pointerEvents: open ? 'auto' : 'none',
    }}>
      <div onClick={onClose} style={{
        position: 'absolute', inset: 0, background: 'rgba(8,7,13,0.55)',
        backdropFilter: open ? 'blur(20px) saturate(140%)' : 'blur(0)',
        WebkitBackdropFilter: open ? 'blur(20px) saturate(140%)' : 'blur(0)',
        opacity: open ? 1 : 0, transition: 'opacity .28s ease',
      }} />
      <div role="dialog" aria-modal="true" style={{
        position: 'relative', width: '100%', maxWidth: 480, padding: 28,
        borderRadius: 'var(--r-2xl)',
        background: 'var(--glass-fill-strong)',
        border: '1px solid var(--glass-edge-strong)',
        backdropFilter: 'var(--glass-blur-heavy)', WebkitBackdropFilter: 'var(--glass-blur-heavy)',
        boxShadow: 'var(--elev-4), var(--glass-inner)',
        transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.96)',
        opacity: open ? 1 : 0, transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease',
      }}>
        <button aria-label="Закрыть" onClick={onClose} style={{
          position: 'absolute', top: 16, right: 16, width: 36, height: 36, cursor: 'pointer',
          borderRadius: 'var(--r-sm)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <i data-lucide="x" style={{ width: 18, height: 18, color: 'var(--text-strong)' }}></i>
        </button>

        <div style={{ position: 'relative' }}>
          <div style={{
            width: 46, height: 46, borderRadius: 'var(--r-md)', marginBottom: 16,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'var(--glass-tint-sky)', border: '1px solid var(--glass-edge)',
          }}>
            <i data-lucide="credit-card" style={{ width: 22, height: 22, color: 'var(--accent-sky)' }}></i>
          </div>
          <p style={{ margin: 0, fontSize: 'var(--t-lg)', color: 'var(--text-strong)', lineHeight: 1.45, fontWeight: 500 }}>
            Консульский сбор оплачивается зарубежной банковской картой. Если у вас такой нет - мы поможем оплатить.
          </p>

          <div style={{ marginTop: 22, display: 'flex', flexDirection: 'column', gap: 2 }}>
            {SCHENGEN_CONSULAR_FEES.map((f, i) => (
              <div key={f.label} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16,
                padding: '14px 4px',
                borderTop: i === 0 ? 'none' : '1px solid var(--glass-edge-faint)',
              }}>
                <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)' }}>{f.label}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--t-lg)', fontWeight: 600, color: 'var(--text-strong)', whiteSpace: 'nowrap' }}>{f.price}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function TariffCard({ data, featured, onOpenFee }) {
  const { Button } = window.RoyalVisaUKDesignSystem_ccc97c;
  return (
    <div style={{
      position: 'relative', padding: 30, borderRadius: 'var(--r-xl)',
      background: featured ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
      border: `1px solid ${featured ? 'rgba(182,166,214,0.4)' : 'var(--glass-edge)'}`,
      backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: featured ? 'var(--elev-3), var(--glass-inner), var(--glow-violet)' : 'var(--glass-shadow), var(--glass-inner)',
      display: 'flex', flexDirection: 'column',
    }}>
      <h3 className="rv-tariff-name" style={{ fontSize: 'var(--t-h3)' }}>{data.name}</h3>
      <p className="rv-tariff-tagline" style={{ marginTop: 8, color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>{data.tagline}</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 22, marginBottom: 24 }}>
        {data.features.map((f) => (
          <div key={f.text} style={{ display: 'flex', gap: 11, alignItems: 'flex-start' }}>
            <i data-lucide="check" style={{ width: 18, height: 18, marginTop: 2, flex: 'none', color: 'var(--success)' }}></i>
            <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)', lineHeight: 1.45 }}>{f.text}</span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 'auto', paddingTop: 20, borderTop: '1px solid var(--glass-edge-faint)' }}>
        <div className="rv-tariff-price" style={{ display: 'flex', alignItems: 'baseline', gap: 8, flexWrap: 'wrap' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 34, fontWeight: 600, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{data.price}</span>
          <span style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>руб.</span>
        </div>
        <div className="rv-tariff-fee" style={{ marginTop: 6, fontSize: 'var(--t-sm)', color: 'var(--text-muted)' }}>
          + <FeeLink onOpen={onOpenFee} />
        </div>
        <div style={{ marginTop: 22 }}>
          <Button variant="secondary" fullWidth size="lg"
            iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>}
            onClick={() => { if (window.__openConsult) window.__openConsult(); }}>
            Записаться на консультацию
          </Button>
        </div>
      </div>
    </div>
  );
}

function Services() {
  const [feeOpen, setFeeOpen] = React.useState(false);
  const tariff = {
    name: 'Всё включено',
    tagline: 'Берём весь процесс на себя - от анкеты до подачи.',
    price: '29 990',
    features: [
      { text: 'Заполняем анкету за вас' },
      { text: 'Готовим полный пакет документов' },
      { text: 'Подбираем оптимальное консульство для подачи' },
    ],
  };

  return (
    <section id="services" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">Стоимость</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Всё включено</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            Берём весь процесс на себя - вам остаётся только прийти на подачу.
          </p>
        </div>
        <div style={{ maxWidth: 760, margin: '0 auto' }}>
          <TariffCard data={tariff} featured={false} onOpenFee={() => setFeeOpen(true)} />
        </div>
      </div>
      <FeeModal open={feeOpen} onClose={() => setFeeOpen(false)} />
    </section>
  );
}

Object.assign(window, { Services });
"""

SCHENGEN_CONSULT_FORM = CONSULT_FORM_UK.replace(
    r"'🇬🇧 Новая заявка - Royal Visas'",
    r"'🇪🇺 Новая заявка - Шенгенская виза'"
)

def inject_promos(src: str) -> str:
    return src.replace('__PROMO_CODES__', json.dumps(PROMO_CODES))

LANDING_APP = r"""/* global React */
function ConsultModal({ open, onClose }) {
  const TG_TOKEN = '8677081622:AAHAvOYbY50uCZnx9QimTXDO98CYJnMnvxA';
  const TG_CHAT_ID = '-5235367527';
  const VISA_LABEL = '📋 Новая заявка - Royal Visas';
  const PROMO_DISCOUNT = 5000;

  const { Button, Input, Switch } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [channel, setChannel] = React.useState('whatsapp');
  const [sent, setSent] = React.useState(false);
  const [name, setName] = React.useState('');
  const [contact, setContact] = React.useState('');
  const [sending, setSending] = React.useState(false);
  const [error, setError] = React.useState('');
  const [opts, setOpts] = React.useState({ weekdays: false, hours: false, anytime: true, urgent: false });

  React.useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  React.useEffect(() => {
    if (open) document.body.style.overflow = 'hidden';
    else document.body.style.overflow = '';
    return () => { document.body.style.overflow = ''; };
  }, [open]);

  React.useEffect(() => {
    if (open && window.lucide) setTimeout(() => window.lucide.createIcons(), 30);
  }, [open]);

  const setOpt = (k, v) => setOpts((p) => {
    const next = { ...p, [k]: v };
    if (k === 'anytime' && v) { next.weekdays = false; next.hours = false; }
    if ((k === 'weekdays' || k === 'hours') && v) next.anytime = false;
    return next;
  });

  const submit = async (e) => {
    e.preventDefault();
    setError(''); setSending(true);
    try {
      const when = [];
      if (opts.weekdays) when.push('только будни');
      if (opts.hours) when.push('рабочие часы (до 18:00)');
      if (opts.anytime) when.push('в любое время');
      const text = [
        VISA_LABEL,
        'Имя: ' + (name || '-'),
        'Канал: ' + (channel === 'whatsapp' ? 'WhatsApp' : 'Telegram'),
        'Контакт: ' + (contact || '-'),
        'Когда писать: ' + (when.join(', ') || '-'),
        opts.urgent ? '⚡ Виза нужна СРОЧНО' : null,
      ].filter(Boolean).join('\n');
      const resp = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: TG_CHAT_ID, text }),
      });
      const jr = await resp.json();
      if (!jr.ok) throw new Error(jr.description || 'send failed');
      setSent(true);
    } catch (err) {
      setError('Не удалось отправить заявку. Напишите нам напрямую в WhatsApp или Telegram.');
    } finally {
      setSending(false);
    }
  };

  const switches = [
    { key: 'weekdays', label: 'Писать только в будние дни', icon: 'calendar-days' },
    { key: 'hours', label: 'Писать только в рабочие часы (до 18:00)', icon: 'clock' },
    { key: 'anytime', label: 'Писать в любое время', icon: 'infinity' },
    { key: 'urgent', label: 'Виза нужна срочно', icon: 'zap' },
  ];

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 200,
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20,
      pointerEvents: open ? 'auto' : 'none',
    }}>
      <div onClick={onClose} style={{
        position: 'absolute', inset: 0, background: 'rgba(8,7,13,0.65)',
        backdropFilter: open ? 'blur(24px) saturate(140%)' : 'blur(0)',
        WebkitBackdropFilter: open ? 'blur(24px) saturate(140%)' : 'blur(0)',
        opacity: open ? 1 : 0, transition: 'opacity .28s ease',
      }} />
      <div role="dialog" aria-modal="true" style={{
        position: 'relative', width: '100%', maxWidth: 560, maxHeight: '90vh', overflowY: 'auto',
        borderRadius: 'var(--r-2xl)',
        background: 'var(--glass-fill-strong)', border: '1px solid var(--glass-edge-strong)',
        backdropFilter: 'var(--glass-blur-heavy)', WebkitBackdropFilter: 'var(--glass-blur-heavy)',
        boxShadow: 'var(--elev-4), var(--glass-inner)',
        transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.97)',
        opacity: open ? 1 : 0,
        transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease',
        padding: 32,
      }}>
        <button aria-label="Закрыть" onClick={onClose} style={{
          position: 'absolute', top: 16, right: 16, zIndex: 10,
          width: 36, height: 36, cursor: 'pointer',
          borderRadius: 'var(--r-sm)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <i data-lucide="x" style={{ width: 18, height: 18, color: 'var(--text-strong)' }}></i>
        </button>
        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <span className="rv-eyebrow">Бесплатная консультация</span>
          <h2 style={{ fontSize: 'var(--t-h2)', marginTop: 12 }}>Оставьте заявку</h2>
          <p style={{ marginTop: 10, fontSize: 'var(--t-body)', color: 'var(--text-body)' }}>Ответим в мессенджере и расскажем о вашей визе.</p>
        </div>
        {sent ? (
          <div style={{ textAlign: 'center', padding: '24px 0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'var(--success-soft)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <i data-lucide="check" style={{ width: 30, height: 30, color: 'var(--success)' }}></i>
            </div>
            <h3 style={{ fontSize: 'var(--t-h3)' }}>Заявка отправлена</h3>
            <p style={{ color: 'var(--text-muted)' }}>Свяжемся с вами в ближайшее время.</p>
            <Button variant="ghost" size="sm" onClick={() => { setSent(false); setName(''); setContact(''); }}>Отправить ещё одну</Button>
          </div>
        ) : (
          <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <Input label="Имя" placeholder="Как к вам обращаться" required value={name} onChange={(e) => setName(e.target.value)} icon={<i data-lucide="user-round" style={{ width: 17, height: 17 }}></i>} />
            <div>
              <div style={{ fontSize: 'var(--t-sm)', fontWeight: 500, color: 'var(--text-body)', marginBottom: 8 }}>Куда вам написать</div>
              <div style={{ display: 'flex', gap: 10 }}>
                {['whatsapp', 'telegram'].map((ch) => (
                  <button key={ch} type="button" onClick={() => { setChannel(ch); setContact(''); setError(''); }} style={{
                    flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 9,
                    height: 48, cursor: 'pointer', borderRadius: 'var(--r-md)',
                    fontFamily: 'var(--font-sans)', fontSize: 'var(--t-body)', fontWeight: 600,
                    color: channel === ch ? '#fff' : 'var(--text-body)',
                    background: channel === ch ? 'var(--grad-twilight)' : 'var(--glass-fill)',
                    border: ('1px solid ' + (channel === ch ? 'rgba(255,255,255,0.2)' : 'var(--glass-edge)')),
                    transition: 'all .2s ease',
                  }}>
                    <i data-lucide={ch === 'whatsapp' ? 'message-circle' : 'send'} style={{ width: 19, height: 19 }}></i>
                    {ch === 'whatsapp' ? 'WhatsApp' : 'Telegram'}
                  </button>
                ))}
              </div>
            </div>
            {channel === 'whatsapp'
              ? <Input key="wa" label="Номер телефона" type="tel" required value={contact} onChange={(e) => setContact(e.target.value)} placeholder="+7 900 000-00-00" icon={<i data-lucide="phone" style={{ width: 17, height: 17 }}></i>} />
              : <Input key="tg" label="Ваш @никнейм" required value={contact} onChange={(e) => setContact(e.target.value)} placeholder="@username" icon={<i data-lucide="at-sign" style={{ width: 17, height: 17 }}></i>} />}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {switches.map((s) => {
                const on = opts[s.key];
                return (
                  <div key={s.key} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 6px', borderRadius: 'var(--r-md)', background: on ? 'var(--glass-fill)' : 'transparent' }}>
                    <i data-lucide={s.icon} style={{ width: 16, height: 16, flex: 'none', color: on ? 'var(--accent-violet)' : 'var(--ink-3)' }}></i>
                    <span style={{ flex: 1, fontSize: 'var(--t-sm)', color: on ? 'var(--text-strong)' : 'var(--text-body)' }}>{s.label}</span>
                    <Switch checked={on} onChange={(v) => setOpt(s.key, v)} size="sm" accent="var(--grad-twilight)" />
                  </div>
                );
              })}
            </div>
            {error && (
              <div style={{ padding: '10px 14px', borderRadius: 'var(--r-md)', background: 'var(--danger-soft)', fontSize: 'var(--t-sm)', color: 'var(--text-body)' }}>{error}</div>
            )}
            <Button type="submit" variant="primary" size="lg" fullWidth disabled={sending}
              iconRight={!sending && <i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>}>
              {sending ? 'Отправляем...' : 'Отправить заявку'}
            </Button>
          </form>
        )}
      </div>
    </div>
  );
}

function LandingApp() {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [consultOpen, setConsultOpen] = React.useState(false);
  const openConsult = React.useCallback(() => setConsultOpen(true), []);
  React.useEffect(() => {
    window.__openConsult = openConsult;
    return () => { delete window.__openConsult; };
  }, [openConsult]);
  React.useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });
  React.useEffect(() => { document.body.style.overflow = menuOpen ? 'hidden' : ''; }, [menuOpen]);
  return (
    <React.Fragment>
      <Header onOpenMenu={() => setMenuOpen(true)} onOpenConsult={openConsult} />
      <MobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} onOpenConsult={openConsult} />
      <ConsultModal open={consultOpen} onClose={() => setConsultOpen(false)} />
      <main><LandingPage /></main>
      <Footer />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<LandingApp />);
setTimeout(() => window.lucide && window.lucide.createIcons(), 80);
"""

LANDING_PAGE_JS = r"""/* global React */
function LandingPage() {
  React.useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });

  const bannerSrc = window.__rv('banner', 'assets/photos/banner.jpg');

  const cards = [
    {
      flag: '🇬🇧',
      title: 'Виза в Великобританию',
      desc: '96% одобрений. Виза от 6 месяцев до 10 лет с многократным въездом. Один из самых надёжных вариантов для путешествий.',
      stat: [['96%', 'Одобрений'], ['10 лет', 'Макс. срок']],
      href: 'uk.html',
      glow: 'var(--glow-violet)',
    },
    {
      flag: '🇪🇺',
      title: 'Шенгенская виза',
      desc: '29 стран Европы по одной визе. Сложнее, чем раньше, но реально. Есть случаи выдачи на 2 года даже в 2026 году.',
      stat: [['29 стран', 'Шенгенской зоны'], ['до 2 лет', 'Срок визы']],
      href: 'schengen.html',
      glow: 'var(--glow-steel)',
    },
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '100px 20px 40px' }}>
      <div style={{ position: 'fixed', inset: 0, zIndex: -1, overflow: 'hidden', pointerEvents: 'none' }}>
        <div style={{ position: 'absolute', top: '10%', left: '20%', width: 600, height: 600, borderRadius: '50%', background: 'var(--grad-royal)', filter: 'blur(140px)', opacity: 0.12 }} />
        <div style={{ position: 'absolute', bottom: '10%', right: '15%', width: 500, height: 500, borderRadius: '50%', background: 'var(--grad-twilight)', filter: 'blur(120px)', opacity: 0.1 }} />
      </div>

      <div style={{ width: '100%', maxWidth: 760, marginBottom: 36 }}>
        <div style={{
          padding: 12, borderRadius: 'var(--r-2xl)',
          background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
          backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
          boxShadow: 'var(--elev-2), var(--glass-inner)',
        }}>
          <img
            src={bannerSrc}
            alt="Royal Visas"
            style={{ width: '100%', height: 'auto', display: 'block', borderRadius: 24 }}
          />
        </div>
      </div>

      <div style={{ textAlign: 'center', marginBottom: 36 }}>
        <h1 style={{ fontSize: 'var(--t-display)', letterSpacing: 'var(--track-tight)', lineHeight: 1.05 }}>
          Какая виза вас<br />
          <span style={{ background: 'var(--grad-royal)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>интересует?</span>
        </h1>
        <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)', maxWidth: 480, margin: '16px auto 0', lineHeight: 'var(--lh-relaxed)' }}>
          Помогаем оформить визу под ключ - от анкеты до подачи документов.
        </p>
      </div>

      <div className="rv-landing-cards" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 20, width: '100%', maxWidth: 760 }}>
        {cards.map((c) => (
          <a key={c.href} href={c.href} style={{ textDecoration: 'none', color: 'inherit', display: 'block' }}>
            <div
              className="rv-landing-card"
              style={{
                height: '100%', padding: 32, borderRadius: 'var(--r-2xl)',
                background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
                backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                boxShadow: 'var(--glass-shadow), var(--glass-inner)',
                display: 'flex', flexDirection: 'column',
                transition: 'border-color .22s ease, transform .22s ease, box-shadow .22s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'rgba(182,166,214,0.5)';
                e.currentTarget.style.transform = 'translateY(-5px)';
                e.currentTarget.style.boxShadow = c.glow + ', var(--glass-inner)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--glass-edge)';
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = 'var(--glass-shadow), var(--glass-inner)';
              }}
            >
              <div style={{ fontSize: 56, marginBottom: 20, lineHeight: 1 }}>{c.flag}</div>
              <h2 style={{ fontSize: 'var(--t-h3)', color: 'var(--text-strong)', marginBottom: 12 }}>{c.title}</h2>
              <p style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)', lineHeight: 1.6, flex: 1 }}>{c.desc}</p>

              <div style={{ display: 'flex', gap: 20, marginTop: 24, paddingTop: 20, borderTop: '1px solid var(--glass-edge-faint)' }}>
                {c.stat.map(([v, l]) => (
                  <div key={l}>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: 20, fontWeight: 600, color: 'var(--text-strong)' }}>{v}</div>
                    <div style={{ fontSize: 'var(--t-xs)', color: 'var(--text-muted)', marginTop: 2 }}>{l}</div>
                  </div>
                ))}
              </div>

              <div style={{ marginTop: 24, display: 'flex', alignItems: 'center', gap: 6, color: 'var(--accent-violet)', fontWeight: 600, fontSize: 'var(--t-sm)' }}>
                Узнать подробнее
                <i data-lucide="arrow-right" style={{ width: 16, height: 16 }}></i>
              </div>
            </div>
          </a>
        ))}
      </div>

      <p style={{ marginTop: 52, fontSize: 'var(--t-xs)', color: 'var(--text-muted)', textAlign: 'center', maxWidth: 520, lineHeight: 1.6 }}>
        Royal Visas - частный визовый сервис. Мы не являемся государственным органом
        и не аффилированы с UKVI или посольствами. Решение по визе принимает консульство.
      </p>
    </div>
  );
}

Object.assign(window, { LandingPage });
"""

# ─── build functions ──────────────────────────────────────────────────────────

SOURCE = '/home/user/ukvisa/uk.html'


def load_new_asset(uuid, path, mime, manifest):
    """Load a binary asset from disk and add/update it in the manifest."""
    manifest[uuid] = {
        'mime': mime,
        'compressed': True,
        'data': pack_binary(path),
    }


def build_uk():
    lines, manifest = load_bundle(SOURCE)

    # Updated wordmark (Royal Visas, no subtitle)
    manifest[UUID_WORDMARK]['data'] = pack(WORDMARK_SVG)

    # Updated header + mobile menu
    manifest[UUID_HEADER]['data'] = pack(HEADER_JS)

    # Updated footer
    manifest[UUID_FOOTER]['data'] = pack(FOOTER_JS)

    # Updated app with ConsultModal
    manifest[UUID_APP]['data'] = pack(APP_JS)

    # ConsultForm with promo codes
    manifest[UUID_CONSULT]['data'] = pack(inject_promos(CONSULT_FORM_UK))

    # Services with 29 990
    manifest[UUID_SERVICES]['data'] = pack(SERVICES_29990)

    # Favicon
    favicon_path = os.path.join(ASSET_DIR, 'favicon.png')
    if os.path.exists(favicon_path):
        load_new_asset(UUID_FAVICON, favicon_path, 'image/png', manifest)

    ext_resources = [
        {'id': 'wordmark', 'uuid': UUID_WORDMARK},
        {'id': 'bigben', 'uuid': UUID_BIGBEN},
        {'id': 'ukmap', 'uuid': UUID_UKMAP},
        {'id': 'towerbridge', 'uuid': UUID_TOWERBRIDGE},
    ]

    write_bundle(lines, manifest, '/home/user/ukvisa/uk.html',
                 'Royal Visas - Визы в Великобританию',
                 ext_resources=ext_resources,
                 favicon_uuid=UUID_FAVICON)


def build_schengen():
    lines, manifest = load_bundle(SOURCE)

    # Updated wordmark
    manifest[UUID_WORDMARK]['data'] = pack(WORDMARK_SVG)

    # Updated header + mobile menu
    manifest[UUID_HEADER]['data'] = pack(HEADER_JS)

    # Updated footer
    manifest[UUID_FOOTER]['data'] = pack(FOOTER_JS)

    # Updated app with ConsultModal
    manifest[UUID_APP]['data'] = pack(APP_JS)

    # Hero with paris.jpg
    manifest[UUID_HERO]['data'] = pack(SCHENGEN_HERO)

    # AboutVisa - Schengen version
    manifest[UUID_ABOUT]['data'] = pack(SCHENGEN_ABOUT)

    # SchengenMap with pixel-color detection
    manifest[UUID_MAP]['data'] = pack(SCHENGEN_MAP)

    # Schengen services with 90 EUR fee
    manifest[UUID_SERVICES]['data'] = pack(SCHENGEN_SERVICES)

    # ConsultForm with promo codes and Schengen label
    manifest[UUID_CONSULT]['data'] = pack(inject_promos(SCHENGEN_CONSULT_FORM))

    # Paris photo
    paris_path = os.path.join(ASSET_DIR, 'paris.jpg')
    if os.path.exists(paris_path):
        load_new_asset(UUID_PARIS, paris_path, 'image/jpeg', manifest)

    # Schengen map
    map_path = os.path.join(ASSET_DIR, 'map.jpg')
    if os.path.exists(map_path):
        load_new_asset(UUID_SCHENGENMAP, map_path, 'image/jpeg', manifest)

    # Favicon
    favicon_path = os.path.join(ASSET_DIR, 'favicon.png')
    if os.path.exists(favicon_path):
        load_new_asset(UUID_FAVICON, favicon_path, 'image/png', manifest)

    ext_resources = [
        {'id': 'wordmark', 'uuid': UUID_WORDMARK},
        {'id': 'paris', 'uuid': UUID_PARIS},
        {'id': 'schengenmap', 'uuid': UUID_SCHENGENMAP},
    ]

    write_bundle(lines, manifest, '/home/user/ukvisa/schengen.html',
                 'Royal Visas - Шенгенская виза',
                 ext_resources=ext_resources,
                 favicon_uuid=UUID_FAVICON)


def build_index():
    lines, manifest = load_bundle(SOURCE)

    # Updated header + footer so landing page has nav
    manifest[UUID_HEADER]['data'] = pack(HEADER_JS)
    manifest[UUID_FOOTER]['data'] = pack(FOOTER_JS)

    # Landing page: LandingPage component + full app wrapper with nav
    manifest[UUID_APP]['data'] = pack(LANDING_PAGE_JS + '\n' + LANDING_APP)

    # Updated wordmark
    manifest[UUID_WORDMARK]['data'] = pack(WORDMARK_SVG)

    # Banner photo
    banner_path = os.path.join(ASSET_DIR, 'banner.jpg')
    if os.path.exists(banner_path):
        load_new_asset(UUID_BANNER, banner_path, 'image/jpeg', manifest)

    # Favicon
    favicon_path = os.path.join(ASSET_DIR, 'favicon.png')
    if os.path.exists(favicon_path):
        load_new_asset(UUID_FAVICON, favicon_path, 'image/png', manifest)

    # Remove heavy assets not used on landing page
    for uuid_to_remove in [UUID_BIGBEN, UUID_TOWERBRIDGE, UUID_UKMAP]:
        if uuid_to_remove in manifest:
            del manifest[uuid_to_remove]

    ext_resources = [
        {'id': 'wordmark', 'uuid': UUID_WORDMARK},
        {'id': 'banner', 'uuid': UUID_BANNER},
    ]

    write_bundle(lines, manifest, '/home/user/ukvisa/index.html',
                 'Royal Visas - Визовый сервис',
                 ext_resources=ext_resources,
                 favicon_uuid=UUID_FAVICON)


# ─── run ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    build_uk()
    build_schengen()
    build_index()
    print('\nAll done!')
    print('\nPromo codes (30 one-time, -5 000 руб.):')
    for c in PROMO_CODES:
        print(' ', c)
    print('  KRISKISS (valid until 2026-10-01)')
