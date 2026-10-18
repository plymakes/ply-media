"""Stories for the weekly plan of 18 Oct 2026 (copied from brand_posts_launch.py; only the content and the 1080x1920 Story canvas change).
Pre-launch rules: three stock pieces, no customisation, NO product images (type, palette and abstract shapes only).
Kit stories (posted by hand, October budget is full) leave the lower half free for an Instagram sticker.
Usage: python3 tools/stories_2026_10_18.py [name-filter] -> build/<name>.png
"""
import base64, runpy, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
flt = sys.argv[1:]
sys.argv = ['x', 'zzz-render-nothing']
m = runpy.run_path(str(Path(__file__).resolve().parent / 'atelier_posts.py'))
C, SU, R, I, P, page, stagger, CSS = m['C'], m['SU'], m['R'], m['I'], m['P'], m['page'], m['stagger'], m['CSS']
# Story canvas: 1080x1920 with Instagram safe zones (top ~250 px, bottom ~260 px)
CSS = CSS.replace('body{width:1080px;height:1350px', 'body{width:1080px;height:1920px').replace(
    '.p{width:1080px;height:1350px;padding:96px 104px 88px', '.p{width:1080px;height:1920px;padding:250px 104px 270px')
ROOT = Path(__file__).resolve().parent.parent
ACC_L, ACC_D = '#9C4421', '#D27A52'


def it(word, bg):
    return f'<i style="color:{ACC_D if bg == I else (P if bg == C else ACC_L)}">{word}</i>'


def layers_bar(n, w0, w1, h, cols, gap=6):
    return '<div style="display:flex;flex-direction:column;align-items:center;gap:%dpx">' % gap + ''.join(
        f'<div style="width:{w0 + (w1 - w0) * i / max(1, n - 1):.0f}px;height:{h}px;border-radius:{h/2}px;background:{cols[i % len(cols)]}"></div>' for i in range(n)) + '</div>'


def top(html, space=520):
    """Keep the artwork high and leave `space` px empty below it for a sticker."""
    return f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-start;height:100%;width:100%;padding-top:60px">{html}<div style="height:{space}px"></div></div>'


stories = {}

# Kit 1 · Wed 21 Oct · bone · Quiz sticker
stories['ply-story-01-what-does-ply-mean'] = page(P, 'Quick quiz', f'What does<br>{it("ply", P)} mean?',
    top(layers_bar(7, 260, 560, 24, [I, SU, C], gap=10)),
    'Tap your answer. Hint: how do we print?', hsize=124)

# Kit 2 · Sat 24 Oct · sand · First Layer reminder
stories['ply-story-02-be-first'] = page(SU, 'The First Layer', f'Be first in {it("line.", SU)}',
    stagger([('First look at every piece', I, P), ('First pick of the first batch', P, I), ('Order before everyone else', C, P)], size=46, pad='26px 46px', step=36, gap=22),
    'DM us “FIRST” to join. Free, no commitment.', hsize=128)

leaf = f'''<svg width="320" height="320" viewBox="0 0 300 300"><circle cx="150" cy="150" r="150" fill="{P}"/>
<path d="M150 230 C 90 200, 80 120, 150 70 C 220 120, 210 200, 150 230 Z" fill="#6F7D5C"/><path d="M150 230 L150 95" stroke="{P}" stroke-width="6" stroke-linecap="round"/></svg>'''
stems = f'''<svg width="320" height="320" viewBox="0 0 300 300"><circle cx="150" cy="150" r="150" fill="{I}"/>''' + ''.join(
    f'<path d="M150 240 Q {150 + dx*0.4} 160 {150 + dx} {t}" stroke="{SU}" stroke-width="5" fill="none" stroke-linecap="round"/><ellipse cx="{150 + dx}" cy="{t - 14}" rx="11" ry="22" fill="{P}" transform="rotate({dx/3} {150 + dx} {t - 14})"/>'
    for dx, t in ((-60, 90), (-15, 70), (25, 82), (65, 100))) + '</svg>'
cap = lambda t: f'<div style="font-size:42px;font-weight:700;margin-top:26px;text-align:center">{t}</div>'

# Kit 3 · Mon 26 Oct · clay · Poll sticker
stories['ply-story-03-plants-or-flowers'] = page(R, 'This or that?', f'Plants or dried {it("flowers?", R)}',
    top(f'<div style="display:flex;gap:72px"><div>{leaf}{cap("Plants")}</div><div>{stems}{cap("Dried flowers")}</div></div>', 440),
    'Vote below. It decides our first photos.', hsize=124)

sw = '<div style="display:flex;gap:44px">' + ''.join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px"><div style="width:230px;height:230px;border-radius:50%;background:{c};{"border:3px solid #4A463F;" if c == "#26241F" else ""}"></div><div style="font-size:34px;font-weight:500;color:{SU}">{n}</div></div>'
    for c, n in ((P, 'Bone'), ('#26241F', 'Charcoal'), (C, 'Terracotta'))) + '</div>'

# Kit 4 · Thu 29 Oct · charcoal · Poll sticker
stories['ply-story-04-your-colour'] = page(I, 'Colours', f'Which one is {it("yours?", I)}', top(sw, 460),
    'Three colours that go together. Vote below.', hsize=128)

# Scheduled · Sun 1 Nov 10:00 · terracotta
stories['ply-story-05-november'] = page(C, 'November', f'The printer<br>lands {it("this month.", C)}',
    layers_bar(11, 300, 700, 28, [P, SU, R], gap=12),
    'Three pieces are coming. DM “FIRST” for first pick of the first batch.', hsize=110)

# Scheduled · Thu 5 Nov 18:00 · bone · answer to the 4 Nov quiz
stories['ply-story-06-quiz-answer'] = page(P, 'Yesterday’s quiz', f'600 {it("layers.", P)}',
    f'''<div style="display:flex;flex-direction:column;align-items:center;gap:56px">
<div style="font-family:IS,Georgia,serif;font-size:96px;line-height:1;letter-spacing:-.02em">12 cm ÷ 0.2 mm</div>
{layers_bar(9, 620, 620, 18, [I, SU, C], gap=10)}
<div style="font-size:38px;font-weight:500;color:#6E6A63">= 600 layers, stacked one by one</div></div>''',
    'That’s a 12 cm piece. Did you get it right?', hsize=170)

out = ROOT / 'build'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for name, html in stories.items():
        if flt and not any(f in name for f in flt):
            continue
        f = out / f'{name}.html'; f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.goto(f.as_uri()); pg.wait_for_timeout(400); pg.screenshot(path=str(out / f'{name}.png'))
    b.close()
print(len(stories), 'stories')
