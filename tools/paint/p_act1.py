"""Act 1 (garbage freighter), painterly. Cool steel and deep blue with rust, red pipes and a magenta tower, as in the original."""
import numpy as np
from kit import *

OUT = "../../assets/backgrounds/"


def freighter_wall(p, floor_y=112, seed=2):
    vgrad(p, 0, floor_y, [(0, "#05070f"), (0.35, "#0e1830"), (1, "#27406a")])
    for x in range(8, W, 46):                                   # vertical beams with lit left edge
        beam = p.m_rect(x, 0, x + 10, floor_y)
        p.shade(beam, "#1c2c50", 1.25, 0.55, tex=0.1, seed=3)
        p.edge(beam, (150, 180, 255), 0.22, "left")
        p.edge(beam, (0, 0, 0), 0.5, "right")
    for x in range(30, W, 92):                                  # red pipes from the ceiling
        ln = 34 + (x * 7) % 36
        pipe = p.m_rect(x, 0, x + 3, ln)
        p.shade(pipe, "#b03030", 1.4, 0.5, angle=(-1, 0), tex=0.05, seed=4)
    p.multiply(0.8 + 0.4 * p.noise(24, 3, seed), 0.5)


def deck(p, y0=112, a="#3a4252", b="#10141c"):
    floor(p, y0, a, b)


def robot_head():
    p = Paint(base="#05070f", seed=31)
    freighter_wall(p)
    # chasm (left)
    p.fill(p.m_rect(0, 112, 104, H), (2, 3, 8))
    p.fill(p.m_poly([(0, 112), (104, 112), (96, 120), (0, 124)]), p.lin(0, 112, 0, 124, "#2a3248", "#05060c"))
    p.fill(p.m_line(0, 112, 104, 112, 1), (180, 200, 230), 0.35)
    # deck right of the chasm
    p.fill(p.m_rect(104, 112, W, H), p.lin(0, 112, 0, H, "#3a4252", "#10141c"))
    p.multiply(0.75 + 0.5 * p.noise(8, 3, 3), 0.45)
    p.fill(p.m_rect(104, 112, W, 113), (200, 210, 220), 0.3)
    p.fill(p.m_rect(103, 112, 105, H), (0, 0, 0), 0.7)
    # giant robot head
    head = p.m_rect(150, 14, 304, 112)
    p.shade(head, "#8b97a6", 1.35, 0.45, tex=0.14, seed=5)
    p.edge(head, (255, 255, 255), 0.3, "top")
    p.edge(head, (0, 0, 0), 0.6)
    brow = p.m_rect(160, 26, 294, 54)
    p.shade(brow, "#5c6676", 1.2, 0.5, seed=6)
    p.edge(brow, (0, 0, 0), 0.5)
    for cx, broken in ((192, True), (258, False)):
        eye = p.m_ell(cx - 16, 32, cx + 16, 66)
        p.fill(eye, p.radial(cx, 49, 17, "#ff6a40" if broken else "#9ff0ff", "#4a0c08" if broken else "#106a88"))
        p.edge(eye, (0, 0, 0), 0.7, width=2)
    p.fill(p.m_line(176, 36, 210, 64, 2), (6, 6, 10))
    p.fill(p.m_line(180, 34, 206, 62, 1), (255, 140, 100), 0.5)
    p.glow(192, 49, 46, (255, 80, 50), 0.4)
    p.glow(258, 49, 40, (120, 220, 255), 0.22)
    mouth = p.m_rect(186, 82, 270, 100)
    p.fill(mouth, (6, 8, 12))
    for x in range(190, 270, 7):
        p.fill(p.m_rect(x, 82, x + 2, 100), (130, 140, 156))
    for x, y in [(160, 20), (296, 20), (160, 104), (296, 104)]:
        p.fill(p.m_rect(x - 1, y - 1, x + 2, y + 2), (50, 56, 66))
    ear_l = p.m_rect(138, 40, 152, 84)
    ear_r = p.m_rect(302, 40, 316, 84)
    for e in (ear_l, ear_r):
        p.shade(e, "#566070", 1.2, 0.5, seed=7)
        p.edge(e, (0, 0, 0), 0.6)
    ant = p.m_rect(214, 2, 240, 14)
    p.shade(ant, "#6c7686", 1.2, 0.5, seed=8)
    p.fill(p.m_line(227, 0, 227, 4, 1), (255, 90, 70))
    p.glow(227, 2, 12, (255, 90, 70), 0.4)
    # sharp metal plate on the deck
    p.fill(p.m_poly([(118, 128), (138, 120), (146, 126), (126, 134)]), (210, 222, 240))
    p.fill(p.m_line(120, 128, 138, 121, 1), (255, 255, 255), 0.9)
    p.glow(130, 126, 18, (220, 235, 255), 0.18)
    p.glow(260, 124, 90, (130, 160, 220), 0.1, 0.3)
    return p


