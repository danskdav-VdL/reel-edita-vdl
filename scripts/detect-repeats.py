#!/usr/bin/env python3
"""detect-repeats.py — Detector de APOYO para decidir DROPs semánticos en el corte.
NO es la compuerta dura (eso es verify-cut.py). Ayuda a leer el bruto y localizar tomas
dobladas, falsos arranques y ecos.

Uso:  detect-repeats.py <transcript.json>
  transcript = { "text", "words":[{"word","start","end"}], "segments":[{"text","start","end"}] }

Imprime:
  1) Segmentos casi-duplicados (near-dup, sim >= --sim, def 0.5) — tomas repetidas obvias.
  2) Trigramas word-level repetidos — repeticiones DENTRO de la frase.
  3) Palabras dragueadas (dur > --drag, def 1.5s) — candidatas a toma doblada/silencio.
"""
import json, re, sys, argparse
from difflib import SequenceMatcher

STOP = {"de","la","el","que","y","a","en","lo","un","una","o","se","es","le","su","del",
        "por","con","los","las","al","ya","si","no","más","mas","tu","mi","me","te","nos",
        "para","como","pero","muy","ha","he","este","esta","eso","esto","ese","esa"}

def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-záéíóúñü0-9 ]", " ", t)
    return [w for w in t.split() if w]

def segments_from(d):
    segs = d.get("segments") or []
    out = []
    for s in segs:
        txt = (s.get("text") or "").strip()
        if txt:
            out.append({"text": txt, "start": s.get("start"), "end": s.get("end")})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--sim", type=float, default=0.5)
    ap.add_argument("--drag", type=float, default=1.5)
    ap.add_argument("--gap", type=int, default=8, help="ventana (segmentos) para buscar near-dups")
    a = ap.parse_args()

    d = json.load(open(a.transcript))
    words = d.get("words", [])
    segs = segments_from(d)

    print("="*80)
    print(f"DETECT-REPEATS · {len(segs)} segmentos · {len(words)} palabras")
    print("="*80)

    # 1) segmentos casi-duplicados (dentro de una ventana cercana)
    print("\n[1] SEGMENTOS CASI-DUPLICADOS (near-dup, sim >= %.2f):" % a.sim)
    found = False
    for i in range(len(segs)):
        ti = norm(segs[i]["text"])
        for j in range(i+1, min(i+1+a.gap, len(segs))):
            tj = norm(segs[j]["text"])
            if not ti or not tj:
                continue
            r = SequenceMatcher(None, ti, tj).ratio()
            if r >= a.sim:
                found = True
                si, sj = segs[i], segs[j]
                print(f"  sim={r:.2f}  #{i}[{si['start']}s] «{si['text'][:60]}»")
                print(f"            #{j}[{sj['start']}s] «{sj['text'][:60]}»  <- suele ganar la ÚLTIMA")
    if not found:
        print("  (ninguno)")

    # 2) trigramas word-level repetidos (contenido, sin stopwords puras)
    print("\n[2] TRIGRAMAS WORD-LEVEL REPETIDOS:")
    wl = [ (w.get("word") or "").lower().strip("¿?¡!,.\"'()") for w in words ]
    wl = [w for w in wl if w]
    tri = {}
    for i in range(len(wl)-2):
        g = tuple(wl[i:i+3])
        if all(t in STOP for t in g):
            continue
        tri.setdefault(g, []).append(i)
    rep = {g:idx for g,idx in tri.items() if len(idx) > 1}
    if rep:
        for g, idx in sorted(rep.items(), key=lambda kv: -len(kv[1])):
            print(f"  x{len(idx)}  «{' '.join(g)}»  (pos {idx[:6]})")
        print("  → Ignora los de contexto distinto a propósito; el resto suelen ser repeticiones reales.")
    else:
        print("  (ninguno)")

    # 3) palabras dragueadas
    print("\n[3] PALABRAS DRAGUEADAS (dur > %.1fs):" % a.drag)
    dragged = False
    for w in words:
        s, e = w.get("start"), w.get("end")
        if s is None or e is None:
            continue
        if (e - s) > a.drag:
            dragged = True
            print(f"  {e-s:.1f}s  [{s:.1f}s]  «{w.get('word','')}»  <- ¿silencio/toma doblada? confirma con silencedetect")
    if not dragged:
        print("  (ninguna)")

if __name__ == "__main__":
    main()
