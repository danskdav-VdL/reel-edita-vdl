# 04-recetas.md — Tratamientos visuales de VdL

**Lo que NO cambia nunca (ni con tratamiento nuevo):** el reel **cierra con la cortinilla oficial**
(`estilo.md` §8) y **no lleva isotipo** en el cuerpo (`estilo.md` §4). Los beat sheets de abajo acaban
en "[CORTINILLA]" justo por eso.

**El movimiento de TODAS las recetas sigue `10-motion-vdl.md`** (familia de curvas, ley del corte, nada
idle, un héroe por plano) y se revisa con `12-revision-visual.md`. Antes de construir un efecto, búscalo
en el catálogo (`11-catalogo-y-recetas.md`).

**Framework universal (esto es lo que no cambia):
1. **Lee el vídeo** (mira el corte aprobado): ¿qué tipo de contenido es?, ¿tiene demo?, ¿datos?, ¿es
   conceptual o práctico?, ¿dónde está el gancho?
2. **Elige o COMBINA** un tratamiento de abajo que encaje con ESE contenido.
3. **No repitas molde fijo.** Dos reels seguidos no deben sentirse calcados. El catálogo es abierto:
   puedes proponer tratamientos nuevos.
4. Aplica siempre la identidad de `estilo.md` (paleta VdL, fondo liquid animado, Sora/Onest, framing).

Cada receta: **cuándo · capas · ritmo · beat sheet de ejemplo**. Colores y framing = VdL.

---

## R1 · Editor-pro (talking-head con producción)
**Cuándo:** VdL habla a cámara explicando algo, sin demo. El caso más común.
- **Capas:** cámara full-frame en los momentos de conexión; salta a PiP (abajo-dcha) cuando entra un
  B-roll/rótulo que ilustra. Fondo liquid animado detrás en los tramos PiP. Subtítulos siempre.
- **Ritmo:** medio-ágil. `snap` (zoom-punch, máx. 3) en palabras clave; `kpop`/`wipe` para rótulos; reencuadres con la nudge curve (`camPiP`/`camFull`). Sin float del PiP.
- **Beat sheet:** [0-3s cold open] → [full-frame gancho + snap en keyword] → [PiP + chip de dato] →
  [full-frame conexión] → [PiP + lista con `type`/checks] → [último tramo a cámara con el CTA] → [CORTINILLA].

## R2 · Screenshare / demo (enseñar producto/herramienta)
**Cuándo:** VdL enseña una pantalla, web, app o flujo (encaja con "sistemas agénticos", tech, SaaS).
- **Capas:** pantalla/inserto a full o en marco de navegador; **cara en PiP abajo-dcha encima**.
  B-roll real (firecrawl) para capturas de webs/logos reales (ver `06-broll.md`).
- **Ritmo:** medio; `typeIn` para comandos/URLs; **cursor grande** (`oversized-cursor`) cuyo clic dispara lo siguiente; la cámara se acerca a lo que se va a pulsar (`ui-focus-zoom`, escala 1.4-2.2, 0.6-0.9 s) y vuelve al resultado — no en cada clic. Mejor la UI recreada con sus tokens y datos ficticios que un pantallazo con pan.
- **Beat sheet:** [cold open con el resultado de la demo] → [PiP + captura scrolleando] →
  [zoom a la parte clave] → [chip con el "qué acaba de pasar"] → [CTA a cámara] → [CORTINILLA].

## R3 · Pantalla partida (comparativa / antes-después)
**Cuándo:** contrastar dos cosas (antes/después, mal/bien, opción A/B).
- **Capas:** split vertical u horizontal; cámara en una zona, visual/dato en la otra. Divisoria con acento lime.
- **Ritmo:** medio; revelar los dos lados con `wipe`, `flashCut` al cerrar la comparación.
- **Beat sheet:** [gancho "esto vs esto"] → [lado A] → [lado B] → [veredicto en rótulo grande].

## R4 · Kinético (texto cinético protagonista)
**Cuándo:** frase potente, cifra o cita que merece ser el visual. Úsalo con moderación ("lo justo").
- **Capas:** fondo liquid animado, tipografía Sora grande, palabra clave en lime (`fillWord`/`wipe`),
  cifras con `slotReveal`. Cámara en PiP o ausente unos segundos.
- **Ritmo:** **waterfall entry** (palabras que suben desde abajo solapadas, opacidad binaria, las pesadas viajan más; `cut-the-curve` §6) y **waterfall cut** entre frases (§4). Frases ≤ 5 palabras. Luego aire (≥ 1 s quieto en la clave).
- **Beat sheet:** [cifra que estalla con `slotReveal` + `ding`] → [frase kinética] → [vuelve a cámara].

## R5 · Minimal-editorial (sobrio, premium)
**Cuándo:** mensaje reflexivo, de marca o de posicionamiento; tono LinkedIn.
- **Capas:** mucho aire, un solo rótulo Sora Light, fondo liquid MUY sutil (opacidad baja).
  Cámara full-frame o PiP estable.
