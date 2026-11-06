"""Act 5: Pestulon and ScumSoft. Magenta sky, green ground, grey bunkers; red cubicles on blue; the finale."""
import numpy as np
from kit import *


def exterior():
    p = Paint(base="#c030c0", seed=71)
    vgrad(p, 0, 80, [(0, "#8a1c9a"), (0.6, "#d848d8"), (1, "#f8a0f0")])
    p.multiply(0.94 + 0.12 * p.noise(28, 2, 3), 0.5)
    ridge(p, 76, 8, "#7a2a8a", "#4a1a5a", seed=3, bottom=96, tex=0.05)
    p.fill(p.m_rect(0, 82, W, H), p.lin(0, 82, 0, H, "#58e868", "#1c8a30"))
    p.multiply(0.8 + 0.4 * p.noise(10, 3, 5), 0.45)
    p.fill(p.m_rect(0, 108, W, H), p.lin(0, 108, 0, H, "#b4b8c4", "#5a5e70"))        # concrete apron
    p.multiply(0.85 + 0.3 * p.noise(6, 3, 6), 0.4)
    p.fill(p.m_rect(0, 108, W, 109), (255, 255, 255), 0.5)
    # radar dish
    dish = p.m_poly([(70, 0), (112, 0), (124, 20), (86, 34), (60, 16)])
    p.shade(dish, "#d058d8", 1.4, 0.4, seed=7)
    p.edge(dish, (60, 0, 70), 0.6)
    p.fill(p.m_line(94, 34, 100, 56, 3), (150, 156, 170))
    # grey bunker with a blue panel
    bunker = p.m_poly([(28, 108), (28, 66), (60, 48), (150, 48), (178, 66), (178, 108)])
    p.shade(bunker, "#c4c8d4", 1.4, 0.4, tex=0.1, seed=8)
    p.edge(bunker, (30, 30, 50), 0.6)
    p.edge(bunker, (255, 255, 255), 0.3, "top")
    panel = p.m_rect(60, 66, 142, 106)
    p.fill(panel, p.lin(0, 66, 0, 106, "#2a52d8", "#0a1860"))
    for y in range(70, 104, 6):
        p.fill(p.m_rect(66, y, 136, y + 1), (255, 90, 90), 0.8)
    p.edge(panel, (0, 0, 0), 0.7)
    p.glow(101, 86, 60, (90, 120, 255), 0.25)
    # second bunker with a door
    b2 = p.m_poly([(186, 108), (186, 76), (210, 62), (252, 62), (274, 76), (274, 108)])
    p.shade(b2, "#b8bcc8", 1.4, 0.4, tex=0.1, seed=9)
    p.edge(b2, (30, 30, 50), 0.6)
    p.fill(p.m_rect(214, 82, 246, 108), (6, 8, 14))
    p.fill(p.m_rect(246, 90, 250, 100), (255, 90, 90))
    p.glow(248, 95, 10, (255, 90, 90), 0.5)
    sign = p.m_rect(98, 36, 160, 48)
    p.fill(sign, (6, 6, 14))
    text(p, 102, 36, "SCUMSOFT", (255, 220, 70), 18)
    # bollards, a lamp post and guards' tower in the distance
    for x in (284, 300):
        b = p.m_rect(x, 96, x + 8, 128)
        p.shade(b, "#c4c8d4", 1.4, 0.4, angle=(-1, 0), seed=10 + x)
    p.fill(p.m_rect(8, 112, 20, 138), (150, 156, 170))
    p.glow(160, 130, 100, (255, 200, 255), 0.08, 0.3)
    return p


