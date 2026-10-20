"""Render one design-option shot with Blender (bpy). Usage: python render.py <shot> [size] [samples]"""
import sys, math, random, json
from pathlib import Path
import numpy as np
import bpy, bmesh
sys.path.insert(0, str(Path(__file__).parent))
import geom as G

OUT = Path(__file__).resolve().parent.parent / 'renders'
OUT.mkdir(exist_ok=True)
MM = 0.001
import os
VT = os.environ.get('VT', 'AgX')
EXPO = float(os.environ.get('EXPO', '-1.6'))
BG = tuple(int(x) for x in os.environ.get('BG', '220,211,196').split(','))
SUFFIX = os.environ.get('SUFFIX', '')

def lin(c):
    c = np.array(c) / 255.0
    return tuple(np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)) + (1.0,)

COL = {
    'ivory': (252, 246, 232), 'charcoal': (60, 58, 55), 'green': (60, 78, 62), 'tan': (206, 179, 139),
    'soap_clay': (222, 186, 165), 'soap_white': (214, 210, 214), 'leaf': (104, 138, 116), 'soil': (52, 42, 36),
    'pebble': (235, 232, 226), 'gold': (212, 175, 105),
}
_mats = {}

def mat(name, rough=0.58, sheen=0.0):
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(COL[name])
    b.inputs['Roughness'].default_value = rough
    try:
        b.inputs['Specular IOR Level'].default_value = 0.35
    except KeyError:
        pass
    _mats[name] = m
    return m

def add_mesh(mesh, name, material, smooth=True):
    v, f = mesh.arrays()
    me = bpy.data.meshes.new(name)
    me.from_pydata((v * MM).tolist(), [], [list(map(int, x)) for x in f])
    me.update()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat(material))
    return ob, G.volume(v, f)

def move(ob, x=0, y=0, z=0, rz=0):
    ob.location = (x * MM, y * MM, z * MM)
    ob.rotation_euler[2] = math.radians(rz)

def soap(x, y, z, colour, L=78, W=50, T=20, rz=0, ry=0):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.active_object
    ob.scale = (L * MM, W * MM, T * MM)
    mod = ob.modifiers.new('bev', 'BEVEL'); mod.width = 8 * MM; mod.segments = 8; mod.limit_method = 'NONE'
    bpy.ops.object.shade_smooth()
    ob.location = (x * MM, y * MM, (z + T / 2) * MM)
    ob.rotation_euler[2] = math.radians(rz)
    ob.rotation_euler[1] = math.radians(ry)
    ob.data.materials.append(mat(colour, rough=0.75))
    return ob

def succulent(x, y, z, scale=1.0, seed=1):
    rnd = random.Random(seed)
    layers = [(10, 21, 18), (8, 15, 42), (6, 9, 66), (4, 5, 80)]
    for li, (count, L, tilt) in enumerate(layers):
        for k in range(count):
            yaw = 360.0 * k / count + li * 17 + rnd.uniform(-6, 6)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1)
            ob = bpy.context.active_object
            me = ob.data
            for vtx in me.vertices:
                px, py, pz = vtx.co
                taper = 1.0 - 0.75 * max(px, 0) ** 1.5
                vtx.co = ((px + 1) / 2 * L * scale, py * 0.22 * L * scale * taper, pz * 0.09 * L * scale * taper)
            bpy.ops.object.shade_smooth()
            ob.scale = (MM, MM, MM)
            ob.rotation_euler = (0, -math.radians(tilt + rnd.uniform(-5, 5)), math.radians(yaw))
            ob.location = (x * MM, y * MM, (z + li * 1.2 * scale) * MM)
            ob.data.materials.append(mat('leaf', rough=0.45))

