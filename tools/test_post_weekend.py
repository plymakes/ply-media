import runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'showcase_posts_07_26.py'))
C, SU, R, I, P = m['C'], m['SU'], m['R'], m['I'], m['P']
html = m['page'](R, 'Weekend question', 'If you could 3D print anything…',
    m['stagger']([('A gift for someone', I, P), ('Something for home', P, I), ('A part to fix', C, P), ('Something wild', SU, I)], size=46, pad='24px 44px', step=36, gap=20),
    'Tell us in the comments. The best answers might become our first designs 👇', hsize=112)
root = Path(__file__).resolve().parent.parent
f = root / 'build' / 'weekend.html'; f.parent.mkdir(exist_ok=True)
f.write_text(f'<html><head><meta charset="utf-8"><style>{m["CSS"]}</style></head><body>{html}</body></html>')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto(f.as_uri()); pg.wait_for_timeout(300)
    pg.screenshot(path=str(root / 'posts' / 'ply-post-28-weekend-question.png')); b.close()
