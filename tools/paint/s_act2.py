"""Act 2 (Phleebhut) with solid objects."""
import numpy as np
from kit import *
from solid import *
from p_act2 import sky, ground, far_ridges

GREEN = "#2fa84a"


def landing_strip():
    p = Paint(base="#7ce0ec", seed=41)
    sky(p, 78)
    far_ridges(p, 54)
    ground(p, 76)
    arch3d(p, 150, 41, 100, 59, GREEN, 1)
    arch3d(p, 252, 56, 66, 46, GREEN, 2)
    spire3d(p, 100, 59, 44, 14, GREEN, 3)
    spire3d(p, 122, 70, 32, 12, GREEN, 4)
    mallard(p, 14, 95, 0.5, lit=True, ramp=True)
    return p


def claw(p, x, flip=False, seed=1):
    sg = -1 if flip else 1
    ground_shadow(p, x - 6 * sg - (0 if not flip else 66), x + 70 * sg if not flip else x + 6, 134, 8, 0.45, 3.0)
    body = p.m_poly([(x, 0), (x + 60 * sg, 0), (x + 66 * sg, 80), (x + 46 * sg, 112), (x, 112)])
    t = np.clip(np.abs(p.xx - x) / 66.0, 0, 1)
    prof = (1.45 - 1.1 * t) if sg == 1 else (1.45 - 1.1 * t)
    p.fill(body, np.clip(rgb("#2ec8c0") * prof[..., None], 0, 255))
    p.edge(body, (0, 40, 50), 0.6)
    for yy in (34, 60, 86):                                      # scale ridges with a bright lip
        p.fill(p.m_line(x, yy, x + 62 * sg, yy + 5, 2), (8, 80, 92), 0.75)
        p.fill(p.m_line(x, yy - 1, x + 62 * sg, yy + 4, 1), (200, 255, 250), 0.4)
    for i in range(3):                                           # three yellow-green talons as lit cones
        tx = x + (36 + i * 9) * sg
        wd = 9 * sg
        a = [(tx, 106), (tx + wd * 0.5, 106), (tx + wd * 0.25, 138)]
        b = [(tx + wd * 0.5, 106), (tx + wd, 106), (tx + wd * 0.25, 138)]
        plane(p, a, "#e8f040", 1.35, angle=(-1, 0), spread=0.2, seed=seed + i, edge=0.5)
        plane(p, b, "#e8f040", 0.55, angle=(-1, 0), spread=0.2, seed=seed + i + 5, edge=0.5)


def world_o_wonders():
    p = Paint(base="#7ce0ec", seed=42)
    sky(p, 50)
    vgrad(p, 40, 106, [(0, "#1c2a68"), (1, "#0a1038")])
    ground(p, 106, seed=5)
    claw(p, 0, False, 1)
    claw(p, 319, True, 5)
    # neon sign with a frame that has depth
    box(p, 82, 8, 160, 46, 4, 3, "#2a3a78", seed=6)
    p.fill(p.m_rect(86, 12, 238, 50), (6, 10, 34))
    text(p, 92, 12, "WORLD O'", (110, 255, 140), 30)
    text(p, 118, 30, "WONDERS", (110, 255, 140), 30)
    p.glow(162, 32, 90, (80, 255, 120), 0.4, 0.5)
    # shop: a block with a canopy slab, recessed doorway and windows with sills
    ground_shadow(p, 60, 270, 108, 8, 0.55, 3.5)
    box(p, 70, 68, 180, 40, 10, 6, "#5a6272", seed=7, tex=0.1)
    box(p, 52, 62, 218, 8, 12, 8, "#d83a46", seed=8, tex=0.08)                    # canopy slab
    for x in range(56, 268, 14):
        p.fill(p.m_rect(x, 63, x + 6, 69), (255, 220, 220), 0.25)
    p.fill(p.m_rect(130, 84, 192, 108), (4, 4, 10))
    p.fill(p.m_rect(130, 84, 192, 86), (0, 0, 0), 0.7)
    p.glow(161, 100, 40, (255, 190, 120), 0.4)
    for x0 in (76, 200):
        p.fill(p.m_rect(x0, 90, x0 + 46, 106), p.lin(0, 90, 0, 106, "#b8f4ff", "#2a8aa0"))
        p.fill(p.m_poly([(x0, 90), (x0 + 16, 90), (x0 + 4, 106), (x0, 106)]), (255, 255, 255), 0.18)
        box(p, x0 - 2, 104, 50, 3, 2, 1, "#9aa4b4", seed=9)
    # a little table with legs and a top that has thickness
    soft_shadow(p, [(208, 130), (246, 130), (252, 138), (212, 138)], 0.5, 1.5)
    for x in (214, 230):
        cylinder_v(p, x, x + 3, 120, 134, "#8a5a30")
    box(p, 210, 112, 28, 6, 4, 2, "#c8783a", seed=10)
    return p


