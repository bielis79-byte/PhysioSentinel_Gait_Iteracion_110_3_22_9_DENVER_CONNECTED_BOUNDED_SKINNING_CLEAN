# V110.3.22.7 · Exportar TODO ampliado

Pestaña 8 se amplía para incluir en una exportación global:
- resultados generales del registro;
- métricas existentes;
- gráficas disponibles;
- vídeos disponibles;
- resultados y salidas de Pestaña 10;
- visor / metadatos anatómicos y vídeos de Pestaña 11;
- resultados cinemáticos, ROM, suavidad, simetría, coordinación,
  ángulo-ángulo y trayectorias 3D de Pestaña 12;
- manifiesto JSON de la exportación.

Se conserva:
- exportación MP4 a FPS fijo;
- cámara manual exacta;
- modo multiplano;
- atlas maestro Denver-Hamner;
- Pestaña 12 solo en su pestaña propia.

Nota técnica:
Los vídeos generados dentro del navegador deben estar disponibles en la sesión
para poder incorporarse automáticamente al ZIP. Si el navegador los descarga
directamente sin devolver bytes a Streamlit, el ZIP incluye sus metadatos y
resultados asociados, pero no puede reinsertar un archivo que solo existe en
Descargas del navegador.
