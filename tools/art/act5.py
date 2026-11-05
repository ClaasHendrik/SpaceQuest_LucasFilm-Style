"""Act 5: Pestulon and ScumSoft. Magenta sky, green ground, grey bunkers; red cubicles on blue; the finale."""
from ega import *


def exterior():
    c = Cv()
    c.vgrad(0, 0, W - 1, 70, [M, M, LM, M])
    c.rect(0, 70, W - 1, H - 1, LG)
    c.drect(0, 70, W - 1, 80, LG, G)
    c.rect(0, 96, W - 1, H - 1, S)                                        # concrete apron
    c.drect(0, 96, W - 1, 104, S, DG)
    # radar dish
    c.poly([(70, 0), (110, 0), (122, 18), (84, 30), (60, 14)], M)
    c.dpoly([(70, 0), (110, 0), (122, 18), (84, 30), (60, 14)], M, LM)
    c.line(92, 30, 98, 50, DG, 2)
    # the grey bunker with a blue panel
    c.poly([(30, 96), (30, 60), (60, 44), (150, 44), (176, 60), (176, 96)], S)
    c.dpoly([(30, 96), (30, 60), (60, 44), (150, 44), (176, 60), (176, 96)], S, DG)
    c.rect(60, 60, 140, 96, DG)
    c.dpoly([(64, 62), (136, 62), (136, 94), (64, 94)], B, K)
    for y in range(66, 92, 6):
        c.line(70, y, 130, y, LR)
    c.poly([(186, 96), (186, 70), (210, 58), (250, 58), (270, 70), (270, 96)], S)  # second bunker
    c.rect(214, 74, 244, 96, K)
    c.rect(280, 84, 300, 120, DG)                                          # bollards
    c.rect(4, 100, 14, 126, DG)
    # ScumSoft sign
    c.rect(100, 36, 160, 46, K)
    c.text(104, 36, "SCUMSOFT", Y, 8)
    # the force field edge
    c.line(0, 70, W - 1, 70, LC)
    return c


def closet():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, DG)
    c.drect(0, 0, W - 1, 90, DG, K)
    c.rect(0, 94, W - 1, H - 1, S)
    for y in range(94, H, 8):
        c.line(0, y, W - 1, y, DG)
    c.box3d(20, 20, 120, 94, N, Y, R)                                      # shelving
    for y in (40, 62):
        c.rect(20, y, 120, y + 3, R)
    c.rect(30, 24, 50, 40, WH)                                             # boxes of toilet paper
    c.rect(60, 28, 80, 40, LC)
    c.rect(30, 46, 40, 62, LB)                                             # bottles
    c.rect(46, 50, 54, 62, LG)
    c.rect(150, 14, 154, 22, S)                                            # hook
    c.poly([(140, 22), (170, 22), (176, 72), (134, 72)], B)                # hanging coveralls
    c.rect(134, 22, 140, 52, B)
    c.rect(170, 22, 176, 52, B)
    c.text(144, 36, "SCUM", WH, 8)
    c.box3d(220, 40, 290, 94, S, WH, DG)                                   # locker with the vaporizer
    c.rect(246, 60, 262, 72, K)
    c.rect(210, 98, 232, 110, B)                                           # bucket
    return c


def cubicle_maze():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, B)
    c.drect(0, 0, W - 1, H - 1, B, LB, 1)
    for row in range(3):
        y = 4 + row * 40
        for col in range(5):
            x = 4 + col * 64
            c.box3d(x, y, x + 56, y + 30, R, LR, N)
            c.drect(x + 2, y + 14, x + 54, y + 30, R, N)
            c.rect(x + 22, y + 20, x + 36, y + 26, WH)                    # a drone at a desk
            c.rect(x + 26, y + 12, x + 32, y + 20, c.rng.choice([LM, LC, LG]))
    for x in (60, 124, 188, 252):                                          # full trash cans
        c.rect(x, 108, x + 8, 120, S)
        c.rect(x + 1, 104, x + 7, 108, WH)
    c.rect(0, 124, W - 1, H - 1, S)
    return c


