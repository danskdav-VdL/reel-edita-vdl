> ⚙️ DOC DE MOTOR (universal). Copiado tal cual por forja-reel. Los colores que veas en los
> ejemplos son PLACEHOLDERS: tu paleta real vive en `references/estilo.md` y sobreescribe el
> `:root`. No hay estilo de nadie embebido aquí, solo la técnica.
>
> 🔴 **El MOVIMIENTO (curvas, duraciones, cortes, qué está prohibido) lo manda `10-motion-vdl.md`.**
> Este archivo es la mecánica de HyperFrames (capas, cámara, helpers). Si algo de aquí lo contradice,
> gana `10-motion-vdl.md`.

# Fases 2-3 — Motion graphics (Hyperframes)

Solo se entra aquí con el corte APROBADO (compuerta Fase 1). Re-transcribe el corte aprobado para tener los timestamps FINALES exactos y mapea cada animación a ellos.

## Arranque (comando probado — evita cuelgues)

```bash
export HYPERFRAMES_SKIP_SKILLS=1   # evita que init se cuelgue comprobando skills contra GitHub
npx hyperframes init motion --video corte-final.mp4 \
  --skip-transcribe --example blank --resolution portrait --non-interactive
```
`--skip-transcribe` (ya tenemos el transcript de Groq; si no, init lanza Whisper y descarga modelo →
cuelgue) · `--example blank` · `--resolution portrait` (1080×1920). Verifica `data-duration` = duración del corte.
Copia los assets de marca que uses (isotipo, fuentes) a `motion/assets/` y referéncialos **relativos**
(el render NO resuelve rutas `file://` externas; da error `missing_local_asset`).

**Capa de diseño (skills de HeyGen, instaladas con `scripts/setup-capa-diseno.sh`).** `HYPERFRAMES_SKIP_SKILLS=1`
solo evita que `init` se cuelgue comprobando versiones; las skills ya están instaladas. Antes de animar,
carga directamente (sin pasar por la entrevista de `/hyperframes` ni sus workflows: esta skill manda):
`motion-doctrine` (ley de cortes y movimiento) → `cut-the-curve` (técnicas) → `hyperframes-animation`
(reglas atómicas y blueprints) → `hyperframes-registry` (catálogo, `11-catalogo-y-recetas.md`). Con cursor:
`oversized-cursor`. Modo B: también `hyperframes-creative` (dirección de arte) y `hyperframes-core`.

## Operativa probada (reglas del runtime Hyperframes)

- **Props animables por GSAP:** el linter usa una LISTA NEGRA, no una lista blanca: `filter` (blur),
  `clipPath` (máscaras, iris, wipes), `strokeDashoffset` (trazos) son válidos (`hyperframes-core`,
  determinism-rules). Prefiere `transform` + `opacity` por rendimiento. **La cámara, SOLO transform**
  (`scale`/`x`/`y`/`opacity`): `top/left/width/height` en `#camera` los bloquea `check`
  (`gsap_non_transform_motion`). Nunca `filter` directamente sobre un `<video>`: sobre su wrapper.
- **Cada elemento con timing** necesita `class="clip"` + `data-start` + `data-duration` + `data-track-index`
  (z-order por track). El `<video>` es el elemento con timing; **no lo anides** dentro de otro elemento
  con `data-start` (congela el vídeo) — mételo en un wrapper SIN timing y anima el wrapper.
- **Timeline** `paused:true`, registrado en `window.__timelines["<composition-id>"]` (el del scaffold, p.ej. `"main"`).
- **Sin solapes en la misma pista:** dos clips en el mismo `data-track-index` no pueden solaparse en el tiempo
  (los subtítulos word-level: recorta la duración de cada uno para no pisar el siguiente).
- Corre `npx hyperframes lint` (0 errores) y `validate` antes de renderizar. Render: `--quality draft` para QC, `high` para entregar.

## Patrón de REVELADO (entradas sutiles sincronizadas, no “todo de golpe”)

