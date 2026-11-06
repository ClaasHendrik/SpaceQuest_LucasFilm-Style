"""Pilot rooms in the painterly style: the escape pod and the garbage mountain."""
import numpy as np
from paint import Paint, rgb, mix, W, H

OUT = "../../assets/backgrounds/"


def pipe_h(p, x0, x1, y0, y1, base, hi=1.5, lo=0.45):
    m = p.m_rect(x0, y0, x1, y1)
    p.fill(m, np.clip(p.lin(0, y0, 0, y1, rgb(base) * hi, rgb(base) * lo), 0, 255))


def bevel(p, x0, y0, x1, y1, base, hi=1.25, lo=0.6, tex=0.1, seed=1, light=0.9, dark=0.45):
    m = p.m_rect(x0, y0, x1, y1)
    p.shade(m, base, hi, lo, tex=tex, seed=seed)
    p.edge(m, (255, 255, 255), 0.25 * light, "top")
    p.edge(m, (255, 255, 255), 0.18 * light, "left")
    p.edge(m, (0, 0, 0), 0.55 * dark * 1.2, "bottom")
    p.edge(m, (0, 0, 0), 0.45 * dark * 1.2, "right")
    return m


def rivets(p, pts, color=(30, 34, 40)):
    for x, y in pts:
        p.a[y, x] = np.array(color, np.float32)
        p.a[y - 1, x - 1] = np.clip(p.a[y - 1, x - 1] * 1.5 + 20, 0, 255)


_POD_PAL = {}


