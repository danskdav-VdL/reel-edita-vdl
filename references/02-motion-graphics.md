> ⚙️ DOC DE MOTOR (universal). Copiado tal cual por forja-reel. Los colores que veas en los
> ejemplos son PLACEHOLDERS: tu paleta real vive en `references/estilo.md` y sobreescribe el
> `:root`. No hay estilo de nadie embebido aquí, solo la técnica.

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

## Operativa probada (reglas del runtime Hyperframes)

- **Props animables por GSAP:** SOLO `opacity, x, y, scale, scaleX/Y, rotation, width, height`.
  **NO** uses `clipPath`, `filter`, `top/left`, `borderWidth` (no se renderizan). Para PiP anima la
  cámara con `scale` + `x/y` (no `top/left`).
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
          {opacity:1,y:0,scale:1,duration:(o.d??0.42),ease:(o.e??"power3.out")},t);
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
- Un `#flash` blanco muy corto (0.05-0.08s) puede enmascarar el corte y darle punch.

## Isotipo VdL como STING (no marca de agua)

El isotipo (chevron `<`) se usa como **sting rápido**: pequeño, en la **esquina superior derecha** (o en
el hueco entre barbilla y banda de subtítulos), entrada y salida rápidas (aparece ~0.5-1s y se va).
**Nunca sobre el rostro ni sobre los subtítulos** (además de "nunca marca de agua"). En el endcard sí
puede ir grande y centrado.

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

Antes de escribir, lee (una vez) la skill `hyperframes`: `house-style.md` y `references/video-composition.md` (reglas de vídeo que pisan los instintos de web: llenar el frame, escalas grandes, color presente, movimiento constante).

## Sistema de capas (z-index)

- `#broll` (z:2): escenas B-roll a pantalla completa, `opacity:0` por defecto.
- `#camera` (z:5): el vídeo. **Va POR ENCIMA del B-roll.**
- `#orbs` (z:9): glows ambientales que laten.
- `#ov` (z:10): overlays (tags, chips, stickers).
- `#br_teaser` (z:13) y `#flash` (z:14): hook y destellos de transición.

⚠️ **Gotcha crítico:** el B-roll está DEBAJO de la cámara. Si la cámara está a pantalla completa, **tapa el B-roll**. Para que un B-roll se vea, la cámara DEBE estar en PiP (esquina). Cada escena B-roll va acompañada de `camPiP()`. (Un diagrama pensado como "overlay full-frame" no se verá si la cámara sigue full.)

## La cámara: animar layout, no transform

Para el PiP con borde nítido, **anima `width/height/top/left/borderWidth/borderRadius`** (no `transform: scale`, que escala también el borde y la sombra). El zoom interno (push-in/snap) va en un wrapper hijo `#vidzoom` con `transform: scale`.

```css
#camera { position:absolute; top:0; left:0; width:1080px; height:1920px;
  border:0 solid var(--violet); border-radius:0; overflow:hidden; z-index:5;
  box-shadow:0 28px 80px rgba(0,0,0,.6); }   /* sombra invisible a full-frame, visible en PiP */
#camera video { width:100%; height:100%; object-fit:cover; }
#vidzoom { width:100%; height:100%; transform-origin:50% 42%; }
```
```js
function camPiP(t){ tl.to("#camera",{top:1120,left:606,width:430,height:764,borderWidth:5,borderRadius:36,duration:0.5,ease:"power3.inOut"},t); }
function camFull(t){ tl.to("#camera",{top:0,left:0,width:1080,height:1920,borderWidth:0,borderRadius:0,y:0,duration:0.42,ease:"power3.inOut"},t); }
function floatPiP(t,dur){ tl.to("#camera",{y:"+=16",duration:1.7,yoyo:true,repeat:Math.max(1,Math.round(dur/1.7)),ease:"sine.inOut"},t); } // deriva suave del PiP
```
Snap-zoom en palabras clave (en tramos full-frame), sobre `#vidzoom`, sin solaparse en el tiempo:
```js
function snap(t){ tl.to("#vidzoom",{scale:1.08,duration:0.18,ease:"power3.out"},t); tl.to("#vidzoom",{scale:1.0,duration:0.34,ease:"power2.inOut"},t+0.2); }
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
  tl.fromTo(sel,{opacity:0,y:opt.fromY??52,scale:opt.fromScale??0.92},{opacity:1,y:0,scale:1,duration:0.32,ease:opt.ein??"back.out(1.7)"},tin);
  tl.fromTo(sel+" .w",{opacity:0,y:16},{opacity:1,y:0,duration:0.2,stagger:0.05,ease:"power2.out"},tin+0.07);
  tl.fromTo(sel+" .ul",{scaleX:0},{scaleX:1,duration:0.3,ease:"power3.out"},tin+0.3);
  tl.to(sel,{opacity:0,y:-26,scale:0.97,duration:0.26,ease:"power2.in"},tout);
}
```

## Helpers de motion ampliados (v10 — vocabulario extendido)

