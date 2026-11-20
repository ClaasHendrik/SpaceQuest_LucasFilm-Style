"""Turns a screenshot taken from a video (arbitrary size, scaled, with a UI around it) back into the original 320x200 EGA index grid.
The mapping is found by comparison with a known original of the same room, then every pixel is sampled at the centre of its block."""
import numpy as np
from PIL import Image

EGA = np.array([(0, 0, 0), (0, 0, 170), (0, 170, 0), (0, 170, 170), (170, 0, 0), (170, 0, 170), (170, 85, 0), (170, 170, 170),
                (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255), (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255)], float)


def sample(img, ox, oy, sx, sy, r=1):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    H, W = a.shape[:2]
    ys = np.clip(((np.arange(200) + 0.5) * sy + oy).astype(int), r, H - r - 1)
    xs = np.clip(((np.arange(320) + 0.5) * sx + ox).astype(int), r, W - r - 1)
    acc = np.zeros((200, 320, 3), np.float32)
    n = 0
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            acc += a[ys[:, None] + dy, xs[None, :] + dx]
            n += 1
    return acc / n


def to_idx(rgb):
    d = ((rgb[:, :, None, :] - EGA[None, None]) ** 2).sum(-1)
    return d.argmin(-1)


def calibrate(img, ref_idx, ignore=None):
    """grid search for the mapping that agrees best with ref_idx (200x320 indices); returns (score, ox, oy, sx, sy)"""
    W, H = img.size
    best = (-1, 0, 0, W / 320.0, H / 200.0)
    for ox in range(-6, 7, 3):
        for oy in range(-6, 7, 3):
            for fx in (0.99, 1.0, 1.01):
                for fy in (0.99, 1.0, 1.01):
                    sx, sy = W / 320.0 * fx, H / 200.0 * fy
                    idx = to_idx(sample(img, ox, oy, sx, sy, r=0))
                    ok = np.ones(idx.shape, bool)
                    ok[:12] = False
                    if ignore is not None:
                        ok &= ~ignore
                    sc = (idx == ref_idx)[ok].mean()
                    if sc > best[0]:
                        best = (float(sc), ox, oy, sx, sy)
    return best
