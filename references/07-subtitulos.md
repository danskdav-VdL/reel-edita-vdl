# 07-subtitulos.md — Subtítulos de VdL

Subtítulos **siempre** (mucha gente ve sin sonido, sobre todo en LinkedIn), con la **palabra clave
resaltada en lime** `#aae05a`. Estilo retención: 2-3 palabras por beat, sincronizadas a la voz.

## Generar los beats

```bash
python3 ~/.claude/skills/reel-edita-vdl/scripts/captions.py \
  --transcript edicion/transcript-final.json \
  --max-words 3 \
  --keywords "<cifras y conceptos potentes de ESTE vídeo>" \
  --out motion/captions.json
```
- **`--keywords`:** pásale las palabras a resaltar según ESTE vídeo. Para VdL, el tipo de keyword es
  **cifras/datos** y **conceptos potentes** (no marcas por defecto). Ej: `--keywords "40%,3x,agéntico,automatización,ROI"`.
  Si una palabra no matchea, el script resalta la más larga del beat.
- `--windows` opcional: limita los subtítulos a los tramos donde VdL habla a cámara.

## Estilo visual (a la altura del micro/pecho)

- Fuente **Onest** (cuerpo), peso 500; palabra clave en **Sora 600** + color lime.
- Contenedor anclado a la altura del pecho/micro, **nunca** pegado al borde inferior.
- Caja legible sobre el fondo movido: navy translúcido + leve sombra.

## 🔴 REGLA DURA: el subtítulo NUNCA sobre el rostro

El subtítulo va **por debajo de la barbilla**, nunca encima de boca/ojos/cara. La posición NO es fija:
se **adapta al encuadre de cada tramo a cámara**.

Cómo posicionarlo bien (hazlo por tramo a cámara / por cada setup de grabación):
1. Extrae 2-3 frames del tramo (`ffmpeg -ss <t> -i corte.mp4 -frames:v 1 -y /tmp/f.jpg`) y localiza la
   **barbilla** (borde inferior de la cara).
2. Ancla el subtítulo con su **borde superior ≥ ~70px por debajo de la barbilla**.
3. **Clamp inferior:** el borde inferior del subtítulo no debe bajar de ~`1600px` (la UI de
   Reels/TikTok/Shorts tapa el tercio inferior).
4. Si la cara queda muy baja en cuadro y no hay hueco, baja el subtítulo hasta justo encima de esa
   franja de UI (~1600px) — pero **jamás lo pongas sobre la cara**. Como último recurso, reduce el
   cuerpo del subtítulo.
5. **Durante B-roll (cámara en PiP)** la cara está en la esquina pequeña: el subtítulo centrado no la
   toca, así que la posición de pecho por defecto vale.
6. 🔴 **En SPLIT arriba/abajo: el subtítulo va EXACTAMENTE en la costura**, es decir **centrado sobre la
   línea que divide el panel visual (arriba) y el rostro (abajo)** — NO flotando en el hueco por debajo de
   la línea. Ancla el contenedor de subtítulos del split en el borde inferior del panel y **centra la caja
   sobre esa línea** (`top:<altura-del-panel>px` + `.cap{transform:translateY(-50%)}`), robusto a 1 o 2
   líneas. Así la banda queda pegada a la costura, nunca sobre la cara ni suelta en medio.

Expón la posición como variable (p. ej. `CAPS_TOP`) en el generador y ajústala por setup; si el vídeo
mezcla varios encuadres (como suele pasar con clips sueltos), usa la posición más segura para todos o
divide por tramos.

```css
#caps{position:absolute;left:60px;right:60px;top:1040px;text-align:center;z-index:11}
#caps .cap{display:inline-block;background:rgba(0,0,75,.88);padding:14px 26px;border-radius:18px;
  font-family:var(--font-text);font-weight:500;font-size:62px;line-height:1.15;color:#fff;
  box-shadow:0 10px 40px rgba(0,0,0,.45)}
#caps .cap .hi{font-family:var(--font-display);font-weight:600;color:#aae05a}  /* keyword en lime */
```
## Reveal PALABRA POR PALABRA + cero solape (regla dura)

1. **Cero solape temporal entre beats consecutivos:** cada subtítulo debe **salir del todo ANTES** de que
   entre el siguiente. Fija el `out` del beat en `next_start − ~0.09s` (nunca dos subtítulos a la vez).
   El generador ya recorta la duración de cada beat para no pisar al siguiente — mantenlo.
2. **Reveal palabra a palabra (por defecto):** dentro de cada beat, las palabras (`.w`) entran con
   **stagger** (una a una), no todas de golpe:
   ```js
   tl.fromTo(sel+" .w",{opacity:0,y:14},{opacity:1,y:0,duration:0.14,stagger:0.05,ease:"power2.out"},tin);
   ```
   La palabra clave se resalta en lime al entrar.
3. **Supresión durante escenas full-screen:** en los takeover a pantalla completa (y en los rótulos de
   contraste que sustituyen al subtítulo), **suprime los beats de subtítulo** de esa ventana para no
   duplicar texto. (Ver `02-motion-graphics.md` §escenas.)

Anima cada beat con una entrada corta sincronizada a su `start`, y salida en el `end`.
Los subtítulos son base permanente: **NO cuentan como "beat visual"** para la regla de ritmo ≤4s.

**Sin emojis en los subtítulos.** El énfasis es por **color** (keyword en lime) y peso (Sora), no por
emoji. Si el brief pide algún icono puntual, usa un glifo/símbolo techy limpio, nunca caritas ("playschool").
