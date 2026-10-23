# La Florería de Eva · demostración web

Web estática para **La Florería**, de Eva Mª Yuste García: decoración con flor y musgo preservados, flor seca y artificial, en el Mercado de los Pinos de Manises (Valencia). Abre `index.html` en un navegador o publica la carpeta tal cual (GitHub Pages, Netlify…). Todas las rutas son relativas.

## Páginas (14)

| Página | Contenido |
| --- | --- |
| `index.html` | Portada con pase de 5 fotos, historia, cifras, 9 colecciones, materiales, destacado de Fallas 2027, negocios que han confiado, cómo encargar, reseñas reales de Google, vistazo a Instagram, mapa y horario |
| `jardines-verticales.html` | Jardines verticales y cuadros de musgo, formatos, exposiciones (Albarracín y Manises), beneficios, galería y preguntas |
| `espacios.html` | Decoración de restaurantes, hoteles, empresas y hogares con los proyectos reales (Los Porrones, Capitanía, El Abuelo Rullo, Nova Dekor) |
| `cupulas-y-rosas-eternas.html` | Cúpulas, bouquets y rosas preservadas, ideas por ocasión y cuidados |
| `flor-seca-y-eucalipto.html` | Eucalipto, pampa, blooms, centros de mesa y jarrones |
| `munecas-artesanas.html` | Muñecas de macramé y lana, parejas, novios y comuniones |
| `fallas.html` | Colección fallera con los precios del catálogo de WhatsApp (18 €, 30 €, 33 €) |
| `bodas.html` | Ramos de novia preservados, pedidas, coche de los novios |
| `comuniones-y-fiestas.html` | Pack de comunión y bautizo, coronas, graduaciones, baby shower |
| `letras-y-personalizados.html` | Letras florales, carteles y regalos con dedicatoria |
| `fechas-especiales.html` | San Valentín, Día de la Madre, Halloween, Todos los Santos y Navidad |
| `sobre-eva.html` | Historia, línea de tiempo, prensa y reseñas |
| `galeria.html` | 147 trabajos reales con filtros por colección y visor |
| `encargos.html` | Formulario que prepara el mensaje de WhatsApp, mapa, pasos y preguntas |

## Lo que la hace «viva»

- Cabeceras a todo el ancho con efecto Ken Burns y parallax, y óvalos flotantes inspirados en la forma del logotipo.
- Flores de tinta dibujadas en SVG con el estilo del logotipo, que se trazan solas al aparecer en pantalla.
- Indicador **abierto / cerrado** en tiempo real (hora de Madrid) y día de hoy resaltado en el horario.
- Contadores animados, cinta en movimiento, reseñas que avanzan solas, galería con filtros y visor (teclado y gestos).
- Cada botón de WhatsApp abre un mensaje ya escrito según la página o el producto.
- Respeta «reducir movimiento» del sistema.

## Paleta (sacada del logotipo)

Tinta `#1f1b16` · topo del óvalo `#9a937c` · papel crema `#f7f3ea` · frambuesa `#c42d45` · coral `#e2553a` · naranja `#e98a3a` · amarillo `#f1c75b` · rosa empolvado `#f1d5d6` · verde hoja `#8bae58`.
Tipografías: Fraunces (títulos), Manrope (texto) y Allura (la letra caligráfica, parecida a la del logotipo).

## Estructura técnica

- `src/*.html`: contenido de cada página. Arriba lleva sus datos (título, cabecera, textos del hero) y, tras `---`, el contenido.
- `tools/build.py`: añade cabecera, menú, hero, pie, flores de tinta y botones, y escribe las páginas en la raíz. Después de cambiar algo en `src/`:

  ```bash
  python tools/build.py
  ```

- `tools/make_share.py`: genera las tarjetas para compartir por WhatsApp (`assets/img/compartir/`, 1200 × 630, con logotipo, título y foto). Los textos de la vista previa están en el diccionario `SHARE` de `tools/build.py`.
- `tools/make_galeria.py`: regenera `src/galeria.html` con las fotos clasificadas por colección.
- `assets/css/site.css` y `assets/js/site.js`: diseño e interacción.
- `assets/img/ig/` (fotos de Instagram a 1080 px), `assets/img/thumb/` (miniaturas), `assets/img/whatsapp/` (catálogo), `assets/img/hero/` (cabeceras), `assets/img/brand/` (logotipo).
- `_fuentes_instagram/`: descargas originales. Solo hacen falta para regenerar cabeceras; no es necesario publicarlas.

### Cambiar una imagen de cabecera

Sustituye `assets/img/hero/<pagina>.webp` (horizontal) y `assets/img/hero/<pagina>-m.webp` (vertical, móvil). El script no sobrescribe las que ya existen; para volver a generarlas desde Instagram: `python tools/build.py --heroes`. Prompts sugeridos en `PROMPTS-IMAGENES.md`.

## Datos usados y pendientes de confirmar con el negocio

- **Datos de las fichas públicas:** WhatsApp y teléfono 607 80 32 22, lafloreriadeva@gmail.com, Mercado de los Pinos, Pl. Rafael Atard, 41, 46940 Manises. Horario de martes a sábado de 9:00 a 14:00. Valoración de 4,9 en Google con 36 reseñas.
- **Otra floristería parecida:** la ficha de negocioscerca.es («Floristería Eva», Carrer Mestre Guillem 14, 961 530 372) parece corresponder a **otra floristería** de Manises. No se ha usado.
- **Precios:** los de Fallas salen del catálogo actual de WhatsApp. El resto son precios publicados en Instagram en 2023 y se muestran como «desde» u orientativos. Conviene revisarlos.
- **Plazos y servicios:** los plazos orientativos, la instalación en negocios y las entregas el mismo día están redactados a partir de las fichas públicas. Hay que confirmarlos con Eva.
- **Reseñas:** son textos reales de Google, sin nombre del autor.
- **Dominio:** `lafloreriadeva.es` aparece en Google con contenido ajeno al negocio (parece caducado o reutilizado). Tenlo en cuenta si se quiere recuperar.
