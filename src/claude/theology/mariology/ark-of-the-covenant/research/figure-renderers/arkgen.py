#!/usr/bin/env python3
"""Pen-and-ink renderer for the Ark plate (fig-ark.tex).

Models the ark in oblique projection and emits fine strokes whose width and
gray follow computed tone, in the manner of a steel engraving.  Deterministic:
fixed seed, stable iteration order.
"""
import math, random

rnd = random.Random(19620815)
OUT = []

def emit(s): OUT.append(s)

# ---------------------------------------------------------------- projection
DX, DY = 1.7, 0.95            # oblique depth vector for z in [0,1]
def proj(x, y, z):
    return (x + DX * z, y + DY * z)

# ---------------------------------------------------------------- stroke kit
def seg(p, q, w, g):
    """One stroke segment; w in pt, g in 0..100 gray."""
    emit(f"\\draw[line width={w:.2f}pt, black!{int(g)}] "
         f"({p[0]:.3f},{p[1]:.3f}) -- ({q[0]:.3f},{q[1]:.3f});")

def polyline(pts, w, g):
    coords = " -- ".join(f"({x:.3f},{y:.3f})" for x, y in pts)
    emit(f"\\draw[line width={w:.2f}pt, black!{int(g)}] {coords};")

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        x = u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0]
        y = u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]
        out.append((x, y))
    return out

def vary_outline(pts, w0, w1, g=100):
    """Outline with tapering weight along the point list."""
    n = len(pts) - 1
    run = [pts[0]]
    for i in range(n):
        run.append(pts[i+1])
        if len(run) >= 4 or i == n - 1:
            t = i / max(n - 1, 1)
            w = w0 + (w1 - w0) * t
            polyline(run, w, g)
            run = [run[-1]]

def hatch(poly, angle_deg, spacing, tone_fn, jitter=0.15,
          wmin=0.08, wmax=0.34, seg_len=0.16, cutoff=0.035):
    """Fill polygon with parallel strokes; per-segment width from tone_fn.

    poly: list of (x,y) defining a convex-ish clip region (we clip in TikZ).
    tone_fn(x, y) -> 0..1 darkness.
    """
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
    half = max(max(xs)-min(xs), max(ys)-min(ys)) * 0.75 + 0.5
    a = math.radians(angle_deg)
    dvec = (math.cos(a), math.sin(a)); nvec = (-dvec[1], dvec[0])
    coords = " -- ".join(f"({x:.3f},{y:.3f})" for x, y in poly)
    emit("\\begin{scope}")
    emit(f"  \\clip {coords} -- cycle;")
    k = -int(half/spacing)
    while k * spacing <= half:
        off = k * spacing
        ox, oy = cx + nvec[0]*off, cy + nvec[1]*off
        t = -half
        pending = None   # (start, w, g) run merging
        while t < half:
            x1, y1 = ox + dvec[0]*t, oy + dvec[1]*t
            t2 = min(t + seg_len, half)
            x2, y2 = ox + dvec[0]*t2, oy + dvec[1]*t2
            mx, my = (x1+x2)/2, (y1+y2)/2
            tone = tone_fn(mx, my)
            tone += rnd.uniform(-jitter, jitter) * 0.08
            if tone < cutoff:
                if pending:
                    polyline([pending[0], (x1, y1)], pending[1], pending[2])
                    pending = None
            else:
                tt = min(max(tone, 0.0), 1.0)
                w = wmin + (wmax - wmin) * tt
                g = 45 + 55 * tt
                wq = round(w*8)/8; gq = min(round(g/6)*6, 100)
                if pending and abs(pending[1]-wq) < 0.001 and pending[2] == gq:
                    pass
                else:
                    if pending:
                        polyline([pending[0], (x1, y1)], pending[1], pending[2])
                    pending = ((x1, y1), wq, gq)
            t = t2
        if pending:
            polyline([pending[0], (ox + dvec[0]*half, oy + dvec[1]*half)],
                     pending[1], pending[2])
        k += 1
    emit("\\end{scope}")

# ------------------------------------------------------------------- lights
# Light comes from upper front-left.  Tones are authored per surface with
# ambient-occlusion bands the way an engraver would place them.

