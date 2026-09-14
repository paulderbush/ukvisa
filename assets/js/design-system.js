/* @ds-bundle: {"format":3,"namespace":"RoyalVisaUKDesignSystem_ccc97c","components":[{"name":"Avatar","sourcePath":"components/core/Avatar.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"GlassCard","sourcePath":"components/core/GlassCard.jsx"},{"name":"Stat","sourcePath":"components/core/Stat.jsx"},{"name":"Accordion","sourcePath":"components/disclosure/Accordion.jsx"},{"name":"AccordionItem","sourcePath":"components/disclosure/Accordion.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Switch","sourcePath":"components/forms/Switch.jsx"}],"sourceHashes":{"components/core/Avatar.jsx":"d983e55f8351","components/core/Badge.jsx":"8e4004a7ae1a","components/core/Button.jsx":"03d29d4dcfb8","components/core/GlassCard.jsx":"b3d4901f0a7c","components/core/Stat.jsx":"fe68d4483031","components/disclosure/Accordion.jsx":"0880cbe475e4","components/forms/Input.jsx":"32d4a766198f","components/forms/Switch.jsx":"c215bd5d2d08","ui_kits/website/AboutVisa.jsx":"0c619b40eea9","ui_kits/website/App.jsx":"d65b85ea3de5","ui_kits/website/ConsultForm.jsx":"04840b8a8e6c","ui_kits/website/Footer.jsx":"79cc5d638772","ui_kits/website/Header.jsx":"d35ad3986764","ui_kits/website/Hero.jsx":"93f35ddff19d","ui_kits/website/Services.jsx":"7941cec25ad8","ui_kits/website/UKMap.jsx":"7d0a672838de","ui_kits/website/image-slot.js":"9309434cb09c"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.RoyalVisaUKDesignSystem_ccc97c = window.RoyalVisaUKDesignSystem_ccc97c || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - Avatar
 * Glass-framed avatar. Shows an image, or initials over a palette gradient.
 */
function Avatar({
  src = null,
  name = '',
  size = 44,
  gradient = 'var(--grad-twilight)',
  ring = true,
  style = {},
  ...rest
}) {
  const initials = name.split(' ').filter(Boolean).slice(0, 2).map(p => p[0].toUpperCase()).join('');
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      position: 'relative',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: size,
      height: size,
      borderRadius: '50%',
      background: src ? 'transparent' : gradient,
      color: '#fff',
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--w-semibold)',
      fontSize: Math.round(size * 0.36),
      letterSpacing: '0.01em',
      overflow: 'hidden',
      flex: 'none',
      border: ring ? '1px solid var(--glass-edge-strong)' : 'none',
      boxShadow: 'var(--glass-inner), var(--elev-1)',
      ...style
    }
  }, rest), src ? /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: name,
    style: {
      width: '100%',
      height: '100%',
      objectFit: 'cover'
    }
  }) : /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative'
    }
  }, initials || '·'), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: '50%',
      background: 'var(--glass-specular)',
      pointerEvents: 'none'
    }
  }));
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - Badge
 * Small status capsule in soft glass. Use for visa statuses, tags, counts.
 */
function Badge({
  children,
  tone = 'neutral',
  dot = false,
  icon = null,
  style = {},
  ...rest
}) {
  const tones = {
    neutral: {
      bg: 'var(--glass-fill-strong)',
      fg: 'var(--text-body)',
      dot: 'var(--ink-3)',
      bd: 'var(--glass-edge)'
    },
    accent: {
      bg: 'var(--glass-tint-violet)',
      fg: 'var(--accent-violet)',
      dot: 'var(--accent-violet)',
      bd: 'rgba(182,166,214,0.3)'
    },
    success: {
      bg: 'var(--success-soft)',
      fg: 'var(--success)',
      dot: 'var(--success)',
      bd: 'rgba(111,174,143,0.3)'
    },
    warning: {
      bg: 'var(--warning-soft)',
      fg: 'var(--warning)',
      dot: 'var(--warning)',
      bd: 'rgba(212,162,94,0.3)'
    },
    danger: {
      bg: 'var(--danger-soft)',
      fg: 'var(--danger)',
      dot: 'var(--danger)',
      bd: 'rgba(201,122,130,0.3)'
    },
    info: {
      bg: 'var(--info-soft)',
      fg: 'var(--accent-sky)',
      dot: 'var(--accent-sky)',
      bd: 'rgba(156,184,208,0.3)'
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      height: 24,
      padding: '0 10px',
      fontSize: 'var(--t-xs)',
      fontWeight: 'var(--w-semibold)',
      letterSpacing: '0.01em',
      lineHeight: 1,
      color: t.fg,
      background: t.bg,
      border: `1px solid ${t.bd}`,
      borderRadius: 'var(--r-pill)',
      backdropFilter: 'var(--glass-blur-light)',
      WebkitBackdropFilter: 'var(--glass-blur-light)',
      whiteSpace: 'nowrap',
      ...style
    }
  }, rest), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: '50%',
      background: t.dot,
      flex: 'none'
    }
  }), icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex'
    }
  }, icon), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - Button
 * A liquid-glass capsule. `primary` is a royal gradient with a wet
 * specular cap; `secondary` is neutral glass; `ghost` is bare until hover.
 */
function Button({
  children,
  variant = 'secondary',
  size = 'md',
  icon = null,
  iconRight = null,
  fullWidth = false,
  disabled = false,
  type = 'button',
  onClick,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const [active, setActive] = React.useState(false);
  const sizes = {
    sm: {
      padding: '0 14px',
      height: 34,
      font: 'var(--t-sm)',
      gap: 7
    },
    md: {
      padding: '0 20px',
      height: 44,
      font: 'var(--t-body)',
      gap: 9
    },
    lg: {
      padding: '0 28px',
      height: 54,
      font: 'var(--t-lg)',
      gap: 11
    }
  };
  const s = sizes[size] || sizes.md;
  const base = {
    position: 'relative',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: s.gap,
    height: s.height,
    padding: s.padding,
    width: fullWidth ? '100%' : 'auto',
    fontFamily: 'var(--font-sans)',
    fontSize: s.font,
    fontWeight: 'var(--w-semibold)',
    letterSpacing: '-0.01em',
    borderRadius: 'var(--r-pill)',
    cursor: disabled ? 'not-allowed' : 'pointer',
    border: '1px solid transparent',
    whiteSpace: 'nowrap',
    transition: 'transform .14s ease, box-shadow .2s ease, background .2s ease, opacity .2s ease',
    transform: active && !disabled ? 'scale(0.97)' : hover && !disabled ? 'translateY(-1px)' : 'none',
    opacity: disabled ? 0.45 : 1,
    overflow: 'hidden',
    WebkitBackdropFilter: 'var(--glass-blur)',
    backdropFilter: 'var(--glass-blur)',
    color: 'var(--text-strong)',
    outline: 'none'
  };
  const variants = {
    primary: {
      background: 'var(--grad-royal)',
      borderColor: 'rgba(255,255,255,0.18)',
      color: '#fff',
      boxShadow: hover && !disabled ? 'var(--glow-mauve), var(--glass-inner)' : 'var(--elev-2), var(--glass-inner)'
    },
    secondary: {
      background: hover && !disabled ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
      borderColor: 'var(--glass-edge)',
      boxShadow: 'var(--glass-shadow), var(--glass-inner)'
    },
    ghost: {
      background: hover && !disabled ? 'var(--glass-fill)' : 'transparent',
      borderColor: hover && !disabled ? 'var(--glass-edge-faint)' : 'transparent',
      color: 'var(--text-body)',
      WebkitBackdropFilter: 'none',
      backdropFilter: 'none',
      boxShadow: 'none'
    }
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setActive(false);
    },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false),
    style: {
      ...base,
      ...variants[variant],
      ...style
    }
  }, rest), variant === 'primary' && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: 'inherit',
      background: 'var(--glass-specular)',
      pointerEvents: 'none'
    }
  }), icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      flex: 'none'
    }
  }, icon), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative'
    }
  }, children), iconRight && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      flex: 'none'
    }
  }, iconRight));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/GlassCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - GlassCard
 * The frosted panel that everything sits on. Optional palette tint,
 * optional hover-lift interactivity, and a soft top sheen.
 */
function GlassCard({
  children,
  tint = 'none',
  elevation = 'md',
  interactive = false,
  padding = 24,
  radius = 'var(--r-xl)',
  specular = false,
  style = {},
  onClick,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const tints = {
    none: 'var(--glass-fill)',
    strong: 'var(--glass-fill-strong)',
    violet: 'var(--glass-tint-violet)',
    sky: 'var(--glass-tint-sky)',
    mauve: 'var(--glass-tint-mauve)',
    plum: 'var(--glass-tint-plum)'
  };
  const elev = {
    flat: 'none',
    sm: 'var(--elev-1)',
    md: 'var(--glass-shadow)',
    lg: 'var(--elev-3)'
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      position: 'relative',
      background: tints[tint] || tints.none,
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      border: '1px solid var(--glass-edge)',
      borderRadius: radius,
      padding,
      boxShadow: interactive && hover ? `var(--elev-3), var(--glass-inner)` : `${elev[elevation] || elev.md}, var(--glass-inner)`,
      transform: interactive && hover ? 'translateY(-3px)' : 'none',
      transition: 'transform .22s cubic-bezier(.2,.7,.2,1), box-shadow .22s ease',
      cursor: interactive ? 'pointer' : 'default',
      overflow: 'hidden',
      ...style
    }
  }, rest), specular && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: 'inherit',
      background: 'var(--glass-specular)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative'
    }
  }, children));
}
Object.assign(__ds_scope, { GlassCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/GlassCard.jsx", error: String((e && e.message) || e) }); }

// components/core/Stat.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - Stat
 * A headline metric in Geist Mono with a label and optional trend delta.
 */
function Stat({
  value,
  label,
  delta = null,
  trend = 'up',
  hint = null,
  align = 'left',
  style = {},
  ...rest
}) {
  const trendColor = trend === 'down' ? 'var(--danger)' : trend === 'flat' ? 'var(--ink-3)' : 'var(--success)';
  const arrow = trend === 'down' ? '↓' : trend === 'flat' ? '→' : '↑';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 6,
      alignItems: align === 'center' ? 'center' : 'flex-start',
      textAlign: align,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 'var(--w-medium)',
      fontSize: 'clamp(2rem, 4vw, 2.75rem)',
      letterSpacing: '-0.02em',
      color: 'var(--text-strong)',
      lineHeight: 1
    }
  }, value), delta != null && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 3,
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--t-sm)',
      fontWeight: 'var(--w-medium)',
      color: trendColor
    }
  }, arrow, " ", delta)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-xs)',
      fontWeight: 'var(--w-semibold)',
      letterSpacing: 'var(--track-eyebrow)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)'
    }
  }, label), hint && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--ink-3)'
    }
  }, hint));
}
Object.assign(__ds_scope, { Stat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Stat.jsx", error: String((e && e.message) || e) }); }

// components/disclosure/Accordion.jsx
try { (() => {
/**
 * Royal Visa UK - Accordion
 * Glass FAQ rows that expand. Pass `items`, or compose AccordionItem manually.
 */
function Accordion({
  items = [],
  allowMultiple = false,
  defaultOpen = [],
  style = {}
}) {
  const [open, setOpen] = React.useState(new Set(defaultOpen));
  const toggle = i => {
    setOpen(prev => {
      const next = new Set(allowMultiple ? prev : []);
      if (prev.has(i)) next.delete(i);else next.add(i);
      return next;
    });
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 12,
      ...style
    }
  }, items.map((item, i) => /*#__PURE__*/React.createElement(AccordionItem, {
    key: i,
    question: item.question,
    answer: item.answer,
    isOpen: open.has(i),
    onToggle: () => toggle(i)
  })));
}
function AccordionItem({
  question,
  answer,
  isOpen,
  onToggle
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      background: isOpen ? 'var(--glass-fill-strong)' : hover ? 'var(--glass-fill)' : 'var(--glass-fill-faint)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      border: '1px solid var(--glass-edge)',
      borderRadius: 'var(--r-lg)',
      boxShadow: isOpen ? 'var(--glass-shadow), var(--glass-inner)' : 'var(--glass-inner-soft)',
      overflow: 'hidden',
      transition: 'background .2s ease, box-shadow .2s ease'
    }
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onToggle,
    "aria-expanded": isOpen,
    style: {
      width: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 16,
      padding: '18px 22px',
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      textAlign: 'left',
      font: 'inherit',
      color: 'var(--text-strong)',
      fontSize: 'var(--t-lg)',
      fontWeight: 'var(--w-medium)'
    }
  }, /*#__PURE__*/React.createElement("span", null, question), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 'none',
      width: 26,
      height: 26,
      borderRadius: '50%',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--glass-fill-strong)',
      border: '1px solid var(--glass-edge)',
      color: 'var(--accent-violet)',
      fontSize: 18,
      lineHeight: 1,
      transform: isOpen ? 'rotate(45deg)' : 'rotate(0deg)',
      transition: 'transform .25s cubic-bezier(.34,1.3,.5,1)'
    }
  }, "+")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateRows: isOpen ? '1fr' : '0fr',
      transition: 'grid-template-rows .3s cubic-bezier(.2,.7,.2,1)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '0 22px 20px',
      color: 'var(--text-body)',
      fontSize: 'var(--t-body)',
      lineHeight: 'var(--lh-relaxed)'
    }
  }, answer))));
}
Object.assign(__ds_scope, { Accordion, AccordionItem });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/disclosure/Accordion.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - Input
 * Glass text field with floating-feel label, optional leading icon and error.
 */