Los elementos internos de una escena B-roll **NO** deben aparecer todos a la vez. Dales estado inicial
oculto (`.rv { opacity:0 }`) y revélalos con GSAP **cuando el narrador menciona cada uno**, con entrada
sutil (fade + `y` + `scale`), no un simple corte:
```js
const rev=(sel,t,o={})=>tl.fromTo(sel,{opacity:0,y:(o.y??24),scale:(o.s??0.94)},
          {opacity:1,y:0,scale:1,duration:(o.d??0.42),ease:(o.e??"power4.out")},t);   // token `llega`
```
Las cifras/keywords (p.ej. un “30-50”, un precio) entran **en el segundo en que se dicen**, no al abrir la escena.

## Coordinación de ZONAS (para que nada choque)

- **Escenas B-roll → mitad superior** (`top:150px; height:~820px`), dejando libre el pecho.
- **Subtítulos → altura del pecho, por DEBAJO de la cara** (ver `07-subtitulos.md`, regla dura).
- **PiP → esquina abajo-dcha, pequeño** (`scale ~0.30`), despejado de subtítulos y escena.
- **Cámara FULL cuando NO hay escena B-roll** que mostrar: si un tramo solo tiene voz sin visual, la
  persona vuelve a pantalla completa (nunca PiP sobre un fondo vacío). PiP/split solo mientras hay B-roll.
- **Split arriba/abajo** (3er encuadre): cámara a `scale ~0.5` anclada en su mitad (mueve con `y`; abajo por
  defecto) + visual/B-roll en la otra mitad; divisoria fina lime; **subtítulos en la franja de la cámara**,
  nunca sobre su cara. Solo transform (`scale`/`x`/`y`), nunca `top/left`. Alterna full ↔ PiP ↔ split.
- **Emojis al mínimo** (`emoji_level=min` por defecto): usa **iconografía limpia/techy** (glifos de línea,
  `>`, `#`, flechas, números de paso) + Sora + acento lime. **Nada de caritas ni emojis coloridos** ("playschool").

## Transiciones cámara↔escena SIN restos (linger)

Al volver de una escena full-screen a la cámara, los chips de la escena NO deben quedar visibles
mientras la persona reaparece. Regla:
- Entra/sal de los takeover full-screen con **corte instantáneo** (`tl.set(sel,{opacity:0/1},t)`),
  **nunca crossfade del contenedor** mientras la cámara aparece.
- **Resetea los elementos hijos** de la escena al salir (`tl.set(sel+" .rv",{opacity:0},tSalida)`) para
  que no queden "encendidos" si la escena se reutiliza o para evitar frames fantasma.
- Para ENTRAR/SALIR de una escena a pantalla completa usa **cut-the-curve en la corriente** (izquierda):
  la escena sale acelerando ~12 % hacia la izquierda y lo siguiente entra ya lanzado desde la derecha
  (`10-motion-vdl.md` §4). Con 2+ escenas full-screen encadenadas, ledger + `seam-stamp` + gate (§5).
- Un `#flash` blanco corto (0.05-0.08s) cuenta como **golpe de pantalla completa**: ≤ 3 por pieza, solo en
  los momentos más fuertes. No es la forma por defecto de "dar punch" a un corte.

## Isotipo VdL — 🔴 NO se anima (no se pone)

**No montes stings de isotipo.** Desde 2026-08-18 el chevron `<` no va en el vídeo: ni en esquina, ni
en el endcard, ni dentro de una escena. La marca la pone la **cortinilla de cierre**, que se pega en
post (`estilo.md` §8, `scripts/cierre.sh`) y no forma parte de este timeline.

Si VdL lo pide explícitamente para un vídeo concreto: incrusta el SVG de `BRAND_DIR` tal cual, entrada
y salida rápidas (~0.5-1s), **nunca sobre el rostro ni sobre los subtítulos**, nunca permanente.

Consecuencia práctica para el ritmo: el beat que antes rellenaba un sting ahora se cubre con un rótulo
lower-third, un cambio de encuadre o un reveal de escena (ver `04-recetas.md`).

## Lint de ritmo: beats = llamadas `tl.*` con tiempo NUMÉRICO literal

