# Fase 4 — SFX, QC y entrega

> ⚙️ DOC DE MOTOR (universal), neutralizado para Valor de Ley. La técnica es la del motor;
> la infraestructura de entrega es la de VdL (revisión en local).

## SFX (sintéticos, sin descargar nada)

VdL quiere **SFX sutiles, sin música**. Se sintetizan con ffmpeg y se mezclan en POST (no dentro de Hyperframes — más simple y desacoplado).

Genera la paleta una vez por proyecto:
```bash
bash ~/.claude/skills/reel-edita-vdl/scripts/make-sfx.sh motion/sfx
```
Crea: `whoosh` (transiciones), `pop` (chips), `type` (tecleo terminal), `buzz` (error), `boom` (impacto/reveal), `ding` (check / cifra clavada), `riser` (subida antes de un reveal).

Mezcla los SFX en el render con una lista de eventos `[ [sfx, tiempo], ... ]`:
```bash
python3 ~/.claude/skills/reel-edita-vdl/scripts/mix-sfx.py \
  --base motion/renders/reel-full.mp4 \
  --sfx-dir motion/sfx \
  --out motion/renders/REEL-FINAL.mp4 \
  --events '[["boom",0.0],["riser",0.2],["whoosh",0.8],["pop",0.98],["whoosh",6.5],["ding",8.6]]'
```
Pon un evento donde haya una entrada/transición/impacto. Los volúmenes ya vienen bajos (acentos bajo la voz) y la mezcla aplica un `alimiter` para no saturar. Si re-cortas o re-sincronizas, **re-temporiza también los eventos** (sus tiempos cambian con la duración).

**Impact-landing en cambios de sección:** una transición se siente "producida" cuando el whoosh **aterriza** en un golpe corto justo en el corte. En los cambios de sección fuertes (y en el corte del cold open al cuerpo) encadena `riser`/`whoosh` que sube → `boom`/`ding` que cae EXACTO en el frame del cambio: `[["whoosh",t-0.4],["boom",t]]`. No en cada corte (cansa); solo en los beats que marcan sección. SFX siempre bajo la voz.

## Librería CC0 (sonidos reales)

`bash scripts/import-sfx-kenney.sh` (una vez por instalación) importa 97 SFX reales CC0 (Kenney.nl /
OpenGameArt, vía el repo de /brag en un commit revisado) a `assets/sfx-kenney/`. `bash scripts/sfx-kit.sh motion/sfx`
deja en el proyecto los sintéticos + los reales, con nombre plano: `mix-sfx.py` los usa igual, `["card-slide-3", 2.4]`.
Los reales vienen más altos que los sintéticos → pasa `--vol` (0.5-0.8 en vídeos sin voz, 0.2-0.35 bajo la voz).

| Momento | Sonidos | Volumen orientativo (bajo voz) |
|---|---|---|
| Tecleo en pantalla | `keypress-001…032` (alternar) | 0.18-0.25 |
| Clic / pulsación / CTA | `click_001…005`, `click1…5`, `mouseclick1`, `select_008` | 0.22-0.30 |
| Pasar página / tarjeta que entra | `card-slide-1…8`, `card-place-1…4`, `card-fan-1…2` | 0.25-0.35 |
| Elemento que se posa, chip | `drop_001…003` | 0.22 |
| Toggle / cambio de modo | `switch_001…007` | 0.22 |
| Reveal cálido | `impactWood_light_*`, `impactWood_medium_*`, `impactSoft_medium_*` | 0.30-0.40 |
| Notificación limpia | `impactPlate_light_*`, `impactGlass_light_*` | 0.20 |
| Remate (1 vez) | `impactBell_heavy_000`, `impactBell_heavy_003`, `bong_001` | 0.30 |
| Hover sutil | `rollover1…5` | 0.15 |

Paleta coherente: en un mismo vídeo, una familia de clics y una de papel, no un poco de todo.

### Reglas de oficio del sonido (de correcciones reales de clientes, `video-shotcraft` aesthetic-rules)
- **Sonidos de objetos reales, no de videojuego.** La pregunta: ¿suena como ESE objeto en el mundo real
  (interruptor, papel, cristal, tecla) o como un aviso de juego (pluck, bloop, bleep)? Lo segundo, fuera,
  salvo que la pieza quiera decir "notificación del sistema". Ojo: dentro de la librería CC0 hay de los dos.
- **Foley antes que adorno:** si en pantalla se teclea, suena teclado; si caen fichas, suena cada ficha.
  Un whoosh genérico no tapa una acción con identidad. Recorta el sonido a lo que dura la acción.
