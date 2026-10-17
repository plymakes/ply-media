"""Product-free pre-launch Reels (17 Oct 2026 pivot). Same engine as reels.py.
Usage: python3 tools/reels_brand.py [name-filter] -> build/<name>-v3.mp4
"""
import runpy, sys
from pathlib import Path
flt = sys.argv[1:]
m = runpy.run_path(str(Path(__file__).resolve().parent / 'reels.py'), run_name='lib')
C, SU, R, I, P, end_card, render = m['C'], m['SU'], m['R'], m['I'], m['P'], m['end_card'], m['render']
ACC_D, ACC_L = '#D27A52', '#9C4421'


def endc(bg, fg, l2):
    return end_card(bg, fg, 'Made in layers.<br>Made in Lebanon.', l2).replace('font-size:120px', 'font-size:92px')


def head(label, title, fg, lab):
    return (f'<div id="lab" class="abs label" style="left:100px;top:180px;color:{lab}">{label}</div>'
            f'<div id="t1" class="abs h" style="left:100px;right:100px;top:250px;font-size:116px;color:{fg}">{title}</div>')


HEAD_JS = "show('lab',prog(t,0,.6),30); show('t1',prog(t,.2,.9),40);"
END_JS = "const e=prog(t,{a},{a}+.5); document.getElementById('end').style.opacity=e; show('e1',prog(t,{a}+.3,{a}+.9),40); show('e2',prog(t,{a}+.7,{a}+1.3),40);"

# ---------- Reel 7: the Ply. mark printed layer by layer ----------
reel7 = dict(name='ply-reel-07-ply-layer-by-layer', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{C}"></div>
{head('Watch it print', 'Made in<br><i style="color:{P}">layers.</i>', P, P)}
<div class="abs" style="left:170px;width:740px;top:1330px;height:36px;border-radius:18px;background:{I}"></div>
<div id="wrap" class="abs" style="left:0;right:0;top:830px;height:500px;clip-path:inset(100% 0 0 0)">
  <div class="abs" style="left:0;right:0;top:0;display:flex;justify-content:center;align-items:baseline">
    <span style="font-family:IS,Georgia,serif;font-size:420px;line-height:1.05;color:transparent;background:repeating-linear-gradient(0deg,{SU} 0 3px,{P} 3px 15px);-webkit-background-clip:text;background-clip:text">Ply</span>
    <span style="display:inline-block;width:56px;height:56px;border-radius:50%;background:{I};margin-left:14px"></span></div></div>
<div id="noz" class="abs" style="width:150px;height:46px;border-radius:23px;background:{I};top:800px;left:300px"></div>
<div id="noztip" class="abs" style="width:26px;height:26px;border-radius:13px;background:{SU};top:836px;left:362px"></div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1440px;font-size:46px;font-weight:500;color:{P};opacity:0">Ply means layer.<br>Our first pieces arrive in November.</div>
{endc(I, P, 'DM “FIRST” to join<br>the First Layer')}
''', js='''
window.setT=t=>{ ''' + HEAD_JS + '''
  const L=32, p=clamp((t-1.2)/5.0), k=Math.floor(p*L), frac=(p*L)%1;
  document.getElementById('wrap').style.clipPath=`inset(${(1-k/L)*100}% 0 0 0)`;
  const top=830+500*(1-k/L)-56, dir=(k%2==0)?frac:1-frac, x=200+dir*620, vis=(p>0&&p<1)?1:0;
  const n=document.getElementById('noz'), nt=document.getElementById('noztip');
  n.style.opacity=vis; nt.style.opacity=vis; n.style.top=top+'px'; n.style.left=x+'px'; nt.style.top=(top+36)+'px'; nt.style.left=(x+62)+'px';
  show('t2',prog(t,6.5,7.1),30); ''' + END_JS.format(a=8.2) + '''
};''')

# ---------- Reel 8: three pieces, coming November ----------
clues = [('01', 'Holds a plant', C, P), ('02', 'Holds dried stems', SU, I), ('03', 'Sits under your coffee', P, I)]
cards = ''
for k, (num, txt, bg, fg) in enumerate(clues):
    top = 660 + k * 260
    bars = ''.join(f'<div class="b{k}" style="position:absolute;left:0;right:0;bottom:{j*20}px;height:14px;border-radius:7px;background:{bg};opacity:0"></div>' for j in range(10))
    cards += (f'<div class="abs" style="left:100px;width:880px;top:{top}px;height:210px">{bars}'
              f'<div id="c{k}" class="abs" style="inset:0;border-radius:24px;background:{bg};color:{fg};opacity:0;display:flex;align-items:center;gap:40px;padding:0 56px">'
              f'<span style="font-family:IS,Georgia,serif;font-size:110px;line-height:1">{num}</span><span style="font-size:52px;font-weight:500">{txt}</span></div></div>')
reel8 = dict(name='ply-reel-08-three-pieces', dur=11.5, html=f'''
<div class="abs" style="inset:0;background:{I}"></div>
{head('Coming in November', 'Three pieces.<br><i style="color:{ACC_D}">Guess them?</i>', P, SU)}
{cards}
<div id="t2" class="abs" style="left:100px;right:100px;top:1500px;font-size:46px;font-weight:500;color:{P};opacity:0">Comment your guesses.<br>The reveal comes with the first real photos.</div>
{endc(C, P, 'DM “FIRST” for first pick<br>of the first batch')}
''', js='''
window.setT=t=>{ ''' + HEAD_JS + '''
  for(let k=0;k<3;k++){ const a=1.2+k*1.6;
    document.querySelectorAll('.b'+k).forEach((b,j)=>{ b.style.opacity=(t>a+j*0.08 && t<a+1.05)?1:0; });
    const c=document.getElementById('c'+k); const p=prog(t,a+0.85,a+1.2); c.style.opacity=p; }
  show('t2',prog(t,6.6,7.2),30); ''' + END_JS.format(a=8.7) + '''
};''')

# ---------- Reel 9: a few hundred layers ----------
stack = ''.join(f'<div class="ly abs" style="left:{240 + abs(j - 30) * 0:.0f}px;width:600px;top:{1380 - j*7.5:.0f}px;height:5px;border-radius:4px;background:{[I, ACC_L, R][j % 3]};opacity:0"></div>' for j in range(60))
reel9 = dict(name='ply-reel-09-hundreds-of-layers', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{P}"></div>
{head('Did you know?', 'One layer is<br><i style="color:{ACC_L}">0.2 mm.</i>', I, I)}
{stack}
<div id="cnt" class="abs h" style="left:0;right:0;top:620px;text-align:center;font-size:150px;color:{I}">0</div>
<div id="cl" class="abs" style="left:0;right:0;top:790px;text-align:center;font-size:34px;font-weight:500;letter-spacing:.22em;color:#6E6A63">LAYERS</div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1480px;font-size:46px;font-weight:500;color:{I};opacity:0">About three human hairs thick.<br>A small piece takes a few hundred.</div>
{endc(I, P, 'Ply means layer.<br>DM “FIRST” to join the First Layer')}
''', js='''
const ly=[...document.querySelectorAll('.ly')];
window.setT=t=>{ ''' + HEAD_JS + '''
  const p=clamp((t-1.2)/5.0); const k=Math.floor(p*ly.length); ly.forEach((e,i)=>e.style.opacity=i<k?1:0);
  document.getElementById('cnt').textContent=Math.round(ease(p)*600);
  show('t2',prog(t,6.6,7.2),30); ''' + END_JS.format(a=8.2) + '''
};''')

for r in (reel7, reel8, reel9):
    if not flt or any(f in r['name'] for f in flt):
        render(r)
