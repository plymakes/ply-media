"""Growth Reels batch, 25 Oct 2026 (weekly plan). One Reel a day at 18:00, 4-8 Nov. Copied from reels_growth_2026_10_21.py; only the content changes.
Same engine as reels.py; images from shop/products (3D renders, always labelled). Hook text is visible from frame 0
so the feed preview and cover show it. Usage: python3 tools/reels_growth_2026_10_25.py [name-filter]
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


# ---------- 23: Send this to the friend who just moved (Wed 4 Nov, product Reel, gifting, DM FIRST) ----------
gifts = [('quilt-planter-small-charcoal.jpg', 'A planter for the windowsill.'),
         ('tile-vase-green.jpg', 'A vase for dried stems.'),
         ('loom-soap-rest-in-use-ivory.jpg', 'A soap rest for the new bathroom.')]
gc = ''.join(card(f'c{k}', img(f), 100, 640, 880, 620) + line(f't{k}', txt, I, 1300, 46) for k, (f, txt) in enumerate(gifts))
REELS.append(dict(name='ply-reel-23-friend-who-moved', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{label('Gift idea', ACC_L)}
{hook('Send this to the friend<br>who just moved.', I, 82)}
{gc}
{endc(I, P, 'Designed and printed in Lebanon.<br>Coming soon. DM “FIRST”')}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<3;k++){ const a=1.3+k*2.0; const inn=k==0?1:prog(t,a,a+.5), out=k<2?prog(t,a+2.0,a+2.3):prog(t,7.6,7.9);
    const e=document.getElementById('c'+k); e.style.opacity=Math.min(inn,1-out); e.style.transform=`translateY(${(1-inn)*60}px) scale(${.96+.04*inn})`;
    show('t'+k,Math.min(k==0?1:prog(t,a+.3,a+.8),1-out),30); }
  ''' + END_JS.format(a=7.9) + '''
};'''))

# ---------- 24: How long does one planter take to print? (Thu 5 Nov, growth Reel, curiosity, follow) ----------
opts = ['30 minutes', 'A few hours', 'A whole day']
oc = ''.join(f'<div id="o{k}" class="abs" style="left:100px;top:{640 + k * 170}px;padding:30px 54px;border-radius:999px;'
             f'background:{P};color:{I};font-size:56px;font-weight:500;opacity:0">{chr(65 + k)} · {o}</div>' for k, o in enumerate(opts))
REELS.append(dict(name='ply-reel-24-how-long', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{SU}"></div>
{label('Guess', I)}
{hook('How long does one<br>planter take to print?', I, 82)}
{oc}
{line('l1', 'B. A few hours: about 4 to 5 each,<br>by our estimate. One layer at a time.', I, 1180, 42)}
{card('c1', img('quilt-planter-small-ivory.jpg'), 290, 1330, 500, 360)}
{cta('cta', 'Follow to see<br>the real time.', 'We time the first one<br>when the printer lands.', I, ACC_L)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const out=prog(t,8.0,8.4);
  for(let k=0;k<3;k++){ const p=1; const e=document.getElementById('o'+k);
    const dim=(k!=1)?prog(t,4.2,4.6)*.65:0; e.style.opacity=Math.min(p,1-out)*(1-dim); e.style.transform=`translateX(${(1-p)*-60}px)`; }
  const hi=prog(t,4.2,4.6); const b=document.getElementById('o1'); b.style.background=hi>0.5?'#9C4421':'#EFEAE2'; b.style.color=hi>0.5?'#EFEAE2':'#1C1B19';
  show('l1',Math.min(prog(t,4.8,5.4),1-out),30);
  const c=document.getElementById('c1'); c.style.opacity=Math.min(prog(t,5.6,6.2),1-out);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,8.4,9.0),40);
};'''))

# ---------- 25: Every Lebanese balcony has mint in an old tin (Fri 6 Nov, growth Reel, relatable, follow; Trial Reel test) ----------
tin = f'''<svg width="520" height="560" viewBox="0 0 260 280">
<g fill="#6F7D5C"><ellipse cx="95" cy="70" rx="26" ry="14" transform="rotate(-35 95 70)"/><ellipse cx="160" cy="62" rx="26" ry="14" transform="rotate(30 160 62)"/>
<ellipse cx="128" cy="40" rx="24" ry="13" transform="rotate(-80 128 40)"/><ellipse cx="78" cy="105" rx="24" ry="13" transform="rotate(-15 78 105)"/>
<ellipse cx="180" cy="100" rx="24" ry="13" transform="rotate(15 180 100)"/></g>
<path d="M128 125 L128 55 M128 100 L95 72 M128 95 L160 66" stroke="#55623F" stroke-width="5" fill="none" stroke-linecap="round"/>
<rect x="55" y="118" width="150" height="150" rx="6" fill="#A9A49B"/><rect x="55" y="118" width="150" height="14" fill="#8A857C"/>
<rect x="55" y="254" width="150" height="14" fill="#8A857C"/><rect x="55" y="150" width="150" height="70" fill="{R}"/>
<path d="M70 170 h120 M70 190 h90" stroke="{C}" stroke-width="6" stroke-linecap="round"/></svg>'''
REELS.append(dict(name='ply-reel-25-mint-in-a-tin', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{R}"></div>
{label('Lebanese balcony', I)}
{hook('Every Lebanese balcony<br>has mint in an old tin.', I, 78)}
<div id="tin" class="abs" style="left:280px;top:660px;opacity:0">{tin}</div>
{line('l1', 'It deserves an upgrade.', I, 1300, 52)}
{card('c1', img('quilt-planter-small-green.jpg'), 100, 640, 880, 620)}
{line('l2', 'Seven drainage holes, a hidden drip tray.<br>The Quilt planter, coming in November.', I, 1300, 40)}
{cta('cta', 'Follow for the<br>first real one.', 'Made in layers.<br>Made in Lebanon.', I, ACC_L)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  const sw=prog(t,4.4,4.9); const ti=document.getElementById('tin'); const p=1;
  ti.style.opacity=Math.min(p,1-sw); ti.style.transform=`translateY(${(1-p)*60}px) rotate(${Math.sin(t*2.2)*1.5}deg)`;
  show('l1',Math.min(prog(t,2.4,3.0),1-sw),30);
  ''' + slide_card('c1', 4.6, 0, 60) + '''
  const out=prog(t,8.0,8.4); document.getElementById('c1').style.opacity=Math.min(prog(t,4.6,5.2),1-out);
  show('l2',Math.min(prog(t,5.4,6.0),1-out),30);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-out);
  show('cta',prog(t,8.4,9.0),40);
};'''))

# ---------- 26: Ivory or Charcoal? (Sat 7 Nov, this-or-that vote, the format with the best 3-second hold so far) ----------
pairs = [('quilt-planter-small-ivory.jpg', 'quilt-planter-small-charcoal.jpg', 'Quilt planter'),
         ('tile-vase-ivory.jpg', 'tile-vase-charcoal.jpg', 'Tile vase'),
         ('pleat-pot-ivory.jpg', 'pleat-pot-charcoal.jpg', 'Pleat pot')]
pc = ''
for k, (a, b, n) in enumerate(pairs):
    pc += card(f'a{k}', img(a), 100, 600, 430, 640) + card(f'b{k}', img(b), 550, 600, 430, 640)
    pc += f'<div id="n{k}" class="abs" style="left:100px;top:1275px;font-size:40px;font-weight:500;color:{P};opacity:0">{n}</div>'
REELS.append(dict(name='ply-reel-26-ivory-or-charcoal', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{label('This or that', SU)}
{hook('Ivory or<br><i style="color:{ACC_D}">Charcoal?</i>', P, 116)}
{pc}
<div id="la" class="abs" style="left:100px;top:540px;width:430px;text-align:center;font-size:30px;font-weight:500;letter-spacing:.2em;color:{SU}">I · IVORY</div>
<div id="lb" class="abs" style="left:550px;top:540px;width:430px;text-align:center;font-size:30px;font-weight:500;letter-spacing:.2em;color:{SU}">C · CHARCOAL</div>
{cta('cta', 'Comment<br>I or C.', 'One letter is enough.<br>Tell us below.', P, ACC_D)}
''', js='''
window.setT=t=>{ ''' + HOOK_JS + '''
  for(let k=0;k<3;k++){ const a=1.0+k*2.3; const inn=prog(t,a,a+.5), out=k<2?prog(t,a+2.3,a+2.6):prog(t,7.9,8.2);
    ['a','b'].forEach((s,j)=>{const e=document.getElementById(s+k); const q=k==0?1:prog(t,a+j*.2,a+.5+j*.2); e.style.opacity=Math.min(q,1-out); e.style.transform=`translateY(${(1-q)*50}px)`;});
    show('n'+k,Math.min(k==0?1:inn,1-out),20); }
  const o=prog(t,7.9,8.2); ['la','lb'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  ['hk','lab'].forEach(i=>document.getElementById(i).style.opacity=1-o);
  show('cta',prog(t,8.3,8.9),40);
};'''))

# ---------- 27: Zoom out: Pleat (Sun 8 Nov, growth Reel, guess, loops) ----------
REELS.append(zoom_reel('ply-reel-27-zoom-pleat', 'pleat-pot-ivory.jpg', 'It’s not a lamp.<br>Guess again.',
                       'Pleat: a pot<br>with a <i style="color:{}">dish lid</i>'.format(ACC_L), 45, 62, s0=3.6, bg=(P, '#EEE9E1')))

if __name__ == '__main__':
    for r in REELS:
        if not flt or any(f in r['name'] for f in flt):
            render(r)