def clamp(v, lo=0.0, hi=1.0): return min(max(v, lo), hi)

# ---------------------------------------------------------------- the chest
def chest():
    emit("% ---- chest ----")
    f00, f10 = proj(0,0,0), proj(5,0,0)
    f11, f01 = proj(5,3,0), proj(0,3,0)
    s10, s11 = proj(5,0,1), proj(5,3,1)

    # front face tone: light, darker toward bottom, AO under molding (y 2.6-2.72)
    def tone_front(x, y):
        t = 0.10 + 0.10 * (1 - y/3.0)
        t -= 0.085 * math.exp(-((x-1.7)/1.9)**2 - ((y-2.0)/0.95)**2)
        if 2.50 < y < 2.72:
            t += 0.22 * (y - 2.50)/0.22
        if y < 0.28:                       # ground bounce shadow
            t += 0.10 * (0.28 - y)/0.28
        if x < 0.25: t += 0.08 * (0.25 - x)/0.25   # left edge turn
        return t
    hatch([f00, f10, f11, f01], 0, 0.055, tone_front, wmax=0.26, seg_len=0.09, cutoff=0.028, jitter=0.15)

    # side face: mid-dark, gradient, AO at top under slab and at front corner
    def tone_side(px, py):
        # invert projection: on x=5 plane, z = (px-5)/DX, y = py - DY*z
        z = (px - 5)/DX; y = py - DY*z
        t = 0.28 + 0.16 * (1 - y/3.0)
        if y > 2.6: t += 0.16 * (y - 2.6)/0.4      # under slab overhang
        if z < 0.15: t += 0.10 * (0.15 - z)/0.15   # corner turn
        return t
    hatch([f10, s10, s11, f11], math.degrees(math.atan2(DY, DX)),
          0.050, tone_side)
    # cross layer on the darker parts of the side face
    def tone_side_cross(px, py):
        t = tone_side(px, py)
        return (t - 0.42) * 0.9 if t > 0.42 else 0.0
    hatch([f10, s10, s11, f11], 90 + 18, 0.075, tone_side_cross, wmax=0.22)

    # outlines, weighted: heavy on shadow side, light toward light
    polyline([f01, f00, f10], 0.5, 100)          # left + bottom front
    polyline([f10, s10], 0.55, 100)              # bottom depth edge
    polyline([s10, s11], 0.6, 100)               # far vertical (shadow side)
    polyline([f10, f11], 0.4, 95)                # front-right vertical
    polyline([f01, f11], 0.32, 90)               # top front edge (under molding)

def molding():
    emit("% ---- golden crown: ovolo molding ----")
    y0, y1 = 2.72, 2.94
    # front band: shaded ovolo — highlight near top, dark under-curve
    def tone_mold(x, y):
        u = clamp((y - y0)/(y1 - y0))     # 0 bottom .. 1 top
        # ovolo: bright band at u~0.75, dark at bottom
        t = 0.42 * (1 - u) ** 1.6 + 0.06
        t -= 0.10 * math.exp(-((u - 0.78)/0.16)**2)
        return clamp(t)
    hatch([(0, y0), (5, y0), (5, y1), (0, y1)], 90, 0.045, tone_mold,
          wmax=0.28, seg_len=0.08)
    m0, m1 = proj(5, y0, 0), proj(5, y0, 1)
    m2, m3 = proj(5, y1, 1), proj(5, y1, 0)
    def tone_mold_side(px, py):
        z = (px - 5)/DX; y = py - DY*z
        return clamp(tone_mold(0, y) + 0.16)
    hatch([m0, m1, m2, m3], 90 + 14, 0.045, tone_mold_side,
          wmax=0.3, seg_len=0.08)
    polyline([(0, y0), (5, y0)], 0.4, 100); polyline([m0, m1], 0.4, 100)
    polyline([(0, y1), (5, y1)], 0.34, 95); polyline([m3, m2], 0.34, 95)

