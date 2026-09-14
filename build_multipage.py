#!/usr/bin/env python3
"""
Builds uk.html, schengen.html, and index.html as clean static files.
No bundler, no runtime unpacking. Assets are served as regular files.
"""
import json, os, re

PROMO_CODES = [
    "1BC8BO99","XSXPA5S6","GYYHMKDL","1FL4J218","BG75BX8M","1APDNR8A","01UYIY5S",
    "GETQ2CJC","8R02U4F8","NMI544QI","Z20F02YF","TCN96F2B","5WRTJCDA","CFCS67U0",
    "XV44AZCL","AEAA6CPF","7HB296TT","0LMEH0JQ","0TQ9H4DE","UIMJY7X9","Z9FHW1IW",
    "9NLOATHO","SZ7N356G","XPQ1XXM5","ZE8LLTOL","FPI2LBBS","F7KBOTS6","QLP2SF23",
    "U1K8J8VR","Q1WRNMM5",
]

# ─── HTML shell ───────────────────────────────────────────────────────────────

HTML_SHELL = """\
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="icon" type="image/png" href="assets/favicon.png">
  <link rel="stylesheet" href="assets/css/styles.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js" crossorigin></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.26.5/babel.min.js" crossorigin></script>
  <script src="https://cdn.jsdelivr.net/npm/lucide@1.22.0/dist/umd/lucide.min.js" crossorigin></script>
  <script src="assets/js/design-system.js"></script>
</head>
<body>
  <div id="root"></div>
{scripts}
</body>
</html>
"""

def make_script(js: str) -> str:
    return f'  <script type="text/babel">\n{js}\n  </script>'

def write_page(out_path: str, title: str, scripts: list[str]):
    body = '\n'.join(make_script(s) for s in scripts)
    html = HTML_SHELL.format(title=title, scripts=body)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Written: {out_path}')

# ─── shared components ────────────────────────────────────────────────────────

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

WORDMARK_DATA_URI = 'data:image/svg+xml;base64,' + __import__('base64').b64encode(WORDMARK_SVG.encode()).decode()

HEADER_JS = r"""
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
          <img src="assets/logo/wordmark.svg" alt="Royal Visas" style={{ height: 40 }} />
        </a>
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
        backdropFilter: open ? 'blur(28px) saturate(140%)' : 'none',
        WebkitBackdropFilter: open ? 'blur(28px) saturate(140%)' : 'none',
        opacity: open ? 1 : 0, transition: 'opacity .32s ease',
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
"""

FOOTER_JS = r"""
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
            <img src="assets/logo/wordmark.svg" alt="Royal Visas" style={{ height: 40 }} />
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
"""

CONSULT_MODAL_JS = r"""
function ConsultModal({ open, onClose, visaLabel }) {
  const TG_TOKEN = '8677081622:AAHAvOYbY50uCZnx9QimTXDO98CYJnMnvxA';
  const TG_CHAT_ID = '-5235367527';
  const VISA_LABEL = visaLabel || '📋 Новая заявка - Royal Visas';
  const PROMO_DISCOUNT = 5000;
  const PROMO_CODES_LIST = window.__promoCodes || [];

  const { Button, Input, Switch } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [visible, setVisible] = React.useState(false);
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
    if (open) { setVisible(true); return; }
    const t = setTimeout(() => setVisible(false), 350);
    return () => clearTimeout(t);
  }, [open]);

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

  if (!visible) return null;

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
        backdropFilter: open ? 'blur(24px) saturate(140%)' : 'none',
        WebkitBackdropFilter: open ? 'blur(24px) saturate(140%)' : 'none',
        opacity: open ? 1 : 0, transition: 'opacity .28s ease, backdrop-filter .28s ease',
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

        <div style={{ padding: '20px 8px 8px' }}>
          <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 20px' }}>
            <span className="rv-eyebrow">Бесплатная консультация</span>
            <p style={{ marginTop: 10, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
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
"""

CONSULT_FORM_JS = r"""
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

function ConsultForm({ visaLabel }) {
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
  const VISA_LABEL = visaLabel || '📋 Новая заявка - Royal Visas';
  const PROMO_DISCOUNT = 5000;
  const PROMO_CODES_LIST = window.__promoCodes || [];

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

  const switchChannel = (c) => { setChannel(c); setContact(''); setError(''); };

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

        <div style={{ maxWidth: 940, margin: '0 auto', padding: 8, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--elev-3), var(--glass-inner)' }}>
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
    </section>
  );
}
"""

# ─── UK page components ───────────────────────────────────────────────────────

