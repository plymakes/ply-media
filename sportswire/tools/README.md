# Newsroom tools

| Command | What it does |
|---|---|
| `python3 tools/render.py specs/<date>/<file>.json` | Renders the card(s) for a spec into `posts/` or `stories/`. Exit 2 = layout problem, fix the text and re-run. |
| `python3 tools/gate.py specs/<date>/<file>.json` | Pre-publish gate. Must print `READY` before anything is scheduled. |
| `python3 tools/publish.py "msg" <paths…>` | Commits, pushes, prints commit-pinned image URLs and checks they load. |
| `python3 tools/log.py add <spec> --status scheduled --when <ISO> --metricool-id <id> --urls <u1,u2>` | Adds the post to `content-log.json`. Also `log.py kill <spec> --reason "…"` and `log.py recent`. |
| `python3 tools/crests.py add <slug> --url … --source-page … --name …` / `--wiki "<Article>"` | Adds a club crest (512 px PNG) to `brand/crests/`, origin in `index.json`. Then `crests.py sheet <slug>`, look, `crests.py ok <slug>`. `crests.py seed` fills the starter list; `crests.py list`. |
| `python3 tools/sweep.py today` · `week --days 42` · `coverage` · `check` (all with `--page lb|cy`); `python3 tools/mapdoc.py lb|cy` | Lebanon sports map (`sources/lebanon-sports.json`): every run's checklist of the top-20 sports, their live competitions, dated events, athletes and fast sources; the weeks ahead; which sports are overdue on @sportswire.lb; map validation. `mapdoc.py` regenerates the readable .md after the JSON changes. |
| `python3 tools/photos.py scan <page>` then `pick <n> --slug … --date … --page … --credit … --shows … --focus x,y` | Event photo from any source, credited (no agency photos): numbered candidate sheet in `build/photos/`, then the chosen one into `media/photos/<YYYY-MM>/` with a sidecar `.json` (source, credit, what it shows). `photos.py check <file>`. |

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

Text rules for every card field: `*word*` = accent colour (use once or twice per card), `\n` = line break. Headlines are kept as written (sentence case, capitalised names: clubs, athletes, countries) and get a final full stop. "A v B" / "A vs B" anywhere on a card becomes "A vs. B" with "vs." in the accent. `"crest"` takes a club slug from `brand/crests/` or a flag `"flag:<iso code>"` from `brand/flags/` (e.g. `flag:lb`, `flag:cy`, `flag:gb-eng`); fixtures items take `home_crest`/`away_crest` (or `crest` with `text`). The first slide's photo gets the biggest band the photo allows. Word limits (gate): headline 8, deck 12, about 30 per card.

Common card fields: `eyebrow` (string or list, joined with ·), `eyebrow_style` (`pill` | `outline`), `headline`, `deck`, `section` (top-right label), `footer` (bold line, bottom left) or `footnote` (muted line), `headline_lines` (max lines, default 4 post / 5 story), `photo`.

`photo`: `{"file": "media/photos/2026-10/2026-10-21-slug.jpg", "focus": [x, y]?, "credit": "…"?, "height": px?}` (focus and credit default to the photo's sidecar). Works on every template except `end`; the card turns dark, gets a hero band, an eyebrow pill and a credit line. In Reels the band is taller with a slow push-in. The renderer fails a photo it would have to enlarge more than 1.25×. Example: `tools/examples/lb-result-photo.json`, `tools/examples/lb-reel-photo.json`; previews in `brand/template-previews/`.

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
- **quiz** (interactive): `options`: `[{text, sub?, crest?, key?}]` (2–4, keys default A–D). Always followed in the same spec by its **answer** slide. Footer defaults to "Swipe for the answer →" (post) / "Tap for the answer →" (Story). Only the right option counts as a claim for the gate; the fact-checker still confirms every wrong option is wrong. Examples: `tools/examples/lb-quiz-sample.json` (carousel with a photo), `lb-quiz-story-sample.json` (two Stories).
- **answer**: the quiz's `options` repeated exactly, `correct` (the key), `explain` (one or two sentences of why). Footnote defaults to "How did you do? Tell us in the comments."
- **vote** (interactive): `options`: `[{name, meta?, text?, photo? | crest?, key?}]` (2–4 tiles; keys default 1–4), `photo_h?`. Footer defaults to "Vote in the comments: 1, 2, 3 or 4". Every stat on a tile is a fact. Example: `tools/examples/lb-vote-sample.json`.
- **matchup**: announce a game with two big logos: `home`/`away`: `{name, crest, label?}`, `big` (kick-off time, e.g. "20:30"), `status` (day · venue). Preview: `brand/template-previews/house-style-matchup.png`.
- **predict** (interactive): `home`/`away`: `{name, crest?, label?}` (scores show as "?"), `status` (day · time · venue). Footer defaults to "Drop your score in the comments". Example: `tools/examples/lb-predict-story-sample.json`.
- **end**: closing slide for carousels and Reels: the page lockup, `headline` (e.g. "every lebanese result, *first*"), optional `deck` ("Follow @sportswire.lb").

### Carousels
Use `"slides": [{"template": …, "card": {…}, "theme"?: …}, …]` instead of `template`/`card`. 4–7 slides, the hook on slide 1, `end` last. Output: `posts/<page>/<YYYY-MM>/<date>-<slug>-01.png` … in order; schedule all URLs in `media`.

### Reels
`"format": "reel"` plus `slides`, each with a `dur` in seconds. Every slide builds in (blocks rise and fade in one after another, big numbers count up) and cuts to the next. Typographic only: no footage. Recipes:
- *Result in 10 seconds*: `preview` hook (big score number + one-line headline, 2–2.5 s) → `result` (3–4 s) → `stats` (2.5–3 s) → `end` (2 s).
- *Spotlight*: `preview` or `news` hook (name + the one fact) → `stats`/`spotlight` (3 s each, max 3) → `end`.
- *Explainer*: question hook → 3–5 `news`/`stats` slides answering it → `end` (max ~30 s).
- *Weekend in 60 seconds*: hook ("the weekend in 60 seconds") → one `result` or `roundup` per competition → `end`.
**Sound: every Reel has sound.** The renderer generates an original soundtrack with `tools/sound.py` (whoosh and hit on every slide change) and muxes it in; choose `"sound": {"mood": "drive" | "bright" | "calm"}`. The gate rejects a Reel whose soundtrack is missing or too quiet.
Output: `reels/<page>/<YYYY-MM>/<date>-<slug>.mp4` (1080×1920, 30 fps, AAC stereo soundtrack), `…-cover.png`, and a 6-frame sheet in `build/` for the visual check. `reel_meta.cover_ms` goes into Metricool's `videoCoverMilliseconds`. Example: `tools/examples/lb-reel-result.json`; preview: `brand/template-previews/reel-result-sample-*`.

Crests: `brand/crests/<name>.png`, origin and check status in `brand/crests/index.json`. Add new ones with `tools/crests.py` (club's own site first, Wikipedia infobox logo second); the gate refuses a crest that hasn't been visually checked.
