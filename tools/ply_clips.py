#!/usr/bin/env python3
"""Ply clip library. scan: index phone clips (ffprobe + 3x2 contact sheet each). md: rebuild library.md.
Usage: python3 ply_clips.py scan <clips folder> <library folder>
       python3 ply_clips.py md <library folder>
Originals are never changed. GPS is never read or looked up."""
import json, re, subprocess, sys
from pathlib import Path

EXT = {'.mp4', '.mov', '.m4v', '.mkv', '.webm', '.jpg', '.jpeg', '.png', '.heic'}

def probe(f):
    out = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', str(f)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def scan(src, lib_dir):
    lib_dir.mkdir(parents=True, exist_ok=True); (lib_dir / 'sheets').mkdir(exist_ok=True)
    lib_file = lib_dir / 'library.json'
    lib = json.loads(lib_file.read_text()) if lib_file.exists() else []
    known = {c['file'] for c in lib}; ids = {c['id'] for c in lib}; new = 0
    for f in sorted(p for p in Path(src).rglob('*') if p.suffix.lower() in EXT and not p.name.startswith('.')):
        f = f.resolve()
        if str(f) in known: continue
        try:
            p = probe(f); v = next((s for s in p['streams'] if s['codec_type'] == 'video'), {})
            rot = int(float((v.get('tags') or {}).get('rotate', 0) or next((d.get('rotation', 0) for d in v.get('side_data_list', []) if 'rotation' in d), 0)))
            w, h = (v.get('height'), v.get('width')) if abs(rot) % 180 == 90 else (v.get('width'), v.get('height'))
            photo = f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.heic'}
            dur = 0.0 if photo else float(p['format'].get('duration', 0) or 0)
            num, den = (v.get('avg_frame_rate') or '0/1').split('/'); fps = round(float(num) / float(den), 2) if float(den) else 0
            cid = re.sub(r'[^a-z0-9]+', '-', f.stem.lower()).strip('-') or 'clip'
            while cid in ids: cid += '-2'
            ids.add(cid); sheet = lib_dir / 'sheets' / f'{cid}.jpg'
            vf = 'scale=720:-2' if photo else f'fps=6/{max(dur, 1):.2f},scale=360:-2,tile=3x2'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(f), '-vf', vf, '-frames:v', '1', str(sheet)], check=True)
            tags = p['format'].get('tags') or {}
            lib.append({'id': cid, 'file': str(f), 'sheet': str(sheet), 'duration': round(dur, 1), 'width': w, 'height': h,
                        'orientation': 'portrait' if w and h and w < h else 'landscape' if w and h and w > h else 'square',
                        'fps': fps, 'audio': any(s['codec_type'] == 'audio' for s in p['streams']),
                        'date': tags.get('com.apple.quicktime.creationdate') or tags.get('creation_time'),
                        'tags': None, 'used': [], 'status': 'active'})
            new += 1
        except Exception as e:
            print(f'skipped {f.name}: {str(e).splitlines()[0] if str(e) else e}')
    lib_file.write_text(json.dumps(lib, indent=1, ensure_ascii=False))
    print(f'{new} new, {len(lib)} in library, {sum(1 for c in lib if not c["tags"])} to tag')
    md(lib_dir)

def md(lib_dir):
    lib = json.loads((lib_dir / 'library.json').read_text())
    rows = ['id | len | orient | date | what | product | colour | shot | flags | best_start | used']
    for c in sorted((c for c in lib if c['status'] == 'active'), key=lambda c: c.get('date') or '', reverse=True):
        t = c['tags'] or {}
        rows.append(' | '.join(str(x) for x in [c['id'], f"{c['duration']}s", c['orientation'], (c.get('date') or '')[:10],
                    t.get('what', '(untagged)'), t.get('product', ''), t.get('colour', ''), t.get('shot', ''),
                    ' '.join(t.get('flags', [])), t.get('best_start', ''), len(c['used'])]))
    (lib_dir / 'library.md').write_text('# Ply clip library\n\n' + '\n'.join(rows) + '\n')

if __name__ == '__main__':
    if len(sys.argv) >= 4 and sys.argv[1] == 'scan': scan(Path(sys.argv[2]), Path(sys.argv[3]))
    elif len(sys.argv) >= 3 and sys.argv[1] == 'md': md(Path(sys.argv[2]))
    else: print(__doc__)
