#!/usr/bin/env python3
"""Event photos for SportsWire cards, quiz/vote tiles and Reels (policy: PLAYBOOK, Images and rights).

    python3 tools/photos.py scan <page URL: club/federation report, outlet article, gallery, or a direct image URL> [--min 1080]
        Lists every image on the page (og:image, <img>, srcset, galleries) with its size,
        downloads the usable ones to build/photos/candidates/ and writes a numbered contact
        sheet (build/photos/candidates-sheet.jpg) to LOOK AT before choosing.
    python3 tools/photos.py pick <n> --slug <slug> --date YYYY-MM-DD --page lb|cy \
        --credit "Sagesse SC" --shows "Sagesse players celebrate the Arab Club Championship title, Ghazir, 20 Oct 2026" \
        [--focus 50,35]   (where the action is, in % from left and top; keeps faces in frame when cropped)
        Copies candidate n to media/photos/<YYYY-MM>/<date>-<slug>.jpg (max 2400 px, JPEG q90)
        and writes the sidecar <same>.json: source page, image URL, credit, what the source page
        says the photo shows, metadata credit/byline, size, licence basis.
    python3 tools/photos.py check <photo.jpg>
        Re-runs the checks (size, blocked agencies in URL and metadata, sidecar complete).

Any source is fine as long as it is credited (Geoffry, 23 Oct 2026: "post anything but credit the
source"): club, federation, league, athlete, organiser, news outlet, data service, Wikimedia Commons.
The credit is the source we took it from (and the photographer when the page names one). The source
page must say what the photo shows (event and people): the photo is part of the facts. One exception
stays: photos credited to agencies (Getty, AFP, Reuters, AP, EPA, Imago...) are refused, because they
send takedowns and repeated strikes can get the Instagram account disabled.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html.parser
import io
import json
import pathlib
import re
import shutil
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAND = ROOT / 'build/photos/candidates'
UA = 'Mozilla/5.0 (compatible; SportsWireNewsroom/1.0; +https://github.com/plymakes/ply-media)'
MIN_SHORT = 600   # short side; the renderer also refuses any photo it would have to enlarge more than 1.25x
MIN_LONG = 1000
BLOCKED = re.compile(r'getty|gettyimages|\bafp\b|afp\.com|reuters|\bap\b photo|apnews|ap images|associated press|\bepa\b|epa-efe|'
                     r'imago|shutterstock|alamy|sportsfile|dpa|anadolu|xinhua|sipa|pa images|panoramic|icon sport|'
                     r'action images|backpage|nurphoto|zuma|newscom|bildbyran|eurokinissi|intime', re.I)
BLOCKED_HOSTS = re.compile(r'gettyimages|getty|afp\.com|reuters|apnews|imago|shutterstock|alamy|sportsfile|epa\.eu|zumapress', re.I)


def http(url: str) -> bytes:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


class Imgs(html.parser.HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base, self.found = base, []

    def add(self, u, how):
        if not u or u.startswith('data:'):
            return
        u = urllib.parse.urljoin(self.base, html.unescape(u.strip()))
        full = re.sub(r'-\d{2,4}x\d{2,4}(\.(?:jpe?g|png|webp))', r'\1', u, flags=re.I)  # WordPress-style resized copy -> original
        for cand in ([full, u] if full != u else [u]):
            if cand not in [f[0] for f in self.found]:
                self.found.append((cand, how if cand == u else how + '+original'))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and (a.get('property') in ('og:image', 'og:image:url', 'og:image:secure_url') or a.get('name') in ('twitter:image',)):
            self.add(a.get('content'), 'og')
        if tag in ('img', 'source'):
            for k in ('srcset', 'data-srcset'):
                if a.get(k):
                    best = max((p.strip().split(' ') for p in a[k].split(',') if p.strip()),
                               key=lambda x: int(re.sub(r'\D', '', x[1]) or 0) if len(x) > 1 else 0)
                    self.add(best[0], 'srcset')
            for k in ('data-lazy-src', 'data-src', 'data-original', 'data-full', 'data-large_image', 'src'):
                if a.get(k):
                    self.add(a[k], tag)
        if tag == 'a' and re.search(r'\.(jpe?g|png|webp)(\?|$)', a.get('href', ''), re.I):
            self.add(a['href'], 'link')


def meta_credit(im) -> str:
    bits = []
    try:
        ex = im.getexif()
        for tag in (0x013B, 0x8298, 0x010E):  # Artist, Copyright, ImageDescription
            if ex.get(tag):
                bits.append(str(ex.get(tag)))
    except Exception:
        pass
    try:
        from PIL import IptcImagePlugin
        ip = IptcImagePlugin.getiptcinfo(im) or {}
        for key in ((2, 80), (2, 110), (2, 115), (2, 116), (2, 120)):
            v = ip.get(key)
            if v:
                bits.append((v[0] if isinstance(v, list) else v).decode('utf-8', 'ignore'))
    except Exception:
        pass
    xmp = im.info.get('xmp') or b''
    if isinstance(xmp, bytes):
        xmp = xmp.decode('utf-8', 'ignore')
    for m in re.findall(r'<(?:dc:creator|dc:rights|photoshop:Credit|photoshop:Source)[^>]*>(.*?)</', xmp, re.S):
        bits.append(re.sub(r'<[^>]+>', ' ', m))
    return ' | '.join(re.sub(r'\s+', ' ', b).strip() for b in bits if b.strip())[:400]


def scan(page: str, min_short: int) -> None:
    from PIL import Image, ImageDraw
    if BLOCKED_HOSTS.search(urllib.parse.urlparse(page).netloc):
        sys.exit(f'blocked source: {page}')
    p = Imgs(page)
    if re.search(r'\.(jpe?g|png|webp)(\?|$)', page, re.I):  # a direct image URL (e.g. an article's lead image when the page itself is JavaScript)
        p.found.append((page, 'direct'))
    else:
        raw = http(page).decode('utf-8', 'ignore')
        p.feed(raw)
    shutil.rmtree(CAND, ignore_errors=True)
    CAND.mkdir(parents=True)
    rows, thumbs = [], []
    for u, how in p.found[:60]:
        if re.search(r'logo|icon|sprite|avatar|emoji|placeholder|banner-ad|\.svg|\.gif', u, re.I):
            continue
        if BLOCKED_HOSTS.search(urllib.parse.urlparse(u).netloc):
            continue
        try:
            data = http(u)
            im = Image.open(io.BytesIO(data))
            im.load()
        except Exception:
            continue
        w, h = im.size
        if min(w, h) < 300:
            continue
        n = len(rows) + 1
        ext = {'JPEG': 'jpg', 'PNG': 'png', 'WEBP': 'webp'}.get(im.format, 'img')
        f = CAND / f'{n:02d}.{ext}'
        f.write_bytes(data)
        credit = meta_credit(im)
        flag = []
        if min(w, h) < min_short or max(w, h) < MIN_LONG:
            flag.append(f'too small (<{min_short}x{MIN_LONG})')
        if BLOCKED.search(credit or ''):
            flag.append('AGENCY in metadata')
        rows.append({'n': n, 'url': u, 'found_as': how, 'w': w, 'h': h, 'file': str(f.relative_to(ROOT)),
                     'meta_credit': credit, 'problems': flag})
        t = im.convert('RGB')
        t.thumbnail((360, 360))
        thumbs.append((n, t, flag))
    (CAND / 'candidates.json').write_text(json.dumps({'page': page, 'scanned': dt.datetime.now().isoformat(timespec='seconds'), 'images': rows}, indent=2))
    if thumbs:
        cols = 4
        sheet = Image.new('RGB', (cols * 380, ((len(thumbs) + cols - 1) // cols) * 400), '#16171B')
        d = ImageDraw.Draw(sheet)
        for i, (n, t, flag) in enumerate(thumbs):
            x, y = (i % cols) * 380 + 10, (i // cols) * 400 + 10
            sheet.paste(t, (x, y))
            d.rectangle([x, y, x + 64, y + 30], fill='#FF3B30' if flag else '#2E7D32')
            d.text((x + 8, y + 8), f'#{n}', fill='white')
        sheet.save(ROOT / 'build/photos/candidates-sheet.jpg', quality=85)
    for r in rows:
        print(f"#{r['n']:<3} {r['w']}x{r['h']:<5} {'OK ' if not r['problems'] else 'NO '} {', '.join(r['problems']):28} {r['meta_credit'][:60]:60} {r['url'][:90]}")
    print(f'\n{len(rows)} candidates. Look at build/photos/candidates-sheet.jpg (and the full files) before picking.' if rows else 'no usable images on that page')


def pick(n: int, slug: str, date: str, page_id: str, credit: str, shows: str, focus: str | None) -> None:
    from PIL import Image
    meta = json.loads((CAND / 'candidates.json').read_text())
    row = next((r for r in meta['images'] if r['n'] == n), None)
    if not row:
        sys.exit(f'no candidate #{n}')
    if row['problems']:
        sys.exit(f'candidate #{n} fails: {", ".join(row["problems"])}')
    im = Image.open(ROOT / row['file']).convert('RGB')
    if max(im.size) > 2400:
        im.thumbnail((2400, 2400), Image.LANCZOS)
    out = ROOT / 'media/photos' / date[:7] / f'{date}-{slug}.jpg'
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=90, optimize=True, progressive=True)
    fx, fy = (int(v) for v in (focus or '50,40').split(','))
    side = {'source_page': meta['page'], 'image_url': row['url'], 'credit': credit, 'shows': shows,
            'meta_credit': row['meta_credit'], 'width': row['w'], 'height': row['h'], 'focus': [fx, fy],
            'page': page_id, 'licence_basis': 'credited to its source (Geoffry, 23 Oct 2026: post anything, credit the source)',
            'sha1': hashlib.sha1(out.read_bytes()).hexdigest(), 'picked': dt.datetime.now().isoformat(timespec='seconds')}
    out.with_suffix('.json').write_text(json.dumps(side, ensure_ascii=False, indent=2) + '\n')
    print(out.relative_to(ROOT))
    problems = check(out)
    if problems:
        print('PROBLEMS:', *problems, sep='\n  - ')
        sys.exit(2)


def check(photo: pathlib.Path) -> list[str]:
    from PIL import Image
    probs = []
    side_f = photo.with_suffix('.json')
    if not photo.exists():
        return [f'photo missing: {photo}']
    if not side_f.exists():
        return [f'sidecar missing: {side_f.name}']
    s = json.loads(side_f.read_text())
    for k in ('source_page', 'image_url', 'credit', 'shows'):
        if not s.get(k):
            probs.append(f'sidecar has no {k}')
    if BLOCKED_HOSTS.search(urllib.parse.urlparse(s.get('source_page', '')).netloc + ' ' + urllib.parse.urlparse(s.get('image_url', '')).netloc):
        probs.append('blocked agency host')
    if BLOCKED.search(' '.join(str(s.get(k, '')) for k in ('credit', 'meta_credit'))):
        probs.append('agency/wire credit (Getty, AFP, Reuters, AP...)')
    w, h = Image.open(photo).size
    archive = s.get('series') == 'archive'  # "From the Archive": framed prints, smaller and older files are fine
    ms, ml = (450, 600) if archive else (MIN_SHORT, MIN_LONG)  # archive prints sit in a 560-900 px frame; the renderer also refuses >1.6x enlargement
    if min(w, h) < ms or max(w, h) < ml:
        probs.append(f'photo too small ({w}x{h}; needs at least {ms} px short side and {ml} px long side)')
    if 'commons.wikimedia.org' in s.get('source_page', '') or 'upload.wikimedia.org' in s.get('image_url', ''):
        if not s.get('author'):
            probs.append('Commons photo has no author recorded (the credit needs one)')
    return probs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['scan', 'pick', 'check'])
    ap.add_argument('arg')
    ap.add_argument('--min', type=int, default=None)
    ap.add_argument('--slug'); ap.add_argument('--date'); ap.add_argument('--page')
    ap.add_argument('--credit'); ap.add_argument('--shows'); ap.add_argument('--focus')
    a = ap.parse_args()
    if a.cmd == 'scan':
        scan(a.arg, a.min or MIN_SHORT)
    elif a.cmd == 'pick':
        for k in ('slug', 'date', 'page', 'credit', 'shows'):
            if not getattr(a, k):
                sys.exit(f'--{k} is required')
        pick(int(a.arg), a.slug, a.date, a.page, a.credit, a.shows, a.focus)
    else:
        pr = check(ROOT / a.arg)
        print('OK' if not pr else '\n'.join(pr))
        sys.exit(1 if pr else 0)


if __name__ == '__main__':
    main()
