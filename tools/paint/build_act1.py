"""Builds every Act 1 background from the reference screens (see restyle.py). The reference screens are the user's own
screenshots and are NOT part of the repository: put them in tools/paint/ref/ as sNNN.png (the numbers on the Sierra Chest
screenshot pages 1-4). Usage: python3 build_act1.py [contact_sheet.png]"""
import sys, os
from PIL import Image
from restyle import restyle

REF = "ref/"
FULL = (0, 10, 320, 200)
FLOOR = (0, 60, 320, 200, {7, 8})     # the paneled floor: grey tiles are worn artificial wherever they are in the picture
# which parts are ARTIFICIAL (structured, pristine: flat, crisp) rather than ORGANIC (worn, banged up, rounded).
# 'flat' boxes: (x0, y0, x1, y1, mode, amp) in screen coordinates; mode 'flat', 'cyl_v' (drum), 'cyl_h' (tube).
# 'organic' boxes win over 'flat' boxes. Brown (rust, rubble) and green (slime) regions are always organic.
ZONES = {
    "garbage_mountain": {"flat": [(0, 10, 320, 92, "flat", 0.05)],
                         "worn": [(92, 72, 198, 152), (0, 92, 92, 162), (192, 62, 240, 105), (182, 104, 224, 142), (196, 150, 252, 190), (262, 80, 320, 145), FLOOR]},
    "junk_field": {"flat": [(0, 10, 320, 44, "flat", 0.05)],
                   "worn": [(36, 95, 110, 150), (0, 35, 60, 160), (150, 10, 320, 100), (150, 10, 215, 100), (48, 135, 108, 175), (175, 95, 290, 160), FLOOR]},
    "junk_tower": {"flat": [(232, 10, 320, 138, "flat", 0.05)],
                   "worn": [(0, 35, 120, 150), (15, 95, 170, 180), (110, 20, 235, 45), (240, 115, 310, 160), FLOOR]},
    "wire_tube": {"flat": [(18, 78, 312, 160, "cyl_h", 0.40)]},
    "robot_head": {"flat": [(205, 100, 262, 200, "flat", 0.05)], "worn": [(175, 58, 320, 200), (0, 40, 100, 130), FLOOR]},
    "conveyor": {"flat": [FULL + ("flat", 0.05)], "worn": [(0, 148, 185, 200), (165, 155, 250, 200)]},
    "rail_west": {"flat": [FULL + ("flat", 0.05)]},
    "crane_cabin": {"flat": [FULL + ("flat", 0.05)]},
    "rail_walk": {"flat": [(72, 10, 232, 160, "cyl_v", 0.30), FULL + ("flat", 0.05)]},
    "rat_lair": {"worn": [(150, 100, 200, 135), (250, 55, 275, 108)]},
    "mallard_bay": {"flat": [(190, 10, 320, 50, "flat", 0.05)], "worn": [(90, 80, 285, 155), (160, 22, 205, 58), (165, 140, 235, 182), (28, 72, 85, 125)]},
    "mallard_bay_l": {"flat": [(190, 10, 320, 50, "flat", 0.05)], "worn": [(90, 80, 285, 155), (160, 22, 205, 58), (165, 140, 235, 182), (28, 72, 85, 125)]},
    "cockpit": {"flat": [FULL + ("flat", 0.05)], "organic": [(105, 118, 190, 200), (0, 95, 78, 195)]},
}
OUT = "../../assets/backgrounds_act1_restyle/"   # staging folder: moved into assets/backgrounds when the rooms are rewired
# name: (screen number, boxes to erase: Roger and other figures, in 320x200 screen coordinates)
SPEC = {
    "garbage_mountain": (14, [(137, 84, 156, 112)]),            # crash site (Roger is painted out of the pod window)
    "junk_field": (15, [(110, 98, 124, 128)]),
    "junk_tower": (16, [(236, 40, 256, 72)]),
    "wire_tube": (26, [(152, 122, 174, 152), (180, 120, 214, 152)]),
    "robot_head": (27, [(78, 120, 96, 150)]),
    "conveyor": (18, [(4, 136, 30, 158)]),
    "rail_west": (19, [(154, 100, 172, 134)]),
    "crane_cabin": (20, [(134, 126, 164, 162)]),
    "rail_walk": (21, [(234, 136, 264, 168)]),
    "rat_lair": (24, [(248, 106, 268, 134)]),
    "mallard_bay": (22, []),
    "mallard_bay_l": (28, [(190, 74, 212, 100)]),   # painted out using the same yard from screen 22
    "cockpit": (29, []),
}


CLASSES = {}


def main():
    done = []
    for name, (n, boxes) in SPEC.items():
        p = REF + "s%03d.png" % n
        if not os.path.exists(p):
            print("missing reference", p)
            continue
        donor = REF + "s022.png" if name == "mallard_bay_l" else None
        img, cmap = restyle(p, erase=boxes, donor=donor, zones=ZONES.get(name), return_class=True)
        img.save(OUT + name + ".png")
        CLASSES[name] = cmap
        done.append(name)
    print(len(done), "backgrounds:", " ".join(done))
    if len(sys.argv) > 1:
        cols = 2
        rows = (len(done) + 1) // 2
        sh = Image.new("RGB", (cols * 650, rows * 330), (24, 24, 24))
        for i, nm in enumerate(done):
            sh.paste(Image.open(OUT + nm + ".png").resize((640, 320), Image.NEAREST), ((i % cols) * 650, (i // cols) * 330 + 8))
        sh.save(sys.argv[1])


if __name__ == "__main__":
    main()