- **Ritmo:** con aire, `focusIn` (blur-resolve) en rótulos, reencuadres con nudge curve, un rack-focus como mucho. Pocos SFX.
- **Beat sheet:** [cold open sobrio] → [idea 1 con focusIn] → [idea 2] → [cierre sobrio a cámara] → [CORTINILLA].

## R6 · Con elementos aportados (assets de VdL/cliente)
**Cuándo:** VdL entrega imágenes/clips/capturas propios en la carpeta `assets/` del proyecto.
- **Capas:** insertos de esos assets a full o en marco; cámara en PiP; logos de cliente en insignia
  (solo assets reales/verificados, nunca inventados). Ver `06-broll.md`.
- **Ritmo:** según el material; sincroniza cada asset con lo que se dice (J-cut ~0.2s antes).
- **Beat sheet:** adáptalo al material entregado.

## R7 · Split arriba/abajo (encuadre partido) — LAYOUT DE REFERENCIA VdL
**Cuándo:** cuando quieres ver a la persona **Y** un visual a la vez (una demo, una captura, un dato,
una comparación) sin que uno tape al otro. Tercer encuadre junto a full-frame y PiP.
- **Layout canónico (regla dura, así debe quedar SIEMPRE que la pantalla se parta en dos):**
  1. **Mitad SUPERIOR = panel OPACO de marca** (navy/degradado, ~`top 0`–`870px`) con el visual: tarjetas,
     logos, lista, diagrama, chips… + kicker arriba. Borde inferior fino lime como divisoria.
  2. **Mitad INFERIOR = la CÁMARA AMPLIADA mostrando el ROSTRO** (no un PiP diminuto en esquina). Baja el
     encuadre con transform (`scale ~1.1` + `y ~+900`) para que la cara caiga en la mitad de abajo.
  3. **Banda de SUBTÍTULO EXACTAMENTE en la COSTURA:** centrada **sobre la línea** que divide panel y
     rostro (borde inferior del panel), NO flotando en el hueco por debajo. Técnica robusta: contenedor
     `top:<alto-del-panel>px` + `.cap{transform:translateY(-50%)}` (se centra sobre la línea con 1 o 2
     líneas). Nunca sobre la cara (que va más abajo). Ver `07-subtitulos.md` punto 6.
- **Cómo (Hyperframes, SOLO transform):** cámara con `scale`+`y` (NUNCA `top/left/width/height` → el linter
  `check` lo bloquea). El panel superior va en z ENCIMA de la cámara (opaco) para tapar la parte alta del
  vídeo desplazado. Alterna con full-frame a lo largo del reel.
- **Ritmo:** entra el visual con revelado sutil (`rev()`) sincronizado a lo que se dice.
- **Beat sheet ej.:** [dice "mira esto"] → split (cara abajo + captura arriba) → [señala un dato] → snap en el dato.

## R8 · Portada con recorte (persona delante del titular)
**Cuándo:** frase-tesis potente, arranque de un análisis o remate. Máx. 1-2 veces por reel.
- **Capas:** fondo liquid de marca → titular ENORME (200-280px, 1-2 palabras) → **persona recortada**
  (`npx hyperframes remove-background <tramo> -o recorte.webm`, WebM con alfa) por delante tapando parte de
  las letras → rótulo pequeño. Cámara normal oculta (`opacity:0`) durante el tramo.
- La persona va al 100 % y POR DELANTE (cumple la regla de "nunca sujeto semitransparente detrás del texto").
- Recorta solo el tramo que se usa (la 1ª vez descarga el modelo; luego ~0,25 s/fotograma).
- **Ritmo:** entra el titular, la persona "aparece" delante con corte limpio, 2-3 s, vuelta a cámara.

## R9 · Producto en uso (Modo B / híbrido)
**Cuándo:** se enseña un proyecto (ver `09-modo-proyecto.md`).
- **Capas:** fondo de marca → UI del producto en marco (móvil o navegador) con **datos ficticios** →
  clics/tecleo simulados → rótulo con el "qué acaba de pasar" → en híbrido, cámara en split (R7).
- **Beat sheet:** [gancho con la afirmación más potente] → [pantalla: entrada] → [acción clave con clic + SFX]
  → [resultado] → [remate] → [CORTINILLA].

**Iconografía (nada "playschool"):** por defecto **casi sin emojis** (`emoji_level=min`). Para marcar
ideas usa **glifos limpios / símbolos técnicos** (flechas, `>`, `#`, números de paso, líneas), tipografía
Sora, y el acento lime — no caritas ni emojis coloridos. Look techy, no infantil. (Ver `estilo.md`.)

---

**Densidad → aire (excepción de ritmo):** en tramos conceptuales densos, baja la densidad de cambios a
propósito (no lo infles a cortes). En ganchos y listas, sube a 5-7 cambios/10s. Nunca >4s sin un beat.

**Cliché a evitar (look-IA):** nada de píldoras de sección genéricas arriba ("EL PROBLEMA / LA SOLUCIÓN"
con puntito de color). Da estructura con el ritmo y los chips de contenido, no con etiquetas-capítulo.
