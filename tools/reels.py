"""Ply Reels: animated 1080x1920 motion graphics rendered frame by frame, encoded to MP4.

Usage: python3 tools/reels.py [name-filter]
Each reel is an HTML page with a window.setT(t) function (t in seconds). Frames are screenshotted
in Chromium and stitched with ffmpeg (H.264, silent AAC track, 30 fps).
"""
import subprocess
import sys
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FS = Path(__file__).resolve().parent / 'fonts'
OUT = ROOT / 'build'
OUT.mkdir(exist_ok=True)
FPS = 30
C, SU, R, I, P = '#B4532A', '#CDBFA8', '#DDB8A2', '#1C1B19', '#EFEAE2'  # Atelier: terracotta, sand, clay, charcoal, bone

FACES = ''.join(f"@font-face{{font-family:SG;font-weight:{w};src:url('{(FS/f'space-grotesk/files/space-grotesk-latin-{w}-normal.woff2').as_uri()}')}}" for w in (400, 500, 700))
FACES += f"@font-face{{font-family:PA;font-weight:600;src:url('{(FS/'noto-naskh-arabic/files/noto-naskh-arabic-arabic-600-normal.woff2').as_uri()}')}}"
FACES += ''.join(f"@font-face{{font-family:IS;font-style:{st};font-weight:500;src:url('{(FS/f'fraunces/files/fraunces-latin-500-{st}.woff2').as_uri()}')}}" for st in ('normal', 'italic'))

