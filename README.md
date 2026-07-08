# reel-edita-vdl

Skill de **Claude Code / Cowork** que convierte un vídeo bruto vertical (o una carpeta de clips) en un
**reel producido con la identidad de Valor de Ley (VdL)**: corte limpio determinista, tratamiento adaptado
al contenido, cámara alternando full-frame / PiP / split, B-roll (propio + capturas web con **firecrawl** +
imágenes/vídeo IA con **Magnific**), subtítulos palabra a palabra, SFX sutiles y fondo *liquid* animado de marca.

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

> Las API keys NO viven en la skill: se leen de un `.env.local` del proyecto (los scripts lo buscan hacia
> arriba desde el cwd). Este repo **no contiene secretos**.

## Estructura
```
reel-edita-vdl/
├── SKILL.md            # flujo (Fase 0 leer-brief → 1 corte → 1.5 tratamiento → 2-3 montaje → 4 SFX/QC → 5 revisor)
├── perfil.json         # perfil de estilo VdL
├── references/         # motor (corte, motion, SFX/QC, revisor) + identidad (estilo, recetas, cold open, subtítulos, B-roll)
└── scripts/            # islands, cut, verify-cut (compuerta), transcribe-groq, captions, gaze, lint-timeline, make-sfx, mix-sfx, detect-repeats
```

## Notas
- Identidad de marca (fuentes, isotipo, colores) en `recursos/brand-kit-vdl/` del workspace VdL.
- Requiere un entorno con shell + ffmpeg (Claude Code o Cowork; no el chat web puro).
