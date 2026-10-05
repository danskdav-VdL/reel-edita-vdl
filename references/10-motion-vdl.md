# 10-motion-vdl.md — El sistema de movimiento de VdL (MOTION.md)

> **Fuente de verdad del movimiento.** Manda sobre cualquier helper, receta o ejemplo antiguo del resto de
> referencias. Si algo de `02-motion-graphics.md` o `04-recetas.md` lo contradice, gana este archivo.
> Es la versión VdL (vertical, marca VdL, en español) de la doctrina con la que HeyGen hace sus propios
> lanzamientos (skills `motion-doctrine` + `cut-the-curve`, instaladas con `scripts/setup-capa-diseno.sh`),
> más lo que funcionó en el film de Staynex (2026-10-02) y valores medidos de vídeos de Apple.

**Por qué existe.** Lo que hace que un motion "parezca caro" no es el efecto, son dos decisiones aplicadas
en TODAS partes (HeyGen, `heygen-apple-motion/README.md`):
1. **Una sola familia de curvas.** Todo lo que llega usa la misma curva; todo lo que se va, su espejo.
   Nada lineal, nada que rebote con un `elastic` de serie. Como es una familia, hasta los movimientos que
   nadie afinó parecen del mismo vídeo.
2. **Vectores casados en cada corte.** Ninguna escena se para antes del corte y ninguna arranca desde
   parado después. Lo que sale aún va en movimiento cuando cambia el plano, y lo que entra llega ya
   lanzado, en el mismo eje y la misma dirección. Por eso parece una sola toma de cámara y no diapositivas.

---

## 1. Dos niveles de ambición (elige antes de montar)

| | **Modo A · reel a cámara** | **Modo B · pieza de motion** (vídeo de proyecto, lanzamiento, pieza de marca) |
|---|---|---|
| Quién manda | la voz y la persona | el movimiento |
| El motion | acompaña: rótulos, B-roll, encuadres. Nunca roba el protagonismo a la cara | es el espectáculo: "go all out" |
| Cortes | cortes secos entre encuadres de cámara (como Apple: ~92 % cortes) + **cut-the-curve** al entrar/salir de escenas a pantalla completa | **una toma continua**: cut-the-curve por defecto, match cuts y morphs, ledger obligatorio |
| Ledger + Seam Gate | solo si hay 2+ escenas full-screen encadenadas | **obligatorio** (§5) |
| Música | sin música (solo SFX), salvo que se pida | **partitura original** en rejilla de tempo (`plantillas/score-plantilla.py`) |
| Momentos estrella | 0-1 | 1-2 (un shader, una escena 3D, un morph largo) |

## 2. Tokens de movimiento (la familia VdL) — elige SOLO de aquí

| Token | GSAP | Duración | Para qué |
|---|---|---|---|
| `llega` | `power4.out` | héroe 0.4-0.8 s · palabra 0.13-0.20 s | toda entrada (≈ `cubic-bezier(0.23,1,0.32,1)` de Emil Kowalski) |
| `se-va` | `power4.in` | ≈ 75 % de su entrada (0.25-0.4 s) | toda salida (el espejo de `llega`) |
| `revela` | `expo.out` | 0.5-0.8 s | llegadas en Z (zoom-through inverso), un reveal grande |
| `costura` | lo genera `seam-stamp.mjs` (power3/4 in ↔ power4 out, expo.out en Z) | 0.34 + 0.42 s | cortes entre escenas (§4) |
| `recoloca` | **nudge curve** (3 tramos, §3) | 0.6-1.2 s | mover un grupo ya compuesto, reencuadrar la cámara (full↔PiP↔split) |
| `pop` | `back.out(1.4)` (máx. 1.7) | 0.3-0.4 s | SOLO chips/badges pequeños. Nunca titulares, nunca cifras |
| `ambiente` | `sine.inOut` | ciclos ≥ 12 s | SOLO el fondo liquid de marca (`estilo.md` §2) |

**Prohibidas:** `bounce.*`, `elastic.*`, `back.out` > 1.7, `linear`/`none` en movimiento (sí en barras de
progreso y en el tramo central del nudge), el `ease` por defecto, `power1`, y cualquier curva inventada
por escena. Elementos parecidos comparten curva + duración (nunca una pareja única por elemento).

**Reglas de tiempo** (doctrina + Apple + video-shotcraft):
- Una entrada sola ≤ 0.8 s. Un build más largo = varios elementos escalonados, no uno lento.
- Escalonado total ≤ 0.5 s (con 8+ elementos, aprieta o escalona solo los primeros). Entre palabras ~0.1 s
  (3 frames a 30 fps), entre letras ~0.03 s.
