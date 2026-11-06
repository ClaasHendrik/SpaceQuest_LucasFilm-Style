"""Act 1 with solid objects (overrides the flat versions in p_act1.py)."""
import numpy as np
from kit import *
from solid import *
from p_act1 import freighter_wall, deck


def robot_head():
    p = Paint(base="#05070f", seed=31)
    freighter_wall(p)
    # chasm (left) with a lit lip
    p.fill(p.m_rect(0, 112, 104, H), (2, 3, 8))
    lip = p.m_poly([(0, 112), (104, 112), (96, 120), (0, 126)])
    p.fill(lip, p.lin(0, 112, 0, 126, "#3a4258", "#05060c"))
    p.fill(p.m_line(0, 112, 104, 112, 1), (200, 215, 240), 0.45)
    p.fill(p.m_rect(104, 112, W, H), p.lin(0, 112, 0, H, "#3a4252", "#10141c"))
    p.multiply(0.75 + 0.5 * p.noise(8, 3, 3), 0.45)
    p.fill(p.m_rect(104, 112, W, 113), (200, 210, 220), 0.35)
    p.fill(p.m_rect(103, 112, 105, H), (0, 0, 0), 0.7)
    # the giant head: a block with a brow ridge, recessed eyes, side plates and a grille
    ground_shadow(p, 140, 330, 112, 10, 0.65, 4.0)
    box(p, 152, 16, 150, 96, 14, 10, "#8f9bab", seed=5, tex=0.12)
    ear_l = box(p, 136, 40, 18, 44, 6, 4, "#6a7486", seed=7)
    ear_r = box(p, 302, 40, 14, 44, 8, 4, "#6a7486", seed=8)
    brow = box(p, 160, 24, 134, 12, 6, 4, "#a8b4c4", seed=9)               # protruding brow
    soft_shadow(p, [(162, 36), (296, 36), (296, 48), (162, 48)], 0.55, 2.0)
    for cx, broken in ((192, True), (260, False)):
        sock = p.m_ell(cx - 19, 36, cx + 19, 74)
        p.fill(sock, (4, 5, 9))
        p.edge(sock, (255, 255, 255), 0.18, "bottom")
        sphere(p, cx, 55, 15, "#ff5a30" if broken else "#8ee8ff", spec=0.8, tint=(255, 120, 60) if broken else (80, 200, 255))
        p.glow(cx, 55, 46, (255, 80, 50) if broken else (120, 220, 255), 0.35 if broken else 0.2)
    p.fill(p.m_line(176, 40, 212, 70, 2), (4, 4, 8))                         # the crack across the broken eye
    p.fill(p.m_line(180, 38, 208, 66, 1), (255, 170, 120), 0.55)
    mouth = p.m_rect(190, 84, 274, 102)
    p.fill(mouth, (4, 6, 10))
    p.fill(p.m_rect(190, 84, 274, 86), (0, 0, 0), 0.6)
    for x in range(194, 274, 7):
        cylinder_v(p, x, x + 3, 86, 101, "#9aa6b8")
    for x, y in [(160, 24), (296, 24), (160, 106), (296, 106), (160, 66), (296, 66)]:
        sphere(p, x, y, 2, "#5a6272", spec=0.6)
    ant = cylinder_v(p, 222, 232, 0, 17, "#8a94a6")
    sphere(p, 227, 2, 3, "#ff6a50", spec=0.9, tint=(255, 90, 70))
    p.glow(227, 2, 14, (255, 90, 70), 0.5)
    weather(p, p.m_rect(152, 16, 302, 112), "#2a1c16", 0.16, 4, 12, 0.56)
    # sharp metal plate on the deck: thin slab with a bright edge
    soft_shadow(p, [(114, 130), (150, 124), (158, 130), (120, 138)], 0.5, 1.5)
    plate = p.m_poly([(118, 128), (140, 120), (148, 126), (126, 134)])
    p.shade(plate, "#d8e4f4", 1.3, 0.7, seed=3)
    p.edge(plate, (0, 0, 0), 0.5)
    p.fill(p.m_line(118, 128, 140, 120, 1), (255, 255, 255), 0.9)
    p.glow(130, 126, 18, (220, 235, 255), 0.18)
    p.glow(260, 124, 90, (130, 160, 220), 0.1, 0.3)
    return p


