"""Roger Wilco sprite sheet, painted at 8x then reduced: 5 frames of 28x52 in his original outfit (grey jumpsuit, magenta sleeves, red belt),
each outfit: stand, walk1..walk4. Right-facing; the game flips for left."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

LW, LH = 28, 52          # logical drawing size
FW, FH = 16, 30          # final sprite size (about 21% of the scene height at 2x)
S = 8
SKIN, SKIN_D, SKIN_L = (238, 168, 148), (192, 118, 106), (252, 206, 188)
TROUSER = ((150, 154, 166), (98, 102, 116), (196, 200, 212))
SLEEVE = ((186, 38, 176), (118, 20, 112), (238, 112, 228))
GREY_T, GREY_D, GREY_L = (176, 180, 190), (120, 124, 138), (216, 220, 228)
BELT = (30, 30, 38)          # black belt (seen at full size in the pathfinding video), with a grey pouch
BOOT = (22, 22, 30)          # tall black boots
HAIR, HAIR_D, HAIR_L = (158, 78, 38), (104, 46, 24), (214, 122, 62)
OUTLINE = (34, 22, 26)


def limb(d, p0, p1, w, base, dark, light):
    (x0, y0), (x1, y1) = [(a * S, b * S) for a, b in (p0, p1)]
    r = w * S / 2
    for off, col, rr in ((0.7 * S * 0.5, dark, r), (0, base, r * 0.86), (-0.9 * S * 0.5, light, r * 0.34)):
        d.line([x0 + off, y0 + off * 0.3, x1 + off, y1 + off * 0.3], fill=col, width=int(2 * rr))
        d.ellipse([x0 + off - rr, y0 + off * 0.3 - rr, x0 + off + rr, y0 + off * 0.3 + rr], fill=col)
        d.ellipse([x1 + off - rr, y1 + off * 0.3 - rr, x1 + off + rr, y1 + off * 0.3 + rr], fill=col)


def poly(d, pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


def fk(hip, t1, bend, l1=9.0, l2=9.0):
    knee = (hip[0] + l1 * math.sin(t1), hip[1] + l1 * math.cos(t1))
    t2 = t1 - bend
    foot = (knee[0] + l2 * math.sin(t2), knee[1] + l2 * math.cos(t2))
    return knee, foot


def frame(outfit, f, pose=None):
    img = Image.new("RGBA", (LW * S, LH * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    phase = [None, 0.0, 0.25, 0.5, 0.75][f]
    if phase is None:
        a_f, a_b, bend_f, bend_b, swing, bob = 0.06, -0.06, 0.0, 0.0, 0.0, 0.0
    else:
        s = math.sin(phase * 2 * math.pi)
        c = math.cos(phase * 2 * math.pi)
        a_f, a_b = 0.52 * s, -0.52 * s
        bend_f = 0.9 * max(0, c) * 1.0 if s < 0.3 else 0.0
        bend_b = 0.9 * max(0, -c) if s > -0.3 else 0.0
        if c > 0:
            bend_b = 0.0
        else:
            bend_f = 0.0
        swing = 0.5 * s
        bob = 0.9 * abs(c)
    if pose in ("r1", "r2", "r3"):          # pick-up gesture: arm out, then a crouch with the arm down
        a_f, a_b, bend_f, bend_b, swing = (0.06, -0.06, 0.0, 0.0, 0.0) if pose == "r1" else (0.9, 0.5, 1.5, 1.5, 0.0)
        bob = 0.0 if pose == "r1" else -5.0
    base_y = 50.0
    hip = (13.0, 31.0 - bob)
    uniform = outfit == 1
    leg_col = TROUSER
    shoe = BOOT
    # back leg and arm first
    for a, b, back in ((a_b, bend_b, True), (a_f, bend_f, False)):
        if back:
            col = tuple(int(v * 0.8) for v in leg_col[0]), tuple(int(v * 0.8) for v in leg_col[1]), leg_col[2]
        else:
            col = leg_col
        knee, foot = fk(hip, a, b)
        foot = (foot[0], min(foot[1], base_y - 1))
        limb(d, hip, knee, 5.2, *col)
        limb(d, knee, foot, 4.4, *col)
        limb(d, (foot[0] - 0.5, foot[1] - 0.5), (foot[0] + 2.6, foot[1] + 0.5), 3.2, shoe, tuple(int(v * 0.6) for v in shoe), tuple(min(255, int(v * 1.3)) for v in shoe))
        if back:
            # back arm
            sh = (12.0, 17.5 - bob)
            elb = (sh[0] - 2.5 * math.sin(swing + 0.3) * -1, sh[1] + 6.5)
            hand = (elb[0] - 2.0 * math.sin(swing) * -1, elb[1] + 6.0)
            acol = tuple(tuple(int(v * 0.82) for v in c) for c in SLEEVE)
            limb(d, sh, elb, 3.6, *acol)
            limb(d, elb, hand, 3.2, *acol)
            limb(d, hand, (hand[0] + 0.4, hand[1] + 1.0), 2.6, SKIN_D, SKIN_D, SKIN)
    # torso
    torso = [(8.5, 16.2 - bob), (17.5, 16.2 - bob), (17.0, 31.5 - bob), (9.0, 31.5 - bob)]
    poly(d, torso, GREY_T)
    poly(d, [(15.0, 17 - bob), (17.5, 16.2 - bob), (17.0, 31.5 - bob), (14.4, 31.5 - bob)], GREY_D)           # shaded side
    poly(d, [(9.4, 17 - bob), (10.6, 17 - bob), (10.4, 31 - bob), (9.2, 31 - bob)], GREY_L)                   # lit edge
    poly(d, [(8.5, 16.2 - bob), (17.5, 16.2 - bob), (17.2, 18.0 - bob), (8.8, 18.0 - bob)], GREY_D)           # collar
    poly(d, [(8.9, 28.4 - bob), (17.0, 28.4 - bob), (17.0, 30.6 - bob), (8.9, 30.6 - bob)], BELT)             # red belt
    poly(d, [(9.4, 29.6 - bob), (12.4, 29.6 - bob), (12.4, 33.4 - bob), (9.4, 33.4 - bob)], (150, 154, 166))   # pouch on the hip
    poly(d, [(9.4, 29.6 - bob), (12.4, 29.6 - bob), (12.4, 30.6 - bob), (9.4, 30.6 - bob)], (96, 100, 114))
    poly(d, [(12.6, 18.0 - bob), (13.4, 18.0 - bob), (13.4, 28.4 - bob), (12.6, 28.4 - bob)], GREY_D)         # zip line
    # neck, head, hair
    poly(d, [(11.4, 13.5 - bob), (14.6, 13.5 - bob), (14.8, 16.6 - bob), (11.2, 16.6 - bob)], SKIN_D)
    hx, hy = 13.4, 8.2 - bob
    # the head: a flatter forehead (a nearly straight front) and a squarer jaw, not an egg
    poly(d, [(hx - 5.4, hy - 1.0), (hx - 4.6, hy - 5.2), (hx - 1.0, hy - 6.2), (hx + 3.0, hy - 5.8), (hx + 4.8, hy - 4.2), (hx + 5.0, hy + 0.5),
             (hx + 4.6, hy + 4.0), (hx + 2.4, hy + 5.8), (hx - 2.2, hy + 6.0), (hx - 4.8, hy + 3.8)], SKIN)
    poly(d, [(hx + 0.6, hy - 5.4), (hx + 3.0, hy - 5.4), (hx + 4.6, hy - 4.0), (hx + 4.8, hy + 0.5), (hx + 4.4, hy + 3.8), (hx + 1.0, hy + 5.2)], SKIN_L)
    d.ellipse([(hx + 4.6) * S, (hy - 0.2) * S, (hx + 6.0) * S, (hy + 1.8) * S], fill=SKIN)   # a small nose
    poly(d, [(hx - 6.2, hy - 1), (hx - 5.2, hy - 5.6), (hx - 1.0, hy - 7.6), (hx + 4.2, hy - 6.6), (hx + 5.6, hy - 3.6),
             (hx + 1.6, hy - 4.6), (hx - 2.0, hy - 3.4), (hx - 3.4, hy + 0.6), (hx - 4.6, hy + 3.4)], HAIR)
    poly(d, [(hx - 5.6, hy - 3), (hx - 1.0, hy - 7.2), (hx + 3.0, hy - 6.4), (hx - 1.0, hy - 5.4)], HAIR_L)
    poly(d, [(hx - 6.0, hy), (hx - 4.4, hy + 3.8), (hx - 3.0, hy + 1.0)], HAIR_D)
    d.ellipse([(hx + 2.2) * S, (hy - 1.2) * S, (hx + 4.2) * S, (hy + 0.9) * S], fill=(250, 250, 250))   # eye
    d.ellipse([(hx + 3.0) * S, (hy - 0.9) * S, (hx + 4.2) * S, (hy + 0.7) * S], fill=(24, 24, 40))
    d.line([(hx + 2.0) * S, (hy - 2.0) * S, (hx + 4.8) * S, (hy - 2.2) * S], fill=HAIR_D, width=int(0.7 * S))     # brow
    d.line([(hx + 2.8) * S, (hy + 3.2) * S, (hx + 4.6) * S, (hy + 3.0) * S], fill=SKIN_D, width=int(0.6 * S))     # mouth
    d.ellipse([(hx - 3.0) * S, (hy + 0.2) * S, (hx - 1.2) * S, (hy + 2.6) * S], fill=SKIN_D)                          # ear
    # front arm over the torso
    sh = (13.4, 17.5 - bob)
    elb = (sh[0] + 2.2 * math.sin(-swing), sh[1] + 6.5)
    hand = (elb[0] + 2.4 * math.sin(-swing * 1.2) + 0.5, elb[1] + 6.0)
    if pose == "r1":
        elb, hand = (sh[0] + 3.6, sh[1] + 3.4), (sh[0] + 8.0, sh[1] + 4.6)
    elif pose == "r2":
        elb, hand = (sh[0] + 3.0, sh[1] + 6.0), (sh[0] + 7.2, sh[1] + 12.0)
    elif pose == "r3":
        elb, hand = (sh[0] + 3.2, sh[1] + 5.4), (sh[0] + 6.4, sh[1] + 10.0)
    acol = SLEEVE
    limb(d, sh, elb, 3.8, *acol)
    limb(d, elb, hand, 3.3, *acol)
    limb(d, hand, (hand[0] + 0.5, hand[1] + 1.2), 2.8, SKIN, SKIN_D, SKIN_L)
    return finalize(img)


def finalize(img):
    # --- reduce: coverage-weighted box filter, hard alpha edge, dark rim outline
    arr = np.asarray(img, np.float32)
    a = arr[..., 3] / 255.0
    rgb = arr[..., :3] * a[..., None]
    pm = np.dstack([rgb, a * 255.0]).astype(np.float32)
    # area-average the premultiplied image down to the final size
    ys = np.linspace(0, LH * S, FH + 1).astype(int)
    xs = np.linspace(0, LW * S, FW + 1).astype(int)
    a_s = np.zeros((FH, FW), np.float32)
    rgb_s = np.zeros((FH, FW, 3), np.float32)
    for j in range(FH):
        for i in range(FW):
            blk = pm[ys[j]:ys[j + 1], xs[i]:xs[i + 1]]
            a_s[j, i] = blk[..., 3].mean() / 255.0
            rgb_s[j, i] = blk[..., :3].mean((0, 1)) / 255.0
    col = np.where(a_s[..., None] > 0, rgb_s * 255.0 / np.maximum(a_s[..., None], 1e-4) , 0)
    col = np.clip(col, 0, 255)
    opaque = a_s >= 0.5
    out = np.zeros((FH, FW, 4), np.uint8)
    out[opaque, :3] = np.clip(col[opaque], 0, 255).astype(np.uint8)
    out[opaque, 3] = 255
    m = Image.fromarray((opaque * 255).astype(np.uint8))
    dil = np.asarray(m.filter(ImageFilter.MaxFilter(3))) > 127
    rim = dil & ~opaque
    out[rim] = (*OUTLINE, 255)
    # darken inner edge pixels slightly for definition
    er = np.asarray(m.filter(ImageFilter.MinFilter(3))) > 127
    inner = opaque & ~er
    out[inner, :3] = (out[inner, :3] * 0.82).astype(np.uint8)
    return Image.fromarray(out, "RGBA")



def _figure_front(f, back=False):
    """front or back view: symmetric legs and arms, face (or hair only for the back)"""
    img = Image.new("RGBA", (LW * S, LH * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ph = [0, 1, 0, 2, 0][f]
    bob = 0.0 if f == 0 else 0.7
    cx = 14.0
    sw = [0.0, -1.2, 0.0, 1.2, 0.0][f]
    hip = 31.0 - bob
    for side, px in ((-1, cx - 2.6), (1, cx + 2.6)):
        lift = 2.4 if (ph == 1 and side == -1) or (ph == 2 and side == 1) else 0.0
        bot = 50.0 - lift
        limb(d, (px, hip), (px, bot - 4.5), 4.6, *TROUSER)
        poly(d, [(px - 2.7, bot - 5.5), (px + 2.7, bot - 5.5), (px + 3.1, bot), (px - 3.1, bot)], BOOT)
        poly(d, [(px - 2.7, bot - 5.5), (px - 1.2, bot - 5.5), (px - 1.4, bot - 0.5), (px - 2.9, bot)], (48, 48, 62))
    for side in (-1, 1):
        sx = cx + side * 6.4
        sh_y = 17.6 - bob
        sw_ = sw * side
        limb(d, (sx, sh_y), (sx + side * 0.6, sh_y + 6.5 + sw_ * 0.4), 3.8, *SLEEVE)
        limb(d, (sx + side * 0.6, sh_y + 6.5 + sw_ * 0.4), (sx + side * 0.9, sh_y + 12.0 + sw_), 3.3, *SLEEVE)
        limb(d, (sx + side * 0.9, sh_y + 11.6 + sw_), (sx + side * 0.9, sh_y + 13.4 + sw_), 2.8, SKIN, SKIN_D, SKIN_L)
    poly(d, [(cx - 6.6, 16.2 - bob), (cx + 6.6, 16.2 - bob), (cx + 6.2, 31.5 - bob), (cx - 6.2, 31.5 - bob)], GREY_T)
    poly(d, [(cx + 2.4, 16.8 - bob), (cx + 6.6, 16.2 - bob), (cx + 6.2, 31.5 - bob), (cx + 2.0, 31.5 - bob)], GREY_D)
    poly(d, [(cx - 6.2, 17.0 - bob), (cx - 4.6, 17.0 - bob), (cx - 4.8, 31.0 - bob), (cx - 6.1, 31.0 - bob)], GREY_L)
    if not back:
        poly(d, [(cx - 3.0, 16.4 - bob), (cx - 1.0, 16.4 - bob), (cx - 1.4, 28.4 - bob), (cx - 2.8, 28.4 - bob)], SLEEVE[0])
    poly(d, [(cx - 6.6, 16.2 - bob), (cx + 6.6, 16.2 - bob), (cx + 6.4, 18.2 - bob), (cx - 6.4, 18.2 - bob)], GREY_D)
    poly(d, [(cx - 6.2, 28.4 - bob), (cx + 6.2, 28.4 - bob), (cx + 6.2, 30.6 - bob), (cx - 6.2, 30.6 - bob)], BELT)
    if not back:
        poly(d, [(cx + 3.4, 29.4 - bob), (cx + 6.2, 29.4 - bob), (cx + 6.2, 33.0 - bob), (cx + 3.4, 33.0 - bob)], (150, 154, 166))
    poly(d, [(cx - 2.2, 13.6 - bob), (cx + 2.2, 13.6 - bob), (cx + 2.4, 16.8 - bob), (cx - 2.4, 16.8 - bob)], SKIN_D)
    hy = 8.2 - bob
    if back:
        d.ellipse([(cx - 5.4) * S, (hy - 6.0) * S, (cx + 5.4) * S, (hy + 6.2) * S], fill=HAIR)
        d.ellipse([(cx - 4.6) * S, (hy - 5.6) * S, (cx + 1.0) * S, (hy + 1.0) * S], fill=HAIR_L)
        poly(d, [(cx - 5.4, hy + 1.0), (cx + 5.4, hy + 1.0), (cx + 4.2, hy + 5.6), (cx - 4.2, hy + 5.6)], HAIR_D)
        d.ellipse([(cx - 6.4) * S, (hy - 0.6) * S, (cx - 4.6) * S, (hy + 2.4) * S], fill=SKIN_D)
        d.ellipse([(cx + 4.6) * S, (hy - 0.6) * S, (cx + 6.4) * S, (hy + 2.4) * S], fill=SKIN_D)
    else:
        d.ellipse([(cx - 5.2) * S, (hy - 6.0) * S, (cx + 5.2) * S, (hy + 6.0) * S], fill=SKIN)
        d.ellipse([(cx - 4.6) * S, (hy - 5.4) * S, (cx + 1.0) * S, (hy + 5.8) * S], fill=SKIN_L)
        poly(d, [(cx - 5.8, hy + 0.6), (cx - 5.4, hy - 5.4), (cx - 1.5, hy - 7.6), (cx + 3.5, hy - 7.0), (cx + 5.6, hy - 4.6), (cx + 5.8, hy + 0.2),
                 (cx + 4.4, hy - 3.6), (cx + 0.5, hy - 4.6), (cx - 3.0, hy - 3.6), (cx - 4.6, hy - 0.5)], HAIR)
        poly(d, [(cx - 4.6, hy - 5.4), (cx - 1.0, hy - 7.2), (cx + 2.5, hy - 6.4), (cx - 1.0, hy - 5.0)], HAIR_L)
        for ex in (-2.6, 1.6):
            d.ellipse([(cx + ex) * S, (hy - 0.8) * S, (cx + ex + 1.8) * S, (hy + 1.0) * S], fill=(250, 250, 250))
            d.ellipse([(cx + ex + 0.4) * S, (hy - 0.5) * S, (cx + ex + 1.4) * S, (hy + 0.8) * S], fill=(24, 24, 40))
        d.line([(cx - 3.0) * S, (hy - 1.8) * S, (cx - 0.8) * S, (hy - 2.0) * S], fill=HAIR_D, width=int(0.7 * S))
        d.line([(cx + 0.8) * S, (hy - 2.0) * S, (cx + 3.0) * S, (hy - 1.8) * S], fill=HAIR_D, width=int(0.7 * S))
        d.line([(cx - 1.0) * S, (hy + 3.4) * S, (cx + 1.0) * S, (hy + 3.4) * S], fill=SKIN_D, width=int(0.6 * S))
        d.ellipse([(cx - 0.6) * S, (hy + 1.2) * S, (cx + 0.6) * S, (hy + 2.6) * S], fill=SKIN_D)
        for ex in (-5.8, 4.4):
            d.ellipse([(cx + ex) * S, (hy - 0.4) * S, (cx + ex + 1.4) * S, (hy + 2.2) * S], fill=SKIN_D)
    return finalize(img)


def build(path):
    """sheet of 16x30 frames: 0-4 side (stand + 4 walk), 5-9 front, 10-14 back, 15-17 pick-up gesture (side)"""
    sheet = Image.new("RGBA", (FW * 18, FH), (0, 0, 0, 0))
    for f in range(5):
        sheet.paste(frame(1, f), (f * FW, 0))
        sheet.paste(_figure_front(f, False), ((5 + f) * FW, 0))
        sheet.paste(_figure_front(f, True), ((10 + f) * FW, 0))
    for k, pz in enumerate(("r1", "r2", "r3")):
        sheet.paste(frame(1, 0, pz), ((15 + k) * FW, 0))
    sheet.save(path)
    return sheet


if __name__ == "__main__":
    sh = build("../../assets/sprites/roger.png")
    bg = Image.new("RGBA", sh.size, (60, 70, 90, 255))
    bg.alpha_composite(sh)
    bg.resize((sh.width * 4, sh.height * 4), Image.NEAREST).save("/tmp/claude-0/-home-user-SpaceQuest-LucasFilm-Style/7db01b00-b598-5261-b0ff-421f4ab3058d/scratchpad/roger_new.png")
