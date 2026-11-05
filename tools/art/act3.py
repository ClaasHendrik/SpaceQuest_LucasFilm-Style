"""Act 3: Monolith Burger. A space station shaped like a hamburger, and its fast-food interior."""
from ega import *


def station_exterior():
    c = Cv()
    c.stars(0, 0, W - 1, H - 1, 140)
    c.ell(250, 8, 296, 40, B)
    c.dell(254, 12, 292, 36, B, LB)
    cx = 150
    # top bun
    c.ell(cx - 90, 20, cx + 90, 78, N)
    c.rect(cx - 90, 52, cx + 90, 56, N)
    c.dell(cx - 82, 24, cx + 82, 56, N, Y)
    for i in range(30):                              # neon sesame seeds
        x = cx - 70 + c.rng.randint(0, 140)
        y = 28 + c.rng.randint(0, 22)
        c.rect(x, y, x + 3, y + 1, WH)
    # lettuce, cheese, patty, bun
    c.rect(cx - 96, 56, cx + 96, 62, LG)
    c.dpoly([(cx - 96, 62), (cx + 96, 62), (cx + 80, 68), (cx - 80, 68)], Y, WH)
    c.rect(cx - 92, 68, cx + 92, 80, R)
    c.drect(cx - 92, 68, cx + 92, 80, N, R)
    for i in range(24):                              # blinking red neon ketchup ring
        c.rect(cx - 92 + i * 8, 82, cx - 88 + i * 8, 84, LR)
    c.rect(cx - 86, 86, cx + 86, 100, N)
    c.drect(cx - 86, 86, cx + 86, 100, N, Y)
    c.rect(cx - 70, 100, cx + 70, 106, N)
    # docking arm and the Mallard
    c.rect(0, 66, 56, 70, S)
    c.rect(52, 62, 62, 76, DG)
    c.poly([(8, 76), (14, 66), (40, 64), (54, 70), (54, 78)], S)
    c.poly([(40, 66), (50, 70), (50, 74), (38, 72)], LC)
    c.text(112, 108, "MONOLITH BURGER", Y, 8)
    return c


def concourse():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, WH)
    c.vgrad(0, 0, W - 1, 80, [LC, WH])
    c.rect(0, 84, W - 1, H - 1, S)
    for y in range(84, H, 8):                         # tile floor
        c.line(0, y, W - 1, y, DG)
    for x in range(0, W, 16):
        c.line(x, 84, x - 10, H - 1, DG)
    # menu board
    c.box3d(70, 8, 250, 40, K, DG, K)
    c.text(76, 12, "1 MONOLITH BURGER", Y, 8)
    c.text(76, 22, "7 FUN MEAL  1.00 BZ", LG, 8)
    c.rect(226, 14, 246, 34, R)
    c.rect(229, 18, 243, 30, Y)
    # counter with a bored clerk
    c.box3d(60, 54, 250, 92, R, LR, N)
    c.drect(60, 54, 250, 92, R, N)
    c.rect(60, 54, 250, 58, WH)
    c.rect(200, 30, 224, 54, LG)                      # clerk, antennae and paper hat
    c.rect(204, 22, 220, 32, WH)
    c.line(206, 22, 202, 14, LG)
    c.line(218, 22, 222, 14, LG)
    # tables (right) and plastic booth
    for x in (262, 290):
        c.rect(x, 78, x + 20, 82, M)
        c.rect(x + 8, 82, x + 12, 108, DG)
        c.rect(x, 108, x + 20, 110, DG)
    # arcade cabinet at the far left
    c.box3d(6, 44, 40, 104, B, LB, K)
    c.rect(12, 52, 34, 74, K)
    c.stars(13, 53, 33, 73, 10)
    c.rect(12, 84, 34, 90, R)
    c.text(10, 28, "ASTRO", LR, 8)
    c.text(10, 36, "CHICKEN", LR, 8)
    return c


def arcade_corner():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, K)
    c.vgrad(0, 0, W - 1, 100, [K, B])
    c.drect(0, 100, W - 1, H - 1, DG, K)
    c.box3d(100, 6, 220, 112, B, LB, K)               # cabinet
    c.rect(100, 6, 108, 112, R)
    c.rect(212, 6, 220, 112, R)
    c.box3d(114, 14, 206, 74, K, DG, K)               # screen
    c.stars(116, 16, 204, 72, 40)
    c.rect(148, 62, 170, 70, M)                       # trampoline pad
    c.poly([(158, 28), (164, 32), (160, 40), (154, 36)], Y)   # chicken
    c.rect(116, 84, 204, 100, DG)
    c.ell(130, 88, 142, 98, R)                        # joystick and buttons
    c.rect(170, 90, 176, 94, LG)
    c.rect(182, 90, 188, 94, LC)
    c.text(122, 2, "ASTRO CHICKEN", LR, 8)
    return c


def astro_chicken_screen():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, B)
    c.rect(0, 0, 8, H - 1, R)
    c.rect(W - 9, 0, W - 1, H - 1, R)
    c.rect(0, 0, W - 1, 6, G)
    c.box3d(24, 10, 296, 106, K, DG, K)
    c.stars(26, 12, 294, 104, 70)
    c.rect(24, 96, 296, 106, S)
    for x in range(40, 290, 22):                      # green domes on the ground
        c.ell(x, 96, x + 14, 104, LG)
    c.rect(130, 90, 190, 96, M)
    c.rect(126, 96, 194, 98, LM)
    c.rect(20, 114, 96, 128, K)
    c.text(24, 114, "FEED: 54", WH, 8)
    c.text(120, 118, "PRESS F5 TO EXIT", WH, 8)
    return c


ROOMS = {
    "monolith_exterior": station_exterior,
    "monolith_concourse": concourse,
    "arcade_corner": arcade_corner,
    "astro_chicken": astro_chicken_screen,
}
