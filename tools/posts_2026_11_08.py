"""Feed post for 22 Nov 2026 (weekly plan 8 Nov). Copied from posts_2026_11_01.py; only the content changes.
Usage: python3 tools/posts_2026_11_08.py -> build/<name>.png
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
# Sun 22 Nov 10:00 · clay · community / Independence Day (no product image)
posts['ply-post-62-independence-day'] = page(R, '22 November', f'Made in layers.<br>Made in {it("Lebanon.", R)}',
    m['stagger']([('Designed here', I, P), ('Printed here', P, I), ('Packed here', C, P)], size=50, pad='28px 52px', step=56, gap=26),
    'Happy Independence Day 🇱🇧 from a small family studio.', hsize=104)

out = ROOT / 'build'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for name, html in posts.items():
        f = out / f'{name}.html'; f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.goto(f.as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=str(out / f'{name}.png'))
    b.close()
print(len(posts), 'posts')