def conveyor():
    p = Paint(base="#05070f", seed=32)
    freighter_wall(p, 100)
    p.fill(p.m_rect(0, 100, W, H), p.lin(0, 100, 0, H, "#1c202c", "#06070b"))
    p.fill(p.m_rect(0, 100, W, 101), (200, 210, 225), 0.2)
    # the belt: a slab with a visible top surface, rollers at the ends and a hazard-striped skirt
    soft_shadow(p, [(0, 118), (260, 118), (276, 130), (0, 134)], 0.6, 3.0)
    box(p, 0, 92, 250, 20, 0, 0, "#444c5c", seed=9)
    top = p.m_poly([(0, 92), (250, 92), (262, 84), (12, 84)])
    p.shade(top, "#5a6478", 1.3, 0.8, angle=(0, -1), seed=10)
    p.edge(top, (255, 255, 255), 0.3, "top")
    p.edge(top, (0, 0, 0), 0.4)
    for x in range(0, 250, 10):
        p.fill(p.m_rect(x, 94, x + 3, 110), (10, 12, 18), 0.8)
        p.fill(p.m_rect(x + 3, 94, x + 4, 110), (255, 255, 255), 0.12)
    cylinder_v(p, 0, 8, 90, 114, "#6a7486")
    cylinder_v(p, 242, 250, 90, 114, "#6a7486")
    skirt = p.m_rect(0, 112, 250, 121)
    p.fill(skirt, p.lin(0, 112, 0, 121, "#8a93a4", "#2a3040"))
    for x in range(0, 250, 12):
        p.fill(p.m_poly([(x, 112), (x + 6, 112), (x + 10, 121), (x + 4, 121)]), (232, 190, 40))
    p.fill(p.m_rect(0, 112, 250, 113), (255, 255, 255), 0.4)
    # scrap riding the belt: faceted lumps with their own shadows
    cols = ["#b05226", "#2c8090", "#7c7c88", "#a02c2e", "#60408a", "#b05226", "#7c7c88"]
    for i, x in enumerate(range(10, 236, 33)):
        soft_shadow(p, [(x - 2, 90), (x + 28, 90), (x + 32, 94), (x + 2, 94)], 0.5, 1.5)
        facet_rock(p, [(x, 90), (x + 6, 76 - i % 3 * 3), (x + 18, 74), (x + 28, 84), (x + 30, 90)], cols[i % 7], seed=20 + i, facets=2)
    # crusher: a block with depth, piston rods and a hydraulic housing
    p.fill(p.m_rect(252, 0, 304, 14), (70, 76, 90))
    box(p, 250, 0, 56, 14, 0, 0, "#6a7486", seed=11)
    cylinder_v(p, 270, 284, 14, 62, "#c4ccd8")
    cylinder_v(p, 262, 266, 14, 62, "#a4acb8")
    cylinder_v(p, 288, 292, 14, 62, "#a4acb8")
    box(p, 252, 62, 50, 36, 8, 5, "#7c8898", seed=12, tex=0.14)
    for x in range(256, 300, 8):
        p.fill(p.m_rect(x, 64, x + 1, 96), (20, 24, 32), 0.6)
    weather(p, p.m_rect(252, 62, 310, 98), "#1a1210", 0.2, 4, 5, 0.56)
    p.fill(p.m_rect(246, 0, 250, 104), (24, 28, 40))
    p.fill(p.m_rect(310, 0, 314, 104), (24, 28, 40))
    for k in range(3):
        p.glow(318, 76 - k * 14, 22, (210, 225, 240), 0.35)
    # drainage pipe: a tube mouth with a bevelled rim
    rim = p.m_ell(298, 112, 322, 140)
    p.shade(rim, "#6a7486", 1.4, 0.4, seed=13)
    p.edge(rim, (0, 0, 0), 0.6)
    mouth = p.m_ell(302, 116, 320, 136)
    p.fill(mouth, p.radial(311, 126, 12, "#0a1834", "#010204", 1.1))
    p.glow(311, 126, 22, (60, 110, 200), 0.3)
    # the vertical trash bucket on its chain: it carries scrap up to the overhead rail
    cylinder_v(p, 14, 18, 0, 56, "#8a94a6")
    ground_shadow(p, 2, 32, 90, 4, 0.4, 2.0)
    cylinder_v(p, 4, 28, 56, 88, "#7a8698")
    rimm = p.m_ell(4, 52, 28, 62)
    p.shade(rimm, "#b0bac8", 1.4, 0.5, seed=41)
    p.fill(p.m_ell(6, 54, 26, 60), (4, 6, 10))
    weather(p, p.m_rect(4, 56, 28, 88), "#5a3a1a", 0.45, 3, 17, 0.45)
    text(p, 6, 128, "DANGER", (255, 210, 60), 16)
    p.glow(130, 100, 100, (255, 200, 110), 0.12, 0.3)
    return p