function Input({
  label = null,
  placeholder = '',
  value,
  defaultValue,
  onChange,
  type = 'text',
  icon = null,
  error = null,
  hint = null,
  disabled = false,
  id,
  style = {},
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const fieldId = id || React.useId();
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 7,
      width: '100%',
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      fontSize: 'var(--t-sm)',
      fontWeight: 'var(--w-medium)',
      color: 'var(--text-body)'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      height: 48,
      padding: '0 16px',
      background: 'var(--glass-fill)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      border: `1px solid ${error ? 'var(--danger)' : focus ? 'var(--accent-violet)' : 'var(--glass-edge)'}`,
      borderRadius: 'var(--r-md)',
      boxShadow: focus ? 'var(--focus-ring), var(--glass-inner-soft)' : 'var(--glass-inner-soft)',
      opacity: disabled ? 0.5 : 1,
      transition: 'border-color .18s ease, box-shadow .18s ease'
    }
  }, icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      color: 'var(--ink-3)',
      flex: 'none'
    }
  }, icon), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    type: type,
    value: value,
    defaultValue: defaultValue,
    placeholder: placeholder,
    onChange: onChange,
    disabled: disabled,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      flex: 1,
      minWidth: 0,
      border: 'none',
      outline: 'none',
      background: 'transparent',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--t-body)',
      color: 'var(--text-strong)'
    }
  }, rest))), error ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--danger)'
    }
  }, error) : hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--ink-3)'
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Royal Visa UK - Switch
 * The signature liquid-glass toggle. A frosted capsule track with a wet
 * glass orb that slides; the "on" state fills the track with a palette
 * gradient seen through the glass.
 */
function Switch({
  checked,
  defaultChecked = false,
  onChange,
  disabled = false,
  size = 'md',
  accent = 'var(--grad-twilight)',
  label = null,
  id,
  style = {},
  ...rest
}) {
  const isControlled = checked !== undefined;
  const [internal, setInternal] = React.useState(defaultChecked);
  const on = isControlled ? checked : internal;
  const fieldId = id || React.useId();
  const dims = {
    sm: {
      w: 42,
      h: 24,
      pad: 3
    },
    md: {
      w: 54,
      h: 32,
      pad: 4
    },
    lg: {
      w: 66,
      h: 38,
      pad: 4
    }
  }[size] || {
    w: 54,
    h: 32,
    pad: 4
  };
  const knob = dims.h - dims.pad * 2;
  const toggle = () => {
    if (disabled) return;
    const next = !on;
    if (!isControlled) setInternal(next);
    onChange && onChange(next);
  };
  const control = /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    role: "switch",
    "aria-checked": on,
    "aria-labelledby": label ? fieldId : undefined,
    onClick: toggle,
    disabled: disabled,
    style: {
      position: 'relative',
      width: dims.w,
      height: dims.h,
      flex: 'none',
      padding: 0,
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      borderRadius: 'var(--r-pill)',
      background: 'var(--glass-fill-strong)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.45), var(--glass-inner-soft)',
      opacity: disabled ? 0.5 : 1,
      outline: 'none',
      overflow: 'hidden',
      transition: 'background .25s ease'
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: 'inherit',
      background: accent,
      opacity: on ? 1 : 0,
      transition: 'opacity .28s ease'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: 'inherit',
      border: '1px solid var(--glass-edge)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      top: dims.pad,
      left: dims.pad,
      width: knob,
      height: knob,
      borderRadius: '50%',
      background: 'linear-gradient(180deg, rgba(255,255,255,0.95), rgba(232,232,240,0.82))',
      boxShadow: '0 2px 6px rgba(0,0,0,0.45), inset 0 1px 1px rgba(255,255,255,0.9), inset 0 -2px 3px rgba(0,0,0,0.12)',
      transform: on ? `translateX(${dims.w - dims.h}px)` : 'translateX(0)',
      transition: 'transform .28s cubic-bezier(.34,1.4,.5,1)'
    }
  }));
  if (!label) return /*#__PURE__*/React.createElement("span", {
    style: style
  }, control);
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 12,
      cursor: disabled ? 'not-allowed' : 'pointer',
      ...style
    }
  }, control, /*#__PURE__*/React.createElement("span", {
    id: fieldId,
    style: {
      fontSize: 'var(--t-body)',
      color: 'var(--text-body)'
    }
  }, label));
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Switch.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/AboutVisa.jsx
try { (() => {
/* global React */
function AboutVisa() {
  const {
    Badge
  } = window.RoyalVisaUKDesignSystem_ccc97c;
  const points = [{
    icon: 'pound-sterling',
    title: 'Дешевле, чем кажется',
    text: 'Британская виза часто выходит выгоднее новых сборов и переплат за редкие слоты Шенгена.'
  }, {
    icon: 'calendar-check',
    title: 'Виза от 6 месяцев',
    text: 'Минимальный срок - полгода. Есть варианты на 2, 5 и 10 лет с многократным въездом.'
  }, {
    icon: 'badge-check',
    title: 'Высокий процент одобрений',
    text: 'При правильно собранном пакете документов одобряют подавляющее большинство заявлений.'
  }];
  return /*#__PURE__*/React.createElement("section", {
    id: "about",
    style: {
      paddingBlock: 'var(--section-gap)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-about-grid",
    style: {
      display: 'grid',
      gridTemplateColumns: '0.95fr 1.05fr',
      gap: 56,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: -24,
      borderRadius: 'var(--r-2xl)',
      background: 'var(--grad-twilight)',
      filter: 'blur(54px)',
      opacity: 0.34,
      zIndex: 0
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 1,
      padding: 12,
      borderRadius: 'var(--r-2xl)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      boxShadow: 'var(--elev-3), var(--glass-inner)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__rv('towerbridge', 'assets/photos/tower-bridge.jpg'),
    alt: "\u0422\u0430\u0443\u044D\u0440\u0441\u043A\u0438\u0439 \u043C\u043E\u0441\u0442, \u041B\u043E\u043D\u0434\u043E\u043D",
    style: {
      display: 'block',
      width: '100%',
      height: 'auto',
      borderRadius: 24
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 26,
      bottom: 26,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      padding: '12px 16px',
      borderRadius: 'var(--r-pill)',
      background: 'var(--glass-fill-solid)',
      border: '1px solid var(--glass-edge)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: 'var(--glass-inner)'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "map-pin",
    style: {
      width: 16,
      height: 16,
      color: 'var(--accent-violet)',
      flex: 'none'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--text-strong)',
      fontWeight: 500
    }
  }, "\u0422\u0430\u0443\u044D\u0440\u0441\u043A\u0438\u0439 \u043C\u043E\u0441\u0442, \u041B\u043E\u043D\u0434\u043E\u043D")))), /*#__PURE__*/React.createElement("div", {
    className: "rv-about-copy"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "rv-eyebrow"
  }, "\u041E \u0432\u0438\u0437\u0435")), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--t-h2)'
    }
  }, "\u0428\u0435\u043D\u0433\u0435\u043D \u0437\u0430\u043A\u0440\u044B\u0432\u0430\u0435\u0442\u0441\u044F. \u0411\u0440\u0438\u0442\u0430\u043D\u0438\u044F\xA0\u2014 \u043D\u0435\u0442"), /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 18,
      fontSize: 'var(--t-lg)',
      color: 'var(--text-body)',
      lineHeight: 'var(--lh-relaxed)'
    }
  }, "\u041F\u043E\u043B\u0443\u0447\u0438\u0442\u044C \u0448\u0435\u043D\u0433\u0435\u043D\u0441\u043A\u0443\u044E \u0432\u0438\u0437\u0443 \u0438\u0437 \u0420\u043E\u0441\u0441\u0438\u0438 \u0441\u0442\u0430\u043B\u043E \u0434\u043E\u043B\u0433\u043E, \u0434\u043E\u0440\u043E\u0433\u043E \u0438 \u043D\u0435\u043F\u0440\u0435\u0434\u0441\u043A\u0430\u0437\u0443\u0435\u043C\u043E: \u043E\u0447\u0435\u0440\u0435\u0434\u0438, \u043E\u0442\u043A\u0430\u0437\u044B, \u0438\u0441\u0447\u0435\u0437\u0430\u044E\u0449\u0438\u0435 \u0441\u043B\u043E\u0442\u044B. \u0412\u0441\u0451 \u0431\u043E\u043B\u044C\u0448\u0435 \u043F\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0435\u043D\u043D\u0438\u043A\u043E\u0432 \u0432\u044B\u0431\u0438\u0440\u0430\u044E\u0442 \u0412\u0435\u043B\u0438\u043A\u043E\u0431\u0440\u0438\u0442\u0430\u043D\u0438\u044E\xA0\u2014 \u0438 \u043D\u0435 \u0437\u0440\u044F."), /*#__PURE__*/React.createElement("div", {
    className: "rv-about-points",
    style: {
      marginTop: 28,
      display: 'flex',
      flexDirection: 'column',
      gap: 12
    }
  }, points.map(p => /*#__PURE__*/React.createElement("div", {
    key: p.title,
    style: {
      display: 'flex',
      gap: 16,
      padding: 18,
      borderRadius: 'var(--r-lg)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: 'var(--glass-inner-soft)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 'none',
      width: 44,
      height: 44,
      borderRadius: 'var(--r-md)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--glass-tint-violet)',
      border: '1px solid var(--glass-edge)'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": p.icon,
    style: {
      width: 21,
      height: 21,
      color: 'var(--accent-violet)'
    }
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--text-strong)',
      fontWeight: 600,
      fontSize: 'var(--t-lg)'
    }
  }, p.title), /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--t-sm)',
      marginTop: 3,
      lineHeight: 1.55
    }
  }, p.text)))))))));
}
Object.assign(window, {
  AboutVisa
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/AboutVisa.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/App.jsx
try { (() => {
/* global React */
function App() {
  const [menuOpen, setMenuOpen] = React.useState(false);

  // refresh Lucide glyphs after every render / state change
  React.useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });

  // lock scroll while the mobile menu is open
  React.useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : '';
  }, [menuOpen]);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    onOpenMenu: () => setMenuOpen(true)
  }), /*#__PURE__*/React.createElement(MobileMenu, {
    open: menuOpen,
    onClose: () => setMenuOpen(false)
  }), /*#__PURE__*/React.createElement("main", null, /*#__PURE__*/React.createElement(Hero, null), /*#__PURE__*/React.createElement(AboutVisa, null), /*#__PURE__*/React.createElement(UKMap, null), /*#__PURE__*/React.createElement(Services, null), /*#__PURE__*/React.createElement(ConsultForm, null)), /*#__PURE__*/React.createElement(Footer, null));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(App, null));
