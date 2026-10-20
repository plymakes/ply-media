"""Growth Reels batch, 21 Oct 2026 (goal: 500 followers by 31 Dec). One Reel a day at 18:00 from 21 Oct to 3 Nov.
Same engine as reels.py; images from shop/products (3D renders, always labelled). Hook text is visible from frame 0
so the feed preview and cover show it. Usage: python3 tools/reels_growth_2026_10_21.py [name-filter]
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
    return (ROOT / 'shop' / 'products' / name).as_uri()


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

# ---------- 14: Building Ply, ep 1: two people, one printer (21 Oct) ----------
grid = [('quilt-planter-small-ivory.jpg', 'Quilt'), ('tile-planter-medium-green.jpg', 'Tile'),
        ('loom-soap-rest-ivory.jpg', 'Loom'), ('pleat-pot-ivory.jpg', 'Pleat')]
cards = ''.join(
    f'<div id="g{k}" class="abs" style="left:{100 + (k % 2) * 450}px;top:{690 + (k // 2) * 305}px;width:430px;height:290px;border-radius:24px;overflow:hidden;opacity:0">'
    f'<img src="{img(f)}" style="width:100%;height:100%;object-fit:cover;display:block">'
    f'<div style="position:absolute;left:18px;top:16px;font-family:IS,Georgia,serif;font-size:44px;color:{I}">{n}</div>{tag(pos="right:16px;bottom:16px")}</div>'
    for k, (f, n) in enumerate(grid))
REELS.append(dict(name='ply-reel-14-building-ply-ep1', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{label('Building Ply · ep 1', SU)}
{hook('Two people.<br>One printer.', P)}
{line('l1', 'A small homeware studio,<br>made in Lebanon.', P, 560)}
{cards}
{line('l2', 'Our first pieces. 3D renders for now:<br>the printer lands in November.', P, 1310, 40)}
<div id="cta" class="abs" style="left:0;right:0;top:860px;text-align:center;opacity:0">
  <div class="h" style="font-size:96px;color:{P}">Follow along</div>
  <div style="font-size:44px;font-weight:500;color:{ACC_D};margin-top:28px">to watch the first print<br>come off the plate.</div>
  <div style="font-size:28px;font-weight:500;letter-spacing:.22em;color:{SU};margin-top:60px">@PLYMAKES</div></div>
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  show('l1',prog(t,1.4,2.0),30);
  for(let k=0;k<4;k++){ const p=prog(t,3.0+k*.45,3.6+k*.45); const e=document.getElementById('g'+k); const out=prog(t,8.0,8.4);
    e.style.opacity=Math.min(p,1-out); e.style.transform=`translateY(${(1-p)*50}px)`; }
  show('l2',Math.min(prog(t,5.2,5.8),1-prog(t,8.0,8.4)),30);
  const o=prog(t,8.0,8.4); ['hk','lab','l1'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  show('cta',prog(t,8.4,9.0),40);
};'''))

# ---------- 15 / 21: Zoom out (texture macro -> full planter), loops ----------
def zoom_reel(name, file, hook_html, reveal, fx, fy, s0=3.4, hook_col=None, shade=True):
    """Starts as an extreme close-up of the texture (fx, fy = focus point in % of the image) and pulls back to the whole piece."""
    return dict(name=name, dur=8.0, html=f'''
<div class="abs" style="inset:0;background:linear-gradient({RBG_TOP} 0,{RBG_TOP} 420px,{RBG_BOT} 1500px,{RBG_BOT} 100%)"></div>
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


REELS.append(zoom_reel('ply-reel-15-zoom-quilt', 'quilt-planter-small-ivory.jpg', 'Guess what<br>this is.', 'The Quilt<br><i style="color:{}">planter</i>'.format(ACC_L), 47, 76, hook_col=I, shade=False))
REELS.append(zoom_reel('ply-reel-21-zoom-tile', 'tile-planter-medium-green.jpg', 'Guess<br>again.', 'The Tile<br><i style="color:{}">planter</i>'.format(ACC_L), 46, 76))

# ---------- 16: Ply in 10 seconds (24 Oct, to pin) ----------
pieces = [('quilt-planter-medium-charcoal.jpg', 'Quilt', 'planter and vase'), ('tile-planter-small-tan.jpg', 'Tile', 'planter and vase'),
          ('loom-soap-rest-in-use-ivory.jpg', 'Loom', 'soap rest'), ('pleat-pot-rings-ivory.jpg', 'Pleat', 'pot with a dish lid')]
pc = ''.join(card(f'p{k}', img(f), 140, 560, 800, 730) +
             f'<div id="pn{k}" class="abs" style="left:140px;top:1315px;opacity:0"><span class="h" style="font-size:72px;color:{I}">{n}</span>'
             f'<span style="font-size:38px;font-weight:500;color:#6E6A63;margin-left:22px">{d}</span></div>' for k, (f, n, d) in enumerate(pieces))
sw = [('#E9E4DA', 'Ivory White'), ('#2B2A27', 'Charcoal'), ('#3E5446', 'Dark Green'), ('#C2A27C', 'Desert Tan')]
swatches = ''.join(f'<div id="w{k}" class="abs" style="left:{140 + k * 205}px;top:760px;width:180px;opacity:0;text-align:center">'
                   f'<div style="width:150px;height:150px;margin:0 auto;border-radius:50%;background:{c};border:2px solid #8A857C"></div>'
                   f'<div style="font-size:30px;font-weight:500;color:{I};margin-top:22px">{n}</div></div>' for k, (c, n) in enumerate(sw))
REELS.append(dict(name='ply-reel-16-ply-in-10-seconds', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Meet Ply', ACC_L)}
{hook('Ply in<br><i style="color:' + ACC_L + '">10 seconds.</i>', I)}
{pc}{swatches}
{line('sw', 'Four matte colours.<br>Chosen to sit together.', I, 1040, 48)}
<div id="fin" class="abs" style="left:100px;right:100px;top:700px;opacity:0">
  <div class="h" style="font-size:104px;color:{I}">3D-printed<br>in Lebanon.</div>
  <div style="font-size:46px;font-weight:500;color:{I};margin-top:40px;line-height:1.3">First pieces in November.<br>Follow along, it starts here.</div>
  <div style="font-size:28px;font-weight:500;letter-spacing:.22em;color:{ACC_L};margin-top:60px">@PLYMAKES</div></div>
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<4;k++){ const a=1.1+k*1.3; const inn=prog(t,a,a+.35), out=prog(t,a+1.3,a+1.6);
    const e=document.getElementById('p'+k); e.style.opacity=Math.min(inn,1-out); e.style.transform=`scale(${.95+.05*inn})`;
    show('pn'+k,Math.min(prog(t,a+.15,a+.5),1-out),20); }
  for(let k=0;k<4;k++) show('w'+k,Math.min(prog(t,6.4+k*.15,6.8+k*.15),1-prog(t,8.6,8.9)),20);
  show('sw',Math.min(prog(t,6.9,7.4),1-prog(t,8.6,8.9)),30);
  const f=prog(t,8.8,9.3); ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-f); show('fin',f,40);
};'''))

# ---------- 17: 3 things about our pots (26 Oct) ----------
facts = [('1', 'No moulds.', 'Every piece is printed,<br>layer by layer.'),
         ('2', 'It starts as plants.', 'PLA is made from plant starch,<br>like corn or sugarcane.'),
         ('3', 'It takes hours.', 'One small planter is several<br>hours on the printer.')]
fx = ''.join(f'<div id="f{k}" class="abs" style="left:100px;right:100px;top:{620 + k * 250}px;display:flex;gap:34px;opacity:0">'
             f'<div class="h" style="font-size:110px;line-height:.9;color:{ACC_L}">{n}</div>'
             f'<div><div class="h" style="font-size:64px;color:{I}">{h}</div><div style="font-size:38px;font-weight:400;line-height:1.3;color:{I};margin-top:10px">{b}</div></div></div>'
             for k, (n, h, b) in enumerate(facts))
REELS.append(dict(name='ply-reel-17-three-things', dur=12.0, html=f'''
<div class="abs" style="inset:0;background:{SU}"></div>
{label('Good to know', I)}
{hook('3 things you didn’t<br>know about our pots', I, 92)}
{fx}
{line('sv', 'Save this for later.', I, 1390, 44)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<3;k++) show('f'+k,prog(t,1.2+k*2.6,1.8+k*2.6),40);
  show('sv',prog(t,9.6,10.2),20);
};'''))

# ---------- 18: Building Ply, ep 2: why only four colours (28 Oct) ----------
REELS.append(dict(name='ply-reel-18-building-ply-ep2', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Building Ply · ep 2', ACC_L)}
{hook('We could print in<br>a hundred colours.', I, 96)}
{line('l1', '<span class="h" style="font-size:96px">We picked <i style="color:' + ACC_L + '">four.</i></span>', I, 540, 46)}
{card('c1', img('pleat-pot-four-colours.jpg'), 100, 700, 880, 540)}
{card('c2', img('loom-soap-rest-four-colours.jpg'), 100, 700, 880, 540)}
{line('l2', 'Ivory White, Charcoal, Dark Green, Desert Tan.<br>Calm on their own, easy together.', I, 1275, 38)}
<div id="cta" class="abs" style="left:0;right:0;top:820px;text-align:center;opacity:0">
  <div class="h" style="font-size:100px;color:{I}">Which one<br>is yours?</div>
  <div style="font-size:44px;font-weight:500;color:{ACC_L};margin-top:34px">Tell us in the comments.</div></div>
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  show('l1',prog(t,1.6,2.2),30);
  ''' + slide_card('c1', 2.8) + '''
  const sw=prog(t,5.4,5.9); document.getElementById('c1').style.opacity=Math.min(prog(t,2.8,3.4),1-sw);
  document.getElementById('c2').style.opacity=Math.min(sw,1-prog(t,8.0,8.4));
  show('l2',Math.min(prog(t,3.6,4.2),1-prog(t,8.0,8.4)),30);
  const o=prog(t,8.0,8.4); ['hk','lab','l1'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  show('cta',prog(t,8.4,9.0),40);
};'''))

# ---------- 19: Loom: is your soap sitting in a puddle? (30 Oct) ----------
REELS.append(dict(name='ply-reel-19-loom-puddle', dur=10.0, html=f'''
<div class="abs" style="inset:0;background:{R}"></div>
{label('Meet Loom', I)}
{hook('Is your soap sitting<br>in a puddle?', I, 100)}
{card('c1', img('loom-soap-rest-in-use-ivory.jpg'), 100, 640, 880, 620)}
{line('l1', 'Loom lets the water run<br>through the slats.', I, 1290, 46)}
{line('l2', 'So the bar can dry between washes.', I, 1290, 46)}
{endc(I, P, 'Meet Loom, our soap rest.<br>Coming soon. DM “FIRST”')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  ''' + slide_card('c1', 1.4) + '''
  show('l1',Math.min(prog(t,2.2,2.8),1-prog(t,4.8,5.2)),30); show('l2',prog(t,5.2,5.8),30);
  ''' + END_JS.format(a=7.8) + '''
};'''))

# ---------- 20: Pleat: where do your rings go at night? (1 Nov) ----------
REELS.append(dict(name='ply-reel-20-pleat-rings', dur=10.0, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{label('Meet Pleat', SU)}
{hook('Where do your rings<br>go at night?', P, 88)}
{card('c1', img('pleat-pot-rings-ivory.jpg'), 100, 640, 880, 620)}
{card('c2', img('pleat-pot-open-charcoal.jpg'), 100, 640, 880, 620)}
{line('l1', 'On the lid. It’s a little dish.', P, 1290, 46)}
{line('l2', 'And the pot keeps the rest.', P, 1290, 46)}
{endc(P, I, 'Meet Pleat, a pot with a dish lid.<br>Coming soon. DM “FIRST”')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  ''' + slide_card('c1', 1.4) + '''
  const sw=prog(t,4.6,5.1); document.getElementById('c1').style.opacity=Math.min(prog(t,1.4,2.0),1-sw); document.getElementById('c2').style.opacity=sw;
  show('l1',Math.min(prog(t,2.2,2.8),1-prog(t,4.6,5.0)),30); show('l2',prog(t,5.1,5.7),30);
  ''' + END_JS.format(a=7.8) + '''
};'''))

# ---------- 22: Building Ply, ep 3: the printer should land next week (3 Nov) ----------
REELS.append(dict(name='ply-reel-22-building-ply-ep3', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{C}"></div>
{label('Building Ply · ep 3', P)}
{hook('Our printer should<br>land next week.', P, 100)}
{line('l1', 'First job:', P, 560, 46)}
{card('c1', img('quilt-planter-small-ivory.jpg'), 190, 640, 700, 620)}
{line('l2', 'A small Quilt planter, printed two ways<br>to find the faster one.', P, 1290, 40)}
<div id="cta" class="abs" style="left:0;right:0;top:820px;text-align:center;opacity:0">
  <div class="h" style="font-size:100px;color:{P}">Follow to see<br>how it goes.</div>
  <div style="font-size:28px;font-weight:500;letter-spacing:.22em;color:{P};opacity:.8;margin-top:60px">@PLYMAKES</div></div>
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  show('l1',Math.min(prog(t,1.4,2.0),1-prog(t,8.0,8.4)),30);
  ''' + slide_card('c1', 2.0) + '''
  document.getElementById('c1').style.opacity=Math.min(prog(t,2.0,2.6),1-prog(t,8.0,8.4));
  show('l2',Math.min(prog(t,3.2,3.8),1-prog(t,8.0,8.4)),30);
  const o=prog(t,8.0,8.4); ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  show('cta',prog(t,8.4,9.0),40);
};'''))

if __name__ == '__main__':
    for r in REELS:
        if not flt or any(f in r['name'] for f in flt):
            render(r)
