#!/usr/bin/env python3
""""From the Archive" history series: the vintage card builder.

Not run directly. tools/render.py hands every spec with "series": "archive" to build() here,
so the usual `python3 tools/render.py specs/<date>/<page>-archive-<slug>.json` renders them,
with the same fit checks and outputs as every other card.

Look: aged newsprint paper with grain and a vignette, letterpress serif (Playfair Display),
typewriter details (Special Elite), body copy in Old Standard TT, sepia ink, the page accent
dulled to an old print colour, photos shown as aged prints (sepia, grain, white border, a slight
tilt) with a typewritten credit. It must look old and still read instantly on a phone.

Slide templates (slides: [{"template": ..., "card": {...}}]):
- cover:   kicker, year, headline, deck?, stamp?, photo?
- story:   title?, text (60-90 words, first letter becomes a drop cap), pull? {big, label}
- ticket:  competition, round?, home, away, score?, rows [{label, value}] (date, venue, crowd)
- ledger:  title, rows [{label, value}] (max 6), note?
- thennow: title?, then {label, text}, now {label, text}
- end:     headline?, deck?

Spec level: "series": "archive", "archive": {"issue": 3}. Photos: card.photo = {"file": "media/archive/..jpg"}
with a sidecar from tools/archive_photo.py (credit line, licence). Headlines here are sentence case.
"""
from __future__ import annotations

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIZES = {'post': (1080, 1350), 'story': (1080, 1920)}

PAGES = {
    'lb': dict(name='SportsWire Lebanon', handle='@sportswire.lb', accent='#9E2A1F', place='Beirut'),
    'cy': dict(name='SportsWire Cyprus', handle='@sportswire.cy', accent='#9A6416', place='Nicosia'),
}
INK, INK2, PAPER, PAPER2, RULE = '#241A12', '#6A5844', '#EDE3CC', '#F5EEDC', '#2B2118'

# paper grain + fibres, multiplied over the page (pure SVG, no image files)
GRAIN = ("data:image/svg+xml;utf8," + re.sub(r'\s+', ' ', """
<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1350'>
<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>
<feColorMatrix values='0 0 0 0 .33  0 0 0 0 .25  0 0 0 0 .16  0 0 0 .55 0'/></filter>
<filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.012 .09' numOctaves='2' seed='7'/>
<feColorMatrix values='0 0 0 0 .45  0 0 0 0 .34  0 0 0 0 .2  0 0 0 .22 0'/></filter>
<rect width='100%' height='100%' filter='url(%23f)'/><rect width='100%' height='100%' filter='url(%23n)' opacity='.55'/>
</svg>""").replace('#', '%23').replace('%23f)', '%23f)').strip())


def esc(s) -> str:
    return html.escape(str(s if s is not None else ''), quote=True)


def rich(s) -> str:
    out = esc(str(s or ''))
    out = re.sub(r'(?<=\S) (?:v|vs|V|VS)\.? (?=\S)', ' <em class="ac">vs.</em> ', out)  # "vs.", in the accent (Geoffry, 23 Oct 2026)
    out = re.sub(r'\*(.+?)\*', r'<em class="ac">\1</em>', out)
    out = re.sub(r'(?<![\w-])(\d+-\d+|\d+-year-old)(?![\w-])', r'<span class="nb">\1</span>', out)  # never break a score or an age across lines
    return out.replace('\n', '<br>')


def photo_block(ph: dict, w: int, h: int, tilt: float = -1.4) -> tuple[str, list[str]]:
    """An aged print: sepia, grain, cream border, a slight tilt, typewritten credit underneath."""
    probs = []
    f = ROOT / ph['file']
    side = f.with_suffix('.json')
    meta = json.loads(side.read_text()) if side.exists() else {}
    credit = ph.get('credit') or meta.get('credit_line') or meta.get('credit') or ''
    if not f.exists():
        return '', [f'photo missing: {ph["file"]}']
    try:
        from PIL import Image
        iw, ih = Image.open(f).size
        if max(w / iw, h / ih) > 1.6:
            probs.append(f'photo {iw}x{ih} would be enlarged {max(w / iw, h / ih):.2f}x (max 1.6 for archive prints): pick a larger file or a smaller box')
    except Exception as e:  # noqa: BLE001
        probs.append(f'cannot read photo: {e}')
    fx, fy = (ph.get('focus') or meta.get('focus') or [50, 40])
    html_ = (f'<figure class="print" style="width:{w}px;transform:rotate({tilt}deg)">'
             f'<div class="pimg" style="height:{h}px;background-image:url({f.as_uri()});background-position:{fx}% {fy}%"></div>'
             f'<div class="pgrain"></div><span class="corner tl"></span><span class="corner tr"></span>'
             f'<span class="corner bl"></span><span class="corner br"></span></figure>'
             f'<div class="pcap" style="font-size:{17 if len(credit) + len(ph.get("note", "")) > 60 else 19}px">'
             f'{esc((ph["note"] + " · ").upper()) if ph.get("note") else ""}{esc(("PHOTO: " + credit).upper()) if credit else ""}</div>')
    return html_, probs


