"""Act 3 (Monolith Burger) with solid objects."""
import numpy as np
from kit import *
from solid import *
from p_act3 import station_exterior as _flat_exterior


def station_exterior():
    p = Paint(base="#02030a", seed=51)
    vgrad(p, 0, H, [(0, "#02030c"), (0.6, "#0a0a28"), (1, "#18103a")])
    p.glow(250, 30, 120, (90, 70, 200), 0.25, 0.7)
    p.stars(p.m_rect(0, 0, W, H), 220, seed=2)
    p.stars(p.m_rect(0, 0, W, H), 30, seed=3, bright=1.6)
    sphere(p, 275, 30, 28, "#6a80ff", spec=0.4, tint=(120, 140, 255))
    cx = 158
    # bottom bun (a thick disc), patty slab, cheese, lettuce, top bun as a lit dome
    soft_shadow(p, [(cx - 84, 124), (cx + 84, 124), (cx + 70, 134), (cx - 70, 134)], 0.5, 4)
    bb = p.m_poly([(cx - 84, 108), (cx - 74, 122), (cx + 74, 122), (cx + 84, 108)])
    p.shade(bb, "#e0a050", 1.4, 0.4, angle=(0, -1), seed=3)
    p.edge(bb, (60, 20, 0), 0.6)
    p.fill(p.m_ell(cx - 84, 104, cx + 84, 114), (255, 220, 150), 0.35)
    patty = p.m_rect(cx - 92, 92, cx + 92, 108)
    p.shade(patty, "#7a3a1c", 1.4, 0.3, angle=(0, -1), tex=0.2, seed=4)
    p.edge(patty, (30, 8, 0), 0.6)
    p.fill(p.m_ell(cx - 92, 88, cx + 92, 98), (140, 70, 36), 0.7)
    for i in range(30):
        x = cx - 88 + i * 6
        sphere(p, x, 111, 2, "#ff5a6a", spec=0.9, tint=(255, 60, 70))
        p.glow(x, 111, 8, (255, 60, 70), 0.3)
    ch = p.m_poly([(cx - 96, 86), (cx + 96, 86), (cx + 84, 96), (cx + 40, 94), (cx + 30, 104), (cx + 20, 94), (cx - 90, 94)])
    p.shade(ch, "#ffe040", 1.4, 0.6, angle=(0, -1), seed=5)
    p.edge(ch, (80, 50, 0), 0.5)
    lt = p.m_poly([(cx - 98, 78), (cx + 98, 78), (cx + 96, 88), (cx - 96, 88)])
    p.shade(lt, "#4ade50", 1.4, 0.45, angle=(0, -1), seed=6)
    p.edge(lt, (0, 50, 10), 0.5)
    for x in range(cx - 96, cx + 96, 12):
        sphere(p, x + 6, 86, 7, "#58e060", squash=0.5, spec=0.3, clip=(p.yy > 82))
    dome(p, cx, 80, 94, 62, "#e8a040", spec=0.45)
    for i in range(34):
        x = cx - 64 + int(p.rng.integers(0, 128))
        y = 30 + int(p.rng.integers(0, 40))
        sphere(p, x, y, 2.5, "#fff2d0", squash=0.6, spec=0.7)
    p.glow(cx - 30, 36, 90, (255, 200, 120), 0.2, 0.6)
    # docking arm with a small Mallard
    box(p, 0, 94, 60, 6, 0, 0, "#8a96a8", seed=7)
    box(p, 56, 88, 12, 22, 3, 2, "#6a7486", seed=8)
    mallard(p, 4, 78, 0.28, lit=True, ramp=False)
    text(p, 84, 126, "MONOLITH BURGER", (255, 230, 80), 18)
    p.glow(156, 130, 80, (255, 230, 80), 0.2, 0.3)
    return p