def escape_pod(locker_open=False, uniform=True):
    p = Paint(base="#1c2a34", seed=11)
    # --- back wall: teal-steel gradient with panel seams and grime
    p.fill(p.m_rect(0, 0, W, 108), p.lin(0, 0, 0, 108, "#142029", "#35505c"))
    for x in range(0, W, 44):
        p.fill(p.m_rect(x, 14, x + 1, 108), (10, 16, 20), 0.7)
        p.fill(p.m_rect(x + 1, 14, x + 2, 108), (120, 160, 175), 0.18)
    p.fill(p.m_rect(0, 62, W, 63), (10, 16, 20), 0.5)
    p.fill(p.m_rect(0, 63, W, 64), (120, 160, 175), 0.12)
    rivets(p, [(x + 5, y) for x in range(0, W, 44) for y in (24, 52, 80, 98)])
    p.multiply(0.8 + 0.4 * p.noise(18, 3, 4), 0.55)
    # --- ceiling with pipes and a warm strip lamp
    p.fill(p.m_rect(0, 0, W, 16), p.lin(0, 0, 0, 16, "#06090c", "#1a2630"))
    pipe_h(p, 0, W, 8, 13, "#6a4a30")
    pipe_h(p, 0, W, 2, 6, "#3a4c58")
    p.fill(p.m_rect(118, 14, 206, 18), (255, 214, 140))
    p.glow(162, 18, 80, (255, 170, 80), 0.55, 0.9)
    # --- floor grating in perspective
    p.fill(p.m_rect(0, 108, W, H), p.lin(0, 108, 0, H, "#2a2e34", "#0e1114"))
    p.fill(p.m_rect(0, 108, W, 110), (150, 170, 180), 0.35)
    for i in range(-10, 30):
        x = 160 + i * 22
        p.fill(p.m_line(x, 110, 160 + i * 40, H, 1), (8, 10, 12), 0.7)
    for y in (116, 126, 138):
        p.fill(p.m_rect(0, y, W, y + 1), (8, 10, 12), 0.6)
    p.multiply(0.85 + 0.3 * p.noise(10, 2, 8), 0.4)
    p.glow(162, 122, 90, (255, 170, 80), 0.16, 0.22)
    # --- cryo chamber (left)
    fr = bevel(p, 10, 20, 82, 110, "#8e9aa4", 1.2, 0.55, seed=2)
    inner = p.m_rect(20, 30, 72, 106)
    p.fill(inner, p.lin(0, 30, 0, 106, "#9fe8f0", "#2a8ca0"))
    p.fill(p.m_rect(20, 30, 72, 50), (255, 255, 255), 0.22)          # frost haze
    p.fill(p.m_poly([(26, 34), (36, 34), (28, 104), (22, 104)]), (255, 255, 255), 0.14)   # glass glint
    door = p.m_poly([(20, 30), (4, 38), (4, 100), (20, 106)])
    p.fill(door, p.lin(4, 0, 20, 0, "#38b4c4", "#79d4e0"))
    p.edge(door, (0, 0, 0), 0.5)
    p.fill(p.m_rect(26, 12, 66, 18), p.lin(0, 12, 0, 18, "#c04040", "#701818"))      # alarm light
    p.glow(46, 15, 26, (255, 70, 60), 0.45, 0.8)
    p.fill(p.m_rect(20, 106, 72, 110), (20, 40, 50))
    # --- control panel
    bevel(p, 94, 44, 130, 86, "#3a4650", 1.2, 0.6, seed=3)
    scr = p.m_rect(98, 50, 126, 66)
    p.fill(scr, p.lin(0, 50, 0, 66, "#1c5a34", "#0a2414"))
    for i in range(6):
        p.fill(p.m_rect(100 + i * 4, 62 - (i * 3) % 9, 102 + i * 4, 64), (110, 255, 150), 0.8)
    for i, c in enumerate([(255, 80, 70), (255, 210, 70), (90, 230, 120), (90, 200, 255)]):
        p.fill(p.m_rect(100 + i * 7, 72, 104 + i * 7, 76), c)
        p.glow(102 + i * 7, 74, 8, c, 0.25)
    # --- wall locker
    lk = bevel(p, 140, 38, 186, 108, "#7c8690", 1.2, 0.6, seed=4)
    if not locker_open:
        p.fill(p.m_rect(162, 40, 164, 106), (10, 14, 18), 0.75)
        p.fill(p.m_rect(156, 66, 158, 80), (230, 190, 90))
        p.fill(p.m_rect(166, 66, 168, 80), (230, 190, 90))
        p.fill(p.m_rect(146, 44, 180, 52), (225, 215, 150), 0.12)
        p.fill(p.m_rect(148, 28, 178, 34), (200, 200, 190), 0.0)
        # a hand-lettered paper sign
        sign = p.m_rect(150, 52, 176, 62)
        p.fill(sign, (226, 218, 190))
        p.edge(sign, (0, 0, 0), 0.4)
        for k in range(4):
            p.fill(p.m_rect(152 + k * 6, 55, 155 + k * 6, 57), (70, 60, 50), 0.8)
    else:
        cav = p.m_rect(146, 42, 180, 104)
        p.fill(cav, p.lin(0, 42, 0, 104, "#0a0d12", "#020304"))
        dr = p.m_poly([(146, 42), (122, 52), (122, 100), (146, 104)])
        p.shade(dr, "#707a84", 1.1, 0.6, seed=5)
        p.edge(dr, (0, 0, 0), 0.55)
        p.fill(p.m_rect(150, 44, 176, 46), (150, 150, 150))          # hanging rail
        if uniform:
            body = p.m_poly([(152, 50), (174, 50), (176, 92), (150, 92)])
            p.shade(body, "#d8702a", 1.25, 0.55, tex=0.08, seed=6)
            p.fill(p.m_rect(152, 50, 174, 55), (240, 236, 226))     # white collar trim
            p.fill(p.m_poly([(150, 56), (146, 80), (152, 80), (154, 58)]), (216, 112, 44))
            p.fill(p.m_poly([(176, 56), (180, 80), (174, 80), (172, 58)]), (216, 112, 44))
            p.fill(p.m_rect(150, 88, 176, 92), (240, 236, 226))
            p.fill(p.m_rect(162, 54, 164, 90), (70, 40, 16), 0.5)
        p.glow(163, 70, 30, (255, 170, 80), 0.18)
    # --- airlock hatch with a porthole onto the junk-filled dark
    bevel(p, 226, 24, 306, 108, "#7a8a96", 1.2, 0.5, seed=7)
    ring = p.m_ell(238, 34, 294, 90)
    p.shade(ring, "#a0aab4", 1.3, 0.4, seed=8)
    glass = p.m_ell(244, 40, 288, 84)
    p.fill(glass, p.radial(266, 62, 24, "#10183a", "#02030a"))
    p.stars(glass, 40, seed=5)
    p.fill(p.m_poly([(252, 74), (262, 70), (266, 76), (256, 80)]), (46, 40, 60), 0.9)   # drifting scrap
    p.edge(glass, (0, 0, 0), 0.7, width=1)
    for k in range(12):
        a = k / 12 * 6.2832
        x, y = int(266 + 29 * np.cos(a)), int(62 + 29 * np.sin(a))
        p.fill(p.m_rect(x - 1, y - 1, x + 1, y + 1), (50, 56, 64))
    hz = p.m_poly([(228, 98), (304, 98), (304, 106), (228, 106)])
    p.fill(hz, (230, 190, 40))
    for x in range(228, 304, 12):
        p.fill(p.m_poly([(x, 98), (x + 6, 98), (x + 2, 106), (x - 4, 106)]), (20, 20, 20))
    p.fill(p.m_rect(220, 60, 226, 86), (150, 40, 36))
    p.glow(266, 62, 70, (80, 110, 200), 0.22, 0.9)
    p.glow(266, 124, 60, (80, 110, 200), 0.16, 0.35)   # cool spill on the floor
    # variants share the closed room's palette, so unchanged parts keep exactly the same colours
    img = p.finish(colors=190, vignette=0.45, palette=_POD_PAL.get("q"))
    if "q" not in _POD_PAL:
        _POD_PAL["q"] = p.last_q
    return img


