#!/usr/bin/env python3
"""Photos for the "From the Archive" history series.

    python3 tools/archive_photo.py info  "File:Camille Chamoun Sports City Stadium.jpg"
    python3 tools/archive_photo.py pick  "File:…jpg" --slug archive-2000-asian-cup --date 2026-10-29 --page lb \
        --shows "What the Commons description says the photo shows" [--focus 50,40]

Only Wikimedia Commons files under Public domain, CC0, CC BY or CC BY-SA are accepted (the licence
is read from Commons itself, never typed by hand). NC/ND, "fair use", GFDL-only and anything
from an agency is refused. The photo is saved to media/archive/<YYYY-MM>/<date>-<slug>.jpg with a
sidecar holding the author, licence, licence URL and the File: page, and the card and caption must
credit it as "<Author> / Wikimedia Commons, <Licence>".

For a club's or federation's own archive photo, use tools/photos.py scan/pick as for news photos,
then add "series": "archive" to its sidecar.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = 'SportsWireArchive/1.0 (https://github.com/plymakes/ply-media; history series photo licence check)'
OK_LICENCE = re.compile(r'^(public domain|pd\b.*|cc0( 1\.0)?|cc by(-sa)?( [0-9.]+)?)$', re.I)
BLOCKED = re.compile(r'getty|\bafp\b|reuters|associated press|\bap photo|\bepa\b|imago|shutterstock|alamy|sportsfile', re.I)
# Only robots-allowed pages are read: the File: description page (/wiki/) and the file itself on
# upload.wikimedia.org. The Commons API lives under /w/, which robots.txt disallows, so it isn't used.


def get(url: str) -> bytes:
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 3:
                wait = int(e.headers.get('Retry-After') or 20)
                if wait > 150:
                    raise
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f'unreachable: {url}')


def strip_html(s: str) -> str:
    s = re.sub(r'<style[^>]*>.*?</style>', ' ', s or '', flags=re.S)  # creator templates carry inline CSS
    s = re.sub(r'\.mw-parser-output[^}]*\}|@media[^{]*\{[^{}]*(\{[^{}]*\}[^{}]*)*\}', ' ', s)
    s = re.sub(r'\bQS:P\S+', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def info(title: str) -> dict:
    if title.startswith('http'):
        title = urllib.parse.unquote(title.rsplit('/wiki/', 1)[-1])
    if not title.startswith('File:'):
        title = 'File:' + title
    page_url = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_'), safe=':()_,.-')
    t = html.unescape(get(page_url).decode('utf-8', 'replace'))

    def span(cls):
        m = re.search(r'class="[^"]*\b' + cls + r'\b[^"]*"[^>]*>(.*?)</span>', t, re.S)
        return strip_html(m.group(1)) if m else ''

    def field(fid):
        m = re.search(r'id="fileinfotpl_' + fid + r'".*?</td>\s*<td[^>]*>(.*?)</td>', t, re.S)
        return strip_html(m.group(1)) if m else ''
    full = re.search(r'class="fullMedia".*?href="(https://upload\.wikimedia\.org/[^"?]+)', t, re.S)
    size = re.search(r'([\d,]+) × ([\d,]+) pixels', t)
    w, h = (int(size.group(1).replace(',', '')), int(size.group(2).replace(',', ''))) if size else (0, 0)
    orig = full.group(1) if full else ''
    img = orig
    # Wikimedia rate-limits originals and asks for standard thumbnail widths (w.wiki/GHai): take the largest one that fits.
    std = [s for s in (330, 500, 960, 1280, 1920) if s <= w]
    if orig and std and not orig.lower().endswith('.svg'):
        base = orig.split('/wikipedia/commons/', 1)[1]
        name = base.rsplit("/", 1)[-1]
        if name.lower().endswith(('.tif', '.tiff')):
            name += '.jpg'  # TIFF thumbnails are served as JPEG
        img = f'https://upload.wikimedia.org/wikipedia/commons/thumb/{base}/{std[-1]}px-{name}'
    nonfree = 'licensetpl_nonfree' in t and span('licensetpl_nonfree').lower() == 'true'
    return {
        'title': title, 'source_page': page_url, 'original_url': orig, 'image_url': img, 'width': w, 'height': h,
        'licence': span('licensetpl_short') or ('Public domain' if re.search(r'public domain', t, re.I) and 'licensetpl' not in t else ''),
        'licence_url': span('licensetpl_link'), 'attribution': span('licensetpl_attr'),
        'author': field('aut'), 'credit_meta': field('src'), 'description': field('desc')[:400], 'date': field('date'),
        'restrictions': 'non-free' if nonfree else '', 'mime': 'image/' + orig.rsplit('.', 1)[-1].lower() if orig else '',
    }


def problems(i: dict) -> list[str]:
    p = []
    if not OK_LICENCE.match(i['licence'].strip()):
        p.append(f'licence "{i["licence"]}" is not allowed (Public domain, CC0, CC BY, CC BY-SA only)')
    if not i['author'] and not i['licence'].lower().startswith(('public domain', 'pd')):
        p.append('no author on Commons: attribution impossible')
    if BLOCKED.search(' '.join([i['author'], i['credit_meta']])):
        p.append('agency/wire photo')
    if i['restrictions']:
        p.append(f'restrictions on Commons: {i["restrictions"]} (check before use)')
    if not i['mime'].startswith('image/'):
        p.append(f'not an image ({i["mime"]})')
    return p


def credit_of(i: dict) -> str:
    if i.get('attribution'):  # the attribution the author asked for, when Commons gives one
        return f"{i['attribution']} / Wikimedia Commons"
    author = i['author'] or 'Unknown author'
    u = re.match(r'https?://(?:www\.)?flickr\.com/(?:photos|people)/([^/\s]+)', author)  # Flickr profile URL -> username
    if u:
        author = u.group(1)
    m = re.search(r'User:([^\s)|\]]+)', author)  # "me ( w:User:Akademan )" -> "Akademan"
    if m:
        author = m.group(1).replace('_', ' ')
    author = re.sub(r'\s*\(talk\)|\s*Own work', '', author).strip(' ,;') or 'Unknown author'
    if len(author) > 60:
        author = author[:57].rsplit(' ', 1)[0] + '…'
    return f'{author} / Wikimedia Commons'


def pick(title, slug, date, page, shows, focus):
    i = info(title)
    pr = problems(i)
    if pr:
        sys.exit('REFUSED: ' + '; '.join(pr))
    out = ROOT / 'media/archive' / date[:7] / f'{date}-{slug}.jpg'
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = get(i['image_url'])
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    im.save(out, quality=92)
    credit = credit_of(i)
    side = {
        'series': 'archive', 'source_page': i['source_page'], 'image_url': i['image_url'], 'original_url': i['original_url'],
        'credit': credit, 'credit_line': f'{credit}, {i["licence"]}', 'author': i['author'], 'licence': i['licence'],
        'licence_url': i['licence_url'], 'commons_description': i['description'], 'commons_date': i['date'],
        'shows': shows, 'width': im.width, 'height': im.height,
        'focus': [int(v) for v in focus.split(',')] if focus else [50, 40], 'page': page,
        'licence_basis': f'Wikimedia Commons free licence ({i["licence"]}), attributed on the card and in the caption',
        'sha1': hashlib.sha1(out.read_bytes()).hexdigest(), 'picked': time.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    out.with_suffix('.json').write_text(json.dumps(side, ensure_ascii=False, indent=2) + '\n')
    print(out.relative_to(ROOT))
    print(f'credit on card: PHOTO: {side["credit_line"]}')
    print(f'caption line:   📸 {side["credit_line"]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['info', 'pick'])
    ap.add_argument('title')
    ap.add_argument('--slug'); ap.add_argument('--date'); ap.add_argument('--page')
    ap.add_argument('--shows'); ap.add_argument('--focus')
    a = ap.parse_args()
    if a.cmd == 'info':
        i = info(a.title)
        print(json.dumps(i, ensure_ascii=False, indent=2))
        pr = problems(i)
        print('OK to use' if not pr else 'REFUSED: ' + '; '.join(pr))
    else:
        for k in ('slug', 'date', 'page', 'shows'):
            if not getattr(a, k):
                sys.exit(f'--{k} is required')
        pick(a.title, a.slug, a.date, a.page, a.shows, a.focus)


if __name__ == '__main__':
    main()