UK_HERO_JS = r"""
function Hero() {
  const { Button, Badge } = window.RoyalVisaUKDesignSystem_ccc97c;
  return (
    <section id="top" style={{ position: 'relative', paddingTop: 132, paddingBottom: 96 }}>
      <div className="rv-container">
        <div className="rv-hero-grid" style={{ display: 'grid', gridTemplateColumns: '1.05fr 0.95fr', gap: 56, alignItems: 'center' }}>
          <div className="rv-hero-copy">
            <div style={{ marginBottom: 22 }}>
              <Badge tone="accent" dot>Виза в Великобританию · с 2022 года</Badge>
            </div>
            <h1 style={{ fontSize: 'var(--t-display)', letterSpacing: 'var(--track-tight)', lineHeight: 1.02 }}>
              Виза в UK<br />
              <span style={{ background: 'var(--grad-royal)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>с гарантией качества</span>
            </h1>
            <p className="rv-hero-lead" style={{ marginTop: 22, fontSize: 'var(--t-lg)', color: 'var(--text-body)', maxWidth: 520, lineHeight: 'var(--lh-relaxed)' }}>
              Помогаем оформить визу в Великобританию под ключ - от анкеты до подачи. 96% одобрений.
            </p>
            <div className="rv-hero-actions" style={{ marginTop: 32, display: 'flex', gap: 14, flexWrap: 'wrap' }}>
              <Button variant="primary" size="lg" iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>} onClick={() => { if (window.__openConsult) window.__openConsult(); }}>
                Бесплатная консультация
              </Button>
              <Button variant="secondary" size="lg" onClick={(e) => { e.preventDefault(); const el = document.getElementById('services'); if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 84, behavior: 'smooth' }); }}>Стоимость</Button>
            </div>
            <div className="rv-hero-stats" style={{ marginTop: 40, display: 'flex', gap: 36, flexWrap: 'wrap' }}>
              {[['96%', 'Одобрений виз'], ['10 лет', 'Макс. срок визы'], ['3–5 дней', 'Оформление']].map(([v, l]) => (
                <div key={l}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: 28, fontWeight: 500, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{v}</div>
                  <div style={{ fontSize: 'var(--t-sm)', color: 'var(--text-muted)', marginTop: 2 }}>{l}</div>
                </div>
              ))}
            </div>
          </div>
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', inset: -30, borderRadius: '50%', background: 'var(--grad-royal)', filter: 'blur(60px)', opacity: 0.42, zIndex: 0 }} />
            <div style={{ position: 'relative', zIndex: 1, padding: 12, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', boxShadow: 'var(--elev-3), var(--glass-inner)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)' }}>
              <img src="assets/photos/bigben.jpg" alt="Биг-Бен, Лондон" style={{ display: 'block', width: '100%', height: 'auto', borderRadius: 24 }} />
              <div style={{ position: 'absolute', left: 26, bottom: 26, display: 'inline-flex', alignItems: 'center', gap: 10, padding: '12px 16px', borderRadius: 'var(--r-pill)', background: 'var(--glass-fill-solid)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-inner)' }}>
                <i data-lucide="map-pin" style={{ width: 16, height: 16, color: 'var(--accent-violet)' }}></i>
                <span style={{ fontSize: 'var(--t-sm)', color: 'var(--text-strong)', fontWeight: 500 }}>Биг-Бен, Лондон</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
"""

UK_ABOUT_JS = r"""
function AboutVisa() {
  const { Badge } = window.RoyalVisaUKDesignSystem_ccc97c;
  const points = [
    { icon: 'calendar-check', title: 'Виза от 6 месяцев до 10 лет', text: 'Туристическая виза с многократным въездом - выбирайте срок под свои планы поездок.' },
    { icon: 'globe', title: 'Вся Великобритания', text: 'Англия, Шотландия, Уэльс, Северная Ирландия - одна виза для всей страны.' },
    { icon: 'shield-check', title: '96% одобрений', text: 'Правильно собранный пакет документов - главный фактор успеха. Берём это на себя.' },
  ];
  return (
    <section id="about" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div className="rv-about-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 56, alignItems: 'center' }}>
          <div>
            <div style={{ position: 'relative', padding: 12, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', boxShadow: 'var(--elev-2), var(--glass-inner)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)' }}>
              <img src="assets/photos/towerbridge.jpg" alt="Тауэрский мост" style={{ display: 'block', width: '100%', height: 'auto', borderRadius: 20 }} />
            </div>
          </div>
          <div className="rv-about-copy">
            <div style={{ marginBottom: 18 }}>
              <span className="rv-eyebrow">О визе</span>
            </div>
            <h2 style={{ fontSize: 'var(--t-h2)' }}>Великобритания открыта для вас</h2>
            <p style={{ marginTop: 18, fontSize: 'var(--t-lg)', color: 'var(--text-body)', lineHeight: 'var(--lh-relaxed)' }}>
              Британская туристическая виза - один из самых надёжных вариантов для путешествий. Правильно оформленный пакет документов существенно повышает шансы на одобрение.
            </p>
            <div className="rv-about-points" style={{ marginTop: 28, display: 'flex', flexDirection: 'column', gap: 12 }}>
              {points.map((p) => (
                <div key={p.title} style={{ display: 'flex', gap: 16, padding: 18, borderRadius: 'var(--r-lg)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-inner-soft)' }}>
                  <div style={{ flex: 'none', width: 44, height: 44, borderRadius: 'var(--r-md)', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--glass-tint-violet)', border: '1px solid var(--glass-edge)' }}>
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
"""

