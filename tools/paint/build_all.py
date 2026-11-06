"""Paints every room in the painterly style into assets/backgrounds. Usage: python3 build_all.py [contact_sheet.png]"""
import sys, importlib
from PIL import Image, ImageDraw
from paint import W, H
import pilot

OUT = "../../assets/backgrounds/"
MODULES = ["p_act1", "p_act2", "p_act3", "p_act4", "p_act5", "s_act1", "s_act2", "s_act3", "s_act4", "s_act5"]   # s_* = solid versions, override p_*


def main():
    written = []
    for name, fn in pilot.ROOMS.items():
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
