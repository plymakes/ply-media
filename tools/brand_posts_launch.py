"""Pre-launch posts after the 17 Oct 2026 pivot: three stock pieces, no customisation, no product images
until the designs are final and real photos exist. Type and flat shapes only.
Slogan: "Made in layers. Made in Lebanon." / "طبقة فوق طبقة، من لبنان"
Usage: python3 tools/brand_posts_launch.py [name-filter] -> build/<name>-v3.png
"""
import base64, math, runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
flt = sys.argv[1:]
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P, page, stagger, CSS = m['C'], m['SU'], m['R'], m['I'], m['P'], m['page'], m['stagger'], m['CSS']
ROOT = Path(__file__).resolve().parent.parent
logo = lambda n: 'data:image/svg+xml;base64,' + base64.b64encode((ROOT / 'brand/logos' / n).read_bytes()).decode()
ACC_L, ACC_D = '#9C4421', '#D27A52'


def it(word, bg):
    return f'<i style="color:{ACC_D if bg == I else (P if bg == C else ACC_L)}">{word}</i>'


def layers_bar(n, w0, w1, h, cols, gap=6):
    return '<div style="display:flex;flex-direction:column;align-items:center;gap:%dpx">' % gap + ''.join(
        f'<div style="width:{w0 + (w1 - w0) * i / max(1, n - 1):.0f}px;height:{h}px;border-radius:{h/2}px;background:{cols[i % len(cols)]}"></div>' for i in range(n)) + '</div>'


posts = {}

posts['ply-post-43-made-in-layers'] = page(I, 'Hello again', f'Made in layers.<br>{it("Made in Lebanon.", I)}',
    f'<img src="{logo("ply-makes-lockup-bone.svg")}" style="width:640px">',
    'Ply designs and 3D-prints calm, useful pieces for your home. First collection in November.', hsize=104)

posts['ply-post-44-ply-means-layer'] = page(P, 'What’s in a name', '',
    f'''<div style="width:100%">
<div style="font-family:IS,Georgia,serif;font-size:300px;line-height:.9;letter-spacing:-.02em">ply<span style="color:{C}">.</span></div>
<div style="font-size:36px;font-weight:500;margin-top:110px;color:#6E6A63">/plaɪ/ &nbsp;·&nbsp; noun</div>
<div style="font-family:IS,Georgia,serif;font-size:62px;line-height:1.15;margin-top:24px">a layer, a strand,<br>a thickness.</div></div>''',
    'Every piece we make is built from hundreds of thin layers. So the name chose itself.', hsize=10)

posts['ply-post-45-how-thin'] = page(SU, 'Did you know?', f'How thin is one {it("layer?", SU)}',
    f'''<div style="display:flex;align-items:center;gap:72px">
<div style="font-family:IS,Georgia,serif;font-size:250px;line-height:1;letter-spacing:-.03em">0.2<span style="font-size:110px">mm</span></div>
<div style="display:flex;flex-direction:column;gap:16px">{''.join(f'<div style="width:{w}px;height:10px;border-radius:5px;background:{I}"></div>' for w in (200, 200, 200))}
<div style="font-size:34px;font-weight:500;margin-top:14px">≈ three hairs</div></div></div>''',
    'About the thickness of three human hairs. A small pot takes a few hundred of them.', hsize=108)

posts['ply-post-46-guess-the-three'] = page(R, 'Coming in November', f'Can you guess the {it("three?", R)}',
    stagger([('01 · Holds a plant', I, P), ('02 · Holds dried stems', P, I), ('03 · Sits under your coffee', C, P)], size=44, pad='24px 44px', step=40, gap=20),
    'Guess in the comments. The reveal comes with the first real photos.', hsize=108)

posts['ply-post-47-sketch-to-shelf'] = page(P, 'How we work', f'From sketch to {it("shelf.", P)}',
    stagger([('1 · Sketch', SU, I), ('2 · 3D model', R, I), ('3 · Test print', C, P), ('4 · Your shelf', I, P)], size=44, pad='24px 44px', step=40, gap=20),
    'Every Ply piece is test-printed and refined before it’s sold.', hsize=112)


def mf(myth, fact):
    return f'''<div style="display:flex;flex-direction:column;gap:14px;width:100%">
<div style="display:flex;gap:20px;align-items:baseline"><span class="pill" style="background:{P};color:{I};padding:8px 20px;font-size:24px">MYTH</span><span style="font-size:38px;font-weight:700;letter-spacing:-.02em;text-decoration:line-through;text-decoration-thickness:4px;color:#4A3B33">{myth}</span></div>
<div style="display:flex;gap:20px;align-items:baseline"><span class="pill" style="background:{I};color:{P};padding:8px 20px;font-size:24px">FACT</span><span style="font-size:38px;font-weight:700;letter-spacing:-.02em;line-height:1.2">{fact}</span></div></div>'''
posts['ply-post-48-myth-fact'] = page(R, 'Myth vs fact', 'Myth vs fact.',
    f'<div style="display:flex;flex-direction:column;gap:64px;width:100%">{mf("3D prints look cheap.", "Good design and careful finishing make the difference.")}{mf("Plastic means throwaway.", "Our PLA comes from plants, and our pieces are made to keep.")}</div>',
    'Got another question about 3D printing? Ask it in the comments.', hsize=112)

