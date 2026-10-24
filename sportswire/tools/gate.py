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


# ---- house style (Geoffry, 23 Oct 2026): fewer words per image, capitals for clubs/athletes/countries, "vs." not "v"
WORD_LIMITS = {'headline': 8, 'deck': 12, 'slide': 30, 'slide_archive_story': 40}
LIST_TEMPLATES = {'standings', 'fixtures', 'roundup', 'end', 'correction'}
WORD_SKIP = {'labels', 'columns', 'eyebrow_style', 'crest', 'home_crest', 'away_crest', 'headline_size', 'headline_lines', 'tone',
             'theme', 'template', 'align', 'section', 'footer_rule', '_theme', 'dur', 'photo', 'photo_height', 'photo_width',
             'photo_w', 'photo_h', 'eyebrow', 'footnote', 'footer', 'label', 'status', 'key', 'code', 'credit', 'alt', 'correct',
             'answer_footnote', 'issue', 'stamp', 'year', 'kicker'}
NOT_NAMES = {'central', 'jersey', 'chad', 'turkey', 'china', 'guinea', 'final', 'cup', 'league', 'club', 'national'}
DEMONYMS = ['Lebanese', 'Cypriot', 'Cypriots', 'Lebanon', 'Cyprus', 'Arab', 'Asian', 'European', 'Olympic', 'Olympics', 'Paralympic',
            'Paralympics', 'Mediterranean', 'Commonwealth', 'Greek', 'Turkish', 'Beirut', 'Nicosia', 'Limassol', 'Larnaca', 'Paphos', 'Pafos']


def words_of(x, key=None) -> list[str]:
    out: list[str] = []
    if key in WORD_SKIP:
        return out
    if isinstance(x, dict):
        for k, v in x.items():
            out += words_of(v, k)
    elif isinstance(x, list):
        for v in x:
            out += words_of(v, key)
    elif isinstance(x, str):
        out += [w for w in re.split(r'\s+', x.replace('*', ' ').replace('\n', ' ')) if re.search(r'[A-Za-z\u0600-\u06FF\u0370-\u03FF]', w)]
    return out


def word_problems(spec: dict) -> list[str]:
    probs = []
    slides = spec.get('slides') or [{'template': spec.get('template'), 'card': spec.get('card', {})}]
    for i, sl in enumerate(slides, 1):
        c, tpl = sl.get('card', {}), sl.get('template')
        if tpl == 'end':
            continue
        for k in ('headline', 'deck'):
            n = len(words_of(c.get(k, '')))
            if n > WORD_LIMITS[k]:
                probs.append(f'slide {i}: {k} has {n} words (max {WORD_LIMITS[k]}): fewer words per image (Geoffry, 23 Oct 2026)')
        if tpl in LIST_TEMPLATES:
            continue
        limit = WORD_LIMITS['slide_archive_story'] if (spec.get('series') == 'archive' and tpl == 'story') else WORD_LIMITS['slide']
        n = len(words_of(c))
        if n > limit:
            probs.append(f'slide {i} ({tpl}): {n} words on the image (max {limit}): cut text or split it across slides; the caption carries the detail')
    return probs


def known_names() -> list[str]:
    names = set(DEMONYMS)
    try:
        for slug, v in json.loads((ROOT / 'brand/crests/index.json').read_text()).items():
            names.add(v.get('name') or ''); names.add(slug.replace('-', ' '))
    except Exception:
        pass
    try:
        names.update(json.loads((ROOT / 'brand/flags/index.json').read_text())['flags'].values())
    except Exception:
        pass
    for mp in ('sources/lebanon-sports.json', 'sources/cyprus-sports.json'):
        try:
            for sp in json.loads((ROOT / mp).read_text())['sports']:
                for a in sp.get('athletes', []):
                    names.update(n.strip() for n in re.split(r'/| and ', a.get('name', '')) if n.strip())
        except Exception:
            pass
    return sorted({n for n in names if len(n) >= 3 and n.lower() not in NOT_NAMES}, key=len, reverse=True)


def case_problems(text: str) -> list[str]:
    text = re.sub(r'https?://\S+|[@#][\w.]+', ' ', text)
    bad = set()
    for n in known_names():
        for m in re.finditer(r'(?<![\w-])' + re.escape(n.lower()) + r'(?![\w-])', text, re.I):
            if m.group(0) == m.group(0).lower():
                bad.add(m.group(0))
    return sorted(bad)



