"""Parametric mesh builders for Ply's new line (all units in mm).

Shapes are drawn from scratch: superellipse/round outlines, Ply's Quilt
(diagonal pillows) and Tile (soft square grid) textures.
"""
import numpy as np

# ---------------------------------------------------------------- outlines

def outline(a, b, n=2.0, M=720, res=8000):
    """Closed outline (half-sizes a, b, superellipse exponent n; n=2 ellipse),
    resampled at equal arc length. Returns points (M,2), outward normals (M,2),
    perimeter."""
    th = np.linspace(0, 2 * np.pi, res, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    x = a * np.sign(c) * np.abs(c) ** (2.0 / n)
    y = b * np.sign(s) * np.abs(s) ** (2.0 / n)
    P = np.stack([x, y], 1)
    seg = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    per = cum[-1]
    t = np.linspace(0, per, M, endpoint=False)
    Pc = np.vstack([P, P[:1]])
    xs = np.interp(t, cum, Pc[:, 0])
    ys = np.interp(t, cum, Pc[:, 1])
    Q = np.stack([xs, ys], 1)
    T = np.roll(Q, -1, 0) - np.roll(Q, 1, 0)
    Nrm = np.stack([T[:, 1], -T[:, 0]], 1)
    Nrm /= np.linalg.norm(Nrm, axis=1, keepdims=True)
    return Q, Nrm, per

# ---------------------------------------------------------------- textures

def _g(x, k, e):
    return np.clip(1 - np.abs(2 * x) ** k, 0, 1) ** e

def tex_quilt(U, V):
    p, q = U + V, U - V
    fp, fq = p - np.floor(p) - 0.5, q - np.floor(q) - 0.5
    return _g(fp, 2.4, 0.55) * _g(fq, 2.4, 0.55)

def tex_tile(U, V):
    fp, fq = U - np.floor(U) - 0.5, V - np.floor(V) - 0.5
    return _g(fp, 7, 0.32) * _g(fq, 7, 0.32)

def tex_rib(U, V):
    fu = U - np.floor(U) - 0.5
    return _g(fu, 2.0, 0.6) + 0 * V

TEX = {'quilt': tex_quilt, 'tile': tex_tile, 'rib': tex_rib}

def ring_frame(a, b, n=2.0, width=6.0, z0=0.0, h=3.0, M=720, mesh=None):
    """Closed flat ring (frame) following an outline: outer edge at (a,b), inner edge `width` inside."""
    mesh = mesh or Mesh()
    P, Nn, per = outline(a, b, n, M)
    def r(off, z):
        return np.column_stack([P[:, 0] + Nn[:, 0] * off, P[:, 1] + Nn[:, 1] * off, np.full(M, z0 + z)])
    rr = 0.8
    rings = [r(0, 0), r(0, h - rr), r(-rr * 0.3, h - rr * 0.3), r(-rr, h), r(-width + rr, h),
             r(-width + rr * 0.3, h - rr * 0.3), r(-width, h - rr), r(-width, 0)]
    ids = [mesh.ring(x) for x in rings]
    for i in range(len(ids)):
        mesh.bridge(ids[i], ids[(i + 1) % len(ids)])
    return mesh

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

# ---------------------------------------------------------------- mesh glue

class Mesh:
    def __init__(self):
        self.v = []
        self.f = []
        self.n = 0

    def ring(self, pts):
        idx = np.arange(self.n, self.n + len(pts))
        self.v.append(np.asarray(pts, float))
        self.n += len(pts)
        return idx

    def point(self, p):
        return self.ring(np.asarray([p], float))[0]

    def bridge(self, r0, r1):
        M = len(r0)
        for i in range(M):
            j = (i + 1) % M
            self.f.append((r0[i], r0[j], r1[j], r1[i]))

    def fan(self, c, r, flip=False):
        M = len(r)
        for i in range(M):
            j = (i + 1) % M
            self.f.append((c, r[j], r[i]) if flip else (c, r[i], r[j]))

    def arrays(self):
        return np.vstack(self.v), self.f

def chain(mesh, rings, start_center=None, end_center=None):
    ids = [mesh.ring(r) for r in rings]
    for a, b in zip(ids[:-1], ids[1:]):
        mesh.bridge(a, b)
    if start_center is not None:
        mesh.fan(mesh.point(start_center), ids[0], flip=True)
    if end_center is not None:
        mesh.fan(mesh.point(end_center), ids[-1])
    return ids

# ---------------------------------------------------------------- pieces

def vessel(a, b, H, n=2.0, wall=2.4, floor=2.4, tex=None, band=None,
           cell=18.0, amp=1.6, taper=0.0, M=720, dz=0.45, rb=2.0,
           floor_tex=None, floor_h=2.6, floor_cell=14.0, z0=0.0,
           mesh=None):
    """Open-top vessel. tex/band: wall texture between band=(zlo,zhi).
    floor_tex: None | 'quilt' | 'tile' | 'ribs' raised pattern on the inner floor."""
    mesh = mesh or Mesh()
    P, Nn, per = outline(a, b, n, M)
    u = np.arange(M) / M
    plain = amp * 0.85 if tex else 0.0
    if tex:
        ncell = max(6, int(round(per / cell)))
        lo, hi = band
        nrow = max(1, int(round((hi - lo) / (per / ncell))))
        ch = (hi - lo) / nrow
        f = TEX[tex]

    def scale(z):
        return 1.0 - taper * (1 - z / H)

    def disp(z):
        if not tex:
            return np.zeros(M)
        w = smoothstep(lo - 0.2, lo + 1.4, z) * (1 - smoothstep(hi - 1.4, hi + 0.2, z))
        U = u * ncell
        V = (z - lo) / ch
        return amp * (w * f(U, V)) + plain * (1 - w)

    def outer(z, extra=0.0):
        s = scale(z)
        d = disp(z) + extra
        return np.column_stack([P[:, 0] * s + Nn[:, 0] * d, P[:, 1] * s + Nn[:, 1] * d,
                                np.full(M, z + z0)])

    def inner(z, extra=0.0):
        s = scale(z)
        d = -wall + extra
        return np.column_stack([P[:, 0] * s + Nn[:, 0] * d, P[:, 1] * s + Nn[:, 1] * d,
                                np.full(M, z + z0)])

    rings = []
    # outer wall, bottom rounding
    zs = np.unique(np.concatenate([np.linspace(0, rb, 8), np.arange(rb, H - 0.8, dz), [H - 0.8]]))
    for z in zs:
        ins = rb - np.sqrt(max(rb ** 2 - (rb - z) ** 2, 0)) if z < rb else 0.0
        rings.append(outer(z, -ins))
    # soft rim
    rings.append(outer(H - 0.25, -0.25))
    rings.append(outer(H, -0.8))
    rings.append(inner(H, 0.6))
    rings.append(inner(H - 0.25, 0.2))
    # inner wall down to floor, with fillet
    ri = 3.0
    zin = np.unique(np.concatenate([np.arange(H - 0.8, floor + ri, -1.2), np.linspace(floor + ri, floor, 8)]))[::-1]
    for z in zin:
        ins = ri - np.sqrt(max(ri ** 2 - (z - floor - ri) ** 2, 0)) if z < floor + ri else 0.0
        rings.append(inner(z, -ins))
    # inner floor (flat or textured heightfield in outline coordinates)
    s = scale(floor)
    edge = np.column_stack([P[:, 0] * s + Nn[:, 0] * (-wall - ri), P[:, 1] * s + Nn[:, 1] * (-wall - ri)])
    ts = np.linspace(1, 0, 70)[1:-1]
    for t in ts:
        xy = edge * t
        h = np.zeros(M)
        if floor_tex:
            m = 1 - smoothstep(0.82, 0.97, t)
            X, Y = xy[:, 0] / floor_cell, xy[:, 1] / floor_cell
            if floor_tex == 'rings':
                rr_ = np.hypot(xy[:, 0], xy[:, 1]) / floor_cell
                h = floor_h * _g(rr_ - np.floor(rr_) - 0.5, 4, 0.5) * m * smoothstep(0.6, 1.0, rr_)
            elif floor_tex == 'ribs':
                fy = Y - np.floor(Y) - 0.5
                hh = _g(fy, 4, 0.5)
                xmax = np.abs(edge[:, 0]).max()
                lim = 1 - smoothstep(xmax - 18, xmax - 9, np.abs(xy[:, 0]))
                h = floor_h * hh * m * lim
            else:
                h = floor_h * TEX[floor_tex](X, Y) * m
        rings.append(np.column_stack([xy, floor + h + z0]))
    centre_h = floor
    if floor_tex in ('quilt', 'tile'):
        centre_h += floor_h * float(TEX[floor_tex](np.array([0.0]), np.array([0.0]))[0])
    elif floor_tex == 'ribs':
        centre_h += floor_h * float(_g(np.array([-0.5]), 4, 0.5)[0])
    chain(mesh, rings, start_center=(0, 0, z0), end_center=(0, 0, centre_h + z0))
    return mesh

def lid(a, b, n=2.0, z0=0.0, h=8.0, dome=0.0, M=720, tex=None, cell=14.0, amp=1.2,
        knob=False, grip=False, mesh=None, top_tex_r=0.78, grip_pitch=3.2, grip_depth=0.6, rim=1.5):
    """Lid sitting at z0. Optional dome, textured top (quilt/tile heightfield), grip ribs on edge."""
    mesh = mesh or Mesh()
    P, Nn, per = outline(a, b, n, M)
    u = np.arange(M) / M
    rings = []
    def side(z, extra=0.0):
        d = extra
        if grip:
            fu = u * int(per / grip_pitch)
            d = d + grip_depth * _g(fu - np.floor(fu) - 0.5, 2.0, 0.6)
        return np.column_stack([P[:, 0] + Nn[:, 0] * d, P[:, 1] + Nn[:, 1] * d, np.full(M, z0 + z)])
    zs = np.linspace(0, h - rim, 12)
    for i, z in enumerate(zs):
        ins = 0.6 if i == 0 else 0.0
        rings.append(side(z, -ins))
    # rounded top edge
    for k in np.linspace(0, np.pi / 2, 7)[1:]:
        r = rim
        rings.append(side(h - rim + r * np.sin(k), -r * (1 - np.cos(k))))
    ts = np.linspace(1, 0, 60)[1:-1]
    for t in ts:
        xy = (P + Nn * -rim) * t
        if dome < 0:
            # dish: flat rim ring, smooth bowl inside
            tt = np.clip((t - 0.0) / 0.86, 0, 1)
            z = h + dome * (1 - smoothstep(0.55, 1.0, tt)) if False else h + dome * (1 - tt ** 2.2)
        else:
            z = h + dome * (1 - t ** 2)
        hh = np.zeros(M)
        if tex:
            m = 1 - smoothstep(top_tex_r - 0.1, top_tex_r, t)
            hh = amp * TEX[tex](xy[:, 0] / cell, xy[:, 1] / cell) * m
        rings.append(np.column_stack([xy, np.full(M, z0) + z + hh]))
    top_c = h + dome
    if tex:
        top_c += amp * float(TEX[tex](np.array([0.0]), np.array([0.0]))[0])
    chain(mesh, rings, start_center=(0, 0, z0 + 0.0), end_center=(0, 0, z0 + top_c))
    if knob:
        knob_mesh(mesh, z0 + top_c - 0.5, r=knob if isinstance(knob, float) else 7.0)
    return mesh

def knob_mesh(mesh, zb, r=7.0, M=120):
    th = np.linspace(0, 2 * np.pi, M, endpoint=False)
    rings = []
    prof = [(0.75, 0.0), (0.78, 0.25), (0.92, 0.55), (1.0, 0.75), (0.96, 0.92), (0.8, 1.0)]
    for rr, zz in prof:
        rings.append(np.column_stack([r * rr * np.cos(th), r * rr * np.sin(th), np.full(M, zb + zz * r * 0.9)]))
    chain(mesh, rings, start_center=(0, 0, zb), end_center=(0, 0, zb + r * 0.92))
    return mesh

def volume(verts, faces):
    v = verts
    vol = 0.0
    for f in faces:
        a = v[f[0]]
        for i in range(1, len(f) - 1):
            b, c = v[f[i]], v[f[i + 1]]
            vol += np.dot(a, np.cross(b, c)) / 6.0
    return abs(vol)
