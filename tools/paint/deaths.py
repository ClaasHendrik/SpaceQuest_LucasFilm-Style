"""Painted death-scene pictures, 160x90, shown at 2x on the death screen. One per death title."""
import numpy as np
from paint import Paint, rgb
from kit import vgrad, text
from solid import *

OUT = "../../assets/deaths/"
W2, H2 = 160, 90


def canvas(seed, base="#05070f"):
    return Paint(w=W2, h=H2, base=base, seed=seed)


def roger(p, x, y, pose="stand", s=1.0):
    """a small Roger in his grey-and-magenta suit; (x, y) = feet. pose: stand, fall, flat, legs"""
    def L(x0, y0, x1, y1, w, c):
        p.fill(p.m_line(x + x0 * s, y + y0 * s, x + x1 * s, y + y1 * s, max(1, int(w * s))), c)
    skin, grey, mag, belt = (240, 170, 150), (176, 180, 190), (190, 40, 180), (196, 34, 40)
    if pose == "stand":
        L(-2, -12, -3, 0, 3, (150, 154, 166)); L(2, -12, 3, 0, 3, (150, 154, 166))
        p.fill(p.m_rect(x - 5 * s, y - 24 * s, x + 5 * s, y - 11 * s), grey)
        p.fill(p.m_rect(x - 5 * s, y - 14 * s, x + 5 * s, y - 12 * s), belt)
        L(-6, -23, -7, -13, 3, mag); L(6, -23, 7, -13, 3, mag)
        p.fill(p.m_ell(x - 4 * s, y - 33 * s, x + 4 * s, y - 24 * s), skin)
        p.fill(p.m_rect(x - 4 * s, y - 33 * s, x + 4 * s, y - 30 * s), (190, 100, 50))
    elif pose == "fall":
        L(-2, -2, -5, 9, 3, (150, 154, 166)); L(2, -2, 6, 8, 3, (150, 154, 166))
        p.fill(p.m_poly([(x - 5 * s, y - 14 * s), (x + 5 * s, y - 14 * s), (x + 4 * s, y - 1 * s), (x - 4 * s, y - 1 * s)]), grey)
        p.fill(p.m_rect(x - 4 * s, y - 4 * s, x + 4 * s, y - 2 * s), belt)
        L(-5, -13, -11, -22, 3, mag); L(5, -13, 11, -21, 3, mag)
        p.fill(p.m_ell(x - 4 * s, y - 23 * s, x + 4 * s, y - 14 * s), skin)
        p.fill(p.m_rect(x - 4 * s, y - 23 * s, x + 4 * s, y - 20 * s), (190, 100, 50))
        p.fill(p.m_rect(x - 1 * s, y - 18 * s, x + 2 * s, y - 16 * s), (120, 30, 30))      # a mouth, open in alarm
    elif pose == "flat":
        p.fill(p.m_ell(x - 18 * s, y - 3 * s, x + 18 * s, y + 3 * s), grey)
        p.fill(p.m_rect(x - 18 * s, y - 1 * s, x - 10 * s, y + 1 * s), mag)
        p.fill(p.m_ell(x + 14 * s, y - 3 * s, x + 21 * s, y + 3 * s), skin)
    elif pose == "legs":
        L(-2, 0, -2, -12, 4, (150, 154, 166)); L(2, 0, 3, -12, 4, (150, 154, 166))


def deceleration(seed=1):
    p = canvas(seed)
    vgrad(p, 0, H2, [(0, "#14183a"), (0.6, "#0a0c1e"), (1, "#020308")])
    for x in (-6, 130):
        facet_rock(p, [(x, 0), (x + 40, 0), (x + 30, H2), (x, H2)], "#3a4258", seed=seed + abs(x) + 1, facets=3)
    p.fill(p.m_rect(0, 0, W2, 6), (50, 56, 70))
    for i in range(7):                                               # speed lines above the figure
        x = 62 + i * 5
        p.fill(p.m_line(x, 6 + (i % 3) * 3, x - 1, 38 + (i % 4) * 5, 1), (140, 160, 220), 0.5)
    roger(p, 80, 50, "fall", 1.0)
    p.fill(p.m_poly([(150, 6), (158, 6), (154, 14)]), (230, 190, 40))
    text(p, 58, 78, "AAAAAAA", (255, 220, 120), 12)
    p.fill(p.m_rect(0, 84, W2, H2), (6, 6, 12))
    p.glow(80, 88, 70, (60, 80, 160), 0.25, 0.3)
    return p


def plate(seed=2):
    p = canvas(seed)
    vgrad(p, 0, 70, [(0, "#0a1228"), (1, "#27406a")])
    p.fill(p.m_rect(0, 70, W2, H2), p.lin(0, 70, 0, H2, "#3a4252", "#10141c"))
    roger(p, 60, 78, "stand", 1.7)
    soft_shadow(p, [(95, 76), (150, 76), (154, 84), (98, 84)], 0.5, 2.0)
    pl = p.m_poly([(92, 70), (128, 54), (140, 62), (104, 80)])
    p.shade(pl, "#d8e4f4", 1.4, 0.7, seed=seed)
    p.edge(pl, (0, 0, 0), 0.5)
    p.fill(p.m_line(92, 70, 128, 54, 1), (255, 255, 255), 0.9)
    p.glow(116, 64, 30, (230, 240, 255), 0.4)
    for i, (x, y) in enumerate([(78, 58), (84, 52), (90, 60), (96, 54)]):               # drops of regret
        p.fill(p.m_ell(x, y, x + 3, y + 4), (220, 40, 50))
    text(p, 84, 30, "OW.", (255, 230, 120), 14)
    return p


