# 09-modo-proyecto.md — MODO B: vídeo de un PROYECTO (sin bruto a cámara)

Método de lanzamiento de `/brag` (github.com/latent-spaces/brag, MIT) **integrado** en el editor de reels.
Sirve para enseñar algo que se ha construido (un producto de VdL, un sistema, una web, un lead magnet, un
flujo de n8n) **sin que nadie grabe nada**. Hereda TODO lo de la skill: identidad (`estilo.md`), banco de
B-roll y stock (`06-broll.md`), SFX (`03-sfx-y-qc.md`), cierre de marca, miniatura, `hyperframes check` y revisor.

**Cuándo:** "hazme un vídeo del proyecto X", "vídeo de lanzamiento de…", "enseña lo que hemos construido",
o te pasan la ruta de un repo / una URL en vez de un vídeo vertical.

**Híbrido (A+B):** si además hay un bruto de alguien hablando a cámara, el Modo B aporta las escenas de producto y el
Modo A (flujo normal) aporta la cámara: tramos a cámara intercalados con escenas del producto (split o
full-screen). Es la versión más potente: persona + producto real.

---

## 1. Inspeccionar la fuente

| Fuente | Cómo se reconoce | De dónde sale el material |
|---|---|---|
| **Repo / carpeta local** | ruta a un proyecto | el CÓDIGO: páginas, componentes, estilos (colores y fuentes exactos), README, docs, `public/` |
| **Web** | URL o dominio | la web tal como la ve un visitante (headless si carga por JS; `npx hyperframes capture <url>` o firecrawl) |

Reúne: qué es (una frase), para quién y qué le resuelve, qué lo diferencia, la afirmación más potente
(con su dato si existe), el gancho visual, **el flujo en uso** (entrada → acción clave → resultado), y la
frase para compartir.

### 🔴 Reglas de seguridad (duras, antes de leer nada)
- **Nunca leas ni muestres** `.env*`, `certs/`, claves, tokens, `*.pem`, credenciales, ni ficheros de
  "altas", accesos o contraseñas. Si un archivo parece contener secretos, sáltalo.
- **Nunca arranques la app contra producción** (una `.env.local` real apunta a la base de datos viva).
  El material visual se reconstruye desde el código con **datos ficticios**, o desde capturas de un
  entorno demo que te den.
- **Cero datos reales de clientes**: ni nombres de empresas, ni personas, ni matrículas, ni emails, ni
  importes. Inventa datos verosímiles y neutros (p. ej. "Transportes Norte S.L.", "1234 ABC").
- Si el proyecto es de un cliente o interno, confirma que se puede enseñar públicamente antes de publicar.

## 2. Planificar — el PLAN DE DIRECCIÓN (el modelo: film de Staynex, 2026-10-02)

En Modo B el motion ES el espectáculo: aquí se va "all out" (`10-motion-vdl.md` §1). Escribe
`edicion/plan.md` con estas secciones, en este orden, y preséntalo ANTES de construir (es la aprobación
de este modo, como el corte en el Modo A):
1. **Ficha:** formato · fps · duración · idioma · marca · tono · **tempo** (p. ej. 120 BPM: negra 0,5 s,
   compás 2 s) — *todos los cortes caen en la rejilla del tempo*.
2. **Qué es en una frase**, para quién, qué resuelve, los 3-4 diferenciales REALES (con el archivo del
   código del que sale cada uno) y la frase para compartir.
3. **Reglas de honestidad:** de dónde sale cada texto (literal del código), qué datos son de demo y cuáles
   ficticios (nombres neutros, sin marcas reales de terceros), y qué NO se dice (cifras de negocio no
   verificadas, logos de integraciones que no están en producción, URLs inventadas).
4. **Sistema visual:** escenario (fondo, grano, viñeta), producto (su tema y tokens), **firma geométrica**
   (una forma de la marca del cliente que se repite: el hexágono de Staynex), tipografía y acentos.
5. **Vocabulario de movimiento cerrado:** la familia VdL + 3-5 transiciones con nombre (iris con la forma
   de marca, match-cut morph, zoom-through, pull-back, whip con motion blur) y dónde va cada una. El cursor,
   en 2-3 momentos como mucho.
6. **Storyboard por actos** con columna de tiempo y de compás (♪): I · el problema/ruido → silencio de
   medio compás → II · reveal de marca → III · 2-4 highlights del producto EN USO (cada uno 2-4 compases)
   → IV · montaje/clímax + remate. Por escena: imagen, cámara, texto en pantalla, sonido.
7. **Mapa de sonido** (momento → sonido) y **ledger** de cortes (`10-motion-vdl.md` §5).

