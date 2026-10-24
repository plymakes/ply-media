# Series: Spotlight and Explained

Geoffry, 24 Oct 2026, after the media audit: two weekly series next to From the Archive (`history/README.md`). The reason is in the numbers. On LB, 10 story-led posts (Aziza Sbaity, run clubs, rugby league explainers) brought 95% of all views, with a median of about 2,500 views; news and results posts had a median of 66. CY showed the same pattern on a smaller scale (136 vs 28). Results keep the pages credible. These two series are what grows them.

Both series follow every PLAYBOOK rule: facts with sources, the independent fact-check, the gate, tags and collaborators, house style.

| | Spotlight | Explained |
|---|---|---|
| What | One Lebanese or Cypriot athlete, coach or community figure the big outlets skip | What's at stake in a big event, explained before it happens |
| When | Wednesday 10:00, both pages, once a week | 12:30 the day before an A event; at most 2 per page per week |
| Format | Carousel, 5–6 slides (or a Reel when there's a strong photo) | Carousel, 5–6 slides |
| Spec | `"series": "spotlight"` | `"series": "explained"` |
| Caption | up to 60 words (gate) | up to 60 words (gate) |
| Hashtags | page tag + `#SportsWireSpotlight` | page tag + `#SportsWireExplained` |
| Planned in | `series/queue.md` (weekly desk) | `series/queue.md` (weekly desk) |
| Built by | the Wednesday morning desk (or the weekly desk ahead) | the morning desk on the day before the event (evergreen ones: the weekly desk ahead) |
| Light | GREEN facts-only; **AMBER when it carries DM answers** | GREEN |

## Spotlight

**Who.** One person per page per week: an athlete, coach, referee, organiser, or the founder of a club or run club. Pick people the big outlets skip: small sports, women's sport, para sport, community sport, Lebanese and Cypriots abroad. Avoid stars every outlet already covers, and don't pick a club or national team (those get the news posts). Adults only: anyone under 18 is AMBER beyond a plain federation result (PLAYBOOK 5), so they aren't Spotlight subjects. No repeats within 12 weeks (`series/log.json`). Rotate sports, men and women, and home and abroad, and put overdue sports first (`tools/sweep.py coverage`). The best Spotlight hangs off something coming up: a championship next week, a race this weekend.

**Three questions by DM (the original access the audit found missing).** Runs can't send Instagram DMs, so this part is Geoffry's:
1. On Sunday the weekly desk picks the Spotlight subjects for the **week after next** (one per page plus a backup). That gives the DM about ten days. It confirms each person's handle (high confidence, `sources/handles.json`) and writes three short, friendly questions into `series/queue.md`. The weekly brief lists them under "Spotlight DMs for Geoffry to send", ready to copy and paste.
2. The questions are about their sport and their story, never their private life, money, politics or injuries. The default set, adjusted to the person:
   - "How did you get into <sport>?"
   - "What's the moment you're proudest of so far?"
   - "What's next for you?"
   The DM also says it's for a SportsWire Spotlight and that we'll invite them as collaborator, so they know to accept the invite.
3. Geoffry pastes the replies in any SportsWire chat (or attaches screenshots). The session that gets them writes them **verbatim** into `series/answers/<page>-<slug>.md` (who, handle, date received, the questions, the answers; translations marked "translated from Arabic/Greek") and pushes.

**Building it** (Wednesday's morning desk, or earlier):
- Slides: 1. hook (`news` with the biggest credited photo, eyebrow `["Spotlight", "<sport>"]`, `section`: "No. <n>"); 2. who they are (`news` rows or `spotlight`); 3. the thing they did (`stats` tiles); 4. "In their words" (`quote`, only with DM answers); 5. what's next (`preview` or `news`); 6. `end`. As a Reel: the tools/README "Spotlight" structure.
- **With DM answers:** each quote is a fact with `"interview": {"with": "<handle>", "via": "Instagram DM", "received_by": "Geoffry", "at": "<ISO>", "answer": "<verbatim>", "file": "series/answers/…md"}`. The gate counts that as the source for the quote and requires the post to be **AMBER**, so it goes to Metricool as a draft and Geoffry publishes it (he's seen the answers). Quote verbatim, trimmed with "…" only, never reworded. Any factual claim inside an answer (a result, a record, a ranking) still needs its own source; if it can't be confirmed, cut that part of the quote.
- **Without answers by Wednesday's morning desk:** build the facts-only version (GREEN, auto-publishes) from official sources (federation, results databases, the person's own channels for news about themselves). If answers arrive later, they can make a short "In their words" follow-up Story or post.
- **Fact-check:** the checker gets the card text and caption as usual. Lines that are the person's own words from our DM are marked `[OWN WORDS FROM OUR INTERVIEW: don't verify the wording, but check any fact inside it]`, and they aren't listed as claims.
- **Tags:** invite the person as collaborator (high-confidence handle), plus their club or federation (max 3, PLAYBOOK 7). That holds on the AMBER version with DM answers too: it's AMBER only so Geoffry sees the quotes, not because it's sensitive. Mention their club, federation and the event organiser.
- **Caption:** one or two plain lines about who they are and why now, then (with answers) one short line of theirs in quotes. On LB, Arabic under the English as usual. No question CTA unless it's natural ("Know someone we should feature? Tell us.").

## Explained

**What.** A 5–6 slide carousel published the day before an A event (national teams, finals, derbies, European nights, a Lebanese or Cypriot athlete in a major championship), explaining what's at stake: what they need, how the format works, who to watch, when and where. Explainers get saved and sent, and Lebanon's rugby league explainers were among the posts that travelled.

**When.** 12:30 the day before the event, both pages. That keeps the 18:00 slot free for the preview of early-start events, and the morning-of preview stays as it is. It takes whatever was planned for 12:30 that day (news moves to 15:00 or 18:00; a quiz carousel moves to Stories). At most 2 per page per week, biggest events first. A week with no A event runs an evergreen one instead (how the Lebanese Premier League works, what an LA28 quota place is, how the Cyprus League split works) on Tuesday at 12:30, the grid's explainer slot.

**Slides.** 1. the question as the hook (`news` with a photo, eyebrow `["Explained", "<competition>"]`), e.g. "What Cyprus need in Armenia."; 2–4. the answer (`standings` for the table, `stats` for the numbers, `news` rows for the rules or format, `fixtures` for what's left); 5. when and where (only a confirmed time and venue, and a broadcaster only if the organiser or broadcaster announces it); 6. `end`.

**Rules.**
- No predictions, no odds, no "should". "What they need" is arithmetic from the official table and the competition's own regulations, with the sums written into the facts.
- Built the day before by the morning desk from the latest official table, because results can change it up to the last round. Evergreen explainers (rules and formats that won't change) can be built and scheduled ahead by the weekly desk.
- Caption: the question in plain words, one or two lines of what to know, then a soft "send this to someone going to the game" if it fits (CAMPAIGN 7.4). LB gets Arabic under the English as usual.
- Tags: the federation, the competition organiser and the clubs or national team in it. Invite the federation or club as collaborator.

## The forward queue

`series/queue.md` holds the next four weeks of both series per page: date, slot, topic, the event it hangs off, the official source to verify, the collab target, and for Spotlights the subject, handle, DM questions and DM status (`to send` → `sent <date>` → `answered <date>` → `none, facts-only`). The weekly desk extends it every Sunday (RUNBOOK 3, step 4b) from `events/`, the CAMPAIGN.md tentpoles and the sports maps. The weekly plan (`plans/<year>-W<week>.md`) copies the coming week's items from it. **Everything in the queue is a lead**: the run that builds the post verifies every date and fact first, and swaps or drops the item if it can't.

## Log

`series/log.json`: one entry per published item (`series`, `issue`, `page`, `date`, `key`, `subject`, `spec`, `metricool_id`). Issue numbers run per page and per series, starting at 1. Check the log before choosing, so there are no repeats.
