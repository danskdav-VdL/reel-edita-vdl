# Avisos de terceros

## scripts/sync-check.mjs

Copiado de https://github.com/iart-ai/javascript-animation-skills (commit f7d0882), `skills/soundtrack/scripts/sync-check.mjs`, con 3 líneas de comentario añadidas al principio.

```
MIT License

Copyright (c) 2026 iart.ai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## scripts/parches/seam-gate-windows.py

Modifica, en la copia instalada en `~/.claude/skills/motion-doctrine/`, el archivo `scripts/seam-gate.mjs` de
https://github.com/heygen-com/hyperframes (commit cafb86a, Apache License 2.0, Copyright HeyGen, Inc.).
Cambios: limpieza del árbol de procesos con `taskkill` en Windows y búsqueda del Chrome de `~/.cache/hyperframes`.
Las líneas cambiadas llevan el comentario `[VdL]`. Las skills de HeyGen no se redistribuyen en este repo:
`scripts/setup-capa-diseno.sh` las descarga de su repositorio original e instala su LICENSE junto a ellas.

## Ideas y valores adaptados (sin copiar código)

- HeyGen `motion-doctrine` / `cut-the-curve` / `hyperframes-launches` (Apache-2.0) -> `references/10-motion-vdl.md`, `11-catalogo-y-recetas.md`.
- `charlie947/motion-graphics-skills` (MIT), `emilkowalski/skills` (MIT), `IskakovDamir/apple-motion` (MIT),
  `bangtutorial/bang-motion` (MIT), `Vincentwei1021/video-shotcraft` (Apache-2.0): reglas y valores resumidos
  y reescritos en español en `references/10`, `11`, `12` y `03`.

## Fuentes del ejemplo `ejemplos/piloto-motion-vdl/assets/fonts/`

Sora y Onest, SIL Open Font License 1.1 (vía Fontsource / Google Fonts). Se redistribuyen sin modificar.
