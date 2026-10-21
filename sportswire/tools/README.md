# Newsroom tools

| Command | What it does |
|---|---|
| `python3 tools/render.py specs/<date>/<file>.json` | Renders the card(s) for a spec into `posts/` or `stories/`. Exit 2 = layout problem, fix the text and re-run. |
| `python3 tools/gate.py specs/<date>/<file>.json` | Pre-publish gate. Must print `READY` before anything is scheduled. |
| `python3 tools/publish.py "msg" <paths…>` | Commits, pushes, prints commit-pinned image URLs and checks they load. |
| `python3 tools/log.py add <spec> --status scheduled --when <ISO> --metricool-id <id> --urls <u1,u2>` | Adds the post to `content-log.json`. Also `log.py kill <spec> --reason "…"` and `log.py recent`. |

Setup in a fresh session: `pip install playwright --break-system-packages` is only needed if `import playwright` fails (Chromium is preinstalled at `/opt/pw-browsers`). Fonts ship in `tools/fonts/`, nothing to download.

Template previews (what each layout looks like): `brand/template-previews/`. Example specs: `tools/examples/` (never schedule them; they hold sample data).

## Spec format

One JSON file per post in `specs/YYYY-MM-DD/<page>-<slug>.json`.

```jsonc
{
  "page": "lb",                      // lb | cy
  "format": "post",                  // post (1080x1350) | story (1080x1920)
  "theme": "dark",                   // dark (ink) | light (bone). Alternate so the grid doesn't stack one colour.
  "date": "2026-10-19",              // publish date (Beirut/Nicosia)
  "event_date": "2026-10-18",        // when the thing happened / happens
  "slug": "riyadi-beat-sagesse",     // short, unique
  "story_key": "lbl-riyadi-sagesse-2026-10-18",  // same story = same key, stops duplicates across runs
  "light": "green",                  // green = auto-publish, amber = Metricool draft for Geoffry
  "template": "result",              // see below; or use "slides": [{template, card, theme?}, …] for a carousel
  "card": { … },                     // template fields, below
  "caption": "…\n\nSource: FIBA\n@club_handle #SportsWireLB #LebanonBasketball",
  "facts": [
    {"claim": "Al Riyadi beat Sagesse 88-80 on 18 Oct 2026 in Beirut",
     "sources": [{"url": "https://…", "tier": 1, "outlet": "FLBB"},
                 {"url": "https://…", "tier": 2, "outlet": "Asia-Basket"}]}
  ],
  "factcheck": {"status": "pass", "checked_at": "…", "claims": [{"claim": "…", "verdict": "CONFIRMED", "url": "https://…"}]},
  "visual_check": {"done": true, "notes": "read back every name and number"},
  "reshare": {"mention": ["riyadi_club"], "collaborators": []},
  "feature": false,                  // true for evergreen features (spotlights, explainers) about older events
  "sensitive_override": null         // one-line reason only when gate flags a word that is plainly not sensitive
}
```

Text rules for every card field: `*word*` = accent colour (use once or twice per card), `\n` = line break. Headlines are lowercased automatically and get a final full stop. Quotes are never lowercased.

Common card fields: `eyebrow` (string or list, joined with ·), `eyebrow_style` (`pill` | `outline`), `headline`, `deck`, `section` (top-right label), `footer` (bold line, bottom left) or `footnote` (muted line), `headline_lines` (max lines, default 4 post / 5 story).

### Templates

- **result**: one match. `home`/`away`: `{name, score, label?, crest?}`; `ours`: `home` | `away` | null (null for local derbies: stay neutral); `status` (e.g. `["Full time", "After extra time"]`); `periods`: `{title, labels, home, away}`; `highlight`: `{big, text}`.
- **roundup**: several results. `rows`: `[{home, home_score, away, away_score, home_crest?, away_crest?, ours?, note?}]` (max 5 on a post, 7 on a story); `status`.
- **news**: signings, appointments, call-ups, announcements, squad news. `entity`: `{crest?, title, sub}`; `rows`: `[{label, value}]` (max 4); `tiles` (small stats).
- **fixtures**: what's on. `groups`: `[{label: "Friday", items: [{home, away, time, note?} | {text, time}]}]`; use `footnote: "All times Cyprus"`.
- **spotlight**: athletes and medals. `people`: `[{name, meta, text, badge: {top, main, tone: gold|silver|bronze|accent}}]` (max 3); `tally`: `{label, items: [{value, label, tone}]}`.
- **stats**: big numbers. `tiles`: `[{value, unit?, label, sub?}]` (2–4).
- **standings**: league table. `columns`, `rows`: `[{pos?, code?, team, values, highlight?}]` (max 8 on a post), `cutline`: `{after, label}`, `next`: `{title, sub, big, bigsub}`.
- **preview**: countdown / next up. `big` (outlined number), `rows`: `[{label, value}]`.
- **quote**: always AMBER. `quote` (verbatim), `speaker`, `role`, `translated_from?`.
- **correction**: `label`, `before`, `wrong`, `right`, `rows`, `text`.
- **end**: closing slide for carousels and Reels: the page lockup, `headline` (e.g. "every lebanese result, *first*"), optional `deck` ("Follow @sportswire.lb").

### Carousels
Use `"slides": [{"template": …, "card": {…}, "theme"?: …}, …]` instead of `template`/`card`. 4–7 slides, the hook on slide 1, `end` last. Output: `posts/<page>/<YYYY-MM>/<date>-<slug>-01.png` … in order; schedule all URLs in `media`.

### Reels
`"format": "reel"` plus `slides`, each with a `dur` in seconds. Every slide builds in (blocks rise and fade in one after another, big numbers count up) and cuts to the next. Typographic only: no footage. Recipes:
- *Result in 10 seconds*: `preview` hook (big score number + one-line headline, 2–2.5 s) → `result` (3–4 s) → `stats` (2.5–3 s) → `end` (2 s).
- *Spotlight*: `preview` or `news` hook (name + the one fact) → `stats`/`spotlight` (3 s each, max 3) → `end`.
- *Explainer*: question hook → 3–5 `news`/`stats` slides answering it → `end` (max ~30 s).
- *Weekend in 60 seconds*: hook ("the weekend in 60 seconds") → one `result` or `roundup` per competition → `end`.
Output: `reels/<page>/<YYYY-MM>/<date>-<slug>.mp4` (1080×1920, 30 fps, silent AAC track), `…-cover.png`, and a 6-frame sheet in `build/` for the visual check. `reel_meta.cover_ms` goes into Metricool's `videoCoverMilliseconds`. Example: `tools/examples/lb-reel-result.json`; preview: `brand/template-previews/reel-result-sample-*`.

Crests: `brand/crests/<name>.png`. Only use files that exist there; add new club crests only from the club's own official site, as a PNG with transparent background, and note the source in `brand/crests/SOURCES.md`.
