# V110.3.22.6 · Fixed-FPS Video Export + Tab 12 cleanup

## Corrección del vídeo
Se sustituye la grabación MediaRecorder en tiempo real por una exportación determinista:

75 estados SKEL ya calculados
→ actualizar explícitamente cada frame Plotly
→ esperar a que WebGL termine de dibujar
→ capturar la misma cámara que el usuario dejó manualmente
→ codificar H.264 mediante WebCodecs
→ mux MP4 con timestamps matemáticos y FPS constantes.

Esto evita el fallo observado en el MP4 anterior:
- 74 frames pero ~0.66 fps
- duración ~112 s
- apariencia de modelo congelado.

Duración esperada para 75 frames:
- 0.5x: ~6.0 s
- 1x: ~3.0 s
- 2x: ~1.5 s

La velocidad de renderizado de Plotly ya NO determina la velocidad del vídeo final.

## Cámara
Se conserva exactamente la orientación manual actual.
Si "Ver en varios planos" está activado, el MP4 conserva la secuencia multiplano.

## Pestaña 12
Eliminado el encabezado y texto duplicado de "Pestaña 12" que aparecía dentro
de la pestaña 11 / visor anatómico. La Pestaña 12 real queda únicamente en su
pestaña propia de resultados y valoraciones.

## Arquitectura anatómica conservada
- Piel = SKEL
- Esqueleto = OpenSim/Hamner
- Músculo = Denver Visible Human
- atlas maestro Denver-Hamner de V110.3.22.5
