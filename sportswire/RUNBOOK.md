# SportsWire runbook

What each scheduled run does, step by step. The scheduled task's own instructions only say which desk to run; everything else lives here so it can be improved without touching the schedule.

## 0. Setup (every run)

1. Call the `add_repo` tool (owner `plymakes`, repo `ply-media`, access `push`), then `git clone --depth 50 https://github.com/plymakes/ply-media && cd ply-media/sportswire`. SportsWire lives only in this `sportswire/` folder; everything outside it belongs to Ply and is never read, changed or committed by a SportsWire run. Run every command from inside `sportswire/`. If the clone or a push is refused, stop before scheduling anything and say so at the top of the brief.
2. `python3 -c "import playwright"` (install with `pip install playwright --break-system-packages` only if that fails; Chromium is already in the image, never run `playwright install`).
3. Read `config.json`, `PLAYBOOK.md`, `brand/brand-guide.md`, `sources/lebanon.md`, `sources/cyprus.md`, `sources/spelling.md`, `corrections.md`, and `python3 tools/log.py recent --days 7`.
4. Metricool: `getBrandSettings`, find each page's brand by `networksData.instagramData` (`sportswire.lb`, `sportswire.cy`). Write the ids into `config.json` if they are missing. A page whose brand or Instagram isn't connected is skipped, and the brief says so in one line.
5. `getScheduledPosts` for both brands, today and tomorrow (each brand's own timezone), so nothing collides with what is already queued.
6. `TaskCreate` a short task list for the run.

## 1. Morning desk (about 09:00)

1. **Re-check yesterday.** For every GREEN post published in the last 36 hours, re-open its tier-1 source and confirm the key facts still stand (amended scores, overturned results, renamed players). Anything that changed → PLAYBOOK section 8 (corrections) first, before anything else.
2. **Sweep, per page.** Search the last 24 hours and today's schedule across the sources in `sources/<country>.md`, plus web search for Lebanese/Cypriot athletes abroad. Note candidate stories with their source links. Aim for 6–10 candidates per page.
3. **Pick.** Rank by: named local athlete or club > reachable confirmed reshare target > freshness > not already covered (`story_key`). Choose up to 4 per page for today, including a spotlight or explainer on at least three days a week (PLAYBOOK "What performs"). Drop anything RED. A quiet day can be one fixtures card plus one spotlight.
4. **Build each story** (subagents may build stories in parallel, one story each, but the fact-check in step 5 is always a different agent):
   - Gather sources; write every atomic fact with its URL(s) and tier into the spec (`specs/<date>/<page>-<slug>.json`, format in `tools/README.md`).
   - Choose the template and theme (alternate dark/light against the page's last post), write card text and caption in the house voice, alt text in `"alt"`.
   - `python3 tools/render.py <spec>`; fix and re-render until it prints `ok`.
   - Open every PNG with Read and check it word by word against the facts; then set `"visual_check": {"done": true, "notes": "…"}`.
5. **Independent fact-check.** Start a fresh agent per story (Agent tool, general-purpose), give it ONLY the card text and caption, and this instruction: *"Verify every factual claim in this sports news post from scratch using web search. Use official federation/league/club sources or established news outlets; ignore fan pages and aggregators except for cross-checking scores. For each claim answer CONFIRMED (with URL), WRONG (correct fact + URL) or UNVERIFIED. Check the spelling of every name against the governing body. Be strict: if you can't confirm it, it's UNVERIFIED."* Paste its per-claim verdicts into `"factcheck"`. Any WRONG → fix, re-render, re-check. Any UNVERIFIED → remove the claim or kill the story.
6. **Gate.** `python3 tools/gate.py <spec>` must print `READY`. Never bypass it; if it can't pass, kill the story with `python3 tools/log.py kill <spec> --reason "…"`.
7. **Publish.** `python3 tools/publish.py "<page> <date> <slug>" <images> <spec>` → commit-pinned URLs, all `OK`.
8. **Schedule** in Metricool (`createScheduledPost`, the page's blogId, its timezone):
   - Feed post: `providers: [{"network":"instagram"}]`, `media`: the pinned URLs in slide order, `mediaAltText`, `text`: the caption, `instagramData: {"type":"POST","collaborators":[…only for positive spotlights with a confirmed handle…],"showReelOnFeed":true,"isAiGenerated":false}`, `autoPublish: true`.
   - Story: `instagramData.type = "STORY"`, no text.
   - GREEN in `auto` mode → `"draft": false`. AMBER, or `review` mode → `"draft": true` (Geoffry publishes from the planner).
   - Times: today's free slots from `config.json` (or `getBestTimeToPostByNetwork` once the page has two weeks of data), never in the past, at least 60 minutes from any other post on that page.
9. **Log**: `python3 tools/log.py add <spec> --status scheduled|draft --when <ISO> --metricool-id <id> --planner-url <url> --urls <u1,u2>`, then `python3 tools/publish.py "log <date>" content-log.json`.
10. **Brief** (PLAYBOOK section 9): `PushNotification` with the one-line version, and the full brief as the final message.

## 2. Evening desk (about 22:15)

Same as the morning desk, but only for results that are **final** today (and anything big that broke this afternoon), for both pages:
- Group results of one competition into one `roundup` card; national-team games and big nights get their own `result` card.
- Schedule from 22:30, 30 minutes apart per page, max 3 per page.
- Games still in progress or finishing after 23:00 are left for the morning desk. Never post a live score as a result.
- Tomorrow's big fixture can get a `preview` Story at 22:30 if confirmed by the competition's official schedule.

## 3. Weekly desk (Sunday about 10:00)

1. Analytics for both brands for the last 7 days (Metricool analytics tools): per post reach, likes, comments, shares, saves; top three and bottom three per page; follower change.
2. Add 2–4 dated lessons to PLAYBOOK section 10 (what worked, what didn't, naming decisions).
3. Week-ahead per page: confirm the coming week's local fixtures and athlete events from official schedules; build a `fixtures` card per page and schedule it Monday 10:30.
4. Plan spotlights for the week (three per page): pick athletes or clubs with something happening and a confirmed handle; note them in the brief.
5. Refresh `sources/handles.json`: confirm any handle the week needed, mark dead ones.
6. Check the connections still work (a push succeeded this week, both Metricool brands present with Instagram connected). Anything failing goes at the top of the brief.
7. Weekly brief to Geoffry: numbers per page, top post, lessons, next week's plan, drafts waiting, any corrections.

## If something breaks
- Push fails → stop before scheduling anything; the brief says GitHub access needs fixing, with the error.
- Metricool error → don't retry blindly; leave the spec and image committed, log it as `killed` with the error, and brief.
- A source site blocks fetching → use another tier-1/2 source; never route around a block.
- Nothing verifiable → schedule nothing and say so. That's a good outcome, not a failure.
