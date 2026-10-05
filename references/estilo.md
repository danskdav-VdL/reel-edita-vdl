# estilo.md — Hoja de marca de Valor de Ley (VdL)

La identidad visual del reel. El motor la consulta en CADA vídeo. Fuente de los tokens:
`recursos/brand-kit-vdl/VdL_brandkit.md` (reconstruido de los assets oficiales).

> **BRAND_DIR** (assets de marca en esta máquina):
> `/Users/diseno/Documents/Claude AI/recursos/brand-kit-vdl`
> Copia al proyecto (`motion/assets/`) los assets que uses, para que el render sea portable.

---

## 1. Paleta (VERIFIED de los SVG y el PDF)

| Rol | Token | Hex |
|---|---|---|
| Base / fondo | navy | `#00004b` |
| **Acento principal** | lime | `#aae05a` |
| **Co-acento** | magenta | `#b41e82` |
| Texto sobre fondo oscuro | white | `#ffffff` |
| (degradado) violeta transición | — | `#3a2770` |
| (degradado) lila bloom | — | `#c865d1` |

**Reglas de color:**
- El **fondo dominante es navy** `#00004b`, y sobre él vive el degradado.
- Lime y magenta son **co-importantes** (no hay primario fijo). Para el ACENTO de rótulos/keyword,
  usa **lime** como opción por defecto (máximo contraste sobre navy); magenta para variar o marcar co-acento.
- **Contraste obligatorio:** nunca magenta sobre navy sin verificar legibilidad; nunca lime sobre blanco.
- Los chips/rótulos van sobre caja oscura navy translúcida `rgba(0,0,75,.88)` con borde de acento.

Mapeo a los slots del motor (`02-motion-graphics.md :root`):
`--violet=#aae05a (lime, acento) · --red=#b41e82 (magenta) · --blue=#00004b (navy) · --green=#3a2770 · --amber=#c865d1`.

---

## 2. Fondo LIQUID ANIMADO — la firma de VdL (IMPRESCINDIBLE)

El fondo de marca **NUNCA es un color plano ni un `linear-gradient` recto**. Es un **degradado líquido
animado**: manchas (blobs) de navy → violeta → magenta → lime que se **desplazan y se funden entre sí
lentamente, en bucle sin costura**, tipo aurora. Movimiento sutil (no debe distraer del contenido).

Es la **única capa ambiente permitida** (`10-motion-vdl.md` §3): no cuenta como el movimiento de la escena,
que necesita además su propia ruta (revelado, cámara con intención, UI que vive…). En Modo B puede bajar
de intensidad o cambiar a escenario oscuro con grano si el producto del cliente lo pide (su marca manda
en su vídeo), pero nunca color plano.

### 2a · Versión 2 (RECOMENDADA desde 2026-10-02): shader de seda — `assets/liquid-vdl.js`

Un campo de flujo en WebGL (domain warp suave + tres familias de cintas tipo aurora con filos de luz finos,
horizonte violeta abajo, barrido de luz diagonal lento, grano fino estable por frame y lime SOLO en los filos
más altos). Es función pura del tiempo → determinista y seek-safe. Se pinta a media resolución y el CSS lo
escala (seda sin coste). Mejor que los 4 blobs en vaivén: nunca se repite, no "late" y tiene profundidad.
```html
<script src="liquid.js"></script>   <!-- copia assets/liquid-vdl.js a motion/liquid.js -->
<canvas id="liquid" style="position:absolute;top:0;left:0;width:1080px;height:1920px;z-index:0"></canvas>
```
```js
const L = liquidVdL(document.getElementById("liquid"), {scale: 0.5});
const clock = {t: 0};
tl.to(clock, {t: DUR, duration: DUR, ease: "none", onUpdate: () => L.draw(clock.t)}, 0);
// L.state = {energy, lime, gx, gy}: energía del flujo, presencia del lime y HALO de interés (0-1, y hacia arriba)
tl.to(L.state, {gx: .5, gy: .78, duration: 1.2, ease: "power2.inOut"}, 11.9);   // el halo sigue al panel superior
```
Probado en el reel de Albarán Digital (2026-10-02): render GPU, 0 errores de `check`.