`lint-timeline.py` solo cuenta los beats de `tl.to/from/fromTo` **directos con tiempo numérico literal**.
Los reveals hechos con un helper (`rev(sel,t)` donde `t` es variable) **NO los cuenta** → marca "gaps >4s"
fantasma. Solución: **emite los beats como líneas `tl.fromTo(..., <número>)` directas** (el generador
sustituye el número). Así el lint mide bien y no persigues huecos que no existen.

## Subtítulos quemados en el bruto (¡ojo!)

Si el material de origen trae subtítulos incrustados (a veces solo en algunas tomas), NO añadas los
tuyos encima (saldrían dobles). Opciones: tápalos con una banda de marca (navy, degradado) en ese tramo,
o pide clips limpios. Detecta esto mirando frames del corte antes de montar.

---

Reescribe `motion/index.html` en vertical: root `data-width="1080" data-height="1920"`, `data-duration` = duración del corte.

Antes de escribir, lee (una vez) de la skill `hyperframes-creative`: `references/house-style.md` y `references/video-composition.md` (reglas de vídeo que pisan los instintos de web: llenar el frame, escalas grandes, color presente). Ojo: donde digan "movimiento constante", léelo como las rutas de `10-motion-vdl.md` §3 (nada idle).

## Sistema de capas (z-index)

- `#broll` (z:2): escenas B-roll a pantalla completa, `opacity:0` por defecto.
- `#camera` (z:5): el vídeo. **Va POR ENCIMA del B-roll.**
- `#ov` (z:10): overlays (rótulos, chips, datos). (Ya no hay `#orbs` que laten ni stickers: movimiento
  idle prohibido, `10-motion-vdl.md` §3.)
- `#br_teaser` (z:13) y `#flash` (z:14): hook y destellos de transición.

⚠️ **Gotcha crítico:** el B-roll está DEBAJO de la cámara. Si la cámara está a pantalla completa, **tapa el B-roll**. Para que un B-roll se vea, la cámara DEBE estar en PiP (esquina). Cada escena B-roll va acompañada de `camPiP()`. (Un diagrama pensado como "overlay full-frame" no se verá si la cámara sigue full.)

## La cámara: SOLO transform (regla dura, la impone el linter)

🔴 **El linter `npm run check` BLOQUEA animar `top/left/width/height` en la cámara** (`gsap_non_transform_motion`:
esas props se redondean a píxel entero y tiemblan en la captura frame-a-frame). Anima la cámara **solo con
`scale` / `x` / `y` / `opacity`**. (El ejemplo de abajo con layout es HISTÓRICO — NO lo uses.)

```js
// Reencuadres con la NUDGE CURVE de 10-motion-vdl.md §3 (arranque suave → tramo rápido → cola larga):
// se nota el movimiento, no "frena de golpe" como power3.inOut. Lleva el estado actual en CAM.
const CAM = {scale:1, x:0, y:0};
function camTo(t, to, d=0.8){
  for (const p of ["scale","x","y"]) if (to[p] !== CAM[p]) nudge("#camera", p, CAM[p], to[p], t, d);
  Object.assign(CAM, to);
}
const camFull  = t => camTo(t, {scale:1,    x:0,   y:0});
const camPiP   = t => camTo(t, {scale:0.40, x:284, y:470});   // esquina abajo-dcha
const camSplit = t => camTo(t, {scale:1.12, x:0,   y:900});   // rostro abajo (R7)
function camHide(t){ tl.set("#camera",{opacity:0},t); }        // takeover: corte limpio (nunca fantasma)
function camShow(t){ tl.set("#camera",{opacity:1},t); }
```
(`nudge()` está en `10-motion-vdl.md` §3; cópialo al script de la composición.)
El zoom interno (push-in/`snap`) va en el wrapper hijo `#vidzoom` con `transform: scale` (máx. 3 snaps/reel).
`flash`/reveals con `fromTo` → usa **`immediateRender:false`** (si no, el estado `from` se aplica en t=0 y
p.ej. un `#flash` blanco lava de blanco todo el arranque).

