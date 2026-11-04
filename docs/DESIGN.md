# Space Quest III — LucasFilm-Style Remake: Design Document

Private personal project. Engine: Godot 4.3 (GDScript). Target: native Linux (Manjaro KDE), always fullscreen.
Status: design v0.1. Source for content: the AdventureDoor SQ3 walkthrough (critical path + deaths list) plus the `game_rebuild_specs.md` engine spec.

## 1. Decisions (fixed)
| Topic | Decision |
|---|---|
| Engine | Godot 4.3, GDScript, exported as a native Linux binary |
| Display | Fullscreen at start (`window/size/mode=3`), 640x400 canvas, integer-scaled with letterbox |
| Interface | LucasFilm Games (Indy LC era) SCUMM verb grid + sentence line + inventory panel; dialogue choices replace the grid |
| Fail states | Classic Sierra: deaths and possible dead ends, manual save/restore, death screen with Restore / Restart / Quit |
| Tone | Rewritten, more atmospheric and understated; humour stays dry and situational, not slapstick |
| Scope | Private. All-new art and music. No original game files are extracted or used |
| Score | Maximum 738 (taken from the in-game status line shown in the walkthrough) |

## 2. Screen layout (640x400)
- Top 0-264: scene viewport (640x264).
- 264-280: sentence line, e.g. `Use ladder with shuttle`.
- 280-400: bottom panel. Left 0-380: verb grid (3 columns x 4 rows). Right 380-640: inventory, 2 columns, scrollable.
- Score shown on demand (hotkey and menu), not as permanent HUD, in the LucasFilm spirit.
- Verbs (no Smell/Taste): Open, Close, Pick up, Look at, Talk to, Use, Push, Pull, Give, Walk to, Wear, Climb.
- Left-click: selected verb on target. Right-click: default verb (Look at for scenery, Pick up for items).
- Dialogue: panel replaced by 2-5 selectable lines.
- Menu (Esc): Save, Restore, Restart, Text speed, Sound, Quit.

## 3. Architecture
Group A engine from the spec, implemented as Godot scenes plus data files.

| Piece | Implementation |
|---|---|
| Room | Godot scene: background, walk polygon (NavigationRegion2D), depth bands, hotspots (Area2D), exits, entry points |
| Actor | Node2D with AnimatedSprite2D, walk speed, facing, talk colour |
| Hotspot | Name, per-verb handlers keyed by verb id; a fallback handler per verb |
| Inventory | Ordered array of item ids; item defs in `data/items.json` |
| Game state | Autoload `GameState`: flags, counters, inventory, score events, current room |
| Scripts | Small GDScript coroutines using the command set: say, walk_to, face, play_anim, give_item, take_item, has_item, set_flag, flag, add_score, change_room, start_timer, die, wait, dialogue |
| Score | `add_score(event_id, points)`, event ids unique, so points are earned once |
| Death | `die(death_id)` shows the title and an unique scene; deaths in `data/deaths.json` |
| Save | JSON in `user://saves/`, containing GameState and room id; unlimited named slots |
| Minigames | Self-contained scenes that return a result: Astro Chicken, radar/shield combat, robot duel, grabber rail ride |

## 4. Content bible (from the walkthrough)
Derived structure only. All text and puzzle steps are re-written for the new tone. Point values per event are not in the walkthrough and still need to be assigned (total must equal 738).

### 4.1 Garbage freighter
Beats: find the pod's location, note the warp motivator and shuttle; collect wire; stand at the robot head's eye and look at the shuttle; ride the conveyor to the upper level and jump before the shredder; use the grabber on the light-blue rail; grab the warp motivator and release it at the shuttle's open panel; drop down the chute; take the reactor from the hole; a rat steals items; recover reactor and wire and take the ladder; climb the shuttle, open the hatch, install reactor and wire; search the seat for buckazoids; start the shuttle via the cockpit computer.
Items: wire, reactor, ladder, buckazoids (350).
Shuttle computer: menu-driven. Engines (1), Navigation (2: Scan, Set Course, Light Speed), Takeoff (3), Radar (7), Weapons (8), Land (3). Front shields (F), back shields (B).
Hazards: chasm by the robot head, sharp metal plate, conveyor shredder, stepping off rails, grabber fall, robot gunfire, rat-and-chute, falling off the shuttle roof, flying without radar, shutting off engines after takeoff, firing lasers without shields.