### 2b · Versión 1 (blobs CSS) — si no hay WebGL

Técnica en Hyperframes (determinista: sin `Math.random()`/`Date.now()`, `repeat` finito, timeline `paused`):
capa `#bg` navy + 4 blobs con `radial-gradient` y blur pesado, animados con GSAP en yoyo lento.

```html
<div id="bg">
  <span data-layout-allow-overflow class="blob b-lime"></span>
  <span data-layout-allow-overflow class="blob b-magenta"></span>
  <span data-layout-allow-overflow class="blob b-violet"></span>
  <span data-layout-allow-overflow class="blob b-lilac"></span>
  <!-- data-layout-allow-overflow: los blobs salen del cuadro A PROPÓSITO; sin él, `check` da ~70 avisos -->
</div>
```
```css
#bg{position:absolute;inset:0;background:#00004b;overflow:hidden;z-index:0}
#bg .blob{position:absolute;width:1200px;height:1200px;border-radius:50%;
  filter:blur(90px);opacity:.55;mix-blend-mode:screen;will-change:transform}
.b-lime   {background:radial-gradient(circle,#aae05a 0%,transparent 62%);top:-200px;left:-200px}
.b-magenta{background:radial-gradient(circle,#b41e82 0%,transparent 62%);top:900px; left:500px}
.b-violet {background:radial-gradient(circle,#3a2770 0%,transparent 62%);top:300px; left:600px}
.b-lilac  {background:radial-gradient(circle,#c865d1 0%,transparent 60%);top:1200px;left:-100px}
```
```js
// bucle sin costura: cada blob deriva lento; repeat finito que cubra data-duration.
// DUR = duración de la composición en segundos.
function liquidBG(DUR){
  const cyc = 14; // s por ciclo (movimiento lento)
  const n = Math.max(1, Math.round(DUR/cyc));
  const drift = (sel,dx,dy,ds)=>tl.to(sel,{x:dx,y:dy,scale:ds,duration:cyc,
      yoyo:true,repeat:n,ease:"sine.inOut"},0);
  drift(".b-lime",   260,  180, 1.15);
  drift(".b-magenta",-220, -160,1.20);
  drift(".b-violet",  180, -220,1.10);
  drift(".b-lilac",  -200,  200,1.18);
}
```
Notas: transiciones difusas (blur alto), nada de bordes duros; no saturar los 4 colores a la vez con
igual peso (opacidad ~.5). La cámara/contenido va SIEMPRE por encima (z-index mayor).

---

## 3. Tipografías (VERIFIED — embebidas en el PDF de marca)

- **Display / titulares → Sora** (pesos 600 SemiBold y 300 Light).
- **Texto / cuerpo / subtítulos → Onest** (pesos 500 Medium y 300 Light).
- Fallback: `Inter`, `system-ui`, `sans-serif`.

Los `.ttf` están en `BRAND_DIR/Fonts/`. Para que el render (Chrome headless) los use sin depender de
CDN, declara `@font-face` con ruta absoluta (o copia los ttf a `motion/assets/fonts/`):
```css
@font-face{font-family:'Sora';font-weight:600;src:url('file:///Users/diseno/Documents/Claude AI/recursos/brand-kit-vdl/Fonts/Sora/static/Sora-SemiBold.ttf')}
@font-face{font-family:'Sora';font-weight:300;src:url('file:///Users/diseno/Documents/Claude AI/recursos/brand-kit-vdl/Fonts/Sora/static/Sora-Light.ttf')}
@font-face{font-family:'Onest';font-weight:500;src:url('file:///Users/diseno/Documents/Claude AI/recursos/brand-kit-vdl/Fonts/Onest/static/Onest-Medium.ttf')}
@font-face{font-family:'Onest';font-weight:300;src:url('file:///Users/diseno/Documents/Claude AI/recursos/brand-kit-vdl/Fonts/Onest/static/Onest-Light.ttf')}
:root{ --font-display:'Sora','Inter',system-ui,sans-serif; --font-text:'Onest','Inter',system-ui,sans-serif; }
```
Titulares/keywords en Sora SemiBold; subtítulos y cuerpo en Onest Medium.

