# -*- coding: utf-8 -*-
"""
Genera la web de La Florería de Eva.

Cada página vive en src/<nombre>.html con una cabecera de datos (clave: valor)
separada del contenido por una línea con '---'. Este script añade <head>,
cabecera, menú, hero, pie de página y adornos, y escribe el resultado en la raíz.

    python tools/build.py            # genera todas las páginas
    python tools/build.py --heroes   # además regenera las imágenes de cabecera

Las imágenes de cabecera se recortan desde las fotos de Instagram solo si no
existen. Si sustituyes assets/img/hero/<pagina>.webp por una imagen nueva,
el script la respeta.
"""
import html
import math
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
HERO = ROOT / "assets" / "img" / "hero"
FUENTES = ROOT / "_fuentes_instagram"
VERSION = "1.1.4"

WA_NUMBER = "34607803222"
PHONE = "607 80 32 22"
EMAIL = "lafloreriadeva@gmail.com"
IG = "https://www.instagram.com/lafloreriadeva/"
FB = "https://www.facebook.com/profile.php?id=100088728496492"
TT = "https://www.tiktok.com/@lafloreriadeva"
MAPS = "https://www.google.com/maps/search/?api=1&query=La+Floreria+de+Eva+Mercado+de+los+Pinos+Manises"

# --------------------------------------------------------------------------
# Navegación
# --------------------------------------------------------------------------
CREACIONES = [
    ("jardines-verticales.html", "Jardines verticales", "Musgo preservado que no se riega", "020"),
    ("cupulas-y-rosas-eternas.html", "Cúpulas y rosas eternas", "Flores que duran años", "131"),
    ("flor-seca-y-eucalipto.html", "Flor seca y eucalipto", "Centros, jarrones y bouquets", "032"),
    ("munecas-artesanas.html", "Muñecas artesanas", "Macramé y lana, hechas a mano", "130"),
    ("letras-y-personalizados.html", "Letras y personalizados", "Nombres, iniciales y carteles", "113"),
]
CELEBRACIONES = [
    ("fallas.html", "Colección fallera", "Brocado, musgo y Senyera", "wa2"),
    ("bodas.html", "Bodas y pedidas", "Ramos de novia que no se marchitan", "039"),
    ("comuniones-y-fiestas.html", "Comuniones y fiestas", "Coronas, packs y graduaciones", "002"),
    ("fechas-especiales.html", "Fechas especiales", "San Valentín, Madre, Navidad…", "157"),
]


def img_paths(ref):
    """'019' -> foto de Instagram; 'wa8' -> captura del catálogo de WhatsApp."""
    ref = ref.strip()
    if ref.startswith("wa"):
        p = f"assets/img/whatsapp/{ref}.webp"
        return p, p
    return f"assets/img/ig/{ref}.webp", f"assets/img/thumb/{ref}.webp"


_SIZES = {}


def img_size(rel):
    if rel not in _SIZES:
        from PIL import Image
        with Image.open(ROOT / rel) as im:
            _SIZES[rel] = im.size
    return _SIZES[rel]


def wa_link(msg=""):
    base = f"https://wa.me/{WA_NUMBER}"
    return base + ("?text=" + urllib.parse.quote(msg) if msg else "")


