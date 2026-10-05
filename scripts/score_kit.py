"""score_kit.py — kit de síntesis para MÚSICA ORIGINAL y diseño de sonido deterministas (sin licencias).

Extraído del film de producto de Staynex (2026-10-02), que demostró que una partitura sintetizada en código
sobre una rejilla de tempo da un acabado de "vídeo de lanzamiento" sin depender de música de terceros.
Todo se sintetiza aquí (o se carga de la librería CC0 de Kenney) -> sin problemas de licencia.

Uso (ver plantillas/score-plantilla.py):
    from score_kit import Kit
    k = Kit(dur=24.0, bpm=120, seed=20261002)
    pads = k.buf(); k.place(pads, k.pad('Dm9', k.BAR), 0.0)
    ...
    k.write_stems(music, sfx, out_dir)

Determinista: misma semilla -> mismo audio, bit a bit. Requiere numpy + scipy.
"""
import os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

KENNEY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sfx-kenney")

# Acordes de ejemplo (MIDI). Añade los tuyos: {'bass': nota_grave, 'v': [voces del pad]}
CHORDS = {
    "Dm9":   {"bass": 38, "v": [50, 53, 57, 60, 64]},
    "Bb9":   {"bass": 34, "v": [50, 53, 57, 60, 62]},
    "F9":    {"bass": 41, "v": [53, 57, 60, 64, 67]},
    "C69":   {"bass": 36, "v": [52, 55, 57, 62, 64]},
    "Dmadd": {"bass": 38, "v": [50, 53, 57, 62, 64]},
    "Am9":   {"bass": 33, "v": [48, 52, 55, 59, 62]},
    "Fmaj9": {"bass": 41, "v": [53, 57, 60, 64, 67]},
    "Cmaj9": {"bass": 36, "v": [48, 52, 55, 59, 62]},
    "G6":    {"bass": 43, "v": [50, 55, 59, 62, 64]},
}


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