---

## 4. Isotipo `<` — 🔴 POR DEFECTO **NO SE USA**

El isotipo VdL es un **chevron `<`** (una "V" girada 90º en sentido horario), de un solo trazo,
`viewBox 0 0 261 273.93`, en `BRAND_DIR` (`Isotipo_VdL_Blanco_ffffff.svg`, `..._Verde_aae05a.svg`,
`..._Morado_b41e82.svg`, `..._BlueNavy_00004b.svg`).

🔴 **REGLA DURA (2026-08-18): el isotipo NO va en el vídeo. En ninguna parte.**
Ni sting en esquina, ni marca de agua, ni endcard, ni dentro de una escena de B-roll.
**La marca la pone la CORTINILLA DE CIERRE** (§8) — es el único sitio donde aparece la identidad.

- **Solo se pone si VdL lo pide EXPLÍCITAMENTE** para ese vídeo ("mete el isotipo en X").
  Si no lo pide, no se pone: no lo añadas "porque queda bien" ni para rellenar un beat.
- Cuando se pida: incrusta el SVG del archivo (**no lo redibujes ni lo aproximes**), nunca sobre
  el rostro ni sobre los subtítulos, y nunca como logo permanente.
- 🔴 **NUNCA escribas el nombre "Valor de Ley" / "VALOR DE LEY" en pantalla.** Sigue vigente: el
  nombre escrito no se pone nunca en el cuerpo del reel. (La cortinilla oficial de cierre sí lleva
  el logotipo completo — es el asset de marca y va tal cual, sin tocar.)
- **Cierre sin velo:** el último tramo a cámara (CTA tipo "Escríbenos", pregunta-gancho) va **sobre
  el vídeo directo** (con sombra para legibilidad), la persona VISIBLE. Nada de velo oscuro/de color
  encima del sujeto. Después entra la cortinilla.

> Por qué: los stings sueltos competían con el cierre de marca y ensuciaban el remate. Con la
> cortinilla el reel tiene UN cierre de marca, siempre el mismo, y el cuerpo queda limpio.

---

## 5. Framing (cómo sale VdL en pantalla)

- **Aparece casi siempre** en cámara. Formato **alternado**: pantalla completa en los momentos de
  conexión/impacto, **PiP** (cámara flotante) cuando hay B-roll o demo detrás.
- **PiP por defecto: abajo-derecha** (`camPiP()` del motor deja el PiP en esa zona).
- **Screenshare/demo → cara en PiP encima** de la pantalla (no solo pantalla).
- Recuerda el gotcha del motor: el B-roll está DEBAJO de la cámara; para ver B-roll, la cámara DEBE ir en PiP.

---

## 6. Estética y ritmo

- **Estética híbrida: enérgica-punchy + sobria-editorial.** Punch en cortes, zooms y entradas de chip;
  sobriedad en tipografía (Sora/Onest limpias), color contenido y composición con aire. Ni recargado
  ni plano: energía con criterio. Encaja con publicar en **LinkedIn + Reels + TikTok + Shorts**.
- **Ritmo: medio.** Dinámico pero deja respirar el mensaje (aire en conceptos densos, agilidad en
  ganchos y listas). Regla dura del motor: ningún tramo >4s sin un beat visual.
- **Movimiento: el sistema de `10-motion-vdl.md`** (una familia de curvas, cortes vivos en la corriente
  izquierda, nada que flote o lata). El "punch" sale de la aceleración y de los cortes, no de flashes.
