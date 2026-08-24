#!/usr/bin/env python3
"""
Builds uk.html, schengen.html, and new index.html from the existing index.html bundle.
"""
import json, base64, gzip, re

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

def write_bundle(lines, manifest, out_path: str, title: str, *, page_js: str = ''):
    """Serialize manifest back and write the output HTML file."""
    import copy
    new_lines = copy.copy(lines)

    # Update manifest line
    mline_prefix = lines[176][:lines[176].index('>')+1]
    mline_suffix = lines[176][lines[176].rindex('<'):]
    new_lines[176] = mline_prefix + json.dumps(manifest, ensure_ascii=False) + mline_suffix

    # Update template (line 182) – re-encode with </script> escaping
    tline = lines[182]
    tstart = tline.index('>') + 1
    tend   = tline.rindex('<')
    raw_json = tline[tstart:tend]
    template_str = json.loads(raw_json)

    # Apply optional page-level JS injections into template
    if page_js:
        # Inject before </body>
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

# ─── component sources ───────────────────────────────────────────────────────

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
  const VISA_LABEL = '🇬🇧 Новая заявка - Royal Visa UK';
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
                          {promoInfo.valid ? 'Скидка 5 000 руб. применена' : promoInfo.msg}
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
            Консульский сбор оплачивается зарубежной банковской картой. Если у вас такой нет - мы поможем оплатить.
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
      {false && <div style={{ position: 'absolute', top: -12, left: 30 }}><Badge tone="accent" dot>Рекомендуем</Badge></div>}
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
            onClick={() => { const el = document.querySelector('#consult'); if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 84, behavior: 'smooth' }); }}>
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
    price: '29 990',
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
              Шенген в 2026 -<br />
              <span style={{
                background: 'var(--grad-royal)', WebkitBackgroundClip: 'text',
                backgroundClip: 'text', color: 'transparent',
              }}>это реально</span>
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
              {[['≈ 70%', 'Одобрений виз'], ['до 2 лет', 'Срок визы'], ['3-4 нед.', 'Решение по заявке']].map(([v, l]) => (
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
              position: 'relative', zIndex: 1, padding: 28, borderRadius: 'var(--r-2xl)',
              background: 'var(--glass-fill)', border: '1px solid var(--glass-edge)',
              boxShadow: 'var(--elev-3), var(--glass-inner)',
              backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
              minHeight: 280, textAlign: 'center', gap: 18,
            }}>
              <div style={{ fontSize: 64 }}>🇪🇺</div>
              <div style={{ fontSize: 'var(--t-h3)', fontWeight: 600, color: 'var(--text-strong)', lineHeight: 1.3 }}>
                27 стран<br />шенгенской зоны
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)', maxWidth: 220, lineHeight: 1.5 }}>
                Одна виза - вся Европа без дополнительных разрешений
              </p>
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
const SCHENGEN_COUNTRIES = [
  { id: 'de', name: 'Германия', flag: '🇩🇪' },
  { id: 'fr', name: 'Франция', flag: '🇫🇷' },
  { id: 'it', name: 'Италия', flag: '🇮🇹' },
  { id: 'es', name: 'Испания', flag: '🇪🇸' },
  { id: 'nl', name: 'Нидерланды', flag: '🇳🇱' },
  { id: 'be', name: 'Бельгия', flag: '🇧🇪' },
  { id: 'at', name: 'Австрия', flag: '🇦🇹' },
  { id: 'ch', name: 'Швейцария', flag: '🇨🇭' },
  { id: 'pl', name: 'Польша', flag: '🇵🇱' },
  { id: 'se', name: 'Швеция', flag: '🇸🇪' },
  { id: 'no', name: 'Норвегия', flag: '🇳🇴' },
  { id: 'dk', name: 'Дания', flag: '🇩🇰' },
  { id: 'fi', name: 'Финляндия', flag: '🇫🇮' },
  { id: 'pt', name: 'Португалия', flag: '🇵🇹' },
  { id: 'gr', name: 'Греция', flag: '🇬🇷' },
  { id: 'cz', name: 'Чехия', flag: '🇨🇿' },
  { id: 'hu', name: 'Венгрия', flag: '🇭🇺' },
  { id: 'sk', name: 'Словакия', flag: '🇸🇰' },
  { id: 'si', name: 'Словения', flag: '🇸🇮' },
  { id: 'hr', name: 'Хорватия', flag: '🇭🇷' },
  { id: 'lt', name: 'Литва', flag: '🇱🇹' },
  { id: 'lv', name: 'Латвия', flag: '🇱🇻' },
  { id: 'ee', name: 'Эстония', flag: '🇪🇪' },
  { id: 'is', name: 'Исландия', flag: '🇮🇸' },
  { id: 'lu', name: 'Люксембург', flag: '🇱🇺' },
  { id: 'li', name: 'Лихтенштейн', flag: '🇱🇮' },
  { id: 'mt', name: 'Мальта', flag: '🇲🇹' },
  { id: 'ro', name: 'Румыния', flag: '🇷🇴' },
  { id: 'bg', name: 'Болгария', flag: '🇧🇬' },
];

