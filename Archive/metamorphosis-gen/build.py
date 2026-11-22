#!/usr/bin/env python3
"""Generates the woodcut webtoon page for The Metamorphosis.
All art is procedural/hand-placed SVG: rough polygons + tapered gouge strokes."""
import math, random, html as H

INK = '#0e0c0a'
PAPER = '#ece3d0'
RUST = '#8c3b1a'
OUT = '/home/user/layhengportflio/Portfolio 2026/samples/metamorphosis/index.html'

rng = random.Random(1915)
_id = [0]
def uid(p='c'):
    _id[0] += 1
    return f'{p}{_id[0]}'

def f(v):
    return str(int(round(v)))

def D(pts, closed=True):
    s = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    return s + (' Z' if closed else '')

def rough(pts, step=16, amp=2.4, closed=True, r=None):
    r = r or rng
    out = []
    n = len(pts)
    rng_edges = range(n if closed else n - 1)
    for i in rng_edges:
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
        L = math.hypot(x1 - x0, y1 - y0)
        k = max(1, int(L / step))
        nx, ny = (-(y1 - y0) / (L or 1), (x1 - x0) / (L or 1))
        for j in range(k):
            t = j / k
            a = 0 if j == 0 else r.uniform(-amp, amp)
            out.append((x0 + (x1 - x0) * t + nx * a, y0 + (y1 - y0) * t + ny * a))
    if not closed:
        out.append(pts[-1])
    return out

def poly(pts, fill=INK, step=16, amp=2.4, extra=''):
    return f'<path d="{D(rough(pts, step, amp))}" fill="{fill}"{extra}/>'

def ellipse_pts(cx, cy, rx, ry, n=48, a0=0, a1=2 * math.pi, squash=None):
    pts = []
    for i in range(n):
        t = a0 + (a1 - a0) * i / n
        y = ry * math.sin(t)
        if squash:
            y *= squash(t)
        pts.append((cx + rx * math.cos(t), cy + y))
    return pts

def taper(pts, w0, w1, fill=INK, cap=True):
    """Tapered stroke along a polyline -> filled polygon."""
    n = len(pts)
    # cumulative length
    cum = [0]
    for i in range(1, n):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    T = cum[-1] or 1
    left, right = [], []
    for i in range(n):
        if i == 0:
            dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * cum[i] / T) / 2
        left.append((pts[i][0] + nx * w, pts[i][1] + ny * w))
        right.append((pts[i][0] - nx * w, pts[i][1] - ny * w))
    return f'<path d="{D(left + right[::-1])}" fill="{fill}"/>'

def curve(p0, p1, bend=0.0, n=10, wob=0.0, r=None):
    """Points along a gently bent line from p0 to p1."""
    r = r or rng
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    pts = []
    for i in range(n + 1):
        t = i / n
        b = math.sin(t * math.pi) * bend * L
        w = r.uniform(-wob, wob) if 0 < i < n else 0
        pts.append((x0 + (x1 - x0) * t + nx * (b + w), y0 + (y1 - y0) * t + ny * (b + w)))
    return pts

def gouge(x, y, ang, length, w, fill=PAPER, bend=None, r=None):
    """One carved stroke: wide at the start, tapering to a point."""
    r = r or rng
    bend = r.uniform(-.08, .08) if bend is None else bend
    p1 = (x + math.cos(ang) * length, y + math.sin(ang) * length)
    return taper(curve((x, y), p1, bend, 3), w, 0.3, fill)

def gouges(box, ang, n, lmin, lmax, wmin, wmax, fill=PAPER, jit=.12, r=None, clip=None):
    r = r or rng
    x0, y0, x1, y1 = box
    out = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        out.append(gouge(x, y, ang + r.uniform(-jit, jit), r.uniform(lmin, lmax), r.uniform(wmin, wmax), fill, r=r))
    g = ''.join(out)
    if clip:
        cid = uid('k')
        return f'<clipPath id="{cid}"><path d="{clip}"/></clipPath><g clip-path="url(#{cid})">{g}</g>'
    return g

def rows(box, ang, gap, wmin, wmax, fill=PAPER, broken=.25, r=None, clip=None, lfrac=(0.5, 1.0)):
    """Parallel carved rows (like a gouge pulled across a block)."""
    r = r or rng
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = math.hypot(x1 - x0, y1 - y0) / 2
    dx, dy = math.cos(ang), math.sin(ang)
    nx, ny = -dy, dx
    out = []
    k = -R
    while k < R:
        # a row split in pieces
        s = -R
        while s < R:
            seg = r.uniform(R * .15, R * .6) * r.uniform(*lfrac)
            if r.random() > broken:
                px, py = cx + nx * k + dx * s, cy + ny * k + dy * s
                out.append(gouge(px, py, ang + r.uniform(-.03, .03), seg, r.uniform(wmin, wmax), fill, bend=r.uniform(-.03, .03), r=r))
            s += seg + r.uniform(4, 30)
        k += gap * r.uniform(.8, 1.25)
    g = ''.join(out)
    if clip:
        cid = uid('k')
        return f'<clipPath id="{cid}"><path d="{clip}"/></clipPath><g clip-path="url(#{cid})">{g}</g>'
    return g

def rot(pts, a, cx=0, cy=0):
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]

# ---------------------------------------------------------------- the insect
def leg(points, widths, spines=True, fill=INK, r=None, hi=True):
    """points: list of joints; widths per joint."""
    r = r or rng
    out = []
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        seg = curve(a, b, r.uniform(-.05, .05), 5)
        out.append(taper(seg, widths[i], widths[i + 1], fill))
        # knuckle
        out.append(f'<circle cx="{f(b[0])}" cy="{f(b[1])}" r="{f(widths[i+1]*0.62)}" fill="{fill}"/>')
        if spines and i == 1:
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            m = int(L / 16)
            for j in range(1, m):
                t = j / m
                px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                side = 1 if j % 2 else -1
                sa = ang + side * 0.9 - 0.25
                out.append(gouge(px, py, sa, r.uniform(9, 16), 3.2, fill, bend=0, r=r))
        if hi and i < 2:
            # carved highlight along the limb
            mx, my = (a[0] * .7 + b[0] * .3), (a[1] * .7 + b[1] * .3)
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            out.append(gouge(mx, my - widths[i] * .15, ang, L * .5, max(1.2, widths[i] * .22), PAPER, bend=0, r=r))
    return ''.join(out)

def body_parts():
    abd = ellipse_pts(190, 0, 205, 128, 56)
    pron = []
    for i in range(48):
        t = 2 * math.pi * i / 48
        x = 445 + 92 * math.cos(t)
        y = 150 * math.sin(t) * (0.86 + 0.14 * math.cos(t))
        pron.append((x, y))
    head = ellipse_pts(566, 0, 46, 58, 32)
    return abd, pron, head

def abd_half(x):
    v = 1 - ((x - 190) / 205) ** 2
    return 128 * math.sqrt(max(0, v))

SEGS = [30, 72, 114, 156, 198, 240, 282, 322, 360]

def insect_top(r, twitch=True, legs_only=False, uid_=''):
    """Top view, head toward +x. ~1000 units across with legs/antennae."""
    parts = []
    LEGS = [
        # attach, femur end, tibia end, tarsus end (y for the near side; mirrored for far side)
        ((405, 95), (300, 240), (130, 310), (30, 350)),
        ((455, 110), (480, 270), (420, 410), (395, 480)),
        ((505, 95), (590, 225), (700, 300), (790, 315)),
    ]
    legsvg = []
    for side in (1, -1):
        for k, (a, b, c, d) in enumerate(LEGS):
            pts = [(a[0], a[1] * side), (b[0], b[1] * side), (c[0], c[1] * side), (d[0], d[1] * side)]
            g = leg(pts, [27, 18, 9, 3], r=r)
            if twitch:
                dur = [1.7, 2.3, 1.3, 2.9, 1.9, 2.6][k + (3 if side < 0 else 0)]
                amp = 4 + k * 2
                g = (f'<g>{g}<animateTransform attributeName="transform" type="rotate" '
                     f'values="0 {a[0]} {a[1]*side};{amp*side} {a[0]} {a[1]*side};{-amp*.6*side} {a[0]} {a[1]*side};0 {a[0]} {a[1]*side}" '
                     f'keyTimes="0;.3;.62;1" dur="{dur}s" repeatCount="indefinite"/></g>')
            legsvg.append(g)
    parts.append(f'<g class="legs">{"".join(legsvg)}</g>')
    if legs_only:
        return ''.join(parts)
    abd, pron, head = body_parts()
    # antennae
    for side in (1, -1):
        pts = []
        for i in range(24):
            t = i / 23
            x = 595 + t * 420
            y = side * (30 + t * 160 + math.sin(t * 5) * 22 * t)
            pts.append((x, y))
        a = taper(pts, 6, .8)
        a = (f'<g>{a}<animateTransform attributeName="transform" type="rotate" values="0 595 {30*side};{3*side} 595 {30*side};0 595 {30*side}" '
             f'dur="{3.1 if side>0 else 2.4}s" repeatCount="indefinite"/></g>')
        parts.append(a)
    parts.append(poly(abd, step=12, amp=2.5))
    parts.append(poly(head, step=10, amp=2))
    # mandibles
    for side in (1, -1):
        parts.append(taper([(598, 14 * side), (622, 22 * side), (636, 10 * side), (630, 2 * side)], 9, 2))
    parts.append(poly(pron, step=12, amp=2.2))
    # carving: segment seams on the abdomen (bowed toward tail)
    carve = []
    for x in SEGS:
        h = abd_half(x) - 7
        if h < 20:
            continue
        pts = []
        for i in range(13):
            t = -1 + 2 * i / 12
            pts.append((x + 16 * (1 - t * t) * -1 + 10, t * h))
        # break the seam into two or three carved pieces
        cut = r.randint(3, 5)
        carve.append(taper(pts[:cut + 1], 1.5, 5.5, PAPER))
        carve.append(taper(pts[cut + 1:], 5, 1.2, PAPER))
    # light from upper left: short gouges between seams on the upper half
    for i in range(len(SEGS) - 1):
        xa, xb = SEGS[i], SEGS[i + 1]
        for _ in range(7):
            x = r.uniform(xa + 8, xb - 6)
            h = abd_half(x)
            y = r.uniform(-h * .92, -h * .15)
            carve.append(gouge(x, y, math.pi / 2 + r.uniform(-.3, .3), r.uniform(10, 26), r.uniform(1.4, 3), r=r))
    # ridge along the back
    carve.append(taper(curve((14, -10), (370, -14), .02, 12, 1.5, r), 1, 4, PAPER))
    # rim light on the upper edge of the abdomen
    rim = [(x, -abd_half(x) + 9) for x in range(10, 380, 12)]
    carve.append(taper(rim, 1, 3.5, PAPER))
    # pronotum: carved concentric arcs following the rim
    for k, (rx, ry, w) in enumerate(((80, 134, 4.2),)):
        arc = [(445 + rx * math.cos(t), ry * math.sin(t) * (0.86 + 0.14 * math.cos(t))) for t in [(-2.5 + i * .16) for i in range(int(31 - k * 4))]]
        cut = r.randint(6, 12)
        carve.append(taper(arc[:cut], 1, w, PAPER))
        carve.append(taper(arc[cut + 2:], w, .8, PAPER))
    for i in range(10):
        t = r.uniform(-2.4, -.6)
        carve.append(gouge(445 + 70 * math.cos(t), 118 * math.sin(t), t + math.pi + r.uniform(-.2, .2), r.uniform(10, 22), r.uniform(1.2, 2.4), r=r))
    # head: dark compound eyes with a carved glint, segmented mouthparts
    for side in (1, -1):
        e = rot(ellipse_pts(572, 36 * side, 16, 10, 14), .5 * side, 572, 36 * side)
        carve.append(gouge(566, 32 * side - 3, -.3, 9, 2.6, r=r))
    for k in range(3):
        carve.append(taper([(530 + k * 18, -40 + k * 6), (538 + k * 18, 0), (530 + k * 18, 40 - k * 6)], 1, 2.4, PAPER))
    parts.append(f'<g>{"".join(carve)}</g>')
    return ''.join(parts)

def insect_belly(r, twitch=True):
    """On his back: brown domed belly in stiff sections, legs waving up."""
    parts = []
    abd, pron, head = body_parts()
    parts.append(poly(abd, step=12, amp=2.4))
    parts.append(poly(pron, step=12, amp=2.4))
    parts.append(poly(head, step=10, amp=2))
    # rust plates between the arches
    plates = []
    segs = [10] + SEGS + [392]
    for i in range(len(segs) - 1):
        xa, xb = segs[i] + 5, segs[i + 1] - 5
        top, bot = [], []
        for j in range(11):
            t = -1 + 2 * j / 10
            ha, hb = abd_half(xa + 3) - 12, abd_half(xb) - 12
            if ha < 8 or hb < 8:
                continue
            top.append((xa - 16 * (1 - t * t) + 12, t * ha))
            bot.append((xb - 16 * (1 - t * t) + 12, t * hb))
        if len(top) > 3:
            plates.append(poly(top + bot[::-1], RUST, 9, 1.6))
            # shade the lower part of each plate with black hatching
            for _ in range(5):
                y = r.uniform(.25, .9) * abd_half((xa + xb) / 2)
                x = r.uniform(xa + 4, xb - 6)
                plates.append(gouge(x, y, math.pi / 2 + r.uniform(-.2, .2), r.uniform(10, 24), r.uniform(1.4, 2.6), INK, r=r))
            # highlight on the upper part
            y = -r.uniform(.4, .8) * abd_half((xa + xb) / 2)
            plates.append(gouge((xa + xb) / 2 - 4, y, -math.pi / 2 + r.uniform(-.2, .2), r.uniform(14, 30), 2.4, PAPER, r=r))
    # thorax plates
    for cx, ry in ((420, 92), (470, 100)):
        e = ellipse_pts(cx, 0, 26, ry, 24)
        plates.append(poly(e, RUST, 8, 1.5))
        plates.append(gouge(cx - 6, -ry * .7, math.pi / 2, ry * .9, 2.2, PAPER, r=r))
    parts.append(''.join(plates))
    # legs waving up/out from the belly
    LEGS = [
        ((410, 40), (330, 200), (230, 250), (190, 330)),
        ((450, 50), (500, 230), (440, 330), (470, 420)),
        ((495, 40), (610, 170), (690, 140), (760, 200)),
    ]
    for side in (1, -1):
        for k, (a, b, c, d) in enumerate(LEGS):
            pts = [(a[0], a[1] * side), (b[0], b[1] * side), (c[0], c[1] * side), (d[0], d[1] * side)]
            g = leg(pts, [22, 14, 7, 2.2], r=r)
            if twitch:
                dur = [1.1, 1.6, .9, 1.4, 1.2, 1.8][k + (3 if side < 0 else 0)]
                amp = 7 + k * 3
                g = (f'<g>{g}<animateTransform attributeName="transform" type="rotate" '
                     f'values="0 {a[0]} {a[1]*side};{amp*side} {a[0]} {a[1]*side};{-amp*side} {a[0]} {a[1]*side};0 {a[0]} {a[1]*side}" '
                     f'keyTimes="0;.35;.7;1" dur="{dur}s" repeatCount="indefinite"/></g>')
            parts.append(g)
    # antennae
    for side in (1, -1):
        pts = [(595 + t * 300, side * (30 + t * 220 - math.sin(t * 4) * 30 * t)) for t in [i / 20 for i in range(21)]]
        parts.append(taper(pts, 6, 1))
    return ''.join(parts)