# Captions that read like a person, not a press release (Geoffry, 24 Oct 2026: "it's very AI ... less words").
VOICE_FROM = '2026-10-24'
CAPTION_WORDS = {'default': 40, 'archive': 60}
SENTENCE_WORDS = 20
AI_TELLS = [r'showcas', r'testament', r'underscor', r'highlighting', r'\bcement', r'solidif', r'remarkable',
            r'thrilling', r'\bclash\b', r'set the stage', r'worth noting', r'a reminder', r'not only\b', r'\bjourney\b',
            r'\bdelve', r'\bboast', r'in the world of', r'when it comes to', r'proved to be', r'—', r'\bunwavering',
            r'\bpivotal\b', r'\bnail-biting\b', r'\bspectacular\b', r'\bfierce\b', r'\bbattle(d)?\b', r'\bsecured?\b',
            r'\bhad already\b', r'\bin a (\w+ )?(game|match|contest) (that|which)\b', r'\bbring(s)? the curtain',
            r'\bwhat a (night|game|performance)\b', r'\bcap(ped)? off\b', r'\bdominant\b', r'\bstellar\b']
ARABIC_FROM = '2026-10-24'   # LB captions: simple Arabic under the English (Geoffry, 24 Oct 2026)
ARABIC_RE = re.compile(r'[؀-ۿ]')


def caption_parts(cap: str) -> tuple[str, str]:
    """English body (before the Arabic, credit, source, tags) and the Arabic block."""
    eng, ar = [], []
    for line in cap.split('\n'):
        t = line.strip()
        if not t:
            continue
        if t.startswith(('📸', 'Source', '@', '#', '(Story')):
            continue
        if ARABIC_RE.search(t) and len(ARABIC_RE.findall(t)) > len(re.findall(r'[A-Za-z]', t)):
            ar.append(t)
        elif not ar:
            eng.append(t)
    return '\n'.join(eng), '\n'.join(ar)


def voice_problems(spec: dict, cap: str) -> list[str]:
    probs = []
    if spec.get('format') == 'story' or cap.startswith('(Story'):
        return probs
    eng, ar = caption_parts(cap)
    n = len(re.findall(r"[A-Za-z0-9][\w'’.-]*", eng))
    limit = CAPTION_WORDS['archive'] if spec.get('series') == 'archive' else CAPTION_WORDS['default']
    if n > limit:
        probs.append(f'English caption is {n} words (max {limit}): say it like a person would, cut every line the card already says (PLAYBOOK 7, Captions)')
    for sent in re.split(r'(?<=[.!?])\s+|\n', eng):
        w = len(re.findall(r"[A-Za-z0-9][\w'’.-]*", sent))
        if w > SENTENCE_WORDS:
            probs.append(f'sentence of {w} words (max {SENTENCE_WORDS}): split it or cut it: "{sent[:60]}…"')
    low = eng.lower()
    tells = sorted({re.search(t, low).group(0) for t in AI_TELLS if re.search(t, low)})
    if tells:
        probs.append('sounds like AI, rewrite plainly: ' + ', '.join(f'"{t}"' for t in tells))
    if spec['page'] == 'lb' and spec['date'] >= ARABIC_FROM:
        aw = len(re.findall(r'[؀-ۿ]+', ar))
        if aw < 4:
            probs.append('Lebanon captions carry a short, simple Arabic version under the English (Geoffry, 24 Oct 2026)')
        elif aw > 45:
            probs.append(f'Arabic part is {aw} words (max 45): keep it short and simple, like a person would write it')
        if ar and spec.get('factcheck', {}).get('arabic_checked') is not True:
            probs.append('the fact-checker must also check the Arabic (same facts as the English, names and numbers right): set factcheck.arabic_checked true')
    return probs

MAX_COLLABORATORS = 3       # Instagram's own limit is higher; three keeps invites meaningful
MAX_INVITES_PER_WEEK = 3    # per account, across both pages: nobody gets spammed with invites (raised from 2, 24 Oct 2026)
MAX_MENTIONS = 6


