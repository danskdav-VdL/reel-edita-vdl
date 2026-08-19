#!/bin/bash
# cierre.sh — pega la CORTINILLA OFICIAL de VdL al final del reel con disolucion cruzada.
#
# El cierre de marca de TODOS los reels de VdL es esta cortinilla. No se disena un endcard
# a mano, no se usa el isotipo suelto: el reel termina SIEMPRE con ella.
#
# Uso:
#   bash ~/.claude/skills/reel-edita-vdl/scripts/cierre.sh <reel.mp4> <salida.mp4> [xfade] [cortinilla.mp4]
#
#   reel.mp4    reel ya montado (cold open + cuerpo, con SFX mezclados)
#   salida.mp4  entregable final
#   xfade       duracion de la disolucion en segundos (default 0.5)
#   cortinilla  opcional: para usar otra cortinilla en vez de la oficial
#
# Hace todo el trabajo: resuelve la cortinilla oficial, la normaliza a la resolucion/fps del
# reel, le pone pista de audio (viene MUDA) + SFX suaves, y une con xfade + acrossfade.
#
# IMPORTANTE: la voz debe terminar ANTES de que empiece la disolucion. El script lo comprueba
# y avisa si la disolucion se comeria una palabra.
set -e

REEL=$1
OUT=$2
XF=${3:-0.5}
CORT_IN=$4

[ -n "$REEL" ] && [ -n "$OUT" ] || { echo "uso: cierre.sh <reel.mp4> <salida.mp4> [xfade] [cortinilla.mp4]"; exit 1; }
[ -f "$REEL" ] || { echo "no existe el reel: $REEL"; exit 1; }

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORT_NAME="cortinilla_compartiendo valor.mp4"

# Donde vive la cortinilla oficial. Se puede forzar con  export VDL_CIERRE_DIR=/ruta
CIERRE_DIR="${VDL_CIERRE_DIR:-}"
if [ -z "$CIERRE_DIR" ]; then
  for d in "/Users/diseno/Documents/Claude AI/recursos/Cierres reels" \
           "$HOME/Documents/Claude AI/recursos/Cierres reels" \
           "recursos/Cierres reels" "../recursos/Cierres reels" "../../recursos/Cierres reels" \
           "../../../recursos/Cierres reels" "../../../../recursos/Cierres reels"; do
    [ -d "$d" ] && CIERRE_DIR="$d" && break
  done
fi
OFICIAL="$CIERRE_DIR/$CORT_NAME"

# ---------------------------------------------------------------- resolver cortinilla
if [ -n "$CORT_IN" ]; then
  CORT="$CORT_IN"
  echo "▸ cortinilla (indicada a mano): $(basename "$CORT")"
elif [ -f "$OFICIAL" ]; then
  CORT="$OFICIAL"
  echo "▸ cortinilla OFICIAL de VdL: $(basename "$CORT")"
