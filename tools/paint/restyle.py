"""Restyle a 320x190 EGA reference screen into the game's painted style.
Keeps every shape, colour relationship and perspective of the reference, and replaces the dithered EGA look with:
flat colour regions mapped to a softer palette, gentle top-to-bottom light, edge light on the top/left of shapes and
shade on the bottom/right (the Indy VGA way of showing volume), a little texture, and no dither.
Usage: from restyle import restyle; img = restyle("ref/s014.png", rows=160)"""
import numpy as np
from PIL import Image

EGA = [(0, 0, 0), (0, 0, 170), (0, 170, 0), (0, 170, 170), (170, 0, 0), (170, 0, 170), (170, 85, 0), (170, 170, 170),
       (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255), (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255)]
# softer, more naturalistic palette for each EGA colour (keeps the hue family of the original)
SOFT = {
    0: (10, 12, 26), 1: (30, 44, 152), 2: (46, 158, 74), 3: (40, 160, 170), 4: (170, 46, 48), 5: (158, 52, 160),
    6: (166, 108, 58), 7: (176, 180, 190), 8: (100, 104, 120), 9: (84, 112, 238), 10: (112, 228, 118), 11: (128, 228, 238),
    12: (244, 104, 96), 13: (232, 118, 228), 14: (246, 226, 100), 15: (246, 249, 255),
}
PAIRS = [(a, b) for a in range(16) for b in range(a + 1, 16)]


def load_indices(path, top=10, height=190):
    a = np.asarray(Image.open(path).convert("RGB"))[top:top + height]
    pal = np.array(EGA)
    d = ((a[:, :, None, :].astype(int) - pal[None, None]) ** 2).sum(-1)
    return d.argmin(-1)


def dedither(idx):
    """label map: 0..15 = pure colours, 16.. = a dithered mix of two colours"""
    h, w = idx.shape
    pal = np.array(EGA, np.float32)
    rgb = pal[idx]
    pad = np.pad(rgb, ((0, 1), (0, 1), (0, 0)), mode="edge")
    mean = (pad[:-1, :-1] + pad[1:, :-1] + pad[:-1, 1:] + pad[1:, 1:]) / 4.0
    cand = [pal[i] for i in range(16)] + [(pal[a] + pal[b]) / 2 for a, b in PAIRS]
    cand = np.array(cand, np.float32)
    d = ((mean[:, :, None, :] - cand[None, None]) ** 2).sum(-1)
    d[:, :, 16:] += 40.0               # prefer pure colours when nearly equal
    lab = d.argmin(-1)
    # a mixed label is only real inside a mixed area: isolated mixed pixels along edges are removed
    for _ in range(3):
        mixed = lab >= 16
        same = np.zeros_like(lab)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                sh = np.roll(np.roll(lab, dy, 0), dx, 1)
                same += (sh == lab)
        bad = mixed & (same < 6)
        if not bad.any():
            break
        fill = idx.copy()
        lab = np.where(bad, fill, lab)
    # mixed labels must also follow their own two colours: snap pixels whose neighbours disagree back to the source colour
    return lab


def soft_color(label):
    if label < 16:
        return np.array(SOFT[label], np.float32)
    a, b = PAIRS[label - 16]
    return (np.array(SOFT[a], np.float32) + np.array(SOFT[b], np.float32)) / 2


def components(lab):
    h, w = lab.shape
    comp = -np.ones((h, w), np.int32)
    n = 0
    for y in range(h):
        for x in range(w):
            if comp[y, x] >= 0:
                continue
            stack = [(y, x)]
            comp[y, x] = n
            v = lab[y, x]
            while stack:
                cy, cx = stack.pop()
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < h and 0 <= nx < w and comp[ny, nx] < 0 and lab[ny, nx] == v:
                        comp[ny, nx] = n
                        stack.append((ny, nx))
            n += 1
    return comp, n


def erase_boxes(lab, boxes, top=10):
    """paint figures out of the background: each box (x0, y0, x1, y1 in 320x200 screen coordinates) is refilled row by
    row from the labels just outside it (left half from the left, right half from the right, flat if both agree)"""
    h, w = lab.shape
    for (x0, y0, x1, y1) in boxes:
        y0, y1 = max(0, y0 - top), min(h - 1, y1 - top)
        xa, xb = max(0, x0 - 1), min(w - 1, x1 + 1)
        for y in range(y0, y1 + 1):
            l, r = lab[y, xa], lab[y, xb]
            if l == r:
                lab[y, x0:x1 + 1] = l
            else:
                mid = (x0 + x1) // 2
                lab[y, x0:mid + 1] = l
                lab[y, mid + 1:x1 + 1] = r
    return lab


