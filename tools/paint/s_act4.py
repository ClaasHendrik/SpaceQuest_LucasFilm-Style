"""Act 4 (Ortega) with solid objects."""
import numpy as np
from kit import *
from solid import *
from p_act4 import sky, far_ridge, cliff, lava


def slab(p, pts, hi="#5a5258", seed=2):
    m = facet_rock(p, pts, hi, seed, 1.4, 0.3, 4, edge=0.5)
    p.edge(m, (255, 200, 160), 0.25, "top")
    return m


def crater():
    p = Paint(base="#8a0c0c", seed=61)
    sky(p)
    far_ridge(p)
    cliff(p, 0, W, 64, H)
    slab(p, [(0, 74), (120, 66), (W, 70), (W, 100), (200, 110), (0, 104)], seed=3)
    lava(p, [(150, 100), (204, 108), (226, 144), (150, 144)], seed=3)
    mallard(p, 12, 66, 0.4, lit=True, ramp=False)
    p.glow(40, 90, 60, (255, 120, 60), 0.15, 0.3)
    return p


def bridge():
    p = Paint(base="#8a0c0c", seed=62)
    sky(p, 44)
    far_ridge(p, 40, 4)
    p.fill(p.m_rect(0, 56, W, H), (8, 2, 4))
    cliff(p, 0, 94, 56, H)
    cliff(p, 230, W, 56, H)
    slab(p, [(0, 66), (96, 66), (96, 88), (0, 92)], seed=4)
    slab(p, [(226, 66), (W, 66), (W, 92), (226, 88)], seed=5)
    lava(p, [(94, 106), (228, 106), (232, H), (92, H)], seed=5)
    for x in (98, 222):                                          # anchor posts
        cylinder_v(p, x, x + 4, 52, 74, "#c8ccd8")
    # rope handrails with a lit top strand, planks as thin boxes with shadows underneath
    for x0, x1 in ((100, 160), (160, 224)):
        p.fill(p.m_line(x0, 54, (x0 + x1) // 2, 78, 1), (230, 220, 210))
        p.fill(p.m_line((x0 + x1) // 2, 78, x1, 54, 1), (230, 220, 210))
    for x in range(100, 222, 9):
        sag = 10 - abs(x - 160) // 6
        y = 74 + 10 - sag
        soft_shadow(p, [(x, y + 3), (x + 7, y + 3), (x + 9, y + 8), (x + 2, y + 8)], 0.5, 1.2)
        box(p, x, y, 7, 3, 2, 1, "#9a5a28", seed=40 + x)
    return p


def station(detonator=True):
    p = Paint(base="#8a0c0c", seed=63)
    sky(p, 44)
    far_ridge(p, 40, 5)
    p.fill(p.m_rect(0, 54, W, H), (6, 3, 4))
    for i in range(12):                                          # black boulders with a red rim light
        x, y = int(p.rng.integers(0, 300)), int(p.rng.integers(60, 100))
        w = int(p.rng.integers(22, 46))
        m = facet_rock(p, [(x, y + w // 2), (x + 3, y + 3), (x + w // 2, y - 4), (x + w - 3, y + 2), (x + w, y + w // 2 + 6),
                           (x + w // 2, y + w // 2 + 10)], "#4a4448", seed=20 + i, hi=1.5, lo=0.12, facets=3, edge=0.6)
        p.edge(m, (255, 90, 50), 0.5, "right")
    p.fill(p.m_rect(0, 112, W, H), p.lin(0, 112, 0, H, "#3a3236", "#0a0608"))
    p.multiply(0.7 + 0.6 * p.noise(6, 3, 6), 0.55)
    p.fill(p.m_rect(0, 112, W, 113), (255, 200, 160), 0.25)
    p.glow(60, 130, 80, (255, 100, 40), 0.18, 0.3)
    # telescope: tripod legs as tubes, a tube body and an eyepiece
    for x1, x2 in ((62, 76), (92, 78)):
        p.fill(p.m_line(x1, 94, x2, 124, 3), (170, 176, 190))
        p.fill(p.m_line(x1 - 1, 94, x2 - 1, 124, 1), (240, 244, 255), 0.6)
    ground_shadow(p, 56, 100, 124, 4, 0.5, 2.0)
    cylinder_h(p, 56, 94, 82, 91, "#aab4c2")
    cylinder_h(p, 92, 100, 84, 90, "#dde4f0")
    sphere(p, 56, 86, 5, "#8a94a6", spec=0.5)
    # the crate
    if detonator:
        ground_shadow(p, 186, 226, 122, 5, 0.55, 2.0)
        box(p, 190, 100, 24, 22, 7, 4, "#40e060", seed=31)
        p.fill(p.m_rect(197, 106, 205, 114), (4, 30, 10))
        p.glow(201, 112, 24, (80, 255, 110), 0.2)
    # wind meter: a pole with cup arms
    cylinder_v(p, 259, 263, 64, 122, "#d4dae8")
    for dx in (-12, 12):
        p.fill(p.m_line(261, 67, 261 + dx, 70, 1), (230, 236, 246))
        sphere(p, 261 + dx, 71, 4, "#f4f4ff", squash=0.8, spec=0.7)
    # two researchers in blue suits with helmets
    person(p, 133, 112, 42, "#2a52d8", "#1c3aa0", skin="#e8b896", seed=32, helmet="#e8f0ff")
    person(p, 156, 112, 42, "#2a52d8", "#1c3aa0", skin="#e8b896", seed=33, helmet="#e8f0ff")
    return p


def dome_room(shield=True):
    p = Paint(base="#8a0c0c", seed=64)
    sky(p, 44)
    far_ridge(p, 40, 6)
    p.fill(p.m_rect(0, 58, W, H), (6, 3, 4))
    cliff(p, 0, W, 108, H)
    slab(p, [(0, 76), (W, 74), (W, 112), (0, 112)], seed=6)
    ground_shadow(p, 106, 250, 118, 10, 0.55, 4.0)
    dome(p, 175, 116, 62, 60, "#eef2fa", spec=0.9)
    box(p, 114, 100, 124, 16, 6, 3, "#9aa2b4", seed=33)                       # the dome's base ring
    box(p, 164, 96, 22, 22, 3, 2, "#2a303c", seed=34)
    p.fill(p.m_rect(167, 100, 183, 116), (6, 8, 14))
    p.glow(175, 108, 22, (120, 200, 255), 0.3)
    # satellite dish: a tilted bowl on a mast
    cylinder_v(p, 78, 84, 70, 104, "#9aa2b4")
    sphere(p, 80, 50, 26, "#d8dee8", squash=0.8, spec=0.6, clip=(p.xx < 82) | (p.yy > 44))
    bowl = p.m_ell(58, 34, 100, 66)
    p.fill(bowl, p.radial(76, 46, 22, "#6a7488", "#c8d0dc", 0.8))
    p.edge(bowl, (0, 0, 0), 0.6)
    cylinder_v(p, 78, 82, 30, 46, "#aab4c4")
    if shield:
        for x in range(36, 263, 4):
            for y in range(20, 113, 4):
                p.a[y, x] = np.clip(p.a[y, x] * 0.75 + np.array([110, 150, 255], np.float32) * 0.35 * (1 if (x // 4 + y // 4) % 2 else 0.5), 0, 255)
        for x in range(36, 263, 22):
            p.fill(p.m_line(x, 20, x, 112, 1), (90, 130, 255), 0.35)
        for q in ((36, 20, 262, 21), (36, 111, 262, 112), (36, 20, 37, 112), (261, 20, 262, 112)):
            p.fill(p.m_rect(*q), (150, 210, 255), 0.85)
        p.glow(150, 66, 140, (80, 120, 255), 0.15, 0.7)
    return p


def ridge_room():
    p = Paint(base="#8a0c0c", seed=65)
    sky(p, 48)
    far_ridge(p, 44, 7)
    p.fill(p.m_rect(0, 62, W, H), (6, 3, 4))
    cliff(p, 0, W, 112, H)
    slab(p, [(0, 78), (W, 76), (W, 116), (0, 116)], seed=7)
    lava(p, [(92, 92), (230, 92), (222, 122), (100, 122)], seed=7)
    for i in range(8):
        p.glow(120 + i * 12, 70 - i * 6, 22, (70, 60, 66), 0.5)
    # the generator pole: a gleaming cylinder with a bright specular line, resting on the rubble
    soft_shadow(p, [(164, 104), (196, 104), (200, 108), (168, 108)], 0.55, 1.5)
    cylinder_h(p, 166, 196, 99, 104, "#e8ecf8")
    p.glow(181, 101, 24, (255, 255, 255), 0.5)
    for dx in (-6, 8, 18):
        facet_rock(p, [(170 + dx, 104), (172 + dx, 100), (178 + dx, 100), (180 + dx, 104)], "#5a5258", seed=90 + dx, facets=0)
    return p


ROOMS = {"ortega_crater": crater, "ortega_bridge": bridge, "ortega_station": station, "ortega_dome": dome_room, "ortega_ridge": ridge_room}
