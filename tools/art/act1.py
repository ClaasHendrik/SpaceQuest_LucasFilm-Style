"""Act 1: the garbage freighter. Palette follows the original: deep blue and black, cyan rails, red pipes, magenta towers."""
from ega import *


def freighter_wall(c, top=0, bottom=100):
    c.vgrad(0, top, W - 1, bottom, [K, B, B, B])
    for x in range(6, W, 40):                       # vertical beams, dithered shading like the original
        c.drect(x, top, x + 9, bottom, B, LB)
        c.rect(x, top, x, bottom, K)
    for x in range(26, W, 80):                      # red pipes down from the ceiling
        c.rect(x, 0, x + 1, 30 + (x % 30), R)
        c.rect(x, 0, x, 30 + (x % 30), LR)


def floor_grating(c, y0=96, base=DG, hi=S):
    c.rect(0, y0, W - 1, H - 1, base)
    c.drect(0, y0, W - 1, y0 + 6, base, K)
    for x in range(0, W, 8):
        c.line(x, y0, x - 14, H - 1, hi)
    c.line(0, y0, W - 1, y0, hi)


def escape_pod(locker_open=False, uniform=True):
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, B)
    c.vgrad(0, 0, W - 1, 40, [K, B])
    for x in range(0, W, 16):                       # wall ribs
        c.drect(x, 0, x + 3, 95, DG, B)
    c.rect(0, 0, W - 1, 6, K)
    c.rect(0, 94, W - 1, 97, S)
    floor_grating(c, 98)
    # cryo chamber (left)
    c.box3d(16, 20, 72, 96, S, WH, DG)
    c.rect(24, 28, 64, 92, K)
    c.drect(24, 28, 64, 92, C, LC)
    c.rect(24, 28, 30, 92, K)                       # open door
    c.poly([(24, 28), (10, 36), (10, 90), (24, 92)], C)
    c.rect(26, 14, 62, 19, R)
    c.rect(30, 16, 34, 17, LR)
    # control panels along the back wall
    c.box3d(84, 34, 112, 70, DG, S, K)
    for i in range(3):
        c.rect(88 + i * 8, 40, 92 + i * 8, 44, [LG, Y, LR][i])
    c.rect(88, 52, 108, 64, K)
    c.drect(88, 52, 108, 64, G, K)
    # wall locker (centre)
    c.box3d(122, 28, 162, 92, S, WH, DG)
    c.rect(128, 34, 156, 86, DG if not locker_open else K)
    c.line(142, 34, 142, 86, K)
    c.rect(137, 56, 138, 62, Y)
    c.text(126, 18, "LOCKER", DG, 8)
    if locker_open:
        c.rect(128, 34, 156, 86, K)
        c.poly([(128, 34), (112, 40), (112, 88), (128, 86)], S)
        if uniform:                                  # orange-and-white uniform on a hanger
            c.rect(138, 38, 146, 40, WH)
            c.poly([(132, 42), (152, 42), (150, 76), (134, 76)], N)
            c.rect(132, 42, 134, 56, WH)
            c.rect(150, 42, 152, 56, WH)
            c.rect(136, 76, 148, 84, WH)
    # airlock hatch (right)
    c.box3d(224, 26, 292, 96, S, WH, DG)
    c.ell(236, 40, 280, 84, DG)
    c.ell(240, 44, 276, 80, K)
    c.stars(242, 46, 274, 78, 18)
    c.poly([(246, 70), (258, 58), (270, 72)], DG)    # a piece of passing junk
    for x in range(228, 290, 8):                     # hazard stripe
        c.poly([(x, 88), (x + 4, 88), (x + 8, 94), (x + 4, 94)], Y)
    c.rect(222, 62, 226, 74, R)
    return c