def conveyor():
    p = Paint(base="#05070f", seed=32)
    freighter_wall(p, 100)
    p.fill(p.m_rect(0, 100, W, H), p.lin(0, 100, 0, H, "#1c202c", "#06070b"))
    # the belt
    belt = p.m_rect(0, 88, 250, 112)
    p.shade(belt, "#444c5c", 1.35, 0.5, angle=(0, -1), tex=0.1, seed=9)
    p.edge(belt, (255, 255, 255), 0.25, "top")
    for x in range(0, 250, 9):
        p.fill(p.m_rect(x, 92, x + 3, 108), (10, 12, 18), 0.8)
    p.fill(p.m_rect(0, 112, 250, 120), p.lin(0, 112, 0, 120, "#8a93a4", "#2a3040"))
    for x in range(0, 250, 12):
        p.fill(p.m_poly([(x, 112), (x + 6, 112), (x + 10, 120), (x + 4, 120)]), (232, 190, 40))
    # scrap riding the belt
    for i, x in enumerate(range(8, 240, 34)):
        c = [(176, 82, 38), (44, 128, 140), (124, 124, 136), (160, 44, 46), (96, 64, 138)][i % 5]
        sh = p.m_poly([(x, 88), (x + 8, 76 - i % 3 * 3), (x + 22, 78), (x + 26, 88)])
        p.shade(sh, c, 1.35, 0.45, seed=10 + i)
        p.edge(sh, (0, 0, 0), 0.5)
    # crusher at the right
    p.fill(p.m_rect(252, 0, 302, 12), (80, 86, 98))
    pist = p.m_rect(270, 12, 284, 60)
    p.shade(pist, "#b8c0cc", 1.4, 0.4, angle=(-1, 0), seed=11)
    blk = p.m_rect(252, 60, 302, 96)
    p.shade(blk, "#778292", 1.3, 0.45, tex=0.16, seed=12)
    p.edge(blk, (255, 255, 255), 0.25, "top")
    p.edge(blk, (0, 0, 0), 0.65)
    for x in range(256, 300, 8):
        p.fill(p.m_rect(x, 62, x + 1, 94), (20, 24, 32), 0.6)
    p.fill(p.m_rect(248, 0, 252, 100), (24, 28, 40))
    p.fill(p.m_rect(302, 0, 306, 100), (24, 28, 40))
    for k in range(3):                                           # steam
        p.glow(310 + k * 3, 70 - k * 14, 22, (210, 225, 240), 0.35)
    # drainage pipe exit
    pipe = p.m_rect(300, 108, 320, 138)
    p.fill(pipe, (3, 4, 8))
    p.edge(pipe, (120, 140, 170), 0.6, "left")
    p.fill(p.m_rect(304, 114, 320, 134), p.lin(0, 114, 0, 134, "#0a1630", "#02040a"))
    p.glow(312, 124, 20, (60, 110, 200), 0.3)
    text(p, 6, 126, "DANGER", (255, 210, 60), 16)
    p.glow(130, 100, 100, (255, 200, 110), 0.12, 0.3)
    return p