def debris(p, rng, x0, x1, y0, y1, n, size, haze, depth, palette):
    items = []
    for _ in range(n):
        cx = rng.uniform(x0, x1)
        cy = rng.uniform(y0, y1)
        items.append((cy, cx))
    for cy, cx in sorted(items):
        r = rng.uniform(*size)
        k = int(rng.integers(4, 8))
        ang = np.sort(rng.uniform(0, 6.2832, k))
        stretch = rng.uniform(0.7, 1.6)
        pts = [(cx + np.cos(a) * r * stretch * rng.uniform(0.6, 1.1), cy + np.sin(a) * r * rng.uniform(0.5, 1.0)) for a in ang]
        base = np.array(palette[int(rng.integers(len(palette)))], np.float32) * rng.uniform(0.7, 1.15)
        base = mix(base, np.array(haze, np.float32), depth)
        m = p.m_poly(pts)
        p.shade(m, np.clip(base, 0, 255), 1.4 - 0.3 * depth, 0.45, tex=0.16, seed=int(rng.integers(1, 50)))
        p.edge(m, (0, 0, 0), 0.35 - 0.2 * depth)
        p.edge(m, (255, 240, 210), 0.22 * (1 - depth), "top")


PAL = [(176, 82, 38), (205, 120, 48), (44, 128, 140), (96, 64, 138), (124, 124, 136), (98, 110, 52),
       (160, 44, 46), (54, 78, 150), (190, 170, 120), (70, 70, 80)]


_GM_PAL = {}


