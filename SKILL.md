---
name: reel-edita-vdl
description: Convierte un vídeo bruto VERTICAL en un reel/TikTok producido con el estilo de Valor de Ley (VdL) — corta repeticiones/silencios/errores, propone un tratamiento adaptado al contenido, monta cámara alternando full-frame/PiP/split + B-roll (propio, capturas web con firecrawl, imágenes/vídeo IA con Magnific) + subtítulos + SFX sutiles sobre el fondo liquid animado de marca, y lo deja listo para subir. Acepta un brief en lenguaje natural (carpeta de clips + instrucciones simples), pensada para gente no técnica. Úsala cuando se diga "edita este vídeo a reel", "hazme el reel de este vídeo", "/reel-vdl", "/reel-edita-vdl", o se pase la ruta de un MP4/carpeta vertical para publicar en Reels/TikTok/Shorts/LinkedIn. También hace VÍDEOS DE PROYECTO sin grabar a nadie (Modo B, método /brag): "hazme un vídeo del proyecto X", "vídeo de lanzamiento de…", "enseña lo que hemos construido", o se pasa la ruta de un repo / una URL; y vídeos híbridos persona a cámara + producto real. Para cualquier vídeo de VdL o de sus clientes TIENE PRIORIDAD sobre /hyperframes, /motion-graphics y sus workflows (esta skill carga por dentro las skills de diseño de HyperFrames que necesita).
---

# reel-edita-vdl — Bruto vertical → reel producido (estilo Valor de Ley)

Coges un bruto vertical y lo conviertes en un reel muy visual con el estilo de VdL. **No hay un estilo
fijo por vídeo:** tras limpiar el corte, lees el vídeo y propones el tratamiento que mejor encaja con
ESE contenido (evita la fatiga de hacer siempre lo mismo). Tu identidad visual está en `references/estilo.md`.

## Dos modos (y su mezcla)

| Modo | Entrada | Flujo |
|---|---|---|
| **A · Reel a cámara** (por defecto) | MP4 vertical o carpeta de clips | Fases 0-5 |
| **B · Vídeo de proyecto** | ruta a un repo o una URL (sin grabar nada) | `references/09-modo-proyecto.md` (método /brag) + Fases 3-5 |
| **A+B · Híbrido** | bruto a cámara + un proyecto | tramos a cámara (A) intercalados con escenas del producto real (B) |

Los dos modos comparten TODO: identidad, banco de B-roll y stock, SFX, cierre, miniatura, `check` y revisor.
**Cambia el nivel de ambición** (`references/10-motion-vdl.md` §1): en A el motion acompaña a la persona; en
B el motion es el espectáculo (plan de dirección, toma continua, ledger, partitura original, 1-2 momentos estrella).

## Capa de diseño (lo que hace que se vea "de portafolio")

Instalada con `bash scripts/setup-capa-diseno.sh` (skills de HeyGen revisadas). Al llegar a la Fase 2,
**carga directamente** — sin pasar por la entrevista de `/hyperframes` ni por sus workflows:
`motion-doctrine` → `cut-the-curve` → `hyperframes-animation` → `hyperframes-registry` (+ `oversized-cursor`
si hay cursor; + `hyperframes-creative` y `hyperframes-core` en Modo B). Y aplica las tres referencias VdL:
- `references/10-motion-vdl.md` — **el sistema de movimiento**: una familia de curvas, ley del corte con la
  corriente a la IZQUIERDA, nada idle, un héroe por plano, lista negra del look IA. Manda sobre todo lo demás.
- `references/11-catalogo-y-recetas.md` — **catálogo primero** (~390 bloques), recetas premium, plantillas de HeyGen.
- `references/12-revision-visual.md` — **bucle de autocrítica**: snapshots → nota 1-10 → arreglar los 3 peores → todo ≥ 8.

## Reglas de oro (léelas antes que nada)

1. **El corte de audio se BLOQUEA y se aprueba ANTES de tocar una sola animación.** Las animaciones se
   sincronizan a timestamps del corte; si recortas después, toda la línea de tiempo se desplaza.
2. **El corte se decide por SILENCEDETECT, no por timestamps de Whisper** (imprecisos ±0.2-0.3s).
   Detecta islotes de voz por energía, quédate con la ÚLTIMA toma de cada frase y pega sin pausas.