def rat_lair(reactor=True, ladder=True):
    p = Paint(base="#020308", seed=33)
    vgrad(p, 0, H, [(0, "#020308"), (0.6, "#06101a"), (1, "#021208")])
    for i in range(34):
        x = int(p.rng.integers(0, W))
        p.fill(p.m_line(x, 0, x + int(p.rng.integers(-16, 16)), int(p.rng.integers(20, 78)), 2), (40, 54, 70), 0.7)
    p.multiply(0.7 + 0.6 * p.noise(14, 3, 4), 0.6)
    # reactor in its pit: a raised collar ring, glowing core
    pit = p.m_ell(80, 98, 242, 156)
    p.fill(pit, p.radial(161, 128, 82, "#9bff6a", "#03140a", 0.4))
    collar = p.m_ell(100, 104, 222, 146)
    p.shade(collar, "#5a6676", 1.5, 0.3, seed=14)
    p.edge(collar, (0, 0, 0), 0.6)
    inner = p.m_ell(112, 110, 210, 140)
    if reactor:
        p.fill(inner, p.radial(161, 124, 46, "#e8ffc0", "#2ac030", 0.45))
        sphere(p, 161, 122, 15, "#c8ff9a", squash=0.7, spec=0.9, tint=(120, 255, 90))
        p.glow(161, 118, 130, (80, 255, 60), 0.5, 0.5)
        cylinder_v(p, 152, 170, 94, 112, "#7a9a8a")
    else:
        p.fill(inner, p.radial(161, 124, 46, "#2a3a30", "#04080a", 0.45))
        p.glow(161, 124, 60, (60, 140, 60), 0.12, 0.5)
    # suspended platforms: slabs with thickness, chains with links
    for x0 in (36, 206):
        soft_shadow(p, [(x0, 82), (x0 + 88, 82), (x0 + 96, 96), (x0 + 6, 96)], 0.5, 2.5)
        box(p, x0, 72, 84, 10, 8, 4, "#8a96a8", seed=15 + x0, tex=0.1)
        for x in (x0 + 12, x0 + 70):
            cylinder_v(p, x, x + 2, 0, 72, "#6a7486")
    from solid import ladder as _ladder
    _ladder(p, 18, 36, 24, 112)
    if ladder:                                                   # the portable ladder, leaning on the platform edge
        ladder_x = 104
        soft_shadow(p, [(ladder_x + 8, 52), (ladder_x + 26, 52), (ladder_x + 30, 80), (ladder_x + 12, 80)], 0.4, 2.0)
        for k in range(2):
            p.fill(p.m_line(ladder_x + k * 14, 80, ladder_x + 8 + k * 14, 40, 3), (180, 190, 205))
            p.fill(p.m_line(ladder_x - 1 + k * 14, 80, ladder_x + 7 + k * 14, 40, 1), (250, 252, 255), 0.7)
        for t in range(1, 6):
            y = 80 - t * 7
            p.fill(p.m_line(ladder_x + (80 - y) * 0.2, y, ladder_x + 14 + (80 - y) * 0.2, y, 2), (150, 160, 175))
    # the rat's pipe: a wide tube mouth in the rock, red eyes inside
    cylinder_h(p, 270, 320, 6, 40, "#8a5a38")
    mouth = p.m_ell(262, 8, 292, 40)
    p.shade(mouth, "#a06a40", 1.4, 0.4, seed=16)
    p.edge(mouth, (0, 0, 0), 0.7)
    dark = p.m_ell(266, 12, 288, 36)
    p.fill(dark, (2, 2, 4))
    for ex in (271, 279):
        p.fill(p.m_rect(ex, 21, ex + 3, 24), (255, 60, 50))
        p.glow(ex + 1, 22, 9, (255, 60, 50), 0.6)
    weather(p, p.m_rect(262, 6, 320, 40), "#2a1a10", 0.5, 4, 8, 0.4)
    for i in range(16):
        x = int(p.rng.integers(250, 316))
        y = int(p.rng.integers(112, 140))
        facet_rock(p, [(x, y + 3), (x + 2, y), (x + 8, y + 1), (x + 9, y + 4)], "#6a5a50", seed=60 + i, facets=0, edge=0.4)
    return p