Snap-zoom en palabras clave (en tramos full-frame), sobre `#vidzoom`, sin solaparse en el tiempo:
```js
function snap(t){ tl.to("#vidzoom",{scale:1.08,duration:0.16,ease:"power4.out"},t); tl.to("#vidzoom",{scale:1.0,duration:0.5,ease:"power4.out"},t+0.36); }
```
**El track de escala de `#vidzoom` es uno solo**: ordena reveal/push/snap por tiempo y que NO se solapen (dos tweens sobre `scale` a la vez = conflicto). Durante PiP, deja `#vidzoom` en 1.0.

## Sistema de estilo (TikTok punchy, marca de VdL)

```css
:root{ --violet:#aae05a; --blue:#00004b; --amber:#c865d1; --green:#3a2770; --red:#b41e82; }
/* Paleta VdL. Fuente de verdad = references/estilo.md. Mapeo a los slots del motor:
   --violet = ACENTO principal = lime #aae05a · --red = magenta #b41e82 (co-acento) ·
   --blue = navy base #00004b · --green = violeta transición #3a2770 · --amber = lila bloom #c865d1. */
/* fuentes: Sora (display/titulares, 300/600) + Onest (texto/cuerpo, 300/500). Ver estilo.md. */
/* fondo: NUNCA color plano. Degradado LIQUID ANIMADO de marca (navy→violeta→magenta→lime), ver estilo.md. */
```
- Chips: fondo oscuro `rgba(20,16,31,.9)`, borde de acento 2.5px, sombra, peso 800/900, 52-80px. Sobre fondo movido necesitan ese fondo+borde para legibilidad.
- **Posición de títulos/chips = altura del micro, NO abajo.** En redes la franja inferior la come la descripción/UI. Ancla el contenedor en `top:1040px` (un poco por debajo del centro, sobre el pecho/micro), nunca `bottom:180px`. La cara (~y300-1000) queda libre.
- **NO pongas píldoras de sección arriba** ("EL PROBLEMA / LA SOLUCIÓN" con puntito de color). Es un cliché de IA y delata que el vídeo está hecho con IA — VdL lo quiere fuera. Si necesitas dar estructura, hazlo con el ritmo y los chips de contenido, no con etiquetas-capítulo genéricas.

## Texto cinético (chips palabra a palabra)

Envuelve cada palabra en `<span class="w">` y la clave en `<span class="w em v">PALABRA<span class="ul"></span></span>` (subrayado animado). El chip entra como caja + las palabras en stagger + el subrayado barre:
```js
function kpop(sel,tin,tout,opt={}){
  tl.fromTo(sel,{opacity:0,y:opt.fromY??52,scale:opt.fromScale??0.94},{opacity:1,y:0,scale:1,duration:0.34,ease:opt.ein??"back.out(1.4)"},tin); // `pop` (chip)
  tl.fromTo(sel+" .w",{opacity:0,y:16},{opacity:1,y:0,duration:0.18,stagger:0.06,ease:"power4.out"},tin+0.07);         // `llega`
  tl.fromTo(sel+" .ul",{scaleX:0},{scaleX:1,duration:0.3,ease:"power4.out"},tin+0.3);
  tl.to(sel,{opacity:0,y:-26,scale:0.97,duration:0.26,ease:"power4.in"},tout);                                           // `se-va`
}
```

## Helpers de motion ampliados (v10 — vocabulario extendido)

Todos estos helpers son deterministas, GPU-safe (`transform`/`opacity`/`filter`/`clip-path`) y están pensados para 1080×1920 con rótulos a la altura del micro.

> ⚠️ Son anteriores al sistema de `10-motion-vdl.md`. Úsalos con sus curvas de la familia VdL y con cupo:
> **`flashCut`, `shake` y `burstLines` cuentan como golpes de pantalla completa (≤ 3 por pieza en total)**;
> `burstLines` (ráfaga) solo en UN momento elegido. Antes de usar uno, mira si el catálogo tiene algo
> mejor (`11-catalogo-y-recetas.md`).

### `wipe(sel, tin, tout)`
Revela un rótulo con máscara izquierda→derecha y barra de luz; úsalo para claims, titulares y nombres de herramienta.