def garbage_mountain(wire=True):
    c = Cv()
    c.vgrad(0, 0, W - 1, 60, [K, K, B])
    c.stars(0, 0, W - 1, 20, 14, (DG, B, LB))
    for x in range(10, W, 60):
        c.rect(x, 0, x + 3, 40, DG)
    for x, y in [(300, 8), (40, 12), (170, 6)]:       # yellow hazard lights in the distance
        c.rect(x, y, x + 2, y + 2, Y)
    # mounds of junk, far to near
    cols = [(B, LB), (M, B), (DG, K), (R, N), (C, B), (S, DG), (N, R), (G, C), (M, LM)]
    r = c.rng
    for layer, (y0, n) in enumerate([(70, 9), (84, 8), (98, 7)]):
        for i in range(n):
            x = i * W // n + r.randint(-8, 8)
            w = r.randint(34, 60)
            h = r.randint(14, 30)
            c1, c2 = r.choice(cols)
            c.dpoly([(x - w // 2, y0 + 22), (x - w // 4, y0 - h), (x + w // 5, y0 - h + 6), (x + w // 2, y0 + 22)], c1, c2)
    c.rect(0, 104, W - 1, H - 1, DG)
    c.drect(0, 104, W - 1, H - 1, DG, K)
    for i in range(70):                              # scattered scrap
        x, y = r.randint(0, W - 4), r.randint(70, 128)
        c1 = r.choice([N, M, C, S, R, LB, G])
        c.rect(x, y, x + r.randint(2, 6), y + r.randint(1, 3), c1)
    # crumpled starfighter cockpit, left foreground... here centre-left
    c.ell(104, 62, 160, 112, DG)
    c.ell(112, 70, 152, 104, K)
    c.line(132, 70, 132, 104, S)
    c.line(112, 87, 152, 87, S)
    c.rect(96, 82, 108, 90, DG)
    # escape pod, left
    c.rect(8, 56, 54, 100, DG)
    c.drect(8, 56, 54, 100, DG, S)
    c.rect(18, 66, 44, 90, K)
    c.rect(20, 68, 42, 88, LB)
    c.text(20, 72, "POD", WH, 8)
    # wire on the ground
    if wire:
        c.line(196, 100, 214, 96, Y, 2)
        c.line(214, 96, 224, 100, N, 2)
    return c


def robot_head():
    c = Cv()
    freighter_wall(c, 0, 100)
    floor_grating(c, 100)
    c.rect(0, 100, 100, H - 1, K)                    # chasm at left
    c.drect(0, 100, 100, H - 1, K, B)
    c.line(100, 100, 100, H - 1, S)
    # giant robot head
    c.box3d(150, 14, 290, 100, S, WH, DG)
    c.box3d(160, 22, 280, 52, DG, S, K)             # brow
    c.ell(176, 34, 204, 62, K)                       # broken eye socket
    c.ell(180, 38, 200, 58, R)
    c.line(176, 34, 204, 62, K, 2)
    c.ell(226, 34, 254, 62, DG)
    c.ell(230, 38, 250, 58, LC)
    c.rect(180, 76, 260, 90, K)                      # grille mouth
    for x in range(184, 260, 6):
        c.line(x, 76, x, 90, S)
    c.box3d(140, 40, 152, 76, DG, S, K)             # ear plates
    c.box3d(288, 40, 300, 76, DG, S, K)
    c.rect(194, 5, 244, 14, DG)                      # neck bolt/antenna
    c.line(219, 0, 219, 6, LR)
    # sharp metal plate on the ground (a deadly pickup)
    c.poly([(110, 112), (128, 106), (132, 112), (116, 118)], WH)
    return c


def conveyor():
    c = Cv()
    freighter_wall(c, 0, 90)
    c.rect(0, 90, W - 1, H - 1, K)
    c.box3d(0, 84, 250, 104, DG, S, K)               # the belt
    for x in range(0, 250, 10):
        c.rect(x, 90, x + 4, 100, K)
    for x in range(0, 250, 28):                      # scrap riding the belt
        c.rect(x + 6, 78, x + 18, 84, [N, M, R, C][(x // 28) % 4])
    c.box3d(0, 104, 250, 112, S, WH, DG)
    for x in range(0, 250, 8):
        c.poly([(x, 104), (x + 4, 104), (x + 8, 112), (x + 4, 112)], Y)
    # hydraulic crusher
    c.rect(252, 0, 296, 12, S)
    c.rect(268, 12, 280, 54, DG)
    c.box3d(252, 54, 296, 92, S, WH, DG)
    for x in range(254, 296, 8):
        c.line(x, 56, x, 90, DG)
    c.rect(250, 0, 253, 100, DG)
    c.rect(297, 0, 300, 100, DG)
    c.drect(300, 20, 314, 60, WH, K)                 # steam
    # drainage pipe exit
    c.box3d(296, 98, 318, 124, K, DG, K)
    c.rect(300, 102, 314, 120, B)
    c.text(2, 118, "DANGER", Y, 8)
    return c


def rat_lair():
    c = Cv()
    c.vgrad(0, 0, W - 1, H - 1, [K, K, B, K])
    for i in range(30):                              # cave ribs
        x = c.rng.randint(0, W)
        c.line(x, 0, x + c.rng.randint(-20, 20), c.rng.randint(20, 70), DG)
    # reactor pit
    c.ell(90, 92, 230, 140, K)
    c.dell(104, 96, 216, 136, G, K)
    c.ell(130, 100, 190, 128, LG)
    c.dell(120, 98, 200, 130, LG, G)
    c.rect(150, 90, 170, 100, WH)
    # suspension platform
    c.box3d(40, 66, 120, 76, S, WH, DG)
    c.box3d(200, 66, 280, 76, S, WH, DG)
    for x in (60, 100, 220, 260):
        c.line(x, 0, x, 66, DG)
    # iron ladder (left)
    c.rect(22, 20, 24, 100, S)
    c.rect(34, 20, 36, 100, S)
    for y in range(24, 100, 7):
        c.line(24, y, 34, y, S)
    # rat pipe top right and a pair of red eyes
    c.box3d(268, 10, 318, 34, N, Y, R)
    c.rect(272, 16, 314, 30, K)
    c.rect(286, 20, 289, 22, LR)
    c.rect(296, 20, 299, 22, LR)
    # lair debris
    for i in range(12):
        x = c.rng.randint(260, 316)
        c.rect(x, 100 + c.rng.randint(0, 24), x + 8, 104 + c.rng.randint(0, 24), c.rng.choice([DG, N, M]))
    c.stars(0, 0, 0, 0, 0)
    return c


def rail_walk(grabber_x=200):
    c = Cv()
    c.vgrad(0, 0, W - 1, 100, [B, B, K, B])
    c.drect(0, 0, W - 1, 100, B, K, 1)
    for x in range(14, W, 36):                       # vertical red pipes
        c.rect(x, 0, x + 1, 56, R)
        c.rect(x, 0, x, 56, LR)
    for y in (6, 12, 18):                            # horizontal conduits
        c.rect(0, y, W - 1, y + 2, M)
        c.rect(0, y, W - 1, y, LM)
    # magenta tower, centre
    c.poly([(140, 0), (200, 0), (210, 26), (206, 100), (136, 100), (130, 26)], M)
    c.dpoly([(140, 0), (170, 0), (170, 100), (136, 100)], M, LM)
    c.dpoly([(170, 0), (200, 0), (206, 100), (170, 100)], M, K)
    c.rect(150, 14, 190, 34, K)
    for x in (156, 166, 176):
        c.rect(x, 18, x + 6, 30, WH)
    # long cyan rail
    c.rect(0, 70, W - 1, 73, C)
    c.rect(0, 70, W - 1, 70, LC)
    # support girders + deck
    for x in range(0, W, 20):
        c.line(x, 74, x + 10, 128, LB)
        c.line(x + 10, 74, x, 128, LB)
    c.rect(0, 120, W - 1, H - 1, K)
    c.rect(0, 118, W - 1, 119, LB)
    c.rect(20, 40, 44, 90, C)                        # teal wall panel left
    c.drect(20, 40, 44, 90, C, B)
    # the grabber hanging from the rail
    c.rect(grabber_x, 60, grabber_x + 14, 70, DG)
    c.rect(grabber_x + 6, 70, grabber_x + 8, 86, S)
    c.rect(grabber_x + 2, 86, grabber_x + 12, 90, R)
    return c


def crane_cabin():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, K)
    c.drect(0, 0, W - 1, 20, DG, K)
    # window strip showing the reactor room below
    c.box3d(19, 13, 301, 53, DG, S, K)
    c.vgrad(21, 15, 299, 51, [K, B])
    c.stars(22, 16, 298, 50, 30, (DG, B, LB))
    c.dell(120, 38, 200, 52, G, K)
    c.dell(110, 30, 210, 56, G, LG)
    for x in range(40, 300, 50):
        c.rect(x, 15, x + 2, 51, DG)
    # control desk
    c.poly([(0, 132), (30, 84), (290, 84), (320, 132)], DG)
    c.dpoly([(0, 132), (30, 84), (290, 84), (320, 132)], DG, S)
    # CRT monitor with wireframe grid
    c.box3d(60, 56, 140, 100, S, WH, DG)
    c.rect(66, 62, 134, 92, K)
    for x in range(70, 134, 8):
        c.line(x, 62, x, 92, G)
    for y in range(64, 92, 7):
        c.line(66, y, 134, y, G)
    c.rect(98, 74, 102, 78, WH)                      # target reticle
    # joystick and red button
    c.rect(180, 86, 190, 96, S)
    c.rect(184, 66, 186, 86, DG)
    c.ell(181, 62, 189, 68, R)
    c.ell(220, 90, 236, 100, R)
    c.ell(222, 90, 234, 96, LR)
    # pilot's seat in front
    c.box3d(250, 70, 300, 128, M, LM, B)
    return c


def mallard_bay(lit=True):
    c = Cv()
    freighter_wall(c, 0, 96)
    c.rect(0, 96, W - 1, H - 1, DG)
    c.drect(0, 96, W - 1, H - 1, DG, K)
    c.line(0, 96, W - 1, 96, S)
    # Aluminum Mallard: small, blocky, battered
    c.poly([(80, 80), (96, 52), (200, 44), (256, 62), (262, 90), (80, 96)], S)
    c.dpoly([(80, 80), (96, 52), (200, 44), (256, 62), (262, 90), (80, 96)], S, DG)
    c.poly([(222, 56), (252, 66), (254, 78), (216, 74)], LC if lit else B)        # cockpit glass
    c.rect(96, 66, 108, 92, K)                       # open rear engine manifold
    for y in range(68, 92, 5):
        c.line(96, y, 108, y, DG)
    c.line(80, 80, 262, 90, K)
    c.rect(150, 60, 176, 72, N)                      # rust patch
    c.drect(140, 72, 190, 84, R, N)
    if lit:
        c.rect(108, 96, 120, 98, Y)                  # amber running lights
        c.rect(236, 84, 244, 86, Y)
    c.poly([(150, 96), (190, 96), (200, 110), (140, 110)], DG)   # boarding ramp
    c.rect(146, 110, 196, 112, S)
    c.rect(60, 96, 70, 112, DG)                      # landing struts
    c.rect(250, 96, 262, 112, DG)
    return c


def cockpit():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, M)
    c.dpoly([(0, 0), (320, 0), (260, 40), (60, 40)], M, B)           # ceiling
    c.dpoly([(0, 0), (60, 40), (60, 100), (0, 132)], M, K)           # left wall
    c.dpoly([(320, 0), (260, 40), (260, 100), (320, 132)], B, K)     # right wall
    c.rect(60, 40, 260, 100, K)                                      # forward window
    c.stars(62, 42, 258, 98, 40)
    c.poly([(60, 100), (260, 100), (320, 132), (0, 132)], DG)        # floor grating
    for i in range(-6, 8):
        c.line(160 + i * 6, 100, 160 + i * 28, 132, K)
    for y in (106, 114, 124):
        c.line(0 + (y - 100) * 2, y, 320 - (y - 100) * 2, y, S)
    c.box3d(4, 56, 52, 120, S, WH, DG)                               # pilot's seat, left
    c.rect(10, 62, 46, 84, DG)
    c.box3d(262, 54, 316, 110, S, WH, DG)                            # nav console, right
    c.rect(268, 60, 310, 82, K)
    c.dpoly([(268, 60), (310, 60), (310, 82), (268, 82)], G, K)
    for i in range(4):
        c.rect(270 + i * 10, 90, 276 + i * 10, 96, [LR, Y, LG, LC][i])
    c.rect(150, 100, 170, 104, LR)
    return c


ROOMS = {
    "escape_pod": lambda: escape_pod(False),
    "escape_pod_open": lambda: escape_pod(True, True),
    "escape_pod_open_empty": lambda: escape_pod(True, False),
    "garbage_mountain": lambda: garbage_mountain(True),
    "garbage_mountain_nowire": lambda: garbage_mountain(False),
    "robot_head": robot_head,
    "conveyor": conveyor,
    "rat_lair": rat_lair,
    "rail_walk": rail_walk,
    "crane_cabin": crane_cabin,
    "mallard_bay": mallard_bay,
    "cockpit": cockpit,
}


def nav_screen():
    c = Cv()
    c.rect(0, 0, W - 1, H - 1, K)
    for i, t in enumerate(("1. RESUME SCAN", "2. SET COURSE", "3. RETURN")):
        x = 6 + i * 76
        c.rect(x, 4, x + 70, 22, K)
        c.rect(x, 4, x + 70, 4, LG)
        c.rect(x, 22, x + 70, 22, LG)
        c.rect(x, 4, x, 22, LG)
        c.rect(x + 70, 4, x + 70, 22, LG)
        c.text(x + 4, 8, t, LG, 8)
    for x in range(6, 316, 28):
        c.line(x, 30, x, 128, M)
    for y in range(30, 130, 22):
        c.line(6, y, 314, y, M)
    c.stars(8, 32, 312, 126, 160, (LB, WH, B, LC))
    c.rect(30, 50, 100, 100, K)
    c.rect(30, 50, 100, 50, WH)
    c.rect(30, 100, 100, 100, WH)
    c.rect(30, 50, 30, 100, WH)
    c.rect(100, 50, 100, 100, WH)
    c.ell(52, 64, 78, 90, M)
    c.dell(56, 68, 74, 86, LM, M)
    c.text(106, 50, "NAME", LR, 8)
    c.text(106, 60, " PLANET PHLEEBHUT", LR, 8)
    c.text(106, 76, "SECTOR 95", LR, 8)
    c.text(106, 92, "1 KNOWN SETTLEMENT", LR, 8)
    return c


ROOMS["nav_screen"] = nav_screen
