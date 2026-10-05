#!/usr/bin/env python3
"""Mezcla SFX sobre un render (en post). La voz del vídeo se mantiene; los SFX
se superponen en los tiempos indicados. Aplica un limitador para no saturar.

Uso:
  mix-sfx.py --base render.mp4 --sfx-dir sfx --out final.mp4 \
    --events '[["boom",0.0],["whoosh",6.5],["ding",8.6], ...]'

events: lista JSON de [nombre_sfx, tiempo_segundos] o [nombre_sfx, tiempo, volumen]. nombre = <nombre>.wav en sfx-dir.
Volúmenes por defecto pensados como acentos bajo la voz; ajusta con --vol si hace falta.
Si re-cortas/re-sincronizas el vídeo, RE-TEMPORIZA los eventos (sus tiempos cambian).
"""
import argparse, json, subprocess, os, sys

DEFAULT_VOL = {"whoosh":0.32,"pop":0.28,"type":0.26,"buzz":0.30,"boom":0.42,"ding":0.36,"riser":0.30}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--sfx-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--events", required=True, help='JSON: [["sfx",t],...]')
    ap.add_argument("--vol", default="{}", help='JSON override de volúmenes por sfx')
    args = ap.parse_args()

    events = json.loads(args.events)
    vol = dict(DEFAULT_VOL); vol.update(json.loads(args.vol))

    inputs = ["-i", args.base]
    fc, labels = [], ["[0:a]"]
    k = 0
    for ev in events:                      # [nombre, t] o [nombre, t, volumen] (volumen por evento)
        name, t = ev[0], ev[1]
        path = os.path.join(args.sfx_dir, f"{name}.wav")
        if not os.path.exists(path):
            print(f"WARN: no existe {path}, saltando", file=sys.stderr); continue
        k += 1                             # índice de entrada REAL (no se desalinea si falta un sfx)
        inputs += ["-i", path]
        ms = int(float(t) * 1000)
        v = ev[2] if len(ev) > 2 else vol.get(name, 0.3)
        fc.append(f"[{k}:a]adelay={ms}|{ms},volume={v}[s{k}]")
        labels.append(f"[s{k}]")
    n = len(labels)
    fc.append("".join(labels) + f"amix=inputs={n}:normalize=0:dropout_transition=0,alimiter=limit=0.97[a]")
    cmd = ["ffmpeg","-y",*inputs,"-filter_complex",";".join(fc),
           "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",args.out,"-loglevel","error"]
    subprocess.run(cmd, check=True)
    print("OK ->", args.out)

if __name__ == "__main__":
    main()