def soil(x, y, z, r, seed=3):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r * MM, depth=2 * MM, location=(x * MM, y * MM, (z - 1) * MM))
    bpy.context.active_object.data.materials.append(mat('soil', rough=0.95))
    rnd = random.Random(seed)
    for _ in range(int(r * 0.9)):
        a, d = rnd.uniform(0, 2 * math.pi), r * math.sqrt(rnd.uniform(0.15, 0.85))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rnd.uniform(0.5, 0.9) * MM,
                                              location=((x + d * math.cos(a)) * MM, (y + d * math.sin(a)) * MM, (z + 0.2) * MM))
        bpy.context.active_object.data.materials.append(mat('pebble', rough=0.8))

# ------------------------------------------------------------------ shots
VOL = {}

def shot_tray_a():
    o, v = add_mesh(G.vessel(65, 45, 22, n=2, tex='quilt', band=(3.5, 18.5), cell=9, amp=1.15,
                             floor_tex='ribs', floor_cell=8, floor_h=2.4), 'tray', 'ivory')
    VOL['tray'] = v
    soap(18, 4, 2.4 + 2.4, 'soap_clay', L=56, W=38, T=16, rz=-14)
    return dict(elev=42, az=-28, target=(0, 0, 10))

def shot_tray_b():
    o, v = add_mesh(G.vessel(65, 47.5, 15, n=5, wall=2.6, floor_tex='tile', floor_cell=13, floor_h=2.8), 'tray', 'charcoal')
    VOL['tray'] = v
    soap(-20, -2, 2.4 + 2.8, 'soap_white', L=56, W=38, T=16, rz=12)
    return dict(elev=38, az=-30, target=(0, 0, 10))

def shot_tray_c():
    o, v = add_mesh(G.vessel(57.5, 57.5, 26, n=2, tex='tile', band=(3.5, 22.5), cell=9.5, amp=1.0), 'tray', 'green')
    VOL['tray'] = v
    return dict(elev=34, az=-25, target=(0, 0, 13))

def _stack(heights, a, b, n, tex, cell, amp, colour, dome, knob_r):
    z = 0.0
    tot = 0.0
    for i, h in enumerate(heights):
        o, v = add_mesh(G.vessel(a, b, h, n=n, tex=tex, band=(4, h - 4), cell=cell, amp=amp, z0=z), f'tier{i}', colour)
        tot += v
        z += h + 0.7
    plain = amp * 0.85
    o, v = add_mesh(G.lid(a + plain, b + plain, n=n, z0=z, h=8, dome=dome, knob=knob_r), 'lid', colour)
    VOL['tiers'] = tot; VOL['lid'] = v
    return z + 8 + dome + knob_r

def shot_stack_a():
    top = _stack([42, 42, 42], 45, 45, 2, 'quilt', 11, 1.25, 'tan', 6, 7.0)
    return dict(elev=18, az=-30, target=(0, 0, top / 2))

def shot_stack_b():
    top = _stack([40, 40, 40], 44, 44, 4, 'tile', 15, 1.2, 'ivory', 0, 6.0)
    return dict(elev=18, az=-35, target=(0, 0, top / 2))

def shot_stack_c():
    top = _stack([56, 40, 28], 47.5, 47.5, 2, 'tile', 12, 1.45, 'green', 7, 7.0)
    return dict(elev=18, az=-30, target=(0, 0, top / 2))

def _pot(x, a, b, n, H, tex, cell, colour, lid_kw, rz=0):
    amp = 1.2
    m = G.vessel(a, b, H, n=n, wall=2.0, floor=2.0, tex=tex, band=(4, H - 4) if tex else None, cell=cell, amp=amp)
    o, v = add_mesh(m, 'pot', colour); move(o, x, 0, 0, rz)
    plain = amp * 0.85 if tex else 0.0
    l, lv = add_mesh(G.lid(a + plain + 0.2, b + plain + 0.2, n=n, z0=H + 0.6, **lid_kw), 'potlid', colour)
    move(l, x, 0, 0, rz)
    VOL['pot'] = v; VOL['potlid'] = lv

def shot_pots_a():
    for x, c in ((-36, 'ivory'), (36, 'green')):
        _pot(x, 29, 29, 2, 46, 'quilt', 13, c, dict(h=13, grip=True))
    return dict(elev=22, az=-20, target=(0, 0, 30))

