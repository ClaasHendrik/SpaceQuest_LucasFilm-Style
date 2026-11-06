"""Generates data/rooms.json. Coordinates are in art pixels (320x132); the game scales them 2x.
Room fields: id, title, act, bg, walk [[x,y]..], entries {name:[x,y]}, no_player, hotspots[].
Hotspot: id, name, rect [x,y,w,h], approach [x,y], look, exit {room, entry} (optional)."""
import json

FLOOR = [[10, 104], [310, 104], [318, 129], [2, 129]]
ROOMS = []


def room(id, title, act, walk=None, entries=None, no_player=False, bg=None, hot=()):
    ROOMS.append({"id": id, "title": title, "act": act, "bg": bg or id, "walk": walk or FLOOR,
                  "entries": entries or {"start": [150, 114]}, "no_player": no_player, "hotspots": list(hot)})


def hs(id, name, rect, look, approach=None, exit=None, default_verb=None):
    h = {"id": id, "name": name, "rect": rect, "look": look}
    if approach:
        h["approach"] = approach
    if exit:
        h["exit"] = {"room": exit[0], "entry": exit[1] if len(exit) > 1 else "start"}
    if default_verb:
        h["default_verb"] = default_verb
    return h


# ---------------------------------------------------------------- Act 1: the garbage freighter
room("robot_head", "The Robot Head", 1, [[104, 106], [310, 106], [318, 129], [100, 129]],
     {"start": [120, 114], "west": [120, 114]}, hot=[
    hs("head", "giant robot head", [150, 14, 150, 86], "A robot head the size of a house, retired without ceremony. Somebody stuck it here and told nobody why.", [220, 110]),
    hs("eye", "broken eye", [176, 34, 28, 28], "One eye is smashed. Through the crack, something metallic glints inside, like a plan.", [190, 110]),
    hs("chasm", "chasm", [0, 100, 100, 29], "A chasm. You can't see the bottom, which is the one detail the rumours agree on.", [110, 112]),
    hs("plate", "metal plate", [110, 106, 22, 12], "A sharp-edged plate of metal, lying about like an invitation to a mistake.", [118, 116]),
    hs("w", "way west", [0, 40, 12, 60], "Back towards the mountain of garbage.", [112, 112], exit=("garbage_mountain", "east")),
])
room("conveyor", "The Conveyor", 1, [[10, 110], [300, 110], [318, 129], [2, 129]],
     {"start": [40, 118], "west": [40, 118]}, hot=[
    hs("belt", "conveyor belt", [0, 84, 250, 20], "A conveyor belt that carries things to a hydraulic crusher. It's the only thing on this ship that's running on time.", [130, 114]),
    hs("crusher", "crusher", [252, 54, 44, 38], "A steel block the size of a bus. It rises, falls, and doesn't take the day off.", [240, 114]),
    hs("pipe", "drainage pipe", [296, 98, 22, 26], "A drainage pipe just beneath the crusher. A very bad idea, helpfully lit.", [290, 118], exit=("rat_lair", "pipe")),
    hs("ladder", "service ladder", [0, 10, 18, 70], "A service ladder up to the overhead rails. Somebody's coffee cup is still on the first rung.", [22, 112], exit=("rail_walk", "start")),
    hs("w", "way west", [0, 114, 40, 15], "Back to the mountain.", [40, 118], exit=("garbage_mountain", "south")),
])
room("rat_lair", "The Reactor Cavern", 1, [[30, 76], [290, 76], [290, 100], [30, 100]],
     {"start": [60, 90], "pipe": [60, 90]}, hot=[
    hs("reactor", "warp-core reactor", [104, 96, 112, 36], "A reactor glowing with the particular green that says 'do not touch' in every language.", [100, 98]),
    hs("ladder", "iron ladder", [22, 20, 16, 80], "A rusty iron ladder up to a crane platform. Each rung is a small act of faith.", [30, 96], exit=("crane_cabin", "start")),
    hs("pipe", "rat's pipe", [268, 10, 50, 24], "From the dark inside come two red eyes, and the sound of something that eats nobody's leftovers.", [270, 96]),
    hs("platform", "suspension platform", [40, 66, 80, 10], "A platform bolted to the ceiling by someone who was in no hurry for a pay review.", [80, 92]),
])
room("rail_walk", "The Overhead Rail", 1, [[10, 112], [310, 112], [318, 129], [2, 129]],
     {"start": [30, 118]}, hot=[
    hs("rail", "cyan rail", [0, 70, 320, 4], "A long rail along the ceiling. Something dangles from it, taking its time.", [150, 118]),
    hs("tower", "magenta tower", [130, 0, 80, 100], "A support tower painted in a colour chosen by someone who clearly never had to look at it.", [170, 118]),
    hs("grabber", "grabber", [196, 60, 18, 32], "A grabber hangs from the rail, waiting for a hand to move it.", [200, 118]),
    hs("w", "way down", [0, 100, 30, 29], "Back down the service ladder.", [30, 118], exit=("conveyor", "start")),
])
room("crane_cabin", "The Crane Cabin", 1, [[40, 104], [250, 104], [300, 129], [10, 129]],
     {"start": [120, 114]}, hot=[
    hs("monitor", "monitor", [60, 56, 80, 44], "An old green monitor showing the room below. In real time, and very green.", [100, 108]),
    hs("stick", "joystick", [180, 62, 12, 38], "A joystick, worn smooth by many hands that are now elsewhere.", [186, 108]),
    hs("button", "red button", [220, 90, 16, 10], "A big red button. It's red for a reason; nobody wrote down what.", [226, 112]),
    hs("window", "window", [19, 13, 282, 40], "Through the glass you see the reactor, glowing in its pit like a bad idea.", [150, 108]),
    hs("hatch", "ladder hatch", [0, 100, 40, 29], "The way back down.", [50, 114], exit=("mallard_bay", "start")),
])
room("mallard_bay", "The Construction Bay", 1, None, {"start": [60, 114]}, hot=[
    hs("ship", "Aluminum Mallard", [80, 44, 182, 66], "A ship stitched together from scrap. It's the first thing in the universe that's all yours. Technically.", [170, 112]),
    hs("engine", "engine manifold", [96, 66, 12, 26], "An open engine mount. Plainly waiting for something glowing and expensive.", [100, 114]),
    hs("ramp", "boarding ramp", [140, 96, 60, 16], "A boarding ramp. Not exactly inviting, but it does lead inside.", [170, 114], exit=("cockpit", "start")),
])
room("cockpit", "The Cockpit", 1, [[70, 104], [250, 104], [300, 129], [20, 129]],
     {"start": [150, 116]}, hot=[
    hs("seat", "pilot's seat", [4, 56, 48, 64], "The pilot's seat. Somebody has been sitting in it for years, in spirit.", [60, 112]),
    hs("computer", "navigation computer", [262, 54, 54, 56], "A computer that thinks about it for a while, then says maybe.", [250, 114], exit=("nav_screen", "start")),
    hs("window", "viewscreen", [60, 40, 200, 60], "Space. A great deal of it. Mostly nobody's.", [160, 108]),
    hs("hatch", "exit hatch", [0, 110, 30, 19], "The way out.", [30, 120], exit=("mallard_bay", "start")),
    hs("launch", "launch lever", [150, 100, 20, 8], "Pulls the ship out into space. (Dev shortcut: takes you to Phleebhut.)", [160, 112], exit=("landing_strip", "start")),
])
room("nav_screen", "Navigation Computer", 1, no_player=True, hot=[
    hs("planet", "planet readout", [30, 50, 70, 50], "Planet Phleebhut. Light atmosphere. One known settlement. You've been to worse places and paid more to see them."),
    hs("map", "star map", [6, 30, 308, 98], "A grid of stars so wide that your pointer seems to apologise."),
    hs("resume", "1. Resume scan", [6, 4, 70, 18], "Scans the next sector."),
    hs("course", "2. Set course", [82, 4, 70, 18], "Sets a course. Not yet connected. (Work in progress.)"),
    hs("return", "3. Return", [158, 4, 70, 18], "Back to the cockpit.", exit=("cockpit", "start")),
])

