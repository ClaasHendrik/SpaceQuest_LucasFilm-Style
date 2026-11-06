"""Act 2: Phleebhut. Magenta ground, green rock arches, black ridges, a pale cyan sky, as in the original."""
import numpy as np
from kit import *


def sky(p, h=76):
    vgrad(p, 0, h, [(0, "#2aa8c8"), (0.55, "#7ce0ec"), (1, "#e8fcfc")])
    p.multiply(0.96 + 0.08 * p.noise(30, 2, 5), 0.5)


def ground(p, y0, seed=2):
    p.fill(p.m_rect(0, y0, W, H), p.lin(0, y0, 0, H, "#d058b4", "#5a1a6c"))
    p.multiply(0.75 + 0.5 * p.noise(9, 3, seed), 0.55)
    p.fill(p.m_rect(0, y0, W, y0 + 1), (255, 220, 255), 0.4)
    for _ in range(60):
        x, y = int(p.rng.integers(0, W)), int(p.rng.integers(y0 + 4, H - 2))
        p.fill(p.m_rect(x, y, x + int(p.rng.integers(2, 9)), y + 1), (60, 10, 70), 0.45)


def rock_arch(p, x, y, w, h, seed=1):
    pts = [(x, y + h), (x + w * 0.1, y + h * 0.4), (x + w * 0.3, y + 4), (x + w * 0.5, y), (x + w * 0.74, y + h * 0.3),
           (x + w, y + h), (x + w * 0.78, y + h), (x + w * 0.6, y + h * 0.42), (x + w * 0.5, y + h * 0.36),
           (x + w * 0.38, y + h * 0.46), (x + w * 0.22, y + h)]
    m = p.m_poly(pts)
    p.shade(m, "#2fa84a", 1.5, 0.3, tex=0.14, seed=seed)
    p.edge(m, (0, 40, 10), 0.6)
    p.edge(m, (220, 255, 200), 0.3, "top")
    p.fill(p.m_poly([(x + w * 0.5, y + 2), (x + w * 0.74, y + h * 0.3), (x + w * 0.6, y + h * 0.4)]), (160, 255, 150), 0.35)


def spire(p, x, y, h, w=14, seed=1):
    m = p.m_poly([(x, y + h), (x + w * 0.3, y + h * 0.4), (x + w / 2, y), (x + w * 0.75, y + h * 0.4), (x + w, y + h)])
    p.shade(m, "#2fa84a", 1.5, 0.3, tex=0.12, seed=seed)
    p.edge(m, (0, 40, 10), 0.6)


def far_ridges(p, y):
    ridge(p, y, 12, "#3a2a58", "#6a3a8a", seed=3, step=(12, 30), bottom=y + 44, tex=0.1)
    ridge(p, y + 8, 8, "#1a1030", "#3a1a58", seed=4, step=(10, 22), bottom=y + 50, tex=0.1)


def landing_strip():
    p = Paint(base="#7ce0ec", seed=41)
    sky(p, 78)
    far_ridges(p, 54)
    ground(p, 76)
    rock_arch(p, 150, 41, 100, 59, 1)
    rock_arch(p, 252, 56, 66, 46, 2)
    spire(p, 100, 59, 44, 14, 3)
    spire(p, 124, 70, 32, 11, 4)
    # the Aluminum Mallard, landed
    hull = [(14, 124), (22, 102), (68, 96), (98, 104), (100, 124)]
    m = shaded(p, hull, "#aab4c2", 1.45, 0.35, seed=5, tex=0.1)
    p.edge(m, (255, 255, 255), 0.3, "top")
    p.fill(p.m_poly([(78, 100), (94, 104), (94, 112), (76, 108)]), p.lin(76, 100, 94, 112, "#bff8ff", "#1a5a78"))
    p.fill(p.m_poly([(46, 124), (66, 124), (72, 136), (40, 136)]), (80, 88, 104))
    for x in (22, 88):
        p.fill(p.m_rect(x, 124, x + 8, 130), (70, 76, 90))
    p.glow(60, 140, 60, (60, 10, 70), 0.0)
    p.fill(p.m_ell(14, 128, 104, 138), (40, 6, 50), 0.5)
    return p


def claw(p, x, flip=False, seed=1):
    sgn = -1 if flip else 1
    body = p.m_poly([(x, 0), (x + 60 * sgn, 0), (x + 66 * sgn, 80), (x + 46 * sgn, 112), (x, 112)])
    p.shade(body, "#2ec8c0", 1.4, 0.35, angle=(-1 * sgn, 0), tex=0.12, seed=seed)
    p.edge(body, (0, 40, 50), 0.6)
    for yy in (36, 62, 88):
        p.fill(p.m_line(x, yy, x + 62 * sgn, yy + 5, 2), (10, 90, 100), 0.7)
        p.fill(p.m_line(x, yy - 1, x + 62 * sgn, yy + 4, 1), (200, 255, 250), 0.35)
    for i in range(3):                                           # yellow-green talons
        tx = x + (40 + i * 8) * sgn
        tal = p.m_poly([(tx, 106), (tx + 9 * sgn, 106), (tx + 4 * sgn, 138)])
        p.shade(tal, "#e8f040", 1.5, 0.4, seed=seed + i)
        p.edge(tal, (60, 80, 0), 0.6)