def shot_pots_b():
    for x, c in ((-36, 'charcoal'), (36, 'tan')):
        _pot(x, 29, 29, 2, 46, 'tile', 12, c, dict(h=12))
    return dict(elev=22, az=-20, target=(0, 0, 30))

def shot_pots_c():
    for x, c, rz in ((-40, 'ivory', 15), (40, 'tan', -10)):
        _pot(x, 33, 26, 2.6, 40, None, 12, c, dict(h=12, dome=2.5, tex='quilt', cell=10, amp=1.1), rz=rz)
    return dict(elev=30, az=-20, target=(0, 0, 26))

def _trio(texs, a, b, n, H, colour, tray):
    ta, tb, tn, th = tray
    o, v = add_mesh(G.vessel(ta, tb, th, n=tn, wall=2.2, floor=2.2), 'trioTray', colour)
    VOL['trioTray'] = v
    xs = (-(2 * a + 5), 0, 2 * a + 5)
    tot = 0
    for i, (x, t) in enumerate(zip(xs, texs)):
        amp = 1.1
        m = G.vessel(a, b, H, n=n, wall=2.0, floor=2.0, tex=t, band=(4, H - 4) if t else None, cell=12, amp=amp, z0=2.4)
        o, v = add_mesh(m, f'mini{i}', colour); move(o, x, 0, 0)
        tot += v
        soil(x, 0, 2.4 + H - 7, min(a, b) - 2.2, seed=i + 5)
        succulent(x, 0, 2.4 + H - 7.5, scale=0.95, seed=i + 1)
    VOL['minis'] = tot
    return dict(elev=24, az=-18, target=(0, 0, 32))

def shot_trio_a():
    return _trio(('quilt', 'tile', None), 28, 28, 2, 52, 'tan', (106, 40, 2, 11))

def shot_trio_b():
    return _trio(('quilt', 'quilt', 'quilt'), 28, 28, 2, 52, 'green', (106, 39, 4, 10))

def shot_trio_c():
    return _trio(('tile', 'tile', 'tile'), 27, 27, 4, 50, 'charcoal', (103, 38, 4, 10))

# ---- minimal ribbed series (Ply's own shapes)
def bar(x, y, z, L, W, T, colour):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.active_object
    ob.scale = (W * MM, L * MM, T * MM)
    mod = ob.modifiers.new('bev', 'BEVEL'); mod.width = min(W, T) * 0.45 * MM; mod.segments = 6; mod.limit_method = 'NONE'
    bpy.ops.object.shade_smooth()
    ob.location = (x * MM, y * MM, (z + T / 2) * MM)
    ob.data.materials.append(mat(colour))
    return ob

def shot_m_tray_a():
    o, v = add_mesh(G.vessel(56, 56, 20, n=2, wall=2.4, tex='rib', band=(1.6, 18.6), cell=3.6, amp=0.9,
                             floor_tex='rings', floor_cell=7.5, floor_h=2.0), 'tray', 'ivory')
    VOL['tray'] = v
    soap(6, 4, 2.4 + 2.0, 'soap_clay', L=58, W=40, T=17, rz=-18)
    return dict(elev=40, az=-26, target=(0, 0, 9))

def shot_m_tray_b():
    o, v = add_mesh(G.vessel(61, 43, 18, n=4.5, wall=2.4, tex='rib', band=(1.6, 16.6), cell=3.6, amp=0.9,
                             floor_tex='ribs', floor_cell=8, floor_h=2.2), 'tray', 'charcoal')
    VOL['tray'] = v
    soap(-14, -2, 2.4 + 2.2, 'soap_white', L=58, W=40, T=17, rz=8)
    return dict(elev=40, az=-28, target=(0, 0, 9))

