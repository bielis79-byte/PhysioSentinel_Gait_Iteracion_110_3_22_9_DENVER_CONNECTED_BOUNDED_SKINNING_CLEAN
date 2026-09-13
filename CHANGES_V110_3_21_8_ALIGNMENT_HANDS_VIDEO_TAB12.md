# V110.3.21.8 · Hamner Alignment + Hands + MP4 + Tab 12

Base: V110.3.21.7.

## Femur / pelvis / knee
Long bones no longer assume that native max-Y is exactly the joint center.
For femur, tibia, humerus and forearm:
- proximal endpoint centroid is estimated from the real mesh;
- distal endpoint centroid is estimated from the real mesh;
- these endpoint centroids are registered directly to the corresponding SKEL joints;
- long-axis rotation keeps an explicit pelvic transverse reference.

Expected improvement:
- hip ↔ femur head continuity;
- femur ↔ knee continuity;
- tibia ↔ ankle continuity.

## Hands
Hands were too small / practically invisible.
Now:
- constrained PCA extracts the real Hamner hand long axis;
- that axis is forced onto the anatomical forearm→hand direction;
- width and thickness are constrained independently;
- target hand length ≈ 0.80 × forearm;
- conservative bounds 0.10–0.24 SKEL units.

## Video
Preserved:
- Hamner walking animation over 75 frames.
- MP4 H.264 download.
Added:
- in-app player for SKEL skin MP4 when generated.
- MP4 download for skin.
Thus both skin and Hamner videos are viewable and downloadable.

## Tab 12
Preserved:
- curves
- ROM
- normalized angular velocity/acceleration
- smoothness
- bilateral symmetry
- coordination
- angle-angle plots
- relative 3D trajectories
including NPZ standalone mode.