def masthead(page, spec, idx, total) -> str:
    issue = (spec.get('archive') or {}).get('issue')
    right = f'{idx:02d} / {total:02d}' if total > 1 else ''
    left = f'No. {int(issue):03d}' if issue else ''
    return (f'<div class="mast"><div class="mrow"><span class="ml">{esc(left)}</span>'
            f'<span class="mt">{esc(page["name"])}</span><span class="mr">{esc(right)}</span></div>'
            f'<div class="msub">· from the archive ·</div><div class="dbl"></div></div>')


def t_cover(c, acc, fmt):
    ph = c.get('photo')
    year = esc(c.get('year', ''))
    stamp = f'<div class="stamp">{esc(c["stamp"]).upper()}</div>' if c.get('stamp') else ''
    kick = f'<div class="kick">{esc(c.get("kicker", "")).upper()}</div>' if c.get('kicker') else ''
    dk = f'<div class="dk">{rich(c["deck"])}</div>' if c.get('deck') else ''
    if ph:
        W = 936
        Hh = c.get('photo_height', 520 if fmt == 'post' else 760)
        try:  # portrait photos become a narrower upright print so they aren't blown up
            from PIL import Image
            iw, ih = Image.open(ROOT / ph['file']).size
            if ih > iw:
                W, Hh = c.get('photo_width', 600), c.get('photo_height', 560 if fmt == 'post' else 800)
        except Exception:  # noqa: BLE001
            pass
        pb, probs = photo_block(ph, W - 36, Hh)
        top = (f'<div class="covtop">{kick}<div class="yrrow"><div class="year sm">{year}</div>{stamp}</div>'
               f'<div class="hl" data-size="{c.get("headline_size", 74)}" data-min="46" data-lines="{c.get("headline_lines", 3)}">{rich(c.get("headline", ""))}</div>{dk}</div>')
        return top + f'<div class="bd ph">{pb}</div>', probs
    body = (f'{kick}<div class="year">{year}</div>{stamp}'
            f'<div class="orn">✦ &nbsp; ✦ &nbsp; ✦</div>'
            f'<div class="hl" data-size="{c.get("headline_size", 88)}" data-min="52" data-lines="{c.get("headline_lines", 4)}">{rich(c.get("headline", ""))}</div>{dk}')
    return f'<div class="bd cov">{body}</div>', []


def t_story(c, acc, fmt):
    title = f'<div class="stt">{rich(c.get("title", "The story"))}</div>'
    text = str(c.get('text', '')).strip()
    first, rest = (text[0], text[1:]) if text else ('', '')
    pull = ''
    if c.get('pull'):
        p = c['pull']
        pull = f'<div class="pull"><div class="pbig">{esc(p.get("big", ""))}</div><div class="plab">{rich(p.get("label", ""))}</div></div>'
    ph = ''
    probs = []
    if c.get('photo'):
        ph, probs = photo_block(c['photo'], c.get('photo_w', 760), c.get('photo_h', 470), tilt=1.6)
        ph = f'<div class="sph">{ph}</div>'
    return (f'<div class="bd story">{title}<div class="cols"><p class="txt"><span class="drop">{esc(first)}</span>{rich(rest)}</p></div>'
            f'{ph}{pull}</div>'), probs


