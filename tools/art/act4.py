"""Act 4: Ortega. Black rock, red cliffs and lava glow, as in the original."""
from ega import *


def sky(c, h=46):
    c.vgrad(0, 0, W - 1, h, [R, R, LR, N])
    for x, y in [(30, 24), (150, 20), (260, 28)]:      # glowing lava cracks on the horizon
        c.line(x, y, x + 16, y - 4, Y)
        c.line(x + 16, y - 4, x + 28, y + 2, LR)


def far_ridge(c, y=40):
    pts = [(0, y + 14)]
    r = __import__("random").Random(11)
    x = 0
    while x < W:
        x += r.randint(14, 34)
        pts.append((x, y + r.randint(-10, 8)))
    pts += [(W, y + 20), (0, y + 20)]
    c.poly(pts, K)


def cliff(c, x0, x1, ytop, ybot):
    c.rect(x0, ytop, x1, ybot, R)
    c.drect(x0, ytop + 8, x1, ybot, R, K)
    for x in range(x0, x1, 7):
        c.line(x, ytop + 4, x - 2, ybot, K)


def platform(c, pts, hi=DG):
    c.poly(pts, K)
    c.dpoly(pts, K, hi)


def crater():
    c = Cv()
    sky(c)
    far_ridge(c)
    c.rect(0, 60, W - 1, H - 1, R)
    cliff(c, 0, W - 1, 60, 132)
    platform(c, [(0, 70), (120, 62), (320, 66), (320, 90), (200, 100), (0, 96)], S)
    c.poly([(150, 90), (200, 100), (220, 132), (150, 132)], K)           # lava pit
    c.dpoly([(150, 90), (200, 100), (220, 132), (150, 132)], R, LR)
    for i in range(18):
        c.px(c.rng.randint(152, 214), c.rng.randint(96, 130), Y)
    c.poly([(16, 56), (56, 50), (66, 62), (20, 66)], S)                  # the Mallard on the rim
    c.poly([(48, 52), (60, 54), (60, 60), (46, 58)], LC)
    c.text(0, 0, "", K)
    return c


def bridge():
    c = Cv()
    sky(c, 40)
    far_ridge(c, 36)
    c.rect(0, 52, W - 1, H - 1, K)
    cliff(c, 0, 90, 52, 132)
    cliff(c, 230, 320, 52, 132)
    platform(c, [(0, 60), (92, 60), (92, 80), (0, 84)], DG)
    platform(c, [(228, 60), (320, 60), (320, 84), (228, 80)], DG)
    c.dpoly([(92, 100), (228, 100), (230, 132), (90, 132)], R, LR)       # lava far below
    for i in range(40):
        c.px(c.rng.randint(94, 226), c.rng.randint(102, 130), Y)
    for x in range(94, 228, 10):                                          # shaky rope bridge planks
        c.rect(x, 66 + abs(x - 160) // 14 - 8, x + 6, 70 + abs(x - 160) // 14 - 8, N)
    c.line(92, 60, 228, 60, S)
    c.line(92, 60, 160, 78, S)
    c.line(160, 78, 228, 60, S)
    return c


def station(detonator=True):
    c = Cv()
    sky(c, 40)
    far_ridge(c, 36)
    c.rect(0, 50, W - 1, H - 1, K)
    for i in range(14):                                                    # black boulders
        x, y = c.rng.randint(0, 300), c.rng.randint(54, 100)
        w = c.rng.randint(20, 46)
        c.ell(x, y, x + w, y + w // 2 + 8, K)
        c.dell(x + 3, y + 2, x + w - 6, y + w // 2, DG, K)
        c.line(x + 4, y + 4, x + w // 2, y + 8, R)
    c.rect(0, 108, W - 1, H - 1, DG)
    c.drect(0, 108, W - 1, H - 1, DG, K)
    c.line(0, 112, 120, 124, LR)
    # telescope on a tripod
    c.line(60, 88, 70, 112, S)
    c.line(80, 88, 70, 112, S)
    c.rect(58, 78, 84, 84, S)
    c.rect(82, 76, 86, 86, WH)
    # green crate
    if detonator:
        c.box3d(190, 92, 214, 112, LG, WH, G)
        c.rect(198, 98, 206, 104, K)
    # anemometer (wind meter)
    c.rect(260, 60, 262, 112, S)
    for dx in (-10, 10):
        c.line(261, 62, 261 + dx, 66, WH)
        c.ell(261 + dx - 2, 64, 261 + dx + 2, 68, WH)
    # two researchers in blue
    for x in (124, 144):
        c.rect(x, 80, x + 8, 98, B)
        c.rect(x + 1, 74, x + 7, 80, LR)
    return c


def dome(shield=True):
    c = Cv()
    sky(c, 40)
    far_ridge(c, 36)
    c.rect(0, 56, W - 1, H - 1, K)
    cliff(c, 0, W - 1, 100, 132)
    platform(c, [(0, 70), (320, 68), (320, 104), (0, 104)], DG)
    c.ell(120, 50, 230, 120, S)                                           # silver research dome
    c.dell(124, 54, 226, 108, S, WH)
    c.rect(120, 86, 230, 106, S)
    c.rect(168, 94, 184, 106, K)
    c.poly([(60, 40), (100, 30), (96, 74), (64, 74)], S)                  # satellite dish
    c.dpoly([(60, 40), (100, 30), (96, 74), (64, 74)], S, WH)
    c.line(80, 74, 80, 96, DG)
    if shield:                                                            # blue defensive force field
        for x in range(40, 261, 4):
            for y in range(20, 105, 4):
                c.px(x + (y // 4 % 2) * 2, y, LB)
        for x in range(40, 261, 20):
            c.line(x, 20, x, 104, B)
        c.line(40, 20, 260, 20, LC)
        c.line(40, 104, 260, 104, LC)
        c.line(40, 20, 40, 104, LC)
        c.line(260, 20, 260, 104, LC)
    return c


def ridge():
    c = Cv()
    sky(c, 44)
    far_ridge(c, 40)
    c.rect(0, 60, W - 1, H - 1, K)
    cliff(c, 0, W - 1, 104, 132)
    platform(c, [(0, 72), (320, 70), (320, 108), (0, 108)], DG)
    c.dell(90, 84, 230, 112, LR, R)                                       # smoking crater
    for i in range(7):
        c.dell(120 + i * 12, 40 - i * 4, 140 + i * 12, 80 - i * 4, DG, K)
    for x in range(110, 220, 14):
        c.line(x, 96, x + 8, 86, S)
    c.rect(168, 94, 190, 97, WH)                                          # the sparkling generator pole
    c.px(166, 92, WH)
    c.px(192, 92, WH)
    return c


ROOMS = {
    "ortega_crater": crater,
    "ortega_bridge": bridge,
    "ortega_station": station,
    "ortega_dome": dome,
    "ortega_ridge": ridge,
}