leaf = f'''<svg width="300" height="300" viewBox="0 0 300 300"><circle cx="150" cy="150" r="150" fill="{P}"/>
<path d="M150 230 C 90 200, 80 120, 150 70 C 220 120, 210 200, 150 230 Z" fill="#6F7D5C"/><path d="M150 230 L150 95" stroke="{P}" stroke-width="6" stroke-linecap="round"/></svg>'''
stems = f'''<svg width="300" height="300" viewBox="0 0 300 300"><circle cx="150" cy="150" r="150" fill="{I}"/>''' + ''.join(
    f'<path d="M150 240 Q {150 + dx*0.4} 160 {150 + dx} {top}" stroke="{SU}" stroke-width="5" fill="none" stroke-linecap="round"/><ellipse cx="{150 + dx}" cy="{top - 14}" rx="11" ry="22" fill="{P}" transform="rotate({dx/3} {150 + dx} {top - 14})"/>'
    for dx, top in ((-60, 90), (-15, 70), (25, 82), (65, 100))) + '</svg>'
cap = lambda t: f'<div style="font-size:40px;font-weight:700;margin-top:24px;text-align:center">{t}</div>'
posts['ply-post-49-plants-or-flowers'] = page(SU, 'This or that?', f'Plants or dried {it("flowers?", SU)}',
    f'<div style="display:flex;gap:72px"><div>{leaf}{cap("A · Plants")}</div><div>{stems}{cap("B · Dried flowers")}</div></div>',
    'Vote A or B in the comments ↓', hsize=112)

posts['ply-post-50-fewer-better'] = page(C, 'What we believe', f'Fewer things.<br>Made {it("well.", C)}',
    layers_bar(9, 300, 620, 26, [P, SU, R], gap=10),
    'Three pieces to start, each one tested until it’s right. That’s the whole plan.', hsize=128)

posts['ply-post-51-made-here'] = page(I, 'Made in Lebanon', f'Designed here.<br>{it("Printed here.", I)}',
    f'<div dir="rtl" lang="ar" style="font-family:PA;font-weight:600;font-size:96px;line-height:1.4;color:{SU};text-align:center">طبقة فوق طبقة،<br>من لبنان</div>',
    'Every Ply piece is printed in Lebanon, one at a time.', hsize=116)

gift = f'''<div style="display:flex;gap:40px;align-items:flex-end">
<div style="width:240px;height:200px;border-radius:16px;background:{C};position:relative"><div style="position:absolute;left:105px;top:0;width:30px;height:200px;background:{P}"></div></div>
<div style="width:200px;height:300px;border-radius:16px;background:{I};position:relative"><div style="position:absolute;left:85px;top:0;width:30px;height:300px;background:{SU}"></div></div>
<div style="width:220px;height:150px;border-radius:16px;background:{SU};position:relative"><div style="position:absolute;left:95px;top:0;width:30px;height:150px;background:{C}"></div></div></div>'''
posts['ply-post-52-christmas-made-here'] = page(P, 'Christmas', f'Christmas, made {it("here.", P)}', gift,
    'Our first pieces land before Christmas. Join the First Layer for first pick.', hsize=120)

posts['ply-post-53-favourite-corner'] = page(SU, 'Weekend question', f'Your favourite corner of {it("home?", SU)}',
    stagger([('The balcony', I, P), ('The desk', P, I), ('The coffee table', C, P), ('The windowsill', R, I)], size=44, pad='22px 44px', step=36, gap=18),
    'Tell us below. Our first pieces are made for these spots.', hsize=112)

posts['ply-post-54-ask-us'] = page(R, 'Q&amp;A', f'Ask us {it("anything.", R)}',
    f'<div style="font-family:IS,Georgia,serif;font-size:520px;line-height:.8;color:{C}">?</div>',
    'About 3D printing, our pieces or the launch. We’ll answer in Stories.', hsize=124)

posts['ply-post-27b-first-layer-launch'] = page(I, 'The First Layer', 'Be first in line.',
    stagger([('First look at every piece', C, P), ('First pick of the first batch', SU, I), ('Order before everyone else', R, I)], size=42, pad='24px 44px', step=36, gap=20),
    'DM “FIRST” or comment 🧡 to join. Free, no commitment.', hsize=124)

sw = '<div style="display:flex;gap:48px">' + ''.join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px"><div style="width:240px;height:240px;border-radius:50%;background:{c};{"border:3px solid #4A463F;" if c == "#26241F" else ""}"></div><div style="font-size:32px;font-weight:500;color:{SU}">{n}</div></div>'
    for c, n in ((P, 'Bone'), ('#26241F', 'Charcoal'), (C, 'Terracotta'))) + '</div>'
posts['ply-post-42-three-colours'] = page(I, 'Colours', f'Three colours. That’s {it("it.", I)}', sw,
    'Chosen to go together, so every piece matches the next one you add.', hsize=116)

posts['ply-post-55-whats-next'] = page(P, 'Help us choose', f'What should piece four {it("be?", P)}',
    stagger([('A · Christmas ornaments', I, P), ('B · Catch-all tray', C, P), ('C · Pen pot', SU, I), ('D · Headphone stand', R, I)], size=42, pad='22px 40px', step=36, gap=16),
    'Vote with your letter in the comments ↓', hsize=112)

out = ROOT / 'build'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for name, html in posts.items():
        if flt and not any(f in name for f in flt):
            continue
        f = out / f'{name}.html'; f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.goto(f.as_uri()); pg.wait_for_timeout(400); pg.screenshot(path=str(out / f'{name}-v3.png'))
    b.close()
print(len(posts), 'posts')