def canyon():
    p = Paint(base="#7ce0ec", seed=43)
    sky(p, 50)
    far_ridges(p, 20)
    facet_rock(p, [(0, 0), (92, 0), (72, 44), (86, 98), (52, H), (0, H)], "#c04aa8", 9, 1.4, 0.25, 6)
    facet_rock(p, [(228, 0), (W, 0), (W, H), (270, H), (252, 88), (242, 44)], "#d86ac0", 10, 1.4, 0.25, 6)
    fl = p.m_poly([(86, 76), (244, 76), (276, H), (46, H)])
    p.fill(fl, p.lin(0, 76, 0, H, "#f0c070", "#9a6030"))
    p.multiply(0.8 + 0.4 * p.noise(7, 3, 4), 0.5)
    arch3d(p, 96, 33, 90, 50, GREEN, 3)
    spire3d(p, 200, 44, 39, 14, GREEN, 4)
    for x, y, w in [(130, 100, 12), (172, 104, 14), (214, 98, 10), (150, 120, 16)]:   # stones lying about
        soft_shadow(p, [(x - 1, y + 5), (x + w, y + 5), (x + w + 3, y + 8), (x + 1, y + 8)], 0.5, 1.2)
        facet_rock(p, [(x, y + 5), (x + 2, y), (x + w - 2, y), (x + w, y + 5)], "#a06a4a", 40 + x, facets=1, edge=0.5)
    return p


def stalk_ridge():
    p = Paint(base="#7ce0ec", seed=44)
    sky(p, 56)
    far_ridges(p, 40)
    ground(p, 70, seed=6)
    facet_rock(p, [(0, 0), (W, 0), (W, 42), (250, 36), (180, 48), (100, 32), (0, 40)], "#a05a2a", 11, 1.35, 0.3, 5)
    soft_shadow(p, [(120, 40), (200, 40), (214, 110), (110, 110)], 0.35, 6.0)
    cylinder_v(p, 148, 164, 40, 72, "#3ac05a")
    for i in range(7):                                           # tendrils as lit tubes
        x = 134 + i * 9
        p.fill(p.m_line(x, 68, x + (i - 3) * 4, 98, 3), (200, 60, 170))
        p.fill(p.m_line(x - 1, 68, x + (i - 3) * 4 - 1, 98, 1), (255, 200, 250), 0.7)
    for i in range(3):                                           # pulsating pods as glowing spheres
        sphere(p, 126 + i * 40, 81, 9, "#ff7ae8", squash=1.25, spec=0.8, tint=(255, 100, 230))
        p.glow(126 + i * 40, 82, 24, (255, 100, 230), 0.35)
    facet_rock(p, [(0, H), (60, 118), (140, 110), (W, 126), (W, H)], "#8a5a46", 12, 1.3, 0.35, 3)
    return p


ROOMS = {"landing_strip": landing_strip, "world_o_wonders": world_o_wonders, "canyon": canyon, "stalk_ridge": stalk_ridge}
