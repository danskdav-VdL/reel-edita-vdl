#!/usr/bin/env bash
# transcribe-groq.sh — Transcripción word-level con Groq Whisper.
# Uso:  transcribe-groq.sh <audio_in> <json_out> [idioma]
# Salida JSON: { "text": "...", "words": [{"word","start","end"}], "segments": [...] }
#   (formato que esperan islands.py / verify-cut.py / detect-repeats.py)
#
# Requiere GROQ_API_KEY. Se busca en el entorno o en un .env.local subiendo desde el cwd.
set -euo pipefail

IN="${1:?uso: transcribe-groq.sh <audio_in> <json_out> [idioma]}"
OUT="${2:?falta ruta de salida JSON}"
LANG="${3:-es}"
MODEL="${GROQ_STT_MODEL:-whisper-large-v3-turbo}"

# --- localizar GROQ_API_KEY ---
if [ -z "${GROQ_API_KEY:-}" ]; then
  dir="$(pwd)"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/.env.local" ] && grep -q '^GROQ_API_KEY=' "$dir/.env.local"; then
      GROQ_API_KEY="$(grep '^GROQ_API_KEY=' "$dir/.env.local" | head -1 | cut -d= -f2-)"
      break
    fi
    dir="$(dirname "$dir")"
  done
fi
if [ -z "${GROQ_API_KEY:-}" ]; then
  echo "ERROR: no encuentro GROQ_API_KEY (ni en entorno ni en .env.local)." >&2
  exit 2
fi

if [ ! -f "$IN" ]; then echo "ERROR: no existe el audio: $IN" >&2; exit 2; fi

# Aviso de tamaño (límite Groq ~25MB). Para reels de 1-3 min el m4a a 64k pesa <2MB.
SIZE=$(wc -c < "$IN")
if [ "$SIZE" -gt 24000000 ]; then
  echo "AVISO: $IN pesa >24MB; Groq puede rechazarlo. Trocea con 'ffmpeg -f segment' y concatena los JSON." >&2
fi

mkdir -p "$(dirname "$OUT")"

HTTP=$(curl -s -w '%{http_code}' -o "$OUT.raw" \
  https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@${IN}" \
  -F "model=${MODEL}" \
  -F "language=${LANG}" \
  -F "response_format=verbose_json" \
  -F "timestamp_granularities[]=word" \
  -F "timestamp_granularities[]=segment")

if [ "$HTTP" != "200" ]; then
  echo "ERROR: Groq devolvió HTTP $HTTP" >&2
  head -c 500 "$OUT.raw" >&2; echo >&2
  rm -f "$OUT.raw"; exit 1
fi

# Normaliza a { text, words:[{word,start,end}], segments } por si el esquema varía.
python3 - "$OUT.raw" "$OUT" <<'PY'
import json, sys
raw, out = sys.argv[1], sys.argv[2]
d = json.load(open(raw))
words = []
for w in d.get("words", []):
    words.append({"word": w.get("word",""), "start": w.get("start"), "end": w.get("end")})
res = {"text": d.get("text",""), "words": words, "segments": d.get("segments", [])}
json.dump(res, open(out,"w"), ensure_ascii=False, indent=2)
print(f"OK: {len(words)} palabras, {len(res['segments'])} segmentos -> {out}")
PY
rm -f "$OUT.raw"
