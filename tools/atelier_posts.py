"""Ply posts in the Atelier style (route A6, from 17 Oct 2026). Reference generator: copy it and change only the content.
Usage: python3 tools/atelier_posts.py [name-filter]  -> renders into build/ as ply-post-NN-name-v2.png"""
import math
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

S = Path(__file__).resolve().parent.parent
FS = Path(__file__).resolve().parent / 'fonts'
OUT = S / 'build'
OUT.mkdir(exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
faces = ''.join(f"@font-face{{font-family:SG;font-weight:{w};src:url('{(FS/f'space-grotesk/files/space-grotesk-latin-{w}-normal.woff2').as_uri()}')}}" for w in (400, 500, 700))
faces += f"@font-face{{font-family:PA;font-weight:600;src:url('{(FS/'noto-naskh-arabic/files/noto-naskh-arabic-arabic-600-normal.woff2').as_uri()}')}}"
faces += ''.join(f"@font-face{{font-family:IS;font-style:{st};font-weight:400;src:url('{(FS/f'instrument-serif/files/instrument-serif-latin-400-{st}.woff2').as_uri()}')}}" for st in ('normal', 'italic'))

# Atelier palette. Names kept from the old generator: C=terracotta, SU=sand, R=clay, I=charcoal, P=bone
C, SU, R, I, P = '#B4532A', '#CDBFA8', '#DDB8A2', '#1C1B19', '#EFEAE2'
THEME = {  # bg: (fg, muted, (word colour, dot colour))
    P: (I, '#6E6A63', (I, C)),
    SU: (I, '#4A463F', (I, C)),
    R: (I, '#4A3B33', (I, C)),
    I: (P, SU, (P, C)),
    C: (P, '#F3E3D6', (P, I)),
}
CSS = faces + """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;font-family:SG,sans-serif;overflow:hidden}
.p{width:1080px;height:1350px;padding:96px 104px 88px;display:flex;flex-direction:column}
.label{font-size:21px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;display:flex;justify-content:space-between}
.h{margin-top:30px;font-family:IS,Georgia,serif;font-weight:400;letter-spacing:-.01em;line-height:.95}
.h i{font-style:italic}
.mid{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;position:relative}
.bottom{display:flex;justify-content:space-between;align-items:flex-end;gap:48px}
.body{font-size:32px;font-weight:500;line-height:1.35;max-width:740px}
.pill{border-radius:999px;font-weight:500;display:inline-block;white-space:nowrap;letter-spacing:-.01em}
"""


def symbol(cols, h=24):
    word, dot = cols
    return f'<div style="display:flex;align-items:baseline;flex-shrink:0"><span style="font-family:IS,Georgia,serif;font-size:{h*2.4:.0f}px;line-height:.8;color:{word}">Ply</span><span style="display:inline-block;width:{h*.32:.0f}px;height:{h*.32:.0f}px;border-radius:50%;background:{dot};margin-left:{h*.08:.0f}px"></span></div>'


def page(bg, label, headline, mid, body, hsize=104):
    fg, muted, sym = THEME[bg]
    return f"""<div class="p" style="background:{bg};color:{fg}">
<div class="label" style="color:{muted if bg in (I,) else fg}"><span>{label}</span><span>@plymakes</span></div>
<div class="h" style="font-size:{round(hsize*1.18)}px">{headline}</div>
<div class="mid">{mid}</div>
<div class="bottom"><div class="body" style="color:{muted if bg in (P, I, SU) else fg}">{body}</div>{symbol(sym)}</div>
</div>"""


def stagger(items, size=40, pad='20px 36px', step=28, gap=16):
    n = len(items)
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px;align-items:flex-start;width:100%">' + ''.join(
        f'<div class="pill" style="background:{b};color:{f};padding:{pad};font-size:{size}px;margin-left:{(n-1-i)*step}px">{t}</div>' for i, (t, b, f) in enumerate(items)) + '</div>'


posts = {}

# 7 paper: things you can print
posts['ply-post-07-you-can-print-that'] = page(P, 'What can a 3D printer make?', 'You can 3D print <i style="color:#B4532A">that?</i>',
    stagger([('Your name in Arabic', C, P), ('A lamp made from a photo', SU, I), ('A dragon that moves', R, I), ('The clip you lost', I, P), ('A pot for your plant', C, P), ('Your kid’s drawing', SU, I)], size=38),
    'Six real things a home-sized printer makes every day. More on each one soon.', hsize=112)

