# SportsWire runbook

What each scheduled run does, step by step. The scheduled task's own instructions only say which desk to run; everything else lives here so it can be improved without touching the schedule.

## 0. Setup (every run)

1. Call the `add_repo` tool (owner `plymakes`, repo `ply-media`, access `push`), then `git clone --depth 50 https://github.com/plymakes/ply-media && cd ply-media/sportswire`. SportsWire lives only in this `sportswire/` folder; everything outside it belongs to Ply and is never read, changed or committed by a SportsWire run. Run every command from inside `sportswire/`. If the clone or a push is refused, stop before scheduling anything and say so at the top of the brief.
2. `python3 -c "import playwright"` (install with `pip install playwright --break-system-packages` only if that fails; Chromium is already in the image, never run `playwright install`).
3. Read `config.json`, `PLAYBOOK.md`, `CAMPAIGN.md`, this week's `plans/<year>-W<week>.md` (ISO week), `brand/brand-guide.md`, `sources/lebanon.md`, `sources/cyprus.md`, `sources/spelling.md`, `corrections.md`, and `python3 tools/log.py recent --days 7`.
4. Metricool: `getBrandSettings`, find each page's brand by `networksData.instagramData` (`sportswire.lb`, `sportswire.cy`). Write the ids into `config.json` if they are missing. A page whose brand or Instagram isn't connected is skipped, and the brief says so in one line.
5. `getScheduledPosts` for both brands, today and tomorrow (each brand's own timezone), so nothing collides with what is already queued.
6. `TaskCreate` a short task list for the run.

## 1. Morning desk (about 09:00)

1. **Re-check yesterday.** For every GREEN post published in the last 36 hours, re-open its tier-1 source and confirm the key facts still stand (amended scores, overturned results, renamed players). Anything that changed → PLAYBOOK section 8 (corrections) first, before anything else.
2. **Sweep, per page.** Search the last 24 hours and today's schedule across the sources in `sources/<country>.md`, plus web search for Lebanese/Cypriot athletes abroad. Note candidate stories with their source links. Aim for 6–10 candidates per page.
3. **Pick.** Today's list per page = today's items from this week's plan (CAMPAIGN.md grid) + the best verified news. Rank news by: named local athlete or club > reachable confirmed reshare target > freshness > not already covered (`story_key`). About 2 feed items per page (max 4), plus Stories. A planned item whose facts can't be verified today is swapped for another campaign format (a spotlight, an explainer, a numbers card) or dropped, and the plan file is updated. Drop anything RED.
   - Reel days: at least 3 Reels per page per week (Mon "weekend in 60 seconds", a spotlight Reel, a result Reel on big nights). Build them with `"format": "reel"` (tools/README.md): hook slide first (the key fact in the first second), 8–15 s for news, up to 30 s for explainers, `end` slide last.
   - Carousels: `slides` with 4–7 cards, `end` slide last, for explainers, week-ahead and spotlights.
4. **Build each story** (subagents may build stories in parallel, one story each, but the fact-check in step 5 is always a different agent):
   - Gather sources; write every atomic fact with its URL(s) and tier into the spec (`specs/<date>/<page>-<slug>.json`, format in `tools/README.md`).
   - Choose the template and theme (alternate dark/light against the page's last post), write card text and caption in the house voice, alt text in `"alt"`.
   - `python3 tools/render.py <spec>`; fix and re-render until it prints `ok`.
   - Open every PNG with Read and check it word by word against the facts; then set `"visual_check": {"done": true, "notes": "…"}`. For a Reel, open the frames sheet (`reel_meta.frames_sheet`) and the cover PNG, and also set `"frames_checked": true`.
5. **Independent fact-check.** Start a fresh agent per story (Agent tool, general-purpose), give it ONLY the card text and caption, and this instruction: *"Verify every factual claim in this sports news post from scratch using web search. Use official federation/league/club sources or established news outlets; ignore fan pages and aggregators except for cross-checking scores. For each claim answer CONFIRMED (with URL), WRONG (correct fact + URL) or UNVERIFIED. Check the spelling of every name against the governing body. Be strict: if you can't confirm it, it's UNVERIFIED."* Paste its per-claim verdicts into `"factcheck"`. Any WRONG → fix, re-render, re-check. Any UNVERIFIED → remove the claim or kill the story.
6. **Gate.** `python3 tools/gate.py <spec>` must print `READY`. Never bypass it; if it can't pass, kill the story with `python3 tools/log.py kill <spec> --reason "…"`.
7. **Publish.** `python3 tools/publish.py "<page> <date> <slug>" <images> <spec>` → commit-pinned URLs, all `OK`.
8. **Schedule** in Metricool (`createScheduledPost`, the page's blogId, its timezone):
   - Feed post: `providers: [{"network":"instagram"}]`, `media`: the pinned URLs in slide order, `mediaAltText`, `text`: the caption, `instagramData: {"type":"POST","collaborators":[…only for positive spotlights with a confirmed handle…],"showReelOnFeed":true,"isAiGenerated":false}`, `autoPublish: true`.
   - Carousel: same as a feed post with every slide URL in `media`, in order.
   - Reel: `media`: [the pinned .mp4 URL], `instagramData: {"type":"REEL","showReelOnFeed":true,"collaborators":[…as above…],"isAiGenerated":false}`, `videoCoverMilliseconds`: `reel_meta.cover_ms`, caption as usual. No audio by default; Trial Reels (`"TRIAL_REEL"`) only once the page has 1,000 followers, and never with collaborators.
   - Story: `instagramData.type = "STORY"`, no text. Daily on matchdays: a `fixtures` Story ("Today"), and the day's main post as a story-format card.
   - GREEN in `auto` mode → `"draft": false`. AMBER, or `review` mode → `"draft": true` (Geoffry publishes from the planner).
   - Times: the plan's slot, or a free slot from `config.json` (`rhythm.slots`), never in the past, at least 90 minutes from any other feed post on that page. If the morning desk runs late, shift to the next free slot rather than stacking posts.
9. **Mark the plan**: tick the item in `plans/<year>-W<week>.md` (done / swapped / dropped, one line why).
10. **Log**: `python3 tools/log.py add <spec> --status scheduled|draft --when <ISO> --metricool-id <id> --planner-url <url> --urls <u1,u2>`, then `python3 tools/publish.py "log <date>" content-log.json`.
11. **Brief** (PLAYBOOK section 9): `PushNotification` with the one-line version, and the full brief as the final message.

## 2. Evening desk (about 22:15)

Same as the morning desk, but only for results that are **final** today (and anything big that broke this afternoon), for both pages:
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
6. Refresh `sources/handles.json`: confirm any handle the week needed, mark dead ones. When a page passes 1,000 followers, note in config that Trial Reels are on.
7. Check the connections still work (a push succeeded this week, both Metricool brands present with Instagram connected). Anything failing goes at the top of the brief.
8. **Weekly brief** to Geoffry: per page followers (and change), top post, progress against the CAMPAIGN.md targets, lessons, next week's highlights, drafts waiting, any corrections.

## If something breaks
- Push fails → stop before scheduling anything; the brief says GitHub access needs fixing, with the error.
- Metricool error → don't retry blindly; leave the spec and image committed, log it as `killed` with the error, and brief.
- A source site blocks fetching → use another tier-1/2 source; never route around a block.
- Nothing verifiable → schedule nothing and say so. That's a good outcome, not a failure.
