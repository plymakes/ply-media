"""Growth Reels batch, 1 Nov 2026 (weekly plan). One Reel a day at 18:00, 9-15 Nov. Copied from reels_growth_2026_10_25.py; only the content changes.
Same engine as reels.py; images from shop/products (3D renders, always labelled). Hook text is visible from frame 0
so the feed preview and cover show it. Usage: python3 tools/reels_growth_2026_11_01.py [name-filter]
-> build/<name>-v3.mp4 (+ -v3-preview.png)
"""
import runpy, sys
from pathlib import Path
flt = sys.argv[1:]
m = runpy.run_path(str(Path(__file__).resolve().parent / 'reels.py'), run_name='lib')
C, SU, R, I, P, end_card, render = m['C'], m['SU'], m['R'], m['I'], m['P'], m['end_card'], m['render']
ROOT = Path(__file__).resolve().parent.parent
ACC_D, ACC_L = '#D27A52', '#9C4421'
RBG_TOP, RBG_BOT = '#DDD4C5', '#E6DDCC'   # background of the studio renders


def img(name):
    return (ROOT / 'shop' / ('banners' if name.startswith('drainage') else 'products') / name).as_uri()


def tag(text='3D render', pos='left:24px;bottom:24px'):
    return (f'<div style="position:absolute;{pos};padding:10px 20px;border-radius:999px;background:rgba(239,234,226,.92);'
            f'color:{I};font-size:22px;font-weight:500;letter-spacing:.18em;text-transform:uppercase">{text}</div>')


def card(id_, src, left, top, w, h, op=0, pos='center'):
    return (f'<div id="{id_}" class="abs" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:28px;overflow:hidden;opacity:{op}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block">{tag()}</div>')


def label(text, col, top=230):
    return f'<div id="lab" class="abs label" style="left:100px;top:{top}px;color:{col}">{text}</div>'


def hook(html, col, size=112, top=290):
    """Hook headline: visible from frame 0 (opacity 1), only drifts a little."""
    return f'<div id="hk" class="abs h" style="left:100px;right:100px;top:{top}px;font-size:{size}px;color:{col}">{html}</div>'


def line(id_, html, col, top, size=46, weight=500):
    return f'<div id="{id_}" class="abs" style="left:100px;right:100px;top:{top}px;font-size:{size}px;font-weight:{weight};line-height:1.25;color:{col};opacity:0">{html}</div>'


def endc(bg, fg, l2):
    return end_card(bg, fg, 'Made in layers.<br>Made in Lebanon.', l2).replace('font-size:120px', 'font-size:92px')


HOOK_JS = "document.getElementById('hk').style.transform=`translateY(${-8*prog(t,0,1.2)}px)`;"
END_JS = "const e=prog(t,{a},{a}+.4); document.getElementById('end').style.opacity=e; show('e1',prog(t,{a}+.2,{a}+.7),40); show('e2',prog(t,{a}+.5,{a}+1.0),40);"


def slide_card(id_, a, dx=0, dy=60):
    return (f"{{const p=prog(t,{a},{a}+.6); const e=document.getElementById('{id_}'); e.style.opacity=p; "
            f"e.style.transform=`translate(${{(1-p)*{dx}}}px,${{(1-p)*{dy}}}px) scale(${{.96+.04*p}})`;}}")


REELS = []


def zoom_reel(name, file, hook_html, reveal, fx, fy, s0=3.4, hook_col=None, shade=True, bg=(RBG_TOP, RBG_BOT), dur=8.0):
    """Starts as an extreme close-up (fx, fy = focus point in % of the image) and pulls back to the whole piece. Loops."""
    return dict(name=name, dur=dur, html=f'''
<div class="abs" style="inset:0;background:linear-gradient({bg[0]} 0,{bg[0]} 420px,{bg[1]} 1500px,{bg[1]} 100%)"></div>
<div id="zw" class="abs" style="left:0;top:420px;width:1080px;height:1080px;transform-origin:{fx}% {fy}%;
  -webkit-mask-image:linear-gradient(transparent 0,#000 6%,#000 94%,transparent 100%)">
  <img src="{img(file)}" style="width:100%;height:100%;display:block"></div>
<div id="sh" class="abs" style="left:0;right:0;top:0;height:640px;background:linear-gradient(rgba(28,27,25,.55),rgba(28,27,25,0));display:{'block' if shade else 'none'}"></div>
{hook(hook_html, hook_col or P, 108, 260)}
<div id="rv" class="abs" style="left:100px;right:100px;top:270px;opacity:0">
  <div class="h" style="font-size:88px;color:{I}">{reveal}</div>
  <div style="display:inline-block;margin-top:22px;padding:10px 20px;border-radius:999px;background:{I};color:{P};font-size:24px;font-weight:500;letter-spacing:.18em">3D RENDER</div></div>
''', js=f'''
window.setT=t=>{{ {HOOK_JS}
  const z=prog(t,0.9,5.6); const s={s0}-({s0}-1)*z;
  document.getElementById('zw').style.transform=`scale(${{s}})`;
  const h=prog(t,2.6,3.2); document.getElementById('hk').style.opacity=1-h; document.getElementById('sh').style.opacity=1-h;
  show('rv',prog(t,5.4,6.0),30);
}};''')


