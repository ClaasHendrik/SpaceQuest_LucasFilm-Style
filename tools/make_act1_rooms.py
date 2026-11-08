"""Writes data/act1_rooms.json: Act 1 on the original layout. Coordinates are art pixels (320x160; the game shows them at 2x).
Hotspot: id, name, rect [x,y,w,h], approach [x,y], look, exit {room, entry}, default_verb. Verbs and puzzles: scripts/rooms/act1.gd"""
import json

R = []


def room(id, title, walk, entries, hot, no_player=False):
    R.append({"id": id, "title": title, "act": 1, "bg": id, "walk": walk, "entries": entries, "no_player": no_player, "hotspots": hot})


def hs(id, name, rect, look, approach=None, exit=None, dv=None):
    h = {"id": id, "name": name, "rect": rect, "look": look}
    if approach:
        h["approach"] = approach
    if exit:
        h["exit"] = {"room": exit[0], "entry": exit[1]}
    if dv:
        h["default_verb"] = dv
    return h


GROUND = [[14, 112], [304, 112], [316, 152], [4, 152]]

room("crash_site", "Crash site", [[40, 112], [292, 112], [316, 152], [6, 152]],
     {"start": [140, 128], "pod": [120, 126], "east": [292, 128], "north": [150, 134]}, [
    hs("pod", "your escape pod", [95, 55, 72, 52], "Your escape pod, lying in the junk like a very expensive mistake. It got you here, and that is the whole review.", [128, 122], exit=("escape_pod", "hatch")),
    hs("object", "small object", [170, 128, 26, 14], "A small object lies on the ground. It is not yours, it is not important, and you are already planning to remember where it is.", [183, 140]),
    hs("barrel", "red barrel", [0, 70, 92, 50], "A big red drum, lying on its side and rusting with the dignity of something that was once in charge of something.", [96, 126]),
    hs("console", "control stick", [193, 92, 66, 50], "A control stick on a broken pedestal. Whatever it controlled has stopped answering.", [226, 142]),
    hs("pipe", "bent pipe", [268, 66, 52, 50], "A pipe, bent into an arch by some event nobody mentions.", [290, 128]),
    hs("e", "way east", [300, 60, 20, 90], "A gap in the junk to the east, leading towards a large tube.", [296, 128], exit=("tube_entrance", "west")),
    hs("s", "way south", [60, 146, 200, 14], "A path south, through more junk.", [150, 148], exit=("junk_field", "north")),
])
room("tube_entrance", "Entrance to the tube", [[10, 114], [310, 114], [316, 152], [4, 152]],
     {"west": [40, 130], "east": [290, 130], "pit": [100, 128]}, [
    hs("arches", "arched doorways", [37, 59, 186, 62], "Three arched doorways into a long, round tube. The middle one is open, and it breathes slightly.", [128, 124], exit=("wire_tube", "west")),
    hs("ladder", "ladder", [236, 80, 36, 52], "A light ladder, leaning on a pile of nothing in particular, waiting for someone to have a reason.", [250, 134], dv="Pick up"),
    hs("w", "way west", [0, 70, 16, 80], "Back to the crash site.", [20, 130], exit=("crash_site", "east")),
    hs("e", "hole in the floor", [276, 120, 44, 32], "A square hole in the floor with a ladder inside. Cold air comes up. So do small, interested sounds.", [292, 132], exit=("dark_room", "ladder")),
])
room("wire_tube", "Inside the tube", [[24, 100], [296, 100], [300, 116], [20, 116]],
     {"west": [40, 108], "east": [276, 108]}, [
    hs("wires", "hanging wires", [135, 58, 82, 20], "Wires hang from the ceiling of the tube, some of them still carrying current and all of them still carrying opinions.", [172, 108], dv="Pick up"),
    hs("w", "tube entrance", [0, 60, 24, 60], "Back out of the tube.", [34, 108], exit=("tube_entrance", "east")),
    hs("e", "far end", [296, 60, 24, 60], "The far end of the tube.", [286, 108], exit=("robot_head", "west")),
])
room("robot_head", "The robot head", [[100, 96], [256, 96], [304, 152], [60, 152]],
     {"west": [110, 118], "top": [150, 120]}, [
    hs("eye", "broken eye", [0, 40, 106, 74], "The robot's eye: a huge red lens, cracked in the middle. Behind the crack there is room for a person with poor judgement.", [112, 120], dv="Use"),
    hs("head", "giant robot head", [178, 46, 142, 114], "A giant robot head with a green diamond on its forehead. It has been looking at the same piece of ceiling for years.", [220, 130]),
    hs("door", "green panel", [122, 72, 46, 62], "A green panel, bent out of its frame. It looks like a door that has given up its job.", [146, 126]),
    hs("chasm", "chasm", [40, 142, 170, 18], "A chasm lies at the edge of the platform. It does not look deep. It looks patient.", [130, 140]),
    hs("w", "way west", [0, 120, 20, 40], "Back along the tube.", [24, 126], exit=("wire_tube", "east")),
])
room("yard", "On top of the head", [[24, 108], [296, 108], [316, 152], [6, 152]],
     {"eye": [40, 130], "claw": [160, 130]}, [
    hs("motivator", "warp motivator", [20, 57, 66, 38], "A white drum with a dark hole in the end: a warp motivator, large, expensive, and lying in the rubble like a cooking pot. Far too heavy for hands.", [60, 126]),
    hs("ship", "shuttle", [95, 58, 190, 60], "A small shuttle lying in the junk, battered into a shape it was never designed for. It looks as if it still hopes.", [180, 128]),
    hs("panel", "open panel", [105, 84, 50, 28], "An open maintenance panel in the shuttle. Inside there is a motivator-sized hole, and nothing to fill it.", [130, 126]),
    hs("ladder", "ladder down", [0, 100, 18, 52], "The ladder down to the robot's platform.", [26, 132], exit=("robot_head", "top")),
    hs("platform", "far platform", [296, 100, 24, 52], "The end of the rail platform. There is a chute here, and a railing that does not inspire trust.", [296, 132]),
])
room("yard_ladder", "On top of the head", [[24, 108], [296, 108], [316, 152], [6, 152]],
     {"eye": [40, 130], "claw": [160, 130]}, [
    hs("motivator", "warp motivator", [20, 57, 66, 38], "A white drum with a dark hole in the end: a warp motivator, large, expensive, and lying in the rubble like a cooking pot.", [60, 126]),
    hs("ship", "shuttle", [95, 58, 190, 60], "A small shuttle lying in the junk, battered into a shape it was never designed for. A ladder now leans against its side.", [180, 128]),
    hs("ladder_on", "ladder", [208, 66, 28, 44], "The ladder, leaning on the shuttle. Its rungs are thin, but so are your options.", [222, 128], dv="Use"),
    hs("hatch", "top hatch", [200, 56, 44, 14], "A small hatch on top of the shuttle, with a latch and a long history of being ignored.", [222, 128]),
    hs("panel", "power panel", [110, 84, 46, 28], "The power panel: a reactor-shaped hole and a wire-shaped hole.", [130, 126]),
    hs("ladder", "ladder down", [0, 100, 18, 52], "The ladder down to the robot's platform.", [26, 132], exit=("robot_head", "top")),
    hs("platform", "far platform", [296, 100, 24, 52], "The end of the rail platform.", [296, 132]),
])
room("junk_field", "Junk field", [[30, 100], [300, 100], [316, 152], [8, 152]],
     {"north": [150, 112], "east": [290, 128]}, [
    hs("wheel", "wrecked fighter wheel", [20, 60, 85, 62], "A big round wheel from some old fighter, with six spokes. It looks like it could have been a gun's very expensive eye.", [60, 126]),
    hs("rocket", "rocket tube", [215, 5, 60, 75], "A white and red rocket tube, standing in the junk like an enormous pen that has run out of ink.", [248, 126]),
    hs("hull", "ship hull", [262, 10, 58, 70], "Part of a ship's hull. The letters say JUP. Whatever they spelled has been lost.", [286, 126]),
    hs("box", "pink box", [70, 112, 60, 30], "A pink box with a door that does not close. It contains the same thing everything here contains: past.", [100, 142]),
    hs("n", "way north", [100, 22, 120, 24], "Back to the crash site.", [150, 108], exit=("crash_site", "south")),
    hs("e", "way east", [300, 60, 20, 90], "The junk continues east, towards a tall tower.", [296, 128], exit=("junk_tower", "west")),
])
room("junk_tower", "The lift tower", [[30, 100], [290, 100], [316, 152], [8, 152]],
     {"west": [40, 128], "top": [200, 40]}, [
    hs("lift", "lift tower", [236, 5, 48, 112], "A tall tower with a lift platform hanging from a chain. A little bucket hangs at the top, collecting scrap and carrying it away to somewhere worse.", [258, 124], dv="Use"),
    hs("slab", "pink slab", [20, 70, 90, 60], "A pink slab leaning against a heap. It has the shape of a staircase for someone much, much bigger.", [64, 138]),
    hs("pod", "wrecked pod", [0, 20, 110, 60], "A big wrecked pod, half buried. It wears a number and some scorch marks.", [60, 128]),
    hs("w", "way west", [0, 100, 18, 52], "Back through the junk field.", [24, 128], exit=("junk_field", "east")),
])
room("conveyor", "The conveyor", [[10, 118], [210, 118], [226, 130], [4, 130]],
     {"start": [30, 126], "lift": [30, 126]}, [
    hs("belt", "conveyor belt", [0, 115, 180, 16], "A moving belt, carrying everything towards a shredder at its end. The belt does not care what.", [100, 126]),
    hs("shredder", "shredder", [168, 126, 70, 30], "A shredder: a red box with steel teeth in a tidy row. It is patient, like the sea.", [200, 128]),
    hs("rail", "cyan rail", [0, 66, 320, 14], "A glowing rail runs overhead. Within reach, if you can jump.", [150, 126], dv="Use"),
    hs("pipes", "overhead pipes", [0, 20, 320, 44], "Pipes and conduits, painted in the colours that someone chose in a hurry.", [150, 126]),
])
room("rail_west", "On the rail", [[2, 100], [318, 100], [318, 112], [2, 112]],
     {"jump": [250, 106], "east": [300, 106], "west": [30, 106]}, [
    hs("chute", "blue chute", [0, 56, 36, 50], "A blue chute leads down into the dark. A sign says ONE WAY, and nobody has painted the other way.", [20, 106], dv="Use"),
    hs("w", "west along the rail", [0, 96, 16, 20], "The rail continues west.", [10, 106], exit=("rail_window", "east")),
    hs("e", "east along the rail", [304, 96, 16, 20], "The rail continues east.", [310, 106]),
])
room("rail_window", "The rail by the window", [[2, 92], [318, 92], [318, 104], [2, 104]],
     {"east": [300, 98], "west": [30, 98]}, [
    hs("window", "control room", [125, 20, 150, 62], "Through the glass: a control room, teal and spotless. A droid sits at the console, reading the same line again and again.", [200, 98]),
    hs("w", "west along the rail", [0, 90, 16, 18], "The rail continues west.", [10, 98], exit=("rail_tower", "east")),
    hs("e", "east along the rail", [304, 90, 16, 18], "Back along the rail.", [310, 98], exit=("rail_west", "west")),
])
room("rail_tower", "The rail tower", [[2, 100], [318, 100], [318, 112], [2, 112]],
     {"east": [300, 106], "west": [30, 106], "dismount": [30, 106]}, [
    hs("tower", "magenta tower", [72, 10, 160, 126], "A tall magenta tower with a window of oval slots, standing in the middle of everything with great self-importance.", [150, 106]),
    hs("grabber", "grabber", [226, 100, 40, 44], "A rail grabber: a little cab, a rod and a claw. Whoever left it went home early and left the keys in.", [250, 106], dv="Use"),
    hs("e", "east along the rail", [304, 92, 16, 22], "Back along the rail.", [310, 106], exit=("rail_window", "west")),
])
room("dark_room", "The dark room", [[10, 100], [300, 100], [316, 152], [4, 152]],
     {"ladder": [236, 120], "chute": [150, 112]}, [
    hs("reactor", "reactor", [128, 86, 62, 40], "A warp-core reactor, sitting in a hole in the rock with a red wire coming down to it like a leash. It hums in a tone that suggests it has plans.", [150, 124], dv="Pick up"),
    hs("hole", "hole", [108, 92, 70, 40], "A hole in the floor, big enough for the reactor and several regrets.", [140, 130]),
    hs("wire", "red wire", [180, 20, 56, 66], "A red wire runs down from the ceiling into the hole. Somebody wanted this reactor to stay where it was.", [200, 112]),
    hs("rats", "red eyes", [262, 16, 58, 34], "In the corners of the room, pairs of small red eyes keep a polite distance, and keep it carefully.", [250, 112]),
    hs("ladder", "ladder", [215, 20, 30, 78], "A ladder up to the tube entrance.", [236, 124], exit=("tube_entrance", "pit")),
])
room("cockpit", "The cockpit", [[70, 110], [250, 110], [300, 152], [20, 152]],
     {"start": [150, 130]}, [
    hs("seat", "pilot's seat", [4, 90, 82, 68], "The pilot's seat. It has the shape of a person who gave up long ago. The cushion is lumpy in a way that suggests savings.", [70, 134]),
    hs("computer", "ship's computer", [205, 62, 115, 64], "A computer that thinks about it for a while, then says maybe.", [220, 134]),
    hs("window", "viewport", [75, 50, 110, 68], "Through the round window: the robot's platform, and everything else in the world, still lying where it fell.", [150, 118]),
    hs("launch", "launch lever", [150, 130, 24, 22], "The launch lever. It does nothing until the computer is ready, and the computer is never ready on the first try.", [160, 140]),
    hs("hatch", "exit hatch", [0, 134, 34, 26], "The hatch back out onto the shuttle's roof.", [34, 148], exit=("yard_ladder", "eye")),
])

json.dump(R, open("data/act1_rooms.json", "w"), indent=1)
print(len(R), "Act 1 rooms,", sum(len(r["hotspots"]) for r in R), "hotspots")
