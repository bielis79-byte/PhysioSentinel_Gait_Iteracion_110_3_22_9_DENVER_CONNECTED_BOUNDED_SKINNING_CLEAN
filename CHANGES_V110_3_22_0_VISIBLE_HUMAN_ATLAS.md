# V110.3.22.0 · High-Fidelity Visible Human Atlas Registration

## Cambio de rama
Se congela Hamner como modelo biomecánico/fallback y se abre una rama anatómica de
alta fidelidad basada en tejidos segmentados reales.

## Fuente inicial
University of Denver Center for Orthopaedic Biomechanics:
Visible Human Male/Female lower-extremity musculoskeletal geometry.

Licencia: CC BY 4.0.
Andreassen et al., Scientific Data 10, 34 (2023).

El dataset aporta, por sujeto:
- 28 huesos del miembro inferior/pelvis;
- 76 músculos;
- cartílagos articulares;
- ligamentos;
- geometría desde pelvis hasta pie.

## Implementación
- carga local del ZIP `Final 3D STL Models`;
- extracción sólo a caché temporal;
- detección automática de huesos/músculos/side;
- registro automático a joints SKEL;
- preservación de geometría volumétrica real;
- adaptación longitudinal al segmento;
- adaptación transversal moderada a la envolvente de piel;
- preview por frame junto a la piel SKEL.

## Transparencia
Esta primera versión de V110.3.22.x mejora de forma real el miembro inferior.
No existe en este dataset una musculatura volumétrica equivalente de cuerpo completo.
El tronco y miembros superiores seguirán en la rama Hamner hasta incorporar una fuente
abierta de calidad comparable.

## Conservado
- visor clásico V110.3.20.9-style;
- OpenSim Hamner como fallback;
- cámara exportable y multivista;
- MP4 por capa;
- Pestaña 12 completa y modo NPZ autónomo.
