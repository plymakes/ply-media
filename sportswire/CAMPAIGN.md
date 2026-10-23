# Season Kickoff: SportsWire growth campaign

**Runs:** Wednesday 21 October – Sunday 6 December 2026 (seven weeks), both pages.
**Owner:** the scheduled runs (morning desk, evening desk, weekly desk). Geoffry reviews AMBER drafts and the weekly brief.
**Rules that still win:** PLAYBOOK.md. Nothing in this campaign relaxes the verification standard, the traffic light or the gate.

## 1. Positioning

SportsWire is the **verified, drama-free sports wire** for Lebanon and for Cyprus: the page you trust for the score, the signing and the story behind the athlete, in English, in a clean modern design. We cover everything (wins, defeats, small sports, women's and youth sport) and take no sides between local clubs.

The long game: grow Lebanese and Cypriot sport by giving athletes, clubs and federations coverage worth resharing. That builds the audience first and a news business later (sponsorships, club media services; see section 9). For these seven weeks the only goal is **followers who stay**.

## 2. Targets

The weekly desk records the baseline on its first run (25 October) in `growth-log.json`. Targets for 6 December, per page:

| Measure | Target |
|---|---|
| Followers | +50% on the 25 Oct baseline (about +6% a week, compounding) |
| Share of reach from non-followers | 70% or more |
| Reels published | at least 3 a week |
| Collab or reshare by an athlete, club or federation | at least 2 a week |
| Average shares + saves per feed item | rising week on week |
| Corrections | zero (any correction is reviewed in the weekly brief) |

## 3. What Instagram rewards now (and how we use it)

- **Reels reach the most new people at our size.** For accounts under 10,000 followers, Reels reached 4.9% of followers per post against 3.5% for images and 2.6% for carousels, and about three times as many non-followers as carousels (Fanpage Karma, 3M+ posts, Jan–Apr 2026). → At least 3 Reels a week per page, short (8–15 s for news, up to 30 s for explainers).
- **Watch time and sends drive distribution.** Instagram's head Adam Mosseri named watch time, sends per reach and likes per reach as the main ranking signals (Jan 2025). Average Reel watch time is now 8.5 s (Metricool, 24M posts, Jun 2026). → The hook lands in the first second. Make posts people forward to a friend: big local wins, "did you know" facts, athlete stories.
- **Carousels earn saves.** Carousels get about 9× more saves than single images (Metricool 2026). → Explainers, week-ahead guides and spotlights are carousels.
- **Single images are fading** (reach −22% year on year, Metricool 2026). → Keep single cards for breaking news and results only.
- **Hashtags don't help; keywords do.** Posts with hashtags averaged ~32% fewer views (Metricool 2026). → At most 3 hashtags; write captions with the words people search ("Lebanese basketball", "Cyprus League", club and athlete names).
- **Questions get comments.** Captions with a question got ~37% more comments (Metricool 2026). → End most captions with one genuine question. Never engagement bait ("comment YES", "tag 3 friends").
- **Originality is required for recommendations.** Reposted clips can get an account excluded. → No match footage or reposted videos, ever. Our Reels are original typographic motion graphics.
- **Trial Reels** (shown only to non-followers) need 1,000 followers. → Switch on when a page passes 1,000: two a week to test hooks, one variable at a time.
- **Consistency beats bursts.** → Something every day on both pages, even if it's a single fixtures Story.

## 4. The formats

All built from `tools/render.py` templates; Reels with `"format": "reel"` (see `tools/README.md`).

| Format | Built with | When |
|---|---|---|
| **Result card** | `result`, `roundup` | Every final result worth reporting, same evening |
| **Result Reel, "in 10 seconds"** | reel: `preview` hook → `result` → `stats` → `end` | National-team games, derbies, European nights, medals |
| **Weekend in 60 seconds** | reel: hook → 3–5 `result`/`roundup` slides → `end` | Monday morning, both pages |
| **Spotlight** | carousel (`news`/`stats`/`spotlight` slides) or reel | 3 a week per page; athlete, coach, club, small sport, women's or youth team (results only, from the federation) |
| **Explainer** | carousel, 4–7 slides | 1–2 a week: "how the new Final 5 works", "what Lebanon need in Group F", "how the Cyprus League split works" |
| **Numbers** | `stats` card or reel | Weekly: the round or the week in numbers |
| **Week ahead** | `fixtures` carousel + Story | Monday 10:00 |
| **Today** | `fixtures` Story | Every day with local fixtures |
| **Countdown** | `preview` Story or reel | Before tentpoles (section 6) |
| **Table** | `standings` | After each full round (PLAYBOOK 4.3: round must be complete) |
| **Correction** | `correction` | Only if needed; always AMBER |
| **Quiz** (interactive) | `quiz` → `answer` (carousel or two Stories) | LB: Wed 12:30 carousel; Stories Mon, Wed, Sat 13:30. A different sport each time, overdue sports first |
| **Vote** (interactive) | `vote`, 2–4 candidates with photos | LB: Mon 18:00 "performance of the week" across all sports |
| **Predict the score** (interactive) | `predict` Story (feed for the biggest games) | Morning of every A/B match, with the Today Story |
| **Today, all sports** | `fixtures` Story, one group per sport | LB: 09:30 every day with an event in any top-20 sport |
| **Tonight's results** | `fixtures`/`roundup` Story across sports | LB: 22:45 on match nights |
| **Lebanese abroad** | `roundup`/`spotlight` carousel | LB: Fri 15:00 and Sun 15:00 (athletes from `sources/lebanon-sports.md`) |
| **Other sports this weekend** | carousel, one slide per sport | LB: Mon 15:00 (volleyball, futsal, handball, women's leagues, individual sports) |

**Every Reel has sound**: the renderer builds an original soundtrack into each one, and the gate blocks silent Reels (PLAYBOOK 7, Reels).

Every carousel and Reel ends with an `end` slide ("every lebanese result, first." / "cypriot sport, in english."). Reels get a cover at the end of the hook slide (`reel_meta.cover_ms`).

## 5. The weekly grid (per page)

The weekly desk turns this into a concrete plan for the coming week in `plans/<year>-W<week>.md`, using real fixtures. The morning desk builds that day's planned items alongside the news.

| Day | 10:00 | 12:30 | 18:00 | Evening |
|---|---|---|---|---|
| Mon | Weekend in 60 s (Reel) | Week ahead (carousel) + Story | Spotlight 1 | — |
| Tue | News / results | Explainer (carousel) | — | Results if any |
| Wed | Spotlight 2 (Reel) | News | — | European nights (CY) / results |
| Thu | News / preview | Numbers (card or Reel) | — | European nights (CY) / results |
| Fri | Weekend preview (carousel) | Spotlight 3 | Today Story | Results |
| Sat | Today Story + news | — | Result Reel if a big one | Results / roundups |
| Sun | Today Story + news | — | Table after the round | Results / roundups |

**@sportswire.lb from 24 Oct 2026** (more sports, more often: Geoffry, 23 Oct). Feed ~3 a day (max 5); Stories 3–6 a day; at least 5 interactive items and 8 different sports a week.

| Day | Stories | 10:00 | 12:30 | 15:00 | 18:00 | 19:30 | Evening |
|---|---|---|---|---|---|---|---|
| Mon | Today · quiz pair 13:30 | Weekend in 60 s (Reel) | Week ahead, all sports (carousel) | Other sports this weekend (carousel) | Vote: performance of the week | — | Results |
| Tue | Today · predict | News / results | Explainer or small-sport spotlight | News | Spotlight 1 | Archive | Results |
| Wed | Today · quiz pair 13:30 | Spotlight 2 (Reel) | Quiz (carousel) | News | News / preview | — | Results |
| Thu | Today · predict | News / preview | Numbers (card or Reel) | News | Spotlight 3 | Archive | Results |
| Fri | Today · predict for every A/B game | Weekend preview, all sports (carousel) | News | Lebanese abroad | News / preview | — | Results · tonight's results Story |
| Sat | Today · predict · quiz pair 13:30 · tonight's results | News | — | News | Result Reel if a big one | — | Results / roundups |
| Sun | Today · predict · tonight's results | News | — | Lebanese abroad (weekend) | Table after the round | — | Results / roundups |

**@sportswire.cy from 24 Oct 2026** (Geoffry: "let's do the same for cyprus"). Same volume; built around Thursday European nights and Friday–Monday league rounds; at least 6 different sports a week.

| Day | Stories | 10:00 | 12:30 | 15:00 | 18:00 | 19:30 | Evening |
|---|---|---|---|---|---|---|---|
| Mon | Today · quiz pair 13:30 | Weekend in 60 s (Reel) | Week ahead, all sports (carousel) | Other sports this weekend (carousel) | Vote: performance of the week | — | Monday league games |
| Tue | Today · predict (basketball in Europe) | News / results | Explainer or small-sport spotlight | News | Spotlight 1 | Archive | Results |
| Wed | Today · quiz pair 13:30 · predict | Spotlight 2 (Reel) | Quiz (carousel) | News | European night preview | — | Basketball in Europe |
| Thu | Today · predict for Omonia and Pafos | Preview (European night) | Numbers | News | Spotlight 3 | Archive | European results |
| Fri | Today · predict | Weekend preview, all sports (carousel) | News | Cypriots abroad | News / preview | — | Results · tonight's results Story |
| Sat | Today · predict · quiz pair 13:30 · tonight's results | News | — | News | Result Reel if a big one | — | League results / roundups |
| Sun | Today · predict · tonight's results | News | — | Cypriots abroad (weekend) | Table after the round (if complete) | — | Results / roundups |

Overdue sports (`python3 tools/sweep.py coverage --page lb|cy`) take the next spotlight, quiz, vote, explainer or archive slot. The two grids above replace the generic grid for both pages from 24 Oct.

**Timing beats the grid.** On event days the grid gives way to the event: a preview that morning (or the evening before for early starts), and the result straight after the final whistle through a result desk (PLAYBOOK 6, Timing).

Target per page: about 2 feed items a day, never more than 4, never two within 90 minutes (30 minutes on results nights). A quiet news day is filled by the planned campaign item, never by padding.

## 6. Tentpoles, 21 Oct – 6 Dec 2026

From the source maps (19 Oct). **These are leads, not facts**: each run re-verifies dates, times and line-ups on the official source before building anything.

**Lebanon**
- Lebanese basketball Division A 2026–27 tips off (expected 24 Oct, FLBB via Annahar): season preview carousel, "new format explained", opening-weekend roundup Reel.
- AFC Challenge League group stage (Al Ansar in Bhutan, Nejmeh in Tajikistan, to 24 Oct): results, "both through?" card.
- Rugby League World Cup: Tonga v Lebanon (expected 23 Oct, Sydney), Lebanon v France (expected 1 Nov): previews, results, Cedars spotlights.
- Arab Club Basketball Championship (final expected 20 Oct, Ghazir): result if Lebanese clubs feature.
- **FIBA World Cup 2027 Asian Qualifiers, home window:** Lebanon v Japan (expected 26 Nov) and Lebanon v China (expected 29 Nov), Zouk Mikael. The campaign's biggest moment: a two-week countdown (Stories plus 2 Reels), "what Lebanon need" explainer, player spotlights, result Reels both nights.

**Cyprus**
- Europa League: Omonia v Benfica (expected 22 Oct), at N.E.C. (5 Nov), at Juventus (26 Nov). Conference League: Pafos v Riga (expected 22 Oct), at Twente (5 Nov), v Midtjylland (26 Nov). Thursday-night result Reels, Friday "both of them" card.
- Cyprus Rally (expected 23–25 Oct): preview numbers card, results.
- UEFA Nations League: Armenia v Cyprus (expected 12 Nov), Cyprus v Montenegro (expected 15 Nov): previews, "what's at stake" explainer, result Reels.
- EURO 2028 qualifying draw (expected 6 Dec, Belfast): "who could Cyprus get" explainer, then the draw result.
- Cyprus League rounds every weekend: Sunday table (once the round is complete), Monday weekend-in-60-seconds.

## 7. Growth levers

1. **Collabs.** Invite the athlete, club or federation as collaborator on positive spotlights and big results (only high-confidence handles; PLAYBOOK 7). One collab post shows on both profiles.
2. **Reshare targets.** Mention the confirmed handle on every post. Athletes and small clubs reshare clean coverage.
3. **Underserved corners.** Women's basketball and football, futsal, volleyball, athletics, swimming, rally, rugby league, run clubs. Our August data: features on athletes and communities reached 30–100× more people than result cards.
4. **Sendable posts.** "Did you know" facts, records, local pride moments, explainers people forward to a friend. A soft "send this to…" line is fine on explainers; never on news.
5. **Keyword captions** and alt text on every image (PLAYBOOK 7).
6. **Stories every day.** Today's fixtures and the day's main post as a Story card; on LB also predict-the-score, quiz pairs and tonight's results (PLAYBOOK 7, Interactive posts). Real poll stickers can't be added by the publishing tools; Geoffry can add one by hand if he wants.
7. **Trial Reels** from 1,000 followers.

## 8. Editorial standards: the no-drama rules

- Verified news only (PLAYBOOK 4). No rumours, no "reportedly", no transfer gossip.
- No hot takes, no opinions on referees, officials or players, no blaming.
- Neutral between local clubs: the derby is the biggest show in town, never a side. Report each club's wins with the same warmth.
- No rage-bait questions ("worst signing ever?", "who's the bigger club?"). Questions invite good-natured answers: "who was your player of the night?", "which game are you going to?".
- Nothing about players' private lives, fights in the stands, politics or sectarian or communal tension. Anything near those is AMBER (a draft for Geoffry) or not covered.
- Defeats are reported plainly and kindly; injuries and sad news are AMBER and never get emojis or CTAs.
- If a post draws ugly comments, the brief tells Geoffry which post. We don't argue in comments.

## 9. Money later (groundwork only)

No paid deals during the campaign. The weekly desk keeps `growth-log.json` (followers, reach, top posts) so there is a clean record for a media kit at about 5,000 followers. Future routes from `strategy.md`: local sponsors, club and federation graphics services, a sponsored daily brief. Gambling promotion is never run on the Lebanon page, and on Cyprus only with licensed operators, labelled, and Geoffry's explicit sign-off.

## 10. The weekly loop

Every Sunday the weekly desk:
1. Pulls the last 7 days per page from Metricool (followers gained and lost, reach, views, interactions, shares, saves, Reels views; `IGEV01, IGEV06, IGEV12, IGEV23, IGEV38, IGEV39, IGEV40, IGEV15, IGEV43, IGEV44`) and appends them to `growth-log.json`.
2. Ranks the week's posts by reach and by shares + saves; names the top and bottom three per page.
3. Shifts next week's mix toward what worked (more of the best format, fewer of the worst). After three weeks a format that is bottom every week is dropped or reworked.
4. Writes next week's plan in `plans/<year>-W<week>.md` from the grid in section 5 and the tentpoles in section 6.
5. Reports progress against section 2 in the weekly brief.
