#!/bin/bash
# import-sfx-kenney.sh — importa la selección de 97 SFX reales CC0 (Kenney.nl + OpenGameArt) desde el repo
# de /brag (github.com/latent-spaces/brag, MIT; los sonidos son CC0) a assets/sfx-kenney/ en .wav 48 kHz,
# listos para mix-sfx.py. Commit fijado y revisado: c893c5e (2026-09-30).
# Uso (desde la raíz de la skill): bash scripts/import-sfx-kenney.sh
set -e
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$SKILL_DIR/assets/sfx-kenney"; TMP=$(mktemp -d)
git clone -q https://github.com/latent-spaces/brag.git "$TMP/brag" && git -C "$TMP/brag" checkout -q c893c5e
B="$TMP/brag/skills/brag/assets/sfx"; mkdir -p "$DEST"; cd "$B"; n=0
for f in keyboard/*.wav interface/click_00*.ogg interface/drop_00*.ogg interface/switch_00*.ogg interface/bong_001.ogg \
         interface/select_008.ogg ui/click[1-5].ogg ui/mouseclick1.ogg ui/rollover*.ogg impact/impactSoft_medium_00*.ogg \
         impact/impactWood_light_00*.ogg impact/impactWood_medium_00*.ogg impact/impactPlate_light_00*.ogg \
         impact/impactGlass_light_00*.ogg impact/impactBell_heavy_000.ogg impact/impactBell_heavy_003.ogg \
         casino/card-slide-*.ogg casino/card-place-*.ogg casino/card-fan-*.ogg; do
  [ -f "$f" ] || continue
  ffmpeg -v error -y -i "$f" -ar 48000 -ac 2 "$DEST/$(basename "${f%.*}").wav" && n=$((n+1))
done
cp sfx-analysis.md "$DEST/"; rm -rf "$TMP"
echo "▸ $n SFX CC0 en $DEST"
