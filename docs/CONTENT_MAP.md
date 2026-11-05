# Content Map: scripts x walkthrough x point list

Basis (per project owner): the five act scripts are the main source; humour stays high. The walkthrough and the point list (`data/points.json`, 40 events, total 738, verified) fill gaps. Script text is an auto-generated, condensed adaptation (~19 pages), so it is treated as a scene outline plus tone reference, not as final text.

Legend: OK = script covers it. GAP = script lacks it, graft in from walkthrough. CONFLICT = script and walkthrough disagree, decision needed.

## Act 1: Garbage Freighter (145 pts)
Script scenes: escape pod interior > garbage mountain base > conveyor belt and crusher > reactor cavern / rat lair > overhead crane cabin > Aluminum Mallard construction bay.

| Point event | Pts | Status | Where |
|---|---|---|---|
| wire | 5 | GAP | Walkthrough: wires hanging in a corridor east of the pod. Script has no wire. |
| trash_bucket | 5 | UNCLEAR | Probably the conveyor/chute entry. Script has a drainage pipe dive instead. |
| jump_rail | 10 | GAP | Script has no rail. Replace with crane access or keep the rail. |
| grab_motivator | 15 | CONFLICT | Script lifts the reactor with a crane. Walkthrough: grabber ride lifts the warp motivator. |
| install_motivator | 15 | CONFLICT | As above. Needs the shuttle's open panel. |
| fall_chute | 5 | OK | Pipe dive into the rat lair. |
| get_reactor | 15 | OK | Reactor in the rat lair. Script uses the crane, walkthrough uses a hole and a rat steal. |
| get_ladder | 10 | PARTIAL | Script has a fixed ladder only. Walkthrough: a portable ladder after the rat steals items. |
| robot_eye | 5 | GAP | Giant robot head's eye. Not in script. |
| ladder_ship_top | 5 | GAP | Climb the shuttle with the ladder. |
| open_hatch | 10 | PARTIAL | Script: ramp lowers by itself. |
| install_reactor, install_wire | 5+5 | PARTIAL | Script installs only the reactor, by crane. |
| escape_freighter | 25 | PARTIAL | Script: ship simply lifts off. Needs cockpit computer (shields, radar, engines). |
| search_cushion | 10 | GAP | Buckazoids in the pilot's seat. Script has no money source. |

Script-only additions to keep: frostbite rule and wall locker uniform (new), TIE Fighter and Corellian freighter nods, rat on the platform and ladder escape, crusher timing scene.
Conflicts needing a ruling: crane vs grabber. Suggestion: keep the script's crane cabin as the grabber ride (same joystick-and-button action, same points) and add the warp motivator as the object grabbed.

## Act 2: Phleebhut (103 pts)
Script scenes: landing strip > World o' Wonders gift shop > canyon paths with Arnoid > stalk plant ridge.

| Point event | Pts | Status |
|---|---|---|
| sell_gem | 8 | OK (Fester Blatz; script lacks the three-offer haggling) |
| buy_hat | 5 | CONFLICT: script buys an "Astro Chicken Hint Book" instead of the hat |
| buy_orat | 5 | OK |
| buy_underwear | 5 | OK (script threatens fiery death) |
| terminator_pods | 45 | OK in spirit (stalk plant replaces pods) |
| get_belt | 35 | OK. Script has no stick/pole alternative or fast solution |
Script-only additions to keep: Arnoid's whistle motive, narrator banter. Not in script: snake, scorpazpoid, lightning, Mog's head, the second solution.

## Act 3: Monolith Burger (140 pts)
| Point event | Pts | Status |
|---|---|---|
| buy_fun_meal, decoder_ring | 10+10 | OK |
| chickens_10 | 50 | PARTIAL: script plays one run; needs the 10-landing rule |
| find_message | 50 | OK |
| decode_message | 20 | OK |
Message text in the script differs from the walkthrough (volcanic planet, not a force field). The force-field clue matters for Act 4, so it must be restored.

## Act 4: Ortega (80 pts)
Script is a two-step version: wear underwear, plant detonator, grab generator pole.
| Point event | Pts | Status |
|---|---|---|
| wear_underwear | 10 | OK |
| telescope | 10 | GAP |
| get_pole | 10 | CONFLICT: script takes it from the rubble. Walkthrough: from the anemometer |
| get_detonator | 10 | PARTIAL: script already has it. Needs the green crate |
| detonator_generator | 20 | OK |
| pole_cross | 20 | GAP: script has no chasm. Pole-vault the device |
Not in script: shaky bridge, hiding from the ScumSoft team, lava pit, long ladder.

## Act 5: Pestulon (270 pts)
| Point event | Pts | Status |
|---|---|---|
| enter_scumsoft | 25 | PARTIAL: invisibility belt entry is good |
| coveralls | 5 | OK |
| photocopy | 5 | GAP: no copy machine or picture |
| keycard | 5 | OK |
| find_two_guys | 20 | OK |
| vaporize_jello | 10 | GAP: script frees the Two Guys at a console |
| nukem_robots | 100 | CONFLICT: script has Elmo Pug mech-suit boxing. Walkthrough: robot duel |
| dogfight | 100 | GAP: script just lifts off. Needs shield battle with five ships |
The mech-suit duel is the only point source for the 100 here. Proposal: keep the mech-suit duel (it is a fun scene) and use it as the nukem_robots event.

## Cross-cutting gaps
- Death scenes: about 30 deaths known from the walkthrough, none in the scripts (separate data file to come).
- Cockpit computer (navigation, scan, light speed, radar, weapons, shields): not in scripts.
- Per-room layouts: not in scripts; visual orientation boxes give a rough composition only.
- Humour: scripts' narrator is a mild joke-teller; the target is much funnier. Rewriting pass planned.

## Proposed merge rule
1. Keep every script scene and line of tone.
2. For each GAP/CONFLICT, add the walkthrough puzzle, so every one of the 40 point events is reachable (this guarantees 738).
3. Resolve conflicts in favour of the script where points are unaffected, and in favour of the walkthrough where they are lost.