UK_MAP_JS = r"""
const UK_NATIONS = {
  scotland: { name: 'Шотландия', capital: 'Эдинбург', accent: '#4d74d6', ref: [60, 100, 200],
    note: 'Хайленд, виски и замки. Та же виза - без отдельного разрешения.' },
  england: { name: 'Англия', capital: 'Лондон', accent: '#ef6a33', ref: [228, 85, 29],
    note: 'Лондон, Оксфорд, побережье. Сердце поездки по одной визе.' },
  wales: { name: 'Уэльс', capital: 'Кардифф', accent: '#f0c419', ref: [237, 196, 22],
    note: 'Горы Сноудонии и старинные крепости - и снова без доплат.' },
  ni: { name: 'Северная Ирландия', capital: 'Белфаст', accent: '#56b061', ref: [86, 160, 84],
    note: 'Та же виза действует и здесь - Дорога гигантов ждёт.' },
};
const NATION_ORDER = ['scotland', 'england', 'wales', 'ni'];

function NationInfo({ id, active, onHover, align }) {
  const n = UK_NATIONS[id];
  const on = active === id;
  const dim = active && !on;
  return (
    <div
      className="rv-nation"
      onMouseEnter={() => onHover(id)}
      onMouseLeave={() => onHover(null)}
      style={{
        padding: 18, borderRadius: 'var(--r-lg)', cursor: 'default',
        textAlign: align === 'right' ? 'right' : 'left',
        background: on ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
        border: `1px solid ${on ? n.accent : 'var(--glass-edge)'}`,
        backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
        boxShadow: on ? `0 8px 30px -8px ${n.accent}, var(--glass-inner)` : 'var(--glass-inner-soft)',
        transform: on ? 'translateY(-2px)' : 'none',
        opacity: dim ? 0.55 : 1,
        transition: 'all .22s ease',
      }}
    >
      <div className="rv-nation-head" style={{ display: 'flex', alignItems: 'center', gap: 9, justifyContent: align === 'right' ? 'flex-end' : 'flex-start' }}>
        <span style={{ width: 10, height: 10, borderRadius: '50%', background: n.accent, flex: 'none', boxShadow: '0 0 10px ' + n.accent }}></span>
        <span style={{ color: 'var(--text-strong)', fontWeight: 600, fontSize: 'var(--t-h4)' }}>{n.name}</span>
      </div>
      <div style={{ marginTop: 6, fontSize: 'var(--t-xs)', letterSpacing: 'var(--track-eyebrow)', textTransform: 'uppercase', color: n.accent, fontWeight: 600 }}>
        Столица · {n.capital}
      </div>
      <p style={{ margin: '8px 0 0', fontSize: 'var(--t-sm)', color: 'var(--text-muted)', lineHeight: 1.5 }}>{n.note}</p>
    </div>
  );
}

function InteractiveUKMap({ active, setActive }) {
  const wrapRef = React.useRef(null);
  const overlayRef = React.useRef(null);
  const dataRef = React.useRef({ ready: false, labels: null, masks: {}, w: 0, h: 0 });
  const [ready, setReady] = React.useState(false);

  React.useEffect(() => {
    let cancelled = false;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      try {
        const w = 360, h = Math.round(360 * img.naturalHeight / img.naturalWidth);
        const c = document.createElement('canvas'); c.width = w; c.height = h;
        const ctx = c.getContext('2d'); ctx.drawImage(img, 0, 0, w, h);
        const data = ctx.getImageData(0, 0, w, h).data;
        const labels = new Uint8Array(w * h);
        const refs = NATION_ORDER.map((id) => UK_NATIONS[id].ref);
        const TH = 115 * 115;
        for (let i = 0; i < w * h; i++) {
          if (data[i * 4 + 3] < 128) { labels[i] = 0; continue; }
          const r = data[i * 4], g = data[i * 4 + 1], b = data[i * 4 + 2];
          let best = 0, bestD = TH;
          for (let k = 0; k < 4; k++) {
            const dr = r - refs[k][0], dg = g - refs[k][1], db = b - refs[k][2];
            const d = dr * dr + dg * dg + db * db;
            if (d < bestD) { bestD = d; best = k + 1; }
          }
          labels[i] = best;
        }
        const masks = {};
        NATION_ORDER.forEach((id, idx) => {
          const mc = document.createElement('canvas'); mc.width = w; mc.height = h;
          const mctx = mc.getContext('2d');
          const out = mctx.createImageData(w, h); const md = out.data;
          for (let i = 0; i < w * h; i++) {
            if (labels[i] === idx + 1) {
              md[i * 4] = data[i * 4]; md[i * 4 + 1] = data[i * 4 + 1];
              md[i * 4 + 2] = data[i * 4 + 2]; md[i * 4 + 3] = 255;
            }
          }
          mctx.putImageData(out, 0, 0);
          masks[id] = mc;
        });
        if (cancelled) return;
        dataRef.current = { ready: true, labels, masks, w, h };
        setReady(true);
      } catch (e) {
        dataRef.current.ready = false;
        setReady(true);
      }
    };
    img.src = "assets/photos/ukmap.png";
    return () => { cancelled = true; };
  }, []);

  React.useEffect(() => {
    const d = dataRef.current; const cv = overlayRef.current;
    if (!cv || !d.ready) return;
    if (cv.width !== d.w) { cv.width = d.w; cv.height = d.h; }
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, d.w, d.h);
    if (active && d.masks[active]) ctx.drawImage(d.masks[active], 0, 0);
  }, [active, ready]);

  const onMove = (e) => {
    const d = dataRef.current; if (!d.ready || !wrapRef.current) return;
    const rect = wrapRef.current.getBoundingClientRect();
    const fx = (e.clientX - rect.left) / rect.width, fy = (e.clientY - rect.top) / rect.height;
    if (fx < 0 || fx > 1 || fy < 0 || fy > 1) { setActive(null); return; }
    const px = Math.min(d.w - 1, Math.floor(fx * d.w)), py = Math.min(d.h - 1, Math.floor(fy * d.h));
    const L = d.labels[py * d.w + px];
    setActive(L ? NATION_ORDER[L - 1] : null);
  };

  return (
    <div
      ref={wrapRef}
      onMouseMove={onMove}
      onMouseLeave={() => setActive(null)}
      style={{ position: 'relative', width: '100%', maxWidth: 300, margin: '0 auto' }}
    >
      <div style={{ position: 'absolute', inset: '8% 12%', borderRadius: '50%', background: 'var(--grad-royal)', filter: 'blur(70px)', opacity: 0.3, zIndex: 0 }}></div>
      <img
        src="assets/photos/ukmap.png"
        alt="Карта Великобритании - четыре части"
        style={{
          position: 'relative', zIndex: 1, display: 'block', width: '100%', height: 'auto',
          filter: active
            ? 'drop-shadow(0 16px 40px rgba(0,0,0,0.55)) brightness(0.45) saturate(0.8)'
            : 'drop-shadow(0 16px 40px rgba(0,0,0,0.55))',
          transition: 'filter .25s ease',
        }}
      />
      <canvas
        ref={overlayRef}
        style={{
          position: 'absolute', inset: 0, zIndex: 2, width: '100%', height: '100%', pointerEvents: 'none',
          filter: active ? `drop-shadow(0 0 16px ${UK_NATIONS[active].accent})` : 'none',
          transition: 'filter .2s ease',
        }}
      ></canvas>
    </div>
  );
}

function UKMap() {
  const [active, setActive] = React.useState(null);
  return (
    <section id="map" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 680, margin: '0 auto 12px' }}>
          <span className="rv-eyebrow">Виза UK</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Одна виза&nbsp;- четыре разных мира</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            Мало кто знает: одна британская виза открывает все четыре части Королевства.
            Англия, Шотландия, Уэльс и Северная Ирландия&nbsp;- без отдельных разрешений.
          </p>
        </div>

        <div className="rv-map-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1.05fr 1fr', gap: 28, alignItems: 'center', marginTop: 36 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <NationInfo id="scotland" active={active} onHover={setActive} align="right" />
            <NationInfo id="ni" active={active} onHover={setActive} align="right" />
          </div>

          <InteractiveUKMap active={active} setActive={setActive} />

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <NationInfo id="england" active={active} onHover={setActive} align="left" />
            <NationInfo id="wales" active={active} onHover={setActive} align="left" />
          </div>
        </div>
      </div>
    </section>
  );
}
"""

