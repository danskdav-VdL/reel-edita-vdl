# Plan — Albarán Digital (Modo B · vídeo de proyecto)

- **Fuente:** `~/iamasters-os/Albaran digital VdL` (código + `docs/00-normativa-deca.md` + `docs/manuales/01-guia-de-uso.md`).
  No se ha leído `.env*`, `certs/` ni nada de altas de clientes. App NO arrancada (apunta a producción).
- **Qué es:** software de albaranes y documentación de transporte que emite el DeCA, obligatorio en digital
  desde el 5 de octubre de 2026, con app del conductor que funciona sin cobertura y prueba de entrega (ePOD).
- **Para quién:** empresas de transporte y logística en España.
- **Ángulo:** la fecha límite (quedan días) + "lo hemos construido en VdL y ya está en producción".
- **Gancho (literal de la guía de uso):** "Desde el 5 de octubre, un camión sin su DeCA sale ilegalmente."
- **Tono:** polished-editorial (marco de Jhon) con la UI real del producto dentro de un móvil.
- **Formato:** vertical 1080×1920 · 24s + endcard (~3,5s).
- **Datos:** TODOS ficticios (Expedición 2026-0142, Talleres Norte S.L., 1234 ABC…). QR de demo apuntando a
  `albarandigital.ejemplo.es` (dominio de ejemplo, no real).

## Storyboard
| # | t | Escena | Texto que se lee |
|---|---|---|---|
| 1 | 0–3.2 | Portada (cold open D): folio, kicker, titular serif línea a línea | `// deca · transporte` · "Desde el 5 de octubre, / un camión sin DeCA / *sale ilegalmente.*" |
| 2 | 3.2–7.2 | Entra el móvil con la expedición (orden de servicio) | `// lo hemos construido en vdl` · "Albarán Digital: / *el DeCA en el móvil.*" |
| 3 | 7.2–11.8 | Tap en "Emitir DeCA" → aparece el QR | `// 01 · antes de salir` · "Se emite el DeCA. / *Con QR para la Inspección.*" |
| 4 | 11.8–16.4 | Sin conexión → firma → "1 cosa por subir" → sincronizado | `// 02 · sin cobertura` · "Se firma igual. / *Sube solo al volver la señal.*" |
| 5 | 16.4–20.4 | ePOD: firma, hora, GPS, fotos, enviado | `// 03 · al entregar` · "Prueba de entrega / *con firma, hora, GPS y fotos.*" |
| 6 | 20.4–24 | Remate | `// en producción` · "Hecho en VdL / para transportistas. / *Antes del 5 de octubre.*" |
| — | +3.5 | Endcard de Jhon | "Menos humo. Más sistemas." |

## Sonido
Sin música (la de brag no tiene licencia verificada). Kenney CC0: `card-slide` al pasar página, `drop` en
tarjetas, `click` en el tap, `impactPlate_light` en el QR, `switch` en sin conexión, `impactGlass_light`
al sincronizar, `impactBell_heavy_000` suave en el remate.
