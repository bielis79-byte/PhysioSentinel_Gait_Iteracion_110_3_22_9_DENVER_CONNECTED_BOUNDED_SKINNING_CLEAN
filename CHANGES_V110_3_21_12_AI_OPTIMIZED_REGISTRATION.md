# V110.3.21.12 · AI/Optimization Anatomical Registration

## Qué cambia
Se sustituye el ajuste manual de pelvis/fémur/manos por registro anatómico automático
basado en piel SKEL + joints + restricciones antropométricas.

## Registro automático
Para cada frame:
- pelvis: centro y escala desde caderas + envolvente de piel;
- huesos largos: extremos reales de malla -> joints SKEL;
- escalado longitudinal exacto al segmento;
- escalado transversal desde la envolvente de piel;
- manos: tamaño y orientación desde muñeca->mano + piel local;
- se preserva la morfología Hamner sin estirar libremente cada frame.

## Control de calidad
Se calcula error proximal/distal de ensamblaje para huesos largos en el frame 1.

## Visor
Se conserva la interfaz clásica:
- Piel
- Esqueleto
- Músculo estimado
- combinaciones
- 0.5x / 1x / 2x
- pausa
- slider 75 frames

## Vídeo
Se conserva:
- selección de capa
- selección de orientación
- reproducción
- descarga MP4

## Pestaña 12
Se conserva íntegra, incluido modo NPZ autónomo.

## Transparencia metodológica
No se incluye un modelo neuronal entrenado.
"AI/Optimization" significa registro automático multirrestricción.
El esqueleto sigue siendo anatomía genérica Hamner ajustada a SKEL, no CT/MRI individual.
La capa muscular sigue siendo funcional/estimada, no volumetría muscular individual.
