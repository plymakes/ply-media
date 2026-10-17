"""Recreate the brand-intro posts 1-6 and post 28 in the Atelier style (Fraunces). Renders build/ply-post-NN-...-v3.png"""
import base64, math, runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P, page, stagger, CSS = m['C'], m['SU'], m['R'], m['I'], m['P'], m['page'], m['stagger'], m['CSS']
root = Path(__file__).resolve().parent.parent
logo = lambda n: 'data:image/svg+xml;base64,' + base64.b64encode((root / 'brand/logos' / n).read_bytes()).decode()
# vase made of layers
layers = ''
n, h, gap, cx, bottom = 22, 18, 4, 436, 460
for i in range(n):
    t = i / (n - 1)
    w = 220 + 170 * math.sin(math.pi * (0.15 + 0.75 * t)) - 60 * t
    y = bottom - (i + 1) * (h + gap)
    col = [I, C, P][(i // 3) % 3]
    layers += f'<div style="position:absolute;left:{cx-w/2:.0f}px;top:{y}px;width:{w:.0f}px;height:{h}px;border-radius:9px;background:{col}"></div>'
posts = {
 'ply-post-01-hello-lebanon': page(I, 'Hello, Lebanon', 'Ply makes it <i style="color:#D27A52">yours.</i>',
    f'<img src="{logo("ply-makes-lockup-bone.svg")}" style="width:700px">',
    '3D-printed gifts and custom prints. Launching soon.', hsize=118),
 'ply-post-02-what-we-make': page(C, 'What we make', 'Your name.<br>Your idea.<br>Your spare part.',
    stagger([('Name gifts', P, I), ('Décor', SU, I), ('Spare parts', I, P)], size=44, pad='22px 44px', step=40, gap=18),
    'Printed layer by layer, made in Lebanon. If you can imagine it, Ply makes it.', hsize=112),
 'ply-post-03-what-first': page(P, 'Help us choose', 'What should Ply make <i style="color:#B4532A">first?</i>',
    stagger([('A · Name keychains', I, P), ('B · Christmas ornaments', C, P), ('C · Name lamps', SU, I), ('D · Something else?', R, I)], size=42, pad='22px 40px', step=36, gap=16),
    'Vote with your letter in the comments ↓', hsize=112),
 'ply-post-04-layer-by-layer': page(SU, 'How 3D printing works', 'Layer by <i style="color:#B4532A">layer.</i>',
    f'<div style="position:relative;width:872px;height:470px">{layers}</div>',
    'Thin layers of plastic, about 0.2 mm each, stacked until your idea stands on its own.', hsize=120),
 'ply-post-05-spare-parts': page(R, 'Ply makes it fit', 'Broken knob? Missing clip? <i style="color:#9C4421">Don’t throw it out.</i>',
    stagger([('1 · Send a photo', P, I), ('2 · We design the part', SU, I), ('3 · Ply prints it', I, P)], size=42, pad='22px 40px', step=36, gap=16),
    'Spare parts for the things you love, printed in Lebanon. Coming soon.', hsize=104),
 'ply-post-06-coming-soon': page(I, 'Coming soon', 'Made in Lebanon, one layer at a time.',
    f'<img src="{logo("ply-mark-bone.svg")}" style="width:520px">',
    'Follow @plymakes to see the first prints.', hsize=112),
 'ply-post-28-weekend-question': page(C, 'Weekend question', 'If you could 3D print anything…',
    stagger([('A gift for someone', P, I), ('Something for home', SU, I), ('A part to fix', I, P), ('Something wild', R, I)], size=44, pad='22px 44px', step=36, gap=18),
    'Tell us in the comments. The best answers might become our first designs.', hsize=112),
}
out = root / 'build'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for name, html in posts.items():
        f = out / f'{name}.html'; f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.goto(f.as_uri()); pg.wait_for_timeout(300); pg.screenshot(path=str(out / f'{name}-v3.png'))
    b.close()
print('ok')