WA_ICON = ('<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.9 9.9 0 0 0 12.04 2Zm5.8 14.13c-.25.69-1.44 1.32-2 1.4-.51.08-1.15.11-1.86-.12-.43-.13-.98-.32-1.68-.62-2.96-1.28-4.89-4.26-5.04-4.46-.15-.2-1.2-1.6-1.2-3.05 0-1.45.76-2.16 1.03-2.46.27-.3.59-.37.79-.37h.57c.18 0 .43-.07.67.51.25.59.84 2.04.91 2.19.07.15.12.32.02.52-.1.2-.15.32-.3.49-.15.17-.31.39-.45.52-.15.15-.3.31-.13.61.17.3.77 1.27 1.65 2.06 1.14 1.01 2.1 1.33 2.4 1.48.3.15.47.12.65-.07.17-.2.74-.86.94-1.16.2-.3.39-.25.66-.15.27.1 1.72.81 2.01.96.3.15.49.22.57.34.07.12.07.71-.18 1.4Z"/></svg>')
ARROW = '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
    "ig": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor"/></svg>',
    "fb": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1Z"/></svg>',
    "tt": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.6 3c.3 2.3 1.6 3.7 3.9 3.9v2.6c-1.3.1-2.5-.3-3.9-1.1v5.1c0 6.5-7.1 8.5-9.9 3.8-1.8-3-.7-8.3 5.2-8.5v2.7c-.4.1-.9.2-1.3.3-1.3.4-2 1.2-1.8 2.6.4 2.7 5.3 3.5 4.9-1.8V3h2.9Z"/></svg>',
    "phone": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>',
    "pin": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
    "mail": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 6.5 8.5 7 8.5-7" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
    "box": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5v-9Zm0 0 9 4.5 9-4.5M12 12v9"/></svg>',
    "clock": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "hand": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" d="M8 13V5.5a1.5 1.5 0 0 1 3 0V11m0-6.5a1.5 1.5 0 0 1 3 0V11m0-5a1.5 1.5 0 0 1 3 0v6.5m0-3a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1.5a6 6 0 0 1-4.6-2.2L4.6 15.4a1.5 1.5 0 0 1 2.3-1.9L8 15"/></svg>',
    "leaf": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" d="M5 19C5 10 10 5 20 4c0 10-5 15-14 15Zm0 0 8-8"/></svg>',
    "star": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z"/></svg>',
}

# --------------------------------------------------------------------------
# Flores de tinta (inspiradas en el logotipo): SVG dibujado con trazo
# --------------------------------------------------------------------------
def _spiral(cx, cy, r0, r1, turns, steps=150):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts)


def _s(d, extra=""):
    return f'<path class="s" pathLength="1" d="{d}" {extra}/>'


def _c(cx, cy, r, fill=None):
    out = ""
    if fill:
        out += f'<circle class="f {fill}" cx="{cx}" cy="{cy}" r="{r}"/>'
    out += f'<circle class="s" pathLength="1" cx="{cx}" cy="{cy}" r="{r}"/>'
    return out


def _leaf(x, y, dx, dy, side=1):
    # hoja con nervio central
    x2, y2 = x + dx * side, y - dy
    d = f"M{x},{y} C{x + dx*0.2*side},{y - dy*0.9} {x2 - dx*0.25*side},{y2 - dy*0.1} {x2},{y2} C{x2 - dx*0.1*side},{y2 + dy*0.6} {x + dx*0.55*side},{y + dy*0.05} {x},{y} Z"
    return (f'<path class="f f-leaf" d="{d}"/>' + _s(d) +
            _s(f"M{x},{y} Q{x + dx*0.45*side},{y - dy*0.45} {x2 - dx*0.12*side},{y2 + dy*0.12}", 'class="s thin"'))