# ---------------------------------------------------------------- Act 2: Phleebhut
room("landing_strip", "Phleebhut: Landing Strip", 2, [[8, 92], [312, 92], [318, 129], [2, 129]], {"start": [120, 116], "west": [120, 116]}, hot=[
    hs("ship", "Aluminum Mallard", [16, 86, 82, 32], "Your ship, parked at a slight angle, like a regret.", [60, 120], exit=("cockpit", "start")),
    hs("arches", "rock arch", [150, 38, 100, 54], "A rock arch the colour of an alien's idea of nature.", [200, 100]),
    hs("spires", "stone spires", [100, 54, 30, 40], "Sharp green spires. A quick glance says 'don't', a long one says 'really don't'.", [120, 100]),
    hs("e", "desert path", [296, 60, 24, 60], "A path east, towards a giant shape in the distance. Possibly a shop.", [300, 112], exit=("world_o_wonders", "west")),
    hs("s", "canyon path", [100, 118, 120, 11], "A path south into a canyon.", [160, 124], exit=("canyon", "start")),
])
room("world_o_wonders", "Phleebhut: World o' Wonders", 2, [[20, 104], [300, 104], [318, 129], [2, 129]], {"start": [150, 116], "west": [30, 116]}, hot=[
    hs("sign", "sign", [86, 10, 150, 38], "'WORLD O' WONDERS.' Both words are used with remarkable optimism.", [160, 108]),
    hs("door", "shop entrance", [130, 76, 60, 22], "The entrance. Inside, a salesman is waiting. He's been waiting since before the planet cooled.", [160, 108]),
    hs("claw", "giant claws", [0, 0, 60, 124], "A pair of giant claws holding up the shop. Whatever they belonged to is not coming back for them.", [70, 116]),
    hs("table", "little table", [210, 104, 26, 16], "A little table. A postcard rack, a stray alien sock.", [222, 122]),
    hs("w", "way west", [0, 100, 14, 29], "Back to the landing strip.", [24, 116], exit=("landing_strip", "west")),
])
room("canyon", "Phleebhut: Canyon Paths", 2, [[84, 76], [236, 76], [266, 129], [54, 129]], {"start": [150, 120]}, hot=[
    hs("arch", "rock arch", [96, 30, 90, 46], "A natural arch. Nothing about this planet is natural for anyone from elsewhere.", [150, 100]),
    hs("spire", "green spire", [200, 40, 20, 36], "A spire like a thorn from some enormous rose.", [210, 100]),
    hs("ne", "mountain trail", [250, 70, 60, 59], "A steep trail up the mountain.", [244, 112], exit=("stalk_ridge", "start")),
    hs("back", "way back", [90, 120, 100, 9], "Back to the landing strip.", [140, 124], exit=("landing_strip", "start")),
])
room("stalk_ridge", "Phleebhut: The Ridge", 2, [[0, 112], [320, 112], [320, 129], [0, 129]], {"start": [30, 118]}, hot=[
    hs("plant", "stalk plant", [140, 38, 30, 60], "A carnivorous stalk plant. Its tendrils drip with something that is not water.", [150, 118]),
    hs("pods", "pods", [120, 64, 100, 20], "Pulsating pods hang from the ledge. They throb, as if listening.", [170, 118]),
    hs("trail", "trail down", [0, 100, 20, 29], "Back down the trail.", [24, 118], exit=("canyon", "start")),
])