Markup opcional para la barra:
```html
<div id="title" class="wipe-title">TEXTO CLAVE <span class="sweep"></span></div>
```

```js
function wipe(sel, tin, tout){
  // técnica inspirada en OpenMontage wipe, reescrita
  tl.set(sel,{opacity:1,clipPath:"inset(0 100% 0 0)"},tin);
  tl.to(sel,{clipPath:"inset(0 0% 0 0)",duration:0.42,ease:"power4.out"},tin);
  tl.fromTo(sel+" .sweep",{x:"-120%",opacity:0.95},{x:"120%",opacity:0,duration:0.42,ease:"power4.out"},tin);
  tl.to(sel,{opacity:0,duration:0.24,ease:"power4.in"},tout);
}
```

### `typeIn(sel, tin, opt)`
Tecleo char a char sin reescribir contenido; úsalo en terminales, comandos, URLs y frases cortas.

Markup requerido:
```html
<div id="cmd"><span class="ch">n</span><span class="ch">p</span><span class="ch">m</span><span class="caret">_</span></div>
```

```js
function typeIn(sel, tin, opt={}){
  // técnica inspirada en OpenMontage typewriter, reescrita
  const step = opt.step ?? 0.04;
  const repeats = Math.max(0, Math.min(opt.repeat ?? 6, 24));
  const chars = gsap.utils.toArray(sel+" .ch");
  tl.set(sel+" .ch",{opacity:0},tin);
  chars.forEach((ch,i)=>tl.set(ch,{opacity:1},tin+i*step));
  tl.fromTo(sel+" .caret",{opacity:1},{opacity:0,duration:0.16,yoyo:true,repeat:repeats,ease:"none"},tin);
}
```

### `flashCut(t, fromSel, toSel)`
Cambia de escena ocultando el corte bajo un flash blanco; úsalo para pasar de problema a solución o de cámara a B-roll.

Requiere el `#flash` estándar:
```html
<div id="flash"></div>
```

```js
function flashCut(t, fromSel, toSel){
  // técnica inspirada en OpenMontage flash-cut, reescrita
  tl.set("#flash",{opacity:1},t);
  tl.set(fromSel,{opacity:0},t);
  tl.set(toSel,{opacity:1},t);
  tl.to("#flash",{opacity:0,duration:0.12,ease:"power2.out"},t+0.03);
}
```

### `whipOut(sel, t)`
Saca una capa con whip-pan y blur; úsalo en hypercuts o para retirar un visual con energía.

```js
function whipOut(sel, t){
  // técnica inspirada en OpenMontage hypercut-whip, reescrita
  tl.to(sel,{x:1300,filter:"blur(30px)",opacity:0,duration:0.18,ease:"power4.in"},t);
}
```

### `burstLines(t, opt)`
Líneas manga radiales para impactos; úsalo solo en beats fuertes, punchlines y cambios de sección energéticos.

Markup requerido (18 líneas, centradas a la altura del micro):
```html
<div id="burstlines">
  <i class="bl" style="--r:0deg"></i><i class="bl" style="--r:20deg"></i><i class="bl" style="--r:40deg"></i>
  <i class="bl" style="--r:60deg"></i><i class="bl" style="--r:80deg"></i><i class="bl" style="--r:100deg"></i>
  <i class="bl" style="--r:120deg"></i><i class="bl" style="--r:140deg"></i><i class="bl" style="--r:160deg"></i>
  <i class="bl" style="--r:180deg"></i><i class="bl" style="--r:200deg"></i><i class="bl" style="--r:220deg"></i>
  <i class="bl" style="--r:240deg"></i><i class="bl" style="--r:260deg"></i><i class="bl" style="--r:280deg"></i>
  <i class="bl" style="--r:300deg"></i><i class="bl" style="--r:320deg"></i><i class="bl" style="--r:340deg"></i>
</div>
```