def closet():
    p = Paint(base="#1c1e28", seed=72)
    vgrad(p, 0, 106, [(0, "#2a2c3a"), (1, "#4a4c60")])
    p.multiply(0.8 + 0.4 * p.noise(10, 3, 4), 0.5)
    p.fill(p.m_rect(0, 106, W, H), p.lin(0, 106, 0, H, "#8a8e9c", "#2c2e3a"))
    for y in range(106, H, 9):
        p.fill(p.m_rect(0, y, W, y + 1), (30, 32, 44), 0.5)
    sh = p.m_rect(18, 22, 122, 108)
    p.shade(sh, "#b8743a", 1.3, 0.4, tex=0.12, seed=11)
    p.edge(sh, (30, 10, 0), 0.6)
    for y in (46, 70):
        p.fill(p.m_rect(18, y, 122, y + 3), (120, 60, 24))
    p.fill(p.m_rect(30, 26, 52, 44), (250, 250, 255))
    p.fill(p.m_rect(60, 30, 82, 44), (150, 230, 255))
    p.fill(p.m_rect(30, 50, 42, 68), (90, 110, 230))
    p.fill(p.m_rect(48, 54, 58, 68), (110, 230, 130))
    # coveralls on a hook
    p.fill(p.m_rect(152, 14, 156, 24), (190, 196, 210))
    cov = p.m_poly([(140, 24), (172, 24), (180, 80), (132, 80)])
    p.shade(cov, "#3a5ad0", 1.35, 0.4, seed=12)
    p.edge(cov, (0, 0, 40), 0.6)
    text(p, 146, 40, "SCUM", (240, 240, 250), 14)
    # locker with the vaporizer
    lk = p.m_rect(220, 40, 292, 108)
    p.shade(lk, "#8a94a6", 1.35, 0.4, seed=13)
    p.edge(lk, (0, 0, 0), 0.6)
    p.fill(p.m_rect(248, 64, 266, 78), (6, 8, 14))
    p.fill(p.m_rect(256, 66, 258, 76), (255, 90, 90))
    bucket = p.m_poly([(208, 106), (232, 106), (230, 124), (210, 124)])
    p.shade(bucket, "#3a52c0", 1.3, 0.4, seed=14)
    p.glow(160, 20, 120, (255, 240, 200), 0.25, 0.8)
    return p


def cubicle_maze():
    p = Paint(base="#2a52d8", seed=73)
    vgrad(p, 0, 112, [(0, "#2a48c0"), (1, "#4a6ae0")])
    for row in range(3):
        y = 4 + row * 38
        for col in range(5):
            x = 4 + col * 64
            cub = p.m_rect(x, y, x + 56, y + 32)
            p.shade(cub, "#d84038", 1.35, 0.45, angle=(0, -1), seed=15 + row * 5 + col)
            p.edge(cub, (50, 0, 0), 0.6)
            p.edge(cub, (255, 200, 180), 0.3, "top")
            desk = p.m_rect(x + 8, y + 22, x + 48, y + 28)
            p.shade(desk, "#c89a64", 1.3, 0.6, angle=(0, -1), seed=40 + col)
            p.fill(p.m_rect(x + 20, y + 10, x + 36, y + 22), (240, 240, 250))
            hd = p.m_ell(x + 24, y + 6, x + 32, y + 14)
            p.fill(hd, (230, 190, 160))
            p.fill(p.m_rect(x + 26, y + 1, x + 31, y + 4), [(120, 255, 130), (255, 120, 230), (120, 220, 255)][(col + row) % 3])
    for x in (56, 120, 184, 248):                                   # full trash cans
        c = p.m_rect(x, 112, x + 10, 132)
        p.shade(c, "#a4aab8", 1.4, 0.4, angle=(-1, 0), seed=60 + x)
        p.fill(p.m_rect(x + 1, 108, x + 9, 113), (240, 240, 250))
    p.fill(p.m_rect(0, 134, W, H), (140, 146, 160))
    p.glow(160, 70, 200, (255, 255, 255), 0.06, 0.6)
    return p


