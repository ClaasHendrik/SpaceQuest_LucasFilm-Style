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


ORGANIC_COLOURS = {6, 2}          # brown (rust, rubble) and green (slime): always worn / organic


def classify(lab, comp, n, zones, rows, height=190, top=10):
    """Decide for every region whether it is ORGANIC (rounded, worn, banged up) or ARTIFICIAL (structured, flat, crisp).
    Priority: organic boxes, then flat boxes, then the colour hint (brown / green), then the shape (rectangular = artificial).
    Returns per-region (mode, amp, zone_box): mode is 'organic', 'flat', 'cyl_v' or 'cyl_h'."""
    h, w = lab.shape
    zones = zones or {}
    def to_row(y):
        return (y - top) * rows / height
    org = [(x0, to_row(y0), x1, to_row(y1)) for (x0, y0, x1, y1) in zones.get("organic", [])]
    worn = [(z[0], to_row(z[1]), z[2], to_row(z[3]), set(z[4]) if len(z) > 4 else None) for z in zones.get("worn", [])]
    flat = [(x0, to_row(y0), x1, to_row(y1), mode, amp) for (x0, y0, x1, y1, mode, amp) in zones.get("flat", [])]
    info = {}
    for c in range(n):
        m = comp == c
        cnt = int(m.sum())
        ys_, xs_ = np.nonzero(m)
        cx, cy = xs_.mean(), ys_.mean()
        label = int(lab[m][0])
        colours = {label} if label < 16 else set(PAIRS[label - 16])
        bw, bh = xs_.max() - xs_.min() + 1, ys_.max() - ys_.min() + 1
        fill = cnt / float(bw * bh)
        mode, amp, box = "organic", 0.0, None
        if any(x0 <= cx <= x1 and y0 <= cy <= y1 for (x0, y0, x1, y1) in org):
            pass
        elif any(x0 <= cx <= x1 and y0 <= cy <= y1 and (allowed is None or colours <= allowed) for (x0, y0, x1, y1, allowed) in worn):
            mode = "worn"            # built as a structured object, now dented and roughened by years of use
        else:
            hit = [z for z in flat if z[0] <= cx <= z[2] and z[1] <= cy <= z[3]]
            if hit:
                z = hit[0]
                mode, amp, box = z[4], z[5], (z[0], z[1], z[2], z[3])
            elif colours & ORGANIC_COLOURS:
                pass
            elif cnt >= 150 and fill >= 0.82:
                mode, amp = "flat", 0.05
        info[c] = (mode, amp, box)
    return info