def rail_walk(motivator="floor"):
    """motivator: 'floor' (on its pedestal), 'gone', or 'installed' (in the ship's panel)"""
    p = Paint(base="#0a1430", seed=34)
    vgrad(p, 0, 112, [(0, "#060a1c"), (0.4, "#122050"), (1, "#2a4a8c")])
    p.multiply(0.8 + 0.4 * p.noise(20, 3, 6), 0.5)
    for x in range(14, W, 38):
        cylinder_v(p, x, x + 4, 0, 52 + (x * 5) % 24, "#c23838")
    for y in (7, 14, 21):
        cylinder_h(p, 0, W, y, y + 4, "#c040c0")
    # the magenta tower
    ground_shadow(p, 120, 232, 124, 6, 0.3, 3.0)
    drum = p.m_poly([(138, 0), (206, 0), (214, 30), (210, 114), (134, 114), (128, 30)])
    n = np.clip((p.xx - 128) / 86, 0, 1)
    p.fill(drum, np.clip(np.asarray(rgb("#d048d8")) * (1.5 - 1.25 * n)[..., None], 0, 255))
    p.edge(drum, (0, 0, 0), 0.6)
    for y in (30, 58, 86):
        p.fill(p.m_rect(128, y, 214, y + 3), (0, 0, 0), 0.3)
        p.fill(p.m_rect(128, y - 1, 214, y), (255, 200, 255), 0.25)
    box(p, 148, 14, 50, 26, 3, 2, "#2a1a34", seed=18)
    p.fill(p.m_rect(151, 17, 195, 38), p.lin(0, 17, 0, 38, "#0a0a18", "#1a1a34"))
    for x in (156, 168, 180):
        p.fill(p.m_rect(x, 21, x + 8, 34), (240, 240, 250))
    p.glow(171, 27, 40, (255, 255, 255), 0.12)
    # the blue garbage chute at the left end of the rail
    cylinder_v(p, 0, 30, 54, 96, "#2a52d8")
    mouth = p.m_ell(-8, 56, 30, 94)
    p.fill(mouth, p.radial(10, 75, 22, "#02060e", "#0a1a50", 1.2))
    p.edge(mouth, (150, 190, 255), 0.5, "top")
    p.glow(12, 75, 30, (60, 110, 220), 0.25)
    # the glossy rail and the lattice beneath it
    cylinder_h(p, 0, W, 75, 81, "#5ad8e0")
    for x in range(0, W, 20):
        p.fill(p.m_line(x, 82, x + 10, 134, 2), (60, 92, 200), 0.95)
        p.fill(p.m_line(x + 10, 82, x, 134, 2), (44, 76, 184), 0.95)
        p.fill(p.m_line(x - 1, 82, x + 9, 134, 1), (170, 200, 255), 0.4)
    p.fill(p.m_rect(0, 130, W, H), p.lin(0, 130, 0, H, "#0a1020", "#02040a"))
    p.fill(p.m_rect(0, 130, W, 132), (120, 150, 230), 0.5)
    # the pedestal with the warp motivator
    soft_shadow(p, [(22, 124), (58, 124), (66, 134), (26, 136)], 0.55, 2.5)
    box(p, 26, 112, 26, 16, 5, 3, "#6a7486", seed=50)
    if motivator == "floor":
        cylinder_v(p, 31, 45, 94, 112, "#c8d8c0")
        for yy in (98, 104, 110):
            p.fill(p.m_rect(31, yy, 45, yy + 1), (30, 70, 30), 0.6)
        sphere(p, 38, 92, 7, "#a8ff8a", spec=0.9, tint=(120, 255, 90))
        p.glow(38, 100, 36, (110, 255, 90), 0.5)
    # the Mallard's back end with its open maintenance panel
    mallard(p, 236, 98, 0.5, lit=True, ramp=False)
    pan = p.m_rect(266, 102, 300, 112)
    p.fill(pan, (4, 6, 10))
    if motivator == "installed":
        sphere(p, 283, 107, 6, "#a8ff8a", squash=0.7, spec=0.9, tint=(120, 255, 90))
        p.glow(283, 107, 30, (110, 255, 90), 0.5)
    else:
        for x in range(268, 298, 6):
            p.fill(p.m_line(x, 103, x + 3, 111, 1), (255, 150, 60), 0.9)
        p.fill(p.m_poly([(266, 102), (300, 102), (304, 94), (270, 94)]), (150, 160, 176))   # the panel lid, hinged open
    p.glow(171, 80, 160, (180, 255, 250), 0.16, 0.2)
    return p


