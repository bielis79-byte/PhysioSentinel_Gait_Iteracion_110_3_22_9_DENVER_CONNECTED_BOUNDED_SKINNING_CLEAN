# V110.3.21.6 · Hamner Walking Animation

## Problema
En V110.3.21.5 el selector "Frame" permitía inspeccionar frames 1..75,
pero el modelo no reproducía la marcha automáticamente.

## Corrección
Se añade un render offline secuencial de los 75 frames ya calculados:

NPZ/SKEL existente
→ joints + skin frame 1..75
→ registro Hamner por frame
→ render secuencial
→ MP4 H.264 a 25 fps

No:
- recalcula fitting;
- reprocesa frontal/lateral;
- genera nuevos q(t);
- captura el navegador.

## UI
Nuevo botón:
`▶ Generar animación Hamner caminando · 75 frames`

Después:
- reproductor de vídeo dentro de Streamlit;
- descarga MP4.

## Conservado
- V110.3.21.5 proporciones antropométricas;
- orientación corregida de pelvis/sacro, pies y manos;
- esqueleto interno SKEL;
- FIX de pestaña 12 en modo NPZ autónomo.
