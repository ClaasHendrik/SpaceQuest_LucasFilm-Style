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
    from solid import box, plane, soft_shadow, rivets, cylinder_h, cylinder_v, TOP, FRONT, SIDE
    p = Paint(base="#4a1a6a", seed=74)
    # wall: deep violet with vertical panelling and a 3D baseboard
    vgrad(p, 0, 106, [(0, "#240c3c"), (1, "#5a2282")])
    for x in range(0, W, 40):
        p.fill(p.m_rect(x, 0, x + 1, 106), (0, 0, 0), 0.35)
        p.fill(p.m_rect(x + 1, 0, x + 2, 106), (200, 150, 255), 0.12)
    p.multiply(0.92 + 0.16 * p.noise(18, 2, 4), 0.5)
    p.fill(p.m_rect(0, 96, W, 108), p.lin(0, 96, 0, 108, "#8a6a9a", "#3a2848"))          # baseboard
    p.fill(p.m_rect(0, 96, W, 97), (255, 255, 255), 0.35)
    # floor with a darker rug under the desk
    p.fill(p.m_rect(0, 108, W, H), p.lin(0, 108, 0, H, "#8a8ca0", "#30323e"))
    p.multiply(0.85 + 0.3 * p.noise(10, 3, 5), 0.4)
    p.fill(p.m_rect(0, 108, W, 109), (255, 255, 255), 0.4)
    rug = p.m_poly([(70, 112), (260, 112), (284, 138), (46, 138)])
    p.shade(rug, "#7a1a2a", 1.25, 0.6, angle=(0, -1), tex=0.2, seed=30)
    p.edge(rug, (255, 200, 120), 0.35)
    p.glow(160, 40, 120, (255, 230, 170), 0.2, 0.8)
    # --- picture on the wall: beveled frame, mat, glass glint and a cast shadow
    soft_shadow(p, [(132, 18), (198, 18), (198, 64), (132, 64)], 0.45, 2.5)
    p.fill(p.m_rect(128, 14, 194, 60), p.lin(128, 14, 194, 60, "#e8c050", "#8a5a14"))
    for pts, k in (([(128, 14), (194, 14), (190, 18), (132, 18)], 1.0), ([(128, 14), (132, 18), (132, 56), (128, 60)], 0.85),
                   ([(194, 14), (194, 60), (190, 56), (190, 18)], 0.45), ([(132, 56), (190, 56), (194, 60), (128, 60)], 0.4)):
        plane(p, pts, "#d8a830", k, spread=0.2, seed=40, edge=0.45)
    p.fill(p.m_rect(133, 19, 189, 55), (10, 6, 18))
    p.edge(p.m_rect(133, 19, 189, 55), (255, 255, 255), 0.25, "bottom")
    p.fill(p.m_rect(133, 19, 189, 20), (0, 0, 0), 0.6)
    if picture:
        p.fill(p.m_rect(136, 22, 186, 52), p.lin(0, 22, 0, 52, "#5a3a7a", "#2a1844"))
        face = p.m_ell(150, 27, 172, 49)
        p.fill(face, p.radial(158, 33, 14, "#ffc8a8", "#c0705a"))
        p.fill(p.m_rect(152, 35, 156, 38), (30, 20, 30))
        p.fill(p.m_rect(162, 35, 166, 38), (30, 20, 30))
        p.fill(p.m_rect(148, 46, 176, 52), (250, 250, 255))
        p.fill(p.m_poly([(136, 22), (156, 22), (136, 44)]), (255, 255, 255), 0.10)       # glass glint
        p.fill(p.m_poly([(166, 52), (186, 30), (186, 40), (176, 52)]), (255, 255, 255), 0.07)
    # --- the desk: top surface, front with drawers and kneehole, thickness on the right side
    soft_shadow(p, [(86, 112), (236, 112), (276, 128), (112, 132)], 0.6, 3.5)
    mf, mt, ms = box(p, 96, 86, 130, 27, 22, 10, "#b86a2c", seed=50, tex=0.08)
    # wood grain on the top surface
    grain = p.noise(2, 3, 9)
    p.fill(mt, np.clip(np.asarray(p.a) * (0.9 + 0.2 * grain[..., None]), 0, 255), 0.5)
    p.fill(p.m_poly([(100, 85), (222, 85), (240, 77), (118, 77)]) & mt, (255, 230, 170), 0.10)
    # drawers: left pedestal and right pedestal, dark kneehole between
    p.fill(p.m_rect(128, 88, 194, 111), (28, 12, 6), 0.9)
    p.fill(p.m_rect(128, 88, 194, 90), (0, 0, 0), 0.5)
    for x0, x1 in ((99, 126), (196, 223)):
        for y0 in (89, 97, 105):
            d = p.m_rect(x0, y0, x1, y0 + 7)
            p.shade(d, "#c8783a", 1.3, 0.75, angle=(0, -1), seed=51 + y0)
            p.edge(d, (0, 0, 0), 0.55)
            p.edge(d, (255, 230, 170), 0.35, "top")
            hx = (x0 + x1) // 2
            p.fill(p.m_rect(hx - 4, y0 + 3, hx + 4, y0 + 4), (245, 220, 120))
            p.fill(p.m_rect(hx - 4, y0 + 4, hx + 4, y0 + 5), (0, 0, 0), 0.45)
    # --- on the desk
    soft_shadow(p, [(138, 84), (196, 84), (204, 88), (146, 89)], 0.45, 1.5)
    mon_f, mon_t, mon_s = box(p, 144, 65, 42, 18, 5, 3, "#8a94a6", seed=60, tex=0.05)
    scr = p.m_rect(147, 68, 181, 80)
    p.fill(scr, p.lin(0, 68, 0, 80, "#4a78ff", "#0a1a70"))
    for i in range(4):
        p.fill(p.m_rect(149, 69 + i * 2.6, 149 + 18 + (i * 7) % 10, 70 + i * 2.6), (200, 230, 255), 0.7)
    p.fill(p.m_poly([(147, 68), (160, 68), (152, 80), (147, 80)]), (255, 255, 255), 0.10)
    p.glow(164, 74, 40, (90, 130, 255), 0.28)
    p.fill(p.m_rect(158, 82, 170, 86), (60, 66, 80))
    # nameplate
    plate = box(p, 176, 82, 22, 5, 4, 2, "#e8c050", seed=61, tex=0.0)
    text(p, 178, 80, "E.PUG", (60, 36, 6), 9)
    # the keycard, lying on the desk in perspective, with a glint and a tiny shadow
    if card:
        soft_shadow(p, [(106, 83), (124, 83), (128, 80), (110, 80)], 0.4, 1.0)
        card_m = p.m_poly([(105, 82), (122, 82), (126, 79), (109, 79)])
        p.fill(card_m, p.lin(105, 82, 126, 79, "#ffffff", "#aab4c8"))
        p.fill(p.m_poly([(108, 81), (112, 81), (114, 79.6), (110, 79.6)]), (90, 210, 255))
        p.edge(card_m, (0, 0, 0), 0.4)
        p.fill(p.m_line(116, 81, 120, 79, 1), (255, 255, 255), 0.9)
        p.glow(116, 80, 12, (200, 240, 255), 0.35)
    # a desk lamp
    p.fill(p.m_ell(206, 80, 220, 85), (30, 34, 44))
    p.fill(p.m_line(213, 82, 216, 64, 1), (150, 158, 172))
    shade_p = p.m_poly([(208, 60), (226, 60), (230, 68), (206, 68)])
    p.shade(shade_p, "#2a9a60", 1.4, 0.45, seed=62)
    p.edge(shade_p, (0, 0, 0), 0.5)
    p.glow(218, 70, 36, (255, 240, 170), 0.35, 0.9)
    # --- photocopier: lid, control panel, output tray, side face
    soft_shadow(p, [(244, 110), (296, 110), (306, 124), (250, 126)], 0.55, 3.0)
    cf, ct, cs = box(p, 248, 56, 42, 54, 10, 6, "#a8b0c2", seed=70, tex=0.05)
    p.fill(p.m_rect(252, 60, 286, 68), (16, 20, 30))
    p.fill(p.m_rect(254, 62, 262, 66), (110, 255, 140), 0.9)
    p.fill(p.m_rect(266, 62, 270, 66), (255, 90, 90), 0.9)
    p.fill(p.m_poly([(250, 76), (288, 76), (290, 80), (248, 80)]), (0, 0, 0), 0.4)
    p.fill(p.m_rect(252, 92, 286, 106), (14, 16, 24))
    p.fill(p.m_rect(254, 94, 284, 95), (255, 255, 255), 0.2)
    p.fill(p.m_poly([(250, 72), (292, 72), (299, 66), (258, 66)]) & ct, (255, 255, 255), 0.15)
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
