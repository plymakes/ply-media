#!/usr/bin/env python3
"""Regenerates the readable sports map from its JSON, keeping the hand-written intro.

    python3 tools/mapdoc.py lb      # sources/lebanon-sports.json -> sources/lebanon-sports.md
    python3 tools/mapdoc.py cy      # sources/cyprus-sports.json  -> sources/cyprus-sports.md

Edit the JSON (dates, sources, athletes, ranks), then run this. The intro is everything in the .md above
"## The top 20"; edit it in the .md directly.
"""
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
page = sys.argv[1] if len(sys.argv) > 1 else 'lb'
base = {'lb': 'lebanon-sports', 'cy': 'cyprus-sports'}[page]
m = json.loads((root / f'sources/{base}.json').read_text())
intro = (root / f'sources/{base}.md').read_text().split('## The top 20', 1)[0]
out = [intro.rstrip(), '']
out.append('## The top 20 (rank order = sweep order)\n')
out.append('| # | Sport | Cover at least every | Why it ranks here |')
out.append('|---|---|---|---|')
for sp in sorted(m['sports'], key=lambda x: x['rank']):
    if sp['rank'] > 20:
        continue
    out.append(f"| {sp['rank']} | {sp['name']} | {sp.get('cover_every_days')} days | {sp.get('why', '')} |")
out.append('\n**Watch list (beyond the top 20):** ' + '; '.join(f"{sp['name']} ({sp.get('why', '')})" for sp in sorted(m['sports'], key=lambda x: x['rank']) if sp['rank'] > 20) + '. These come into the sweep only when one of their dated events is on.\n')
out.append('## General fast sources (all sports)\n')
out.append('| Source | Good for | Speed | Tier | Notes |')
out.append('|---|---|---|---|---|')
for s in m['general_sources']:
    out.append(f"| [{s['name']}]({s['url']}) | {', '.join(s.get('use', []))} | {s.get('speed', '')} | {s.get('tier')} | {s.get('note', '')} |")
out.append('\n**Don\'t rely on:** ' + '; '.join(m.get('avoid', [])) + '.\n')
for sp in sorted(m['sports'], key=lambda x: x['rank']):
    out.append(f"## {sp['rank']}. {sp['name']}\n")
    f = sp.get('federation') or {}
    out.append(f"- **Governing body:** {f.get('name', '')}. Site: {f.get('site') or 'none found'}. Handles: {f.get('handles') or 'UNCONFIRMED'}.")
    if sp.get('seasonal'):
        out.append(f"- **Season:** {sp['seasonal']}.")
    if sp.get('notes'):
        for n in sp['notes']:
            out.append(f'- {n}')
    out.append('- **Competitions we track:**')
    for c in sp.get('competitions', []):
        se = c.get('season') or {}
        when = 'year-round' if c.get('year_round') else (f"{se.get('start') or '?'} → {se.get('end') or '?'}" if (se.get('start') or se.get('end')) else 'dates to confirm')
        md = f"; usual days {', '.join(c['match_days'])}" if c.get('match_days') else ''
        est = ' (end estimated)' if c.get('end_estimated') else ''
        out.append(f"  - **{c['name']}** ({c.get('level')}, priority {c.get('priority', 'C')}; {when}{est}{md})")
        if c.get('notes'):
            out.append(f"    - {c['notes']}")
        for s in c.get('sources', []):
            note = f" ({s['note']})" if s.get('note') else ''
            out.append(f"    - [{s['name']}]({s['url']}): {', '.join(s.get('use', []))}; {s.get('speed', '')}; tier {s.get('tier')}{note}")
    if sp.get('images'):
        out.append(f"- **Photos appear first at:** {sp['images']}.")
    if sp.get('athletes'):
        out.append('- **People to follow:** ' + '; '.join(f"{a['name']} ({a.get('where', '')})" for a in sp['athletes']) + '.')
    if sp.get('sources'):
        out.append('- **Sport-wide sources:** ' + '; '.join(f"[{s['name']}]({s['url']})" for s in sp['sources']) + '.')
    out.append('')
out.append('## Dated events (also in the JSON; `tools/sweep.py week` lists them)\n')
out.append('| Date | Sport | Event | Who | Confirmed |')
out.append('|---|---|---|---|---|')
for e in sorted(m['calendar'], key=lambda e: e['date']):
    when = e['date'] + (f" → {e['end']}" if e.get('end') else '')
    out.append(f"| {when} | {e['sport']} | {e['event']} | {e.get('who', '')} | {'yes' if e.get('confirmed', True) else 'to confirm'} |")
out.append('\n## Gaps to close (weekly desk, step 6a)\n')
for g in m.get('gaps', []):
    out.append(f'- {g}')
(root / f'sources/{base}.md').write_text('\n'.join(out) + '\n')
print('written', len(out), 'lines')