def t_ticket(c, acc, fmt):
    rows = ''.join(f'<div class="trow"><span class="tl">{esc(r["label"]).upper()}</span><span class="tv">{rich(r["value"])}</span></div>'
                   for r in c.get('rows', []))
    score = f'<div class="tscore">{esc(c["score"])}</div>' if c.get('score') else '<div class="tvs ac">vs.</div>'
    rnd = f'<div class="tround">{esc(c["round"]).upper()}</div>' if c.get('round') else ''
    title = f'<div class="stt">{rich(c["title"])}</div>' if c.get('title') else ''
    return (f'<div class="bd tk">{title}<div class="ticket"><div class="stub"><span>{esc(c.get("stub", "")).upper()}</span></div>'
            f'<div class="tmain"><div class="tcomp">{esc(c.get("competition", "")).upper()}</div>{rnd}'
            f'<div class="tteams"><div class="tt nw">{esc(c.get("home", ""))}</div>{score}<div class="tt nw">{esc(c.get("away", ""))}</div></div>'
            f'<div class="trows">{rows}</div></div></div>'
            + (f'<div class="tnote">{rich(c["note"])}</div>' if c.get('note') else '') + '</div>'), []


def t_ledger(c, acc, fmt):
    rows = ''.join(f'<div class="lrow"><span class="ll">{rich(r["label"])}</span><span class="ldots"></span><span class="lv">{rich(r["value"])}</span></div>'
                   for r in c.get('rows', []))
    note = f'<div class="lnote">{rich(c["note"])}</div>' if c.get('note') else ''
    return f'<div class="bd ledger"><div class="stt">{rich(c.get("title", "By the numbers"))}</div><div class="lrows">{rows}</div>{note}</div>', []


def t_thennow(c, acc, fmt):
    def col(d, cls):
        return f'<div class="tn {cls}"><div class="tnl">{esc(d.get("label", ""))}</div><div class="tnt">{rich(d.get("text", ""))}</div></div>'
    return (f'<div class="bd thennow"><div class="stt">{rich(c.get("title", "Then and now"))}</div>'
            f'<div class="tncols">{col(c.get("then", {}), "then")}<div class="tnsep"></div>{col(c.get("now", {}), "now")}</div></div>'), []


def t_end(c, acc, fmt):
    hl = c.get('headline', 'More from the archive every *Tuesday* and *Thursday*.')
    dk = c.get('deck', '')
    return (f'<div class="bd endc"><div class="orn">✦ &nbsp; ✦ &nbsp; ✦</div>'
            f'<div class="hl" data-size="{c.get("headline_size", 80)}" data-min="50" data-lines="4">{rich(hl)}</div>'
            + (f'<div class="dk">{rich(dk)}</div>' if dk else '') + '<div class="orn">✦ &nbsp; ✦ &nbsp; ✦</div></div>'), []


TEMPLATES = dict(cover=t_cover, story=t_story, ticket=t_ticket, ledger=t_ledger, thennow=t_thennow, end=t_end)


