#!/usr/bin/env python3
"""content-log.json helper.

    python3 tools/log.py add <spec.json> --status scheduled|draft --when 2026-10-20T10:30:00+03:00 \
        --metricool-id 123 --planner-url https://… --urls https://raw…/a.png,https://raw…/b.png
    python3 tools/log.py kill <spec.json or page:slug> --reason "only one tier-2 source"
    python3 tools/log.py set <page:slug> --status published|corrected [--note "…"]
    python3 tools/log.py recent [--days 7]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / 'content-log.json'


def load():
    return json.loads(LOG.read_text())


def save(d):
    LOG.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['add', 'kill', 'set', 'recent'])
    ap.add_argument('target', nargs='?')
    ap.add_argument('--status')
    ap.add_argument('--when')
    ap.add_argument('--metricool-id')
    ap.add_argument('--planner-url')
    ap.add_argument('--urls', default='')
    ap.add_argument('--reason', default='')
    ap.add_argument('--note', default='')
    ap.add_argument('--days', type=int, default=7)
    a = ap.parse_args()
    d = load()

    if a.cmd == 'recent':
        cutoff = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
        for e in d['posts']:
            if e.get('date', '') >= cutoff:
                print(f"{e.get('date')} {e.get('page')} {e.get('status'):9} {e.get('scheduled_for', '')[:16]:16} {e.get('slug')}  {e.get('story_key', '')}  {e.get('reason', '')}")
        return

    if a.cmd in ('add', 'kill') and a.target and a.target.endswith('.json'):
        spec = json.loads(pathlib.Path(a.target).read_text())
        entry = {
            'page': spec.get('page'), 'date': spec.get('date'), 'slug': spec.get('slug'),
            'story_key': spec.get('story_key'), 'light': spec.get('light'),
            'template': spec.get('template') or ','.join(s['template'] for s in spec.get('slides', [])),
            'headline': (spec.get('card') or (spec.get('slides') or [{}])[0].get('card', {})).get('headline', ''),
            'caption_first_line': (spec.get('caption') or '').split('\n')[0][:160],
            'sources': sorted({s['url'] for f in spec.get('facts', []) for s in f.get('sources', [])}),
            'reshare': spec.get('reshare'), 'spec': a.target, 'logged_at': now(),
        }
    elif a.target and ':' in a.target:
        page, slug = a.target.split(':', 1)
        entry = {'page': page, 'slug': slug, 'date': dt.date.today().isoformat(), 'logged_at': now()}
    else:
        raise SystemExit('target must be a spec path or page:slug')

    if a.cmd == 'add':
        entry.update(status=a.status or 'scheduled', scheduled_for=a.when, metricool_id=a.metricool_id,
                     planner_url=a.planner_url, image_urls=[u for u in a.urls.split(',') if u])
        d['posts'].append(entry)
    elif a.cmd == 'kill':
        entry.update(status='killed', reason=a.reason)
        d['posts'].append(entry)
    elif a.cmd == 'set':
        for e in reversed(d['posts']):
            if e.get('page') == entry['page'] and e.get('slug') == entry['slug']:
                e['status'] = a.status
                if a.note:
                    e.setdefault('notes', []).append(f'{now()} {a.note}')
                break
        else:
            raise SystemExit('not found')
    save(d)
    print('logged')


if __name__ == '__main__':
    main()