# ---------------------------------------------------------------- figures
def figure(path_pts, rim=None, r=None, fill=INK, step=14, amp=2.6):
    out = [poly(path_pts, fill, step, amp)]
    if rim:
        for seg in rim:
            out.append(taper(seg, 1, 4.5, PAPER))
    return ''.join(out)


def _n(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    return -dy / L, dx / L

def rimline(a, b, w, light, frac=.32, fill=PAPER, t0=.08, t1=.85):
    nx, ny = _n(a, b)
    side = 1 if nx * light[0] + ny * light[1] > 0 else -1
    o = w * frac * side
    p0 = (a[0] + (b[0] - a[0]) * t0 + nx * o, a[1] + (b[1] - a[1]) * t0 + ny * o)
    p1 = (a[0] + (b[0] - a[0]) * t1 + nx * o, a[1] + (b[1] - a[1]) * t1 + ny * o)
    return taper(curve(p0, p1, .02, 4), max(1.5, w * .14), .6, fill)

def person(J, s=1.0, face=1, coat=None, skirt=None, hat=None, beard=False, moust=False, bun=False,
           light=(-.7, -.7), fill=INK, rimc=PAPER, r=None, folds=True, rims=True):
    r = r or rng
    o, rim = [], []
    def limb(a, b, w0, w1):
        o.append(taper(curve(a, b, r.uniform(-.03, .03), 4), w0 * s, w1 * s, fill))
        o.append(f'<circle cx="{f(b[0])}" cy="{f(b[1])}" r="{f(w1*s*.5)}" fill="{fill}"/>')
        if rims:
            rim.append(rimline(a, b, (w0 + w1) / 2 * s, light, fill=rimc))
    # legs
    for h, k, ft in (('lp', 'lk', 'lf'), ('rp', 'rk', 'rf')):
        if h in J and k in J:
            limb(J[h], J[k], 54, 38)
            limb(J[k], J[ft], 38, 22)
            fx = J.get(ft + 'd', face)
            o.append(taper([J[ft], (J[ft][0] + fx * 46 * s, J[ft][1] + 4 * s)], 24 * s, 12 * s, fill))
    # torso
    ls, rs, lp, rp = J['ls'], J['rs'], J['lp'], J['rp']
    sg0 = 1 if rs[0] > ls[0] else -1
    wy = ls[1] + (lp[1] - ls[1]) * .58
    nb = ((ls[0] + rs[0]) / 2, min(ls[1], rs[1]) - 10 * s)
    ls2, rs2 = (ls[0], ls[1] + 14 * s), (rs[0], rs[1] + 14 * s)
    wl = (ls[0] + (lp[0] - ls[0]) * .62 + sg0 * 6 * s, wy)
    wr = (rs[0] + (rp[0] - rs[0]) * .62 - sg0 * 6 * s, wy)
    tor = [ls2, (nb[0] - sg0 * 18 * s, nb[1]), (nb[0] + sg0 * 18 * s, nb[1]), rs2, wr, (rp[0] + sg0 * 14 * s, rp[1] + 10 * s), (lp[0] - sg0 * 14 * s, lp[1] + 10 * s), wl]
    o.append(poly(tor, fill, 12, 1.8))
    if rims:
        rim.append(rimline(ls if light[0] < 0 else rs, lp if light[0] < 0 else rp, 30 * s, light, .1, rimc, .1, .9))
    if coat:
        hem, fl = coat
        sg = 1 if rp[0] > lp[0] else -1
        hemj = [(rp[0] + sg * fl - sg * (rp[0] - lp[0] + 2 * fl) * t / 6, hem + (14 * s if i % 2 else -6 * s)) for i, t in enumerate(range(7))]
        c = [(ls[0] - sg * 8 * s, ls[1] + 12 * s), ((ls[0] + rs[0]) / 2, min(ls[1], rs[1]) - 6 * s), (rs[0] + sg * 8 * s, rs[1] + 12 * s), (rs[0] + (rp[0] - rs[0]) * .6 - sg * 2 * s, ls[1] + (lp[1] - ls[1]) * .58), (rp[0] + sg * (16 * s + fl * .3), rp[1])] + hemj + [(lp[0] - sg * (16 * s + fl * .3), lp[1]), (ls[0] + (lp[0] - ls[0]) * .6 + sg * 2 * s, ls[1] + (lp[1] - ls[1]) * .58)]
        cp = rough(c, 14, 2.4)
        o.append(f'<path d="{D(cp)}" fill="{fill}"/>')
        if folds:
            o.append(rows((lp[0] - fl, lp[1], rp[0] + fl, hem), 1.5, 26 * s, 1.2, 3 * s, rimc, .6, r, D(cp)))
    if skirt:
        hem, fl = skirt
        wy = min(lp[1], rp[1]) - 40 * s
        c = [(lp[0] - 8 * s, wy), (rp[0] + 8 * s, wy), (rp[0] + fl * .45, (wy + hem) / 2), (rp[0] + fl, hem), (lp[0] - fl, hem), (lp[0] - fl * .45, (wy + hem) / 2)]
        cp = rough(c, 14, 2.4)
        o.append(f'<path d="{D(cp)}" fill="{fill}"/>')
        if folds:
            for i in range(5):
                t = (i + .5) / 5
                x0 = lp[0] + (rp[0] - lp[0]) * t
                x1 = (lp[0] - fl) + ((rp[0] + fl) - (lp[0] - fl)) * t
                o.append(taper(curve((x0, wy + 30 * s), (x1, hem - 10 * s), .03, 4), 1, 4 * s, rimc))
    # arms
    for sh, el, ha in (('ls', 'le', 'lh'), ('rs', 're', 'rh')):
        if el in J:
            limb(J[sh], J[el], 40, 31)
            limb(J[el], J[ha], 31, 20)
            o.append(poly(ellipse_pts(J[ha][0], J[ha][1], 17 * s, 15 * s, 10), fill, 8, 1))
    # neck + head
    nk, hd = J['neck'], J['head']
    o.append(taper([((ls[0] + rs[0]) / 2, (ls[1] + rs[1]) / 2), nk, hd], 34 * s, 22 * s, fill))
    ang = math.atan2(hd[1] - nk[1], hd[0] - nk[0]) + math.pi / 2
    o.append(poly(rot(ellipse_pts(hd[0], hd[1], 29 * s, 37 * s, 22), ang, hd[0], hd[1]), fill, 8, 1.2))
    # profile: nose and chin toward the face side
    o.append(poly(rot([(hd[0] + face * 24 * s, hd[1] - 6 * s), (hd[0] + face * 40 * s, hd[1] + 6 * s), (hd[0] + face * 24 * s, hd[1] + 12 * s)], ang, hd[0], hd[1]), fill, 6, .5))
    if moust:
        o.append(poly(rot([(hd[0] + face * 14 * s, hd[1] + 14 * s), (hd[0] + face * 46 * s, hd[1] + 18 * s), (hd[0] + face * 20 * s, hd[1] + 24 * s)], ang, hd[0], hd[1]), fill, 6, .8))
    if beard:
        o.append(poly(rot([(hd[0] - face * 14 * s, hd[1] + 14 * s), (hd[0] + face * 30 * s, hd[1] + 18 * s), (hd[0] + face * 18 * s, hd[1] + 78 * s), (hd[0] - face * 4 * s, hd[1] + 66 * s)], ang, hd[0], hd[1]), fill, 6, 2))
        if rims:
            o.append(gouges((hd[0] - 10 * s, hd[1] + 20 * s, hd[0] + 26 * s, hd[1] + 70 * s), 1.4, 6, 10 * s, 26 * s, 1, 2.2 * s, rimc, .2, r))
    if bun:
        o.append(poly(ellipse_pts(hd[0] - face * 26 * s, hd[1] - 14 * s, 18 * s, 16 * s, 12), fill, 6, 1))
    if hat == 'bowler':
        o.append(poly(rot(ellipse_pts(hd[0], hd[1] - 30 * s, 30 * s, 24 * s, 16, math.pi, 2 * math.pi), ang, hd[0], hd[1]), fill, 6, 1))
        o.append(taper(rot([(hd[0] - 44 * s, hd[1] - 26 * s), (hd[0] + 44 * s, hd[1] - 26 * s)], ang, hd[0], hd[1]), 9 * s, 7 * s, fill))
    if hat == 'cap':
        o.append(poly(rot([(hd[0] - 30 * s, hd[1] - 20 * s), (hd[0] - 26 * s, hd[1] - 52 * s), (hd[0] + 28 * s, hd[1] - 50 * s), (hd[0] + 30 * s, hd[1] - 20 * s), (hd[0] + face * 58 * s, hd[1] - 16 * s)], ang, hd[0], hd[1]), fill, 6, 1))
    if hat == 'feather':
        o.append(poly(rot([(hd[0] - 40 * s, hd[1] - 22 * s), (hd[0] - 20 * s, hd[1] - 54 * s), (hd[0] + 26 * s, hd[1] - 56 * s), (hd[0] + 44 * s, hd[1] - 22 * s)], ang, hd[0], hd[1]), fill, 6, 1))
    if rims:
        # a carved edge of light on the head
        rim.append(taper(rot([(hd[0] - 18 * s, hd[1] - 26 * s), (hd[0] - 26 * s, hd[1]), (hd[0] - 18 * s, hd[1] + 22 * s)], ang, hd[0], hd[1]) if light[0] < 0 else
                         rot([(hd[0] + 18 * s, hd[1] - 26 * s), (hd[0] + 26 * s, hd[1]), (hd[0] + 18 * s, hd[1] + 22 * s)], ang, hd[0], hd[1]), 1, 4 * s, rimc))
    return ''.join(o) + ''.join(rim)

def P(**kw):
    """Joint dict with tuples."""
    return {k: tuple(v) for k, v in kw.items()}

def shift(J, dx, dy, sc=1):
    return {k: (v[0] * sc + dx, v[1] * sc + dy) if isinstance(v, tuple) else v for k, v in J.items()}

# ---------------------------------------------------------------- panels
def svg(W, H, body, label, fx='xMidYMid slice', cls=''):
    return (f'<svg class="art {cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="{fx}" role="img" aria-label="{H_(label)}">'
            f'{body}</svg>')

def H_(s):
    return H.escape(s, quote=True)

def layer(depth, inner):
    return f'<g class="ly" data-d="{depth}">{inner}</g>'

def paper_rect(W, H, fill=INK):
    return f'<rect width="{W}" height="{H}" fill="{fill}"/>'

def window(x, y, w, h, r, rain=True, light=PAPER, skew=0):
    """A tilted window: paper panes, black mullions, rain strokes."""
    pts = [(x, y), (x + w, y + skew), (x + w, y + h + skew * .6), (x, y + h)]
    out = [poly(pts, light, 14, 2)]
    if rain:
        rid = uid('rain')
        drops = []
        rr = random.Random(5)
        for _ in range(int(w * h / 900)):
            px, py = rr.uniform(x - 40, x + w + 40), rr.uniform(y - h, y + h)
            drops.append(gouge(px, py, 1.95, rr.uniform(18, 46), rr.uniform(1.2, 2.4), INK, bend=0, r=rr))
        cid = uid('k')
        out.append(f'<clipPath id="{cid}"><path d="{D(pts)}"/></clipPath><g clip-path="url(#{cid})"><g class="rain">{"".join(drops)}'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;{-h*.36:.0f} {h:.0f}" dur="1.6s" repeatCount="indefinite"/></g></g>')
    # mullions
    mx = x + w / 2
    out.append(poly([(mx - 7, y - 4), (mx + 7, y - 4 + skew / 2), (mx + 7, y + h + 4 + skew * .3), (mx - 7, y + h + 4)], INK, 20, 1.5))
    my = y + h * .42
    out.append(poly([(x - 4, my - 7), (x + w + 4, my - 7 + skew * .5), (x + w + 4, my + 7 + skew * .5), (x - 4, my + 7)], INK, 20, 1.5))
    # frame
    fr = rough(pts, 18, 2)
    out.append(f'<path d="{D(fr)}" fill="none" stroke="{INK}" stroke-width="16"/>')
    return ''.join(out)

PANELS = []

def panel(pid, W, H, hcls, label, art, caps, fx='xMidYMid slice', bg=INK, extra_cls=''):
    PANELS.append(dict(id=pid, W=W, H=H, h=hcls, label=label, art=art, caps=caps, fx=fx, bg=bg, cls=extra_cls))

# ---- 1 title
def p_title():
    W, Hh = 1600, 1000
    r = random.Random(11)
    o = [paper_rect(W, Hh, INK)]
    # pale sky wedge carved with rows
    sky = [(0, 0), (1600, 0), (1600, 560), (0, 700)]
    o.append(layer(.25, poly(sky, PAPER, 30, 3) + rows((0, 0, 1600, 700), -0.12, 15, 1.6, 4.2, INK, .45, r, D(sky))))
    # city: spires and roofs
    city = [(0, 1000), (0, 640), (60, 640), (60, 560), (90, 520), (120, 560), (120, 610), (210, 600), (250, 540), (290, 600), (330, 590),
            (360, 470), (372, 380), (384, 470), (400, 600), (470, 610), (520, 520), (560, 610), (640, 600), (650, 420), (668, 300),
            (686, 420), (700, 560), (720, 430), (738, 330), (756, 430), (770, 590), (860, 600), (900, 540), (960, 600), (1040, 580),
            (1080, 500), (1120, 580), (1200, 590), (1240, 470), (1262, 410), (1284, 470), (1300, 590), (1380, 600), (1420, 540),
            (1470, 600), (1600, 560), (1600, 1000)]
    citysvg = poly(city, INK, 18, 3)
    # lit windows, carved
    wins = []
    for _ in range(70):
        x = r.uniform(20, 1580); y = r.uniform(640, 980)
        wins.append(poly([(x, y), (x + 12, y), (x + 12, y + 20), (x, y + 20)], PAPER, 8, 1.4))
    o.append(layer(.08, citysvg + ''.join(wins)))
    o.append(rows((0, 860, 1600, 1000), 0.02, 12, 1.2, 3, PAPER, .5, r))
    body = ''.join(o)
    # carved title (font + roughened via filter)
    body += ('<g filter="url(#carve)">'
             '<text x="800" y="230" text-anchor="middle" class="t-title">THE METAMORPHOSIS</text>'
             '<text x="800" y="318" text-anchor="middle" class="t-sub">FRANZ KAFKA · 1915</text></g>')
    panel('title', W, Hh, 'h1', 'A carved print of Prague roofs and spires under a rainy sky, with the title The Metamorphosis.', body, [], bg=INK)

# ---- 2 morning: the bed
def p_morning():
    W, Hh = 1600, 1000
    r = random.Random(21)
    o = [paper_rect(W, Hh)]
    # back wall planes carved
    o.append(layer(.05, rows((0, 0, 1600, 640), 0.0, 22, 1.2, 3.2, PAPER, .55, r, D([(0, 0), (1600, 0), (1600, 560), (0, 660)]))))
    o.append(layer(.12, window(1080, 120, 330, 380, r, skew=-30)))
    # light from the window on the floor
    o.append(poly([(1080, 520), (1410, 480), (1600, 760), (1600, 1000), (1220, 1000)], PAPER, 20, 3))
    o.append(rows((1000, 480, 1600, 1000), -0.9, 16, 1.5, 4, INK, .4, r, D([(1080, 520), (1410, 480), (1600, 760), (1600, 1000), (1220, 1000)])))
    # bed: dark frame, pale quilt, the shape beneath
    bed_frame = [(140, 560), (980, 470), (1060, 700), (1040, 900), (180, 980), (110, 760)]
    o.append(poly(bed_frame, INK, 18, 3))
    head = [(110, 300), (220, 270), (250, 600), (130, 640)]
    o.append(poly(head, INK, 16, 3) + gouges((120, 290, 240, 620), 1.45, 22, 40, 120, 2, 5, PAPER, .06, r, D(head)))
    quilt = [(200, 560), (930, 480), (1020, 690), (980, 820), (240, 900), (180, 740)]
    qd = D(quilt)
    o.append(poly(quilt, PAPER, 16, 3))
    # the shape under the quilt: a dark hump with ridges showing
    hump = ellipse_pts(600, 640, 300, 120, 40)
    hump = rot(hump, -.12, 600, 640)
    o.append(f'<clipPath id="qclip"><path d="{qd}"/></clipPath><g clip-path="url(#qclip)">' + poly(hump, INK, 14, 3) +
             ''.join(taper(curve((x, 560 - (x - 300) * .1), (x - 30, 740 - (x - 300) * .1), .12, 8), 5, 1, PAPER) for x in range(360, 880, 46)) +
             rows((200, 480, 1020, 900), -0.12, 20, 1.5, 4, INK, .5, r, D([(200, 560), (930, 480), (1020, 690), (900, 700), (300, 760), (180, 740)])) + '</g>')
    # a few thin legs escaping the quilt edge
    for i, x in enumerate((430, 520, 610, 700)):
        y = 860 - (x - 430) * .08
        g = leg([(x, y - 20), (x - 20, y + 40), (x + 15, y + 90), (x - 5, y + 120)], [9, 6, 3, 1], r=r)
        o.append(f'<g>{g}<animateTransform attributeName="transform" type="rotate" values="0 {x} {y-20};{6 if i%2 else -6} {x} {y-20};0 {x} {y-20}" dur="{1.4+i*.35}s" repeatCount="indefinite"/></g>')
    o.append(rows((0, 900, 1600, 1000), 0.02, 14, 1.4, 3.5, PAPER, .5, r))
    panel('morning', W, Hh, 'h1', 'A dark bedroom at dawn. Rain runs down the window. On the bed, under a pale quilt, a long dark shape with ridges, and thin legs at the edge.',
          ''.join(o), [
              ('cap', 'One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin.', 'l:5%;t:7%;w:30em', 'l:5%;t:5%'),
          ])

# ---- 3 the belly, close
def p_belly():
    W, Hh = 1600, 1300
    r = random.Random(31)
    o = [paper_rect(W, Hh)]
    o.append(rows((0, 0, 1600, 1300), 0.5, 26, 1.4, 4, PAPER, .5, r))
    bug = insect_belly(r)
    o.append(layer(.1, f'<g transform="translate(330 690) rotate(-28) scale(1.55)">{bug}</g>'))
    panel('belly', W, Hh, 'h2', 'Close up from above: Gregor on his back. A domed brown belly divided by arches into stiff sections, and many thin, spiny legs waving in the air.',
          ''.join(o), [
              ('cap', 'He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections.', 'r:5%;t:6%;w:24em', 'l:5%;t:4%'),
              ('cap', 'His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.', 'l:5%;b:7%;w:22em', 'r:5%;b:5%'),
          ])

# ---- 4 the full insect
def p_insect():
    W, Hh = 1600, 1150
    r = random.Random(41)
    o = [paper_rect(W, Hh, PAPER)]
    # sheet: pale with black folds, dark corners
    o.append(rows((0, 0, 1600, 1150), -0.4, 30, 2, 6, INK, .35, r))
    o.append(poly([(0, 0), (380, 0), (0, 300)], INK, 20, 3))
    o.append(poly([(1600, 1150), (1600, 760), (1180, 1150)], INK, 20, 3))
    # cast shadow
    sh = rot(ellipse_pts(880, 760, 420, 150, 40), -.42, 880, 760)
    o.append(poly(sh, INK, 16, 3) + rows((300, 400, 1300, 950), -0.42, 11, 1.2, 2.6, PAPER, .6, r, D(sh)))
    bug = insect_top(r)
    o.append(layer(.06, f'<g transform="translate(330 860) rotate(-24) scale(1.18)">{bug}</g>'))
    panel('insect', W, Hh, 'h2', 'Gregor seen whole on the bed: a huge beetle-like body, a dark carved shell in segments, a broad shield behind the head, long antennae and six spiny jointed legs.',
          ''.join(o), [
              ('think', '“What’s happened to me?”', 'r:8%;t:8%', 'r:5%;t:5%'),
              ('cap', 'It wasn’t a dream.', 'l:6%;b:8%', 'l:5%;b:5%'),
          ], bg=PAPER)

# ---- 5 alarm clock
def p_clock():
    W, Hh = 1600, 950
    r = random.Random(51)
    o = [paper_rect(W, Hh)]
    o.append(gouges((0, 0, 1600, 950), 0, 0, 1, 1, 1, 1))
    # ticking rays
    rays = []
    for i in range(40):
        a = i / 40 * 2 * math.pi
        rays.append(gouge(800 + math.cos(a) * 330, 470 + math.sin(a) * 330, a, r.uniform(120, 520), r.uniform(3, 9), PAPER, r=r))
    o.append(layer(.2, f'<g class="spin">{"".join(rays)}</g>'))
    face = ellipse_pts(800, 470, 270, 270, 64)
    o.append(poly(ellipse_pts(800, 470, 300, 300, 64), INK, 12, 2))
    o.append(poly(face, PAPER, 12, 2))
    # bells and legs
    for s in (-1, 1):
        o.append(poly(ellipse_pts(800 + s * 210, 190, 90, 70, 30, math.pi, 2 * math.pi), INK, 10, 2))
        o.append(taper([(800 + s * 200, 700), (800 + s * 260, 790)], 26, 12))
    # hour marks carved as wedges
    for i in range(12):
        a = i / 12 * 2 * math.pi - math.pi / 2
        o.append(taper([(800 + math.cos(a) * 250, 470 + math.sin(a) * 250), (800 + math.cos(a) * 205, 470 + math.sin(a) * 205)], 14 if i % 3 == 0 else 7, 2))
    o.append(rows((520, 190, 1080, 750), 0.7, 18, .8, 1.8, INK, .7, r, D(face)))
    # hands: half past six moving toward quarter to seven
    o.append(f'<g class="hand-m">{taper([(800, 470), (800 + math.cos(math.radians(70))*230, 470 + math.sin(math.radians(70))*230)], 18, 3)}</g>')
    o.append(taper([(800, 470), (800 + math.cos(math.radians(105)) * 150, 470 + math.sin(math.radians(105)) * 150)], 24, 6))
    o.append('<circle cx="800" cy="470" r="16" fill="%s"/>' % INK)
    panel('clock', W, Hh, 'h1', 'The alarm clock, huge and close, its hands past half past six, rays carved around it like ticking.',
          ''.join(o), [
              ('think', '“God in Heaven!”', 'l:7%;t:10%', 'l:5%;t:5%'),
              ('cap', 'It was half past six and the hands were quietly moving forwards,', 'r:6%;b:8%;w:20em', 'r:5%;b:5%'),
          ])

# ---- 6 the door, voices
def p_door():
    W, Hh = 1600, 1250
    r = random.Random(61)
    o = [paper_rect(W, Hh)]
    door = [(520, 110), (1110, 70), (1140, 1250), (500, 1250)]
    o.append(poly(door, PAPER, 18, 3))
    o.append(rows((480, 60, 1160, 1250), 1.53, 24, 1.5, 4.5, INK, .35, r, D(door)))
    for (a, b, c, d) in (((590, 190), (1040, 165), (1050, 560), (585, 580)), ((582, 680), (1052, 660), (1064, 1150), (576, 1165))):
        p = [a, b, c, d]
        o.append(f'<path d="{D(rough(p,18,2))}" fill="none" stroke="{INK}" stroke-width="14"/>')
    # knock marks on the door
    for (x, y) in ((760, 430), (900, 900)):
        o.append(f'<g class="knock">{"".join(gouge(x, y, a, r.uniform(40, 90), 7, INK, r=r) for a in [i*0.785+.2 for i in range(8)])}</g>')
    # keyhole + lock
    o.append(poly([(1035, 620), (1075, 618), (1078, 720), (1036, 722)], INK, 10, 1.5))
    # floor and dark
    o.append(rows((0, 1100, 1600, 1250), 0.03, 14, 1.4, 4, PAPER, .5, r))
    panel('voices', W, Hh, 'h2', 'The bedroom door from inside, tall and pale in the dark, shaking with knocks. Voices come through it from three sides.',
          ''.join(o), [
              ('say', '“it’s quarter to seven. Didn’t you want to go somewhere?”', 'l:4%;t:9%;w:16em', 'l:4%;t:4%', 'tail-r'),
              ('say', '“Gregor, Gregor”', 'r:5%;t:30%', 'r:4%;t:30%', 'tail-l'),
              ('say', '“what’s wrong?”', 'r:9%;t:43%', 'r:8%;t:41%', 'tail-l'),
              ('say', '“Gregor? Aren’t you well? Do you need anything?”', 'l:5%;b:16%;w:15em', 'l:4%;b:10%', 'tail-r'),
          ])

# ---- 7 the key
def p_key():
    W, Hh = 1600, 1000
    r = random.Random(71)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 1000), 1.57, 30, 2, 6, INK, .3, r))
    # big lock plate
    plate = [(760, 120), (1180, 100), (1200, 900), (780, 930)]
    o.append(poly(plate, INK, 16, 3))
    o.append(rows((760, 100, 1200, 930), 0.05, 16, 1, 3, PAPER, .55, r, D(plate)))
    o.append(poly([(950, 380), (1010, 378), (1030, 640), (930, 645)], PAPER, 10, 1.5))
    # the key bow sticking out, bitten by the mandibles
    key = [(860, 420), (980, 410), (990, 520), (870, 530)]
    o.append(poly(key, INK, 10, 2) + poly(ellipse_pts(925, 470, 32, 30, 20), PAPER, 6, 1))
    # head from the left: profile with mandibles around the key
    head = [(-20, 160), (300, 120), (560, 230), (720, 360), (760, 430), (700, 470), (760, 520), (720, 590), (560, 700), (300, 820), (-20, 800)]
    o.append(layer(.08, poly(head, INK, 16, 3) + rows((0, 120, 760, 820), -0.3, 18, 1.4, 4, PAPER, .45, r, D(head))
             + poly(rot(ellipse_pts(470, 330, 60, 38, 24), .3, 470, 330), PAPER, 6, 1.2) + f'<circle cx="485" cy="335" r="16" fill="{INK}"/>'
             + taper([(700, 430), (820, 400), (880, 440)], 30, 8) + taper([(700, 540), (830, 560), (880, 515)], 30, 8)))
    # brown fluid over the key, dripping
    drip = taper([(880, 520), (884, 600), (880, 700), (886, 820), (884, 1000)], 14, 6, RUST)
    o.append(f'<g class="drip">{drip}<circle cx="884" cy="1000" r="10" fill="{RUST}"/></g>')
    panel('key', W, Hh, 'h1', 'Extreme close up: Gregor’s dark head and jaws clamp the bow of the key in the lock. A brown fluid runs over the key and drips down.',
          ''.join(o), [
              ('cap', 'he bit on the key with all his strength,', 'l:5%;t:7%', 'l:5%;t:4%'),
              ('cap', 'a brown fluid came from his mouth, flowed over the key and dripped onto the floor.', 'r:5%;b:9%;w:18em', 'l:5%;b:5%'),
              ('say', '“he’s turning the key.”', 'r:6%;t:9%', 'r:4%;t:22%', 'tail-r'),
          ], bg=PAPER)