def rat_lair():
    p = Paint(base="#020308", seed=33)
    vgrad(p, 0, H, [(0, "#020308"), (0.6, "#06101a"), (1, "#021208")])
    for i in range(34):                                          # stalactite ribs
        x = int(p.rng.integers(0, W))
        p.fill(p.m_line(x, 0, x + int(p.rng.integers(-16, 16)), int(p.rng.integers(20, 78)), 2), (40, 54, 70), 0.7)
    p.multiply(0.7 + 0.6 * p.noise(14, 3, 4), 0.6)
    # reactor pit glow
    pit = p.m_ell(86, 100, 236, 152)
    p.fill(pit, p.radial(161, 126, 76, "#9bff6a", "#03140a", 0.4))
    core = p.m_ell(134, 110, 188, 136)
    p.fill(core, p.radial(161, 122, 28, "#e8ffc0", "#3ad02a", 0.45))
    p.glow(161, 118, 120, (80, 255, 60), 0.5, 0.5)
    p.fill(p.m_rect(150, 98, 172, 108), (200, 230, 190))
    # suspension platforms and chains
    for x0 in (36, 206):
        pl = p.m_rect(x0, 72, x0 + 84, 82)
        p.shade(pl, "#7c8898", 1.3, 0.45, angle=(0, -1), seed=13 + x0)
        p.edge(pl, (255, 255, 255), 0.3, "top")
        p.edge(pl, (0, 0, 0), 0.6, "bottom")
        for x in (x0 + 12, x0 + 70):
            p.fill(p.m_line(x, 0, x, 72, 1), (70, 82, 96))
    # iron ladder
    for x in (20, 34):
        p.fill(p.m_rect(x, 24, x + 3, 112), (150, 160, 176))
        p.fill(p.m_rect(x, 24, x + 1, 112), (230, 240, 255), 0.5)
    for y in range(30, 112, 8):
        p.fill(p.m_rect(21, y, 35, y + 2), (140, 150, 166))
    # rat pipe, top right, with red eyes
    pp = p.m_rect(262, 8, 320, 38)
    p.shade(pp, "#8a5a38", 1.3, 0.4, angle=(0, -1), seed=14)
    p.edge(pp, (0, 0, 0), 0.7)
    mouth = p.m_ell(268, 12, 316, 36)
    p.fill(mouth, (2, 2, 4))
    for ex in (284, 298):
        p.fill(p.m_rect(ex, 20, ex + 4, 23), (255, 60, 50))
        p.glow(ex + 2, 21, 10, (255, 60, 50), 0.5)
    # lair debris and bones
    for i in range(16):
        x = int(p.rng.integers(250, 316))
        y = int(p.rng.integers(112, 140))
        p.fill(p.m_rect(x, y, x + int(p.rng.integers(3, 10)), y + 3), (90, 80, 76))
    return p


def rail_walk(grabber_x=198):
    p = Paint(base="#0a1430", seed=34)
    vgrad(p, 0, 112, [(0, "#060a1c"), (0.4, "#122050"), (1, "#2a4a8c")])
    p.multiply(0.8 + 0.4 * p.noise(20, 3, 6), 0.5)
    for x in range(14, W, 38):                                   # vertical red pipes
        ln = 52 + (x * 5) % 24
        pp = p.m_rect(x, 0, x + 3, ln)
        p.shade(pp, "#c23838", 1.4, 0.5, angle=(-1, 0), tex=0.05, seed=15)
    for y in (7, 14, 21):                                        # magenta conduits
        pp = p.m_rect(0, y, W, y + 3)
        p.shade(pp, "#c040c0", 1.4, 0.55, angle=(0, -1), tex=0.05, seed=16)
    # teal wall panel at left
    pan = p.m_rect(18, 44, 48, 104)
    p.shade(pan, "#2a9ea6", 1.25, 0.5, seed=17)
    p.edge(pan, (0, 0, 0), 0.55)
    # magenta tower
    tower = p.m_poly([(140, 0), (204, 0), (214, 30), (210, 112), (134, 112), (128, 30)])
    p.shade(tower, "#d048d8", 1.35, 0.35, angle=(-1, 0), tex=0.12, seed=18)
    p.edge(tower, (0, 0, 0), 0.6)
    win = p.m_rect(150, 16, 196, 38)
    p.fill(win, p.lin(0, 16, 0, 38, "#0a0a18", "#1a1a34"))
    for x in (156, 168, 180):
        p.fill(p.m_rect(x, 20, x + 8, 34), (240, 240, 250))
    p.glow(171, 27, 40, (255, 255, 255), 0.12)
    # long glossy cyan rail
    rail = p.m_rect(0, 76, W, 80)
    p.fill(rail, p.lin(0, 76, 0, 80, "#a0fff8", "#1a8a96"))
    p.fill(p.m_rect(0, 76, W, 77), (255, 255, 255), 0.6)
    # support lattice and deck
    for x in range(0, W, 20):
        p.fill(p.m_line(x, 81, x + 10, 132, 1), (80, 110, 210), 0.9)
        p.fill(p.m_line(x + 10, 81, x, 132, 1), (60, 90, 190), 0.9)
    p.fill(p.m_rect(0, 128, W, H), p.lin(0, 128, 0, H, "#0a1020", "#02040a"))
    p.fill(p.m_rect(0, 128, W, 130), (120, 150, 230), 0.5)
    # the grabber
    gr = p.m_rect(grabber_x, 66, grabber_x + 16, 78)
    p.shade(gr, "#8a94a4", 1.3, 0.4, seed=19)
    p.edge(gr, (0, 0, 0), 0.6)
    p.fill(p.m_rect(grabber_x + 7, 78, grabber_x + 9, 98), (170, 176, 190))
    claw = p.m_poly([(grabber_x + 1, 98), (grabber_x + 15, 98), (grabber_x + 12, 106), (grabber_x + 4, 106)])
    p.shade(claw, "#c04848", 1.3, 0.5, seed=20)
    p.glow(grabber_x + 8, 100, 20, (255, 90, 80), 0.25)
    p.glow(171, 80, 160, (180, 255, 250), 0.16, 0.2)
    return p


