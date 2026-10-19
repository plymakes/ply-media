"""Reels built from the Quilt and Tile studio renders (19 Oct 2026: Geoffry allowed renders on Instagram, labelled as 3D renders).
Same engine as reels.py / reels_brand.py; images come from shop/products and shop/banners.
Usage: python3 tools/reels_renders_2026_10_19.py [name-filter] -> build/<name>-v3.mp4 (+ -v3-preview.png)
"""
import runpy, sys
from pathlib import Path
flt = sys.argv[1:]
m = runpy.run_path(str(Path(__file__).resolve().parent / 'reels.py'), run_name='lib')
C, SU, R, I, P, end_card, render = m['C'], m['SU'], m['R'], m['I'], m['P'], m['end_card'], m['render']
ROOT = Path(__file__).resolve().parent.parent
ACC_D, ACC_L = '#D27A52', '#9C4421'


def img(name):
    folder = 'banners' if name.startswith('drainage') else 'products'
    return (ROOT / 'shop' / folder / name).as_uri()


def endc(bg, fg, l2):
    return end_card(bg, fg, 'Made in layers.<br>Made in Lebanon.', l2).replace('font-size:120px', 'font-size:92px')


def head(label, title, fg, lab):
    return (f'<div id="lab" class="abs label" style="left:100px;top:180px;color:{lab}">{label}</div>'
            f'<div id="t1" class="abs h" style="left:100px;right:100px;top:250px;font-size:116px;color:{fg}">{title}</div>')


def tag(text='3D render'):
    """Small pill inside an image card so every render is labelled."""
    return (f'<div style="position:absolute;left:24px;bottom:24px;padding:10px 20px;border-radius:999px;background:rgba(239,234,226,.92);'
            f'color:{I};font-size:22px;font-weight:500;letter-spacing:.18em;text-transform:uppercase">{text}</div>')


def card(id_, src, left, top, w, h, extra='', pos='center'):
    return (f'<div id="{id_}" class="abs" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:28px;overflow:hidden;opacity:0;{extra}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block">{tag()}</div>')


HEAD_JS = "show('lab',prog(t,0,.6),30); show('t1',prog(t,.2,.9),40);"
END_JS = "const e=prog(t,{a},{a}+.5); document.getElementById('end').style.opacity=e; show('e1',prog(t,{a}+.3,{a}+.9),40); show('e2',prog(t,{a}+.7,{a}+1.3),40);"