def flower(kind, x=0, y=0, scale=1.0):
    g = f'<g transform="translate({x} {y}) scale({scale})">'
    if kind == "rose":
        g += _c(60, 60, 46, "f-rose")
        g += _s(_spiral(60, 60, 2, 44, 4.2))
        g += _s("M60,106 C57,140 63,175 60,220")
        g += _leaf(60, 168, 36, 30, -1) + _leaf(60, 196, 34, 26, 1)
    elif kind == "bloom":
        g += _c(60, 52, 36, "f-blush")
        for i in range(18):
            a = i / 18 * 2 * math.pi
            g += _s(f"M{60 + 8*math.cos(a):.1f},{52 + 8*math.sin(a):.1f} L{60 + 32*math.cos(a):.1f},{52 + 32*math.sin(a):.1f}", 'class="s thin"')
        g += _c(60, 52, 6)
        g += _s("M60,88 C64,130 56,170 60,220")
        g += _leaf(60, 178, 30, 26, 1)
    elif kind == "tulip":
        cup = "M24,50 C22,92 40,104 60,104 C80,104 98,92 96,50 C84,62 72,60 60,40 C48,60 36,62 24,50 Z"
        g += f'<path class="f f-coral" d="{cup}"/>' + _s(cup)
        for i, xx in enumerate(range(34, 92, 8)):
            top = 56 if abs(xx - 60) > 14 else 50
            g += _s(f"M{xx},{top} Q{xx + (60 - xx)*0.12:.1f},{80} {60 + (xx - 60)*0.55:.1f},{100}", 'class="s thin"')
        g += _s("M60,104 C58,140 62,180 60,220")
        g += _leaf(60, 160, 34, 34, -1)
    elif kind == "pod":
        body = "M30,54 C28,96 46,112 60,112 C74,112 92,96 90,54 Z"
        g += f'<path class="f f-orange" d="{body}"/>' + _s(body)
        g += _c(60, 50, 30, "f-orange")
        for i in range(12):
            a = i / 12 * 2 * math.pi
            g += _c(round(60 + 18*math.cos(a), 1), round(50 + 12*math.sin(a), 1), 3.2)
        for xx in range(40, 84, 7):
            g += _s(f"M{xx},{62} Q{60 + (xx-60)*0.7:.1f},{92} {60 + (xx-60)*0.35:.1f},{110}", 'class="s thin"')
        g += _s("M60,112 C62,150 58,185 60,220")
    elif kind == "berries":
        g += _s("M60,220 C58,170 64,120 60,40")
        for i, (bx, by) in enumerate([(60, 34), (46, 52), (74, 58), (44, 76), (76, 84), (46, 102), (74, 110), (50, 128)]):
            g += _c(bx, by, 7.5, "f-blush")
            if i:
                g += _s(f"M60,{by + 4} L{bx},{by}", 'class="s thin"')
    elif kind == "buds":
        g += _c(36, 40, 15, "f-rose") + _s(_spiral(36, 40, 1, 13, 2.2, 60), 'class="s thin"')
        g += _c(82, 62, 13, "f-rose") + _s(_spiral(82, 62, 1, 11, 2, 60), 'class="s thin"')
        g += _s("M36,55 C40,110 52,160 56,220") + _s("M82,75 C78,120 66,170 60,220")
    elif kind == "yellow":
        g += _c(60, 56, 30, "f-sun")
        for r in (22, 14, 6):
            g += f'<path class="s thin" pathLength="1" d="M{60 - r},{56} a{r},{r*0.9} 0 1 0 {2*r},0 a{r},{r*0.9} 0 1 0 {-2*r},0"/>'
        g += _s("M60,86 C56,130 64,175 60,220")
        g += _leaf(60, 150, 30, 34, 1)
    elif kind == "grass":
        for xx, h in [(20, 120), (40, 160), (60, 110), (80, 150), (100, 130)]:
            g += _s(f"M{xx},220 C{xx - 4},{220 - h*0.5} {xx + 6},{220 - h*0.8} {xx + 2},{220 - h}", 'class="s thin"')
    g += "</g>"
    return g


def ink(kind, cls=""):
    return (f'<svg class="ink {cls}" viewBox="0 0 120 225" aria-hidden="true" focusable="false">'
            f'{flower(kind)}</svg>')


def bouquet(cls=""):
    parts = [
        ("grass", 40, 70, 0.95), ("berries", 0, 50, 0.85), ("buds", 72, 6, 0.9),
        ("rose", 105, 30, 1.05), ("pod", 205, 22, 0.9), ("bloom", 245, 0, 0.85),
        ("tulip", 50, 92, 0.75), ("yellow", 280, 70, 0.8), ("berries", 330, 40, 0.8),
        ("grass", 300, 90, 0.8),
    ]
    inner = "".join(flower(k, x, y, s) for k, x, y, s in parts)
    return f'<svg class="ink ink--bouquet {cls}" viewBox="0 0 430 270" aria-hidden="true" focusable="false">{inner}</svg>'


def sprigs(cls=""):
    parts = [("berries", 0, 20, .6), ("rose", 60, 0, .7), ("tulip", 140, 30, .6), ("bloom", 205, 8, .62), ("buds", 270, 30, .6)]
    inner = "".join(flower(k, x, y, s) for k, x, y, s in parts)
    return f'<svg class="ink ink--row {cls}" viewBox="0 0 345 170" aria-hidden="true" focusable="false">{inner}</svg>'