```css
#burstlines{position:absolute;left:540px;top:1040px;width:1px;height:1px;z-index:12;pointer-events:none}
#burstlines .bl{position:absolute;left:-3px;top:-260px;width:6px;height:520px;background:linear-gradient(to top,rgba(255,194,61,0),rgba(255,194,61,.9));transform:rotate(var(--r)) scaleY(0);transform-origin:50% 100%;border-radius:999px}
```

```js
function burstLines(t, opt={}){
  // técnica inspirada en OpenMontage radial-burst-lines, reescrita
  tl.fromTo("#burstlines .bl",{scaleY:0,opacity:opt.opacity ?? 0.9},{scaleY:1,opacity:0,duration:0.42,ease:"expo.out",stagger:0},t);
}
```

### `shake(t, opt)`
Sacudida de impacto con amplitud decreciente sobre `#vidzoom`; úsalo en tramos full-frame y no durante PiP.

```js
function shake(t, opt={}){
  // técnica inspirada en OpenMontage screen-shake, reescrita
  const amps = opt.amps ?? [-24,20,-15,11,-7,4,-2,0];
  amps.forEach((a,i)=>tl.to("#vidzoom",{x:a,y:a*0.5,duration:0.05,ease:"none"},t+i*0.05));
  tl.to("#vidzoom",{x:0,y:0,duration:0.01,ease:"none"},t+amps.length*0.05);
}
```

### `slotReveal(sel, t, value, opt)`
Cifra/precio que cuaja tipo tragaperras; úsalo para números de negocio, precios, métricas y comparativas.

Markup requerido:
```html
<div id="price"><span class="digit">0</span><span class="digit">0</span><span class="digit">0</span><span class="underline"></span></div>
```

```js
function slotReveal(sel, t, value, opt={}){
  // técnica inspirada en OpenMontage slot-machine-reveal, reescrita
  const DIGITS = "0123456789";
  const chars = String(value).split("");
  const nodes = gsap.utils.toArray(sel+" .digit");
  const spins = opt.spins ?? 18;
  const proxy = {p:0};
  tl.to(proxy,{p:1,duration:opt.duration ?? 0.6,ease:"power4.out",onUpdate:()=>{
    nodes.forEach((node,i)=>{
      const finalChar = chars[i] ?? "";
      const lockAt = 0.62 + i*0.06;
      if (proxy.p >= lockAt || !/\d/.test(finalChar)) {
        node.textContent = finalChar;
      } else {
        node.textContent = DIGITS.charAt(Math.floor((proxy.p*spins+i*3)*10)%10);
      }
    });
  }},t);
  nodes.forEach((node,i)=>tl.fromTo(node,{scale:1},{scale:1.12,duration:0.08,yoyo:true,repeat:1,ease:"power2.out"},t+0.48+i*0.04));
  tl.fromTo(sel+" .underline",{scaleX:0,opacity:0.9},{scaleX:1,opacity:1,duration:0.28,ease:"power4.out"},t+0.48);
}
```

### `focusIn(sel, tin, tout)`
Entrada/salida blur-resolve tipo focus pull; úsalo en rótulos sobrios, citas y palabras clave.

```js
function focusIn(sel, tin, tout){
  // técnica inspirada en OpenMontage blur-resolve, reescrita
  tl.fromTo(sel,{filter:"blur(18px)",opacity:0,scale:1.06},{filter:"blur(0px)",opacity:1,scale:1,duration:0.4,ease:"power4.out"},tin);
  tl.to(sel,{filter:"blur(12px)",opacity:0,duration:0.3,ease:"power4.in"},tout);
}
```

### `fillWord(sel, tin)`
Rellena una palabra desde contorno a sólido; úsalo para la palabra clave de una frase.

Markup requerido:
```html
<span id="kw" class="fillword"><span class="outline">FUTURO</span><span class="fill">FUTURO</span></span>
```

```css
.fillword{position:relative;display:inline-block;font-family:Inter,sans-serif;font-weight:900}
.fillword .outline{color:transparent;-webkit-text-stroke:2px var(--violet)}
.fillword .fill{position:absolute;inset:0;color:var(--violet);clip-path:inset(100% 0 0 0)}
```

