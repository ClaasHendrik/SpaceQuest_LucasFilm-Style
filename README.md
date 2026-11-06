# Space Quest III, LucasFilm-style remake (private project)

Godot 4.3 / GDScript. 640x480 (4:3), starts fullscreen. Lucasfilm-style interface and painterly art for every room. See `docs/DESIGN.md` and `docs/CONTENT_MAP.md`.

## Run
```bash
godot --path .
```
Dev shortcuts: F2 / F3 = previous / next room; `--room=<id>` starts in a given room; env `HOTSPOTS=1` outlines clickable areas and walkable ground.
Controls: left-click = selected verb, right-click = default verb (Look at / Pick up), Esc = menu (Save/Restore/Restart/Quit), Tab = show score.

## Tests
```bash
godot --headless --path . -- --selftest      # logic: puzzle, score, save/restore, death
SHOT_DIR=/tmp xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x800 -- --shot
```

## Art and tools
- `tools/paint/` paints all art: `cd tools/paint && python3 build_all.py` (every room, 320x144 scenes shown at 2x, painted with gradients and light and finished with a 190-colour palette) and `python3 roger.py` (the Roger sprite sheet). Rooms: `pilot.py` (escape pod, garbage mountain), `p_act*.py` (backgrounds), and `s_act*.py` (the same rooms rebuilt with solid objects; these override `p_act*`). Shared helpers: `paint.py` (canvas, lighting), `kit.py` (gradients, ridges, text) and `solid.py` (lit-plane boxes, spheres, cylinders, rock faces, ladders, figures, the Mallard ship).
- Font: VT323 (SIL Open Font License) in `assets/fonts/`.
- `tools/make_rooms.py` writes `data/rooms.json` (rooms, walk areas, hotspots, exits)
- `tools/make_gallery.py` builds `docs/room_gallery.pdf` (all rooms, from in-game screenshots made by tests/shot.gd); `tools/make_pilot_pdf.py` builds `docs/pilot_samples.pdf` (the art pilot)

## Status
M0/M1 slice plus art pass: verb UI, inventory, score (data/points.json, 738), death screen, save/restore (one slot). 31 explorable rooms across all five acts, all painted in the Lucasfilm style. **Act 1 (the garbage freighter) is fully playable, from the escape pod to the escape: all 15 point events (145 points), timers, deaths and the ship's computer. See docs/act1_walkthrough.pdf.** Acts 2-5 are explorable but have no puzzles yet. Navigation computer + launch lever travel between planets.
Not yet: puzzles in Acts 2-5, dialogue trees, minigames, sound, death scenes, pathfinding beyond a single polygon.