UK_SERVICES_JS = r"""
const CONSULAR_FEES = [
  { label: 'Туристическая виза на 6 месяцев', price: '150 £' },
  { label: 'Туристическая виза на 2 года', price: '550 £' },
  { label: 'Туристическая виза на 5 лет', price: '980 £' },
  { label: 'Туристическая виза на 10 лет', price: '1250 £' },
];

function FeeLink({ onOpen }) {
  return (
    <button onClick={onOpen} style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: 0, background: 'none', border: 'none', cursor: 'pointer', font: 'inherit', color: 'var(--accent-sky)', fontWeight: 600, textDecoration: 'underline', textUnderlineOffset: 3, textDecorationColor: 'rgba(185,210,230,0.45)' }}>
      консульский сбор<i data-lucide="info" style={{ width: 14, height: 14 }}></i>
    </button>
  );
}

function FeeModal({ open, onClose }) {
  const [visible, setVisible] = React.useState(false);
  React.useEffect(() => {
    if (open) { setVisible(true); return; }
    const t = setTimeout(() => setVisible(false), 350); return () => clearTimeout(t);
  }, [open]);
  React.useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);
  if (!visible) return null;
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20, pointerEvents: open ? 'auto' : 'none' }}>
      <div onClick={onClose} style={{ position: 'absolute', inset: 0, background: 'rgba(8,7,13,0.55)', backdropFilter: open ? 'blur(20px) saturate(140%)' : 'none', WebkitBackdropFilter: open ? 'blur(20px) saturate(140%)' : 'none', opacity: open ? 1 : 0, transition: 'opacity .28s ease' }} />
      <div role="dialog" aria-modal="true" style={{ position: 'relative', width: '100%', maxWidth: 480, padding: 28, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill-strong)', border: '1px solid var(--glass-edge-strong)', backdropFilter: 'var(--glass-blur-heavy)', WebkitBackdropFilter: 'var(--glass-blur-heavy)', boxShadow: 'var(--elev-4), var(--glass-inner)', transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.96)', opacity: open ? 1 : 0, transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease' }}>
        <button aria-label="Закрыть" onClick={onClose} style={{ position: 'absolute', top: 16, right: 16, width: 36, height: 36, cursor: 'pointer', borderRadius: 'var(--r-sm)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <i data-lucide="x" style={{ width: 18, height: 18, color: 'var(--text-strong)' }}></i>
        </button>
        <div style={{ width: 46, height: 46, borderRadius: 'var(--r-md)', marginBottom: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--glass-tint-sky)', border: '1px solid var(--glass-edge)' }}>
          <i data-lucide="credit-card" style={{ width: 22, height: 22, color: 'var(--accent-sky)' }}></i>
        </div>
        <p style={{ margin: 0, fontSize: 'var(--t-lg)', color: 'var(--text-strong)', lineHeight: 1.45, fontWeight: 500 }}>
          Консульский сбор оплачивается зарубежной банковской картой. Если у вас такой нет - мы поможем оплатить.
        </p>
        <div style={{ marginTop: 22, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {CONSULAR_FEES.map((f, i) => (
            <div key={f.label} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, padding: '14px 4px', borderTop: i === 0 ? 'none' : '1px solid var(--glass-edge-faint)' }}>
              <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)' }}>{f.label}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--t-lg)', fontWeight: 600, color: 'var(--text-strong)', whiteSpace: 'nowrap' }}>{f.price}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Services() {
  const { Button } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [feeOpen, setFeeOpen] = React.useState(false);
  const tariff = {
    name: 'Всё включено',
    tagline: 'Берём весь процесс на себя - от анкеты до подачи.',
    price: '29 990',
    features: [
      'Заполняем анкету за вас',
      'Готовим полный пакет документов',
      'Помогаем поймать слот в визовый центр на подачу документов',
    ],
  };
  return (
    <section id="services" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">Стоимость</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Всё включено</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>Берём весь процесс на себя - вам остаётся только прийти на подачу.</p>
        </div>
        <div style={{ maxWidth: 760, margin: '0 auto', position: 'relative', padding: 30, borderRadius: 'var(--r-xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-shadow), var(--glass-inner)', display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ fontSize: 'var(--t-h3)' }}>{tariff.name}</h3>
          <p style={{ marginTop: 8, color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>{tariff.tagline}</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 22, marginBottom: 24 }}>
            {tariff.features.map((f) => (
              <div key={f} style={{ display: 'flex', gap: 11, alignItems: 'flex-start' }}>
                <i data-lucide="check" style={{ width: 18, height: 18, marginTop: 2, flex: 'none', color: 'var(--success)' }}></i>
                <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)', lineHeight: 1.45 }}>{f}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 'auto', paddingTop: 20, borderTop: '1px solid var(--glass-edge-faint)' }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, flexWrap: 'wrap' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 34, fontWeight: 600, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{tariff.price}</span>
              <span style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>руб.</span>
            </div>
            <div style={{ marginTop: 6, fontSize: 'var(--t-sm)', color: 'var(--text-muted)' }}>+ <FeeLink onOpen={() => setFeeOpen(true)} /></div>
            <div style={{ marginTop: 22 }}>
              <Button variant="secondary" fullWidth size="lg" iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>} onClick={() => { if (window.__openConsult) window.__openConsult(); }}>
                Записаться на консультацию
              </Button>
            </div>
          </div>
        </div>
      </div>
      <FeeModal open={feeOpen} onClose={() => setFeeOpen(false)} />
    </section>
  );
}
"""