def elmo_office(card=True, picture=True):
    p = Paint(base="#4a1a6a", seed=74)
    vgrad(p, 0, 112, [(0, "#2a0e44"), (1, "#6a2a90")])
    p.multiply(0.9 + 0.2 * p.noise(18, 2, 4), 0.5)
    p.fill(p.m_rect(0, 112, W, H), p.lin(0, 112, 0, H, "#9a9ca8", "#40424e"))
    desk = p.m_rect(96, 78, 232, 112)
    p.shade(desk, "#b86a30", 1.35, 0.4, angle=(0, -1), seed=16)
    p.edge(desk, (30, 10, 0), 0.6)
    p.edge(desk, (255, 220, 170), 0.3, "top")
    mon = p.m_rect(142, 60, 190, 78)
    p.shade(mon, "#6a7284", 1.3, 0.5, seed=17)
    p.fill(p.m_rect(146, 62, 186, 76), p.lin(0, 62, 0, 76, "#2a52d8", "#0a1860"))
    if card:
        p.fill(p.m_rect(108, 80, 124, 87), (250, 250, 255))
        p.fill(p.m_rect(110, 82, 122, 85), (110, 220, 255))
    if picture:
        fr = p.m_rect(128, 14, 194, 58)
        p.shade(fr, "#c89a30", 1.4, 0.4, seed=18)
        p.edge(fr, (30, 20, 0), 0.6)
        p.fill(p.m_rect(134, 20, 188, 52), (14, 8, 24))
        p.fill(p.m_ell(150, 26, 172, 48), (240, 150, 130))
        p.fill(p.m_rect(146, 46, 176, 52), (240, 240, 250))
    cop = p.m_rect(250, 44, 296, 112)
    p.shade(cop, "#9aa2b4", 1.35, 0.4, seed=19)
    p.edge(cop, (0, 0, 0), 0.6)
    p.fill(p.m_rect(254, 48, 292, 62), (200, 210, 226))
    p.fill(p.m_rect(266, 74, 280, 84), (255, 90, 90))
    p.glow(160, 36, 100, (255, 240, 200), 0.18, 0.7)
    return p


def cell_block():
    p = Paint(base="#0a1a60", seed=75)
    vgrad(p, 0, H, [(0, "#06104a"), (1, "#1c3aa8")])
    for x in range(10, 90, 9):
        p.fill(p.m_line(x, 4, x + 4, 112, 1), (0, 0, 20), 0.5)
    ch = p.m_poly([(76, 22), (244, 22), (270, 60), (244, 112), (76, 112), (50, 60)])
    p.shade(ch, "#2a52d8", 1.35, 0.4, seed=20)
    p.edge(ch, (0, 0, 40), 0.7)
    p.fill(p.m_rect(150, 28, 172, 58), (200, 40, 40))
    text(p, 154, 28, "6", (255, 255, 255), 30)
    for x in (110, 196):                                            # green pods with the Two Guys
        pod = p.m_rect(x, 44, x + 32, 100)
        p.shade(pod, "#3ae060", 1.4, 0.4, seed=21 + x)
        p.edge(pod, (0, 40, 10), 0.6)
        p.fill(p.m_rect(x + 5, 52, x + 27, 94), (6, 12, 20))
        p.fill(p.m_ell(x + 11, 56, x + 21, 66), (240, 190, 160))
        p.fill(p.m_rect(x + 10, 66, x + 22, 90), (60, 90, 200))
        p.glow(x + 16, 72, 36, (100, 255, 140), 0.3)
    cons = p.m_poly([(94, 112), (226, 112), (252, 132), (68, 132)])
    p.shade(cons, "#5a7aff", 1.3, 0.5, angle=(0, -1), seed=22)
    p.fill(p.m_rect(150, 116, 170, 122), (255, 230, 90))
    p.glow(160, 118, 40, (255, 230, 90), 0.3)
    p.glow(160, 66, 180, (120, 160, 255), 0.12, 0.7)
    return p


