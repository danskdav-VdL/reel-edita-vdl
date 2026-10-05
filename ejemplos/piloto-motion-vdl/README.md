# Piloto de motion VdL (2026-10-02)

Pieza vertical de 12 s hecha para PROBAR de punta a punta la capa de diseño nueva en Windows, siguiendo
`references/10`, `11` y `12` al pie de la letra. Es una referencia de **técnica**, no un entregable
(datos ficticios, sin cortinilla porque en ese PC no estaba).

Qué demuestra:
- fondo liquid de marca como única capa ambiente (`data-layout-allow-overflow` en los blobs);
- waterfall entry (cascada binaria que acelera) + push-in con intención en la escena 1;
- corte en Z con el signo casado (inverse zoom-through) a 4 s y **cut-the-curve a la izquierda** a 8 s,
  estampados desde `ledger.json` y verificados con el Seam Gate (PASS);
- UI que vive: cursor grande que entra de fuera, clic con aplastamiento + onda y cambio de estado en el
  MISMO frame, pausa de 0.35 s antes del resultado, respuesta que aterriza en su hueco, nudge curve;
- partitura original (`edicion/audio/compose.py`, de la plantilla) con los cortes en la rejilla de 120 BPM;
  máster a −14 LUFS; miniatura en el frame 0.

Rehacerlo:
```bash
export HYPERFRAMES_SKIP_SKILLS=1
npx hyperframes check . --at-transitions --caption-zone "x0=0;y0=.84;x1=1;y1=1;severity=error"
node ~/.claude/skills/motion-doctrine/scripts/seam-gate.mjs verify --ledger ledger.json --project .
npx hyperframes render --quality high -o renders/cuerpo.mp4
python3 edicion/audio/compose.py
bash ~/.claude/skills/reel-edita-vdl/scripts/mux-master.sh renders/cuerpo.mp4 edicion/audio/mix.wav AF/VIDEO-piloto-motion-FINAL.mp4
bash ~/.claude/skills/reel-edita-vdl/scripts/poster.sh AF/VIDEO-piloto-motion-FINAL.mp4 11.8
```
Notas del bucle de autocrítica: ronda 1 → gancho 6, composición 6 (hueco en blanco en la tarjeta),
movimiento 7 (el cursor no clavaba el botón). Ronda 2 → todo ≥ 8 salvo el gancho (7: es solo tipográfico;
con material real del producto sube). Fuentes Sora y Onest: SIL Open Font License (Google Fonts/Fontsource).
