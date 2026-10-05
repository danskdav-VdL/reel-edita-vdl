"""score-plantilla.py — PARTITURA ORIGINAL + diseño de sonido para un vídeo de motion (Modo B / pieza de marca).

Copia este archivo a <proyecto>/edicion/audio/compose.py y ajusta SOLO la sección "PLAN".
La estructura por actos (tensión -> respiración -> reveal -> groove -> remate) es la que funcionó en el
film de Staynex (2026-10-02). Todo cae en la REJILLA del tempo: los cortes del vídeo deben caer en ella
también (planifícalos en compases: a 120 BPM, 1 negra = 0,5 s, 1 compás = 2 s).

    python3 compose.py            -> music.wav, sfx.wav, mix.wav en esta carpeta
    bash ~/.claude/skills/reel-edita-vdl/scripts/mux-master.sh <video.mp4> mix.wav <FINAL.mp4>

Reglas de sonido (references/03-sfx-y-qc.md): sonidos de objetos reales, no pitidos de videojuego;
pocos golpes de pantalla completa (≤3 por pieza); la campana UNA vez; el sonido se hace con la imagen
YA bloqueada (si cambia el timing, se re-temporiza toda la tabla de SFX).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser("~/.claude/skills/reel-edita-vdl/scripts"))
from score_kit import Kit, CHORDS

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================ PLAN (edita aquí)
DUR = 24.0                 # duración total del vídeo (s), SIN la cortinilla
BPM = 120                  # 120 -> compás = 2 s. Cambia y re-planifica los cortes en compases.
SEED = 20261002            # misma semilla = mismo audio

k = Kit(dur=DUR, bpm=BPM, seed=SEED)
BAR, BEAT, S16 = k.BAR, k.BEAT, k.S16

# Secciones en segundos (múltiplos de BAR). Ajusta a tu storyboard.
TENSION = (0.0, 3.5)             # acto I: reloj + pulso filtrado que se abre
RESPIRA = (3.5, 4.0)             # silencio REAL (la coma dramática antes del reveal)
REVEAL = (4.0, 8.0)              # acto II: golpe sub + pads anchos + campanitas
GROOVE = (8.0, 20.0)             # acto III: el producto en uso (bombo, palmas, bajo, arpegio)
REMATE = (20.0, DUR)             # acto IV: golpe final + pad largo + fundido
LOOP = ["Dm9", "Bb9", "F9", "C69"]  # progresión del groove (ver CHORDS en score_kit.py)

# Tabla de SFX: (segundo, nombre, volumen). Nombres = funciones del kit (whoosh/shimmer/tick/boom/riser)
# o sonidos CC0 de assets/sfx-kenney (click_002, card-slide-3, impactSoft_medium_002, keypress-001…).
# Cada fila = una acción visible en pantalla (escríbela en el comentario).
SFX = [
    (0.25, "impactGlass_light_002", 0.45),   # primer elemento que aparece
    (4.05, "shimmer", 1.0),                  # trazo del logo / reveal
    (7.40, "whoosh", 1.0),                   # corte a la escena del producto
    (8.00, "impactSoft_medium_004", 0.6),    # aterrizaje en el corte
    (12.00, "click_002", 0.7),               # clic del cursor
    (12.05, "switch_004", 0.4),              # cambio de estado
    (20.00, "impactBell_heavy_000", 0.4),    # remate (la campana UNA vez)
]
# ============================================================ FIN DEL PLAN

pads, bass, drums, arps, bells, fx = (k.buf() for _ in range(6))

# --- ACTO I: tensión (semicorcheas de hi-hat que crecen + pulso de bajo que se abre + riser)
a, b = TENSION
for i in range(int((b - a) / S16)):
    t = a + i * S16
    k.place(drums, k.hat(False, 0.05 + 0.08 * (t - a) / (b - a)), t, pan=0.25 if i % 2 else -0.25)
pulse = np.zeros(k.N)
for i in range(int((b - a) / (S16 * 2))):
    seg = k.bass_note(38 if i % 8 else 50, 0.2, 0.22, cut=260)
    j = k.t2i(a + i * S16 * 2); n = min(len(seg), k.N - j); pulse[j:j + n] += seg[:n]
pulse = k.timevar_lp(pulse, lambda tt: 300 + 2200 * min(1, max(0, (tt - a) / (b - a))) ** 1.6)
k.place(bass, pulse, 0.0)
k.place(pads, k.pad("Dmadd", b - a, gain=0.075, bright=1100, att=min(2.0, (b - a) / 2), rel=0.02)[:, :k.t2i(b - a)], a)
k.place(fx, k.riser(min(1.5, b - a), 0.22), b - min(1.5, b - a))

# --- ACTO II: reveal
a, b = REVEAL
k.place(fx, k.boom(0.85), a)
for i, ch in enumerate(["F9", "Dm9"]):
    t0 = a + i * BAR
    if t0 >= b: break
    k.place(pads, k.pad(ch, BAR, gain=0.13, bright=2200, att=0.25 if i == 0 else 0.6, rel=0.6), t0)
    k.place(bass, k.bass_note(CHORDS[ch]["bass"], BAR * 0.95, 0.18, cut=250), t0)
for o, m in [(0.5, 84), (1.0, 79), (1.25, 81), (2.0, 76), (2.5, 81), (3.0, 84)]:
    if a + o < b: k.place(bells, k.bell(m, 0.055), a + o, pan=(m - 80) / 10)
k.place(fx, k.riser(1.2, 0.2, 500, 9000), b - 1.2)

# --- ACTO III: groove (bajo sincopado + bombo a negras + palmas en 2 y 4 + arpegio) con sidechain
a, b = GROOVE
BASS_PAT = [0, 3, 6, 8, 10, 11, 14]
ARP_PAT = [0, 2, 1, 3, 2, 4, 3, 1]
kicks = []
nbars = int(round((b - a) / BAR))
for bi in range(nbars):
    t0 = a + bi * BAR; ch = LOOP[bi % len(LOOP)]; lift = bi >= nbars // 2
    k.place(pads, k.pad(ch, BAR, gain=0.085, bright=3000 if lift else 2500, att=0.08, rel=0.35), t0)
    for s in BASS_PAT:
        k.place(bass, k.bass_note(CHORDS[ch]["bass"] + (12 if s in (10, 14) else 0), 0.22, 0.26, cut=520), t0 + s * S16)
    for q in range(4):
        k.place(drums, k.kick(0.85), t0 + q * BEAT); kicks.append(t0 + q * BEAT)
    for q in (1, 3):
        k.place(drums, k.clap(0.32), t0 + q * BEAT, pan=0.05)
    for s in range(16):
        if s % 2: k.place(drums, k.hat(False, 0.05 + (0.025 if s % 4 == 3 else 0)), t0 + s * S16, pan=-0.3)
    voices = CHORDS[ch]["v"]
    for s in range(16):
        k.place(arps, k.pluck(voices[ARP_PAT[s % 8] % len(voices)] + 12, 0.065 if lift else 0.055,
                              cut=3800 if lift else 2800, dec=8), t0 + s * S16, pan=-0.4 if s % 2 else 0.4)
side = k.sidechain(kicks)
pads *= side; arps *= side

# --- ACTO IV: remate
a, b = REMATE
k.place(fx, k.boom(0.9), a)
k.place(pads, k.pad("F9", max(1.0, b - a - 1.0), gain=0.14, bright=2400, att=0.05, rel=1.5), a)
k.place(bass, k.bass_note(41, max(1.0, b - a - 1.0), 0.2, cut=230), a)
for o, m in [(0.5, 84), (1.0, 81), (1.5, 79), (2.25, 77)]:
    if a + o < b: k.place(bells, k.bell(m, 0.05, 1.8), a + o, pan=(m - 80) / 10)

# --- mezcla
arps_w = arps + k.pingpong(arps) * 0.8
wet = k.reverb(pads * 0.6 + arps_w * 0.5 + bells * 0.9 + drums * 0.12 + fx * 0.25)
music = pads + bass + drums + arps_w + bells + fx + wet * 1.4
music = k.gate(music, *RESPIRA)
music = k.fade_out(music, DUR - 2.4, DUR)

# --- diseño de sonido (tabla SFX)
sfx = k.buf()
for t, name, vol in SFX:
    synth = {"whoosh": lambda: k.whoosh(0.5, 0.22), "shimmer": lambda: k.shimmer(0.8, 0.05),
             "tick": lambda: k.tick(0.1), "boom": lambda: k.boom(0.7), "riser": lambda: k.riser(1.0, 0.18)}
    sig = synth[name]() if name in synth else k.kenney(name)
    k.place(sfx, sig, t, vol)

print("->", k.write_stems(music, sfx, HERE))
