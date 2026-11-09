# Art principles (agreed with the project owner; apply to every act)

Status: living document. Written during Act 1; to be finalised at the end of the project. Every later act must follow it.

## 1. Source and fidelity
- Each room is rebuilt from its **original screen** (the Sierra Chest screenshots): same objects, positions, colours, relations
  and perspective (target: at least 80% faithful). Free interpretation from the generated script is not allowed in the picture.
- Style target: the **Lucasfilm Games look** (Indiana Jones and the Last Crusade, VGA): smooth painted shading, no dithering,
  rounded volume on worn things, strong colour moods per scene (at least 80% emulation).
- The reference screenshots are private files. They stay out of the repository (`tools/paint/ref/` is git-ignored).
  Anything derived from them is for private use only.
- Figures (Roger, NPCs) are **painted out of the backgrounds** and drawn separately. Roger wears his **original grey jumpsuit with
  magenta sleeves and a red belt**, at about 21% of the picture height.

## 2. The three surface classes (the central rule)
Every region of every picture is classified before it is shaded:
| Class | Meaning | Treatment | Colour in the overview |
|---|---|---|---|
| **Organic** | rock, junk piles, slime, rust, people; things grown or heaped | rounded volume, lit from the top left, irregular | green |
| **Artificial** | structured, pristine: walls, floors of a clean room, panels, consoles, drive bays, pipes | flat shading, crisp straight edges, thin highlights; tubes and drums get a **cylinder gradient** | blue |
| **Worn artificial** | built as structured things, now beaten up by years of use: crashed ships, old machines, containers, battered paneled floors | **beaten up, not washed smooth**: keep the straight lines, add dents (dark upper-left, lit lower-right), scratches and grime streaks; only about 40% of the organic rounding | orange |

Rules of thumb:
- Brown (rust, rubble) and green (slime) regions are always organic.
- A large, almost rectangular region is artificial unless a zone says otherwise.
- A paneled floor in a wrecked place is **worn artificial**; a floor in a clean interior is artificial.
- When unsure, write the zone down in the room's `ZONES` entry and show the classification overlay to the owner.

## 3. Consistency
- The same object looks **identical** in every room where it appears (same dents, rust, colours). Technique: paint it once, or share
  the palette and composite only the real differences (see `build_act1.py`, ship yard).
- Marks (dents, scratches, grime) come from a **fixed pattern tied to picture position**, never from the order of regions.
- Wear stays **sparse and subtle** (agreed after a review): a few dents, a few dark scratches, a little grime. **No bright or white scratches** (they read as vapour). If an object looks 'made of damage', there are too many marks.
- One palette per picture (112 colours, no dither); pictures that show the same place share a palette.

- **Painting out figures:** never patch with copied or filled pixels (it gives repeats and boxes). Repaint the area as a proper object that
  fits its surroundings (`tools/paint/touchup.py`: the pod window as a glass pane, the empty arch as a receding tunnel). A sensible picture first, closeness to the original second.

## 3b. Animation (Lucasfilm style, not Sierra)
- Reference: the Sierra video shows content only (what happens), not the style of motion. The motion style follows the SCUMM/Lucasfilm
  conventions as far as they are known to us from stills: a character turns to face the way he walks (side, front, back; left is the side view flipped),
  a smooth 4-frame walk cycle, a deliberate pose when doing something (reach and crouch for picking up).
- Roger: 16x30 frames, sheet in `assets/sprites/roger.png` (side 0-4, front 5-9, back 10-14, pick-up 15-17; built by `tools/paint/roger.py`).
- Roger walks in a straight line to the click and stops at the first obstacle (original behaviour).
- Dangers are shown, not only told: the rats' eyes blink in the dark room, the conveyor belt runs. New animations are drawn in code over the still background.
- Still missing: climbing, falling, talking, lying flat (Act 2), and the animated deaths.

## 4. Interface and layout
- 640x480 window, fullscreen on Linux. Picture 320x160 shown at 2x (older rooms are 320x144 and sit at the top).
- Speech in the black strip on top (Roger yellow); cyan sentence line; green verb grid in five columns; magenta inventory with scroll arrows.
- Verbs: Push, Pull, Give, Open, Close, Look, Walk to, Pick up, What is, Use, Turn on, Turn off, Talk to, Travel.
  Talk to and Travel are greyed out unless something in the room responds.
- Pixel font: VT323.

## 5. Gameplay and story
- The generated act scripts are the main source for scenes and tone; the walkthrough fills the puzzle gaps; the points list
  (`data/points.json`, 738) must stay exactly reachable.
- Classic Sierra deaths (unique title, short text, painted picture) and manual save/restore.
- Humour: dry and atmospheric, close to the Lucasfilm style; keep the jokes, play them straight.
- The underwear puzzle from the generated script was dropped in Act 1 (not in the original). The Thermoweave underwear in Acts 2 and 4
  comes from the original game and the points list.

## 6. Process per act
1. Collect the original screens for the act; map them to rooms; list objects the puzzles need that the originals do not show.
2. Restyle with `restyle.py`; write the zone classification; produce the **original | redo | classification** overview and get approval.
3. Fix, room by room, on the owner's corrections (classification first, then look).
4. Wire the rooms into the game: art, hotspots, room graph, puzzles; extend the self-test so the act scores exactly its points.
5. Paint the puzzle objects the originals do not show (same principles); then animation, death pictures, script rewrite, sound.
6. Commit and push after every step; overviews go to the owner as PDFs.

## 7. Where things live
- `tools/paint/restyle.py` restyling engine; `build_act1.py` zones and per-room settings (copy for each act);
  `solid.py` / `paint.py` tools for objects the originals do not show; `deaths.py` death pictures.
- `docs/STYLE_ANALYSIS.md` analysis of the Lucasfilm reference frames.
