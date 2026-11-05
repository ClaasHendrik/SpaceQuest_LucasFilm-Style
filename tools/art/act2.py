"""Act 2: Phleebhut. Magenta ground, green rock arches, black ridges, as in the original."""
from ega import *


def sky(c, h=70):
    c.vgrad(0, 0, W - 1, h, [C, C, LC, LC, WH])


def ridge(c, y, col=K, seed=3):
    r = __import__("random").Random(seed)
    pts = [(0, y + 20)]
    x = 0
    while x < W:
        x += r.randint(10, 26)
        pts.append((x, y + r.randint(-12, 6)))
    pts += [(W, y + 24), (W, y + 30), (0, y + 30)]
    c.poly(pts, col)


def ground(c, y):
    c.rect(0, y, W - 1, H - 1, M)
    c.drect(0, y, W - 1, y + 20, M, LM)
    c.drect(0, y + 40, W - 1, H - 1, M, B)
    for _ in range(40):
        x, yy = c.rng.randint(0, W), c.rng.randint(y + 4, H - 2)
        c.rect(x, yy, x + c.rng.randint(2, 7), yy, c.rng.choice([LM, B, M]))


def arch(c, x, y, w, h, col=G, hi=LG):
    c.poly([(x, y + h), (x + w // 6, y + h // 3), (x + w // 2, y), (x + 5 * w // 6, y + h // 3), (x + w, y + h),
            (x + 3 * w // 4, y + h), (x + w // 2, y + h // 3), (x + w // 4, y + h)], col)
    c.dpoly([(x + w // 4, y + h // 3), (x + w // 2, y + 2), (x + 3 * w // 4, y + h // 3), (x + w // 2, y + h // 3 + 6)], col, hi)


def spire(c, x, y, h, w=14):
    c.poly([(x, y + h), (x + w // 2, y), (x + w, y + h)], G)
    c.dpoly([(x, y + h), (x + w // 2, y), (x + w // 2, y + h)], G, LG)


def landing_strip():
    c = Cv()
    sky(c, 64)
    ridge(c, 44, K, 3)
    ridge(c, 52, DG, 8)
    ground(c, 66)
    arch(c, 150, 38, 100, 54)
    arch(c, 250, 52, 66, 42, G, LG)
    spire(c, 100, 54, 40)
    spire(c, 124, 62, 28, 10)
    # the Aluminum Mallard, landed
    c.poly([(16, 106), (24, 90), (68, 86), (96, 94), (98, 106)], S)
    c.dpoly([(16, 106), (24, 90), (68, 86), (96, 94), (98, 106)], S, DG)
    c.poly([(78, 90), (92, 94), (92, 100), (76, 98)], LC)
    c.rect(24, 106, 30, 112, DG)
    c.rect(86, 106, 92, 112, DG)
    c.poly([(48, 106), (64, 106), (70, 118), (42, 118)], DG)
    c.text(0, 124, "", K)
    return c


def claw(c, x, flip=False):
    sgn = -1 if flip else 1
    c.poly([(x, 0), (x + 56 * sgn, 0), (x + 60 * sgn, 70), (x + 40 * sgn, 100), (x, 100)], C)
    c.dpoly([(x, 0), (x + 56 * sgn, 0), (x + 60 * sgn, 70), (x + 40 * sgn, 100), (x, 100)], C, LC)
    for i, yy in enumerate((40, 62, 84)):             # scaly bands
        c.line(x, yy, x + 56 * sgn, yy + 4, B)
    for i in range(3):                                # three yellow-green talons
        tx = x + (40 + i * 6) * sgn
        c.poly([(tx, 96), (tx + 8 * sgn, 96), (tx + 4 * sgn, 124)], Y)
        c.dpoly([(tx, 96), (tx + 8 * sgn, 96), (tx + 4 * sgn, 124)], Y, LG)


def world_o_wonders():
    c = Cv()
    sky(c, 40)
    c.rect(0, 60, W - 1, H - 1, M)
    ground(c, 96)
    c.rect(0, 40, W - 1, 96, B)
    c.drect(0, 40, W - 1, 96, B, K)
    claw(c, 0)
    claw(c, 319, True)
    # sign
    c.rect(86, 10, 236, 48, K)
    c.rect(88, 12, 234, 46, B)
    c.text(94, 14, "WORLD O'", LG, 16)
    c.text(112, 28, "WONDERS", LG, 16)
    # shop front
    c.box3d(70, 62, 250, 98, DG, S, K)
    c.poly([(60, 62), (260, 62), (270, 76), (50, 76)], R)
    c.dpoly([(60, 62), (260, 62), (270, 76), (50, 76)], R, DG)
    c.rect(130, 76, 190, 98, K)                       # doorway
    c.rect(76, 82, 120, 96, LC)                       # shop window
    c.rect(200, 82, 244, 96, LC)
    c.rect(210, 104, 236, 112, N)                     # little table
    c.rect(214, 112, 216, 120, N)
    c.rect(230, 112, 232, 120, N)
    return c


def canyon():
    c = Cv()
    sky(c, 40)
    ridge(c, 20, K, 5)
    # left and right cliffs
    c.poly([(0, 0), (90, 0), (70, 40), (84, 90), (50, 132), (0, 132)], M)
    c.dpoly([(0, 0), (90, 0), (70, 40), (84, 90), (50, 132), (0, 132)], M, K)
    c.poly([(230, 0), (320, 0), (320, 132), (270, 132), (250, 80), (240, 40)], M)
    c.dpoly([(230, 0), (320, 0), (320, 132), (270, 132), (250, 80), (240, 40)], M, LM)
    c.poly([(84, 70), (240, 70), (270, 132), (50, 132)], N)
    c.dpoly([(84, 70), (240, 70), (270, 132), (50, 132)], N, Y)
    c.line(0, 0, 0, 0, K)
    arch(c, 96, 30, 90, 46)
    spire(c, 200, 40, 36)
    for x in (130, 170, 210):
        c.rect(x, 90 + (x % 5), x + 8, 94 + (x % 5), DG)
    return c


def stalk_ridge(grabbed=False):
    c = Cv()
    sky(c, 50)
    c.rect(0, 50, W - 1, H - 1, M)
    c.vgrad(0, 50, W - 1, H - 1, [M, M, B, K])
    # cliff shelf at the top with the stalk plant
    c.poly([(0, 0), (320, 0), (320, 40), (250, 34), (180, 44), (100, 30), (0, 38)], N)
    c.dpoly([(0, 0), (320, 0), (320, 40), (250, 34), (180, 44), (100, 30), (0, 38)], N, R)
    c.rect(150, 38, 162, 70, G)                       # plant stalk
    c.dpoly([(150, 38), (162, 38), (166, 70), (146, 70)], G, LG)
    for i in range(5):                                # dangling tendrils
        x = 140 + i * 11
        c.line(x, 66, x + (i - 2) * 3, 92, LM, 2)
    for i in range(3):                                # pulsating pods
        c.ell(120 + i * 40, 64, 134 + i * 40, 84, M)
        c.dell(122 + i * 40, 66, 132 + i * 40, 80, LM, M)
    # mountain trail
    c.poly([(0, 132), (60, 108), (140, 100), (320, 118), (320, 132)], DG)
    c.dpoly([(0, 132), (60, 108), (140, 100), (320, 118), (320, 132)], DG, S)
    return c


ROOMS = {
    "landing_strip": landing_strip,
    "world_o_wonders": world_o_wonders,
    "canyon": canyon,
    "stalk_ridge": stalk_ridge,
}