def hangar():
    p = Paint(base="#02030a", seed=76)
    vgrad(p, 0, 34, [(0, "#02030a"), (1, "#0a1a4a")])
    p.fill(p.m_rect(18, 36, 302, 106), p.lin(0, 36, 0, 106, "#a0fff8", "#38c8d0"))
    for x in range(30, 302, 40):
        p.fill(p.m_rect(x, 36, x + 7, 68), (30, 150, 160))
    arena = p.m_ell(52, 84, 268, 120)
    p.fill(arena, p.radial(160, 100, 110, "#e8ffff", "#38b8c0", 0.4))
    p.edge(arena, (0, 40, 50), 0.6)
    for x, c in ((98, "#d84040"), (216, "#aab4c2")):                # two mech suits
        s = p.m_rect(x - 12, 50, x + 12, 104)
        p.shade(s, c, 1.4, 0.35, seed=23 + x)
        p.edge(s, (0, 0, 0), 0.7)
        p.fill(p.m_rect(x - 10, 44, x + 10, 54), (240, 240, 250))
        p.fill(p.m_rect(x - 6, 47, x + 6, 51), (255, 220, 80))
        p.fill(p.m_ell(x - 22, 70, x - 10, 84), (240, 240, 250))
        p.fill(p.m_ell(x + 10, 70, x + 22, 84), (240, 240, 250))
    p.fill(p.m_rect(0, 118, W, H), p.lin(0, 118, 0, H, "#1a2030", "#04050a"))
    p.glow(160, 90, 160, (160, 255, 250), 0.2, 0.5)
    return p


def space_battle():
    p = Paint(base="#02030a", seed=77)
    p.stars(p.m_rect(0, 0, W, H), 260, seed=2)
    p.stars(p.m_rect(0, 0, W, H), 30, seed=3, bright=1.6)
    ring = p.m_ell(58, 36, 222, 130)
    p.fill(ring, p.radial(140, 83, 90, "#0a1860", "#02030a", 0.6))
    p.edge(ring, (60, 90, 255), 0.7, width=2)
    p.fill(p.m_rect(138, 62, 142, 104), (110, 255, 140))
    p.fill(p.m_rect(116, 81, 164, 85), (110, 255, 140))
    p.fill(p.m_ell(133, 76, 147, 90), (2, 3, 10))
    p.fill(p.m_rect(248, 6, 312, 32), (4, 14, 8))
    for q in ((248, 6, 312, 7), (248, 31, 312, 32), (248, 6, 249, 32), (311, 6, 312, 32)):
        p.fill(p.m_rect(*q), (110, 255, 140))
    p.fill(p.m_rect(279, 17, 283, 21), (255, 80, 70))
    p.glow(281, 19, 14, (255, 80, 70), 0.6)
    text(p, 6, 4, "SHIELD  F", (110, 255, 140), 16)
    p.fill(p.m_rect(6, 20, 90, 25), (110, 255, 140))
    p.glow(140, 83, 120, (80, 110, 255), 0.12, 0.6)
    return p


def deep_space():
    p = Paint(base="#02030a", seed=78)
    vgrad(p, 0, H, [(0, "#02030a"), (1, "#0a0a28")])
    p.stars(p.m_rect(0, 0, W, H), 340, seed=4)
    for r, c in [(86, "#101a70"), (66, "#2a3aa8"), (44, "#7a4ad0")]:
        g = p.m_ell(160 - r, 78 - r // 2, 160 + r, 78 + r // 2)
        p.fill(g, p.radial(160, 78, r, c, "#02030a", 0.5), 0.85)
    core = p.m_ell(122, 62, 198, 94)
    p.fill(core, p.radial(160, 78, 38, "#fffce0", "#a090ff", 0.45))
    p.glow(160, 78, 100, (200, 180, 255), 0.5, 0.5)
    text(p, 98, 6, "THE END", (255, 110, 110), 34)
    text(p, 76, 118, "Roger Wilco will return.", (110, 255, 140), 18)
    return p


ROOMS = {
    "pestulon_exterior": exterior,
    "closet": closet,
    "cubicle_maze": cubicle_maze,
    "elmo_office": elmo_office,
    "cell_block": cell_block,
    "hangar": hangar,
    "space_battle": space_battle,
    "deep_space": deep_space,
}