def cta(id_, big, small, fg, acc, top=820):
    return (f'<div id="{id_}" class="abs" style="left:0;right:0;top:{top}px;text-align:center;opacity:0">'
            f'<div class="h" style="font-size:100px;color:{fg}">{big}</div>'
            f'<div style="font-size:44px;font-weight:500;color:{acc};margin-top:34px;line-height:1.3">{small}</div>'
            f'<div style="font-size:28px;font-weight:500;letter-spacing:.22em;color:{fg};opacity:.75;margin-top:60px">@PLYMAKES</div></div>')


def pill(id_, text, top, bg, fg, left=100, size=54, op=0):
    return (f'<div id="{id_}" class="abs" style="left:{left}px;top:{top}px;padding:26px 48px;border-radius:999px;'
            f'background:{bg};color:{fg};font-size:{size}px;font-weight:500;opacity:{op}">{text}</div>')


# ---------- 28: Tag the one who leaves the soap in a puddle (Mon 9 Nov, Loom follow-up to the best-reach Reel, send-worthy) ----------
REELS.append(dict(name='ply-reel-28-soap-puddle-tag', dur=10.0, html=f'''
<div class="abs" style="inset:0;background:{SU}"></div>
{label('Bathroom', I)}
{hook('Tag the one who leaves<br>the soap in a <i style="color:{ACC_L}">puddle.</i>', I, 80)}
{card('c1', img('loom-soap-rest-in-use-charcoal.jpg'), 100, 640, 880, 620, op=1)}
{line('l1', 'Loom has slats, so the water runs through.', I, 1300, 42)}
{line('l2', 'The bar dries between washes.', I, 1300, 42)}
{cta('cta', 'Send this<br>to them.', 'Loom soap rest.<br>Designed and printed in Lebanon.', I, ACC_L)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const out=prog(t,6.6,7.0);
  show('l1',Math.min(prog(t,2.0,2.5),1-prog(t,4.0,4.3)),30);
  show('l2',Math.min(prog(t,4.3,4.8),1-out),30);
  const c=document.getElementById('c1'); c.style.opacity=1-out; c.style.transform=`scale(${1+.04*prog(t,0,6.6)})`;
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,7.0,7.6),40);
};'''))

# ---------- 29: Building Ply ep 4: the first print isn't for sale (Tue 10 Nov, growth, follow) ----------
checks = ['1 · Does the tray twist off?', '2 · Do all seven holes drain?', '3 · Are the layers even?', '4 · Does it stand flat?']
chk = ''.join(pill(f'k{k}', t, 640 + k * 160, [I, C, SU, R][k], [P, P, I, I][k], size=48) for k, t in enumerate(checks))
REELS.append(dict(name='ply-reel-29-building-ply-ep4', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Building Ply · episode 4', ACC_L)}
{hook('The first print<br>isn’t for <i style="color:{ACC_L}">sale.</i>', I, 104)}
{card('c1', img('quilt-planter-small-ivory.jpg'), 100, 640, 880, 620, op=1)}
{chk}
{line('l1', 'It’s a test. We check four things:', I, 560, 42)}
{endc(I, P, 'Follow for<br>the first test.')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const sw=prog(t,2.4,2.8); document.getElementById('c1').style.opacity=1-sw;
  document.getElementById('hk').style.opacity=1-sw*0.0;
  const out=prog(t,7.6,7.9);
  show('l1',Math.min(prog(t,2.6,3.0),1-out),20);
  for(let k=0;k<4;k++){ const a=3.0+k*0.9; const e=document.getElementById('k'+k); const p=prog(t,a,a+.4);
    e.style.opacity=Math.min(p,1-out); e.style.transform=`translateX(${(1-p)*-60}px)`; }
  ''' + END_JS.format(a=7.9) + '''
};'''))

# ---------- 30: Things that don't survive a car in August (Wed 11 Nov, Lebanese relatable care tip, follow) ----------
items = [('Chocolate', I, P), ('Lipstick', I, P), ('Crayons', I, P), ('Our planters', C, P)]
it_html = ''.join(pill(f'i{k}', t, 640 + k * 160, b, f, op=1 if k == 0 else 0) for k, (t, b, f) in enumerate(items))
REELS.append(dict(name='ply-reel-30-car-in-august', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{R}"></div>
{label('Lebanese summer', I)}
{hook('Things that don’t survive<br>a car in <i style="color:{ACC_L}">August:</i>', I, 76)}
<div id="sun" class="abs" style="left:620px;top:620px;transform:scale(.8);transform-origin:top left">{'<svg width="420" height="420" viewBox="0 0 200 200"><circle cx="100" cy="100" r="46" fill="' + C + '"/>' + ''.join(f'<rect x="96" y="14" width="8" height="30" rx="4" fill="{C}" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 45)) + '</svg>'}</div>
{it_html}
{card('c1', img('quilt-vase-tan.jpg'), 100, 640, 880, 620)}
{line('l1', 'PLA softens around 55 °C.<br>Keep it indoors or in the shade.', I, 1300, 42)}
{cta('cta', 'Follow for<br>more care tips.', 'Made in layers.<br>Made in Lebanon.', I, ACC_L)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  document.getElementById('sun').style.transform=`scale(.8) rotate(${t*6}deg)`;
  const sw=prog(t,5.4,5.8);
  for(let k=0;k<4;k++){ const a=0.6+k*1.1; const e=document.getElementById('i'+k); const p=k==0?1:prog(t,a,a+.4);
    e.style.opacity=Math.min(p,1-sw); e.style.transform=`translateX(${(1-p)*-60}px)`; }
  document.getElementById('sun').style.opacity=1-sw;
  const out=prog(t,8.2,8.6);
  const c=document.getElementById('c1'); const q=prog(t,5.6,6.2); c.style.opacity=Math.min(q,1-out); c.style.transform=`translateY(${(1-q)*60}px)`;
  show('l1',Math.min(prog(t,6.2,6.8),1-out),30);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,8.6,9.2),40);
};'''))