# ---- 8 the door opens
def p_reveal():
    W, Hh = 1600, 1050
    r = random.Random(81)
    o = [paper_rect(W, Hh, PAPER)]
    # living room light, jagged floor
    o.append(rows((0, 0, 1600, 1050), -0.05, 26, 1.4, 4, INK, .5, r))
    floor = [(0, 760), (1600, 700), (1600, 1050), (0, 1050)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 690, 1600, 1050), -0.04, 18, 1.5, 4, PAPER, .45, r, D(floor)))
    # the doorway at right, black, Gregor half out of it
    dw = [(1180, 80), (1600, 40), (1600, 1050), (1180, 1050)]
    o.append(poly(dw, INK, 18, 3))
    bug = insect_top(r)
    o.append(layer(.05, f'<g transform="translate(1680 520) rotate(200) scale(.95)">{bug}</g>'))
    o.append(poly([(1150, 60), (1200, 60), (1215, 1050), (1165, 1050)], PAPER, 12, 2))
    # the chief clerk recoiling, hand to mouth
    clerk = [(380, 1010), (420, 760), (380, 560), (330, 470), (360, 380), (330, 330), (350, 260), (410, 240), (450, 280), (440, 340),
             (470, 360), (520, 330), (540, 360), (480, 430), (470, 560), (520, 760), (560, 1010), (500, 1010), (470, 800), (440, 1010)]
    o.append(layer(.18, figure(clerk, [[(445, 290), (468, 380), (470, 560), (510, 760)]], r)))
    # mother sinking into her skirts
    mom = [(560, 1010), (600, 880), (660, 820), (700, 700), (690, 640), (720, 600), (760, 640), (760, 720), (800, 830), (900, 900), (960, 1010)]
    o.append(layer(.12, figure(mom, [[(740, 650), (770, 760), (880, 880)]], r)))
    # father, fists
    fa = [(880, 1010), (900, 700), (860, 560), (870, 440), (920, 400), (910, 330), (950, 290), (1000, 310), (1000, 380), (1060, 430),
          (1080, 560), (1060, 700), (1080, 1010), (1020, 1010), (990, 760), (950, 1010)]
    o.append(layer(.1, figure(fa, [[(1000, 330), (1050, 440), (1070, 560)]], r)))
    panel('reveal', W, Hh, 'h1', 'The door is open. In the black doorway, half of Gregor’s shell and head lean out. The chief clerk backs away with his hand at his mouth, the mother sinks into her skirts, the father clenches his fists.',
          ''.join(o), [
              ('burst', '“Oh!”', 'l:16%;t:8%', 'l:6%;t:6%'),
              ('cap', 'his hand pressed against his open mouth and slowly retreating as if driven by a steady and invisible force.', 'l:4%;b:5%;w:20em', 'l:4%;b:4%'),
          ], bg=PAPER)

