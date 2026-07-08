# Fase 1 — Bloquear el corte (determinista por silencedetect)

Meta: corte ágil (≈60-90s), **sin silencios en el cuerpo, sin errores, sin una sola repetición**, validado por `verify-cut.py` (exit 0) antes de animar nada.

## Entrada: uno o varios clips (multi-clip) + rotación + concat LIMPIO

El "bruto" puede ser **un solo MP4** o **una carpeta de clips** (tomas/segmentos de un mismo guion,
p. ej. 15 `.mov` de móvil). Si es carpeta:

1. **Orden:** por nombre (o `creation_time` de ffprobe) — es el orden del guion.
2. **Rotación (¡crítico!):** los móviles graban 1920×1080 con metadato `rotation=-90` → en realidad son
   verticales. Comprueba `ffprobe -show_entries stream_tags=rotate:stream_side_data=rotation` y **quema
   la orientación** al concatenar (no confíes en el metadato; aplica el transpose/scale que corresponda).
3. **Concat LIMPIO (regla dura):** concatena con el **filtro `concat`** re-encodeando a H.264
   (decodifica cada clip por separado). **NUNCA `-c copy` con material de cámara**: empalmar HEVC da
   errores `Could not find ref / RPS` y **deriva temporal acumulativa** (~0.4s al final).
   ```bash
   # cada clip vertical y re-encodeado; sin empalmar bitstream
   ffmpeg -i c1.mp4 -i c2.mp4 ... -filter_complex \
     "[0:v][0:a][1:v][1:a]...concat=n=N:v=1:a=1[v][a]" \
     -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k \
     edicion/bruto-ensamblado.mp4
   ```
4. **islands/verify SIEMPRE sobre el MISMO archivo que usa `cut.py`.** Si cambias el `bruto` (p. ej.
   rehaces el concat), **re-transcribe y re-deriva islands** — si no, los timestamps no cuadran.

## Auto-trim del arranque (hook)

