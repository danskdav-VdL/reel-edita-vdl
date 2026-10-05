#!/bin/bash
# poster.sh — MINIATURA: extrae el mejor fotograma (asentado, texto completo, sin transición) a <video>.jpg
# y lo "hornea" como FOTOGRAMA 0 del vídeo, porque LinkedIn, X, Slack, WhatsApp y casi todas las
# plataformas usan el frame 0 como miniatura. Reemplaza SOLO el primer frame: misma duración, mismo
# número de frames y audio copiado tal cual (técnica tomada de /brag).
#
# Uso: bash poster.sh <video.mp4> <segundo-del-mejor-frame> [salida.mp4]
#   sin salida -> sobrescribe el vídeo (hace copia temporal y comprueba la duración antes de reemplazar)
# Calidad: CRF=19 por defecto (redes); CRF=16 bash poster.sh ... para máster.
# El .jpg queda al lado del vídeo: súbelo como portada personalizada donde se pueda (IG, TikTok, YouTube,
# editor de LinkedIn).
set -e
IN=$1; T=$2; OUT=${3:-$1}
[ -f "$IN" ] && [ -n "$T" ] || { echo "uso: poster.sh <video.mp4> <segundo> [salida.mp4]"; exit 1; }
JPG="${OUT%.*}.jpg"
ffmpeg -v error -y -ss "$T" -i "$IN" -frames:v 1 -q:v 2 "$JPG"
TMP="${OUT%.*}.poster-tmp.mp4"
ffmpeg -v error -y -i "$IN" -i "$JPG" -filter_complex \
  "[1:v]scale=iw:ih[p];[0:v][p]overlay=0:0:enable='eq(n,0)'[v]" \
  -map "[v]" -map "0:a?" -c:v libx264 -crf ${CRF:-19} -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart "$TMP"
D1=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
D2=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP")
python3 -c "import sys; sys.exit(0 if abs($D1-$D2)<0.05 else 1)" || { echo "ERROR: la duración cambió ($D1 -> $D2); no reemplazo"; rm -f "$TMP"; exit 1; }
mv "$TMP" "$OUT"
echo "▸ miniatura: $JPG (t=${T}s) · horneada como frame 0 de $OUT"