def crane_cabin():
    p = Paint(base="#04060a", seed=35)
    vgrad(p, 0, H, [(0, "#0a0e18"), (1, "#05070c")])
    p.fill(p.m_rect(18, 12, 302, 56), p.lin(0, 12, 0, 56, "#020308", "#08241a"))
    p.fill(p.m_ell(100, 36, 220, 70), p.radial(160, 56, 62, "#caff9a", "#0a3a14", 0.35))
    p.glow(160, 56, 140, (90, 255, 70), 0.4, 0.5)
    for x in range(18, 302, 56):
        cylinder_v(p, x, x + 4, 12, 56, "#5a6676")
    box(p, 14, 6, 292, 6, 0, 0, "#7a8494", seed=21)
    box(p, 14, 56, 292, 6, 0, 3, "#3a4252", seed=22)
    # control desk: a heavy console with a visible top surface
    soft_shadow(p, [(0, 138), (320, 138), (320, 144), (0, 144)], 0.4, 3)
    topp = p.m_poly([(0, 94), (320, 94), (306, 84), (14, 84)])
    p.shade(topp, "#5a6478", 1.35, 0.8, angle=(0, -1), tex=0.1, seed=23)
    p.edge(topp, (255, 255, 255), 0.35, "top")
    front = p.m_poly([(0, H), (0, 94), (320, 94), (320, H)])
    p.shade(front, "#2e3646", 1.1, 0.5, angle=(0, -1), tex=0.1, seed=24)
    p.fill(p.m_rect(0, 94, W, 95), (255, 255, 255), 0.4)
    for x in range(20, 320, 54):
        p.fill(p.m_rect(x, 100, x + 1, 138), (0, 0, 0), 0.5)
        p.fill(p.m_rect(x + 1, 100, x + 2, 138), (255, 255, 255), 0.12)
    # CRT: a deep box with a recessed screen and a stand
    soft_shadow(p, [(60, 84), (162, 84), (170, 92), (66, 92)], 0.5, 2.0)
    box(p, 56, 56, 92, 28, 8, 5, "#7a8494", seed=25, tex=0.06)
    p.fill(p.m_rect(63, 62, 141, 80), p.lin(0, 62, 0, 80, "#0e3a1c", "#04140a"))
    for x in range(67, 141, 9):
        p.fill(p.m_line(x, 62, x, 80, 1), (60, 220, 100), 0.7)
    for y in range(64, 80, 6):
        p.fill(p.m_line(63, y, 141, y, 1), (60, 220, 100), 0.7)
    p.fill(p.m_rect(99, 69, 107, 72), (255, 255, 255))
    p.fill(p.m_rect(63, 62, 141, 63), (0, 0, 0), 0.6)
    p.glow(102, 71, 80, (80, 255, 120), 0.25)
    cylinder_v(p, 94, 108, 84, 90, "#5a6474")
    # joystick: base, shaft, ball, and a red button dome
    box(p, 186, 86, 16, 8, 3, 2, "#8a94a6", seed=26)
    cylinder_v(p, 192, 196, 66, 86, "#d0d8e4")
    sphere(p, 194, 62, 7, "#ff6a5a", spec=0.9, tint=(255, 100, 80))
    soft_shadow(p, [(218, 90), (250, 90), (254, 96), (222, 96)], 0.4, 1.5)
    box(p, 218, 90, 32, 5, 3, 2, "#6a7486", seed=27)
    sphere(p, 234, 90, 11, "#ff5a4a", squash=0.45, spec=0.9, tint=(255, 90, 70), clip=(p.yy <= 92))
    p.glow(234, 91, 28, (255, 70, 60), 0.3)
    # pilot's seat: a padded shell with a cushion
    soft_shadow(p, [(250, 130), (316, 130), (320, 144), (252, 144)], 0.5, 3.0)
    box(p, 250, 70, 46, 56, 8, 5, "#8a2a90", seed=28, tex=0.1)            # backrest
    box(p, 252, 104, 62, 18, 8, 5, "#b85ac0", seed=29, tex=0.1)           # seat cushion
    box(p, 256, 76, 34, 22, 3, 2, "#a040a8", seed=30, tex=0.1)            # padded panel
    p.glow(160, 60, 160, (90, 255, 70), 0.12, 0.5)
    return p