```js
function fillWord(sel, tin){
  // técnica inspirada en OpenMontage outline-to-fill, reescrita
  tl.fromTo(sel+" .fill",{clipPath:"inset(100% 0 0 0)"},{clipPath:"inset(0% 0 0 0)",duration:0.5,ease:"power4.out"},tin);
}
```

### `iris(t, dir, opt)`
Apertura/cierre circular para transición de sección; úsalo sobre una escena u overlay, con anillo opcional.

Markup opcional para el anillo:
```html
<section id="scene"><span class="iris-ring"></span></section>
```

```js
function iris(t, dir, opt={}){
  // técnica inspirada en OpenMontage iris-open, reescrita
  const sel = opt.sel ?? "#iris";
  const from = dir === "open" ? "circle(0% at 50% 50%)" : "circle(75% at 50% 50%)";
  const to = dir === "open" ? "circle(75% at 50% 50%)" : "circle(0% at 50% 50%)";
  tl.fromTo(sel,{clipPath:from},{clipPath:to,duration:opt.duration ?? 0.5,ease:"expo.out"},t);
  tl.fromTo(sel+" .iris-ring",{scale:0.2,opacity:0.85},{scale:1.35,opacity:0,duration:opt.duration ?? 0.5,ease:"expo.out"},t);
}
```

## Vocabulario de easings

Ya no vive aquí: usa SOLO los tokens de `10-motion-vdl.md` §2 (`llega` power4.out · `se-va` power4.in ·
`revela` expo.out · `costura` estampada · `recoloca` nudge curve · `pop` back.out(1.4) solo chips ·
`ambiente` sine solo el fondo). `bouncy`/`back.out(2.4)` y los floats `sine` sobre contenido quedan prohibidos.

## Hook (0-3s) — lo más importante

Los 3 primeros segundos deciden el scroll. Movimiento inmediato. Patrón validado: **teaser del dato más bestia a pantalla completa que estalla y revela la cara**:
- `#br_teaser` (z:13) full-frame con el dato gigante (ej. "100.000 ⭐ / ¿en una semana?") que LLEGA en Z
  (`revela`: `scale 1.25→1`, `blur 10→0`, `expo.out` 0.5s) y la pregunta en `pop`.
- A ~1.2-1.5s (que se haya podido leer) **corte en Z con el signo casado** (inverse zoom-through): el dato
  se ALEJA (`scale 1→0.8`, `blur 0→10`, opacidad lineal, `power3.in` 0.2s) y la cámara llega también
  alejándose (`#vidzoom` `scale 1.25→1.0`, `expo.out` 0.5s). ❌ Nunca "el dato crece hacia cámara y la cara
  entra encogiendo" (vector invertido: el error nº 1 de la doctrina). Sin glitch-shake.
Alternativas si encaja mejor: slam tipográfico palabra-a-palabra, o micro-tráiler de 0.8s con flashes de las mejores escenas. Decide con VdL si dudas.

## B-roll diseñado (catálogo, adáptalo al contenido)

Cada uno full-frame con fondo de marca y **un héroe + 1-2 apoyos** (`10-motion-vdl.md` §6): nada de
relleno decorativo (ghost glyphs, tokens de fondo, métricas inventadas). Si el plano se ve vacío, falta
historia (revela por fases, mueve la cámara con intención), no decoración. Cámara en PiP o fuera. Ejemplos usados:
- **Tarjeta de repo/dato**: card con contador animado (count-up vía proxy `{v:0}`→objetivo + `onUpdate` `toLocaleString('es-ES')`), badge, barras `scaleY`, pills.
- **Chat de IA que falla**: burbujas (user/bot), puntos de "escribiendo", ventana de app que glitchea en rojo (errores tipo `TypeError`, `build failed`). Buen recurso para el "problema".
- **Terminal en vivo**: ventana `spec-kit — zsh` que va escribiendo comandos uno a uno (cada línea entra con slide + check verde + tick SFX, cursor que parpadea con `repeat` finito). Pieza central para enumeraciones/pasos.
- **Reveal/sting**: logo gigante + kicker + badges.
- **Diagrama de flujo**: nodos + flecha (A → B).
- **Rejilla**: grid 2×2 con checks que encajan.
- **Endcard CTA**: "PRUÉBALO" + URL + @handle.

