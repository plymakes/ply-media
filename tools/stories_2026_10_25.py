"""Stories for 25 Oct - 8 Nov 2026 (weekly plan 25 Oct; copied from stories_2026_10_19.py, only the content changes).
Since 19 Oct 2026 Geoffry allows the Quilt and Tile renders on Instagram, always labelled "3D render".
Scheduled Stories carry no sticker; kit Stories (posted by hand) leave the lower half free for a sticker.
Usage: python3 tools/stories_2026_10_25.py [name-filter] -> build/<name>.png
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

# ---- Scheduled Stories (no sticker). Day · time (Cyprus) · background · Highlight ----
# Sun 25 Oct 12:00 · sand · Ideas
stories['ply-story-18-sunday-reset'] = page(SU, 'Sunday reset', f'A dry bar<br>of {it("soap.", SU)}', rcard('loom-soap-rest-in-use-ivory.jpg', 760, 780),
    'Loom lets the water run through, so the bar dries between washes. Coming soon.', hsize=124)
# Sun 25 Oct 20:00 · charcoal · About
stories['ply-story-19-grandparents-floor'] = page(I, 'Beirut floors', f'Whose teta had<br>floors like {it("these?", I)}', rcard('tile-planter-small-ivory.jpg', 760, 740),
    'Our Tile planter borrows that old cement-tile grid. Reply with the pattern you grew up on.', hsize=108)
# Mon 26 Oct 20:00 · clay · How it works
stories['ply-story-20-no-moulds'] = page(R, 'How it works', f'No {it("moulds.", R)}', svg_stack(),
    'Every piece is printed from a file, so we can improve a design after every test.', hsize=140)
# Tue 27 Oct 12:00 · bone · Ideas
stories['ply-story-21-pleat-desk'] = page(P, 'Desk', f'On your desk:<br>{it("Pleat.", P)}', rcard('pleat-pot-green.jpg', 760, 760),
    'Clips inside, rings on the lid. Coming soon in four colours.', hsize=124)
# Wed 28 Oct 20:00 · terracotta · Ideas
stories['ply-story-22-loom-four-colours'] = page(C, 'Colours', f'One soap rest.<br>{it("Four colours.", C)}', rcard('loom-soap-rest-four-colours.jpg', 820, 700),
    'Ivory White, Charcoal, Dark Green and Desert Tan, all in a soft matte finish.', hsize=116)
# Thu 29 Oct 12:00 · sand · How it works
stories['ply-story-23-hot-car'] = page(SU, 'Care tip', f'Not for the<br>{it("hot car.", SU)}', sun,
    'PLA softens around 55 °C. Indoors or in the shade, it keeps its shape.', hsize=132)
# Fri 30 Oct 20:00 · charcoal · How it works
stories['ply-story-24-damp-winter'] = page(I, 'Care tip', f'Damp Beirut<br>{it("winter?", I)}', drops,
    'No rust, no peeling paint. Just wipe it with a damp cloth.', hsize=132)
# Sat 31 Oct 20:00 · clay · Ideas
stories['ply-story-25-repot-something'] = page(R, 'Weekend plan', f'Repot<br>{it("something.", R)}', rcard('quilt-planter-small-tan.jpg', 760, 760),
    'Succulents and herbs love a small pot with good drainage.', hsize=132)
# Mon 2 Nov 12:00 · bone · Ideas
stories['ply-story-26-kitchen-herbs'] = page(P, 'Kitchen', f'Mint, thyme<br>or {it("basil?", P)}', rcard('tile-planter-small-ivory.jpg', 760, 740),
    'A sunny kitchen windowsill is enough. Water when the top feels dry.', hsize=124)
# Mon 2 Nov 20:00 · sand · Ideas
stories['ply-story-27-why-matte'] = page(SU, 'Finish', f'Why {it("matte?", SU)}', swatches(),
    'A soft finish that hides fingerprints and lets the layers show gently.', hsize=150)
# Tue 3 Nov 12:00 · terracotta · Christmas
stories['ply-story-28-gift-list'] = page(C, 'Gift list', f'Start your<br>{it("gift list.", C)}',
    stagger([('Plant lover · a planter', I, P), ('Minimalist · a vase', P, I), ('New flat · Loom', SU, I), ('Ring collector · Pleat', R, I)], size=50, pad='26px 46px', step=40, gap=24),
    'Four pieces, four colours. First ones in November.', hsize=124)
# Tue 3 Nov 20:00 · charcoal · About
stories['ply-story-29-ep3-is-up'] = page(I, 'Building Ply', f'Episode 3<br>is {it("up.", I)}', svg_stack(('#3E5446', '#C2A27C', '#E9E4DA', '#B4532A')),
    'Our printer should land next week. Watch it on our profile.', hsize=140)
# Wed 4 Nov 12:00 · clay · Ideas
stories['ply-story-30-desert-tan'] = page(R, 'Colour', f'Desert {it("Tan.", R)}', rcard('quilt-vase-tan.jpg', 760, 840),
    'Warm like sandstone and old village walls.', hsize=140)
# Wed 4 Nov 20:00 · bone · Ideas
stories['ply-story-31-where-would-yours-go'] = page(P, 'Your home', f'Where would<br>yours {it("go?", P)}',
    stagger([('The windowsill', I, P), ('The desk', C, P), ('The bathroom shelf', SU, I), ('The bedside table', R, I)], size=52, pad='28px 50px', step=40, gap=24),
    'Reply and tell us. We read every message.', hsize=124)
# Thu 5 Nov 12:00 · sand · Ideas
stories['ply-story-32-ivory-white'] = page(SU, 'Colour', f'Ivory {it("White.", SU)}', rcard('tile-vase-ivory.jpg', 760, 840),
    'Soft, like fresh plaster. It lets the stems do the talking.', hsize=140)
# Fri 6 Nov 12:00 · terracotta · How it works
stories['ply-story-33-twist-empty-click'] = page(C, 'Hidden tray', f'Twist. Empty.<br>{it("Click.", C)}',
    stagger([('1 · Twist the tray off', I, P), ('2 · Empty the water', P, I), ('3 · Click it back on', SU, I)], size=54, pad='30px 52px', step=44, gap=26),
    'The drip tray hides under the planter. No saucer on show.', hsize=124)
# Fri 6 Nov 20:00 · charcoal · Ideas
stories['ply-story-34-mint-in-a-tin'] = page(I, 'Balcony', f'Mint still<br>in a {it("tin?", I)}', rcard('quilt-planter-small-green.jpg', 760, 740),
    'Reply with a photo of yours. We love a good balcony.', hsize=112)
# Sat 7 Nov 12:00 · clay · Ideas
stories['ply-story-35-charcoal'] = page(R, 'Colour', f'{it("Charcoal.", R)}', rcard('tile-planter-small-charcoal.jpg', 760, 840),
    'Calm and graphic. Green leaves look even greener against it.', hsize=140)
# Sat 7 Nov 20:00 · sand · About
stories['ply-story-36-one-family'] = page(SU, 'About us', f'One family.<br>{it("One printer.", SU)}', svg_stack(),
    'A small homeware studio in Lebanon, made in layers.', hsize=128)
# Sun 8 Nov 12:00 · bone · Ideas
stories['ply-story-37-design-next'] = page(P, 'Your vote', f'What should<br>we design {it("next?", P)}',
    stagger([('A · Christmas ornaments', I, P), ('B · Catch-all tray', C, P), ('C · Pen pot', SU, I), ('D · Headphone stand', R, I)], size=50, pad='26px 46px', step=40, gap=24),
    'Vote with a letter in the comments of today’s post.', hsize=124)
# Sun 8 Nov 20:00 · terracotta · About
stories['ply-story-38-printer-week'] = page(C, 'Coming up', f'Printer<br>{it("week.", C)}', box,
    'If all goes to plan, our printer lands this week. The unboxing goes up here.', hsize=150)

# ---- Story kit (posted by hand, lower half left free for the sticker) ----
# Mon 2 Nov · charcoal · Quiz sticker · How it works
stories['ply-story-39-vase-quiz'] = page(I, 'Quiz', f'Can our vases<br>hold {it("water?", I)}', top('', 600),
    'Answer below. We reply to every guess.', hsize=128)
# Thu 5 Nov · bone · Question sticker · About
stories['ply-story-40-ask-us'] = page(P, 'Your questions', f'Ask us<br>{it("anything.", P)}', top('', 600),
    '3D printing, the pieces, the colours, the launch.', hsize=140)
# Sat 7 Nov · clay · Poll sticker · Ideas
stories['ply-story-41-loom-colour'] = page(R, 'Bathroom', f'Loom in your bathroom:<br>which {it("colour?", R)}', top('', 600),
    'Vote below.', hsize=112)

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
