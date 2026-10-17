"""Post 27: 'Join the First Layer' announcement, built with the showcase helpers."""
import runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P = m['C'], m['SU'], m['R'], m['I'], m['P']
html = m['page'](I, 'The First Layer', 'Be first in line.',
    m['stagger']([('First look at every new design', C, P), ('Priority slots for Christmas', SU, I), ('Order before everyone else', R, I)], size=42, pad='24px 44px', step=36, gap=20),
    'DM “FIRST” or comment 🧡 to join. Free, no commitment.', hsize=124)
root = Path(__file__).resolve().parent.parent
f = root / 'build' / 'first-layer.html'; f.parent.mkdir(exist_ok=True)
f.write_text(f'<html><head><meta charset="utf-8"><style>{m["CSS"]}</style></head><body>{html}</body></html>')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto(f.as_uri()); pg.wait_for_timeout(300)
    pg.screenshot(path=str(root / 'build' / 'ply-post-27-first-layer-v3.png')); b.close()
print('ok')
