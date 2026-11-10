"""Finds Roger in every reference screen and groups screens that show the same room.
Usage: python3 find_roger.py <dir with sNNN.png> <out.json>"""
import sys, json, glob, re
import numpy as np
from restyle import load_indices, figure_mask

SK, MAG = 12, {5, 13}
src, out = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(src + "/s[0-9][0-9][0-9].png"))
data = {}


def comps(mask):
    h, w = mask.shape
    seen = np.zeros_like(mask)
    res = []
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not seen[y, x]:
                st, pts = [(y, x)], []
                seen[y, x] = True
                while st:
                    cy, cx = st.pop()
                    pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                st.append((ny, nx))
                res.append(pts)
    return res


for f in files:
    n = int(re.search(r"s(\d+)\.png", f).group(1))
    idx = load_indices(f, 10, 190)
    # candidate pixels: skin or magenta; Roger = a small cluster that has BOTH and a brown/grey neighbourhood
    cand = (idx == SK) | np.isin(idx, list(MAG))
    found = []
    for pts in comps(cand):
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        kinds = {int(idx[p]) for p in pts}
        if 8 <= len(pts) <= 90 and bw <= 26 and bh <= 40 and SK in kinds and (kinds & MAG):
            found.append((min(xs), min(ys), max(xs), max(ys)))
    boxes = []
    for (x0, y0, x1, y1) in found:
        b = (max(0, x0 - 6), max(0, y0 - 14 + 10), min(319, x1 + 6), min(199, y1 + 22 + 10))
        m = figure_mask(idx, b)
        if m.sum() >= 40:
            boxes.append((b, int(m.sum())))
    data[n] = boxes
json.dump({str(k): v for k, v in data.items()}, open(out, "w"))
print(len(files), "screens;", sum(1 for v in data.values() if v), "with a figure")