# ---- 9 father with stick
def p_father():
    W, Hh = 1400, 1500
    r = random.Random(91)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1400, 1500), 0.9, 22, 1.5, 5, INK, .35, r))
    # curtains flying from an open window
    for i in range(5):
        x = 60 + i * 50
        o.append(layer(.3, taper(curve((x, 0), (x + 380 + i * 30, 520 + i * 40), .25 - i * .03, 14), 60 - i * 8, 6)))
    # father: low angle, huge, stamping
    fa = [(380, 1500), (470, 1060), (420, 760), (470, 520), (560, 430), (540, 330), (590, 250), (680, 240), (720, 300), (700, 380),
          (780, 410), (900, 300), (1040, 120), (1080, 150), (930, 380), (860, 560), (900, 760), (840, 1050), (1000, 1500), (820, 1500),
          (700, 1150), (600, 1500)]
    o.append(layer(.12, figure(fa, [[(700, 300), (790, 430), (880, 560)], [(560, 440), (500, 600), (460, 760)]], r)))
    # stick
    o.append(layer(.12, taper([(1050, 140), (1310, -60)], 20, 12)))
    # newspaper in the other hand
    np_ = [(250, 560), (470, 500), (500, 700), (290, 780)]
    o.append(layer(.15, poly(np_, PAPER, 12, 2) + rows((240, 490, 510, 790), -0.27, 12, 1, 2.4, INK, .3, r, D(np_)) + taper([(470, 560), (520, 520)], 30, 22)))
    # Gregor small, backing away at the bottom
    bug = insect_top(r)
    o.append(f'<g transform="translate(1150 1370) rotate(160) scale(.42)">{bug}</g>')
    panel('father', W, Hh, 'h3', 'From the floor: the father looms, a huge black figure with the clerk’s stick raised and a newspaper in his fist, curtains flying. Gregor backs away below.',
          ''.join(o), [
              ('cap', 'making hissing noises at him like a wild man.', 'r:6%;b:16%;w:14em', 'l:5%;b:5%'),
          ], bg=PAPER)

# ---- 10 under the couch, the milk
def p_milk():
    W, Hh = 1600, 1000
    r = random.Random(101)
    o = [paper_rect(W, Hh)]
    lightw = [(140, 120), (420, 100), (900, 1000), (0, 1000), (0, 700)]
    o.append(poly(lightw, PAPER, 18, 3) + rows((0, 100, 900, 1000), 1.1, 18, 1.2, 3.5, INK, .45, r, D(lightw)))
    o.append(poly([(110, 90), (440, 70), (440, 120), (110, 140)], INK, 12, 2))
    # sister in the doorway, setting down the dish
    sis = [(210, 820), (230, 640), (250, 480), (236, 400), (250, 330), (300, 310), (330, 350), (320, 420), (350, 470), (400, 560),
           (430, 640), (380, 650), (350, 600), (360, 820)]
    o.append(layer(.1, figure(sis, [[(320, 360), (345, 470), (400, 570)]], r)))
    dish = ellipse_pts(470, 790, 70, 18, 24)
    o.append(poly(dish, INK, 8, 1) + poly(ellipse_pts(470, 785, 56, 10, 20), PAPER, 6, .8))
    # the couch, black, and Gregor beneath: antennae and a glint
    couch = [(900, 520), (1600, 470), (1600, 820), (900, 830)]
    o.append(poly(couch, INK, 16, 3) + rows((900, 460, 1600, 840), -0.05, 30, 1, 3, PAPER, .6, r, D(couch)))
    o.append(rows((900, 830, 1600, 1000), 0.0, 9, .6, 1.4, PAPER, .7, r))
    for s in (1, -1):
        o.append(f'<g>{taper([(960, 900 + s*10), (850, 880 + s*30), (720, 860 + s*55)], 5, 1)}<animateTransform attributeName="transform" type="rotate" values="0 960 900;{4*s} 960 900;0 960 900" dur="{2.2 if s>0 else 3}s" repeatCount="indefinite"/></g>')
    o.append(poly(ellipse_pts(985, 892, 9, 5, 10), PAPER, 4, .5))
    panel('milk', W, Hh, 'h1', 'Night in Gregor’s room. Through the door, light falls on the floor where his sister bends to set down a dish. Under the black couch, two antennae and the glint of an eye.',
          ''.join(o), [
              ('cap', 'By the door there was a dish filled with sweetened milk with little pieces of white bread floating in it.', 'r:5%;t:8%;w:20em', 'r:5%;t:5%'),
          ])

# ---- 11 the picture
def p_picture():
    W, Hh = 1600, 1200
    r = random.Random(111)
    o = [paper_rect(W, Hh, PAPER)]
    # bare wallpaper: stamped flowers
    fl = []
    for i in range(0, 1600, 110):
        for j in range(0, 900, 110):
            x, y = i + (55 if (j // 110) % 2 else 0), j + 40
            fl.append(''.join(gouge(x, y, a, 14, 4, INK, bend=0, r=r) for a in (0, 1.57, 3.14, 4.71)))
    o.append(layer(.05, ''.join(fl)))
    floor = [(0, 900), (1600, 860), (1600, 1200), (0, 1200)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 850, 1600, 1200), 0.4, 20, 1.5, 4, PAPER, .45, r, D(floor)))
    # the picture of the lady in furs
    fr = [(820, 150), (1160, 140), (1170, 600), (830, 610)]
    o.append(poly(fr, INK, 14, 2))
    inner = [(860, 190), (1125, 182), (1132, 565), (868, 572)]
    o.append(poly(inner, PAPER, 12, 2))
    lady = [(900, 560), (920, 450), (960, 400), (960, 330), (930, 300), (950, 240), (1010, 220), (1070, 250), (1080, 300), (1050, 330),
            (1050, 400), (1090, 450), (1100, 560)]
    o.append(figure(lady, None, r) + poly(ellipse_pts(1000, 470, 70, 38, 20), PAPER, 8, 2)
             + rows((880, 380, 1120, 560), .6, 10, .8, 2, INK, .5, r, D(ellipse_pts(1000, 470, 70, 38, 20))))
    # Gregor pressed against the glass
    bug = insect_top(r)
    o.append(f'<g transform="translate(1000 640) rotate(-90) scale(.62)">{bug}</g>')
    # women carrying the chest out at left
    chest = [(140, 700), (420, 690), (430, 900), (150, 910)]
    o.append(layer(.15, poly(chest, INK, 14, 2) + ''.join(taper([(150, 750 + k * 50), (420, 745 + k * 50)], 5, 5, PAPER) for k in range(3))
             + figure([(60, 1100), (80, 860), (70, 700), (100, 640), (90, 590), (130, 570), (160, 600), (150, 660), (170, 720), (190, 860), (210, 1100)], None, r)
             + figure([(400, 1100), (430, 860), (420, 720), (450, 650), (440, 600), (480, 580), (510, 610), (500, 670), (530, 720), (530, 860), (560, 1100)], None, r)))
    panel('picture', W, Hh, 'h2', 'The emptied room, bare flowered wallpaper. Two women drag the chest of drawers away. On the wall, Gregor’s dark body covers the framed picture of the lady in furs.',
          ''.join(o), [
              ('cap', 'He hurried up onto the picture and pressed himself against its glass,', 'r:5%;b:30%;w:14em', 'r:4%;t:4%'),
              ('say', '“Oh God, oh God!”', 'l:5%;t:8%', 'l:4%;t:16%', 'tail-b'),
          ], bg=PAPER)

# ---- 12 apples (tall)
def p_apples():
    W, Hh = 1200, 1800
    r = random.Random(121)
    o = [paper_rect(W, Hh)]
    o.append(rows((0, 0, 1200, 1800), 0.6, 30, 1.2, 4, PAPER, .5, r))
    # father's arm from the top, throwing
    arm = [(1200, 0), (1200, 220), (900, 330), (700, 360), (660, 300), (860, 200)]
    o.append(layer(.2, poly(arm, PAPER, 14, 3) + rows((600, 0, 1200, 380), -0.4, 12, 1, 2.6, INK, .4, r, D(arm))))
    # apples falling (rust)
    apples = []
    for i, (x, y, rr_) in enumerate(((520, 520, 34), (760, 700, 30), (420, 900, 28), (640, 1040, 32), (860, 1180, 26))):
        a = poly(ellipse_pts(x, y, rr_, rr_ * .92, 18), RUST, 8, 1.5) + gouge(x - rr_ * .4, y - rr_ * .5, -.6, rr_ * .6, 4, PAPER, r=r) + taper([(x, y - rr_), (x + 6, y - rr_ - 22)], 6, 3)
        apples.append(f'<g class="apple" data-i="{i}">{a}</g>')
    o.append(''.join(apples))
    # Gregor at the bottom, an apple lodged in his back
    bug = insect_top(r)
    o.append(f'<g transform="translate(260 1560) rotate(-10) scale(.9)">{bug}</g>')
    o.append(poly(ellipse_pts(470, 1520, 30, 26, 18), RUST, 6, 1.2) + gouge(460, 1508, -.5, 16, 3, PAPER, r=r))
    panel('apples', W, Hh, 'h3', 'A tall panel. From above, the father’s arm throws small red apples that fall through the dark. Below, Gregor, with one apple sunk into his back.',
          ''.join(o), [
              ('cap', 'It was an apple; then another one immediately flew at him;', 'l:5%;t:6%;w:14em', 'l:5%;t:4%'),
              ('cap', 'hit squarely and lodged in his back;', 'r:5%;b:6%', 'r:5%;b:4%'),
          ])

# ---- 13 violin
def p_violin():
    W, Hh = 1600, 1000
    r = random.Random(131)
    o = [paper_rect(W, Hh)]
    # lamp light cone
    cone = [(760, 0), (840, 0), (1250, 1000), (350, 1000)]
    o.append(poly(cone, PAPER, 18, 3) + rows((350, 0, 1250, 1000), 1.57, 16, 1, 3, INK, .55, r, D(cone)))
    # sister with the violin
    sis = [(700, 1000), (720, 760), (690, 560), (720, 470), (700, 420), (710, 350), (760, 320), (800, 350), (800, 420), (860, 450),
           (930, 430), (960, 470), (880, 520), (840, 600), (860, 760), (900, 1000)]
    o.append(layer(.1, figure(sis, [[(800, 360), (830, 450), (840, 600), (860, 760)]], r)))
    o.append(layer(.1, taper([(800, 470), (1010, 360)], 6, 3) + poly(rot(ellipse_pts(900, 440, 60, 28, 18), -.45, 900, 440), INK, 8, 1.5)))
    # music stand
    o.append(taper([(600, 1000), (600, 560)], 8, 6) + poly([(530, 520), (680, 500), (690, 580), (540, 600)], INK, 10, 1.5))
    # three lodgers at the window, smoke
    for k, x in enumerate((1180, 1320, 1450)):
        lodger = [(x - 60, 1000), (x - 50, 700), (x - 70, 520), (x - 40, 420), (x - 40, 360), (x - 20, 320), (x + 20, 320), (x + 40, 360),
                  (x + 40, 420), (x + 30, 470), (x + 15, 520), (x + 60, 540), (x + 70, 700), (x + 60, 1000)]
        o.append(layer(.16, figure(lodger, [[(x - 40, 380), (x - 50, 480)]], r)))
        smoke = [(x + 20 + math.sin(t / 3) * 20 * (1 + t / 8), 360 - t * 30) for t in range(10)]
        o.append(f'<g class="smoke">{taper(smoke, 6, 1, PAPER)}</g>')
    panel('violin', W, Hh, 'h1', 'Lamplight. Grete plays the violin at a music stand, her head leaning to one side. By the window, three bearded gentlemen stand smoking.',
          ''.join(o), [
              ('cap', 'Yet Gregor’s sister was playing so beautifully.', 'l:5%;t:8%;w:14em', 'l:5%;t:4%'),
          ])

# ---- 14 drawn to the music
def p_drawn():
    W, Hh = 1600, 900
    r = random.Random(141)
    o = [paper_rect(W, Hh)]
    beam = [(1600, 200), (1600, 520), (300, 900), (0, 900), (0, 820)]
    o.append(poly(beam, PAPER, 18, 3) + rows((0, 200, 1600, 900), -0.3, 14, 1, 3, INK, .5, r, D(beam)))
    o.append(layer(.25, figure([(1430, 520), (1440, 380), (1460, 330), (1490, 310), (1520, 330), (1530, 380), (1550, 520)], None, r)))
    bug = insect_top(r)
    o.append(layer(.06, f'<g transform="translate(160 650) rotate(-14) scale(1.05)">{bug}</g>'))
    # dust and threads trailing
    o.append(''.join(gouge(r.uniform(40, 700), r.uniform(560, 860), r.uniform(0, 6.28), r.uniform(10, 40), 1.6, PAPER, r=r) for _ in range(40)))
    panel('drawn', W, Hh, 'h1', 'Low on the floor, Gregor crawls out of the dark into a long beam of light toward the small far figure of his sister.',
          ''.join(o), [
              ('cap', 'Was he an animal if music could captivate him so?', 'r:5%;t:9%;w:15em', 'r:5%;t:5%'),
          ])

# ---- 15 lodgers
def p_lodgers():
    W, Hh = 1600, 950
    r = random.Random(151)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 950), 0.25, 20, 1.6, 5, INK, .35, r))
    head = [(500, 950), (520, 700), (470, 560), (480, 380), (560, 250), (700, 220), (820, 280), (850, 420), (820, 520), (860, 620),
            (840, 700), (900, 950)]
    o.append(layer(.1, figure(head, [[(820, 300), (845, 430)]], r)))
    beard = [(560, 560), (820, 520), (790, 700), (700, 760), (600, 720)]
    o.append(layer(.1, poly(beard, INK, 10, 4) + gouges((560, 520, 820, 760), 1.4, 40, 20, 60, 1.5, 3, PAPER, .2, r, D(beard))
                       + poly(ellipse_pts(760, 410, 26, 12, 14), PAPER, 6, 1) + f'<circle cx="768" cy="411" r="7" fill="{INK}"/>'))
    arm = [(840, 600), (1100, 520), (1380, 480), (1400, 520), (1120, 600), (900, 700)]
    o.append(layer(.2, poly(arm, INK, 14, 2.5) + taper([(1370, 490), (1560, 470)], 22, 6)))
    panel('lodgers', W, Hh, 'h1', 'The middle gentleman, bearded, in profile, thrusts a long pointing finger across the room.',
          ''.join(o), [
              ('say', '“Mr. Samsa!”', 'r:8%;t:10%', 'r:5%;t:6%', 'tail-b'),
          ], bg=PAPER)

# ---- 16 sister
def p_sister():
    W, Hh = 1400, 1200
    r = random.Random(161)
    o = [paper_rect(W, Hh)]
    lamp = [(640, 0), (760, 0), (1200, 760), (200, 760)]
    o.append(poly(lamp, PAPER, 16, 3) + rows((200, 0, 1200, 760), 1.57, 14, 1, 3, INK, .55, r, D(lamp)))
    table = [(100, 760), (1300, 740), (1320, 800), (90, 820)]
    o.append(poly(table, INK, 14, 2) + rows((0, 800, 1400, 1200), 0.0, 16, 1.2, 3.4, PAPER, .5, r))
    sis = [(560, 760), (580, 560), (550, 440), (560, 360), (590, 300), (660, 290), (690, 340), (680, 420), (740, 470), (840, 640),
           (880, 730), (820, 750), (760, 620), (740, 760)]
    o.append(layer(.1, figure(sis, [[(680, 340), (690, 440), (780, 560)]], r)))
    for x in (260, 1110):
        o.append(layer(.18, figure([(x - 90, 760), (x - 70, 560), (x - 40, 470), (x - 30, 400), (x, 380), (x + 30, 400), (x + 40, 470), (x + 70, 560), (x + 90, 760)], None, r)))
    panel('sister', W, Hh, 'h2', 'At the table under the lamp, Grete stands and strikes the table with her hand, between her seated father and mother.',
          ''.join(o), [
              ('say', '“We have to try and get rid of it”', 'l:8%;t:8%', 'l:5%;t:5%', 'tail-r'),
          ])

