"""Act 5 (ScumSoft) with solid objects."""
import numpy as np
from kit import *
from solid import *
from p_act5 import exterior as _flat_exterior


def exterior():
    p = Paint(base="#c030c0", seed=71)
    vgrad(p, 0, 80, [(0, "#8a1c9a"), (0.6, "#d848d8"), (1, "#f8a0f0")])
    p.multiply(0.94 + 0.12 * p.noise(28, 2, 3), 0.5)
    ridge(p, 76, 8, "#7a2a8a", "#4a1a5a", seed=3, bottom=96, tex=0.05)
    p.fill(p.m_rect(0, 82, W, H), p.lin(0, 82, 0, H, "#58e868", "#1c8a30"))
    p.multiply(0.8 + 0.4 * p.noise(10, 3, 5), 0.45)
    p.fill(p.m_rect(0, 110, W, H), p.lin(0, 110, 0, H, "#b4b8c4", "#5a5e70"))
    p.multiply(0.85 + 0.3 * p.noise(6, 3, 6), 0.4)
    p.fill(p.m_rect(0, 110, W, 111), (255, 255, 255), 0.5)
    for x in range(0, W, 30):                                                  # slab joints on the apron
        p.fill(p.m_line(x, 111, x - 20, H, 1), (60, 64, 80), 0.4)
    # radar dish on a mast: a lit bowl
    cylinder_v(p, 92, 98, 30, 56, "#8a94a6")
    bowl = p.m_poly([(70, 0), (112, 0), (124, 22), (86, 36), (60, 18)])
    p.shade(bowl, "#d058d8", 1.5, 0.35, seed=7)
    p.edge(bowl, (60, 0, 70), 0.6)
    sphere(p, 98, 22, 4, "#fff0ff", spec=0.9)
    # the main bunker: wall, side, roof slab with a lip, recessed blue panel
    building(p, 28, 52, 140, 58, 14, 8, "#c4c8d4", "#d8dce8", seed=8)
    box(p, 24, 46, 150, 8, 16, 9, "#e0e4ee", seed=9)
    panel = p.m_rect(56, 66, 140, 104)
    box(p, 54, 64, 90, 42, 3, 2, "#2a3050", seed=10)
    p.fill(p.m_rect(58, 68, 138, 102), p.lin(0, 68, 0, 102, "#2a52d8", "#0a1860"))
    for y in range(72, 100, 6):
        p.fill(p.m_rect(62, y, 134, y + 1), (255, 90, 90), 0.8)
    p.fill(p.m_poly([(58, 68), (80, 68), (64, 102), (58, 102)]), (255, 255, 255), 0.12)
    p.glow(98, 86, 60, (90, 120, 255), 0.25)
    # sign
    box(p, 94, 34, 70, 14, 3, 2, "#1a1a2a", seed=11)
    text(p, 98, 34, "SCUMSOFT", (255, 220, 70), 18)
    # second bunker with a door
    building(p, 190, 74, 80, 36, 10, 6, "#b8bcc8", "#d0d4e0", seed=12)
    box(p, 214, 82, 30, 28, 2, 1, "#10121c", seed=13)
    p.fill(p.m_rect(216, 84, 242, 108), (4, 6, 12))
    sphere(p, 250, 96, 2.5, "#ff5a5a", spec=0.9, tint=(255, 90, 90))
    p.glow(250, 96, 12, (255, 90, 90), 0.5)
    # bollards and a lamp post
    for x in (284, 302):
        ground_shadow(p, x - 2, x + 14, 130, 4, 0.5, 1.5)
        cylinder_v(p, x, x + 8, 100, 130, "#c4c8d4")
        sphere(p, x + 4, 100, 4, "#e4e8f0", squash=0.6, spec=0.6)
    cylinder_v(p, 10, 15, 60, 136, "#9aa2b4")
    sphere(p, 12, 58, 5, "#fff4c0", spec=0.9, tint=(255, 240, 170))
    p.glow(12, 58, 30, (255, 240, 170), 0.3)
    p.glow(160, 130, 100, (255, 200, 255), 0.08, 0.3)
    return p


