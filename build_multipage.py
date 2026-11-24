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
    ['form.html', 'Анкета'],
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
    price: '34 990',
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
    price: '34 990',
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

# ─── form page ───────────────────────────────────────────────────────────────

FORM_JS = r"""
const EU_SCHENGEN_COUNTRIES = [
  'Австрия','Бельгия','Болгария','Венгрия','Германия','Греция','Дания',
  'Испания','Италия','Кипр','Латвия','Литва','Люксембург','Мальта','Нидерланды',
  'Норвегия','Польша','Португалия','Румыния','Словакия','Словения','Финляндия',
  'Франция','Хорватия','Чехия','Швейцария','Швеция','Эстония','Исландия',
  'Лихтенштейн','Ирландия',
];
const SPECIAL_TRIP_COUNTRIES = ['США','Канада','Австралия','Новая Зеландия'];
const PRIORITY_COUNTRIES_LIST = [...EU_SCHENGEN_COUNTRIES, ...SPECIAL_TRIP_COUNTRIES].sort((a,b)=>a.localeCompare(b,'ru'));

const ALL_COUNTRIES_LIST = [
  'Австралия','Австрия','Азербайджан','Албания','Алжир','Ангола','Аргентина','Армения',
  'Афганистан','Бангладеш','Бахрейн','Беларусь','Бельгия','Болгария','Боливия',
  'Бразилия','Великобритания','Венгрия','Венесуэла','Вьетнам','Гана','Германия',
  'Греция','Грузия','Дания','Египет','Израиль','Индия','Индонезия','Ирак','Иран',
  'Ирландия','Исландия','Испания','Италия','Иордания','Йемен','Казахстан',
  'Камбоджа','Канада','Катар','Кения','Китай','Кипр','Колумбия','Куба','Кувейт',
  'Кыргызстан','Латвия','Ливан','Лихтенштейн','Литва','Люксембург','Малайзия',
  'Мальта','Марокко','Мексика','Молдова','Монголия','Нидерланды','Нигерия',
  'Новая Зеландия','Норвегия','ОАЭ','Оман','Пакистан','Перу','Польша','Португалия',
  'Румыния','Саудовская Аравия','Сербия','Сингапур','Словакия','Словения','США',
  'Таджикистан','Таиланд','Тунис','Турция','Туркменистан','Узбекистан','Украина',
  'Финляндия','Франция','Хорватия','Чехия','Чили','Швейцария','Швеция','Эстония',
  'Эфиопия','ЮАР','Южная Корея','Япония',
].sort((a,b)=>a.localeCompare(b,'ru'));

const INPUT_S = {
  width:'100%', boxSizing:'border-box',
  padding:'12px 16px', fontSize:16, lineHeight:1.4,
  borderRadius:'var(--r-md)',
  border:'1.5px solid var(--glass-edge)',
  background:'var(--surface-2)',
  color:'var(--text-strong)',
  outline:'none', fontFamily:'inherit',
  transition:'border-color 0.15s',
  WebkitAppearance:'none',
};
const LABEL_S = {
  display:'block', marginBottom:6,
  fontSize:14, fontWeight:500,
  color:'var(--text-muted)',
};

function Field({ label, hint, children }) {
  return (
    <div style={{ marginBottom:20 }}>
      {label && <label style={LABEL_S}>{label}</label>}
      {children}
      {hint && <p style={{margin:'4px 0 0',fontSize:13,color:'var(--text-faint)'}}>{hint}</p>}
    </div>
  );
}

function TextInput({ value, onChange, type='text' }) {
  return (
    <input type={type} value={value}
      onChange={e=>onChange(e.target.value)}
      style={INPUT_S}
      onFocus={e=>e.target.style.borderColor='var(--accent-mauve)'}
      onBlur={e=>e.target.style.borderColor='var(--glass-edge)'}
    />
  );
}

function TextArea({ value, onChange, rows=3 }) {
  return (
    <textarea value={value}
      onChange={e=>onChange(e.target.value)}
      rows={rows}
      style={{...INPUT_S, resize:'vertical'}}
      onFocus={e=>e.target.style.borderColor='var(--accent-mauve)'}
      onBlur={e=>e.target.style.borderColor='var(--glass-edge)'}
    />
  );
}

function DatePicker({ value, onChange }) {
  return (
    <input type="date" value={value}
      onChange={e=>onChange(e.target.value)}
      style={INPUT_S}
      onFocus={e=>e.target.style.borderColor='var(--accent-mauve)'}
      onBlur={e=>e.target.style.borderColor='var(--glass-edge)'}
    />
  );
}

function SelectInput({ value, onChange, options }) {
  return (
    <select value={value}
      onChange={e=>onChange(e.target.value)}
      style={INPUT_S}
      onFocus={e=>e.target.style.borderColor='var(--accent-mauve)'}
      onBlur={e=>e.target.style.borderColor='var(--glass-edge)'}
    >
      {options.map(o=>typeof o==='string'
        ? <option key={o} value={o}>{o}</option>
        : <option key={o.value} value={o.value}>{o.label}</option>
      )}
    </select>
  );
}

function CountrySearch({ value, onChange, countries, id }) {
  return (
    <div>
      <input list={id} value={value}
        onChange={e=>onChange(e.target.value)}
        style={INPUT_S}
        onFocus={e=>e.target.style.borderColor='var(--accent-mauve)'}
        onBlur={e=>e.target.style.borderColor='var(--glass-edge)'}
        autoComplete="off"
      />
      <datalist id={id}>
        {countries.map(c=><option key={c} value={c}/>)}
      </datalist>
    </div>
  );
}

function YesNo({ value, onChange }) {
  const btn = (v, label) => (
    <button key={v} type="button" onClick={()=>onChange(v)} style={{
      padding:'10px 32px',
      borderRadius:'var(--r-pill)',
      border:`1.5px solid ${value===v?'var(--accent-mauve)':'var(--glass-edge)'}`,
      background: value===v?'var(--accent-mauve)':'transparent',
      color: value===v?'#fff':'var(--text-body)',
      fontSize:16, fontWeight:500,
      cursor:'pointer', transition:'all 0.15s', fontFamily:'inherit',
    }}>{label}</button>
  );
  return (
    <div style={{display:'flex',gap:10,flexWrap:'wrap'}}>
      {btn('yes','Да')}
      {btn('no','Нет')}
    </div>
  );
}

function Divider({ label }) {
  return (
    <div style={{display:'flex',alignItems:'center',gap:12,margin:'8px 0 20px'}}>
      <div style={{flex:1,height:1,background:'var(--glass-edge-faint)'}}/>
      <span style={{fontSize:13,fontWeight:600,color:'var(--text-muted)',letterSpacing:'0.04em',textTransform:'uppercase'}}>{label}</span>
      <div style={{flex:1,height:1,background:'var(--glass-edge-faint)'}}/>
    </div>
  );
}

function FormSection({ num, title, subtitle, children }) {
  return (
    <section style={{
      background:'var(--glass-fill-solid)',
      border:'1px solid var(--glass-edge)',
      borderRadius:'var(--r-xl)',
      padding:'28px 24px',
      marginBottom:20,
    }}>
      <div style={{
        display:'flex', alignItems:'flex-start', gap:14,
        marginBottom:24, paddingBottom:16,
        borderBottom:'1px solid var(--glass-edge-faint)',
      }}>
        <div style={{
          width:32, height:32, borderRadius:'var(--r-md)',
          background:'var(--grad-royal)', color:'#fff',
          display:'flex', alignItems:'center', justifyContent:'center',
          fontSize:13, fontWeight:700, flexShrink:0,
        }}>{num}</div>
        <div>
          <h2 style={{margin:0, fontSize:18, fontWeight:600, color:'var(--text-strong)'}}>{title}</h2>
          {subtitle && <p style={{margin:'3px 0 0', fontSize:13, color:'var(--text-muted)'}}>{subtitle}</p>}
        </div>
      </div>
      {children}
    </section>
  );
}

function Row2({ children }) {
  return (
    <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(220px, 1fr))', gap:'0 20px'}}>
      {children}
    </div>
  );
}

function Row3({ children }) {
  return (
    <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(180px, 1fr))', gap:'0 16px'}}>
      {children}
    </div>
  );
}

function AddBtn({ onClick, label }) {
  return (
    <button type="button" onClick={onClick} style={{
      display:'flex', alignItems:'center', gap:8,
      padding:'8px 16px', borderRadius:'var(--r-md)',
      border:'1px dashed var(--glass-edge)', background:'transparent',
      color:'var(--text-muted)', fontSize:14, cursor:'pointer', fontFamily:'inherit',
      marginTop:4,
    }}>
      <i data-lucide="plus" style={{width:16,height:16}}></i>
      {label}
    </button>
  );
}

function TripEntry({ trip, onChange, onDelete, canDelete, countries, idPrefix }) {
  return (
    <div style={{
      display:'flex', flexWrap:'wrap', gap:12, alignItems:'flex-start',
      padding:'14px 16px', borderRadius:'var(--r-md)',
      background:'rgba(255,255,255,0.03)',
      border:'1px solid var(--glass-edge-faint)',
      marginBottom:10,
    }}>
      <div style={{flex:'2 1 180px', minWidth:160}}>
        <label style={{...LABEL_S, fontSize:12}}>Страна</label>
        <CountrySearch
          id={`${idPrefix}-country`}
          value={trip.country}
          onChange={v=>onChange({...trip, country:v})}
          countries={countries}
        />
      </div>
      <div style={{flex:'1 1 140px', minWidth:130}}>
        <label style={{...LABEL_S, fontSize:12}}>Дата въезда</label>
        <DatePicker value={trip.from} onChange={v=>onChange({...trip, from:v})} />
      </div>
      <div style={{flex:'1 1 140px', minWidth:130}}>
        <label style={{...LABEL_S, fontSize:12}}>Дата выезда</label>
        <DatePicker value={trip.to} onChange={v=>onChange({...trip, to:v})} />
      </div>
      {canDelete && (
        <div style={{flex:'0 0 auto', paddingTop:22}}>
          <button type="button" onClick={onDelete} style={{
            width:36, height:44, borderRadius:'var(--r-md)',
            border:'1px solid var(--glass-edge)', background:'transparent',
            cursor:'pointer', color:'var(--text-muted)',
            display:'flex', alignItems:'center', justifyContent:'center',
          }}>
            <i data-lucide="trash-2" style={{width:16,height:16}}></i>
          </button>
        </div>
      )}
    </div>
  );
}

function TravelHistorySection({ data, onChange }) {
  const upd = (key, val) => onChange({...data, [key]:val});
  const addTrip = key => () => upd(key, [...data[key], {country:'', from:'', to:''}]);
  const removeTrip = (key, idx) => () => upd(key, data[key].filter((_,i)=>i!==idx));
  const updateTrip = (key, idx) => trip => { const a=[...data[key]]; a[idx]=trip; upd(key,a); };

  return (
    <FormSection num="8" title="История поездок" subtitle="Путешествия за последние 10 лет">

      <Field label="Бывали ли вы в Великобритании ранее?">
        <YesNo value={data.wasInUKBefore} onChange={v=>upd('wasInUKBefore',v)} />
      </Field>

      {data.wasInUKBefore==='yes' && (
        <div style={{marginBottom:20}}>
          <p style={{fontSize:14, color:'var(--text-muted)', marginBottom:10}}>Укажите поездки в UK:</p>
          {data.ukVisits.map((t,i)=>(
            <TripEntry key={i} trip={t}
              onChange={updateTrip('ukVisits',i)}
              onDelete={removeTrip('ukVisits',i)}
              canDelete={data.ukVisits.length>1}
              countries={['Великобритания']}
              idPrefix={`uk-${i}`}
            />
          ))}
          <AddBtn onClick={addTrip('ukVisits')} label="Добавить поездку в UK" />
        </div>
      )}

      <div style={{height:1, background:'var(--glass-edge-faint)', margin:'4px 0 20px'}}/>

      <Field label="Были ли поездки за рубеж за последние 10 лет?">
        <YesNo value={data.hadAnyTrips} onChange={v=>upd('hadAnyTrips',v)} />
      </Field>

      {data.hadAnyTrips==='yes' && (<>

        <Field
          label="Были ли поездки в США, Канаду, Австралию, Новую Зеландию или страны ЕС/Шенген?"
          hint="Если да — укажите до 2 поездок. Лучше выбрать из разных категорий: например, 1 страна Шенгена и 1 из США/Австралии/Канады/Новой Зеландии."
        >
          <YesNo value={data.hadPriorityTrips} onChange={v=>upd('hadPriorityTrips',v)} />
        </Field>

        {data.hadPriorityTrips==='yes' && (
          <div style={{marginBottom:20}}>
            {data.priorityTrips.map((t,i)=>(
              <TripEntry key={i} trip={t}
                onChange={updateTrip('priorityTrips',i)}
                onDelete={removeTrip('priorityTrips',i)}
                canDelete={data.priorityTrips.length>1}
                countries={PRIORITY_COUNTRIES_LIST}
                idPrefix={`pri-${i}`}
              />
            ))}
            {data.priorityTrips.length<2 && (
              <AddBtn onClick={addTrip('priorityTrips')} label="Добавить ещё поездку (макс. 2)" />
            )}
          </div>
        )}

        <Field
          label="Были ли поездки в другие страны (кроме указанных выше)?"
          hint="Укажите все поездки за последние 10 лет в любые другие страны."
        >
          <YesNo value={data.hadOtherTrips} onChange={v=>upd('hadOtherTrips',v)} />
        </Field>

        {data.hadOtherTrips==='yes' && (
          <div style={{marginBottom:20}}>
            {data.otherTrips.map((t,i)=>(
              <TripEntry key={i} trip={t}
                onChange={updateTrip('otherTrips',i)}
                onDelete={removeTrip('otherTrips',i)}
                canDelete={data.otherTrips.length>1}
                countries={ALL_COUNTRIES_LIST}
                idPrefix={`oth-${i}`}
              />
            ))}
            <AddBtn onClick={addTrip('otherTrips')} label="Были ещё поездки? Добавить" />
          </div>
        )}

      </>)}
    </FormSection>
  );
}

const GENDER_OPTIONS = [
  {value:'',label:'-- выберите --'},
  {value:'male',label:'Мужской'},{value:'female',label:'Женский'},
];
const MARITAL_OPTIONS = [
  '-- выберите --','Не состою в браке','Состою в браке','Разведён / Разведена',
  'Вдовец / Вдова','Гражданский брак',
];
const HOUSING_OPTIONS = [
  '-- выберите --','Собственное жильё','Аренда','Живу с родителями / родственниками','Служебное жильё',
];
const EMPLOYMENT_OPTIONS = [
  '-- выберите --','Работаю по найму (полная занятость)','Работаю по найму (частичная занятость)',
  'Самозанятый / ИП','Владелец бизнеса','Государственный служащий',
  'Пенсионер','Студент','В отпуске по уходу за ребёнком','Временно не работаю',
];
const VISIT_PURPOSE_OPTIONS = [
  '-- выберите --','Туризм / отдых','Деловая поездка','Посещение друзей или родственников',
  'Медицинское лечение','Участие в конференции / семинаре',
  'Учёба (краткосрочная)','Транзит','Другое',
];
const PAYS_OPTIONS = [
  '-- выберите --','Самостоятельно','Супруг / Супруга','Другое',
];
const UK_STAY_OPTIONS = [
  '-- выберите --','Отель','У друзей','У родственников',
];
const OTHER_INCOME_OPTIONS = [
  {value:'',label:'-- нет --'},
  {value:'rent',label:'Аренда'},
  {value:'dividends',label:'Дивиденды'},
  {value:'savings',label:'Накопления'},
  {value:'other',label:'Другое'},
];

const INITIAL_STATE = {
  firstName:'', lastName:'', otherNames:'', dob:'',
  birthCity:'', birthCountry:'', nationality:'', gender:'', maritalStatus:'',
  spouseName:'', spouseDob:'',
  passportNo:'', passportIssuer:'', passportIssueDate:'', passportExpiry:'',
  rfPassportNo:'', rfPassportIssuer:'', rfPassportIssueDate:'',
  changedName:null, previousFullName:'',
  hasOtherCitizenship:null, otherCitizenships:[''],
  regAddress:'', regAddressDate:'', housingStatus:'',
  actualAddressSame:null, actualAddress:'', actualAddressDate:'', actualHousingStatus:'',
  phone:'', email:'',
  employmentStatus:'', employerName:'', employerPhone:'',
  jobTitle:'', jobDescription:'', startDate:'',
  employerLegalAddress:'', employerActualSame:null, employerActualAddress:'',
  monthlyIncome:'', monthlyExpenses:'', savings:'',
  otherIncomeType:'', otherIncomeAmount:'', otherIncomeDesc:'',
  visitPurpose:'', arrivalDate:'', departureDate:'', tripDescription:'',
  ukExpenses:'',
  whoPaysTripExpenses:'', sponsorName:'', sponsorPhone:'', sponsorEmail:'', sponsorWho:'',
  hasUKRelatives:null, relativeName:'', relativeRelation:'',
  relativeCitizenship:'', relativeUKStatus:'', relativePassport:'',
  ukStayType:'', hotelName:'', ukAddress:'',
  stayWithListedRelative:null, otherHostInfo:'',
  hostName:'', hostPhone:'', hostEmail:'',
  travelHistory:{
    wasInUKBefore:null,
    ukVisits:[{country:'Великобритания', from:'', to:''}],
    hadAnyTrips:null,
    hadPriorityTrips:null,
    priorityTrips:[{country:'', from:'', to:''}],
    hadOtherTrips:null,
    otherTrips:[{country:'', from:'', to:''}],
  },
  motherName:'', motherDob:'', motherNationality:'',
  fatherName:'', fatherDob:'', fatherNationality:'',
  hasDependents:null, dependentsInfo:'',
  wasRefused:null, wasDeported:null, violatedVisa:null, hasCriminalRecord:null,
  violationsDetails:'',
  additionalInfo:'',
};

function FormApp() {
  const [form, setForm] = React.useState(INITIAL_STATE);
  const [submitted, setSubmitted] = React.useState(false);
  const [menuOpen, setMenuOpen] = React.useState(false);

  React.useEffect(()=>{ if(window.lucide) window.lucide.createIcons(); });
  React.useEffect(()=>{ document.body.style.overflow = menuOpen?'hidden':''; },[menuOpen]);

  const upd = key => val => setForm(f=>({...f,[key]:val}));
  const updTH = val => setForm(f=>({...f,travelHistory:val}));

  const [sending, setSending] = React.useState(false);
  const [sendError, setSendError] = React.useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setSending(true);
    setSendError('');
    const TG_TOKEN = '8677081622:AAHAvOYbY50uCZnx9QimTXDO98CYJnMnvxA';
    const TG_CHAT_ID = '-5235367527';
    const f = form;
    const th = f.travelHistory || {};
    const yn = v => v === 'yes' ? 'Да' : v === 'no' ? 'Нет' : v || '—';
    const val = v => v || '—';
    const lines = [
      '📋 *Новая анкета — Royal Visas*',
      '',
      '*1. Личные данные*',
      `Имя: ${val(f.firstName)}`,
      `Фамилия: ${val(f.lastName)}`,
      `Дата рождения: ${val(f.dob)}`,
      `Менял(а) имя/фамилию: ${yn(f.changedName)}`,
      f.changedName === 'yes' ? `Прежнее ФИО: ${val(f.previousFullName)}` : null,
      `Город рождения: ${val(f.birthCity)}`,
      `Страна рождения: ${val(f.birthCountry)}`,
      `Гражданство: ${val(f.nationality)}`,
      `Пол: ${val(f.gender)}`,
      `Семейное положение: ${val(f.maritalStatus)}`,
      (f.maritalStatus === 'Состою в браке' || f.maritalStatus === 'Гражданский брак') ? `ФИО супруга/супруги: ${val(f.spouseName)}` : null,
      (f.maritalStatus === 'Состою в браке' || f.maritalStatus === 'Гражданский брак') ? `Дата рождения супруга/супруги: ${val(f.spouseDob)}` : null,
      '',
      '*2. Паспорта*',
      `Загранпаспорт №: ${val(f.passportNo)}`,
      `Выдан: ${val(f.passportIssuer)}`,
      `Дата выдачи: ${val(f.passportIssueDate)}`,
      `Срок действия: ${val(f.passportExpiry)}`,
      `Внутренний паспорт №: ${val(f.rfPassportNo)}`,
      `Кем выдан: ${val(f.rfPassportIssuer)}`,
      `Дата выдачи (внутр.): ${val(f.rfPassportIssueDate)}`,
      `Другое гражданство: ${yn(f.hasOtherCitizenship)}`,
      (f.hasOtherCitizenship === 'yes' && f.otherCitizenships && f.otherCitizenships.filter(Boolean).length)
        ? `Другие гражданства: ${f.otherCitizenships.filter(Boolean).join(', ')}` : null,
      '',
      '*3. Адрес и контакты*',
      `Адрес регистрации: ${val(f.regAddress)}`,
      `Дата регистрации: ${val(f.regAddressDate)}`,
      `Статус жилья (рег.): ${val(f.housingStatus)}`,
      `Факт. адрес совпадает: ${yn(f.actualAddressSame)}`,
      f.actualAddressSame === 'no' ? `Факт. адрес: ${val(f.actualAddress)}` : null,
      f.actualAddressSame === 'no' ? `Дата (факт.): ${val(f.actualAddressDate)}` : null,
      f.actualAddressSame === 'no' ? `Статус жилья (факт.): ${val(f.actualHousingStatus)}` : null,
      `Телефон: ${val(f.phone)}`,
      `Email: ${val(f.email)}`,
      '',
      '*4. Занятость*',
      `Статус: ${val(f.employmentStatus)}`,
      `Работодатель: ${val(f.employerName)}`,
      `Телефон работодателя: ${val(f.employerPhone)}`,
      `Должность: ${val(f.jobTitle)}`,
      `Описание: ${val(f.jobDescription)}`,
      `Дата начала работы: ${val(f.startDate)}`,
      `Юр. адрес работодателя: ${val(f.employerLegalAddress)}`,
      `Факт. адрес совпадает с юр.: ${yn(f.employerActualSame)}`,
      f.employerActualSame === 'no' ? `Факт. адрес работодателя: ${val(f.employerActualAddress)}` : null,
      `Доход в месяц: ${val(f.monthlyIncome)}`,
      `Расходы в месяц: ${val(f.monthlyExpenses)}`,
      `Накопления: ${val(f.savings)}`,
      `Другой доход (тип): ${val(f.otherIncomeType)}`,
      f.otherIncomeType ? `Другой доход (сумма): ${val(f.otherIncomeAmount)}` : null,
      f.otherIncomeType === 'Другое' ? `Описание дохода: ${val(f.otherIncomeDesc)}` : null,
      '',
      '*5. Поездка*',
      `Цель: ${val(f.visitPurpose)}`,
      `Дата въезда: ${val(f.arrivalDate)}`,
      `Дата выезда: ${val(f.departureDate)}`,
      `Описание поездки: ${val(f.tripDescription)}`,
      `Расходы в UK: ${val(f.ukExpenses)}`,
      `Кто оплачивает: ${val(f.whoPaysTripExpenses)}`,
      f.whoPaysTripExpenses && f.whoPaysTripExpenses !== 'Самостоятельно' ? `Спонсор: ${val(f.sponsorName)}` : null,
      f.whoPaysTripExpenses && f.whoPaysTripExpenses !== 'Самостоятельно' ? `Телефон спонсора: ${val(f.sponsorPhone)}` : null,
      f.whoPaysTripExpenses && f.whoPaysTripExpenses !== 'Самостоятельно' ? `Email спонсора: ${val(f.sponsorEmail)}` : null,
      f.whoPaysTripExpenses === 'Другое' ? `Кем приходится: ${val(f.sponsorWho)}` : null,
      '',
      '*6. Родственники в UK*',
      `Есть родственники в UK: ${yn(f.hasUKRelatives)}`,
      f.hasUKRelatives === 'yes' ? `Имя: ${val(f.relativeName)}` : null,
      f.hasUKRelatives === 'yes' ? `Степень родства: ${val(f.relativeRelation)}` : null,
      f.hasUKRelatives === 'yes' ? `Гражданство родственника: ${val(f.relativeCitizenship)}` : null,
      f.hasUKRelatives === 'yes' ? `Статус в UK: ${val(f.relativeUKStatus)}` : null,
      f.hasUKRelatives === 'yes' ? `Паспорт родственника: ${val(f.relativePassport)}` : null,
      '',
      '*7. Проживание в UK*',
      `Тип размещения: ${val(f.ukStayType)}`,
      f.ukStayType === 'Отель' ? `Название отеля: ${val(f.hotelName)}` : null,
      `Адрес в UK: ${val(f.ukAddress)}`,
      f.ukStayType === 'У родственников' && f.hasUKRelatives === 'yes'
        ? `Проживание у указанных родственников: ${yn(f.stayWithListedRelative)}` : null,
      f.ukStayType === 'У родственников' && (f.hasUKRelatives !== 'yes' || f.stayWithListedRelative === 'no')
        ? `Доп. инфо о хозяине: ${val(f.otherHostInfo)}` : null,
      f.ukStayType === 'У друзей' ? `Имя хозяина: ${val(f.hostName)}` : null,
      f.ukStayType === 'У друзей' ? `Телефон хозяина: ${val(f.hostPhone)}` : null,
      f.ukStayType === 'У друзей' ? `Email хозяина: ${val(f.hostEmail)}` : null,
      '',
      '*8. История поездок*',
      `Был(а) в UK раньше: ${yn(th.wasInUKBefore)}`,
      th.wasInUKBefore === 'yes' && th.ukVisits && th.ukVisits.length
        ? th.ukVisits.map((v,i)=>`  UK поездка ${i+1}: ${v.from||'?'} — ${v.to||'?'}`).join('\n') : null,
      `Были другие поездки: ${yn(th.hadAnyTrips)}`,
      `Шенген/США/CAN/AUS: ${yn(th.hadPriorityTrips)}`,
      th.hadPriorityTrips === 'yes' && th.priorityTrips && th.priorityTrips.filter(p=>p.country).length
        ? th.priorityTrips.filter(p=>p.country).map((v,i)=>`  Поездка ${i+1}: ${v.country}, ${v.from||'?'} — ${v.to||'?'}`).join('\n') : null,
      `Другие страны: ${yn(th.hadOtherTrips)}`,
      th.hadOtherTrips === 'yes' && th.otherTrips && th.otherTrips.filter(p=>p.country).length
        ? th.otherTrips.filter(p=>p.country).map((v,i)=>`  Поездка ${i+1}: ${v.country}, ${v.from||'?'} — ${v.to||'?'}`).join('\n') : null,
      '',
      '*9. Родители*',
      `Мать: ${val(f.motherName)}, ${val(f.motherDob)}, ${val(f.motherNationality)}`,
      `Отец: ${val(f.fatherName)}, ${val(f.fatherDob)}, ${val(f.fatherNationality)}`,
      '',
      '*10. Иждивенцы*',
      `Есть иждивенцы: ${yn(f.hasDependents)}`,
      f.hasDependents === 'yes' ? `Инфо: ${val(f.dependentsInfo)}` : null,
      '',
      '*11. Отказы и нарушения*',
      `Отказ в визе: ${yn(f.wasRefused)}`,
      `Депортация: ${yn(f.wasDeported)}`,
      `Нарушение визы: ${yn(f.violatedVisa)}`,
      `Судимость: ${yn(f.hasCriminalRecord)}`,
      (f.wasRefused === 'yes' || f.wasDeported === 'yes' || f.violatedVisa === 'yes' || f.hasCriminalRecord === 'yes')
        ? `Детали: ${val(f.violationsDetails)}` : null,
      '',
      '*12. Доп. информация*',
      `${val(f.additionalInfo)}`,
    ];
    const text = lines.filter(l => l !== null).join('\n');
    try {
      const resp = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: TG_CHAT_ID, text, parse_mode: 'Markdown' }),
      });
      const data = await resp.json();
      if (!data.ok) throw new Error(data.description || 'Telegram error');
      setSubmitted(true);
      window.scrollTo({top:0, behavior:'smooth'});
    } catch(err) {
      setSendError('Не удалось отправить анкету. Попробуйте снова или напишите нам напрямую.');
    } finally {
      setSending(false);
    }
  };

  if (submitted) {
    return (
      <React.Fragment>
        <Header onOpenMenu={()=>setMenuOpen(true)} onOpenConsult={()=>{}} />
        <MobileMenu open={menuOpen} onClose={()=>setMenuOpen(false)} onOpenConsult={()=>setMenuOpen(false)} />
        <div style={{minHeight:'80vh', display:'flex', alignItems:'center', justifyContent:'center', paddingTop:100, paddingBottom:60}}>
          <div className="rv-container" style={{maxWidth:500, textAlign:'center'}}>
            <div style={{
              width:72, height:72, borderRadius:'50%', background:'var(--grad-royal)',
              display:'flex', alignItems:'center', justifyContent:'center', margin:'0 auto 24px',
            }}>
              <i data-lucide="check" style={{width:36,height:36,color:'#fff'}}></i>
            </div>
            <h1 style={{fontSize:28, fontWeight:700, color:'var(--text-strong)', marginBottom:12}}>
              Анкета отправлена!
            </h1>
            <p style={{fontSize:17, color:'var(--text-muted)', lineHeight:1.6, marginBottom:32}}>
              Мы получили ваши данные и свяжемся с вами в ближайшее время.
            </p>
            <a href="uk.html" style={{
              display:'inline-block', padding:'14px 32px', borderRadius:'var(--r-pill)',
              background:'var(--grad-royal)', color:'#fff', fontWeight:600, fontSize:16, textDecoration:'none',
            }}>Вернуться на сайт</a>
          </div>
        </div>
        <Footer />
      </React.Fragment>
    );
  }

  return (
    <React.Fragment>
      <Header onOpenMenu={()=>setMenuOpen(true)} onOpenConsult={()=>{}} />
      <MobileMenu open={menuOpen} onClose={()=>setMenuOpen(false)} onOpenConsult={()=>setMenuOpen(false)} />

      <main style={{paddingTop:100, paddingBottom:60}}>
        <div className="rv-container" style={{maxWidth:760}}>

          <div style={{marginBottom:32, textAlign:'center'}}>
            <h1 style={{fontSize:32, fontWeight:700, letterSpacing:'-0.02em', color:'var(--text-strong)', marginBottom:8}}>
              Анкета для визы в Великобританию
            </h1>
            <p style={{fontSize:16, color:'var(--text-muted)', lineHeight:1.6}}>
              Заполните все поля — данные используются для подготовки заявления.
            </p>
          </div>

          <form onSubmit={handleSubmit}>

            <FormSection num="1" title="Личные данные" subtitle="Заполняем как в загранпаспорте">
              <Row2>
                <Field label="Имя (Given names)">
                  <TextInput value={form.firstName} onChange={upd('firstName')} />
                </Field>
                <Field label="Фамилия (Family name)">
                  <TextInput value={form.lastName} onChange={upd('lastName')} />
                </Field>
              </Row2>
              <Field label="Меняли ли вы имя или фамилию?">
                <YesNo value={form.changedName} onChange={upd('changedName')} />
              </Field>
              {form.changedName==='yes' && (
                <Field label="Прежнее ФИО (полностью)">
                  <TextInput value={form.previousFullName} onChange={upd('previousFullName')} />
                </Field>
              )}
              <Row3>
                <Field label="Дата рождения">
                  <DatePicker value={form.dob} onChange={upd('dob')} />
                </Field>
                <Field label="Место рождения" hint="Как в загранпаспорте">
                  <TextInput value={form.birthCity} onChange={upd('birthCity')} />
                </Field>
                <Field label="Страна рождения" hint="Как в загранпаспорте">
                  <TextInput value={form.birthCountry} onChange={upd('birthCountry')} />
                </Field>
              </Row3>
              <Row3>
                <Field label="Гражданство">
                  <TextInput value={form.nationality} onChange={upd('nationality')} />
                </Field>
                <Field label="Пол">
                  <SelectInput value={form.gender} onChange={upd('gender')} options={GENDER_OPTIONS} />
                </Field>
                <Field label="Семейное положение">
                  <SelectInput value={form.maritalStatus} onChange={upd('maritalStatus')} options={MARITAL_OPTIONS} />
                </Field>
              </Row3>
              {(form.maritalStatus === 'Состою в браке' || form.maritalStatus === 'Гражданский брак') && (
                <Row2>
                  <Field label="ФИО супруга / супруги">
                    <TextInput value={form.spouseName} onChange={upd('spouseName')} />
                  </Field>
                  <Field label="Дата рождения супруга / супруги">
                    <DatePicker value={form.spouseDob} onChange={upd('spouseDob')} />
                  </Field>
                </Row2>
              )}
            </FormSection>

            <FormSection num="2" title="Паспорта" subtitle="Загранпаспорт и внутренний паспорт">
              <Row2>
                <Field label="Номер загранпаспорта">
                  <TextInput value={form.passportNo} onChange={upd('passportNo')} />
                </Field>
                <Field label="Орган выдачи">
                  <TextInput value={form.passportIssuer} onChange={upd('passportIssuer')} />
                </Field>
              </Row2>
              <Row2>
                <Field label="Дата выдачи">
                  <DatePicker value={form.passportIssueDate} onChange={upd('passportIssueDate')} />
                </Field>
                <Field label="Срок действия">
                  <DatePicker value={form.passportExpiry} onChange={upd('passportExpiry')} />
                </Field>
              </Row2>

              <Divider label="Внутренний паспорт" />
              <Row2>
                <Field label="Серия и номер">
                  <TextInput value={form.rfPassportNo} onChange={upd('rfPassportNo')} />
                </Field>
                <Field label="Кем выдан">
                  <TextInput value={form.rfPassportIssuer} onChange={upd('rfPassportIssuer')} />
                </Field>
              </Row2>
              <Row2>
                <Field label="Дата выдачи">
                  <DatePicker value={form.rfPassportIssueDate} onChange={upd('rfPassportIssueDate')} />
                </Field>
              </Row2>

              <Divider label="Другое гражданство" />
              <Field label="Есть ли у вас другое гражданство?">
                <YesNo value={form.hasOtherCitizenship} onChange={upd('hasOtherCitizenship')} />
              </Field>
              {form.hasOtherCitizenship==='yes' && (
                <div>
                  {form.otherCitizenships.map((c,i)=>(
                    <div key={i} style={{display:'flex',gap:10,marginBottom:10,alignItems:'center'}}>
                      <div style={{flex:1}}>
                        <label style={{...LABEL_S,fontSize:12}}>Страна паспорта {i+1}</label>
                        <TextInput value={c} onChange={v=>{
                          const arr=[...form.otherCitizenships]; arr[i]=v; upd('otherCitizenships')(arr);
                        }} />
                      </div>
                      {form.otherCitizenships.length>1 && (
                        <button type="button" onClick={()=>{
                          upd('otherCitizenships')(form.otherCitizenships.filter((_,j)=>j!==i));
                        }} style={{
                          marginTop:20, width:36, height:44, borderRadius:'var(--r-md)',
                          border:'1px solid var(--glass-edge)', background:'transparent',
                          cursor:'pointer', color:'var(--text-muted)',
                          display:'flex', alignItems:'center', justifyContent:'center', flexShrink:0,
                        }}>
                          <i data-lucide="trash-2" style={{width:16,height:16}}></i>
                        </button>
                      )}
                    </div>
                  ))}
                  <AddBtn
                    onClick={()=>upd('otherCitizenships')([...form.otherCitizenships,''])}
                    label="У меня есть ещё одно гражданство"
                  />
                </div>
              )}
            </FormSection>

            <FormSection num="3" title="Контактные данные и адрес">
              <Divider label="Адрес регистрации" />
              <Field label="Адрес регистрации">
                <TextArea value={form.regAddress} onChange={upd('regAddress')} rows={2} />
              </Field>
              <Row2>
                <Field label="Прописан(а) с">
                  <DatePicker value={form.regAddressDate} onChange={upd('regAddressDate')} />
                </Field>
                <Field label="Статус жилья">
                  <SelectInput value={form.housingStatus} onChange={upd('housingStatus')} options={HOUSING_OPTIONS} />
                </Field>
              </Row2>

              <Field label="Фактический адрес проживания совпадает с адресом регистрации?">
                <YesNo value={form.actualAddressSame} onChange={upd('actualAddressSame')} />
              </Field>

              {form.actualAddressSame==='no' && (<>
                <Divider label="Фактический адрес" />
                <Field label="Фактический адрес проживания">
                  <TextArea value={form.actualAddress} onChange={upd('actualAddress')} rows={2} />
                </Field>
                <Row2>
                  <Field label="Проживаю по этому адресу с">
                    <DatePicker value={form.actualAddressDate} onChange={upd('actualAddressDate')} />
                  </Field>
                  <Field label="Статус жилья">
                    <SelectInput value={form.actualHousingStatus} onChange={upd('actualHousingStatus')} options={HOUSING_OPTIONS} />
                  </Field>
                </Row2>
              </>)}

              <Divider label="Контакты" />
              <Row2>
                <Field label="Мобильный телефон">
                  <TextInput value={form.phone} onChange={upd('phone')} type="tel" />
                </Field>
                <Field label="Адрес электронной почты">
                  <TextInput value={form.email} onChange={upd('email')} type="email" />
                </Field>
              </Row2>
            </FormSection>

            <FormSection num="4" title="Занятость и доходы">
              <Row2>
                <Field label="Статус занятости">
                  <SelectInput value={form.employmentStatus} onChange={upd('employmentStatus')} options={EMPLOYMENT_OPTIONS} />
                </Field>
                <Field label="Должность">
                  <TextInput value={form.jobTitle} onChange={upd('jobTitle')} />
                </Field>
              </Row2>
              <Row2>
                <Field label="Название работодателя / компании">
                  <TextInput value={form.employerName} onChange={upd('employerName')} />
                </Field>
                <Field label="Телефон работодателя">
                  <TextInput value={form.employerPhone} onChange={upd('employerPhone')} type="tel" />
                </Field>
              </Row2>

              <Field label="Юридический адрес работодателя">
                <TextArea value={form.employerLegalAddress} onChange={upd('employerLegalAddress')} rows={2} />
              </Field>
              <Field label="Фактический адрес совпадает с юридическим?">
                <YesNo value={form.employerActualSame} onChange={upd('employerActualSame')} />
              </Field>
              {form.employerActualSame==='no' && (
                <Field label="Фактический адрес работодателя">
                  <TextArea value={form.employerActualAddress} onChange={upd('employerActualAddress')} rows={2} />
                </Field>
              )}

              <Field label="Описание должностных обязанностей">
                <TextArea value={form.jobDescription} onChange={upd('jobDescription')} rows={2} />
              </Field>
              <Row3>
                <Field label="Дата начала работы">
                  <DatePicker value={form.startDate} onChange={upd('startDate')} />
                </Field>
                <Field label="Ежемесячный доход (после налогов)" hint="В местной валюте">
                  <TextInput value={form.monthlyIncome} onChange={upd('monthlyIncome')} />
                </Field>
                <Field label="Ежемесячные расходы" hint="В местной валюте">
                  <TextInput value={form.monthlyExpenses} onChange={upd('monthlyExpenses')} />
                </Field>
              </Row3>
              <Row2>
                <Field label="Сбережения / накопления" hint="В местной валюте">
                  <TextInput value={form.savings} onChange={upd('savings')} />
                </Field>
                <Field label="Другие источники дохода">
                  <SelectInput value={form.otherIncomeType} onChange={upd('otherIncomeType')} options={OTHER_INCOME_OPTIONS} />
                </Field>
              </Row2>
              {form.otherIncomeType!=='' && (<>
                {form.otherIncomeType==='other' && (
                  <Field label="Опишите источник дохода">
                    <TextInput value={form.otherIncomeDesc} onChange={upd('otherIncomeDesc')} />
                  </Field>
                )}
                <Field label="Сумма" hint="В местной валюте">
                  <TextInput value={form.otherIncomeAmount} onChange={upd('otherIncomeAmount')} />
                </Field>
              </>)}
            </FormSection>

            <FormSection num="5" title="Цель и детали поездки">
              <Row2>
                <Field label="Основная цель визита">
                  <SelectInput value={form.visitPurpose} onChange={upd('visitPurpose')} options={VISIT_PURPOSE_OPTIONS} />
                </Field>
                <Field label="Кто оплачивает поездку?">
                  <SelectInput value={form.whoPaysTripExpenses} onChange={upd('whoPaysTripExpenses')} options={PAYS_OPTIONS} />
                </Field>
              </Row2>

              {form.whoPaysTripExpenses==='Супруг / Супруга' && (
                <div style={{marginBottom:20, padding:'16px', borderRadius:'var(--r-md)', background:'rgba(255,255,255,0.03)', border:'1px solid var(--glass-edge-faint)'}}>
                  <p style={{fontSize:13, color:'var(--text-muted)', margin:'0 0 12px'}}>Данные супруга / супруги:</p>
                  <Row3>
                    <Field label="ФИО">
                      <TextInput value={form.sponsorName} onChange={upd('sponsorName')} />
                    </Field>
                    <Field label="Телефон">
                      <TextInput value={form.sponsorPhone} onChange={upd('sponsorPhone')} type="tel" />
                    </Field>
                    <Field label="Email">
                      <TextInput value={form.sponsorEmail} onChange={upd('sponsorEmail')} type="email" />
                    </Field>
                  </Row3>
                </div>
              )}

              {form.whoPaysTripExpenses==='Другое' && (
                <div style={{marginBottom:20, padding:'16px', borderRadius:'var(--r-md)', background:'rgba(255,255,255,0.03)', border:'1px solid var(--glass-edge-faint)'}}>
                  <Row2>
                    <Field label="Кто оплачивает?">
                      <TextInput value={form.sponsorWho} onChange={upd('sponsorWho')} />
                    </Field>
                    <Field label="ФИО">
                      <TextInput value={form.sponsorName} onChange={upd('sponsorName')} />
                    </Field>
                  </Row2>
                  <Row2>
                    <Field label="Телефон">
                      <TextInput value={form.sponsorPhone} onChange={upd('sponsorPhone')} type="tel" />
                    </Field>
                    <Field label="Email">
                      <TextInput value={form.sponsorEmail} onChange={upd('sponsorEmail')} type="email" />
                    </Field>
                  </Row2>
                </div>
              )}

              <Row3>
                <Field label="Дата въезда в UK">
                  <DatePicker value={form.arrivalDate} onChange={upd('arrivalDate')} />
                </Field>
                <Field label="Дата выезда из UK">
                  <DatePicker value={form.departureDate} onChange={upd('departureDate')} />
                </Field>
                <Field label="Личные расходы в UK" hint="В местной валюте">
                  <TextInput value={form.ukExpenses} onChange={upd('ukExpenses')} />
                </Field>
              </Row3>
              <Field label="Описание поездки">
                <TextArea value={form.tripDescription} onChange={upd('tripDescription')} rows={3} />
              </Field>
            </FormSection>

            <FormSection num="6" title="Родственники в Великобритании">
              <Field label="Есть ли у вас родственники в UK?">
                <YesNo value={form.hasUKRelatives} onChange={upd('hasUKRelatives')} />
              </Field>
              {form.hasUKRelatives==='yes' && (<>
                <Row2>
                  <Field label="Имя родственника">
                    <TextInput value={form.relativeName} onChange={upd('relativeName')} />
                  </Field>
                  <Field label="Степень родства">
                    <TextInput value={form.relativeRelation} onChange={upd('relativeRelation')} />
                  </Field>
                </Row2>
                <Row3>
                  <Field label="Гражданство родственника">
                    <TextInput value={form.relativeCitizenship} onChange={upd('relativeCitizenship')} />
                  </Field>
                  <Field label="Статус пребывания в UK">
                    <TextInput value={form.relativeUKStatus} onChange={upd('relativeUKStatus')} />
                  </Field>
                  <Field label="Номер паспорта родственника">
                    <TextInput value={form.relativePassport} onChange={upd('relativePassport')} />
                  </Field>
                </Row3>
              </>)}
            </FormSection>

            <FormSection num="7" title="Проживание в Великобритании">
              <Field label="Где будете жить в UK?">
                <SelectInput value={form.ukStayType} onChange={upd('ukStayType')} options={UK_STAY_OPTIONS} />
              </Field>

              {form.ukStayType==='Отель' && (<>
                <Field label="Название отеля">
                  <TextInput value={form.hotelName} onChange={upd('hotelName')} />
                </Field>
                <Field label="Адрес отеля в UK">
                  <TextArea value={form.ukAddress} onChange={upd('ukAddress')} rows={2} />
                </Field>
              </>)}

              {form.ukStayType==='У друзей' && (<>
                <Field label="Адрес проживания в UK">
                  <TextArea value={form.ukAddress} onChange={upd('ukAddress')} rows={2} />
                </Field>
                <Row2>
                  <Field label="Имя принимающего лица">
                    <TextInput value={form.hostName} onChange={upd('hostName')} />
                  </Field>
                  <Field label="Телефон принимающего лица">
                    <TextInput value={form.hostPhone} onChange={upd('hostPhone')} type="tel" />
                  </Field>
                </Row2>
                <Field label="Email принимающего лица">
                  <TextInput value={form.hostEmail} onChange={upd('hostEmail')} type="email" />
                </Field>
              </>)}

              {form.ukStayType==='У родственников' && (<>
                {form.hasUKRelatives==='yes' && (
                  <Field label="Вы будете проживать у родственников, которых указали выше?">
                    <YesNo value={form.stayWithListedRelative} onChange={upd('stayWithListedRelative')} />
                  </Field>
                )}
                {(form.hasUKRelatives!=='yes' || form.stayWithListedRelative==='no') && (<>
                  <Field label="Адрес проживания в UK">
                    <TextArea value={form.ukAddress} onChange={upd('ukAddress')} rows={2} />
                  </Field>
                  <Row2>
                    <Field label="Имя принимающего лица">
                      <TextInput value={form.hostName} onChange={upd('hostName')} />
                    </Field>
                    <Field label="Телефон принимающего лица">
                      <TextInput value={form.hostPhone} onChange={upd('hostPhone')} type="tel" />
                    </Field>
                  </Row2>
                  <Field label="Email принимающего лица">
                    <TextInput value={form.hostEmail} onChange={upd('hostEmail')} type="email" />
                  </Field>
                </>)}
                {form.stayWithListedRelative==='yes' && (
                  <Field label="Адрес проживания в UK">
                    <TextArea value={form.ukAddress} onChange={upd('ukAddress')} rows={2} />
                  </Field>
                )}
              </>)}
            </FormSection>

            <TravelHistorySection data={form.travelHistory} onChange={updTH} />

            <FormSection num="9" title="Сведения о родителях">
              <div style={{marginBottom:20, paddingBottom:20, borderBottom:'1px solid var(--glass-edge-faint)'}}>
                <div style={{fontSize:15, fontWeight:600, color:'var(--text-body)', marginBottom:12}}>Мать</div>
                <Row3>
                  <Field label="Имя и фамилия">
                    <TextInput value={form.motherName} onChange={upd('motherName')} />
                  </Field>
                  <Field label="Дата рождения">
                    <DatePicker value={form.motherDob} onChange={upd('motherDob')} />
                  </Field>
                  <Field label="Гражданство">
                    <TextInput value={form.motherNationality} onChange={upd('motherNationality')} />
                  </Field>
                </Row3>
              </div>
              <div>
                <div style={{fontSize:15, fontWeight:600, color:'var(--text-body)', marginBottom:12}}>Отец</div>
                <Row3>
                  <Field label="Имя и фамилия">
                    <TextInput value={form.fatherName} onChange={upd('fatherName')} />
                  </Field>
                  <Field label="Дата рождения">
                    <DatePicker value={form.fatherDob} onChange={upd('fatherDob')} />
                  </Field>
                  <Field label="Гражданство">
                    <TextInput value={form.fatherNationality} onChange={upd('fatherNationality')} />
                  </Field>
                </Row3>
              </div>
            </FormSection>

            <FormSection num="10" title="Иждивенцы">
              <Field label="Есть ли лица, финансово зависящие от вас?">
                <YesNo value={form.hasDependents} onChange={upd('hasDependents')} />
              </Field>
              {form.hasDependents==='yes' && (
                <Field label="Кто именно?" hint="Имя, возраст, степень родства">
                  <TextArea value={form.dependentsInfo} onChange={upd('dependentsInfo')} rows={3} />
                </Field>
              )}
            </FormSection>

            <FormSection num="11" title="История отказов и нарушений" subtitle="Отвечайте честно — сокрытие информации является основанием для отказа в визе">
              <Field label="Отказывали в визе в любую страну?">
                <YesNo value={form.wasRefused} onChange={upd('wasRefused')} />
              </Field>
              <Field label="Депортировали из какой-либо страны?">
                <YesNo value={form.wasDeported} onChange={upd('wasDeported')} />
              </Field>
              <Field label="Нарушали условия визы или иммиграционный закон?">
                <YesNo value={form.violatedVisa} onChange={upd('violatedVisa')} />
              </Field>
              <Field label="Есть судимости или административные взыскания?">
                <YesNo value={form.hasCriminalRecord} onChange={upd('hasCriminalRecord')} />
              </Field>
              {(form.wasRefused==='yes'||form.wasDeported==='yes'||form.violatedVisa==='yes'||form.hasCriminalRecord==='yes') && (
                <Field label="Подробности" hint="Страна, год, обстоятельства">
                  <TextArea value={form.violationsDetails} onChange={upd('violationsDetails')} rows={4} />
                </Field>
              )}
            </FormSection>

            <FormSection num="12" title="Дополнительная информация">
              <Field label="Любая другая информация для визового офицера" hint="Причина визита, обстоятельства или что-то важное для рассмотрения заявки">
                <TextArea value={form.additionalInfo} onChange={upd('additionalInfo')} rows={4} />
              </Field>
            </FormSection>

            <div style={{
              background:'var(--glass-fill-solid)',
              border:'1px solid var(--glass-edge)',
              borderRadius:'var(--r-xl)',
              padding:'28px 24px',
              textAlign:'center',
            }}>
              <p style={{fontSize:14, color:'var(--text-muted)', marginBottom:20}}>
                Нажимая кнопку, вы соглашаетесь на обработку персональных данных для подготовки визового заявления.
              </p>
              {sendError && (
                <p style={{color:'#e05', fontSize:14, marginBottom:12, textAlign:'center'}}>{sendError}</p>
              )}
              <button type="submit" disabled={sending} style={{
                padding:'16px 48px',
                borderRadius:'var(--r-pill)',
                background:'var(--grad-royal)',
                color:'#fff', fontSize:17, fontWeight:600,
                border:'1px solid rgba(255,255,255,0.18)',
                boxShadow:'var(--glow-mauve), var(--glass-inner)',
                cursor: sending ? 'not-allowed' : 'pointer',
                opacity: sending ? 0.7 : 1,
                fontFamily:'inherit',
              }}>
                {sending ? 'Отправляем...' : 'Отправить анкету'}
              </button>
            </div>

          </form>
        </div>
      </main>

      <Footer />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<FormApp />);
setTimeout(()=>window.lucide&&window.lucide.createIcons(), 80);
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

def build_form():
    write_page('form.html', 'Анкета для визы UK - Royal Visas', [
        HEADER_JS,
        FOOTER_JS,
        FORM_JS,
    ])

if __name__ == '__main__':
    build_uk()
    build_schengen()
    build_index()
    build_form()
    print('\nAll done!')
    print('\nPromo codes (30 one-time, -5 000 руб.):')
    for c in PROMO_CODES:
        print(' ', c)
    print('  KRISKISS (valid until 2026-10-01)')
