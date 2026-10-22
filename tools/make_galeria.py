# -*- coding: utf-8 -*-
"""Genera src/galeria.html con todas las fotos clasificadas por colección."""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATS = {
    "jardines": {"018": "Composición de jardines verticales", "019": "Jardín con helechos", "020": "Musgo bola y rodajas de madera", "021": "Jardín con marco de madera", "028": "Jardín redondo efecto bosque", "146": "Jardín alargado", "147": "Cuadro de musgo en verdes", "148": "Composición orgánica de musgo", "149": "Musgo con discos de madera", "150": "Musgo bola y liquen", "151": "Cuadro «Amore» de musgo", "152": "Detalle de musgo y madera", "182": "Cuadros con árbol preservado", "188": "Jardín con toques naranjas", "189": "Cuadro de musgo y liquen", "080": "Jardín redondo colgante", "025": "Sauce llorón preservado", "192": "Bonsái preservado"},
    "cupulas": {"060": "Cúpula con rosa roja y nombre", "072": "Cúpula especial profes", "077": "Cúpula grabada para el profe", "086": "Esfera con flor para mamá", "087": "Rosa azul con letra M", "101": "Cúpula fallera con rosa", "123": "Cubitos de metacrilato", "128": "Centro de cerámica con rosa", "131": "Cúpulas con luces", "132": "Cubo con tres rosas azules", "179": "Ocho rosas sobre musgo", "180": "Jarrón con rosa y luces", "190": "Cúpulas con flor seca y luces", "197": "Rosas preservadas de colores", "005": "Bouquet de rosa eterna", "046": "Bouquet con rosa eterna", "127": "Rosas de tallo largo"},
    "flor-seca": {"024": "Pampa, paniculata y eucalipto", "031": "Eucalipto en jarrón de cuerda", "032": "Eucalipto color vino", "033": "Bloom arcoíris", "034": "Jarrón de cristal y cuerda", "035": "Centro rosa palo con avena", "042": "Eucalipto sobre cómoda", "109": "Centro con aro", "110": "Centro con peonía y mariposa", "111": "Jarrón en tonos rojos", "112": "Jarrones vintage", "136": "Centro en tonos neutros", "137": "Centro en morados", "143": "Flores silvestres amarillas", "144": "Jarrón silvestre con musgo", "191": "Cesto de flor seca de colores", "200": "Arreglo blanco en cristal", "201": "Arreglo en morado", "203": "Arreglos en base de madera", "056": "Coronas decorativas", "173": "Jarrón rojo con luces", "175": "Jarrón lila con luces"},
    "munecas": {"057": "Muñequita con lazo rojo", "092": "Muñequita en aro", "093": "Muñequita con pétalos", "094": "Muñequita sobre flor", "100": "Muñequita con boina", "103": "Muñeca de lana rosa", "104": "Muñeca con flores moradas", "106": "Novios de hilo", "107": "Muñeca de comunión", "108": "Muñeco de comunión", "125": "Parejita en columpio", "130": "Parejita de macramé", "134": "Novios en columpio", "135": "Muñequita de macramé", "141": "Muñequita con alas", "142": "Muñeca en marco", "161": "Muñequitas en bola de cristal", "162": "Muñeca con flores", "163": "Muñequitas en aros"},
    "fallas": {"wa2": "Muñequita fallera en bastidor", "wa4": "Fallero con mocador", "wa3": "Bastidor de perfil", "wa1": "Fallera y fallero", "wa6": "Muñequita fallera en cúpula", "wa7": "Cuadro con foto y musgo", "001": "Fallera en relieve", "000": "Un record tan etern", "097": "Muñequita fallera y cúpula", "098": "Muñequita con nombre", "099": "Muñequita con brocado", "062": "Peinado con flores"},
    "celebraciones": {"002": "Coronas de comunión", "006": "Rincón de comunión", "009": "Mesa dulce", "012": "Fiesta con globos", "013": "Pasillo de ceremonia", "014": "Corona en su caja", "038": "Pedida de mano", "039": "Ramo de rosas eternas", "068": "Ramo de novia de colores", "069": "Coronita de bautizo", "071": "Placa para el coche de novios", "129": "Ramo de novia en cúpula", "139": "Ramo de novia blanco", "008": "Corona de graduación", "010": "Ramilletes de lavanda", "011": "Ramo envuelto en rojo", "054": "Diadema de flores", "102": "Cúpula baby shower", "004": "Corona de flores preservadas", "003": "Ramo con rosas y espigas"},
    "letras": {"085": "Letra M de margaritas", "113": "Letras con luces", "114": "Letra I con luz", "115": "Letra R en rojo", "116": "Letra C en lila", "117": "Letra E con perlas", "118": "Letra M en morado", "195": "Letras florales", "126": "Rodaja «Amore mío»", "176": "Rodaja «Te quiero»", "181": "Corona de familia", "122": "Corona LOVE", "120": "Corona con corazón", "172": "Corona «Te quiero siempre»"},
    "temporada": {"153": "Corona de Navidad", "154": "Velas rojas", "155": "Velas plateadas", "157": "Centro navideño", "158": "Centro en cesta", "159": "Centro dorado", "164": "Centro con cestita", "165": "Centro dorado con rosas", "166": "Centro dorado", "170": "Árboles de madera", "171": "Aros navideños", "177": "Centro con corteza", "184": "Halloween", "055": "Todos los Santos", "124": "Corazones de cerámica", "121": "Corona de San Valentín", "186": "Terrario con luz", "193": "Faroles con plantita"},
    "espacios": {"027": "Rte. Los Porrones", "030": "Trabajo en Los Porrones", "016": "Capitanía de Valencia", "015": "Catering en Capitanía", "037": "Instalando un jardín vertical", "026": "Bonsái en Nova Dekor", "036": "Flor seca en un dormitorio"},
}
LABELS = [("all", "Todo"), ("jardines", "Jardines verticales"), ("cupulas", "Cúpulas y rosas"), ("flor-seca", "Flor seca"),
          ("munecas", "Muñecas"), ("fallas", "Fallas"), ("celebraciones", "Bodas y fiestas"), ("letras", "Letras"),
          ("temporada", "Temporada"), ("espacios", "Espacios")]

