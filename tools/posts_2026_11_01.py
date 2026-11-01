"""Feed post for 15 Nov 2026 (weekly plan 1 Nov). Copied from posts_loom_pleat_2026_10_20.py; only the content changes.
Usage: python3 tools/posts_2026_11_01.py -> build/<name>.png
"""
import runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P, page, stagger, CSS = m['C'], m['SU'], m['R'], m['I'], m['P'], m['page'], m['stagger'], m['CSS']
ROOT = Path(__file__).resolve().parent.parent
ACC_L, ACC_D = '#9C4421', '#D27A52'


def it(word, bg):
    return f'<i style="color:{ACC_D if bg == I else (P if bg == C else ACC_L)}">{word}</i>'


posts = {}
# Sun 15 Nov 10:00 · sand · community / made in Lebanon (no product image)
posts['ply-post-61-designed-printed-packed'] = page(SU, 'Made in Lebanon', f'Designed here.<br>Printed here.<br>{it("Packed here.", SU)}',
    stagger([('Quilt & Tile planters', I, P), ('Quilt & Tile vases', P, I), ('Loom soap rest', R, I), ('Pleat pot', C, P)], size=48, pad='28px 50px', step=48, gap=24),
    'One family, one printer, start to finish in Lebanon.', hsize=104)

out = ROOT / 'build'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for name, html in posts.items():
        f = out / f'{name}.html'; f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.goto(f.as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=str(out / f'{name}.png'))
    b.close()
print(len(posts), 'posts')