def crusher(seed=3):
    p = canvas(seed)
    vgrad(p, 0, 70, [(0, "#05070f"), (1, "#1c2c50")])
    p.fill(p.m_rect(0, 70, W2, H2), p.lin(0, 70, 0, H2, "#2a303e", "#0a0c12"))
    box(p, 20, 74, 120, 10, 6, 3, "#444c5c", seed=seed)                                    # the belt
    box(p, 52, 8, 56, 66, 6, 4, "#7c8898", seed=seed + 1, tex=0.14)                         # the crusher, all the way down
    for x in range(56, 106, 8):
        p.fill(p.m_rect(x, 12, x + 1, 70), (20, 24, 32), 0.6)
    cylinder_v(p, 76, 84, 0, 8, "#c4ccd8")
    p.fill(p.m_rect(44, 72, 120, 76), (10, 12, 18), 0.6)
    roger(p, 80, 78, "flat", 1.2)
    p.fill(p.m_rect(56, 70, 106, 74), (8, 10, 14))                                         # the squashed gap beneath the block
    for i in range(5):
        p.fill(p.m_poly([(64 + i * 8, 66), (68 + i * 8, 62 - (i % 2) * 6), (72 + i * 8, 66)]), (255, 240, 200), 0.8)    # stars
    text(p, 10, 26, "CLANG.", (255, 220, 120), 12)
    return p


def rat(seed=4):
    p = canvas(seed, "#020308")
    vgrad(p, 0, H2, [(0, "#06101a"), (1, "#021208")])
    m = p.m_ell(30, 8, 130, 84)
    p.fill(m, p.radial(80, 46, 56, "#2a1a10", "#030202", 0.8))
    p.edge(m, (0, 0, 0), 0.7)
    for ex in (58, 98):                                                                    # red eyes
        p.fill(p.m_rect(ex - 2, 28, ex + 3, 32), (255, 60, 50))
        p.glow(ex, 30, 14, (255, 60, 50), 0.7)
    p.fill(p.m_ell(66, 38, 94, 56), (200, 150, 140))                                       # nose
    p.fill(p.m_rect(76, 44, 84, 74), (240, 236, 220))                                      # teeth
    p.fill(p.m_rect(70, 52, 90, 78), (6, 2, 4))
    roger(p, 80, 82, "legs", 1.0)                                                          # Roger's legs, sticking out of the rat
    for x in (46, 114):
        for k in range(3):
            p.fill(p.m_line(x, 40 + k * 4, x + (22 if x < 80 else -22), 36 + k * 6, 1), (230, 220, 200), 0.8)
    text(p, 54, 2, "SQUEAK.", (255, 120, 100), 12)
    return p


def bad_flight(seed=5):
    p = canvas(seed)
    p.stars(p.m_rect(0, 0, W2, H2), 90, seed=2)
    box(p, 0, 0, 160, 30, 0, 0, "#6a7486", seed=seed)
    for x in range(0, 160, 20):
        p.fill(p.m_rect(x, 0, x + 1, 30), (0, 0, 0), 0.45)
    facet_rock(p, [(60, 90), (66, 58), (98, 52), (112, 70), (100, 90)], "#aeb8c8", seed=seed, facets=2)   # the crumpled ship
    p.fill(p.m_poly([(90, 56), (104, 60), (100, 70)]), (170, 230, 250))
    p.glow(86, 40, 40, (255, 160, 60), 0.7)
    for i in range(10):
        a = i * 0.63
        p.fill(p.m_poly([(86 + 20 * np.cos(a), 40 + 14 * np.sin(a)), (88 + 26 * np.cos(a), 42 + 18 * np.sin(a)), (84 + 24 * np.cos(a), 44 + 16 * np.sin(a))]), (255, 220, 100))
    text(p, 6, 70, "BONK.", (255, 220, 120), 12)
    return p


def decompression(seed=6):
    p = canvas(seed)
    p.stars(p.m_rect(0, 0, W2, H2), 130, seed=3)
    wall = p.m_poly([(0, 0), (70, 0), (60, 90), (0, 90)])
    p.shade(wall, "#6a7486", 1.2, 0.5, seed=seed)
    wall2 = p.m_poly([(110, 0), (160, 0), (160, 90), (118, 90)])
    p.shade(wall2, "#6a7486", 1.2, 0.5, seed=seed + 1)
    for (x, y, w_) in [(78, 12, 8), (88, 40, 6), (98, 64, 7), (84, 76, 5), (104, 24, 5)]:             # debris streaming out
        facet_rock(p, [(x, y + 4), (x + 1, y), (x + w_, y + 1), (x + w_ + 1, y + 4)], "#aeb8c8", seed=x, facets=0)
    roger(p, 92, 50, "fall", 0.8)
    p.fill(p.m_line(66, 30, 110, 24, 1), (255, 255, 255), 0.4)
    p.fill(p.m_line(64, 60, 112, 66, 1), (255, 255, 255), 0.4)
    p.glow(90, 46, 50, (255, 120, 60), 0.3)
    text(p, 6, 76, "WHOOSH.", (255, 220, 120), 12)
    return p


PICS = {
    "deceleration": deceleration, "plate": plate, "crusher": crusher, "rat": rat, "bad_flight": bad_flight, "decompression": decompression,
}

if __name__ == "__main__":
    import sys
    from PIL import Image
    for name, fn in PICS.items():
        fn().finish(colors=160, vignette=0.35).save(OUT + name + ".png")
    print(len(PICS), "death pictures")
    sh = Image.new("RGB", (3 * 330, 2 * 190), (24, 24, 24))
    for i, n in enumerate(PICS):
        sh.paste(Image.open(OUT + n + ".png").resize((320, 180), Image.NEAREST), ((i % 3) * 330 + 5, (i // 3) * 190 + 5))
    if len(sys.argv) > 1:
        sh.save(sys.argv[1])