def shot_m_tray_c():
    a, b, H = 62, 42, 22
    o, v = add_mesh(G.vessel(a, b, H, n=2, wall=2.4, tex='rib', band=(1.6, H - 1.4), cell=3.6, amp=0.9), 'base', 'tan')
    plain = 0.9 * 0.85
    # draining top: frame + slats resting just below the rim
    zt = H - 5.5
    ai, bi = a - 2.4 - 0.4, b - 2.4 - 0.4
    f, fv = add_mesh(G.ring_frame(ai, bi, 2, width=5.0, z0=zt, h=3.2), 'frame', 'tan')
    xs = np.arange(-ai + 9, ai - 8, 6.2)
    for x in xs:
        half = (bi - 1.5) * math.sqrt(max(1 - (x / (ai - 1.5)) ** 2, 0))
        if half > 4:
            bar(x, 0, zt, 2 * half, 3.4, 3.2, 'tan')
    VOL['tray'] = v
    soap(10, 2, zt + 3.2, 'soap_clay', L=58, W=40, T=17, rz=-10)
    return dict(elev=40, az=-26, target=(0, 0, 11))

# ---- slatted soap rests (fins joined by low cross-ties, no rim)
def fin(xs, ztop, y0, t, colour, bev=0.7):
    n = len(xs)
    verts = []
    for y in (y0, y0 + t):
        for x, z in zip(xs, ztop):
            verts.append((x * MM, y * MM, z * MM))
        for x in xs[::-1]:
            verts.append((x * MM, y * MM, 0.0))
    m = 2 * n
    faces = [list(range(m))[::-1], list(range(m, 2 * m))]
    for i in range(m):
        j = (i + 1) % m
        faces.append([i, j, m + j, m + i])
    me = bpy.data.meshes.new('fin'); me.from_pydata(verts, [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('fin', me); bpy.context.collection.objects.link(ob)
    mod = ob.modifiers.new('bev', 'BEVEL'); mod.width = bev * MM; mod.segments = 4; mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(25)
    ob.data.materials.append(mat(colour))
    return ob

def tie(x, y0, y1, z, r, colour):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r * MM, depth=(y1 - y0) * MM,
                                        location=(x * MM, (y0 + y1) / 2 * MM, z * MM), rotation=(math.radians(90), 0, 0))
    ob = bpy.context.active_object; bpy.ops.object.shade_smooth(); ob.data.materials.append(mat(colour))

def soap_round(x, y, z, colour, D=70, T=26):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=D / 2 * MM, depth=T * MM, location=(x * MM, y * MM, (z + T / 2) * MM))
    ob = bpy.context.active_object
    mod = ob.modifiers.new('bev', 'BEVEL'); mod.width = 6 * MM; mod.segments = 8; mod.limit_method = 'ANGLE'
    try:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    except Exception:
        bpy.ops.object.shade_smooth()
    ob.data.materials.append(mat(colour, rough=0.8))

