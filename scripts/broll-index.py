#!/usr/bin/env python3
"""broll-index.py — indexa el banco de B-roll (carpeta broll/) en broll/index.json.

Lee cada clip/foto, saca categoría y etiquetas del NOMBRE del archivo
(<categoria>_<que-se-ve-con-guiones>_<nn>.<ext>) y, para vídeos, duración, resolución, fps y
orientación con ffprobe. La skill usa el índice para elegir el clip que encaja con cada tramo.

Uso: python3 broll-index.py [--dir <ruta/al/banco>]   (o variable BROLL_DIR; por defecto ./broll)
Solo lee los archivos; nunca los modifica.
"""
import argparse, json, os, subprocess, sys
from datetime import date

VID = {".mp4", ".mov", ".m4v"}
IMG = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
# Productos/clientes que se detectan en el nombre del archivo (p. ej. {"albaran-digital"}).
# Vacío = no se rastrea nada.
VARIEDADES = set()


def probe(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration",
                              "-of", "json", path], capture_output=True, text=True, check=True).stdout
        d = json.loads(out)
        s = d["streams"][0]
        w, h = s.get("width"), s.get("height")
        rot = 0
        for sd in s.get("side_data_list", []) or []:
            rot = int(sd.get("rotation", 0) or 0)
        if abs(rot) == 90:
            w, h = h, w
        n, _, den = s.get("r_frame_rate", "0/1").partition("/")
        fps = round(float(n) / float(den or 1), 2) if float(den or 1) else None
        return {"duracion_s": round(float(d["format"]["duration"]), 2), "w": w, "h": h, "fps": fps,
                "orientacion": "vertical" if (h or 0) > (w or 0) else "horizontal"}
    except Exception as e:
        return {"error_probe": str(e)[:120]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.environ.get("BROLL_DIR", os.path.join(os.getcwd(), "broll")))
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        sys.exit(f"No existe {a.dir}")
    items, avisos = [], []
    for root, dirs, files in os.walk(a.dir):
        dirs[:] = [x for x in dirs if not x.startswith('_')]  # _candidatos = búsquedas sin aprobar
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext not in VID | IMG or f.startswith("_"):  # _vista-banco.jpg y similares
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, a.dir)
            base = os.path.splitext(f)[0]
            parts = base.split("_")
            cat = os.path.basename(root)
            if len(parts) < 2:
                avisos.append(f"{rel}: nombre sin formato <categoria>_<descripcion>_<nn>")
            desc = parts[1] if len(parts) >= 2 else base
            tags = [t for t in desc.lower().split("-") if t]
            it = {"archivo": rel, "tipo": "video" if ext in VID else "foto", "categoria": cat,
                  "descripcion": desc.replace("-", " "), "tags": tags,
                  "producto": next((v for v in VARIEDADES if v in desc.lower()), None),
                  "origen": "stock" if "_stk-" in base else "propio", "usado_en": []}
            ficha = os.path.splitext(full)[0] + ".json"
            if os.path.exists(ficha):
                try:
                    fj = json.load(open(ficha))
                    it.update({"fuente": fj.get("fuente"), "credito": fj.get("credito"), "pagina": fj.get("pagina")})
                except Exception:
                    pass
            if ext in VID:
                it.update(probe(full))
                if it.get("orientacion") == "horizontal":
                    avisos.append(f"{rel}: es horizontal (en un reel vertical habrá que recortar)")
            items.append(it)
    idx_path = os.path.join(a.dir, "index.json")
    # conserva el historial de uso de un índice anterior
    if os.path.exists(idx_path):
        try:
            prev = {i["archivo"]: i.get("usado_en", []) for i in json.load(open(idx_path))["items"]}
            for it in items:
                it["usado_en"] = prev.get(it["archivo"], [])
        except Exception:
            pass
    json.dump({"actualizado": date.today().isoformat(), "total": len(items), "items": items},
              open(idx_path, "w"), ensure_ascii=False, indent=2)
    por_cat = {}
    print(f"  propio: {sum(i['origen']=='propio' for i in items)} · stock: {sum(i['origen']=='stock' for i in items)}")
    for it in items:
        por_cat[it["categoria"]] = por_cat.get(it["categoria"], 0) + 1
    print(f"índice -> {idx_path} · {len(items)} archivos")
    for c, n in sorted(por_cat.items()):
        print(f"  {c}: {n}")
    for w in avisos:
        print("  ⚠️", w)


if __name__ == "__main__":
    main()
