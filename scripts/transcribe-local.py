#!/usr/bin/env python3
"""transcribe-local.py — plan B de transcribe-groq.sh: word-level en LOCAL con faster-whisper (GPU si hay).

Misma salida que transcribe-groq.sh: { "text": "...", "words": [{"word","start","end"}], "segments": [...] }
(el formato que esperan islands.py / verify-cut.py / detect-repeats.py / captions.py).

Uso: python3 transcribe-local.py <audio_o_video> <json_out> [idioma=es] [--model large-v3] [--prompt "texto"]
Requiere: pip install faster-whisper (el modelo se descarga la 1.ª vez a ~/.cache/huggingface).
"""
import argparse, json, os, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("out"); ap.add_argument("lang", nargs="?", default="es")
    ap.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "large-v3"))
    ap.add_argument("--prompt", default=None, help="vocabulario/nombres propios para guiar la transcripción")
    a = ap.parse_args()
    # Windows + GPU: ctranslate2 necesita cuBLAS/cuDNN; torch (cu12x) ya las trae en torch/lib.
    if os.name == "nt":
        import importlib.util, pathlib
        spec = importlib.util.find_spec("torch")
        if spec and spec.origin:
            lib = pathlib.Path(spec.origin).parent / "lib"
            if lib.exists():
                os.add_dll_directory(str(lib)); os.environ["PATH"] = str(lib) + os.pathsep + os.environ.get("PATH", "")
    from faster_whisper import WhisperModel
    try:
        import ctranslate2
        dev = "cuda" if ctranslate2.get_cuda_device_count() > 0 and os.environ.get("WHISPER_DEVICE") != "cpu" else "cpu"
    except Exception:
        dev = "cpu"

    def run(dev):
        model = WhisperModel(a.model, device=dev, compute_type="float16" if dev == "cuda" else "int8")
        segs, info = model.transcribe(a.audio, language=a.lang, word_timestamps=True, vad_filter=False,
                                      beam_size=5, initial_prompt=a.prompt, condition_on_previous_text=False)
        words, segments, texts = [], [], []
        for s in segs:                       # el generador es perezoso: los errores de CUDA salen aquí
            texts.append(s.text.strip())
            segments.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()})
            for w in (s.words or []):
                words.append({"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
        return words, segments, texts, info

    try:
        words, segments, texts, info = run(dev)
    except RuntimeError as e:
        if dev != "cuda" or not any(k in str(e).lower() for k in ("cublas", "cudnn", "cuda")):
            raise
        print(f"  (GPU no disponible: {str(e)[:70]}… -> CPU)")
        dev = "cpu"
        words, segments, texts, info = run(dev)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump({"text": " ".join(texts), "words": words, "segments": segments, "language": info.language,
               "engine": f"faster-whisper {a.model} ({dev})"}, open(a.out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"▸ {len(words)} palabras, {len(segments)} segmentos -> {a.out} ({dev})")


if __name__ == "__main__":
    sys.exit(main())