BASE_CSS = FACES + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:SG,sans-serif}
.abs{position:absolute}
.label{font-size:26px;font-weight:500;letter-spacing:.22em;text-transform:uppercase}
.h{font-family:IS,Georgia,serif;font-weight:500;letter-spacing:-.015em;line-height:1}
.fade{transition:none}
"""

# shared JS helpers: easing, clamp, end card
JS_HELPERS = """
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=clamp(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2};
const prog=(t,a,b)=>ease((t-a)/(b-a));
function show(id,o,dy=0){const e=document.getElementById(id);e.style.opacity=o;e.style.transform=`translateY(${(1-o)*dy}px)`;}
"""


def stack(cols, h, left, top, idp):
    w, step = h * 2.75, h / 3
    return ''.join(f'<div id="{idp}{i}" class="abs" style="left:{left + (2-i)*step:.0f}px;top:{top + i*h:.0f}px;width:{w:.0f}px;height:{h}px;border-radius:{h/2}px;background:{c}"></div>' for i, c in enumerate(cols))


def end_card(bg_col, fg, line1, line2):
    """End card: the Ply MAKES lockup, a serif line and the call to action. Hidden until shown via JS (ids e*)."""
    dot = I if bg_col == C else C
    return f'''<div id="end" class="abs" style="inset:0;background:{bg_col};opacity:0">
<div class="abs" style="left:0;right:0;top:560px;display:flex;justify-content:center;align-items:baseline;gap:28px">
<span style="font-family:IS,Georgia,serif;font-size:220px;line-height:.8;color:{fg}">Ply</span>
<span style="font-size:34px;font-weight:500;letter-spacing:.45em;color:{fg};opacity:.75">MAKES</span>
<span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:{dot};margin-left:-22px"></span></div>
<div id="e1" class="abs h" style="left:100px;right:100px;top:960px;text-align:center;font-size:120px;color:{fg}">{line1}</div>
<div id="e2" class="abs" style="left:100px;right:100px;top:1280px;text-align:center;font-size:42px;font-weight:400;line-height:1.35;color:{fg};opacity:.85">{line2}</div>
<div class="abs" style="left:0;right:0;bottom:150px;text-align:center;font-size:28px;font-weight:500;letter-spacing:.22em;color:{fg};opacity:.7">@PLYMAKES</div></div>'''


# ---------- Reel 1: Arabic name printed layer by layer ----------
LAYERS = 30
reel1 = dict(name='ply-reel-01-name-layer-by-layer', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{C}"></div>
<div id="lab" class="abs label" style="left:100px;top:180px;color:{P}">Watch it print</div>
<div id="t1" class="abs h" style="left:100px;right:100px;top:250px;font-size:116px;color:{P}">Your name.<br>Layer by layer.</div>
<div class="abs" style="left:190px;width:700px;top:1290px;height:40px;border-radius:20px;background:{I}"></div>
<div id="nameWrap" class="abs" style="left:0;right:0;top:820px;height:470px;clip-path:inset(100% 0 0 0)">
  <div dir="rtl" lang="ar" class="abs" style="left:0;right:0;top:0;text-align:center;font-family:PA;font-weight:600;font-size:400px;line-height:1.15;color:transparent;background:repeating-linear-gradient(0deg, #CDBFA8 0 3px, {P} 3px 15px);-webkit-background-clip:text;background-clip:text">ليلى</div>
</div>
<div id="noz" class="abs" style="width:150px;height:46px;border-radius:23px;background:{P};top:800px;left:300px"></div>
<div id="noztip" class="abs" style="width:26px;height:26px;border-radius:13px;background:{R};top:836px;left:362px"></div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1420px;font-size:46px;font-weight:500;color:{P};opacity:0">Arabic or English, any colour.<br>Coming soon to Ply.</div>
{end_card(I, P, 'Join the<br>First Layer', 'DM “FIRST” for first access<br>and a Christmas priority slot')}
''', js=f'''
window.setT=t=>{{
  show('lab',prog(t,0,.6),30); show('t1',prog(t,.2,.9),40);
  const p=clamp((t-1.2)/5.0); const layers={LAYERS}; const k=Math.floor(p*layers);
  const frac=(p*layers)%1;
  document.getElementById('nameWrap').style.clipPath=`inset(${{(1-k/layers)*100}}% 0 0 0)`;
  const top=820+470*(1-k/layers)-56; const dir=(k%2==0)?frac:1-frac; const x=250+dir*430;
  const vis=(p>0&&p<1)?1:0;
  for(const id of ['noz','noztip']){{const e=document.getElementById(id);e.style.opacity=vis;}}
  document.getElementById('noz').style.top=top+'px';document.getElementById('noz').style.left=x+'px';
  document.getElementById('noztip').style.top=(top+36)+'px';document.getElementById('noztip').style.left=(x+62)+'px';
  show('t2',prog(t,6.4,7.0),30);
  const e=prog(t,8.0,8.5); document.getElementById('end').style.opacity=e;
  show('e1',prog(t,8.3,8.9),40); show('e2',prog(t,8.7,9.3),40);
}};''')

# ---------- Reel 2: lithophane, light off -> light on ----------
reel2 = dict(name='ply-reel-02-light-on', dur=10.0, html=f'''
<div id="bg" class="abs" style="inset:0;background:{I}"></div>
<div id="lab" class="abs label" style="left:100px;top:180px;color:#A9ACB3">Lithophane</div>
<div id="t1" class="abs h" style="left:100px;right:100px;top:250px;font-size:120px;color:{P}">Lights off…</div>
<div id="t1b" class="abs h" style="left:100px;right:100px;top:250px;font-size:120px;color:{SU};opacity:0">Lights on.</div>
<div class="abs" style="left:240px;top:620px;width:600px;height:780px;border-radius:28px;overflow:hidden;background:#E6E1D5">
  <div class="abs" style="inset:0;background:repeating-linear-gradient(0deg, rgba(19,21,26,.05) 0 6px, transparent 6px 20px)"></div>
  <div id="glow" class="abs" style="inset:0;opacity:0;background:radial-gradient(circle at 50% 36%,#FFF6DC 0%,#FFD98A 42%,#E39A40 100%)">
    <div class="abs" style="left:270px;top:150px;width:150px;height:150px;border-radius:50%;background:#FFFBEF"></div>
    <div class="abs" style="left:-80px;top:470px;width:460px;height:460px;border-radius:50%;background:#B8742E"></div>
    <div class="abs" style="left:250px;top:520px;width:520px;height:520px;border-radius:50%;background:#8C5420"></div>
    <div class="abs" style="left:60px;top:640px;width:500px;height:360px;border-radius:50%;background:#6B3D16"></div>
  </div>
</div>
<div id="halo" class="abs" style="left:140px;top:520px;width:800px;height:980px;border-radius:80px;background:radial-gradient(closest-side, rgba(255,194,58,.35), rgba(255,194,58,0));opacity:0"></div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1500px;font-size:46px;font-weight:500;color:{P};opacity:0">A photo hidden in plastic.<br>Thin layers glow, thick ones block light.</div>
{end_card(C, P, 'Your photo,<br>in light', 'DM “FIRST” to join the First Layer<br>and order first')}
''', js='''
window.setT=t=>{
  show('lab',prog(t,0,.6),30); show('t1',prog(t,.2,.8),40);
  const on=t>3.0?1:0; const flick=(t>3.0&&t<3.25)?(Math.floor(t*40)%2):on;
  document.getElementById('glow').style.opacity=flick; document.getElementById('halo').style.opacity=flick;
  document.getElementById('t1').style.opacity=t>3.0?0:prog(t,.2,.8);
  document.getElementById('t1b').style.opacity=on;
  show('t2',prog(t,4.2,4.8),30);
  const e=prog(t,7.2,7.7); document.getElementById('end').style.opacity=e;
  show('e1',prog(t,7.5,8.1),40); show('e2',prog(t,7.9,8.5),40);
};''')

# ---------- Reel 3: cedar ornament stacking up ----------
tiers = [(150, 0), (250, 1), (340, 0), (220, 1), (330, 0), (430, 1), (300, 0), (420, 0), (520, 1)]
tier_html = ''
y0 = 700
for i, (w, alt) in enumerate(tiers):
    tier_html += f'<div id="tier{i}" class="abs" style="left:{540 - w/2:.0f}px;top:{y0 + i*52}px;width:{w}px;height:42px;border-radius:21px;background:{P if not alt else "#E3D9C9"};opacity:0"></div>'
trunk_top = y0 + len(tiers) * 52
reel3 = dict(name='ply-reel-03-cedar-ornament', dur=11.0, html=f'''
<div class="abs" style="inset:0;background:{C}"></div>
<div id="lab" class="abs label" style="left:100px;top:180px;color:{P}">Christmas</div>
<div id="t1" class="abs h" style="left:100px;right:100px;top:250px;font-size:120px;color:{P}">A cedar for<br>your tree.</div>
<div id="orn" class="abs" style="left:0;top:0;width:1080px;height:1920px;transform-origin:540px 580px">
  <div id="loop" class="abs" style="left:510px;top:580px;width:60px;height:60px;border-radius:50%;border:10px solid {SU};opacity:0"></div>
  <div id="str" class="abs" style="left:536px;top:638px;width:8px;height:62px;background:{SU};opacity:0"></div>
  {tier_html}
  <div id="trunk" class="abs" style="left:495px;top:{trunk_top}px;width:90px;height:76px;border-radius:0 0 22px 22px;background:{R};opacity:0"></div>
  <div id="tag" class="abs" style="left:0;right:0;top:{trunk_top + 110}px;text-align:center;font-size:72px;font-family:IS,Georgia,serif;color:{P};opacity:0">Maya · 2026</div>
</div>
<div id="t2" class="abs" style="left:100px;right:100px;top:1560px;font-size:46px;font-weight:500;color:{P};opacity:0">Lebanese cedar ornaments with a name or a year.<br>Coming this Christmas.</div>
{end_card(I, P, 'Christmas slots<br>are limited', 'DM “FIRST” to join the First Layer<br>and get priority')}
''', js=f'''
window.setT=t=>{{
  show('lab',prog(t,0,.6),30); show('t1',prog(t,.2,.9),40);
  const n={len(tiers)};
  document.getElementById('trunk').style.opacity=prog(t,1.0,1.3);
  for(let i=0;i<n;i++){{ const j=n-1-i; const a=1.3+i*0.42; const e=document.getElementById('tier'+j);
    const p=prog(t,a,a+.35); e.style.opacity=p; e.style.transform=`translateY(${{(1-p)*-60}}px)`; }}
  const s=1.3+n*0.42; show('str',prog(t,s,s+.3)); show('loop',prog(t,s+.2,s+.5)); show('tag',prog(t,s+.5,s+1.0),30);
  const sw=t>s+.6? Math.sin((t-s-.6)*3.2)*4*Math.exp(-(t-s-.6)*.5):0;
  document.getElementById('orn').style.transform=`rotate(${{sw}}deg)`;
  show('t2',prog(t,s+1.0,s+1.6),30);
  const e=prog(t,8.6,9.1); document.getElementById('end').style.opacity=e;
  show('e1',prog(t,8.9,9.5),40); show('e2',prog(t,9.3,9.9),40);
}};''')

REELS = [reel1, reel2, reel3]


def render(reel):
    with tempfile.TemporaryDirectory() as td, sync_playwright() as p:
        td = Path(td)
        page_file = td / 'reel.html'
        page_file.write_text(f'<html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>{reel["html"]}<script>{JS_HELPERS}{reel["js"]}</script></body></html>')
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(page_file.as_uri())
        pg.wait_for_timeout(500)
        n = int(reel['dur'] * FPS)
        for i in range(n):
            pg.evaluate(f'window.setT({i / FPS})')
            pg.screenshot(path=str(td / f'f{i:04d}.png'))
        pg.evaluate(f'window.setT({reel["dur"] * 0.45})')
        pg.screenshot(path=str(OUT / f'{reel["name"]}-v3-preview.png'))
        b.close()
        out = OUT / f'{reel["name"]}-v3.mp4'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(td / 'f%04d.png'),
                        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
                        '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(out)], check=True)
        print(out.name, out.stat().st_size // 1024, 'KB')


if __name__ == '__main__':
    flt = sys.argv[1:]
    for r in REELS:
        if not flt or any(f in r['name'] for f in flt):
            render(r)
