"""Hand-painted touch-ups that go over the restyled pictures where the original shows a figure (Roger): instead of patching with
copied pixels, the area is repainted as a proper object that fits its surroundings. Coordinates are in picture pixels (320x160)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def _mask(size, pts):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.asarray(m) > 127


def _grad(a, mask, y0, y1, c0, c1):
    h, w = mask.shape
    yy = np.arange(h)[:, None].repeat(w, 1).astype(np.float32)
    t = np.clip((yy - y0) / max(1.0, y1 - y0), 0, 1)[..., None]
    col = np.asarray(c0, np.float32) + (np.asarray(c1, np.float32) - np.asarray(c0, np.float32)) * t
    a[mask] = col[mask]


def crash_site(img):
    """the pod's cockpit window: a glass pane in a dark frame, lit from the top left, with a reflection streak"""
    a = np.asarray(img.convert("RGB")).astype(np.float32).copy()
    size = img.size
    pane = [(125, 77), (141, 74), (155, 77), (156, 90), (148, 96), (129, 97), (123, 90)]
    inner = _mask(size, pane)
    frame = _mask(size, [(123, 75), (141, 72), (157, 75), (158, 92), (149, 98), (128, 99), (121, 91)])
    a[frame & ~inner] = (14, 18, 36)                                   # the dark frame around the pane
    _grad(a, inner, 74, 97, (150, 236, 244), (30, 140, 156))           # glass: light at the top, deep teal at the bottom
    h, w = inner.shape
    yy, xx = np.mgrid[0:h, 0:w]
    streak = inner & (np.abs((xx - 126) - (yy - 75) * 0.85 - 4) < 1.6)
    a[streak] = np.minimum(255, a[streak] * 0.5 + 255 * 0.5)          # a diagonal reflection
    streak2 = inner & (np.abs((xx - 136) - (yy - 75) * 0.85 - 4) < 0.8)
    a[streak2] = np.minimum(255, a[streak2] * 0.7 + 255 * 0.3)
    rim_top = inner & ~_mask(size, [(125, 78), (141, 75), (155, 78), (155, 90), (148, 95), (129, 96), (124, 90)])
    a[rim_top] *= 0.72                                                 # a soft shaded rim inside the glass edge
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def _arch(d, cx, base_y, half_w, height, fill=None, outline=None, width=1):
    """an arch (a rectangle with a round top) centred on cx, standing on base_y"""
    r = half_w
    top = base_y - height
    box_top = top + r
    if fill is not None:
        d.rectangle([cx - half_w, box_top, cx + half_w, base_y], fill=fill)
        d.ellipse([cx - half_w, top, cx + half_w, top + 2 * r], fill=fill)
    if outline is not None:
        d.arc([cx - half_w, top, cx + half_w, top + 2 * r], 180, 360, fill=outline, width=width)
        d.line([cx - half_w, box_top, cx - half_w, base_y], fill=outline, width=width)
        d.line([cx + half_w, box_top, cx + half_w, base_y], fill=outline, width=width)


def tube_entrance(img):
    """the empty left arch: a tunnel that recedes into the dark in nested arch ribs towards a faint far light. Crisp edges, a few
    flat shades, lit on the left. Only the opening is painted; the ground in front of it is the original floor."""
    a = np.asarray(img.convert("RGB")).astype(np.float32).copy()
    size = img.size
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cx, base = 59, 124
    outer = Image.new("RGB", size, (0, 0, 0))
    d = ImageDraw.Draw(outer)
    # the tunnel as nested arches, each smaller, higher and lighter than the one before
    steps = [(18, 36, (14, 18, 42)), (15, 30, (20, 24, 54)), (12, 24, (28, 32, 66)), (9, 18, (38, 44, 82)), (6, 12, (52, 60, 104)), (3, 6, (90, 110, 150))]
    mask_all = Image.new("L", size, 0)
    ImageDraw.Draw(mask_all).rectangle([cx - 18, base - 36 + 18, cx + 18, base], fill=255)
    ImageDraw.Draw(mask_all).ellipse([cx - 18, base - 36, cx + 18, base - 36 + 36], fill=255)
    for k, (hw, ht, col) in enumerate(steps):
        by = base - k * 2                                    # each rib stands a little higher: the floor rises towards the far end
        _arch(d, cx, by, hw, ht, fill=col)
        _arch(d, cx - 1, by, hw, ht, outline=tuple(min(255, int(c * 1.5)) for c in col))   # a lit left edge on every rib
    inside = np.asarray(mask_all) > 127
    paint = np.asarray(outer).astype(np.float32)
    a[inside] = paint[inside]
    # shade the right wall of the tunnel
    right = inside & (xx > cx + 6)
    a[right] *= 0.8
    # the far light: a small bright slit
    a[(yy >= base - 22) & (yy <= base - 19) & (xx >= cx - 2) & (xx <= cx + 2)] = (170, 200, 230)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


TOUCHUPS = {"crash_site": crash_site, "tube_entrance": tube_entrance}
