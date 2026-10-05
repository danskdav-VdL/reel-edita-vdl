# 06-broll.md — B-roll de VdL (real + propio)

VdL usa **B-roll real** (capturas de webs/marcas) y **assets propios** que aporta por proyecto.
**Nunca imágenes inventadas ni datos que el audio no diga.** Solo material real/verificado.

Recuerda el gotcha del motor: el B-roll (#broll, z:2) va DEBAJO de la cámara (#camera, z:5). Para que
se vea, la cámara DEBE ir en **PiP** (abajo-dcha). Cada escena B-roll → `camPiP()`.

## 0. PRIMERO: el banco propio (`BROLL_DIR`, por defecto ./broll)

Antes de capturar webs o diseñar escenas, **mira el banco**: clips y fotos reales, reutilizables.
- **Carpetas** (adaptables): `01-escritorio · 02-pantalla · 03-manos · 04-producto · 05-equipo · 06-ambiente · 07-fotos`…
- **Nombre = búsqueda:** `<categoria>_<que-se-ve-con-guiones>_<nn>.<ext>` (stock: `…_stk-<fuente>-<id>` + ficha `.json`).

1. `python3 scripts/broll-index.py` → `index.json` (archivo, categoría, tags, duración, fps, orientación, origen, `usado_en`).
2. Para cada tramo del beat sheet, busca por tags/categoría lo que ilustra la frase.
3. **Copia** (no muevas) los elegidos a `motion/assets/broll/`, rutas relativas.
4. Verticales a full-frame o split; horizontales recortados o en marco. Recorta 1 s de margen. No repitas un
   clip usado en los 3 últimos reels. Propio > stock.
5. Al entregar, añade el proyecto a `usado_en` de cada clip usado.
6. **Stock** si no hay plano propio (revisión visual obligatoria, nada entra sin verlo):
   `python3 scripts/stock-search.py buscar "<query en inglés>" --tipo video` → revisa `_candidatos/<busqueda>/hoja.jpg`
   con Read → `python3 scripts/stock-search.py bajar --busqueda <slug> --elegidos 2,7 --categoria <cat> --desc <que-se-ve>`
   → `bash scripts/grade-look.sh <clip> <salida> 0.7 --vertical` (etalonado VdL + recorte 9:16) → `broll-index.py`.
   Claves en `.env.local`: `PIXABAY_API_KEY` (vídeo+foto), `UNSPLASH_ACCESS_KEY` (fotos). Pixabay casi no tiene
   vertical y **mezcla contenido generado con IA** → descártalo al revisar. Máx. ~40 % stock por reel, siempre
   etalonado, personas de stock **nunca** presentadas como el equipo o clientes, sin marcas de terceros visibles.
7. Si nada encaja, sigue con capturas/logos/escenas y **anota en el resumen qué plano faltó** para grabarlo.

## 1. B-roll real con firecrawl (capturas de webs/logos)

`FIRECRAWL_API_KEY` está en el `.env.local` del proyecto. Úsalo para traer capturas reales de una web,
producto o logo que VdL mencione (marketing, tech, SaaS, "sistemas agénticos").

```bash
# ejemplo: captura de una web (screenshot) vía firecrawl scrape
curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://ejemplo.com","formats":["screenshot@fullPage"]}' \
  -o motion/assets/broll/ejemplo.json
# extrae la URL/imagen del screenshot del JSON y descárgala a motion/assets/broll/
```
Hyperframes también trae `npx hyperframes capture` para preparar webs para vídeo — úsalo si encaja.
Coloca la captura en un **marco de navegador** con scroll suave (`smooth`), sincronizada con lo que se dice.

## 1b. Logos de marcas mencionadas (REGLA DURA)

Cuando el guion **nombra una marca** (TikTok, Amazon, Shopify, Meta, Google…), hay que **usar su logo
REAL** en el reel — nunca un glifo/emoji genérico que la sustituya. Consíguelo como **SVG vectorial o PNG
con fondo transparente** desde una fuente fiable y guárdalo en `motion/assets/`:

```bash
# Simple Icons (monocromo, muy limpio; /white para blanco sobre navy)
curl -sL "https://cdn.simpleicons.org/tiktok/white"  -o motion/assets/tiktok.svg
# vectorlogo.zone (con color) — OJO: a veces trae el wordmark fuera de lienzo, límpialo
curl -sL "https://www.vectorlogo.zone/logos/amazon/amazon-icon.svg" -o /tmp/az.svg
# alternativa: cdn.jsdelivr.net/gh/gilbarbara/logos/logos/<marca>.svg
```
- Simple Icons retira algunas marcas grandes (p.ej. Amazon) por trademark → usa otra fuente.
- **Recolorea** el logo para que contraste sobre navy (blanco, o su color de marca si va sobre caja oscura).
- Colócalo en la tarjeta/badge de la escena (con su etiqueta de texto al lado para máxima claridad).
- **Si no consigues un logo limpio, PÍDESELO al usuario** (que lo adjunte a `assets/`). No lo dibujes a mano.

## 2. Assets propios de VdL / cliente

VdL deja imágenes, clips, capturas o logos en la carpeta **`assets/` del proyecto**. Tómalos de ahí:
- Insertos a full-frame o en marco; logos de cliente en insignia (badge) — **solo reales**.
- Sincroniza cada asset con la frase que ilustra (J-cut: entra ~0.15-0.3s antes de la palabra).

## 3. B-roll diseñado (cuando no hay captura ni asset)

Escenas construidas con motion (ver catálogo en `02-motion-graphics.md`): tarjeta de dato con contador,
terminal en vivo (`typeIn`), diagrama de flujo, rejilla 2×2 con checks. Todas con
fondo **liquid animado** de marca + relleno (8-10 elementos, nada de medio frame vacío), cámara en PiP.

## 4. Imágenes / vídeo generados por IA — MCP `magnific`

Si el tratamiento pide imágenes o vídeo generados (portadas, cold opens ilustrados, metáforas visuales,
B-roll que no existe como captura real), usa el **MCP `magnific`** (conectado vía
`claude mcp add --transport http magnific https://mcp.magnific.com`). Descubre sus tools con **ToolSearch**
en tiempo de ejecución (p. ej. `select:` por nombre tras un keyword search "magnific image/video") y
llama a la de generación que corresponda. Guarda los assets en `motion/assets/` y referéncialos relativos.
Regla anti-humo: nada de datos/cifras inventadas en las imágenes; el contenido visual debe sostener lo que dice el audio.

## 5. Data-viz (activado en el perfil)

Para explicar cifras/procesos: gráficas de barras (`scaleY`), contadores (count-up con proxy
`{v:0}`→objetivo y `toLocaleString('es-ES')`), esquemas de nodos. Colores VdL: barras en lime/magenta
sobre navy. Los números que aparezcan **tienen que decirse en el audio** (regla anti-humo del revisor).
