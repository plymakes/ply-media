"""Growth Reels batch, 8 Nov 2026 (weekly plan). One Reel a day at 18:00, 16-22 Nov. Copied from reels_growth_2026_11_01.py; only the content changes.
Same engine as reels.py; images from shop/products (3D renders, always labelled). Hook text is visible from frame 0
so the feed preview and cover show it. Usage: python3 tools/reels_growth_2026_11_08.py [name-filter]
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



# ---------- 35: How many layers in one planter? (Mon 16 Nov, curiosity number, best format last week, follow) ----------
bars = ''.join(f'<div class="abs" id="b{k}" style="left:{190 + abs(k - 9) * 6}px;width:{700 - abs(k - 9) * 12}px;top:{1420 - k * 30}px;height:26px;border-radius:13px;background:{["#E9E4DA", "#C2A27C"][k % 2]};opacity:0"></div>' for k in range(18))
REELS.append(dict(name='ply-reel-35-how-many-layers', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{label('Did you know', SU)}
{hook('How many layers<br>in one <i style="color:{ACC_D}">planter?</i>', P, 100)}
{bars}
<div id="num" class="abs h" style="left:0;right:0;top:640px;text-align:center;font-size:220px;color:{P}">0</div>
{line('l1', 'About 0.2 mm each, about 10 cm tall.<br>Our estimate: around 500.', P, 1490, 42)}
{endc(P, I, 'Follow to see<br>the real one printed.')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const c=prog(t,1.0,6.0); document.getElementById('num').textContent=Math.round(500*c);
  for(let k=0;k<18;k++){ const a=1.0+k*0.27; document.getElementById('b'+k).style.opacity=prog(t,a,a+.2); }
  show('l1',prog(t,6.0,6.6),30);
  ''' + END_JS.format(a=8.2) + '''
};'''))

# ---------- 36: Building Ply ep 5: our filament hates humidity (Tue 17 Nov, Lebanese relatable, follow) ----------
spools = ''.join(f'<div id="sp{k}" class="abs" style="left:{130 + k * 215}px;top:720px;width:180px;height:180px;border-radius:50%;background:{c};border:14px solid {P};box-shadow:0 0 0 3px #8A857C;opacity:0"></div>' for k, c in enumerate(('#E9E4DA', '#2B2A27', '#3E5446', '#C2A27C')))
drp = ''.join(f'<svg id="d{k}" class="abs" style="left:{x}px;top:{y}px;opacity:0" width="90" height="120" viewBox="0 0 60 80"><path d="M30 4 C 10 36, 6 54, 30 74 C 54 54, 50 36, 30 4 Z" fill="{I}"/></svg>' for k, (x, y) in enumerate(((180, 980), (470, 1040), (760, 990))))
REELS.append(dict(name='ply-reel-36-building-ply-ep5', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{R}"></div>
{label('Building Ply · episode 5', I)}
{hook('Our filament hates<br>humidity. So does<br>your hair in <i style="color:{ACC_L}">August.</i>', I, 84)}
{spools}{drp}
{line('l1', 'Damp filament prints rough, stringy layers.', I, 1220, 42)}
{line('l2', 'So every spool stays sealed until it goes<br>into the printer’s dry box.', I, 1220, 42)}
{endc(I, P, 'Follow for<br>episode 6.')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<4;k++){ const a=0.3+k*0.35; const p=prog(t,a,a+.4); const e=document.getElementById('sp'+k); e.style.opacity=p; e.style.transform=`translateY(${(1-p)*50}px)`; }
  for(let k=0;k<3;k++){ const a=2.2+k*0.4; const p=prog(t,a,a+.3); const g=prog(t,4.6,5.0); const e=document.getElementById('d'+k); e.style.opacity=Math.min(p,1-g); e.style.transform=`translateY(${(t-a)*30}px)`; }
  const out=prog(t,7.8,8.1);
  show('l1',Math.min(prog(t,2.2,2.7),1-prog(t,4.6,4.9)),30);
  show('l2',Math.min(prog(t,5.0,5.5),1-out),30);
  ''' + END_JS.format(a=8.1) + '''
};'''))

# ---------- 37: Guess what this is? zoom on Loom (Wed 18 Nov, zoom/guess format, loops) ----------
REELS.append(zoom_reel('ply-reel-37-zoom-loom', 'loom-soap-rest-ivory.jpg', 'Guess what<br>this <i>is.</i>',
                       'Loom, our<br>soap rest.', 50, 52, s0=3.6))

# ---------- 38: Every teta has a tin that isn't biscuits (Thu 19 Nov, relatable, product, DM FIRST) ----------
tin = (f'<svg width="560" height="360" viewBox="0 0 280 180"><ellipse cx="140" cy="50" rx="120" ry="34" fill="#5E7FA3"/>'
       f'<rect x="20" y="50" width="240" height="90" fill="#4D6E92"/><ellipse cx="140" cy="140" rx="120" ry="34" fill="#4D6E92"/>'
       f'<ellipse cx="140" cy="50" rx="120" ry="34" fill="#6B8CB0"/><ellipse cx="140" cy="50" rx="80" ry="20" fill="none" stroke="#E9E4DA" stroke-width="4"/></svg>')
things = ['Buttons', 'Needles', 'Hair ties', 'Zero biscuits']
th = ''.join(pill(f'i{k}', t, 1150 + k * 130, [P, I, R, C][k], [I, P, I, P][k], left=100 + k * 40, size=46) for k, t in enumerate(things))
REELS.append(dict(name='ply-reel-38-teta-tin', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{SU}"></div>
{label('Every Lebanese home', I)}
{hook('Every teta has a<br>biscuit tin with <i style="color:{ACC_L}">no<br>biscuits</i> in it.', I, 88)}
<div id="tin" class="abs" style="left:260px;top:720px">{tin}</div>
{th}
{card('c1', img('pleat-pot-open-charcoal.jpg'), 100, 640, 880, 620)}
{line('l1', 'Pleat is our version: a small ribbed pot<br>with a lid. Rings, hair ties, buttons.', I, 1300, 40)}
{cta('cta', 'DM us<br>“FIRST”', 'For first pick of Pleat.<br>Designed and printed in Lebanon.', I, ACC_L)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const sw=prog(t,5.0,5.4);
  document.getElementById('tin').style.opacity=1-sw; document.getElementById('tin').style.transform=`rotate(${Math.sin(t*3)*2}deg)`;
  for(let k=0;k<4;k++){ const a=1.2+k*0.8; const e=document.getElementById('i'+k); const p=prog(t,a,a+.4); e.style.opacity=Math.min(p,1-sw); e.style.transform=`translateX(${(1-p)*-60}px)`; }
  const out=prog(t,8.2,8.6);
  const c=document.getElementById('c1'); const q=prog(t,5.2,5.8); c.style.opacity=Math.min(q,1-out); c.style.transform=`scale(${.96+.04*q})`;
  show('l1',Math.min(prog(t,5.8,6.4),1-out),30);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,8.6,9.2),40);
};'''))

# ---------- 39: Why is it called Ply? (Fri 20 Nov, curiosity, follow) ----------
lay = ''.join(f'<div id="y{k}" class="abs" style="left:240px;width:600px;top:{1300 - k * 56}px;height:44px;border-radius:22px;background:{["#C2A27C", "#3E5446", "#2B2A27", "#DDB8A2"][k % 4]};opacity:0"></div>' for k, _ in enumerate(range(8)))
REELS.append(dict(name='ply-reel-39-why-ply', dur=10.5, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Our name', ACC_L)}
{hook('Why is it<br>called <i style="color:{ACC_L}">Ply?</i>', I, 116)}
{lay}
<div id="w1" class="abs h" style="left:0;right:0;top:640px;text-align:center;font-size:120px;color:{I};opacity:0">ply <span style="font-size:56px;color:#8A857C">(n.)</span></div>
<div id="w2" class="abs" style="left:0;right:0;top:800px;text-align:center;font-size:56px;font-weight:500;color:{ACC_L};opacity:0">a layer.</div>
{line('l1', 'Every piece is printed one thin layer<br>on top of the last. So: Ply.', I, 1400, 42)}
{endc(I, P, 'Follow along.<br>Made in Lebanon.')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const out=prog(t,7.6,7.9);
  show('w1',Math.min(prog(t,1.2,1.7),1-out),30); show('w2',Math.min(prog(t,2.0,2.5),1-out),30);
  for(let k=0;k<8;k++){ const a=3.0+k*0.3; const e=document.getElementById('y'+k); const p=prog(t,a,a+.25); e.style.opacity=Math.min(p,1-out); e.style.transform=`translateY(${(1-p)*-40}px)`; }
  show('l1',Math.min(prog(t,5.6,6.1),1-out),30);
  ''' + END_JS.format(a=7.9) + '''
};'''))

# ---------- 40: Who's the hardest person to buy for? (Sat 21 Nov, gifting with the first frame FIXED to a question, DM FIRST) ----------
gifts = [('quilt-vase-green.jpg', 'The one who kills every plant: a vase for dried stems.'),
         ('loom-soap-rest-in-use-ivory.jpg', 'The one with the perfect bathroom: Loom.'),
         ('pleat-pot-tan.jpg', 'The one who loses earrings: Pleat.')]
gc = ''.join(card(f'c{k}', img(f), 100, 640, 880, 620, op=1 if k == 0 else 0) + line(f't{k}', txt, I, 1300, 42) for k, (f, txt) in enumerate(gifts))
REELS.append(dict(name='ply-reel-40-hardest-to-buy-for', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Christmas list', ACC_L)}
{hook('Who’s the hardest<br>person to buy <i style="color:{ACC_L}">for?</i>', I, 100)}
{gc}
{endc(I, P, 'Designed and printed in Lebanon.<br>Coming soon. DM “FIRST”')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<3;k++){ const a=1.0+k*2.2; const inn=k==0?1:prog(t,a,a+.5), out=k<2?prog(t,a+2.0,a+2.3):prog(t,7.8,8.1);
    const e=document.getElementById('c'+k); e.style.opacity=Math.min(inn,1-out); e.style.transform=`translateY(${(1-inn)*60}px) scale(${.96+.04*inn})`;
    show('t'+k,Math.min(k==0?prog(t,0.4,0.9):prog(t,a+.3,a+.8),1-out),30); }
  ''' + END_JS.format(a=8.1) + '''
};'''))

# ---------- 41: Dark Green or Desert Tan? (Sun 22 Nov, this-or-that vote, HOLD format, comment G or D) ----------
REELS.append(dict(name='ply-reel-41-green-or-tan', dur=9.5, html=f'''
<div class="abs" style="inset:0;background:{R}"></div>
{label('This or that', I)}
{hook('Dark Green or<br><i style="color:{ACC_L}">Desert Tan?</i>', I, 104)}
{card('a0', img('tile-planter-small-green.jpg'), 100, 640, 430, 640, op=1)}
{card('b0', img('tile-vase-tan.jpg'), 550, 640, 430, 640, op=1)}
<div id="la" class="abs" style="left:100px;top:580px;width:430px;text-align:center;font-size:30px;font-weight:500;letter-spacing:.2em;color:{I}">G · GREEN</div>
<div id="lb" class="abs" style="left:550px;top:580px;width:430px;text-align:center;font-size:30px;font-weight:500;letter-spacing:.2em;color:{I}">D · DESERT TAN</div>
{line('l1', 'Tile planter and Tile vase. Same texture, two moods.', I, 1320, 40)}
{cta('cta', 'Comment<br>G or D.', 'One letter is enough.', I, ACC_L)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const o=prog(t,6.2,6.5);
  ['a0','b0'].forEach((s,j)=>{const e=document.getElementById(s); e.style.opacity=1-o; e.style.transform=`scale(${1+.03*prog(t,0,6.2)})`;});
  show('l1',Math.min(prog(t,1.8,2.4),1-o),30);
  ['la','lb','hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  show('cta',prog(t,6.6,7.2),40);
};'''))

if __name__ == '__main__':
    for r in REELS:
        if not flt or any(f in r['name'] for f in flt):
            render(r)
