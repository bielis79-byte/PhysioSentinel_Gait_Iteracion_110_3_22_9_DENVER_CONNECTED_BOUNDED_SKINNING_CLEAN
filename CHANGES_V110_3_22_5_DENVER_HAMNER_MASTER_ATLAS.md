# V110.3.22.5 · Denver-Hamner Master Atlas

Cambio arquitectónico principal:
Denver ya no se ajusta directamente e independientemente a cada frame SKEL.

Pipeline:
1. ZIP Denver -> carga y limpieza ligera STL.
2. Se conserva el sistema de coordenadas común original del atlas.
3. Se infieren unidades de forma global (mm -> m cuando corresponde).
4. Se construye y cachea un MASTER ATLAS muscular.
5. Se define un frame donante común por segmento:
   pelvis / muslo / pierna / pie.
6. Frame 1:
   MASTER Denver -> jerarquía OpenSim/Hamner -> SKEL.
7. Frames 2-75:
   no se repite PCA ni fitting.
   Se aplican transformaciones rígidas de segmentos.
8. Músculos bi/multiarticulares:
   deformación attachment-aware entre los dos segmentos anatómicos relevantes.

Consecuencias:
- se evita el PCA independiente por músculo;
- se preserva la relación espacial original entre STL;
- huesos siguen siendo OpenSim/Hamner;
- Denver solo aporta músculo volumétrico;
- el atlas maestro se cachea y no debe reprocesarse para cada frame;
- interfaz única de reproducción y descarga se conserva.

Limitaciones:
- todavía no se calculan fuerzas, activaciones ni momentos;
- el wrapping se aproxima mediante cadenas anatómicas y skinning, no por un solver OpenSim completo;
- sigue siendo un atlas de referencia registrado, no anatomía individual obtenida por CT/MRI.
