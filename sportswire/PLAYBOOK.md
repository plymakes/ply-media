# SportsWire newsroom playbook

This repository is the newsroom for two faceless, English-language Instagram sports news pages run by Geoffry:

| Page | Instagram | Covers |
|---|---|---|
| SportsWire LB | @sportswire.lb | Lebanese sport, and Lebanese athletes anywhere in the world |
| SportsWire CY | @sportswire.cy | Cypriot sport, and Cypriot athletes anywhere in the world |

Scheduled runs find the news, verify it, design the card, publish through Metricool and log everything here. This newsroom lives in the `sportswire/` folder of the public `plymakes/ply-media` repo (Geoffry's decision, 19 Oct 2026); the rest of that repo is Ply's and is never touched. Images in `posts/` and `stories/` are public on purpose: Metricool reads them from commit-pinned raw URLs.

Read these before every run, in this order: `config.json`, this file, `brand/brand-guide.md`, `sources/lebanon.md` and `sources/cyprus.md`, `sources/handles.json`, the last 7 days of `content-log.json`, and `corrections.md`.

---

## 1. The one rule

**Being late is fine. Being wrong is not.** These pages publish news about real, named people. A story that cannot be verified to the standard below is not posted, however big it looks. Missing a story costs nothing; a wrong name, score or claim costs the page its credibility and can hurt a real person.

When in doubt: do not post, and mention it in the brief.

---

## 2. What we cover

Coverage first, not trophy-chasing (Geoffry, 26 Aug 2026). These are coverage pages that follow the whole scene.

- Anything involving a named Lebanese or Cypriot athlete, at home or abroad, whatever the result: wins, losses, draws, debuts, call-ups, personal bests, records, brave exits, farewells.
- Local clubs and national teams: results (including defeats), signings that are officially announced, milestones, previews, squad lists.
- Young players breaking through; a Lebanese or Cypriot name appearing in a bigger foreign league or competition.
- Quiet days: who plays today, who travels, fixtures and standings.
- Global sport only if it is enormous or has a direct local thread.

Priorities. Lebanon: basketball first, then football, then everything else (rugby league, athletics, swimming, skiing, combat sports, weightlifting, tennis/padel, motorsport, futsal, volleyball). Cyprus: football first (league, cup, national team, European ties), then athletics, sailing, shooting, basketball, volleyball, tennis, swimming, cycling, motorsport.

Each page posts only its own country. A story with both a Lebanese and a Cypriot angle can run on both pages, written separately.

---

## 3. Sources

Full source maps: `sources/lebanon.md`, `sources/cyprus.md`.

- **Tier 1, primary:** the federation, league or competition official site or verified official account (FIBA, AFC, UEFA, FIFA, CFA, FLBB, LFA, World Athletics, official results platforms), and the club's or athlete's own verified account for news about themselves (signings, injuries they announce, retirements, **and the final score of their own match**). "Account" means any of the club's verified channels: Instagram, X, Facebook, Threads, YouTube or website. Official live-stats pages (FIBA LiveStats, Genius Sports, the organiser's live centre) are tier 1 for a score once they show the game as final.
- **Tier 2, established media:** named news outlets with editorial standards (e.g. Cyprus Mail, in-cyprus/Philenews, CNA, L'Orient Today, Annahar, elsport, MTV Lebanon sport, Arab News, NNA, Reuters, AP, AFP). Data services (Flashscore, Sofascore, Soccerway, Asia-Basket) count as tier 2 for scores and statistics only.
- **Tier 3, never enough alone:** fan pages, aggregator Instagram/X/Facebook accounts, forums, blogs, "reports say", transfer-rumour sites, Transfermarkt for transfer completion, AI-generated summaries, Wikipedia. Use them only as tips to go and find a tier 1 or 2 source.

Two sources are **independent** only if neither one is citing or copying the other. Two outlets repeating the same club statement are one source (the statement), which is fine because a club statement about itself is tier 1.

---

## 4. Verification standard (every post, no exceptions)

### 4.1 Break the story into atomic facts
Every name, club, competition, score, date, time, venue, number, record, ranking, age and quote that appears on the card or in the caption is a separate fact.

### 4.2 Each fact must be confirmed by
- one tier 1 source, **or**
- two independent tier 2 sources that agree exactly.

Write the source URL against every fact in the spec file (`specs/…json`, see section 7). A fact without a URL is removed from the post.

### 4.3 Specific checks
- **Scores and results:** only once the match is officially over (full time, after extra time/penalties). Never post live or half-time scores as results. Official websites are often hours behind, so don't wait for a write-up (Geoffry, 21 Oct 2026). A final score is confirmed by **any one** of:
  - a full-time post from either club's verified account (any channel) or from the organiser/competition, or an official live-stats page showing it as final;
  - a data service (Sofascore, Flashscore, Asia-Basket) showing the game as finished, plus one tier 2 outlet with the same score;
  - two independent tier 2 outlets with the same score.
  If any source you have seen gives a different score, wait for a second official source or the box score (the Lebanon24 "97-69" flash for a 98-69 semi-final, 20 Oct 2026). The winner and score only: scorers, stats and records still need their own sources. A link Geoffry sends in chat to an official post counts as that post.
  Instagram blocks automated fetching: find club posts through X, Threads or Facebook (search results often show them), or read Instagram in the built-in browser on Geoffry's Mac when it is available.
- **Names:** spell every person and club exactly as the governing body does (FIBA, AFC, UEFA, World Athletics, the federation). Use `sources/spelling.md`; add new names there with the source of the spelling. Never guess a transliteration.
- **Dates and times:** convert to the page's local time (Lebanon: Asia/Beirut, Cyprus: Asia/Nicosia) and say "local time" when it matters.
- **Records and "firsts":** only if the governing body or two tier 2 outlets explicitly call it a record or a first. Never infer one.
- **Transfers and signings:** only when officially announced by the buying club, the selling club or the league. "Agreed", "close", "in talks", "set to" never run.
- **Coach changes:** only on official club announcement.
- **Quotes:** only verbatim, from a primary source (official channel, video, press conference transcript) or a tier 2 outlet quoting directly. Translate faithfully and say so ("translated from Greek/Arabic"). Never paraphrase into quote marks.
- **Tables and rounds:** before saying "after N rounds", "top after…" or "game in hand", open the official fixture list and confirm the round is complete and which games are still to come (a round often spans Friday to Monday). "Game in hand" only for a match that was postponed, never for one still scheduled in the same round. Re-open the table right before scheduling: a later game may already have changed it.
- **Ages and numbers:** recompute from the source; do not copy derived numbers from tier 3.
- **Freshness:** the event happened in the last 36 hours, or is upcoming. Older stories only as features clearly framed as such. Check the log so the same story is not posted twice.

### 4.4 Independent fact-check (separate agent)
After the card text and caption are written, start a **separate agent that has not seen your sources**. Give it only the final card text and caption, and ask it to verify every factual claim from scratch with web search against tier 1/2 sources, and to answer per claim: CONFIRMED (with URL), WRONG (with the correct fact and URL) or UNVERIFIED. Then:
- all CONFIRMED → continue;
- any WRONG → fix the fact, re-render, and run the check again;
- any UNVERIFIED → drop that claim from the post, or kill the story.
Record the result in the spec file (`factcheck`).

### 4.5 Visual check
Open every rendered PNG and read it back word by word against the spec: names, scores, dates, the right crest on the right club, a photo that shows what its source says (and nothing awkward), no text clipped or overflowing, nothing overlapping. A post is never scheduled without this check.

---

## 5. Traffic light: what auto-publishes and what waits for Geoffry

`config.json` has `"mode"`. In `"auto"` mode green stories publish automatically. In `"review"` mode every post is created as a Metricool draft.

- **GREEN, auto-publish** (passes section 4 completely): final results, fixtures, standings, squad lists, officially announced signings and appointments, call-ups, personal bests and records confirmed by the governing body, previews, schedules, milestones.
- **AMBER, Metricool draft for Geoffry** (`"draft": true`, listed in the brief): deaths and obituaries; injuries and health; arrests, court cases, doping, bans, disciplinary decisions, allegations; crowd trouble, violence, racism incidents; anything that criticises a named person beyond describing a sporting result; anything touching politics, religion, war, sectarian or communal tension, or the Cyprus problem / clubs from the north; stories about athletes under 18 beyond a plain result published by their federation; any quote; any story with only one tier 1 source that is a social-media post rather than an official site.
- **RED, never post:** rumours and "reportedly" stories; unconfirmed transfers; betting odds, tips or gambling promotion; private life (relationships, family, money); anything sourced only from tier 3; graphic images; anything that would need a photo we do not have the rights to; anything satirical.

Metricool's approval workflow is not on the Starter plan, so AMBER items are created with `"draft": true` and Geoffry publishes them from the Metricool planner.

---

## 6. Rhythm and campaign

The current growth campaign, its formats, weekly grid, tentpoles and targets are in **`CAMPAIGN.md`**; this week's concrete plan is in `plans/<year>-W<week>.md`. In short:

- **Morning desk (daily, about 09:00):** re-check recent posts, sweep the news, then build today's news posts **and** today's planned campaign items for both pages, scheduled into the slots in `config.json` (10:00, 12:30, 18:00).
- **Afternoon desk (daily, about 15:50):** breaking news since the morning, new or changed events, previews for tomorrow-morning events, result desks for anything new.
- **Result desks (one-off, per A/B event):** run about 30–40 minutes after each event's expected end and post the result straight away.
- **Evening desk (daily, about 22:15):** the catch-all for final results not covered by a result desk, from 22:30, at least 30 minutes apart per page.
- **Weekly desk (Sunday, about 11:50):** analytics into `growth-log.json`, lessons into section 10, next week's plan, week-ahead content.

Volume per page: about 2 feed items a day (at most 4), at least 3 Reels and 2 carousels a week, Stories daily on matchdays. Never two feed posts on one page within 90 minutes (30 on results nights). Group several results of one competition into one `roundup` card. Quality beats volume every time: an empty slot is better than a weak or unverified post.

### Timing: before and after every event (Geoffry, 21 Oct 2026)
We are a news page, so timing is part of being right.
- **Before:** every A or B event (below) gets a preview **on the morning of the event day** (10:00 or 12:30 slot), or **the evening before** (18:00) when it starts before about 14:00. Never in the last 3 hours before tip-off or kick-off.
- **After, always:** the result goes out **as soon as it is final and verified**, normally within 30–60 minutes of the final whistle, through a dedicated result desk scheduled for that event (RUNBOOK section 4). Late games are still posted that night; nothing waits for the next morning unless the result can't be verified.
- **Priority A:** national teams, finals, derbies, European nights, medals, a Lebanese or Cypriot athlete in a major final. Preview + result card, and a result Reel when we win or it's historic.
- **Priority B:** top-flight league games of the big clubs, other Lebanese/Cypriot teams in international tournaments. Preview inside the day's fixtures card or Story; result card or roundup.
- **Priority C:** everything else; covered by roundups in the evening desk.
- Every day's events and their before/after posts are tracked in `events/<date>.json`.

The step-by-step for each run is in `RUNBOOK.md`.

---

## 7. Making a post

1. **Spec.** Write `specs/YYYY-MM-DD/<page>-<slug>.json` (format in `tools/README.md`): page, template, card text fields, caption, facts with source URLs, traffic light, reshare target, fact-check result.
2. **Render.** `python3 tools/render.py specs/YYYY-MM-DD/<file>.json` writes `posts/<page>/YYYY-MM/<date>-<slug>.png` (feed, 1080×1350; carousels get `-01`, `-02`…), `stories/<page>/…` (1080×1920) or, for `"format": "reel"`, `reels/<page>/…/<slug>.mp4` plus a cover PNG and a frames sheet in `build/`. Only the templates in `tools/render.py` are used, so every post matches the brand. Do not hand-write HTML or invent new layouts; if a story needs a layout that does not exist, use the closest template and mention it in the brief.
3. **Look** at every PNG, and for Reels the frames sheet and the cover (section 4.5).
4. **Commit and push** to `main`.
5. **Schedule** in Metricool with the commit-pinned URL `https://raw.githubusercontent.com/plymakes/ply-media/<commit-sha>/sportswire/<path>` (printed by `tools/publish.py`) (never `/main/`, so a later change can't swap the image). Check the URL returns the image before scheduling.
6. **Log** in `content-log.json` and push again.

### Captions
House voice (see `brand/brand-guide.md` and the captions in `brand/reference/`): warm, confident, short sentences, facts first.
- Line 1: the hook, with the key fact (score, name, number). No clickbait, no ALL CAPS, no "BREAKING" unless it truly is.
- Then two or three short paragraphs: what happened, the numbers, what's next (with local time).
- One flag emoji as the sign-off (🇱🇧 / 🇨🇾); at most one or two other emojis; none on sad news.
- A source line: `Source: <official body or outlet>` (gate checks for it).
- Mention the club or athlete with their confirmed handle from `sources/handles.json` (only confirmed handles; never guess a handle).
- Write the words people search into the caption itself ("Lebanese basketball", "Cyprus League", full club and athlete names). Then at most 3 hashtags (the page tag plus one or two topic tags, e.g. `#SportsWireLB #LebaneseBasketball`); hashtags no longer add reach.
- End most captions with one genuine, good-natured question ("who was your player of the night?"). Never engagement bait ("comment YES", "tag 3 friends") and never on sad news.
- Partisan for the country ("we" for the national team), neutral between local clubs (never "we" for a club). Report defeats plainly and kindly. No opinions about referees, officials or players.
- Language: English; a word of Lebanese Arabic or Greek only for warmth, never for facts. Names in their official English spelling.

### Reshare targets
For every post, identify the athlete, club or federation most likely to reshare it, with a handle confirmed in `sources/handles.json`. Mention them in the caption. For positive spotlight posts about one athlete or club, also add them as an Instagram collaborator (`instagramData.collaborators`); at most one collaborator per post, never on AMBER posts or defeats.

### Images and rights
Posts and Reels carry **club crests** and, where a compliant one exists, an **official event photo** (Geoffry, 21 Oct 2026: "they look more professional"). Runs find, choose and place them on their own.

- **Crests** (`brand/crests/`, origin in `brand/crests/index.json`): on every score panel, result row and entity where a club or national team appears. Source: the club's own website first, its Wikipedia infobox logo second (`tools/crests.py`). A new crest is used only after it has been looked at on the contact sheet and marked checked (the gate enforces this). Editorial identification only: never altered, recoloured or used as decoration.
- **Photos: official club, federation, league or competition media only, always credited** (Geoffry's choice, 21 Oct 2026). That means the club's or federation's own website, press release or official gallery. Credit on the card ("PHOTO: AL RIYADI", automatic) and in the caption ("📸 Al Riyadi"; the gate checks).
- **Never:** agency or wire photos (Getty, AFP, Reuters, AP, EPA, Imago, Shutterstock, Alamy, Sportsfile…; also when they appear on a club or UEFA page with that credit), watermarked or text-burned images, fan pages, aggregators, other news sites' photos, screenshots of TV, AI-generated or edited images of real people.
- **Right photo, right event:** use a photo only when the source page itself says what it shows (the match, the date, the people). Never guess who is in a photo, never use a photo from another game or season, never crop someone out to change what happened. Results: the clubs' own post-game report or gallery, after the final whistle. Previews: crests, plus an official photo only if it plainly fits (the team, this season).
- **Choosing:** look at every candidate (`tools/photos.py scan` makes a numbered sheet): sharp, well lit, action or celebration over posed shots, the faces of our story's people visible, nothing embarrassing (falls, injuries, arguments). Set `focus` on the action so the crop keeps it.
- **Quality:** the renderer refuses any photo it would have to enlarge more than 1.25× for its layout; then pick a bigger one or go typographic.
- **Sensitive:** no photos on injury, death, legal or disciplinary stories, and none of minors unless their federation names them in the release. If anyone (club, athlete, photographer) asks us to remove a photo, Geoffry is told at once and the post is replaced or deleted.
- No compliant photo → the typographic card, as before. That's fine.
- Set `instagramData.isAiGenerated` to false (designed graphics and real photos, nothing generated) and write alt text for every image.

### Reels
**Every Reel has sound** (Geoffry, 21 Oct 2026). `tools/render.py` builds an original soundtrack into every Reel (`tools/sound.py`: drums, bass, chords, whooshes and hits timed to the slide changes; tempo and key vary per Reel). Pick the mood with `"sound": {"mood": "drive"}` (results, big nights), `"bright"` (wins, spotlights) or `"calm"` (explainers, tables). The gate rejects any Reel without an audible soundtrack. No copyrighted music, ever; don't add Instagram catalog audio on top. Reels are typographic motion graphics only: no match footage or reposted video.

### What performs (from the LB insights export, 19 Aug – 7 Sep 2026)
Athlete and community features reached 30–100 times more people than result cards: "rugby league did you know" 8,218 views, "Aziza Sbaity" 6,051, "meet Lindzi" 4,618, "run clubs" 3,916, "Lynn El Hajj" 3,833, almost all (93–99%) from non-followers, helped by the athletes resharing. Plain result cards sat at 60–110 views. So every page runs **at least three spotlights or explainers a week** (an athlete, a club, a sport nobody covers, a "did you know"), each built on official sources and aimed at a confirmed reshare target, alongside the results. Results keep the page credible; spotlights grow it.

---


**History series ("From the Archive") only:** besides official club/federation/organiser archive photos, Wikimedia Commons files under Public domain, CC0, CC BY or CC BY-SA may be used, picked with `tools/archive_photo.py` (it reads the licence and author from the Commons file page and refuses anything else). Credit them on the card and in the caption as "<Author> / Wikimedia Commons, <Licence>". Commons is never used for news posts. Agency/wire photos stay banned everywhere, even when someone has uploaded them to Commons.

## 8. Corrections

If a published post turns out to be wrong:
1. Tell Geoffry immediately (push notification and top of the brief) with the post link, what was wrong and the correct fact with its source.
2. Prepare a correction post as a Metricool **draft** and log it in `corrections.md`.
3. Geoffry decides whether to delete or edit the original (tools can't edit a published Instagram caption).
4. Add the lesson to section 10 so it doesn't happen again.

Each run also re-checks the previous day's posts against the latest official sources (scores amended, results overturned, name corrections) and flags anything that changed.

---

## 9. Briefs to Geoffry

Every run ends with a short brief (push notification and final message):
- Published / scheduled today per page: time, one-line topic.
- Drafts waiting for his approval, with why each is AMBER and the Metricool planner link.
- Stories killed for failing verification (one line each), so he can check them himself if he wants.
- Corrections or anything that changed since posting.
Keep it under 150 words. If nothing was verifiable, say so in one line.

---

## 10. Learnings

(The weekly desk adds dated, one-line lessons here: what performed, what to avoid, naming decisions.)

- 2026-10-19: Planning documents are not sources. `strategy.md` (Aug 2026) said Lebanon qualified for the 2027 AFC Asian Cup; they did not (Yemen 2-0 Lebanon, 4 Jun 2026, per L'Orient Today). Verify every "known" fact like any other.
- 2026-10-19: Official pages can contradict themselves (FIBA's article and head-to-head table gave different China–Lebanon scores). When two tier-1 pages disagree, use the box score / match sheet, and if that's not available, don't post the number.
- 2026-10-19: Aggregators can count matches still in progress (Sofascore's Cyprus table on 19 Oct). Tables come from the CFA page, not aggregators.
- 2026-10-19: The first dry run (CY table after the 17–18 Oct games) was killed by the independent fact-check: every number matched the CFA, but "after six rounds" and "game in hand" were wrong because two round-6 games were played on the Monday. Rule added to 4.3 (tables and rounds). This is the gate working as designed.
- 21 Oct: the 09:15 cloud morning run ended in 30 seconds with nothing done. A check showed fresh cloud sessions started by a recurring scheduled task have no `add_repo` and git is refused, so they can never publish. Desks now run inside the SportsWire session as one-off `send_later` messages that each run tops up (schedule/README.md). Never schedule SportsWire work with `create_trigger`.
- 21 Oct: Club names follow FIBA for basketball ("Al Riyadi"), the FLBB where FIBA has no listing ("Antonin", not "Antonine"). When briefing a fact-checker, say which body is the spelling authority, or it may flag the house spelling. A Lebanon24 flash had Riyadi's semi as 97-69; the club, WAM and four outlets had 98-69: one fast flash is never enough.
- 22 Oct: An athlete's own press release, reprinted by several outlets, is still one source. The Tziortzis "third in the European Championship" line came only from his release; the series' standings didn't show it, so it was dropped. Count divisions and categories from the organiser (the NASCAR Euro Series has three: V8GP, OPEN, Rookie Challenge).
- 23 Oct: A site whose robots.txt disallows automated access counts as a refusal, the same as a blocked fetch. The AFC's data API (api.the-afc.com) is `Disallow: /`, so it is no longer used, with curl or anything else. For AFC games use the www.the-afc.com match reports and news (allowed), then tier-2 outlets (Annahar, elsport, Grand Lebanon) for kick-off times. UEFA's match data (match.uefa.com) has no such rule and stays fine. Before relying on any data endpoint, check its robots.txt once and note it in `sources/`.
- 23 Oct: First archive posts. The research agent wrote that Lebanon finished "third" in their 2000 Asian Cup group; the RSSSF table shows they were fourth (level on points with Thailand, worse goal difference). For any group position, work it out from the full table yourself, tie-breakers included. The independent check caught it, which is why archive posts go through the same gate as news.