# 8 sun: how long
rows = [('Name keychain', '≈ 30 min', 70), ('Phone stand', '≈ 2 hours', 170), ('Flower vase', '≈ 6 hours', 300), ('Cosplay helmet', '1–2 days', 470)]
bars = '<div style="width:100%;display:flex;flex-direction:column;gap:30px">' + ''.join(
    f'<div><div style="font-size:34px;font-weight:700;margin-bottom:10px">{n}<span style="font-weight:500;color:#3B3E45">&nbsp;&nbsp;{t}</span></div><div style="height:40px;width:{w+120}px;border-radius:20px;background:{c}"></div></div>'
    for (n, t, w), c in zip(rows, (I, R, C, I))) + '</div>'
posts['ply-post-08-how-long'] = page(SU, 'Print times', 'How long does a print take?', bars,
    'Approximate times. Size, detail and strength all change the clock.', hsize=100)

# 9 coral: flexi dragon
segs = ''
for k in range(15):
    x = 120 + k * 46
    y = 200 + 90 * math.sin(k / 14 * 2 * math.pi)
    s = 74 - k * 3
    col = [I, P, C][k % 3]
    segs += f'<div style="position:absolute;left:{x:.0f}px;top:{y - s/2:.0f}px;width:{s*0.72:.0f}px;height:{s:.0f}px;border-radius:{s*0.36:.0f}px;background:{col}"></div>'
head = '<div style="position:absolute;left:24px;top:142px;width:120px;height:104px;border-radius:52px 60px 60px 52px;background:#13151A"></div><div style="position:absolute;left:52px;top:170px;width:22px;height:22px;border-radius:11px;background:#F3F0E8"></div>'
posts['ply-post-09-flexi-dragon'] = page(R, 'Print-in-place', 'Printed in one piece. It still moves.',
    f'<div style="position:relative;width:860px;height:400px">{segs}{head}</div>',
    'The joints print already linked: no glue, no assembly. Flexi toys are a kids’ favourite.', hsize=100)

# 10 ink: lithophane
ridges = ''.join(f'<div style="height:6px;background:rgba(19,21,26,.06);margin-top:14px"></div>' for _ in range(18))
lit = """<div style="position:relative;width:340px;height:440px;border-radius:20px;overflow:hidden;background:radial-gradient(circle at 50% 38%,#FFF4D6 0%,#FFD98A 45%,#E9A24A 100%)">
<div style="position:absolute;left:150px;top:90px;width:90px;height:90px;border-radius:50%;background:#FFFBEF"></div>
<div style="position:absolute;left:-40px;top:250px;width:260px;height:260px;border-radius:50%;background:#B8742E"></div>
<div style="position:absolute;left:150px;top:290px;width:300px;height:300px;border-radius:50%;background:#8C5420"></div>
<div style="position:absolute;left:40px;top:360px;width:280px;height:200px;border-radius:50%;background:#6B3D16"></div></div>"""
off = f'<div style="width:340px;height:440px;border-radius:20px;background:#E6E1D5;padding-top:8px">{ridges}</div>'
cap = lambda t: f'<div style="margin-top:20px;font-size:28px;font-weight:500;color:#A9ACB3;text-align:center">{t}</div>'
posts['ply-post-10-lithophane'] = page(I, 'Lithophane', 'A photo hidden in plastic.',
    f'<div style="display:flex;gap:56px"><div>{off}{cap("Light off")}</div><div>{lit}{cap("Light on")}</div></div>',
    'Thick areas block light, thin areas glow. Any photo can become a night lamp.', hsize=104)

# 11 cobalt: Arabic name
name = 'ليلى'
layers = ''.join(f'<div dir="rtl" lang="ar" style="position:absolute;left:{x}px;top:{y}px;font-family:PA;font-weight:600;font-size:300px;line-height:1;color:{c}">{name}</div>'
                 for x, y, c in [(36, 36, SU), (24, 24, R), (12, 12, R), (0, 0, P)])