def uk_app_js(promo_codes):
    return f"""
window.__promoCodes = {json.dumps(promo_codes)};

function App() {{
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [consultOpen, setConsultOpen] = React.useState(false);
  const openConsult = React.useCallback(() => setConsultOpen(true), []);
  React.useEffect(() => {{
    window.__openConsult = openConsult;
    return () => {{ delete window.__openConsult; }};
  }}, [openConsult]);
  React.useEffect(() => {{
    if (window.lucide) window.lucide.createIcons();
  }});
  React.useEffect(() => {{ document.body.style.overflow = menuOpen ? 'hidden' : ''; }}, [menuOpen]);
  return (
    <React.Fragment>
      <Header onOpenMenu={{() => setMenuOpen(true)}} onOpenConsult={{openConsult}} />
      <MobileMenu open={{menuOpen}} onClose={{() => setMenuOpen(false)}} onOpenConsult={{openConsult}} />
      <ConsultModal open={{consultOpen}} onClose={{() => setConsultOpen(false)}} visaLabel="🇬🇧 Новая заявка - Royal Visas" />
      <main>
        <Hero />
        <AboutVisa />
        <UKMap />
        <Services />
        <ConsultForm visaLabel="🇬🇧 Новая заявка - Royal Visas" />
      </main>
      <Footer />
    </React.Fragment>
  );
}}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
setTimeout(() => window.lucide && window.lucide.createIcons(), 80);
"""

# ─── Schengen page components ─────────────────────────────────────────────────

