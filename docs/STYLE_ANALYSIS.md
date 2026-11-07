# Style analysis: Lucasfilm Games, Indiana Jones and the Last Crusade (VGA)

Source: the user's reference screenshots (51 VGA frames, plus EGA/CGA/Japanese variants, which were set aside). The
reference images are not stored in this repository. Observations come from looking at the frames at full size and
zoomed, plus a few measurements. Colour counts were not measured: the screenshots are resampled and the count is meaningless.

## 1. Screen and interface
- 4:3 frame: a black strip on top for speech, the scene (about 70%), a cyan sentence line, then verbs (green, 5 columns)
  and the inventory (magenta, with blue scroll triangles). Already matched in the game.
- Unavailable verbs are grey ("Talk to", "Travel"). Matched.

## 2. Backgrounds
- **Painterly, not dithered.** Dither pixels are under 1% in the median VGA scene. Shading is done with 3 to 6 flat
  colour steps (banding), and occasional fine hatching for texture (stone, fur, foliage).
- **One palette per scene,** chosen for mood: blue-purple catacombs, red and cream Venice, warm brown study,
  teal and violet laboratory, blue night castle. Colours are saturated and there is strong warm-versus-cool contrast.
- **Strong perspective.** Floors are drawn as receding planes (tiles, carpets and patterns are foreshortened), with
  the horizon and vanishing lines clearly implied. Walls meet floors with a visible darker line.
- **Lighting is deliberate, and it is a set of effects:** a warm pool under a lamp (library lamp over the bookcase), a fire
  throwing yellow light on the rug, coloured light from stained glass on the floor, soft shafts, glowing windows.
  Shadows are large flat darker shapes under and beside objects, not blurred.
- About 23% of pixels are near-black: dark outlines, deep shadows and the black interface strips.

## 3. Solid objects (the main point)
Every solid object is built from planes, and every plane has its own lit tone, with small clear details:
- **Frames and doorways:** a frame has thickness, drawn as a light line on the top and left edges and a dark line on the
  bottom and right. The opening shows a darker inside with a visible depth.
- **Open doors:** the leaf is a parallelogram hinged to the frame. The free edge is *taller* than the hinge edge when
  the door swings towards the viewer. The leaf has a visible edge (thickness), panel recesses, a handle, a darker tone
  than the wall, and it throws a shadow on the wall behind.
- **Vehicles (cars):** a body in two to three tones, a dark underside and wheel arches, round wheels with bright
  hubcaps, a grille with vertical bars, chrome highlights as 1 to 2 pixel lines along the edges, headlamps as white discs, and a
  dark ground shadow under the car.
- **Aircraft and zeppelin:** simple silhouettes with a lit top, shaded belly, a rudder, wing struts as thin lines,
  and cloud-like gradients on the large hull. Detail is kept sparse, and the shape reads at a glance.
- **Furniture and props:** boxes with a lit top, a lit front and a dark side, drawers as insets, books as rows of
  small coloured rectangles (the bookcase is the best example), and objects scattered on top with their own shadows.
- **Buildings:** two-tone roof planes, plaster walls with dark timber, windows with frames and sills, steps as
  stacked bands.
- Edges are rarely pure black: dark brown, dark blue or a darker shade of the object's own colour is used for the outline
  and applied only where an object needs separating from the background.

## 4. Figures
- Small: Indy is about 14% of the scene height, about 30 px in a 218 px viewport (my Roger is 52 of 144, about 36%, which is
  much larger than the original's proportions).
- Simple faces: a few pixels for eyes and mouth, a hat or hair as one coloured block with a darker shadow side.
- Clothing in two to three tones, with the light colour on one side. Hands are one or two pixels.
- A soft darker outline only on the shadow side; the lit side relies on colour contrast.
- Poses are few: stand, walk (about four frames), a handful of action poses. Faces appear in larger close-up portraits.

## 5. Where my current art differs
| Area | Original | Mine now | Fix |
|---|---|---|---|
| Open doors | hinged leaf with thickness, correct perspective, shadow | flat quads, free edge shrinks the wrong way, no hinge or edge | a door primitive (below) |
| Cavities (locker, panels) | inside has depth: back wall, side walls, shelf, light falling in | a flat black rectangle | a recess primitive |
| Frame depth | light top-left edge, dark bottom-right edge | a plain outline | bevel helper |
| Cast shadows | large, flat, directional | soft blurred ovals, uniformly lit | directional shadow shapes |
| Light effects | lamp pools, fire, coloured light | some glows, but generic | named effects per scene |
| Texture | banded steps, hatching | noise-based grain, rust "stickers" | banding + hatching |
| Vehicles | grille, chrome, hubcaps, shadow | a single lit hull | detail layer for the Mallard |
| Figure scale | about 14% of scene | about 36% | decision needed (see below) |
| Edge colour | dark tone of the object | mostly black | per-material outline colours |

## 6. Plan
1. Build the missing primitives in `tools/paint/solid.py`: hinged door (correct perspective, thickness, handle, shadow),
   recess (a cavity with depth), bevelled frame, directional shadow, chrome highlight, banded gradient, hatching.
2. Redo the two objects the user flagged (locker and cryo door), then show them next to the originals.
3. Apply the primitives to every door, panel, cabinet and ship in all rooms, and add one named light effect per room.
4. Revisit the figures: scale, outline and colours (the original grey-and-magenta suit).

Open decision: figure scale. The original has small figures in big scenes. Mine are about 2.5 times larger, which makes
rooms feel cramped and objects less detailed. Shrinking Roger would let the scenery carry more of the picture.
