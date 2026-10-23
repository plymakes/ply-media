# SportsWire runbook

What each scheduled run does, step by step. The scheduled message only says which desk to run; everything else lives here so it can be improved without touching the schedule. Runs happen inside Geoffry's SportsWire session, queued with `send_later` (how and why: `schedule/README.md`).

## 0. Setup (every run)

1. **Repo.** If `/home/claude/ply-media/sportswire` exists: `cd /home/claude/ply-media && git status --short` (commit or stash nothing outside `sportswire/`), then `git pull --rebase origin main && cd sportswire`. Otherwise call `add_repo` (owner `plymakes`, repo `ply-media`, access `push`; "already attached" is fine), then `git clone --depth 50 https://github.com/plymakes/ply-media /home/claude/ply-media && cd /home/claude/ply-media/sportswire`. SportsWire lives only in this `sportswire/` folder; everything outside it belongs to Ply and is never read, changed or committed by a SportsWire run. Run every command from inside `sportswire/`. If the clone or a push is refused, stop before scheduling anything and say so at the top of the brief.
2. `python3 -c "import playwright, numpy, scipy" && ffmpeg -version | head -1` (install what's missing with `pip install playwright numpy scipy --break-system-packages`; Chromium is already in the image, never run `playwright install`).
3. Read `config.json`, `PLAYBOOK.md`, `CAMPAIGN.md`, this week's `plans/<year>-W<week>.md` (ISO week), `brand/brand-guide.md`, `sources/lebanon.md`, `sources/cyprus.md`, `sources/spelling.md`, `corrections.md`, and `python3 tools/log.py recent --days 7`.
4. Metricool: `getBrandSettings`, find each page's brand by `networksData.instagramData` (`sportswire.lb`, `sportswire.cy`). Write the ids into `config.json` if they are missing. A page whose brand or Instagram isn't connected is skipped, and the brief says so in one line.
5. `getScheduledPosts` for both brands, today and tomorrow (each brand's own timezone), so nothing collides with what is already queued.
6. `TaskCreate` a short task list for the run.
7. **Top up the schedule** (`schedule/README.md`). `list_triggers`, then make sure every desk in the next 48 hours (morning 08:51, afternoon 15:50, evening 22:15, Beirut/Cyprus time) and the next Sunday weekly desk (11:52) has an enabled one-off task named as in that file, plus the next monthly history desk (the 20th at 10:20, section 6). Create each missing one with `send_later` (`at` in UTC, converted with `Asia/Nicosia`; `initiation: "human_schedule"`; message = the matching `schedule/<desk>.txt`, verbatim). Never create duplicates; never use `create_trigger`. Do this first, before the desk's own work, so a run that fails later can't break the chain.

## 1. Morning desk (about 09:00)

1. **Re-check yesterday.** For every GREEN post published in the last 36 hours, re-open its tier-1 source and confirm the key facts still stand (amended scores, overturned results, renamed players). Anything that changed → PLAYBOOK section 8 (corrections) first, before anything else.
2. **Sweep, per page.** Search the last 24 hours and today's schedule across the sources in `sources/<country>.md`, plus web search for Lebanese/Cypriot athletes abroad. Note candidate stories with their source links. Aim for 6–10 candidates per page.
3. **Pick.** Today's list per page = today's items from this week's plan (CAMPAIGN.md grid) + the best verified news. Rank news by: named local athlete or club > reachable confirmed reshare target > freshness > not already covered (`story_key`). About 2 feed items per page (max 4), plus Stories. A planned item whose facts can't be verified today is swapped for another campaign format (a spotlight, an explainer, a numbers card) or dropped, and the plan file is updated. Drop anything RED.
   - Reel days: at least 3 Reels per page per week (Mon "weekend in 60 seconds", a spotlight Reel, a result Reel on big nights). Build them with `"format": "reel"` (tools/README.md): hook slide first (the key fact in the first second), 8–15 s for news, up to 30 s for explainers, `end` slide last, and a `sound.mood`. Every Reel has sound; the gate checks it.
   - Carousels: `slides` with 4–7 cards, `end` slide last, for explainers, week-ahead and spotlights.
3b. **Event calendar** (PLAYBOOK 6, Timing). Write or update `events/<today>.json` (format in section 5) with every A and B event for both pages today, plus tomorrow's events that start before about 14:00. For each event, confirm the date and start time on the official source (competition, federation or club page; convert to Beirut/Cyprus time). If the start time can't be confirmed, keep `start_confirmed: false` and never print a time on a card.
   - **Previews:** A/B events today get a preview in today's 10:00 or 12:30 slot (or inside the "Today" fixtures card/Story for B). Events tomorrow before about 14:00 get their preview tonight at 18:00. Never schedule a preview inside the 3 hours before the start.
   - **Result desks:** for every A/B event today, queue a one-off result desk with `send_later` (`at` = expected end + 35 minutes, in UTC; `initiation: "human_schedule"`; `name`: `SportsWire result · <date> <short event name>`; message = `schedule/result.txt` with DATE, EVENT_ID and ATTEMPT filled in). Expected end: football start + 1 h 55 min, basketball start + 2 h 05 min, other sports from the official schedule. If the start time is unknown, use 22:00 Beirut/Cyprus. Group events of one competition that end within 45 minutes of each other into one desk (one roundup). At most 6 result desks a day across both pages. Write each returned `trigger_id` into the event. Result desks run in this session one after another, so if an evening desk is still running the result desk starts right after it.
4. **Build each story** (subagents may build stories in parallel, one story each, but the fact-check in step 5 is always a different agent):
   - Gather sources; write every atomic fact with its URL(s) and tier into the spec (`specs/<date>/<page>-<slug>.json`, format in `tools/README.md`).
   - Choose the template and theme (alternate dark/light against the page's last post), write card text and caption in the house voice, alt text in `"alt"`.
   - **Crests and photo** (PLAYBOOK, Images and rights). Add `crest` names for every club and national team on the card. Basketball clubs in FIBA competitions: FIBA's own team logo is the best source (on a FIBA game page find `assets.fiba.basketball/...logoflag--light--organisation_<id>...`, swap `w_48/f_auto/q_auto` for `w_512/f_png`). A missing crest: `python3 tools/crests.py add <slug> --url <logo on the club's own site> --source-page <site> --name "<Name>"` (football clubs in UEFA competitions: the UEFA logo `https://img.uefa.com/imgml/TP/teams/logos/240x240/<uefa club id>.png` with the UEFA club page as `--source-page`; Wikipedia lookups are off, see "Fetching pages"), then `python3 tools/crests.py sheet <slug>`, look, and `python3 tools/crests.py ok <slug>`. For a photo: find the club's or federation's own report/gallery for this event, `python3 tools/photos.py scan <that page>`, open `build/photos/candidates-sheet.jpg` (and the full file you like), and `python3 tools/photos.py pick <n> --slug <slug> --date <date> --page <lb|cy> --credit "<Club>" --shows "<what the page says it shows>" --focus <x,y>`. Then `"photo": {"file": "media/photos/…jpg"}` on the hook/main card and "📸 <Club>" in the caption. Sidebar images on a club page usually belong to other articles: use the article's own lead image or gallery. No compliant photo → leave it out. Commit the photo and its `.json` with the card.
   - `python3 tools/render.py <spec>`; fix and re-render until it prints `ok`.
   - Open every PNG with Read and check it word by word against the facts; then set `"visual_check": {"done": true, "notes": "…"}`. For a Reel, open the frames sheet (`reel_meta.frames_sheet`) and the cover PNG, and also set `"frames_checked": true`.
5. **Independent fact-check.** Start a fresh agent per story (Agent tool, general-purpose), give it ONLY the card text and caption, and this instruction: *"Verify every factual claim in this sports news post from scratch using web search. Use official federation/league/club sources or established news outlets; ignore fan pages and aggregators except for cross-checking scores. For each claim answer CONFIRMED (with URL), WRONG (correct fact + URL) or UNVERIFIED. Check the spelling of every name against the governing body. Be strict: if you can't confirm it, it's UNVERIFIED."* Paste its per-claim verdicts into `"factcheck"`. Any WRONG → fix, re-render, re-check. Any UNVERIFIED → remove the claim or kill the story.
6. **Gate.** `python3 tools/gate.py <spec>` must print `READY`. Never bypass it; if it can't pass, kill the story with `python3 tools/log.py kill <spec> --reason "…"`.
7. **Publish.** `python3 tools/publish.py "<page> <date> <slug>" <images> <spec>` → commit-pinned URLs, all `OK`.
8. **Schedule** in Metricool (`createScheduledPost`, the page's blogId, its timezone):
   - Feed post: `providers: [{"network":"instagram"}]`, `media`: the pinned URLs in slide order, `mediaAltText`, `text`: the caption, `instagramData: {"type":"POST","collaborators":[…only for positive spotlights with a confirmed handle…],"showReelOnFeed":true,"isAiGenerated":false}`, `autoPublish: true`.
   - Carousel: same as a feed post with every slide URL in `media`, in order.
   - Reel: `media`: [the pinned .mp4 URL], `instagramData: {"type":"REEL","showReelOnFeed":true,"collaborators":[…as above…],"isAiGenerated":false}`, `videoCoverMilliseconds`: `reel_meta.cover_ms`, caption as usual. The soundtrack is already in the video (every Reel has sound); don't add `audioConfiguration`. Trial Reels (`"TRIAL_REEL"`) only once the page has 1,000 followers, and never with collaborators.
   - Story: `instagramData.type = "STORY"`, no text. Daily on matchdays: a `fixtures` Story ("Today"), and the day's main post as a story-format card.
   - GREEN in `auto` mode → `"draft": false`. AMBER, or `review` mode → `"draft": true` (Geoffry publishes from the planner).
   - Times: the plan's slot, or a free slot from `config.json` (`rhythm.slots`), never in the past, at least 90 minutes from any other feed post on that page. If the morning desk runs late, shift to the next free slot rather than stacking posts.
9. **Mark the plan**: tick the item in `plans/<year>-W<week>.md` (done / swapped / dropped, one line why).
10. **Log**: `python3 tools/log.py add <spec> --status scheduled|draft --when <ISO> --metricool-id <id> --planner-url <url> --urls <u1,u2>`, then `python3 tools/publish.py "log <date>" content-log.json`.
11. **Brief** (PLAYBOOK section 9): `PushNotification` with the one-line version, and the full brief as the final message.

## 1b. Afternoon desk (about 15:50)

A shorter morning desk for timeliness: sweep breaking news since the morning desk (signings, call-ups, appointments, announcements), check `events/<today>.json` for new or changed events (moved kick-offs, added games) and fix them, create result desks for events that don't have one, and schedule previews for tomorrow's early events at 18:00. Same verification, gate and publish steps. At most 2 new feed posts per page.

## 2. Evening desk (about 22:15)

Same as the morning desk, but only for results that are **final** today and **not already handled by a result desk** (check `events/<today>.json`: skip events whose result is `posted`, or whose result desk is still due to run), for both pages:
- Group results of one competition into one `roundup` card; national-team games and big nights get their own `result` card.
- Schedule from 22:30, 30 minutes apart per page, max 3 per page.
- Games still in progress or finishing after 23:00 are left for the morning desk. Never post a live score as a result.
- Tomorrow's big fixture can get a `preview` Story at 22:30 if confirmed by the competition's official schedule.

## 3. Weekly desk (Sunday about 11:50)

1. **Numbers.** For each page, pull the last 7 days from Metricool (`getAnalyticsDataByMetrics`, metric ids in CAMPAIGN.md section 10) and append one entry per page to `growth-log.json` (week, followers, gained, lost, reach, views, interactions, shares, saves, Reels views, posts and Reels published). The first run records the baseline.
2. **Rank the week's posts** per page by reach and by shares + saves (Metricool `posts` and `reels` connectors); name the top and bottom three.
3. **Lessons.** Add 2–4 dated lines to PLAYBOOK section 10 (what worked, what didn't, naming decisions), and adjust next week's format mix toward what worked (CAMPAIGN.md section 10).
4. **Next week's plan.** Write `plans/<year>-W<next week>.md` in the same table format as the current one: for each page and day, the campaign items from the CAMPAIGN.md grid filled with real fixtures and tentpoles, each with the official source to verify and a confirmed reshare target. At least three spotlights, three Reels and two carousels per page.
5. **Week-ahead content.** Build Monday's "weekend in 60 seconds" Reel and the "week ahead" fixtures carousel per page (verified like everything else) and schedule them for Monday 10:00 and 12:30.
6. Refresh `sources/handles.json`: confirm any handle the week needed, mark dead ones. Fill missing crests for any club that appeared this week from official logos (`tools/crests.py add <slug> --url … --source-page …`; Wikipedia lookups are off), then `tools/crests.py sheet`, look, `tools/crests.py ok <slugs>` for the right ones and `tools/crests.py rm <slugs>` for wrong ones (kit pictures, old crests, wordmarks too small for a tile). When a page passes 1,000 followers, note in config that Trial Reels are on.
6b. **Archive TODOs.** If `history/<this month>.md` (or next month's) lists archive posts still marked TODO for the coming Tuesday or Thursday, build, check and schedule them now (section 6, steps 4–7).
7. Check the connections still work (a push succeeded this week, both Metricool brands present with Instagram connected). Anything failing goes at the top of the brief.
8. **Weekly brief** to Geoffry: per page followers (and change), top post, progress against the CAMPAIGN.md targets, lessons, next week's highlights, drafts waiting, any corrections.

## 4. Result desk (one-off, per event)

A result desk is a one-off message into this session, queued with `send_later` by the morning or afternoon desk (never `create_trigger`). Its job: post the result of one event (or one group of events) as soon as it is final and verified.

1. Setup as in section 0 (steps 1–5), but read only `config.json`, `PLAYBOOK.md`, `sources/spelling.md`, `sources/handles.json` and `events/<date>.json`.
2. Find the event by id. If its result is already `posted`, stop.
3. Look for a **final** result (full time, after extra time/penalties) in the fast places first, as PLAYBOOK 4.3 allows: both clubs' and the organiser's X, Threads and Facebook posts (search for them; Instagram through the built-in browser if available), official live stats, Sofascore/Flashscore/Asia-Basket, then fast tier 2 outlets (elsport, MTV Lebanon sport, Annahar; Philenews, CNA for Cyprus). Club websites last. Live or half-time scores never count. If it's not final yet: queue **one** follow-up result desk 40 minutes later with `send_later` (same message, attempt number + 1; at most 2 follow-ups), write its id into the event, and stop. After the last attempt, set the result to `handover` so the evening or next morning desk takes it.
4. Build the result post exactly as in section 1 steps 4–8: facts with sources, `result` card (or `roundup`), plus a result Reel for an A event we won or a historic one (every Reel has sound), independent fact-check, gate READY, publish.
5. Schedule it in Metricool for **now + 3 minutes** (never in the past), `autoPublish: true` (or `draft: true` if AMBER or in review mode).
6. Set the event's result to `posted` (with the spec path and Metricool id), log it in `content-log.json`, push. PushNotification: "Posted: <result> on <page>".

**Result desk message:** `schedule/result.txt`, with DATE, EVENT_ID and ATTEMPT filled in.

## 5. Event calendar format

`events/<YYYY-MM-DD>.json`:
```json
{"date": "2026-10-21", "events": [{
  "id": "lb-dubai-final", "page": "lb", "priority": "A", "sport": "basketball",
  "title": "Al Riyadi v Antonine, Shabab Al Ahli Dubai tournament final",
  "start_local": null, "start_confirmed": false, "expected_end_local": "2026-10-21T21:45+03:00",
  "venue": "Sheikh Saeed bin Maktoum Hall, Dubai",
  "result_sources": ["https://www.riyadi.com/", "https://www.annahar.com/sports/basketball"],
  "preview": {"status": "posted|scheduled|none", "spec": "specs/...json", "metricool_id": 0, "when": "..."},
  "result_desk": {"trigger_ids": ["trig_..."], "next_run": "..."},
  "result": {"status": "pending|posted|handover|cancelled", "spec": null, "metricool_id": null}
}]}
```

## 6. History desk ("From the Archive", monthly, the 20th about 10:20)

The series rules, look and photo policy are in `history/README.md`; read it first. One run covers the whole of next month: every Tuesday and Thursday, 19:30, one archive carousel per page.

1. **Slots.** List next month's Tuesdays and Thursdays. For each page that is the number of posts to make (8–10). Read `history/log.json` (no repeats; balance sports, eras, clubs, men's and women's sport) and `history/ideas.md`.
2. **Research** (subagents may research in parallel, one per page): for each slot, find a story whose anniversary falls that week if possible, otherwise one that echoes current news, otherwise an evergreen classic. Collect every atomic fact with source URLs and tiers to the PLAYBOOK section 4 standard (organiser archives first; Wikipedia only as a lead), plus a rights-safe photo option or "none". Write it all into `history/<YYYY-MM>.md`: the candidates, what was confirmed and what wasn't, and the chosen calendar per page. Add good leads you didn't use to `history/ideas.md`.
3. **Photos.** `python3 tools/archive_photo.py info "File:…"` then `pick` (Commons, licence read from the file page; refused unless PD/CC0/CC BY/CC BY-SA), or `tools/photos.py` for a club/federation archive photo plus `"series": "archive"` in its sidecar. Look at each photo before using it. No safe photo → cover without one.
4. **Build** each post as a spec `specs/<publish date>/<page>-archive-<slug>.json` with `"series": "archive"`, `"archive": {"issue": <n>}` (running number per page, from the log), `"format": "post"`, `"light": "green"`, the `slides` (cover, story, ticket or ledger, thennow, end), caption (hook line, 2–3 short paragraphs, a question, "📸 …" if there is a photo, "Source: …", mentions, `#SportsWireLB`/`#SportsWireCY` and `#FromTheArchive`), alt text per slide, and the facts with sources (anniversary arithmetic written out). `python3 tools/render.py <spec>`; fix until `ok`; open every PNG and check it word by word; set `visual_check`.
5. **Fact-check** each post with a fresh agent that sees only the slide text and caption (RUNBOOK 1, step 5 wording, plus: "these are historical facts; prefer the organiser's archive; Wikipedia alone is UNVERIFIED"). WRONG → fix, re-render, re-check. UNVERIFIED → cut it or swap the story. Then `python3 tools/gate.py <spec>` must print READY.
6. **Publish and schedule**: `python3 tools/publish.py …` then `createScheduledPost` per post for its Tuesday/Thursday at 19:30, `autoPublish: true`, `draft: false` (GREEN). Check the day first with `getScheduledPosts`: keep 90 minutes from any other feed post (move to 20:00 if needed).
7. **Track**: `python3 tools/log.py add …` per post, append each to `history/log.json` (key, page, publish date, event year, title, spec, Metricool id), and mark it in the month file (scheduled + id). Anything not finished stays `TODO` in the month file for the weekly desk.
8. **Next run**: queue next month's history desk with `send_later` (the 20th at 10:20 Asia/Nicosia, converted to UTC; name `SportsWire history desk · <Mon YYYY>`; message `schedule/history.txt` verbatim), unless one already exists.
9. **Brief** (under 120 words): per page the month's archive calendar (date, year, headline), anything dropped and why, TODOs left. PushNotification with the one-line version.

## If something breaks
- Push fails → stop before scheduling anything; the brief says GitHub access needs fixing, with the error.
- Metricool error → don't retry blindly; leave the spec and image committed, log it as `killed` with the error, and brief.
- A source site blocks fetching → use another tier-1/2 source; never route around a block.

## Fetching pages (so runs never stall)
- Scheduled runs are set to approve their own actions automatically; nothing waits for Geoffry. Web pages are read with WebSearch and WebFetch.
- **Search first, then fetch.** Find the page with WebSearch and fetch the URL from the results. A URL typed from memory or edited by hand may be refused.
- **Long URLs** (Arabic slugs are percent-encoded and can exceed the fetch limit): use the short form many sites accept (e.g. `https://www.annahar.com/sports/358828/` without the slug), a different link to the same article from search results, or another outlet reporting the same facts.
- **Sites that refuse automated fetching** (seen so far: philenews.com / in-cyprus, the961.com, lorientlejour.com sport, Transfermarkt, Kathimerini Cyprus, some Arabic portals): these are refused by the network for everyone; never use another tool, a cache, a mirror or a proxy to get around it. Search snippets can point you to the story; confirm the facts on a site that opens.
- **robots.txt counts.** A site or API whose robots.txt disallows automated access is refused, even if curl would get through: never curl it instead. Known: api.the-afc.com (AFC data API) is disallowed; www.the-afc.com is allowed; match.uefa.com is allowed. Wikimedia disallows `/w/` (the API) but allows `/wiki/` pages and upload.wikimedia.org files: `tools/archive_photo.py` reads only those, and `tools/crests.py --wiki/find/seed` is switched off (use official logos with `--url`).
- Instagram itself can't be fetched: confirm handles through the organisation's own website or `sources/handles.json`.
- Nothing verifiable → schedule nothing and say so. That's a good outcome, not a failure.
