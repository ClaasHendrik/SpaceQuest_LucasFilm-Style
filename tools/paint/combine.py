"""Combines several screenshots of the same room into one picture without the figure: every pixel Roger hides in the base screen is
taken from another screenshot where that pixel is free (not Roger, not the mouse cursor).
Usage: python3 combine.py <out dir>   (reads the base screens from /tmp/claude-0/sq3 and the new ones from tools/paint/ref2/new_*.npy)"""
import sys, json
import numpy as np
from PIL import Image
from restyle import load_indices, figure_mask
from video_screens import EGA

SK, MAG = 12, {5, 13}


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


def detect(idx200, rows=slice(14, 200)):
    """boxes (screen coordinates) around figures that look like Roger, in a 200x320 index array"""
    sub = idx200[10:200]
    cand = (sub == SK) | np.isin(sub, list(MAG))
    out = []
    for pts in comps(cand):
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        kinds = {int(sub[p]) for p in pts}
        if 8 <= len(pts) <= 90 and bw <= 26 and bh <= 40 and SK in kinds and (kinds & MAG):
            out.append((max(0, min(xs) - 6), max(10, min(ys) + 10 - 14), min(319, max(xs) + 6), min(199, max(ys) + 10 + 22)))
    return out


def figure_mask200(idx200, boxes):
    m = np.zeros((200, 320), bool)
    sub = idx200[10:200]
    for b in boxes:
        m[10:200] |= figure_mask(sub, b, top=10) if False else figure_mask(idx200[10:200], b, top=10)
    return m


def cursor_mask(src, base, hidden=None):
    """small white/black clusters that are not in the base screen: the mouse cursor and similar overlays"""
    cand = (src != base) & np.isin(src, [15, 0])
    if hidden is not None:
        cand &= ~dilate(hidden, 3)              # where the figure was, differences are the revealed background, not a cursor
    cand[:12] = False
    m = np.zeros(src.shape, bool)
    for pts in comps(cand):
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        if len(pts) <= 140 and max(xs) - min(xs) < 16 and max(ys) - min(ys) < 20:
            for (y, x) in pts:
                m[max(0, y - 2):y + 3, max(0, x - 2):x + 3] = True
    return m


def dilate(m, r):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def merge(base, base_boxes, sources):
    """base: 200x320 indices; sources: list of (name, 200x320 indices). Returns (merged, hidden mask, filled mask, per-source use)"""
    hidden = figure_mask200(base, base_boxes)
    out = base.copy()
    todo = hidden.copy()
    used = {}
    for name, src in sources:
        sm = dilate(figure_mask200(src, detect(src)), 2) | cursor_mask(src, base, hidden)
        take = todo & ~sm
        out[take] = src[take]
        used[name] = int(take.sum())
        todo &= ~take
    return out, hidden, hidden & ~todo, used


def save_idx(idx, path):
    Image.fromarray(EGA[idx].astype(np.uint8)).save(path)
