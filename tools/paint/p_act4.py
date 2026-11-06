"""Act 4: Ortega. Black rock, red cliffs and lava glow."""
import numpy as np
from kit import *


def sky(p, h=52):
    vgrad(p, 0, h, [(0, "#8a0c0c"), (0.5, "#e03a2a"), (1, "#f0902a")])
    p.multiply(0.94 + 0.12 * p.noise(26, 2, 3), 0.5)
    for x, y in [(30, 30), (150, 24), (262, 32)]:                 # glowing lava cracks on the horizon
        p.fill(p.m_line(x, y, x + 18, y - 5, 1), (255, 230, 100))
        p.fill(p.m_line(x + 18, y - 5, x + 30, y + 2, 1), (255, 160, 60))
        p.glow(x + 15, y - 3, 22, (255, 180, 60), 0.3)


def far_ridge(p, y=44, seed=3):
    ridge(p, y, 11, "#120408", "#2a0808", seed=seed, step=(12, 30), bottom=y + 40, tex=0.0)


def cliff(p, x0, x1, y0, y1):
    m = p.m_rect(x0, y0, x1, y1)
    p.fill(m, p.lin(0, y0, 0, y1, "#e04a30", "#400c10"))
    for x in range(x0, x1, 6):
        p.fill(p.m_line(x, y0 + 3, x - 3, y1, 1), (20, 4, 6), 0.55)
    p.multiply(0.8 + 0.4 * p.noise(5, 3, 8), 0.5)
    p.fill(p.m_rect(x0, y0, x1, y0 + 1), (255, 200, 140), 0.4)


def platform(p, pts, hi="#5a5258", lo="#0a0608", seed=2):
    m = p.m_poly(pts)
    p.shade(m, hi, 1.4, 0.3, angle=(0, -1), tex=0.18, seed=seed)
    p.edge(m, (255, 200, 160), 0.25, "top")
    p.edge(m, (0, 0, 0), 0.5)
    return m


def lava(p, pts, seed=1):
    m = p.m_poly(pts)
    p.fill(m, p.lin(0, min(q[1] for q in pts), 0, max(q[1] for q in pts), "#ffd040", "#c02010"))
    p.multiply(0.7 + 0.6 * p.noise(5, 3, seed), 0.6)
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    p.glow(sum(xs) / len(xs), sum(ys) / len(ys), 80, (255, 120, 40), 0.4, 0.6)


def crater():
    p = Paint(base="#8a0c0c", seed=61)
    sky(p)
    far_ridge(p)
    cliff(p, 0, W, 64, H)
    platform(p, [(0, 74), (120, 66), (W, 70), (W, 100), (200, 110), (0, 104)])
    lava(p, [(150, 100), (204, 108), (226, 144), (150, 144)], seed=3)
    hull = [(14, 62), (56, 54), (68, 66), (22, 70)]
    m = shaded(p, hull, "#aab4c2", 1.45, 0.35, seed=4, tex=0.1)
    p.fill(p.m_poly([(48, 55), (62, 58), (62, 64), (46, 62)]), (160, 240, 255))
    p.glow(40, 66, 60, (255, 120, 60), 0.15, 0.3)
    return p


