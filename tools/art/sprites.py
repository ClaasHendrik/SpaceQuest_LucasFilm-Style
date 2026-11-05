"""Roger sprite sheet: 6 frames of 14x28 (underwear: stand, walk1, walk2; uniform: stand, walk1, walk2)."""
from PIL import Image
from ega import EGA, K, B, N, S, DG, WH, LR, R, Y, LB

FW, FH = 14, 28
HEAD = [
    "....NNNNN.....",
    "...NNNNNNN....",
    "...NNLLLNN....",
    "...NLLLLLN....",
    "...LLKLKLL....",
    "...LLLLLLL....",
    "....LLRRL.....",
    "....LLLLL.....",
]
def torso(shirt, trim):
    return [
        f"...{shirt*7}....",
        f"..{trim}{shirt*8}{trim}..".replace("..", "..", 1)[:14],
        f".{trim}{trim}{shirt*8}{trim}{trim}.."[:14],
        f".LL{shirt*7}LL...",
        f".LL{shirt*7}LL...",
        f"...{shirt*7}....",
        f"...{shirt*7}....",
        f"...{trim*7}....",
    ]
def legs(pants, boot, frame):
    if frame == 0:
        return [f"...{pants*3}.{pants*3}...", f"...{pants*3}.{pants*3}...", f"...{pants*3}.{pants*3}...",
                f"...{pants*3}.{pants*3}...", f"..{boot*4}.{boot*4}.."[:14]]
    if frame == 1:
        return [f"...{pants*3}.{pants*3}...", f"..{pants*3}...{pants*3}..", f".{pants*3}.....{pants*3}.",
                f".{pants*3}.....{pants*3}.", f".{boot*4}.....{boot*4}.."[:14]]
    return [f"...{pants*3}.{pants*3}...", f"...{pants*3}..{pants*3}..", f"...{pants*3}...{pants*3}.",
            f"...{pants*3}...{pants*3}.", f"..{boot*4}...{boot*4}."[:14]]
CM = {".": None, "N": N, "L": LR, "K": K, "R": R, "W": WH, "O": N, "Y": Y, "B": B, "S": S, "D": DG, "P": 9}

def frame(shirt, trim, pants, boot, f):
    rows = HEAD + torso(shirt, trim) + legs(pants, boot, f)
    rows = [r.ljust(FW, ".")[:FW] for r in rows]
    rows += ["." * FW] * (FH - len(rows))
    return rows

def build(path):
    sheet = Image.new("RGBA", (FW * 6, FH), (0, 0, 0, 0))
    outfits = [("L", "L", "L", "L"), ("O", "W", "W", "D")]   # underwear (bare skin + trunks), uniform
    for oi, (shirt, trim, pants, boot) in enumerate(outfits):
        for f in range(3):
            rows = frame(shirt, trim, pants, boot, f)
            if oi == 0:  # white high-waisted trunks over bare skin
                rows[15] = "...WWWWWWW...."
                rows[16] = rows[16].replace("L", "W")
            for y, r in enumerate(rows):
                for x, ch in enumerate(r):
                    c = CM.get(ch)
                    if False:
                        c = WH            # dithered pink skin
                    if c is not None:
                        sheet.putpixel(((oi * 3 + f) * FW + x, y), EGA[c] + (255,))
    sheet.save(path)

if __name__ == "__main__":
    build("../../assets/sprites/roger.png")
