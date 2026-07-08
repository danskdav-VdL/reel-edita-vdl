#!/usr/bin/env python3
"""FASE 1 (paso 1) — Detecta los ISLOTES de voz del bruto con silencedetect (ffmpeg,
energía de audio: límites EXACTOS, no los timestamps jitter de Whisper) y propone qué
islote conservar quedándose con la ÚLTIMA toma de cada frase.

Por qué: los brutos suelen tener cada frase regrabada 2-4 veces + falsos arranques +
bloopers + pausas internas de 5-9s. Cortar por timestamps de Whisper deja silencios y
repeticiones. Cortar pegado a los islotes elimina las pausas; quedarse con la última toma
elimina las repeticiones.

Uso:
  islands.py --media bruto.mp4 --transcript word.json [--noise -30dB] [--d 0.35]
             [--min-island 0.25] [--pad-in 0.04] [--pad-out 0.09] [--out islands.json]

Salida:
  - Tabla legible: cada islote con t, texto, KEEP/DROP propuesto y motivo.
  - JSON (islands.json): lista de islotes con campo "keep" (bool) y rangos ya con padding.

Flujo: revisa la tabla, corrige los "keep" en el JSON si hace falta (bloopers/tangentes que
la heurística no pilla), y pásalo a cut.py. SIEMPRE verifica el resultado con verify-cut.py.
"""
import json, re, sys, subprocess, argparse
from difflib import SequenceMatcher

def norm_tokens(t):
    t = t.lower()
    t = re.sub(r"[^a-záéíóúñü0-9 ]", " ", t)
    return [w for w in t.split() if len(w) > 1]

def silences(media, noise, d):
    out = subprocess.run(
        ["ffmpeg","-hide_banner","-nostats","-i",media,
         "-af",f"silencedetect=noise={noise}:d={d}","-f","null","-"],
        capture_output=True, text=True).stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", out)]
    ends   = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", out)]
    return starts, ends

def duration(media):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",media], capture_output=True, text=True).stdout.strip()
    return float(r)

def build_islands(media, noise, d, min_island):
    starts, ends = silences(media, noise, d)
    dur = duration(media)
    # Islote de voz = hueco entre el fin de un silencio y el inicio del siguiente.
    # Construimos la línea temporal de bordes.
    pts = []
    # punto inicial: si el audio NO empieza en silencio, la voz arranca en 0
    cur = 0.0
    # Mezclar starts/ends en orden
    # Recorremos los silencios en orden de aparición
    sil = sorted(list(zip(starts, ["s"]*len(starts))) + list(zip(ends, ["e"]*len(ends))))
    islands = []
    speech_start = 0.0
    in_speech = True
    # Reconstrucción robusta: alternar usando starts/ends emparejados
    # silencedetect emite start luego end; los emparejamos secuencialmente
    pairs = []
    si = 0
    # Emparejar cada start con el siguiente end >= start
    ei = 0
    s_sorted = sorted(starts); e_sorted = sorted(ends)
    for s in s_sorted:
        # primer end mayor que s
        e_cand = [e for e in e_sorted if e > s]
        if e_cand:
            pairs.append((s, e_cand[0]))
        else:
            pairs.append((s, dur))
    # fusionar solapados
    pairs = sorted(pairs)
    merged = []
    for s,e in pairs:
        if merged and s <= merged[-1][1] + 0.01:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s,e))
    # islotes = complemento de los silencios dentro de [0, dur]
    cur = 0.0
    for s,e in merged:
        if s - cur >= min_island:
            islands.append([round(cur,3), round(s,3)])
        cur = e
    if dur - cur >= min_island:
        islands.append([round(cur,3), round(dur,3)])
    return islands, dur

def text_for(island, words):
    s,e = island
    ws = [w["word"] for w in words if w.get("start") is not None and s-0.15 <= w["start"] <= e+0.05]
    return " ".join(ws).strip()

def is_earlier_take(toks_i, toks_j):
    """¿toks_i es una toma anterior/parcial de toks_j (toma posterior)?"""
    if not toks_i or not toks_j: return False
    set_i, set_j = set(toks_i), set(toks_j)
    contain = len(set_i & set_j) / len(set_i)
    ratio = SequenceMatcher(None, toks_i, toks_j).ratio()
    # i contenido en j (j igual o más completo) o muy parecidos
    if contain >= 0.7 and len(toks_j) >= len(toks_i)*0.75: return True
    if ratio >= 0.6 and len(toks_j) >= len(toks_i): return True
    # prefijo: i es el arranque de j
    if len(toks_i) <= len(toks_j) and toks_j[:len(toks_i)] == toks_i: return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media", required=True)
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--noise", default="-30dB")
    ap.add_argument("--d", type=float, default=0.35)
    ap.add_argument("--min-island", type=float, default=0.25)
    ap.add_argument("--pad-in", type=float, default=0.04)
    ap.add_argument("--pad-out", type=float, default=0.09)
    ap.add_argument("--window", type=int, default=6, help="nº islotes adelante a comparar")
    ap.add_argument("--out", default="islands.json")
    a = ap.parse_args()

    words = json.load(open(a.transcript)).get("words", [])
    islands, dur = build_islands(a.media, a.noise, a.d, a.min_island)
    rows = []
    for isl in islands:
        rows.append({"start": isl[0], "end": isl[1], "dur": round(isl[1]-isl[0],2),
                     "text": text_for(isl, words)})
    toks = [norm_tokens(r["text"]) for r in rows]

    # Heurística última-toma: marcar DROP si existe una toma posterior cercana igual/más completa
    keep = [True]*len(rows)
    reason = [""]*len(rows)
    for i in range(len(rows)):
        for j in range(i+1, min(i+1+a.window, len(rows))):
            if is_earlier_take(toks[i], toks[j]):
                keep[i] = False
                reason[i] = f"toma anterior de #{j} (última toma gana)"
                break
        if keep[i] and len(toks[i]) <= 1 and rows[i]["dur"] < 0.7:
            reason[i] = "FRAGMENTO corto — revisar (¿muletilla/blooper?)"

    print("="*92)
    print(f"ISLOTES DE VOZ: {len(rows)}  ·  bruto {dur:.1f}s  ·  noise={a.noise} d={a.d}s")
    print("="*92)
    kept_dur = 0.0
    for i,r in enumerate(rows):
        tag = "KEEP " if keep[i] else "drop "
        if keep[i]: kept_dur += r["dur"]
        rs = f"  <- {reason[i]}" if reason[i] else ""
        print(f"[{tag}] #{i:02d} {r['start']:7.2f}-{r['end']:7.2f} ({r['dur']:4.1f}s)  {r['text'][:78]}{rs}")
    print("-"*92)
    print(f"PROPUESTA: conservar {sum(keep)} islotes ~{kept_dur:.1f}s")
    print("Revisa los DROP (sobre todo FRAGMENTO/bloopers/tangentes) y ajusta 'keep' en el JSON si hace falta.")

    out = {"media": a.media, "duration": dur, "pad_in": a.pad_in, "pad_out": a.pad_out,
           "islands": [{"i":i, "start":r["start"], "end":r["end"], "dur":r["dur"],
                        "text":r["text"], "keep":keep[i], "reason":reason[i]} for i,r in enumerate(rows)]}
    json.dump(out, open(a.out,"w"), ensure_ascii=False, indent=2)
    print(f"\nJSON -> {a.out}")

if __name__ == "__main__":
    main()