# ---- 17 dawn, death
def p_dawn():
    W, Hh = 1600, 1300
    r = random.Random(171)
    o = [paper_rect(W, Hh)]
    win = [(980, 140), (1360, 110), (1380, 600), (1000, 620)]
    o.append(poly(win, PAPER, 16, 2))
    # clock tower against the grey dawn
    tower = [(1120, 620), (1130, 330), (1160, 300), (1175, 200), (1190, 300), (1220, 330), (1230, 620)]
    o.append(poly(tower, INK, 10, 2) + rows((980, 100, 1380, 620), 0.0, 12, .8, 2, INK, .55, r, D(win)) + poly(ellipse_pts(1175, 390, 22, 22, 14), PAPER, 6, 1))
    o.append(poly([(1170, 120), (1182, 120), (1190, 610), (1172, 610)], INK, 10, 1) + poly([(990, 360), (1370, 340), (1370, 352), (990, 372)], INK, 10, 1))
    # rays of first light sweeping across the floor
    rays = []
    for i in range(7):
        a = 2.2 + i * .06
        rays.append(poly([(1180, 380), (1180 + math.cos(a) * 1800, 380 + math.sin(a) * 1800), (1180 + math.cos(a + .025) * 1800, 380 + math.sin(a + .025) * 1800)], PAPER, 40, 4))
    o.append(f'<g class="rays">{"".join(rays)}</g>')
    o.append(rows((0, 900, 1600, 1300), 0.0, 22, .8, 2.4, PAPER, .6, r))
    bug = insect_top(random.Random(9), twitch=False)
    o.append(f'<g transform="translate(260 1030) rotate(-4) scale(.95)">{bug}</g>')
    o.append(poly(ellipse_pts(470, 1010, 26, 22, 16), '#5a3a26', 6, 1.2) + ''.join(gouge(470 + r.uniform(-20, 20), 1010 + r.uniform(-18, 18), r.uniform(0, 6), 8, 2, PAPER, r=r) for _ in range(6)))
    panel('dawn', W, Hh, 'h2', 'Gregor’s room before morning. Through the window, a clock tower against the first grey light, rays reaching across the floor. Gregor lies still, flat, the old apple dark on his back.',
          ''.join(o), [
              ('cap', 'He thought back of his family with emotion and love.', 'l:5%;t:8%;w:16em', 'l:5%;t:4%'),
              ('cap', 'Then, without his willing it, his head sank down completely, and his last breath flowed weakly from his nostrils.', 'r:5%;b:6%;w:20em', 'l:5%;b:4%'),
          ])

# ---- 18 charwoman
def p_char():
    W, Hh = 1400, 1200
    r = random.Random(181)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1400, 1200), 1.2, 22, 1.4, 4.5, INK, .4, r))
    door = [(380, 60), (1040, 40), (1060, 1200), (360, 1200)]
    o.append(poly(door, INK, 16, 3))
    cw = [(520, 1200), (560, 860), (520, 640), (560, 470), (600, 420), (580, 360), (600, 300), (560, 270), (700, 230), (820, 260),
          (760, 290), (780, 360), (770, 420), (840, 470), (900, 640), (860, 860), (900, 1200)]
    o.append(figure(cw, None, r, PAPER))
    o.append(rows((500, 220, 920, 1200), 1.4, 12, .8, 2, INK, .5, r, D(cw)))
    # ostrich feather on the hat
    o.append(f'<g class="feather">{taper(curve((700, 240), (690, 40), .25, 10), 16, 2, PAPER)}<animateTransform attributeName="transform" type="rotate" values="0 700 240;5 700 240;-4 700 240;0 700 240" dur="2.4s" repeatCount="indefinite"/></g>')
    # broom
    o.append(taper([(820, 500), (1240, 1120)], 12, 10, PAPER) + poly([(1180, 1080), (1330, 1050), (1380, 1200), (1170, 1200)], PAPER, 10, 3))
    panel('char', W, Hh, 'h2', 'The charwoman fills the dark doorway, broom in hand, a tall feather on her hat.',
          ''.join(o), [
              ('say', '“Come and ’ave a look at this, it’s dead, just lying there, stone dead!”', 'l:5%;t:8%;w:15em', 'l:4%;t:4%', 'tail-r'),
          ], bg=PAPER)

# ---- 19 tram
def p_tram():
    W, Hh = 1600, 950
    r = random.Random(191)
    o = [paper_rect(W, Hh, PAPER)]
    sun_r = []
    for i in range(28):
        a = math.pi + i / 27 * math.pi
        sun_r.append(gouge(1200 + math.cos(a) * 130, 330 + math.sin(a) * 130, a, r.uniform(140, 420), r.uniform(3, 7), INK, r=r))
    o.append(layer(.3, f'<g class="sunrays">{"".join(sun_r)}</g>' + poly(ellipse_pts(1200, 330, 110, 110, 40), INK, 10, 2) + poly(ellipse_pts(1200, 330, 92, 92, 40), PAPER, 10, 2)))
    hills = [(0, 620), (300, 560), (600, 600), (900, 540), (1200, 580), (1600, 520), (1600, 950), (0, 950)]
    o.append(layer(.15, poly(hills, INK, 20, 3) + rows((0, 520, 1600, 950), -0.05, 16, 1.4, 4, PAPER, .45, r, D(hills))))
    # tram
    tram = [(260, 760), (300, 560), (900, 540), (960, 740)]
    o.append(layer(.05, poly(tram, INK, 14, 2) + ''.join(poly([(330 + k * 110, 590), (420 + k * 110, 586), (424 + k * 110, 680), (334 + k * 110, 684)], PAPER, 10, 1.5) for k in range(5))
             + taper([(600, 540), (700, 380)], 6, 3) + taper([(700, 380), (1600, 360)], 4, 3) + taper([(0, 380), (700, 380)], 4, 3)))
    o.append(taper([(0, 780), (1600, 760)], 8, 8) + taper([(0, 820), (1600, 800)], 8, 8))
    panel('tram', W, Hh, 'h1', 'Open country. A small tram crosses carved hills under a large sun with long black rays.',
          ''.join(o), [
              ('cap', 'They had the tram, filled with warm sunshine, all to themselves.', 'l:5%;t:8%;w:16em', 'l:5%;t:5%'),
          ], bg=PAPER)

# ---- 20 stretch
def p_stretch():
    W, Hh = 1600, 1000
    r = random.Random(201)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 860, 1600, 1000), 0.0, 22, 1, 3, INK, .6, r))
    g = [(720, 860), (740, 640), (720, 520), (690, 380), (640, 150), (670, 140), (730, 330), (760, 310), (750, 270), (770, 230), (810, 230),
         (830, 270), (820, 310), (850, 330), (910, 140), (940, 150), (890, 380), (860, 520), (850, 640), (880, 860)]
    o.append(layer(.08, f'<g class="stretchfig">{figure(g, [[(830, 280), (850, 340), (880, 300)]], r)}</g>'))
    panel('stretch', W, Hh, 'h1', 'White paper. At the tram stop, Grete stands and stretches her arms high.',
          ''.join(o), [
              ('cap', 'Grete was the first to get up and stretch out her young body.', 'l:6%;b:12%;w:15em', 'l:5%;b:6%'),
          ], bg=PAPER)


# ================================================================ revised panels (skeleton figures)
BASE = dict(head=(0, -600), neck=(0, -540), ls=(-56, -512), rs=(54, -512), le=(-74, -372), re=(70, -372),
            lh=(-80, -236), rh=(78, -236), lp=(-30, -320), rp=(30, -320), lk=(-36, -160), rk=(36, -160),
            lf=(-40, 0), rf=(40, 0))

def pose(ox, oy, s=1.0, face=1, **over):
    """Base standing pose (elongated, Caligari-thin), overridden joint by joint, placed at (ox, oy)."""
    J = dict(BASE)
    J.update(over)
    out = {}
    for k, v in J.items():
        if v is None:
            continue
        x, y = v
        out[k] = (ox + x * s * face, oy + y * s)
    return out

def fig(J, s, face=1, **kw):
    return person(J, s, face, **kw)

def shadow_on_wall(J, s, face, dx, dy, skew=.35, scale=1.25, **kw):
    """A long cast shadow of a figure: the same skeleton, skewed and stretched."""
    by = max(v[1] for v in J.values())
    S = {k: (J[k][0] + (J[k][1] - by) * -skew * scale + dx, by + (J[k][1] - by) * scale + dy) for k in J}
    return person(S, s * scale, face, rims=False, **kw)

# ---- 1 title
def p_title():
    W, Hh = 1600, 1000
    r = random.Random(11)
    o = [paper_rect(W, Hh, PAPER)]
    sky = [(0, 400), (1600, 360), (1600, 620), (0, 700)]
    o.append(layer(.25, rows((0, 360, 1600, 700), -0.08, 13, 1.6, 4.4, INK, .4, r, D(sky))))
    city = [(0, 1000), (0, 640), (60, 640), (60, 560), (90, 520), (120, 560), (120, 610), (210, 600), (250, 540), (290, 600), (330, 590),
            (360, 470), (372, 380), (384, 470), (400, 600), (470, 610), (520, 520), (560, 610), (640, 600), (650, 420), (668, 300),
            (686, 420), (700, 560), (720, 430), (738, 330), (756, 430), (770, 590), (860, 600), (900, 540), (960, 600), (1040, 580),
            (1080, 500), (1120, 580), (1200, 590), (1240, 470), (1262, 410), (1284, 470), (1300, 590), (1380, 600), (1420, 540),
            (1470, 600), (1600, 560), (1600, 1000)]
    wins = []
    for _ in range(60):
        x = r.uniform(20, 1580); y = r.uniform(650, 960)
        wins.append(poly([(x, y), (x + 10, y), (x + 10, y + 22), (x, y + 22)], PAPER, 8, 1.2))
    o.append(layer(.08, poly(city, INK, 18, 3) + ''.join(wins)))
    o.append(rows((0, 880, 1600, 1000), 0.02, 12, 1.2, 3, PAPER, .5, r))
    # a carved border
    o.append(f'<path d="{D(rough([(24, 24), (1576, 24), (1576, 976), (24, 976)], 30, 2.5))}" fill="none" stroke="{INK}" stroke-width="10"/>')
    body = ''.join(o)
    panel('title', W, Hh, 'h1', 'A woodcut of Prague roofs and spires under a rainy sky. Carved title: The Metamorphosis, Franz Kafka, 1915.', body, [], bg=PAPER)

# ---- 2 morning: the bed
def p_morning():
    W, Hh = 1600, 1000
    r = random.Random(21)
    o = [paper_rect(W, Hh)]
    o.append(layer(.05, rows((0, 0, 1600, 640), 0.0, 22, 1.2, 3.2, PAPER, .55, r, D([(0, 0), (1600, 0), (1600, 560), (0, 660)]))))
    o.append(layer(.12, window(1080, 120, 330, 380, r, skew=-30)))
    lw = [(1080, 520), (1410, 480), (1600, 760), (1600, 1000), (1220, 1000)]
    o.append(poly(lw, PAPER, 20, 3) + rows((1000, 480, 1600, 1000), -0.9, 16, 1.5, 4, INK, .4, r, D(lw)))
    # bed frame and tall carved headboard
    o.append(poly([(140, 560), (980, 470), (1060, 700), (1040, 900), (180, 980), (110, 760)], INK, 18, 3))
    hb = [(100, 250), (230, 220), (260, 620), (120, 660)]
    o.append(poly(hb, INK, 16, 3) + ''.join(taper([(130 + k * 26, 280 - k * 6), (138 + k * 28, 600 - k * 8)], 4, 2, PAPER) for k in range(4)))
    quilt = [(200, 560), (930, 480), (1020, 690), (980, 820), (240, 900), (180, 740)]
    qd = D(quilt)
    o.append(poly(quilt, PAPER, 16, 3))
    # the long shape under the quilt: shadowed underside, ridges pressing through
    inner = []
    hump = rot(ellipse_pts(600, 650, 330, 125, 40), -.12, 600, 650)
    lower = [p for p in hump if p[1] > 640 - (p[0] - 600) * .12]
    inner.append(rows((240, 560, 980, 820), -0.12, 9, 1.4, 3.6, INK, .25, r, D(rot(ellipse_pts(600, 700, 330, 80, 30, 0, math.pi), -.12, 600, 650))))
    for i, x in enumerate(range(330, 900, 52)):
        y0 = 600 - (x - 300) * .12
        inner.append(taper(curve((x + 16, y0 - 6), (x - 14, y0 + 150), -.16, 8), 2, 7, INK))
    # quilt folds elsewhere
    inner.append(rows((180, 480, 1020, 900), -0.12, 34, 1.4, 3.4, INK, .55, r, D([(200, 560), (930, 480), (960, 540), (220, 640)])))
    inner.append(rows((180, 760, 1020, 900), -0.06, 18, 1.4, 4, INK, .3, r, D([(180, 790), (1000, 740), (980, 820), (240, 900)])))
    o.append(f'<clipPath id="qclip"><path d="{qd}"/></clipPath><g clip-path="url(#qclip)">' + ''.join(inner) + '</g>')
    for i, x in enumerate((420, 500, 590, 680, 770)):
        y = 880 - (x - 420) * .1
        g = leg([(x, y - 30), (x - 30, y + 30), (x + 12, y + 80), (x - 10, y + 104)], [12, 8, 4, 1.2], r=r)
        o.append(f'<g>{g}<animateTransform attributeName="transform" type="rotate" values="0 {x} {y-30};{9 if i%2 else -9} {x} {y-30};0 {x} {y-30}" dur="{1.1+i*.3:.1f}s" repeatCount="indefinite"/></g>')
    o.append(rows((0, 920, 1600, 1000), 0.02, 14, 1.4, 3.5, PAPER, .5, r))
    panel('morning', W, Hh, 'h1', 'A dark bedroom at dawn. Rain runs down the window. On the bed a long hump lies under the quilt, ridged like a shell, and thin legs twitch at its edge.',
          ''.join(o), [
              ('cap', 'One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin.', 'l:5%;t:7%;w:30em', 'l:5%;t:5%'),
          ])

# ---- 3 the belly, close
def p_belly():
    W, Hh = 1600, 1300
    r = random.Random(31)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 1300), 0.5, 22, 1.6, 4.6, INK, .3, r))
    o.append(poly([(0, 0), (520, 0), (0, 520)], INK, 20, 3) + poly([(1600, 1300), (1600, 700), (1000, 1300)], INK, 20, 3))
    bug = insect_belly(r)
    o.append(layer(.1, f'<g transform="translate(300 720) rotate(-28) scale(1.5)">{bug}</g>'))
    panel('belly', W, Hh, 'h2', 'Close up from above: Gregor on his back on the sheet. A domed brown belly divided by arches into stiff sections, and many thin, spiny legs waving in the air.',
          ''.join(o), [
              ('cap', 'He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections.', 'r:5%;t:6%;w:24em', 'l:5%;t:4%'),
              ('cap', 'His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.', 'l:5%;b:7%;w:22em', 'r:5%;b:5%'),
          ], bg=PAPER)

