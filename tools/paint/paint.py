"""Painterly toolkit for 320x144 scenes: float canvas, gradients, lighting, noise, glow, then a 256-colour VGA-style finish."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 320, 144


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def mix(a, b, t):
    return a + (b - a) * t


class Paint:
    def __init__(self, w=W, h=H, base="#000000", seed=5):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 3), np.float32)
        self.a[:] = rgb(base) if isinstance(base, str) else base
        self.rng = np.random.default_rng(seed)
        self.yy, self.xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self.gn = None

    # ---------------------------------------------------------------- masks
    def m_poly(self, pts):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
        return np.asarray(m) > 127

    def m_rect(self, x0, y0, x1, y1):
        m = np.zeros((self.h, self.w), bool)
        m[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = True
        return m

    def m_ell(self, x0, y0, x1, y1):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).ellipse([x0, y0, x1, y1], fill=255)
        return np.asarray(m) > 127

    def m_line(self, x0, y0, x1, y1, width=1):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).line([x0, y0, x1, y1], fill=255, width=width)
        return np.asarray(m) > 127

    # ---------------------------------------------------------------- fields
    def lin(self, x0, y0, x1, y1, c0, c1):
        """linear gradient array from (x0,y0)=c0 to (x1,y1)=c1"""
        dx, dy = x1 - x0, y1 - y0
        t = ((self.xx - x0) * dx + (self.yy - y0) * dy) / max(1e-6, dx * dx + dy * dy)
        t = np.clip(t, 0, 1)[..., None]
        return mix(rgb(c0) if isinstance(c0, str) else c0, rgb(c1) if isinstance(c1, str) else c1, t)

    def radial(self, cx, cy, r, c0, c1, squash=1.0):
        d = np.sqrt(((self.xx - cx) / 1.0) ** 2 + ((self.yy - cy) / squash) ** 2) / r
        t = np.clip(d, 0, 1)[..., None]
        return mix(rgb(c0) if isinstance(c0, str) else c0, rgb(c1) if isinstance(c1, str) else c1, t)

    def noise(self, scale=8, octaves=3, seed=0):
        rng = np.random.default_rng(seed + 100)
        out = np.zeros((self.h, self.w), np.float32)
        amp, tot = 1.0, 0.0
        for o in range(octaves):
            s = max(2, int(scale / (2 ** o)))
            gh, gw = self.h // s + 3, self.w // s + 3
            g = rng.random((gh, gw)).astype(np.float32)
            gi = Image.fromarray((g * 255).astype(np.uint8)).resize((gw * s, gh * s), Image.BICUBIC)
            out += amp * np.asarray(gi, np.float32)[: self.h, : self.w] / 255.0
            tot += amp
            amp *= 0.5
        return out / tot

    # ---------------------------------------------------------------- painting
    def fill(self, mask, color, alpha=1.0):
        c = rgb(color) if isinstance(color, str) else np.asarray(color, np.float32)
        if c.ndim == 1:
            c = np.broadcast_to(c, self.a.shape)
        m = mask[..., None]
        self.a = np.where(m, self.a * (1 - alpha) + c * alpha, self.a)

    def shade(self, mask, color, hi=1.3, lo=0.55, angle=(-1, -1), tex=0.12, seed=1):
        """fill a shape with directional light (top-left by default) and light texture"""
        ys, xs = np.nonzero(mask)
        if len(xs) == 0:
            return
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        ax, ay = angle
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        span = max(1.0, abs(ax) * (x1 - x0) / 2 + abs(ay) * (y1 - y0) / 2)
        t = ((self.xx - cx) * (-ax) + (self.yy - cy) * (-ay)) / (span * 1.0)
        t = np.clip(0.5 + 0.5 * t / (abs(ax) + abs(ay) + 1e-6) * 1.0, 0, 1)
        k = (hi + (lo - hi) * t)[..., None]
        if self.gn is None:
            self.gn = self.noise(5, 2, 77)
        n = (np.roll(self.gn, (seed * 7) % self.h, 0) - 0.5) * 2 * tex
        c = (rgb(color) if isinstance(color, str) else np.asarray(color, np.float32)) * (k + n[..., None])
        self.fill(mask, np.clip(c, 0, 255))

    def edge(self, mask, color, alpha=0.6, side="all", width=1):
        """darken/lighten the rim of a mask (outline or bevel)"""
        m = Image.fromarray((mask * 255).astype(np.uint8))
        er = np.asarray(m.filter(ImageFilter.MinFilter(1 + 2 * width))) > 127
        rim = mask & ~er
        if side == "top":
            rim &= ~np.roll(mask, 1, 0) | ~mask
            rim = mask & ~np.roll(mask, 1, 0)
        elif side == "left":
            rim = mask & ~np.roll(mask, 1, 1)
        elif side == "bottom":
            rim = mask & ~np.roll(mask, -1, 0)
        elif side == "right":
            rim = mask & ~np.roll(mask, -1, 1)
        self.fill(rim, color, alpha)

    def glow(self, cx, cy, r, color, strength=0.6, squash=1.0):
        d = np.sqrt((self.xx - cx) ** 2 + ((self.yy - cy) / squash) ** 2) / r
        f = np.clip(1 - d, 0, 1) ** 2 * strength
        self.a = self.a + f[..., None] * (rgb(color) if isinstance(color, str) else np.asarray(color, np.float32))
        self.a = np.clip(self.a, 0, 255)

    def multiply(self, field, amount=1.0):
        self.a = np.clip(self.a * (1 - amount + amount * field[..., None]), 0, 255)

    def blur_region(self, mask, radius=1.2):
        img = Image.fromarray(np.clip(self.a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius))
        b = np.asarray(img, np.float32)
        self.a = np.where(mask[..., None], b, self.a)

    def stars(self, mask, n, seed=3, bright=1.0):
        rng = np.random.default_rng(seed)
        ys, xs = np.nonzero(mask)
        if len(xs) == 0:
            return
        for i in rng.integers(0, len(xs), n):
            v = rng.random()
            col = np.array([200, 210, 255], np.float32) * (0.35 + 0.65 * v) * bright
            self.a[ys[i], xs[i]] = col

    # ---------------------------------------------------------------- finish
    def finish(self, colors=160, grain=2.0, dither=5.0, vignette=0.0, seed=9, palette=None):
        a = self.a.copy()
        if vignette:
            d = np.sqrt(((self.xx - self.w / 2) / (self.w / 2)) ** 2 + ((self.yy - self.h / 2) / (self.h / 2)) ** 2)
            a *= (1 - vignette * np.clip(d - 0.5, 0, 1) ** 2)[..., None]
        rng = np.random.default_rng(seed)
        a += rng.normal(0, grain, a.shape[:2])[..., None]
        bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16 - 0.5
        a += np.tile(bayer, (self.h // 4 + 1, self.w // 4 + 1))[: self.h, : self.w, None] * dither * 2
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
        if palette is not None:
            q = im.quantize(palette=palette, dither=Image.Dither.NONE)
        else:
            q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        self.last_q = q
        return q.convert("RGB")