def tag_problems(spec: dict, cap: str, handles: dict, cards: list, high: set) -> list[str]:
    probs = []
    rs = spec.get('reshare') or {}
    cols = [c.lower() for c in rs.get('collaborators', [])]
    mentioned = {h.lower().rstrip('.') for h in re.findall(r'@([\w.]+)', cap)}
    # every account whose crest or national team is on the card is tagged in the caption
    logos: set[str] = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ('crest', 'home_crest', 'away_crest') and v:
                    logos.add(str(v))
                else:
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for c in cards:
        walk(c)
    sport = spec.get('sport')
    need = set()
    for h, v in handles.items():
        if not v.get('confirmed') or v.get('page') not in (spec['page'], None):
            continue
        if v.get('crest') and v['crest'] in logos:
            need.add(h.lower())
        nt = v.get('national_team') or {}
        if nt and f'flag:{nt.get("flag")}' in logos and nt.get('sport') == sport:
            need.add(h.lower())
    for h in sorted(need - mentioned):
        probs.append(f'tag @{h} in the caption: its logo is on the card (always tag the people in the story)')
    # the sport's federation (and other accounts that cover the whole sport) on every feed post (Geoffry, 24 Oct 2026)
    is_story = spec.get('format') == 'story' or cap.startswith('(Story')
    if not is_story and spec['date'] >= '2026-10-24':
        for h, v in handles.items():
            cov = v.get('covers') or {}
            if v.get('confirmed') and cov and v.get('page') == spec['page'] and sport in cov.get('sports', []) \
                    and h.lower() not in mentioned:
                probs.append(f'tag @{h} ({v.get("who")}): it covers {sport} on this page, so it goes on every {sport} post')
    if not mentioned and not (is_story and rs.get('no_tag_reason')):
        probs.append('no @mention in the caption: tag the federation and every club, athlete and organiser in the story (feed posts always tag someone; find the handle or add it to sources/handles.json)')
    if len(mentioned) > MAX_MENTIONS:
        probs.append(f'{len(mentioned)} @mentions: max {MAX_MENTIONS}, only accounts that are part of the story (no tagging for reach alone)')
    # collaborators: where applicable, within limits
    if len(cols) > MAX_COLLABORATORS:
        probs.append(f'{len(cols)} collaborators: max {MAX_COLLABORATORS}')
    for c in cols:
        if c not in mentioned:
            probs.append(f'collaborator @{c} should also be @mentioned in the caption')
    tpl = spec.get('template') or ''
    if tpl == 'result' or any(sl.get('template') == 'result' for sl in spec.get('slides', [])):
        for c in cards:
            if c.get('home') and c.get('away'):
                try:
                    hs, as_ = float(c['home']['score']), float(c['away']['score'])
                except (TypeError, ValueError, KeyError):
                    continue
                loser = c['home'] if hs < as_ else c['away'] if as_ < hs else None
                if loser and loser.get('crest') and not rs.get('invite_reason'):
                    for h, v in handles.items():
                        if v.get('crest') == loser['crest'] and h.lower() in cols:
                            probs.append(f'@{h} lost this game: no invite on a defeat, unless the post is good news for them (set reshare.invite_reason, e.g. "qualified despite the defeat")')
    if spec['light'] == 'green' and not is_story and len(cols) < MAX_COLLABORATORS:
        skip = {k.lower() for k in (rs.get('not_invited') or {})}
        fed = {h.lower() for h, v in handles.items() if v.get('covers')}
        for h in sorted((mentioned & high) - set(cols) - skip - fed - {'sportswire.lb', 'sportswire.cy'}):
            probs.append(f'invite @{h} as a collaborator (everyone possible, max {MAX_COLLABORATORS}), or put it in reshare.not_invited with a reason (e.g. "lost and the post is about the defeat", "invited 3 times this week", "neutral derby: both or neither")')
    try:
        log = json.loads((ROOT / 'content-log.json').read_text()).get('posts', [])
        since = (dt.date.fromisoformat(spec['date']) - dt.timedelta(days=6)).isoformat()
        for c in cols:
            n = sum(1 for e in log if e.get('date', '') >= since and e.get('status') in ('scheduled', 'published')
                    and e.get('slug') != spec['slug'] and c in [x.lower() for x in ((e.get('reshare') or {}).get('collaborators') or [])])
            if n >= MAX_INVITES_PER_WEEK:
                probs.append(f'@{c} has already been invited {n} times in the last 7 days: mention only this time (no spamming)')
    except Exception:
        pass
    return probs


