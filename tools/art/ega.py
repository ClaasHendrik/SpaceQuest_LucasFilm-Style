"""EGA pixel-art toolkit. All room art is painted at 320x132 native and shown at 2x (640x264)."""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 320, 132
EGA = [(0, 0, 0), (0, 0, 170), (0, 170, 0), (0, 170, 170), (170, 0, 0), (170, 0, 170), (170, 85, 0), (170, 170, 170),
       (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255), (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255)]
K, B, G, C, R, M, N, S, DG, LB, LG, LC, LR, LM, Y, WH = range(16)


class Cv:
    def __init__(self, w=W, h=H, bg=K):
        self.w, self.h = w, h
        self.im = Image.new("RGB", (w, h), EGA[bg])
        self.d = ImageDraw.Draw(self.im)
        self.rng = random.Random(7)

    # --- solid primitives
    def rect(self, x0, y0, x1, y1, c):
        self.d.rectangle([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=EGA[c])

    def poly(self, pts, c):
        self.d.polygon(pts, fill=EGA[c])

    def line(self, x0, y0, x1, y1, c, w=1):
        self.d.line([x0, y0, x1, y1], fill=EGA[c], width=w)

    def ell(self, x0, y0, x1, y1, c):
        self.d.ellipse([x0, y0, x1, y1], fill=EGA[c])

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.im.putpixel((x, y), EGA[c])

    # --- dithered fills (checkerboard through a mask)
    def _checker(self, c1, c2, phase=0):
        p = Image.new("RGB", (self.w, self.h), EGA[c1])
        pp = p.load()
        for y in range(self.h):
            for x in range(self.w):
                if (x + y + phase) % 2:
                    pp[x, y] = EGA[c2]
        return p

    def dpoly(self, pts, c1, c2, phase=0):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon(pts, fill=255)
        self.im.paste(self._checker(c1, c2, phase), mask=m)

    def drect(self, x0, y0, x1, y1, c1, c2, phase=0):
        self.dpoly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], c1, c2, phase)

    def dell(self, x0, y0, x1, y1, c1, c2, phase=0):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).ellipse([x0, y0, x1, y1], fill=255)
        self.im.paste(self._checker(c1, c2, phase), mask=m)

    def vgrad(self, x0, y0, x1, y1, cols):
        """vertical banded gradient with dithered seams"""
        n = len(cols)
        hh = y1 - y0 + 1
        for i, c in enumerate(cols):
            ya = y0 + hh * i // n
            yb = y0 + hh * (i + 1) // n - 1
            self.rect(x0, ya, x1, yb, c)
            if i + 1 < n:
                self.drect(x0, max(y0, yb - 2), x1, min(y1, yb + 2), c, cols[i + 1])

    def stars(self, x0, y0, x1, y1, n, cols=(WH, S, LB, LC, Y)):
        for _ in range(n):
            self.px(self.rng.randint(x0, x1), self.rng.randint(y0, y1), self.rng.choice(cols))

    def text(self, x, y, s, c, size=8):
        f = ImageFont.load_default(size)
        self.d.fontmode = "1"
        self.d.text((x, y), s, font=f, fill=EGA[c])

    # --- composite helpers
    def box3d(self, x0, y0, x1, y1, face, light, dark):
        self.rect(x0, y0, x1, y1, face)
        self.line(x0, y0, x1, y0, light)
        self.line(x0, y0, x0, y1, light)
        self.line(x0, y1, x1, y1, dark)
        self.line(x1, y0, x1, y1, dark)

    def girders(self, x0, y0, x1, y1, c, step=12):
        self.rect(x0, y0, x1, y1, c)
        for x in range(x0, x1, step):
            self.line(x, y0, min(x + step, x1), y1, K)
            self.line(min(x + step, x1), y0, x, y1, K)

    def save(self, path, scale=1):
        im = self.im if scale == 1 else self.im.resize((self.w * scale, self.h * scale), Image.NEAREST)
        im.save(path)