- **Nunca desde `scale(0)`**: entra desde 0.9-0.97 + opacidad, o con desplazamiento (`y` 40-80 px).
- **Pausa antes del clímax: 0.3-0.75 s** de quietud entre la acción y su resultado (la coma dramática).
- **Lo que se tiene que leer, se lee:** ~0.3 s por palabra desde que la línea está ENTERA en pantalla.
  Lo clave (cifra, claim, wordmark de cliente) **≥ 1 s quieto** al asentarse.
- **Primera versión = demasiado rápida.** Siempre. Interacciones de UI a velocidad de persona real
  (que se pueda seguir con el dedo). Ante la duda, un punto más lento.
- **La velocidad sale de la ACELERACIÓN, no de ir rápido.** Muchos elementos iguales entran "cada vez
  más rápido" (huecos ×0.84 por elemento) y al llenar, 0.5 s quietos.

## 3. Movimiento sostenido: nada respira, todo actúa

🔴 **Prohibido el relleno idle**: flotar, latir, respirar, "glow pulse", yoyos en bucle sobre contenido.
Se lee como "el vídeo está esperando". (Esto sustituye el antiguo `floatPiP`, los `#orbs` que laten y los
stickers que botan.) Si a una escena le sobran segundos, **falta historia, no meneo**. Cada tramo entre la
entrada y la salida se cubre con una de estas rutas (escríbela en el plan):

| Ruta | Qué es |
|---|---|
| **Revelado por fases** | retener contenido y pagarlo en cada beat de la voz: el plano gana información (por defecto con 2+ grupos) |
| **Cámara con intención** | un recorrido: abre amplio → viaja → llega al sujeto. Un push-in continuo del 4-8 % en UNA dirección durante un hold vale; un vaivén no |
| **UI que vive** | el producto hace su trabajo: avanza un progreso, cambia un estado, cuentan cifras |
| **Secuencia animada** | los elementos actúan el beat: una tarjeta se archiva, algo se arrastra, un resultado se ensambla |
| **Cursor que guía** | un cursor grande (`oversized-cursor`) lleva el ojo al disparador y su CLIC desencadena lo siguiente |

**Movimiento causal:** clic → aplastamiento → muelle → vuelo → impacto → rebote → revelado. El efecto
empieza EN el frame que lo causa, nunca "un poco después". Lo grande rebota lento, lo pequeño seco.

**El fondo liquid de marca** es la única capa ambiente permitida (lento, `sine`, sin protagonismo). No
cuenta como "movimiento de la escena": la escena necesita además una de las rutas.

**Nudge curve** (reencuadres y grupos que se apartan; en vez de `power3.inOut`, que "frena de golpe"):
```js
// mueve `sel` en la propiedad `prop` de `a` a `b` empezando en `t`, durante `d` segundos
function nudge(sel, prop, a, b, t, d){
  const D = b - a;
  tl.fromTo(sel, {[prop]: a},          {[prop]: a + D*0.10, duration: d*0.20, ease: "power3.in",  immediateRender:false}, t);
  tl.to(sel,     {[prop]: a + D*0.75,  duration: d*0.18, ease: "none"},       t + d*0.20);  // el arranque: aquí aparece lo nuevo
  tl.to(sel,     {[prop]: b,           duration: d*0.62, ease: "power4.out"}, t + d*0.38);  // cola larga ≥ 3× la rampa
}
```
**Waterfall entry** (llegada en cascada de un titular; `cut-the-curve` §6): opacidad BINARIA, desde abajo,
las palabras pesadas (`.em`) viajan más, cada hueco ×0.84 del anterior (acelera). Probado en el piloto:
```js
function waterfall(sel, t0, gap0){
  let t = t0, gap = gap0;
  gsap.utils.toArray(sel).forEach(el => {
    const heavy = el.classList.contains("em");          // las palabras en lime pesan más
    gsap.set(el, {y: heavy ? 76 : 48, autoAlpha: 0});
    tl.set(el, {autoAlpha: 1}, t);                      // binaria: nada de fundido en una llegada
    tl.to(el, {y: 0, duration: heavy ? 0.2 : 0.15, ease: "power4.out"}, t);
    t += gap; gap *= 0.84;
  });
  return t;                                             // cuándo ha llegado la última
}
// palabras como <span class="w">, con display:inline-block (si no, los transforms no hacen nada)
```
Para la cámara de Modo A: `nudge("#camera","scale",1,0.40,t,0.8)` + `nudge("#camera","x",0,284,t,0.8)` +
`nudge("#camera","y",0,470,t,0.8)` (PiP). Revela el contenido nuevo DURANTE el tramo central.

