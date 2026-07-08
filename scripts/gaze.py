#!/usr/bin/env python3
"""gaze.py — Detecta tramos donde el sujeto NO mira a cámara (mira a notas/abajo o gira la cabeza).
Sirve para cubrir esos tramos con visuales full-screen en el montaje (regla VdL: si no mira, no sale).

Método (lo que funcionó — RESPETAR):
  - Proxies 2D estables: posición de la NARIZ respecto a la línea de ojos (cabeceo/pitch y giro/yaw)
    + gaze HORIZONTAL del iris. NO se usan los ángulos de Euler de solvePnP (saltan ±90° = falsos +).
  - Se DESCARTA el gaze vertical del iris (gaze_v): los parpadeos dan outliers enormes.
  - Umbral de "mira abajo": pitch > mediana + ~0.07. Giro: desviación de yaw / gaze_h respecto a la mediana.
  - El detector SUBESTIMA cabeceos suaves -> VERIFICA SIEMPRE en vídeo los tramos (extrae frames).

Uso: gaze.py --media corte.mp4 [--step 0.2] [--pitch-margin 0.07] [--yaw-dev 0.06]
             [--gaze-dev 0.16] [--min-win 0.4] [--merge-gap 0.5] [--out gaze.json]
Salida: JSON [{start,end,dur,reason}] + tabla legible. Cada ventana = "sujeto fuera -> visual full-screen".
"""
import argparse, json, statistics, sys
try:
    import cv2, mediapipe as mp
except ImportError:
    sys.exit("Faltan dependencias: pip install --user mediapipe opencv-python")

# landmarks (FaceMesh refine_landmarks=True)
NOSE, CHIN = 1, 152
L_OUT, L_IN = 33, 133      # ojo izq: esquina externa / interna
R_OUT, R_IN = 263, 362     # ojo der
L_IRIS, R_IRIS = 468, 473

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media", required=True)
    ap.add_argument("--step", type=float, default=0.2, help="muestreo en segundos")
    ap.add_argument("--pitch-margin", type=float, default=0.07)
    ap.add_argument("--yaw-dev", type=float, default=0.06)
    ap.add_argument("--gaze-dev", type=float, default=0.16)
    ap.add_argument("--min-win", type=float, default=0.4, help="ventana mínima de mirada-fuera (s)")
    ap.add_argument("--merge-gap", type=float, default=0.5, help="fusionar ventanas separadas < esto (s)")
    ap.add_argument("--out", default="gaze.json")
    a = ap.parse_args()

    cap = cv2.VideoCapture(a.media)
    if not cap.isOpened():
        sys.exit(f"No puedo abrir {a.media}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    dur = total / fps if fps else 0

    fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True,
                                         max_num_faces=1, min_detection_confidence=0.5)
    samples = []  # (t, pitch, yaw, gaze_h, face_ok)
    t = 0.0
    while t < dur:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
        ok, frame = cap.read()
        if not ok:
            break
        res = fm.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not res.multi_face_landmarks:
            samples.append((round(t,2), None, None, None, False))
            t += a.step; continue
        lm = res.multi_face_landmarks[0].landmark
        def P(i): return (lm[i].x, lm[i].y)
        nose = P(NOSE); chin = P(CHIN)
        lo, li, ro, ri = P(L_OUT), P(L_IN), P(R_OUT), P(R_IN)
        eye_mid = ((lo[0]+ro[0])/2, (lo[1]+ro[1])/2)
        interoc = abs(ro[0]-lo[0]) or 1e-4
        face_h = abs(chin[1]-eye_mid[1]) or 1e-4
        # pitch: nariz por debajo de la línea de ojos (mira abajo -> sube)
        pitch = (nose[1]-eye_mid[1]) / face_h
        # yaw: nariz desplazada lateralmente respecto al centro de los ojos
        yaw = (nose[0]-eye_mid[0]) / interoc
        # gaze_h: posición horizontal del iris dentro de cada ojo (0..1, centro ~0.5); media de ambos
        def gh(iris, out, inn):
            span = (inn[0]-out[0]) or 1e-4
            return (iris[0]-out[0]) / span
        gaze_h = (gh(P(L_IRIS), lo, li) + gh(P(R_IRIS), ro, ri)) / 2
        samples.append((round(t,2), pitch, yaw, gaze_h, True))
        t += a.step
    cap.release(); fm.close()

    valid = [s for s in samples if s[4]]
    if not valid:
        sys.exit("No se detectó cara en ningún muestreo.")
    med_pitch = statistics.median(s[1] for s in valid)
    med_yaw   = statistics.median(s[2] for s in valid)
    med_gaze  = statistics.median(s[3] for s in valid)

    # marcar mira-fuera
    flags = []
    for (ts, pitch, yaw, gaze_h, ok) in samples:
        if not ok:
            flags.append((ts, True, {"sin cara"}))  # sin cara = tratar como fuera (conservador)
            continue
        reasons = set()
        if pitch > med_pitch + a.pitch_margin: reasons.add("mira abajo")
        if abs(yaw - med_yaw) > a.yaw_dev:     reasons.add("gira cabeza")
        if abs(gaze_h - med_gaze) > a.gaze_dev: reasons.add("mirada lateral")
        flags.append((ts, bool(reasons), reasons))

    # agrupar en ventanas + fusionar huecos cortos
    wins = []
    cur = None
    for (ts, out, why) in flags:
        if out:
            if cur is None: cur = [ts, ts + a.step, set(why)]
            else: cur[1] = ts + a.step; cur[2] |= why
        else:
            if cur is not None: wins.append(cur); cur = None
    if cur is not None: wins.append(cur)
    merged = []
    for w in wins:
        if merged and w[0] - merged[-1][1] < a.merge_gap:
            merged[-1][1] = w[1]; merged[-1][2] |= w[2]
        else:
            merged.append(w)
    out_wins = [{"start": round(s,2), "end": round(e,2), "dur": round(e-s,2),
                 "reason": ", ".join(sorted(r for r in why if r))}
                for (s,e,why) in merged if (e-s) >= a.min_win]

    print("="*80)
    print(f"GAZE · {a.media} · {dur:.1f}s · muestreo {a.step}s · medianas pitch={med_pitch:.2f} yaw={med_yaw:.2f} gaze={med_gaze:.2f}")
    print("="*80)
    if out_wins:
        for w in out_wins:
            print(f"  MIRA-FUERA  {w['start']:6.2f}-{w['end']:6.2f} ({w['dur']:4.1f}s)  {w['reason']}")
        print(f"\n{len(out_wins)} ventana(s) 'sujeto fuera'. En el beat sheet -> cubrir con VISUAL full-screen.")
    else:
        print("  (ningún tramo claro de mirada-fuera)")
    print("\n⚠️  VERIFICA SIEMPRE en vídeo: el detector SUBESTIMA cabeceos suaves. Extrae frames de cada "
          "ventana (ffmpeg -ss <t> -frames:v 1) y confirma antes de sustituir a la persona por visual.")
    json.dump(out_wins, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"\nJSON -> {a.out}")

if __name__ == "__main__":
    main()
