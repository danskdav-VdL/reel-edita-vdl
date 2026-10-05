# reel-edita-vdl

Skill de **Claude Code / Cowork** que convierte un vídeo bruto vertical (o una carpeta de clips) en un
**reel producido con la identidad de Valor de Ley (VdL)**: corte limpio determinista, tratamiento adaptado
al contenido, cámara alternando full-frame / PiP / split, B-roll (propio + capturas web con **firecrawl** +
imágenes/vídeo IA con **Magnific**), subtítulos palabra a palabra, SFX sutiles, fondo *liquid* animado de
marca y **cierre con la cortinilla oficial de VdL**.

Pensada para usarse con un **brief en lenguaje natural** (gente no técnica): se invoca con `/reel-edita-vdl`,
se le pasa la carpeta del bruto + instrucciones simples, y monta sola — con **un único punto de aprobación
humana: el corte**.

## Instalación
Copiar esta carpeta a la carpeta de skills de Claude Code:
```bash
cp -R reel-edita-vdl ~/.claude/skills/
```
Reiniciar la sesión → invocable como `/reel-edita-vdl`.

## Dependencias
- **Imprescindibles:** `ffmpeg`, `node`/`npx`, **Hyperframes** (`npx hyperframes`), **Groq** (`GROQ_API_KEY` en `.env.local`).
- **B-roll:** **firecrawl** (`FIRECRAWL_API_KEY` en `.env.local`) para capturas web; **Magnific** (conector MCP) para imágenes/vídeo IA.
- **Mirada a cámara:** `mediapipe` + `opencv` (`pip install --user mediapipe opencv-python`).
- **Capa de diseño de motion** (skills de HeyGen revisadas: HyperFrames oficiales + `motion-doctrine`,
  `cut-the-curve`, `seam-craft`, `oversized-cursor`), una vez por máquina:
  ```bash
  bash scripts/setup-capa-diseno.sh      # instala, aplica el parche Windows del verificador y apaga la telemetría
  bash scripts/import-sfx-kenney.sh      # 97 SFX CC0 (no se versionan)
  ```
- **Partitura original (Modo B):** `numpy` + `scipy` (`pip install --user numpy scipy`).
- **Windows:** los scripts llaman a `python3`; crea un shim `~/bin/python3` (Git Bash) que ejecute
  `python` con `PYTHONUTF8=1`.

> Las API keys NO viven en la skill: se leen de un `.env.local` del proyecto (los scripts lo buscan hacia
> arriba desde el cwd). Este repo **no contiene secretos**.

## Estructura
```
reel-edita-vdl/
├── SKILL.md            # flujo (Fase 0 leer-brief → 1 corte → 1.5 tratamiento → 2-3 montaje → 4 SFX/QC → 5 revisor)
├── perfil.json         # perfil de estilo VdL
├── references/         # motor (corte, motion, SFX/QC, revisor) + identidad (estilo, recetas, cold open, subtítulos, B-roll)
│                       #   09 modo proyecto · 10 SISTEMA DE MOVIMIENTO · 11 catálogo/recetas/plantillas · 12 autocrítica
├── plantillas/         # score-plantilla.py (partitura original por actos en rejilla de tempo)
├── ejemplos/           # ejemplo Modo B (estructura)
└── scripts/            # islands, cut, verify-cut (compuerta), transcribe-groq, captions, gaze, lint-timeline, make-sfx, mix-sfx,
                        # cierre, detect-repeats, poster, sfx-kit, broll-index, stock-search, grade-look, score_kit,
                        # mux-master, sync-check, setup-capa-diseno, parches/
```

## Reglas duras de marca (18/08/2026)

- 🔴 **El isotipo `<` NO se usa en el vídeo.** Ni sting en esquina, ni marca de agua, ni endcard, ni dentro
  de una escena. Solo si VdL lo pide **explícitamente** para ese vídeo. Tampoco se escribe nunca
  "Valor de Ley" en el cuerpo del reel. Ver `references/estilo.md` §4.
- 🔴 **Todos los reels cierran con la cortinilla oficial de VdL**, siempre la misma, unida con **disolución
  cruzada** (~0.5s) en post. No se diseña un endcard de marca a mano ni se retoca la cortinilla.
  Ver `references/estilo.md` §8 y `scripts/cierre.sh`:
  ```bash
  bash scripts/cierre.sh <reel-montado.mp4> <FINAL.mp4> [xfade]
  ```
  El script resuelve la cortinilla, la normaliza a la resolución/fps del reel, le pone pista de audio
  (viene muda) + SFX suaves, y une con `xfade` + `acrossfade`. Avisa si la disolución pisaría voz.
  La cortinilla se busca en `recursos/Cierres reels/` del workspace; se puede forzar con
  `export VDL_CIERRE_DIR="/ruta/a/Cierres reels"`.

Ambas reglas las hace cumplir el **revisor** de la Fase 5 (checks 10 y 11): si el isotipo aparece sin
petición explícita, o falta la cortinilla, el reel **no se entrega**.

## Notas
- Identidad de marca (fuentes, colores, isotipo) en `recursos/brand-kit-vdl/` del workspace VdL;
  la cortinilla de cierre en `recursos/Cierres reels/`.
- Requiere un entorno con shell + ffmpeg (Claude Code o Cowork; no el chat web puro).

## Código de terceros

Ver `THIRD_PARTY_NOTICES.md`. Resumen: `scripts/sync-check.mjs` (MIT, iart.ai); el parche
`scripts/parches/seam-gate-windows.py` modifica `seam-gate.mjs` de HeyGen (Apache-2.0) en la copia instalada;
las skills de HeyGen se descargan de su repo al instalar (no se redistribuyen aquí).