def slatted(L, D, H, colour, top='flat', t=2.3, gap=2.7, end_t=2.3, footprint='rect', a=None, b=None, end_r=5.0, dip=4.0):
    pitch = t + gap
    nf = int((D - 2 * end_t) // pitch)
    ys = [-D / 2]
    y = -D / 2 + end_t + gap
    while y + t <= D / 2 - end_t - gap + 0.01:
        ys.append(y); y += pitch
    ys.append(D / 2 - end_t)
    vol = 0.0
    for i, y0 in enumerate(ys):
        tt = end_t if i in (0, len(ys) - 1) else t
        yc = y0 + tt / 2
        if footprint == 'oval':
            k = 1 - (yc / (b)) ** 2
            if k <= 0.05:
                continue
            half = a * math.sqrt(k)
        else:
            half = L / 2
        xs = np.linspace(-half, half, 60)
        if top == 'cradle':
            z = H - dip * (1 - (xs / half) ** 2) * (1 - (yc / (D / 2)) ** 2 * 0.5)
        elif top == 'cascade':
            z = H - 9.0 * (xs + half) / (2 * half)
        else:
            z = np.full_like(xs, H)
        # rounded ends in elevation
        rr = end_r
        edge = np.clip((half - np.abs(xs)) / rr, 0, 1)
        z = np.minimum(z, 2.0 + (z - 2.0) * np.sqrt(1 - (1 - edge) ** 2))
        fin(xs, z, y0, tt, colour)
        vol += np.trapz(z, xs) * tt
    span = (ys[0], ys[-1] + end_t)
    xt = (L / 2 if footprint != 'oval' else a * 0.75) * 0.55
    for x in (-xt, xt):
        if footprint == 'oval':
            yl = b * math.sqrt(max(1 - ((abs(x) + 4) / a) ** 2, 0)) - 3
            tie(x, -yl, yl, 3.2, 1.8, colour)
        else:
            tie(x, span[0] + 0.5, span[1] - 0.5, 3.2, 1.8, colour)
    VOL['soap_rest'] = vol / 1000.0 * 1000

def shot_s_rest_a():
    slatted(116, 84, 28, 'ivory', top='cradle', end_r=16.0, dip=7.0)
    soap_round(4, 0, 21.5, 'soap_clay', D=60, T=22)
    return dict(elev=24, az=-34, target=(0, 0, 18))

def shot_s_rest_b():
    slatted(116, 80, 28, 'tan', top='cascade', end_r=8.0)
    soap(6, 0, 22.4, 'soap_clay', L=60, W=42, T=18, rz=0, ry=math.degrees(math.atan(9 / 116)))
    return dict(elev=24, az=-34, target=(0, 0, 18))

def shot_s_rest_c():
    slatted(120, 84, 24, 'charcoal', top='flat', footprint='oval', a=60, b=44, end_r=10.0)
    soap(0, 0, 24, 'soap_clay', L=60, W=42, T=18, rz=12)
    return dict(elev=28, az=-30, target=(0, 0, 16))

# ---- minimal ribbed stacking pots
def _mstack(heights, a, b, n, colour, taper=0.0, dome=0.0, lid_h=7.0):
    z = 0.0
    tot = 0.0
    amp = 0.9
    for i, h in enumerate(heights):
        o, v = add_mesh(G.vessel(a, b, h, n=n, wall=2.2, floor=2.0, tex='rib', band=(1.8, h - 1.6), cell=3.6,
                                 amp=amp, taper=taper, z0=z), f'tier{i}', colour)
        tot += v
        z += h + 0.8
    plain = amp * 0.85
    o, v = add_mesh(G.lid(a + plain, b + plain, n=n, z0=z, h=lid_h, dome=dome), 'lid', colour)
    VOL['tiers'] = tot; VOL['lid'] = v
    return z + lid_h + dome

def shot_m_stack_a():
    top = _mstack([40, 40, 40], 42, 42, 2, 'ivory', lid_h=7.0, dome=1.5)
    return dict(elev=16, az=-30, target=(0, 0, top / 2))

def shot_m_stack_b():
    top = _mstack([46, 36, 26], 44, 44, 2, 'charcoal', taper=0.06, lid_h=7.0, dome=4.0)
    return dict(elev=16, az=-30, target=(0, 0, top / 2))

def shot_m_stack_c():
    top = _mstack([38, 38, 38], 40, 40, 4.0, 'green', lid_h=7.0, dome=0.0)
    return dict(elev=16, az=-36, target=(0, 0, top / 2))

# ---- minimal ribbed twist-top pots
def _mpot(x, a, b, n, H, colour, lid_h=10.0, dome=0.0, rz=0, body_tex='rib', grip=False):
    amp = 0.75 if body_tex else 0.0
    m = G.vessel(a, b, H, n=n, wall=2.0, floor=2.0, tex=body_tex, band=(1.6, H - 1.4), cell=3.2, amp=amp)
    o, v = add_mesh(m, 'pot', colour); move(o, x, 0, 0, rz)
    plain = amp * 0.85
    l, lv = add_mesh(G.lid(a + plain + 0.15, b + plain + 0.15, n=n, z0=H + 0.7, h=lid_h, dome=dome, grip=grip), 'potlid', colour)
    move(l, x, 0, 0, rz)
    VOL.setdefault('pots', []).append((round(v / 1000, 2), round(lv / 1000, 2)))

def shot_m_pots_a():
    _mpot(-34, 27, 27, 2, 38, 'ivory', lid_h=9)
    _mpot(32, 27, 27, 2, 60, 'tan', lid_h=9)
    return dict(elev=20, az=-18, target=(0, 0, 34))

def shot_m_pots_b():
    _mpot(-34, 27, 27, 2, 32, 'charcoal', lid_h=16, dome=2, body_tex=None, grip=True)
    _mpot(32, 27, 27, 2, 54, 'ivory', lid_h=16, dome=2, body_tex=None, grip=True)
    return dict(elev=20, az=-18, target=(0, 0, 36))

def shot_m_pots_c():
    _mpot(-34, 26, 26, 4.0, 38, 'green', lid_h=9, rz=8)
    _mpot(32, 26, 26, 4.0, 60, 'tan', lid_h=9, rz=-6)
    return dict(elev=20, az=-22, target=(0, 0, 34))

# ---- fine-ribbed canisters with a dish lid
def gold_ring(x, y, z, R=9.0, r=1.1, tilt=0, rz=0):
    bpy.ops.mesh.primitive_torus_add(major_radius=R * MM, minor_radius=r * MM, major_segments=96, minor_segments=24,
                                     location=(x * MM, y * MM, (z + r) * MM), rotation=(math.radians(tilt), 0, math.radians(rz)))
    ob = bpy.context.active_object; bpy.ops.object.shade_smooth()
    m = mat('gold', rough=0.28)
    m.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1.0
    ob.data.materials.append(m)

def _canister(x, a, b, n, H, colour, lid_h=15.0, dish=-8.0, rz=0, rings=True):
    amp = 0.6
    m = G.vessel(a, b, H, n=n, wall=2.0, floor=2.2, tex='rib', band=(5.5, H - 1.2), cell=2.0, amp=amp, rb=5.5, M=1080)
    o, v = add_mesh(m, 'can', colour); move(o, x, 0, 0, rz)
    plain = amp * 0.85
    l, lv = add_mesh(G.lid(a + plain + 0.2, b + plain + 0.2, n=n, z0=H + 0.8, h=lid_h, dome=dish, M=1080,
                           grip=True, grip_pitch=2.0, grip_depth=0.6, rim=1.6), 'canlid', colour)
    move(l, x, 0, 0, rz)
    if rings:
        zc = H + 0.8 + lid_h + dish
        gold_ring(x - 4, -3, zc + 0.6, R=8.5, tilt=10, rz=20)
        gold_ring(x + 6, 4, zc + 1.6, R=8.0, r=0.9, tilt=24, rz=-30)
    VOL.setdefault('cans', []).append((round(v / 1000, 2), round(lv / 1000, 2)))

def shot_m_can_a():
    _canister(0, 33, 33, 2, 92, 'charcoal', lid_h=15, dish=-8)
    return dict(elev=28, az=-20, target=(0, 0, 55))

def shot_m_can_b():
    _canister(0, 40, 40, 2, 50, 'ivory', lid_h=15, dish=-8)
    return dict(elev=30, az=-20, target=(0, 0, 34))

def shot_m_can_c():
    _canister(0, 32, 32, 4.0, 86, 'green', lid_h=15, dish=-8, rz=12)
    return dict(elev=28, az=-24, target=(0, 0, 52))

# ---- fine-ribbed mini planters
def _mini(x, y, a, H, colour, z0=0.0, seed=1, plant=0.85):
    m = G.vessel(a, a, H, n=2, wall=2.0, floor=2.2, tex='rib', band=(5.0, H - 1.2), cell=2.0, amp=0.6, rb=5.0, M=900, z0=z0)
    o, v = add_mesh(m, 'mini', colour); move(o, x, y, 0)
    soil(x, y, z0 + H - 6, a - 2.2, seed=seed + 4)
    succulent(x, y, z0 + H - 6.5, scale=plant, seed=seed)
    VOL.setdefault('minis', []).append(round(v / 1000, 2))

def shot_m_mini_a():
    o, v = add_mesh(G.vessel(102, 36, 10, n=4.0, wall=2.2, floor=2.0, tex='rib', band=(1.6, 8.8), cell=2.0, amp=0.5, M=1080), 'tray', 'tan')
    VOL['tray'] = round(v / 1000, 2)
    for i, x in enumerate((-64, 0, 64)):
        _mini(x, 0, 28, 54, 'tan', z0=2.0, seed=i + 1)
    return dict(elev=24, az=-16, target=(0, 0, 30))

def shot_m_mini_b():
    for i, (x, H) in enumerate(((-64, 48), (0, 64), (64, 80))):
        _mini(x, 0, 28, H, 'ivory', seed=i + 1)
    return dict(elev=20, az=-16, target=(0, 0, 42))

def shot_m_mini_c():
    for i, (x, c) in enumerate(((-96, 'ivory'), (-32, 'charcoal'), (32, 'green'), (96, 'tan'))):
        _mini(x, 0, 28, 56, c, seed=i + 1)
    return dict(elev=22, az=-12, target=(0, 0, 32))

# ---- final product shots (picked designs)
COLR = os.environ.get('COLR', 'ivory')

def shot_p_soap():
    slatted(116, 84, 28, COLR, top='cradle', end_r=16.0, dip=7.0, t=1.6, gap=3.4, end_t=1.6)
    return dict(elev=30, az=-34, target=(0, 0, 13), margin=1.1)

def shot_p_soap_use():
    slatted(116, 84, 28, COLR, top='cradle', end_r=16.0, dip=7.0, t=1.6, gap=3.4, end_t=1.6)
    soap_round(4, 0, 21.5, 'soap_clay', D=62, T=22)
    return dict(elev=26, az=-34, target=(0, 0, 16), margin=1.12)

def shot_p_pot():
    _canister(0, 33, 33, 2, 92, COLR, lid_h=15, dish=-8, rings=False)
    return dict(elev=24, az=-20, target=(0, 0, 55), margin=1.05)

def shot_p_pot_use():
    _canister(0, 33, 33, 2, 92, COLR, lid_h=15, dish=-8, rings=True)
    return dict(elev=30, az=-20, target=(0, 0, 58), margin=1.05)

def _offset_new(before, dx=0, dy=0, rz=0):
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.location.x += dx * MM; o.location.y += dy * MM
            if rz:
                o.rotation_euler[2] += math.radians(rz)

def shot_p_soap_top():
    slatted(116, 84, 28, COLR, top='cradle', end_r=16.0, dip=7.0, t=1.6, gap=3.4, end_t=1.6)
    return dict(elev=72, az=-8, target=(0, 0, 10), margin=1.0)

def shot_p_soap_line():
    cols = ['ivory', 'charcoal', 'green', 'tan']
    pos = [(-66, 52), (66, 52), (-66, -52), (66, -52)]
    for c, (x, y) in zip(cols, pos):
        before = set(o.name for o in bpy.context.scene.objects)
        slatted(116, 84, 28, c, top='cradle', end_r=16.0, dip=7.0, t=1.6, gap=3.4, end_t=1.6)
        _offset_new(before, x, y)
    return dict(elev=40, az=-24, target=(0, 0, 10), margin=1.0)

def shot_p_pot_open():
    amp = 0.6
    m = G.vessel(33, 33, 92, n=2, wall=2.0, floor=2.2, tex='rib', band=(5.5, 90.8), cell=2.0, amp=amp, rb=5.5, M=1080)
    o, v = add_mesh(m, 'can', COLR); move(o, -24, 12, 0)
    l, lv = add_mesh(G.lid(33 + amp * 0.85 + 0.2, 33 + amp * 0.85 + 0.2, n=2, z0=0.0, h=15, dome=-8, M=1080,
                           grip=True, grip_pitch=2.0, grip_depth=0.6, rim=1.6), 'canlid', COLR)
    move(l, 52, -22, 0)
    gold_ring(48, -24, 7.6, R=8.5, tilt=8, rz=20)
    gold_ring(58, -18, 8.4, R=8.0, r=0.9, tilt=20, rz=-30)
    return dict(elev=30, az=-18, target=(10, -4, 40), margin=1.0)

def shot_p_pot_line():
    for c, x in zip(['ivory', 'charcoal', 'green', 'tan'], (-111, -37, 37, 111)):
        _canister(x, 33, 33, 2, 92, c, lid_h=15, dish=-8, rings=False)
    return dict(elev=18, az=-10, target=(0, 0, 55), margin=0.98)

# ------------------------------------------------------------------ scene

def setup(size, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x = sc.render.resolution_y = size
    sc.render.film_transparent = True
    sc.view_settings.view_transform = VT
    for lk in ('AgX - Medium High Contrast', 'Medium High Contrast', 'AgX - Base Contrast'):
        try:
            sc.view_settings.look = lk
            print('LOOK', lk)
            break
        except TypeError:
            pass
    sc.view_settings.exposure = EXPO
    sc.render.threads_mode = 'FIXED'; sc.render.threads = 2
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = lin((220, 211, 196)); bg.inputs['Strength'].default_value = 0.3
    bpy.ops.mesh.primitive_plane_add(size=20)
    pl = bpy.context.active_object; pl.is_shadow_catcher = True
    def area(loc, size_m, energy, rot):
        L = bpy.data.lights.new('L', 'AREA'); L.size = size_m; L.energy = energy
        ob = bpy.data.objects.new('L', L); bpy.context.collection.objects.link(ob)
        ob.location = loc; ob.rotation_euler = rot
        return ob
    area((-0.45, -0.35, 0.55), float(os.environ.get('KEYSIZE', '0.35')), 24, (math.radians(42), 0, math.radians(-38)))
    area((0.55, -0.25, 0.3), 0.8, 5, (math.radians(65), 0, math.radians(65)))
    area((0.0, 0.5, 0.55), 0.6, 9, (math.radians(-40), 0, math.radians(180)))

def camera(elev, az, target, lens=70, margin=0.98):
    bpy.context.view_layer.update()
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and not o.is_shadow_catcher]
    pts = []
    for o in objs:
        for c in o.bound_box:
            pts.append(o.matrix_world @ __import__('mathutils').Vector(c))
    pts = np.array([[p.x, p.y, p.z] for p in pts])
    t = np.array(target) * MM
    R = np.max(np.linalg.norm(pts - t, axis=1))
    fov = 2 * math.atan(18 / lens)
    d = R / math.sin(fov / 2) * margin
    e, a = math.radians(elev), math.radians(az)
    loc = t + d * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    cam = bpy.data.cameras.new('C'); cam.lens = lens
    co = bpy.data.objects.new('C', cam); bpy.context.collection.objects.link(co)
    co.location = loc
    em = bpy.data.objects.new('T', None); bpy.context.collection.objects.link(em); em.location = t
    con = co.constraints.new('TRACK_TO'); con.target = em; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'
    bpy.context.scene.camera = co

def main():
    name = sys.argv[1]
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 900
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 64
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup(size, samples)
    cam = globals()['shot_' + name]()
    camera(**cam)
    bpy.context.scene.render.filepath = str(OUT / f'{name}{SUFFIX}_rgba.png')
    bpy.ops.render.render(write_still=True)
    # composite over Ply background
    from PIL import Image
    im = Image.open(OUT / f'{name}{SUFFIX}_rgba.png').convert('RGBA')
    bgc = Image.new('RGBA', im.size, BG + (255,))
    Image.alpha_composite(bgc, im).convert('RGB').save(OUT / f'{name}{SUFFIX}.jpg', quality=92)
    vv = {k: (round(v / 1000.0, 2) if not isinstance(v, list) else v) for k, v in VOL.items()}
    json.dump(vv, open(OUT / f'{name}_vol.json', 'w'))
    print('VOLUME_CM3', vv)

if __name__ == '__main__':
    main()
