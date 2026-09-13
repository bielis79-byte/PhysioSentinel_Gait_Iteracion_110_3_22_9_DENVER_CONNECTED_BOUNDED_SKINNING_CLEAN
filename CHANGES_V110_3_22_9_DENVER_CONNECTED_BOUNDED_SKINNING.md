# V110.3.22.9 · Denver Connected + Bounded Skinning

Nueva versión basada SOLO en pruebas offline previas.

## Huesos
- Denver sigue siendo la geometría visible en pelvis y miembros inferiores.
- Se elimina el muestreo de triángulos aislados.
- Simplificación topológica mediante quadric decimation.
- Si la simplificación falla, se mantiene la malla completa.
- 1200 caras objetivo por pieza para preservar apariencia anatómica.

## Músculos
Se integra el bounded skinning probado:
- frame 1: registro morfológico completo a un segmento huésped;
- vientre central cuasi-rígido;
- deformación localizada en extremos proximal/distal;
- sin reescalado global frame a frame;
- salvaguarda de conservación de forma.

Prueba offline previa:
- ratio de tamaño anterior: 2.23–2.67x;
- ratio nuevo: 0.966–1.144x;
- mediana: 1.007x;
- criterio 0.80–1.25: superado;
- 100% de vértices de músculos ensayados dentro del bbox de piel SKEL.

## Caché
La clave incluye v110.3.22.9 para impedir reutilizar geometría rota de versiones anteriores.

## Se conserva
- cámara libre;
- 0.5x/1x/2x;
- MP4 a FPS fijo;
- multiplano;
- Pestaña 8 Exportar TODO;
- Pestaña 12 única;
- OpenSim/Hamner como rig interno y fallback de tronco/brazos/manos.

La anatomía sigue siendo atlas Denver registrado a SKEL, no CT/RM individual.
