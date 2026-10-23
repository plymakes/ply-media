# From the Archive: the history series

Geoffry's brief (23 Oct 2026): posts that bring something from the history of Lebanese and Cypriot sport, researched in depth once a month, tracked in notes here on GitHub, looking old while staying attractive, **twice a week**.

## The rhythm

- **Both pages, every Tuesday and Thursday at 19:30** (Beirut/Cyprus time): one archive carousel per page per slot, so 2 a week on @sportswire.lb and 2 a week on @sportswire.cy. 19:30 sits 90 minutes after the 18:00 slot and 90 minutes before results start at 21:00. If a big live night needs the slot, move the archive post to 20:00 or the next day; never drop news for it.
- **Monthly history desk** on the 20th of each month (10:20): deep research for the whole of next month, then builds, checks and schedules every archive post for that month in Metricool, and writes the month's notes file. The first run (Mon 26 Oct 2026) covers November.
- Anything the monthly desk could not finish is listed as TODO in the month file; the Sunday weekly desk builds the TODOs for the coming week.

## What makes a good archive post

- **Anniversary first.** Prefer stories whose date falls in that week ("26 years ago this week"), then stories that echo current news (Lebanon in the 2026 Rugby League World Cup → their first World Cup in 2000), then evergreen classics.
- Named people and clubs, a clear moment (a final, a first, a record, a debut), and something that still matters today (the "then and now").
- Balance across sports, eras, clubs and genders over a month. Never take sides between local clubs; no politics, no war framing beyond the plain fact that a game was played or cancelled; nothing about deaths, scandals or court cases (those are AMBER at best and not what this series is for).
- No repeats: check `log.json` for the topic key before choosing.

## Proof (same rule as every post)

Every fact on the card and in the caption needs one tier-1 source (governing body, organiser, club) or two independent established outlets, written into the spec with URLs, then an independent fact-check and `tools/gate.py` READY. History has its own traps:
- Old scores and dates differ between sites. Prefer the organiser's own archive (FIFA/AFC/UEFA/FIBA/IOC/Olympics.com, World Athletics, the federation), then RSSSF and established newspapers' archives. Wikipedia is a lead only.
- "First", "only", "record" and "best ever" need a source that says it in those words.
- Counted anniversaries ("26 years ago") are arithmetic from the verified date: write the sum into the facts.
- Ages, attendances and goal times: only if a source gives them.

## The look

`"series": "archive"` in the spec sends it to `tools/archive.py` (rendered by the normal `python3 tools/render.py <spec>`): aged newsprint with grain and vignette, letterpress serif (Playfair Display), typewriter labels (Special Elite), body copy in Old Standard TT, sepia ink, the page colour dulled to an old print colour (LB oxblood, CY ochre). Headlines in this series are sentence case in serif.

Carousel, 4–6 slides, `end` last:
1. `cover`: kicker ("On this day · 29 October 2000" / "This week in 2000"), the year, headline, short deck, a stamp ("26 years ago"), and the photo if there is a rights-safe one.
2. `story`: 50–75 words with a pull number (up to 90 words without), first letter as a drop cap.
3. `ticket` (a match: competition, teams, score, date, venue, crowd) or `ledger` (by the numbers, max 6 rows).
4. `thennow`: what happened next / where it stands today.
5. `end`: "More from the archive every Tuesday and Thursday."

Sample: `tools/examples/lb-archive-sample.json` (layout only).

## Photos

Old photos are hard to clear, so the rule is narrow:
- **Wikimedia Commons** files under Public domain, CC0, CC BY or CC BY-SA, through `tools/archive_photo.py pick` (it reads the licence and author from the Commons file page itself and refuses anything else). Credit on the card ("PHOTO: <Author> / Wikimedia Commons, <Licence>", added automatically) and in the caption ("📸 <Author> / Wikimedia Commons, <Licence>").
- The **club's, federation's or organiser's own archive** photo, as for news (`tools/photos.py`), with `"series": "archive"` added to its sidecar.
- Never agency or wire photos, never screenshots of TV, never "found on Google".
- No photo is fine: the cover then runs the big year, stamp and headline, which is designed to stand alone.

## Notes kept here

- `YYYY-MM.md`: one file per month: the research (candidates with sources and what was confirmed), the chosen calendar per page, and the status of each post (built / checked / scheduled with Metricool id / TODO / dropped and why).
- `log.json`: every archive post ever made: topic key, page, publish date, year of the event, title, spec, Metricool id. The monthly desk reads it to avoid repeats and to balance sports and eras.
- `ideas.md`: the running backlog of leads per page with one source link each.