def garbage_mountain(wire=True):
    p = Paint(base="#0a0c1c", seed=21)
    rng = np.random.default_rng(3)
    # --- cavernous hangar: dark top, bluish haze at the horizon
    p.fill(p.m_rect(0, 0, W, 90), p.lin(0, 0, 0, 90, "#050612", "#2c2e58"))
    for x in range(10, W, 64):                                   # colossal ribs
        rib = p.m_poly([(x, 0), (x + 10, 0), (x + 16, 80), (x + 4, 80)])
        p.shade(rib, "#101428", 1.0, 0.6, tex=0.1, seed=3)
        p.edge(rib, (140, 150, 220), 0.18, "left")
    p.fill(p.m_rect(0, 22, W, 27), (12, 14, 32), 0.9)
    p.fill(p.m_rect(0, 23, W, 24), (110, 120, 190), 0.18)
    for x, y, c in [(36, 14, (255, 210, 70)), (150, 8, (255, 200, 60)), (284, 12, (255, 210, 70)), (222, 30, (255, 90, 60))]:
        p.glow(x, y, 26, c, 0.55)
        p.fill(p.m_rect(x - 1, y - 1, x + 2, y + 2), (255, 240, 180))
    p.multiply(0.85 + 0.3 * p.noise(30, 3, 2), 0.35)
    # --- solid masses of rubble first, so the piles have bulk
    def hill(pts, c_hi, c_lo, seed):
        m = p.m_poly(pts)
        p.fill(m, p.lin(0, min(q[1] for q in pts), 0, 112, c_hi, c_lo))
        p.multiply(0.75 + 0.5 * p.noise(7, 3, seed), 0.5)
    hill([(0, 76), (24, 62), (60, 70), (96, 56), (140, 64), (190, 48), (240, 60), (280, 50), (320, 62), (320, 112), (0, 112)], "#46486e", "#232644", 1)
    hill([(0, 90), (40, 78), (90, 84), (150, 70), (210, 82), (260, 72), (320, 84), (320, 112), (0, 112)], "#5a4650", "#2a1f26", 2)
    haze = (52, 54, 100)
    debris(p, rng, 0, W, 56, 84, 70, (7, 15), haze, 0.65, PAL)
    debris(p, rng, 0, W, 72, 102, 90, (8, 20), haze, 0.35, PAL)
    # --- ground
    p.fill(p.m_rect(0, 104, W, H), p.lin(0, 104, 0, H, "#463a34", "#17110f"))
    p.multiply(0.6 + 0.8 * p.noise(5, 3, 9), 0.6)
    p.fill(p.m_rect(0, 104, W, 105), (160, 140, 130), 0.22)
    for k in range(40):                                          # scratches and puddles of light
        x, y = int(rng.integers(0, W)), int(rng.integers(108, H - 2))
        p.fill(p.m_rect(x, y, x + int(rng.integers(4, 18)), y + 1), (20, 14, 12), 0.5)
    debris(p, rng, 0, W, 104, 140, 46, (2, 8), haze, 0.05, PAL)
    # --- escape pod (left)
    pod = p.m_poly([(6, 112), (6, 74), (16, 64), (50, 64), (60, 74), (60, 112)])
    p.shade(pod, "#7e8a98", 1.35, 0.4, tex=0.1, seed=4)
    p.edge(pod, (0, 0, 0), 0.6)
    win = p.m_ell(18, 74, 48, 100)
    p.fill(win, p.radial(33, 87, 16, "#9be4f0", "#1c5c78"))
    p.edge(win, (0, 0, 0), 0.7)
    p.fill(p.m_rect(8, 106, 58, 110), (230, 190, 40), 0.9)
    p.glow(33, 87, 36, (110, 220, 255), 0.25)
    # --- wrecked starfighter cockpit: a dented sphere with a cracked hexagonal window
    ball = p.m_ell(106, 62, 172, 124)
    p.shade(ball, "#7a8090", 1.5, 0.3, tex=0.16, seed=5)
    p.edge(ball, (0, 0, 0), 0.6)
    win = p.m_poly([(124, 80), (154, 78), (162, 98), (150, 114), (126, 112), (118, 96)])
    p.fill(win, p.lin(120, 78, 160, 114, "#2a3c58", "#04060c"))
    p.edge(win, (0, 0, 0), 0.8)
    p.fill(p.m_line(130, 82, 150, 110, 1), (170, 190, 220), 0.35)
    p.fill(p.m_line(144, 80, 124, 100, 1), (170, 190, 220), 0.25)
    p.fill(p.m_line(138, 80, 136, 112, 1), (10, 12, 20), 0.8)
    p.fill(p.m_poly([(104, 86), (112, 82), (114, 100), (102, 104)]), (84, 88, 100))      # bent strut
    p.fill(p.m_poly([(168, 92), (180, 88), (182, 102), (170, 104)]), (96, 100, 112))
    p.glow(139, 100, 40, (255, 120, 60), 0.1, 0.8)
    # --- wire
    if wire:
        p.fill(p.m_line(200, 114, 214, 109, 2), (230, 190, 60))
        p.fill(p.m_line(214, 109, 230, 114, 2), (180, 90, 40))
        p.fill(p.m_line(200, 113, 214, 108, 1), (255, 245, 170), 0.6)
    p.glow(33, 120, 60, (110, 220, 255), 0.12, 0.3)
    img = p.finish(colors=170, vignette=0.5, palette=_GM_PAL.get("q"))
    if "q" not in _GM_PAL:
        _GM_PAL["q"] = p.last_q
    return img


ROOMS = {
    # the locker-open variant goes first: it holds every colour, and the others reuse its palette
    "escape_pod_open": lambda: escape_pod(True, True),
    "escape_pod": lambda: escape_pod(False),
    "escape_pod_open_empty": lambda: escape_pod(True, False),
    "garbage_mountain": lambda: garbage_mountain(True),
    "garbage_mountain_nowire": lambda: garbage_mountain(False),
}

if __name__ == "__main__":
    import sys
    from PIL import Image
    for name, fn in ROOMS.items():
        fn().save(OUT + name + ".png")
        print("wrote", name)
    if len(sys.argv) > 1:
        names = list(ROOMS)
        tiles = [Image.open(OUT + n + ".png").resize((W * 3, H * 3), Image.NEAREST) for n in names[:4]]
        sh = Image.new("RGB", (W * 6, H * 6))
        for i, t in enumerate(tiles):
            sh.paste(t, ((i % 2) * W * 3, (i // 2) * H * 3))
        sh.save(sys.argv[1])
