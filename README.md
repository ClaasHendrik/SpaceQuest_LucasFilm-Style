# Space Quest III, LucasFilm-style remake (private project)

Godot 4.3 / GDScript. 640x400, starts fullscreen. See `docs/DESIGN.md` and `docs/CONTENT_MAP.md`.

## Run
```bash
godot --path .
```
Controls: left-click = selected verb, right-click = default verb (Look at / Pick up), Esc = menu (Save/Restore/Restart/Quit), Tab = show score.

## Tests
```bash
godot --headless --path . -- --selftest      # logic: puzzle, score, save/restore, death
SHOT_DIR=/tmp xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x800 -- --shot
```

## Status
M0/M1 slice: verb UI, inventory, score (data/points.json, 738), death screen, save/restore (one slot), two test rooms from Act 1 with placeholder art.
Not yet: real art, pathfinding beyond a single polygon, dialogue trees, sound, the rest of the game.
