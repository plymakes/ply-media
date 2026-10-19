#!/usr/bin/env python3
"""Commit, push and print commit-pinned image URLs for Metricool.

    python3 tools/publish.py "message" posts/lb/2026-10/x.png specs/2026-10-19/lb-x.json ...

- Stages the given paths (relative to the sportswire/ folder, plus its
  content-log.json), commits, rebases on origin/main and pushes with the
  session's GitHub access. Retries the rebase+push up to 3 times, because the
  Ply runs push to the same repo. Only ever stages files inside sportswire/.
- Prints one https://raw.githubusercontent.com/<repo>/<sha>/<path> URL per image
  and checks each one actually serves the image (retries for up to 90 s, since
  the raw CDN can lag a few seconds behind a push). Exit code 1 if any fail.
Never schedule with a /main/ URL: a later push could swap the picture.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / 'config.json').read_text())
REPO = CFG['repo']
SUBDIR = CFG.get('repo_subdir', '').strip('/')


def git(*args, check=True) -> str:
    r = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f'git {args[0]} failed:\n{r.stderr}{r.stdout}')
    return r.stdout.strip()


def remote() -> str:
    return f'https://github.com/{REPO}.git'


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    msg, paths = sys.argv[1], sys.argv[2:]
    for p in paths:
        if p.startswith(('/', '..')) or '..' in pathlib.PurePath(p).parts:
            sys.exit(f'refusing {p}: only paths inside the sportswire/ folder may be published')
    git('add', '--', *paths)
    if (ROOT / 'content-log.json').exists():
        git('add', '--', 'content-log.json')
    if git('diff', '--cached', '--name-only'):
        git('commit', '-q', '-m', msg)
    for attempt in range(3):
        git('pull', '-q', '--rebase', remote(), 'main')
        r = subprocess.run(['git', '-C', str(ROOT), 'push', '-q', remote(), 'HEAD:main'], capture_output=True, text=True)
        if r.returncode == 0:
            break
        time.sleep(5)
    else:
        sys.exit(f'git push failed after 3 tries:\n{r.stderr}{r.stdout}')
    sha = git('rev-parse', 'HEAD')
    rc = 0
    for p in paths:
        if not p.endswith(('.png', '.jpg', '.jpeg', '.mp4')):
            continue
        url = f'https://raw.githubusercontent.com/{REPO}/{sha}/{SUBDIR + "/" if SUBDIR else ""}{p}'
        ok = False
        for _ in range(18):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=15) as r:
                    ok = r.status == 200 and r.headers.get('Content-Length', '1') != '0'
            except Exception:
                ok = False
            if ok:
                break
            time.sleep(5)
        print(('OK   ' if ok else 'FAIL ') + url)
        rc |= 0 if ok else 1
    print(f'commit {sha}')
    return rc


if __name__ == '__main__':
    sys.exit(main())