posts['ply-post-11-arabic-name'] = page(C, 'Name signs', 'Your name. In Arabic. In 3D.',
    f'<div style="position:relative;width:560px;height:440px;margin-top:-20px">{layers}<div style="position:absolute;left:-20px;right:-60px;top:400px;height:44px;border-radius:22px;background:#13151A"></div></div>',
    'Name signs and keychains in Arabic or English, in the colours you choose.', hsize=104)

# 12 paper: myth vs fact
def mf(myth, fact):
    return f'''<div style="display:flex;flex-direction:column;gap:14px;width:100%">
<div style="display:flex;gap:20px;align-items:baseline"><span class="pill" style="background:{R};color:{I};padding:8px 20px;font-size:24px">MYTH</span><span style="font-size:38px;font-weight:700;letter-spacing:-.02em;text-decoration:line-through;text-decoration-thickness:4px;color:#5C5F66">{myth}</span></div>
<div style="display:flex;gap:20px;align-items:baseline"><span class="pill" style="background:{C};color:{P};padding:8px 20px;font-size:24px">FACT</span><span style="font-size:38px;font-weight:700;letter-spacing:-.02em;line-height:1.2">{fact}</span></div></div>'''
posts['ply-post-12-myth-fact'] = page(P, 'Myth vs fact', 'Myth vs fact.',
    f'<div style="display:flex;flex-direction:column;gap:64px;width:100%">{mf("It’s only for engineers.", "Send an idea or a photo. We handle the technical part.")}{mf("3D prints break easily.", "Tough materials like PETG make clips, hooks and car mounts.")}</div>',
    'Got another 3D printing question? Ask it in the comments.', hsize=112)

# 13 sun: kids drawing
pts = []
for k in range(11):
    a = -math.pi / 2 + k * math.pi / 5
    r = 150 if k % 2 == 0 else 64
    j = [6, -8, 10, -4, 7, -9, 5, -6, 8, -5, 6][k]
    pts.append((190 + (r + j) * math.cos(a), 200 + (r + j) * math.sin(a)))
doodle = ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
clean = []
for k in range(10):
    a = -math.pi / 2 + k * math.pi / 5
    r = 150 if k % 2 == 0 else 64
    clean.append((190 + r * math.cos(a), 200 + r * math.sin(a)))
cl = ' '.join(f'{x:.0f},{y:.0f}' for x, y in clean)
paper_card = f'''<div style="width:380px;height:420px;background:#FFFFFF;border-radius:20px;transform:rotate(-4deg)"><svg width="380" height="420"><polyline points="{doodle}" fill="none" stroke="{C}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="168" cy="200" r="7" fill="{I}"/><circle cx="212" cy="200" r="7" fill="{I}"/><path d="M168 228 q22 18 44 0" fill="none" stroke="{I}" stroke-width="7" stroke-linecap="round"/></svg></div>'''
solid = f'''<svg width="400" height="440"><circle cx="190" cy="34" r="30" fill="none" stroke="{I}" stroke-width="10"/>
<polygon points="{cl}" transform="translate(16 46)" fill="{I}"/><polygon points="{cl}" transform="translate(8 38)" fill="{C}"/><polygon points="{cl}" transform="translate(0 30)" fill="{R}"/>
<circle cx="190" cy="94" r="14" fill="{SU}"/><circle cx="168" cy="230" r="7" fill="{I}"/><circle cx="212" cy="230" r="7" fill="{I}"/><path d="M168 258 q22 18 44 0" fill="none" stroke="{I}" stroke-width="7" stroke-linecap="round"/></svg>'''
arrow = f'<div style="font-size:80px;font-weight:700">→</div>'
posts['ply-post-13-kids-drawing'] = page(SU, 'Little designers', 'Your kid draws it. Ply prints it.',
    f'<div style="display:flex;align-items:center;gap:20px">{paper_card}{arrow}{solid}</div>',
    'We trace the drawing and turn it into a keychain or fridge magnet they can keep.', hsize=104)

