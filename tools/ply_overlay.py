#!/usr/bin/env python3
"""Render a transparent 1080x1920 text overlay PNG in Ply type (for ffmpeg overlay on clips).
Usage: python3 ply_overlay.py out.png "Headline with *one* accent | second line" ["small body line"] [--label "3D RENDER"] [--ar "سطر عربي"] [--pos top|middle] [--size 88] [--panel]
Fonts come from ply-media/tools/fonts (set PLY_FONTS if the repo is elsewhere). Text stays inside the Reels safe band
(180 px sides, 220 px top, 500 px bottom)."""
import argparse, html, os, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('headline'); ap.add_argument('body', nargs='?', default='')
ap.add_argument('--label', default=''); ap.add_argument('--ar', default=''); ap.add_argument('--pos', default='top'); ap.add_argument('--size', type=int, default=88, help='headline px, min 84')
ap.add_argument('--panel', action='store_true', help='soft bone panel behind text, for busy footage'); a = ap.parse_args()
FS = next((Path(d) for d in [os.environ.get('PLY_FONTS', ''), Path.cwd() / 'tools/fonts', '/home/claude/plymakes/ply-media/tools/fonts', '/home/claude/ply-media/tools/fonts', Path.home() / 'ply-media/tools/fonts'] if d and Path(d).is_dir()), None)
if not FS: raise SystemExit('Brand fonts not found: clone plymakes/ply-media or set PLY_FONTS=<repo>/tools/fonts')
face = lambda fam, path, w, st='normal': f"@font-face{{font-family:{fam};font-weight:{w};font-style:{st};src:url('{(FS / path).as_uri()}')}}"
css = ''.join([face('SG', f'space-grotesk/files/space-grotesk-latin-{w}-normal.woff2', w) for w in (400, 500)] +
              [face('FR', 'fraunces/files/fraunces-latin-500-normal.woff2', 500), face('FR', 'fraunces/files/fraunces-latin-500-italic.woff2', 500, 'italic'),
               face('AR', 'noto-naskh-arabic/files/noto-naskh-arabic-arabic-600-normal.woff2', 600)])
head = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html.escape(a.headline)).replace(' | ', '<br>')  # ' | ' forces a line break
top = {'top': 260, 'middle': 760}[a.pos]
panel = 'background:rgba(239,234,226,.92);padding:36px 40px;border-radius:28px;' if a.panel else 'text-shadow:0 2px 18px rgba(28,27,25,.35);'
ink = '#1C1B19' if a.panel else '#EFEAE2'
page = f"""<html><head><style>{css}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;background:transparent}}
.box{{position:absolute;left:180px;right:180px;top:{top}px;{panel}color:{ink}}}
.h{{font-family:FR,serif;font-weight:500;font-size:{a.size}px;line-height:1.02;letter-spacing:-.015em;text-wrap:balance}}
.h em{{font-style:italic;color:{'#B4532A' if a.panel else '#EFEAE2'}}}
.b{{font-family:SG,sans-serif;font-size:44px;line-height:1.3;margin-top:24px}}
.ar{{font-family:AR,serif;font-size:52px;line-height:1.5;margin-top:20px;direction:rtl;text-align:right}}
.lab{{position:absolute;left:180px;top:228px;font-family:SG,sans-serif;font-weight:500;font-size:26px;letter-spacing:.22em;
     color:#EFEAE2;background:rgba(28,27,25,.72);padding:8px 14px;border-radius:8px}}</style></head><body>
{f'<div class="lab">{html.escape(a.label)}</div>' if a.label else ''}
<div class="box" style="{'margin-top:70px' if a.label and a.pos == 'top' else ''}"><div class="h">{head}</div>
{f'<div class="b">{html.escape(a.body)}</div>' if a.body else ''}{f'<div class="ar" lang="ar">{html.escape(a.ar)}</div>' if a.ar else ''}</div></body></html>"""
tmp = Path(a.out).resolve().with_suffix('.overlay.html'); tmp.write_text(page)  # file:// page so file:// fonts load
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(tmp.as_uri())
    need = ['500 88px FR', 'italic 500 88px FR', '400 44px SG', '500 26px SG'] + (['600 52px AR'] if a.ar else [])
    missing = pg.evaluate("async n => { await Promise.all(n.map(f => document.fonts.load(f, f.includes('AR') ? 'عربي' : 'Ply'))); return n.filter(f => !document.fonts.check(f)); }", need)
    if missing: raise SystemExit(f'fonts not loaded: {missing} (check PLY_FONTS={FS})')
    pg.screenshot(path=a.out, omit_background=True); b.close()
tmp.unlink()
print(a.out)