def restyle(path, rows=160, top=10, height=190, seed=3, light=0.07, edge=0.12, grain=0.3, texture=0.012, erase=(), volume=0.26, bands=5, colors=112, donor=None):
    idx = load_indices(path, top, height)
    lab = dedither(idx)
    if donor is not None and erase:
        # the same scene without the figure: copy the labels from there instead of guessing them
        dlab = dedither(load_indices(donor, top, height))
        for (x0, y0, x1, y1) in erase:
            lab[max(0, y0 - top):y1 - top + 1, x0:x1 + 1] = dlab[max(0, y0 - top):y1 - top + 1, x0:x1 + 1]
    else:
        lab = erase_boxes(lab, erase, top)
    # resample rows (the picture is squeezed vertically to fit the game's picture area)
    ys = np.minimum(((np.arange(rows) + 0.5) * height / rows).astype(int), height - 1)
    lab = lab[ys]
    h, w = lab.shape
    base = np.zeros((h, w, 3), np.float32)
    for v in np.unique(lab):
        base[lab == v] = soft_color(int(v))
    comp, n = components(lab)
    out = base.copy()
    yy = np.arange(h)[:, None].repeat(w, 1)
    # per-region light: a banded gradient from top to bottom, stronger on big surfaces
    for c in range(n):
        m = comp == c
        cnt = m.sum()
        if cnt < 60:
            continue
        ys_, xs_ = np.nonzero(m)
        y0, y1 = ys_.min(), ys_.max()
        if y1 - y0 < 6:
            continue
        amp = light * (2.2 if cnt > 1500 else 1.0)
        t = (yy - y0) / max(1, y1 - y0)
        tq = (np.floor(np.clip(t, 0, 0.999) * bands) + 0.5) / bands            # banded, as in the reference frames
        out[m] = out[m] * (1 + amp * (0.5 - tq))[m][:, None]
    # volume: each shape is lit from the top left, so its top/left rim brightens and its bottom/right rim darkens,
    # rounded over a few pixels; lit areas turn slightly warm, shaded areas slightly cool
    lit_total = np.zeros((h, w), np.float32)
    for c in range(n):
        m = comp == c
        cnt = m.sum()
        if cnt < 40 or lab[m][0] == 0:
            continue
        mf = m.astype(np.float32)
        bl = box_blur(box_blur(mf, 2), 2)
        gy, gx = np.gradient(bl)
        lit = 0.7071 * (gx + gy)
        mx = np.abs(lit).max()
        if mx <= 0:
            continue
        lit = lit / mx
        lit_total = np.where(m, lit, lit_total)
    k = np.where(lit_total > 0, 1 + volume * lit_total, 1 + volume * 0.8 * lit_total)
    k = np.clip(k, 0.72, 1.2)
    out = out * k[..., None]
    out[..., 0] *= 1 + 0.05 * lit_total
    out[..., 2] *= 1 - 0.05 * lit_total
    # edge light between neighbouring shapes
    L = lum(base)
    def shifted(arr, dy, dx):
        return np.roll(np.roll(arr, dy, 0), dx, 1)
    for (dy, dx, sign) in ((1, 0, +1), (0, 1, +1), (-1, 0, -1), (0, -1, -1)):
        nb_comp = shifted(comp, dy, dx)
        nb_L = shifted(L, dy, dx)
        diff = (nb_comp != comp) & (np.abs(nb_L - L) > 14)
        if sign > 0:
            sel = diff & (nb_L < L)
            out = np.where(sel[..., None], out * (1 + edge), out)
        else:
            sel = diff & (nb_L > L)
            out = np.where(sel[..., None], out * (1 - edge * 0.8), out)
    # texture and grain
    rng = np.random.default_rng(seed)
    out = out * (1 + (rng.random((h, w, 1)) - 0.5) * 2 * texture)
    out = out + rng.normal(0, grain, (h, w, 1))
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")
    return img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")


def box_blur(a, r):
    k = 2 * r + 1
    p = np.pad(a, r, mode="edge")
    c = np.cumsum(np.pad(p, ((0, 0), (1, 0))), axis=1)
    p = (c[:, k:] - c[:, :-k]) / k
    c = np.cumsum(np.pad(p, ((1, 0), (0, 0))), axis=0)
    return (c[k:] - c[:-k]) / k


def lum(rgb):
    return rgb[..., 0] * 0.3 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11
