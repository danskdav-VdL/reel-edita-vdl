#!/usr/bin/env python3
"""stock-search.py — busca y descarga B-roll de stock (Pixabay, Unsplash, Pexels) para el banco de B-roll.

Banco: variable BROLL_DIR (por defecto ./broll). Claves en .env.local (se busca hacia arriba desde el cwd).
Pexels: emisión de claves nuevas PAUSADA (09/2026); el script la usa si ya tienes una.

Dos pasos, para que SIEMPRE haya una revisión visual antes de meter nada en el banco:

  1) buscar  -> baja miniaturas y monta una HOJA DE CONTACTO numerada para revisarla (con Read)
     python3 stock-search.py buscar "coffee pouring slow motion" --tipo video --fuentes pexels,pixabay --n 12
  2) bajar   -> descarga en calidad completa los números elegidos al banco, con nombre y ficha de créditos
     python3 stock-search.py bajar --busqueda coffee-pouring-slow-motion --elegidos 3,7 \
         --categoria 04-cafe --desc cafe-vertido-taza

Claves (gratis) en .env.local:  PEXELS_API_KEY · PIXABAY_API_KEY · UNSPLASH_ACCESS_KEY
Solo se usan las fuentes con clave. Unsplash solo tiene fotos.

Licencias: Pexels, Pixabay y Unsplash permiten uso comercial gratis y sin atribución obligatoria.
Aun así se guarda una ficha .json con autor y URL al lado de cada archivo (créditos opcionales y
trazabilidad). Unsplash exige avisar de cada descarga a su API: el script lo hace.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

BANCO = os.environ.get("BROLL_DIR", os.path.join(os.getcwd(), "broll"))
CAND = os.path.join(BANCO, "_candidatos")
UA = {"User-Agent": "reel-edita-broll/1.0"}


# ------------------------------------------------------------------ util
def load_env():
    paths, d = [], os.getcwd()
    while True:
        paths.append(os.path.join(d, ".env.local"))
        if os.path.dirname(d) == d:
            break
        d = os.path.dirname(d)
    for p in paths:
        if os.path.exists(p):
            for line in open(p):
                m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$", line)
                if m and m.group(1) not in os.environ:
                    os.environ[m.group(1)] = m.group(2).strip().strip('"').strip("'")


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def download(url, path, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        while True:
            b = r.read(1 << 16)
            if not b:
                break
            f.write(b)


def slug(s):
    s = s.lower()
    for a, b in zip("áéíóúñü", "aeiounu"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


# ------------------------------------------------------------------ proveedores -> formato común
# cada candidato: {fuente, id, tipo, thumb, full, w, h, dur, fps, autor, autor_url, pagina, licencia, extra}

def pexels(q, tipo, n, vertical):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return []
    h = {"Authorization": key}
    o = "&orientation=portrait" if vertical else ""
    out = []
    if tipo == "video":
        d = get_json(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page={n}{o}", h)
        for v in d.get("videos", []):
            files = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("height")]
            if not files:
                continue
            # la mejor versión que no pase de ~2160 de alto
            best = max((f for f in files if f["height"] <= 2200), key=lambda f: f["height"], default=files[0])
            out.append(dict(fuente="pexels", id=str(v["id"]), tipo="video", thumb=v.get("image"), full=best["link"],
                            w=best.get("width"), h=best.get("height"), dur=v.get("duration"), fps=best.get("fps"),
                            autor=v.get("user", {}).get("name"), autor_url=v.get("user", {}).get("url"),
                            pagina=v.get("url"), licencia="Pexels License (uso comercial, sin atribución obligatoria)"))
    else:
        d = get_json(f"https://api.pexels.com/v1/search?query={urllib.parse.quote(q)}&per_page={n}{o}", h)
        for p in d.get("photos", []):
            out.append(dict(fuente="pexels", id=str(p["id"]), tipo="foto", thumb=p["src"].get("medium"),
                            full=p["src"].get("original"), w=p.get("width"), h=p.get("height"),
                            autor=p.get("photographer"), autor_url=p.get("photographer_url"), pagina=p.get("url"),
                            licencia="Pexels License (uso comercial, sin atribución obligatoria)"))
    return out


def pixabay(q, tipo, n, vertical):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return []
    n = max(3, min(n, 200))
    out = []
    if tipo == "video":
        d = get_json(f"https://pixabay.com/api/videos/?key={key}&q={urllib.parse.quote(q)}&per_page={n}&safesearch=true")
        for v in d.get("hits", []):
            vs = v.get("videos", {})
            best = next((vs[k] for k in ("large", "medium", "small") if vs.get(k, {}).get("url")), None)
            if not best:
                continue
            out.append(dict(fuente="pixabay", id=str(v["id"]), tipo="video", thumb=best.get("thumbnail"),
                            full=best["url"], w=best.get("width"), h=best.get("height"), dur=v.get("duration"),
                            autor=v.get("user"), autor_url=f"https://pixabay.com/users/{v.get('user')}-{v.get('user_id')}/",
                            pagina=v.get("pageURL"), licencia="Pixabay Content License (uso comercial, sin atribución)"))
    else:
        o = "&orientation=vertical" if vertical else ""
        d = get_json(f"https://pixabay.com/api/?key={key}&q={urllib.parse.quote(q)}&image_type=photo&per_page={n}&safesearch=true{o}")
        for p in d.get("hits", []):
            out.append(dict(fuente="pixabay", id=str(p["id"]), tipo="foto", thumb=p.get("webformatURL"),
                            full=p.get("largeImageURL"), w=p.get("imageWidth"), h=p.get("imageHeight"),
                            autor=p.get("user"), autor_url=f"https://pixabay.com/users/{p.get('user')}-{p.get('user_id')}/",
                            pagina=p.get("pageURL"), licencia="Pixabay Content License (uso comercial, sin atribución)"))
    return out


def unsplash(q, tipo, n, vertical):
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key or tipo != "foto":
        return []
    o = "&orientation=portrait" if vertical else ""
    d = get_json(f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(q)}&per_page={min(n,30)}{o}",
                 {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"})
    out = []
    for p in d.get("results", []):
        out.append(dict(fuente="unsplash", id=p["id"], tipo="foto", thumb=p["urls"].get("small"),
                        full=p["urls"].get("full"), w=p.get("width"), h=p.get("height"),
                        autor=p.get("user", {}).get("name"), autor_url=p.get("user", {}).get("links", {}).get("html"),
                        pagina=p.get("links", {}).get("html"),
                        licencia="Unsplash License (uso comercial, sin atribución obligatoria; se agradece el crédito)",
                        extra={"download_location": p.get("links", {}).get("download_location")}))
    return out


PROV = {"pexels": pexels, "pixabay": pixabay, "unsplash": unsplash}


# ------------------------------------------------------------------ comandos
def cmd_buscar(a):
    fuentes = [f.strip() for f in a.fuentes.split(",")]
    faltan = [f for f in fuentes if not os.environ.get({"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY",
                                                           "unsplash": "UNSPLASH_ACCESS_KEY"}[f])]
    if len(faltan) == len(fuentes):
        sys.exit("No hay ninguna clave de stock en .env.local (PEXELS_API_KEY / PIXABAY_API_KEY / UNSPLASH_ACCESS_KEY).")
    for f in faltan:
        print(f"  (sin clave para {f}: se omite)")
    cands = []
    for f in fuentes:
        if f in faltan:
            continue
        try:
            cands += PROV[f](a.query, a.tipo, a.n, not a.horizontal)
        except Exception as e:
            print(f"  ⚠️ {f}: {e}")
    if not cands:
        sys.exit("Sin resultados. Prueba otra búsqueda (en inglés suele dar más).")
    for c in cands:
        c["orient"] = "V" if (c.get("h") or 0) > (c.get("w") or 0) else "H"
    # Pixabay casi no tiene vídeo vertical: se muestran también los horizontales (se recortan a 9:16 con
    # grade-look.sh --vertical), pero los verticales van primero.
    cands.sort(key=lambda c: 0 if c["orient"] == "V" or a.horizontal else 1)
    d = os.path.join(CAND, slug(a.query))
    os.makedirs(d, exist_ok=True)
    for i, c in enumerate(cands, 1):
        c["n"] = i
        try:
            download(c["thumb"], os.path.join(d, f"{i:02d}.jpg"))
        except Exception as e:
            c["thumb_error"] = str(e)[:80]
    json.dump({"query": a.query, "tipo": a.tipo, "candidatos": cands}, open(os.path.join(d, "candidatos.json"), "w"),
              ensure_ascii=False, indent=2)
    hoja = contact_sheet(d, cands)
    print(f"{len(cands)} candidatos · hoja de contacto: {hoja}")
    for c in cands:
        extra = f"{c.get('dur')}s {c.get('fps') or ''}fps" if c["tipo"] == "video" else ""
        print(f"  #{c['n']:02d} {c['orient']} {c['fuente']:<8} {c.get('w')}x{c.get('h')} {extra} · {c.get('autor')}")
    print(f"\nSiguiente: bajar --busqueda {slug(a.query)} --elegidos 1,4 --categoria <cat> --desc <que-se-ve>")


def contact_sheet(d, cands):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return "(sin PIL: revisa las miniaturas sueltas en la carpeta)"
    horiz = sum(1 for c in cands if c.get("orient") == "H") > len(cands) / 2
    W, H, cols = (480, 270, 4) if horiz else (270, 480, 6)
    rows = (len(cands) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W, rows * (H + 34)), (0, 0, 75))
    dr = ImageDraw.Draw(sheet)
    try:
        font = next(ImageFont.truetype(p, 20) for p in ("/System/Library/Fonts/Menlo.ttc",
                    "C:/Windows/Fonts/consola.ttf", "DejaVuSansMono.ttf") if os.path.exists(p) or not p.startswith(("/", "C:")))
    except Exception:
        font = ImageFont.load_default()
    for i, c in enumerate(cands):
        x, y = (i % cols) * W, (i // cols) * (H + 34)
        p = os.path.join(d, f"{c['n']:02d}.jpg")
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((W, H))
            sheet.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
        lab = f"#{c['n']:02d} {c['orient']} {c['fuente'][:3]}"
        if c["tipo"] == "video":
            lab += f" {c.get('dur')}s"
        dr.text((x + 6, y + H + 6), lab, fill=(170, 224, 90), font=font)
    out = os.path.join(d, "hoja.jpg")
    sheet.save(out, quality=85)
    return out


def cmd_bajar(a):
    d = os.path.join(CAND, a.busqueda)
    meta = json.load(open(os.path.join(d, "candidatos.json")))
    elegidos = [int(x) for x in a.elegidos.split(",")]
    dest = os.path.join(BANCO, a.categoria)
    os.makedirs(dest, exist_ok=True)
    for k, n in enumerate(elegidos, 1):
        c = next(c for c in meta["candidatos"] if c["n"] == n)
        ext = ".mp4" if c["tipo"] == "video" else (".jpg" if c["fuente"] != "pixabay" else os.path.splitext(c["full"].split("?")[0])[1] or ".jpg")
        desc = slug(a.desc) + (f"-{k}" if len(elegidos) > 1 else "")
        name = f"{a.categoria}_{desc}_stk-{c['fuente']}-{c['id']}{ext}"
        path = os.path.join(dest, name)
        full = c["full"]
        if c["fuente"] == "unsplash":
            full += ("&" if "?" in full else "?") + "w=2400&q=85"
            dl = c.get("extra", {}).get("download_location")
            if dl:  # requisito de la API de Unsplash: registrar la descarga
                try:
                    get_json(dl, {"Authorization": f"Client-ID {os.environ['UNSPLASH_ACCESS_KEY']}"})
                except Exception:
                    pass
        download(full, path)
        ficha = {k2: c.get(k2) for k2 in ("fuente", "id", "tipo", "w", "h", "dur", "fps", "autor", "autor_url", "pagina", "licencia")}
        ficha["busqueda"] = meta["query"]
        ficha["credito"] = f"{'Vídeo' if c['tipo']=='video' else 'Foto'}: {c.get('autor')} / {c['fuente'].capitalize()}"
        json.dump(ficha, open(os.path.splitext(path)[0] + ".json", "w"), ensure_ascii=False, indent=2)
        print("  ✓", os.path.relpath(path, BANCO))
    print("Hecho. Actualiza el índice: python3 scripts/broll-index.py")


def main():
    load_env()
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("buscar")
    b.add_argument("query")
    b.add_argument("--tipo", choices=["video", "foto"], default="video")
    b.add_argument("--fuentes", default="pixabay,unsplash,pexels")  # pexels: claves nuevas pausadas (09/2026)
    b.add_argument("--n", type=int, default=12, help="resultados por fuente")
    b.add_argument("--horizontal", action="store_true", help="no filtrar a vertical")
    d = sp.add_parser("bajar")
    d.add_argument("--busqueda", required=True)
    d.add_argument("--elegidos", required=True)
    d.add_argument("--categoria", required=True)
    d.add_argument("--desc", required=True)
    a = ap.parse_args()
    cmd_buscar(a) if a.cmd == "buscar" else cmd_bajar(a)


if __name__ == "__main__":
    main()