else
  # fallback: unico mp4 en la carpeta de cierres
  N=0
  [ -n "$CIERRE_DIR" ] && N=$(find "$CIERRE_DIR" -maxdepth 1 -name "*.mp4" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$N" = "1" ]; then
    CORT=$(find "$CIERRE_DIR" -maxdepth 1 -name "*.mp4")
    echo "▸ cortinilla encontrada: $(basename "$CORT")"
  else
    echo "ERROR: no encuentro la cortinilla oficial de cierre."
    echo "  buscaba: <recursos/Cierres reels>/$CORT_NAME"
    [ -n "$CIERRE_DIR" ] && echo "  carpeta detectada: $CIERRE_DIR ($N archivos .mp4)"
    [ "$N" != "0" ] && [ "$N" != "1" ] && echo "  hay varias: PREGUNTA a VdL cual es la buena (no elijas tu)."
    echo "  arregla la ruta con:  export VDL_CIERRE_DIR=\"/ruta/a/Cierres reels\""
    echo "  o pasala a mano:      cierre.sh <reel> <salida> $XF <cortinilla.mp4>"
    exit 1
  fi
fi

TMP=$(dirname "$OUT")
mkdir -p "$TMP"

# ---------------------------------------------------------------- geometria del reel
RW=$(ffprobe -v error -select_streams v:0 -show_entries stream=width  -of csv=p=0 "$REEL")
RH=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$REEL")
RFPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$REEL" | awk -F/ '{printf "%d", ($2?$1/$2:$1)}')
RD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$REEL")
CD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CORT")

echo "  reel ${RW}x${RH} @${RFPS}fps · ${RD}s   cortinilla ${CD}s"

# ---------------------------------------------------------------- normalizar cortinilla
# La cortinilla oficial viene a 60fps y SIN pista de audio -> hay que igualarla al reel
# y darle audio, o el concat/xfade falla o descuadra.
NORM="$TMP/_cort_norm.mp4"
ffmpeg -y -v error -i "$CORT" -f lavfi -t "$CD" -i anullsrc=r=48000:cl=stereo \
  -map 0:v -map 1:a \
  -vf "fps=${RFPS},scale=${RW}:${RH}:flags=lanczos,setsar=1" \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k "$NORM"

# SFX suaves: whoosh en el barrido lime + ding al asentar el logotipo.
# (El reel no lleva musica, asi que el cierre queda limpio.)
SFXDIR=""
for d in "$(dirname "$REEL")/../sfx" "$(dirname "$REEL")/sfx" "motion/sfx"; do
  [ -d "$d" ] && SFXDIR="$d" && break
done
CORTF="$NORM"
if [ -n "$SFXDIR" ] && [ -f "$SFXDIR/whoosh.wav" ]; then
  ffmpeg -y -v error -i "$NORM" -f lavfi -t "$CD" -i anullsrc=r=48000:cl=stereo -map 0:v -map 0:a -c copy "$TMP/_cort_a.mp4" 2>/dev/null || cp "$NORM" "$TMP/_cort_a.mp4"
  python3 "$SKILL_DIR/scripts/mix-sfx.py" --base "$NORM" --sfx-dir "$SFXDIR" \
    --out "$TMP/_cort_sfx.mp4" --events '[["whoosh",0.02],["ding",0.62]]' \
    --vol '{"whoosh":0.22,"ding":0.14}' >/dev/null 2>&1 && CORTF="$TMP/_cort_sfx.mp4" \
    && echo "  SFX de cierre: whoosh (barrido) + ding (logotipo)"
fi

# ---------------------------------------------------------------- comprobar que no corta voz
OFF=$(python3 -c "print(round($RD-$XF,3))")
TOT=$(python3 -c "print(round($RD+$CD-$XF,3))")
# ultimo tramo con voz: si hay habla despues del inicio de la disolucion, avisar
VOZ=$(ffmpeg -hide_banner -nostats -i "$REEL" -af "silencedetect=noise=-34dB:d=0.25" -f null - 2>&1 \
      | grep -oE "silence_start: [0-9.]+" | tail -1 | grep -oE "[0-9.]+" || echo "0")
if [ -n "$VOZ" ] && [ "$(python3 -c "print(float('$VOZ') > $OFF)")" = "True" ]; then
  echo "  ⚠️  OJO: parece haber voz hasta ${VOZ}s y la disolucion empieza en ${OFF}s."
  echo "      Baja el xfade o deja mas cola de silencio en el corte."
fi

echo "▸ disolucion de ${XF}s en t=${OFF}s -> total ${TOT}s"
ffmpeg -y -v error -i "$REEL" -i "$CORTF" -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=$XF:offset=$OFF[v];\
   [0:a][1:a]acrossfade=d=$XF:c1=tri:c2=tri[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"

rm -f "$TMP/_cort_norm.mp4" "$TMP/_cort_a.mp4" "$TMP/_cort_sfx.mp4"
echo "▸ CIERRE UNIDO -> $OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