# ---------------------------------------------------------------- Act 3: Monolith Burger
room("monolith_exterior", "Monolith Burger: Station", 3, no_player=True, hot=[
    hs("station", "Monolith Burger station", [60, 20, 190, 90], "An orbital station shaped like a hamburger. Billions served. Billions regretted."),
    hs("arm", "docked ship", [0, 60, 60, 20], "Your ship is docked at the lower bun, like a bad habit.", exit=("cockpit", "start")),
    hs("air", "airlock", [52, 62, 14, 16], "The airlock. A sign inside says 'Please enjoy responsibly', which makes it clear nobody means it.", exit=("monolith_concourse", "start")),
])
room("monolith_concourse", "Monolith Burger: Concourse", 3, [[10, 100], [300, 100], [318, 129], [2, 129]], {"start": [270, 116], "arcade": [60, 114]}, hot=[
    hs("counter", "counter", [60, 54, 190, 38], "A counter streaked with something that was a meal in a previous life.", [150, 108]),
    hs("clerk", "clerk", [200, 22, 24, 34], "A teenage alien clerk who looks as though he's been bored since before you were born.", [210, 108]),
    hs("menu", "menu board", [70, 8, 180, 32], "The menu board offers eight kinds of burger. All taste of the same disappointment.", [160, 108]),
    hs("cabinet", "arcade cabinet", [6, 44, 34, 60], "A cabinet for a game called Astro Chicken. It blinks like it knows something.", [50, 110], exit=("arcade_corner", "start")),
    hs("tables", "tables", [262, 78, 50, 34], "Tables bolted to the floor. A sensible precaution, given the food.", [270, 118]),
    hs("air", "airlock", [304, 60, 16, 50], "Back to your ship.", [296, 116], exit=("monolith_exterior", "start")),
])
room("arcade_corner", "Monolith Burger: Arcade", 3, no_player=True, hot=[
    hs("screen", "screen", [114, 14, 92, 60], "A chicken falls slowly through a toxic sky. You know the feeling."),
    hs("play", "play game", [116, 84, 88, 18], "Drop in a coin and take the stick.", exit=("astro_chicken", "start"), default_verb="Use"),
    hs("back", "step back", [0, 112, 320, 20], "Step away from the machine.", exit=("monolith_concourse", "arcade")),
])
room("astro_chicken", "Astro Chicken", 3, no_player=True, hot=[
    hs("pad", "trampoline pad", [130, 90, 60, 10], "Land softly on the pad. Ten times, apparently."),
    hs("exit", "press F5 to exit", [120, 114, 100, 14], "Leave the game.", exit=("arcade_corner", "start")),
])