# ---- 7 the key
def p_key():
    W, Hh = 1600, 1000
    r = random.Random(71)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 1000), 1.57, 26, 2, 6, INK, .3, r))
    plate = [(880, 220), (1080, 210), (1100, 760), (890, 770)]
    o.append(poly(plate, INK, 14, 2.5) + rows((870, 200, 1110, 780), 1.57, 14, 1, 2.6, PAPER, .6, r, D(plate)))
    o.append(poly(ellipse_pts(990, 450, 30, 30, 18), PAPER, 6, 1) + poly([(975, 470), (1005, 470), (1020, 600), (960, 600)], PAPER, 8, 1))
    # the key: shaft into the hole, ring bow outside
    o.append(taper([(836, 470), (990, 468)], 22, 18))
    o.append(poly(ellipse_pts(790, 470, 54, 50, 26), INK, 8, 1.5) + poly(ellipse_pts(790, 470, 24, 22, 16), PAPER, 6, 1))
    # the head in profile from the left, angular capsule with seams
    head = [(-40, 170), (220, 140), (430, 190), (580, 280), (650, 370), (660, 450), (640, 540), (560, 630), (400, 700), (190, 750), (-40, 770)]
    hd = D(head)
    hg = [poly(head, INK, 14, 3), rows((0, 140, 660, 770), -0.25, 16, 1.2, 3.4, PAPER, .55, r, hd)]
    for x0, b in ((250, .1), (360, .12)):
        hg.append(taper(curve((x0, 170), (x0 - 30, 740), b, 10), 2, 6, PAPER))
    # compound eye: dark, ringed by carving
    for k, (rx, ry) in enumerate(((78, 56), (58, 40), (36, 24))):
        e = rot(ellipse_pts(470, 330, rx, ry, 26), .35, 470, 330)
        hg.append(f'<path d="{D(rough(e, 10, 1.5))}" fill="none" stroke="{PAPER}" stroke-width="{3.5-k}"/>')
    hg.append(gouge(440, 312, -.4, 22, 4, r=r))
    # antenna sweeping back
    hg.append(taper(curve((520, 220), (200, -40), -.15, 16), 10, 1.5))
    # mandibles clamping the ring, with teeth
    for up in (1, -1):
        pts = [(600, 470 - up * 80), (700, 470 - up * 100), (770, 470 - up * 70), (800, 470 - up * 28)]
        hg.append(taper(pts, 46, 6))
        for k in range(4):
            t = .3 + k * .15
            x = pts[0][0] + (pts[-1][0] - pts[0][0]) * t
            y = 470 - up * (80 + 10 - 60 * t)
            hg.append(gouge(x, y + up * 12, math.pi / 2 * up, 14, 8, INK, bend=0, r=r))
    # palps
    for k, (x, y) in enumerate(((610, 590), (650, 570))):
        hg.append(taper([(x, y), (x + 30, y + 70), (x + 10, y + 130), (x + 30, y + 180)], 14, 3))
    o.append(layer(.08, ''.join(hg)))
    drip = taper([(800, 520), (804, 600), (798, 700), (806, 820), (802, 1000)], 16, 6, RUST)
    o.append(f'<g class="drip">{drip}<circle cx="802" cy="1000" r="12" fill="{RUST}"/></g>')
    panel('key', W, Hh, 'h1', 'Extreme close up: Gregor’s carved insect head in profile, its jaws clamped on the ring of the key in the lock. A brown fluid runs over the key and drips down.',
          ''.join(o), [
              ('cap', 'he bit on the key with all his strength,', 'l:5%;t:7%', 'l:5%;t:4%'),
              ('cap', 'a brown fluid came from his mouth, flowed over the key and dripped onto the floor.', 'r:5%;b:9%;w:18em', 'l:5%;b:5%'),
              ('say', '“he’s turning the key.”', 'r:6%;t:9%', 'r:4%;t:22%', 'tail-r'),
          ], bg=PAPER)

# ---- 8 the door opens
def p_reveal():
    W, Hh = 1600, 1050
    r = random.Random(81)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 760), -0.05, 26, 1.4, 4, INK, .5, r))
    floor = [(0, 760), (1600, 700), (1600, 1050), (0, 1050)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 690, 1600, 1050), -0.04, 18, 1.5, 4, PAPER, .45, r, D(floor)))
    dw = [(1180, 80), (1600, 40), (1600, 1050), (1180, 1050)]
    o.append(poly(dw, INK, 18, 3))
    bug = insect_top(r)
    o.append(layer(.05, f'<g transform="translate(1720 540) rotate(186) scale(1)">{bug}</g>'))
    o.append(poly([(1150, 60), (1200, 60), (1215, 1050), (1165, 1050)], PAPER, 12, 2))
    # long shadows thrown back across the floor
    clerkJ = pose(330, 1040, 1.22, 1, head=(-80, -590), neck=(-62, -536), ls=(-110, -505), rs=(0, -505), re=(40, -440), rh=(-30, -575),
                  le=(-190, -460), lh=(-290, -530), lp=(-60, -320), rp=(0, -320), lk=(-120, -165), lf=(-190, 0), rk=(10, -160), rf=(40, 0))
    momJ = pose(760, 900, .82, 1, head=(50, -330), neck=(16, -370), ls=(-48, -350), rs=(44, -340), le=(-50, -250), lh=(10, -200),
                re=(70, -250), rh=(40, -200), lp=(-30, -160), rp=(30, -160), lk=None, rk=None, lf=None, rf=None)
    faJ = pose(1010, 900, .9, 1, ls=(-66, -515), rs=(64, -515), le=(-120, -400), lh=(-70, -470), re=(124, -390), rh=(150, -480),
               lp=(-36, -320), rp=(36, -320), lk=(-62, -160), lf=(-86, 0), rk=(62, -160), rf=(86, 0))
    o.append(layer(.18, fig(clerkJ, 1.22, 1, coat=(950, 40), hat='bowler', moust=True, r=r, light=(.8, -.6))))
    o.append(layer(.12, fig(momJ, .82, 1, skirt=(900, 180), bun=True, r=r, light=(.8, -.6))))
    o.append(layer(.1, fig(faJ, .9, 1, coat=(830, 34), moust=True, r=r, light=(.8, -.6))))
    panel('reveal', W, Hh, 'h1', 'The door is open. From the black doorway Gregor’s head and shell lean out. The chief clerk, in a bowler hat, backs away with his hand at his mouth; the mother sinks down into her skirts; the father clenches his fists.',
          ''.join(o), [
              ('burst', '“Oh!”', 'l:24%;t:6%', 'l:8%;t:6%'),
              ('cap', 'his hand pressed against his open mouth and slowly retreating as if driven by a steady and invisible force.', 'l:4%;b:5%;w:20em', 'l:4%;b:4%'),
          ], bg=PAPER)

# ---- 9 father with stick: his shadow on the wall
def p_father():
    W, Hh = 1400, 1500
    r = random.Random(91)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1400, 1100), 0.9, 24, 1.5, 5, INK, .45, r))
    floor = [(0, 1100), (1400, 1040), (1400, 1500), (0, 1500)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 1040, 1400, 1500), -0.05, 18, 1.4, 4, PAPER, .45, r, D(floor)))
    for i in range(5):
        x = 40 + i * 46
        o.append(layer(.3, taper(curve((x, 0), (x + 360 + i * 30, 480 + i * 36), .25 - i * .03, 14), 54 - i * 8, 6)))
    # the father in the foreground, huge, from below: stick raised, newspaper out, stamping
    J = pose(640, 1580, 2.05, 1, head=(30, -600), neck=(16, -540), ls=(-62, -510), rs=(68, -512), re=(150, -640), rh=(168, -770),
             le=(-150, -430), lh=(-240, -420), lp=(-36, -320), rp=(36, -320), lk=(-90, -160), lf=(-120, 0), rk=(110, -220), rf=(150, -110))
    stick = taper([(J['rh'][0], J['rh'][1] + 20), (J['rh'][0] + 260, J['rh'][1] - 330)], 26, 14)
    news = [(J['lh'][0] - 170, J['lh'][1] - 120), (J['lh'][0] + 30, J['lh'][1] - 170), (J['lh'][0] + 60, J['lh'][1] + 70), (J['lh'][0] - 140, J['lh'][1] + 120)]
    o.append(layer(.12, fig(J, 2.05, 1, coat=(1400, 70), moust=True, r=r, light=(-.8, -.5))
                   + stick + poly(news, PAPER, 12, 2) + rows((news[0][0] - 10, news[1][1] - 10, news[2][0] + 10, news[3][1] + 10), -0.25, 12, 1, 2.4, INK, .3, r, D(news))))
    bug = insect_top(r)
    o.append(f'<g transform="translate(1180 1380) rotate(160) scale(.42)">{bug}</g>')
    panel('father', W, Hh, 'h3', 'From the floor: the father looms, a huge black figure with the clerk’s stick raised high and a newspaper thrust out, one foot stamping, curtains flying. Gregor backs away below.',
          ''.join(o), [
              ('cap', 'making hissing noises at him like a wild man.', 'r:6%;b:24%;w:14em', 'r:5%;b:16%'),
          ], bg=PAPER)

# ---- 10 under the couch, the milk
def p_milk():
    W, Hh = 1600, 1000
    r = random.Random(101)
    o = [paper_rect(W, Hh)]
    lightw = [(140, 120), (420, 100), (900, 1000), (0, 1000), (0, 700)]
    o.append(poly(lightw, PAPER, 18, 3) + rows((0, 100, 900, 1000), 1.1, 18, 1.2, 3.5, INK, .45, r, D(lightw)))
    o.append(poly([(110, 90), (440, 70), (440, 120), (110, 140)], INK, 12, 2))
    J = pose(300, 900, .95, 1, head=(150, -470), neck=(110, -450), ls=(40, -470), rs=(110, -440), lp=(-20, -300), rp=(30, -300),
             re=(160, -300), rh=(170, -90), le=(40, -330), lh=(70, -200), lk=None, rk=None, lf=None, rf=None)
    o.append(layer(.1, fig(J, .95, 1, skirt=(900, 120), bun=True, r=r, light=(-.8, -.5))))
    # her shadow thrown long across the floor
    o.append(poly(ellipse_pts(470, 830, 70, 18, 24), INK, 8, 1) + poly(ellipse_pts(470, 825, 56, 10, 20), PAPER, 6, .8))
    couch = [(900, 520), (1600, 470), (1600, 820), (900, 830)]
    o.append(poly(couch, INK, 16, 3) + rows((900, 460, 1600, 840), -0.05, 30, 1, 3, PAPER, .6, r, D(couch)))
    o.append(rows((900, 830, 1600, 1000), 0.0, 9, .6, 1.4, PAPER, .7, r))
    for sd in (1, -1):
        o.append(f'<g>{taper([(960, 900 + sd*10), (850, 880 + sd*30), (720, 860 + sd*55)], 5, 1)}<animateTransform attributeName="transform" type="rotate" values="0 960 900;{4*sd} 960 900;0 960 900" dur="{2.2 if sd>0 else 3}s" repeatCount="indefinite"/></g>')
    o.append(f'<path d="{D(rot(ellipse_pts(985, 892, 12, 7, 12), .3, 985, 892))}" fill="none" stroke="{PAPER}" stroke-width="2"/>')
    panel('milk', W, Hh, 'h1', 'Night in Gregor’s room. Through the open door, light falls on the floor where his sister bends to set down a dish. Under the black couch, two antennae and the rim of an eye.',
          ''.join(o), [
              ('cap', 'By the door there was a dish filled with sweetened milk with little pieces of white bread floating in it.', 'r:5%;t:8%;w:20em', 'r:5%;t:5%'),
          ])

# ---- 11 the picture
def p_picture():
    W, Hh = 1600, 1200
    r = random.Random(111)
    o = [paper_rect(W, Hh, PAPER)]
    fl = []
    for i in range(0, 1700, 120):
        for j in range(0, 900, 120):
            x, y = i + (60 if (j // 120) % 2 else 0), j + 50
            fl.append(''.join(gouge(x + math.cos(a) * 4, y + math.sin(a) * 4, a, 15, 6, INK, bend=.2, r=r) for a in (0, 1.26, 2.51, 3.77, 5.03)))
    o.append(layer(.05, ''.join(fl)))
    floor = [(0, 900), (1600, 860), (1600, 1200), (0, 1200)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 850, 1600, 1200), 0.4, 20, 1.5, 4, PAPER, .45, r, D(floor)))
    fr = [(820, 150), (1160, 140), (1170, 600), (830, 610)]
    o.append(poly(fr, INK, 14, 2) + poly([(860, 190), (1125, 182), (1132, 565), (868, 572)], PAPER, 12, 2))
    lady = [(900, 560), (920, 450), (960, 400), (960, 330), (930, 300), (950, 240), (1010, 220), (1070, 250), (1080, 300), (1050, 330),
            (1050, 400), (1090, 450), (1100, 560)]
    o.append(poly(lady, INK, 10, 2) + poly(ellipse_pts(1000, 470, 70, 38, 20), PAPER, 8, 2))
    bug = insect_top(r)
    o.append(f'<g transform="translate(900 760) rotate(-62) scale(.64)">{bug}</g>')
    # the two women dragging the chest out
    chest = [(160, 690), (420, 680), (430, 900), (170, 910)]
    A = pose(70, 1100, .9, 1, head=(70, -560), neck=(56, -510), ls=(10, -490), rs=(90, -470), le=(70, -400), lh=(100, -380),
             re=(130, -380), rh=(110, -330), lp=(-20, -320), rp=(30, -320), lk=None, rk=None, lf=None, rf=None)
    B = pose(530, 1100, .9, -1, head=(70, -560), neck=(56, -510), ls=(10, -490), rs=(90, -470), le=(70, -400), lh=(100, -380),
             re=(130, -380), rh=(110, -330), lp=(-20, -320), rp=(30, -320), lk=None, rk=None, lf=None, rf=None)
    o.append(layer(.15, poly(chest, INK, 14, 2) + ''.join(taper([(170, 740 + k * 52), (420, 735 + k * 52)], 5, 5, PAPER) for k in range(3))
             + fig(A, .9, 1, skirt=(1100, 110), bun=True, r=r, light=(.8, -.6)) + fig(B, .9, -1, skirt=(1100, 110), bun=True, r=r, light=(.8, -.6))))
    panel('picture', W, Hh, 'h2', 'The emptied room, bare flowered wallpaper. Two women drag the chest of drawers away. On the wall, Gregor’s dark body covers the framed picture of the lady in furs.',
          ''.join(o), [
              ('cap', 'He hurried up onto the picture and pressed himself against its glass,', 'r:5%;b:30%;w:14em', 'r:4%;t:4%'),
              ('say', '“Oh God, oh God!”', 'l:5%;t:8%', 'l:4%;t:16%', 'tail-b'),
          ], bg=PAPER)

