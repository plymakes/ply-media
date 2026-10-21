#!/usr/bin/env python3
"""Club and team crests for SportsWire cards: find, download, normalise, record.

    python3 tools/crests.py find "Sagesse SC basketball"            # Wikipedia candidates (title + logo file)
    python3 tools/crests.py add sagesse --wiki "Sagesse SC" --name "Sagesse SC"
    python3 tools/crests.py add riyadi --url https://www.riyadi.com/logo.png --source-page https://www.riyadi.com/ --name "Al Riyadi"
    python3 tools/crests.py seed                                     # the starter list below (skips ones we have)
    python3 tools/crests.py sheet [slug ...]                         # contact sheet in build/ for the visual check
    python3 tools/crests.py list

Every crest is a 512 px PNG in brand/crests/<slug>.png with its origin in brand/crests/index.json.
Prefer the club's own website; a club's Wikipedia infobox logo is the fallback (same crest, easier to
fetch). After adding crests, ALWAYS open the sheet and check each one is the right club and the current
crest; delete any that isn't (`python3 tools/crests.py rm <slug>`). Crests are used for editorial
identification only (PLAYBOOK, Images and rights).

Wikipedia rate-limits shared IPs hard: this tool batches requests, waits between them and honours
Retry-After. Never hammer it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRESTS = ROOT / 'brand/crests'
INDEX = CRESTS / 'index.json'
UA = 'SportsWireNewsroom/1.0 (+https://github.com/plymakes/ply-media; sports news cards)'
API = 'https://en.wikipedia.org/w/api.php'

# slug -> (display name, Wikipedia article). The weekly desk extends this as new clubs appear.
SEED = {
    # Lebanon, basketball
    'riyadi': ('Al Riyadi', 'Al Riyadi Club Beirut'),
    'sagesse': ('Sagesse SC', 'Sagesse SC'),
    'homenetmen-beirut': ('Homenetmen', 'Homenetmen Beirut B.C.'),
    'antranik': ('Antranik', 'Antranik SC'),
    'beirut-club': ('Beirut Club', 'Beirut Club (basketball)'),
    'champville': ('Champville', 'Champville SC'),
    'hoops-club': ('Hoops Club', 'Hoops Club'),
    'antonine': ('Antonine', 'Antonine Sports Club'),
    # Lebanon, football
    'al-ansar': ('Al Ansar FC', 'Al Ansar FC'),
    'nejmeh': ('Nejmeh SC', 'Nejmeh SC'),
    'al-ahed': ('Al Ahed FC', 'Al Ahed FC'),
    'safa': ('Safa SC', 'Safa SC'),
    'shabab-al-sahel': ('Shabab Al Sahel', 'Shabab Al Sahel FC'),
    'tadamon-sour': ('Tadamon Sour', 'Tadamon Sour SC'),
    # Lebanon, federations / national teams
    'lfa': ('Lebanon (LFA)', 'Lebanon national football team'),
    'flbb': ('Lebanon (FLBB)', 'Lebanon men\'s national basketball team'),
    # Cyprus, First Division 2026-27
    'ael': ('AEL Limassol', 'AEL Limassol'),
    'aek-larnaca': ('AEK Larnaca', 'AEK Larnaca FC'),
    'apollon': ('Apollon Limassol', 'Apollon Limassol FC'),
    'aris-limassol': ('Aris Limassol', 'Aris Limassol FC'),
    'apoel': ('APOEL', 'APOEL FC'),
    'omonia-29m': ('Omonia 29 M', 'ALS Omonia 29 M'),
    'omonia-aradippou': ('Omonia Aradippou', 'Omonia Aradippou'),
    'olympiakos-nicosia': ('Olympiakos Nicosia', 'Olympiakos Nicosia'),
    'nea-salamis': ('Nea Salamis', 'Nea Salamis Famagusta FC'),
    'krasava': ('Krasava', 'Krasava ENY Ypsonas FC'),
    'anorthosis': ('Anorthosis Famagusta', 'Anorthosis Famagusta FC'),
    'karmiotissa': ('Karmiotissa', 'Karmiotissa FC'),
    'cfa': ('Cyprus (CFA)', 'Cyprus national football team'),
    # Europe this autumn (opponents of Omonia and Pafos)
    'riga-fc': ('Riga FC', 'Riga FC'),
    'atalanta': ('Atalanta', 'Atalanta BC'),
    'twente': ('Twente', 'FC Twente'),
    'kairat': ('Kairat', 'FC Kairat'),
}


def load_index() -> dict:
    return json.loads(INDEX.read_text()) if INDEX.exists() else {}


def save_index(d: dict) -> None:
    INDEX.write_text(json.dumps(dict(sorted(d.items())), ensure_ascii=False, indent=2) + '\n')


def http(url: str, tries: int = 5) -> bytes:
    for i in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                wait = int(e.headers.get('Retry-After') or 10) + 2 + i * 5
                if wait > 150:  # a long block: skip this one now, a later run fills the gap
                    raise RuntimeError(f'{urllib.parse.urlparse(url).netloc} asks us to wait {wait}s; skipped for now') from e
                print(f'  rate-limited by {urllib.parse.urlparse(url).netloc}, waiting {wait}s', file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError('unreachable')


def wiki_query(**params) -> dict:
    params = {'action': 'query', 'format': 'json', 'formatversion': '2', 'redirects': '1', **params}
    return json.loads(http(API + '?' + urllib.parse.urlencode(params)))


def wiki_logo(titles: list[str]) -> dict:
    """title -> {title, page_url, image_url, file} using the infobox page image, in one batched call."""
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        d = wiki_query(titles='|'.join(chunk), prop='pageimages|info', piprop='thumbnail|name|original',
                       pithumbsize='1280', inprop='url')
        q = d['query']
        alias = {}
        for kind in ('normalized', 'redirects'):
            for n in q.get(kind, []):
                alias[n['to']] = alias.get(n['from'], n['from'])
        for p in q['pages']:
            src = alias.get(p['title'], p['title'])
            while src in alias:
                src = alias[src]
            img = ((p.get('original') or {}).get('source', '') or '').split('?')[0]
            if img.lower().endswith('.svg'):
                thumb = ((p.get('thumbnail') or {}).get('source', '') or '').split('?')[0]
                img = thumb or img  # Wikimedia's PNG render of the SVG; else we render it ourselves
            out[src] = {'title': p['title'], 'page_url': p.get('fullurl'), 'image_url': img or None,
                        'file': p.get('pageimage'), 'missing': p.get('missing', False)}
        time.sleep(2)
    return out


def infobox_logo(title: str) -> str | None:
    """First image in the article's infobox (club logos are usually non-free files, so not a 'page image')."""
    import re
    time.sleep(3)
    d = json.loads(http(API.replace('/w/api.php', '/w/api.php') + '?' + urllib.parse.urlencode(
        {'action': 'parse', 'format': 'json', 'formatversion': '2', 'page': title, 'prop': 'text', 'section': '0', 'redirects': '1'})))
    html_ = (d.get('parse') or {}).get('text', '')
    box = re.search(r'<table[^>]*class="[^"]*infobox.*?</table>', html_, re.S)
    if not box:
        return None
    src = None
    for tag in re.findall(r'<img[^>]+>', box.group(0)):  # skip kit pieces, flags and icons: the logo is a real-sized image
        s = re.search(r'src="(//upload\.wikimedia\.org/[^"]+)"', tag)
        w = re.search(r'width="(\d+)"', tag)
        if not s or (w and int(w.group(1)) < 80) or re.search(r'kit_|_kit|flag_of|icon|edit', s.group(1), re.I):
            continue
        src = 'https:' + s.group(1)
        break
    if not src:
        return None
    # thumb URL -> original file (non-free logos are stored small, so the original is the best we can get)
    o = re.match(r'(https://upload\.wikimedia\.org/wikipedia/[^/]+)/thumb/(.+?)/[^/]+$', src)
    if o and not o.group(2).lower().endswith('.svg'):
        return f'{o.group(1)}/{o.group(2)}'
    return src


