# Fase 5 — REVISOR (subagente independiente, OBLIGATORIO antes de entregar)

Objetivo: que el reel **no se entregue nunca** sin que un revisor independiente lo haya validado. Históricamente los fallos (silencios, repeticiones, desincronía) llegan a la entrega porque el mismo que monta es el que revisa. Este paso rompe eso: un subagente que NO montó el reel lo audita con ojos frescos y datos, y la entrega se bloquea si no pasa.

## Cuándo

Justo antes de la entrega (revisión local), sobre el **render final** (`renders/REEL-FINAL.mp4`), su corte (`edicion/corte-final.mp4`) y el `motion/index.html`. No se envía nada hasta tener un veredicto **PASS**.

## Cómo lanzarlo

Spawnea un subagente (tool `Agent`, tipo `general-purpose`) con el prompt de abajo. Pásale las rutas reales. El subagente devuelve JSON `{"verdict":"PASS|FAIL","scores":{...},"blockers":[],"warnings":[],"notes":"..."}`. Si `verdict != "PASS"`, **no entregues**: arregla los `blockers` y vuelve a lanzar el revisor. Itera hasta PASS.

## Prompt del subagente (plantilla)

> Eres el REVISOR final de un reel vertical de Valor de Ley. NO lo has montado tú: tu trabajo es encontrar fallos antes de que llegue a la entrega. Sé estricto; ante la duda, marca BLOCKER.
>
> Archivos:
> - Render final: `<ruta REEL-FINAL.mp4>`
> - Corte (audio): `<ruta corte-final.mp4>`
> - Transcript del corte (word-level): `<ruta transcript-final.json>`
> - Timeline Hyperframes: `<ruta motion/index.html>`
>
> Ejecuta y razona:
> 1. **Cortes (compuerta dura):** corre
>    `python3 ~/.claude/skills/reel-edita-vdl/scripts/verify-cut.py --media <corte-final.mp4> --transcript <transcript-final.json>`
>    Si sale exit≠0 → BLOCKER con el detalle (silencios/repeticiones).
> 2. **Ritmo estático (compuerta dura):** corre
>    `python3 ~/.claude/skills/reel-edita-vdl/scripts/lint-timeline.py <motion/index.html> --json`
>    Si `errors` no está vacío o reporta algún gap>4s → BLOCKER: "Hueco de ritmo >4s en [a,b] — viola la regla dura; rellénalo antes de entregar".
> 3. **Audio real:** re-transcribe el AUDIO DEL RENDER FINAL desde cero con
>    `ffmpeg -i <REEL-FINAL.mp4> -vn -ac 1 -b:a 64k -y /tmp/rev.m4a && bash ~/.claude/skills/reel-edita-vdl/scripts/transcribe-groq.sh /tmp/rev.m4a /tmp/rev-word.json`
>    y corre `verify-cut.py --media <REEL-FINAL.mp4> --transcript /tmp/rev-word.json`. Lee el texto entero: ¿el habla fluye natural?, ¿hay alguna repetición o frase cortada? Cualquier repetición audible → BLOCKER.
> 4. **Sincronía visual:** extrae frames del render (`ffmpeg -i <REEL-FINAL.mp4> -vf "fps=1/3" -y /tmp/qc_%03d.jpg`) y `Read` los frames; comprueba que cada gráfico/escena aparece cuando se dice lo que ilustra (no antes ni después). Desfases notables (>0.5s) → BLOCKER.
> 5. **Cold open (0-3s):** ¿el payoff/gancho se entiende y es legible **desde el frame 1**? El titular-hook arriba solo se permite durante el cold open (≤2s); si hay texto arriba DESPUÉS de entrar el cuerpo → BLOCKER. Si el cold open lleva imagen IA, ¿se ve cutre (texto basura, manos/ojos raros, render hiperbrillante)? → BLOCKER.
> 6. **Ritmo:** además del lint, en los tramos ágiles ¿hay ~5-7 cambios visuales/10s (ni lento <4, ni ruido >8)? ¿los tramos densos respiran con aire en vez de atropellarse a cortes? Desajuste claro → WARNING.
> 7. **Legibilidad y solapes:** textos que se salen, se pisan, ilegibles, o dos escenas a la vez → BLOCKER.
> 8. **Cero humo / datos:** ¿hay cifras/datos en pantalla (incluido el titular del cold open) que el audio NO dice (inventados)? → BLOCKER. (regla dura de VdL)
> 9. **Clichés IA:** píldoras de sección genéricas arriba ("EL PROBLEMA/LA SOLUCIÓN" con puntito), etc. → WARNING.
> 10. **Isotipo `<` (regla dura 2026-08-18):** el chevron **NO debe aparecer en NINGUNA parte** del cuerpo del
>     reel — ni sting en esquina, ni marca de agua, ni endcard, ni dentro de una escena. Si aparece y VdL no lo
>     pidió explícitamente para este vídeo → **BLOCKER**. Tampoco el nombre "Valor de Ley"/"VALOR DE LEY"
>     escrito en el cuerpo → BLOCKER. (Ojo: la CORTINILLA de cierre sí lleva el logotipo completo con el
>     chevron — eso es correcto y NO es blocker. Y "VdL" en un subtítulo, porque se dice en el audio, tampoco.)
> 11. **Cierre con cortinilla (regla dura 2026-08-18):** el reel **tiene que terminar con la cortinilla oficial**
>     de VdL (barrido lime → logotipo `valor de ley` sobre degradado navy/magenta, ~4s), unida con **disolución
>     cruzada** (no corte seco). Comprueba en los frames finales que está, que la disolución es suave, y que
>     **no corta ninguna palabra** (aísla el audio del tramo y confirma que la voz acabó antes). Si falta la
>     cortinilla, o hay un endcard de marca hecho a mano en su lugar, o la disolución pisa voz → **BLOCKER**.
> 12. **Miniatura:** el frame 0 debe ser un fotograma fuerte y asentado (no negro, no a mitad de transición)
>     y debe existir su `.jpg` al lado del final → si no, WARNING.
> 13. **Modo B (vídeo de proyecto):** cualquier dato real de cliente (empresa, persona, matrícula, email,
>     importe) o cualquier secreto visible (clave, token, URL interna con credenciales) → **BLOCKER**. Cifras
>     o claims que no estén en la fuente del proyecto → **BLOCKER**.
> 14. **Look IA y sistema de movimiento** (`10-motion-vdl.md` §7 y §2): recorre la lista negra con los
>     frames. Curvas fuera de la familia VdL, `bounce`/`elastic`, elementos que flotan/laten/respiran en
>     bucle, más de 3 golpes de pantalla completa (flash/shake/bombeo), la misma transición vistosa en cada
>     corte, layout de diapositiva (prueba anti-PowerPoint de `12-revision-visual.md` §3) → **WARNING**
>     (BLOCKER si son 3 o más o si es el gancho).
> 15. **Cortes vivos** (Modo B, o Modo A con 2+ escenas full-screen seguidas): `seam-gate.mjs verify` con
>     el `motion/ledger.json` → exit 0. Si falla, o no hay ledger en Modo B → **BLOCKER**. Comprueba también
>     el signo de Z en el cold open (dato que crece + cara que encoge = vector invertido → BLOCKER).
> 16. **Legibilidad real:** reduce 2-3 frames con texto a 480 px de ancho; lo que hay que leer debe leerse
>     y estar ≥ ~0.3 s/palabra en pantalla entero. Texto en "medio legible" → WARNING; ilegible → BLOCKER.
>
> Calcula también un radar `scores` 0-10 (enteros). Mantén PASS/FAIL como compuerta dura: el radar es informativo y alimenta el Loop de retención (correlacionar score con retención-3s), no sustituye los blockers.
> - `corte`: 10 si `verify-cut.py` sale exit 0 y la lectura real fluye limpia; baja con cada repetición, silencio o corte raro.
> - `ritmo`: `10 - nº de gaps>4s*4 - (1 si densidad media <4)`, limitado a 0-10.
> - `sincronia`: baja con desfases visual/audio >0.5s.
> - `legibilidad`: baja por textos fuera de sitio, solapes o safe zone rota.
> - `antihumo`: baja por datos inventados, clichés IA o afirmaciones que el audio no sostiene.
> - `motion`: 10 si cumple la familia de curvas, cortes vivos y cero idle; baja por cada punto del check 14.
>
> Devuelve SOLO este JSON:
> `{"verdict":"PASS|FAIL","scores":{"corte":N,"ritmo":N,"sincronia":N,"legibilidad":N,"antihumo":N,"motion":N},"blockers":["..."],"warnings":["..."],"notes":"resumen 1-2 frases"}`

## Regla de entrega

- `verdict == "PASS"` y `blockers == []` → se puede entregar.
- Cualquier otra cosa → arreglar y re-revisar. No mandar a VdL un reel con blockers.
- Cualquier gap>4s de `lint-timeline.py` es blocker de ritmo aunque el radar tenga buena nota.
- Sin cortinilla de cierre, o con isotipo no solicitado, **no se entrega** (reglas duras de marca).
- Los `warnings` se le comunican a VdL en el mensaje de entrega (no bloquean, pero se dicen).
