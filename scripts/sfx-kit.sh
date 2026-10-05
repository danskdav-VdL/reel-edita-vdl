#!/bin/bash
# sfx-kit.sh — prepara la paleta completa de SFX de un proyecto en <dest>:
#   1) los SFX SINTETIZADOS de siempre (make-sfx.sh): whoosh, pop, type, buzz, boom, ding, riser
#   2) + la librería CC0 de Kenney (assets/sfx-kenney/, 97 sonidos reales; se importan con import-sfx-kenney.sh): teclas, clics, papel/tarjetas,
#      golpes suaves de madera, campana. Ver references/03-sfx-y-qc.md §"Librería CC0".
# Todo en .wav y con nombre plano, así mix-sfx.py los usa por nombre: ["card-slide-3", 2.4], ["keypress-017", 3.1]…
# Uso: bash sfx-kit.sh motion/sfx
set -e
DEST=${1:-motion/sfx}
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$DEST"
bash "$SKILL_DIR/scripts/make-sfx.sh" "$DEST" >/dev/null
cp "$SKILL_DIR"/assets/sfx-kenney/*.wav "$DEST/"
echo "▸ SFX en $DEST: $(ls "$DEST"/*.wav | wc -l | tr -d ' ') (sintéticos + Kenney CC0)"