class Kit:
    def __init__(self, dur, bpm=120, sr=48000, seed=20261002, tail=1.0):
        self.SR = sr
        self.DUR = float(dur)
        self.N = int(sr * (dur + tail))
        self.BPM = bpm
        self.BEAT = 60.0 / bpm          # negra
        self.BAR = self.BEAT * 4        # compás 4/4
        self.S16 = self.BEAT / 4        # semicorchea
        self.rs = np.random.RandomState(seed)
        self.IR = self._make_ir()

    # ------------------------------------------------------------ utilidades
    def t2i(self, t):
        return int(round(t * self.SR))

    def buf(self):
        return np.zeros((2, self.N), dtype=np.float64)

    def grid(self, bar, beat=0, s16=0):
        """Tiempo (s) de un punto de la rejilla: compás, negra, semicorchea (todo desde 0)."""
        return bar * self.BAR + beat * self.BEAT + s16 * self.S16

    def snap(self, t, div=4):
        """Redondea t a la rejilla (div=4 -> negras... usa 16 para semicorcheas)."""
        step = self.BAR / div
        return round(t / step) * step

    def lp(self, x, fc, order=2):
        return sosfilt(butter(order, min(fc, self.SR * 0.45), "low", fs=self.SR, output="sos"), x)

    def hp(self, x, fc, order=2):
        return sosfilt(butter(order, fc, "high", fs=self.SR, output="sos"), x)

    def bp(self, x, lo, hi, order=2):
        return sosfilt(butter(order, [lo, hi], "band", fs=self.SR, output="sos"), x)

    def saw(self, f, n, phase=0.0):
        t = np.arange(n) / self.SR
        return 2.0 * ((t * f + phase) % 1.0) - 1.0

    def sine(self, f, n, phase=0.0):
        t = np.arange(n) / self.SR
        return np.sin(2 * np.pi * f * t + phase)

    def adsr(self, n, a, d, s, r, sus_len=None):
        SR = self.SR
        a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
        if sus_len is None:
            sus_len = n - a_n - d_n - r_n
        sus_len = max(0, int(sus_len))
        e = np.concatenate([np.linspace(0, 1, max(a_n, 1), endpoint=False),
                            np.linspace(1, s, max(d_n, 1), endpoint=False),
                            np.full(int(sus_len), s),
                            np.linspace(s, 0, max(r_n, 1))])
        if len(e) < n:
            e = np.pad(e, (0, n - len(e)))
        return e[:n]

    def place(self, dst, sig, t, gain=1.0, pan=0.0):
        """Suma una señal mono o estéreo en t (paneo de potencia constante)."""
        i = self.t2i(t)
        if i >= dst.shape[1] or i < 0:
            return
        if sig.ndim == 1:
            l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
            sig = np.vstack([sig * l * 1.414, sig * r * 1.414])
        n = min(sig.shape[1], dst.shape[1] - i)
        dst[:, i:i + n] += sig[:, :n] * gain

    def timevar_lp(self, x, cut_fn, block=512):
        """Paso bajo variable en el tiempo, por bloques, con estado arrastrado."""
        y = np.zeros_like(x); zi = np.zeros((1, 2))
        for s in range(0, len(x), block):
            fc = float(cut_fn((s + block / 2) / self.SR))
            sos = butter(2, min(max(fc, 40), self.SR * 0.45), "low", fs=self.SR, output="sos")
            y[s:s + block], zi = sosfilt(sos, x[s:s + block], zi=zi)
        return y

    # ------------------------------------------------------------ instrumentos
    def pad_voice(self, m, n, bright=1800):
        f = mtof(m); x = np.zeros(n)
        for dc in (-0.09, 0.0, 0.08):           # ~ ±8 cents de desafinación
            x += self.saw(f * 2 ** (dc / 12), n, phase=self.rs.rand())
        return self.lp(x / 3.0, bright, 2)

    def pad(self, chord, dur, gain=0.11, bright=1700, att=0.5, rel=1.2, width=0.6):
        t2i = self.t2i
        n = t2i(dur + rel); out = np.zeros((2, n))
        for k, m in enumerate(CHORDS[chord]["v"]):
            v = self.pad_voice(m, n, bright) * self.adsr(n, att, 0.4, 0.85, rel,
                                                         sus_len=t2i(dur) - t2i(att) - t2i(.4))
            pan = (-width if k % 2 == 0 else width) * (0.4 + 0.6 * k / 5)
            out[0] += v * np.cos((pan + 1) * np.pi / 4); out[1] += v * np.sin((pan + 1) * np.pi / 4)
        return out * gain

    def kick(self, gain=0.9):
        n = self.t2i(0.45); t = np.arange(n) / self.SR
        f = 46 + 110 * np.exp(-t * 38); ph = 2 * np.pi * np.cumsum(f) / self.SR
        x = np.sin(ph) * np.exp(-t * 10.5)
        click = self.hp(self.rs.randn(n), 3000) * np.exp(-t * 400) * 0.25
        return np.tanh((x + click) * 1.4) * gain

    def clap(self, gain=0.4):
        n = self.t2i(0.35); t = np.arange(n) / self.SR
        nz = self.bp(self.rs.randn(n), 900, 3800); env = np.zeros(n)
        for o in (0.0, 0.011, 0.022):
            i = self.t2i(o); env[i:] += np.exp(-(t[:n - i]) * 55) * 0.7
        env += np.exp(-t * 14) * 0.35
        return nz * env * gain

    def hat(self, open_=False, gain=0.12):
        n = self.t2i(0.3 if open_ else 0.06); t = np.arange(n) / self.SR
        return self.hp(self.rs.randn(n), 7500, 2) * np.exp(-t * (14 if open_ else 90)) * gain

    def bass_note(self, m, dur, gain=0.32, cut=650):
        t2i = self.t2i
        n = t2i(dur + 0.08); f = mtof(m)
        x = 0.65 * self.saw(f, n) + 0.35 * np.sign(self.sine(f, n))
        y = self.timevar_lp(x, lambda tt: cut + 1400 * np.exp(-tt * 22), block=256)
        sub = self.sine(f, n) * 0.42
        e = self.adsr(n, 0.004, 0.12, 0.7, 0.07, sus_len=max(0, t2i(dur) - t2i(.124)))
        return np.tanh((y * 0.8 + sub) * e * 1.2) * gain

    def pluck(self, m, gain=0.08, cut=2600, dec=7.0):
        n = self.t2i(0.5); t = np.arange(n) / self.SR; f = mtof(m)
        x = self.saw(f, n) * 0.6 + self.saw(f * 1.004, n, .3) * 0.4
        x = self.timevar_lp(x, lambda tt: 500 + cut * np.exp(-tt * 9), block=256)
        return x * np.exp(-t * dec) * gain

    def bell(self, m, gain=0.07, dec=2.2):
        n = self.t2i(2.2); t = np.arange(n) / self.SR; f = mtof(m)
        x = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 3)
             + 0.25 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 5)
             + 0.12 * np.sin(2 * np.pi * f * 5.43 * t) * np.exp(-t * 8))
        return x * np.exp(-t * dec) * (1 - np.exp(-t * 300)) * gain

    # ------------------------------------------------------------ diseño de sonido
    def riser(self, dur, gain=0.18, f0=300, f1=6000):
        SR = self.SR; n = self.t2i(dur); t = np.arange(n) / SR; p = t / dur
        nz = self.rs.randn(n); y = np.zeros(n); zi = np.zeros((2, 2)); blk = 512
        for s in range(0, n, blk):
            fc = f0 * (f1 / f0) ** ((s + blk / 2) / n)
            sos = butter(2, [fc * 0.7, min(fc * 1.4, SR * 0.45)], "band", fs=SR, output="sos")
            y[s:s + blk], zi = sosfilt(sos, nz[s:s + blk], zi=zi)
        f = 110 * (2 ** (p * 2.5)); ph = 2 * np.pi * np.cumsum(f) / SR
        tone = self.lp(np.sign(np.sin(ph)) * 0.25 + np.sin(ph * 2) * 0.2, 3000)
        return (y * 1.6 + tone * 0.5) * p ** 2.2 * gain

    def whoosh(self, dur=0.55, gain=0.22, up=True):
        SR = self.SR; n = self.t2i(dur); t = np.arange(n) / SR; p = t / dur
        nz = self.rs.randn(n); y = np.zeros(n); zi = np.zeros((2, 2)); blk = 256
        for s in range(0, n, blk):
            pc = (s + blk / 2) / n; c = (pc if up else 1 - pc)
            fc = 400 + 5200 * np.sin(np.pi * min(1, c)) ** 1.5
            sos = butter(2, [fc * 0.6, min(fc * 1.6, SR * 0.45)], "band", fs=SR, output="sos")
            y[s:s + blk], zi = sosfilt(sos, nz[s:s + blk], zi=zi)
        return y * np.sin(np.pi * p) ** 2 * gain

    def boom(self, gain=0.75):
        n = self.t2i(2.0); t = np.arange(n) / self.SR
        f = 34 + 60 * np.exp(-t * 6); ph = 2 * np.pi * np.cumsum(f) / self.SR
        x = np.sin(ph) * np.exp(-t * 2.2)
        nz = self.lp(self.rs.randn(n), 900) * np.exp(-t * 9) * 0.35
        return np.tanh((x + nz) * 1.6) * gain

    def shimmer(self, dur=0.9, gain=0.05):
        n = self.t2i(dur); t = np.arange(n) / self.SR; out = np.zeros(n)
        for k, m in enumerate([88, 91, 95, 98, 100]):
            out += np.sin(2 * np.pi * mtof(m) * t + k) * np.exp(-((t - k * dur / 7) ** 2) / 0.02)
        return out * gain

    def tick(self, gain=0.12, f=2400):
        n = self.t2i(0.05); t = np.arange(n) / self.SR
        return np.sin(2 * np.pi * f * t) * np.exp(-t * 120) * gain

    def kenney(self, name):
        """Carga un SFX CC0 de assets/sfx-kenney (import-sfx-kenney.sh) como estéreo float."""
        sr, x = wavfile.read(os.path.join(KENNEY_DIR, name + ".wav"))
        x = x.astype(np.float64)
        if np.max(np.abs(x)) > 2:
            x /= 32768.0
        return x.T if x.ndim == 2 else np.vstack([x, x])

    # ------------------------------------------------------------ efectos y mezcla
    def _make_ir(self, sec=2.6, pre=0.02):
        n = self.t2i(sec); t = np.arange(n) / self.SR
        ir = np.zeros((2, n + self.t2i(pre)))
        for c in range(2):
            x = self.rs.randn(n) * np.exp(-t * 2.6)
            ir[c, self.t2i(pre):] = self.hp(self.lp(x, 6500), 180)
        return ir / np.max(np.abs(ir)) * 0.06

    def reverb(self, x):
        out = np.zeros_like(x)
        for c in range(2):
            out[c] = fftconvolve(x[c], self.IR[c])[:x.shape[1]]
        return out

    def pingpong(self, x, d=None, fb=0.38, taps=5):
        d = self.BEAT * 0.75 if d is None else d      # corchea con puntillo
        out = np.zeros_like(x); mono = x.mean(axis=0)
        for k in range(1, taps + 1):
            i = self.t2i(d * k)
            out[k % 2, i:] += mono[:x.shape[1] - i] * fb ** k
        return self.lp(out, 4200)

    def sidechain(self, kick_times, depth=0.42, rel=11.0, win=0.32):
        """Curva de 'bombeo' (ducking) a partir de los golpes de bombo; multiplica pads/arps por ella."""
        side = np.ones(self.N)
        for t in kick_times:
            i = self.t2i(t); n = self.t2i(win)
            env = 1 - depth * np.exp(-np.arange(n) / self.SR * rel)
            m = min(n, self.N - i)
            if m > 0:
                side[i:i + m] = np.minimum(side[i:i + m], env[:m])
        return side

    def gate(self, x, t0, t1, fade=0.012):
        """Silencio REAL entre t0 y t1 (la 'respiración' antes de un reveal), con micro-fundido."""
        g = np.ones(x.shape[1]); a, b = self.t2i(t0), self.t2i(t1)
        g[a:b] = 0.0; f = self.t2i(fade)
        g[max(0, a - f):a] = np.linspace(1, 0, a - max(0, a - f))
        return x * g

    def fade_out(self, x, t0, t1, curve=1.6):
        a, b = self.t2i(t0), self.t2i(t1)
        x[:, a:b] *= np.linspace(1, 0, b - a) ** curve
        x[:, b:] = 0
        return x

    @staticmethod
    def norm_peak(x, p=0.89):
        m = np.max(np.abs(x))
        return x * (p / m) if m > 0 else x

    def master_bus(self, music):
        """EQ suave (low-cut, -3.5 dB en graves, +3 dB en agudos) + saturación tanh."""
        for c in range(2):
            music[c] = self.hp(music[c], 30, 2)
            music[c] = music[c] - 0.33 * self.lp(music[c], 110, 2)
            music[c] = music[c] + 0.45 * self.hp(music[c], 2800, 2)
        return np.tanh(music * 1.15) / 1.15

    def write(self, path, x):
        y = np.clip(x[:, :self.t2i(self.DUR)], -1, 1).T.astype(np.float32)
        wavfile.write(path, self.SR, y)

    def write_stems(self, music, sfx, out_dir):
        """Escribe music.wav, sfx.wav y mix.wav (pre-máster). Masteriza luego con mux-master.sh."""
        os.makedirs(out_dir, exist_ok=True)
        music_s = self.master_bus(music)
        self.write(os.path.join(out_dir, "music.wav"), self.norm_peak(music_s, 0.7))
        self.write(os.path.join(out_dir, "sfx.wav"), self.norm_peak(sfx, 0.7))
        mix = np.tanh((self.norm_peak(music_s, 0.62) + sfx) * 1.05)
        self.write(os.path.join(out_dir, "mix.wav"), self.norm_peak(mix, 0.95))
        return os.path.join(out_dir, "mix.wav")