3. **Nada se entrega sin pasar la COMPUERTA DURA y el REVISOR.** `verify-cut.py` exit 0 antes de animar;
   revisor PASS antes de entregar.
4. **Identidad VdL siempre** (`references/estilo.md`): paleta navy/lime/magenta, **fondo liquid animado**
   (nunca plano), Sora/Onest. **El isotipo `<` NO se usa** (salvo que VdL lo pida para ese vídeo) y el
   reel **SIEMPRE cierra con la cortinilla oficial** (`estilo.md` §8).
5. **El movimiento sigue `references/10-motion-vdl.md`** y nada se renderiza en alta sin pasar el bucle de
   `references/12-revision-visual.md` (todo ≥ 8). Primera versión = demasiado rápida: siempre.

## Entrada y workspace

**Input:** ruta de **un MP4 vertical** o de **una carpeta de clips** (varias tomas/segmentos de un guion
→ se concatenan; ver `01-corte-y-limpieza.md`) + el **cliente/agencia** y un **nombre de vídeo**.

**Ubicación y nomenclatura del proyecto (regla dura):**
- Cada vídeo = un **proyecto** (carpeta con todo dentro). Nombre de carpeta:
  **`AAAAMMDD_nombre-del-video_<cliente|VdL>`** (fecha del día; `VdL` si es de la agencia).
- **Cliente:** `clientes/<Cliente>/reels/AAAAMMDD_nombre_<cliente>/`
- **Agencia:** `agencia/reels/AAAAMMDD_nombre_VdL/`
- Dentro del proyecto: `edicion/` (corte, transcripts), `motion/` (Hyperframes) y **`AF/`** (carpeta del
  **entregable final** — ahí va el `REEL-...-FINAL.mp4`).
- **Nunca toques el bruto original.**

**Sin `GROQ_API_KEY`:** transcribe en local con `python3 scripts/transcribe-local.py <audio> <json> es` (faster-whisper,
mismo formato JSON; usa GPU si encuentra cuBLAS y si no cae solo a CPU: ~15 s por toma de 30 s con large-v3).
**Verifica al empezar:** `ffmpeg`, `npx hyperframes`, `GROQ_API_KEY` y `FIRECRAWL_API_KEY` en `.env.local`,
y que existe `~/.claude/skills/motion-doctrine` (si no: `bash ~/.claude/skills/reel-edita-vdl/scripts/setup-capa-diseno.sh`).
Para gaze (mira-a-cámara): `mediapipe` + `opencv` (`pip install --user "mediapipe==0.10.14" opencv-python` — mediapipe ≥1.0 quitó la API `solutions` que usa `gaze.py`).
**Windows:** los scripts llaman a `python3`; si solo existe `python`, crea un shim `~/bin/python3` (Git Bash) que lo invoque con `PYTHONUTF8=1` (si no, fallan los acentos/emojis y la lectura de JSON).
Opcionales (B-roll de stock, §0 de `06-broll.md`): `PIXABAY_API_KEY`, `UNSPLASH_ACCESS_KEY` en `.env.local`.

**Generación de imágenes/vídeo:** si el tratamiento necesita imágenes o vídeo generados por IA
(portadas, B-roll ilustrado), usa el **MCP `magnific`** (descubre sus tools con ToolSearch en tiempo de
ejecución). Solo assets reales/verificados o generados; nunca datos inventados.

Resolución de la composición = **la del bruto** (no forzar 1080×1920 salvo que se pida).

Autonomía (perfil VdL): **consulta en cada fase** — presenta decisiones clave y espera OK.
Meta a futuro: acercar Fase 1.5→5 a autónomo; **pero por ahora se MANTIENE la aprobación humana del
CORTE** (Fase 1) antes de montar motions/subtítulos/SFX.

---

## FASE 0 — LEER EL BRIEF (la usa gente NO técnica)

El input es **la carpeta del bruto + un brief en lenguaje natural**. Tu trabajo: **entender el brief y
traducirlo a parámetros** con el mínimo de preguntas. Corre en **Cowork o Claude Code** (necesita ffmpeg/node).

1. Identifica **proyecto** (cliente vs VdL) + **nombre** → crea `AAAAMMDD_nombre_<cliente|VdL>` en
   `clientes/<Cliente>/reels/` o `agencia/reels/` con `bruto/ assets/ edicion/ motion/ AF/`.
2. Lee el brief y extrae parámetros:

