# 12-revision-visual.md — El bucle de autocrítica (antes de renderizar en alta)

Lo que separa un resultado "de portafolio" de uno correcto no es el primer intento: es **mirar los
fotogramas, puntuarlos con honestidad y arreglar lo peor, varias veces**, antes del render final. Esta fase
va entre la construcción (Fase 3) y el render high (Fase 4). La hace quien monta; el revisor independiente
de la Fase 5 sigue siendo obligatorio después.

## 1. Mirar (siempre con fotogramas, nunca "de memoria")

```bash
npx hyperframes check motion --at-transitions --caption-zone "x0=0;y0=.84;x1=1;y1=1;severity=error"  # 0 errores
npx hyperframes snapshot motion --at <cada beat asentado>,<mitad de cada transición>                  # -> contact-sheet.jpg
npx hyperframes snapshot motion --at <t> --zoom "#rotulo"        # recorte de alta densidad para leer letra pequeña
npx hyperframes compare motionA motionB --at <t> --labels A,B    # dos variantes lado a lado (decisiones de diseño)
```
Lee `snapshots/contact-sheet.jpg` con `Read`. Para la legibilidad en móvil, reduce un frame a 480 px de
ancho (`ffmpeg -i frame.png -vf scale=480:-1 m.png`) y léelo: si no se lee ahí, no se lee en el feed.

## 2. Puntuar (1-10, sin regalar notas)

| Criterio | 10 = | Se hunde si… |
|---|---|---|
| **Gancho** | en 2 s se entiende de qué va y apetece seguir | arranque lento, primer frame débil o negro |
| **Legibilidad móvil** | todo lo que hay que leer se lee a 480 px y aguanta ~0.3 s/palabra | texto pequeño, poco contraste, se va antes de leerse, en la zona de UI |
| **Calidad del movimiento** | familia VdL, cortes vivos, nada idle, causa→efecto | eases mezclados, rebotes, cosas que flotan, escenas que se paran antes del corte |
| **Variedad** | cambian tamaños de plano y ritmos; 2-3 transiciones repetidas con criterio | siempre el mismo plano, el mismo efecto en cada corte |
| **Composición** | un héroe por plano, orden frase → objeto → detalle | layout de diapositiva, relleno decorativo, todo a la vez |
| **Marca** | se reconoce VdL (liquid, Sora/Onest, lime) o la marca del cliente | colores/fuentes genéricas, look de plantilla |
| **Sincronía** | lo que se ve llega cuando se dice / cae en la rejilla de tempo | desfases > 0.5 s, cortes fuera de compás en Modo B |

**Arregla los 3 peores y vuelve a mirar.** Repite hasta que **todos los criterios estén en ≥ 8** (máx. 3
rondas; si no converge, presenta el estado y pregunta). Apunta las notas de cada ronda en `edicion/plan.md`.

## 3. Pruebas anti-PowerPoint (de `bang-motion`, adaptadas)

Congela un frame cualquiera y pregúntate:
1. ¿Podría ser una **diapositiva corporativa** sin cambiar nada? → falla, rehazlo.
2. ¿Sé **dónde mirar en 0.2 s**? → si no, sobran elementos.
3. Si oculto todo el texto, ¿el fondo sigue siendo bonito **pero no ruidoso**? → las dos cosas deben ser sí.
4. En cada transición, ¿se mueve algo **por la cámara o por un portador**, y no solo porque cada elemento
   se anima a sí mismo? → debe ser sí.
5. ¿Hay **un objeto que se queda** y viaja entre escenas (héroe > 60 % del tiempo en Modo B)? → si cada
   escena empieza de cero, es un deck en autoplay.

## 4. Compuertas mecánicas (las que no dependen del gusto)

| Compuerta | Comando | Cuándo |
|---|---|---|
| Layout, contraste, franja de UI | `npx hyperframes check …` (arriba) | siempre, 0 errores |
| Ritmo (sin huecos > 4 s) | `python3 scripts/lint-timeline.py motion/index.html` | Modo A |
| Cortes vivos y casados | `node ~/.claude/skills/motion-doctrine/scripts/seam-gate.mjs verify --ledger motion/ledger.json --project motion` | Modo B siempre; Modo A con 2+ takeovers seguidos |
| Cortes en el beat (AVISO) | `node scripts/sync-check.mjs AF/<final>.mp4 --cues-file edicion/cortes.json` | piezas con música; con whips/motion blur da falsos "OFF-BEAT" de ~100 ms |
| Corte de audio (Modo A) | `verify-cut.py` | antes de animar (Fase 1) |

## 5. Fallos típicos que aparecen en la 1.ª ronda (del piloto, 2026-10-02)

- **Hueco en blanco dentro de una tarjeta**: un elemento oculto (`autoAlpha:0`) sigue reservando su sitio.
  Lo que llega después sácalo del contenedor y que **aterrice en su hueco** (burbuja bajo la tarjeta).
- **Cursor que "casi" pulsa**: la punta del SVG no es su esquina (con el arrow de 96 px, la punta está a
  ~16,8 px del origen). Mide en el snapshot del frame del clic y ajusta.
- **Al recolocar un grupo hacia arriba tapa el rótulo** (`text_occluded`): el rótulo sale (`se-va`) ANTES.
- **Texto final en la franja de UI** (`caption_zone_collision`): sube el remate a la zona segura (y ≤ 1420).
- **Cursor que sale por encima de lo que acaba de aparecer**: que salga en horizontal, por donde vino.
- `sync-check.mjs` marca **STARTLE** en el golpe que sigue al silencio deliberado de medio compás: es la
  "coma dramática" buscada; valídalo de oído, no lo quites para contentar al script.

## 6. Pedir y dar feedback por rangos

Cuando el usuario (o tú) corrija, hazlo por **rangos de tiempo concretos** ("8.0-9.5 s: la tarjeta llega
antes que su frase") y no con adjetivos ("más dinámico"). Tras cualquier cambio de timing: re-pasa el gate
de los cortes afectados y **re-temporiza la tabla de SFX entera** (`03-sfx-y-qc.md`).