def elmo_office(card=True, picture=True):
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, M)
    c.drect(0, 0, W - 1, 100, M, B)
    c.rect(0, 100, W - 1, H - 1, S)
    c.box3d(100, 70, 230, 100, N, Y, R)                                    # a very large desk
    c.rect(140, 56, 190, 70, DG)
    c.rect(144, 58, 186, 68, B)
    if card:
        c.rect(110, 72, 124, 78, WH)
        c.rect(112, 74, 122, 76, LC)
    if picture:
        c.box3d(130, 14, 190, 54, N, Y, R)
        c.rect(136, 20, 184, 48, K)
        c.rect(150, 26, 170, 44, LR)
        c.text(138, 50, "ELMO PUG", Y, 8)
    c.rect(250, 40, 290, 100, DG)                                          # copy machine
    c.rect(254, 44, 286, 56, S)
    return c


def cell_block():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, B)
    c.drect(0, 0, W - 1, H - 1, B, K)
    c.box3d(80, 10, 240, 100, B, LB, K)                                   # octagonal chamber
    c.rect(150, 22, 170, 52, R)
    c.text(155, 30, "6", WH, 16)
    for x in (112, 192):                                                  # green pods with the Two Guys
        c.box3d(x, 40, x + 30, 92, G, LG, K)
        c.rect(x + 6, 50, x + 24, 86, K)
        c.rect(x + 10, 54, x + 20, 62, LR)
        c.rect(x + 10, 62, x + 20, 82, B)
    c.poly([(100, 100), (220, 100), (250, 118), (70, 118)], LB)           # console
    c.rect(150, 104, 170, 110, Y)
    for x in range(20, 80, 8):
        c.line(x, 4, x + 4, 100, K)
    c.rect(0, 118, W - 1, H - 1, K)
    return c


def hangar():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, K)
    c.vgrad(0, 0, W - 1, 30, [K, B])
    c.rect(20, 34, 300, 100, LC)
    c.drect(20, 34, 300, 100, LC, WH)
    for x in range(30, 300, 40):
        c.rect(x, 34, x + 6, 62, C)
    c.ell(60, 80, 260, 110, LC)
    c.dell(70, 84, 250, 108, C, LC)
    c.rect(90, 50, 110, 96, R)                                            # two mech suits
    c.rect(86, 44, 114, 54, LR)
    c.rect(210, 56, 224, 96, S)
    c.rect(206, 50, 228, 58, DG)
    c.rect(0, 108, W - 1, H - 1, K)
    return c


def space_battle():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, K)
    c.stars(0, 0, W - 1, H - 1, 160)
    c.ell(60, 40, 220, 120, B)
    c.dell(64, 44, 216, 116, B, K)
    c.line(150, 66, 150, 98, LG)
    c.line(134, 82, 166, 82, LG)
    c.ell(142, 74, 158, 90, K)
    c.ell(142, 74, 158, 90, K)
    c.rect(250, 6, 310, 28, K)                                            # radar
    c.rect(250, 6, 310, 6, LG)
    c.rect(250, 28, 310, 28, LG)
    c.rect(280, 16, 282, 18, LR)
    c.text(4, 4, "SHIELD  F", LG, 8)
    c.rect(4, 14, 80, 18, LG)
    return c


def deep_space():
    c = Cv()
    c.stars(0, 0, W - 1, H - 1, 260, (WH, LB, B, LC, Y))
    for r, col in [(70, B), (54, LB), (38, M)]:
        c.dell(160 - r, 70 - r // 2, 160 + r, 70 + r // 2, col, K)
    c.dell(120, 56, 200, 84, WH, LC)
    c.text(94, 8, "THE END", LR, 16)
    c.text(76, 108, "Roger Wilco will return.", LG, 8)
    return c


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
