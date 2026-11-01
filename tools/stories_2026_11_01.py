"""Stories for 9 - 15 Nov 2026 (weekly plan 1 Nov; copied from stories_2026_10_25.py, only the content changes).
Since 19 Oct 2026 Geoffry allows the Quilt and Tile renders on Instagram, always labelled "3D render".
Scheduled Stories carry no sticker; kit Stories (posted by hand) leave the lower half free for a sticker.
Usage: python3 tools/stories_2026_11_01.py [name-filter] -> build/<name>.png
"""
import runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
flt = sys.argv[1:]
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P, page, stagger, CSS = m['C'], m['SU'], m['R'], m['I'], m['P'], m['page'], m['stagger'], m['CSS']
CSS = CSS.replace('body{width:1080px;height:1350px', 'body{width:1080px;height:1920px').replace(
    '.p{width:1080px;height:1350px;padding:96px 104px 88px', '.p{width:1080px;height:1920px;padding:250px 104px 270px')
ROOT = Path(__file__).resolve().parent.parent
ACC_L, ACC_D = '#9C4421', '#D27A52'


def it(word, bg):
    return f'<i style="color:{ACC_D if bg == I else (P if bg == C else ACC_L)}">{word}</i>'


def src(name):
    return (ROOT / 'shop' / ('banners' if name.startswith('drainage') else 'products') / name).as_uri()


def rcard(name, w=760, h=760, pos='center', zoom=1.0, label='3D render'):
    """A render in a rounded card with the '3D render' pill."""
    return (f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:32px;overflow:hidden;flex-shrink:0">'
            f'<img src="{src(name)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};transform:scale({zoom});transform-origin:{pos};display:block">'
            f'<div style="position:absolute;left:24px;bottom:24px;padding:10px 20px;border-radius:999px;background:rgba(239,234,226,.92);color:{I};'
            f'font-size:22px;font-weight:500;letter-spacing:.18em;text-transform:uppercase">{label}</div></div>')


def pair(a, b, w=420, h=560):
    return f'<div style="display:flex;gap:32px">{rcard(a, w, h)}{rcard(b, w, h)}</div>'


def top(html, space=520):
    return f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-start;height:100%;width:100%;padding-top:60px">{html}<div style="height:{space}px"></div></div>'


stories = {}


def svg_stack(cols=('#E9E4DA', '#3E5446', '#C2A27C', '#2B2A27', '#E9E4DA', '#3E5446'), w=520, h=56, gap=10):
    """Simple layer stack: printed layers as soft bars."""
    return ('<div style="display:flex;flex-direction:column;gap:%dpx;align-items:center">' % gap +
            ''.join(f'<div style="width:{w - abs(i - len(cols) / 2) * 30:.0f}px;height:{h}px;border-radius:{h // 2}px;background:{c}"></div>' for i, c in enumerate(cols)) + '</div>')


def swatches(size=170):
    return '<div style="display:flex;gap:30px">' + ''.join(
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{c};border:3px solid #8A857C"></div>'
        for c in ('#E9E4DA', '#2B2A27', '#3E5446', '#C2A27C')) + '</div>'