## 4. La ley del corte (cut-the-curve) y la corriente del vídeo

- **Ley del vector:** cómo sale la escena A decide cómo entra la B: **mismo eje, misma dirección,
  velocidad casada, corte a mitad de movimiento en los dos lados**. En Z la dirección es el SIGNO de la
  escala: si A se aleja (encoge), B también llega encogiendo (desde 1.25 → 1), nunca "creciendo desde
  pequeño" (es el error más común, porque crecer desde pequeño es la entrada por defecto).
- **La corriente:** cada pieza elige UNA dirección dominante. **VdL: IZQUIERDA** (avance neutro). Las
  demás están reservadas y significan algo: **ARRIBA** = conclusión/elevación · **Z hacia delante** =
  profundizar en la misma idea · **Z hacia atrás** = LLEGADA de algo grande (payoff) · **estallido de
  escala** = salir de un mundo. Nunca dos cortes seguidos en direcciones opuestas (ping-pong = error);
  un cambio de dirección necesita una causa visible (clic, impacto) o un cambio de capítulo.
- **Recorrido parcial:** ~12 % del cuadro, nunca salir entero de pantalla. En vertical 1080×1920:
  **x ≈ 130 px, y ≈ 230 px** (el stamp usa `xPercent/yPercent` 10-12, ya proporcional).
- **Desenfoque en Z:** 10 px en texto, 18-20 px en superficies a pantalla completa. Se desenfoca el
  WRAPPER, nunca los hijos ni un `<video>` directamente.
- **Presupuesto de transiciones:** 2-3 tipos por pieza, repetidos. Por defecto cut-the-curve en la
  corriente. Los efectos llamativos (shader, light leak, rack-focus) en **1-2 momentos** narrativos, nunca
  en cada corte ("es como poner en negrita cada palabra").
- **Golpes de pantalla completa** (flash, shake, bombeo de escala de todo el cuadro): **≤ 3 por pieza**,
  separados ≥ 16 tiempos de música, en los golpes más fuertes. El resto del ritmo, solo en la capa de
  elementos. Nada de cámara en mano (handheld shake) en piezas de producto.
- **Nunca crossfade entre dos layouts cargados** (doble exposición sucia): sale lo viejo, entra lo nuevo,
  o se pasa por el fondo.
- **Suelo del escenario opaco:** `#root { background: #00004b }`. Un corte a mitad de ventana deja la
  suma de opacidades < 1 y, sin suelo, aparece un destello BLANCO (`seam-craft`).
- **Portadores:** el ojo sigue objetos. El mejor corte entrega un objeto concreto a través del corte en
  la misma posición y velocidad (un cursor a mitad de trayecto, un contenedor que se encoge y encaja en el
  siguiente layout, una burbuja que se convierte en ticket — el match-cut de Staynex).

## 5. Ledger + Seam Gate (Modo B obligatorio; Modo A con 2+ takeovers encadenados)

Antes de animar la línea maestra, escribe **`motion/ledger.json`** (una fila por corte: tiempo, vector de
salida y de entrada, selectores, técnica). Esquema: `~/.claude/skills/motion-doctrine/references/seam-gate.md`.
```bash
MD=~/.claude/skills/motion-doctrine/scripts
node $MD/seam-stamp.mjs --ledger motion/ledger.json --write motion/index.html   # genera los cortes (pasan por construcción)
node $MD/seam-gate.mjs verify --ledger motion/ledger.json --project motion        # exit 0 = cortes vivos
node $MD/seam-gate.mjs probe --t <segundo> --project motion                       # quién se mueve en ese corte
```
- En `index.html` deja los marcadores `// <seams:auto>` y `// </seams:auto>` donde quieras el bloque.
- Escenas = capas a pantalla completa (`#esc-1`, `#esc-2`…) con `position:absolute;top:0;left:0`.
- Cualquier cambio en el primer/último segundo de una escena **reabre** su corte: vuelve a pasar el gate.
- Hand-made solo los match-cut/morph (`"type":"match-cut"` con `carrier`); el resto, estampado.
- Probado en Windows (parche en `scripts/parches/seam-gate-windows.py`; no deja procesos colgados).

## 6. Composición: un plano, una idea

- **Un héroe por plano** + 1-2 apoyos. Nada de "relleno para que no quede vacío" (ghost glyphs, tokens
  de fondo, métricas decorativas). Si falta información, añade historia, no decoración.
- **Una frase ≤ 5-6 palabras por plano.** Si un claim necesita más, son dos planos o es un visual.
  (Excepción: las maquetas de UI, que se leen como IMAGEN y deben ser fieles al producto real.)