# ---------- 31: Your teta's floor, but make it a planter (Thu 12 Nov, heritage, follow) ----------
def tile_svg(k):
    cols = [(SU, C), (R, I), (P, '#3E5446'), (SU, '#3E5446'), (R, C), (P, I)]
    bg, fg = cols[k % len(cols)]
    return (f'<svg width="280" height="200" viewBox="0 0 140 100"><rect width="140" height="100" fill="{bg}"/>'
            f'<path d="M70 8 L112 50 L70 92 L28 50 Z" fill="none" stroke="{fg}" stroke-width="6"/>'
            f'<circle cx="70" cy="50" r="12" fill="{fg}"/><circle cx="0" cy="0" r="16" fill="{fg}"/><circle cx="140" cy="0" r="16" fill="{fg}"/>'
            f'<circle cx="0" cy="100" r="16" fill="{fg}"/><circle cx="140" cy="100" r="16" fill="{fg}"/></svg>')
grid = ''.join(f'<div id="g{k}" class="abs" style="left:{100 + (k % 3) * 300}px;top:{640 + (k // 3) * 210}px;width:280px;height:200px;border-radius:12px;overflow:hidden">{tile_svg(k + k // 3)}</div>' for k in range(9))
REELS.append(dict(name='ply-reel-31-teta-floor', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{label('Beirut floors', SU)}
{hook('Your teta’s floor,<br>but make it a <i style="color:{ACC_D}">planter.</i>', P, 88)}
{grid}
{card('c1', img('tile-planter-small-ivory.jpg'), 100, 640, 880, 620)}
{line('l1', 'The Tile planter: the same grid, softened.<br>Coming in November.', P, 1300, 40)}
{cta('cta', 'Follow for<br>the first real one.', 'Made in layers.<br>Made in Lebanon.', P, ACC_D)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const sw=prog(t,3.8,4.2);
  for(let k=0;k<9;k++){ const a=1.0+k*0.2; const w=prog(t,a,a+.3)-prog(t,a+.3,a+.6); const e=document.getElementById('g'+k);
    e.style.opacity=1-sw; e.style.transform=`translateY(${-14*w}px)`; }
  const out=prog(t,8.0,8.4);
  const c=document.getElementById('c1'); const q=prog(t,4.0,4.6); c.style.opacity=Math.min(q,1-out); c.style.transform=`scale(${.96+.04*q})`;
  show('l1',Math.min(prog(t,4.6,5.2),1-out),30);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,8.4,9.0),40);
};'''))

# ---------- 32: Secret Santa, sorted (Fri 13 Nov, product Reel, gifting, DM FIRST) ----------
gifts = [('pleat-pot-tan.jpg', 'For the one with too many rings.'),
         ('quilt-vase-ivory.jpg', 'For the one who forgets to water.'),
         ('loom-soap-rest-green.jpg', 'For the one who loves a tidy sink.')]
gc = ''.join(card(f'c{k}', img(f), 100, 640, 880, 620, op=1 if k == 0 else 0) + line(f't{k}', txt, I, 1300, 44) for k, (f, txt) in enumerate(gifts))
REELS.append(dict(name='ply-reel-32-secret-santa', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Gift idea', ACC_L)}
{hook('Secret Santa,<br><i style="color:{ACC_L}">sorted.</i>', I, 112)}
{gc}
{endc(I, P, 'Designed and printed in Lebanon.<br>Coming soon. DM “FIRST”')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<3;k++){ const a=1.3+k*2.0; const inn=k==0?1:prog(t,a,a+.5), out=k<2?prog(t,a+2.0,a+2.3):prog(t,7.6,7.9);
    const e=document.getElementById('c'+k); e.style.opacity=Math.min(inn,1-out); e.style.transform=`translateY(${(1-inn)*60}px) scale(${.96+.04*inn})`;
    show('t'+k,Math.min(k==0?prog(t,0.6,1.1):prog(t,a+.3,a+.8),1-out),30); }
  ''' + END_JS.format(a=7.9) + '''
};'''))