| El usuario dice… | Parámetro |
|---|---|
| "capturas de la web/página/docs de X" | **firecrawl** → capturar esa web e insertarla donde se nombra |
| "te dejé B-roll / usa estos vídeos" (en `assets/`) | usar **assets propios** en los tramos que correspondan |
| "genera/añade imágenes o vídeo IA en la parte de X" | **Magnific** (`images_generate`/`video_generate`) para ese tramo |
| "intercala full / PiP / split arriba-abajo" | **rotación de encuadres** (`04-recetas.md`); por defecto alterna full↔PiP y usa **split** cuando hay 2 cosas que mostrar a la vez |
| "poco/nada de emojis", "techy", "nada playschool" | **`emoji_level = none\|min`** |
| "para TikTok/Reels", "~30s", "más corto" | plataforma/duración objetivo |
| (nada dicho) | defaults VdL |

3. **Pregunta como MUCHO una cosa** si es imprescindible y ambigua (p. ej. cliente vs VdL). Si no, tira
   con defaults y **avisa de los supuestos**.
4. **`emoji_level` (por defecto `min`):** casi sin emojis. Sustituye emojis por **iconografía limpia**
   (glifos de línea, símbolos técnicos, números de nivel) + tipografía Sora. **Nada de caritas ni
   colorines** (look "playschool"). `none` = ningún emoji.
5. Único punto que PARA y espera OK humano = el **corte (Fase 1)**. El resto lo haces y al final presentas
   el reel + un **resumen en cristiano** (qué capturas usaste, qué imágenes generaste, qué encuadres…).

### Plantilla de brief (para el usuario)
```
Proyecto: <cliente | VdL> · Nombre: <nombre del vídeo>
Bruto en: <carpeta>   ·   B-roll propio en: <carpeta/assets/broll> (opcional)
Quiero que: <instrucciones en lenguaje normal>
  - capturas de <web/tema> · imágenes IA en la parte de <...>
  - encuadres: <full / PiP / split> · emojis: <pocos/ninguno> · plataforma: <Reels/TikTok/…>
Aprobación: enséñame el corte antes de montar.
```

---

## FASE 1 — BLOQUEAR EL CORTE (determinista) · `references/01-corte-y-limpieza.md`

0. **Si la entrada es carpeta de clips:** ordénalos (nombre/creation_time), comprueba `rotation` con
   ffprobe (móvil = 1920×1080 + `rotation=-90` → vertical) y **concaténalos con el filtro `concat`
   re-encodeando** (nunca `-c copy`) quemando la orientación → `edicion/bruto-ensamblado.mp4`. Todo lo
   que sigue (islands/verify) va SOBRE ESE archivo. Auto-recorta el aire muerto del arranque (~0.15-0.25s
   antes de la 1ª palabra). Ver `01-corte-y-limpieza.md`.
1. Extrae audio y transcribe word-level una vez (reutiliza):
   `ffmpeg -i <bruto> -vn -ac 1 -b:a 64k -y edicion/bruto-audio.m4a`
   `bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh edicion/bruto-audio.m4a edicion/bruto-word.json`
2. `python3 ~/.claude/skills/reel-edita-vdl/scripts/islands.py --media <bruto> --transcript edicion/bruto-word.json --out edicion/islands.json`
   → revisa la tabla KEEP/DROP y ajusta los `keep` (bloopers, falsos arranques, tangentes). Regla: última toma.
3. `python3 ~/.claude/skills/reel-edita-vdl/scripts/cut.py --islands edicion/islands.json --out edicion/corte-final.mp4`.
4. **COMPUERTA DURA:** re-transcribe el corte y verifica:
   `ffmpeg -i edicion/corte-final.mp4 -vn -ac 1 -b:a 64k -y edicion/cf.m4a`
   `bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh edicion/cf.m4a edicion/transcript-final.json`
   `python3 ~/.claude/skills/reel-edita-vdl/scripts/verify-cut.py --media edicion/corte-final.mp4 --transcript edicion/transcript-final.json`
   exit 0 = pasa; itera hasta exit 0.
5. **LECTURA HUMANA:** imprime el texto corrido del corte y léelo entero buscando repeticiones/reinicios
   (apoyo: `detect-repeats.py`).
6. Presenta el corte limpio (duración, qué se quitó) y **espera OK de VdL**.

## FASE 1.5 — LEER EL VÍDEO Y PROPONER TRATAMIENTO · `references/04-recetas.md`