def slab():
    emit("% ---- propitiatory slab ----")
    a, b = (-0.12, 3.02), (5.12, 3.02)
    c, d = (5.12, 3.32), (-0.12, 3.32)
    sb = (b[0]+DX, b[1]+DY); sc = (c[0]+DX, c[1]+DY)
    td = (d[0]+DX, d[1]+DY)   # back-left of top

    def tone_edge(x, y):
        u = clamp((y - 3.02)/0.30)
        return 0.16 + 0.14 * (1 - u)
    hatch([a, b, c, d], 90, 0.045, tone_edge, wmax=0.22, seg_len=0.08)
    def tone_edge_side(px, py):
        return 0.40 + 0.10 * (1 - (py - 3.02 - DY*((px-5.12)/DX))/0.30)
    hatch([b, sb, sc, c], 90 + 14, 0.045, tone_edge_side, seg_len=0.08)

    # top: nearly white; faint sheen + AO pools around the cherub feet
    feet = [(1.15, 3.86), (1.75, 3.86), (6.7-1.15, 3.86+0.0), (6.7-1.75, 3.86)]
    def tone_top(x, y):
        t = 0.030
        for fx, fy in ((1.45, 3.92), (5.25, 3.92)):
            r = math.hypot(x - fx, y - fy)
            t += 0.16 * math.exp(-(r/0.42)**2)
        # slight darkening toward back edge
        t += 0.05 * clamp((y - 3.9)/0.4)
        return t
    hatch([d, c, sc, td], math.degrees(math.atan2(DY, DX)), 0.065, tone_top,
          wmax=0.16, cutoff=0.02)
    polyline([d, a, b], 0.42, 100)
    polyline([b, sb], 0.46, 100); polyline([sb, sc], 0.5, 100)
    polyline([c, b], 0.34, 92)
    polyline([d, c], 0.3, 88); polyline([d, td], 0.3, 88); polyline([td, sc], 0.3, 88)

def staves():
    emit("% ---- staves and rings ----")
    y0, y1 = 0.34, 0.54            # near stave, through front rings
    x0, x1 = -1.55, 6.1
    def tone_stave(x, y):
        u = clamp((y - y0)/(y1 - y0))
        t = 0.08 + 0.42 * (1 - u) ** 2         # dark under-curve
        t -= 0.06 * math.exp(-((u - 0.7)/0.2)**2)  # highlight
        return clamp(t)
    hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 0, 0.030, tone_stave,
          wmax=0.24, seg_len=0.3)
    # rounded tips
    for tx, sgn in ((x0, -1), (x1, 1)):
        pts = []
        for i in range(13):
            th = math.pi/2 - i*math.pi/12
            pts.append((tx + sgn*0.14*math.cos(th)*1.15,
                        (y0+y1)/2 + 0.5*(y1-y0)*math.sin(th)))
        polyline(pts, 0.34, 100)
    polyline([(x0, y0), (x1, y0)], 0.4, 100)
    polyline([(x0, y1), (x1, y1)], 0.3, 92)
    # far stave tip beyond the side face
    fy0, fy1 = y0 + DY*0.97, y1 + DY*0.97
    fx0, fx1 = 6.72, 7.7
    def tone_far(x, y):
        u = clamp((y - fy0)/(fy1 - fy0))
        return clamp(0.14 + 0.4 * (1 - u) ** 2)
    hatch([(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)], 0, 0.03, tone_far,
          wmax=0.22, seg_len=0.25)
    pts = []
    for i in range(13):
        th = math.pi/2 - i*math.pi/12
        pts.append((fx1 + 0.13*math.cos(th)*1.15,
                    (fy0+fy1)/2 + 0.5*(fy1-fy0)*math.sin(th)))
    polyline(pts, 0.3, 100)
    polyline([(fx0, fy0), (fx1, fy0)], 0.36, 100)
    polyline([(fx0, fy1), (fx1, fy1)], 0.26, 90)

    # rings: tori with crescent shading
    for cx in (0.35, 4.65):
        emit(f"\\draw[line width=0.5pt, black] ({cx},0.44) ellipse (0.165 and 0.2);")
        emit(f"\\draw[line width=0.28pt, black!75] ({cx},0.44) ellipse (0.085 and 0.115);")
        # weight on the lower-left of the torus
        emit(f"\\draw[line width=0.7pt, black] ({cx-0.117},0.30) "
             f"arc[start angle=220, end angle=320, x radius=0.165, y radius=0.2];")
        emit(f"\\draw[line width=0.34pt, black!70] ({cx-0.06},0.35) "
             f"arc[start angle=225, end angle=315, x radius=0.085, y radius=0.115];")

