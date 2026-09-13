# V110.3.22.8 · Denver realistic skeleton + muscles + export NameError fix

## Corrección del error Streamlit
Se corrige el NameError mostrado al entrar en Pestaña 8:
`_v3227_render_export_all_tabs_10_11_12` se estaba llamando antes de que Python
hubiera ejecutado su definición. La función de Exportar TODO queda ahora definida
antes de `with tabs[7]:`.

## Nuevo modelo visual anatómico
Cuando se carga el ZIP Final 3D STL Models de Denver:

VISUAL:
- huesos reales segmentados Denver para pelvis y miembros inferiores;
- músculos volumétricos Denver;
- tronco, brazos y manos Hamner solo como fallback visual, porque el dataset
  Denver empleado es de miembro inferior.

RIG / MOVIMIENTO:
- OpenSim/Hamner sigue siendo la jerarquía cinemática interna;
- SKEL aporta joints, antropometría estimada y los 75 frames;
- las STL Denver se registran al rig y después siguen sus transformaciones.

## Diferencia respecto a V110.3.22.7
Ya NO se enseñan huesos Hamner simplificados en la extremidad inferior cuando
Denver está disponible. Las mallas visibles de pelvis, fémures, tibias, peronés,
talus, calcáneos y huesos del pie proceden del atlas Denver.

## Registro anatómico
- atlas Denver conserva sus coordenadas compartidas;
- cada segmento se registra como grupo rígido;
- no se hace PCA independiente de cada hueso;
- los huesos permanecen rígidos durante los 75 frames;
- los músculos usan el retargeting attachment-aware introducido previamente.

## Conservado
- exportación MP4 a FPS fijo;
- cámara manual exacta;
- modo multiplano;
- Pestaña 12 no duplicada en Pestaña 11;
- Pestaña 8 Exportar TODO, incluyendo Tabs 10/11/12.

## Limitación metodológica
Es una anatomía de referencia registrada al paciente estimado por vídeo.
No equivale a CT/MRI individual. Denver aporta alta fidelidad morfológica, no
la anatomía específica del paciente.