def cockpit():
    p = Paint(base="#1a0a2a", seed=37)
    p.fill(p.m_poly([(0, 0), (W, 0), (264, 42), (56, 42)]), p.lin(0, 0, 0, 42, "#4a1a6a", "#7a3aa0"))
    p.fill(p.m_poly([(0, 0), (56, 42), (56, 104), (0, H)]), p.lin(0, 0, 56, 0, "#1a0a2a", "#6a2a8a"))
    p.fill(p.m_poly([(W, 0), (264, 42), (264, 104), (W, H)]), p.lin(264, 0, W, 0, "#8a3ab0", "#2a1048"))
    for i in range(1, 6):
        t = i / 6
        for sgn in (1, -1):
            x = int(56 * t) if sgn == 1 else W - int(56 * t)
            p.fill(p.m_line(x, int(42 * t), x, int(104 + 40 * t), 2), (14, 4, 26), 0.8)
            p.fill(p.m_line(x + sgn, int(42 * t), x + sgn, int(104 + 40 * t), 1), (210, 150, 255), 0.18)
    p.fill(p.m_rect(56, 42, 264, 104), (2, 3, 10))
    p.stars(p.m_rect(56, 42, 264, 104), 90, seed=7)
    p.stars(p.m_rect(56, 42, 264, 104), 14, seed=8, bright=1.5)
    box(p, 54, 38, 212, 5, 0, 0, "#9a8cc0", seed=29)
    box(p, 54, 102, 212, 5, 0, 0, "#4a3a6a", seed=30)
    p.fill(p.m_poly([(56, 104), (264, 104), (W, H), (0, H)]), p.lin(0, 104, 0, H, "#4a3a5a", "#14101e"))
    for i in range(-8, 9):
        p.fill(p.m_line(160 + i * 12, 105, 160 + i * 42, H, 2), (0, 0, 0), 0.55)
        p.fill(p.m_line(161 + i * 12, 105, 161 + i * 42, H, 1), (200, 190, 230), 0.12)
    for y in (112, 122, 134):
        p.fill(p.m_line(int(56 - (y - 104) * 1.8), y, int(264 + (y - 104) * 1.8), y, 1), (0, 0, 0), 0.5)
    # pilot's seat: shell, headrest, cushion, with a floor shadow
    soft_shadow(p, [(4, 124), (60, 124), (70, 138), (6, 140)], 0.55, 3.0)
    box(p, 6, 54, 40, 58, 7, 5, "#7a8498", seed=31)                       # backrest
    box(p, 12, 62, 28, 24, 3, 2, "#4a4e64", seed=33)                       # headrest pad
    box(p, 8, 108, 52, 16, 8, 5, "#5a5e74", seed=34)                       # seat cushion
    # navigation console: a sloped slab with a screen and lit buttons
    soft_shadow(p, [(258, 114), (316, 112), (320, 128), (262, 130)], 0.55, 3.0)
    box(p, 262, 58, 52, 56, 6, 4, "#7a8494", seed=32)
    p.fill(p.m_rect(268, 63, 310, 85), p.lin(0, 63, 0, 85, "#1a6a3a", "#042010"))
    p.fill(p.m_rect(268, 63, 310, 64), (0, 0, 0), 0.6)
    for i, c in enumerate([(255, 90, 80), (255, 210, 80), (100, 230, 130), (100, 200, 255)]):
        sphere(p, 273 + i * 10, 97, 3, c, spec=0.9, tint=c)
        p.glow(273 + i * 10, 97, 10, c, 0.3)
    p.glow(290, 74, 50, (80, 255, 140), 0.2)
    p.glow(160, 80, 150, (140, 150, 255), 0.15, 0.6)
    return p