sun = f'<svg width="420" height="420" viewBox="0 0 200 200"><circle cx="100" cy="100" r="46" fill="{C}"/>' + ''.join(
    f'<rect x="96" y="14" width="8" height="30" rx="4" fill="{C}" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 45)) + '</svg>'
drops = '<svg width="420" height="420" viewBox="0 0 200 200">' + ''.join(
    f'<path d="M{x} {y} C {x-18} {y+28}, {x-18} {y+52}, {x} {y+52} C {x+18} {y+52}, {x+18} {y+28}, {x} {y} Z" fill="{SU}"/>' for x, y in ((60, 30), (130, 60), (85, 110))) + '</svg>'
box = (f'<svg width="460" height="420" viewBox="0 0 230 210"><path d="M115 20 L210 60 L115 100 L20 60 Z" fill="{SU}"/>'
       f'<path d="M20 60 L115 100 L115 200 L20 160 Z" fill="{R}"/><path d="M210 60 L115 100 L115 200 L210 160 Z" fill="#C9A68F"/>'
       f'<path d="M67 40 L162 80 L162 112" stroke="{P}" stroke-width="10" fill="none"/></svg>')


tile = ('<svg width="560" height="400" viewBox="0 0 140 100"><rect width="140" height="100" rx="6" fill="#DDB8A2"/>'
        '<path d="M70 8 L112 50 L70 92 L28 50 Z" fill="none" stroke="#1C1B19" stroke-width="5"/><circle cx="70" cy="50" r="12" fill="#B4532A"/>'
        '<circle cx="0" cy="0" r="16" fill="#1C1B19"/><circle cx="140" cy="0" r="16" fill="#1C1B19"/><circle cx="0" cy="100" r="16" fill="#1C1B19"/><circle cx="140" cy="100" r="16" fill="#1C1B19"/></svg>')

# ---- Scheduled Stories (no sticker). Day · time (Cyprus) · background · Highlight ----
# Mon 9 Nov 12:00 · bone · About
stories['ply-story-42-printer-on-its-way'] = page(P, 'Printer week', f'On its way<br>to {it("Lebanon.", P)}', box,
    'If all goes to plan, it lands this week. The unboxing goes up here.', hsize=132)
# Mon 9 Nov 20:00 · sand · Ideas
stories['ply-story-43-soft-soap'] = page(SU, 'Bathroom', f'Soft soap?<br>Blame the {it("puddle.", SU)}', rcard('loom-soap-rest-tan.jpg', 760, 760),
    'Loom lets the water run through the slats. Coming soon.', hsize=116)
# Tue 10 Nov 12:00 · clay · How it works
stories['ply-story-44-four-checks'] = page(R, 'First test', f'What we check<br>{it("first.", R)}',
    stagger([('Does the tray twist off?', I, P), ('Do all seven holes drain?', C, P), ('Are the layers even?', P, I), ('Does it stand flat?', SU, I)], size=48, pad='26px 44px', step=36, gap=22),
    'Every test print gets these four checks.', hsize=124)
# Tue 10 Nov 20:00 · charcoal · About
stories['ply-story-45-ep4-is-up'] = page(I, 'Building Ply', f'Episode 4<br>is {it("up.", I)}', svg_stack(('#C2A27C', '#E9E4DA', '#3E5446', '#B4532A')),
    'The first print isn’t for sale. Watch it on our profile.', hsize=140)
# Wed 11 Nov 12:00 · terracotta · Ideas
stories['ply-story-46-pleat-bedside'] = page(C, 'Bedside', f'Rings off,<br>{it("lid on.", C)}', rcard('pleat-pot-charcoal.jpg', 760, 760),
    'Pleat: a small ribbed pot with a dish for a lid. Coming soon.', hsize=124)
# Wed 11 Nov 20:00 · bone · How it works
stories['ply-story-47-why-no-water'] = page(P, 'Your question', f'Why no water<br>in the {it("vases?", P)}', rcard('tile-vase-charcoal.jpg', 700, 780),
    'Printed walls aren’t reliably watertight. Dried stems last for months.', hsize=116)
# Thu 12 Nov 12:00 · sand · About
stories['ply-story-48-patterned-floors'] = page(SU, 'Beirut floors', f'Patterned floors,<br>soft {it("shapes.", SU)}', tile,
    'The Tile pieces borrow the grid of old cement tiles.', hsize=112)
# Thu 12 Nov 20:00 · clay · Ideas
stories['ply-story-49-dark-green-close'] = page(R, 'Up close', f'Dark {it("Green.", R)}', rcard('quilt-planter-small-green.jpg', 760, 840, zoom=1.25),
    'Deep and calm. Leaves look greener against it.', hsize=140)
# Fri 13 Nov 12:00 · charcoal · Christmas
stories['ply-story-50-gift-list-2'] = page(I, 'Gift list', f'Who’s on your<br>{it("list?", I)}',
    stagger([('Your sister · Pleat', P, I), ('The new flat · Loom', C, P), ('Your teta · a planter', SU, I), ('Your boss · a vase', R, I)], size=50, pad='26px 46px', step=40, gap=24),
    'Four pieces, four colours. Made in Lebanon.', hsize=124)
# Fri 13 Nov 20:00 · terracotta · About
stories['ply-story-51-small-batches'] = page(C, 'Small batches', f'One printer.<br>{it("Small batches.", C)}', svg_stack(),
    'First pick goes to the First Layer. DM us “FIRST” to join.', hsize=116)
# Sat 14 Nov 12:00 · bone · Ideas
stories['ply-story-52-plant-something-small'] = page(P, 'Weekend plan', f'Plant something<br>{it("small.", P)}', rcard('quilt-planter-small-ivory.jpg', 760, 760),
    'A succulent, a cactus or a herb. About 10 cm is plenty.', hsize=116)
# Sat 14 Nov 20:00 · sand · How it works
stories['ply-story-53-45ml'] = page(SU, 'Hidden tray', f'About 45 ml,<br>{it("out of sight.", SU)}', drops.replace(f'fill="{SU}"', f'fill="{I}"'),
    'That’s what the drip tray under the planter holds.', hsize=116)
# Sun 15 Nov 12:00 · clay · Ideas
stories['ply-story-54-one-shelf'] = page(R, 'Colours', f'Four colours,<br>{it("one shelf.", R)}', swatches(),
    'Ivory White, Charcoal, Dark Green, Desert Tan.', hsize=124)
# Sun 15 Nov 20:00 · charcoal · About
stories['ply-story-55-coming-up'] = page(I, 'Coming up', f'Real photos,<br>{it("soon.", I)}', svg_stack(('#E9E4DA', '#3E5446', '#C2A27C', '#B4532A')),
    'Once the test prints pass, the renders make way for the real thing.', hsize=132)

# ---- Story kit (posted by hand, lower half left free for the sticker) ----
# Tue 10 Nov · charcoal · Emoji slider · About
stories['ply-story-56-slider-first-print'] = page(I, 'First print', f'Ready for the<br>{it("real thing?", I)}', top('', 600),
    'Slide below.', hsize=112)
# Thu 12 Nov · sand · Poll · Ideas
stories['ply-story-57-poll-teta-floor'] = page(SU, 'Teta’s house', f'The floor at<br>teta’s: patterned<br>or {it("plain?", SU)}', top('', 560),
    'Vote below.', hsize=104)
# Sat 14 Nov · clay · Quiz · How it works
stories['ply-story-58-quiz-water'] = page(R, 'Quiz', f'Where does the<br>water {it("go?", R)}', top('', 600),
    'Pick your answer below.', hsize=120)

out = ROOT / 'build'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for name, html in stories.items():
        if flt and not any(f in name for f in flt):
            continue
        f = out / f'{name}.html'; f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.goto(f.as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=str(out / f'{name}.png'))
    b.close()
print(len(stories), 'stories')