seen, items = set(), []
for c, d in CATS.items():
    for k, v in d.items():
        if k not in seen:
            seen.add(k)
            items.append((k, v, c))
random.seed(7)
random.shuffle(items)
gal = "[[gal-masonry|" + "|".join(f"{k} {v} {{{c}}}" for k, v, c in items) + "]]"
btns = "".join(f'<button type="button" data-f="{k}"' + (' class="is-on"' if k == "all" else "") + f">{v}</button>" for k, v in LABELS)

HEAD = """title: Galería de trabajos · La Florería de Eva, Manises
description: Más de 150 trabajos reales de La Florería de Eva: jardines verticales, cúpulas con rosas eternas, flor seca, muñecas de macramé, colección fallera, bodas, comuniones, letras florales y decoración de temporada.
nav: galeria
hero: 045:0.5:0.4
inset: 044, 043
crumbs: Galería
eyebrow: Trabajos reales · hechos a mano
h1: Galería de <span class="script">creaciones</span>
lead: Una selección de las piezas que han salido del taller de Eva. Filtra por colección y toca cualquier foto para verla en grande.
cta1: Quiero algo así | ¡Hola Eva! 🌸 He visto tu galería y me gustaría algo parecido a:
cta2: Ver galería | #galeria
---
"""

BODY = f"""<section class="section" id="galeria">
  <div class="container">
    <div class="head head--center reveal">
      <p class="eyebrow">{len(items)} piezas reales</p>
      <h2 class="h2">Todo sale <em class="script">de sus manos</em></h2>
      <p>Todas las fotos son trabajos publicados por La Florería en Instagram y en su catálogo de WhatsApp. ¿Ves algo que te encanta? Pídelo igual o con tus colores.</p>
    </div>
    <div class="filters reveal" data-filters="g-all" role="toolbar" aria-label="Filtrar galería">{btns}</div>
    <div id="g-all">{gal}</div>
  </div>
</section>

<section class="section section--ink">
  <div class="container split">
    <div class="split-media reveal-l">
      <div class="frame-oval"><img src="assets/img/ig/041.webp" alt="Obra de flores con rostro de mujer pintado" loading="lazy"></div>
      <div class="mini"><img src="assets/img/ig/040.webp" alt="Obra con flores amarillas y rojas sobre un rostro de mujer" loading="lazy"></div>
    </div>
    <div class="reveal-r">
      <p class="eyebrow">Obra de exposición</p>
      <h2 class="h2">Rodéate de <em class="script">buenas vibras</em></h2>
      <p class="lead">«Porque los colores influyen de manera positiva en nuestro estado de ánimo sin darnos cuenta».</p>
      <p>Con estas palabras presentaba Eva la primera obra de una serie para exposición: retratos de mujer en los que el pelo se convierte en un estallido de flores. Rosas, gerberas, peonías y ranúnculos en amarillos, corales, rosas y blancos. Piezas únicas —«para los gustos, los colores»— que demuestran que la flor también puede ser arte de pared.</p>
      <p>¿Quieres una para tu casa o tu negocio? Se pueden encargar con la paleta que prefieras.</p>
      [[wa|¡Hola Eva! Me encantan tus cuadros de mujeres con flores. ¿Puedo encargar uno?|Encargar una obra]]
    </div>
  </div>
</section>

<section class="section">
  <div class="container center reveal">
    <p class="eyebrow">Hay mucho más</p>
    <h2 class="h2">Sigue el día a día <em class="script">en Instagram</em></h2>
    <p class="narrow">Novedades, procesos e historias destacadas por colecciones: Cúpulas, Eucalipto, Jardín vertical, Flor seca, Jarrones, Muñequitas, Letras, Colección Triana… y lo último que sale del taller.</p>
    <div class="actions actions--center mt-1">
      <a class="btn btn--rose btn--lg" href="https://www.instagram.com/lafloreriadeva/" target="_blank" rel="noopener">[[icon|ig]]<span>@lafloreriadeva</span></a>
      <a class="btn btn--line btn--lg" href="https://www.tiktok.com/@lafloreriadeva" target="_blank" rel="noopener">[[icon|tt]]<span>TikTok</span></a>
      <a class="btn btn--line btn--lg" href="https://www.facebook.com/profile.php?id=100088728496492" target="_blank" rel="noopener">[[icon|fb]]<span>Facebook</span></a>
    </div>
  </div>
</section>
"""

(ROOT / "src" / "galeria.html").write_text(HEAD + BODY, encoding="utf-8")
print(len(items), "fotos en la galería")
