# 04-recetas.md — Tratamientos visuales de VdL

**Framework universal (esto es lo que no cambia):**
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
- **Ritmo:** medio-ágil. `snap` (zoom-punch) en palabras clave; `kpop`/`wipe` para rótulos; float sutil del PiP.
- **Beat sheet:** [0-3s cold open] → [full-frame gancho + snap en keyword] → [PiP + chip de dato] →
  [full-frame conexión] → [PiP + lista con `type`/checks] → [cierre con sting de isotipo].

## R2 · Screenshare / demo (enseñar producto/herramienta)
**Cuándo:** VdL enseña una pantalla, web, app o flujo (encaja con "sistemas agénticos", tech, SaaS).
- **Capas:** pantalla/inserto a full o en marco de navegador; **cara en PiP abajo-dcha encima**.
  B-roll real (firecrawl) para capturas de webs/logos reales (ver `06-broll.md`).
- **Ritmo:** medio; `typeIn` para comandos/URLs, `snap` sobre lo que señala, whoosh en cambios de vista.
- **Beat sheet:** [cold open con el resultado de la demo] → [PiP + captura scrolleando] →
  [zoom a la parte clave] → [chip con el "qué acaba de pasar"] → [endcard].

## R3 · Pantalla partida (comparativa / antes-después)
**Cuándo:** contrastar dos cosas (antes/después, mal/bien, opción A/B).
- **Capas:** split vertical u horizontal; cámara en una zona, visual/dato en la otra. Divisoria con acento lime.
- **Ritmo:** medio; revelar los dos lados con `wipe`, `flashCut` al cerrar la comparación.
- **Beat sheet:** [gancho "esto vs esto"] → [lado A] → [lado B] → [veredicto en rótulo grande].

## R4 · Kinético (texto cinético protagonista)
**Cuándo:** frase potente, cifra o cita que merece ser el visual. Úsalo con moderación ("lo justo").
- **Capas:** fondo liquid animado, tipografía Sora grande, palabra clave en lime (`fillWord`/`wipe`),
  cifras con `slotReveal`. Cámara en PiP o ausente unos segundos.
- **Ritmo:** ágil en la entrada de palabras (`kpop` stagger), aire después para que respire.
- **Beat sheet:** [cifra que estalla con `slotReveal` + `ding`] → [frase kinética] → [vuelve a cámara].

## R5 · Minimal-editorial (sobrio, premium)
**Cuándo:** mensaje reflexivo, de marca o de posicionamiento; tono LinkedIn.
- **Capas:** mucho aire, un solo rótulo Sora Light, fondo liquid MUY sutil (opacidad baja), isotipo discreto.
  Cámara full-frame o PiP estable.
- **Ritmo:** con aire, `focusIn` (blur-resolve) en rótulos, transiciones `glass`. Pocos SFX.
- **Beat sheet:** [cold open sobrio] → [idea 1 con focusIn] → [idea 2] → [cierre con isotipo lime].

## R6 · Con elementos aportados (assets de VdL/cliente)
**Cuándo:** VdL entrega imágenes/clips/capturas propios en la carpeta `assets/` del proyecto.
- **Capas:** insertos de esos assets a full o en marco; cámara en PiP; logos de cliente en insignia
  (solo assets reales/verificados, nunca inventados). Ver `06-broll.md`.
- **Ritmo:** según el material; sincroniza cada asset con lo que se dice (J-cut ~0.2s antes).
- **Beat sheet:** adáptalo al material entregado.

## R7 · Split arriba/abajo (encuadre partido)
**Cuándo:** cuando quieres ver a la persona **Y** un visual a la vez (una demo, una captura, un dato,
una comparación) sin que uno tape al otro. Tercer encuadre junto a full-frame y PiP.
- **Capas:** la **cámara ocupa una mitad** (normalmente la de ABAJO, a la altura natural de la cara) y el
  **B-roll/visual la otra mitad** (arriba). Divisoria fina con acento lime. Alterna con full/PiP a lo largo del reel.
- **Cómo (Hyperframes, solo transform):** cámara a media pantalla con `scale ~0.5` + `y` para anclarla en
  su mitad; el visual (captura/imagen/escena) en la otra mitad, a pantalla-mitad. Nada de `top/left`
  (usa `scale`+`x/y`). Subtítulos: colócalos en la franja de la CÁMARA, nunca sobre su cara.
- **Ritmo:** entra el visual con revelado sutil (`rev()`) sincronizado a lo que se dice.
- **Beat sheet ej.:** [dice "mira esto"] → split (cara abajo + captura arriba) → [señala un dato] → snap en el dato.

**Iconografía (nada "playschool"):** por defecto **casi sin emojis** (`emoji_level=min`). Para marcar
ideas usa **glifos limpios / símbolos técnicos** (flechas, `>`, `#`, números de paso, líneas), tipografía
Sora, y el acento lime — no caritas ni emojis coloridos. Look techy, no infantil. (Ver `estilo.md`.)

---

**Densidad → aire (excepción de ritmo):** en tramos conceptuales densos, baja la densidad de cambios a
propósito (no lo infles a cortes). En ganchos y listas, sube a 5-7 cambios/10s. Nunca >4s sin un beat.

**Cliché a evitar (look-IA):** nada de píldoras de sección genéricas arriba ("EL PROBLEMA / LA SOLUCIÓN"
con puntito de color). Da estructura con el ritmo y los chips de contenido, no con etiquetas-capítulo.