# 14 coral: matte vs silk
disc = lambda bgc, lab, sub: f'<div style="display:flex;flex-direction:column;align-items:center;gap:24px"><div style="width:360px;height:360px;border-radius:50%;background:{bgc}"></div><div style="font-size:44px;font-weight:700">{lab}</div><div style="font-size:28px;font-weight:500;margin-top:-16px">{sub}</div></div>'
silk = 'linear-gradient(135deg,#8C5A12 0%,#E8B44A 30%,#FFF1C4 48%,#E0A73A 62%,#7A4B0E 100%)'
posts['ply-post-14-matte-or-silk'] = page(R, 'This or that?', 'Matte or silk?',
    f'<div style="display:flex;gap:64px">{disc(C, "A · Matte", "Soft, no shine")}{disc(silk, "B · Silk", "Shiny, metallic")}</div>',
    'Same print, two finishes. Vote A or B in the comments ↓', hsize=124)

# 15 ink: remote battery cover
btn = ''.join(f'<div style="width:44px;height:44px;border-radius:22px;background:#3A3E48"></div>' for _ in range(9))
remote = f'''<div style="position:relative;width:250px;height:600px;border-radius:60px;background:#2A2D35;padding:60px 52px">
<div style="width:56px;height:56px;border-radius:28px;background:{R};margin:0 auto 40px"></div>
<div style="display:grid;grid-template-columns:repeat(3,44px);gap:30px 26px;justify-content:center">{btn}</div>
<div style="position:absolute;left:44px;right:44px;bottom:40px;height:180px;border-radius:30px;border:4px dashed #6E727A"></div></div>'''
cover = f'<div style="width:162px;height:180px;border-radius:30px;background:{SU};transform:rotate(14deg);margin-left:56px;margin-top:300px"></div>'
posts['ply-post-15-battery-cover'] = page(I, 'Ply makes it fit', 'Lost the battery cover? Again?',
    f'<div style="display:flex;align-items:flex-start">{remote}{cover}</div>',
    'Covers, clips and knobs can often be measured, redesigned and printed. Coming soon.', hsize=100)

# 16 cobalt: cedar ornament
tiers = [(150, 0), (250, 1), (340, 0), (220, 1), (330, 0), (430, 1), (300, 0), (420, 0), (520, 1)]
cedar = '<div style="display:flex;flex-direction:column;align-items:center;gap:10px">'
cedar += f'<div style="width:46px;height:46px;border-radius:50%;border:8px solid {SU};margin-bottom:-4px"></div><div style="width:6px;height:40px;background:{SU}"></div>'
for w, alt in tiers:
    cedar += f'<div style="width:{w}px;height:36px;border-radius:18px;background:{P if not alt else "#E3D9C9"}"></div>'
cedar += f'<div style="width:70px;height:60px;border-radius:0 0 18px 18px;background:{R}"></div></div>'
posts['ply-post-16-cedar-ornament'] = page(C, 'Christmas', 'A cedar for your tree.', cedar,
    'Lebanese cedar ornaments with a name or a year. Coming this Christmas.', hsize=112)

# 17 paper: desk glow-up
hp = f'''<div style="position:relative;width:200px;height:380px"><div style="position:absolute;left:84px;top:40px;width:32px;height:320px;border-radius:16px;background:{C}"></div>
<div style="position:absolute;left:30px;top:20px;width:140px;height:40px;border-radius:20px;background:{C}"></div>
<div style="position:absolute;left:20px;top:340px;width:160px;height:40px;border-radius:20px;background:{C}"></div></div>'''
ph = f'''<div style="position:relative;width:200px;height:380px"><div style="position:absolute;left:70px;top:90px;width:110px;height:230px;border-radius:24px;background:{I};transform:rotate(-14deg)"></div>
<div style="position:absolute;left:20px;top:300px;width:170px;height:80px;border-radius:24px;background:{R}"></div></div>'''
clips = '<div style="display:flex;flex-direction:column;gap:22px;justify-content:flex-end;height:380px">' + ''.join(
    f'<div style="width:180px;height:56px;border-radius:28px;background:{c};position:relative"><div style="position:absolute;left:70px;top:-6px;width:40px;height:30px;border-radius:15px;background:#F3F0E8"></div></div>' for c in (SU, R, C)) + '</div>'
lab = lambda t: f'<div style="font-size:28px;font-weight:700;margin-top:24px;text-align:center">{t}</div>'
posts['ply-post-17-desk-glow-up'] = page(P, 'Desk setup', 'Desk glow-up.',
    f'<div style="display:flex;gap:64px;align-items:flex-end"><div>{hp}{lab("Headphone stand")}</div><div>{ph}{lab("Phone stand")}</div><div>{clips}{lab("Cable clips")}</div></div>',
    'Small prints that make a desk feel like yours. Pick the colours to match.', hsize=124)

