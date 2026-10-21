#!/usr/bin/env python3
"""SportsWire card renderer: JSON spec in, on-brand PNG(s) out.

    python3 tools/render.py specs/2026-10-19/lb-slug.json [more.json ...]

Every card is built from the fixed templates below, so every post matches the
house style (ink/bone, Rubik ExtraBold lowercase headlines, Manrope body,
JetBrains Mono scores and labels, LB red / CY amber accent). The page lays
itself out, shrinks the headline to fit, and reports anything that still
overflows. Exit code 2 means at least one card has a layout problem: fix the
text (shorter headline, fewer rows) and render again. Never schedule a card
that failed.

Spec format: tools/README.md.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS_CSS = (ROOT / 'tools/fonts/fonts.css').read_text().replace('url(./files/', f"url({(ROOT / 'tools/fonts/files').as_uri()}/")

PAGES = {
    'lb': dict(name='SPORTSWIRE LEBANON', handle='@SPORTSWIRE.LB', accent={'dark': '#FF3B30', 'light': '#FF3B30'},
               glow='radial-gradient(900px 700px at 0% 100%, rgba(255,59,48,.13), transparent 70%)'),
    'cy': dict(name='SPORTSWIRE CYPRUS', handle='@SPORTSWIRE.CY', accent={'dark': '#FFB300', 'light': '#E38C00'},
               glow='radial-gradient(800px 650px at 100% 0%, rgba(255,179,0,.12), transparent 70%)'),
}
THEMES = {
    'dark': dict(bg='#16171B', fg='#FAFAF8', muted='#A6AAB4', faint='#7E838F', panel='rgba(255,255,255,.035)',
                 panel2='rgba(255,255,255,.07)', line='rgba(255,255,255,.12)', tile='#FAFAF8', invbg='#FAFAF8', invfg='#16171B'),
    'light': dict(bg='#F3F1EB', fg='#16171B', muted='#66655F', faint='#8A867D', panel='#FAFAF8',
                  panel2='#FFFFFF', line='#DEDAD0', tile='#FFFFFF', invbg='#16171B', invfg='#FAFAF8'),
}
TONES = {  # medal / badge colours per theme
    'gold': {'dark': '#FFB300', 'light': '#D98A00'},
    'silver': {'dark': '#C9CBD1', 'light': '#8A8D96'},
    'bronze': {'dark': '#C08552', 'light': '#A86B3C'},
}
SIZES = {'post': (1080, 1350), 'story': (1080, 1920), 'reel': (1080, 1920)}


# ----------------------------------------------------------------- text helpers

def esc(s) -> str:
    return html.escape(str(s if s is not None else ''), quote=True)


def rich(s, lower=False) -> str:
    """Escape, then *accent* -> accent span, newline -> <br>."""
    s = str(s or '')
    if lower:
        s = s.lower()
    out = esc(s)
    out = re.sub(r'\*(.+?)\*', r'<span class="ac">\1</span>', out)
    return out.replace('\n', '<br>')


def headline(s) -> str:
    s = str(s or '').strip()
    core = s.rstrip('*')
    if core and core[-1].isalnum():
        s += '.'
    return rich(s, lower=True)


def eyebrow(e) -> str:
    if not e:
        return ''
    parts = e if isinstance(e, list) else [e]
    return ' &nbsp;·&nbsp; '.join(esc(p).upper() for p in parts)


def crest(name, size=72, tile=True) -> str:
    if not name:
        return ''
    f = ROOT / 'brand/crests' / f'{name}.png'
    if not f.exists():
        print(f'  ! crest "{name}" not in brand/crests, left out', file=sys.stderr)
        return ''
    img = f'<img src="{f.as_uri()}" style="max-width:{size*0.78:.0f}px;max-height:{size*0.78:.0f}px">'
    if not tile:
        return f'<span class="crest" style="width:{size}px;height:{size}px">{img}</span>'
    return f'<span class="crest tile" style="width:{size}px;height:{size}px">{img}</span>'


def kv_rows(rows) -> str:
    return '<div class="kv">' + ''.join(
        f'<div class="kvr"><span class="k">{esc(r["label"]).upper()}</span><span class="v nw">{rich(r["value"])}</span></div>'
        for r in rows) + '</div>'


# ----------------------------------------------------------------- photos
# A card can carry an official event photo (PLAYBOOK, Images and rights): "photo": {"file": "media/photos/…jpg",
# "focus": [x%, y%], "credit": "Sagesse SC"}. Credit and focus default to the photo's sidecar JSON.
# Posts and Stories: a hero band across the top that fades into ink, the headline overlapping its foot.
# Reels: a taller band with a slow push-in while the text builds underneath.
PHOTO_BOX = {'post': 640, 'story': 960, 'reel': 1060}
PHOTO_MIN = {'post': 540, 'story': 760, 'reel': 760}
MAX_UPSCALE = 1.25


def photo_parts(ph: dict, fmt: str, W: int, pad_t: int, pad_r: int) -> tuple[str, str, list[str]]:
    """-> (html placed first inside .cv, spacer html after the header, problems)"""
    probs = []
    f = ROOT / ph['file']
    side = {}
    if f.with_suffix('.json').exists():
        side = json.loads(f.with_suffix('.json').read_text())
    if not f.exists():
        return '', '', [f'photo file missing: {ph["file"]}']
    from PIL import Image
    iw, ih = Image.open(f).size
    # the band shrinks to what the photo can fill sharply (never below the minimum that still looks deliberate)
    box = int(ph.get('height', min(PHOTO_BOX[fmt], int(ih * MAX_UPSCALE))))
    box = max(box, PHOTO_MIN[fmt])
    scale = max(W / iw, box / ih)
    if scale > MAX_UPSCALE:
        probs.append(f'photo is too small for this layout ({iw}x{ih} would be enlarged {scale:.2f}x): pick a bigger one or drop it')
    fx, fy = ph.get('focus') or side.get('focus') or [50, 40]
    credit = ph.get('credit') or side.get('credit') or ''
    if not credit:
        probs.append('photo has no credit')
    html_ = (f'<div class="pho" style="height:{box}px"><div class="phi" style="background-image:url({f.as_uri()});'
             f'background-position:{fx}% {fy}%;transform-origin:{fx}% {fy}%"></div><div class="phg"></div></div>'
             f'<div class="phc" style="top:{pad_t + 66}px;right:{pad_r}px">PHOTO: {esc(credit).upper()}</div>')
    spacer = {'post': box - 395, 'story': box - 470, 'reel': 0}[fmt]
    return html_, (f'<div class="phs" style="height:{max(0, spacer)}px"></div>' if spacer > 0 else ''), probs


# ----------------------------------------------------------------- templates
# Each returns (body_html, options). Options: align ('start'|'end'|'center'), hl (headline px), centered (bool)

def t_result(c, th, acc):
    ours = c.get('ours')

    def side(s, key, default_label):
        hi = ours == key
        return (f'<div class="sc{" hi" if hi else ""}"><div class="scn">{crest(s.get("crest"), 64)}<span class="nm nw">{esc(s["name"])}</span></div>'
                f'<div class="num{" ac" if hi else ""}">{esc(s["score"])}</div>'
                f'<div class="lbl">{esc(s.get("label", default_label)).upper()}</div></div>')
    b = f'<div class="score">{side(c["home"], "home", "HOME")}{side(c["away"], "away", "AWAY")}</div>'
    if c.get('status'):
        b += f'<div class="status">{eyebrow(c["status"])}</div>'
    p = c.get('periods')
    if p:
        cols = len(p['labels'])
        grid = f'grid-template-columns: 1.6fr repeat({cols}, 1fr)'
        hdr = f'<div class="pr ph" style="{grid}"><span>{esc(p.get("title", "BY PERIOD")).upper()}</span>' + ''.join(f'<span class="pc">{esc(x).upper()}</span>' for x in p['labels']) + '</div>'
        rows = ''
        for side_key, other in (('home', 'away'), ('away', 'home')):
            vals = p[side_key]
            cells = ''
            for i, v in enumerate(vals):
                win = ours == side_key and str(v).isdigit() and str(p[other][i]).isdigit() and int(v) > int(p[other][i])
                cells += f'<span class="pc pv{" ac" if win else ""}">{esc(v)}</span>'
            rows += f'<div class="pr" style="{grid}"><span class="pn nw">{esc(c[side_key]["name"])}</span>{cells}</div>'
        b += f'<div class="periods">{hdr}{rows}</div>'
    if c.get('highlight'):
        h = c['highlight']
        b += f'<div class="hb"><span class="hbn ac">{esc(h["big"])}</span><span class="hbt">{rich(h["text"])}</span></div>'
    return b, {}


def t_roundup(c, th, acc):
    rows = ''
    for r in c['rows']:
        ours = r.get('ours')
        hn = f'<span class="rt rh nw{" fgs" if ours == "home" else ""}">{esc(r["home"])}</span>'
        an = f'<span class="rt ra nw{" fgs" if ours == "away" else ""}">{esc(r["away"])}</span>'
        hc, ac_ = crest(r.get('home_crest'), 56), crest(r.get('away_crest'), 56)
        score = f'<span class="rs">{esc(r["home_score"])}<i>–</i>{esc(r["away_score"])}</span>'
        note = f'<div class="rn">{rich(r["note"])}</div>' if r.get('note') else ''
        rows += f'<div class="rr"><div class="rg"><span class="rside rL">{hn}{hc}</span>{score}<span class="rside">{ac_}{an}</span></div>{note}</div>'
    if c.get('status'):
        rows = f'<div class="status" style="margin:0 0 18px">{eyebrow(c["status"])}</div>' + rows
    return f'<div class="round">{rows}</div>', {}


def t_news(c, th, acc):
    b = ''
    if c.get('entity'):
        e = c['entity']
        b += (f'<div class="ent">{crest(e.get("crest"), 96)}<div><div class="entt nw">{esc(e["title"])}</div>'
              f'<div class="ents">{rich(e.get("sub", ""))}</div></div></div>')
    if c.get('rows'):
        b += kv_rows(c['rows'])
    if c.get('tiles'):
        b += tiles(c['tiles'], small=True)
    return b, {'align': c.get('align', 'end')}


def t_fixtures(c, th, acc):
    out = ''
    for g in c['groups']:
        items = ''
        for it in g['items']:
            text = it.get('text') or f'{it["home"]} v {it["away"]}'
            note = f'<div class="fxn">{rich(it["note"])}</div>' if it.get('note') else ''
            items += f'<div class="fxi"><div class="fxl"><span class="fxt nw">{esc(text)}</span>{note}</div><span class="fxm">{esc(it.get("time", ""))}</span></div>'
        out += f'<div class="fxg"><div class="fxd">{esc(g["label"]).upper()}</div>{items}</div>'
    return f'<div class="fx">{out}</div>', {'align': c.get('align', 'end')}


def badge(bd, th_name, acc):
    tone = bd.get('tone', 'accent')
    col = acc if tone == 'accent' else TONES.get(tone, {}).get(th_name, '#7E838F')
    return (f'<div class="badge" style="border-color:{col};background:color-mix(in srgb,{col} 14%,transparent)">'
            f'<span class="bt" style="color:{col}">{esc(bd.get("top", "")).upper()}</span><span class="bm">{esc(bd.get("main", ""))}</span></div>')


def t_spotlight(c, th, acc):
    th_name = c['_theme']
    ppl = ''
    for p in c['people']:
        bd = badge(p['badge'], th_name, acc) if p.get('badge') else ''
        ppl += (f'<div class="sp">{bd}<div class="spx"><div class="spn nw">{esc(p["name"])}</div>'
                f'<div class="spm">{esc(p.get("meta", "")).upper()}</div><div class="spt">{rich(p.get("text", ""))}</div></div></div>')
    b = f'<div class="spl">{ppl}</div>'
    if c.get('tally'):
        t = c['tally']
        cells = ''.join(
            f'<div class="tc"><span class="tv" style="color:{acc if i.get("tone") == "accent" else TONES.get(i.get("tone"), {}).get(th_name, "inherit")}">{esc(i["value"])}</span><span class="tl">{esc(i["label"]).upper()}</span></div>'
            for i in t['items'])
        b += f'<div class="tally" style="grid-template-columns:1.4fr repeat({len(t["items"])},1fr)"><div class="tc tlab">{rich(t.get("label", ""))}</div>{cells}</div>'
    return b, {}


def tiles(items, small=False):
    n = len(items)
    cols = 2 if n in (2, 4) else (3 if n == 3 else 2)
    cells = ''
    for t in items:
        unit = f'<span class="tu">{esc(t["unit"])}</span>' if t.get('unit') else ''
        sub = f'<div class="tsub">{rich(t["sub"])}</div>' if t.get('sub') else ''
        cells += f'<div class="ti"><div class="tval">{esc(t["value"])}{unit}</div><div><div class="tlab2">{rich(t["label"])}</div>{sub}</div></div>'
    return f'<div class="tiles{" sm" if small else ""}" style="grid-template-columns:repeat({cols},1fr)">{cells}</div>'


def t_stats(c, th, acc):
    return tiles(c['tiles']), {}


def t_standings(c, th, acc):
    cols = c['columns']
    grid = f'grid-template-columns: 64px {"110px " if any(r.get("code") for r in c["rows"]) else ""}1fr repeat({len(cols)}, 130px)'
    has_code = any(r.get('code') for r in c['rows'])
    hdr = f'<div class="str sth" style="{grid}"><span></span>{"<span></span>" if has_code else ""}<span>{esc(c.get("team_label", "TEAM"))}</span>' + ''.join(f'<span class="stv">{esc(x).upper()}</span>' for x in cols) + '</div>'
    rows = ''
    cut = (c.get('cutline') or {}).get('after')
    for i, r in enumerate(c['rows'], 1):
        hi = r.get('highlight')
        code = f'<span class="code">{esc(r["code"])}</span>' if has_code else ''
        vals = ''.join(f'<span class="stv{" ac" if hi and j == len(r["values"]) - 1 else ""}">{esc(v)}</span>' for j, v in enumerate(r['values']))
        rows += f'<div class="str{" hi" if hi else ""}" style="{grid}"><span class="pos{" ac" if hi else ""}">{esc(r.get("pos", i))}</span>{code}<span class="stt nw">{esc(r["team"])}</span>{vals}</div>'
        if cut and i == cut:
            rows += f'<div class="cut"><span>{esc(c["cutline"].get("label", "")).upper()}</span><i></i></div>'
    b = f'<div class="st">{hdr}{rows}</div>'
    if c.get('next'):
        n = c['next']
        b += (f'<div class="nxt"><div><div class="nxtt">{esc(n["title"])}</div><div class="nxts">{rich(n.get("sub", ""))}</div></div>'
              f'<div class="nxr"><div class="nxb">{esc(n.get("big", ""))}</div><div class="nxbs">{esc(n.get("bigsub", "")).upper()}</div></div></div>')
    return b, {}


def t_preview(c, th, acc):
    big = f'<div class="bignum">{esc(c["big"])}</div>' if c.get('big') else ''
    return big, {'pre_headline': True, 'align': 'end', 'rows_after': c.get('rows')}


def t_quote(c, th, acc):
    q = (f'<div class="qm ac">“</div><div class="qt">{rich(c["quote"])}</div>'
         f'<div class="qs"><div class="qn">{esc(c["speaker"])}</div><div class="qr">{esc(c.get("role", "")).upper()}</div></div>')
    if c.get('translated_from'):
        q += f'<div class="qtr">TRANSLATED FROM {esc(c["translated_from"]).upper()}</div>'
    return f'<div class="quote">{q}</div>', {'no_headline': True, 'align': 'center'}


def t_correction(c, th, acc):
    return '', {'correction': True}


def t_end(c, th, acc):
    return '', {'end': True}


TEMPLATES = dict(end=t_end, result=t_result, roundup=t_roundup, news=t_news, fixtures=t_fixtures, spotlight=t_spotlight,
                 stats=t_stats, standings=t_standings, preview=t_preview, quote=t_quote, correction=t_correction)


# ----------------------------------------------------------------- page

def css(W, H, fmt, th, acc, glow):
    pad_t, pad_b = (60, 62) if fmt == 'post' else (170, 190) if fmt == 'story' else (200, 330)
    pad_r = 150 if fmt == 'reel' else 72  # keep clear of the Reel's like/comment/share buttons
    return f"""{FONTS_CSS}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{th['bg']};color:{th['fg']};font-family:Manrope,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
