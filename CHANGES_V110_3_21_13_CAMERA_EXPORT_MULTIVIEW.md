# V110.3.21.13 · Camera Export + Multiview

## Problema corregido
Los MP4 se renderizaban con una cámara distinta a la utilizada en el visor y podían
aparecer torcidos, desplazados o inclinados.

## Cámara exportable
Nuevo modo `Manual exportable`:
- azimut
- elevación
- rotación (roll)
- zoom

La misma configuración se aplica al visor y al MP4.

## Importante
El giro libre hecho sólo con el ratón dentro del iframe Plotly no puede ser leído de forma
fiable por Streamlit. Por eso se ofrece una cámara manual reproducible mediante controles.

## Exportación multivista
Nuevo MP4 secuencial:
1. frontal
2. lateral derecha
3. posterior
4. lateral izquierda
5. superior
6. oblicua

Cada orientación reproduce el ciclo completo de 75 frames.

## Estabilidad de encuadre
- proyección ortográfica;
- límites fijos para todo el vídeo;
- centro corporal robusto;
- sin recentrado frame a frame;
- ejes ocultos en exportación;
- evita inclinaciones/desplazamientos espurios.

## Capas
Se mantiene selección:
- Piel
- Esqueleto
- Músculo estimado
- Piel + Esqueleto
- Esqueleto + Músculo
- Todas

## Pestaña 12
Se conserva íntegra.