def css(W, H, acc, fonts_css) -> str:
    return f"""{fonts_css}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{PAPER};color:{INK};font-family:'Old Standard TT',serif;-webkit-font-smoothing:antialiased}}
.cv{{position:relative;width:{W}px;height:{H}px;padding:64px 72px 58px;display:flex;flex-direction:column;overflow:hidden;
  background:
   radial-gradient(ellipse 80% 65% at 50% 42%, rgba(255,251,238,.75), rgba(255,251,238,0) 70%),
   radial-gradient(ellipse 60% 40% at 88% 12%, rgba(160,120,60,.10), transparent 70%),
   radial-gradient(ellipse 50% 35% at 10% 92%, rgba(150,105,50,.12), transparent 70%),
   radial-gradient(ellipse 140% 120% at 50% 50%, transparent 55%, rgba(90,62,30,.38) 100%),
   {PAPER}}}
.cv::after{{content:'';position:absolute;inset:0;background-image:url("{GRAIN}");background-size:{W}px {H}px;mix-blend-mode:multiply;opacity:.9;pointer-events:none}}
.cv > *{{position:relative;z-index:1}}
.mast{{flex:none}}
.mrow{{display:flex;align-items:baseline;justify-content:space-between;gap:24px}}
.ml,.mr{{font:400 22px 'Special Elite';letter-spacing:.06em;color:{INK2};min-width:120px}}
.mr{{text-align:right}}
.mt{{font:700 30px 'Old Standard TT';letter-spacing:.32em;text-transform:uppercase;color:{INK};text-align:center}}
.msub{{text-align:center;font:italic 400 24px 'Old Standard TT';color:{INK2};margin-top:6px;letter-spacing:.06em}}
.dbl{{margin-top:14px;height:9px;border-top:4px solid {RULE};border-bottom:1.5px solid {RULE}}}
.kick{{font:400 26px 'Special Elite';letter-spacing:.14em;color:{acc};margin-top:34px}}
.year{{font:900 260px/0.86 'Playfair Display';letter-spacing:-.02em;color:{acc};margin-top:18px;
  text-shadow:4px 4px 0 rgba(36,26,18,.18);opacity:.94}}
.year.sm{{font-size:150px;margin-top:6px}}
.yrrow{{display:flex;align-items:center;justify-content:space-between;gap:20px}}
.stamp{{display:inline-block;align-self:flex-start;margin-top:18px;transform:rotate(-7deg);border:5px double {acc};color:{acc};
  font:400 34px 'Special Elite';letter-spacing:.12em;padding:12px 26px 10px;opacity:.9;filter:blur(.25px)}}
.yrrow .stamp{{margin-top:0}}
.orn{{text-align:center;color:{INK2};font:400 26px 'Old Standard TT';margin:26px 0 18px;letter-spacing:.2em}}
.hl{{font:900 88px/1.0 'Playfair Display';letter-spacing:-.01em;color:{INK};margin-top:18px}}
.hl .ac,.stt .ac,.dk .ac,.txt .ac,.tnt .ac,.lv .ac,.ll .ac,.plab .ac{{color:{acc};font-style:italic}}
.dk{{font:400 32px/1.36 'Old Standard TT';color:#3B2E22;margin-top:20px;max-width:900px}}
.bd{{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;overflow:hidden}}
.bd.cov{{justify-content:center}}
.bd.ph{{justify-content:center;align-items:center;padding-top:22px}}
.covtop{{flex:none}}
.print{{position:relative;background:#F8F2E2;padding:18px 18px 18px;box-shadow:0 18px 34px rgba(50,30,10,.30),0 2px 4px rgba(50,30,10,.25)}}
.pimg{{width:100%;background-size:cover;background-repeat:no-repeat;filter:grayscale(1) sepia(.55) contrast(1.12) brightness(.95)}}
.pgrain{{position:absolute;inset:18px;background-image:url("{GRAIN}");background-size:700px;mix-blend-mode:multiply;opacity:.75}}
.corner{{position:absolute;width:38px;height:38px;background:linear-gradient(135deg,#2B2118 50%,transparent 50%);opacity:.85}}
.corner.tl{{left:-6px;top:-6px}}
.corner.tr{{right:-6px;top:-6px;transform:rotate(90deg)}}
.corner.br{{right:-6px;bottom:-6px;transform:rotate(180deg)}}
.corner.bl{{left:-6px;bottom:-6px;transform:rotate(270deg)}}
.pcap{{font:400 19px 'Special Elite';letter-spacing:.06em;color:{INK2};margin-top:20px;text-align:center;max-width:920px}}
.stt{{font:italic 900 76px/1.05 'Playfair Display';color:{INK};margin:40px 0 30px;flex:none}}
.cols{{flex:none}}
.txt{{font:400 43px/1.42 'Old Standard TT';color:#2E2319;text-align:left}}
.drop{{float:left;font:900 172px/0.8 'Playfair Display';color:{acc};margin:8px 18px 0 0}}
.sph{{display:flex;flex-direction:column;align-items:center;margin-top:26px}}
.pull{{margin-top:auto;border-top:2px solid {RULE};border-bottom:2px solid {RULE};padding:20px 0;display:flex;align-items:center;gap:30px}}
.pbig{{font:900 128px/1 'Playfair Display';color:{acc};flex:none}}
.plab{{font:italic 400 38px/1.3 'Old Standard TT';color:#3B2E22}}
.bd.tk{{justify-content:center}}
.ticket{{display:flex;background:{PAPER2};border:2px solid {RULE};box-shadow:0 16px 34px rgba(50,30,10,.24);transform:rotate(-1.2deg);margin-top:10px}}
.stub{{flex:none;width:96px;border-right:3px dashed {RULE};display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.03)}}
.stub span{{writing-mode:vertical-rl;transform:rotate(180deg);font:400 26px 'Special Elite';letter-spacing:.3em;color:{acc}}}
.tmain{{flex:1;padding:44px 46px 40px;min-width:0}}
.tcomp{{font:700 30px 'Old Standard TT';letter-spacing:.22em;color:{INK};text-align:center}}
.tround{{font:400 28px 'Special Elite';letter-spacing:.16em;color:{acc};text-align:center;margin-top:10px}}
.tteams{{display:flex;flex-direction:column;align-items:center;gap:4px;margin:26px 0 22px;border-top:1.5px solid {RULE};border-bottom:1.5px solid {RULE};padding:22px 0}}
.tt{{font:900 74px/1.08 'Playfair Display';color:{INK};text-align:center;max-width:100%;white-space:nowrap;overflow:hidden}}
.tscore{{font:900 150px/1 'Playfair Display';color:{acc};letter-spacing:.02em}}
.tvs{{font:italic 400 44px 'Old Standard TT';color:{INK2}}}
.trows{{display:flex;flex-direction:column;gap:16px}}
.trow{{display:flex;justify-content:space-between;gap:20px;align-items:baseline}}
.tl{{font:400 26px 'Special Elite';letter-spacing:.14em;color:{INK2};flex:none}}
.tv{{font:400 36px 'Old Standard TT';color:{INK};text-align:right}}
.tnote{{font:italic 400 34px/1.35 'Old Standard TT';color:#3B2E22;margin-top:40px;text-align:center}}
.lrows{{display:flex;flex-direction:column;justify-content:space-evenly;flex:1;min-height:0;padding:10px 0 20px}}
.lrow{{display:flex;align-items:baseline;gap:14px}}
.ll{{font:400 44px/1.2 'Old Standard TT';color:#2E2319;max-width:620px}}
.ldots{{flex:1;border-bottom:4px dotted {INK2};transform:translateY(-10px);min-width:30px}}
.lv{{font:900 76px 'Playfair Display';color:{acc};white-space:nowrap}}
.lnote{{flex:none;font:400 24px/1.4 'Special Elite';color:{INK2};border-top:1.5px solid {RULE};padding-top:16px}}
.tncols{{display:flex;gap:34px;flex:1;min-height:0;padding-bottom:10px}}
.tn{{flex:1;display:flex;flex-direction:column;min-width:0}}
.tnl{{font:900 120px/1 'Playfair Display';color:{acc};border-bottom:2px solid {RULE};padding-bottom:14px;margin-bottom:26px}}
.tn.now .tnl{{color:{INK}}}
.tnt{{font:400 40px/1.38 'Old Standard TT';color:#2E2319}}
.tnsep{{width:2px;background:{RULE};opacity:.7}}
.bd.endc{{justify-content:center;align-items:center;text-align:center}}
.endc .hl{{text-align:center}}
.endc .dk{{text-align:center}}
.ft{{flex:none;display:flex;justify-content:space-between;align-items:center;border-top:1.5px solid {RULE};padding-top:14px;margin-top:20px}}
.fl{{font:400 22px 'Special Elite';letter-spacing:.08em;color:{INK2}}}
.fr{{font:400 22px 'Special Elite';letter-spacing:.1em;color:{INK}}}
.nw{{white-space:nowrap}}
.nb{{white-space:nowrap}}
"""


def build(slide: dict, spec: dict, idx: int, total: int, fonts_css: str) -> tuple[str, int, int, list[str]]:
    page = PAGES[spec['page']]
    fmt = spec.get('format', 'post')
    W, H = SIZES[fmt]
    acc = page['accent']
    tpl = slide['template']
    c = dict(slide.get('card', {}))
    body, probs = TEMPLATES[tpl](c, acc, fmt)
    left = c.get('footnote') or ('Swipe for the story  →' if tpl == 'cover' and total > 1 else 'From the archive')
    ft = f'<div class="ft"><span class="fl">{esc(left)}</span><span class="fr">{esc(page["handle"]).upper()}</span></div>'
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{css(W, H, acc, fonts_css)}</style></head>'
           f'<body><div class="cv">{masthead(page, spec, idx, total)}{body}{ft}</div></body></html>')
    return doc, W, H, probs