def restyle(path, rows=160, top=10, height=190, seed=3, light=0.07, edge=0.12, grain=0.3, texture=0.012, erase=(), volume=0.26, bands=5, colors=112, donor=None, zones=None, return_class=False):
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
    info = classify(lab, comp, n, zones, rows, height, top)
    class_map = np.zeros((h, w), np.uint8)             # 1 = organic, 2 = artificial
    yy_f = np.arange(h)[:, None].repeat(w, 1).astype(np.float32)
    xx_f = np.arange(w)[None, :].repeat(h, 0).astype(np.float32)
    # per-region light
    for c in range(n):
        m = comp == c
        cnt = m.sum()
        mode, amp_z, box = info[c]
        class_map[m] = {"organic": 1, "worn": 3}.get(mode, 2)
        if cnt < 30 or lab[m][0] == 0:
            continue
        ys_, xs_ = np.nonzero(m)
        y0, y1 = ys_.min(), ys_.max()
        if mode == "organic":
            if y1 - y0 < 6:
                continue
            amp = light * (2.2 if cnt > 1500 else 1.0)
            t = (yy - y0) / max(1, y1 - y0)
        elif mode == "flat":
            amp = amp_z
            t = (yy - y0) / max(1, y1 - y0)
        elif mode == "worn":
            if y1 - y0 < 6:
                continue
            amp = light * 1.6
            t = (yy - y0) / max(1, y1 - y0)
        elif mode == "cyl_v":            # a vertical drum or pipe: bright on the lit left, dark on the right
            bx0, by0, bx1, by1 = box
            amp = amp_z
            t = (xx_f - bx0) / max(1.0, bx1 - bx0)
        else:                            # "cyl_h": a horizontal tube: bright along the top, dark along the bottom
            bx0, by0, bx1, by1 = box
            amp = amp_z
            t = (yy_f - by0) / max(1.0, by1 - by0)
        tq = (np.floor(np.clip(t, 0, 0.999) * bands) + 0.5) / bands
        out[m] = out[m] * (1 + amp * (0.5 - tq))[m][:, None]
    # volume (organic regions only): lit from the top left, rounded over a few pixels; lit = warm, shaded = cool
    lit_total = np.zeros((h, w), np.float32)
    for c in range(n):
        if info[c][0] not in ("organic", "worn"):
            continue
        m = comp == c
        cnt = m.sum()
        if cnt < 40 or lab[m][0] == 0:
            continue
        mf = m.astype(np.float32)
        wornc = info[c][0] == "worn"
        bl = box_blur(box_blur(mf, 1 if wornc else 2), 1 if wornc else 2)
        gy, gx = np.gradient(bl)
        lit = 0.7071 * (gx + gy)
        mx = np.abs(lit).max()
        if mx <= 0:
            continue
        lit_total = np.where(m, lit / mx * (0.42 if wornc else 1.0), lit_total)
    k = np.where(lit_total > 0, 1 + volume * lit_total, 1 + volume * 0.8 * lit_total)
    k = np.clip(k, 0.72, 1.2)
    out = out * k[..., None]
    out[..., 0] *= 1 + 0.05 * lit_total
    out[..., 2] *= 1 - 0.05 * lit_total
    # worn regions are beaten up rather than washed smooth: dings, scratches and a little grime, with the straight edges left alone
    rngw = np.random.default_rng(seed + 11)
    for c in range(n):
        if info[c][0] != "worn":
            continue
        m = comp == c
        cnt = int(m.sum())
        if cnt < 120 or lab[m][0] == 0:
            continue
        ys_, xs_ = np.nonzero(m)
        inner = box_blur(m.astype(np.float32), 1) > 0.99           # keep marks off the outline
        iy, ix = np.nonzero(inner)
        if len(ix) < 20:
            continue
        for _ in range(min(28, 1 + cnt // 130)):                    # dents: dark upper-left, lit lower-right inside the dent
            j = int(rngw.integers(0, len(ix)))
            cx_, cy_ = ix[j], iy[j]
            r = float(rngw.uniform(1.8, 3.6))
            x0_, x1_ = int(max(0, cx_ - 4)), int(min(w, cx_ + 5))
            y0_, y1_ = int(max(0, cy_ - 4)), int(min(h, cy_ + 5))
            for yy_ in range(y0_, y1_):
                for xx_ in range(x0_, x1_):
                    dx_, dy_ = (xx_ - cx_) / r, (yy_ - cy_) / (r * 0.8)
                    d2 = dx_ * dx_ + dy_ * dy_
                    if d2 < 1.0 and inner[yy_, xx_]:
                        out[yy_, xx_] *= 1 + 0.42 * (dx_ + dy_) * 0.7071 * (1 - 0.3 * d2)
        for _ in range(min(34, 1 + cnt // 100)):                    # scratches
            j = int(rngw.integers(0, len(ix)))
            ang = float(rngw.uniform(0, 3.1416))
            ln = int(rngw.integers(4, 12))
            k_ = 1.32 if rngw.random() < 0.5 else 0.7
            for t_ in range(ln):
                xx_, yy_ = int(ix[j] + np.cos(ang) * t_), int(iy[j] + np.sin(ang) * t_)
                if 0 <= xx_ < w and 0 <= yy_ < h and inner[yy_, xx_]:
                    out[yy_, xx_] *= k_
        for _ in range(min(10, cnt // 300)):                        # grime runs: short darker vertical streaks
            j = int(rngw.integers(0, len(ix)))
            ln = int(rngw.integers(4, 12))
            for t_ in range(ln):
                yy_ = iy[j] + t_
                if 0 <= yy_ < h and inner[yy_, ix[j]]:
                    out[yy_, ix[j]] *= 0.88
    # edge light between neighbouring shapes
    L = lum(base)
    def shifted(arr, dy, dx):
        return np.roll(np.roll(arr, dy, 0), dx, 1)
    for (dy, dx, sign) in ((1, 0, +1), (0, 1, +1), (-1, 0, -1), (0, -1, -1)):
        nb_comp = shifted(comp, dy, dx)
        nb_L = shifted(L, dy, dx)
        diff = (nb_comp != comp) & (np.abs(nb_L - L) > 14)
        e_here = np.where(class_map == 2, edge * 1.6, np.where(class_map == 3, edge * 1.25, edge))[..., None]
        if sign > 0:
            sel = diff & (nb_L < L)
            out = np.where(sel[..., None], out * (1 + e_here), out)
        else:
            sel = diff & (nb_L > L)
            out = np.where(sel[..., None], out * (1 - e_here * 0.8), out)
    # texture and grain
    rng = np.random.default_rng(seed)
    out = out * (1 + (rng.random((h, w, 1)) - 0.5) * 2 * texture)
    out = out + rng.normal(0, grain, (h, w, 1))
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")
    img = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    return (img, class_map) if return_class else img


def box_blur(a, r):
    k = 2 * r + 1
    p = np.pad(a, r, mode="edge")
    c = np.cumsum(np.pad(p, ((0, 0), (1, 0))), axis=1)
    p = (c[:, k:] - c[:, :-k]) / k
    c = np.cumsum(np.pad(p, ((1, 0), (0, 0))), axis=0)
    return (c[k:] - c[:-k]) / k


def lum(rgb):
    return rgb[..., 0] * 0.3 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11
