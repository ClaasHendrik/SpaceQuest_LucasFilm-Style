# Act 1 on the original layout: room map and puzzles

Sources: the original screens (Sierra Chest set, score shown in each frame), the AdventureDoor walkthrough, the points list.
Items marked (?) are my reading of the screens and should be corrected by playtesting.

## Rooms (art = restyled original screen)
| Id | Original screen | Role |
|---|---|---|
| escape_pod | none (kept from the script; the original starts in the crash site) | opening: locker with the manual, hatch out |
| crash_site | s014 | start; small object on the ground, wrecked pod, console |
| tube_entrance | s025 | arches leading into the tube; the portable ladder lies here (?) |
| wire_tube | s026 | tube with hanging wires (wire +5); the rat steals what you carry |
| robot_head | s027 | broken eye = climb up (robot_eye +5); chasm kills |
| yard | s022 | on top of the head: the shuttle with its open panel, the motivator (white drum), the claw |
| yard_ladder | s028 | the same with the ladder against the shuttle |
| cockpit | s029 | seat (buckazoids), computer, launch |
| junk_field | s015 | junk, passage east |
| junk_tower | s016 | the lift tower: the "vertical trash bucket" (trash_bucket +5) |
| conveyor | s018 | conveyor belt toward the shredder (timed), rail overhead (jump_rail +10) |
| rail_west / rail_window / rail_tower | s019 / s020 / s021 | the rail walkway; the grabber hangs at the tower (?) |
| dark_room | s023 | below the chute: the reactor in the hole, rats, ladder up |

## Map (east = right)
escape_pod -> crash_site -east-> tube_entrance -east-> wire_tube -east-> robot_head -eye-> yard -ladder-> robot_head
crash_site -south-> junk_field -east-> junk_tower -lift-> conveyor -jump-> rail_west -west-> rail_window -west-> rail_tower
rail_tower: grabber -> claw over the yard; rail_west: blue chute -> dark_room -ladder-> tube_entrance

## Puzzle order and points (total 145)
1. wire from the tube (+5, wire)
2. robot head eye: climb up, look at the shuttle (+5, robot_eye)
3. south, east: the lift (+5, trash_bucket); on the conveyor, jump to the rail before the shredder (+10, jump_rail)
4. rail to the tower, ride the grabber: claw over the yard: grab the warp motivator (white drum) (+15) and put it into the shuttle's open panel (+15)
5. dismount, step into the blue chute (+5, fall_chute) -> dark room (rats on a timer)
6. take the reactor from the hole (+15, get_reactor); the rat in the tube steals the reactor and the wire; fetch both again
7. the ladder at the tube entrance (+10, get_ladder)
8. yard: ladder against the shuttle (+5), open the hatch (+10), reactor (+5), wire (+5)
9. cockpit: search the seat (+10); computer: engines, radar, takeoff, weapons, front shields, fire (+25)

## Simplifications (flagged)
- The grabber ride is a claw you move left and right over the yard, not a ride through three screens with a U-turn.
- The yard picture does not change when the motivator is lifted out (the white drum stays in the art); only s028 (ladder) is a variant.
- The rail rooms are shown while walking; the exact connections between s019, s020 and s021 are my reading.