.cv{{position:relative;width:{W}px;height:{H}px;padding:{pad_t}px {pad_r}px {pad_b}px 72px;display:flex;flex-direction:column}}
.glow{{position:absolute;inset:0;pointer-events:none;background:{glow}}}
.ac{{color:{acc}}}
.nw{{white-space:nowrap;overflow:hidden;display:block}}
.hd{{display:flex;align-items:center;justify-content:space-between;min-height:48px;position:relative}}
.brand{{display:flex;align-items:center;gap:18px;font:500 25px Manrope;letter-spacing:.17em;color:{th['muted']}}}
.brand img{{width:46px;height:46px;margin-left:-6px}}
.sec{{font:600 21px 'JetBrains Mono';letter-spacing:.2em;color:{th['faint']}}}
.eb{{font:700 23px/1.35 'JetBrains Mono';letter-spacing:.2em;color:{acc};margin-top:46px;position:relative}}
.eb.pill{{align-self:flex-start;background:{acc};color:#16171B;padding:13px 26px;border-radius:999px}}
.eb.pillo{{align-self:flex-start;border:2px solid color-mix(in srgb,{acc} 60%,transparent);padding:12px 24px;border-radius:999px}}
.hl{{font-family:Rubik;font-weight:800;letter-spacing:-.03em;line-height:.92;margin-top:20px;position:relative;overflow-wrap:break-word}}
.dk{{font:400 31px/1.42 Manrope;color:{th['muted']};margin-top:22px;position:relative;letter-spacing:-.005em}}
.bd{{flex:1;min-height:0;display:flex;flex-direction:column;gap:26px;margin-top:40px;position:relative}}
.bd.end{{justify-content:flex-end}}
.bd>*{{flex-shrink:0}}
.bd.mid{{justify-content:center}}
.ft{{display:flex;align-items:flex-end;justify-content:space-between;gap:28px;margin-top:30px;position:relative}}
.ft.rule{{border-top:1px solid {th['line']};padding-top:30px}}
.kick{{font:800 31px/1.22 Manrope;letter-spacing:-.01em;max-width:720px}}
.fnote{{font:500 26px/1.4 Manrope;color:{th['muted']};max-width:720px}}
.hn{{font:500 22px 'JetBrains Mono';letter-spacing:.14em;color:{th['faint']};white-space:nowrap;margin-left:auto}}
.crest{{display:inline-flex;align-items:center;justify-content:center;flex:none}}
.crest.tile{{background:{th['tile']};border-radius:18px}}
.panel{{background:{th['panel']};border:1px solid {th['line']};border-radius:24px}}
/* result */
.score{{display:grid;grid-template-columns:1fr 1fr;border:1px solid {th['line']};border-radius:26px;overflow:hidden}}
.sc{{padding:28px 36px 26px;background:{th['panel']};min-width:0}}
.sc+.sc{{border-left:1px solid {th['line']}}}
.sc.hi{{background:color-mix(in srgb,{acc} 15%,{th['bg']})}}
.scn{{display:flex;align-items:center;gap:16px;min-width:0}}
.nm{{font:800 44px Rubik;letter-spacing:-.01em;min-width:0}}
.num{{font:700 112px/1 'JetBrains Mono';margin-top:16px;letter-spacing:-.02em}}
.lbl{{font:600 21px Manrope;letter-spacing:.17em;color:{th['faint']};margin-top:12px}}
.status{{font:700 21px 'JetBrains Mono';letter-spacing:.2em;color:{th['faint']};margin-top:-6px}}
.periods{{border:1px solid {th['line']};border-radius:24px;overflow:hidden;background:{th['panel']}}}
.pr{{display:grid;align-items:center;padding:0 32px;height:82px}}
.pr+.pr{{border-top:1px solid {th['line']}}}
.ph{{height:60px;font:600 21px Manrope;letter-spacing:.17em;color:{th['faint']};background:{th['panel2']}}}
.pn{{font:800 34px Rubik}}
.pc{{text-align:center}}
.pv{{font:500 40px 'JetBrains Mono'}}
.hb{{display:flex;align-items:center;gap:30px;padding:28px 34px;border:1px solid {th['line']};border-radius:24px;background:{th['panel']}}}
.hbn{{font:700 66px/1 'JetBrains Mono';white-space:nowrap}}
.hbt{{font:400 29px/1.35 Manrope;color:{th['muted']}}}
/* roundup */
.round{{display:flex;flex-direction:column}}
.rr{{padding:24px 0;border-top:1px solid {th['line']}}}
.rr:last-child{{border-bottom:1px solid {th['line']}}}
.rg{{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:26px}}
.rside{{display:flex;align-items:center;gap:16px;min-width:0}}
.rL{{justify-content:flex-end}}
.rt{{font:800 38px Rubik;letter-spacing:-.01em;min-width:0;color:{th['fg']}}}
.rh{{text-align:right}}
.rs{{font:700 52px 'JetBrains Mono';white-space:nowrap;min-width:150px;text-align:center}}
.rs i{{font-style:normal;color:{th['faint']};margin:0 10px}}
.rn{{font:400 25px/1.35 Manrope;color:{th['muted']};text-align:center;margin-top:10px}}
/* news */
.ent{{display:flex;align-items:center;gap:28px;padding:26px 30px;border:1px solid {th['line']};border-radius:24px;background:{th['panel']}}}
.entt{{font:800 46px Rubik;letter-spacing:-.01em}}
.ents{{font:500 26px/1.35 Manrope;color:{th['muted']};margin-top:6px}}
.kv{{border-top:1px solid {th['line']}}}
.kvr{{display:flex;align-items:center;justify-content:space-between;gap:30px;padding:24px 4px;border-bottom:1px solid {th['line']}}}
.k{{font:600 22px 'JetBrains Mono';letter-spacing:.18em;color:{th['faint']};white-space:nowrap}}
.v{{font:800 34px Rubik;letter-spacing:-.005em;text-align:right;min-width:0}}
/* fixtures */
.fx{{border-top:1px solid {th['line']}}}
.fxg{{padding:26px 0 22px;border-bottom:1px solid {th['line']}}}
.fxd{{font:700 22px 'JetBrains Mono';letter-spacing:.2em;color:{acc};margin-bottom:12px}}
.fxi{{display:flex;align-items:baseline;justify-content:space-between;gap:24px;padding:7px 0}}
.fxl{{min-width:0}}
.fxt{{font:800 36px/1.2 Rubik;letter-spacing:-.01em}}
.fxn{{font:400 23px Manrope;color:{th['muted']};margin-top:2px}}
.fxm{{font:500 31px 'JetBrains Mono';color:{th['faint']};white-space:nowrap}}
/* spotlight */
.spl{{border-top:1px solid {th['line']}}}
.sp{{display:flex;gap:36px;align-items:flex-start;padding:34px 0;border-bottom:1px solid {th['line']}}}
.badge{{width:132px;height:132px;border-radius:50%;border:5px solid;flex:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px}}
.bt{{font:600 20px Manrope;letter-spacing:.14em}}
.bm{{font:700 34px 'JetBrains Mono'}}
.spx{{min-width:0;flex:1}}
.spn{{font:800 50px Rubik;letter-spacing:-.015em}}
.spm{{font:600 22px 'JetBrains Mono';letter-spacing:.2em;color:{th['faint']};margin-top:10px}}
.spt{{font:400 29px/1.35 Manrope;color:{th['muted']};margin-top:14px}}
.tally{{display:grid;border:1px solid {th['line']};border-radius:24px;overflow:hidden;background:{th['panel']}}}
.tc{{padding:28px 20px;display:flex;flex-direction:column;align-items:center;gap:10px}}
.tc+.tc{{border-left:1px solid {th['line']}}}
.tlab{{align-items:flex-start;justify-content:center;font:500 26px/1.25 Manrope;color:{th['muted']};padding-left:30px}}
.tv{{font:700 54px/1 'JetBrains Mono'}}
.tl{{font:600 20px Manrope;letter-spacing:.17em;color:{th['faint']}}}
/* stats tiles */
.tiles{{display:grid;gap:22px}}
.ti{{background:{th['panel']};border:1px solid {th['line']};border-radius:28px;padding:40px 40px 34px;display:flex;flex-direction:column;justify-content:space-between;gap:40px;min-height:300px}}
.tiles.sm .ti{{min-height:0;padding:28px 30px;gap:16px}}
.tval{{font:800 150px/.9 Rubik;letter-spacing:-.04em;white-space:nowrap}}
.tiles.sm .tval{{font-size:72px}}
.tu{{font-size:.38em;letter-spacing:-.01em;margin-left:6px}}
.tlab2{{font:600 32px/1.2 Manrope}}
.tsub{{font:400 24px/1.35 Manrope;color:{th['muted']};margin-top:4px}}
/* standings */
.st{{display:flex;flex-direction:column}}
.str{{display:grid;align-items:center;height:80px;padding:0 24px;border-radius:18px}}
.sth{{height:50px;font:600 21px Manrope;letter-spacing:.16em;color:{th['faint']}}}
.str.hi{{background:{th['invbg']};color:{th['invfg']}}}
.pos{{font:600 32px Manrope;color:{th['faint']}}}
.code{{font:600 21px 'JetBrains Mono';letter-spacing:.06em;border:2px solid {th['line']};border-radius:10px;padding:6px 10px;justify-self:start}}
.str.hi .code{{border-color:color-mix(in srgb,{th['invfg']} 35%,transparent)}}
.stt{{font:800 36px Rubik;letter-spacing:-.01em;min-width:0;padding-right:16px}}
.stv{{font:500 36px 'JetBrains Mono';text-align:center}}
.sth .stv{{font:600 21px Manrope;letter-spacing:.16em}}
.cut{{display:flex;align-items:center;gap:20px;font:600 19px Manrope;letter-spacing:.17em;color:{th['faint']};margin:10px 0 10px 4px}}
.cut i{{flex:1;border-top:2px dashed {th['line']}}}
.nxt{{display:flex;justify-content:space-between;align-items:center;gap:24px;background:{th['invbg']};color:{th['invfg']};border-radius:26px;padding:32px 36px}}
.nxtt{{font:800 36px Rubik}}
.nxts{{font:400 26px Manrope;opacity:.65;margin-top:6px}}
.nxr{{text-align:right}}
.nxb{{font:700 52px 'JetBrains Mono';color:{acc}}}
.nxbs{{font:600 19px Manrope;letter-spacing:.16em;opacity:.7;margin-top:6px}}
/* preview */
.bignum{{font:800 300px/0.85 Rubik;color:transparent;-webkit-text-stroke:5px {th['fg']};letter-spacing:-.04em;margin-top:44px;position:relative}}
/* quote */
.quote{{display:flex;flex-direction:column;gap:26px}}
.qm{{font:800 240px/1 Manrope;height:120px;margin-top:-30px}}
.qt{{font:700 56px/1.2 Manrope;letter-spacing:-.02em}}
.qs{{margin-top:14px}}
.qn{{font:800 40px Rubik}}
.qr{{font:600 21px 'JetBrains Mono';letter-spacing:.18em;color:{th['faint']};margin-top:10px}}
.qtr{{font:500 19px 'JetBrains Mono';letter-spacing:.16em;color:{th['faint']}}}
/* correction */
.cv.center{{align-items:center;text-align:center}}
.corr-hl{{margin-top:56px}}
.corr-hl s{{color:{th['faint']};text-decoration:none;position:relative;display:inline-block}}
.corr-hl s::after{{content:'';position:absolute;left:-4%;right:-4%;top:52%;height:9px;border-radius:5px;background:{acc};transform:rotate(-2deg)}}
.center .kv{{width:640px}}
/* photo hero */
.pho{{position:absolute;left:0;top:0;width:100%;overflow:hidden;background:#000}}
.phi{{position:absolute;inset:0;background-size:cover;background-repeat:no-repeat;will-change:transform}}
.phg{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(22,23,27,.78) 0%,rgba(22,23,27,.25) 20%,rgba(22,23,27,0) 34%,rgba(22,23,27,.5) 55%,rgba(22,23,27,.9) 78%,#16171B 96%)}}
.phc{{position:absolute;font:600 17px 'JetBrains Mono';letter-spacing:.16em;color:rgba(250,250,248,.78);text-shadow:0 1px 8px rgba(0,0,0,.65)}}
.phs{{flex:none}}
.cv.photo .hd .brand{{color:rgba(250,250,248,.92);text-shadow:0 1px 8px rgba(0,0,0,.5)}}
.cv.photo .hl,.cv.photo .eb{{text-shadow:0 2px 18px rgba(0,0,0,.35)}}
.cv.reel.photo{{justify-content:flex-end}}
/* reels: header pinned top, content centred in the safe area and a touch larger */
.cv.reel{{justify-content:center}}
.cv.reel .hd{{position:absolute;top:{pad_t}px;left:72px;right:{pad_r}px}}
.cv.reel .bd{{flex:0 0 auto}}
.cv.reel .ft{{position:absolute;left:72px;right:{pad_r}px;bottom:{pad_b - 90}px}}
.cv.reel > .eb, .cv.reel > .hl, .cv.reel > .dk, .cv.reel > .bd, .cv.reel > .bignum{{zoom:1.12}}
"""


FIT_JS = r"""
() => {
  const W = document.body.clientWidth, H = document.body.clientHeight;
  const problems = [];
  const cv = document.querySelector('.cv'), bd = document.querySelector('.bd'), hl = document.querySelector('.hl');
  const over = () => cv.scrollHeight > H + 1 || (bd && bd.scrollHeight > bd.clientHeight + 1);
  // single-line items: shrink until they fit (down to 70%)
  document.querySelectorAll('.nw').forEach(el => {
    let fs = parseFloat(getComputedStyle(el).fontSize), min = fs * 0.7;
    while (el.scrollWidth > el.clientWidth + 1 && fs > min) { fs -= 1; el.style.fontSize = fs + 'px'; }
    if (el.scrollWidth > el.clientWidth + 1) problems.push('text too long for one line: "' + el.textContent.trim().slice(0, 60) + '"');
  });
  if (hl) {
    let fs = parseFloat(hl.dataset.size), min = parseFloat(hl.dataset.min), maxLines = parseInt(hl.dataset.lines);
    hl.style.fontSize = fs + 'px';
    const lines = () => Math.round(hl.getBoundingClientRect().height / (fs * 0.92));
    const wordTooWide = () => hl.scrollWidth > hl.clientWidth + 1;
    while ((over() || lines() > maxLines || wordTooWide()) && fs > min) { fs -= 2; hl.style.fontSize = fs + 'px'; }
    if (lines() > maxLines) problems.push('headline needs ' + lines() + ' lines at minimum size: shorten it');
    if (wordTooWide()) problems.push('a headline word is wider than the card');
    hl.dataset.final = fs;
  }
  if (over()) problems.push('content does not fit the card: cut rows or shorten the deck');
  document.querySelectorAll('.dk,.spt,.rn,.hbt,.fnote,.kick').forEach(el => {
    if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden') problems.push('clipped text: ' + el.textContent.slice(0, 50));
  });
  return {problems, headline_px: hl ? parseFloat(hl.dataset.final) : null};
}
"""


LAST_PROBLEMS: list[str] = []  # problems found while building the last slide (e.g. photo too small)


def build(slide: dict, spec: dict, idx: int, total: int) -> tuple[str, int, int]:
    page = PAGES[spec['page']]
    fmt = spec.get('format', 'post')
    W, H = SIZES[fmt]
    th_name = slide.get('theme', spec.get('theme', 'dark'))
    ph = (slide.get('card') or {}).get('photo')
    if ph:
        th_name = 'dark'  # photos always sit on ink
    th = THEMES[th_name]
    acc = page['accent'][th_name]
    glow = page['glow'] if th_name == 'dark' else 'none'
    tpl = slide['template']
    c = dict(slide.get('card', {}))
    c['_theme'] = th_name
    body, opt = TEMPLATES[tpl](c, th, acc)

    mark = (ROOT / 'brand/logos' / f'mark-{spec["page"]}-on-{th_name}.svg').as_uri()
    right = c.get('section', '')
    if total > 1 and fmt != 'reel':
        right = f'{idx:02d} / {total:02d}'
    hd = f'<div class="hd"><div class="brand"><img src="{mark}">{page["name"]}</div><div class="sec">{esc(right).upper()}</div></div>'

    eb = ''
    if c.get('eyebrow'):
        cls = {'pill': ' pill', 'outline': ' pillo'}.get(c.get('eyebrow_style', 'pill' if ph else ''), '')  # solid pill stays legible on any photo
        eb = f'<div class="eb{cls}">{eyebrow(c["eyebrow"])}</div>'

    base = {'post': 104, 'story': 116, 'reel': 120}[fmt]
    hsize = c.get('headline_size', opt.get('hl', base))
    lines = c.get('headline_lines', 4 if fmt == 'post' else 5)
    hl = ''
    if opt.get('correction'):
        hl = (f'<div class="hl corr-hl" data-size="{hsize}" data-min="64" data-lines="6">{rich(c.get("before", ""), True)}<br>'
              f'<s>{esc(str(c["wrong"]).lower())}</s><br>{headline(c["right"])}</div>')
    elif not opt.get('no_headline') and c.get('headline'):
        hl = f'<div class="hl" data-size="{hsize}" data-min="60" data-lines="{lines}">{headline(c["headline"])}</div>'
    dk = f'<div class="dk">{rich(c["deck"])}</div>' if c.get('deck') else ''

    if opt.get('end'):  # closing frame of a Reel or carousel: lockup, one line, follow prompt
        lock = (ROOT / 'brand/logos' / f'lockup-horizontal-{spec["page"]}-{th_name}.svg').as_uri()
        top = ''
        main = (f'<div class="bd mid" style="align-items:flex-start;gap:44px"><img src="{lock}" style="width:640px;max-width:100%">'
                f'<div class="hl" data-size="{c.get("headline_size", 96)}" data-min="60" data-lines="4">{headline(c.get("headline", "follow for every result."))}</div>'
                + (f'<div class="dk">{rich(c["deck"])}</div>' if c.get('deck') else '') + '</div>')
    elif opt.get('pre_headline'):  # preview: big number sits between eyebrow and headline
        top = eb + body + hl + dk
        rows = kv_rows(opt['rows_after']) if opt.get('rows_after') else ''
        main = f'<div class="bd end">{rows}</div>'
    elif opt.get('correction'):
        pill = f'<div class="eb pill" style="align-self:center;margin-top:{120 if fmt == "story" else 70}px">{esc(c.get("label", "QUICK CORRECTION")).upper()}</div>'
        top = pill + hl
        rows = kv_rows(c['rows']) if c.get('rows') else ''
        txt = f'<div class="dk" style="max-width:820px">{rich(c.get("text", ""))}</div>' if c.get('text') else ''
        main = f'<div class="bd" style="align-items:center;justify-content:center">{rows}{txt}</div>'
    else:
        top = eb + hl + dk
        align = opt.get('align', c.get('align', 'start'))
        cls = {'end': ' end', 'center': ' mid'}.get(align, '')
        main = f'<div class="bd{cls}">{body}</div>'

    left = ''
    if c.get('footer'):
        left = f'<div class="kick">{rich(c["footer"])}</div>'
    elif c.get('footnote'):
        left = f'<div class="fnote">{rich(c["footnote"])}</div>'
    ft = f'<div class="ft{" rule" if c.get("footer_rule") else ""}">{left}<div class="hn">{page["handle"]}</div></div>'

    center = ' center' if opt.get('correction') else ''
    if fmt == 'reel':
        center += ' reel'
    photo_html, spacer, photo_probs = '', '', []
    if ph:
        pad_t = (60 if fmt == 'post' else 170 if fmt == 'story' else 200)
        pad_r = 150 if fmt == 'reel' else 72
        photo_html, spacer, photo_probs = photo_parts(ph, fmt, W, pad_t, pad_r)
        if photo_html:
            center += ' photo'
            glow = 'none'
    LAST_PROBLEMS[:] = photo_probs
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{css(W, H, fmt, th, acc, glow)}</style></head>'
           f'<body><div class="cv{center}">{photo_html}<div class="glow"></div>{hd}{spacer}{top}{main}{ft}</div></body></html>')
    return doc, W, H


def out_path(spec: dict, idx: int, total: int) -> pathlib.Path:
    date = spec['date']
    kind = {'post': 'posts', 'story': 'stories', 'reel': 'reels'}[spec.get('format', 'post')]
    suffix = f'-{idx:02d}' if total > 1 else ''
    return ROOT / kind / spec['page'] / date[:7] / f'{date}-{spec["slug"]}{suffix}.png'



# ----------------------------------------------------------------- reels
# A Reel is a list of slides (any template above, plus 'end'), each shown for `dur` seconds.
# Every slide builds in: its blocks rise and fade in one after another, big numbers count up,
# then it cuts to the next. Typographic only: no footage, no third-party video.
# EVERY REEL HAS SOUND: an original soundtrack from tools/sound.py, with a whoosh and a hit on
# each slide change. Set "sound": {"mood": "drive" | "bright" | "calm"} in the spec (default drive).

ANIM_JS = r"""
() => {
  const rowSel = '.str,.kvr,.fxg,.rr,.sp,.ti,.ent,.score,.periods,.hb,.tally,.nxt,.quote';
  const els = [];
  const push = e => { if (e && !els.includes(e)) els.push(e); };
  ['.hd','.eb','.bignum','.hl','.dk'].forEach(s => document.querySelectorAll(s).forEach(push));
  const bd = document.querySelector('.bd');
  if (bd) [...bd.children].forEach(ch => {
    const rows = ch.matches(rowSel) ? [] : [...ch.querySelectorAll(rowSel)].filter(r => !r.parentElement.closest(rowSel) || r.parentElement === ch);
    if (rows.length) rows.forEach(push); else push(ch);
  });
  document.querySelectorAll('.ft').forEach(push);
  els.sort((a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1);
  els.forEach((e, i) => { e.dataset.at = (0.05 + i * 0.11).toFixed(2); e.style.willChange = 'opacity, transform'; });
  const counters = [...document.querySelectorAll('.num,.tval,.bignum')].filter(e => /^\d{1,4}$/.test(e.childNodes[0] && e.childNodes[0].nodeType === 3 ? e.childNodes[0].nodeValue.trim() : ''));
  counters.forEach(e => { e.dataset.target = e.childNodes[0].nodeValue.trim(); });
  const ease = x => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);
  window.__set = (t, dur) => {
    els.forEach(e => { const p = ease((t - parseFloat(e.dataset.at)) / 0.42); e.style.opacity = p; e.style.transform = `translateY(${(1 - p) * 46}px)`; });
    counters.forEach(e => { const host = e.closest('[data-at]'); const at = host ? parseFloat(host.dataset.at) : 0; const v = Math.round(parseInt(e.dataset.target) * ease((t - at) / 0.9)); e.childNodes[0].nodeValue = String(v); });
    const phi = document.querySelector('.phi');
    if (phi) phi.style.transform = `scale(${(1 + 0.08 * Math.min(1, t / dur)).toFixed(4)})`;  // slow push-in on photo slides
    const out = Math.max(0, Math.min(1, (dur - t) / 0.18));
    document.querySelector('.cv').style.opacity = out;
  };
  return {blocks: els.length, counters: counters.length};
}
"""


def render_reel(spec: dict, sp: str, browser) -> tuple[list[str], list[str]]:
    import shutil
    import subprocess
    import tempfile
    fps = 30
    slides = spec['slides']
    tmpdir = pathlib.Path(tempfile.mkdtemp(prefix='reel-'))
    problems: list[str] = []
    frame = 0
    cover_ms = None
    total_dur = sum(float(s.get('dur', 3)) for s in slides)
    if total_dur > 60:
        problems.append(f'Reel is {total_dur:.0f}s: keep news Reels under 20s and explainers under 45s')
    for i, slide in enumerate(slides, 1):
        dur = float(slide.get('dur', 3.0))
        doc, W, H = build(slide, spec, i, len(slides))
        pg = browser.new_page(viewport={'width': W, 'height': H})
        tmp = ROOT / 'build' / f'{spec["page"]}-{spec["slug"]}-reel-{i}.html'
        tmp.parent.mkdir(exist_ok=True)
        tmp.write_text(doc)
        pg.goto(tmp.as_uri())
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(250)
        res = pg.evaluate(FIT_JS)
        problems.extend(f'slide {i}: {pr}' for pr in list(LAST_PROBLEMS) + res['problems'])
        pg.evaluate(ANIM_JS)
        n = int(round(dur * fps))
        for k in range(n):
            t = k / fps
            pg.evaluate(f'window.__set({t}, {dur})')
            pg.screenshot(path=str(tmpdir / f'{frame:05d}.jpg'), type='jpeg', quality=92)
            if i == 1 and cover_ms is None and t >= min(dur - 0.3, 1.6):
                cover_ms = int(frame / fps * 1000)
                pg.screenshot(path=str(tmpdir / 'cover.png'))
            frame += 1
        pg.close()
    date = spec['date']
    out = ROOT / 'reels' / spec['page'] / date[:7] / f'{date}-{spec["slug"]}.mp4'
    cover = out.with_name(out.stem + '-cover.png')
    out.parent.mkdir(parents=True, exist_ok=True)
    # every Reel has sound (Geoffry, 21 Oct 2026): original soundtrack timed to the slide changes
    import runpy
    snd = runpy.run_path(str(ROOT / 'tools/sound.py'), run_name='sound')
    cuts, acc_t = [], 0.0
    for sl in slides[:-1]:
        acc_t += float(sl.get('dur', 3.0)); cuts.append(round(acc_t, 3))
    wav = tmpdir / 'sound.wav'
    sound_info = snd['make'](str(wav), frame / fps, cuts, spec['slug'], spec.get('sound', {}).get('mood', 'drive'))
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', str(tmpdir / '%05d.jpg'),
           '-i', str(wav), '-shortest',
           '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
           '-r', str(fps), '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-movflags', '+faststart', str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        problems.append('ffmpeg failed: ' + r.stderr[-300:])
    if (tmpdir / 'cover.png').exists():
        shutil.copy(tmpdir / 'cover.png', cover)
    # contact sheet of 6 frames for the visual check
    sheet = out.with_name(out.stem + '-frames.jpg')
    picks = sorted(tmpdir.glob('[0-9]*.jpg'))
    if picks:
        idxs = [int(j * (len(picks) - 1) / 5) for j in range(6)]
        from PIL import Image
        thumbs = [Image.open(picks[j]).convert('RGB').resize((270, 480)) for j in idxs]
        canvas = Image.new('RGB', (270 * 6 + 5 * 8, 480), '#888888')
        for j, im in enumerate(thumbs):
            canvas.paste(im, (j * 278, 0))
        sheet.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(build_dir := (ROOT / 'build' / sheet.name))
    shutil.rmtree(tmpdir, ignore_errors=True)
    vol = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(out), '-map', '0:a', '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re as _re
    mv = _re.search(r'mean_volume: (-?[\d.]+) dB', vol)
    mean_db = float(mv.group(1)) if mv else -99.0
    if mean_db < -30:
        problems.append(f'soundtrack is too quiet or missing (mean {mean_db} dB): every Reel needs sound')
    spec['reel_meta'] = {'seconds': round(frame / fps, 2), 'fps': fps, 'cover_ms': cover_ms or 0, 'sound': {**sound_info, 'mean_db': mean_db},
                         'cover': str(cover.relative_to(ROOT)), 'frames_sheet': f'build/{sheet.name}'}
    return [str(out.relative_to(ROOT)), str(cover.relative_to(ROOT))], problems

def render(spec_paths: list[str]) -> int:
    from playwright.sync_api import sync_playwright
    worst = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for sp in spec_paths:
            spec = json.loads(pathlib.Path(sp).read_text())
            if spec.get('format') == 'reel':
                outputs, problems = render_reel(spec, sp, b)
                worst = 2 if problems else worst
                print(('FAIL ' if problems else 'ok   ') + outputs[0] + f"  ({spec['reel_meta']['seconds']}s, cover at {spec['reel_meta']['cover_ms']} ms, frames: {spec['reel_meta']['frames_sheet']})")
                for pr in problems:
                    print(f'     - {pr}')
                spec['images'] = outputs
                spec['render'] = {'ok': not problems, 'problems': problems}
                spec.pop('visual_check', None)
                pathlib.Path(sp).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
                continue
            slides = spec.get('slides') or [{'template': spec['template'], 'card': spec['card'], **({'theme': spec['theme']} if 'theme' in spec else {})}]
            outputs, problems = [], []
            for i, slide in enumerate(slides, 1):
                doc, W, H = build(slide, spec, i, len(slides))
                pg = b.new_page(viewport={'width': W, 'height': H})
                tmp = ROOT / 'build' / f'{spec["page"]}-{spec["slug"]}-{i}.html'
                tmp.parent.mkdir(exist_ok=True)
                tmp.write_text(doc)
                pg.goto(tmp.as_uri())
                pg.evaluate('document.fonts.ready')
                pg.wait_for_timeout(250)
                res = pg.evaluate(FIT_JS)
                res['problems'] = list(LAST_PROBLEMS) + res['problems']
                out = out_path(spec, i, len(slides))
                out.parent.mkdir(parents=True, exist_ok=True)
                pg.screenshot(path=str(out))
                pg.close()
                rel = out.relative_to(ROOT)
                outputs.append(str(rel))
                problems.extend(res['problems'])
                if res['problems']:
                    worst = 2
                    print(f'FAIL {rel}')
                    for pr in res['problems']:
                        print(f'     - {pr}')
                else:
                    print(f'ok   {rel}  (headline {res["headline_px"]}px)')
            spec['images'] = outputs
            spec['render'] = {'ok': not problems, 'problems': problems}
            spec.pop('visual_check', None)  # a new render always needs a new look
            pathlib.Path(sp).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
        b.close()
    return worst


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(render(sys.argv[1:]))
