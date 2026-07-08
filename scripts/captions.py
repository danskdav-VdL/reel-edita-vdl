#!/usr/bin/env python3
"""Genera 'beats' de subtitulo a partir de un transcript word-level (Groq/Whisper).
Estilo retencion: 2-3 palabras por beat, sincronizadas a la voz, con una palabra-clave
resaltada. Salida JSON: [{start, end, words:[{w, hi}]}].

Uso: captions.py --transcript corte-final.json [--max-words 3] [--out captions.json]
     [--keywords "palabra1,palabra2,..."] [--windows "2.4-6.1,34-38"]

El resaltado: si una palabra esta en la lista de --keywords, se marca hi=true (se pinta
en tu COLOR DE ACENTO en la composicion). Si no hay match, se resalta la palabra mas larga
del beat. NO hay lista de keywords fija: pasa las TUYAS por --keywords segun el contenido
de cada video (cifras, nombres de marca, conceptos potentes). Esto es lo que evita que los
subtitulos salgan iguales a los de nadie.
"""
import json, re, argparse

def norm(w): return re.sub(r"[^a-zA-Z0-9à-ÿ.]", "", w.lower())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--max-words", type=int, default=3)
    ap.add_argument("--out", default="captions.json")
    ap.add_argument("--keywords", default="",
                    help="palabras a resaltar (en TU color de acento), separadas por coma")
    ap.add_argument("--windows", default="",
                    help="solo beats dentro de estas ventanas (a camara), ej '2.4-6.1,34-38'")
    a = ap.parse_args()
    wins = []
    for seg in a.windows.split(","):
        seg = seg.strip()
        if "-" in seg:
            lo, hi = seg.split("-"); wins.append((float(lo), float(hi)))
    kw = set(k.strip().lower() for k in a.keywords.split(",") if k.strip())

    words = [w for w in json.load(open(a.transcript)).get("words", []) if w.get("start") is not None]
    beats = []
    i = 0
    while i < len(words):
        chunk = words[i:i+a.max_words]
        # romper el beat si una palabra acaba en signo fuerte (. ? !)
        cut = len(chunk)
        for j, w in enumerate(chunk):
            if re.search(r"[.?!]$", w["word"].strip()):
                cut = j+1; break
        chunk = chunk[:cut]
        start = chunk[0]["start"]
        end = chunk[-1].get("end", chunk[-1]["start"]+0.3)
        # elegir keyword: primera que este en kw, si no la mas larga del beat
        hi_idx = -1
        for j, w in enumerate(chunk):
            if norm(w["word"]) in kw: hi_idx = j; break
        if hi_idx == -1:
            hi_idx = max(range(len(chunk)), key=lambda j: len(norm(chunk[j]["word"])))
        ws = [{"w": w["word"].strip(), "hi": (j == hi_idx)} for j, w in enumerate(chunk)]
        mid = (start+end)/2
        if not wins or any(lo <= mid <= hi for lo, hi in wins):
            beats.append({"start": round(start, 2), "end": round(end, 2), "words": ws})
        i += cut

    json.dump(beats, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"{len(beats)} beats -> {a.out}")
    for b in beats[:6]:
        print(f"  {b['start']:5.2f}-{b['end']:5.2f}  " +
              " ".join(("*"+x["w"]+"*" if x["hi"] else x["w"]) for x in b["words"]))
    print("  ...")

if __name__ == "__main__":
    main()