No dejes >~0.5s de aire muerto al inicio. Ajusta el `start` del primer islote para que el hook entre
**~0.15-0.25s antes de la primera palabra**. (En `islands.json`, mueve el `start` del islote #0.)

## 🔴 REGLA DURA — nunca la misma frase repetida seguida (aunque Whisper la fusione)

El fallo más grave detectado de oído: una frase grabada **dos veces con micro-silencio** que Whisper
transcribe **UNA sola vez** (queda una **palabra dragueada** de 2-3s). No aparece como repetición en el
texto → se cuela al corte. `verify-cut.py` lo caza con el **check 1b** (hueco sin silencio / palabra
dragueada). Método de remediación cuando salte (o lo oigas):
1. Aísla el tramo sospechoso: `ffmpeg -ss <ini> -to <fin> -i bruto.mp4 -vn /tmp/susp.wav`.
2. **Re-transcribe ralentizado** para que Whisper separe las dos tomas:
   `ffmpeg -i /tmp/susp.wav -filter:a "atempo=0.7" /tmp/susp_slow.wav` → transcribe.
3. Confirma que son dos tomas de la misma frase y **quédate con la ÚLTIMA** (ajusta islands → re-cut → re-verify).

## MÉTODO CANÓNICO (2026-06-21) — scripts, no a mano

Los timestamps de Whisper son imprecisos → cortar por ellos deja silencios y repeticiones (falló 3 veces). El corte se hace por **islotes de voz de `silencedetect`** + **última toma** + **concat sin pausas**, con tres scripts:

```bash
# 0) transcribir el bruto UNA vez (word-level). Reutilizar para todo.
ffmpeg -i bruto.mp4 -vn -ac 1 -b:a 64k -y edicion/bruto-audio.m4a
bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh edicion/bruto-audio.m4a edicion/bruto-word.json

# 1) islotes + propuesta última-toma (silencedetect)
python3 ~/.claude/skills/reel-edita-vdl/scripts/islands.py \
  --media bruto.mp4 --transcript edicion/bruto-word.json --out edicion/islands.json
#    -> revisa la tabla KEEP/DROP. Corrige a mano en islands.json los DROP que
#       la heurística no pilla: bloopers ("joder"), falsos arranques, tangentes, fragmentos.

# 2) montar el corte (pega islotes sin pausas; pad hacia dentro del silencio)
python3 ~/.claude/skills/reel-edita-vdl/scripts/cut.py \
  --islands edicion/islands.json --out edicion/corte-final.mp4

# 3) COMPUERTA DURA (bloqueante): re-transcribir el corte y verificar
ffmpeg -i edicion/corte-final.mp4 -vn -ac 1 -b:a 64k -y edicion/cf.m4a
bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh edicion/cf.m4a edicion/transcript-final.json
python3 ~/.claude/skills/reel-edita-vdl/scripts/verify-cut.py \
  --media edicion/corte-final.mp4 --transcript edicion/transcript-final.json
#    exit 0 = PASA. exit 1 = arregla islands.json (silencio/repetición que indique),
#    re-cut.py, re-verifica. ITERA hasta exit 0. No animes sin PASS.
```

**Por qué funciona:** silencedetect da límites exactos (no jitter), pegar islotes elimina las pausas internas de 5-9s (los "muchos silencios"), y quedarse con la última toma elimina las repeticiones. La compuerta caza lo que el ojo deja pasar (p.ej. "pues aquí tienes" doblado tras una pausa larga).

---

## Apoyo: conocimiento de patrones (para el ajuste semántico del paso 1)

Lo de abajo es el detector antiguo (`detect-repeats.py`) y los patrones de repetición observados. Útil para decidir los DROP semánticos en `islands.json`, pero el flujo canónico es islands→cut→verify.

## 1. Transcripción word-level

```bash
ffmpeg -i bruto.mp4 -vn -ac 1 -b:a 64k -y edicion/audio.m4a
bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh edicion/audio.m4a edicion/transcript.json
```
(Groq `whisper-large-v3-turbo`, `GROQ_API_KEY` del `.env.local` del proyecto — los scripts lo buscan hacia arriba desde el cwd —, español, granularidad palabra+segmento. Si el audio >24MB, trocear con `ffmpeg -f segment` y concatenar.)

## 2. Detectar repeticiones, falsos arranques y tomas dobladas

```bash
python3 ~/.claude/skills/reel-edita-vdl/scripts/detect-repeats.py edicion/transcript.json
```
Imprime tres cosas:
- **Segmentos casi-duplicados** (near-dup, sim≥0.5) — tomas repetidas obvias.
- **Trigramas word-level repetidos** — capturan repeticiones DENTRO de la frase que el nivel de segmento no ve. Ignora los que son contexto distinto a propósito (ej. "github acaba de" en "decirte" vs "publicar"; "con inteligencia artificial" en dos frases). El resto suelen ser repeticiones reales.
- **Palabras dragueadas** (duración >1.5s) — candidatas a toma doblada: una palabra que dura 3-7s casi siempre esconde un silencio o que la dijo dos veces. Confírmalo con silencedetect.

Para una palabra dragueada o una zona sospechosa, mira la estructura habla/silencio:
```bash
ffmpeg -i corte.mp4 -af "silencedetect=noise=-30dB:d=0.18" -f null - 2>&1 | grep silence_start
```
Si ves habla–silencio–habla dentro de lo que el transcript marca como una palabra/frase → la dijo dos veces (toma doblada) o reinició la frase (falso arranque).

**Patrones reales vistos** (para que sepas qué buscar):
- *Toma doblada de palabra*: "masticadito" dicho 2 veces con un micro-silencio entre medias.
- *Falso arranque*: "Lo que ahora GitHub te lo da bastante…" (incompleto) y reinicia "Lo que ahora simplemente GitHub te lo da bastante masticadito para que…" (completa).
- *Restatement redundante*: "5 tasks, es decir, **tareas**, te hace una lista programada de **tareas**" → "tareas" dos veces.
- *Toma con/sin detalle*: "Gratis, licencia MIT…" vs "Gratis y con licencia MIT" → quédate con la última.
- *Eco al final*: "¿Te suena, no?" … "¿No?" repetido.

## 3. Regla de decisión: ÚLTIMA toma

Ante cualquier repetición, **conserva la ÚLTIMA toma completa** y elimina las anteriores (es la heurística de VdL: "normalmente la buena es la final"). Excepción de sentido común: si la última está incompleta y la anterior es la completa, quédate con la completa — el criterio real es *que no suene repetido y tenga coherencia al leerlo seguido*.

## 4. Ejecutar el corte

Construye una lista de **keep-ranges** (segundos sobre el bruto) que excluya las tomas malas. Córtalo con ffmpeg `filter_complex` (trim+concat, re-encode, precisión de frame). Patrón:

```python
# keeps = [(start,end), ...]  en segundos
parts=[f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}]" for i,(s,e) in enumerate(keeps)]
concat="".join(f"[v{i}][a{i}]" for i in range(len(keeps)))+f"concat=n={len(keeps)}:v=1:a=1[v][a]"
# ffmpeg -y -i bruto -filter_complex "<parts;concat>" -map [v] -map [a] -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k corte-content.mp4
```

Luego barre los silencios (incluye pausas internas y muertos largos). El flujo canónico (`islands.py → cut.py`) ya pega los islotes sin pausas, así que esto es solo un apoyo del método antiguo. Si tienes `auto-editor` instalado (`pip install auto-editor`) puedes usarlo; si no, no hace falta:
```bash
auto-editor edicion/corte-content.mp4 --margin 0.18s --no-open -o edicion/corte-final.mp4   # opcional
```

**Cortes mid-frase (quitar una repetición dentro de una frase):** los timestamps de whisper son imprecisos (±0.2-0.3s). NO cortes a ciegas por el timestamp de whisper — usa `silencedetect` para encontrar los límites de silencio reales alrededor de lo que quieres quitar y corta entre silencios. Verifica SIEMPRE re-transcribiendo (paso 5).

## 5. RE-VERIFICAR (sobre el corte ya hecho)

```bash
ffmpeg -i edicion/corte-final.mp4 -vn -ac 1 -b:a 64k -y edicion/audio-final.m4a
bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh edicion/audio-final.m4a edicion/transcript-final.json
python3 ~/.claude/skills/reel-edita-vdl/scripts/detect-repeats.py edicion/transcript-final.json
```
Lee el texto completo del corte de principio a fin buscando frases reiniciadas o conceptos repetidos. **Si aparece cualquier repetición, recórtala (sobre el corte actual) y vuelve a re-verificar.** Itera hasta que `detect-repeats.py` solo deje los falsos positivos de contexto distinto. Solo entonces el corte está limpio.

> Comprueba la duración: objetivo 1–3 min. Si quedó <1 min, avisa a VdL (quizá cortaste de más).

## 6. COMPUERTA — aprobación de VdL

Presenta: duración final, nº de cortes, **lista de qué se eliminó y por qué** (cada repetición/error). Abre el corte para que lo vea. **Espera su OK explícito.** No empieces la Fase 2 hasta que apruebe el corte. Este es el punto donde se evita el re-trabajo caro: una vez animes, recortar obliga a re-sincronizar todo.