# ---- 12 apples (tall)
def p_apples():
    W, Hh = 1200, 1800
    r = random.Random(121)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1200, 1400), 0.75, 26, 1.4, 4.4, INK, .4, r))
    # the father's sleeve and fist from the top right
    arm = taper([(1320, -80), (1060, 120), (860, 300)], 170, 90)
    fist = poly(ellipse_pts(840, 320, 60, 54, 18), INK, 8, 2)
    cuff = taper([(930, 240), (880, 330)], 16, 16, PAPER)
    o.append(layer(.2, arm + fist + cuff + rows((820, -80, 1320, 360), -0.7, 22, 1.2, 3, PAPER, .55, r, D([(1320, -80), (1060, 120), (860, 300), (900, 380), (1130, 210), (1320, 60)]))))
    apples = []
    for i, (x, y, rr_) in enumerate(((700, 520, 36), (520, 700, 32), (780, 900, 30), (430, 1060, 34), (640, 1200, 28))):
        a = poly(ellipse_pts(x, y, rr_, rr_ * .92, 18), RUST, 8, 1.5) + gouge(x - rr_ * .4, y - rr_ * .5, -.6, rr_ * .6, 4, PAPER, r=r) + taper([(x, y - rr_), (x + 6, y - rr_ - 22)], 6, 3)
        apples.append(f'<g class="apple" data-i="{i}">{a}</g>')
    o.append(''.join(apples))
    floor = [(0, 1400), (1200, 1360), (1200, 1800), (0, 1800)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 1360, 1200, 1800), 0.02, 16, 1.3, 3.6, PAPER, .45, r, D(floor)))
    bug = insect_top(r)
    o.append(f'<g transform="translate(220 1570) rotate(-8) scale(.92)">{bug}</g>')
    o.append(poly(ellipse_pts(430, 1520, 32, 28, 18), RUST, 6, 1.2) + gouge(420, 1506, -.5, 18, 3, PAPER, r=r))
    panel('apples', W, Hh, 'h3', 'A tall panel. From above, the father’s black sleeve and fist; small red apples fall through the room. Below, Gregor, one apple sunk into his back.',
          ''.join(o), [
              ('cap', 'It was an apple; then another one immediately flew at him;', 'l:5%;t:6%;w:14em', 'l:5%;t:4%'),
              ('cap', 'hit squarely and lodged in his back;', 'r:5%;b:6%', 'r:5%;b:4%'),
          ], bg=PAPER)

# ---- 13 violin
def violin(cx, cy, ang, sc=1.0):
    body = ellipse_pts(0, 0, 70, 34, 28, squash=lambda t: 1 - .28 * abs(math.cos(2 * t)) * (abs(math.sin(t)) > .5))
    g = [poly([(x * sc, y * sc) for x, y in body], INK, 8, 1.2), taper([(60 * sc, 0), (170 * sc, 0)], 12 * sc, 9 * sc),
         poly([(160 * sc, -9 * sc), (196 * sc, -12 * sc), (196 * sc, 12 * sc), (160 * sc, 9 * sc)], INK, 6, 1),
         taper([(-50 * sc, -2 * sc), (160 * sc, -1 * sc)], 1.4, 1.4, PAPER), taper([(-50 * sc, 4 * sc), (160 * sc, 3 * sc)], 1.4, 1.4, PAPER)]
    for sd in (1, -1):
        g.append(taper([(-12 * sc, sd * 10 * sc), (-2 * sc, sd * 18 * sc), (10 * sc, sd * 12 * sc)], 2, 2, PAPER))
    return f'<g transform="translate({f(cx)} {f(cy)}) rotate({ang})">{"".join(g)}</g>'

def p_violin():
    W, Hh = 1600, 1000
    r = random.Random(131)
    o = [paper_rect(W, Hh)]
    cone = [(760, 0), (840, 0), (1250, 1000), (350, 1000)]
    o.append(poly(cone, PAPER, 18, 3) + rows((350, 0, 1250, 1000), 1.57, 16, 1, 3, INK, .55, r, D(cone)))
    # Grete: head bent to the violin under her chin
    J = pose(820, 1000, 1.0, -1, head=(28, -585), neck=(14, -535), ls=(-54, -510), rs=(56, -512), le=(-120, -490), lh=(-200, -520),
             re=(110, -400), rh=(60, -470), lp=(-30, -320), rp=(30, -320), lk=None, rk=None, lf=None, rf=None)
    o.append(layer(.1, fig(J, 1.0, -1, skirt=(1000, 150), bun=True, r=r, light=(.7, -.7))
                   + violin(J['ls'][0] + 6, J['ls'][1] - 10, -168, 1.1)
                   + taper([(J['rh'][0] + 10, J['rh'][1] + 40), (J['rh'][0] - 120, J['rh'][1] - 140)], 4, 3)))
    o.append(taper([(560, 1000), (560, 560)], 8, 6) + poly([(490, 520), (640, 500), (650, 580), (500, 600)], INK, 10, 1.5))
    # three gentlemen, smoking, black against the window
    win = [(1090, 200), (1580, 180), (1580, 760), (1100, 780)]
    o.append(poly(win, PAPER, 16, 2) + rows((1090, 180, 1580, 780), 0.05, 18, 1, 2.6, INK, .5, r, D(win)) + taper([(1330, 190), (1335, 770)], 14, 14) + taper([(1095, 470), (1580, 460)], 14, 14))
    for k, x in enumerate((1180, 1320, 1460)):
        arms = dict(le=(-80, -380), lh=(-40, -300), re=(80, -380), rh=(36, -300))
        if k == 1:
            arms.update(re=(60, -430), rh=(30, -560))
        L = pose(x, 1000, .9, -1, **arms)
        o.append(layer(.16, fig(L, .9, -1, coat=(1000 - 60, 26), beard=True, r=r, light=(-.8, -.5))))
        hx, hy = L['head']
        smoke = [(hx - 20 + math.sin(t / 3) * 18 * (1 + t / 8), hy - 30 - t * 30) for t in range(10)]
        o.append(taper(smoke, 6, 1, PAPER))
    panel('violin', W, Hh, 'h1', 'Lamplight. Grete plays the violin at a music stand, her head bent over it. By the window, three bearded gentlemen in long coats stand smoking.',
          ''.join(o), [
              ('cap', 'Yet Gregor’s sister was playing so beautifully.', 'l:5%;t:8%;w:14em', 'l:5%;t:4%'),
          ])

# ---- 14 drawn to the music
def p_drawn():
    W, Hh = 1600, 900
    r = random.Random(141)
    o = [paper_rect(W, Hh)]
    beam = [(1600, 200), (1600, 520), (300, 900), (0, 900), (0, 820)]
    o.append(poly(beam, PAPER, 18, 3) + rows((0, 200, 1600, 900), -0.3, 14, 1, 3, INK, .5, r, D(beam)))
    J = pose(1480, 560, .45, -1, le=(-120, -490), lh=(-200, -520), re=(110, -400), rh=(60, -470), lk=None, rk=None, lf=None, rf=None)
    o.append(layer(.25, fig(J, .45, -1, skirt=(560, 70), bun=True, r=r, rims=False) + violin(J['ls'][0] + 3, J['ls'][1] - 5, -168, .5)))
    bug = insect_top(r)
    o.append(layer(.06, f'<g transform="translate(120 700) rotate(-16) scale(1.05)">{bug}</g>'))
    o.append(''.join(gouge(r.uniform(40, 700), r.uniform(560, 860), r.uniform(0, 6.28), r.uniform(10, 40), 1.6, PAPER, r=r) for _ in range(40)))
    panel('drawn', W, Hh, 'h1', 'Low on the floor, Gregor crawls out of the dark into a long beam of light toward the small far figure of his sister with her violin.',
          ''.join(o), [
              ('cap', 'Was he an animal if music could captivate him so?', 'r:5%;t:9%;w:15em', 'r:5%;t:5%'),
          ])

# ---- 15 lodgers: the pointing hand, three shadows on the wall
def p_lodgers():
    W, Hh = 1600, 950
    r = random.Random(151)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 760), 0.25, 22, 1.6, 5, INK, .4, r))
    floor = [(0, 760), (1600, 730), (1600, 950), (0, 950)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 730, 1600, 950), 0.0, 16, 1.4, 3.6, PAPER, .45, r, D(floor)))
    # three tall shadows thrown up the wall, leaning
    sh = []
    for k, x in enumerate((640, 860, 1080)):
        arms = {'re': (150, -480), 'rh': (320, -470)} if k == 1 else {'le': (-120, -430), 'lh': (-110, -570), 're': (110, -430), 'rh': (130, -580)}
        J = pose(x, 760, 1.0, 1, **arms)
        sh.append(shadow_on_wall(J, 1.0, 1, 0, 0, skew=.42, scale=1.08, coat=(760 - 70, 30), beard=True, hat='bowler', r=r, folds=False))
    o.append(layer(.3, f'<g opacity=".92">{"".join(sh)}</g>'))
    bug = insect_top(r)
    o.append(f'<g transform="translate(1560 860) rotate(178) scale(.34)">{bug}</g>')
    panel('lodgers', W, Hh, 'h1', 'On the wall, the long leaning shadows of the three bearded gentlemen in bowler hats: the middle one thrusts out an arm and points, the others throw up their hands. Far right on the floor, Gregor.',
          ''.join(o), [
              ('say', '“Mr. Samsa!”', 'l:62%;t:8%', 'l:50%;t:6%', 'tail-l'),
          ], bg=PAPER)

# ---- 16 sister
def p_sister():
    W, Hh = 1400, 1200
    r = random.Random(161)
    o = [paper_rect(W, Hh)]
    lamp = [(640, 0), (760, 0), (1200, 760), (200, 760)]
    o.append(poly(lamp, PAPER, 16, 3) + rows((200, 0, 1200, 760), 1.57, 14, 1, 3, INK, .55, r, D(lamp)))
    G = pose(560, 1110, 1.0, 1, le=(-110, -430), lh=(-150, -340), re=(100, -370), rh=(150, -235), lk=None, rk=None, lf=None, rf=None)
    o.append(layer(.1, fig(G, 1.0, 1, skirt=(1110, 90), bun=True, r=r, light=(-.6, -.8))))
    o.insert(2, shadow_on_wall(G, 1.0, 1, 330, -150, skew=-.55, scale=1.2, skirt=(1110, 90), bun=True, r=r, folds=False))
    table = [(60, 880), (1340, 860), (1360, 930), (40, 950)]
    o.append(poly(table, INK, 14, 2) + taper([(60, 885), (1340, 865)], 3, 3, PAPER) + poly([(40, 950), (1360, 930), (1400, 1200), (0, 1200)], INK, 20, 3) + rows((0, 950, 1400, 1200), 0.0, 16, 1.2, 3.4, PAPER, .5, r))
    panel('sister', W, Hh, 'h2', 'At the table under the lamp, Grete stands and strikes the table with her hand. Her shadow rises huge on the wall behind her.',
          ''.join(o), [
              ('say', '“We have to try and get rid of it”', 'l:8%;t:8%', 'l:5%;t:5%', 'tail-r'),
          ])

# ---- 18 charwoman: black figure in a lit doorway
def p_char():
    W, Hh = 1400, 1200
    r = random.Random(181)
    o = [paper_rect(W, Hh)]
    o.append(rows((0, 0, 1400, 1200), 1.2, 26, 1.2, 3.6, PAPER, .55, r))
    door = [(380, 60), (1040, 40), (1060, 1200), (360, 1200)]
    o.append(poly(door, PAPER, 16, 3) + rows((360, 40, 1060, 1200), 1.57, 20, 1, 2.6, INK, .55, r, D(door)))
    J = pose(700, 1230, 1.5, 1, ls=(-66, -505), rs=(66, -505), lp=(-44, -320), rp=(44, -320), le=(-120, -380), lh=(-60, -310),
             re=(110, -400), rh=(150, -320))
    o.append(fig(J, 1.5, 1, skirt=(1230, 120), hat='feather', r=r, light=(.7, -.7)))
    hx, hy = J['head']
    o.append(f'<g>{taper(curve((hx + 10, hy - 70), (hx - 20, hy - 290), .3, 10), 22, 2)}<animateTransform attributeName="transform" type="rotate" values="0 {f(hx)} {f(hy-70)};6 {f(hx)} {f(hy-70)};-5 {f(hx)} {f(hy-70)};0 {f(hx)} {f(hy-70)}" dur="2.4s" repeatCount="indefinite"/></g>')
    bx, by = J['rh']
    o.append(taper([(bx, by - 60), (bx + 380, by + 680)], 14, 12) + poly([(bx + 330, by + 640), (bx + 470, by + 610), (bx + 520, by + 760), (bx + 310, by + 760)], INK, 10, 3))
    panel('char', W, Hh, 'h2', 'The charwoman stands black against the lit doorway, big-boned, broom in hand, a tall ostrich feather on her hat.',
          ''.join(o), [
              ('say', '“Come and ’ave a look at this, it’s dead, just lying there, stone dead!”', 'l:4%;t:8%;w:13em', 'l:4%;t:4%', 'tail-r'),
          ])

# ---- 19 tram
def p_tram():
    W, Hh = 1600, 950
    r = random.Random(191)
    o = [paper_rect(W, Hh, PAPER)]
    sun_r = [gouge(1180 + math.cos(a) * 130, 300 + math.sin(a) * 130, a, r.uniform(160, 460), r.uniform(3, 8), INK, r=r)
             for a in [math.pi + i / 27 * math.pi for i in range(28)]]
    o.append(layer(.3, f'<g class="sunrays">{"".join(sun_r)}</g>' + poly(ellipse_pts(1180, 300, 110, 110, 40), INK, 10, 2) + poly(ellipse_pts(1180, 300, 90, 90, 40), PAPER, 10, 2)))
    hills = [(0, 700), (260, 650), (560, 690), (860, 630), (1200, 680), (1600, 620), (1600, 950), (0, 950)]
    o.append(layer(.15, poly(hills, INK, 20, 3) + rows((0, 620, 1600, 950), -0.05, 14, 1.4, 4, PAPER, .4, r, D(hills))))
    o.append(taper([(0, 846), (1600, 826)], 8, 8, PAPER) + taper([(0, 880), (1600, 860)], 8, 8, PAPER))
    tram = [(300, 830), (300, 600), (330, 560), (1000, 548), (1030, 590), (1040, 818)]
    wins = ''.join(poly([(350 + k * 128, 600), (450 + k * 128, 597), (452 + k * 128, 700), (352 + k * 128, 703)], PAPER, 10, 1.4) for k in range(5))
    heads = ''.join(poly(ellipse_pts(400 + k * 128, 672, 20, 24, 12), INK, 6, 1) + taper([(372 + k * 128, 703), (428 + k * 128, 701)], 30, 30) for k in (1, 2, 3))
    o.append(layer(.05, poly(tram, INK, 14, 2) + wins + heads + taper([(660, 552), (760, 380)], 6, 3) + taper([(0, 376), (1600, 360)], 3, 3)
             + ''.join(poly(ellipse_pts(x, 832, 30, 30, 14), INK, 6, 1) for x in (400, 520, 820, 940))))
    panel('tram', W, Hh, 'h1', 'Open country. A small tram with three heads in its windows crosses under a large carved sun with long rays.',
          ''.join(o), [
              ('cap', 'They had the tram, filled with warm sunshine, all to themselves.', 'l:5%;t:8%;w:16em', 'l:5%;t:5%'),
          ], bg=PAPER)

# ---- 20 stretch
def p_stretch():
    W, Hh = 1600, 1000
    r = random.Random(201)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 880, 1600, 1000), 0.0, 22, 1, 3, INK, .6, r))
    o.append(f'<path d="{D(rough(ellipse_pts(800, 330, 300, 300, 60), 14, 2))}" fill="none" stroke="{INK}" stroke-width="5"/>')
    J = pose(800, 900, 1.12, 1, head=(6, -620), neck=(2, -558), le=(-48, -690), lh=(-34, -830), re=(52, -690), rh=(38, -830),
             lp=(-28, -320), rp=(28, -320))
    o.append(layer(.08, f'<g class="stretchfig">{fig(J, 1.12, 1, skirt=(900, 90), bun=True, r=r, light=(.7, -.7))}</g>'))
    panel('stretch', W, Hh, 'h1', 'White paper and a pale sun. Grete stands and stretches her arms high above her head.',
          ''.join(o), [
              ('cap', 'Grete was the first to get up and stretch out her young body.', 'l:6%;b:12%;w:15em', 'l:5%;b:6%'),
          ], bg=PAPER)

