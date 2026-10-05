#!/bin/bash
# mux-master.sh — une el vídeo con la mezcla de audio y la masteriza a loudness de redes (2 pasadas).
# Sacado del film de Staynex (2026-10-02). El vídeo se copia tal cual (sin re-encode).
#
# Uso: bash mux-master.sh <video.mp4> <mix.wav> <salida.mp4> [LUFS=-14] [TP=-1.0]
#   -14 LUFS / -1 dBTP = lo que normalizan Instagram, TikTok, YouTube y LinkedIn.
set -e
V=$1; A=$2; OUT=$3; I=${4:--14}; TP=${5:--1.0}
[ -f "$V" ] && [ -f "$A" ] && [ -n "$OUT" ] || { echo "uso: mux-master.sh <video.mp4> <mix.wav> <salida.mp4> [LUFS] [TP]"; exit 1; }
TMP="${OUT%.*}.master-tmp.wav"
J=$(ffmpeg -hide_banner -i "$A" -af loudnorm=I=$I:TP=$TP:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
gi(){ echo "$J" | python3 -c "import sys,json; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i "$A" -af "loudnorm=I=$I:TP=$TP:LRA=11:measured_I=$(gi input_i):measured_TP=$(gi input_tp):measured_LRA=$(gi input_lra):measured_thresh=$(gi input_thresh):offset=$(gi target_offset):linear=true,aresample=48000" -c:a pcm_s24le "$TMP"
ffmpeg -hide_banner -loglevel error -y -i "$V" -i "$TMP" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT"
rm -f "$TMP"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E " I:| Peak:" | tail -2
echo "▸ máster -> $OUT"
