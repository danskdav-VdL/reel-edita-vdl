#!/bin/bash
# grade-look.sh — etalona un clip (sobre todo de stock) para que case con la paleta de la marca.
# Preset VdL: sombras hacia navy (#00004b), medios neutros, altas limpias, saturación contenida, grano fino.
# Alternativa nativa: `npx hyperframes media-treatment --analyze/--grading`.
# No toca el original: escribe una copia.
#
# Uso: bash grade-look.sh <entrada.mp4> <salida.mp4> [intensidad 0-1, default 0.7] [--vertical]
#   --vertical  recorta al centro a 9:16 (para clips horizontales) y escala a 1080x1920
set -e
IN=$1; OUT=$2; K=${3:-0.7}; V=$4
[ -f "$IN" ] || { echo "uso: grade-look.sh <entrada> <salida> [0-1] [--vertical]"; exit 1; }
CROP=""
[ "$V" = "--vertical" ] && CROP="crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920:flags=lanczos,"
# colorbalance: sombras hacia navy, medios casi neutros, altas limpias · eq: contraste/saturación suaves · noise: grano
ffmpeg -y -v error -i "$IN" -vf "${CROP}\
colorbalance=rs=-$(python3 -c "print(0.06*$K)"):gs=-$(python3 -c "print(0.04*$K)"):bs=$(python3 -c "print(0.10*$K)"):bm=$(python3 -c "print(0.02*$K)"):rh=$(python3 -c "print(0.01*$K)"):bh=-$(python3 -c "print(0.01*$K)"),\
eq=contrast=$(python3 -c "print(1-0.08*$K)"):saturation=$(python3 -c "print(1-0.18*$K)"):gamma=1.02,\
curves=all='0/$(python3 -c "print(0.05*$K)") 1/0.97',\
noise=alls=$(python3 -c "print(int(7*$K))"):allf=t,format=yuv420p" \
  -c:v libx264 -crf 17 -preset medium -an "$OUT"
echo "▸ etalonado -> $OUT"
