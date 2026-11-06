"""Act 3: Monolith Burger. A space station shaped like a hamburger, and a bright plastic fast-food interior."""
import numpy as np
from kit import *


def station_exterior():
    p = Paint(base="#02030a", seed=51)
    vgrad(p, 0, H, [(0, "#02030c"), (0.6, "#0a0a28"), (1, "#18103a")])
    p.glow(250, 30, 120, (90, 70, 200), 0.25, 0.7)
    p.stars(p.m_rect(0, 0, W, H), 220, seed=2)
    p.stars(p.m_rect(0, 0, W, H), 30, seed=3, bright=1.6)
    pl = p.m_ell(246, 6, 304, 56)
    p.fill(pl, p.radial(262, 20, 44, "#8a9cff", "#101a60"))
    cx = 156
    # bottom bun
    bb = p.m_poly([(cx - 78, 108), (cx - 70, 120), (cx + 70, 120), (cx + 78, 108)])
    p.shade(bb, "#e0a050", 1.4, 0.4, angle=(0, -1), seed=3)
    p.edge(bb, (60, 20, 0), 0.6)
    # patty
    patty = p.m_rect(cx - 90, 92, cx + 90, 108)
    p.shade(patty, "#7a3a1c", 1.4, 0.3, angle=(0, -1), tex=0.2, seed=4)
    p.edge(patty, (30, 8, 0), 0.6)
    # neon ketchup ring
    for i in range(30):
        x = cx - 88 + i * 6
        p.fill(p.m_rect(x, 110, x + 3, 112), (255, 60, 70))
        p.glow(x + 1, 111, 8, (255, 60, 70), 0.35)
    # cheese
    ch = p.m_poly([(cx - 96, 86), (cx + 96, 86), (cx + 84, 96), (cx + 40, 94), (cx + 30, 104), (cx + 20, 94), (cx - 90, 94)])
    p.shade(ch, "#ffe040", 1.4, 0.6, angle=(0, -1), seed=5)
    p.edge(ch, (80, 50, 0), 0.5)
    # lettuce
    lt = p.m_poly([(cx - 98, 78), (cx + 98, 78), (cx + 96, 86), (cx - 96, 86)])
    p.shade(lt, "#4ade50", 1.4, 0.45, angle=(0, -1), seed=6)
    p.edge(lt, (0, 50, 10), 0.5)
    for x in range(cx - 96, cx + 96, 12):
        p.fill(p.m_ell(x, 82, x + 12, 90), (60, 200, 70), 0.9)
    # top bun
    tb = p.m_ell(cx - 92, 20, cx + 92, 86)
    p.shade(tb, "#e8a040", 1.5, 0.3, angle=(-1, -1), tex=0.1, seed=7)
    p.fill(p.m_rect(cx - 92, 70, cx + 92, 80), (0, 0, 0), 0.0)
    p.edge(tb, (70, 24, 0), 0.5)
    p.fill(p.m_rect(cx - 96, 74, cx + 96, 78), (0, 0, 0), 0.0)
    for i in range(34):                                            # glowing sesame seeds
        x = cx - 68 + int(p.rng.integers(0, 136))
        y = 28 + int(p.rng.integers(0, 40))
        p.fill(p.m_ell(x, y, x + 5, y + 3), (255, 245, 210))
    p.glow(cx - 30, 36, 90, (255, 200, 120), 0.2, 0.6)
    # docking arm and the Mallard
    p.fill(p.m_rect(0, 96, 60, 102), (120, 130, 146))
    p.fill(p.m_rect(56, 90, 68, 108), (90, 98, 112))
    hull = [(6, 100), (14, 88), (40, 85), (56, 92), (56, 102)]
    m = shaded(p, hull, "#aab4c2", 1.45, 0.35, seed=8, tex=0.1)
    p.fill(p.m_poly([(40, 88), (52, 92), (52, 98), (38, 96)]), (160, 240, 255))
    text(p, 84, 124, "MONOLITH BURGER", (255, 230, 80), 18)
    p.glow(156, 128, 80, (255, 230, 80), 0.2, 0.3)
    return p


