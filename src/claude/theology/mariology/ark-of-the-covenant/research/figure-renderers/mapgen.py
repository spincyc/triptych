#!/usr/bin/env python3
"""Relief hachures for the journey map (fig-journey.tex).

Builds a coarse elevation model of the southern Levant in map coordinates
(x = (lon-34.2)*6, y = (lat-31.05)*6), computes slope and aspect, and emits
downslope hachure strokes whose weight follows slope and a north-west light,
in the manner of the nineteenth-century engraved relief maps.
"""
import math, random

rnd = random.Random(19620815)

# ---------------------------------------------------------------- the relief
def ridge(pts, h, sigma):
    """Gaussian-section ridge along a polyline."""
    def ele(x, y):
        best = 1e9
        for i in range(len(pts) - 1):
            ax, ay = pts[i]; bx, by = pts[i+1]
            dx, dy = bx - ax, by - ay
            L2 = dx*dx + dy*dy
            t = 0 if L2 == 0 else max(0, min(1, ((x-ax)*dx + (y-ay)*dy)/L2))
            px, py = ax + t*dx, ay + t*dy
            d = math.hypot(x - px, y - py)
            best = min(best, d)
        return h * math.exp(-(best/sigma)**2)
    return ele

FEATURES = [
    # central Judea-Samaria massif
    ridge([(5.0,-0.8),(5.3,1.0),(5.7,2.4),(6.05,3.6),(6.15,4.38),(6.3,5.4),
           (6.5,6.5),(6.5,7.4),(6.3,8.3),(6.1,9.2),(5.9,9.9)], 1.0, 0.62),
    # Ebal and Garizim knolls
    ridge([(6.46,7.26),(6.62,7.32)], 0.34, 0.24),
    ridge([(6.28,6.68),(6.44,6.66)], 0.28, 0.20),
    # Shephelah foothills
    ridge([(4.3,0.6),(4.6,2.2),(4.9,3.4),(5.1,4.4),(5.2,5.3),(5.3,6.0)], 0.34, 0.38),
    # Carmel
    ridge([(4.66,10.65),(5.2,10.05),(5.75,9.7)], 0.55, 0.24),
    # Lower Galilee hills
    ridge([(5.9,10.4),(6.6,10.7),(7.3,10.8)], 0.35, 0.5),
    ridge([(6.1,11.4),(6.9,11.6)], 0.5, 0.55),
    # Transjordan plateau (broad) with a sharper western rim
    ridge([(9.4,0.5),(9.5,2.5),(9.5,4.5),(9.45,6.5),(9.35,8.5),(9.3,11.5)],
          1.05, 0.95),
    ridge([(8.95,0.8),(9.0,2.6),(9.0,4.4),(8.95,6.2),(8.9,8.2),(8.85,11.0)],
          0.22, 0.30),
    # Nebo knoll on the rim
    ridge([(9.08,4.26),(9.32,4.33)], 0.30, 0.23),
]
RIVER = [(7.8,0.2),(7.8,2.0),(7.8,4.3),(7.95,6.0),(8.05,8.0),
         (8.2,9.9),(8.3,11.8)]
RIFT = ridge(RIVER, 1.05, 0.30)

def elevation(x, y):
    e = sum(f(x, y) for f in FEATURES)
    return e - RIFT(x, y)

EPS = 0.045
def grad(x, y):
    gx = (elevation(x+EPS, y) - elevation(x-EPS, y)) / (2*EPS)
    gy = (elevation(x, y+EPS) - elevation(x, y-EPS)) / (2*EPS)
    return gx, gy

# ---------------------------------------------------------------- the masks
def x_coast(y):
    pts = [(-0.1,0.52),(1.3,1.05),(2.4,1.68),(3.72,2.22),(4.7,2.72),
           (6.0,3.30),(7.4,3.55),(8.7,4.14),(9.42,4.32),(10.68,4.62),
           (11.3,4.95),(12.05,5.5)]
    for i in range(len(pts)-1):
        y0, x0 = pts[i]; y1, x1 = pts[i+1]
        if y0 <= y <= y1:
            t = (y - y0)/(y1 - y0)
            return x0 + t*(x1 - x0)
    return pts[-1][1] if y > pts[-1][0] else pts[0][1]

