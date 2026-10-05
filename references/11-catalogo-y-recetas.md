# 11-catalogo-y-recetas.md — Catálogo primero, recetas premium y plantillas de HeyGen

## 1. Regla: catálogo PRIMERO, a mano después

Antes de construir a mano cualquier efecto con nombre (un contador, un mapa, un subtítulo con estilo, un
lower-third, una transición, un marco de móvil, un chat de IA…), **búscalo en el registro de HyperFrames**
(~390 bloques y componentes probados; skill `hyperframes-registry`):

```bash
npx hyperframes catalog <palabras>            # p. ej. "catalog count up", "catalog map spain"
npx hyperframes catalog --tag transition      # por etiqueta: text, data, transition, lower-third, vertical…
npx hyperframes catalog --json > catalogo.json   # todo, con descripción, tamaño y URL del vídeo de muestra
(cd motion && npx hyperframes add <nombre>)   # bloque -> compositions/<nombre>.html · componente -> compositions/components/
```
- **Mira la muestra antes de elegir** (`preview.video` en el JSON, o `snapshot` tras añadirlo): los nombres
  engañan (`vfx-liquid-background` es una distorsión líquida sobre una web de ejemplo, NO un fondo de marca).
- `add` copia el snippet al portapapeles de Windows (inofensivo, pero sobrescribe lo que tuvieras copiado).
- **Bloque** = sub-composición propia (`data-composition-src`, a su tamaño; muchos son 1920×1080 → para
  vertical, mételo en un marco o adapta su layout). **Componente** = snippet HTML/CSS/JS que se pega.
- **Adáptalo a VdL** siempre: colores → tokens de `estilo.md`, fuentes → Sora/Onest, y sus curvas → la
  familia de `10-motion-vdl.md` (salvo que el movimiento del bloque sea justo lo que quieres). Pasa `check`.
- Nunca uses del catálogo: endcards/logo-outro/cta-close/logo-sting (el cierre es SIEMPRE la cortinilla
  oficial), ni nada que meta el isotipo o el nombre "Valor de Ley" en el cuerpo.

### Candidatos útiles para VdL (verifica la muestra; la lista no sustituye a buscar)
| Necesidad | Del catálogo |
|---|---|
| Texto cinético | `per-word-rise`, `kinetic-center-build`, `kinetic-type-swap`, `type-match-cut`, `text-match-cut`, `marker-highlight`, `inline-highlight`, `variable-axis-type`, `svg-mask-reveal`, `texture-mask-text` |
| Subtítulos (respetando `07-subtitulos.md`) | `caption-highlight`, `caption-pill-karaoke`, `caption-weight-shift`, `caption-editorial-emphasis` |
| Rótulos / lower-third | `lt-accent-underline`, `lt-side-rule`, `lt-mask-reveal`, `lt-kicker-name` |
| Datos y cifras | `count-up`, `number-wheel`, `chart-story`, `conic-progress-ring`, `animated-bar-chart`, `data-chart`, `spain-map` (coropletas de España), `world-map` |
| Producto / UI (Modo B, R2, R9) | `browser-device-stage`, `device-frame-stage`, `ui-focus-zoom`, `gesture-tap`, `press-ripple`, `typed-prompt`, `streaming-text`, `notification-stack`, `native-notification-pop`, `modal-morph`, `morph-swap`, `state-chip-rail`, `screen-flow-carousel`, `oversized-cursor`, `tracing-beam` |
| IA / chats (vertical) | `ai-chat-reveal`, `claude-exchange`, `chatgpt-exchange`, `message-thread-reveal`, `notes-reveal` |
| Diagramas / sistemas | `flowchart-vertical`, `constellation-hub`, `grid-card-assemble`, `code-terminal-run` |
| Comparar | `before-after-wipe`, `comparison-split`, `split-tilt-cards` |
| Prueba social | `logo-wall`, `trust-strip`, `testimonial-card`, `x-post`, `yt-comment-card` |
| Cámara y cortes | `cut-the-curve`, `match-cut`, `whip-pan-cut`, `iris-reveal`, `zoom-through-transition`, `push-in`, `pull-back-reveal`, `parallax-device-dive`, `focus-rack`, `motion-blur` |
| Momento estrella (1-2 por pieza) | `cinematic-zoom`, `sdf-iris`, `domain-warp-dissolve`, `light-leak`, `ui-3d-reveal`, `liquid-glass-notification` |
| Textura | `grain-overlay` (grano fino ~4-6 % en Modo B; en Modo A casi nunca) |

## 2. Recetas premium (qué hace que cada una "se vea cara")

Adaptadas de `charlie947/motion-graphics-skills` (effects.md, MIT), de las plantillas de HeyGen y del film de
Staynex. Construir SIEMPRE con la familia de `10-motion-vdl.md` y en la timeline pausada de HyperFrames.