def crane_cabin():
    p = Paint(base="#04060a", seed=35)
    vgrad(p, 0, H, [(0, "#0a0e18"), (1, "#05070c")])
    # window onto the reactor room
    p.fill(p.m_rect(18, 12, 302, 56), p.lin(0, 12, 0, 56, "#020308", "#08241a"))
    p.fill(p.m_ell(100, 36, 220, 70), p.radial(160, 56, 62, "#caff9a", "#0a3a14", 0.35))
    p.glow(160, 56, 140, (90, 255, 70), 0.4, 0.5)
    for x in range(18, 302, 56):
        p.fill(p.m_rect(x, 12, x + 3, 56), (50, 58, 70))
    fr = p.m_rect(14, 8, 306, 12)
    p.shade(fr, "#6a7482", 1.3, 0.5, seed=21)
    p.fill(p.m_rect(14, 56, 306, 60), (30, 36, 46))
    # control desk
    desk = p.m_poly([(0, H), (24, 92), (296, 92), (320, H)])
    p.shade(desk, "#4a5262", 1.3, 0.45, angle=(0, -1), tex=0.12, seed=22)
    p.edge(desk, (255, 255, 255), 0.25, "top")
    # CRT with a wireframe grid and reticle
    crt = p.m_rect(56, 60, 148, 108)
    p.shade(crt, "#7a8494", 1.25, 0.5, seed=23)
    p.edge(crt, (0, 0, 0), 0.6)
    scr = p.m_rect(64, 67, 140, 101)
    p.fill(scr, p.lin(0, 67, 0, 101, "#0e3a1c", "#04140a"))
    for x in range(68, 140, 9):
        p.fill(p.m_line(x, 67, x, 101, 1), (60, 220, 100), 0.7)
    for y in range(70, 101, 8):
        p.fill(p.m_line(64, y, 140, y, 1), (60, 220, 100), 0.7)
    p.fill(p.m_rect(98, 82, 108, 86), (255, 255, 255))
    p.glow(102, 84, 80, (80, 255, 120), 0.25)
    # joystick and red button
    p.fill(p.m_rect(188, 92, 200, 104), (120, 126, 140))
    p.fill(p.m_rect(192, 70, 196, 92), (190, 196, 210))
    ball = p.m_ell(188, 64, 202, 76)
    p.fill(ball, p.radial(194, 69, 7, "#ff8a7a", "#a01818"))
    btn = p.m_ell(224, 96, 246, 108)
    p.fill(btn, p.radial(234, 100, 11, "#ff9a8a", "#a01010"))
    p.glow(234, 100, 28, (255, 70, 60), 0.3)
    # pilot's seat
    seat = p.m_rect(252, 76, 308, H)
    p.shade(seat, "#9a3aa0", 1.3, 0.4, tex=0.14, seed=24)
    p.edge(seat, (0, 0, 0), 0.6)
    p.glow(160, 60, 160, (90, 255, 70), 0.12, 0.5)
    return p