# 18 sun: plant pots
def pot(widths, col, leaf):
    s = '<div style="display:flex;flex-direction:column;align-items:center">'
    s += f'<div style="position:relative;width:200px;height:150px"><div style="position:absolute;left:58px;top:30px;width:60px;height:120px;border-radius:60px 0;background:{leaf};transform:rotate(-20deg)"></div><div style="position:absolute;left:96px;top:10px;width:56px;height:130px;border-radius:0 56px;background:{leaf};transform:rotate(18deg)"></div></div>'
    s += ''.join(f'<div style="width:{w}px;height:24px;border-radius:12px;background:{col};margin-top:5px"></div>' for w in widths)
    return s + '</div>'
pots = f'<div style="display:flex;gap:48px;align-items:flex-end">{pot([210,200,190,180,170,160,150,140,130], C, '#6F7D5C')}{pot([150,180,200,210,210,200,180,150], R, '#6F7D5C')}{pot([170,170,170,170,170,170,170,170,170,170,170], I, '#6F7D5C')}</div>'
posts['ply-post-18-plant-pots'] = page(SU, 'Plant people', 'Your plants deserve better pots.', pots,
    'Self-watering pots, succulent planters and wall pots, in any colour.', hsize=104)

# 19 coral: pet tag
tag = f'''<div style="position:relative;width:640px;height:300px">
<div style="position:absolute;left:0;top:20px;width:160px;height:160px;border-radius:50%;background:{P}"></div>
<div style="position:absolute;left:0;top:120px;width:160px;height:160px;border-radius:50%;background:{P}"></div>
<div style="position:absolute;right:0;top:20px;width:160px;height:160px;border-radius:50%;background:{P}"></div>
<div style="position:absolute;right:0;top:120px;width:160px;height:160px;border-radius:50%;background:{P}"></div>
<div style="position:absolute;left:80px;right:80px;top:60px;height:180px;background:{P}"></div>
<div style="position:absolute;left:0;right:0;top:92px;text-align:center;font-size:110px;font-weight:700;letter-spacing:.02em;color:{I}">LUNA</div>
<div style="position:absolute;left:-70px;top:115px;width:70px;height:70px;border-radius:50%;border:12px solid {I}"></div></div>'''
posts['ply-post-19-pet-tag'] = page(R, 'For pets', 'For the good boys and girls.', tag,
    'Name tags with your number on the back. Light, tough, any colour.', hsize=104)

# 20 ink: guess the object (pawn)
prof = [60, 64, 70, 76, 80, 80, 76, 70, 60, 50, 46, 44, 46, 50, 56, 64, 72, 80, 90, 100, 110, 120, 130, 140, 150, 156, 160]
pawn = '<div style="display:flex;flex-direction:column;align-items:center;gap:4px">' + ''.join(
    f'<div style="width:{w*2.2:.0f}px;height:14px;border-radius:7px;background:{SU if i < 9 else (R if i < 15 else P)}"></div>' for i, w in enumerate(prof)) + '</div>'
posts['ply-post-20-guess-the-object'] = page(I, 'Quiz', 'Guess what we’re printing.', pawn,
    'Every 3D print is just layers like these. Answer in the comments ↓', hsize=104)

# 21 cobalt: PLA from plants
flow = stagger([('Corn or sugarcane', SU, I), ('Plant starch', R, I), ('PLA filament', P, I), ('Your print', I, P)], size=44, pad='24px 44px', step=40, gap=20)
posts['ply-post-21-pla-from-plants'] = page(C, 'Did you know?', 'Our plastic starts as a plant.',
    f'<div style="width:100%">{flow}</div>',
    'PLA, the most common printing material, is made from plant starch instead of oil.', hsize=104)