1. Mira el corte (extrae frames con ffmpeg + `Read`) para entender qué tipo de vídeo es y su estructura.
2. **MIRADA A CÁMARA:** corre `python3 ~/.claude/skills/reel-edita-vdl/scripts/gaze.py --media edicion/corte-final.mp4 --out edicion/gaze.json`.
   **VERIFICA SIEMPRE en vídeo** los tramos que marca (extrae frames; el detector subestima cabeceos suaves).
   En el beat sheet, marca esas ventanas como **"sujeto fuera → visual a pantalla completa"** (regla VdL:
   si no mira a cámara, no sale). Las enumeraciones que lee de notas → listas animadas full-screen (cubren
   la mirada-fuera y dan ritmo). Ver los 4 puntos del método en el docstring de `gaze.py`.
3. Elige/combina un tratamiento de `references/04-recetas.md`.
4. Decide el COLD OPEN (1-3s) según el contenido · `references/08-cold-open.md`.
5. Propón a VdL 2-3 opciones con tu recomendación. **Espera que elija.**

## FASE 2 — PLANIFICAR EL MONTAJE · `references/02-motion-graphics.md`

Re-transcribe el corte aprobado → saca segment timings → **beat sheet**: mapea cada tramo, marca ritmo
(ágil en gancho/listas, aire en conceptos densos) y qué es full-frame / B-roll / cámara PiP. Para cada tramo
anota su **ruta de movimiento sostenido** (`10-motion-vdl.md` §3) y, si hay escenas full-screen encadenadas,
escribe el **ledger** de cortes (`motion/ledger.json`, §5). En Modo B esta fase es el **plan de dirección**
de `09-modo-proyecto.md` §2 (por actos, en compases), y se aprueba antes de construir.

## FASE 3 — CONSTRUIR (Hyperframes) · `references/02-motion-graphics.md` + `estilo.md`

Arranque (comando probado, no se cuelga): `export HYPERFRAMES_SKIP_SKILLS=1` y
`npx hyperframes init motion --video corte-final.mp4 --skip-transcribe --example blank --resolution portrait --non-interactive`.
Copia los assets de marca a `motion/assets/` (rutas relativas). Reglas del runtime, patrón de revelado
sincronizado y coordinación de zonas: **ver `references/02-motion-graphics.md`** (la cámara solo por
transform; `class="clip"`+`data-*`; sin solapes por pista). **Catálogo primero** para cualquier efecto con
nombre (`11-catalogo-y-recetas.md`); cortes estampados desde el ledger con `seam-stamp.mjs`.
`index.html` a la resolución del bruto (vertical) con las capas:
1. **Fondo liquid animado** de marca (`estilo.md` §2) en `#bg` · nunca plano.
2. Cámara alternando **full-frame / PiP (abajo-dcha) / split arriba-abajo** + escenas B-roll · `02-motion-graphics.md`.
3. B-roll real (firecrawl) / assets propios / insertos · `references/06-broll.md`.
4. Subtítulos a nivel del micro (`scripts/captions.py`, palabra-clave en lime `#aae05a`) · `references/07-subtitulos.md`.
5. Rótulos y texto a nivel del micro. **Sin isotipo** (`estilo.md` §4) y **sin el nombre de la marca escrito**.
6. COLD OPEN como clip separado, antepuesto con `ffmpeg concat` (no dentro del timeline) · `references/08-cold-open.md`.
7. **CIERRE:** la cortinilla oficial se pega al final en post (no en el timeline) · `estilo.md` §8.

`npx hyperframes validate` + `inspect` a 0 errores, y `python3 scripts/lint-timeline.py motion/index.html`
sin gaps >4s antes de renderizar.
Gate adicional (lint + runtime + layout + contraste WCAG + franja de UI): `npx hyperframes check motion --at-transitions --caption-zone "x0=0;y0=.84;x1=1;y1=1;severity=error"` a 0 errores, y `npx hyperframes snapshot motion --at <t1>,<t2>,…` para revisar con `Read` (gotchas en `02-motion-graphics.md` §Check).
Con ledger: `node ~/.claude/skills/motion-doctrine/scripts/seam-gate.mjs verify --ledger motion/ledger.json --project motion` → exit 0.

## FASE 3.5 — BUCLE DE AUTOCRÍTICA · `references/12-revision-visual.md`