def concourse():
    p = Paint(base="#f0ece0", seed=52)
    vgrad(p, 0, 102, [(0, "#e8f4ff"), (1, "#fff6e0")])
    for x in range(0, W, 40):                                    # red wall stripes
        p.fill(p.m_rect(x, 0, x + 18, 102), (230, 60, 60), 0.18)
    p.multiply(0.94 + 0.12 * p.noise(24, 2, 3), 0.4)
    # tile floor with a glossy reflection
    p.fill(p.m_rect(0, 102, W, H), p.lin(0, 102, 0, H, "#d4d8e0", "#8a90a4"))
    for y in range(102, H, 10):
        p.fill(p.m_rect(0, y, W, y + 1), (90, 96, 112), 0.5)
    for x in range(-40, W + 40, 24):
        p.fill(p.m_line(x, 102, x - (x - 160) // 3, H, 1), (90, 96, 112), 0.4)
    p.fill(p.m_rect(0, 102, W, 104), (255, 255, 255), 0.5)
    # menu board
    board = p.m_rect(54, 10, 196, 46)
    p.fill(board, p.lin(0, 10, 0, 46, "#1c1c28", "#0c0c14"))
    p.edge(board, (200, 200, 210), 0.6, width=2)
    text(p, 60, 12, "1 MONOLITH BURGER", (255, 220, 80), 16)
    text(p, 60, 26, "7 FUN MEAL   1 BZ", (110, 255, 140), 16)
    p.glow(125, 28, 100, (255, 255, 200), 0.18, 0.5)
    # counter
    ct = p.m_rect(56, 62, 262, 104)
    p.shade(ct, "#d83a3a", 1.35, 0.5, angle=(0, -1), tex=0.08, seed=9)
    p.edge(ct, (60, 0, 0), 0.6)
    top = p.m_rect(54, 58, 264, 64)
    p.shade(top, "#e8ecf4", 1.4, 0.7, angle=(0, -1), seed=10)
    p.fill(p.m_rect(54, 58, 264, 59), (255, 255, 255), 0.8)
    # bored alien clerk
    cl = p.m_poly([(204, 62), (210, 40), (226, 40), (232, 62)])
    p.shade(cl, "#6ad868", 1.3, 0.5, seed=11)
    p.edge(cl, (0, 50, 0), 0.6)
    p.fill(p.m_ell(208, 24, 228, 42), (110, 226, 108))
    p.fill(p.m_rect(207, 18, 229, 28), (250, 250, 250))
    p.fill(p.m_line(210, 18, 206, 8, 1), (110, 226, 108))
    p.fill(p.m_line(226, 18, 230, 8, 1), (110, 226, 108))
    p.fill(p.m_rect(214, 31, 217, 33), (20, 20, 20))
    p.fill(p.m_rect(221, 31, 224, 33), (20, 20, 20))
    # booths and stools
    for x in (266, 296):
        t = p.m_ell(x, 90, x + 22, 98)
        p.shade(t, "#b050c0", 1.4, 0.5, seed=12)
        p.fill(p.m_rect(x + 9, 98, x + 13, 120), (110, 116, 130))
        p.fill(p.m_ell(x + 1, 120, x + 21, 124), (80, 86, 100))
        p.fill(p.m_ell(x - 2, 80, x + 24, 88), (230, 60, 60), 0.0)
    # arcade cabinet far left
    cab = p.m_poly([(4, 120), (6, 50), (44, 50), (46, 120)])
    p.shade(cab, "#2a52d8", 1.35, 0.4, angle=(-1, 0), seed=13)
    p.edge(cab, (0, 0, 40), 0.6)
    scr = p.m_rect(11, 58, 39, 82)
    p.fill(scr, (2, 3, 10))
    p.stars(scr, 14, seed=4)
    p.glow(25, 70, 40, (120, 160, 255), 0.35)
    p.fill(p.m_rect(11, 92, 39, 98), (230, 60, 60))
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
    cab = p.m_poly([(92, H), (100, 10), (222, 10), (230, H)])
    p.shade(cab, "#2a52d8", 1.4, 0.35, angle=(-1, 0), seed=14)
    p.edge(cab, (0, 0, 40), 0.6)
    p.fill(p.m_rect(100, 10, 112, H), (220, 56, 60), 0.9)
    p.fill(p.m_rect(210, 10, 222, H), (190, 40, 50), 0.9)
    scr = p.m_rect(118, 22, 204, 84)
    p.fill(scr, (2, 3, 10))
    p.stars(scr, 60, seed=5)
    p.fill(p.m_rect(148, 72, 176, 78), (220, 80, 220))
    chick = p.m_poly([(158, 34), (166, 38), (162, 48), (154, 44)])
    p.shade(chick, "#ffe040", 1.4, 0.6, seed=15)
    p.glow(162, 52, 90, (150, 190, 255), 0.4)
    panel = p.m_poly([(112, 92), (210, 92), (216, 116), (106, 116)])
    p.shade(panel, "#3a4258", 1.3, 0.5, angle=(0, -1), seed=16)
    p.fill(p.m_ell(128, 98, 142, 110), p.radial(135, 102, 7, "#ff8a7a", "#a01818"))
    p.fill(p.m_rect(166, 100, 174, 106), (110, 255, 140))
    p.fill(p.m_rect(182, 100, 190, 106), (110, 230, 255))
    text(p, 118, 1, "ASTRO CHICKEN", (255, 110, 150), 16)
    p.glow(162, 5, 50, (255, 110, 150), 0.3, 0.5)
    return p


def astro_chicken_screen():
    p = Paint(base="#08102a", seed=54)
    p.fill(p.m_rect(0, 0, 10, H), (200, 50, 56))
    p.fill(p.m_rect(W - 10, 0, W, H), (200, 50, 56))
    p.fill(p.m_rect(0, 0, W, 8), (40, 160, 70))
    p.fill(p.m_rect(10, 8, W - 10, H), p.lin(0, 8, 0, H, "#122a74", "#0a1440"))
    scr = p.m_rect(26, 12, 294, 112)
    p.fill(scr, (1, 2, 8))
    p.stars(scr, 120, seed=6)
    p.stars(scr, 16, seed=7, bright=1.6)
    p.fill(p.m_rect(26, 102, 294, 112), p.lin(0, 102, 0, 112, "#b8bcc8", "#6a7084"))
    for x in range(40, 290, 24):
        d = p.m_ell(x, 100, x + 16, 110)
        p.fill(d, p.radial(x + 8, 104, 8, "#a0ff90", "#1a8a30", 0.7))
    p.fill(p.m_rect(128, 94, 192, 102), p.lin(0, 94, 0, 102, "#ff80ff", "#901890"))
    text(p, 28, 118, "FEED: 54", (255, 255, 255), 16)
    text(p, 108, 124, "PRESS F5 TO EXIT", (255, 255, 255), 16)
    p.glow(160, 60, 150, (120, 150, 255), 0.1, 0.5)
    return p


ROOMS = {
    "monolith_exterior": station_exterior,
    "monolith_concourse": concourse,
    "arcade_corner": arcade_corner,
    "astro_chicken": astro_chicken_screen,
}