def ground_shadow():
    emit("% ---- cast shadow ----")
    # soft-edged pool to the lower right; density falls off outward
    core = (3.4, -0.28)
    def tone_sh(x, y):
        dx = (x - core[0]) / 3.2; dy = (y - core[1]) / 0.30
        r = math.hypot(dx, dy)
        return clamp(0.30 * (1 - r) * 1.4, 0, 0.30)
    hatch([(0.1, -0.55), (6.9, -0.55), (7.6, -0.05), (0.9, -0.05)],
          0, 0.055, tone_sh, wmax=0.2, cutoff=0.02, seg_len=0.22)

# --------------------------------------------------------------- the cherub
def feather(base, tip, half_w, curve, layer_fill=True,
            w_rachis=0.22, barbs=True, gray=88):
    """One feather: white-filled vane, rachis, barb texture.

    base, tip: endpoints of the rachis. curve: sideways bow of the vane
    (positive = bow left of base->tip direction).
    """
    bx, by = base; tx, ty = tip
    dx, dy = tx - bx, ty - by
    L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
    nx, ny = -uy, ux
    # vane outline: two curves base->tip bowed to each side
    c1a = (bx + ux*L*0.3 + nx*(half_w + curve), by + uy*L*0.3 + ny*(half_w + curve))
    c1b = (bx + ux*L*0.75 + nx*(half_w*0.8 + curve), by + uy*L*0.75 + ny*(half_w*0.8 + curve))
    c2a = (bx + ux*L*0.75 - nx*(half_w*0.8 - curve), by + uy*L*0.75 - ny*(half_w*0.8 - curve))
    c2b = (bx + ux*L*0.3 - nx*(half_w - curve), by + uy*L*0.3 - ny*(half_w - curve))
    path = (f"({bx:.3f},{by:.3f}) .. controls ({c1a[0]:.3f},{c1a[1]:.3f}) and "
            f"({c1b[0]:.3f},{c1b[1]:.3f}) .. ({tx:.3f},{ty:.3f}) .. controls "
            f"({c2a[0]:.3f},{c2a[1]:.3f}) and ({c2b[0]:.3f},{c2b[1]:.3f}) .. "
            f"({bx:.3f},{by:.3f})")
    if layer_fill:
        emit(f"\\fill[white] {path} -- cycle;")
    emit(f"\\draw[line width=0.24pt, black!{gray}] {path};")
    # rachis, slightly bowed with the curve
    ra = (bx + ux*L*0.35 + nx*curve*0.7, by + uy*L*0.35 + ny*curve*0.7)
    rb = (bx + ux*L*0.75 + nx*curve*0.7, by + uy*L*0.75 + ny*curve*0.7)
    emit(f"\\draw[line width={w_rachis}pt, black!{gray}] ({bx:.3f},{by:.3f}) "
         f".. controls ({ra[0]:.3f},{ra[1]:.3f}) and ({rb[0]:.3f},{rb[1]:.3f}) "
         f".. ({tx:.3f},{ty:.3f});")
    if barbs:
        nb = max(3, int(L / 0.09))
        for i in range(1, nb):
            t = i / nb
            px = bx + ux*L*t + nx*curve*0.7*math.sin(math.pi*t)
            py = by + uy*L*t + ny*curve*0.7*math.sin(math.pi*t)
            blen = half_w * (0.85 - 0.45*abs(t - 0.45)) * 0.9
            ang = math.atan2(uy, ux) + math.radians(38)
            for s in (1, -1):
                a2 = math.atan2(uy, ux) + s*math.radians(42)
                q = (px + blen*math.cos(a2), py + blen*math.sin(a2))
                emit(f"\\draw[line width=0.09pt, black!55] ({px:.3f},{py:.3f}) "
                     f"-- ({q[0]:.3f},{q[1]:.3f});")

