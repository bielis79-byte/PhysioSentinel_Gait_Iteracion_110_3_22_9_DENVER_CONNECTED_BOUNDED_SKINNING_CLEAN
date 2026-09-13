# V110.3.21.9 · Unified 3-Layer Viewer

## BodyParts3D
Removed from the principal workflow.
No BodyParts3D preparation, viewer, or video controls are shown in the active interface.

## Hips
Pelvis placement is now driven mainly by the midpoint between bilateral hip joints.
Pelvis scale is tied to hip width.
This reduces separation between acetabular region and femoral heads.

## Hands and fingers
Hand geometry is anchored from the SKEL wrist joint.
The hand/finger longitudinal direction follows wrist -> hand.
PCA is only used to preserve morphology, not to choose free orientation.
Hand length is constrained to ~0.72 x forearm.

## Unified viewer
One interface now controls:
- Skin
- Skeleton
- Muscle
for the same selected frame.

## Muscle layer
BodyParts3D muscles are not used.
A functional OpenSim/SKEL muscle-path layer is shown from SKEL joints.

## Video
Same interface includes:
- Skin MP4 player + download
- Hamner MP4 player + download

## Tab 12
Preserved including NPZ standalone:
- joint curves
- ROM
- derivatives
- smoothness
- symmetry
- coordination
- angle-angle plots
- relative 3D trajectories

## Interface
Legacy/diagnostic Hamner controls are moved into a collapsed advanced section.