Snapshots de cada beat asentado y de la mitad de cada transición → contact sheet → nota 1-10 en gancho,
legibilidad móvil, calidad del movimiento, variedad, composición, marca y sincronía → arregla los 3 peores →
repite hasta **todo ≥ 8** (máx. 3 rondas). Pruebas anti-PowerPoint. Solo entonces render en alta.

## FASE 4 — SFX, QC Y ENTREGA · `references/03-sfx-y-qc.md`

1. SFX sutiles (sin música en Modo A): `bash scripts/sfx-kit.sh motion/sfx` deja los sintéticos de `make-sfx.sh` + la
   librería CC0 de sonidos reales (clics, teclas, papel, madera). Sonidos de objetos reales, no de videojuego;
   una fila de la tabla por acción visible. Modo B: **partitura original** (`plantillas/score-plantilla.py`)
   + máster con `scripts/mux-master.sh` (−14 LUFS). Ver `03-sfx-y-qc.md`.
2. Render `--quality standard` → QC con frames (ffmpeg) + `hyperframes validate/inspect` (huecos,
   solapes, sincronía, legibilidad) → arreglar.
3. Mezcla SFX en post (`scripts/mix-sfx.py`).
4. Render `--quality high` final + re-mezcla SFX.
5. **CIERRE DE MARCA (obligatorio):** pega la cortinilla oficial con disolución cruzada —
   `bash ~/.claude/skills/reel-edita-vdl/scripts/cierre.sh <reel-montado.mp4> REEL-<nombre>-FINAL.mp4 0.5`
   (ver `estilo.md` §8). Deja ~0.5-0.8s de cola de silencio para que no pise voz.
6. **MINIATURA (frame 0):** `bash ~/.claude/skills/reel-edita-vdl/scripts/poster.sh AF/REEL-<nombre>-FINAL.mp4 <segundo>`
   — elige el fotograma más fuerte ya asentado (texto entero, sin transición); lo guarda como `.jpg` y lo
   hornea como frame 0 (la miniatura de LinkedIn/X/WhatsApp). El `.jpg` sirve de portada en IG/TikTok/YouTube.
7. Copia el entregable final a la carpeta **`AF/`** del proyecto (además de `motion/renders/`).

## FASE 5 — REVISOR (subagente independiente, OBLIGATORIO) · `references/05-revisor.md`

Spawnea un subagente revisor (tool `Agent`) que NO montó el reel. Re-transcribe el AUDIO DEL RENDER
FINAL desde cero y lee el texto entero buscando repeticiones. Corre `verify-cut.py` y
`lint-timeline.py --json` sobre el render, y revisa frames. Devuelve PASS/FAIL. Solo se entrega si PASS
y sin blockers.

## Reglas que no se negocian

- Brutos intactos. Output a `edicion/` y `motion/` de la carpeta del proyecto.
- Corte por silencedetect (islands→cut→verify), nunca por timestamps de Whisper.
- COMPUERTA `verify-cut.py` (exit 0) antes de animar. REVISOR (PASS) antes de entregar.
- Tratamiento propuesto según el contenido, no molde fijo.
- **Fondo liquid animado siempre. SIN isotipo en el vídeo** (salvo petición explícita de VdL) · `estilo.md` §4.
- **CIERRE OBLIGATORIO: la cortinilla oficial de VdL**, con disolución cruzada (~0.5s), pegada en post con `scripts/cierre.sh`. Siempre la misma, nunca otra ni un endcard a mano · `estilo.md` §8.
- TEXTO/SUBTÍTULOS/rótulos a NIVEL DEL MICRÓFONO, nunca pegados al borde inferior (la UI tapa el tercio de abajo).
- **SUBTÍTULOS NUNCA SOBRE EL ROSTRO.** Por debajo de la barbilla (≥~70px), adaptando la posición al
  encuadre de cada tramo; clamp por encima de la franja de UI (~1600px). Ver `references/07-subtitulos.md`.
- **Cámara FULL cuando no hay B-roll que mostrar** (la persona vuelve a pantalla completa; PiP/split solo con B-roll).
- **Encuadres: alterna full-frame, PiP y split arriba/abajo** según el tramo (no siempre el mismo). Ver `04-recetas.md`.
- **SPLIT arriba/abajo (regla de layout, ref. visual VdL):** visual/gráfico en la MITAD SUPERIOR (panel
  opaco de marca, ~top 0–870px) + la **cámara ampliada en la MITAD INFERIOR mostrando el ROSTRO** (bajar
  el encuadre con transform `y`+`scale`, no PiP diminuto) + **banda de subtítulo en la costura** (~top 890px,
  por encima del rostro que va abajo). NO usar PiP pequeño en esquina para el split. Ver `04-recetas.md` R7.