# ================================================================ polish: profile close-ups
HEAD = [(290, 270), (530, 270), (536, 330), (548, 350), (590, 400), (548, 412), (548, 440), (535, 480), (500, 520), (470, 560),
        (330, 580), (310, 500), (288, 420)]

def tr(pts, cx, cy, s, face, ox=410, oy=420):
    return [(cx + (x - ox) * s * face, cy + (y - oy) * s) for x, y in pts]

def profile(cx, cy, s, face, hat=None, bun=False, moust=False, r=None, eye=True, rimside=True):
    """A carved head in profile, nose toward `face`. Center ~ middle of the skull."""
    r = r or rng
    T = lambda pts: tr(pts, cx, cy, s, face)
    o = [poly(T(HEAD), INK, 10, 1.8)]
    if bun:
        o.append(poly(T(ellipse_pts(300, 320, 52, 48, 18)), INK, 8, 1.5))
        o.append(taper(T([(300, 290), (330, 330), (300, 360)]), 1, 4 * s, PAPER))
        for k in range(4):
            o.append(taper(T([(520 - k * 6, 290 + k * 12), (440, 280 + k * 16), (360, 300 + k * 14)]), 1, 3.6 * s, PAPER))
    if hat == 'bowler':
        o.append(poly(T(ellipse_pts(405, 262, 125, 98, 24, math.pi, 2 * math.pi)), INK, 10, 1.5))
        o.append(taper(T([(250, 268), (575, 260)]), 26 * s, 18 * s))
        o.append(taper(T([(300, 205), (360, 178), (460, 176)]), 1, 5 * s, PAPER))
    if hat == 'cap':
        o.append(poly(T([(282, 300), (290, 200), (520, 196), (540, 280), (640, 300), (540, 300)]), INK, 10, 1.5))
        o.append(taper(T([(300, 230), (510, 226)]), 1, 6 * s, PAPER))
    if moust:
        o.append(poly(T([(545, 415), (610, 430), (590, 448), (540, 440)]), INK, 6, 1))
    if eye:
        o.append(poly(T(ellipse_pts(500, 338, 20, 8, 12)), PAPER, 4, .5) + poly(T(ellipse_pts(506, 338, 6, 6, 8)), INK, 3, .3))
    if rimside:
        o.append(taper(T([(524, 285), (530, 330), (546, 356), (582, 398)]), 1, 6 * s, PAPER))
        o.append(taper(T([(540, 440), (530, 478), (498, 514)]), 5 * s, 1, PAPER))
        o.append(taper(T([(500, 280), (420, 270), (340, 280)]), 4 * s, 1, PAPER))
    return ''.join(o)

# ---- 8 the door opens: the clerk in close profile, mother and father small against the window light
def p_reveal():
    W, Hh = 1600, 1050
    r = random.Random(82)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1600, 760), -0.04, 26, 1.2, 3.6, INK, .5, r))
    o.append(poly([(0, 0), (700, 0), (700, 150), (0, 300)], INK, 20, 3) + rows((0, 0, 700, 300), -0.2, 18, 1, 2.6, PAPER, .55, r, D([(0, 0), (700, 0), (700, 150), (0, 300)])))
    win = [(700, 150), (1110, 130), (1120, 760), (710, 770)]
    o.append(layer(.2, poly([(680, 130), (1130, 110), (1140, 780), (690, 790)], INK, 14, 2) + poly(win, PAPER, 16, 2) + rows((700, 130, 1120, 770), 0.02, 16, 1, 2.4, INK, .62, r, D(win))
                   + taper([(905, 140), (910, 765)], 12, 12) + taper([(705, 420), (1115, 410)], 12, 12)))
    # the mother sinking into her skirts, the father with fists raised: black against the light
    momJ = pose(820, 770, .62, 1, head=(50, -330), neck=(16, -370), ls=(-48, -350), rs=(44, -340), le=(-50, -250), lh=(10, -200),
                re=(70, -250), rh=(40, -200), lp=(-30, -160), rp=(30, -160), lk=None, rk=None, lf=None, rf=None)
    faJ = pose(1010, 770, .64, 1, ls=(-66, -515), rs=(64, -515), le=(-120, -400), lh=(-70, -480), re=(124, -390), rh=(150, -490),
               lp=(-36, -320), rp=(36, -320), lk=(-62, -160), lf=(-86, 0), rk=(62, -160), rf=(86, 0))
    o.append(layer(.2, fig(momJ, .62, 1, skirt=(770, 140), bun=True, r=r, rims=False) + fig(faJ, .64, 1, coat=(700, 24), moust=True, r=r, rims=False)))
    floor = [(0, 760), (1600, 740), (1600, 1050), (0, 1050)]
    o.append(poly(floor, INK, 20, 3) + rows((0, 740, 1600, 1050), -0.03, 18, 1.2, 3.6, PAPER, .5, r, D(floor)))
    # the doorway of Gregor's room, his head and shell leaning out
    o.append(poly([(1250, 60), (1600, 30), (1600, 1050), (1250, 1050)], INK, 18, 3))
    bug = insect_top(r)
    o.append(layer(.05, f'<g transform="translate(1800 560) rotate(192) scale(.95)">{bug}</g>'))
    o.append(poly([(1225, 50), (1270, 50), (1282, 1050), (1238, 1050)], PAPER, 12, 2))
    # the chief clerk, close, recoiling with his hand at his mouth
    cl = []
    coat = [(300, 560), (480, 552), (580, 610), (700, 720), (760, 1050), (120, 1050), (170, 720), (250, 610)]
    cl.append(poly(coat, INK, 14, 2.4) + rows((120, 540, 760, 1050), 1.3, 26, 1.2, 3.4, PAPER, .55, r, D(coat)))
    cl.append(poly([(468, 556), (520, 600), (470, 640), (440, 600)], PAPER, 6, 1))
    cl.append(profile(410, 420, 1.0, 1, hat='bowler', moust=False, r=r))
    cl.append(taper([(720, 900), (660, 640), (600, 520)], 84, 58))
    cl.append(poly([(540, 418), (602, 404), (628, 452), (612, 512), (556, 522), (530, 482)], INK, 8, 1.2))
    for k in range(4):
        y = 420 + k * 22
        cl.append(taper([(600, y + 4), (550, y - 6), (515, y - 14)], 22 - k * 2, 13, INK))
        cl.append(taper([(596, y + 2), (548, y - 8)], 3, .6, PAPER))
    cl.append(taper([(640, 560), (690, 700)], 1, 5, PAPER))
    o.append(layer(.06, f'<g transform="translate(-60 0)">{"".join(cl)}</g>'))
    panel('reveal', W, Hh, 'h1', 'The door is open. Close in the foreground, the chief clerk in a bowler hat, eyes wide, presses his hand to his mouth and backs away. Behind him, against the window light, the mother sinks into her skirts and the father raises his fists. At right, Gregor’s head and shell lean out of the dark doorway.',
          ''.join(o), [
              ('burst', '“Oh!”', 'l:36%;t:5%', 'l:44%;t:4%'),
              ('cap', 'his hand pressed against his open mouth and slowly retreating as if driven by a steady and invisible force.', 'l:4%;b:5%;w:20em', 'l:4%;b:4%'),
          ])

# ---- 16 Grete strikes the table
def p_sister():
    W, Hh = 1400, 1200
    r = random.Random(162)
    o = [paper_rect(W, Hh, PAPER)]
    o.append(rows((0, 0, 1400, 820), 1.57, 16, 1, 3, INK, .5, r))
    for sd in (-1, 1):
        dark = [(0, 0), (380, 0), (0, 700)] if sd < 0 else [(1400, 0), (1000, 0), (1400, 640)]
        o.append(poly(dark, INK, 18, 3))
    o.append(taper([(630, 0), (630, 60)], 10, 10) + poly(ellipse_pts(630, 80, 70, 34, 20, math.pi, 2 * math.pi), INK, 8, 1.5))
    # the father at the right edge, in his uniform cap, turned toward her
    fa = poly([(1180, 560), (1400, 540), (1400, 820), (1120, 820)], INK, 12, 2) + profile(1300, 420, .82, -1, hat='cap', moust=True, r=r)
    o.append(layer(.2, fa))
    # Grete in profile, close
    g = []
    dress = [(330, 500), (500, 520), (620, 600), (680, 820), (200, 820), (240, 610)]
    g.append(poly(dress, INK, 14, 2.4) + rows((200, 500, 680, 820), 1.4, 24, 1, 3, PAPER, .55, r, D(dress)))
    g.append(profile(420, 400, .9, 1, bun=True, r=r))
    g.append(taper([(560, 580), (720, 650), (860, 790)], 74, 46))
    g.append(poly([(820, 770), (960, 760), (1000, 800), (830, 815)], INK, 8, 1.2))
    for k in range(4):
        g.append(taper([(950, 768 + k * 9), (1010, 772 + k * 9)], 12, 8, INK))
    g.append(taper([(600, 590), (760, 680), (850, 770)], 1, 6, PAPER))
    o.append(layer(.06, ''.join(g)))
    table = [(0, 800), (1400, 790), (1400, 1200), (0, 1200)]
    o.append(poly(table, INK, 20, 3) + rows((0, 820, 1400, 1200), 0.0, 18, 1.2, 3.2, PAPER, .55, r, D(table)))
    # plates left by the gentlemen, and the blow
    for x, y in ((260, 900), (520, 950), (1150, 920)):
        o.append(poly(ellipse_pts(x, y, 90, 26, 24), PAPER, 8, 1.4) + poly(ellipse_pts(x, y, 54, 14, 18), INK, 6, 1))
    o.append(''.join(gouge(900 + math.cos(a) * 70, 810 + math.sin(a) * 30, a, r.uniform(50, 130), 6, PAPER, r=r) for a in [i * .45 + .1 for i in range(8)]))
    o.append(poly([(820, 770), (960, 760), (1000, 800), (830, 815)], INK, 8, 1.2))
    panel('sister', W, Hh, 'h2', 'Under the lamp, Grete in close profile brings her hand down flat on the table among the gentlemen’s plates. At the right edge, her father in his uniform cap turns to her.',
          ''.join(o), [
              ('say', '“We have to try and get rid of it”', 'l:6%;t:7%', 'l:5%;t:5%', 'tail-b'),
          ])
for fn in (p_title, p_morning, p_belly, p_insect, p_clock, p_door, p_key, p_reveal, p_father,
           'II', p_milk, p_picture, p_apples, 'III', p_violin, p_drawn, p_lodgers, p_sister, p_dawn, p_char, p_tram, p_stretch):
    if isinstance(fn, str):
        PANELS.append(dict(gutter=fn))
    else:
        fn()

# ---------------------------------------------------------------- page
def pos(spec):
    m = {'l': 'left', 'r': 'right', 't': 'top', 'b': 'bottom', 'w': 'max-width'}
    out = []
    for kv in spec.split(';'):
        k, v = kv.split(':')
        out.append(f'--{m[k]}:{v}')
    return ';'.join(out)

def pos_m(spec):
    m = {'l': 'left', 'r': 'right', 't': 'top', 'b': 'bottom', 'w': 'max-width'}
    def adj(k, v):
        if k == 'b' and v.endswith('%'):
            return f'calc({v} + 30px)'
        return v
    return ';'.join(f'--m{m[k]}:{adj(k, v)}' for k, v in (kv.split(':') for kv in spec.split(';')))

def cap_html(c):
    kind, text, dpos, mpos = c[:4]
    tail = c[4] if len(c) > 4 else ''
    return f'<p class="{kind} {tail}" style="{pos(dpos)};{pos_m(mpos)}">{H.escape(text)}</p>'

# scene choreography: how each scene arrives, how long it holds, where the camera pushes in
SCENE = {
    'title':   dict(tr='none',  len=1.0),
    'morning': dict(tr='ink',   len=1.3, o='50% 45%'),
    'belly':   dict(tr='zoom',  len=1.4, o='38% 66%'),          # push into the hump under the quilt
    'insect':  dict(tr='wipe',  len=1.4),
    'clock':   dict(tr='black', len=1.2),
    'voices':  dict(tr='wipe',  len=1.5),
    'key':     dict(tr='ink',   len=1.3, o='66% 50%'),
    'reveal':  dict(tr='zoom',  len=1.4, o='61% 46%', pf='xMinYMid slice'),   # push through the keyhole
    'father':  dict(tr='wipe',  len=1.3),
    'II':      dict(tr='black', len=.8),
    'milk':    dict(tr='ray',   len=1.3, o='15% 10%', pf='xMinYMid slice'),
    'picture': dict(tr='ink',   len=1.3, o='62% 30%'),
    'apples':  dict(tr='wipe',  len=1.6),
    'III':     dict(tr='black', len=.8),
    'violin':  dict(tr='ray',   len=1.3, o='50% 0%'),
    'drawn':   dict(tr='zoom',  len=1.3, o='22% 70%'),
    'lodgers': dict(tr='wipe',  len=1.3),
    'sister':  dict(tr='ink',   len=1.3, o='60% 70%', pf='xMinYMid slice'),
    'dawn':    dict(tr='black', len=1.5),
    'char':    dict(tr='ray',   len=1.3, o='50% 0%'),
    'tram':    dict(tr='ink',   len=1.3, o='74% 32%'),
    'stretch': dict(tr='ray',   len=1.4, o='50% 33%'),
}

parts = []
for P in PANELS:
    if 'gutter' in P:
        g = P['gutter']
        sc = SCENE[g]
        label = {'II': 'Part two', 'III': 'Part three'}[g]
        parts.append(f'<section class="scene card" id="p-{g}" data-tr="{sc["tr"]}" data-len="{sc["len"]}">'
                     f'<h2><span aria-hidden="true">{g}</span><span class="sr">{label}</span></h2></section>')
        continue
    sc = SCENE[P['id']]
    caps = ''.join(cap_html(c) for c in P['caps'])
    extra = ''
    if P['id'] == 'title':
        extra = '<h1 class="title"><span class="t1">The Metamorphosis</span><span class="t2">Franz Kafka · 1915</span></h1>'
    attrs = f'data-tr="{sc["tr"]}" data-len="{sc["len"]}"' + (f' data-o="{sc["o"]}"' if 'o' in sc else '') + (f' data-pf="{sc["pf"]}"' if 'pf' in sc else '')
    parts.append(f'<section class="scene" id="p-{P["id"]}" {attrs} style="--bg:{P["bg"]};--ar:{P["W"]}/{P["H"]}">{extra}'
                 f'<div class="art-wrap">{svg(P["W"], P["H"], P["art"], P["label"], P["fx"])}</div>'
                 f'{"<div class=caps>" + caps + "</div>" if caps else ""}</section>')

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<filter id="carve" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="4"/>
<feDisplacementMap in="SourceGraphic" scale="7" xChannelSelector="R" yChannelSelector="G"/></filter>
</defs></svg>'''

TEMPLATE = open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'template.html')).read()
page = TEMPLATE.replace('{{DEFS}}', DEFS).replace('{{PANELS}}', '\n'.join(parts))
open(OUT, 'w').write(page)
import shutil, os
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stage.js'), os.path.join(os.path.dirname(OUT), 'stage.js'))
print('bytes', len(page))