def cherub():
    """Left cherub, kneeling, bowed toward +x; wing sweeps up and forward.

    Draw order: far wing, main wing (deep rows first), body, arms, head ---
    each later element white-fills over the earlier, as in a layered plate.
    """
    emit("% ---- cherub ----")
    # wing chord frame -----------------------------------------------------
    Lb = bez((1.14,5.30),(1.30,6.05),(2.10,6.42),(3.30,6.06), n=60)
    Tb = bez((1.54,5.17),(2.02,5.36),(2.72,5.62),(3.30,6.06), n=60)
    def L(t):
        i = min(int(t*60), 60); return Lb[i]
    def T(t):
        i = min(int(t*60), 60); return Tb[i]
    def S(t, u):
        a, b = L(t), T(t)
        return (a[0]*(1-u)+b[0]*u, a[1]*(1-u)+b[1]*u)
    def beyond(t, u_from, u_to, over):
        a, b = S(t, u_from), S(t, u_to)
        dx, dy = b[0]-a[0], b[1]-a[1]
        n = math.hypot(dx, dy) or 1
        return (b[0] + dx/n*over, b[1] + dy/n*over)

    # far wing: falls behind the back, a few long shaded feathers
    emit("% far wing")
    for i, (b, t, w) in enumerate([
            ((1.10,5.06),(0.76,4.28),0.065),
            ((1.20,5.04),(0.94,4.20),0.058),
            ((1.28,5.02),(1.10,4.16),0.05)]):
        feather(b, t, w, 0.02, gray=55, w_rachis=0.12, barbs=False)

    # main wing ------------------------------------------------------------
    emit("% principal wing, feather rows from deep to near")
    # primaries: blades lying along the surface, sweeping to the tip
    for k in range(7):
        t = 0.45 + 0.078*k
        base = S(t, 0.30)
        t2 = min(t + 0.17, 1.0)
        tip = S(t2, 1.0)
        if t2 < 0.99:
            a, b = S(t, 0.55), S(t2, 1.0)
            d = math.hypot(b[0]-a[0], b[1]-a[1]) or 1
            over = 0.10 * (1 - max(0, t - 0.75)/0.25)
            tip = (b[0] + (b[0]-a[0])/d*over, b[1] + (b[1]-a[1])/d*over)
        feather(base, tip, 0.060 - 0.003*k, 0.014, gray=92)
    # secondaries: inner surface, same sweep
    for k in range(6):
        t = 0.06 + 0.075*k
        base = S(t, 0.22)
        tip = S(min(t + 0.15, 1.0), 1.0)
        feather(base, tip, 0.070, 0.012, gray=84)
    # covert row 1
    for k in range(8):
        t = 0.06 + 0.105*k
        base = S(t, 0.04)
        tip = S(min(t + 0.15, 1.0), 0.56)
        feather(base, tip, 0.048, 0.010, gray=72, w_rachis=0.13, barbs=False)
    # covert row 0, smallest, nearest the leading edge
    for k in range(10):
        t = 0.04 + 0.096*k
        base = S(t, 0.0)
        tip = S(min(t + 0.12, 1.0), 0.30)
        feather(base, tip, 0.036, 0.008, gray=62, w_rachis=0.11, barbs=False)
    # leading edge: bold doubled sweep
    emit("\\draw[line width=0.6pt, black] (1.14,5.30) .. controls (1.30,6.05) and "
         "(2.10,6.42) .. (3.30,6.06);")
    emit("\\draw[line width=0.24pt, black!70] (1.19,5.31) .. controls (1.34,5.99) and "
         "(2.10,6.34) .. (3.25,6.02);")

    # body -----------------------------------------------------------------
    emit("% body")
    robe = []
    robe += bez((1.78, 3.86), (1.80, 4.10), (1.72, 4.34), (1.63, 4.52))
    robe += bez((1.63, 4.52), (1.68, 4.70), (1.72, 4.88), (1.69, 5.04))
    robe += bez((1.69, 5.04), (1.66, 5.16), (1.58, 5.24), (1.47, 5.28))
    robe += bez((1.47, 5.28), (1.32, 5.33), (1.18, 5.30), (1.11, 5.21))
    robe += bez((1.11, 5.21), (1.03, 5.08), (1.02, 4.92), (1.04, 4.76))
    robe += bez((1.04, 4.76), (1.05, 4.46), (1.02, 4.14), (1.00, 3.86))
    robe.append((1.78, 3.86))
    emit("\\fill[white] " + " -- ".join(f"({x:.3f},{y:.3f})" for x, y in robe) + " -- cycle;")
    folds = [1.16, 1.30, 1.46]
    def tone_robe(x, y):
        if y > 5.26: return 0.0
        t = 0.075 + 0.22 * clamp((1.52 - x)/0.52)
        for fx in folds:
            t += 0.12 * math.exp(-((x - fx)/0.04)**2)
        t += 0.10 * clamp((4.05 - y)/0.25)
        t += 0.11 * math.exp(-((y - 4.60)/0.26)**2) * clamp((x - 1.35)/0.3)
        t -= 0.04 * clamp((x - 1.58)/0.2)
        return clamp(t)
    hatch(robe, 96, 0.034, tone_robe, wmax=0.19, seg_len=0.10, cutoff=0.03)
    vary_outline(robe, 0.34, 0.34)
    for fx in folds:
        emit(f"\\draw[line width=0.13pt, black!55] ({fx+0.015},3.88) "
             f".. controls ({fx-0.01},4.4) and ({fx-0.02},4.8) .. ({fx-0.05},5.08);")
    emit("\\draw[line width=0.3pt, black!85] (1.02,3.845) -- (1.76,3.845);")

    # arms crossed on the breast
    emit("\\fill[white] (1.42,4.97) .. controls (1.55,4.93) and (1.65,4.85) .. (1.69,4.73)"
         " .. controls (1.71,4.81) and (1.67,4.93) .. (1.57,5.01)"
         " .. controls (1.50,5.05) and (1.44,5.04) .. (1.42,4.97) -- cycle;")
    emit("\\draw[line width=0.24pt, black!85] (1.42,4.97) .. controls (1.55,4.93) and "
         "(1.65,4.85) .. (1.69,4.73);")
    emit("\\draw[line width=0.18pt, black!65] (1.45,4.89) .. controls (1.54,4.85) and "
         "(1.61,4.79) .. (1.65,4.71);")

    # head, bowed profile --------------------------------------------------
    emit("% head")
    # scaled 1.15 about (1.48,5.40): skull, face line, hair following the crown
    emit("\\fill[white] (1.27,5.28) .. controls (1.22,5.54) and (1.41,5.68) .. (1.57,5.61)"
         " .. controls (1.69,5.55) and (1.71,5.44) .. (1.665,5.36)"
         " .. controls (1.715,5.32) and (1.715,5.285) .. (1.69,5.255)"
         " .. controls (1.685,5.235) and (1.665,5.228) .. (1.65,5.231)"
         " .. controls (1.638,5.208) and (1.612,5.202) .. (1.594,5.212)"
         " .. controls (1.52,5.17) and (1.41,5.17) .. (1.34,5.21) -- cycle;")
    # face line: brow, nose, lip, chin
    emit("\\draw[line width=0.26pt, black!95] "
         "(1.665,5.36) .. controls (1.715,5.32) and (1.715,5.285) .. (1.69,5.255)"
         " .. controls (1.685,5.235) and (1.665,5.228) .. (1.65,5.231)"
         " .. controls (1.638,5.208) and (1.612,5.202) .. (1.594,5.212);")
    # jaw
    emit("\\draw[line width=0.2pt, black!80] (1.594,5.212) .. controls (1.53,5.176) and "
         "(1.44,5.176) .. (1.375,5.212);")
    # crown outline
    emit("\\draw[line width=0.3pt, black!95] (1.27,5.28) .. controls (1.22,5.54) and "
         "(1.41,5.68) .. (1.57,5.61) .. controls (1.66,5.567) and (1.694,5.46) .. (1.665,5.36);")
    # hair: nested arcs following the crown, forehead to nape
    crown = bez((1.315,5.245), (1.235,5.53), (1.42,5.685), (1.60,5.60), n=30)
    ctr = (1.47, 5.40)
    for k in range(6):
        f = 1.0 - 0.10*k
        pts = [(ctr[0] + (x-ctr[0])*f, ctr[1] + (y-ctr[1])*f) for x, y in crown]
        lo = 2 + k; hi = len(pts) - 1 - k//2
        polyline(pts[lo:hi], 0.11, 70)
    # closed eye, serene
    emit("\\draw[line width=0.12pt, black!85] (1.627,5.297) .. controls (1.642,5.289) and "
         "(1.658,5.289) .. (1.668,5.295);")
    # neck into collar
    emit("\\draw[line width=0.16pt, black!60] (1.45,5.195) .. controls (1.475,5.14) and "
         "(1.50,5.10) .. (1.52,5.05);")