SCHENGEN_HERO_JS = r"""
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
              Шенген в 2026<br />
              <span style={{ background: 'var(--grad-royal)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>это реально</span>
            </h1>
            <p className="rv-hero-lead" style={{ marginTop: 22, fontSize: 'var(--t-lg)', color: 'var(--text-body)', maxWidth: 520, lineHeight: 'var(--lh-relaxed)' }}>
              Получить шенген сложнее, чем раньше, но реально. Поможем оформить визу в Европу под ключ.
            </p>
            <div className="rv-hero-actions" style={{ marginTop: 32, display: 'flex', gap: 14, flexWrap: 'wrap' }}>
              <Button variant="primary" size="lg" iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>} onClick={(e) => go(e, '#consult')}>
                Бесплатная консультация
              </Button>
              <Button variant="secondary" size="lg" onClick={(e) => go(e, '#services')}>Стоимость</Button>
            </div>
            <div className="rv-hero-stats" style={{ marginTop: 40, display: 'flex', gap: 36, flexWrap: 'wrap' }}>
              {[['≈ 70%', 'Одобрений виз'], ['до 2 лет', 'Срок визы'], ['3–4 нед.', 'Решение по заявке']].map(([v, l]) => (
                <div key={l}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: 28, fontWeight: 500, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{v}</div>
                  <div style={{ fontSize: 'var(--t-sm)', color: 'var(--text-muted)', marginTop: 2 }}>{l}</div>
                </div>
              ))}
            </div>
          </div>
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', inset: -30, borderRadius: '50%', background: 'var(--grad-royal)', filter: 'blur(60px)', opacity: 0.42, zIndex: 0 }} />
            <div style={{ position: 'relative', zIndex: 1, padding: 12, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', boxShadow: 'var(--elev-3), var(--glass-inner)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)' }}>
              <img src="assets/photos/paris.jpg" alt="Эйфелева башня, Париж" style={{ display: 'block', width: '100%', height: 'auto', borderRadius: 24 }} />
              <div style={{ position: 'absolute', left: 26, bottom: 26, display: 'inline-flex', alignItems: 'center', gap: 10, padding: '12px 16px', borderRadius: 'var(--r-pill)', background: 'var(--glass-fill-solid)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-inner)' }}>
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
"""

SCHENGEN_ABOUT_JS = r"""
function AboutVisa() {
  const points = [
    { icon: 'calendar-check', title: 'Выдают даже на 2 года', text: 'В 2026 году есть случаи выдачи шенгена на 2 года с многократным въездом.' },
    { icon: 'globe', title: '27 стран по одной визе', text: 'Германия, Франция, Италия, Испания и ещё 23 страны - все по одному разрешению без дополнительных сборов.' },
    { icon: 'shield-check', title: 'Помогаем даже в сложных случаях', text: 'Знаем актуальные требования консульств и собираем убедительный пакет документов.' },
  ];
  return (
    <section id="about" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div className="rv-about-copy">
          <div style={{ marginBottom: 18 }}><span className="rv-eyebrow">О визе</span></div>
          <h2 style={{ fontSize: 'var(--t-h2)' }}>Европа открыта - в наше время</h2>
          <p style={{ marginTop: 18, fontSize: 'var(--t-lg)', color: 'var(--text-body)', lineHeight: 'var(--lh-relaxed)' }}>
            Шенген получить сложнее, чем раньше, но путешествовать по Европе в 2026 году - это реально. Правильно собранный пакет документов значительно повышает шансы на одобрение.
          </p>
          <div className="rv-about-points" style={{ marginTop: 28, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12 }}>
            {points.map((p) => (
              <div key={p.title} style={{ display: 'flex', gap: 16, padding: 18, borderRadius: 'var(--r-lg)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-inner-soft)' }}>
                <div style={{ flex: 'none', width: 44, height: 44, borderRadius: 'var(--r-md)', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--glass-tint-violet)', border: '1px solid var(--glass-edge)' }}>
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
    </section>
  );
}
"""

SCHENGEN_MAP_JS = r"""
const SCHENGEN_GEO_GROUPS = [
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
  const [hoveredId, setHoveredId] = React.useState(null);
  return (
    <section id="map" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 680, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">Шенгенская зона</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Одна виза - вся Европа</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>29 стран шенгенской зоны. Одна виза даёт доступ ко всем - без отдельных разрешений.</p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
          {SCHENGEN_GEO_GROUPS.map((geo) => (
            <div key={geo.label}>
              <div style={{ fontSize: 'var(--t-sm)', fontWeight: 600, letterSpacing: 'var(--track-eyebrow)', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 14 }}>{geo.label}</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {geo.countries.map((c) => {
                  const on = hoveredId === c.id;
                  return (
                    <div key={c.id} onMouseEnter={() => setHoveredId(c.id)} onMouseLeave={() => setHoveredId(null)} style={{ padding: '10px 16px', borderRadius: 'var(--r-lg)', display: 'flex', alignItems: 'center', gap: 10, background: on ? 'var(--glass-fill-strong)' : 'var(--glass-fill)', border: `1px solid ${on ? 'rgba(182,166,214,0.5)' : 'var(--glass-edge)'}`, backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: on ? 'var(--glow-violet), var(--glass-inner)' : 'var(--glass-inner-soft)', transform: on ? 'translateY(-2px)' : 'none', cursor: 'default', transition: 'all .18s ease' }}>
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
          ))}
        </div>
      </div>
    </section>
  );
}
"""