def bridge():
    p = Paint(base="#8a0c0c", seed=62)
    sky(p, 44)
    far_ridge(p, 40, 4)
    p.fill(p.m_rect(0, 56, W, H), (8, 2, 4))
    cliff(p, 0, 94, 56, H)
    cliff(p, 230, W, 56, H)
    platform(p, [(0, 66), (96, 66), (96, 88), (0, 92)])
    platform(p, [(226, 66), (W, 66), (W, 92), (226, 88)])
    lava(p, [(94, 106), (228, 106), (232, H), (92, H)], seed=5)
    for x in range(98, 226, 10):                                   # rope bridge planks sagging in the middle
        sag = 10 - abs(x - 160) // 7
        p.fill(p.m_rect(x, 72 + 10 - sag, x + 7, 76 + 10 - sag), (150, 90, 44))
        p.fill(p.m_rect(x, 72 + 10 - sag, x + 7, 73 + 10 - sag), (230, 170, 100), 0.6)
    for x0, x1 in ((96, 160), (160, 228)):
        p.fill(p.m_line(x0, 64, (x0 + x1) // 2, 86, 1), (210, 200, 190))
        p.fill(p.m_line((x0 + x1) // 2, 86, x1, 64, 1), (210, 200, 190))
    return p


def station(detonator=True):
    p = Paint(base="#8a0c0c", seed=63)
    sky(p, 44)
    far_ridge(p, 40, 5)
    p.fill(p.m_rect(0, 54, W, H), (6, 3, 4))
    # black boulders with a red rim light
    for i in range(14):
        x, y = int(p.rng.integers(0, 300)), int(p.rng.integers(56, 104))
        w = int(p.rng.integers(22, 48))
        b = p.m_ell(x, y, x + w, y + w // 2 + 10)
        p.shade(b, "#4a4448", 1.5, 0.15, tex=0.2, seed=20 + i)
        p.edge(b, (255, 90, 50), 0.45, "right")
        p.edge(b, (0, 0, 0), 0.5)
    p.fill(p.m_rect(0, 112, W, H), p.lin(0, 112, 0, H, "#3a3236", "#0a0608"))
    p.multiply(0.7 + 0.6 * p.noise(6, 3, 6), 0.55)
    p.fill(p.m_rect(0, 112, W, 113), (255, 200, 160), 0.25)
    p.fill(p.m_line(0, 124, 130, 134, 2), (255, 120, 50), 0.8)
    p.glow(60, 130, 80, (255, 100, 40), 0.18, 0.3)
    # telescope on a tripod
    for x1, x2 in ((62, 74), (86, 74)):
        p.fill(p.m_line(x1, 92, x2, 122, 2), (190, 196, 208))
    tube = p.m_rect(58, 82, 92, 90)
    p.shade(tube, "#aab4c2", 1.4, 0.4, angle=(0, -1), seed=30)
    p.edge(tube, (0, 0, 0), 0.6)
    p.fill(p.m_rect(90, 80, 96, 92), (230, 236, 246))
    # green crate
    if detonator:
        cr = p.m_rect(190, 100, 214, 122)
        p.shade(cr, "#40e060", 1.4, 0.45, seed=31)
        p.edge(cr, (0, 60, 10), 0.6)
        p.fill(p.m_rect(198, 106, 206, 114), (4, 30, 10))
        p.glow(202, 112, 24, (80, 255, 110), 0.2)
    # wind meter
    p.fill(p.m_rect(260, 64, 262, 122), (210, 216, 228))
    for dx in (-11, 11):
        p.fill(p.m_line(261, 66, 261 + dx, 70, 1), (230, 236, 246))
        p.fill(p.m_ell(261 + dx - 3, 67, 261 + dx + 3, 73), (250, 250, 255))
    # two researchers in blue suits
    for x in (126, 148):
        suit = p.m_poly([(x, 112), (x + 2, 86), (x + 12, 86), (x + 14, 112)])
        p.shade(suit, "#2a52d8", 1.4, 0.4, seed=32 + x)
        p.edge(suit, (0, 0, 40), 0.6)
        p.fill(p.m_ell(x + 1, 76, x + 13, 88), (230, 190, 160))
        p.fill(p.m_rect(x + 3, 80, x + 11, 84), (150, 220, 255), 0.9)
    return p


def dome(shield=True):
    p = Paint(base="#8a0c0c", seed=64)
    sky(p, 44)
    far_ridge(p, 40, 6)
    p.fill(p.m_rect(0, 58, W, H), (6, 3, 4))
    cliff(p, 0, W, 108, H)
    platform(p, [(0, 76), (W, 74), (W, 112), (0, 112)])
    # the silver research dome
    d = p.m_ell(116, 52, 232, 126)
    p.shade(d, "#c8d0dc", 1.6, 0.3, angle=(-1, -1), tex=0.08, seed=33)
    p.edge(d, (0, 0, 0), 0.5)
    p.fill(p.m_rect(116, 92, 232, 114), (150, 158, 172))
    p.fill(p.m_rect(166, 100, 184, 114), (6, 8, 14))
    p.glow(175, 106, 22, (120, 200, 255), 0.3)
    # satellite dish
    dish = p.m_poly([(56, 40), (104, 28), (100, 76), (62, 76)])
    p.shade(dish, "#d8dee8", 1.5, 0.4, seed=34)
    p.edge(dish, (0, 0, 0), 0.6)
    p.fill(p.m_line(80, 76, 80, 100, 2), (120, 128, 144))
    if shield:                                                     # blue force-field mesh
        sh = p.m_rect(36, 20, 262, 112)
        for x in range(36, 263, 4):
            for y in range(20, 113, 4):
                p.a[y, x] = np.clip(p.a[y, x] * 0.5 + np.array([110, 150, 255], np.float32) * 0.6 * (1 if (x // 4 + y // 4) % 2 else 0.5), 0, 255)
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
    platform(p, [(0, 78), (W, 76), (W, 116), (0, 116)])
    lava(p, [(92, 92), (230, 92), (222, 122), (100, 122)], seed=7)
    for i in range(8):                                             # smoke from the crater
        p.glow(120 + i * 12, 70 - i * 6, 22, (70, 60, 66), 0.5)
    p.fill(p.m_rect(168, 100, 192, 103), (240, 244, 255))
    p.fill(p.m_rect(168, 100, 192, 101), (255, 255, 255))
    p.glow(180, 101, 22, (255, 255, 255), 0.5)
    return p


ROOMS = {
    "ortega_crater": crater,
    "ortega_bridge": bridge,
    "ortega_station": station,
    "ortega_dome": dome,
    "ortega_ridge": ridge_room,
}
