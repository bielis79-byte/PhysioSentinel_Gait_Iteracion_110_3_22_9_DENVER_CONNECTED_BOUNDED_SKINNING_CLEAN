# V110.3.21.11 · Layer Video + Orientation

## Vídeo
- Corrige el pipeline de exportación MP4 usando imageio-ffmpeg directo.
- Selección de capa antes de exportar:
  - Piel
  - Esqueleto
  - Músculo funcional
  - Piel + Esqueleto
  - Esqueleto + Músculo
  - Todas
- Reproductor dentro de Streamlit.
- Botón de descarga MP4.

## Orientación
- Frontal
- Posterior
- Lateral derecha
- Lateral izquierda
- Oblicua clínica

La misma orientación seleccionada se aplica al visor y al vídeo exportado.

## Anatomía
- Se mantiene OpenSim Hamner para esqueleto.
- La capa muscular se renombra y documenta como `Músculo funcional`:
  OpenSim/Hamner no aporta mallas musculares volumétricas anatómicas reales.
- No se vuelve a presentar esa capa como musculatura anatómica real.

## Pestaña 12
Se conserva completa y funcional en modo NPZ autónomo.