# ---------- 33: Where does the water go? (Sat 14 Nov, product Reel, drip tray, DM FIRST) ----------
steps = ['Seven holes in a raised floor.', 'A drip tray hidden underneath.', 'Twist it off, empty it, click it back.']
st = ''.join(line(f's{k}', s, P, 1400, 44) for k, s in enumerate(steps))
REELS.append(dict(name='ply-reel-33-where-water-goes', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{C}"></div>
{label('How it drains', P)}
{hook('Where does the<br>water <i>go?</i>', P, 112)}
{card('c1', img('quilt-planter-small-charcoal.jpg'), 100, 640, 880, 700, op=1)}
{card('c2', img('drainage-square.jpg'), 100, 640, 880, 700, pos='top')}
{st}
{cta('cta', 'DM us<br>“FIRST”', 'For first pick of the Quilt<br>and Tile planters.', P, I)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const out=prog(t,8.0,8.4);
  const sw=prog(t,2.2,2.7); document.getElementById('c1').style.opacity=1-sw;
  const c2=document.getElementById('c2'); c2.style.opacity=Math.min(sw,1-out); c2.style.transform=`scale(${1+.05*prog(t,2.2,8)})`;
  for(let k=0;k<3;k++){ const a=2.6+k*1.8; show('s'+k,Math.min(prog(t,a,a+.4),k<2?1-prog(t,a+1.6,a+1.8):1-out),20); }
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,8.4,9.0),40);
};'''))

# ---------- 34: Quilt or Tile? (Sun 15 Nov, this-or-that vote, comment Q or T) ----------
pairs = [('quilt-planter-small-green.jpg', 'tile-planter-small-tan.jpg', 'Planters'),
         ('quilt-vase-charcoal.jpg', 'tile-vase-charcoal.jpg', 'Vases')]
pc = ''
for k, (a, b, n) in enumerate(pairs):
    pc += card(f'a{k}', img(a), 100, 600, 430, 640, op=1 if k == 0 else 0) + card(f'b{k}', img(b), 550, 600, 430, 640, op=1 if k == 0 else 0)
    pc += f'<div id="n{k}" class="abs" style="left:100px;top:1275px;font-size:40px;font-weight:500;color:{P};opacity:{1 if k == 0 else 0}">{n}</div>'
REELS.append(dict(name='ply-reel-34-quilt-or-tile', dur=9.5, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{label('This or that', SU)}
{hook('Quilt or<br><i style="color:{ACC_D}">Tile?</i>', P, 116)}
{pc}
<div id="la" class="abs" style="left:100px;top:540px;width:430px;text-align:center;font-size:30px;font-weight:500;letter-spacing:.2em;color:{SU}">Q · QUILT</div>
<div id="lb" class="abs" style="left:550px;top:540px;width:430px;text-align:center;font-size:30px;font-weight:500;letter-spacing:.2em;color:{SU}">T · TILE</div>
{cta('cta', 'Comment<br>Q or T.', 'One letter is enough.', P, ACC_D)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<2;k++){ const a=0.2+k*3.0; const out=k<1?prog(t,3.2,3.5):prog(t,6.4,6.7);
    ['a','b'].forEach((s,j)=>{const e=document.getElementById(s+k); const q=k==0?1:prog(t,a+j*.2,a+.5+j*.2); e.style.opacity=Math.min(q,1-out); e.style.transform=`translateY(${(1-q)*50}px)`;});
    show('n'+k,Math.min(k==0?1:prog(t,a,a+.5),1-out),20); }
  const o=prog(t,6.4,6.7); ['la','lb'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  show('cta',prog(t,6.8,7.4),40);
};'''))

if __name__ == '__main__':
    for r in REELS:
        if not flt or any(f in r['name'] for f in flt):
            render(r)
