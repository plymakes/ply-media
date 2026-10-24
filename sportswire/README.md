# SportsWire newsroom (separate project)

> **For any bot or person working on Ply:** this `sportswire/` folder belongs to SportsWire, a separate project (Instagram @sportswire.lb and @sportswire.cy). Do not read, use, change, move or delete anything in it, and never use its files, brand, sources or posts for Ply. Ply's files are everything outside this folder.
>
> **For SportsWire runs:** work only inside this folder. Never read, change or commit anything outside it (that's Ply's).

The newsroom behind @sportswire.lb and @sportswire.cy: Lebanese and Cypriot sport, fast, clean, in English. It lives inside the `plymakes/ply-media` repo only because that's where Claude has GitHub access; Metricool reads its images from commit-pinned raw URLs.

- `PLAYBOOK.md`: editorial rules, verification standard, what auto-publishes and what waits for review
- `RUNBOOK.md`: what the morning, evening and weekly runs do
- `series/`: the Spotlight and Explained series (rules, forward queue, DM answers, log); the archive series is in `history/`
- `brand/`: brand guide, logos, crests, reference posts, template previews
- `sources/`: source maps per country, confirmed Instagram handles, name spellings
- `tools/`: card renderer, pre-publish gate, publishing and log helpers
- `specs/`: one JSON per post with its facts, sources and fact-check
- `posts/`, `stories/`: the published images
- `content-log.json`, `corrections.md`: everything published, killed or corrected