# ---------- Reel 10: Quilt or Tile? ----------
reel10 = dict(name='ply-reel-10-quilt-or-tile', dur=10.5, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{head('Quilt or Tile?', 'Two textures.<br><i style="color:{ACC_D}">Which one?</i>', P, SU)}
{card('cq', img('quilt-planter-medium-charcoal.jpg'), 90, 640, 430, 560)}
{card('ct', img('tile-planter-medium-charcoal.jpg'), 560, 640, 430, 560)}
<div id="lq" class="abs" style="left:90px;width:430px;top:1230px;text-align:center;color:{P};opacity:0"><div class="h" style="font-size:120px">Q</div><div style="font-size:36px;font-weight:500;letter-spacing:.22em;margin-top:6px">QUILT</div></div>
<div id="lt" class="abs" style="left:560px;width:430px;top:1230px;text-align:center;color:{P};opacity:0"><div class="h" style="font-size:120px">T</div><div style="font-size:36px;font-weight:500;letter-spacing:.22em;margin-top:6px">TILE</div></div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1470px;font-size:46px;font-weight:500;color:{P};opacity:0">Same planter, two textures.<br>Comment Q or T.</div>
{endc(C, P, 'Comment Q or T,<br>then DM “FIRST” for first pick')}
''', js='''
window.setT=t=>{ ''' + HEAD_JS + '''
  const a=prog(t,1.0,1.7), b=prog(t,1.6,2.3);
  const q=document.getElementById('cq'), w=document.getElementById('ct');
  q.style.opacity=a; q.style.transform=`translateX(${(1-a)*-520}px)`;
  w.style.opacity=b; w.style.transform=`translateX(${(1-b)*520}px)`;
  show('lq',prog(t,2.3,2.9),30); show('lt',prog(t,2.6,3.2),30);
  const pulse=t>3.6&&t<7.2?Math.floor((t-3.6)/0.9)%2:-1;
  q.style.boxShadow=pulse===0?`0 0 0 8px ${'#D27A52'}`:'none'; w.style.boxShadow=pulse===1?`0 0 0 8px ${'#D27A52'}`:'none';
  show('t2',prog(t,3.4,4.0),30); ''' + END_JS.format(a=7.4) + '''
};''')

# ---------- Reel 11: four colours ----------
cols = [('ivory', 'Ivory White', '#E9E4DA'), ('charcoal', 'Charcoal', '#2B2A27'), ('green', 'Dark Green', '#3E5446'), ('tan', 'Desert Tan', '#C2A27C')]
big = ''.join(card(f'b{k}', img(f'quilt-planter-small-{c}.jpg'), 160, 560, 760, 760) for k, (c, _, _) in enumerate(cols))
names = ''.join(f'<div id="n{k}" class="abs" style="left:0;right:0;top:1360px;display:flex;justify-content:center;align-items:center;gap:22px;opacity:0">'
                f'<span style="width:44px;height:44px;border-radius:50%;background:{sw};border:2px solid #8A857C"></span>'
                f'<span class="h" style="font-size:72px;color:{I}">{n}</span></div>' for k, (_, n, sw) in enumerate(cols))
grid = ''.join(f'<div id="g{k}" class="abs" style="left:{160 + (k % 2) * 390}px;top:{560 + (k // 2) * 390}px;width:370px;height:370px;border-radius:24px;overflow:hidden;opacity:0">'
               f'<img src="{img(f"quilt-planter-small-{c}.jpg")}" style="width:100%;height:100%;object-fit:cover;display:block">'
               f'<div style="position:absolute;left:18px;bottom:18px;padding:8px 16px;border-radius:999px;background:rgba(239,234,226,.92);color:{I};font-size:22px;font-weight:500">{n}</div></div>'
               for k, (c, n, _) in enumerate(cols))
reel11 = dict(name='ply-reel-11-four-colours', dur=11.5, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{head('Four colours', 'Pick <i style="color:{ACC_L}">yours.</i>', I, I)}
{big}{names}{grid}
<div id="gt" class="abs" style="left:160px;width:760px;top:1350px;font-size:22px;font-weight:500;letter-spacing:.18em;color:#6E6A63;opacity:0">3D RENDERS · QUILT PLANTER, SMALL</div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1420px;font-size:46px;font-weight:500;color:{I};opacity:0">Chosen to sit together.<br>Comment the one that’s yours.</div>
{endc(I, P, 'Which one is yours?<br>DM “FIRST” to join the First Layer')}
''', js='''
window.setT=t=>{ ''' + HEAD_JS + '''
  for(let k=0;k<4;k++){ const a=0.9+k*1.15;
    const inn=prog(t,a,a+.4), out=k<3?prog(t,a+1.15,a+1.5):prog(t,5.6,5.9);
    document.getElementById('b'+k).style.opacity=Math.min(inn,1-out);
    show('n'+k,Math.min(prog(t,a+.1,a+.4),1-out),20);
    const g=prog(t,5.8+k*.15,6.2+k*.15); const ge=document.getElementById('g'+k); ge.style.opacity=g; ge.style.transform=`scale(${.9+.1*g})`; }
  show('gt',prog(t,6.3,6.7)); show('t2',prog(t,6.6,7.2),30); ''' + END_JS.format(a=8.8) + '''
};''')

