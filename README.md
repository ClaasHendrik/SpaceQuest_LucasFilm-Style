# Space Quest III, LucasFilm-style remake (private project)

Godot 4.3 / GDScript. 640x480 (4:3), starts fullscreen. Lucasfilm-style interface and painterly art (pilot: first two rooms). See `docs/DESIGN.md` and `docs/CONTENT_MAP.md`.

## Run
```bash
godot --path .
```
Dev shortcuts: F2 / F3 = previous / next room; `--room=<id>` starts in a given room.
Controls: left-click = selected verb, right-click = default verb (Look at / Pick up), Esc = menu (Save/Restore/Restart/Quit), Tab = show score.

## Tests
```bash
godot --headless --path . -- --selftest      # logic: puzzle, score, save/restore, death
SHOT_DIR=/tmp xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x800 -- --shot
```

## Art and tools
- `tools/paint/` paints the new-style art (320x144 scenes at 2x, painted with gradients and light, finished with a 190-colour palette): `cd tools/paint && python3 pilot.py && python3 roger.py`. The pilot covers the escape pod and garbage mountain; the other 29 rooms still use the earlier EGA draft from `tools/art/` (`cd tools/art && python3 build.py` regenerates them; it would overwrite the pilot rooms, so run `pilot.py` afterwards).
- Font: VT323 (SIL Open Font License) in `assets/fonts/`.
- `tools/make_rooms.py` writes `data/rooms.json` (rooms, walk areas, hotspots, exits)
- `tools/make_gallery.py` builds `docs/room_gallery.pdf` (old EGA draft, all rooms); `tools/make_pilot_pdf.py` builds `docs/pilot_samples.pdf` (new style, see tests/shot_pilot.gd)

## Status
M0/M1 slice plus art pass: verb UI, inventory, score (data/points.json, 738), death screen, save/restore (one slot). 31 explorable rooms across all five acts with EGA-style art; the first two rooms have working puzzles. Navigation computer + launch lever travel between planets.
Not yet: puzzles beyond the first two rooms, dialogue trees, minigames, sound, death scenes, pathfinding beyond a single polygon.