def cherubim():
    emit("% left cherub")
    emit("\\begin{scope}")
    cherub()
    emit("\\end{scope}")
    emit("% right cherub, mirrored about the slab centre")
    emit("\\begin{scope}[shift={(6.7,0)}, xscale=-1]")
    cherub()
    emit("\\end{scope}")

# --------------------------------------------------------------- assembly
def labels():
    emit("% ---- dimensions ----")
    emit("\\draw[line width=0.2pt, black!70, {Stealth[length=1.4mm]}-{Stealth[length=1.4mm]}] (0,-0.72) -- (5,-0.72);")
    emit("\\node[stiny] at (2.5,-1.04) {two cubits and a half};")
    emit("\\draw[line width=0.2pt, black!70, {Stealth[length=1.4mm]}-{Stealth[length=1.4mm]}] (-0.66,0) -- (-0.66,3);")
    emit("\\node[stiny, rotate=90] at (-1.02,1.5) {a cubit and a half};")
    emit("\\draw[line width=0.2pt, black!70, {Stealth[length=1.4mm]}-{Stealth[length=1.4mm]}] (5.6,-0.45) -- (7.3,0.5);")
    emit("\\node[stiny, anchor=west] at (7.42,-0.02) {a cubit and a half};")
    emit("% ---- labels ----")
    emit("\\node[slabel, anchor=west] (lc) at (8.2,5.7) {cherubims of beaten gold, their wings\\\\covering, their faces toward each other\\\\and toward the propitiatory};")
    emit("\\draw[line width=0.2pt, black!70] (lc.west) -- (5.0,5.8);")
    emit("\\node[slabel, anchor=west] (lp) at (8.2,4.35) {the propitiatory,\\\\of the purest gold};")
    emit("\\draw[line width=0.2pt, black!70] (lp.west) -- (6.55,4.12);")
    emit("\\node[slabel, anchor=west] (lk) at (8.2,3.1) {``a golden crown round about''\\\\(Ex 25:11)};")
    emit("\\draw[line width=0.2pt, black!70] (lk.west) -- (6.4,3.6);")
    emit("\\node[slabel, anchor=west] (lw) at (8.2,2.0) {setim wood, overlaid with gold\\\\within and without};")
    emit("\\draw[line width=0.2pt, black!70] (lw.west) -- (6.4,2.2);")
    emit("\\node[slabel, anchor=west] (ls) at (8.2,0.9) {the staves, always in the rings};")
    emit("\\draw[line width=0.2pt, black!70] (ls.west) -- (7.55,1.3);")

def main():
    emit("% Drawing: the ark as commanded (Ex 25:10-22).  Rendered plate:")
    emit("% strokes generated from a modeled scene (research note in scope.md);")
    emit("% forms beyond Scripture's measures are editorial conjecture.")
    emit("\\begin{sketchfig}")
    emit("\\begin{tikzpicture}[scale=0.82]")
    ground_shadow()
    chest()
    molding()
    slab()
    cherubim()
    staves()
    labels()
    emit("\\end{tikzpicture}")
    emit("""\\sketchcaption{The ark as commanded. The measures are Scripture's (Exodus
25:10--22, Douay wording in the labels); the forms are not --- Scripture
nowhere describes the cherubims' shape, and this reconstruction is editorial
conjecture, drawn to fix the parts and their names, not the look.}
\\end{sketchfig}""")
    path = 'src/claude/theology/mariology/ark-of-the-covenant/figures/fig-ark.tex'
    with open(path, 'w') as f:
        f.write("\n".join(OUT) + "\n")
    print(f"wrote {path}: {len(OUT)} lines")

if __name__ == '__main__':
    main()