# ---------------------------------------------------------------- Act 4: Ortega
room("ortega_crater", "Ortega: Crater Field", 4, [[10, 80], [300, 80], [318, 129], [2, 129]], {"start": [60, 100]}, hot=[
    hs("ship", "Aluminum Mallard", [16, 50, 50, 16], "Your ship on the ridge, smoking quietly to itself.", [50, 90], exit=("cockpit", "start")),
    hs("lava", "lava pit", [150, 90, 70, 40], "A pit of glowing lava. It looks like the sunset, if the sunset wanted you dead.", [140, 100]),
    hs("s", "path south", [60, 120, 120, 9], "A narrow stone path south.", [100, 124], exit=("ortega_bridge", "start")),
])
room("ortega_bridge", "Ortega: The Shaky Bridge", 4, [[4, 64], [316, 64], [316, 84], [4, 84]], {"start": [24, 72], "east": [296, 72]}, hot=[
    hs("bridge", "shaky bridge", [92, 56, 136, 40], "A rope bridge over a chasm of lava. Strictly for people who've made peace with their choices.", [100, 72]),
    hs("w", "path back", [0, 60, 14, 24], "Back to the crater.", [20, 72], exit=("ortega_crater", "start")),
    hs("e", "path east", [304, 60, 16, 24], "On to the station.", [300, 72], exit=("ortega_station", "start")),
])
room("ortega_station", "Ortega: Boulder Field", 4, [[10, 100], [310, 100], [318, 129], [2, 129]], {"start": [30, 112], "east": [290, 112]}, hot=[
    hs("scope", "telescope", [56, 76, 34, 40], "A telescope pointed at the distant dome. It's been left alone, which has never happened to a telescope before.", [74, 116]),
    hs("crate", "green crate", [190, 92, 24, 20], "A green crate stamped 'DANGER, NOT A TOY'. A fine toy.", [202, 116]),
    hs("wind", "wind meter", [254, 58, 16, 56], "A wind meter. The wind here has opinions.", [262, 116]),
    hs("men", "researchers", [120, 72, 36, 28], "Two ScumSoft researchers in blue, arguing about whose turn it is to look important.", [140, 110]),
    hs("w", "way back", [0, 60, 14, 60], "Back to the bridge.", [20, 112], exit=("ortega_bridge", "east")),
    hs("e", "path ahead", [304, 56, 16, 60], "A path to the ridge.", [296, 112], exit=("ortega_dome", "start")),
])
room("ortega_dome", "Ortega: ScumSoft Dome", 4, [[10, 90], [310, 90], [318, 129], [2, 129]], {"start": [30, 112], "east": [290, 112]}, hot=[
    hs("dome", "research dome", [120, 50, 110, 70], "A silver dome of ScumSoft design, shiny, secure and entirely without taste.", [175, 112]),
    hs("dish", "satellite dish", [60, 30, 40, 44], "A dish that points at a sky nobody else wants. It hums, as if bored.", [80, 100]),
    hs("w", "way back", [0, 70, 16, 40], "Back to the boulder field.", [20, 112], exit=("ortega_station", "east")),
    hs("e", "ridge path", [304, 70, 16, 40], "A path to the ridge.", [296, 112], exit=("ortega_ridge", "start")),
])
room("ortega_ridge", "Ortega: The Ridge", 4, [[10, 90], [310, 90], [318, 129], [2, 129]], {"start": [30, 112]}, hot=[
    hs("pole", "metal pole", [166, 90, 28, 10], "A gleaming metal pole, quite unharmed, lying in the middle of the destruction like a promise.", [180, 106]),
    hs("crater", "crater", [90, 84, 140, 28], "A smoking crater where something used to be. You'd rather not think about what.", [160, 116]),
    hs("w", "way back", [0, 70, 16, 40], "Back to the dome.", [20, 112], exit=("ortega_dome", "east")),
])

