"""Paints every room in the painterly style into assets/backgrounds. Usage: python3 build_all.py [contact_sheet.png]"""
import sys, importlib
from PIL import Image, ImageDraw
from paint import W, H
import pilot

OUT = "../../assets/backgrounds/"
SKIP = {'garbage_mountain','garbage_mountain_nowire','robot_head','conveyor','rat_lair','rat_lair_noreactor','rat_lair_noladder','rat_lair_empty','rail_walk','rail_walk_gone','rail_walk_installed','crane_cabin','mallard_bay','mallard_bay_l','mallard_bay_r','mallard_bay_lr','cockpit'}   # Act 1 now comes from build_act1.py (original screens)
MODULES = ["p_act1", "p_act2", "p_act3", "p_act4", "p_act5", "s_act1", "s_act2", "s_act3", "s_act4", "s_act5"]   # s_* = solid versions, override p_*


def main():
    written = []
    for name, fn in pilot.ROOMS.items():
        if name in SKIP:
            continue
        fn().save(OUT + name + ".png")
        written.append(name)
    rooms = {}
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        rooms.update(mod.ROOMS)
    for name, fn in rooms.items():
        if name in SKIP:
            continue
        fn().finish(colors=190, vignette=0.45).save(OUT + name + ".png")
        written.append(name)
    print(len(written), "backgrounds:", " ".join(written))
    if len(sys.argv) > 1:
        only = sys.argv[2:] or written
        cols = 2
        rows = (len(only) + cols - 1) // cols
        tw, th = W * 3, H * 3
        sh = Image.new("RGB", (cols * tw, rows * (th + 14)), (30, 30, 30))
        d = ImageDraw.Draw(sh)
        for i, n in enumerate(only):
            im = Image.open(OUT + n + ".png").resize((tw, th), Image.NEAREST)
            x, y = (i % cols) * tw, (i // cols) * (th + 14)
            sh.paste(im, (x, y + 14))
            d.text((x + 3, y + 1), n, fill=(255, 255, 0))
        sh.save(sys.argv[1])


main()