def closet():
    p = Paint(base="#1c1e28", seed=72)
    vgrad(p, 0, 108, [(0, "#2a2c3a"), (1, "#4a4c60")])
    p.multiply(0.8 + 0.4 * p.noise(10, 3, 4), 0.5)
    p.fill(p.m_rect(0, 108, W, H), p.lin(0, 108, 0, H, "#8a8e9c", "#2c2e3a"))
    for y in range(108, H, 9):
        p.fill(p.m_rect(0, y, W, y + 1), (30, 32, 44), 0.5)
    p.fill(p.m_rect(0, 108, W, 109), (255, 255, 255), 0.4)
    # shelves: a deep unit with a dark back, boards with front edges, items sitting on them
    soft_shadow(p, [(14, 108), (130, 108), (138, 124), (20, 126)], 0.55, 3.0)
    box(p, 16, 22, 108, 86, 8, 5, "#6a3a1a", seed=11, tex=0.08)
    p.fill(p.m_rect(20, 26, 120, 104), p.lin(0, 26, 0, 104, "#1c1008", "#2a180c"))
    for y in (46, 68, 90):
        box(p, 20, y, 100, 4, 6, 3, "#b8743a", seed=12 + y)
    box(p, 28, 28, 24, 18, 3, 2, "#f2f2fa", seed=20)
    box(p, 58, 30, 22, 16, 3, 2, "#9ae4ff", seed=21)
    box(p, 28, 50, 12, 18, 2, 1, "#5a6ee6", seed=22)
    cylinder_v(p, 48, 56, 52, 68, "#6ae08a")
    cylinder_v(p, 74, 84, 72, 90, "#e8c050")
    sphere(p, 98, 38, 7, "#ffe0a0", spec=0.6)
    # coveralls on a hook, with folds
    cylinder_v(p, 152, 156, 12, 24, "#c0c8d8")
    cov = [(138, 24), (172, 24), (182, 82), (130, 82)]
    m = plane(p, cov, "#3a5ad0", 1.0, angle=(-1, 0), spread=0.7, tex=0.1, seed=13, rim=0.3)
    for x in (146, 156, 166):
        p.fill(p.m_line(x, 28, x + (x - 156) // 3, 80, 1) & m, (0, 0, 40), 0.4)
        p.fill(p.m_line(x + 1, 28, x + 1 + (x - 156) // 3, 80, 1) & m, (200, 210, 255), 0.18)
    text(p, 146, 40, "SCUM", (240, 240, 250), 14)
    soft_shadow(p, [(150, 28), (192, 28), (198, 84), (156, 84)], 0.3, 4.0)
    # the locker with the vaporizer inside, and a bucket
    soft_shadow(p, [(216, 108), (298, 108), (310, 124), (222, 126)], 0.55, 3.0)
    box(p, 220, 40, 66, 68, 9, 5, "#8a94a6", seed=14)
    box(p, 246, 62, 18, 16, 2, 1, "#06080e", seed=15)
    sphere(p, 257, 70, 3, "#ff6a6a", spec=0.9, tint=(255, 90, 90))
    ground_shadow(p, 204, 238, 126, 4, 0.5, 2.0)
    cylinder_v(p, 208, 232, 108, 126, "#3a52c0")
    p.fill(p.m_ell(208, 105, 232, 111), (18, 24, 60))
    p.glow(160, 20, 120, (255, 240, 200), 0.25, 0.8)
    return p


def cubicle_maze():
    p = Paint(base="#2a52d8", seed=73)
    vgrad(p, 0, 112, [(0, "#2a48c0"), (1, "#4a6ae0")])
    for row in range(3):
        y = 4 + row * 38
        for col in range(5):
            x = 4 + col * 64
            soft_shadow(p, [(x + 2, y + 34), (x + 62, y + 34), (x + 64, y + 38), (x, y + 38)], 0.35, 1.5)
            wall = p.m_rect(x, y, x + 56, y + 30)
            p.shade(wall, "#d84038", 1.3, 0.7, angle=(0, -1), tex=0.05, seed=15 + row * 5 + col)
            p.edge(wall, (50, 0, 0), 0.55)
            box(p, x, y + 6, 4, 24, 4, 0, "#b0302c", seed=40 + col)                      # side partition with thickness
            box(p, x + 8, y + 20, 42, 5, 4, 3, "#c89a64", seed=50 + col)                   # desk top
            box(p, x + 17, y + 11, 18, 9, 2, 1, "#9aa4b4", seed=60 + col)                  # monitor
            p.fill(p.m_rect(x + 19, y + 12, x + 33, y + 18), (80, 130, 255), 0.9)
            head = sphere(p, x + 40, y + 12, 4, "#e8b896", spec=0.2)
            p.fill(p.m_rect(x + 36, y + 7, x + 44, y + 10), [(120, 255, 130), (255, 120, 230), (120, 220, 255)][(col + row) % 3])
    for x in (56, 120, 184, 248):                                                          # full trash cans
        ground_shadow(p, x - 2, x + 14, 132, 4, 0.5, 1.5)
        cylinder_v(p, x, x + 10, 112, 132, "#a4aab8")
        p.fill(p.m_ell(x, 108, x + 10, 114), (240, 240, 250))
        sphere(p, x + 5, 108, 4, "#fafaff", squash=0.8, spec=0.4)
    p.fill(p.m_rect(0, 134, W, H), (140, 146, 160))
    p.glow(160, 70, 200, (255, 255, 255), 0.06, 0.6)
    return p


def cell_block():
    p = Paint(base="#0a1a60", seed=75)
    vgrad(p, 0, H, [(0, "#06104a"), (1, "#1c3aa8")])
    for x in range(10, 90, 9):
        cylinder_v(p, x, x + 3, 4, 112, "#1a3090")
    ch = [(76, 22), (244, 22), (270, 60), (244, 112), (76, 112), (50, 60)]
    m = facet_rock(p, ch, "#2a52d8", 20, 1.3, 0.5, 0, edge=0.7)
    p.fill(p.m_poly([(76, 22), (244, 22), (236, 30), (84, 30)]), (255, 255, 255), 0.18)
    box(p, 148, 28, 26, 32, 3, 2, "#8a1c1c", seed=21)
    p.fill(p.m_rect(150, 30, 172, 58), (200, 40, 40))
    text(p, 154, 28, "6", (255, 255, 255), 30)
    for x in (108, 194):                                                                    # glass pods with the Two Guys
        soft_shadow(p, [(x - 4, 100), (x + 40, 100), (x + 46, 112), (x, 114)], 0.5, 2.5)
        box(p, x, 42, 34, 58, 6, 4, "#3ae060", seed=22 + x, tex=0.06)
        p.fill(p.m_rect(x + 5, 50, x + 29, 94), (6, 12, 20))
        person(p, x + 17, 94, 40, "#5a78d8", "#2a3a90", skin="#e8b896", seed=23 + x, hair="#5a3a1a")
        p.fill(p.m_poly([(x + 5, 50), (x + 16, 50), (x + 5, 72)]), (255, 255, 255), 0.14)
        p.glow(x + 17, 72, 36, (100, 255, 140), 0.3)
    soft_shadow(p, [(90, 114), (232, 114), (258, 134), (62, 134)], 0.5, 3.0)
    cons = p.m_poly([(94, 112), (226, 112), (252, 132), (68, 132)])
    p.shade(cons, "#5a7aff", 1.35, 0.5, angle=(0, -1), seed=24)
    p.edge(cons, (255, 255, 255), 0.35, "top")
    p.edge(cons, (0, 0, 0), 0.5)
    for i, c in enumerate([(255, 230, 90), (110, 255, 140), (255, 110, 100)]):
        sphere(p, 134 + i * 26, 121, 3.5, c, squash=0.6, spec=0.9, tint=c)
        p.glow(134 + i * 26, 121, 14, c, 0.35)
    p.glow(160, 66, 180, (120, 160, 255), 0.12, 0.7)
    return p


def mech(p, x, base_y, body, trim, flip=False):
    """a boxing mech suit: legs, torso, dome head with visor, heavy gloves"""
    ground_shadow(p, x - 22, x + 22, base_y - 2, 6, 0.6, 2.5)
    for dx in (-12, 2):
        box(p, x + dx, base_y - 30, 10, 30, 3, 2, body, seed=3 + dx, tex=0.05)
        box(p, x + dx - 2, base_y - 6, 14, 6, 3, 2, trim, seed=5 + dx)
    box(p, x - 16, base_y - 64, 32, 36, 6, 4, body, seed=7)
    p.fill(p.m_rect(x - 10, base_y - 54, x + 10, base_y - 44), (20, 24, 34))
    p.fill(p.m_rect(x - 10, base_y - 44, x + 10, base_y - 42), (255, 220, 90), 0.8)
    dome(p, x, base_y - 62, 11, 11, trim, spec=0.8)
    p.fill(p.m_rect(x - 7, base_y - 70, x + 7, base_y - 66), (255, 220, 90), 0.9)
    for sx in (-1, 1):
        cylinder_v(p, x + sx * 19 - 2, x + sx * 19 + 3, base_y - 60, base_y - 40, trim)
        sphere(p, x + sx * 21, base_y - 38, 8, "#f4f4fa", spec=0.7)


def hangar():
    p = Paint(base="#02030a", seed=76)
    vgrad(p, 0, 34, [(0, "#02030a"), (1, "#0a1a4a")])
    p.fill(p.m_rect(18, 36, 302, 106), p.lin(0, 36, 0, 106, "#a0fff8", "#38c8d0"))
    for x in range(30, 302, 40):
        cylinder_v(p, x, x + 7, 36, 70, "#2a98a8")
    # arena ring: a lit floor disc with a raised rim
    ring = p.m_ell(46, 82, 274, 124)
    p.shade(ring, "#a8f4f0", 1.4, 0.5, angle=(0, -1), seed=6)
    p.edge(ring, (0, 40, 50), 0.6)
    arena = p.m_ell(58, 86, 262, 116)
    p.fill(arena, p.radial(160, 100, 104, "#f0ffff", "#48c0c8", 0.4))
    mech(p, 108, 106, "#d84040", "#f2f2fa")
    mech(p, 214, 106, "#aab4c2", "#e8eef8")
    p.fill(p.m_rect(0, 120, W, H), p.lin(0, 120, 0, H, "#1a2030", "#04050a"))
    p.glow(160, 90, 160, (160, 255, 250), 0.2, 0.5)
    return p


ROOMS = {"pestulon_exterior": exterior, "closet": closet, "cubicle_maze": cubicle_maze, "cell_block": cell_block, "hangar": hangar}