SALT = [(7.8,4.32),(7.45,3.1),(7.35,2.4),(7.5,1.1),(7.85,0.72),
        (8.3,0.85),(8.22,2.35),(8.42,2.8),(8.32,3.95)]
def in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1)/(y2 - y1)*(x2 - x1)
            if x < xi: inside = not inside
    return inside

def seg_dist(x, y, pts):
    best = 1e9
    for i in range(len(pts) - 1):
        ax, ay = pts[i]; bx, by = pts[i+1]
        dx, dy = bx - ax, by - ay
        L2 = dx*dx + dy*dy
        t = 0 if L2 == 0 else max(0, min(1, ((x-ax)*dx + (y-ay)*dy)/L2))
        best = min(best, math.hypot(x - ax - t*dx, y - ay - t*dy))
    return best

def masked(x, y):
    if x < x_coast(y) + 0.14: return True                 # the Great Sea
    if in_poly(x, y, SALT): return True                   # the Salt Sea
    if seg_dist(x, y, SALT + SALT[:1]) < 0.13: return True
    if math.hypot((x-8.4)/0.46, (y-10.45)/0.66) < 1.18: return True  # Galilee
    if seg_dist(x, y, RIVER) < 0.17: return True          # the Jordan channel
    if not (0.12 < x < 11.08 and 0.02 < y < 11.93): return True      # frame
    return False

# ------------------------------------------------------------- the hachures
LIGHT = (-0.7071, 0.7071)     # from the north-west

def strokes():
    out = []
    out.append("% ---- terrain: relief hachures from the elevation model ----")
    step = 0.13
    ny = int(12.0/step); nx = int(11.2/step)
    for j in range(ny):
        for i in range(nx):
            x = 0.06 + i*step + rnd.uniform(-0.4, 0.4)*step
            y = 0.04 + j*step + rnd.uniform(-0.4, 0.4)*step
            if masked(x, y): continue
            gx, gy = grad(x, y)
            sl = math.hypot(gx, gy)
            if sl < 0.42: continue
            dxn, dyn = -gx/sl, -gy/sl          # downhill
            # illumination: slopes facing away from the light darker
            facing = dxn*LIGHT[0] + dyn*LIGHT[1]
            L = min(0.085 + 0.075*sl, 0.24)
            w = 0.09 + 0.09*min(sl, 1.8)/1.8 + 0.05*max(0.0, -facing)
            g = int(min(34 + 20*min(sl, 1.8) + 13*max(0.0, -facing), 80))
            # slight downhill curvature
            mx = x + dxn*L*0.5 + -dyn*0.15*L*rnd.uniform(-1, 1)
            my = y + dyn*L*0.5 + dxn*0.15*L*rnd.uniform(-1, 1)
            ex, ey = x + dxn*L, y + dyn*L
            out.append(
                f"\\draw[line width={w:.2f}pt, black!{g}] ({x:.3f},{y:.3f}) "
                f".. controls ({mx:.3f},{my:.3f}) and ({mx:.3f},{my:.3f}) .. "
                f"({ex:.3f},{ey:.3f});")
    # labels that live in the terrain
    out.append("\\node[stiny, black!80, fill=white, inner sep=1pt] at (9.95,3.55) {Nebo:\\\\the hidden-ark\\\\tradition\\\\(2 Mach 2)};")
    out.append("\\node[stiny, anchor=west, black!70, fill=white, inner sep=0.8pt] at (7.02,7.2) {Ebal};")
    out.append("\\node[stiny, black!60, rotate=75, fill=white, fill opacity=0.75, text opacity=1, inner sep=0.8pt] at (5.05,2.8) {\\emph{the hill country}};")
    return out

def main():
    path = 'src/claude/theology/mariology/ark-of-the-covenant/figures/fig-journey.tex'
    s = open(path).read()
    start = s.index("% ---- terrain:")
    end = s.index("% ---- the route of the ark")
    block = "\n".join(strokes()) + "\n"
    s = s[:start] + block + s[end:]
    open(path, 'w').write(s)
    print(f"terrain block: {len(block.splitlines())} lines")

if __name__ == '__main__':
    main()