# 22 paper: board game organiser
cells = [(0, 0, 2, 1, C), (2, 0, 1, 1, R), (0, 1, 1, 2, SU), (1, 1, 2, 1, I), (1, 2, 1, 1, R), (2, 2, 1, 1, C)]
grid = '<div style="position:relative;width:660px;height:480px;border-radius:28px;background:#DCD8CE;padding:20px">'
for x, y, w, h, c in cells:
    grid += f'<div style="position:absolute;left:{20+x*210}px;top:{20+y*150}px;width:{w*210-16}px;height:{h*150-16}px;border-radius:20px;background:{c};display:flex;flex-wrap:wrap;gap:12px;padding:22px;align-content:flex-start">' + ''.join(
        f'<div style="width:28px;height:28px;border-radius:50%;background:{P if c in (C, I, R) else I};opacity:.9"></div>' for _ in range(min(6, w*h*3))) + '</div>'
grid += '</div>'
posts['ply-post-22-board-games'] = page(P, 'Game night', 'Game night, sorted.', grid,
    'Custom inserts and token trays that fit your favourite board game box.', hsize=124)

# 23 sun: wedding favours
kc = lambda t, b, f, rot: f'<div style="display:flex;align-items:center;transform:rotate({rot}deg)"><div style="width:64px;height:64px;border-radius:50%;border:10px solid {I};margin-right:-6px"></div><div class="pill" style="background:{b};color:{f};padding:22px 44px;font-size:56px;letter-spacing:-.02em">{t}</div></div>'
posts['ply-post-23-wedding-favours'] = page(SU, 'Weddings and events', 'Favours your guests will actually keep.',
    f'<div style="display:flex;flex-direction:column;gap:40px;align-items:center">{kc("Nour &amp; Karim", C, P, -4)}{kc("12 · 06 · 2027", I, P, 3)}{kc("Table 7", R, I, -2)}</div>',
    'Name keychains, place cards and table numbers for weddings, baptisms and birthdays.', hsize=100)

# 24 coral: for businesses
posts['ply-post-24-for-business'] = page(R, 'For businesses', 'Your logo, printed.',
    stagger([('Logo keychains', I, P), ('Table numbers', P, I), ('Menu and QR stands', C, P), ('Display props', I, P)], size=46, pad='24px 44px', step=40, gap=20),
    'For cafés, shops and events in Lebanon. Message us to be first in line.', hsize=124)

# 25 ink: colours
spools = [('#F7F7F2', 'White'), ('#0E0F12', 'Black'), ('#2B55F5', 'Blue'), ('#E23B3B', 'Red'), ('#F2C230', 'Yellow'), ('#E8603C', 'Orange'), ('#6F7D5C', 'Green'), ('#7B4BD6', 'Purple'), ('#9AA0A8', 'Grey'), (silk, 'Silk gold'), ('#CFF5C9', 'Glow'), ('#7FC8F8', 'Sky')]
sp = '<div style="display:grid;grid-template-columns:repeat(4,170px);gap:36px 40px">' + ''.join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px"><div style="width:150px;height:150px;border-radius:50%;background:{c};display:flex;align-items:center;justify-content:center;{"border:3px solid #33363E;" if n=="Black" else ""}"><div style="width:44px;height:44px;border-radius:50%;background:#13151A;border:6px solid #33363E"></div></div><div style="font-size:26px;font-weight:500;color:#A9ACB3">{n}</div></div>'
    for c, n in spools) + '</div>'
posts['ply-post-25-pick-your-colours'] = page(I, 'Materials', 'Pick your colours.', sp,
    'Matte, silk and glow-in-the-dark, and you can mix colours in one print.', hsize=124)

# 26 cobalt: printer on its way
prog = '<div style="width:100%"><div style="display:flex;flex-direction:column-reverse;gap:10px">' + ''.join(
    f'<div style="height:34px;border-radius:17px;background:{(SU if i < 7 else "rgba(243,240,232,.18)")};width:{100 - (9-i)*2}%"></div>' for i in range(10)) + '</div>' \
    + f'<div style="margin-top:28px;font-size:34px;font-weight:700">Arriving in November</div></div>'
posts['ply-post-26-printer-on-its-way'] = page(C, 'Coming soon', 'Our printer is on its way.', prog,
    'Follow along for the first prints, the first fails and the first orders.', hsize=112)

only = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for n, h in posts.items():
        if only and not any(o in n for o in only):
            continue
        f = OUT / f'{n}.html'
        f.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>')
        pg.goto(f.as_uri())
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f'{n}-v2.png'))
    b.close()
print(len(posts), 'posts')
