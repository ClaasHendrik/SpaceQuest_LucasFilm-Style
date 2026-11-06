"""Shared painting helpers for all rooms (built on paint.Paint)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from paint import Paint, rgb, mix, W, H
from pilot import pipe_h, bevel, rivets, debris, PAL

FONT = "../../assets/fonts/VT323-Regular.ttf"


def vgrad(p, y0, y1, stops, x0=0, x1=W):
    """multi-stop vertical gradient: stops = [(t, '#hex'), ...] with t in 0..1"""
    m = p.m_rect(x0, y0, x1, y1)
    t = np.clip((p.yy - y0) / max(1, y1 - y0), 0, 1)
    out = np.zeros(p.a.shape, np.float32)
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        seg = np.clip((t - t0) / max(1e-6, t1 - t0), 0, 1)[..., None]
        sel = ((t >= t0) & (t <= t1))[..., None]
        out = np.where(sel, mix(rgb(c0), rgb(c1), seg), out)
    out = np.where((t < stops[0][0])[..., None], rgb(stops[0][1]), out)
    out = np.where((t > stops[-1][0])[..., None], rgb(stops[-1][1]), out)
    p.fill(m, out)


def ridge(p, base_y, amp, c_hi, c_lo, seed=1, step=(10, 26), x0=0, x1=W, bottom=None, tex=0.1):
    """a jagged silhouette (mountains, rubble, cliff line) shaded top to bottom"""
    r = np.random.default_rng(seed)
    bottom = bottom if bottom is not None else base_y + 60
    pts = [(x0, bottom)]
    x = x0
    while x < x1 + 20:
        pts.append((x, base_y + r.uniform(-amp, amp)))
        x += r.uniform(*step)
    pts += [(x1 + 20, bottom)]
    m = p.m_poly(pts)
    p.fill(m, p.lin(0, base_y - amp, 0, bottom, c_hi, c_lo))
    if tex:
        p.multiply(1 - tex + 2 * tex * p.noise(6, 3, seed), 0.8)
    return m


def shaded(p, pts, color, hi=1.3, lo=0.5, seed=1, tex=0.1, edge=0.45):
    m = p.m_poly(pts)
    p.shade(m, color, hi, lo, tex=tex, seed=seed)
    if edge:
        p.edge(m, (0, 0, 0), edge)
    return m


def text(p, x, y, s, color, size=14, alpha=1.0):
    f = ImageFont.truetype(FONT, size)
    im = Image.new("L", (p.w, p.h), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    d.text((x, y), s, font=f, fill=255)
    p.fill(np.asarray(im) > 127, color, alpha)


def floor(p, y0, c_top, c_bot, lines=True, noise_seed=3, perspective=True):
    p.fill(p.m_rect(0, y0, W, H), p.lin(0, y0, 0, H, c_top, c_bot))
    p.multiply(0.75 + 0.5 * p.noise(8, 3, noise_seed), 0.45)
    p.fill(p.m_rect(0, y0, W, y0 + 1), (200, 210, 220), 0.25)
    if lines and perspective:
        for i in range(-12, 32):
            p.fill(p.m_line(160 + i * 18, y0 + 1, 160 + i * 36, H, 1), (0, 0, 0), 0.35)
        for y in (y0 + 8, y0 + 18, y0 + 30):
            if y < H:
                p.fill(p.m_rect(0, y, W, y + 1), (0, 0, 0), 0.3)


def save(p, name, out, colors=190, vignette=0.45, palette=None, grain=2.0):
    img = p.finish(colors=colors, vignette=vignette, palette=palette, grain=grain)
    img.save(out + name + ".png")
    return img
