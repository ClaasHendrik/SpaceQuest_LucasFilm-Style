"""Builds every Act 1 background from the reference screens (see restyle.py). The reference screens are the user's own
screenshots and are NOT part of the repository: put them in tools/paint/ref/ as sNNN.png (the numbers on the Sierra Chest
screenshot pages 1-4). Usage: python3 build_act1.py [contact_sheet.png]"""
import sys, os
from PIL import Image
from restyle import restyle

REF = "ref/"
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
    "mallard_bay_l": (28, [(190, 74, 212, 100)]),
    "cockpit": (29, []),
}


def main():
    done = []
    for name, (n, boxes) in SPEC.items():
        p = REF + "s%03d.png" % n
        if not os.path.exists(p):
            print("missing reference", p)
            continue
        restyle(p, erase=boxes).save(OUT + name + ".png")
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