def svg_to_png(data: bytes) -> bytes:
    from playwright.sync_api import sync_playwright
    tmp = ROOT / 'build' / 'crest-tmp.svg'
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_bytes(data)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1024, 'height': 1024})
        page = tmp.with_suffix('.html')
        page.write_text(f'<html><body style="margin:0;background:transparent"><img src="{tmp.name}" style="width:1024px;height:1024px;object-fit:contain"></body></html>')
        pg.goto(page.as_uri())  # a file:// page, so the local SVG is allowed to load
        pg.wait_for_timeout(400)
        png = pg.screenshot(omit_background=True)
        b.close()
    return png


def normalise(data: bytes, src_url: str) -> 'Image.Image':
    from PIL import Image
    if src_url.lower().split('?')[0].endswith('.svg') or data[:200].lstrip().startswith((b'<svg', b'<?xml')):
        data = svg_to_png(data)
    im = Image.open(io.BytesIO(data))
    im = im.convert('RGBA')
    # trim transparent (or flat white) border
    bbox = im.getchannel('A').getbbox()
    if bbox and bbox != (0, 0, *im.size):
        im = im.crop(bbox)
    else:
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        from PIL import ImageChops
        diff = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 12 else 0)
        bb = diff.getbbox()
        if bb:
            im = im.crop(bb)
    w, h = im.size
    side = max(w, h)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - w) // 2, (side - h) // 2))
    return sq.resize((512, 512), Image.LANCZOS), (w, h)