def mallard_bay(lit=True):
    p = Paint(base="#05070f", seed=36)
    freighter_wall(p, 104)
    p.fill(p.m_rect(0, 104, W, H), p.lin(0, 104, 0, H, "#343c4c", "#0c1018"))
    p.multiply(0.7 + 0.6 * p.noise(8, 3, 3), 0.5)
    p.fill(p.m_rect(0, 104, W, 106), (190, 205, 225), 0.3)
    # the Aluminum Mallard: small, angular, battered
    hull = [(76, 86), (94, 54), (202, 44), (260, 64), (268, 96), (76, 102)]
    m = shaded(p, hull, "#aab4c2", 1.45, 0.35, seed=25, tex=0.16)
    p.edge(m, (255, 255, 255), 0.3, "top")
    glass = p.m_poly([(224, 56), (256, 68), (258, 82), (218, 78)])
    p.fill(glass, p.lin(218, 56, 258, 82, "#bff8ff" if lit else "#2a3a50", "#1a5a78" if lit else "#0a1018"))
    p.edge(glass, (0, 0, 0), 0.7)
    eng = p.m_rect(94, 70, 108, 100)
    p.fill(eng, (4, 5, 8))
    for y in range(72, 100, 5):
        p.fill(p.m_rect(94, y, 108, y + 1), (110, 120, 134))
    p.fill(p.m_rect(148, 62, 178, 78), (150, 76, 40), 0.9)               # rust
    p.multiply(0.9 + 0.2 * p.noise(5, 2, 7), 0.5)
    p.fill(p.m_poly([(138, 78), (196, 80), (190, 92), (142, 90)]), (120, 54, 34), 0.8)
    p.fill(p.m_line(76, 86, 268, 96, 1), (10, 12, 16), 0.6)
    if lit:
        for x, y in [(112, 100), (240, 90), (180, 52)]:
            p.fill(p.m_rect(x, y, x + 6, y + 2), (255, 210, 90))
            p.glow(x + 3, y + 1, 18, (255, 190, 60), 0.5)
    ramp = p.m_poly([(150, 102), (192, 102), (204, 118), (138, 118)])
    p.shade(ramp, "#6a7484", 1.3, 0.4, seed=26)
    p.edge(ramp, (0, 0, 0), 0.6)
    for x in (62, 258):
        p.fill(p.m_rect(x, 102, x + 12, 118), (60, 68, 82))
    p.glow(172, 112, 70, (255, 200, 120), 0.12, 0.3)
    return p