### 4.2 Phleebhut
Beats: leave the shuttle; World o' Wonders shop; sell the gem (refuse the first two offers, accept the third); buy orat on a stick, Astro Chicken flight hat, ThermoWeave underwear; the terminator pursues you.
Two terminator solutions: fast (Mog's head, pulleys) gives fewer points; full (lure it under the hanging pods in the cave) gives full points and the invisibility belt (use the stick).
Hazards: snake, scorpazpoid, hanging pods, lightning, display case, terminator, Mog's head machinery and elevator shaft.

### 4.3 Monolith Burger
Beats: order the Monolith Fun Meal (option 7), pay, eat at the empty table to get the decoder ring; play Astro Chicken, land 10 times, decode the message with the ring.
The message (to be re-written): the Two Guys are held by ScumSoft on Pestulon, behind a force field that must be switched off, guarded by jello pistols.
Hazards: entering the alien ship twice.
Astro Chicken losing is not a death, but spending all coins makes the game unwinnable.

### 4.4 Ortega
Beats: wear thermal underwear before walking out; cross the shaky bridge; hide behind the rocks until the men leave; use the telescope; take the thermal detonator from the green box; climb the long ladder, drop the detonator into the dome; take the pole from the wind meter; pole-vault the chasm (without the detonator).
Hazards: no underwear, lava pit, being seen by the ScumSoft team, falling from the dome, carrying the detonator over the bridge or while pole-vaulting.

### 4.5 Pestulon / ScumSoft
Beats: wear the belt, exit; the force field is now down; enter the building; push the red button; coveralls and vaporizer from the closet; office maze (vaporize each full trashcan); boss's office: wait until the boss leaves, take the keycard; take the boss's picture from the wall, copy it, re-hang the copy; use the keycard and the picture at the scanner door; Two Guys, push the button, vaporize them; robot duel; escape by shuttle; five-ship space battle with correct shield side; ending.
Hazards: guards, force field, maze in own clothes, trashcans without vaporizer (or too many misses), stealing the portrait, the pit around the Two Guys, losing the duel, wrong shield, depleted shields.

### 4.6 Death catalogue
Death titles are known from the walkthrough (e.g. "Deceleration Trauma", "It Slices, It Dices...", "Decompression Blues", "Rats!", "Hole In One!", "Sunbathing Not Recommended", "You Have Blown Your Cover", "Down For the Count"). Each gets a new atmospheric description and a short animated scene.

## 5. Tone guide
- Roger is a janitor out of his depth; the world is vast, lonely and rusting rather than a joke machine.
- Humour comes from understatement and the gap between Roger and his circumstances.
- Narrator text is short and observant, with no fourth-wall breaking or direct references to the developers.
- ScumSoft becomes an unnerving corporate monoculture. The Two Guys are tired and quietly desperate.
- The "Pirates" aspect is dread: licensing, software piracy and entertainment as extraction.

## 6. Milestones
1. M0: Project scaffold, fullscreen, 640x400, verb UI shell, test room with placeholder art.
2. M1: Core engine: walking, hotspots, inventory, dialogue, flags, score, death, save/restore.
3. M2: Garbage freighter complete (rooms, puzzles, grabber ride, shuttle computer).
4. M3: Flight, radar/shield combat, Phleebhut.
5. M4: Monolith Burger plus Astro Chicken.
6. M5: Ortega.
7. M6: Pestulon, ScumSoft, robot duel, finale.
8. M7: Art pass, audio, polish, Linux export.

## 7. Open items
- Per-event score values (total 738), currently unknown.
- Room-by-room screen counts and layouts: the walkthrough gives the path but not the map.
- Full text of the rewritten script.
