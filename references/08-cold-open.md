# 08-cold-open.md — Cold open de VdL (0-3s)

Los **primeros 1-3s deciden el scroll**. VdL usa cold open **siempre**: se antepone lo más potente
antes del saludo. Se monta como **clip aparte** y se une con `ffmpeg concat` (NO dentro del timeline,
para no romper la sincronía del cuerpo). Sin imágenes IA (no activadas): el gancho es real o tipográfico.

## Estilos (elige según el contenido de ESE vídeo)

**A · Resultado-real (default).** Enseña el payoff antes de explicarlo: la cifra/resultado/demo más
fuerte a pantalla completa que estalla y revela la cara.
- Dato gigante en **Sora 600** (keyword en lime) que LLEGA en Z (`revela`: `scale 1.25→1`, `blur 10→0`,
  `expo.out` 0.5s). Cuando ya se ha leído (~1.2-1.5s), **inverse zoom-through**: el dato se aleja
  (`1→0.8`, blur 10, `power3.in` 0.2s) y la cámara llega también alejándose (`1.25→1`, `expo.out`).
  Mismo signo de Z a los dos lados del corte (`10-motion-vdl.md` §4); sin shake. El `flash` solo si este
  es uno de los ≤ 3 golpes de pantalla completa de la pieza.
- El dato **tiene que decirse** en el vídeo (nada inventado).

**B · Texto-hook.** Una frase-gancho potente (pregunta o afirmación de contraste, estilo VdL:
"Porque crecer no es vender más. Es vender mejor.") en tipografía grande sobre el fondo liquid animado,
palabra clave en lime. Úsalo cuando no hay un dato/imagen fuerte pero sí una idea que frena el scroll.

**C · Micro-tráiler (0.8s).** (Gasta golpes de pantalla completa: cuéntalos.) Ráfaga de 2-3 flashes de los mejores momentos/escenas del reel con
whooshes, y cae en la cámara. Para vídeos con varias piezas visuales potentes.

**E · Portada con recorte.** Como un texto-hook pero con la persona recortada DELANTE del titular
enorme (receta R8 de `04-recetas.md`). Para frases-tesis potentes.

## Reglas

- Legible **desde el frame 1** (primer frame ya fuerte, con contraste).
- El **titular arriba solo se permite durante el cold open (≤2s)**; en cuanto entra el cuerpo, el texto
  baja a la altura del micro. Texto arriba después del cold open = fallo (lo marca el revisor).
- Impact-landing sonoro: `riser`/`whoosh` que sube → `boom`/`ding` que cae EXACTO en el corte al cuerpo.
- Fondo: el degradado **liquid animado** de marca (ver `estilo.md`), nunca color plano.

## Montaje (clip aparte + concat)

```bash
# render del cold open como composición corta (~1-3s) -> coldopen.mp4 (misma resolución que el cuerpo)
# luego:
printf "file 'coldopen.mp4'\nfile 'reel-cuerpo.mp4'\n" > motion/concat.txt
ffmpeg -f concat -safe 0 -i motion/concat.txt -c copy motion/renders/reel-full.mp4
# si difieren de códec/resolución, re-encodea en el concat en vez de -c copy.
```

## Loop de retención

Tras publicar, si VdL comparte la retención-3s: caída en seg 1 → primer frame más fuerte; caída en
seg 3 → promesa floja, reescribe la frase-gancho. Alimenta el cold open del siguiente reel.
