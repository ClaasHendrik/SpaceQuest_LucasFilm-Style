"""Solid-object painting: objects built from separately lit planes (top / front / side / underside),
with thickness, edge highlights, panel detail and soft contact shadows. Key light: top-left, slightly warm."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from paint import rgb, mix

# light factor per plane orientation
TOP, FRONT, SIDE, UNDER = 1.35, 1.0, 0.62, 0.38


def soft_shadow(p, pts, strength=0.55, blur=3.0, tint=(10, 6, 20), clip=None):
    """a blurred shadow polygon multiplied onto whatever is beneath"""
    m = Image.new("L", (p.w, p.h), 0)
    ImageDraw.Draw(m).polygon([tuple(q) for q in pts], fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255.0
    if clip is not None:
        m = m * clip
    k = (m * strength)[..., None]
    p.a = np.clip(p.a * (1 - k) + np.asarray(tint, np.float32) * k, 0, 255)


def plane(p, pts, base, k, angle=(-1, -1), spread=0.35, tex=0.06, seed=1, edge=0.45, rim=None):
    """one lit plane: k = overall light on this plane, spread = how much light varies across it"""
    m = p.m_poly(pts)
    p.shade(m, base, k * (1 + spread / 2), k * (1 - spread / 2), angle=angle, tex=tex, seed=seed)
    if edge:
        p.edge(m, (0, 0, 0), edge)
    if rim:
        p.edge(m, (255, 245, 225), rim, "top")
    return m


def box(p, x, y, w, h, dx, dy, base, seed=1, tex=0.06, front_detail=None):
    """3/4-view box: front face (x,y,w,h); top slopes back-right by (dx,dy); right side visible.
    returns (front_mask, top_mask, side_mask)"""
    top = [(x, y), (x + w, y), (x + w + dx, y - dy), (x + dx, y - dy)]
    side = [(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)]
    front = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    mt = plane(p, top, base, TOP, angle=(-1, 1), spread=0.25, tex=tex, seed=seed, edge=0.35, rim=0.45)
    ms = plane(p, side, base, SIDE, angle=(-1, 0), spread=0.3, tex=tex, seed=seed + 1, edge=0.5)
    mf = plane(p, front, base, FRONT, angle=(-1, -1), spread=0.35, tex=tex, seed=seed + 2, edge=0.5)
    # crisp highlight along the front-top edge and a dark line where planes meet
    p.fill(p.m_line(x, y, x + w, y, 1), (255, 255, 255), 0.45)
    p.fill(p.m_line(x + w, y, x + w, y + h, 1), (0, 0, 0), 0.5)
    return mf, mt, ms


def cylinder_h(p, x0, x1, y0, y1, base, seed=1):
    """horizontal cylinder: light along the top, dark underside, a bright specular line"""
    m = p.m_rect(x0, y0, x1, y1)
    t = np.clip((p.yy - y0) / max(1, y1 - y0), 0, 1)
    prof = 1.45 - 1.05 * t + 0.0
    prof = np.where(t < 0.18, prof + 0.25, prof)
    c = rgb(base) if isinstance(base, str) else np.asarray(base, np.float32)
    p.fill(m, np.clip(c * prof[..., None], 0, 255))
    p.fill(p.m_rect(x0, y0 + 1 + int((y1 - y0) * 0.14), x1, y0 + 2 + int((y1 - y0) * 0.14)), (255, 255, 255), 0.35)
    p.edge(m, (0, 0, 0), 0.4)


def cylinder_v(p, x0, x1, y0, y1, base, seed=1):
    m = p.m_rect(x0, y0, x1, y1)
    t = np.clip((p.xx - x0) / max(1, x1 - x0), 0, 1)
    prof = 1.45 - 1.05 * t
    prof = np.where(t < 0.2, prof + 0.2, prof)
    c = rgb(base) if isinstance(base, str) else np.asarray(base, np.float32)
    p.fill(m, np.clip(c * prof[..., None], 0, 255))
    p.fill(p.m_rect(x0 + 1 + int((x1 - x0) * 0.16), y0, x0 + 2 + int((x1 - x0) * 0.16), y1), (255, 255, 255), 0.35)
    p.edge(m, (0, 0, 0), 0.4)


def rivets(p, pts, light=(255, 255, 255)):
    for x, y in pts:
        p.fill(p.m_rect(x, y, x + 1, y + 1), (0, 0, 0), 0.6)
        p.fill(p.m_rect(x - 1, y - 1, x, y), light, 0.35)


def panel_lines(p, mask, lines, dark=0.55, light=0.28):
    for (x0, y0, x1, y1) in lines:
        ln = p.m_line(x0, y0, x1, y1, 1) & mask
        p.fill(ln, (0, 0, 0), dark)
        ln2 = p.m_line(x0 + 1, y0 + 1, x1 + 1, y1 + 1, 1) & mask
        p.fill(ln2, (255, 255, 255), light)


def weather(p, mask, color, amount=0.8, scale=5, seed=1, thresh=0.5, feather=1.2):
    """feathered, noise-broken weathering (rust, soot) clipped to a mask: no hard sticker edges"""
    n = p.noise(scale, 3, seed)
    a = np.clip((n - thresh) * 5.0, 0, 1)
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))
    a = a * (np.asarray(m, np.float32) / 255.0) * amount
    c = rgb(color) if isinstance(color, str) else np.asarray(color, np.float32)
    p.a = np.clip(p.a * (1 - a[..., None]) + c * a[..., None], 0, 255)


def dent(p, cx, cy, r, mask=None):
    """a shallow dent: dark lower-right crescent plus a bright upper-left edge"""
    d = p.m_ell(cx - r, cy - r * 0.7, cx + r, cy + r * 0.7)
    d2 = p.m_ell(cx - r + 1.5, cy - r * 0.7 + 1.5, cx + r + 1.5, cy + r * 0.7 + 1.5)
    if mask is not None:
        d &= mask
        d2 &= mask
    p.fill(d2 & ~d, (255, 255, 255), 0.35)
    p.fill(d & ~p.m_ell(cx - r + 1.5, cy - r * 0.7 + 1.5, cx + r + 1.5, cy + r * 0.7 + 1.5), (0, 0, 0), 0.4)


def mallard(p, ox, oy, s=1.0, lit=True, ramp=True, seed=40):
    """The Aluminum Mallard, a small battered junk ship, 3/4 side view, nose to the right.
    (ox, oy) = tail-top of the hull in scene coordinates, s = scale."""
    def T(pts):
        return [(ox + x * s, oy + y * s) for x, y in pts]

    def R(x0, y0, x1, y1):
        return (ox + x0 * s, oy + y0 * s, ox + x1 * s, oy + y1 * s)

    # soft shadow under the ship
    soft_shadow(p, T([(-10, 70), (30, 66), (180, 68), (214, 74), (180, 82), (30, 82)]), 0.6, 3.5 * max(s, 0.5))
    # landing struts with pads, behind the hull
    for x0 in (30, 150):
        a = R(x0, 54, x0 + 9, 70)
        cylinder_v(p, int(a[0]), int(a[2]), int(a[1]), int(a[3]), "#6a7486")
        pad = p.m_poly(T([(x0 - 6, 70), (x0 + 16, 70), (x0 + 20, 74), (x0 - 10, 74)]))
        p.shade(pad, "#8a94a6", 1.3, 0.5, seed=seed + 1)
        p.edge(pad, (0, 0, 0), 0.5)
    # underside (dark plane)
    plane(p, T([(0, 46), (16, 60), (186, 62), (198, 50)]), "#7a8498", UNDER, spread=0.2, seed=seed + 2)
    # hull top plane (lit from above) and the long side plane
    top = plane(p, T([(24, 8), (46, -4), (126, -8), (170, 0), (178, 12), (122, 2)]), "#d4dce8", TOP, angle=(-1, 1),
                spread=0.3, seed=seed + 3, rim=0.5)
    side = plane(p, T([(0, 46), (0, 26), (24, 8), (122, 2), (178, 12), (200, 34), (198, 50), (184, 60), (16, 60)]),
                 "#aeb8c8", FRONT, angle=(-0.25, -1), spread=0.85, tex=0.1, seed=seed + 4, rim=0.35)
    # nose facet in shadow-ish, catching a different angle
    plane(p, T([(176, 12), (200, 34), (198, 50), (182, 42), (170, 24)]), "#aeb8c8", 0.72, spread=0.3, seed=seed + 5)
    # panel seams with a bright edge beside each dark line
    panel_lines(p, side, [(int(ox + x * s), int(oy + 4 * s), int(ox + (x - 6) * s), int(oy + 60 * s)) for x in (46, 86, 126, 164)])
    panel_lines(p, side, [(int(ox + 4 * s), int(oy + 30 * s), int(ox + 196 * s), int(oy + 36 * s))])
    if s >= 0.5:
        rivets(p, [(int(ox + x * s), int(oy + (10 - (x - 40) * 0.02 + 36 * (1 if x > 130 else 0) * 0) * s)) for x in range(46, 176, 10)][:0] or [])
        rivets(p, [(int(ox + x * s), int(oy + 33 * s)) for x in range(8, 196, 9)])
        rivets(p, [(int(ox + x * s), int(oy + 56 * s)) for x in range(24, 180, 12)])
    # ambient occlusion where the hull curves under, and a darker band along the bottom seam
    ao = p.m_poly(T([(14, 52), (186, 54), (184, 60), (16, 60)])) & side
    p.multiply(1 - 0.5 * np.clip((p.yy - (oy + 50 * s)) / (10 * s + 1e-6), 0, 1) * ao, 1.0)
    # welded patch, vents and a hatch outline
    patch = p.m_poly(T([(130, 20), (156, 18), (158, 40), (132, 42)])) & side
    p.shade(patch, "#c0c8d6", 1.2, 0.7, seed=seed + 20)
    p.edge(patch, (0, 0, 0), 0.5)
    p.edge(patch, (255, 255, 255), 0.3, "top")
    rivets(p, [(int(ox + x * s), int(oy + y * s)) for x, y in ((133, 22), (153, 21), (134, 40), (155, 39))])
    for i in range(5):
        a_ = R(14, 36 + i * 3.4, 36, 37.5 + i * 3.4)
        p.fill(p.m_rect(*a_), (6, 8, 12), 0.85)
        p.fill(p.m_rect(a_[0], a_[3], a_[2], a_[3] + 1), (255, 255, 255), 0.25)
    dent(p, ox + 70 * s, oy + 46 * s, 7 * s, side)
    dent(p, ox + 104 * s, oy + 22 * s, 5 * s, side)
    dent(p, ox + 176 * s, oy + 46 * s, 5 * s, side)
    # feathered rust and soot streaks
    weather(p, p.m_poly(T([(56, 8), (120, 6), (126, 40), (60, 36)])) & side, "#b4642c", 0.85, 4, seed, 0.46)
    weather(p, p.m_poly(T([(0, 28), (40, 30), (44, 58), (0, 58)])) & side, "#14100e", 0.8, 5, seed + 3, 0.42)
    for x in (70, 92, 112):                                       # rust runs down the plating
        weather(p, p.m_poly(T([(x, 30), (x + 5, 30), (x + 4, 58), (x - 1, 58)])) & side, "#7a3a1a", 0.7, 3, seed + x, 0.5)
    # the fin's shadow on the hull
    soft_shadow(p, T([(70, 8), (104, 6), (112, 28), (84, 30)]), 0.4, 2.5 * max(s, 0.5), clip=side.astype(np.float32))
    # tail fin: a small box standing on the hull
    fin = [(58, 0), (80, -4), (72, -28), (60, -26)]
    plane(p, T(fin), "#aeb8c8", FRONT, spread=0.4, seed=seed + 6, rim=0.4)
    plane(p, T([(80, -4), (86, -6), (78, -30), (72, -28)]), "#aeb8c8", SIDE, spread=0.3, seed=seed + 7)
    p.fill(p.m_poly(T([(60, -26), (72, -28), (78, -30), (66, -28)])), (255, 255, 255), 0.4)
    # engine manifold at the tail: a flange ring with pipes inside
    ring = p.m_ell(*R(-12, 26, 8, 62))
    p.shade(ring, "#8a94a6", 1.4, 0.4, seed=seed + 8)
    p.edge(ring, (0, 0, 0), 0.6)
    inner = p.m_ell(*R(-8, 31, 5, 57))
    p.fill(inner, p.radial(ox - 1 * s, oy + 44 * s, 14 * s, "#ff9a50" if lit else "#201008", "#0a0404", 1.6))
    for yy in (36, 44, 52):
        cylinder_h(p, int(ox - 6 * s), int(ox + 4 * s), int(oy + (yy - 1.5) * s), int(oy + (yy + 2) * s), "#7a8494")
    if lit:
        p.glow(ox - 2 * s, oy + 44 * s, 26 * s, (255, 150, 70), 0.5, 0.8)
    # cockpit canopy: glass with a reflection and a metal frame
    glass = p.m_poly(T([(148, 6), (176, 12), (190, 32), (150, 28)]))
    p.fill(glass, p.lin(ox + 148 * s, oy + 6 * s, ox + 190 * s, oy + 32 * s, "#d8fcff" if lit else "#4a6078", "#2a7898" if lit else "#101c2c"))
    p.fill(p.m_poly(T([(152, 9), (162, 11), (156, 26), (152, 25)])) & glass, (255, 255, 255), 0.5)
    p.edge(glass, (0, 0, 0), 0.8)
    p.fill(p.m_line(*[int(v) for v in R(163, 9, 168, 29)], 1), (30, 36, 46), 0.9)
    if lit:
        p.glow(ox + 170 * s, oy + 20 * s, 34 * s, (150, 230, 255), 0.25, 0.8)
    # amber running lights with glow
    if lit:
        for x, y in ((24, 56), (102, 3), (186, 44)):
            a = R(x, y, x + 6, y + 2)
            p.fill(p.m_rect(*a), (255, 220, 110))
            p.glow(ox + (x + 3) * s, oy + (y + 1) * s, 20 * s, (255, 190, 70), 0.55)
    # boarding ramp on the floor, drawn with steps
    if ramp:
        rp = p.m_poly(T([(84, 60), (122, 60), (136, 82), (70, 82)]))
        p.shade(rp, "#8a94a6", 1.35, 0.45, angle=(0, -1), seed=seed + 9)
        p.edge(rp, (0, 0, 0), 0.5)
        for i in range(1, 4):
            yy = 60 + i * 5.5
            p.fill(p.m_line(*[int(v) for v in R(84 - i * 4.6, yy, 122 + i * 4.6, yy)], 1), (0, 0, 0), 0.5)
            p.fill(p.m_line(*[int(v) for v in R(84 - i * 4.6, yy + 1, 122 + i * 4.6, yy + 1)], 1), (255, 255, 255), 0.25)
        p.fill(p.m_rect(*R(88, 52, 118, 60)), (4, 6, 10))          # open hatch above the ramp


# ====================================================================== more solids
def ground_shadow(p, x0, x1, y, h=6, strength=0.55, blur=3.0):
    """soft elliptical contact shadow on the floor under an object"""
    pts = [(x0 + (x1 - x0) * (0.5 + 0.5 * np.cos(a)), y + h * 0.5 * (1 + np.sin(a))) for a in np.linspace(0, 6.283, 20)]
    soft_shadow(p, pts, strength, blur)


def sphere(p, cx, cy, r, base, squash=1.0, key=(-0.55, -0.65), spec=0.5, bounce=0.18, clip=None, tint=None):
    """a lit ball: diffuse from the key light, specular highlight, reflected light from below"""
    nx = (p.xx - cx) / r
    ny = (p.yy - cy) / (r * squash)
    d = nx * nx + ny * ny
    m = d <= 1.0
    if clip is not None:
        m = m & clip
    nz = np.sqrt(np.clip(1 - d, 0, 1))
    kx, ky = key
    kz = np.sqrt(max(0.0, 1 - kx * kx - ky * ky))
    lam = np.clip(nx * (-kx) * -1 * 0 + (-nx * kx - ny * ky) + nz * kz, 0, 1)
    lam = np.clip(-(nx * kx + ny * ky) + nz * kz * 0.6, 0, 1.2)
    c = (rgb(base) if isinstance(base, str) else np.asarray(base, np.float32))
    sh = 0.28 + 0.95 * lam
    col = c * sh[..., None]
    sp = np.clip(-(nx * kx + ny * ky) * 0.7 + nz * 0.5, 0, 1) ** 18 * spec * 255
    col = col + sp[..., None]
    low = np.clip(ny, 0, 1) * np.clip(1 - np.abs(nx), 0, 1)
    col = col + (low * bounce)[..., None] * (np.asarray(tint, np.float32) if tint is not None else c * 0.8)
    p.fill(m, np.clip(col, 0, 255))
    p.edge(m, (0, 0, 0), 0.45)
    return m


def dome(p, cx, base_y, rx, ry, base, spec=0.5):
    """half an ellipsoid sitting on base_y"""
    m = sphere(p, cx, base_y, rx, base, squash=ry / rx, spec=spec, clip=(p.yy <= base_y))
    return m


def ladder(p, x0, x1, y0, y1, color="#aab4c4", rungs=7, wall_shadow=True):
    if wall_shadow:
        soft_shadow(p, [(x0 + 3, y0 + 2), (x1 + 4, y0 + 2), (x1 + 4, y1), (x0 + 3, y1)], 0.35, 1.6)
    cylinder_v(p, x0, x0 + 3, y0, y1, color)
    cylinder_v(p, x1 - 3, x1, y0, y1, color)
    n = max(2, int((y1 - y0) / rungs))
    for i in range(1, n):
        y = y0 + i * (y1 - y0) / n
        p.fill(p.m_rect(x0 + 3, y, x1 - 3, y + 2), (0, 0, 0), 0.55)
        p.fill(p.m_rect(x0 + 3, y - 1, x1 - 3, y), (255, 255, 255), 0.5)


def facet_rock(p, pts, base, seed=1, hi=1.5, lo=0.25, facets=3, edge=0.55):
    """a faceted rock face: strong directional light plus a few planar breaks"""
    m = p.m_poly(pts)
    p.shade(m, base, hi, lo, angle=(-1, -0.8), tex=0.2, seed=seed)
    rng = np.random.default_rng(seed)
    ys, xs = np.nonzero(m)
    if len(xs):
        done, tries = 0, 0
        while done < facets and tries < 40:
            tries += 1
            i = int(rng.integers(0, len(xs)))
            ang = rng.uniform(0, 6.283)
            L = rng.uniform(6, 22)
            x1, y1 = int(xs[i] + np.cos(ang) * L), int(ys[i] + np.sin(ang) * L)
            if not (0 <= x1 < p.w and 0 <= y1 < p.h and m[y1, x1]):
                continue
            ln = p.m_line(xs[i], ys[i], x1, y1, 1) & m
            p.fill(ln, (0, 0, 0), 0.4)
            p.fill(p.m_line(xs[i] + 1, ys[i] + 1, x1 + 1, y1 + 1, 1) & m, (255, 255, 255), 0.18)
            done += 1
    p.edge(m, (0, 0, 0), edge)
    p.edge(m, (255, 255, 255), 0.25, "top")
    return m


def spire3d(p, x, y, h, w, base, seed=1):
    """a cone-like spire: lit left plane, shadowed right plane, ground shadow"""
    ground_shadow(p, x - w * 0.2, x + w * 1.4, y + h - 2, 5, 0.5, 2.5)
    plane(p, [(x, y + h), (x + w * 0.5, y), (x + w * 0.5, y + h)], base, 1.25, angle=(-1, 0), spread=0.4, seed=seed, edge=0.5, rim=0.3)
    plane(p, [(x + w * 0.5, y), (x + w, y + h), (x + w * 0.5, y + h)], base, 0.5, angle=(-1, 0), spread=0.3, seed=seed + 1, edge=0.5)


def arch3d(p, x, y, w, h, base, seed=1):
    """a natural rock arch with a lit outer face, a shadowed underside and a cast ground shadow"""
    ground_shadow(p, x, x + w * 1.1, y + h - 2, 7, 0.5, 3.0)
    outer = [(x, y + h), (x + w * 0.1, y + h * 0.4), (x + w * 0.3, y + 4), (x + w * 0.5, y), (x + w * 0.74, y + h * 0.3),
             (x + w, y + h), (x + w * 0.78, y + h), (x + w * 0.6, y + h * 0.42), (x + w * 0.5, y + h * 0.36),
             (x + w * 0.38, y + h * 0.46), (x + w * 0.22, y + h)]
    m = facet_rock(p, outer, base, seed, 1.55, 0.3, 4)
    under = p.m_poly([(x + w * 0.22, y + h), (x + w * 0.38, y + h * 0.46), (x + w * 0.5, y + h * 0.36), (x + w * 0.6, y + h * 0.42), (x + w * 0.78, y + h),
                      (x + w * 0.7, y + h), (x + w * 0.55, y + h * 0.5), (x + w * 0.4, y + h * 0.52), (x + w * 0.3, y + h)]) & m
    p.fill(under, (0, 0, 0), 0.45)
    return m


def person(p, x, feet_y, h, torso, legs, skin="#e8b896", hair="#6a3a1a", seed=1, helmet=None, arms=None, facing=1):
    """a small shaded figure (NPCs): legs, torso, arms, head; light from the left"""
    s = h / 46.0
    ground_shadow(p, x - 7 * s, x + 7 * s, feet_y - 1, 3, 0.5, 1.5)
    for dx in (-3.2, 1.4):
        l = p.m_rect(x + dx * s, feet_y - 19 * s, x + (dx + 3.4) * s, feet_y)
        p.shade(l, legs, 1.25, 0.5, angle=(-1, 0), tex=0.05, seed=seed)
        p.edge(l, (0, 0, 0), 0.5)
    tb = p.m_poly([(x - 5.5 * s, feet_y - 19 * s), (x + 5.5 * s, feet_y - 19 * s), (x + 6.2 * s, feet_y - 34 * s), (x - 6.2 * s, feet_y - 34 * s)])
    p.shade(tb, torso, 1.3, 0.45, angle=(-1, 0), tex=0.06, seed=seed + 1)
    p.edge(tb, (0, 0, 0), 0.5)
    for dx, k in ((-8.2, 1.15), (5.2, 0.6)):
        a = p.m_rect(x + dx * s, feet_y - 33 * s, x + (dx + 3) * s, feet_y - 19 * s)
        p.shade(a, arms or torso, k * 1.1, k * 0.6, angle=(-1, 0), tex=0.04, seed=seed + 2)
        p.edge(a, (0, 0, 0), 0.5)
    head = sphere(p, x, feet_y - 39 * s, 5.2 * s, skin, 1.08, spec=0.2)
    if helmet:
        h2 = p.m_ell(x - 5.8 * s, feet_y - 46 * s, x + 5.8 * s, feet_y - 36 * s) & (p.yy < feet_y - 38.5 * s)
        p.shade(h2, helmet, 1.4, 0.5, seed=seed + 3)
    else:
        h2 = p.m_ell(x - 5.4 * s, feet_y - 45.5 * s, x + 5.4 * s, feet_y - 37 * s) & (p.yy < feet_y - 39.5 * s)
        p.shade(h2, hair, 1.3, 0.5, seed=seed + 3)
    p.fill(p.m_rect(x + 1.2 * s * facing, feet_y - 40 * s, x + 2.6 * s * facing, feet_y - 38.8 * s), (20, 20, 30))


def building(p, x, y, w, h, dx, dy, wall, roof, seed=1):
    """a flat-roofed block seen in 3/4: front wall, side wall, roof slab with thickness"""
    ground_shadow(p, x, x + w + dx + 8, y + h - 1, 6, 0.5, 3.0)
    mf, mt, ms = box(p, x, y, w, h, dx, dy, wall, seed=seed, tex=0.08)
    p.fill(mt, p.lin(0, y - dy, 0, y, roof, roof), 0.0)
    return mf, mt, ms


# ====================================================================== doors and cavities (from the style analysis)
def _lerp(a, b, t):
    return a + (b - a) * t


def hinged_door(p, hx, y0, y1, dx, base, side=-1, eye=70.0, scale=1.12, panels=2, handle=True, glass=None, seed=1, shade_k=0.78):
    """A door leaf hinged at x=hx, swung open towards the viewer.
    The free edge is dx away from the hinge (side=-1: to the left) and is TALLER than the hinge edge (perspective about eye).
    The leaf has a visible edge (thickness), hinges, inset panels (or a glass pane) and a handle, and throws a shadow."""
    fx = hx + side * dx
    ty = eye - (eye - y0) * scale
    by = eye + (y1 - eye) * scale
    poly = [(hx, y0), (fx, ty), (fx, by), (hx, y1)]

    def at(u, v):   # u: 0 at the hinge .. 1 at the free edge; v: 0 top .. 1 bottom
        x = _lerp(hx, fx, u)
        return (x, _lerp(_lerp(y0, ty, u), _lerp(y1, by, u), v))

    # shadows first: on the wall behind (falls right and down) and on the floor in front of the door
    soft_shadow(p, [(x + 5, y + 1.5) for x, y in poly], 0.42, 1.0)
    soft_shadow(p, [(fx, by), (hx, y1), (hx + 12, y1 + 3.5), (fx + 12, by + 3.5)], 0.38, 1.4)
    # the leaf: its inner face is turned away from the key light, so it is darker than the outer face
    m = plane(p, poly, base, shade_k, angle=(-1, 0), spread=0.5, tex=0.04, seed=seed, edge=0.5)
    # thickness: a lit strip on the free edge and a thin strip along the top
    edge_strip = [(fx, ty), (fx - 2 * (-side) * -1, ty + 0.5), (fx - 2 * (-side) * -1, by - 0.5), (fx, by)]
    p.fill(p.m_poly([(fx, ty), (fx + side * 2, ty + 0.6), (fx + side * 2, by - 0.6), (fx, by)]), rgb(base) * 1.5 if isinstance(base, str) else base)
    p.fill(p.m_poly([(fx, ty), (fx + side * 2, ty + 0.6), (fx + side * 2, by - 0.6), (fx, by)]), (255, 255, 255), 0.18)
    p.fill(p.m_line(hx, y0 - 1, fx, ty - 1, 1), (255, 255, 255), 0.4)
    # hinge edge: a dark crease and two small hinges
    p.fill(p.m_line(hx, y0, hx, y1, 2), (0, 0, 0), 0.55)
    for v in (0.12, 0.86):
        hy = _lerp(y0, y1, v)
        p.fill(p.m_rect(hx - 1.5, hy - 2, hx + 1.5, hy + 2), (200, 205, 215))
        p.fill(p.m_rect(hx - 0.5, hy - 2, hx + 0.5, hy + 2), (60, 64, 76))
    if glass is not None:
        a, b, c, d = at(0.14, 0.07), at(0.86, 0.07), at(0.86, 0.93), at(0.14, 0.93)
        gm = p.m_poly([a, b, c, d])
        p.fill(gm, rgb(glass) if isinstance(glass, str) else glass, 0.55)
        p.fill(p.m_poly([at(0.24, 0.1), at(0.42, 0.1), at(0.30, 0.9), at(0.2, 0.9)]) & gm, (255, 255, 255), 0.30)
        p.edge(gm, (0, 0, 0), 0.5)
        p.edge(gm, (255, 255, 255), 0.25, "top")
    else:
        n = panels
        for i in range(n):
            v0 = 0.08 + i * (0.84 / n) + 0.02
            v1 = 0.08 + (i + 1) * (0.84 / n) - 0.02
            a, b, c, d = at(0.16, v0), at(0.84, v0), at(0.84, v1), at(0.16, v1)
            inset = p.m_poly([a, b, c, d])
            p.fill(inset, (0, 0, 0), 0.16)
            p.fill(p.m_line(a[0], a[1], b[0], b[1], 1) & m, (0, 0, 0), 0.5)      # top and left inner edges are in shadow
            p.fill(p.m_line(a[0], a[1], d[0], d[1], 1) & m, (0, 0, 0), 0.4)
            p.fill(p.m_line(d[0], d[1], c[0], c[1], 1) & m, (255, 255, 255), 0.4)   # bottom and right inner edges catch light
            p.fill(p.m_line(b[0], b[1], c[0], c[1], 1) & m, (255, 255, 255), 0.3)
    if handle:
        hxx, hyy = at(0.86, 0.52)
        p.fill(p.m_rect(hxx - 1.5, hyy - 3.5, hxx + 1.5, hyy + 3.5), (0, 0, 0), 0.5)
        p.fill(p.m_rect(hxx - 1, hyy - 3, hxx + 1, hyy + 3), (232, 214, 150))
        p.fill(p.m_rect(hxx - 1, hyy - 3, hxx, hyy - 2), (255, 255, 255), 0.9)
    return m


def recess(p, x0, y0, x1, y1, d=7.0, wall="#4a5664", back_top="#0a0e14", back_bot="#03050a", floor_c="#8a96a6", seed=1):
    """An opening with real depth: you see the left inner wall, the roof (dark), the floor (lit) and the back wall.
    Returns the back wall rectangle (bx0, by0, bx1, by1)."""
    dt, db = d * 0.6, d * 0.8
    bx0, by0, bx1, by1 = x0 + d, y0 + dt, x1, y1 - db
    p.fill(p.m_rect(bx0, by0, bx1, by1), p.lin(0, by0, 0, by1, back_top, back_bot))
    lw = plane(p, [(x0, y0), (bx0, by0), (bx0, by1), (x0, y1)], wall, 0.62, angle=(-1, 0), spread=0.3, tex=0.03, seed=seed, edge=0.4)
    plane(p, [(x0, y0), (x1, y0), (x1, by0), (bx0, by0)], wall, 0.3, angle=(0, -1), spread=0.2, tex=0.03, seed=seed + 1, edge=0.4)
    plane(p, [(x0, y1), (bx0, by1), (x1, by1), (x1, y1)], floor_c, 1.0, angle=(0, -1), spread=0.3, tex=0.03, seed=seed + 2, edge=0.4)
    # contact darkening where the walls meet the back wall
    p.fill(p.m_rect(bx0, by0, bx0 + 2, by1), (0, 0, 0), 0.4)
    p.fill(p.m_rect(bx0, by0, bx1, by0 + 2), (0, 0, 0), 0.4)
    return bx0, by0, bx1, by1


def hanging_garment(p, cx, top, h, base="#d8702a", trim=(240, 236, 226), seed=1):
    """a uniform on a hanger: sloped shoulders, a V collar, folds, sleeves with cuffs, a hook, and a shadow on the wall behind"""
    # shadow on the back wall
    soft_shadow(p, [(cx - 8, top + 4), (cx + 14, top + 4), (cx + 16, top + h), (cx - 6, top + h)], 0.42, 1.2)
    # hook and hanger
    p.fill(p.m_line(cx, top - 3, cx, top + 1, 1), (210, 214, 224))
    p.fill(p.m_poly([(cx - 10, top + 6), (cx, top + 1), (cx + 10, top + 6)]), (150, 154, 168))
    # sleeves hang behind and beside the body
    for sx, sgn, k in ((cx - 11, -1, 1.15), (cx + 8, 1, 0.55)):
        sl = [(cx + sgn * 6, top + 7), (cx + sgn * 11, top + 9), (cx + sgn * 13.5, top + h * 0.78), (cx + sgn * 9, top + h * 0.8)]
        plane(p, sl, base, k, angle=(-1, 0), spread=0.3, tex=0.04, seed=seed + 3, edge=0.5)
        p.fill(p.m_poly([sl[3], sl[2], (sl[2][0], sl[2][1] + 3), (sl[3][0], sl[3][1] + 3)]), trim)
    # body with a lit left side and a darker right side
    body = [(cx - 7, top + 5), (cx - 3, top + 3), (cx + 3, top + 3), (cx + 7, top + 5), (cx + 8, top + h * 0.92), (cx - 8, top + h * 0.92)]
    mb = plane(p, body, base, 1.0, angle=(-1, 0), spread=0.9, tex=0.05, seed=seed, edge=0.55)
    # folds
    for dx_ in (-4, -1, 3):
        p.fill(p.m_line(cx + dx_, top + 12, cx + dx_ + 0.5, top + h * 0.9, 1) & mb, (0, 0, 0), 0.32)
        p.fill(p.m_line(cx + dx_ - 1, top + 12, cx + dx_ - 0.5, top + h * 0.9, 1) & mb, (255, 220, 170), 0.2)
    # white V collar and the hem band
    p.fill(p.m_poly([(cx - 4, top + 3), (cx, top + 9), (cx + 4, top + 3), (cx + 2.5, top + 3), (cx, top + 6.5), (cx - 2.5, top + 3)]), trim)
    p.fill(p.m_rect(cx - 8, top + h * 0.86, cx + 8, top + h * 0.92), trim)
    p.fill(p.m_line(cx, top + 9, cx, top + h * 0.86, 1), (90, 44, 16), 0.5)
