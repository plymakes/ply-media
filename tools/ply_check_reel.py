#!/usr/bin/env python3
"""Check a finished Ply reel before it is shown or scheduled.
Usage: python3 ply_check_reel.py reel.mp4 [expected_seconds]
Checks 1080x1920, h264, yuv420p, ~30 fps, audio track, real sound at Reel loudness (every Ply Reel has sound), duration, size, black frames, leftover metadata,
and writes stills (hook 0.5 s, middle, last second) next to the file for a visual check."""
import json, subprocess, sys
from pathlib import Path

f = Path(sys.argv[1]); want = float(sys.argv[2]) if len(sys.argv) > 2 else None
p = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', str(f)],
                              capture_output=True, text=True, check=True).stdout)
v = next((s for s in p['streams'] if s['codec_type'] == 'video'), {}); a = [s for s in p['streams'] if s['codec_type'] == 'audio']
dur = float(p['format']['duration']); num, den = v.get('avg_frame_rate', '0/1').split('/')
fps = float(num) / float(den) if float(den) else 0; mb = int(p['format']['size']) / 1e6
tags = {k: val for k, val in (p['format'].get('tags') or {}).items() if k not in ('major_brand', 'minor_version', 'compatible_brands', 'encoder')}
lufs = None
if a:  # integrated loudness: a silent track (anullsrc) reads about -70 or -inf
    out = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(f), '-vn', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re as _re
    m = _re.findall(r'I:\s+(-?[\d.]+|-inf) LUFS', out); lufs = float(m[-1]) if m and m[-1] != '-inf' else -99.0
black = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(f), '-vf', 'blackdetect=d=0.3:pix_th=0.08', '-an', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr.count('black_start')
checks = [('1080x1920', v.get('width') == 1080 and v.get('height') == 1920, f"{v.get('width')}x{v.get('height')}"),
          ('h264 yuv420p', v.get('codec_name') == 'h264' and v.get('pix_fmt') == 'yuv420p', f"{v.get('codec_name')} {v.get('pix_fmt')}"),
          ('~30 fps', abs(fps - 30) < 0.5, f'{fps:.2f}'),
          ('audio track', bool(a), 'yes' if a else 'none'),
          ('sound, not silent (-18..-12 LUFS)', lufs is not None and -18 <= lufs <= -12, f'{lufs:.1f} LUFS' if lufs is not None else 'no audio: run tools/ply_sound.py'),
          ('duration', want is None or abs(dur - want) <= 0.5, f'{dur:.2f}s'),
          ('size < 100 MB', mb < 100, f'{mb:.1f} MB'),
          ('no black gaps', black == 0, f'{black} found'),
          ('no metadata (GPS/date)', not tags, ', '.join(tags) or 'clean')]
for name, ok, detail in checks: print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
for label, t in (('hook', 0.5), ('mid', dur / 2), ('end', max(dur - 1, 0))):
    out = f.with_name(f'{f.stem}-still-{label}.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(f), '-frames:v', '1', '-q:v', '3', str(out)], check=True)
    print('still:', out)
sys.exit(0 if all(ok for _, ok, _ in checks) else 1)