- **Orden de atención:** la frase → el objeto principal → los detalles. Nunca al revés (un badge que
  aparece antes que su frase).
- **Lo que entra volando aterriza en un hueco real** del layout (se encaja, no flota encima).
- **Brillos y barridos de luz:** como mucho uno por plano, sobre el héroe, recortado a su `border-radius`.
- **Tamaño de texto que se lee** (medido en el frame renderizado, con escalas y perspectiva aplicadas):
  frases a leer ≥ 56 px de cuerpo efectivo, texto auxiliar ≥ 32 px; titulares 96-150 px; mayúsculas de
  un titular ~6-7 % del lado corto (≈ 72 px de altura de mayúscula). Texto que no está para leerse =
  textura (desenfocado/atenuado). No existe el "medio legible": o se lee, o se quita.
- **Zona segura vertical:** nada importante fuera de **y 360-1420** en piezas para Reels/TikTok, ni en
  los **120 px de la derecha** (botones de la app), ni en la franja inferior (`check --caption-zone`).
  En Modo A rige además la regla del micro y de la barbilla (`07-subtitulos.md`).
- **Tipografía:** Sora/Onest (marca), sentence case, peso 500-600 en titulares, tracking −0.015/−0.02 em,
  interlineado 1.04-1.08. Sin punto final automático en frases cortas. Contraste de pesos marcado (300 vs
  600), no 400 vs 700.

## 7. Lista negra del "look IA" (el revisor la aplica, `05-revisor.md` check 14)

| Delata IA | En su lugar |
|---|---|
| todo entra a la vez con un fade desde abajo de ~300 ms | escalonado irregular, entrada con 2-3 propiedades, familia VdL |
| fundidos de opacidad sueltos | opacidad + desplazamiento/escala/blur |
| holds muertos o congelados | una ruta de movimiento sostenido (§3) |
| flotar/latir/respirar en bucle | quitarlo: historia, no meneo |
| la misma transición vistosa en cada corte | cut-the-curve + 1-2 momentos estrella |
| flash/glitch/shake en cada corte fuerte | ≤ 3 golpes de pantalla completa por pieza |
| rebotes elásticos, `bounce` | `llega`/`se-va`; overshoot mínimo solo en chips |
| layout de diapositiva (kicker + título 2 líneas + cuerpo + 4 chips) | una frase ≤ 5 palabras + un objeto |
| píldoras "EL PROBLEMA / LA SOLUCIÓN" | estructura con ritmo y contenido |
| partículas, lens flares, ondas de choque, RGB split, glow en todo | prohibidos salvo UN momento elegido a propósito |
| emojis/stickers decorativos (👀🔥) | iconografía de línea VdL o nada |
| pantallazos quietos con zoom/pan | UI recreada con sus tokens reales y USADA (cursor, datos que se llenan) |
| cámara fija todo el vídeo | cambios de tamaño de plano (amplio ↔ cerrado) con intención |
| la misma energía en todas las escenas | alternar tensión y respiro; el final es el pico de energía |
| contadores que se pasan de su valor | overshoot solo en transformaciones espaciales, nunca en datos |

## 8. Ritmo de referencia (medido en 6 recaps de Apple, 30 fps — orientativo, no molde)

- Plano: mediana 1.9 s (p25 1.1 s · p75 3.5 s); el primero ~4.3 s; ~3.2 cortes cada 10 s con voz.
- Texto: en pantalla ~1.5 s; mantenido ~1.1 s; aparece **2 frames antes** de que se diga (J-cut).
- Entradas animadas: mediana 8 frames (0.27 s); desde escala 1.13 o 0.82; blur ~10 px; desplazamiento ~2 % del alto.
- Cámara: 38 % planos quietos · 35 % push/pull a ~4.5 %/s · 19 % paneo a ~2.6 % del cuadro/s.
- Audio: música ~120 BPM; voz ~3 palabras/s; música −12 dB bajo la voz.
- **El montaje sigue a la VOZ, no al beat:** solo ~1/3 de los cortes caen en un golpe de música. En
  piezas SIN voz (Modo B), en cambio, los cortes van a la rejilla del tempo (Staynex: todo en compases).

Fuentes: `heygen-com/hyperframes` (motion-doctrine, cut-the-curve, seam-craft, Apache-2.0) ·
`heygen-com/hyperframes-launches` · `IskakovDamir/apple-motion` (mediciones, MIT) · `emilkowalski/skills`
(MIT) · `Vincentwei1021/video-shotcraft` (aesthetic-rules, Apache-2.0) · `bangtutorial/bang-motion`
(anti-ppt, MIT) · film de Staynex (VdL, 2026-10-02).