- **Tabla de SFX = una fila por acción visible** (segundo, sonido, volumen, comentario de qué pasa). Nada
  "por sensación". `mix-sfx.py` acepta `[sonido, t, volumen]` por evento; guárdala en `edicion/sfx.json` y
  pásala con `--events "$(cat edicion/sfx.json)"`.
- **Ráfagas sin efecto metralleta:** alterna 2 muestras, baja el volumen en escalera (p. ej. 0.40 → 0.25)
  y acelera los intervalos siguiendo la animación.
- **El sonido se hace con la imagen BLOQUEADA.** Si cambia la duración u orden de un plano, se re-temporiza
  la tabla ENTERA (y se vuelve a pasar `sync-check.mjs` si hay música).

### Música original (Modo B y piezas de marca)
La música de terceros sin licencia clara no se usa. En su lugar, **partitura sintetizada en código**,
determinista y sin licencias (`scripts/score_kit.py` + `plantillas/score-plantilla.py`, sacado del film de
Staynex): actos tensión → silencio → reveal → groove → remate, todo en la rejilla del tempo (120 BPM =
compás de 2 s). Planifica los cortes del vídeo EN COMPASES para que caigan en la rejilla.
```bash
cp ~/.claude/skills/reel-edita-vdl/plantillas/score-plantilla.py edicion/audio/compose.py   # edita la sección PLAN
python3 edicion/audio/compose.py                                                           # music/sfx/mix.wav
bash ~/.claude/skills/reel-edita-vdl/scripts/mux-master.sh motion/renders/cuerpo.mp4 edicion/audio/mix.wav motion/renders/cuerpo-audio.mp4
node ~/.claude/skills/reel-edita-vdl/scripts/sync-check.mjs motion/renders/cuerpo-audio.mp4 --cues-file edicion/cortes.json   # aviso
```
`mux-master.sh` masteriza a **−14 LUFS / −1 dBTP** en 2 pasadas (lo que normalizan IG/TikTok/YouTube/LinkedIn).
En Modo A (con voz) sigue siendo **sin música** salvo que se pida; si se pide, la música va −12 dB bajo la voz.

### Vídeos sin voz (Modo B)
- El render de una composición sin audio **no tiene pista de audio** → `mix-sfx.py` falla. Antes de mezclar:
  `ffmpeg -i cuerpo.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -map 0:v -map 1:a -c:v copy -c:a aac cuerpo-a.mp4`.
- Solo con SFX queda muy bajo (~−34 LUFS): al final `-af "loudnorm=I=-16:TP=-1.5:LRA=11"`.
- Además del máster, versión ligera: `-crf 26 -maxrate 8M -bufsize 16M`.

## Defaults de SFX (aplicar siempre salvo que se diga lo contrario)

- **Cold open:** SIEMPRE `riser` + `boom` (rompe el scroll). Al entrar el cuerpo, `boom` de aterrizaje.
- **Cortes de escena / cambios de sección:** `whoosh` (impact-landing: `[["whoosh",t-0.4],["boom",t]]`).
- **Listas / enumeraciones / métricas:** un `tick`/`ding` por CADA ítem (sincronizado a su reveal).
- **Cierre (cortinilla):** lo pone `scripts/cierre.sh` — `whoosh` en el barrido lime + `ding` al
  asentar el logotipo. No añadas SFX de endcard a mano ni SFX de isotipo (ya no hay isotipo).
- Todo **sutil, bajo la voz, sin música**.

**⚠️ Offset del cold open:** el cold open se concatena DELANTE del cuerpo, así que los eventos SFX del
cuerpo se **desplazan por la duración del cold open**. Patrón: calcula los eventos con los tiempos del
cuerpo y luego súmales `COLD_OPEN_DUR` antes de mezclar sobre el máster con cold open ya concatenado
(o mezcla SFX en el cuerpo ANTES de anteponer el cold open).

## QC visual (obligatorio) — sin `/watch`, con ffmpeg + Hyperframes

En este entorno no está la skill `/watch`. El QC se hace igual de bien con dos herramientas: los diagnósticos nativos de Hyperframes y frames extraídos con ffmpeg que se revisan con `Read`.

**1. Validación estática de la composición (antes de render):**
```bash
npx hyperframes validate motion/index.html   # errores JS, assets que faltan, contraste
npx hyperframes inspect  motion/index.html    # layout visual a lo largo del timeline
python3 ~/.claude/skills/reel-edita-vdl/scripts/lint-timeline.py motion/index.html --json   # gaps de ritmo
```

