# V110.3.22.1 · Free Camera Exact-View Export

## Interfaz simplificada
Eliminados:
- azimut
- elevación
- rotación
- zoom
- selector de cámara predefinida
- paneles de exportación separados

El usuario orienta el modelo directamente con el ratón dentro de Plotly.

## Controles visibles
- Piel
- Esqueleto
- Músculo
- combinaciones
- 0.5x / 1x / 2x
- pausa
- slider 1..75
- Multiplano
- Descargar vídeo

## Descarga desde la vista actual
El botón `Descargar vídeo` registra en el navegador el mismo visor.
Antes de iniciar la grabación se captura la cámara Plotly actual.
Durante los 75 frames se fuerza esa misma cámara, por lo que el vídeo conserva:
- orientación manual
- inclinación
- perspectiva visual
- encuadre de la vista

Chrome moderno intenta primero MediaRecorder MP4/H.264.
Si el navegador no ofrece MediaRecorder MP4, cae a WebM y lo comunica explícitamente.

## Multiplano
Al activar `Multiplano`, durante la reproducción la cámara pasa secuencialmente por:
1. frontal
2. lateral derecha
3. posterior
4. lateral izquierda
5. superior

La descarga conserva también el modo Multiplano cuando está activo.

## Conservado
- Visible Human high-fidelity branch
- OpenSim Hamner fallback
- registro anatómico optimizado
- Pestaña 12 completa
- NPZ standalone
