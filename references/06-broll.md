# 06-broll.md — B-roll de VdL (real + propio)

VdL usa **B-roll real** (capturas de webs/marcas) y **assets propios** que aporta por proyecto.
**Nunca imágenes inventadas ni datos que el audio no diga.** Solo material real/verificado.

Recuerda el gotcha del motor: el B-roll (#broll, z:2) va DEBAJO de la cámara (#camera, z:5). Para que
se vea, la cámara DEBE ir en **PiP** (abajo-dcha). Cada escena B-roll → `camPiP()`.

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

## 2. Assets propios de VdL / cliente

VdL deja imágenes, clips, capturas o logos en la carpeta **`assets/` del proyecto**. Tómalos de ahí:
- Insertos a full-frame o en marco; logos de cliente en insignia (badge) — **solo reales**.
- Sincroniza cada asset con la frase que ilustra (J-cut: entra ~0.15-0.3s antes de la palabra).

## 3. B-roll diseñado (cuando no hay captura ni asset)

Escenas construidas con motion (ver catálogo en `02-motion-graphics.md`): tarjeta de dato con contador,
terminal en vivo (`typeIn`), diagrama de flujo, rejilla 2×2 con checks, reveal de isotipo. Todas con
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