**2. Extrae frames de TODO el render y míralos** (no te fíes de 3 frames sueltos):
```bash
mkdir -p motion/qc
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 motion/renders/reel-full.mp4)
# ~1 frame cada 3s a lo largo de todo el render
ffmpeg -i motion/renders/reel-full.mp4 -vf "fps=1/3" -y motion/qc/frame_%03d.jpg -loglevel error
```
Luego `Read` los frames y revisa: **huecos vacíos** en el B-roll (rellénalos), **solapes** de texto, **sincronía** (cada chip/escena con lo que dice en ese momento), **legibilidad**, que la cara no quede tapada y que los títulos estén a la altura del micro/pecho.

**Chequeo de ritmo medible:** cuenta los cambios visuales (corte, movimiento de cámara, aparición de chip, zoom, escena B-roll, reveal) por cada 10s. Diana: **5-7 cambios/10s** en los tramos ágiles. <4 = se lee lento (mete movimiento/B-roll); >8 = ruido (quita). **Excepción deliberada:** los tramos "denso → aire" (ver `04-recetas.md`) van por debajo a propósito — no los infles a fuerza de cortes.

**🔴 REGLA DURA DE RITMO: nunca más de 3-4 s sin que pase algo visual.** Cada ≤4 s tiene que entrar un beat: animación, B-roll, zoom/punch (`snap`), chip/rótulo cinético, sello, movimiento de cámara (PiP/full), reveal o un float continuo perceptible. **Los subtítulos NO cuentan** como beat — son base permanente del vídeo, así que un tramo con solo talking-head + captions = tramo muerto aunque haya texto en pantalla. QC obligatorio: recorre la timeline listando los beats no-subtítulo y mide los huecos; cualquier hueco >4 s se rellena (un `snap` o un sello cinético sincronizado con una palabra-ancla basta). `lint-timeline.py` marca como error cualquier gap >4s.

Si re-sincronizaste tras un re-corte, verifica con frames exactos los puntos que se desplazaron:
```bash
for t in 62 75 90 93.4; do ffmpeg -ss $t -i motion/renders/reel-full.mp4 -frames:v 1 -y motion/qc/chk_$t.jpg -loglevel error; done
```

## Render

```bash
npx hyperframes render --quality standard --output renders/reel-full.mp4   # para QC
npx hyperframes render --quality high     --output renders/reel-full-hi.mp4 # entrega final
```
`draft` para iterar rápido un trozo; `standard` para revisar; `high` para entregar. Un render de ~100s tarda un par de minutos. Verifica duración con `ffprobe`.

**Truco de eficiencia:** para validar un look nuevo, renderiza solo los primeros ~20s (baja `data-duration` temporalmente) como proof-of-concept antes de renderizar el minuto y medio entero.

## Orden final de la Fase 4

1. `sfx-kit.sh motion/sfx` (una vez por proyecto; sintéticos + CC0).
2. Render `standard` → QC (frames + `hyperframes validate/inspect`) → arreglar → re-render hasta que esté pulido.
3. Render `high` final.
4. `mix-sfx.py` sobre el render high → `REEL-FINAL.mp4`.
5. Cierre (`cierre.sh`) → miniatura en frame 0 (`poster.sh`).
6. Última pasada de QC (frames) sobre el final.

## Entrega (local)

El resultado se deja para revisión **en local**: `REEL-<slug>-FINAL.mp4` (alta calidad, resolución heredada del bruto) en `motion/renders/`, dentro de la carpeta del proyecto. Avisa a VdL con la ruta y abre el archivo para que lo revise.

- **Nunca se toca el bruto original.** Todo el output vive en `edicion/` y `motion/` del proyecto.
- **Parámetros de entrega a redes:** H.264 `yuv420p`, `-color_primaries bt709 -color_trc bt709 -colorspace bt709`,
  rango tv, `-movflags +faststart`, AAC 48 kHz (aunque sea silencio). Comprueba con `ffprobe` que sale a la
  resolución y fps esperados antes de entregar.
- Si hace falta una versión más ligera para compartir (p. ej. por debajo de un límite de tamaño para mensajería), genera una copia manteniendo la resolución original, sin reescalar:
```bash
ffmpeg -y -i REEL-FINAL.mp4 -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart REEL-DOC.mp4
# si pesa demasiado, sube el crf (20-22). Mantiene la resolución (no reescalar).
```

## Loop de retención (post-publicación)

El reel no acaba al entregarlo: cierra el loop con los datos. Cuando VdL publique, revisa (si comparte captura de Insights) la **retención a 3s**:
- Caída en el **segundo 1** → el cold open visual/sonoro es débil (primer frame más fuerte, más contraste/impacto).
- Caída en el **segundo 3** → paró el scroll pero la **promesa es floja** (reescribir la frase-gancho del cold open).
- Caída a mitad → mete un cambio visual fuerte (B-roll, punch-in, rótulo grande) en el segundo donde cae.

Esto alimenta el cold open y el ritmo del SIGUIENTE reel. Ver `08-cold-open.md`.
