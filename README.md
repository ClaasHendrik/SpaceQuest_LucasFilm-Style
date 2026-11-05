# Space Quest III, LucasFilm-style remake (private project)

Godot 4.3 / GDScript. 640x400, starts fullscreen. See `docs/DESIGN.md` and `docs/CONTENT_MAP.md`.

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
- `tools/art/` paints all room backgrounds (320x132, EGA 16 colours, shown at 2x) and the Roger sprite sheet: `cd tools/art && python3 sprites.py && python3 build.py`
- `tools/make_rooms.py` writes `data/rooms.json` (rooms, walk areas, hotspots, exits)
- `tools/make_gallery.py` builds `docs/room_gallery.pdf` from in-game screenshots (see tests/shot.gd)

## Status
M0/M1 slice plus art pass: verb UI, inventory, score (data/points.json, 738), death screen, save/restore (one slot). 31 explorable rooms across all five acts with EGA-style art; the first two rooms have working puzzles. Navigation computer + launch lever travel between planets.
Not yet: puzzles beyond the first two rooms, dialogue trees, minigames, sound, death scenes, pathfinding beyond a single polygon.