def concourse():
    p = Paint(base="#f0ece0", seed=52)
    vgrad(p, 0, 102, [(0, "#e8f4ff"), (1, "#fff6e0")])
    for x in range(0, W, 40):
        p.fill(p.m_rect(x, 0, x + 18, 102), (230, 60, 60), 0.18)
    p.multiply(0.94 + 0.12 * p.noise(24, 2, 3), 0.4)
    p.fill(p.m_rect(0, 102, W, H), p.lin(0, 102, 0, H, "#d4d8e0", "#8a90a4"))
    for y in range(102, H, 10):
        p.fill(p.m_rect(0, y, W, y + 1), (90, 96, 112), 0.5)
    for x in range(-40, W + 40, 24):
        p.fill(p.m_line(x, 102, x - (x - 160) // 3, H, 1), (90, 96, 112), 0.4)
    p.fill(p.m_rect(0, 102, W, 104), (255, 255, 255), 0.5)
    box(p, 54, 8, 144, 40, 5, 3, "#2a2a38", seed=9)                                # menu board
    p.fill(p.m_rect(58, 12, 194, 44), p.lin(0, 12, 0, 44, "#1c1c28", "#0c0c14"))
    text(p, 60, 12, "1 MONOLITH BURGER", (255, 220, 80), 16)
    text(p, 60, 26, "7 FUN MEAL   1 BZ", (110, 255, 140), 16)
    p.glow(125, 28, 100, (255, 255, 200), 0.18, 0.5)
    # the bored clerk stands behind the counter, so he is painted first
    person(p, 218, 76, 40, "#6ad868", "#3a8a50", skin="#6ad868", seed=11, helmet="#fafafa")
    p.fill(p.m_line(214, 30, 210, 20, 1), (110, 226, 108))
    p.fill(p.m_line(224, 30, 228, 20, 1), (110, 226, 108))
    sphere(p, 210, 19, 2, "#a0ffa0", spec=0.8)
    sphere(p, 228, 19, 2, "#a0ffa0", spec=0.8)
    # the counter: real top surface, front panel, kick plate
    soft_shadow(p, [(50, 108), (262, 108), (276, 126), (56, 128)], 0.5, 3.5)
    box(p, 56, 66, 206, 40, 14, 8, "#d83a3a", seed=10, tex=0.06)
    p.fill(p.m_poly([(56, 66), (262, 66), (276, 58), (70, 58)]), (240, 244, 252), 0.55)
    p.fill(p.m_poly([(56, 66), (262, 66), (276, 58), (70, 58)]), p.lin(0, 58, 0, 66, "#ffffff", "#c8d0e0"), 0.8)
    p.fill(p.m_rect(56, 66, 262, 68), (255, 255, 255), 0.7)
    for x in range(70, 262, 34):
        p.fill(p.m_rect(x, 72, x + 1, 100), (0, 0, 0), 0.35)
    p.fill(p.m_rect(56, 100, 262, 106), (60, 64, 76))
    # stools: a seat disc with thickness on a pole and a base
    for x in (270, 298):
        soft_shadow(p, [(x - 4, 124), (x + 24, 124), (x + 28, 130), (x, 130)], 0.5, 1.5)
        cylinder_v(p, x + 9, x + 13, 98, 122, "#aab0c0")
        p.fill(p.m_ell(x + 1, 120, x + 21, 126), (70, 76, 92))
        s_top = p.m_ell(x, 88, x + 22, 98)
        p.shade(s_top, "#b050c0", 1.45, 0.5, seed=12)
        p.edge(s_top, (0, 0, 0), 0.5)
        p.fill(p.m_ell(x + 2, 89, x + 20, 95), (255, 200, 255), 0.25)
    # arcade cabinet at the far left, a real box with a side face and a sloped panel
    soft_shadow(p, [(0, 122), (56, 122), (66, 134), (4, 136)], 0.5, 3.0)
    box(p, 4, 50, 38, 72, 8, 5, "#2a52d8", seed=13)
    p.fill(p.m_rect(10, 58, 36, 84), (2, 3, 10))
    p.stars(p.m_rect(10, 58, 36, 84), 14, seed=4)
    p.glow(23, 71, 40, (120, 160, 255), 0.35)
    p.fill(p.m_poly([(4, 94), (42, 94), (46, 99), (8, 99)]), (60, 70, 100))
    sphere(p, 14, 96, 2.5, "#ff6a6a", spec=0.9)
    text(p, 6, 34, "ASTRO", (255, 90, 90), 14)
    text(p, 6, 44, "CHICKEN", (255, 90, 90), 14)
    return p


def arcade_corner():
    p = Paint(base="#08041a", seed=53)
    vgrad(p, 0, H, [(0, "#0a0620"), (0.7, "#1c0c3c"), (1, "#080414")])
    for x, y, c in [(30, 20, (255, 70, 140)), (290, 24, (70, 200, 255)), (60, 100, (255, 200, 60))]:
        p.glow(x, y, 60, c, 0.35)
    p.fill(p.m_rect(0, 112, W, H), p.lin(0, 112, 0, H, "#1a1430", "#05030c"))
    p.glow(160, 124, 120, (100, 140, 255), 0.18, 0.2)
    soft_shadow(p, [(84, 138), (252, 138), (262, 144), (90, 144)], 0.6, 4)
    # the cabinet: tall box with side panel, bezel-recessed screen, sloped control deck
    box(p, 96, 12, 120, 128, 14, 4, "#2a52d8", seed=14, tex=0.06)
    p.fill(p.m_rect(96, 12, 108, 140), (220, 56, 60), 0.9)
    p.fill(p.m_rect(204, 12, 216, 140), (190, 40, 50), 0.9)
    box(p, 114, 20, 92, 68, 3, 2, "#10162a", seed=15)
    p.fill(p.m_rect(118, 24, 202, 84), (2, 3, 10))
    p.stars(p.m_rect(118, 24, 202, 84), 60, seed=5)
    p.fill(p.m_rect(148, 72, 176, 78), (220, 80, 220))
    sphere(p, 162, 42, 7, "#ffe040", spec=0.8)
    p.fill(p.m_poly([(118, 24), (150, 24), (122, 56), (118, 56)]), (255, 255, 255), 0.07)
    p.glow(162, 52, 90, (150, 190, 255), 0.4)
    p.fill(p.m_poly([(104, 92), (214, 92), (222, 118), (96, 118)]), p.lin(0, 92, 0, 118, "#4a5470", "#242a40"))
    p.fill(p.m_line(104, 92, 214, 92, 1), (255, 255, 255), 0.5)
    sphere(p, 134, 104, 7, "#ff5a4a", spec=0.9, tint=(255, 90, 70))
    cylinder_v(p, 132, 136, 100, 108, "#c0c8d8")
    sphere(p, 168, 104, 3, "#6aff8a", spec=0.9)
    sphere(p, 184, 104, 3, "#6adfff", spec=0.9)
    text(p, 118, 1, "ASTRO CHICKEN", (255, 110, 150), 16)
    p.glow(162, 5, 50, (255, 110, 150), 0.3, 0.5)
    return p


ROOMS = {"monolith_exterior": station_exterior, "monolith_concourse": concourse, "arcade_corner": arcade_corner}