setTimeout(() => window.lucide && window.lucide.createIcons(), 80);
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/ConsultForm.jsx
try { (() => {
/* global React */
function ChannelButton({
  active,
  icon,
  label,
  onClick
}) {
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onClick,
    style: {
      flex: 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 9,
      height: 48,
      cursor: 'pointer',
      borderRadius: 'var(--r-md)',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--t-body)',
      fontWeight: 600,
      color: active ? '#fff' : 'var(--text-body)',
      background: active ? 'var(--grad-twilight)' : 'var(--glass-fill)',
      border: `1px solid ${active ? 'rgba(255,255,255,0.2)' : 'var(--glass-edge)'}`,
      boxShadow: active ? 'var(--glow-steel), var(--glass-inner)' : 'var(--glass-inner-soft)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      transition: 'all .2s ease'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": icon,
    style: {
      width: 19,
      height: 19
    }
  }), label);
}
function ConsultForm() {
  const {
    Button,
    Input,
    Switch
  } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [channel, setChannel] = React.useState('whatsapp');
  const [sent, setSent] = React.useState(false);
  const [name, setName] = React.useState('');
  const [contact, setContact] = React.useState('');
  const [sending, setSending] = React.useState(false);
  const [error, setError] = React.useState('');
  const [opts, setOpts] = React.useState({
    weekdays: false,
    hours: false,
    anytime: true,
    urgent: false
  });

  // --- Telegram delivery ---
  // NOTE: this token is visible in the page source. For production, move sending
  // behind a small server/serverless proxy so the token stays secret.
  const TG_TOKEN = '8677081622:AAHAvOYbY50uCZnx9QimTXDO98CYJnMnvxA';
  const TG_CHAT_ID = '-5235367527'; // your Telegram group id (bot must be a member)

  const resolveChatId = async () => {
    if (TG_CHAT_ID) return TG_CHAT_ID;
    const r = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/getUpdates');
    const j = await r.json();
    const ups = j.result || [];
    for (let i = ups.length - 1; i >= 0; i--) {
      const m = ups[i].message || ups[i].my_chat_member || ups[i].edited_message;
      if (m && m.chat && m.chat.id) return m.chat.id;
    }
    throw new Error('chat id not found - send /start to the bot first');
  };
  const switchChannel = c => {
    setChannel(c);
    setContact('');
    setError('');
  };
  const submit = async e => {
    e.preventDefault();
    setError('');
    setSending(true);
    try {
      const chatId = await resolveChatId();
      const when = [];
      if (opts.weekdays) when.push('только будни');
      if (opts.hours) when.push('рабочие часы (до 18:00)');
      if (opts.anytime) when.push('в любое время');
      const text = ['🇬🇧 Новая заявка - Royal Visa UK', 'Имя: ' + (name || '-'), 'Канал: ' + (channel === 'whatsapp' ? 'WhatsApp' : 'Telegram'), 'Контакт: ' + (contact || '-'), 'Когда писать: ' + (when.join(', ') || '-'), opts.urgent ? '⚡ Виза нужна СРОЧНО' : null].filter(Boolean).join('\n');
      const resp = await fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          chat_id: chatId,
          text
        })
      });
      const jr = await resp.json();
      if (!jr.ok) throw new Error(jr.description || 'send failed');
      setSent(true);
    } catch (err) {
      setError('Не удалось отправить заявку. Напишите нам напрямую в WhatsApp или Telegram - кнопки в подвале.');
    } finally {
      setSending(false);
    }
  };
  const setOpt = (k, v) => setOpts(p => {
    const next = {
      ...p,
      [k]: v
    };
    // "в любое время" is mutually exclusive with the two restrictions
    if (k === 'anytime' && v) {
      next.weekdays = false;
      next.hours = false;
    }
    if ((k === 'weekdays' || k === 'hours') && v) next.anytime = false;
    return next;
  });
  const switches = [{
    key: 'weekdays',
    label: 'Писать только в будние дни',
    icon: 'calendar-days'
  }, {
    key: 'hours',
    label: 'Писать только в рабочие часы (до 18:00)',
    icon: 'clock'
  }, {
    key: 'anytime',
    label: 'Писать в любое время',
    icon: 'infinity'
  }, {
    key: 'urgent',
    label: 'Виза нужна срочно',
    icon: 'zap'
  }];
  return /*#__PURE__*/React.createElement("section", {
    id: "consult",
    style: {
      paddingBlock: 'var(--section-gap)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      maxWidth: 620,
      margin: '0 auto 44px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "rv-eyebrow"
  }, "\u0411\u0435\u0441\u043F\u043B\u0430\u0442\u043D\u0430\u044F \u043A\u043E\u043D\u0441\u0443\u043B\u044C\u0442\u0430\u0446\u0438\u044F"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--t-h1)',
      marginTop: 14
    }
  }, "\u041E\u0441\u0442\u0430\u0432\u044C\u0442\u0435 \u0437\u0430\u044F\u0432\u043A\u0443\xA0\u2014 \u043E\u0442\u0432\u0435\u0442\u0438\u043C \u0432 \u043C\u0435\u0441\u0441\u0435\u043D\u0434\u0436\u0435\u0440\u0435"), /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 16,
      fontSize: 'var(--t-lg)',
      color: 'var(--text-body)'
    }
  }, "\u0420\u0430\u0441\u0441\u043A\u0430\u0436\u0435\u043C, \u043A\u0430\u043A\u0430\u044F \u0432\u0438\u0437\u0430 \u043F\u043E\u0434\u0445\u043E\u0434\u0438\u0442 \u0438\u043C\u0435\u043D\u043D\u043E \u0432\u0430\u043C, \u0438 \u043A\u0430\u043A \u0431\u044B\u0441\u0442\u0440\u043E \u0435\u0451 \u043F\u043E\u043B\u0443\u0447\u0438\u0442\u044C.")), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 940,
      margin: '0 auto',
      padding: 8,
      borderRadius: 'var(--r-2xl)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: 'var(--elev-3), var(--glass-inner)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-form-grid",
    style: {
      display: 'grid',
      gridTemplateColumns: '1.1fr 0.9fr',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 28
    }
  }, sent ? /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      minHeight: 320,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 64,
      height: 64,
      borderRadius: '50%',
      background: 'var(--success-soft)',
      border: '1px solid rgba(111,174,143,0.4)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "check",
    style: {
      width: 30,
      height: 30,
      color: 'var(--success)'
    }
  })), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: 'var(--t-h3)'
    }
  }, "\u0417\u0430\u044F\u0432\u043A\u0430 \u043E\u0442\u043F\u0440\u0430\u0432\u043B\u0435\u043D\u0430"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      maxWidth: 320
    }
  }, "\u0421\u0432\u044F\u0436\u0435\u043C\u0441\u044F \u0441 \u0432\u0430\u043C\u0438 \u0432 ", channel === 'whatsapp' ? 'WhatsApp' : 'Telegram', " \u0432 \u0431\u043B\u0438\u0436\u0430\u0439\u0448\u0435\u0435 \u0432\u0440\u0435\u043C\u044F."), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm",
    onClick: () => {
      setSent(false);
      setName('');
      setContact('');
    }
  }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u0435\u0449\u0451 \u043E\u0434\u043D\u0443")) : /*#__PURE__*/React.createElement("form", {
    onSubmit: submit,
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 18
    }
  }, /*#__PURE__*/React.createElement(Input, {
    label: "\u0418\u043C\u044F",
    placeholder: "\u041A\u0430\u043A \u043A \u0432\u0430\u043C \u043E\u0431\u0440\u0430\u0449\u0430\u0442\u044C\u0441\u044F",
    required: true,
    value: name,
    onChange: e => setName(e.target.value),
    icon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "user-round",
      style: {
        width: 17,
        height: 17
      }
    })
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--t-sm)',
      fontWeight: 500,
      color: 'var(--text-body)',
      marginBottom: 8
    }
  }, "\u041A\u0443\u0434\u0430 \u0432\u0430\u043C \u043D\u0430\u043F\u0438\u0441\u0430\u0442\u044C"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(ChannelButton, {
    active: channel === 'whatsapp',
    icon: "message-circle",
    label: "WhatsApp",
    onClick: () => switchChannel('whatsapp')
  }), /*#__PURE__*/React.createElement(ChannelButton, {
    active: channel === 'telegram',
    icon: "send",
    label: "Telegram",
    onClick: () => switchChannel('telegram')
  }))), channel === 'whatsapp' ? /*#__PURE__*/React.createElement(Input, {
    key: "wa",
    label: "\u041D\u043E\u043C\u0435\u0440 \u0442\u0435\u043B\u0435\u0444\u043E\u043D\u0430",
    type: "tel",
    required: true,
    value: contact,
    onChange: e => setContact(e.target.value),
    placeholder: "+7 900 000-00-00",
    icon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "phone",
      style: {
        width: 17,
        height: 17
      }
    })
  }) : /*#__PURE__*/React.createElement(Input, {
    key: "tg",
    label: "\u0412\u0430\u0448 @\u043D\u0438\u043A\u043D\u0435\u0439\u043C",
    required: true,
    value: contact,
    onChange: e => setContact(e.target.value),
    placeholder: "@username",
    icon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "at-sign",
      style: {
        width: 17,
        height: 17
      }
    })
  }), error && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 9,
      alignItems: 'flex-start',
      padding: '12px 14px',
      borderRadius: 'var(--r-md)',
      background: 'var(--danger-soft)',
      border: '1px solid rgba(201,122,130,0.35)'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "triangle-alert",
    style: {
      width: 17,
      height: 17,
      marginTop: 1,
      flex: 'none',
      color: 'var(--danger)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--text-body)',
      lineHeight: 1.45
    }
  }, error)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4
    }
  }, /*#__PURE__*/React.createElement(Button, {
    type: "submit",
    variant: "primary",
    size: "lg",
    fullWidth: true,
    disabled: sending,
    iconRight: !sending && /*#__PURE__*/React.createElement("i", {
      "data-lucide": "arrow-right",
      style: {
        width: 18,
        height: 18
      }
    })
  }, sending ? 'Отправляем…' : 'Отправить заявку')))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 28,
      borderRadius: 'var(--r-xl)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge-faint)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--t-sm)',
      fontWeight: 600,
      letterSpacing: 'var(--track-eyebrow)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)',
      marginBottom: 18
    }
  }, "\u041A\u043E\u0433\u0434\u0430 \u0443\u0434\u043E\u0431\u043D\u043E"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 6
    }
  }, switches.map(s => {
    const on = opts[s.key];
    return /*#__PURE__*/React.createElement("div", {
      key: s.key,
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        padding: '12px 8px',
        borderRadius: 'var(--r-md)',
        background: on ? 'var(--glass-fill)' : 'transparent',
        transition: 'background .2s ease'
      }
    }, /*#__PURE__*/React.createElement("i", {
      "data-lucide": s.icon,
      style: {
        width: 18,
        height: 18,
        flex: 'none',
        color: on ? s.key === 'urgent' ? 'var(--warning)' : 'var(--accent-violet)' : 'var(--ink-3)'
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        fontSize: 'var(--t-body)',
        color: on ? 'var(--text-strong)' : 'var(--text-body)'
      }
    }, s.label), /*#__PURE__*/React.createElement(Switch, {
      checked: on,
      onChange: v => setOpt(s.key, v),
      size: "sm",
      accent: s.key === 'urgent' ? 'var(--grad-royal)' : 'var(--grad-twilight)'
    }));
  })))))));
}
Object.assign(window, {
  ConsultForm
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/ConsultForm.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Footer.jsx
try { (() => {
/* global React */
function Footer() {
  const go = (e, href) => {
    e.preventDefault();
    const el = document.querySelector(href);
    if (el) window.scrollTo({
      top: el.getBoundingClientRect().top + window.scrollY - 84,
      behavior: 'smooth'
    });
  };
  const links = [['#about', 'О визе'], ['#map', 'Виза UK'], ['#services', 'Услуги'], ['#consult', 'Консультация']];
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      paddingTop: 56,
      paddingBottom: 40
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 32,
      borderRadius: 'var(--r-2xl)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: 'var(--glass-shadow), var(--glass-inner)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-footer-top",
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 24,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__rv('wordmark', 'assets/logo/royal-visa-wordmark.svg'),
    alt: "Royal Visa UK",
    style: {
      height: 40
    }
  }), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: 8,
      flexWrap: 'wrap'
    }
  }, links.map(([h, l]) => /*#__PURE__*/React.createElement("a", {
    key: h,
    href: h,
    onClick: e => go(e, h),
    style: {
      padding: '8px 14px',
      borderRadius: 'var(--r-pill)',
      fontSize: 'var(--t-sm)',
      color: 'var(--text-body)'
    }
  }, l))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10
    }
  }, (() => {
    const MSG = 'Здравствуйте! Интересует виза в Великобританию';
    const contacts = [['message-circle', 'WhatsApp', 'https://wa.me/447342193316?text=' + encodeURIComponent(MSG)], ['send', 'Telegram', 'https://t.me/paulderbush'], ['mail', 'E-mail', 'mailto:paul.derbush@icloud.com?subject=' + encodeURIComponent('Виза в Великобританию') + '&body=' + encodeURIComponent(MSG)]];
    return contacts.map(([ic, t, href]) => /*#__PURE__*/React.createElement("a", {
      key: t,
      href: href,
      target: "_blank",
      rel: "noopener noreferrer",
      "aria-label": t,
      style: {
        width: 42,
        height: 42,
        borderRadius: 'var(--r-md)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--glass-fill)',
        border: '1px solid var(--glass-edge)'
      }
    }, /*#__PURE__*/React.createElement("i", {
      "data-lucide": ic,
      style: {
        width: 18,
        height: 18,
        color: 'var(--accent-violet)'
      }
    })));
  })())), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 1,
      background: 'var(--glass-edge-faint)',
      margin: '24px 0'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      gap: 16,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 'var(--t-sm)',
      color: 'var(--text-muted)',
      maxWidth: 560,
      lineHeight: 1.5
    }
  }, "Royal Visa UK\xA0\u2014 \u0447\u0430\u0441\u0442\u043D\u044B\u0439 \u0432\u0438\u0437\u043E\u0432\u044B\u0439 \u0441\u0435\u0440\u0432\u0438\u0441. \u041C\u044B \u043D\u0435 \u044F\u0432\u043B\u044F\u0435\u043C\u0441\u044F \u0433\u043E\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u0435\u043D\u043D\u044B\u043C \u043E\u0440\u0433\u0430\u043D\u043E\u043C \u0438 \u043D\u0435 \u0430\u0444\u0444\u0438\u043B\u0438\u0440\u043E\u0432\u0430\u043D\u044B \u0441 UK Visas\xA0& Immigration. \u0420\u0435\u0448\u0435\u043D\u0438\u0435 \u043F\u043E \u0432\u0438\u0437\u0435 \u043F\u0440\u0438\u043D\u0438\u043C\u0430\u0435\u0442 \u043A\u043E\u043D\u0441\u0443\u043B\u044C\u0441\u0442\u0432\u043E."), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 'var(--t-sm)',
      color: 'var(--ink-3)'
    }
  }, "\xA9 2026 Royal Visa UK")))));
}
Object.assign(window, {
  Footer
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Footer.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Header.jsx
try { (() => {
/* global React */
function Header({
  onOpenMenu
}) {
  const {
    Button
  } = window.RoyalVisaUKDesignSystem_ccc97c;
  const [scrolled, setScrolled] = React.useState(false);
  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, {
      passive: true
    });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  const links = [{
    href: '#about',
    label: 'О визе'
  }, {
    href: '#map',
    label: 'Виза UK'
  }, {
    href: '#services',
    label: 'Услуги'
  }];
  const go = (e, href) => {
    e.preventDefault();
    const el = document.querySelector(href);
    if (el) window.scrollTo({
      top: el.getBoundingClientRect().top + window.scrollY - 84,
      behavior: 'smooth'
    });
  };
  return /*#__PURE__*/React.createElement("header", {
    style: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 50,
      transition: 'background .3s ease, box-shadow .3s ease, border-color .3s ease',
      background: scrolled ? 'var(--glass-fill-solid)' : 'transparent',
      backdropFilter: scrolled ? 'var(--glass-blur)' : 'none',
      WebkitBackdropFilter: scrolled ? 'var(--glass-blur)' : 'none',
      borderBottom: `1px solid ${scrolled ? 'var(--glass-edge-faint)' : 'transparent'}`,
      boxShadow: scrolled ? 'var(--elev-1)' : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container",
    style: {
      height: 72,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "#top",
    onClick: e => go(e, '#top'),
    style: {
      display: 'flex',
      alignItems: 'center',
      flex: 'none'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__rv('wordmark', 'assets/logo/royal-visa-wordmark.svg'),
    alt: "Royal Visa UK",
    style: {
      height: 40
    }
  })), /*#__PURE__*/React.createElement("nav", {
    className: "rv-desktop-nav",
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6
    }
  }, links.map(l => /*#__PURE__*/React.createElement("a", {
    key: l.href,
    href: l.href,
    onClick: e => go(e, l.href),
    style: {
      padding: '9px 16px',
      borderRadius: 'var(--r-pill)',
      fontSize: 'var(--t-sm)',
      fontWeight: 'var(--w-medium)',
      color: 'var(--text-body)',
      transition: 'color .15s, background .15s'
    },
    onMouseEnter: e => {
      e.currentTarget.style.color = 'var(--text-strong)';
      e.currentTarget.style.background = 'var(--glass-fill)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.color = 'var(--text-body)';
      e.currentTarget.style.background = 'transparent';
    }
  }, l.label)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 10
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "sm",
    onClick: e => go(e, '#consult')
  }, "\u0411\u0435\u0441\u043F\u043B\u0430\u0442\u043D\u0430\u044F \u043A\u043E\u043D\u0441\u0443\u043B\u044C\u0442\u0430\u0446\u0438\u044F"))), /*#__PURE__*/React.createElement("button", {
    className: "rv-burger",
    "aria-label": "\u041C\u0435\u043D\u044E",
    onClick: onOpenMenu,
    style: {
      display: 'none',
      width: 46,
      height: 46,
      flex: 'none',
      cursor: 'pointer',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 'var(--r-md)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      boxShadow: 'var(--glass-inner-soft)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "menu",
    style: {
      width: 22,
      height: 22,
      color: 'var(--text-strong)'
    }
  }))));
}
function MobileMenu({
  open,
  onClose
}) {
  const {
    Button
  } = window.RoyalVisaUKDesignSystem_ccc97c;
  const links = [{
    href: '#about',
    label: 'О визе'
  }, {
    href: '#map',
    label: 'Виза UK'
  }, {
    href: '#services',
    label: 'Услуги'
  }];
  const go = (e, href) => {
    e.preventDefault();
    onClose();
    setTimeout(() => {
      const el = document.querySelector(href);
      if (el) window.scrollTo({
        top: el.getBoundingClientRect().top + window.scrollY - 84,
        behavior: 'smooth'
      });
    }, 240);
  };
  return /*#__PURE__*/React.createElement("div", {
    "aria-hidden": !open,
    style: {
      position: 'fixed',
      inset: 0,
      zIndex: 60,
      pointerEvents: open ? 'auto' : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: 'absolute',
      inset: 0,
      background: 'rgba(8,7,13,0.62)',
      backdropFilter: open ? 'blur(28px) saturate(140%)' : 'blur(0px)',
      WebkitBackdropFilter: open ? 'blur(28px) saturate(140%)' : 'blur(0px)',
      opacity: open ? 1 : 0,
      transition: 'opacity .32s ease, backdrop-filter .32s ease'
    }
  }), /*#__PURE__*/React.createElement("button", {
    "aria-label": "\u0417\u0430\u043A\u0440\u044B\u0442\u044C",
    onClick: onClose,
    style: {
      position: 'absolute',
      top: 18,
      right: 18,
      zIndex: 2,
      width: 48,
      height: 48,
      cursor: 'pointer',
      borderRadius: '50%',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      opacity: open ? 1 : 0,
      transition: 'opacity .3s ease'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "x",
    style: {
      width: 22,
      height: 22,
      color: 'var(--text-strong)'
    }
  })), /*#__PURE__*/React.createElement("nav", {
    style: {
      position: 'absolute',
      inset: 0,
      zIndex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 34,
      padding: 24,
      opacity: open ? 1 : 0,
      transform: open ? 'translateY(0)' : 'translateY(12px)',
      transition: 'opacity .32s ease, transform .4s cubic-bezier(.2,.8,.2,1)',
      pointerEvents: open ? 'auto' : 'none'
    }
  }, links.map(l => /*#__PURE__*/React.createElement("a", {
    key: l.href,
    href: l.href,
    onClick: e => go(e, l.href),
    style: {
      fontSize: 30,
      fontWeight: 'var(--w-semibold)',
      letterSpacing: '-0.02em',
      color: 'var(--text-strong)'
    }
  }, l.label)), /*#__PURE__*/React.createElement("a", {
    href: "#consult",
    onClick: e => go(e, '#consult'),
    style: {
      marginTop: 8,
      padding: '16px 34px',
      borderRadius: 'var(--r-pill)',
      background: 'var(--grad-royal)',
      color: '#fff',
      fontSize: 19,
      fontWeight: 'var(--w-semibold)',
      border: '1px solid rgba(255,255,255,0.18)',
      boxShadow: 'var(--glow-mauve), var(--glass-inner)'
    }
  }, "\u0411\u0435\u0441\u043F\u043B\u0430\u0442\u043D\u0430\u044F \u043A\u043E\u043D\u0441\u0443\u043B\u044C\u0442\u0430\u0446\u0438\u044F")));
}
Object.assign(window, {
  Header,
  MobileMenu
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Hero.jsx
try { (() => {
/* global React */
function Hero() {
  const {
    Button,
    Badge
  } = window.RoyalVisaUKDesignSystem_ccc97c;
  const go = (e, href) => {
    e.preventDefault();
    const el = document.querySelector(href);
    if (el) window.scrollTo({
      top: el.getBoundingClientRect().top + window.scrollY - 84,
      behavior: 'smooth'
    });
  };
  return /*#__PURE__*/React.createElement("section", {
    id: "top",
    style: {
      position: 'relative',
      paddingTop: 132,
      paddingBottom: 96
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-hero-grid",
    style: {
      display: 'grid',
      gridTemplateColumns: '1.05fr 0.95fr',
      gap: 56,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-hero-copy"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 22
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "accent",
    dot: true
  }, "\u0412\u0438\u0437\u044B \u0432 \u0412\u0435\u043B\u0438\u043A\u043E\u0431\u0440\u0438\u0442\u0430\u043D\u0438\u044E \xB7 \u0441 2014 \u0433\u043E\u0434\u0430")), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--t-display)',
      letterSpacing: 'var(--track-tight)',
      lineHeight: 1.02
    }
  }, "\u0412\u0430\u0448\u0430 \u0432\u0438\u0437\u0430 \u0432\xA0\u0421\u043E\u0435\u0434\u0438\u043D\u0451\u043D\u043D\u043E\u0435", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("span", {
    style: {
      background: 'var(--grad-royal)',
      WebkitBackgroundClip: 'text',
      backgroundClip: 'text',
      color: 'transparent'
    }
  }, "\u041A\u043E\u0440\u043E\u043B\u0435\u0432\u0441\u0442\u0432\u043E")), /*#__PURE__*/React.createElement("p", {
    className: "rv-hero-lead",
    style: {
      marginTop: 22,
      fontSize: 'var(--t-lg)',
      color: 'var(--text-body)',
      maxWidth: 520,
      lineHeight: 'var(--lh-relaxed)'
    }
  }, "\u041F\u043E\u043A\u0430 \u0428\u0435\u043D\u0433\u0435\u043D \u0437\u0430\u043A\u0440\u044B\u0432\u0430\u0435\u0442\u0441\u044F, \u0411\u0440\u0438\u0442\u0430\u043D\u0438\u044F \u043E\u0442\u043A\u0440\u044B\u0432\u0430\u0435\u0442\u0441\u044F. \u041F\u043E\u043C\u043E\u0436\u0435\u043C \u043E\u0444\u043E\u0440\u043C\u0438\u0442\u044C \u0432\u0438\u0437\u0443 \u0432\xA0UK\xA0\u2014 \u043E\u0442 \u0441\u043B\u043E\u0442\u0430 \u0432 \u0432\u0438\u0437\u043E\u0432\u043E\u043C \u0446\u0435\u043D\u0442\u0440\u0435 \u0434\u043E \u0433\u043E\u0442\u043E\u0432\u043E\u0433\u043E \u043F\u0430\u043A\u0435\u0442\u0430 \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432."), /*#__PURE__*/React.createElement("div", {
    className: "rv-hero-actions",
    style: {
      marginTop: 32,
      display: 'flex',
      gap: 14,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    iconRight: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "arrow-right",
      style: {
        width: 18,
        height: 18
      }
    }),
    onClick: e => go(e, '#consult')
  }, "\u0411\u0435\u0441\u043F\u043B\u0430\u0442\u043D\u0430\u044F \u043A\u043E\u043D\u0441\u0443\u043B\u044C\u0442\u0430\u0446\u0438\u044F"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "lg",
    onClick: e => go(e, '#services')
  }, "\u0422\u0430\u0440\u0438\u0444\u044B \u0438 \u0446\u0435\u043D\u044B")), /*#__PURE__*/React.createElement("div", {
    className: "rv-hero-stats",
    style: {
      marginTop: 40,
      display: 'flex',
      gap: 36,
      flexWrap: 'wrap'
    }
  }, [['96%', 'Одобрений виз'], ['от 6 мес.', 'Срок визы'], ['3–8 нед.', 'Решение по заявке']].map(([v, l]) => /*#__PURE__*/React.createElement("div", {
    key: l
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 28,
      fontWeight: 500,
      letterSpacing: '-0.02em',
      color: 'var(--text-strong)'
    }
  }, v), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--text-muted)',
      marginTop: 2
    }
  }, l))))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: -30,
      borderRadius: '50%',
      background: 'var(--grad-royal)',
      filter: 'blur(60px)',
      opacity: 0.42,
      zIndex: 0
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 1,
      padding: 12,
      borderRadius: 'var(--r-2xl)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      boxShadow: 'var(--elev-3), var(--glass-inner)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__rv('bigben', 'assets/photos/bigben.jpg'),
    alt: "\u0411\u0438\u0433-\u0411\u0435\u043D, \u0412\u0435\u0441\u0442\u043C\u0438\u043D\u0441\u0442\u0435\u0440",
    style: {
      display: 'block',
      width: '100%',
      height: 'auto',
      borderRadius: 24
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 26,
      bottom: 26,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      padding: '12px 16px',
      borderRadius: 'var(--r-pill)',
      background: 'var(--glass-fill-solid)',
      border: '1px solid var(--glass-edge)',
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: 'var(--glass-inner)'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "map-pin",
    style: {
      width: 16,
      height: 16,
      color: 'var(--accent-violet)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-sm)',
      color: 'var(--text-strong)',
      fontWeight: 500
    }
  }, "\u0411\u0438\u0433-\u0411\u0435\u043D (\u042D\u043B\u0438\u0437\u0430\u0431\u0435\u0442-\u0442\u0430\u0443\u044D\u0440), \u041B\u043E\u043D\u0434\u043E\u043D")))))));
}
Object.assign(window, {
  Hero
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Hero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Services.jsx
try { (() => {
/* global React */
const CONSULAR_FEES = [{
  label: 'Туристическая виза на 6 месяцев',
  price: '150 £'
}, {
  label: 'Туристическая виза на 2 года',
  price: '550 £'
}, {
  label: 'Туристическая виза на 5 лет',
  price: '980 £'
}, {
  label: 'Туристическая виза на 10 лет',
  price: '1250 £'
}];
function FeeLink({
  onOpen
}) {
  return /*#__PURE__*/React.createElement("button", {
    onClick: onOpen,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 5,
      padding: 0,
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      font: 'inherit',
      color: 'var(--accent-sky)',
      fontWeight: 600,
      textDecoration: 'underline',
      textUnderlineOffset: 3,
      textDecorationColor: 'rgba(185,210,230,0.45)'
    }
  }, "\u043A\u043E\u043D\u0441\u0443\u043B\u044C\u0441\u043A\u0438\u0439 \u0441\u0431\u043E\u0440", /*#__PURE__*/React.createElement("i", {
    "data-lucide": "info",
    style: {
      width: 14,
      height: 14
    }
  }));
}
function FeeModal({
  open,
  onClose
}) {
  React.useEffect(() => {
    const onKey = e => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);
  return /*#__PURE__*/React.createElement("div", {
    "aria-hidden": !open,
    style: {
      position: 'fixed',
      inset: 0,
      zIndex: 80,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 20,
      pointerEvents: open ? 'auto' : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: 'absolute',
      inset: 0,
      background: 'rgba(8,7,13,0.55)',
      backdropFilter: open ? 'blur(20px) saturate(140%)' : 'blur(0)',
      WebkitBackdropFilter: open ? 'blur(20px) saturate(140%)' : 'blur(0)',
      opacity: open ? 1 : 0,
      transition: 'opacity .28s ease, backdrop-filter .28s ease'
    }
  }), /*#__PURE__*/React.createElement("div", {
    role: "dialog",
    "aria-modal": "true",
    style: {
      position: 'relative',
      width: '100%',
      maxWidth: 480,
      padding: 28,
      borderRadius: 'var(--r-2xl)',
      background: 'var(--glass-fill-strong)',
      border: '1px solid var(--glass-edge-strong)',
      backdropFilter: 'var(--glass-blur-heavy)',
      WebkitBackdropFilter: 'var(--glass-blur-heavy)',
      boxShadow: 'var(--elev-4), var(--glass-inner)',
      transform: open ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.96)',
      opacity: open ? 1 : 0,
      transition: 'transform .32s cubic-bezier(.2,.8,.2,1), opacity .26s ease'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: 'inherit',
      background: 'var(--glass-specular)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("button", {
    "aria-label": "\u0417\u0430\u043A\u0440\u044B\u0442\u044C",
    onClick: onClose,
    style: {
      position: 'absolute',
      top: 16,
      right: 16,
      width: 36,
      height: 36,
      cursor: 'pointer',
      borderRadius: 'var(--r-sm)',
      background: 'var(--glass-fill)',
      border: '1px solid var(--glass-edge)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "x",
    style: {
      width: 18,
      height: 18,
      color: 'var(--text-strong)'
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 46,
      height: 46,
      borderRadius: 'var(--r-md)',
      marginBottom: 16,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--glass-tint-sky)',
      border: '1px solid var(--glass-edge)'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "credit-card",
    style: {
      width: 22,
      height: 22,
      color: 'var(--accent-sky)'
    }
  })), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 'var(--t-lg)',
      color: 'var(--text-strong)',
      lineHeight: 1.45,
      fontWeight: 500
    }
  }, "\u041A\u043E\u043D\u0441\u0443\u043B\u044C\u0441\u043A\u0438\u0439 \u0441\u0431\u043E\u0440 \u043E\u043F\u043B\u0430\u0447\u0438\u0432\u0430\u0435\u0442\u0441\u044F \u0437\u0430\u0440\u0443\u0431\u0435\u0436\u043D\u043E\u0439 \u0431\u0430\u043D\u043A\u043E\u0432\u0441\u043A\u043E\u0439 \u043A\u0430\u0440\u0442\u043E\u0439. \u0415\u0441\u043B\u0438 \u0443 \u0432\u0430\u0441 \u0442\u0430\u043A\u043E\u0439 \u043D\u0435\u0442\xA0\u2014 \u043C\u044B \u043F\u043E\u043C\u043E\u0436\u0435\u043C \u043E\u043F\u043B\u0430\u0442\u0438\u0442\u044C."), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 22,
      display: 'flex',
      flexDirection: 'column',
      gap: 2
    }
  }, CONSULAR_FEES.map((f, i) => /*#__PURE__*/React.createElement("div", {
    key: f.label,
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 16,
      padding: '14px 4px',
      borderTop: i === 0 ? 'none' : '1px solid var(--glass-edge-faint)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-body)',
      color: 'var(--text-body)'
    }
  }, f.label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--t-lg)',
      fontWeight: 600,
      color: 'var(--text-strong)',
      whiteSpace: 'nowrap'
    }
  }, f.price)))))));
}
function TariffCard({
  data,
  featured,
  onOpenFee
}) {
  const {
    Button,
    Badge
  } = window.RoyalVisaUKDesignSystem_ccc97c;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      padding: 30,
      borderRadius: 'var(--r-xl)',
      background: featured ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
      border: `1px solid ${featured ? 'rgba(182,166,214,0.4)' : 'var(--glass-edge)'}`,
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: featured ? 'var(--elev-3), var(--glass-inner), var(--glow-violet)' : 'var(--glass-shadow), var(--glass-inner)',
      display: 'flex',
      flexDirection: 'column'
    }
  }, featured && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: -12,
      left: 30
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "accent",
    dot: true
  }, "\u0420\u0435\u043A\u043E\u043C\u0435\u043D\u0434\u0443\u0435\u043C")), /*#__PURE__*/React.createElement("h3", {
    className: "rv-tariff-name",
    style: {
      fontSize: 'var(--t-h3)'
    }
  }, data.name), /*#__PURE__*/React.createElement("p", {
    className: "rv-tariff-tagline",
    style: {
      marginTop: 8,
      color: 'var(--text-muted)',
      fontSize: 'var(--t-sm)'
    }
  }, data.tagline), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 12,
      marginTop: 22,
      marginBottom: 24
    }
  }, data.features.map(f => /*#__PURE__*/React.createElement("div", {
    key: f.text,
    style: {
      display: 'flex',
      gap: 11,
      alignItems: 'flex-start'
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": f.you ? 'user-round' : 'check',
    style: {
      width: 18,
      height: 18,
      marginTop: 2,
      flex: 'none',
      color: f.you ? 'var(--accent-violet)' : 'var(--success)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--t-body)',
      color: 'var(--text-body)',
      lineHeight: 1.45
    }
  }, f.text)))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'auto',
      paddingTop: 20,
      borderTop: '1px solid var(--glass-edge-faint)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-tariff-price",
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 8,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 34,
      fontWeight: 600,
      letterSpacing: '-0.02em',
      color: 'var(--text-strong)'
    }
  }, data.price), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--t-sm)'
    }
  }, "\u0440\u0443\u0431.")), /*#__PURE__*/React.createElement("div", {
    className: "rv-tariff-fee",
    style: {
      marginTop: 6,
      fontSize: 'var(--t-sm)',
      color: 'var(--text-muted)'
    }
  }, "+ ", /*#__PURE__*/React.createElement(FeeLink, {
    onOpen: onOpenFee
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 22
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: featured ? 'primary' : 'secondary',
    fullWidth: true,
    size: "lg",
    iconRight: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "arrow-right",
      style: {
        width: 18,
        height: 18
      }
    }),
    onClick: () => {
      const el = document.querySelector('#consult');
      if (el) window.scrollTo({
        top: el.getBoundingClientRect().top + window.scrollY - 84,
        behavior: 'smooth'
      });
    }
  }, "\u0412\u044B\u0431\u0440\u0430\u0442\u044C \u0442\u0430\u0440\u0438\u0444"))));
}
function Services() {
  const [feeOpen, setFeeOpen] = React.useState(false);
  const tariffs = [{
    name: 'Самостоятельный',
    featured: false,
    tagline: 'Вы готовите всё сами - мы ловим слот на подачу.',
    price: '11 990',
    features: [{
      text: 'Вы самостоятельно заполняете анкету',
      you: true
    }, {
      text: 'Вы самостоятельно готовите документы',
      you: true
    }, {
      text: 'Мы помогаем поймать слот в визовый центр на подачу документов'
    }]
  }, {
    name: 'Всё включено',
    featured: true,
    tagline: 'Берём весь процесс на себя - от анкеты до подачи.',
    price: '24 990',
    features: [{
      text: 'Мы заполняем анкету за вас'
    }, {
      text: 'Мы готовим полный пакет документов'
    }, {
      text: 'Мы помогаем поймать слот в визовый центр на подачу документов'
    }]
  }];
  return /*#__PURE__*/React.createElement("section", {
    id: "services",
    style: {
      paddingBlock: 'var(--section-gap)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      maxWidth: 620,
      margin: '0 auto 44px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "rv-eyebrow"
  }, "\u0423\u0441\u043B\u0443\u0433\u0438"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--t-h1)',
      marginTop: 14
    }
  }, "\u0414\u0432\u0430 \u0442\u0430\u0440\u0438\u0444\u0430\xA0\u2014 \u043E\u0434\u0438\u043D \u0440\u0435\u0437\u0443\u043B\u044C\u0442\u0430\u0442"), /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 16,
      fontSize: 'var(--t-lg)',
      color: 'var(--text-body)'
    }
  }, "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435, \u0441\u043A\u043E\u043B\u044C\u043A\u043E \u0431\u0435\u0440\u0451\u0442\u0435 \u043D\u0430 \u0441\u0435\u0431\u044F, \u0430 \u0441\u043A\u043E\u043B\u044C\u043A\u043E\xA0\u2014 \u043C\u044B.")), /*#__PURE__*/React.createElement("div", {
    className: "rv-tariffs",
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 24,
      maxWidth: 840,
      margin: '0 auto'
    }
  }, tariffs.map(t => /*#__PURE__*/React.createElement(TariffCard, {
    key: t.name,
    data: t,
    featured: t.featured,
    onOpenFee: () => setFeeOpen(true)
  })))), /*#__PURE__*/React.createElement(FeeModal, {
    open: feeOpen,
    onClose: () => setFeeOpen(false)
  }));
}
Object.assign(window, {
  Services
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Services.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/UKMap.jsx
try { (() => {
/* global React */
const UK_NATIONS = {
  scotland: {
    name: 'Шотландия',
    capital: 'Эдинбург',
    accent: '#4d74d6',
    ref: [60, 100, 200],
    note: 'Хайленд, виски и замки. Та же виза - без отдельного разрешения.'
  },
  england: {
    name: 'Англия',
    capital: 'Лондон',
    accent: '#ef6a33',
    ref: [228, 85, 29],
    note: 'Лондон, Оксфорд, побережье. Сердце поездки по одной визе.'
  },
  wales: {
    name: 'Уэльс',
    capital: 'Кардифф',
    accent: '#f0c419',
    ref: [237, 196, 22],
    note: 'Горы Сноудонии и старинные крепости - и снова без доплат.'
  },
  ni: {
    name: 'Северная Ирландия',
    capital: 'Белфаст',
    accent: '#56b061',
    ref: [86, 160, 84],
    note: 'Та же виза действует и здесь - Дорога гигантов ждёт.'
  }
};
const NATION_ORDER = ['scotland', 'england', 'wales', 'ni'];
function NationInfo({
  id,
  active,
  onHover,
  align
}) {
  const n = UK_NATIONS[id];
  const on = active === id;
  const dim = active && !on;
  return /*#__PURE__*/React.createElement("div", {
    className: "rv-nation",
    onMouseEnter: () => onHover(id),
    onMouseLeave: () => onHover(null),
    style: {
      padding: 18,
      borderRadius: 'var(--r-lg)',
      cursor: 'default',
      textAlign: align === 'right' ? 'right' : 'left',
      background: on ? 'var(--glass-fill-strong)' : 'var(--glass-fill)',
      border: `1px solid ${on ? n.accent : 'var(--glass-edge)'}`,
      backdropFilter: 'var(--glass-blur)',
      WebkitBackdropFilter: 'var(--glass-blur)',
      boxShadow: on ? `0 8px 30px -8px ${n.accent}, var(--glass-inner)` : 'var(--glass-inner-soft)',
      transform: on ? 'translateY(-2px)' : 'none',
      opacity: dim ? 0.55 : 1,
      transition: 'all .22s ease'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-nation-head",
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 9,
      justifyContent: align === 'right' ? 'flex-end' : 'flex-start'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 10,
      borderRadius: '50%',
      background: n.accent,
      flex: 'none',
      boxShadow: '0 0 10px ' + n.accent
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-strong)',
      fontWeight: 600,
      fontSize: 'var(--t-h4)'
    }
  }, n.name)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6,
      fontSize: 'var(--t-xs)',
      letterSpacing: 'var(--track-eyebrow)',
      textTransform: 'uppercase',
      color: n.accent,
      fontWeight: 600
    }
  }, "\u0421\u0442\u043E\u043B\u0438\u0446\u0430 \xB7 ", n.capital), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '8px 0 0',
      fontSize: 'var(--t-sm)',
      color: 'var(--text-muted)',
      lineHeight: 1.5
    }
  }, n.note));
}
function InteractiveUKMap({
  active,
  setActive
}) {
  const wrapRef = React.useRef(null);
  const overlayRef = React.useRef(null);
  const dataRef = React.useRef({
    ready: false,
    labels: null,
    masks: {},
    w: 0,
    h: 0
  });
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    let cancelled = false;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      try {
        const w = 360,
          h = Math.round(360 * img.naturalHeight / img.naturalWidth);
        const c = document.createElement('canvas');
        c.width = w;
        c.height = h;
        const ctx = c.getContext('2d');
        ctx.drawImage(img, 0, 0, w, h);
        const data = ctx.getImageData(0, 0, w, h).data;
        const labels = new Uint8Array(w * h);
        const refs = NATION_ORDER.map(id => UK_NATIONS[id].ref);
        const TH = 115 * 115;
        for (let i = 0; i < w * h; i++) {
          if (data[i * 4 + 3] < 128) {
            labels[i] = 0;
            continue;
          }
          const r = data[i * 4],
            g = data[i * 4 + 1],
            b = data[i * 4 + 2];
          let best = 0,
            bestD = TH;
          for (let k = 0; k < 4; k++) {
            const dr = r - refs[k][0],
              dg = g - refs[k][1],
              db = b - refs[k][2];
            const d = dr * dr + dg * dg + db * db;
            if (d < bestD) {
              bestD = d;
              best = k + 1;
            }
          }
          labels[i] = best;
        }
        const masks = {};
        NATION_ORDER.forEach((id, idx) => {
          const mc = document.createElement('canvas');
          mc.width = w;
          mc.height = h;
          const mctx = mc.getContext('2d');
          const out = mctx.createImageData(w, h);
          const md = out.data;
          for (let i = 0; i < w * h; i++) {
            if (labels[i] === idx + 1) {
              md[i * 4] = data[i * 4];
              md[i * 4 + 1] = data[i * 4 + 1];
              md[i * 4 + 2] = data[i * 4 + 2];
              md[i * 4 + 3] = 255;
            }
          }
          mctx.putImageData(out, 0, 0);
          masks[id] = mc;
        });
        if (cancelled) return;
        dataRef.current = {
          ready: true,
          labels,
          masks,
          w,
          h
        };
        setReady(true);
      } catch (e) {
        dataRef.current.ready = false;
        setReady(true);
      }
    };
    img.src = window.__rv('ukmap', 'assets/uk-map.png');
    return () => {
      cancelled = true;
    };
  }, []);
  React.useEffect(() => {
    const d = dataRef.current;
    const cv = overlayRef.current;
    if (!cv || !d.ready) return;
    if (cv.width !== d.w) {
      cv.width = d.w;
      cv.height = d.h;
    }
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, d.w, d.h);
    if (active && d.masks[active]) ctx.drawImage(d.masks[active], 0, 0);
  }, [active, ready]);
  const onMove = e => {
    const d = dataRef.current;
    if (!d.ready || !wrapRef.current) return;
    const rect = wrapRef.current.getBoundingClientRect();
    const fx = (e.clientX - rect.left) / rect.width,
      fy = (e.clientY - rect.top) / rect.height;
    if (fx < 0 || fx > 1 || fy < 0 || fy > 1) {
      setActive(null);
      return;
    }
    const px = Math.min(d.w - 1, Math.floor(fx * d.w)),
      py = Math.min(d.h - 1, Math.floor(fy * d.h));
    const L = d.labels[py * d.w + px];
    setActive(L ? NATION_ORDER[L - 1] : null);
  };
  return /*#__PURE__*/React.createElement("div", {
    ref: wrapRef,
    onMouseMove: onMove,
    onMouseLeave: () => setActive(null),
    style: {
      position: 'relative',
      width: '100%',
      maxWidth: 300,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: '8% 12%',
      borderRadius: '50%',
      background: 'var(--grad-royal)',
      filter: 'blur(70px)',
      opacity: 0.3,
      zIndex: 0
    }
  }), /*#__PURE__*/React.createElement("img", {
    src: window.__rv('ukmap', 'assets/uk-map.png'),
    alt: "\u041A\u0430\u0440\u0442\u0430 \u0412\u0435\u043B\u0438\u043A\u043E\u0431\u0440\u0438\u0442\u0430\u043D\u0438\u0438 \u2014 \u0447\u0435\u0442\u044B\u0440\u0435 \u0447\u0430\u0441\u0442\u0438",
    style: {
      position: 'relative',
      zIndex: 1,
      display: 'block',
      width: '100%',
      height: 'auto',
      filter: active ? 'drop-shadow(0 16px 40px rgba(0,0,0,0.55)) brightness(0.45) saturate(0.8)' : 'drop-shadow(0 16px 40px rgba(0,0,0,0.55))',
      transition: 'filter .25s ease'
    }
  }), /*#__PURE__*/React.createElement("canvas", {
    ref: overlayRef,
    style: {
      position: 'absolute',
      inset: 0,
      zIndex: 2,
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      filter: active ? `drop-shadow(0 0 16px ${UK_NATIONS[active].accent})` : 'none',
      transition: 'filter .2s ease'
    }
  }));
}
function UKMap() {
  const [active, setActive] = React.useState(null);
  return /*#__PURE__*/React.createElement("section", {
    id: "map",
    style: {
      paddingBlock: 'var(--section-gap)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "rv-container"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      maxWidth: 680,
      margin: '0 auto 12px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "rv-eyebrow"
  }, "\u0412\u0438\u0437\u0430 UK"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--t-h1)',
      marginTop: 14
    }
  }, "\u041E\u0434\u043D\u0430 \u0432\u0438\u0437\u0430\xA0\u2014 \u0447\u0435\u0442\u044B\u0440\u0435 \u0440\u0430\u0437\u043D\u044B\u0445 \u043C\u0438\u0440\u0430"), /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 16,
      fontSize: 'var(--t-lg)',
      color: 'var(--text-body)'
    }
  }, "\u041C\u0430\u043B\u043E \u043A\u0442\u043E \u0437\u043D\u0430\u0435\u0442: \u043E\u0434\u043D\u0430 \u0431\u0440\u0438\u0442\u0430\u043D\u0441\u043A\u0430\u044F \u0432\u0438\u0437\u0430 \u043E\u0442\u043A\u0440\u044B\u0432\u0430\u0435\u0442 \u0432\u0441\u0435 \u0447\u0435\u0442\u044B\u0440\u0435 \u0447\u0430\u0441\u0442\u0438 \u041A\u043E\u0440\u043E\u043B\u0435\u0432\u0441\u0442\u0432\u0430. \u0410\u043D\u0433\u043B\u0438\u044F, \u0428\u043E\u0442\u043B\u0430\u043D\u0434\u0438\u044F, \u0423\u044D\u043B\u044C\u0441 \u0438 \u0421\u0435\u0432\u0435\u0440\u043D\u0430\u044F \u0418\u0440\u043B\u0430\u043D\u0434\u0438\u044F\xA0\u2014 \u0431\u0435\u0437 \u043E\u0442\u0434\u0435\u043B\u044C\u043D\u044B\u0445 \u0440\u0430\u0437\u0440\u0435\u0448\u0435\u043D\u0438\u0439.")), /*#__PURE__*/React.createElement("div", {
    className: "rv-map-grid",
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1.05fr 1fr',
      gap: 28,
      alignItems: 'center',
      marginTop: 36
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(NationInfo, {
    id: "scotland",
    active: active,
    onHover: setActive,
    align: "right"
  }), /*#__PURE__*/React.createElement(NationInfo, {
    id: "ni",
    active: active,
    onHover: setActive,
    align: "right"
  })), /*#__PURE__*/React.createElement(InteractiveUKMap, {
    active: active,
    setActive: setActive
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(NationInfo, {
    id: "england",
    active: active,
    onHover: setActive,
    align: "left"
  }), /*#__PURE__*/React.createElement(NationInfo, {
    id: "wales",
    active: active,
    onHover: setActive,
    align: "left"
  })))));
}
Object.assign(window, {
  UKMap
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/UKMap.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/image-slot.js
try { (() => {
// @ds-adherence-ignore -- omelette starter scaffold (raw elements/hex/px by design)
/* BEGIN USAGE */
/**
 * <image-slot> - user-fillable image placeholder.
 *
 * Drop this into a deck, mockup, or page wherever you want the user to
 * supply an image. You control the slot's shape and size; the user fills it
 * by dragging an image file onto it (or clicking to browse). The dropped
 * image persists across reloads via a .image-slots.state.json sidecar -
 * same read-via-fetch / write-via-window.omelette pattern as
 * design_canvas.jsx, so the filled slot shows on share links, downloaded
 * zips, and PPTX export. Outside the omelette runtime the slot is read-only.
 *
 * The host bridge only allows sidecar writes at the project root, so the
 * HTML that uses this component is assumed to live at the project root too
 * (same constraint as design_canvas.jsx).
 *
 * Attributes:
 *   id           Persistence key. REQUIRED for the drop to survive reload -
 *                every slot on the page needs a distinct id.
 *   shape        'rect' | 'rounded' | 'circle' | 'pill'   (default 'rounded')
 *                'circle' applies 50% border-radius; on a non-square slot
 *                that's an ellipse - set equal width and height for a true
 *                circle.
 *   radius       Corner radius in px for 'rounded'.       (default 12)
 *   mask         Any CSS clip-path value. Overrides `shape` - use this for
 *                hexagons, blobs, arbitrary polygons.
 *   fit          object-fit: cover | contain | fill.       (default 'cover')
 *                With cover (the default) double-clicking the filled slot
 *                enters a reframe mode: the whole image spills past the mask
 *                (translucent outside, opaque inside), drag to reposition,
 *                corner-drag to scale. The crop persists alongside the image
 *                in the sidecar. contain/fill stay static.
 *   position     object-position for fit=contain|fill.     (default '50% 50%')
 *   placeholder  Empty-state caption.                      (default 'Drop an image')
 *   src          Optional initial/fallback image URL. A user drop overrides
 *                it; clearing the drop reveals src again.
 *
 * Size and layout come from ordinary CSS on the element - width/height
 * inline or from a parent grid - so it composes with any layout.
 *
 * Usage:
 *   <image-slot id="hero"   style="width:800px;height:450px" shape="rounded" radius="20"
 *               placeholder="Drop a hero image"></image-slot>
 *   <image-slot id="avatar" style="width:120px;height:120px" shape="circle"></image-slot>
 *   <image-slot id="kite"   style="width:300px;height:300px"
 *               mask="polygon(50% 0, 100% 50%, 50% 100%, 0 50%)"></image-slot>
 */
/* END USAGE */

(() => {
  const STATE_FILE = '.image-slots.state.json';
  // 2× a ~600px slot in a 1920-wide deck - retina-sharp without making the
  // sidecar enormous. A 1200px WebP at q=0.85 is ~150-300KB.
  const MAX_DIM = 1200;
  // Raster formats only. SVG is excluded (can carry script; createImageBitmap
  // on SVG blobs is inconsistent). GIF is excluded because the canvas
  // re-encode keeps only the first frame, so an animated GIF would silently
  // go still - better to reject than surprise.
  const ACCEPT = ['image/png', 'image/jpeg', 'image/webp', 'image/avif'];

  // ── Shared sidecar store ────────────────────────────────────────────────
  // One fetch + immediate write-on-change for every <image-slot> on the
  // page. Reads via fetch() so viewing works anywhere the HTML and sidecar
  // are served together; writes go through window.omelette.writeFile, which
  // the host allowlists to *.state.json basenames only.
  const subs = new Set();
  let slots = {};
  // ids explicitly cleared before the sidecar fetch resolved - otherwise
  // the merge below can't tell "never set" from "just deleted" and would
  // resurrect the sidecar's stale value.
  const tombstones = new Set();
  let loaded = false;
  let loadP = null;
  function load() {
    if (loadP) return loadP;
    loadP = fetch(STATE_FILE).then(r => r.ok ? r.json() : null).then(j => {
      // Merge: sidecar loses to any in-memory change that raced ahead of
      // the fetch (drop or clear) so neither is clobbered by hydration.
      if (j && typeof j === 'object') {
        const merged = Object.assign({}, j, slots);
        // A framing-only write that raced ahead of hydration must not
        // drop a user image that's only on disk - inherit u from the
        // sidecar for any in-memory entry that lacks one.
        for (const k in slots) {
          if (merged[k] && !merged[k].u && j[k]) {
            merged[k].u = typeof j[k] === 'string' ? j[k] : j[k].u;
          }
        }
        for (const id of tombstones) delete merged[id];
        slots = merged;
      }
      tombstones.clear();
    }).catch(() => {}).then(() => {
      loaded = true;
      subs.forEach(fn => fn());
    });
    return loadP;
  }

  // Serialize writes so two near-simultaneous drops on different slots
  // can't reorder at the backend and leave the sidecar with only the
  // first. A save requested mid-flight just marks dirty and re-fires on
  // completion with the then-current slots.
  let saving = false;
  let saveDirty = false;
  function save() {
    if (saving) {
      saveDirty = true;
      return;
    }
    const w = window.omelette && window.omelette.writeFile;
    if (!w) return;
    saving = true;
    Promise.resolve(w(STATE_FILE, JSON.stringify(slots))).catch(() => {}).then(() => {
      saving = false;
      if (saveDirty) {
        saveDirty = false;
        save();
      }
    });
  }
  const S_MAX = 5;
  const clampS = s => Math.max(1, Math.min(S_MAX, s));

  // Normalize a stored slot value. Pre-reframe sidecars stored a bare
  // data-URL string; newer ones store {u, s, x, y}. Either shape is valid.
  function getSlot(id) {
    const v = slots[id];
    if (!v) return null;
    return typeof v === 'string' ? {
      u: v,
      s: 1,
      x: 0,
      y: 0
    } : v;
  }
  function setSlot(id, val) {
    if (!id) return;
    if (val) {
      slots[id] = val;
      tombstones.delete(id);
    } else {
      delete slots[id];
      if (!loaded) tombstones.add(id);
    }
    subs.forEach(fn => fn());
    // A drop is rare + high-value - write immediately so nav-away can't lose
    // it. Gate on the initial read so we don't overwrite a sidecar we haven't
    // merged yet; the merge in load() keeps this change once the read lands.
    if (loaded) save();else load().then(save);
  }

  // ── Image downscale ─────────────────────────────────────────────────────
  // Encode through a canvas so the sidecar carries resized bytes, not the
  // raw upload. Longest side is capped at 2× the slot's rendered width
  // (retina) and at MAX_DIM. WebP keeps alpha and is ~10× smaller than PNG
  // for photos, so there's no need for per-image format picking.
  async function toDataUrl(file, targetW) {
    const bitmap = await createImageBitmap(file);
    try {
      const cap = Math.min(MAX_DIM, Math.max(1, Math.round(targetW * 2)) || MAX_DIM);
      const scale = Math.min(1, cap / Math.max(bitmap.width, bitmap.height));
      const w = Math.max(1, Math.round(bitmap.width * scale));
      const h = Math.max(1, Math.round(bitmap.height * scale));
      const canvas = document.createElement('canvas');
      canvas.width = w;
      canvas.height = h;
      canvas.getContext('2d').drawImage(bitmap, 0, 0, w, h);
      return canvas.toDataURL('image/webp', 0.85);
    } finally {
      bitmap.close && bitmap.close();
    }
  }

  // ── Custom element ──────────────────────────────────────────────────────
  const stylesheet = ':host{display:inline-block;position:relative;vertical-align:top;' + '  font:13px/1.3 system-ui,-apple-system,sans-serif;color:rgba(0,0,0,.55);width:240px;height:160px}' + '.frame{position:absolute;inset:0;overflow:hidden;background:rgba(0,0,0,.04)}' +
  // .frame img (clipped) and .spill (unclipped ghost + handles) share the
  // same left/top/width/height in frame-%, computed by _applyView(), so the
  // inside-mask crop and the outside-mask spill stay pixel-aligned.
  '.frame img{position:absolute;max-width:none;transform:translate(-50%,-50%);' + '  -webkit-user-drag:none;user-select:none;touch-action:none}' +
  // Reframe mode (double-click): the full image spills past the mask. The
  // spill layer is sized to the IMAGE bounds so its corners are where the
  // resize handles belong. The ghost <img> inside is translucent; the real
  // clipped <img> underneath shows the opaque in-mask crop.
  '.spill{position:absolute;transform:translate(-50%,-50%);display:none;z-index:1;' + '  cursor:grab;touch-action:none}' + ':host([data-panning]) .spill{cursor:grabbing}' + '.spill .ghost{position:absolute;inset:0;width:100%;height:100%;opacity:.35;' + '  pointer-events:none;-webkit-user-drag:none;user-select:none;' + '  box-shadow:0 0 0 1px rgba(0,0,0,.2),0 12px 32px rgba(0,0,0,.2)}' + '.spill .handle{position:absolute;width:12px;height:12px;border-radius:50%;' + '  background:#fff;box-shadow:0 0 0 1.5px #c96442,0 1px 3px rgba(0,0,0,.3);' + '  transform:translate(-50%,-50%)}' + '.spill .handle[data-c=nw]{left:0;top:0;cursor:nwse-resize}' + '.spill .handle[data-c=ne]{left:100%;top:0;cursor:nesw-resize}' + '.spill .handle[data-c=sw]{left:0;top:100%;cursor:nesw-resize}' + '.spill .handle[data-c=se]{left:100%;top:100%;cursor:nwse-resize}' + ':host([data-reframe]){z-index:10}' + ':host([data-reframe]) .spill{display:block}' + ':host([data-reframe]) .frame{box-shadow:0 0 0 2px #c96442}' + '.empty{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;' + '  justify-content:center;gap:6px;text-align:center;padding:12px;box-sizing:border-box;' + '  cursor:pointer;user-select:none}' + '.empty svg{opacity:.45}' + '.empty .cap{max-width:90%;font-weight:500;letter-spacing:.01em}' + '.empty .sub{font-size:11px}' + '.empty .sub u{text-underline-offset:2px;text-decoration-color:rgba(0,0,0,.25)}' + '.empty:hover .sub u{color:rgba(0,0,0,.75);text-decoration-color:currentColor}' + ':host([data-over]) .frame{outline:2px solid #c96442;outline-offset:-2px;' + '  background:rgba(201,100,66,.10)}' + '.ring{position:absolute;inset:0;pointer-events:none;border:1.5px dashed rgba(0,0,0,.25);' + '  transition:border-color .12s}' + ':host([data-over]) .ring{border-color:#c96442}' + ':host([data-filled]) .ring{display:none}' +
  // Controls sit BELOW the mask (top:100%), absolutely positioned so the
  // author-declared slot height is unaffected. The gap is padding, not a
  // top offset, so the hover target stays contiguous with the frame.
  '.ctl{position:absolute;top:100%;left:50%;transform:translateX(-50%);padding-top:8px;' + '  display:flex;gap:6px;opacity:0;pointer-events:none;transition:opacity .12s;z-index:2;' + '  white-space:nowrap}' + ':host([data-filled][data-editable]:hover) .ctl,:host([data-reframe]) .ctl' + '  {opacity:1;pointer-events:auto}' + '.ctl button{appearance:none;border:0;border-radius:6px;padding:5px 10px;cursor:pointer;' + '  background:rgba(0,0,0,.65);color:#fff;font:11px/1 system-ui,-apple-system,sans-serif;' + '  backdrop-filter:blur(6px)}' + '.ctl button:hover{background:rgba(0,0,0,.8)}' + '.err{position:absolute;left:8px;bottom:8px;right:8px;color:#b3261e;font-size:11px;' + '  background:rgba(255,255,255,.85);padding:4px 6px;border-radius:5px;pointer-events:none}';
  const icon = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' + 'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>' + '<path d="m21 15-5-5L5 21"/></svg>';
  class ImageSlot extends HTMLElement {
    static get observedAttributes() {
      return ['shape', 'radius', 'mask', 'fit', 'position', 'placeholder', 'src', 'id'];
    }
    constructor() {
      super();
      const root = this.attachShadow({
        mode: 'open'
      });
      // .spill and .ctl sit OUTSIDE .frame so overflow:hidden + border-radius
      // on the frame (circle, pill, rounded) can't clip them.
      root.innerHTML = '<style>' + stylesheet + '</style>' + '<div class="frame" part="frame">' + '  <img part="image" alt="" draggable="false" style="display:none">' + '  <div class="empty" part="empty">' + icon + '    <div class="cap"></div>' + '    <div class="sub">or <u>browse files</u></div></div>' + '  <div class="ring" part="ring"></div>' + '</div>' + '<div class="spill">' + '  <img class="ghost" alt="" draggable="false">' + '  <div class="handle" data-c="nw"></div><div class="handle" data-c="ne"></div>' + '  <div class="handle" data-c="sw"></div><div class="handle" data-c="se"></div>' + '</div>' + '<div class="ctl"><button data-act="replace" title="Replace image">Replace</button>' + '  <button data-act="clear" title="Remove image">Remove</button></div>' + '<input type="file" accept="' + ACCEPT.join(',') + '" hidden>';
      this._frame = root.querySelector('.frame');
      this._ring = root.querySelector('.ring');
      this._img = root.querySelector('.frame img');
      this._empty = root.querySelector('.empty');
      this._cap = root.querySelector('.cap');
      this._sub = root.querySelector('.sub');
      this._spill = root.querySelector('.spill');
      this._ghost = root.querySelector('.ghost');
      this._err = null;
      this._input = root.querySelector('input');
      this._depth = 0;
      this._gen = 0;
      this._view = {
        s: 1,
        x: 0,
        y: 0
      };
      this._subFn = () => this._render();
      // Shadow-DOM listeners live with the shadow DOM - bound once here so
      // disconnect/reconnect (e.g. React remount) doesn't stack handlers.
      this._empty.addEventListener('click', () => this._input.click());
      root.addEventListener('click', e => {
        const act = e.target && e.target.getAttribute && e.target.getAttribute('data-act');
        if (act === 'replace') {
          this._exitReframe(true);
          this._input.click();
        }
        if (act === 'clear') {
          this._exitReframe(false);
          this._gen++;
          this._local = null;
          if (this.id) setSlot(this.id, null);else this._render();
        }
      });
      this._input.addEventListener('change', () => {
        const f = this._input.files && this._input.files[0];
        if (f) this._ingest(f);
        this._input.value = '';
      });
      // naturalWidth/Height aren't known until load - re-apply so the cover
      // baseline is computed from real dimensions, not the 100%×100% fallback.
      this._img.addEventListener('load', () => this._applyView());
      // Gated on editable + fit=cover so share links and contain/fill slots
      // stay static.
      this.addEventListener('dblclick', e => {
        if (!this.hasAttribute('data-editable') || !this._reframes()) return;
        e.preventDefault();
        if (this.hasAttribute('data-reframe')) this._exitReframe(true);else this._enterReframe();
      });
      // Pan + resize both originate on the spill layer. A handle pointerdown
      // drives an aspect-locked resize anchored at the opposite corner; any
      // other pointerdown on the spill pans. Offsets are frame-% so a
      // reframed slot survives responsive resize / PPTX export.
      this._spill.addEventListener('pointerdown', e => {
        if (e.button !== 0 || !this.hasAttribute('data-reframe')) return;
        e.preventDefault();
        e.stopPropagation();
        this._spill.setPointerCapture(e.pointerId);
        const rect = this.getBoundingClientRect();
        const fw = rect.width || 1,
          fh = rect.height || 1;
        const corner = e.target.getAttribute && e.target.getAttribute('data-c');
        let move;
        if (corner) {
          // Resize about the OPPOSITE corner. Viewport-px throughout (rect
          // fw/fh, not clientWidth) so the math survives a transform:scale()
          // ancestor - deck_stage renders slides scaled-to-fit.
          const iw = this._img.naturalWidth || 1,
            ih = this._img.naturalHeight || 1;
          const base = Math.max(fw / iw, fh / ih);
          const sx = corner.includes('e') ? 1 : -1;
          const sy = corner.includes('s') ? 1 : -1;
          const s0 = this._view.s;
          const w0 = iw * base * s0,
            h0 = ih * base * s0;
          const cx0 = (50 + this._view.x) / 100 * fw;
          const cy0 = (50 + this._view.y) / 100 * fh;
          const ox = cx0 - sx * w0 / 2,
            oy = cy0 - sy * h0 / 2;
          const diag0 = Math.hypot(w0, h0);
          const ux = sx * w0 / diag0,
            uy = sy * h0 / diag0;
          move = ev => {
            const proj = (ev.clientX - rect.left - ox) * ux + (ev.clientY - rect.top - oy) * uy;
            const s = clampS(s0 * proj / diag0);
            const d = diag0 * s / s0;
            this._view.s = s;
            this._view.x = (ox + ux * d / 2) / fw * 100 - 50;
            this._view.y = (oy + uy * d / 2) / fh * 100 - 50;
            this._clampView();
            this._applyView();
          };
        } else {
          this.setAttribute('data-panning', '');
          const start = {
            px: e.clientX,
            py: e.clientY,
            x: this._view.x,
            y: this._view.y
          };
          move = ev => {
            this._view.x = start.x + (ev.clientX - start.px) / fw * 100;
            this._view.y = start.y + (ev.clientY - start.py) / fh * 100;
            this._clampView();
            this._applyView();
          };
        }
        const up = () => {
          try {
            this._spill.releasePointerCapture(e.pointerId);
          } catch {}
          this._spill.removeEventListener('pointermove', move);
          this._spill.removeEventListener('pointerup', up);
          this._spill.removeEventListener('pointercancel', up);
          this.removeAttribute('data-panning');
          this._dragUp = null;
        };
        // Stashed so _exitReframe (Escape / outside-click mid-drag) can
        // tear the capture + listeners down synchronously.
        this._dragUp = up;
        this._spill.addEventListener('pointermove', move);
        this._spill.addEventListener('pointerup', up);
        this._spill.addEventListener('pointercancel', up);
      });
      // Wheel zoom stays available inside reframe mode as a trackpad nicety -
      // zooms toward the cursor (offset' = cursor·(1-k) + offset·k).
      this.addEventListener('wheel', e => {
        if (!this.hasAttribute('data-reframe')) return;
        e.preventDefault();
        const r = this.getBoundingClientRect();
        const cx = (e.clientX - r.left) / r.width * 100 - 50;
        const cy = (e.clientY - r.top) / r.height * 100 - 50;
        const prev = this._view.s;
        const next = clampS(prev * Math.pow(1.0015, -e.deltaY));
        if (next === prev) return;
        const k = next / prev;
        this._view.s = next;
        this._view.x = cx * (1 - k) + this._view.x * k;
        this._view.y = cy * (1 - k) + this._view.y * k;
        this._clampView();
        this._applyView();
      }, {
        passive: false
      });
    }
    connectedCallback() {
      // Warn once per page - an id-less slot works for the session but
      // cannot persist, and two id-less slots would share nothing.
      if (!this.id && !ImageSlot._warned) {
        ImageSlot._warned = true;
        console.warn('<image-slot> without an id will not persist its dropped image.');
      }
      this.addEventListener('dragenter', this);
      this.addEventListener('dragover', this);
      this.addEventListener('dragleave', this);
      this.addEventListener('drop', this);
      subs.add(this._subFn);
      // width%/height% in _applyView encode the frame aspect at call time -
      // a host resize (responsive grid, pane divider) would stretch the
      // image until the next _render. Re-render on size change: _render()
      // re-seeds _view from stored before clamp/apply, so a shrink→grow
      // cycle round-trips instead of ratcheting x/y toward the narrower
      // frame's clamp range.
      this._ro = new ResizeObserver(() => this._render());
      this._ro.observe(this);
      load();
      this._render();
    }
    disconnectedCallback() {
      subs.delete(this._subFn);
      this.removeEventListener('dragenter', this);
      this.removeEventListener('dragover', this);
      this.removeEventListener('dragleave', this);
      this.removeEventListener('drop', this);
      if (this._ro) {
        this._ro.disconnect();
        this._ro = null;
      }
      this._exitReframe(false);
    }
    _enterReframe() {
      if (this.hasAttribute('data-reframe')) return;
      this.setAttribute('data-reframe', '');
      this._applyView();
      // Close on click outside (the spill handler stopPropagation()s so
      // in-image drags don't reach this) and on Escape. Listeners are held
      // on the instance so _exitReframe / disconnectedCallback can detach
      // exactly what was attached.
      this._outside = e => {
        if (e.composedPath && e.composedPath().includes(this)) return;
        this._exitReframe(true);
      };
      this._esc = e => {
        if (e.key === 'Escape') this._exitReframe(true);
      };
      document.addEventListener('pointerdown', this._outside, true);
      document.addEventListener('keydown', this._esc, true);
    }
    _exitReframe(commit) {
      if (!this.hasAttribute('data-reframe')) return;
      if (this._dragUp) this._dragUp();
      this.removeAttribute('data-reframe');
      this.removeAttribute('data-panning');
      if (this._outside) document.removeEventListener('pointerdown', this._outside, true);
      if (this._esc) document.removeEventListener('keydown', this._esc, true);
      this._outside = this._esc = null;
      if (commit) this._commitView();
    }
    attributeChangedCallback() {
      if (this.shadowRoot) this._render();
    }

    // handleEvent - one listener object for all four drag events keeps the
    // add/remove symmetric and the depth counter correct.
    handleEvent(e) {
      if (e.type === 'dragenter' || e.type === 'dragover') {
        // Without preventDefault the browser never fires 'drop'.
        e.preventDefault();
        e.stopPropagation();
        if (e.dataTransfer) e.dataTransfer.dropEffect = 'copy';
        if (e.type === 'dragenter') this._depth++;
        this.setAttribute('data-over', '');
      } else if (e.type === 'dragleave') {
        // dragenter/leave fire for every descendant crossing - count depth
        // so hovering the icon inside the empty state doesn't flicker.
        if (--this._depth <= 0) {
          this._depth = 0;
          this.removeAttribute('data-over');
        }
      } else if (e.type === 'drop') {
        e.preventDefault();
        e.stopPropagation();
        this._depth = 0;
        this.removeAttribute('data-over');
        const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
        if (f) this._ingest(f);
      }
    }
    async _ingest(file) {
      this._setError(null);
      if (!file || ACCEPT.indexOf(file.type) < 0) {
        this._setError('Drop a PNG, JPEG, WebP, or AVIF image.');
        return;
      }
      // toDataUrl can take hundreds of ms on a large photo. A Clear or a
      // newer drop during that window would be clobbered when this await
      // resumes - bump + capture a generation so stale encodes bail.
      const gen = ++this._gen;
      try {
        const w = this.clientWidth || this.offsetWidth || MAX_DIM;
        const url = await toDataUrl(file, w);
        if (gen !== this._gen) return;
        // Only exit reframe once the new image is in hand - a rejected type
        // or decode failure leaves the in-progress crop untouched.
        this._exitReframe(false);
        const val = {
          u: url,
          s: 1,
          x: 0,
          y: 0
        };
        setSlot(this.id || '', val);
        // Keep a session-local copy for id-less slots so the drop still
        // shows, even though it cannot persist.
        if (!this.id) {
          this._local = val;
          this._render();
        }
      } catch (err) {
        if (gen !== this._gen) return;
        this._setError('Could not read that image.');
        console.warn('<image-slot> ingest failed:', err);
      }
    }
    _setError(msg) {
      if (this._err) {
        this._err.remove();
        this._err = null;
      }
      if (!msg) return;
      const d = document.createElement('div');
      d.className = 'err';
      d.textContent = msg;
      this.shadowRoot.appendChild(d);
      this._err = d;
      setTimeout(() => {
        if (this._err === d) {
          d.remove();
          this._err = null;
        }
      }, 3000);
    }

    // Reframing (pan/resize) is only meaningful for fit=cover - contain/fill
    // keep the old object-fit path and double-click is a no-op.
    _reframes() {
      return this.hasAttribute('data-filled') && (this.getAttribute('fit') || 'cover') === 'cover';
    }

    // Cover-baseline geometry, shared by clamp/apply/resize. Null until the
    // img has loaded (naturalWidth is 0 before that) or when the slot has no
    // layout box - ResizeObserver fires with a 0×0 rect under display:none,
    // and clamping against a degenerate 1×1 frame would silently pull the
    // stored pan toward zero.
    _geom() {
      const iw = this._img.naturalWidth,
        ih = this._img.naturalHeight;
      const fw = this.clientWidth,
        fh = this.clientHeight;
      if (!iw || !ih || !fw || !fh) return null;
      return {
        iw,
        ih,
        fw,
        fh,
        base: Math.max(fw / iw, fh / ih)
      };
    }
    _clampView() {
      // Pan range on each axis is half the overflow past the frame edge.
      const g = this._geom();
      if (!g) return;
      const mx = Math.max(0, (g.iw * g.base * this._view.s / g.fw - 1) * 50);
      const my = Math.max(0, (g.ih * g.base * this._view.s / g.fh - 1) * 50);
      this._view.x = Math.max(-mx, Math.min(mx, this._view.x));
      this._view.y = Math.max(-my, Math.min(my, this._view.y));
    }
    _applyView() {
      const g = this._geom();
      const fit = this.getAttribute('fit') || 'cover';
      if (fit !== 'cover' || !g) {
        // Non-cover, or dimensions not known yet (before img load).
        this._img.style.width = '100%';
        this._img.style.height = '100%';
        this._img.style.left = '50%';
        this._img.style.top = '50%';
        this._img.style.objectFit = fit;
        this._img.style.objectPosition = this.getAttribute('position') || '50% 50%';
        return;
      }
      // Cover baseline: img fills the frame on its tighter axis at s=1, so
      // pan works immediately on the overflowing axis without zooming first.
      // Width/height and left/top are all frame-% - depends only on the
      // frame aspect ratio, so a responsive resize keeps the same crop. The
      // spill layer mirrors the same box so its corners = image corners.
      const k = g.base * this._view.s;
      const w = g.iw * k / g.fw * 100 + '%';
      const h = g.ih * k / g.fh * 100 + '%';
      const l = 50 + this._view.x + '%';
      const t = 50 + this._view.y + '%';
      this._img.style.width = w;
      this._img.style.height = h;
      this._img.style.left = l;
      this._img.style.top = t;
      this._img.style.objectFit = '';
      this._spill.style.width = w;
      this._spill.style.height = h;
      this._spill.style.left = l;
      this._spill.style.top = t;
    }
    _commitView() {
      const v = {
        s: this._view.s,
        x: this._view.x,
        y: this._view.y
      };
      if (this._userUrl) v.u = this._userUrl;
      // Framing-only (no u) persists too so an author-src slot remembers its
      // crop; clearing the sidecar still falls through to src=.
      if (this.id) setSlot(this.id, v);else {
        this._local = v;
      }
    }
    _render() {
      // Shape / mask. Presets use border-radius so the dashed ring can
      // follow the rounded outline; clip-path is only applied for an
      // explicit `mask` (the ring is hidden there since a rectangle
      // dashed border chopped by an arbitrary polygon looks broken).
      const mask = this.getAttribute('mask');
      const shape = (this.getAttribute('shape') || 'rounded').toLowerCase();
      let radius = '';
      if (shape === 'circle') radius = '50%';else if (shape === 'pill') radius = '9999px';else if (shape === 'rounded') {
        const n = parseFloat(this.getAttribute('radius'));
        radius = (Number.isFinite(n) ? n : 12) + 'px';
      }
      this._frame.style.borderRadius = mask ? '' : radius;
      this._frame.style.clipPath = mask || '';
      this._ring.style.borderRadius = mask ? '' : radius;
      this._ring.style.display = mask ? 'none' : '';

      // Controls and reframe entry gate on this so share links stay read-only.
      const editable = !!(window.omelette && window.omelette.writeFile);
      this.toggleAttribute('data-editable', editable);
      this._sub.style.display = editable ? '' : 'none';

      // Content. The sidecar is also writable by the agent's write_file
      // tool, so its value isn't guaranteed canvas-originated - only accept
      // data:image/ URLs from it. The `src` attribute is author-controlled
      // (Claude wrote it into the HTML) so it passes through unchanged.
      let stored = this.id ? getSlot(this.id) : this._local;
      if (stored && stored.u && !/^data:image\//i.test(stored.u)) stored = null;
      const srcAttr = this.getAttribute('src') || '';
      this._userUrl = stored && stored.u || null;
      const url = this._userUrl || srcAttr;
      // Don't clobber an in-flight reframe with a store-triggered re-render.
      if (!this.hasAttribute('data-reframe')) {
        this._view = {
          s: stored && Number.isFinite(stored.s) ? clampS(stored.s) : 1,
          x: stored && Number.isFinite(stored.x) ? stored.x : 0,
          y: stored && Number.isFinite(stored.y) ? stored.y : 0
        };
      }
      this._cap.textContent = this.getAttribute('placeholder') || 'Drop an image';
      // Toggle via style.display - the [hidden] attribute alone loses to
      // the display:flex / display:block rules in the stylesheet above.
      if (url) {
        if (this._img.getAttribute('src') !== url) {
          this._img.src = url;
          this._ghost.src = url;
        }
        this._img.style.display = 'block';
        this._empty.style.display = 'none';
        this.setAttribute('data-filled', '');
        this._clampView();
        this._applyView();
      } else {
        this._img.style.display = 'none';
        this._img.removeAttribute('src');
        this._ghost.removeAttribute('src');
        this._empty.style.display = 'flex';
        this.removeAttribute('data-filled');
      }
    }
  }
  if (!customElements.get('image-slot')) {
    customElements.define('image-slot', ImageSlot);
  }
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/image-slot.js", error: String((e && e.message) || e) }); }

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.GlassCard = __ds_scope.GlassCard;

__ds_ns.Stat = __ds_scope.Stat;

__ds_ns.Accordion = __ds_scope.Accordion;

__ds_ns.AccordionItem = __ds_scope.AccordionItem;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Switch = __ds_scope.Switch;

})();
