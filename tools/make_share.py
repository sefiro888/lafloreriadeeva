# -*- coding: utf-8 -*-
"""
Genera las imágenes para compartir (WhatsApp, Facebook, etc.) en
assets/img/compartir/<pagina>.jpg, de 1200 × 630 px.

Necesita Playwright y el servidor local en marcha:
    python -m http.server 8765
    python tools/make_share.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "compartir"
BASE = "http://localhost:8765/"

# página: (etiqueta, título, palabra caligráfica, subtítulo, foto, foto pequeña)
CARDS = {
    "index": ("Mercado de los Pinos · Manises", "Flores que", "no se marchitan", "Jardines de musgo, cúpulas con rosas eternas y detalles hechos a mano.", "ig/020", "ig/131"),
    "jardines-verticales": ("La especialidad de la casa", "Jardines", "en el aire", "Musgo preservado que no se riega y dura años.", "ig/019", "ig/151"),
    "espacios": ("Hostelería · empresas · hogar", "Espacios que", "respiran", "Decoración preservada para restaurantes, hoteles y casas.", "ig/027", "ig/018"),
    "cupulas-y-rosas-eternas": ("Regalos que duran años", "Una rosa", "para siempre", "Cúpulas de cristal con rosa eterna, musgo y luces.", "ig/190", "ig/131"),
    "flor-seca-y-eucalipto": ("Para vestir tu casa", "El encanto de", "lo natural", "Eucalipto, pampa y flor seca a juego con tu hogar.", "ig/032", "ig/024"),
    "munecas-artesanas": ("Macramé y lana", "Muñecas", "con alma", "Novios, comuniones y parejitas tejidas a mano.", "ig/130", "ig/103"),
    "fallas": ("Fallas 2027", "Colección", "fallera", "Muñequitas y cuadros con brocado valenciano. Desde 18 €.", "whatsapp/wa2", "whatsapp/wa8"),
    "bodas": ("Sí, quiero", "El ramo que", "no se marchita", "Ramos de novia preservados, pedidas y detalles de boda.", "ig/039", "ig/129"),
    "comuniones-y-fiestas": ("Comuniones · bautizos · graduaciones", "Su gran día,", "todo a juego", "Coronas de flores, ramos y el pack completo de decoración.", "ig/002", "ig/008"),
    "letras-y-personalizados": ("Con nombre propio", "Tu inicial,", "en flor", "Letras florales, carteles y regalos con dedicatoria.", "ig/113", "ig/114"),
    "fechas-especiales": ("Todo el año", "Cada fecha,", "un detalle", "San Valentín, Día de la Madre, Todos los Santos y Navidad.", "ig/157", "ig/127"),
    "sobre-eva": ("Eva Mª Yuste García", "Hola, soy", "Eva", "Artista floral en el Mercado de los Pinos desde 2022.", "ig/037", "ig/059"),
    "galeria": ("Trabajos reales", "Galería de", "creaciones", "Casi 150 piezas hechas a mano en Manises.", "ig/045", "ig/020"),
    "encargos": ("Hablemos de tu idea", "Encárgalo", "a tu manera", "WhatsApp, recogida en el mercado o envío a toda España.", "ig/191", "ig/039"),
}

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Allura&family=Fraunces:opsz,wght,SOFT@9..144,300..500,50&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{font-family:Manrope,sans-serif;color:#1f1b16;position:relative;
 background:radial-gradient(120% 90% at 100% 0%,#f3d9da 0%,rgba(243,217,218,0) 55%),linear-gradient(120deg,#fbf9f4 0%,#f4efe4 60%,#efe6dc 100%)}}
.left{{position:absolute;left:70px;top:52px;width:610px;height:526px;display:flex;flex-direction:column}}
.brand{{display:flex;align-items:center;gap:20px}}
.brand img{{width:96px;height:auto;filter:drop-shadow(0 8px 14px rgba(31,27,22,.22))}}
.brand b{{display:block;font-family:Allura,cursive;font-weight:400;font-size:62px;line-height:.9;color:#1f1b16}}
.brand small{{display:block;margin-top:6px;font-size:15px;font-weight:800;letter-spacing:.26em;color:#c42d45}}
.eyebrow{{margin-top:44px;display:flex;align-items:center;gap:14px;font-size:17px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#c42d45}}
.eyebrow:before{{content:"";width:46px;height:2px;background:#c42d45}}
h1{{margin-top:16px;font-family:Fraunces,serif;font-weight:300;font-variation-settings:"SOFT" 50,"opsz" 120;font-size:{size}px;line-height:1;letter-spacing:-.02em}}
h1 em{{display:block;font-family:Allura,cursive;font-style:normal;font-weight:400;color:#c42d45;font-size:1.3em;line-height:.95;letter-spacing:0}}
p{{margin-top:14px;font-size:24px;line-height:1.35;color:#4a4338;max-width:560px}}
.pill{{margin-top:auto;align-self:flex-start;display:flex;align-items:center;gap:12px;background:#1fa855;color:#fff;border-radius:999px;padding:14px 26px;font-size:21px;font-weight:800}}
.pill svg{{width:26px;height:26px}}
.right{{position:absolute;right:62px;top:34px;width:400px;height:562px}}
.ring{{position:absolute;inset:-12px -14px -12px -14px;border:2px dashed rgba(156,147,124,.75);border-radius:50%}}
.oval{{position:absolute;inset:0;border-radius:50%;overflow:hidden;border:8px solid #fff;box-shadow:0 30px 60px -20px rgba(31,27,22,.45)}}
.oval img,.mini img{{width:100%;height:100%;object-fit:cover}}
.mini{{position:absolute;left:-70px;bottom:6px;width:170px;height:220px;border-radius:50%;overflow:hidden;border:7px solid #fff;box-shadow:0 20px 40px -14px rgba(31,27,22,.5)}}
.ink{{position:absolute;left:640px;bottom:-6px;width:230px;opacity:.9}}
</style></head><body>
<div class="left">
  <div class="brand"><img src="{base}assets/img/brand/logo.webp"><div><b>La Florería</b><small>DE EVA · MANISES</small></div></div>
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}<em>{script}</em></h1>
  <p>{sub}</p>
  <div class="pill"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91A9.9 9.9 0 0 0 12.04 2Zm5.8 14.13c-.25.69-1.44 1.32-2 1.4-.51.08-1.15.11-1.86-.12-.43-.13-.98-.32-1.68-.62-2.96-1.28-4.89-4.26-5.04-4.46-.15-.2-1.2-1.6-1.2-3.05 0-1.45.76-2.16 1.03-2.46.27-.3.59-.37.79-.37h.57c.18 0 .43-.07.67.51.25.59.84 2.04.91 2.19.07.15.12.32.02.52-.1.2-.15.32-.3.49-.15.17-.31.39-.45.52-.15.15-.3.31-.13.61.17.3.77 1.27 1.65 2.06 1.14 1.01 2.1 1.33 2.4 1.48.3.15.47.12.65-.07.17-.2.74-.86.94-1.16.2-.3.39-.25.66-.15.27.1 1.72.81 2.01.96.3.15.49.22.57.34.07.12.07.71-.18 1.4Z"/></svg>Pide por WhatsApp · 607 80 32 22</div>
</div>
<div class="right"><div class="ring"></div><div class="oval"><img src="{base}assets/img/{img}.webp"></div><div class="mini"><img src="{base}assets/img/{mini}.webp"></div></div>
<div class="ink">{ink}</div>
</body></html>"""


def main():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from build import bouquet
    OUT.mkdir(parents=True, exist_ok=True)
    ink = bouquet("is-in").replace('class="ink', 'style="width:100%" class="ink')
    style = ("<style>.ink .s{fill:none;stroke:#1f1b16;stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}"
             ".ink .s.thin{stroke-width:1.5}.f-rose{fill:#e04a62}.f-blush{fill:#f4c4cc}.f-coral{fill:#e8503a}"
             ".f-orange{fill:#ec7a34}.f-sun{fill:#f5d67c}.f-leaf{fill:#9cc067}.ink .f{opacity:.92}</style>")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for name, (eyebrow, title, script, sub, img, mini) in CARDS.items():
            size = 76 if len(title) + len(script) < 26 else 66
            html = TEMPLATE.format(base=BASE, eyebrow=eyebrow, title=title, script=script, sub=sub,
                                   img=img, mini=mini, size=size, ink=style + ink)
            pg.set_content(html, wait_until="networkidle")
            pg.wait_for_timeout(300)
            f = OUT / f"{name}.jpg"
            pg.screenshot(path=str(f), type="jpeg", quality=86)
            print("ok", f.name, f.stat().st_size // 1024, "KB")
        b.close()


if __name__ == "__main__":
    main()