| Receta | Qué es | Lo que la hace premium |
|---|---|---|
| **Objeto que se transforma** (botón → reproductor, burbuja → ticket) | un mismo objeto cambia de forma | es UN objeto (shared element), nunca un fundido entre dos; queda un "fantasma" tenue del origen; el contenido nuevo aparece en la 2.ª mitad, cuando ya hay sitio |
| **Búsqueda → resultados** | la caja se abre, se teclea, entran resultados | la caja se abre ANTES de teclear (no compiten); resultados escalonados que suben 14 px; cada uno con UN dato real |
| **Tarjeta → espacio de trabajo** | una tarjeta crece hasta la app completa | el título viaja de la tarjeta a la barra de la ventana (no se duplica); guías discontinuas de esquina a esquina; el contenido espera a pasar la mitad |
| **Pestañas** | la selección pasa a otra pestaña | la píldora se ESTIRA (borde delantero primero, el trasero un beat después) y se encoge al llegar |
| **Barras → línea** | el gráfico cambia de forma | los valores no cambian (la gente se fía); la línea se DIBUJA, no aparece |
| **Zoom a un KPI** | una cifra sale del dashboard | corchetes de acento "marcan" el elegido antes de moverse; crece desde su posición real; el resto se atenúa |
| **Texto enmascarado** | la imagen/color sube DENTRO de las letras | solo se ve dentro de las letras; la segunda línea entra por máscara, no por fundido |
| **Titular → maquetación** | una frase se recoloca en un layout editorial | es el mismo texto que viaja (no se reescribe); lo demás llega en orden de lectura |
| **Persianas** | lamas que se abren sobre una imagen | en secuencia, cada lama con un filo de luz (objeto físico) |
| **Capas en perspectiva** | las capas de un sistema se separan en profundidad | un solo punto de fuga; cada capa conserva contenido real |
| **Lupa** | una lente recorre una tabla borrosa | solo lo de dentro de la lente está nítido, a 1.1×, con un borde de cristal |
| **Caminos con pulsos** (n8n, flujos) | pulsos de luz viajan entre nodos | el nodo RESPONDE al llegar el pulso (causa→efecto); la línea la dibuja el pulso |
| **Campo → orden** (Staynex, actos I-II) | caos de elementos que se ordena alrededor del héroe | el caos acelera hacia cámara, corte a negro + medio compás de silencio, y el reveal llega sobre el orden |
| **Hypercut final** (Staynex) | 4 planos de 0.5 s con whip + motion blur | SOLO una vez y en el clímax; cada plano con un nombre grande y real |

## 3. Plantillas de HeyGen (código Apache-2.0; sus ASSETS no se usan)

`github.com/heygen-com/hyperframes-launches` — el código de sus vídeos de lanzamiento. En
`heygen-apple-motion/` hay 4 plantillas pensadas para re-marcar (01 UI sting 720², 02 bouncy UI 1080²,
03 message sting 720², **04 generate-reel 720×1280 vertical**) y ~20 lanzamientos completos como referencia.

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/heygen-com/hyperframes-launches.git /tmp/hfl
cp -r /tmp/hfl/heygen-apple-motion/04-generate-reel <proyecto>/motion     # solo código; sin sus vídeos/fuentes/logos
```
Re-marcar = cambiar la CAPA DE MARCA y dejar el movimiento intacto (lo explica su `README.md`, léelo):
- **Cambia:** textos, colores (tokens VdL), marcas (las del cliente; VdL sin isotipo), `@font-face`
  (Sora/Onest, con nombre de familia propio para que el render no la sustituya), iconos, superficies.
- **Escribe la historia del cliente en los beats** (son huecos, no pantallas fijas): selección → envío →
  trabajo en curso → resultados que llegan como objetos → salida.
- **No toques:** números de frame, `duration`, `data-start/data-duration`, curvas, arrays por frame,
  constantes de muelle, tweens de los wrappers, la ruta del cursor. Trae `ledger.json`: pásale el gate.
- Lo que dependa del ancho de un texto (banda de selección, etiquetas) se re-mide tras renderizar una vez.
- Vertical a 1080×1920: `npx hyperframes render --resolution portrait-4k` (3×, entero) y reescala con
  `ffmpeg -vf scale=1080:1920:flags=lanczos`. Después: SFX/partitura, cierre, miniatura (como siempre).
- Sus fuentes, logos, vídeos y música NO tienen licencia Apache (ver su NOTICE): no se usan.

## 4. Packs de terceros revisados (2026-10-02) — ninguno instalado, se aprovechó lo bueno

| Repo (commit) | Veredicto | Por qué no se instala | Qué se trajo aquí |
|---|---|---|---|
| `charlie947/motion-graphics-skills` (4cd156a) | seguro | `reel-export`/`launch-video` chocan con esta skill; `brand-intake` escribe en CLAUDE.md; su contrato no es el de HyperFrames | recetas (§2), zona segura vertical, parámetros de exportación |
| `emilkowalski/skills` (d16ebe6) | seguro | son de UI web: "anima esto" las dispararía en vídeo con reglas de <300 ms | curvas y reglas de entrada (`10-motion-vdl.md` §2) |
| `IskakovDamir/apple-motion` (d0a9c10) | seguro | solo Remotion; su descripción pisa el Modo B | ritmo medido de Apple (`10-motion-vdl.md` §8) |
| `Vincentwei1021/video-shotcraft` (5ddbf52) | **reservas serias** | invita a subir el vídeo a un issue PÚBLICO de GitHub (fuga de material de cliente), arranca servidores solo, Remotion de pago | reglas estéticas por caso (`10-motion-vdl.md`, `03-sfx-y-qc.md`) |
| `bangtutorial/bang-motion` (c1aa65e) | seguro con reservas | formato propio incompatible; se solapa con todo; en indonesio | pruebas anti-PowerPoint (`12-revision-visual.md`) |
| `iart-ai/javascript-animation-skills` (f7d0882) | seguro | otro paradigma (canvas a mano) | `scripts/sync-check.mjs` (MIT) |
| `iart-ai/motion-skills` (4a98223) | seguro | no contiene skills (es un índice) | — |

Instaladas (primera parte, HeyGen): skills oficiales de HyperFrames + `motion-doctrine`, `cut-the-curve`,
`seam-craft`, `oversized-cursor` → `bash scripts/setup-capa-diseno.sh`.
