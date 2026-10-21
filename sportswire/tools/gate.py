#!/usr/bin/env python3
"""Pre-publish gate. A post is scheduled only if this prints READY.

    python3 tools/gate.py specs/2026-10-19/lb-slug.json [more.json ...]

Checks, in order:
  1. spec has page, slug, date, event_date, caption, light (green|amber), facts
  2. every fact is backed by one tier-1 source or two tier-2 sources on different sites
  3. every number on the card and in the caption appears in a verified fact
  4. the independent fact-check passed (every claim CONFIRMED)
  5. the card rendered without layout problems and was visually checked
  6. caption rules: length, hashtags, source line, only confirmed @handles
  7. traffic light: rumour words never publish; sensitive topics must be AMBER
  8. not a duplicate of something already in content-log.json, and fresh enough
Exit code 0 = all READY, 1 = something is not ready (reasons printed).
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent

RUMOUR = [r'\breportedly\b', r'\brumou?rs?\b', r'\bset to (sign|join|leave|be)\b', r'\bclose to (signing|joining)\b',
          r'\bin talks\b', r'\baccording to reports\b', r'\ballegedly\b', r'\bexpected to (sign|join|leave)\b',
          r'\bunconfirmed\b', r'\bsources say\b', r'\bodds\b', r'\bbetting\b', r'\bbet\b']
SENSITIVE = [r'\bdied\b', r'\bdeath\b', r'\bpassed away\b', r'\bfuneral\b', r'\bobituary\b', r'\binjur(y|ies|ed)\b',
             r'\bsurgery\b', r'\bhospital', r'\barrest', r'\bcourt\b', r'\btrial\b', r'\bbann?ed\b', r'\bban\b',
             r'\bsuspen(ded|sion)\b', r'\bdoping\b', r'\bdisciplinary\b', r'\ballegation', r'\bassault', r'\bracis',
             r'\bviolen', r'\bclash(es|ed)?\b', r'\bpolice\b', r'\bwar\b', r'\bstrike(s)?\b', r'\bpolitic',
             r'\bsectarian\b', r'\boccupied\b', r'\bnorth(ern)? cyprus\b', r'\btrnc\b', r'\bisrael', r'\bhezbollah\b']


def numbers(text: str) -> set[str]:
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[@#][\w.]+', ' ', text)
    out = set()
    for m in re.findall(r'(?<![A-Za-z0-9])\d+(?:[.,:]\d+)*', text):  # digits inside names (Cairo24) don't count
        out.add(m.replace(',', ''))
    return out


def card_text(spec: dict) -> str:
    skip = {'labels', 'columns', 'eyebrow_style', 'crest', 'home_crest', 'away_crest', 'headline_size', 'headline_lines',
            'tone', 'theme', 'template', 'align', 'section', 'footer_rule', '_theme', 'dur', 'photo'}
    parts: list[str] = []

    def walk(x, key=None):
        if key in skip:
            return
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, (str, int, float)) and not isinstance(x, bool):
            parts.append(str(x))
    slides = spec.get('slides') or [{'card': spec.get('card', {})}]
    for s in slides:
        walk(s.get('card', {}))
    return '\n'.join(parts)


def check(path: str) -> list[str]:
    p = pathlib.Path(path)
    spec = json.loads(p.read_text())
    probs: list[str] = []
    for k in ('page', 'slug', 'date', 'event_date', 'caption', 'light', 'facts'):
        if not spec.get(k):
            probs.append(f'missing "{k}"')
    if probs:
        return probs
    if spec['page'] not in ('lb', 'cy'):
        probs.append('page must be lb or cy')
    if spec['light'] not in ('green', 'amber'):
        probs.append('light must be green or amber (red stories are never specced)')

    # 2. sources per fact
    claims_text = ''
    for i, f in enumerate(spec['facts'], 1):
        srcs = f.get('sources') or []
        claims_text += ' ' + f.get('claim', '')
        t1 = [s for s in srcs if s.get('tier') == 1 and s.get('url', '').startswith('http')]
        t2_sites = {urlparse(s['url']).netloc.replace('www.', '') for s in srcs if s.get('tier') == 2 and s.get('url', '').startswith('http')}
        if not t1 and len(t2_sites) < 2:
            probs.append(f'fact {i} "{f.get("claim", "")[:60]}" needs a tier-1 source or two tier-2 sources on different sites')

    # 3. numbers
    verified = numbers(claims_text)
    shown = numbers(card_text(spec)) | numbers(spec['caption'])
    missing = sorted(n for n in shown - verified if not (len(n) == 4 and n == spec['date'][:4] and n in claims_text))
    if missing:
        probs.append('numbers on the card/caption not found in any verified fact: ' + ', '.join(missing))

    # 4. independent fact-check
    fc = spec.get('factcheck') or {}
    if fc.get('status') != 'pass':
        probs.append('independent fact-check has not passed (factcheck.status != "pass")')
    bad = [c for c in fc.get('claims', []) if c.get('verdict') != 'CONFIRMED']
    if bad:
        probs.append(f'{len(bad)} fact-check claim(s) not CONFIRMED: ' + '; '.join(c.get('claim', '')[:50] for c in bad))
    if fc.get('status') == 'pass' and not fc.get('claims'):
        probs.append('factcheck.claims is empty: list each claim the checker confirmed')

    # 5. render + visual check
    r = spec.get('render') or {}
    if not spec.get('images'):
        probs.append('not rendered yet (no images)')
    else:
        for im in spec['images']:
            if not (ROOT / im).exists():
                probs.append(f'image missing on disk: {im}')
    if spec.get('format') == 'reel':
        meta = spec.get('reel_meta') or {}
        if not any(str(im).endswith('.mp4') for im in spec.get('images', [])):
            probs.append('reel has no rendered .mp4')
        snd = meta.get('sound') or {}
        if snd.get('mean_db', -99) < -30:
            probs.append('reel has no soundtrack or it is too quiet: every Reel must have sound (re-render with tools/render.py)')
        if meta.get('seconds', 0) > 45:
            probs.append(f'reel is {meta.get("seconds")}s (news Reels under 20s, explainers under 45s)')
        if not (spec.get('visual_check') or {}).get('frames_checked'):
            probs.append('look at the frames sheet and the cover, then set visual_check.frames_checked true')
    if r.get('problems'):
        probs.append('render reported layout problems: ' + '; '.join(r['problems']))
    if not (spec.get('visual_check') or {}).get('done'):
        probs.append('visual check not recorded (visual_check.done must be true after looking at every PNG)')

    # 5b. photos and crests (PLAYBOOK, Images and rights)
    cap = spec['caption']
    cards = [spec['card']] if 'card' in spec else [s.get('card', {}) for s in spec.get('slides', [])]
    crest_idx = json.loads((ROOT / 'brand/crests/index.json').read_text()) if (ROOT / 'brand/crests/index.json').exists() else {}
    crest_names: set[str] = set()

    def crests_in(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ('crest', 'home_crest', 'away_crest') and v:
                    crest_names.add(str(v))
                else:
                    crests_in(v)
        elif isinstance(x, list):
            for v in x:
                crests_in(v)
    photo_check = None
    for c in cards:
        crests_in(c)
        ph = c.get('photo')
        if not ph:
            continue
        if photo_check is None:
            import runpy
            photo_check = runpy.run_path(str(ROOT / 'tools/photos.py'), run_name='photos')['check']
        f = ROOT / ph.get('file', '')
        for pr in photo_check(f):
            probs.append(f'photo {ph.get("file")}: {pr}')
        side = json.loads(f.with_suffix('.json').read_text()) if f.with_suffix('.json').exists() else {}
        credit = ph.get('credit') or side.get('credit') or ''
        if credit and credit.lower() not in cap.lower():
            probs.append(f'caption must credit the photo ("📸 {credit}")')
        if spec.get('light') == 'green' and re.search(r'injur|stretcher|blood|fight|brawl|tears', side.get('shows', ''), re.I):
            probs.append('photo looks sensitive (injury, fight, distress): drop it or make the post AMBER')
    for name in sorted(crest_names):
        if not (ROOT / 'brand/crests' / f'{name}.png').exists():
            probs.append(f'crest "{name}" is not in brand/crests (add it with tools/crests.py, or remove it)')
        elif name in crest_idx and not crest_idx[name].get('checked'):
            probs.append(f'crest "{name}" has not been visually checked (tools/crests.py sheet {name}, look, then tools/crests.py ok {name})')

    # 6. caption
    if len(cap) > 2200:
        probs.append(f'caption is {len(cap)} characters (max 2200)')
    tags = re.findall(r'#\w+', cap)
    if len(tags) > 3:
        probs.append(f'{len(tags)} hashtags (max 3: keyword-rich captions do the discovery work now)')
    if not re.search(r'^Source[s]?:', cap, re.M):
        probs.append('caption needs a "Source: ..." line')
    handles = json.loads((ROOT / 'sources/handles.json').read_text()).get('handles', {})
    confirmed = {h.lower() for h, v in handles.items() if v.get('confirmed')}
    used = {h.lower().rstrip('.') for h in re.findall(r'@([\w.]+)', cap)}
    for col in (spec.get('reshare') or {}).get('collaborators', []):
        used.add(col.lower())
    for h in sorted(used - confirmed):
        probs.append(f'@{h} is not a confirmed handle in sources/handles.json')
    high = {h.lower() for h, v in handles.items() if v.get('confirmed') and v.get('confidence', 'high') == 'high'}
    for col in (spec.get('reshare') or {}).get('collaborators', []):
        if col.lower() not in high:
            probs.append(f'collaborator @{col} needs a high-confidence handle (linked from its own official site or approved by Geoffry)')
        if spec['light'] != 'green':
            probs.append('no collaborator invites on AMBER posts')

    # 7. traffic light
    alltext = (card_text(spec) + '\n' + cap).lower()
    for pat in RUMOUR:
        if re.search(pat, alltext):
            probs.append(f'rumour/betting language "{re.search(pat, alltext).group(0)}": rewrite with confirmed facts only, or drop the story')
    if spec['light'] == 'green':
        hits = sorted({re.search(pat, alltext).group(0) for pat in SENSITIVE if re.search(pat, alltext)})
        if hits and not spec.get('sensitive_override'):
            probs.append('looks sensitive (' + ', '.join(hits) + '): must be AMBER (Metricool draft for Geoffry), or set "sensitive_override" with a one-line reason if it is plainly not sensitive (e.g. "strike" meaning a goal)')
        is_quote = spec.get('template') == 'quote' or any(s.get('template') == 'quote' for s in spec.get('slides', []))
        if is_quote:
            probs.append('quote cards are always AMBER')

    # 8. duplicates and freshness
    log = json.loads((ROOT / 'content-log.json').read_text())
    for e in log.get('posts', []):
        if e.get('page') == spec['page'] and e.get('slug') == spec['slug'] and e.get('status') != 'killed':
            probs.append(f'already in content-log ({e.get("status")} {e.get("scheduled_for", "")})')
        if spec.get('story_key') and e.get('story_key') == spec['story_key'] and e.get('page') == spec['page'] and e.get('status') in ('scheduled', 'published', 'draft'):
            probs.append(f'same story_key already posted: {e.get("slug")}')
    try:
        ev = dt.date.fromisoformat(spec['event_date'][:10])
        age = (dt.date.fromisoformat(spec['date']) - ev).days
        if age > 2 and not spec.get('feature'):
            probs.append(f'event is {age} days old: only post it as a feature ("feature": true) with a fresh angle')
    except ValueError:
        probs.append('event_date must be YYYY-MM-DD')
    return probs


def main(paths: list[str]) -> int:
    rc = 0
    for p in paths:
        probs = check(p)
        if probs:
            rc = 1
            print(f'NOT READY  {p}')
            for pr in probs:
                print(f'   - {pr}')
        else:
            print(f'READY      {p}')
    return rc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1:]))