Rellena el hueco inicial de un B-roll con algo sincronizado al audio (ej. si nombra herramientas, que aparezcan como chips mientras las dice).

## J-cuts / L-cuts (no cambies escena "a hachazos")

El corte de audio está pegado sin pausas, pero las **escenas/B-roll no tienen por qué cambiar exactamente en el límite de frase**. Para que fluya:
- **J-cut** (visual entra ANTES que su audio): empieza a revelar la escena/chip ~0.15-0.3s antes de que VdL diga la palabra que ilustra → el ojo ya está ahí cuando llega la voz.
- **L-cut** (visual sale DESPUÉS): mantén la escena anterior ~0.15-0.3s sobre el inicio de la frase siguiente antes de transicionar.
- Solapa así las entradas/salidas (`kpop` in un pelín antes del timestamp, out un pelín después) en vez de alinear todo al milisegundo del corte. Alinear cada cambio exacto al límite de frase es lo que hace que un talking-head se sienta troceado.

## Transiciones y ambiente

- Corte por defecto: **cut-the-curve en la corriente** (izquierda), 2-3 tipos de transición por pieza.
- `flash()` / glitch-shake: **solo** dentro del cupo de ≤ 3 golpes de pantalla completa (p. ej. UNA escena
  tipo "error"). Nunca como puntuación de cada corte.
- ❌ Orbs que laten, stickers (👀🔥🥄), floats: prohibidos (movimiento idle / look playschool).
- El ambiente lo da el fondo liquid de marca; la vida de cada escena, una ruta de `10-motion-vdl.md` §3.

## Check — gate unificado de Hyperframes (0.8.x)

```bash
npx hyperframes check motion --at-transitions \
  --caption-zone "x0=0;y0=.84;x1=1;y1=1;severity=error"   # franja de UI de Reels/TikTok: nada de texto ahí
npx hyperframes snapshot motion --at 1.8,5.5,9.8           # PNG + contact-sheet.jpg para revisar con Read
```
Se **suma** a `validate` + `inspect` + `lint-timeline.py` (no los sustituye).

**Gotchas reales:**
- **Capas que salen de cuadro** siguen "visibles" para el comprobador → falsos errores de contraste.
  Solución: `tl.set(capa, {opacity:0}, fin_de_transición)`.
- **Mockups con `overflow:hidden`** (móvil con pantallas que se deslizan dentro) → `text_occluded` falso. El
  opt-out solo vale en el propio elemento de texto, no se hereda:
  `document.querySelectorAll("#phone *").forEach(e=>e.setAttribute("data-layout-allow-occlusion",""))`
  (solo tras verificar a ojo con `snapshot`).
- **Titulares con interlineado ≤1.0** → `content_overlap`. Sube a ~1.04 o marca la línea con `data-layout-allow-overlap`.
- **Elementos absolutos sin `top/left`** caen en su posición estática. Siempre `top:0;left:0` y mover con `x/y`.
- Excepciones que reconoce el auditor: `data-layout-allow-occlusion`, `-allow-overlap`, `-allow-overflow`,
  `-allow-caption-zone`, `-ignore`.
- Otras utilidades: `media-treatment` (etalonaje determinista), `normalize-audio` (LUFS), `capture` (web para
  vídeo), `remove-background` (recorte de persona, ver R8). Telemetría anónima: `npx hyperframes telemetry disable`.

## Reglas Hyperframes (no negociables)

Determinista (sin `Math.random()`/`Date.now()`); `gsap.timeline({paused:true})` registrado en `window.__timelines["main"]`; nunca `repeat:-1` (calcula repeticiones finitas); vídeo `muted` + `<audio>` separado; no animar dimensiones del `<video>` (anima wrapper); overlays = divs normales (sin `class="clip"`) controlados por el timeline (CSS `opacity:0` de base; `fromTo` para entrar, `to` para salir). Lint + inspect a 0 errores antes de renderizar.
