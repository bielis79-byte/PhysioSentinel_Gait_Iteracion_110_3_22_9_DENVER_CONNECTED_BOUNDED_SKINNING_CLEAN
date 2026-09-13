# V110.3.22.4 · Viewer Flow Critical Fix

Corrección crítica confirmada en V110.3.22.3:
- `_html` del visor se construía correctamente.
- faltaba `components.html(_html, ...)`.
- por eso Streamlit saltaba desde el control de calidad directamente a Pestaña 12.

V110.3.22.4:
1. monta SIEMPRE el visor unificado antes de Pestaña 12 cuando Hamner está preparado;
2. invalida la caché anatómica al cargar/cambiar el ZIP Denver;
3. incluye el SHA del atlas Denver en la clave de caché;
4. conserva la interfaz acordada:
   Piel | Esqueleto | Músculo | combinaciones |
   0.5x | 1x | 2x | pausa | Ver en varios planos |
   Descargar vídeo tal como se ve;
5. mantiene cámara libre con ratón, sin azimut/elevación/zoom numéricos;
6. corrige el texto metodológico:
   Piel=SKEL, Esqueleto=OpenSim/Hamner, Músculo=Visible Human Denver.

Nota:
Esta versión corrige el flujo/visor. El registro muscular Denver sigue siendo
una estimación atlas→SKEL y debe validarse visualmente antes de considerarlo definitivo.