function UKMap() {
  const [active, setActive] = React.useState(null);
  return (
    <section id="map" style={{ paddingBlock: 'var(--section-gap)' }}>
      <div className="rv-container">
        <div style={{ textAlign: 'center', maxWidth: 680, margin: '0 auto 12px' }}>
          <span className="rv-eyebrow">Шенгенская зона</span>
          <h2 style={{ fontSize: 'var(--t-h1)', marginTop: 14 }}>Одна виза - вся Европа</h2>
          <p style={{ marginTop: 16, fontSize: 'var(--t-lg)', color: 'var(--text-body)' }}>
            29 стран шенгенской зоны. Одна виза даёт доступ ко всем - без отдельных разрешений.
          </p>
        </div>

        <div style={{ marginTop: 36 }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' }}>
            {SCHENGEN_COUNTRIES.map((c) => {
              const on = active?.id === c.id;
              return (
                <div
                  key={c.id}
                  onMouseEnter={() => setActive(c)}
                  onMouseLeave={() => setActive(null)}
                  style={{
                    padding: '10px 18px', borderRadius: 'var(--r-lg)',
                    display: 'flex', alignItems: 'center', gap: 10,
                    background: on ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
                    border: `1px solid ${on ? 'rgba(182,166,214,0.5)' : 'var(--glass-edge)'}`,
                    backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
                    boxShadow: on ? 'var(--glow-violet), var(--glass-inner)' : 'var(--glass-inner-soft)',
                    transform: on ? 'translateY(-2px)' : 'none',
                    cursor: 'default',
                    transition: 'all .2s ease',
                  }}
                >
                  <span style={{ fontSize: 22, lineHeight: 1 }}>{c.flag}</span>
                  <span style={{ fontSize: 'var(--t-sm)', fontWeight: on ? 600 : 400, color: on ? 'var(--text-strong)' : 'var(--text-body)', whiteSpace: 'nowrap' }}>{c.name}</span>
                </div>
              );
            })}
          </div>
          {active && (
            <div style={{
              marginTop: 24, padding: '16px 24px', borderRadius: 'var(--r-lg)',
              background: 'var(--glass-fill-strong)', border: '1px solid rgba(182,166,214,0.35)',
              backdropFilter: 'var(--glass-blur)', WebkitBackdropFilter: 'var(--glass-blur)',
              display: 'flex', alignItems: 'center', gap: 14, maxWidth: 400, margin: '24px auto 0',
              boxShadow: 'var(--glow-violet), var(--glass-inner)',
            }}>
              <span style={{ fontSize: 36 }}>{active.flag}</span>
              <div>
                <div style={{ fontWeight: 600, color: 'var(--text-strong)', fontSize: 'var(--t-lg)' }}>{active.name}</div>
                <div style={{ color: 'var(--text-muted)', fontSize: 'var(--t-sm)', marginTop: 2 }}>Входит в Шенгенскую зону</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { UKMap });
"""

SCHENGEN_CONSULT_FORM = CONSULT_FORM_UK.replace(
    r"'🇬🇧 Новая заявка - Royal Visa UK'",
    r"'🇪🇺 Новая заявка - Шенгенская виза'"
)

def inject_promos(src: str) -> str:
    return src.replace('__PROMO_CODES__', json.dumps(PROMO_CODES))

# ─── build uk.html ────────────────────────────────────────────────────────────

def build_uk():
    lines, manifest = load_bundle('/home/user/ukvisa/index.html')

    # ConsultForm with promo codes
    manifest['4ccf8b6e-9863-4ccf-8411-475d3a657df9']['data'] = pack(inject_promos(CONSULT_FORM_UK))

    # Services with 29 990
    manifest['072e9989-17ac-4031-8550-5080c67b7c43']['data'] = pack(SERVICES_29990)

    write_bundle(lines, manifest, '/home/user/ukvisa/uk.html',
                 'Royal Visa UK - Визы в Великобританию')

# ─── build schengen.html ─────────────────────────────────────────────────────

def build_schengen():
    lines, manifest = load_bundle('/home/user/ukvisa/index.html')

    # Hero - Schengen version
    manifest['d8b75256-d161-4203-a466-a96659caa0e7']['data'] = pack(SCHENGEN_HERO)

    # AboutVisa - Schengen version
    manifest['afcfe05f-048b-413e-9060-b183e4dc0578']['data'] = pack(SCHENGEN_ABOUT)

    # UKMap -> SchengenMap (same UUID, different content, exports UKMap)
    manifest['44cc7cd7-30a7-4ae5-b112-9943037e47e5']['data'] = pack(SCHENGEN_MAP)

    # ConsultForm with promo codes and Schengen label
    manifest['4ccf8b6e-9863-4ccf-8411-475d3a657df9']['data'] = pack(inject_promos(SCHENGEN_CONSULT_FORM))

    # Services with 29 990
    manifest['072e9989-17ac-4031-8550-5080c67b7c43']['data'] = pack(SERVICES_29990)

    # Update Header/Footer nav - "О визе" eyebrow says Schengen context
    # (keep existing header/footer - they are generic enough)

    write_bundle(lines, manifest, '/home/user/ukvisa/schengen.html',
                 'Royal Visa - Шенгенская виза')

# ─── build new index.html (landing page) ─────────────────────────────────────

INDEX_HTML = """\
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Royal Visa - Визовый сервис</title>
  <meta name="description" content="Визы в Великобританию и Шенгенскую зону. Оформление под ключ с 2022 года.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #09080f;
      --surface: rgba(255,255,255,0.045);
      --border: rgba(255,255,255,0.1);
      --border-hover: rgba(182,166,214,0.5);
      --text: #f2f0ff;
      --muted: rgba(242,240,255,0.55);
      --accent: #9b8ec4;
      --grad: linear-gradient(135deg, #b6a6d6 0%, #7b68ae 50%, #4f3f8a 100%);
      --glow: rgba(155,142,196,0.3);
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #f4f2ff;
        --surface: rgba(0,0,0,0.04);
        --border: rgba(0,0,0,0.1);
        --text: #1a1528;
        --muted: rgba(26,21,40,0.55);
      }
    }
    body {
      background: var(--bg); color: var(--text);
      font-family: 'Inter', sans-serif; min-height: 100vh;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      padding: 24px;
    }
    .logo { height: 44px; margin-bottom: 48px; }
    .eyebrow {
      font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
      color: var(--accent); font-weight: 600; margin-bottom: 16px; text-align: center;
    }
    h1 {
      font-size: clamp(28px, 5vw, 44px); font-weight: 700; text-align: center;
      line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 12px;
    }
    .sub {
      font-size: 17px; color: var(--muted); text-align: center;
      max-width: 480px; line-height: 1.6; margin-bottom: 52px;
    }
    .cards {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px; width: 100%; max-width: 680px;
    }
    .card {
      display: flex; flex-direction: column;
      padding: 32px 28px; border-radius: 20px;
      background: var(--surface); border: 1px solid var(--border);
      backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
      text-decoration: none; color: inherit;
      transition: border-color .2s ease, transform .2s ease, box-shadow .2s ease;
      cursor: pointer;
    }
    .card:hover {
      border-color: var(--border-hover);
      transform: translateY(-4px);
      box-shadow: 0 16px 48px var(--glow);
    }
    .card-flag { font-size: 48px; margin-bottom: 18px; }
    .card-title { font-size: 22px; font-weight: 700; margin-bottom: 8px; }
    .card-desc { font-size: 14px; color: var(--muted); line-height: 1.55; flex: 1; }
    .card-link {
      display: inline-flex; align-items: center; gap: 6px;
      margin-top: 24px; font-size: 14px; font-weight: 600; color: var(--accent);
    }
    .card-link svg { width: 16px; height: 16px; }
    .footer-note {
      margin-top: 52px; font-size: 12px; color: var(--muted);
      text-align: center; max-width: 480px; line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="eyebrow">Визовый сервис с 2022 года</div>
  <h1>Какая виза вас&nbsp;интересует?</h1>
  <p class="sub">Помогаем оформить визу под ключ - от анкеты до подачи документов.</p>

  <div class="cards">
    <a href="uk.html" class="card">
      <div class="card-flag">🇬🇧</div>
      <div class="card-title">Виза в&nbsp;Великобританию</div>
      <p class="card-desc">
        96% одобрений. Виза от 6 месяцев до 10 лет с многократным въездом.
        Один из самых надёжных вариантов для путешествий.
      </p>
      <div class="card-link">
        Узнать подробнее
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </div>
    </a>

    <a href="schengen.html" class="card">
      <div class="card-flag">🇪🇺</div>
      <div class="card-title">Шенгенская виза</div>
      <p class="card-desc">
        29 стран Европы по одной визе. Сложнее, чем раньше, но реально.
        Есть случаи выдачи на 2 года даже в 2026 году.
      </p>
      <div class="card-link">
        Узнать подробнее
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </div>
    </a>
  </div>

  <p class="footer-note">
    Royal Visa - частный визовый сервис. Мы не являемся государственным органом
    и не аффилированы с UKVI или посольствами. Решение по визе принимает консульство.
  </p>
</body>
</html>
"""

def build_index():
    with open('/home/user/ukvisa/index.html', 'w', encoding='utf-8') as f:
        f.write(INDEX_HTML)
    print('Written: /home/user/ukvisa/index.html')

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