# ---------- Reel 12: seven holes, hidden tray ----------
steps = [('1', 'Seven holes in a raised floor'), ('2', 'A drip tray hidden underneath'), ('3', 'Twist it off, empty, click it back')]
lines = ''.join(f'<div id="s{k}" class="abs" style="left:100px;right:100px;top:{1330 + k * 78}px;display:flex;align-items:baseline;gap:26px;opacity:0">'
                f'<span class="h" style="font-size:64px;color:{ACC_L}">{n}</span><span style="font-size:42px;font-weight:500;color:{I}">{t}</span></div>' for k, (n, t) in enumerate(steps))
reel12 = dict(name='ply-reel-12-hidden-tray', dur=12.0, html=f'''
<div class="abs" style="inset:0;background:{SU}"></div>
{head('How it drains', 'No saucer<br><i style="color:{ACC_L}">on show.</i>', I, I)}
{card('cd', img('drainage-square.jpg'), 100, 540, 880, 742, pos='top')}
{lines}
{endc(I, P, 'Roots never sit in water.<br>DM “FIRST” to join the First Layer')}
''', js='''
window.setT=t=>{ ''' + HEAD_JS + '''
  const c=prog(t,1.0,1.7); const d=document.getElementById('cd'); d.style.opacity=c; d.style.transform=`scale(${.94+.06*c})`;
  for(let k=0;k<3;k++) show('s'+k,prog(t,2.2+k*1.4,2.7+k*1.4),30);
  ''' + END_JS.format(a=8.6) + '''
};''')

# ---------- Reel 13: why tiles (old Beirut floors) ----------
N, S, G = 6, 112, 10
x0 = (1080 - (N * S + (N - 1) * G)) // 2
motif_cols = [(P, C), (SU, I), (R, P), (P, I)]
tiles = ''
for r in range(N):
    for c in range(N):
        bg, dot = motif_cols[(r + c) % 4] if (r + c) % 2 else motif_cols[(r * 3 + c) % 4]
        inner = (f'<div style="position:absolute;inset:22px;border-radius:50%;background:{dot}"></div>' if (r + c) % 2 == 0 else
                 f'<div style="position:absolute;left:50%;top:50%;width:52px;height:52px;margin:-26px 0 0 -26px;transform:rotate(45deg);background:{dot}"></div>')
        tiles += (f'<div class="tl abs" data-d="{r + c}" style="left:{x0 + c * (S + G)}px;top:{680 + r * (S + G)}px;width:{S}px;height:{S}px;border-radius:18px;'
                  f'background:{bg};overflow:hidden;opacity:0">{inner}</div>')
reel13 = dict(name='ply-reel-13-why-tiles', dur=11.5, html=f'''
<div class="abs" style="inset:0;background:{C}"></div>
{head('Why tiles?', 'Beirut floors.<br><i style="color:{P}">A new shape.</i>', P, P)}
<div id="grid">{tiles}</div>
{card('cp', img('tile-planter-medium-tan.jpg'), 170, 660, 740, 740)}
<div id="t2" class="abs" style="left:100px;right:100px;top:1450px;font-size:44px;font-weight:500;color:{P};opacity:0">The Tile planter borrows the grid of<br>the cement tiles in old Lebanese homes.</div>
{endc(I, P, 'First prints in November.<br>DM “FIRST” to join the First Layer')}
''', js='''
const tl=[...document.querySelectorAll('.tl')];
window.setT=t=>{ ''' + HEAD_JS + '''
  const out=prog(t,3.6,4.2);
  tl.forEach(e=>{ const d=+e.dataset.d; const p=prog(t,1.0+d*0.16,1.35+d*0.16); e.style.opacity=Math.min(p,1-out); e.style.transform=`scale(${.6+.4*p})`; });
  const c=prog(t,4.0,4.7); const cp=document.getElementById('cp'); cp.style.opacity=c; cp.style.transform=`scale(${.92+.08*c})`;
  show('t2',prog(t,5.0,5.6),30); ''' + END_JS.format(a=8.6) + '''
};''')

for r in (reel10, reel11, reel12, reel13):
    if not flt or any(f in r['name'] for f in flt):
        render(r)