def world_o_wonders():
    p = Paint(base="#7ce0ec", seed=42)
    sky(p, 50)
    vgrad(p, 40, 106, [(0, "#1c2a68"), (1, "#0a1038")])
    ground(p, 106, seed=5)
    claw(p, 0, False, 1)
    claw(p, 319, True, 5)
    # neon sign
    p.fill(p.m_rect(84, 10, 240, 52), (6, 10, 34))
    for q in ((84, 10, 240, 11), (84, 51, 240, 52), (84, 10, 85, 52), (239, 10, 240, 52)):
        p.fill(p.m_rect(*q), (30, 60, 140))
    text(p, 92, 12, "WORLD O'", (110, 255, 140), 30)
    text(p, 118, 30, "WONDERS", (110, 255, 140), 30)
    p.glow(162, 32, 90, (80, 255, 120), 0.4, 0.5)
    # shop front
    front = p.m_rect(70, 68, 250, 108)
    p.shade(front, "#4a5260", 1.3, 0.45, seed=6)
    p.edge(front, (0, 0, 0), 0.6)
    can = p.m_poly([(58, 68), (262, 68), (274, 84), (46, 84)])
    p.shade(can, "#d03a46", 1.35, 0.4, angle=(0, -1), seed=7)
    p.edge(can, (0, 0, 0), 0.6)
    p.fill(p.m_rect(130, 84, 192, 108), (4, 4, 10))
    p.glow(161, 100, 40, (255, 190, 120), 0.4)
    for x0 in (76, 200):
        win = p.m_rect(x0, 90, x0 + 46, 106)
        p.fill(win, p.lin(0, 90, 0, 106, "#b8f4ff", "#2a8aa0"))
        p.edge(win, (0, 0, 0), 0.6)
    tb = p.m_rect(210, 113, 236, 119)
    p.shade(tb, "#b86a30", 1.3, 0.45, seed=8)
    p.fill(p.m_rect(214, 119, 217, 131), (110, 60, 30))
    p.fill(p.m_rect(230, 119, 233, 131), (110, 60, 30))
    p.fill(p.m_ell(10, 134, 60, 142), (40, 6, 50), 0.4)
    return p


def canyon():
    p = Paint(base="#7ce0ec", seed=43)
    sky(p, 50)
    far_ridges(p, 20)
    # left and right magenta cliffs
    left = p.m_poly([(0, 0), (92, 0), (72, 44), (86, 98), (52, H), (0, H)])
    p.shade(left, "#c04aa8", 1.3, 0.3, angle=(1, 0), tex=0.14, seed=9)
    p.edge(left, (40, 0, 50), 0.6)
    right = p.m_poly([(228, 0), (W, 0), (W, H), (270, H), (252, 88), (242, 44)])
    p.shade(right, "#d86ac0", 1.4, 0.3, angle=(-1, 0), tex=0.14, seed=10)
    p.edge(right, (40, 0, 50), 0.6)
    # sandy canyon floor
    floor_m = p.m_poly([(86, 76), (244, 76), (276, H), (46, H)])
    p.fill(floor_m, p.lin(0, 76, 0, H, "#f0c070", "#9a6030"))
    p.multiply(0.8 + 0.4 * p.noise(7, 3, 4), 0.5)
    rock_arch(p, 96, 33, 90, 50, 3)
    spire(p, 200, 44, 39, 14, 4)
    for x, y in [(130, 100), (172, 104), (214, 98), (150, 120)]:
        p.fill(p.m_ell(x, y, x + 9, y + 4), (90, 56, 40))
    return p


def stalk_ridge():
    p = Paint(base="#7ce0ec", seed=44)
    sky(p, 56)
    far_ridges(p, 40)
    ground(p, 70, seed=6)
    shelf = p.m_poly([(0, 0), (W, 0), (W, 42), (250, 36), (180, 48), (100, 32), (0, 40)])
    p.shade(shelf, "#a05a2a", 1.3, 0.35, angle=(0, -1), tex=0.14, seed=11)
    p.edge(shelf, (30, 6, 0), 0.6)
    p.edge(shelf, (255, 220, 160), 0.3, "top")
    # the carnivorous stalk plant
    st = p.m_poly([(150, 40), (162, 40), (168, 72), (144, 72)])
    p.shade(st, "#3ac05a", 1.5, 0.3, angle=(-1, 0), seed=12)
    p.edge(st, (0, 50, 10), 0.6)
    for i in range(6):
        x = 138 + i * 10
        p.fill(p.m_line(x, 68, x + (i - 3) * 4, 98, 3), (230, 90, 200))
        p.fill(p.m_line(x, 68, x + (i - 3) * 4 - 1, 98, 1), (255, 200, 250), 0.6)
    for i in range(3):                                           # pulsating pods
        pod = p.m_ell(118 + i * 40, 70, 134 + i * 40, 92)
        p.fill(pod, p.radial(126 + i * 40, 78, 11, "#ffa0f0", "#a02090", 1.2))
        p.glow(126 + i * 40, 80, 20, (255, 100, 230), 0.3)
    trail = p.m_poly([(0, H), (60, 118), (140, 110), (W, 126), (W, H)])
    p.shade(trail, "#8a5a46", 1.3, 0.35, angle=(0, -1), tex=0.14, seed=13)
    p.edge(trail, (255, 230, 200), 0.3, "top")
    return p


ROOMS = {
    "landing_strip": landing_strip,
    "world_o_wonders": world_o_wonders,
    "canyon": canyon,
    "stalk_ridge": stalk_ridge,
}