def add(slug: str, name: str, *, wiki: str | None = None, url: str | None = None, source_page: str | None = None,
        info: dict | None = None) -> bool:
    idx = load_index()
    if wiki and not info:
        info = wiki_logo([wiki]).get(wiki)
    if wiki and info and not info.get('missing') and not info.get('image_url'):
        img = infobox_logo(info.get('title') or wiki)  # non-free logos aren't page images; read the infobox
        if img:
            info = {**info, 'image_url': img}
    if wiki:
        if not info or info.get('missing') or not info.get('image_url'):
            print(f'  ✗ {slug}: no logo found on Wikipedia "{wiki}"')
            return False
        url, source_page = info['image_url'], info['page_url']
    if not url:
        print(f'  ✗ {slug}: nothing to download')
        return False
    data = http(url)
    im, orig = normalise(data, url)
    CRESTS.mkdir(parents=True, exist_ok=True)
    im.save(CRESTS / f'{slug}.png', optimize=True)
    idx[slug] = {'name': name, 'source_page': source_page, 'image_url': url, 'original_px': list(orig),
                 'via': 'wikipedia infobox' if wiki else 'official site', 'fetched': dt.date.today().isoformat(),
                 'checked': False, 'use': 'editorial identification only'}
    save_index(idx)
    print(f'  ✓ {slug}: {name}  ({orig[0]}x{orig[1]} from {urllib.parse.urlparse(url).netloc})')
    return True


def seed() -> None:
    have = {p.stem for p in CRESTS.glob('*.png')}
    todo = {k: v for k, v in SEED.items() if k not in have}
    if not todo:
        print('all seed crests present')
        return
    infos = wiki_logo([v[1] for v in todo.values()])
    for slug, (name, title) in todo.items():
        try:
            add(slug, name, wiki=title, info=infos.get(title))
        except Exception as e:  # one bad file shouldn't stop the rest
            print(f'  ✗ {slug}: {e}')
        time.sleep(1.5)


def sheet(slugs: list[str]) -> pathlib.Path:
    from PIL import Image, ImageDraw, ImageFont
    files = [CRESTS / f'{s}.png' for s in slugs] if slugs else sorted(CRESTS.glob('*.png'))
    files = [f for f in files if f.exists()]
    cols = 6
    cell = 220
    rows = (len(files) + cols - 1) // cols
    canvas = Image.new('RGB', (cols * cell, rows * (cell + 40)), '#F3F1EB')
    d = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype(str(ROOT / 'tools/fonts/files/manrope-latin-600-normal.woff2'), 18)
    except Exception:
        font = ImageFont.load_default()
    for i, f in enumerate(files):
        im = Image.open(f).convert('RGBA').resize((180, 180), Image.LANCZOS)
        x, y = (i % cols) * cell + 20, (i // cols) * (cell + 40) + 14
        tile = Image.new('RGBA', (180, 180), (255, 255, 255, 255))
        tile.alpha_composite(im)
        canvas.paste(tile.convert('RGB'), (x, y))
        d.text((x, y + 186), f.stem[:22], fill='#16171B', font=font)
    out = ROOT / 'build' / 'crests-sheet.png'
    out.parent.mkdir(exist_ok=True)
    canvas.save(out)
    print(out.relative_to(ROOT))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['find', 'add', 'seed', 'sheet', 'list', 'rm', 'ok'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--wiki')
    ap.add_argument('--url')
    ap.add_argument('--source-page')
    ap.add_argument('--name')
    a = ap.parse_args()
    if a.cmd == 'find':
        q = ' '.join(a.args)
        d = wiki_query(generator='search', gsrsearch=q, gsrlimit='5', prop='pageimages', piprop='name')
        for p in sorted(d['query'].get('pages', []), key=lambda p: p.get('index', 0)):
            print(f"{p['title']}  |  {p.get('pageimage', '(no image)')}")
    elif a.cmd == 'add':
        slug = a.args[0]
        ok = add(slug, a.name or slug, wiki=a.wiki, url=a.url, source_page=a.source_page)
        sys.exit(0 if ok else 1)
    elif a.cmd == 'seed':
        seed()
    elif a.cmd == 'sheet':
        sheet(a.args)
    elif a.cmd == 'list':
        idx = load_index()
        for f in sorted(CRESTS.glob('*.png')):
            e = idx.get(f.stem, {})
            print(f"{f.stem:22} {e.get('name', '?'):24} {'checked' if e.get('checked') else 'UNCHECKED'}  {e.get('source_page', '')}")
    elif a.cmd == 'rm':
        idx = load_index()
        for s in a.args:
            (CRESTS / f'{s}.png').unlink(missing_ok=True)
            idx.pop(s, None)
        save_index(idx)
    elif a.cmd == 'ok':  # mark crests as visually checked
        idx = load_index()
        for s in a.args:
            if s in idx:
                idx[s]['checked'] = dt.date.today().isoformat()
        save_index(idx)


if __name__ == '__main__':
    main()