Todos estos helpers son deterministas, GPU-safe (`transform`/`opacity`/`filter`/`clip-path`) y están pensados para 1080×1920 con rótulos a la altura del micro.

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
  tl.to(sel,{clipPath:"inset(0 0% 0 0)",duration:0.42,ease:"power3.out"},tin);
  tl.fromTo(sel+" .sweep",{x:"-120%",opacity:0.95},{x:"120%",opacity:0,duration:0.42,ease:"power3.out"},tin);
  tl.to(sel,{opacity:0,duration:0.24,ease:"power2.in"},tout);
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
  tl.to(proxy,{p:1,duration:opt.duration ?? 0.6,ease:"power3.out",onUpdate:()=>{
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
  tl.fromTo(sel+" .underline",{scaleX:0,opacity:0.9},{scaleX:1,opacity:1,duration:0.28,ease:"power3.out"},t+0.48);
}
```

### `focusIn(sel, tin, tout)`
Entrada/salida blur-resolve tipo focus pull; úsalo en rótulos sobrios, citas y palabras clave.

```js
function focusIn(sel, tin, tout){
  // técnica inspirada en OpenMontage blur-resolve, reescrita
  tl.fromTo(sel,{filter:"blur(18px)",opacity:0,scale:1.06},{filter:"blur(0px)",opacity:1,scale:1,duration:0.4,ease:"power2.out"},tin);
  tl.to(sel,{filter:"blur(12px)",opacity:0,duration:0.3,ease:"power2.in"},tout);
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
  tl.fromTo(sel+" .fill",{clipPath:"inset(100% 0 0 0)"},{clipPath:"inset(0% 0 0 0)",duration:0.5,ease:"power3.out"},tin);
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

## Vocabulario de easings canónico (coherencia entre reels)

No inventes curvas nuevas por reel; elige de esta paleta. Es el equivalente al diccionario de easings de ReelStack.

| Intención | GSAP ease | Duración típica | Uso |
|---|---|---|---|
| `snappy` | `back.out(1.7)` | 0.30-0.40s | entradas de chip/rótulo/sello con punch |
| `gentle` | `power2.out` | 0.30-0.50s | fades de escena, apariciones suaves |
| `bouncy` | `back.out(2.4)` | 0.30-0.45s | stickers/badges juguetones, números clavados |
| `glass` | `power3.inOut` | 0.42-0.50s | movimientos de cámara (PiP↔full), transiciones premium |
| `smooth` | `sine.inOut` | 1.5-3.0s | push-ins/scroll lentos de B-roll, floats |
| salida | `power2.in` | 0.26-0.30s | salidas de elementos (fade/blur out) |

## Hook (0-3s) — lo más importante

Los 3 primeros segundos deciden el scroll. Movimiento inmediato. Patrón validado: **teaser del dato más bestia a pantalla completa que estalla y revela la cara**:
- `#br_teaser` (z:13) full-frame con el dato gigante (ej. "100.000 ⭐ / ¿en una semana?") que entra con slam (`scale 1.32→1` en 0.16s) + glitch-shake (`x` yoyo) + la pregunta en pop.
- A ~0.8s estalla: `scale→1.5, opacity→0, filter:blur(22px)` + `flash()`, y la cámara se revela con zoom-out (`#vidzoom` `scale 1.3→1.0`).
Alternativas si encaja mejor: slam tipográfico palabra-a-palabra, o micro-tráiler de 0.8s con flashes de las mejores escenas. Decide con VdL si dudas.

## B-roll diseñado (catálogo, adáptalo al contenido)

Cada uno full-frame con `scene-bg`+`grid`, **relleno** (8-10 elementos; nada de medio frame vacío — añade ghost glyph gigante a baja opacidad, tokens mono de fondo, métricas), y la cámara en PiP. Ejemplos usados:
- **Tarjeta de repo/dato**: card con contador animado (count-up vía proxy `{v:0}`→objetivo + `onUpdate` `toLocaleString('es-ES')`), badge, barras `scaleY`, pills.
- **Chat de IA que falla**: burbujas (user/bot), puntos de "escribiendo", ventana de app que glitchea en rojo (errores tipo `TypeError`, `build failed`, 💩). Buen recurso para el "problema".
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

- `flash()` (overlay blanco que parpadea 0.05s) en los cortes fuertes; glitch (shake `x` de `#camera`) al entrar a una escena tipo "error".
- Orbs (`#orbs`): 2 glows en esquinas que laten (`scale`/`opacity` yoyo, `repeat` finito que cubra la duración).
- Stickers (👀🔥🥄): pop+bounce cerca del chip, a la altura del micro.

## Reglas Hyperframes (no negociables)

Determinista (sin `Math.random()`/`Date.now()`); `gsap.timeline({paused:true})` registrado en `window.__timelines["main"]`; nunca `repeat:-1` (calcula repeticiones finitas); vídeo `muted` + `<audio>` separado; no animar dimensiones del `<video>` (anima wrapper); overlays = divs normales (sin `class="clip"`) controlados por el timeline (CSS `opacity:0` de base; `fromTo` para entrar, `to` para salir). Lint + inspect a 0 errores antes de renderizar.
