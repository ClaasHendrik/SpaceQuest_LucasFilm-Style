"""Render all room backgrounds to assets/backgrounds and a contact sheet. Usage: python3 build.py [sheet_path]"""
import sys, importlib
from PIL import Image, ImageDraw
from ega import Cv, W, H

MODULES = ["act1", "act2", "act3", "act4", "act5"]
OUT = "../../assets/backgrounds/"


def main():
    allrooms = {}
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        allrooms.update(mod.ROOMS)
    for name, fn in allrooms.items():
        fn().save(OUT + name + ".png")
    print(len(allrooms), "backgrounds written")
    if len(sys.argv) > 1:
        names = list(allrooms)
        cols = 3
        rows = (len(names) + cols - 1) // cols
        s = Image.new("RGB", (cols * (W * 2 + 8), rows * (H * 2 + 22)), (40, 40, 40))
        d = ImageDraw.Draw(s)
        for i, n in enumerate(names):
            im = Image.open(OUT + n + ".png").resize((W * 2, H * 2), Image.NEAREST)
            x, y = (i % cols) * (W * 2 + 8), (i // cols) * (H * 2 + 22)
            s.paste(im, (x, y + 16))
            d.text((x + 2, y + 2), n, fill=(255, 255, 0))
        s.save(sys.argv[1])


main()