- **CÁMARA solo por transform (scale/x/y/opacity), NUNCA `top/left/width/height`** (el linter `check` lo
  bloquea: `gsap_non_transform_motion`). Para ocultar a la persona en un takeover, `opacity:0` de la cámara.
- **Marcas mencionadas → logo REAL:** cuando en el guion se nombra una marca (TikTok, Amazon, etc.), busca
  su **logo en internet (SVG vectorial o PNG con fondo transparente)** y úsalo en el reel. Fuentes fiables:
  `cdn.simpleicons.org/<marca>[/white]`, `vectorlogo.zone`, `cdn.jsdelivr.net/gh/gilbarbara/logos`. Recolorea
  para que contraste sobre navy. Si no se consigue uno limpio, **pídeselo al usuario** (que lo adjunte). Ver `06-broll.md`.
- **PROHIBIDO el sujeto semi-transparente detrás del texto** (nada de "fantasma" a ~50% con el vídeo
  translúcido). Para un rótulo/titular a pantalla: o la persona VISIBLE al 100% con el texto en lower-third,
  o **ocúltala del todo** (`opacity:0`) y pon detrás **fondo plano / degradado / liquid animado de marca**
  (nunca el vídeo atenuado del sujeto). Un `flash`/`immediateRender:false` en los `fromTo` para no lavar el arranque.
- **NUNCA escribir el texto "Valor de Ley" / "VALOR DE LEY" en pantalla** en el cuerpo del reel. La marca
  aparece SOLO en la cortinilla de cierre (que sí lleva el logotipo oficial, y va tal cual sin retocar).
- **Emojis al mínimo** (`emoji_level=min` por defecto): iconografía techy/limpia, **nada "playschool"** (ni caritas ni colorines). Ver `estilo.md`.
- Elementos de B-roll: revelado **sincronizado al audio** con entrada sutil, no todos de golpe (patrón `rev()` en `02-motion-graphics.md`).
- Si el bruto trae **subtítulos quemados**, tápalos con banda de marca o pide clips limpios (no dobles subtítulos).
- Beat visual ≤4s (`scripts/lint-timeline.py`, gap>4s = error).
- Cero repeticiones y cero silencios en el cuerpo. Última toma siempre.
- **Nunca la misma frase repetida seguida, aunque Whisper la fusione** en una palabra larga. La caza el
  check 1b de `verify-cut.py`; remediación = aislar + re-transcribir a 0.7x + última toma (ver `01`).
- **Si el sujeto no mira a cámara, no sale:** se cubre con visual full-screen (paso gaze en Fase 1.5, verificado en vídeo).
- **Isotipo `<`: NO se pone.** Ni sting, ni esquina, ni endcard, ni marca de agua. Solo si VdL lo pide
  explícitamente para ese vídeo; entonces nunca sobre el rostro ni sobre los subtítulos.
- Transiciones cámara↔escena sin crossfade con restos (corte limpio o **cut-the-curve** en la corriente
  izquierda); subtítulos suprimidos durante escenas full-screen. Nunca el signo de Z invertido en un corte.
- **Zoom-in rápido (`snap`) MÁXIMO 3 veces en todo el reel.** Es un recurso puntual, no un relleno de
  ritmo. Para los demás beats usa rótulos lower-third, reveals de escena o cambios de encuadre.
- **Golpes de pantalla completa (flash, shake, bombeo) ≤ 3 por pieza.** Nada que flote, lata o respire en
  bucle (solo el fondo liquid). Curvas solo de la familia VdL (`10-motion-vdl.md` §2): sin `bounce`/`elastic`.
- **Catálogo antes que hacer a mano** (`11-catalogo-y-recetas.md`); packs de skills de terceros NO se
  instalan sin revisión (ver su §4).
- Que NO parezca hecho por IA: evita clichés (píldoras "EL PROBLEMA/LA SOLUCIÓN", etiquetas-capítulo genéricas).
- Determinismo Hyperframes: sin `Math.random()`/`Date.now()`; `repeat` finito; timelines `paused`.
