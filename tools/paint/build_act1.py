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
    "crash_site": {"flat": [(0, 10, 320, 92, "flat", 0.05)],
                         "worn": [(92, 72, 198, 152), (0, 92, 92, 162), (192, 62, 240, 105), (182, 104, 224, 142), (196, 150, 252, 190), (262, 80, 320, 145), FLOOR]},
    "junk_field": {"flat": [(0, 10, 320, 44, "flat", 0.05)],
                   "worn": [(36, 95, 110, 150), (0, 35, 60, 160), (150, 10, 320, 100), (150, 10, 215, 100), (48, 135, 108, 175), (175, 95, 290, 160), FLOOR]},
    "junk_tower": {"flat": [(232, 10, 320, 138, "flat", 0.05)],
                   "worn": [(0, 35, 120, 150), (15, 95, 170, 180), (110, 20, 235, 45), (240, 115, 310, 160), FLOOR]},
    "wire_tube": {"flat": [(18, 78, 312, 160, "cyl_h", 0.40)]},
    "robot_head": {"flat": [(205, 100, 262, 200, "flat", 0.05)], "worn": [(175, 58, 320, 200), (0, 40, 100, 130), FLOOR]},
    "conveyor": {"flat": [FULL + ("flat", 0.05)], "worn": [(0, 148, 185, 200), (165, 155, 250, 200)]},
    "rail_west": {"flat": [FULL + ("flat", 0.05)]},
    "rail_window": {"flat": [FULL + ("flat", 0.05)]},
    "rail_tower": {"flat": [(72, 10, 232, 160, "cyl_v", 0.30), FULL + ("flat", 0.05)]},
    "dark_room": {"worn": [(130, 100, 190, 135)]},
    "tube_entrance": {},
    "yard": {"flat": [(190, 10, 320, 50, "flat", 0.05)], "worn": [(90, 80, 285, 155), (160, 22, 205, 58), (165, 140, 235, 182), (28, 72, 85, 125), FLOOR]},
    "yard_ladder": {"flat": [(190, 10, 320, 50, "flat", 0.05)], "worn": [(90, 80, 285, 155), (160, 22, 205, 58), (165, 140, 235, 182), (28, 72, 85, 125), FLOOR]},
    "cut_takeoff": {"flat": [FULL + ("flat", 0.05)]},
    "cut_blast": {"flat": [FULL + ("flat", 0.05)]},
    "cut_free": {},
    "cut_away": {},
    "cockpit": {"flat": [FULL + ("flat", 0.05)], "organic": [(105, 118, 190, 200), (0, 95, 78, 195)]},
}
OUT = "../../assets/backgrounds/"
# name: (screen number, boxes to erase: Roger and other figures, in 320x200 screen coordinates)
SPEC = {
    "crash_site": (14, [(137, 84, 156, 112)]),            # crash site (Roger is painted out of the pod window)
    "junk_field": (15, [(110, 98, 124, 128)]),
    "junk_tower": (16, [(236, 40, 256, 72)]),
    "wire_tube": (26, [(152, 122, 174, 152), (180, 120, 214, 152)]),
    "robot_head": (27, [(78, 120, 96, 150)]),
    "conveyor": (18, [(4, 136, 30, 158)]),
    "rail_west": (19, [(154, 100, 172, 134)]),
    "rail_window": (20, [(134, 126, 164, 162)]),
    "rail_tower": (21, [(234, 136, 264, 168)]),
    "dark_room": (23, [(80, 108, 98, 128)]),
    "tube_entrance": (25, [(48, 90, 70, 124)]),
    "yard": (22, []),
    "yard_ladder": (28, [(190, 74, 212, 100)]),   # painted out using the same yard from screen 22
    "cockpit": (29, []),
    "cut_takeoff": (31, []),
    "cut_blast": (34, []),
    "cut_free": (36, []),
    "cut_away": (37, []),
}


CLASSES = {}
# picture states: the same room after something was taken. name: (base room, boxes to erase, in 320x200 screen coordinates).
# The variant is rendered from the same source with the extra boxes erased and copied over the base only inside those boxes,
# so everything else stays identical to the base picture.
STATES = {
    "wire_tube_nowire": ("wire_tube", [(130, 76, 222, 106)]),
    "dark_room_noreactor": ("dark_room", [(124, 108, 196, 164, -72, 0)]),
    "yard_nomot": ("yard", [(14, 74, 92, 126, 0, 50)]),
    "yard_ladder_nomot": ("yard_ladder", [(14, 74, 92, 126, 0, 50)]),
}


def main():
    done = []
    for name, (n, boxes) in SPEC.items():
        p = REF + "s%03d.png" % n
        if not os.path.exists(p):
            print("missing reference", p)
            continue
        donor = REF + "s022.png" if name == "yard_ladder" else None
        pal = None
        if name == "yard_ladder":          # same palette as the other ship-yard picture
            pal = Image.open(OUT + "yard.png").convert("RGB").quantize(colors=112, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        img, cmap = restyle(p, erase=boxes, donor=donor, zones=ZONES.get(name), return_class=True, palette_from=pal)
        img.save(OUT + name + ".png")
        CLASSES[name] = cmap
        done.append(name)
    # the two ship-yard pictures show the same place: take everything from the first one and use the second one's own pixels only
    # where the two source screens really differ (the ladder, the cart, Roger), so the ship has identical dents and rust in both
    if "yard" in CLASSES and "yard_ladder" in CLASSES:
        import numpy as np
        from restyle import load_indices, box_blur
        ia, ib = load_indices(REF + "s022.png"), load_indices(REF + "s028.png")
        ys = np.minimum(((np.arange(160) + 0.5) * 190 / 160).astype(int), 189)
        real = (ia != ib)[ys]
        mask = box_blur(real.astype(np.float32), 4) > 0.02
        A, B = np.asarray(Image.open(OUT + "yard.png").convert("RGB")), np.asarray(Image.open(OUT + "yard_ladder.png").convert("RGB"))
        Image.fromarray(np.where(mask[..., None], B, A)).save(OUT + "yard_ladder.png")
        CLASSES["yard_ladder"] = np.where(mask, CLASSES["yard_ladder"], CLASSES["yard"])
    import numpy as np
    from restyle import box_blur
    for name, (base, extra) in STATES.items():
        n, boxes = SPEC[base]
        donor = REF + "s022.png" if base == "yard_ladder" else None
        var = restyle(REF + "s%03d.png" % n, erase=boxes + extra, donor=donor, zones=ZONES.get(base))
        basearr = np.asarray(Image.open(OUT + base + ".png").convert("RGB"))
        mask = np.zeros(basearr.shape[:2], bool)
        for (x0, y0, x1, y1) in [e[:4] for e in extra]:
            ya, yb = int((y0 - 10) * 160 / 190) - 2, int((y1 - 10) * 160 / 190) + 2
            mask[max(0, ya):yb, max(0, x0 - 2):x1 + 2] = True
        Image.fromarray(np.where(mask[..., None], np.asarray(var), basearr)).save(OUT + name + ".png")
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
