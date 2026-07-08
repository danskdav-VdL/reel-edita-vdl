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

Técnica en Hyperframes (determinista: sin `Math.random()`/`Date.now()`, `repeat` finito, timeline `paused`):
capa `#bg` navy + 4 blobs con `radial-gradient` y blur pesado, animados con GSAP en yoyo lento.

```html
<div id="bg">
  <span class="blob b-lime"></span>
  <span class="blob b-magenta"></span>
  <span class="blob b-violet"></span>
  <span class="blob b-lilac"></span>
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

## 4. Isotipo (VERIFIED — usar el SVG tal cual, NUNCA inventar)

El isotipo VdL es un **chevron `<`** (una "V" girada 90º en sentido horario), de un solo trazo,
`viewBox 0 0 261 273.93`. Archivos en `BRAND_DIR` (4 versiones monocromas):
- `Isotipo_VdL_Blanco_ffffff.svg` · `Isotipo_VdL_Verde_aae05a.svg` (lime) ·
  `Isotipo_VdL_Morado_b41e82.svg` (magenta) · `Isotipo_VdL_BlueNavy_00004b.svg`.

**Reglas duras:**
- **NUNCA como marca de agua** (ni logo permanente en una esquina durante todo el vídeo).
- Se usa como **sting**: pequeño y **rápido** (aparece ~0.5-1s y se va), en la **esquina superior derecha**
  o en el hueco entre barbilla y banda de subtítulos. **Nunca sobre el rostro ni sobre los subtítulos.**
  Sobre navy o el degradado, en **blanco o lime** para contraste. En el endcard sí puede ir grande y centrado.
- **No lo redibujes ni lo aproximes**: incrusta el SVG del archivo. Sin reglas oficiales de área de
  respeto → deja aire generoso alrededor y tamaño legible.

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
- **Audio: solo SFX sutiles, sin música.** SFX bajo la voz (ver `03-sfx-y-qc.md`).
- **Cold open sí** (ver `08-cold-open.md`).
- **Emojis: al mínimo (`emoji_level=min` por defecto), look techy — NADA "playschool".** Evita caritas y
  emojis coloridos. Para marcar ideas usa **iconografía limpia**: glifos de línea, símbolos técnicos
  (`>`, `#`, `→`, `//`), números de paso/nivel, y el acento lime sobre Sora. `none` = cero emojis.
  El isotipo VdL (chevron `<`) es el sello gráfico, no emojis.

---

## 7. Posición del texto (REGLA FIJA DEL MOTOR)

Todo el texto (subtítulos, rótulos, chips) va **a la altura del micrófono/pecho** — contenedor
anclado en `top:~1040px`, **nunca pegado al borde inferior** (la UI de Reels/TikTok/Shorts tapa el
tercio de abajo). La cara (~y300–1000) queda libre. Ver `07-subtitulos.md`.