- **Audio: solo SFX sutiles, sin música** en reels a cámara (Modo A). En piezas de motion (Modo B):
  partitura original sintetizada (`03-sfx-y-qc.md` §Música original).
- **Cold open sí** (ver `08-cold-open.md`).
- 🔴 **Nunca el sujeto semi-transparente detrás del texto** (look "fantasma"). Para un titular/rótulo a
  pantalla: persona VISIBLE al 100% con texto en lower-third, o persona OCULTA (`opacity:0`) con fondo
  plano/degradado/liquid animado detrás. Jamás el vídeo del sujeto atenuado al ~50% bajo el texto.
- **Zoom-in rápido (`snap`) MÁX. 3 veces por reel** (recurso puntual, no relleno de ritmo).
- **Emojis: al mínimo (`emoji_level=min` por defecto), look techy — NADA "playschool".** Evita caritas y
  emojis coloridos. Para marcar ideas usa **iconografía limpia**: glifos de línea, símbolos técnicos
  (`>`, `#`, `→`, `//`), números de paso/nivel, y el acento lime sobre Sora. `none` = cero emojis.
  El sello gráfico es la tipografía y el acento lime, no emojis (y **no** el isotipo — ver §4).

---

## 7. Posición del texto (REGLA FIJA DEL MOTOR)

Todo el texto (subtítulos, rótulos, chips) va **a la altura del micrófono/pecho** — contenedor
anclado en `top:~1040px`, **nunca pegado al borde inferior** (la UI de Reels/TikTok/Shorts tapa el
tercio de abajo). La cara (~y300–1000) queda libre. Ver `07-subtitulos.md`.

---

## 8. Cierre de marca — LA CORTINILLA (obligatoria, siempre la misma)

🔴 **REGLA DURA (2026-08-18): TODOS los reels de VdL terminan con la cortinilla oficial.**
Siempre la misma, ni otra ni una versión rediseñada. No se diseña un endcard de marca a mano.

> **CIERRE_VdL** (en esta máquina):
> `/Users/diseno/Documents/Claude AI/recursos/Cierres reels/cortinilla_compartiendo valor.mp4`

Qué es: barrido lime que revela el **logotipo completo** (`valor de ley` + chevron) sobre el
degradado navy→magenta de marca. **4.0s · 1080×1920 · 60 fps · SIN pista de audio.**

**Cómo se monta (un solo comando, hace todo):**
```bash
bash ~/.claude/skills/reel-edita-vdl/scripts/cierre.sh <reel-montado.mp4> <FINAL.mp4> [xfade]
```
El script resuelve la cortinilla, la **normaliza a la resolución y fps del reel**, le añade **pista de
audio** (viene muda) + SFX suaves (whoosh en el barrido + ding al asentar el logotipo) y la une con
**disolución cruzada** (`xfade` en vídeo + `acrossfade` en audio). Avisa si la disolución pisaría voz.

**Reglas del cierre:**
- **Transición: disolución cruzada, `0.5s` por defecto** (nunca corte seco: la cortinilla ya trae su
  propio barrido y el corte seco encima se siente brusco).
- Va **DESPUÉS de todo** (cold open + cuerpo + SFX ya mezclados). No entra en el timeline de
  Hyperframes: se pega en post, como el cold open pero al final.
- **La voz tiene que haber terminado antes de que empiece la disolución.** Deja ~0.5-0.8s de cola de
  silencio al final del corte. Si no cabe, baja el `xfade` — nunca cortes una palabra.
- **No la retoques**: ni recolorear, ni recortar, ni cambiarle el ritmo, ni superponerle texto.
- No hace falta CTA gráfico encima: el CTA lo dice la voz en el último tramo a cámara.
- Suma **~3.5s** a la duración final (4.0 − 0.5 de disolución). Cuéntalo al planificar duración.
- Si la cortinilla no está en su sitio o hay varias en la carpeta, el script **para y pregunta** —
  no improvises un cierre alternativo.