# ---------------------------------------------------------------- Act 5: Pestulon (ScumSoft)
room("pestulon_exterior", "Pestulon: ScumSoft Headquarters", 5, [[10, 100], [300, 100], [318, 129], [2, 129]], {"start": [180, 116]}, hot=[
    hs("bunker", "ScumSoft building", [30, 44, 146, 52], "The ScumSoft headquarters. Each window is a monitor; each monitor is turned to look at you.", [140, 112]),
    hs("sign", "ScumSoft sign", [100, 36, 60, 10], "SCUMSOFT. They don't even pretend.", [130, 112]),
    hs("door", "door", [214, 74, 30, 22], "A door in the side of the building. A scanner winks next to it.", [230, 106], exit=("closet", "start")),
    hs("dish", "radar dish", [60, 0, 62, 30], "A dish that watches all the sky for the one thing that will upset them."),
    hs("pad", "landing pad", [270, 96, 48, 33], "Your ship waits on the pad, looking small and out of place.", [290, 116], exit=("cockpit", "start")),
])
room("closet", "ScumSoft: Maintenance Closet", 5, None, {"start": [260, 116]}, hot=[
    hs("shelf", "shelves", [20, 20, 100, 74], "Shelves of cleaning supplies. Every bottle says 'Not for Consumption' in a tone of long-suffering.", [70, 108]),
    hs("coveralls", "coveralls", [134, 22, 42, 50], "A janitor's coveralls, hanging like a surrender.", [155, 108]),
    hs("locker", "locker", [220, 40, 70, 54], "A locker with something inside that looks like a handheld vaporizer.", [255, 108]),
    hs("bucket", "bucket", [210, 98, 22, 12], "A bucket. The only thing here that isn't pretending to be more.", [220, 118]),
    hs("door", "door", [304, 40, 16, 60], "Back to the corridor.", [296, 112], exit=("cubicle_maze", "start")),
])
room("cubicle_maze", "ScumSoft: The Cubicle Maze", 5, [[8, 104], [312, 104], [318, 129], [2, 129]], {"start": [30, 116]}, hot=[
    hs("cubicles", "cubicles", [4, 4, 312, 98], "Cubicles in endless rows. Each has a drone, a lamp and a look like a closed door.", [150, 110]),
    hs("cans", "trash cans", [56, 104, 210, 18], "Full trash cans. Each looks like the end of somebody's career.", [150, 118]),
    hs("w", "way back", [0, 100, 14, 29], "Back to the closet.", [20, 116], exit=("closet", "start")),
    hs("office", "boss's office", [296, 36, 24, 66], "The office of the boss. The nameplate is longer than the person.", [290, 112], exit=("elmo_office", "start")),
])
room("elmo_office", "ScumSoft: Elmo Pug's Office", 5, None, {"start": [40, 116]}, hot=[
    hs("desk", "desk", [100, 70, 130, 30], "A desk so large it needs its own zip code.", [160, 108]),
    hs("picture", "portrait", [130, 14, 60, 40], "A portrait of the boss, looking exactly as important as he'd like to be.", [160, 108]),
    hs("copier", "copy machine", [250, 40, 40, 60], "A copy machine. It's making copies of something it ought not to be copying.", [262, 108]),
    hs("w", "door", [0, 40, 16, 60], "Back to the cubicles.", [24, 112], exit=("cubicle_maze", "start")),
    hs("e", "security door", [304, 40, 16, 60], "A heavy security door. It has a scanner, and presumably a grudge.", [296, 112], exit=("cell_block", "start")),
])
room("cell_block", "ScumSoft: The Cell Block", 5, [[20, 108], [300, 108], [318, 130], [2, 130]], {"start": [40, 116]}, hot=[
    hs("pods", "glass pods", [112, 40, 110, 52], "Two glass pods. Inside: the two weariest men in the galaxy, writing spreadsheets.", [166, 112]),
    hs("console", "console", [100, 100, 120, 18], "A control console blinking its small, uncaring lights.", [160, 120]),
    hs("w", "door", [0, 60, 16, 60], "Back to the office.", [24, 116], exit=("elmo_office", "east")),
    hs("e", "blast door", [304, 60, 16, 60], "A blast door to the hangar.", [296, 116], exit=("hangar", "start")),
])
room("hangar", "ScumSoft: The Hangar", 5, [[10, 110], [310, 110], [318, 130], [2, 130]], {"start": [40, 118]}, hot=[
    hs("arena", "arena", [60, 80, 200, 30], "A combat arena in the middle of the hangar. Nobody installed it to be friendly.", [160, 118]),
    hs("suits", "mech suits", [86, 44, 144, 52], "Two mech suits with boxing gloves. An engineer had a day.", [160, 118]),
    hs("w", "door", [0, 60, 16, 60], "Back to the cell block.", [24, 118], exit=("cell_block", "start")),
    hs("e", "ship hatch", [304, 60, 16, 60], "The way to the ship.", [296, 118], exit=("space_battle", "start")),
])
room("space_battle", "Space Battle", 5, no_player=True, hot=[
    hs("radar", "radar", [250, 6, 60, 22], "A radar. It shows enemies in front, behind and everywhere between."),
    hs("shield", "shield meter", [4, 4, 76, 18], "The shield meter. Higher is better, as with most things."),
    hs("view", "viewscreen", [60, 40, 160, 80], "Space. Full of things that want your ship for scrap.", exit=("deep_space", "start")),
])
room("deep_space", "The End", 5, no_player=True, hot=[
    hs("galaxy", "galaxy", [110, 40, 100, 60], "A whole galaxy, and for once you're not mopping any of it."),
])

# The art is 320x144; this layout was drawn for 132 rows, so stretch every y coordinate to match.
K = 144 / 132
for r in ROOMS:
    r["walk"] = [[x, round(y * K)] for x, y in r["walk"]]
    r["entries"] = {k: [x, round(y * K)] for k, (x, y) in r["entries"].items()}
    for h in r["hotspots"]:
        x, y, w, hh = h["rect"]
        h["rect"] = [x, round(y * K), w, round(hh * K)]
        if "approach" in h:
            h["approach"] = [h["approach"][0], round(h["approach"][1] * K)]
        # keep everything inside the 320x144 stage
        h["rect"][3] = min(h["rect"][3], 144 - h["rect"][1])
json.dump(ROOMS, open("data/rooms.json", "w"), indent=1)
print(len(ROOMS), "rooms,", sum(len(r["hotspots"]) for r in ROOMS), "hotspots")