- **Forma:** Gancho (2-3s) → Revelación (2-4s) → 2-3 highlights del producto EN USO → Remate + endcard.
- **Duración:** 18-30s (vertical 1080×1920 por defecto; 1080×1350 si va como vídeo en el feed de LinkedIn).
  Film de producto para web/presentación: hasta ~60 s en 1920×1080 a 60 fps (Staynex: 58 s).
- **Tono:** parte de los presets de brag (`polished`, `cinematic`, `deadpan`, `app-store`…) pero con la
  voz de la marca (ver `estilo.md`). Por defecto: **polished**.

### Leyes creativas (de brag, adaptadas)
- **Claro para un desconocido:** tras verlo una vez se entiende qué hace, para quién y por qué importa.
- **El gancho lo es todo:** los 2 primeros segundos se planifican primero.
- **Enseña la cosa:** reutiliza lo REAL (su UI, componentes, textos, colores) antes que recrearlo. Mejor
  el producto funcionando que una landing describiéndolo. Nada de relleno abstracto.
- **Específico:** usa sus textos y su normativa/dato real. Prohibido el lenguaje SaaS genérico.
- **Legible:** ~0,3s por palabra desde que la línea está entera en pantalla. El ritmo sale del movimiento
  y los cortes, nunca de quitar el texto antes de tiempo.
- **Vivo:** clics simulados, tecleo, elementos que aparecen uno a uno, mejor que diapositivas quietas.
- **Cada fotograma publicable.**
- **Nada inventado:** cifras, claims y testimonios solo si están en la fuente.

## 3. Identidad: la de la marca envolviendo el producto

- El **marco** es el de la marca (`estilo.md`): su fondo, su tipografía, sus rótulos y su cierre
  (en VdL: fondo liquid animado, Sora/Onest, acento lime y la cortinilla oficial).
- El **producto** se enseña con SU identidad (sus colores, su tipografía, su UI) dentro de un marco:
  móvil, ventana de navegador o polaroid. Así se distingue "la marca que cuenta" de "el producto que enseña".

## 4. Construir (Hyperframes)

Mismas reglas del motor (`02-motion-graphics.md`): cada fotograma función pura del tiempo, sin
`Math.random()`/`Date.now()`, fuentes e imágenes cargadas antes de capturar, props animables solo por
transform/opacity.

- Composición sin `<video>` de cámara: `npx hyperframes init motion --example blank --resolution portrait --non-interactive`
  (sin `--video`) y fija `data-duration` a la duración del storyboard.
- UI del producto recreada en HTML/CSS con sus tokens reales (colores, radios, tipografía) y datos
  ficticios. Móvil: marco de 390×844 escalado. Escritorio: ventana de navegador con barra.
- Transiciones: no hagas crossfade entre dos layouts cargados (doble exposición sucia). Sale lo viejo,
  entra lo nuevo, o "pasar página" por el fondo.
- **Una toma continua:** ledger primero, cortes estampados con `seam-stamp`, match-cuts/morphs a mano con
  su portador, y un héroe (o la firma geométrica) presente > 60 % del tiempo (`10-motion-vdl.md` §4-5).
- **Catálogo primero** (`11-catalogo-y-recetas.md`): marcos de dispositivo, cursor, chats, contadores,
  mapas… se adaptan del registro antes de escribirlos. Para una pieza corta, valora re-marcar una
  plantilla de HeyGen (`11-catalogo-y-recetas.md` §3).
- **Gates:** `check` a 0 errores + `seam-gate.mjs verify` exit 0 + bucle de `12-revision-visual.md`
  (todo ≥ 8) ANTES del render final.

## 5. Sonido

Sin voz: el sonido cuenta. Usa la **librería CC0** (`sfx-kit.sh`): teclas en el tecleo, clics en las
pulsaciones, `card-slide`/`card-place` en tarjetas y páginas, `impactWood_*`/`impactSoft_medium` en los
reveals, `impactBell_heavy_000` UNA vez en el remate. Pocos sonidos y bien puestos.
**Música:** la de brag (ende.app) NO tiene licencia verificada → no se usa. Por defecto, **partitura
original sintetizada** con `plantillas/score-plantilla.py` (ver `03-sfx-y-qc.md` §Música original), en la
misma rejilla de tempo que el storyboard, con el silencio de medio compás antes del reveal. Máster con
`scripts/mux-master.sh` (−14 LUFS).

## 6. Entregar

1. Render → `AF/VIDEO-<nombre>-FINAL.mp4` + cierre de marca (`cierre.sh`) + **miniatura en frame 0** (`poster.sh`).
2. `AF/share-copy.txt`: 1-3 frases publicables en la voz de la marca, sin "estamos emocionados de anunciar".
3. Revisor (Fase 5) con los checks del Modo B: datos ficticios, cero secretos, texto legible, nada inventado.
