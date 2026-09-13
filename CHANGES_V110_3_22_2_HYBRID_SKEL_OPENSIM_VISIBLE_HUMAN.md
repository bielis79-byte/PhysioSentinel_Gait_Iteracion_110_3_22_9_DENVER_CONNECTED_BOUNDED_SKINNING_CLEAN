# V110.3.22.2 · SKEL + OpenSim skeleton + Visible Human muscle

Arquitectura anatómica fijada:
- Piel: SKEL.
- Esqueleto: OpenSim/Hamner registrado sobre joints SKEL.
- Músculo volumétrico: Visible Human cuando el ZIP está cargado.
- Fallback muscular: trayectos funcionales OpenSim/Hamner si Visible Human no está disponible.

Cambios:
- Visible Human deja de actuar como esqueleto alternativo.
- Eliminada la vista ósea Visible Human independiente del flujo principal.
- Los huesos del visor unificado proceden exclusivamente de OpenSim/Hamner.
- Añadida secuencia muscular volumétrica Visible Human compacta para los 75 frames.
- Las tres capas comparten exactamente el mismo frame SKEL.
- Se conserva la interfaz libre V110.3.22.1: orientación con ratón, 0.5x/1x/2x, pausa, Multiplano y descarga desde la vista actual.
- Se conserva Pestaña 12.
- BodyParts3D y Rajagopal continúan fuera del flujo activo.

Nota metodológica:
Visible Human es un atlas de referencia y no representa CT/MRI individual del paciente.