# --------------------------------------------------------------------------
# Atajos dentro del contenido
# --------------------------------------------------------------------------
def sc_gallery(args, cls="gallery"):
    items = []
    for raw in args:
        raw = raw.strip()
        if not raw:
            continue
        m = re.match(r"^(\S+)\s+(.*?)(?:\s*\{(.+?)\})?$", raw)
        ref, cap, cat = m.group(1), m.group(2), m.group(3) or ""
        full, thumb = img_paths(ref)
        w, h = img_size(thumb)
        cat_attr = f' data-cat="{cat}"' if cat else ""
        items.append(
            f'<a class="g-item reveal" href="{full}" data-lb data-cap="{html.escape(cap)}"{cat_attr}>'
            f'<img src="{thumb}" alt="{html.escape(cap)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            f'<span class="g-cap">{cap}</span></a>')
    return f'<div class="{cls}" data-gallery>' + "".join(items) + "</div>"


def sc_wa(args):
    msg = args[0].strip() if args else ""
    label = args[1].strip() if len(args) > 1 else "Pedir por WhatsApp"
    style = args[2].strip() if len(args) > 2 else "btn--wa"
    return f'<a class="btn {style}" href="{wa_link(msg)}" target="_blank" rel="noopener">{WA_ICON}<span>{label}</span></a>'


def shortcodes(body):
    def rep(m):
        parts = m.group(1).split("|")
        name = parts[0].strip()
        args = parts[1:]
        if name == "gal":
            return sc_gallery(args)
        if name == "gal-masonry":
            return sc_gallery(args, "gallery gallery--masonry")
        if name == "wa":
            return sc_wa(args)
        if name == "walink":
            return wa_link(args[0].strip() if args else "")
        if name == "ink":
            return ink(args[0].strip(), args[1].strip() if len(args) > 1 else "")
        if name == "bouquet":
            return bouquet(args[0].strip() if args else "")
        if name == "sprigs":
            return sprigs(args[0].strip() if args else "")
        if name == "icon":
            return ICONS[args[0].strip()]
        if name == "arrow":
            return ARROW
        if name == "waicon":
            return WA_ICON
        return m.group(0)
    return re.sub(r"\[\[(.+?)\]\]", rep, body, flags=re.S)


# --------------------------------------------------------------------------
# Imágenes de cabecera
# --------------------------------------------------------------------------
def source_image(ref):
    from PIL import Image, ImageOps
    if ref.startswith("wa"):
        f = ROOT / "assets" / "img" / "whatsapp" / f"{ref}.webp"
    else:
        f = next(FUENTES.glob(f"{ref}-*.jpg"))
    return ImageOps.exif_transpose(Image.open(f)).convert("RGB")


def crop(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        x = int((w - nw) * fx)
        return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio)
    y = int((h - nh) * fy)
    return im.crop((0, y, w, y + nh))


def make_hero(name, ref, fx, fy, force):
    HERO.mkdir(parents=True, exist_ok=True)
    wide, tall = HERO / f"{name}.webp", HERO / f"{name}-m.webp"
    if wide.exists() and tall.exists() and not force:
        return
    try:
        im = source_image(ref)
    except StopIteration:
        print("  ! no encuentro la foto", ref)
        return
    a = crop(im, 16 / 10, fx, fy)
    a.thumbnail((1600, 1000))
    a.save(wide, quality=80, method=6)
    b = crop(im, 4 / 5.4, fx, fy)
    b.thumbnail((1000, 1350))
    b.save(tall, quality=80, method=6)
    print("  hero", name, ref)


# --------------------------------------------------------------------------
# Plantilla
# --------------------------------------------------------------------------
def parse(path):
    text = path.read_text(encoding="utf-8")
    head, body = text.split("\n---\n", 1)
    meta = {}
    key = None
    for line in head.splitlines():
        if not line.strip():
            continue
        if re.match(r"^[a-z_0-9]+:", line):
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
        elif key:
            meta[key] += " " + line.strip()
    return meta, body


def nav_html(active):
    def mega(items, label, key):
        cur = " is-current" if active == key else ""
        lis = "".join(
            f'<li><a class="mega-link" href="{h}"><img src="{img_paths(r)[1]}" alt="" loading="lazy">'
            f'<span><b>{t}</b><small>{d}</small></span></a></li>' for h, t, d, r in items)
        return (f'<li class="has-mega{cur}"><button class="nav-link nav-toggle" aria-expanded="false">{label}'
                f'<svg class="i chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>'
                f'<div class="mega"><ul>{lis}</ul></div></li>')

    def link(h, t, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li><a class="nav-link" href="{h}"{cur}>{t}</a></li>'

    return ("<ul class=\"nav-list\">" + link("index.html", "Inicio", "inicio") +
            mega(CREACIONES, "Creaciones", "creaciones") +
            mega(CELEBRACIONES, "Celebraciones", "celebraciones") +
            link("espacios.html", "Espacios", "espacios") +
            link("sobre-eva.html", "Eva", "eva") +
            link("galeria.html", "Galería", "galeria") +
            link("encargos.html", "Encargos", "encargos") + "</ul>")


def header(meta):
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site-header" data-header>
  <div class="topbar">
    <div class="container topbar-in">
      <span class="status" data-status><i class="dot"></i><span data-status-text>Martes a sábado · 9:00 a 14:00</span></span>
      <span class="topbar-mid">{ICONS["box"]} Envíos a toda España</span>
      <span class="topbar-links">
        <a href="tel:+34607803222">{ICONS["phone"]} {PHONE}</a>
        <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{ICONS["ig"]}</a>
        <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{ICONS["fb"]}</a>
        <a href="{TT}" target="_blank" rel="noopener" aria-label="TikTok">{ICONS["tt"]}</a>
      </span>
    </div>
  </div>
  <div class="container nav-wrap">
    <a class="brand" href="index.html" aria-label="La Florería de Eva, inicio">
      <img class="brand-logo" src="assets/img/brand/logo-sm.webp" alt="" width="46" height="54">
      <span class="brand-txt"><span class="brand-script">La Florería</span><span class="brand-sub">de Eva · Manises</span></span>
    </a>
    <nav class="nav" id="menu" aria-label="Principal">
      {nav_html(meta.get("nav", ""))}
      <div class="nav-mobile-extra">
        <a class="btn btn--wa" href="{wa_link("¡Hola Eva! 🌸 Quería hacerte una consulta.")}" target="_blank" rel="noopener">{WA_ICON}<span>Escribir por WhatsApp</span></a>
        <p>{ICONS["pin"]} Mercado de los Pinos, puesto 41 · Manises</p>
        {sprigs("nav-ink")}
      </div>
    </nav>
    <a class="btn btn--wa btn--sm nav-cta" href="{wa_link("¡Hola Eva! 🌸 Quería hacerte una consulta.")}" target="_blank" rel="noopener">{WA_ICON}<span>Encargar</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú"><span></span><span></span><span></span></button>
  </div>
</header>'''


def hero(meta, name):
    slides = [s.strip() for s in meta.get("slides", "").split(",") if s.strip()]
    pics = []
    if slides:
        for i, s in enumerate(slides):
            ref, fx, fy = (s.split(":") + ["0.5", "0.5"])[:3]
            make_hero(f"{name}-{i+1}", ref, float(fx), float(fy), FORCE)
            pics.append(f"{name}-{i+1}")
    else:
        ref, fx, fy = (meta["hero"].split(":") + ["0.5", "0.5"])[:3]
        make_hero(name, ref, float(fx), float(fy), FORCE)
        pics.append(name)
    media = ""
    for i, p in enumerate(pics):
        on = " is-on" if i == 0 else ""
        load = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
        media += (f'<picture class="hero-slide{on}"><source media="(max-width: 760px)" srcset="assets/img/hero/{p}-m.webp">'
                  f'<img src="assets/img/hero/{p}.webp" alt="" {load} decoding="async"></picture>')
    insets = [s.strip() for s in meta.get("inset", "").split(",") if s.strip()]
    ovals = ""
    if insets:
        ovals = '<div class="hero-ovals" aria-hidden="true"><svg class="oval-ring" viewBox="0 0 300 400"><ellipse cx="150" cy="200" rx="146" ry="196"/></svg>'
        for i, r in enumerate(insets[:2]):
            ovals += f'<figure class="oval oval--{"ab"[i]}"><img src="{img_paths(r)[0]}" alt="" loading="eager"></figure>'
        ovals += "</div>"
    crumbs = ""
    if meta.get("crumbs"):
        bits = ['<a href="index.html">Inicio</a>'] + [html.escape(c.strip()) for c in meta["crumbs"].split(">")]
        crumbs = '<nav class="crumbs" aria-label="Migas de pan">' + '<span aria-hidden="true">/</span>'.join(bits) + "</nav>"
    actions = ""
    if meta.get("cta1"):
        lab, msg = (meta["cta1"].split("|") + [""])[:2]
        actions += f'<a class="btn btn--wa btn--lg" href="{wa_link(msg.strip())}" target="_blank" rel="noopener">{WA_ICON}<span>{lab.strip()}</span></a>'
    if meta.get("cta2"):
        lab, href = (meta["cta2"].split("|") + ["#contenido"])[:2]
        actions += f'<a class="btn btn--ghost btn--lg" href="{href.strip()}"><span>{lab.strip()}</span>{ARROW}</a>'
    variant = meta.get("hero_variant", "page")
    dots = ""
    if len(pics) > 1:
        dots = '<div class="hero-dots" role="tablist" aria-label="Fotografías">' + "".join(
            f'<button type="button" class="{"is-on" if i == 0 else ""}" aria-label="Foto {i+1}"></button>' for i in range(len(pics))) + "</div>"
    return f'''<section class="hero hero--{variant}" data-hero>
  <div class="hero-media" data-parallax>{media}</div>
  <div class="hero-shade"></div>
  <div class="container hero-in">
    <div class="hero-copy">
      {crumbs}
      <p class="eyebrow eyebrow--light">{meta.get("eyebrow", "")}</p>
      <h1 class="hero-title">{meta["h1"]}</h1>
      <p class="hero-lead">{meta.get("lead", "")}</p>
      <div class="hero-actions">{actions}</div>
    </div>
    {ovals}
  </div>
  {bouquet("hero-ink")}
  {dots}
  <a class="hero-scroll" href="#contenido" aria-label="Bajar al contenido"><span></span></a>
</section>
<div class="ribbon" aria-hidden="true"><div class="ribbon-track">{"".join(f"<span>{w}</span><i>✿</i>" for w in RIBBON * 2)}</div></div>'''


RIBBON = ["Todo hecho a mano", "Flor preservada", "Musgo natural", "Flor seca", "Diseños exclusivos",
          "Envíos a toda España", "Mercado de los Pinos · Manises", "Decorando tu vida"]


def footer():
    def col(items):
        return "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, *_ in items)
    return f'''<section class="pre-footer">
  <div class="container pre-footer-in reveal">
    {bouquet("pf-ink")}
    <p class="eyebrow">Hecho a mano en Manises</p>
    <h2 class="display">¿Lo creamos <em class="script">para ti</em>?</h2>
    <p>Cuéntale a Eva qué tienes en mente: una fecha, unos colores, un nombre, una foto. Ella te propone la pieza y te dice el precio sin compromiso.</p>
    <div class="pf-actions">
      <a class="btn btn--wa btn--lg" href="{wa_link("¡Hola Eva! 🌸 Me gustaría encargarte una pieza. Te cuento:")}" target="_blank" rel="noopener">{WA_ICON}<span>Escribir a Eva</span></a>
      <a class="btn btn--line btn--lg" href="tel:+34607803222">{ICONS["phone"]}<span>{PHONE}</span></a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="f-brand">
      <img src="assets/img/brand/logo.webp" alt="Logotipo de La Florería" width="120" height="140" loading="lazy">
      <p>Decoración con flor y musgo preservados, flor seca y artificial. Diseños exclusivos hechos a mano por Eva Mª Yuste desde 2022.</p>
      <div class="socials">
        <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{ICONS["ig"]}</a>
        <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{ICONS["fb"]}</a>
        <a href="{TT}" target="_blank" rel="noopener" aria-label="TikTok">{ICONS["tt"]}</a>
        <a href="{wa_link()}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_ICON}</a>
      </div>
    </div>
    <div><h3>Creaciones</h3><ul>{col(CREACIONES)}<li><a href="espacios.html">Decoración de espacios</a></li></ul></div>
    <div><h3>Celebraciones</h3><ul>{col(CELEBRACIONES)}<li><a href="galeria.html">Galería</a></li><li><a href="sobre-eva.html">Conoce a Eva</a></li></ul></div>
    <div class="f-visit">
      <h3>Visítanos</h3>
      <p><a href="{MAPS}" target="_blank" rel="noopener">{ICONS["pin"]}<span>Mercado de los Pinos, puesto 41<br>Pl. Rafael Atard, 41 · 46940 Manises (Valencia)</span></a></p>
      <p><a href="tel:+34607803222">{ICONS["phone"]}<span>{PHONE}</span></a></p>
      <p><a href="mailto:{EMAIL}">{ICONS["mail"]}<span>{EMAIL}</span></a></p>
      <table class="hours" data-hours>
        <tr data-day="1"><th>Lunes</th><td>Cerrado</td></tr>
        <tr data-day="2"><th>Martes</th><td>9:00 – 14:00</td></tr>
        <tr data-day="3"><th>Miércoles</th><td>9:00 – 14:00</td></tr>
        <tr data-day="4"><th>Jueves</th><td>9:00 – 14:00</td></tr>
        <tr data-day="5"><th>Viernes</th><td>9:00 – 14:00</td></tr>
        <tr data-day="6"><th>Sábado</th><td>9:00 – 14:00</td></tr>
        <tr data-day="0"><th>Domingo</th><td>Cerrado</td></tr>
      </table>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <span data-year>2026</span> La Florería de Eva · Manises</p>
    <p>Todo hecho a mano 👐 · Envíos a toda España</p>
  </div>
</footer>
<a class="wa-float" href="{wa_link("¡Hola Eva! 🌸 Te escribo desde la web.")}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{WA_ICON}<span class="wa-float-tip">¿Hablamos?</span></a>
<button class="to-top" type="button" aria-label="Volver arriba"><svg class="i" viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
<div class="lightbox" data-lightbox hidden>
  <button class="lb-close" type="button" aria-label="Cerrar">×</button>
  <button class="lb-prev" type="button" aria-label="Anterior">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="Siguiente">›</button>
</div>'''


def page(meta, body, name):
    title = meta["title"]
    desc = meta["description"]
    og = f"assets/img/hero/{name}.webp" if not meta.get("slides") else f"assets/img/hero/{name}-1.webp"
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#1f1b16">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="La Florería de Eva">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og}">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/brand/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Allura&family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,50;1,9..144,300..600,50&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Florist","name":"La Florería de Eva","image":"assets/img/brand/logo.png","telephone":"+34 607 80 32 22","email":"{EMAIL}","address":{{"@type":"PostalAddress","streetAddress":"Mercado de los Pinos, Pl. Rafael Atard, 41","addressLocality":"Manises","postalCode":"46940","addressRegion":"Valencia","addressCountry":"ES"}},"openingHours":"Tu-Sa 09:00-14:00","foundingDate":"2022-10-22","founder":"Eva Mª Yuste García","sameAs":["{IG}","{FB}","{TT}"],"aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"36"}}}}</script>
</head>
<body class="page-{name}">
{header(meta)}
<main id="main">
{hero(meta, name)}
<div id="contenido"></div>
{shortcodes(body)}
</main>
{footer()}
<script src="assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
'''


FORCE = "--heroes" in sys.argv


def main():
    for f in sorted(SRC.glob("*.html")):
        meta, body = parse(f)
        name = f.stem
        out = ROOT / f"{name}.html"
        out.write_text(page(meta, body, name), encoding="utf-8")
        print("ok", out.name)


if __name__ == "__main__":
    main()
