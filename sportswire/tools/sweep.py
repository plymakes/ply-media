#!/usr/bin/env python3
"""Sports maps for both pages: what to check on every run (Geoffry, 23 Oct 2026: "those should be listed to go
over everytime ... the top 20 sports in lebanon"; then "let's do the same for cyprus").

Every command takes --page lb (default) or --page cy.

    python3 tools/sweep.py today [--date YYYY-MM-DD]      checklist for this run: every top-20 sport in rank
                                                          order, its live competitions, today's usual match
                                                          days, dated events in the next 7 days, athletes to
                                                          look up today, and the fast sources to open
    python3 tools/sweep.py week [--date …] [--days 14]    every dated event in the coming days, all sports
    python3 tools/sweep.py coverage [--days 21]           posts per sport on the page (content-log) against
                                                          each sport's "cover_every_days": overdue sports first
    python3 tools/sweep.py check                          validates the page's map

The maps: sources/lebanon-sports.json and sources/cyprus-sports.json (data), with a readable .md next to each.
Every spec names its "sport" with an id from its page's map (the gate checks).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAPS = {'lb': ROOT / 'sources/lebanon-sports.json', 'cy': ROOT / 'sources/cyprus-sports.json'}
NAMES = {'lb': 'Lebanon', 'cy': 'Cyprus'}
PAGE = 'lb'
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def load() -> dict:
    return json.loads(MAPS[PAGE].read_text())


def d(s: str | None) -> dt.date | None:
    if not s:
        return None
    s = str(s)
    try:
        if len(s) == 7:
            return dt.date.fromisoformat(s + '-01')
        return dt.date.fromisoformat(s[:10])
    except ValueError:
        return None


def season_state(comp: dict, day: dt.date) -> str:
    """'on' | 'off' | 'check' (dates not known) | 'soon' (starts within 14 days)"""
    se = comp.get('season') or {}
    a, b = d(se.get('start')), d(se.get('end'))
    if a and len(str(se.get('end', ''))) == 7 and b:  # "2027-05" means to the end of that month
        b = (b.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    if a and b:
        if a <= day <= b:
            return 'on'
        if dt.timedelta(0) < a - day <= dt.timedelta(days=14):
            return 'soon'
        return 'off'
    if comp.get('year_round'):
        return 'on'
    return 'check'


def src_line(s: dict) -> str:
    use = '/'.join(s.get('use', []))
    fetch = s.get('fetch', 'ok')
    flag = '' if fetch == 'ok' else f'  [{fetch}]'
    return f"      - {s.get('name')} (t{s.get('tier', '?')}, {use}{', ' + s['speed'] if s.get('speed') else ''}): {s.get('url')}{flag}"


def events_between(m: dict, a: dt.date, b: dt.date) -> list[dict]:
    out = []
    for e in m.get('calendar', []):
        s, t = d(e.get('date')), d(e.get('end') or e.get('date'))
        if s and t and s <= b and t >= a:
            out.append(e)
    return sorted(out, key=lambda e: e.get('date', ''))


def today(m: dict, day: dt.date) -> None:
    wd = DAYS[day.weekday()]
    print(f'# {NAMES[PAGE]} sports sweep: {wd} {day.isoformat()}  (map updated {m.get("updated")})\n')
    print('Go through every sport below, in order. For each live competition: today\'s games (time, venue), '
          'last night\'s results, news. Open the fast sources; confirm on tier 1 or two tier 2 (PLAYBOOK 4).\n')
    soon = events_between(m, day, day + dt.timedelta(days=7))
    if soon:
        print('## Dated events, today to +7 days')
        for e in soon:
            when = e['date'] + (f' → {e["end"]}' if e.get('end') and e['end'] != e['date'] else '')
            conf = '' if e.get('confirmed', True) else '  (date UNCONFIRMED: check)'
            print(f"- {when}  [{e.get('sport')}] {e.get('event')}  {e.get('who', '')}{conf}  {e.get('source', '')}")
        print()
    for sp in sorted(m['sports'], key=lambda x: x.get('rank', 99)):
        if sp.get('rank', 99) > 20 and not any(day.isoformat() <= (e.get('end') or e['date']) and e['date'] <= (day + dt.timedelta(days=2)).isoformat() for e in m.get('calendar', []) if e.get('sport') == sp['id']):
            continue  # beyond the top 20 only when one of its events is on now
        live = []
        for c in sp.get('competitions', []):
            st = season_state(c, day)
            if st in ('on', 'check', 'soon'):
                md = c.get('match_days') or []
                live.append((c, st, wd in md))
        print(f"## {sp.get('rank')}. {sp['name']}  (cover every {sp.get('cover_every_days', '?')} days)")
        for c, st, matchday in live:
            tag = {'on': 'IN SEASON', 'check': 'dates unknown: check', 'soon': 'STARTS SOON'}[st]
            md = ' · usual match day today' if matchday else ''
            print(f"  - {c['name']} [{tag}{md}]  priority {c.get('priority', 'C')}")
            for s in (c.get('sources') or [])[:4]:
                print(src_line(s))
        if not live:
            print('  - no competition in season: check news and the athletes below')
        ath = sp.get('athletes') or []
        if ath:
            daily = [a for a in ath if a.get('check') == 'daily']
            rot = [a for a in ath if a.get('check') != 'daily']
            todays = daily + [a for i, a in enumerate(rot) if i % 7 == day.weekday()]
            if todays:
                print('  - athletes to look up today: ' + '; '.join(f"{a['name']} ({a.get('where', '')})" + (f" {a['track']}" if a.get('track') else '') for a in todays))
        gs = sp.get('sources') or []
        if gs:
            print('  - sport-wide sources:')
            for s in gs[:3]:
                print(src_line(s))
        print()
    gen = m.get('general_sources') or []
    if gen:
        print('## General fast sources (all sports)')
        for s in gen:
            print(src_line(s))


def week(m: dict, day: dt.date, days: int) -> None:
    print(f'# Dated events {day} → {day + dt.timedelta(days=days)}\n')
    for e in events_between(m, day, day + dt.timedelta(days=days)):
        when = e['date'] + (f' → {e["end"]}' if e.get('end') and e['end'] != e['date'] else '')
        conf = '' if e.get('confirmed', True) else '  (UNCONFIRMED)'
        print(f"- {when}  [{e.get('sport')}] {e.get('event')}  {e.get('who', '')}{conf}  {e.get('source', '')}")
    print('\nSeasons starting or ending in this window:')
    for sp in m['sports']:
        for c in sp.get('competitions', []):
            se = c.get('season') or {}
            for k in ('start', 'end'):
                x = d(se.get(k))
                if x and day <= x <= day + dt.timedelta(days=days):
                    print(f"- {se[k]}  {sp['name']}: {c['name']} {k}s")


KEYWORDS_CY = {  # for log entries written before "sport" was recorded
    'football': r'cyprus-league|omonia|apoel|pafos|aek-larnaca|anorthosis|ael|apollon|aris|nations-league|uefa|cfa|riga|benfica|round-\d+-fixtures|table',
    'basketball': r'basket|keravnos|petrolina|fiba|europe-cup',
    'motorsport': r'tziortzis|nascar|rally',
    'sailing': r'kontides|sailing',
}
KEYWORDS = {  # for log entries written before "sport" was recorded
    'basketball': r'basket|flbb|riyadi|sagesse|homenetmen|champville|antranik|beirut-club|dubai-final|division-a',
    'football': r'football|afc|lfa|nejmeh|ahed|ansar|safa|cedars-u|fifa|wafu|waff|premier-league',
    'rugby-league': r'rlwc|rugby-league|cedars-rl|lebanonrl|tonga|samoa',
}


def sport_of(e: dict) -> str | None:
    if e.get('sport'):
        return e['sport']
    text = ' '.join(str(e.get(k, '')) for k in ('slug', 'story_key', 'headline'))
    for sid, pat in (KEYWORDS_CY if e.get('page') == 'cy' else KEYWORDS).items():
        if re.search(pat, text, re.I):
            return sid
    return None


def coverage(m: dict, days: int) -> None:
    log = json.loads((ROOT / 'content-log.json').read_text()).get('posts', [])
    today_ = dt.date.today()
    last: dict[str, str] = {}
    count: dict[str, int] = {}
    cutoff = (today_ - dt.timedelta(days=days)).isoformat()
    for e in log:
        if e.get('page') != PAGE or e.get('status') not in ('scheduled', 'published', 'corrected'):
            continue
        sid = sport_of(e)
        if not sid:
            continue
        last[sid] = max(last.get(sid, ''), e.get('date', ''))
        if e.get('date', '') >= cutoff:
            count[sid] = count.get(sid, 0) + 1
    rows = []
    for sp in sorted(m['sports'], key=lambda x: x.get('rank', 99)):
        if sp.get('rank', 99) > 20:
            continue
        every = int(sp.get('cover_every_days', 21))
        l = last.get(sp['id'])
        since = dt.date.fromisoformat(m.get('tracking_since', '2026-10-23'))  # a sport never posted counts from when tracking began
        gap = (today_ - min(dt.date.fromisoformat(l), today_)).days if l else (today_ - since).days
        rows.append((gap - every, sp, l, gap, every))
    print(f'# @sportswire.{PAGE} coverage, last {days} days (overdue first)\n')
    for over, sp, l, gap, every in sorted(rows, key=lambda r: -r[0]):
        state = 'OVERDUE' if over > 0 else 'ok'
        print(f"{state:8} #{sp['rank']:<2} {sp['name']:24} posts {count.get(sp['id'], 0):>2}  last {l or 'never':10}  every {every} d")
    print('\nOverdue sports get the next free spotlight, quiz, vote, explainer or archive slot (CAMPAIGN.md 5).')


def check(m: dict) -> int:
    probs = []
    ids = set()
    if len([s for s in m['sports'] if s.get('rank', 99) <= 20]) != 20:
        probs.append('the map must rank exactly 20 sports 1-20')
    for sp in m['sports']:
        if sp['id'] in ids:
            probs.append(f'duplicate sport id {sp["id"]}')
        ids.add(sp['id'])
        for c in sp.get('competitions', []):
            srcs = c.get('sources') or []
            if len(srcs) < 2:
                probs.append(f'{sp["id"]} / {c["name"]}: needs at least 2 sources (has {len(srcs)})')
            if not any('result' in s.get('use', []) for s in srcs + (sp.get('sources') or [])):
                probs.append(f'{sp["id"]} / {c["name"]}: no source marked for results')
            for s in srcs:
                if not str(s.get('url', '')).startswith('http'):
                    probs.append(f'{sp["id"]} / {c["name"]}: source without a URL ({s.get("name")})')
            se = c.get('season') or {}
            for k in ('start', 'end'):
                if se.get(k) and not d(se[k]):
                    probs.append(f'{c["name"]}: season {k} "{se[k]}" is not YYYY-MM(-DD)')
    for e in m.get('calendar', []):
        if not d(e.get('date')):
            probs.append(f'calendar: bad date in {e}')
        if e.get('sport') not in ids:
            probs.append(f'calendar: unknown sport "{e.get("sport")}" ({e.get("event")})')
    hosts = {}
    for sp in m['sports']:
        for c in sp.get('competitions', []):
            for s in c.get('sources', []):
                hosts.setdefault(urlparse(s.get('url', '')).netloc.replace('www.', ''), 0)
    print('\n'.join(probs) if probs else f'map OK: {len(m["sports"])} sports, {sum(len(s.get("competitions", [])) for s in m["sports"])} competitions, {len(m.get("calendar", []))} dated events, {len(hosts)} source sites')
    return 1 if probs else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['today', 'week', 'coverage', 'check'])
    ap.add_argument('--date')
    ap.add_argument('--days', type=int)
    ap.add_argument('--page', choices=['lb', 'cy'], default='lb')
    a = ap.parse_args()
    global PAGE
    PAGE = a.page
    if not MAPS[PAGE].exists():
        print(f'no map yet for {PAGE}: {MAPS[PAGE].relative_to(ROOT)}')
        return 0
    m = load()
    day = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    if a.cmd == 'today':
        today(m, day)
    elif a.cmd == 'week':
        week(m, day, a.days or 14)
    elif a.cmd == 'coverage':
        coverage(m, a.days or 21)
    else:
        return check(m)
    return 0


if __name__ == '__main__':
    sys.exit(main())