def mallard_bay_v(ladder_on=False, reactor_on_floor=False, lit=True):
    from p_act1 import mallard_bay as _bay
    p = Paint(base="#05070f", seed=36)
    freighter_wall(p, 104)
    p.fill(p.m_rect(0, 104, W, H), p.lin(0, 104, 0, H, "#343c4c", "#0c1018"))
    p.multiply(0.7 + 0.6 * p.noise(8, 3, 3), 0.5)
    p.fill(p.m_rect(0, 104, W, 106), (190, 205, 225), 0.3)
    p.glow(172, 118, 120, (255, 200, 120), 0.12, 0.3)
    mallard(p, 62, 46, 1.0, lit=lit)
    if ladder_on:                                                # a ladder propped against the hull up to the hatch
        soft_shadow(p, [(204, 34), (222, 34), (232, 116), (214, 116)], 0.4, 2.0)
        for k in range(2):
            p.fill(p.m_line(204 + k * 14, 40, 218 + k * 14, 118, 3), (180, 190, 205))
            p.fill(p.m_line(203 + k * 14, 40, 217 + k * 14, 118, 1), (250, 252, 255), 0.7)
        for t in range(1, 11):
            y = 40 + t * 7
            xo = (y - 40) * 0.18
            p.fill(p.m_line(204 + xo, y, 218 + xo, y, 2), (150, 160, 175))
    if reactor_on_floor:
        ground_shadow(p, 236, 270, 124, 5, 0.5, 2.0)
        cylinder_v(p, 240, 262, 100, 124, "#7a9a8a")
        p.fill(p.m_ell(240, 96, 262, 104), p.radial(251, 100, 11, "#e8ffc0", "#2ac030", 0.5))
        sphere(p, 251, 98, 6, "#c8ff9a", squash=0.6, spec=0.9, tint=(120, 255, 90))
        p.glow(251, 106, 40, (80, 255, 60), 0.45)
    return p


def make_grabber_png(path):
    """the rail grabber as a transparent sprite (24x46): painted on black and on white, alpha recovered from the difference"""
    from PIL import Image
    imgs = []
    for bg in ((0, 0, 0), (255, 255, 255)):
        q = Paint(w=24, h=46, base=bg, seed=5)
        box(q, 2, 4, 20, 12, 3, 2, "#9aa4b4", seed=19)
        cylinder_v(q, 10, 14, 16, 34, "#c4ccd8")
        box(q, 3, 32, 18, 6, 3, 2, "#c04848", seed=20)
        for dx in (2, 17):
            q.fill(q.m_poly([(dx, 38), (dx + 4, 38), (dx + 2, 45)]), (210, 70, 70))
        imgs.append(q.a.copy())
    b, w = imgs
    alpha = np.clip(1 - (w - b).mean(axis=2) / 255.0, 0, 1)
    rgb_ = np.where(alpha[..., None] > 0.02, b / np.maximum(alpha[..., None], 1e-3), 0)
    out = np.dstack([np.clip(rgb_, 0, 255), alpha * 255]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(path)


ROOMS = {
    "robot_head": robot_head,
    "conveyor": conveyor,
    "rat_lair": lambda: rat_lair(True, True),
    "rat_lair_noreactor": lambda: rat_lair(False, True),
    "rat_lair_noladder": lambda: rat_lair(True, False),
    "rat_lair_empty": lambda: rat_lair(False, False),
    "rail_walk": lambda: rail_walk("floor"),
    "rail_walk_gone": lambda: rail_walk("gone"),
    "rail_walk_installed": lambda: rail_walk("installed"),
    "crane_cabin": crane_cabin,
    "cockpit": cockpit,
    "mallard_bay": lambda: mallard_bay_v(False, False),
    "mallard_bay_l": lambda: mallard_bay_v(True, False),
    "mallard_bay_r": lambda: mallard_bay_v(False, True),
    "mallard_bay_lr": lambda: mallard_bay_v(True, True),
}