SCHENGEN_SERVICES_JS = r"""
const SCHENGEN_CONSULAR_FEES = [
  { label: 'Краткосрочная шенгенская виза (стандарт)', price: '90 €' },
  { label: 'Дети до 6 лет', price: 'Бесплатно' },
  { label: 'Дети 6–12 лет', price: '45 €' },
];

function FeeLink({ onOpen }) {
  return (
    <button onClick={onOpen} style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: 0, background: 'none', border: 'none', cursor: 'pointer', font: 'inherit', color: 'var(--accent-sky)', fontWeight: 600, textDecoration: 'underline', textUnderlineOffset: 3, textDecorationColor: 'rgba(185,210,230,0.45)' }}>
      консульский сбор<i data-lucide="info" style={{ width: 14, height: 14 }}></i>
    </button>
  );
}

function FeeModal({ open, onClose }) {
  const [visible, setVisible] = React.useState(false);
  React.useEffect(() => {
    if (open) { setVisible(true); return; }
    const t = setTimeout(() => setVisible(false), 350); return () => clearTimeout(t);
  }, [open]);
  React.useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);
  if (!visible) return null;
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20, pointerEvents: open ? 'auto' : 'none' }}>
      <div onClick={onClose} style={{ position: 'absolute', inset: 0, background: 'rgba(8,7,13,0.55)', backdropFilter: open ? 'blur(20px) saturate(140%)' : 'none', WebkitBackdropFilter: open ? 'blur(20px) saturate(140%)' : 'none', opacity: open ? 1 : 0, transition: 'opacity .28s ease' }} />
      <div role="dialog" aria-modal="true" style={{ position: 'relative', width: '100%', maxWidth: 480, padding: 28, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill-strong)', border: '1px solid var(--glass-edge-strong)', backdropFilter: 'var(--glass-blur-heavy)', WebkitBackdropFilter: 'var(--glass-blur-heavy)', boxShadow: 'var(--elev-4), var(--glass-inner)', transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.96)', opacity: open ? 1 : 0, transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease' }}>
        <button aria-label="Закрыть" onClick={onClose} style={{ position: 'absolute', top: 16, right: 16, width: 36, height: 36, cursor: 'pointer', borderRadius: 'var(--r-sm)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <i data-lucide="x" style={{ width: 18, height: 18, color: 'var(--text-strong)' }}></i>
        </button>
        <div style={{ width: 46, height: 46, borderRadius: 'var(--r-md)', marginBottom: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--glass-tint-sky)', border: '1px solid var(--glass-edge)' }}>
          <i data-lucide="credit-card" style={{ width: 22, height: 22, color: 'var(--accent-sky)' }}></i>
        </div>
        <p style={{ margin: 0, fontSize: 'var(--t-lg)', color: 'var(--text-strong)', lineHeight: 1.45, fontWeight: 500 }}>
          Консульский сбор оплачивается зарубежной банковской картой. Если у вас такой нет - мы поможем оплатить.
        </p>
        <div style={{ marginTop: 22, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {SCHENGEN_CONSULAR_FEES.map((f, i) => (
            <div key={f.label} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, padding: '14px 4px', borderTop: i === 0 ? 'none' : '1px solid var(--glass-edge-faint)' }}>
              <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)' }}>{f.label}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--t-lg)', fontWeight: 600, color: 'var(--text-strong)', whiteSpace: 'nowrap' }}>{f.price}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Services() {
  const { Button } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [feeOpen, setFeeOpen] = React.useState(false);
  const tariff = {
    name: 'Всё включено',
    tagline: 'Берём весь процесс на себя - от анкеты до подачи.',
    price: '29 990',
    features: ['Заполняем анкету за вас', 'Готовим полный пакет документов', 'Подбираем оптимальное консульство для подачи'],
  };
  return (
    <section id="services" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 620, margin: '0 auto 44px' }}>
          <span className="rv-eyebrow">Стоимость</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Всё включено</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>Берём весь процесс на себя - вам остаётся только прийти на подачу.</p>
        </div>
        <div style={{ maxWidth: 760, margin: '0 auto', padding: 30, borderRadius: 'var(--r-xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-shadow), var(--glass-inner)', display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ fontSize: 'var(--t-h3)' }}>{tariff.name}</h3>
          <p style={{ marginTop: 8, color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>{tariff.tagline}</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 22, marginBottom: 24 }}>
            {tariff.features.map((f) => (
              <div key={f} style={{ display: 'flex', gap: 11, alignItems: 'flex-start' }}>
                <i data-lucide="check" style={{ width: 18, height: 18, marginTop: 2, flex: 'none', color: 'var(--success)' }}></i>
                <span style={{ fontSize: 'var(--t-body)', color: 'var(--text-body)', lineHeight: 1.45 }}>{f}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 'auto', paddingTop: 20, borderTop: '1px solid var(--glass-edge-faint)' }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 34, fontWeight: 600, letterSpacing: '-0.02em', color: 'var(--text-strong)' }}>{tariff.price}</span>
              <span style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)' }}>руб.</span>
            </div>
            <div style={{ marginTop: 6, fontSize: 'var(--t-sm)', color: 'var(--text-muted)' }}>+ <FeeLink onOpen={() => setFeeOpen(true)} /></div>
            <div style={{ marginTop: 22 }}>
              <Button variant="secondary" fullWidth size="lg" iconRight={<i data-lucide="arrow-right" style={{ width: 18, height: 18 }}></i>} onClick={() => { const el = document.getElementById('consult'); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>
                Записаться на консультацию
              </Button>
            </div>
          </div>
        </div>
      </div>
      <FeeModal open={feeOpen} onClose={() => setFeeOpen(false)} />
    </section>
  );
}
"""

