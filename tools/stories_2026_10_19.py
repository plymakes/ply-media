"""Stories for 20 Oct - 1 Nov 2026 (copied from stories_2026_10_18.py; only the content changes).
Since 19 Oct 2026 Geoffry allows the Quilt and Tile renders on Instagram, always labelled "3D render".
Scheduled Stories carry no sticker; kit Stories (posted by hand) leave the lower half free for a sticker.
Usage: python3 tools/stories_2026_10_19.py [name-filter] -> build/<name>.png
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

# Scheduled · Tue 20 Oct 12:00 · bone · About
stories['ply-story-07-meet-the-quilt'] = page(P, 'New', f'Meet the {it("Quilt.", P)}', rcard('quilt-planter-small-ivory.jpg'),
    'A soft diamond quilt, in a calm matte finish. First prints in November.', hsize=128)

# Scheduled · Wed 21 Oct 20:00 · charcoal · About
stories['ply-story-08-meet-the-tile'] = page(I, 'New', f'Meet the {it("Tile.", I)}', rcard('tile-planter-small-charcoal.jpg'),
    'A grid of soft squares, a nod to the cement-tile floors of old Beirut homes.', hsize=128)

# Scheduled · Thu 22 Oct 12:00 · sand · Ideas · close-up of the texture
stories['ply-story-09-up-close'] = page(SU, 'Up close', f'Feel the {it("quilt.", SU)}', rcard('quilt-planter-small-tan.jpg', 840, 840, pos='50% 62%', zoom=1.9, label='3D render · close-up'),
    'Each diamond is a soft little pillow, built from hundreds of thin layers.', hsize=128)

# Scheduled · Fri 23 Oct 12:00 · terracotta · About
stories['ply-story-10-designed-here'] = page(C, 'Made in Lebanon', f'Designed here.<br>{it("Printed here.", C)}', rcard('tile-planter-small-tan.jpg', 760, 720),
    'Every piece is printed in Lebanon, one at a time, on our own printer.', hsize=120)

# Scheduled · Sat 24 Oct 20:00 · clay · How it works
stories['ply-story-11-seven-holes'] = page(R, 'How it drains', f'Seven holes.<br>{it("One hidden tray.", R)}', rcard('drainage-square.jpg', 840, 708, pos='top'),
    'Extra water runs into a tray under the pot. Twist it off to empty, click it back on.', hsize=116)

# Scheduled · Sun 25 Oct 20:00 · bone · About · First Layer how-to (no render)
stories['ply-story-12-join-first-layer'] = page(P, 'The First Layer', f'Want first {it("pick?", P)}',
    stagger([('1 · Send us a DM', I, P), ('2 · Type “FIRST”', C, P), ('3 · That’s it', SU, I)], size=56, pad='30px 54px', step=44, gap=26),
    'First look at every piece, first pick of the small first batch. Free, no commitment.', hsize=128)

# Scheduled · Mon 26 Oct 12:00 · charcoal · Ideas
stories['ply-story-13-dark-green'] = page(I, 'Colour', f'Dark {it("Green.", I)}', rcard('quilt-vase-green.jpg', 760, 840),
    'Deep and calm, like the cedar and pine forests in our mountains.', hsize=140)

# Scheduled · Tue 27 Oct 20:00 · sand · How it works · fact (no render)
leaf = f'''<svg width="420" height="420" viewBox="0 0 300 300"><circle cx="150" cy="150" r="150" fill="{P}"/>
<path d="M150 235 C 85 200, 75 115, 150 62 C 225 115, 215 200, 150 235 Z" fill="#6F7D5C"/><path d="M150 235 L150 92" stroke="{P}" stroke-width="6" stroke-linecap="round"/></svg>'''
stories['ply-story-14-pla-from-plants'] = page(SU, 'Did you know?', f'Made from {it("plants.", SU)}', leaf,
    'PLA, the material we print with, comes from plant starch such as corn or sugarcane.', hsize=128)

# Scheduled · Wed 28 Oct 12:00 · clay · Ideas
stories['ply-story-15-dried-stems'] = page(R, 'Styling', f'Dried stems,<br>{it("all year.", R)}', rcard('tile-vase-tan.jpg', 760, 780),
    'Our vases hold dried or faux stems: bunny tails, pampas, wheat. They last for months.', hsize=120)

# Scheduled · Wed 28 Oct 12:00 · bone · Ideas (21 Oct: medium planter dropped, one size now)
stories['ply-story-16-one-size'] = page(P, 'Size', f'Made for the {it("windowsill.", P)}', pair('tile-planter-small-green.jpg', 'quilt-planter-small-green.jpg'),
    'About 10 × 10 cm. Fits a nursery pot up to 8 cm: succulents, small cacti, herbs.', hsize=120)

# Scheduled · Sat 31 Oct 12:00 · terracotta · Christmas
stories['ply-story-17-housewarming'] = page(C, 'Gifting', f'A gift for a<br>{it("new home.", C)}', rcard('quilt-planter-small-charcoal.jpg', 760, 760),
    'A planter or a vase in a calm matte colour. First pieces arrive before Christmas.', hsize=112)

# Kit 4 (redone) · Thu 29 Oct · charcoal · Poll sticker with four options · Ideas
sw = '<div style="display:grid;grid-template-columns:repeat(4,190px);gap:28px">' + ''.join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:20px"><div style="width:180px;height:180px;border-radius:50%;background:{c};border:3px solid #4A463F"></div>'
    f'<div style="font-size:30px;font-weight:500;color:{SU};text-align:center;white-space:nowrap">{n}</div></div>'
    for c, n in (('#E9E4DA', 'Ivory White'), ('#2B2A27', 'Charcoal'), ('#3E5446', 'Dark Green'), ('#C2A27C', 'Desert Tan'))) + '</div>'
stories['ply-story-04-your-colour'] = page(I, 'Colours', f'Which one is {it("yours?", I)}', top(sw, 560),
    'Four colours that go together. Vote below.', hsize=128)

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