def cockpit():
    p = Paint(base="#1a0a2a", seed=37)
    # side walls and ceiling in magenta-violet perspective
    p.fill(p.m_poly([(0, 0), (W, 0), (264, 42), (56, 42)]), p.lin(0, 0, 0, 42, "#4a1a6a", "#7a3aa0"))
    p.fill(p.m_poly([(0, 0), (56, 42), (56, 104), (0, H)]), p.lin(0, 0, 56, 0, "#1a0a2a", "#6a2a8a"))
    p.fill(p.m_poly([(W, 0), (264, 42), (264, 104), (W, H)]), p.lin(264, 0, W, 0, "#8a3ab0", "#2a1048"))
    for i in range(1, 6):                                       # wall ribs
        t = i / 6
        p.fill(p.m_line(int(56 * t), int(42 * t), int(56 * t), int(104 + 40 * t), 1), (20, 8, 36), 0.7)
        p.fill(p.m_line(W - int(56 * t), int(42 * t), W - int(56 * t), int(104 + 40 * t), 1), (20, 8, 36), 0.7)
    # viewscreen with stars
    p.fill(p.m_rect(56, 42, 264, 104), (2, 3, 10))
    p.stars(p.m_rect(56, 42, 264, 104), 90, seed=7)
    p.stars(p.m_rect(56, 42, 264, 104), 14, seed=8, bright=1.5)
    p.fill(p.m_rect(54, 40, 266, 44), (150, 130, 190))
    p.fill(p.m_rect(54, 102, 266, 106), (60, 40, 90))
    # floor grating
    p.fill(p.m_poly([(56, 104), (264, 104), (W, H), (0, H)]), p.lin(0, 104, 0, H, "#4a3a5a", "#14101e"))
    for i in range(-8, 9):
        p.fill(p.m_line(160 + i * 12, 105, 160 + i * 42, H, 1), (0, 0, 0), 0.55)
    for y in (112, 122, 134):
        p.fill(p.m_line(int(56 - (y - 104) * 1.8), y, int(264 + (y - 104) * 1.8), y, 1), (0, 0, 0), 0.5)
    # pilot's seat (left) and nav console (right)
    seat = p.m_rect(6, 56, 54, 126)
    p.shade(seat, "#8a94a6", 1.3, 0.4, seed=27)
    p.edge(seat, (0, 0, 0), 0.6)
    cushion = p.m_rect(12, 62, 48, 92)
    p.shade(cushion, "#4a4e60", 1.2, 0.5, seed=28)
    con = p.m_poly([(262, 56), (316, 50), (316, 118), (262, 112)])
    p.shade(con, "#7a8494", 1.3, 0.4, seed=29)
    p.edge(con, (0, 0, 0), 0.6)
    scr = p.m_rect(268, 62, 312, 84)
    p.fill(scr, p.lin(0, 62, 0, 84, "#1a6a3a", "#042010"))
    for i, c in enumerate([(255, 90, 80), (255, 210, 80), (100, 230, 130), (100, 200, 255)]):
        p.fill(p.m_rect(270 + i * 10, 94, 276 + i * 10, 100), c)
        p.glow(273 + i * 10, 97, 10, c, 0.3)
    p.glow(290, 74, 50, (80, 255, 140), 0.2)
    p.glow(160, 80, 150, (140, 150, 255), 0.15, 0.6)
    return p


def nav_screen():
    p = Paint(base="#02030a", seed=38)
    vgrad(p, 0, H, [(0, "#04040e"), (1, "#0a0618")])
    for x in range(6, 316, 30):
        p.fill(p.m_line(x, 34, x, 138, 1), (170, 40, 170), 0.8)
    for y in range(34, 140, 20):
        p.fill(p.m_line(6, y, 314, y, 1), (170, 40, 170), 0.8)
    p.stars(p.m_rect(6, 34, 314, 138), 260, seed=9)
    p.glow(60, 90, 70, (120, 60, 220), 0.18)
    for i, t in enumerate(("1. RESUME SCAN", "2. SET COURSE", "3. RETURN")):
        x = 6 + i * 78
        p.fill(p.m_rect(x, 4, x + 72, 26), (4, 10, 6))
        for q in ((x, 4, x + 72, 5), (x, 25, x + 72, 26), (x, 4, x + 1, 26), (x + 71, 4, x + 72, 26)):
            p.fill(p.m_rect(*q), (60, 230, 90))
        text(p, x + 5, 9, t, (60, 230, 90), 13)
    p.fill(p.m_rect(30, 54, 108, 112), (2, 2, 8))
    for q in ((30, 54, 108, 55), (30, 111, 108, 112), (30, 54, 31, 112), (107, 54, 108, 112)):
        p.fill(p.m_rect(*q), (240, 240, 250))
    pl = p.m_ell(52, 66, 86, 100)
    p.fill(pl, p.radial(62, 76, 22, "#ffb0f8", "#601070"))
    p.glow(69, 83, 36, (255, 120, 255), 0.4)
    for i, t in enumerate(("NAME", " PLANET PHLEEBHUT", "SECTOR 95", "LIGHT ATMOSPHERE", "1 KNOWN SETTLEMENT")):
        text(p, 116, 52 + i * 14, t, (255, 110, 100), 15)
    return p


ROOMS = {
    "robot_head": robot_head,
    "conveyor": conveyor,
    "rat_lair": rat_lair,
    "rail_walk": rail_walk,
    "crane_cabin": crane_cabin,
    "mallard_bay": mallard_bay,
    "cockpit": cockpit,
    "nav_screen": nav_screen,
}