def schengen_app_js(promo_codes):
    return f"""
window.__promoCodes = {json.dumps(promo_codes)};

function App() {{
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [consultOpen, setConsultOpen] = React.useState(false);
  const openConsult = React.useCallback(() => setConsultOpen(true), []);
  React.useEffect(() => {{
    window.__openConsult = openConsult;
    return () => {{ delete window.__openConsult; }};
  }}, [openConsult]);
  React.useEffect(() => {{
    if (window.lucide) window.lucide.createIcons();
  }});
  React.useEffect(() => {{ document.body.style.overflow = menuOpen ? 'hidden' : ''; }}, [menuOpen]);
  return (
    <React.Fragment>
      <Header onOpenMenu={{() => setMenuOpen(true)}} onOpenConsult={{openConsult}} />
      <MobileMenu open={{menuOpen}} onClose={{() => setMenuOpen(false)}} onOpenConsult={{openConsult}} />
      <ConsultModal open={{consultOpen}} onClose={{() => setConsultOpen(false)}} visaLabel="🇪🇺 Новая заявка - Шенгенская виза" />
      <main>
        <Hero />
        <AboutVisa />
        <UKMap />
        <Services />
        <ConsultForm visaLabel="🇪🇺 Новая заявка - Шенгенская виза" />
      </main>
      <Footer />
    </React.Fragment>
  );
}}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
setTimeout(() => window.lucide && window.lucide.createIcons(), 80);
"""

# ─── Landing page ─────────────────────────────────────────────────────────────

LANDING_PAGE_JS = r"""
function LandingPage() {
  React.useEffect(() => { if (window.lucide) window.lucide.createIcons(); });
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
        <div style={{ padding: 12, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--elev-2), var(--glass-inner)' }}>
          <img src="assets/photos/banner.jpg" alt="Royal Visas" style={{ width: '100%', height: 'auto', display: 'block', borderRadius: 24 }} />
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
            <div className="rv-landing-card" style={{ height: '100%', padding: 32, borderRadius: 'var(--r-2xl)', background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)', backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)', boxShadow: 'var(--glass-shadow), var(--glass-inner)', display: 'flex', flexDirection: 'column', transition: 'border-color .22s ease, transform .22s ease, box-shadow .22s ease' }}
              onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'rgba(182,166,214,0.5)'; e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.boxShadow = c.glow + ', var(--glass-inner)'; }}
              onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--glass-edge)'; e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = 'var(--glass-shadow), var(--glass-inner)'; }}
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
        Royal Visas - частный визовый сервис. Мы не являемся государственным органом и не аффилированы с UKVI или посольствами. Решение по визе принимает консульство.
      </p>
    </div>
  );
}
"""

LANDING_APP_JS = r"""
function LandingApp() {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [consultOpen, setConsultOpen] = React.useState(false);
  const openConsult = React.useCallback(() => setConsultOpen(true), []);
  React.useEffect(() => {
    window.__openConsult = openConsult;
    return () => { delete window.__openConsult; };
  }, [openConsult]);
  React.useEffect(() => { if (window.lucide) window.lucide.createIcons(); });
  React.useEffect(() => { document.body.style.overflow = menuOpen ? 'hidden' : ''; }, [menuOpen]);
  return (
    <React.Fragment>
      <Header onOpenMenu={() => setMenuOpen(true)} onOpenConsult={openConsult} />
      <MobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} onOpenConsult={openConsult} />
      <ConsultModal open={consultOpen} onClose={() => setConsultOpen(false)} visaLabel="📋 Новая заявка - Royal Visas" />
      <main><LandingPage /></main>
      <Footer />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<LandingApp />);
setTimeout(() => window.lucide && window.lucide.createIcons(), 80);
"""

# ─── build functions ──────────────────────────────────────────────────────────

TITLE = 'Royal Visas - Визы в Европу и Великобританию'

def build_uk():
    write_page('uk.html', TITLE, [
        HEADER_JS,
        FOOTER_JS,
        CONSULT_MODAL_JS,
        CONSULT_FORM_JS,
        UK_HERO_JS,
        UK_ABOUT_JS,
        UK_MAP_JS,
        UK_SERVICES_JS,
        uk_app_js(PROMO_CODES),
    ])

def build_schengen():
    write_page('schengen.html', TITLE, [
        HEADER_JS,
        FOOTER_JS,
        CONSULT_MODAL_JS,
        CONSULT_FORM_JS,
        SCHENGEN_HERO_JS,
        SCHENGEN_ABOUT_JS,
        SCHENGEN_MAP_JS,
        SCHENGEN_SERVICES_JS,
        schengen_app_js(PROMO_CODES),
    ])

def build_index():
    write_page('index.html', TITLE, [
        HEADER_JS,
        FOOTER_JS,
        CONSULT_MODAL_JS,
        LANDING_PAGE_JS,
        LANDING_APP_JS,
    ])

if __name__ == '__main__':
    build_uk()
    build_schengen()
    build_index()
    print('\nAll done!')
    print('\nPromo codes (30 one-time, -5 000 руб.):')
    for c in PROMO_CODES:
        print(' ', c)
    print('  KRISKISS (valid until 2026-10-01)')
