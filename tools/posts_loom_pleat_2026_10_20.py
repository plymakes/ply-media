"""Feed posts for the two new pieces, Loom (soap rest) and Pleat (pot with a dish lid). 20 Oct 2026.
Calm, design-first, one idea per post (inspired by how Conifer Homewares presents products; Ply's own designs and words).
Every product image is a 3D render and is labelled on the image and in the caption.
Usage: python3 tools/posts_loom_pleat_2026_10_20.py [name-filter] -> build/<name>-v3.png
"""
import runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
flt = sys.argv[1:]
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P, page, CSS, OUT = m['C'], m['SU'], m['R'], m['I'], m['P'], m['page'], m['CSS'], m['OUT']
ROOT = Path(__file__).resolve().parent.parent
ACC_L, ACC_D = '#9C4421', '#D27A52'


def it(word, bg):
    return f'<i style="color:{ACC_D if bg == I else (P if bg == C else ACC_L)}">{word}</i>'


def img(name):
    return (ROOT / 'shop' / 'products' / name).as_uri()


def card(name, w=760, h=760, label='3D render'):
    return (f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:28px;overflow:hidden">'
            f'<img src="{img(name)}" style="width:100%;height:100%;object-fit:cover;display:block">'
            f'<div style="position:absolute;left:22px;bottom:22px;padding:9px 18px;border-radius:999px;background:rgba(239,234,226,.92);'
            f'color:{I};font-size:20px;font-weight:500;letter-spacing:.18em;text-transform:uppercase">{label}</div></div>')


posts = {}

posts['ply-post-56-meet-loom'] = page(SU, 'New · coming soon', f'Meet {it("Loom.", SU)}',
    card('loom-soap-rest-in-use-ivory.jpg', 720, 720),
    'A soap rest with slats that cradle the bar and let water fall straight through.', hsize=112)

posts['ply-post-57-why-slats'] = page(R, 'Loom soap rest', f'Why {it("slats?", R)}',
    card('loom-soap-rest-charcoal.jpg', 720, 720),
    'Water runs straight through, so the bar dries between washes. No puddle, no soft soap.', hsize=112)

posts['ply-post-58-meet-pleat'] = page(P, 'New · coming soon', f'Meet {it("Pleat.", P)}',
    card('pleat-pot-charcoal.jpg', 720, 720),
    'Fine pleats all the way round, and a softly rounded base.', hsize=112)

posts['ply-post-59-lid-is-a-dish'] = page(I, 'Pleat pot', f'The lid is {it("a dish.", I)}',
    card('pleat-pot-open-charcoal.jpg', 720, 720),
    'Rings on top. Cotton buds, hair ties or pens inside.', hsize=104)

two = (f'<div style="display:flex;gap:28px">{card("pleat-pot-four-colours.jpg", 430, 430, "3D renders")}'
       f'{card("loom-soap-rest-four-colours.jpg", 430, 430, "3D renders")}</div>')
posts['ply-post-60-four-colours-new-pieces'] = page(C, 'Loom + Pleat', f'Four colours,<br>{it("one family.", C)}', two,
    'Ivory White, Charcoal, Dark Green, Desert Tan. Made to sit next to the Quilt and Tile planters.', hsize=84)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for n, h in posts.items():
        if flt and not any(o in n for o in flt):
            continue
        f = OUT / f'{n}.html'
        f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>')
        pg.goto(f.as_uri())
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f'{n}-v3.png'))
    b.close()
print(len(posts), 'posts')
