"""Stories for 16 - 22 Nov 2026 (weekly plan 8 Nov; copied from stories_2026_11_01.py, only the content changes).
Since 19 Oct 2026 Geoffry allows the Quilt and Tile renders on Instagram, always labelled "3D render".
Scheduled Stories carry no sticker; kit Stories (posted by hand) leave the lower half free for a sticker.
Usage: python3 tools/stories_2026_11_08.py [name-filter] -> build/<name>.png
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

tin = ('<svg width="560" height="360" viewBox="0 0 280 180"><ellipse cx="140" cy="140" rx="120" ry="34" fill="#4D6E92"/>'
       '<rect x="20" y="50" width="240" height="90" fill="#4D6E92"/><ellipse cx="140" cy="50" rx="120" ry="34" fill="#6B8CB0"/>'
       '<ellipse cx="140" cy="50" rx="80" ry="20" fill="none" stroke="#E9E4DA" stroke-width="4"/></svg>')
balcony = (f'<svg width="600" height="420" viewBox="0 0 300 210"><rect x="20" y="120" width="260" height="10" rx="5" fill="{I}"/>'
           + ''.join(f'<rect x="{30 + k * 30}" y="130" width="6" height="70" fill="{I}"/>' for k in range(9))
           + f'<rect x="20" y="196" width="260" height="10" rx="5" fill="{I}"/><rect x="70" y="84" width="40" height="36" rx="6" fill="#3E5446"/>'
           f'<rect x="130" y="90" width="34" height="30" rx="6" fill="{C}"/><rect x="190" y="80" width="44" height="40" rx="6" fill="#C2A27C"/>'
           f'<path d="M90 84 C 80 60, 100 50, 90 30 M90 84 C 100 64, 112 60, 118 46" stroke="#3E5446" stroke-width="5" fill="none"/></svg>')
flag_free = svg_stack(('#B4532A', '#E9E4DA', '#3E5446', '#E9E4DA', '#B4532A'))

# ---- Scheduled Stories (no sticker). Day · time (Cyprus) · background · Highlight ----
# Mon 16 Nov 12:00 · bone · How it works
stories['ply-story-59-about-500'] = page(P, 'Did you know', f'About 500 layers.<br>One {it("planter.", P)}', svg_stack(('#C2A27C', '#E9E4DA', '#3E5446', '#2B2A27', '#C2A27C', '#E9E4DA', '#3E5446')),
    'About 0.2 mm each, stacked into a 10 cm planter. Our estimate.', hsize=112)
# Mon 16 Nov 20:00 · sand · Ideas
stories['ply-story-60-windowsill'] = page(SU, 'Windowsill check', f'About 10 cm<br>{it("wide.", SU)}', rcard('quilt-planter-small-ivory.jpg', 760, 760),
    'Fits a nursery pot up to 8 cm. Made for the windowsill.', hsize=132)
# Tue 17 Nov 12:00 · clay · Ideas
stories['ply-story-61-humid-flat'] = page(R, 'Plant tip', f'Humid flat?<br>Water {it("less.", R)}', drops.replace(f'fill="{SU}"', f'fill="{I}"'),
    'Let the top 2 cm of soil dry before you water again.', hsize=124)
# Tue 17 Nov 20:00 · charcoal · About
stories['ply-story-62-ep5-is-up'] = page(I, 'Building Ply', f'Episode 5<br>is {it("up.", I)}', swatches(150),
    'Our filament vs Lebanese humidity. Watch it on our profile.', hsize=140)
# Wed 18 Nov 12:00 · terracotta · Ideas
stories['ply-story-63-slats'] = page(C, 'Loom', f'Slats, not<br>a {it("dish.", C)}', rcard('loom-soap-rest-charcoal.jpg', 760, 760),
    'The water runs through, so the bar dries. Coming soon.', hsize=124)
# Wed 18 Nov 20:00 · bone · Ideas
stories['ply-story-64-small-balcony'] = page(P, 'Small spaces', f'Made for small<br>{it("balconies.", P)}', balcony,
    'Tabletop pieces for railings, sills and corners.', hsize=116)
# Thu 19 Nov 12:00 · sand · About
stories['ply-story-65-tin'] = page(SU, 'Every home', f'The tin with<br>no {it("biscuits.", SU)}', tin,
    'Every teta has one. Pleat is ours. More at 18:00.', hsize=124)
# Thu 19 Nov 20:00 · clay · Ideas
stories['ply-story-66-pleat-holds'] = page(R, 'Pleat holds', f'What goes<br>{it("inside?", R)}',
    stagger([('Rings', I, P), ('Hair ties', P, I), ('Buttons', C, P), ('Cotton buds', SU, I)], size=52, pad='26px 48px', step=40, gap=24),
    'And the lid is a dish. (Pleat, coming soon.)', hsize=124)
# Fri 20 Nov 12:00 · charcoal · About
stories['ply-story-67-ply-layer'] = page(I, 'Our name', f'Ply, {it("n.", I)}<br>a layer.', svg_stack(('#C2A27C', '#E9E4DA', '#3E5446', '#B4532A', '#E9E4DA')),
    'Every piece is printed one layer at a time. Hence the name.', hsize=140)
# Fri 20 Nov 20:00 · terracotta · How it works
stories['ply-story-68-what-pla'] = page(C, 'Your question', f'What is it<br>made {it("of?", C)}',
    stagger([('PLA Matte', P, I), ('Made from plant starch', I, P), ('Soft matte finish', SU, I)], size=50, pad='26px 46px', step=40, gap=24),
    'Keep it indoors or in the shade: it softens around 55 °C.', hsize=124)
# Sat 21 Nov 12:00 · bone · Christmas
stories['ply-story-69-hard-to-buy'] = page(P, 'Gift list', f'Hard to<br>buy {it("for?", P)}',
    stagger([('Kills every plant · a vase', I, P), ('Perfect bathroom · Loom', R, I), ('Loses earrings · Pleat', SU, I), ('Has a windowsill · a planter', C, P)], size=46, pad='24px 42px', step=36, gap=22),
    'Designed and printed in Lebanon. Coming soon.', hsize=124)
# Sat 21 Nov 20:00 · sand · How it works
stories['ply-story-70-matte'] = page(SU, 'Finish', f'Matte, not<br>{it("shiny.", SU)}', rcard('tile-planter-small-tan.jpg', 760, 840, zoom=1.3),
    'Soft to the touch, and every layer line shows how it was made.', hsize=124)
# Sun 22 Nov 12:00 · clay · About
stories['ply-story-71-independence'] = page(R, '22 November', f'Made in layers.<br>Made in {it("Lebanon.", R)}', flag_free,
    'Happy Independence Day, from a small family studio.', hsize=112)
# Sun 22 Nov 20:00 · charcoal · About
stories['ply-story-72-thank-you'] = page(I, 'Thank you', f'Thanks for<br>following {it("along.", I)}', svg_stack(('#E9E4DA', '#3E5446', '#C2A27C', '#B4532A')),
    'Real prints are next. Turn on notifications so you see them first.', hsize=124)

# ---- Story kit (posted by hand, lower half left free for the sticker) ----
# Mon 16 Nov · charcoal · Quiz · How it works
stories['ply-story-73-quiz-layers'] = page(I, 'Quiz', f'How many layers<br>in one {it("planter?", I)}', top('', 600),
    'Pick your answer below.', hsize=108)
# Wed 18 Nov · sand · Poll · Ideas
stories['ply-story-74-poll-soap'] = page(SU, 'Bathroom', f'Your soap lives:<br>dish or {it("puddle?", SU)}', top('', 600),
    'Be honest. Vote below.', hsize=108)
# Fri 20 Nov · clay · Question sticker · About
stories['ply-story-75-question-first'] = page(R, 'Your pick', f'What should we<br>print {it("first?", R)}', top('', 600),
    'Tell us below: piece and colour.', hsize=108)

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