def card_text(spec: dict) -> str:
    skip = {'labels', 'columns', 'eyebrow_style', 'crest', 'home_crest', 'away_crest', 'headline_size', 'headline_lines',
            'tone', 'theme', 'template', 'align', 'section', 'footer_rule', '_theme', 'dur', 'photo',
            'photo_height', 'photo_width', 'photo_w', 'photo_h'}  # layout sizes, not facts
    parts: list[str] = []

    def walk(x, key=None):
        if key in skip:
            return
        if isinstance(x, dict):
            if 'options' in x and x.get('correct'):  # quiz answer: the wrong options are not claims, only the right one is
                keys = [str(o.get('key') or 'ABCD'[i]).upper() for i, o in enumerate(x['options'])]
                x = {**x, 'options': [o for k, o in zip(keys, x['options']) if k == str(x['correct']).upper()]}
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, (str, int, float)) and not isinstance(x, bool):
            parts.append(str(x))
    slides = spec.get('slides') or [{'card': spec.get('card', {}), 'template': spec.get('template')}]
    for s in slides:
        card = s.get('card', {})
        if s.get('template') == 'quiz':  # the question's options are checked on the answer slide (only the right one is a claim)
            card = {k: v for k, v in card.items() if k != 'options'}
        walk(card)
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

    # 1b. specs name their sport from the page's sports map, so coverage of every top-20 sport can be tracked
    mp = ROOT / {'lb': 'sources/lebanon-sports.json', 'cy': 'sources/cyprus-sports.json'}.get(spec['page'], 'none')
    if spec['date'] >= '2026-10-24' and mp.exists():
        ids = {x['id'] for x in json.loads(mp.read_text())['sports']}
        if not spec.get('sport'):
            probs.append(f'"sport" missing: use an id from {mp.relative_to(ROOT)} (tools/sweep.py check --page {spec["page"]})')
        elif spec['sport'] not in ids:
            probs.append(f'"sport": "{spec["sport"]}" is not an id in {mp.relative_to(ROOT)}')

    # 1c. house style for new posts (Geoffry, 23 Oct 2026)
    if spec['date'] >= '2026-10-24':
        probs += word_problems(spec)
        low = case_problems(card_text(spec) + '\n' + spec['caption'])
        if low:
            probs.append('capitalise clubs, athletes and countries: ' + ', '.join(f'"{w}"' for w in low))
        if re.search(r'\b[A-Z][\w.\'-]* v\.? [A-Z]', spec['caption']):
            probs.append('write "vs." between teams in the caption, not "v" (cards convert it automatically)')
    if spec['date'] >= VOICE_FROM:
        probs += voice_problems(spec, spec['caption'])

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

    # 3b. a quiz always carries its answer, and the answer slide repeats the same options
    sl = spec.get('slides') or [{'template': spec.get('template'), 'card': spec.get('card', {})}]
    quizzes = [x for x in sl if x.get('template') == 'quiz']
    answers = [x for x in sl if x.get('template') == 'answer']
    if quizzes and not answers:
        probs.append('a quiz needs its "answer" slide in the same spec (next carousel slide, or the next Story)')
    for q, a in zip(quizzes, answers):
        qo = [o.get('text') for o in q['card'].get('options', [])]
        ao = [o.get('text') for o in a['card'].get('options', [])]
        if qo != ao:
            probs.append('the answer slide must repeat the quiz options exactly, in the same order')

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

    def photos_in(x, out):  # card photo plus photos on quiz/vote options
        if isinstance(x, dict):
            if isinstance(x.get('photo'), dict) and x['photo'].get('file'):
                out.append(x['photo'])
            for k, v in x.items():
                if k != 'photo':
                    photos_in(v, out)
        elif isinstance(x, list):
            for v in x:
                photos_in(v, out)
        return out
    all_photos = []
    for c in cards:
        crests_in(c)
        photos_in(c, all_photos)
    for ph in all_photos:
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
        if name.startswith('flag:'):
            if not (ROOT / 'brand/flags' / f'{name[5:]}.svg').exists():
                probs.append(f'flag "{name}" is not in brand/flags (use the ISO code, e.g. flag:lb, flag:cy, flag:gb-eng)')
            continue
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

    # 6b. tags (Geoffry, 23 Oct 2026: "always tag the people affected, mention and invite collaborators where applicable…
    #     tag as much as possible to increase reach without spamming people")
    if spec['date'] >= '2026-10-23':
        probs += tag_problems(spec, cap, handles, cards, high)

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
