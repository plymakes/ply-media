# Cyprus sports map: the top 20 sports, every competition we track, and the fast sources

Geoffry's brief (23 Oct 2026), after the Lebanon map: "let's do the same for cyprus then". The same ask applies: all sports Cypriots compete in, at home and abroad, every league and tournament to keep track of, the top 20 sports gone through on every run, more frequent posting (Stories and posts), clubs and individual athletes, all games, interactive posts with images, and multiple fast, reliable sources per sport for schedules, scores, results and images.

- **Data:** `sources/cyprus-sports.json` (what `tools/sweep.py --page cy` reads). This file is the readable version; when they disagree, fix both. The older notes in `sources/cyprus.md` (19 Oct) still hold the spelling guide and handle table.
- **Every run:** `python3 tools/sweep.py today --page cy` walks all 20 sports in this order with their live competitions, dated events, athletes to look up and sources to open. `python3 tools/sweep.py coverage --page cy` shows which sports are overdue on @sportswire.cy. Every CY spec names its `sport` with an id from the JSON (the gate checks).
- **Weekly upkeep:** RUNBOOK section 3, step 6a.
- **Research:** four parallel researchers on 23 Oct 2026 (football and basketball; other team sports; individual and Olympic sports; motorsport, athletes abroad, multi-sport and outlets), with WebSearch and WebFetch only, building on `sources/cyprus.md`. Wikipedia was used as a lead only. Instagram and X can't be fetched, so **handles are listed only where the organisation's own website links them**; everything else is UNCONFIRMED. A source listed here is where to look, not proof: every fact still needs PLAYBOOK section 4.
- **Times:** CFA and CBF pages show Cyprus time; UEFA shows CET; **FIBA event pages and FotMob show UTC**. Cyprus is UTC+3 until Sun 25 Oct 2026 04:00, then UTC+2. Convert every time before it goes on a card.
- **Sensitive ground:** clubs and events in the north, and anything touching the Cyprus problem, are AMBER (PLAYBOOK section 5). Whether Cyprus attends the 2027 European Games in Istanbul is unconfirmed and politically sensitive: report only what the Cyprus Olympic Committee announces.

## How the ranking was made

Following and media attention in Cyprus (outlet coverage volume, club and federation followers where a third-party directory shows them, crowds), how much is happening in the season ahead (leagues, European ties, national-team windows, championships), and current Cypriot results and names (the record 18 medals at the 2026 Mediterranean Games, 12 at the Glasgow Commonwealth Games, world rankings). Cover frequency follows the rank.

## The top 20 (rank order = sweep order)

| # | Sport | Cover at least every | Why it ranks here |
|---|---|---|---|
| 1 | Football (incl. futsal and women's) | 2 days | By far the biggest following and coverage (Pafos ~176K, APOEL ~84K, Omonia ~65K on Instagram), league every weekend, Omonia and Pafos in Europe every other Thursday, Nations League decider on 15 Nov. |
| 2 | Basketball | 2 days | Second team sport by coverage: 10-team league with a TV deal, Keravnos and Petrolina AEK in the FIBA Europe Cup, AEL in two European competitions, both national teams playing in November. |
| 3 | Volleyball (indoor and beach) | 7 days | Live TV on RIK and AlfaSports.TV, Allwyn title sponsor, big multi-sport clubs, Pafiakos and Olympiada Neapolis in CEV cups; leagues start 6 and 10 Nov. |
| 4 | Athletics and running | 7 days | The most decorated sport this year (Kesidis world No. 12, Kulichenko, the Fotopoulou sisters, Trajkovic), an active federation, and a full running calendar (Larnaka Marathon 15 Nov). |
| 5 | Shooting (shotgun) | 14 days | Konstantia Nikolaou is world No. 9 in skeet; the Doha World Championship (1–14 Nov) opens LA28 qualifying; Larnaca hosts the junior shotgun Worlds in May. |
| 6 | Sailing | 14 days | Pavlos Kontides (2x Olympic silver, 2026 European champion) is the most covered Cypriot athlete. |
| 7 | Gymnastics (artistic and rhythmic) | 14 days | Marios Georgiou (European silver, two Taranto golds) and the first-ever Cyprus men's team at the Worlds (Rotterdam, finals 24–25 Oct). |
| 8 | Judo | 14 days | Seven Commonwealth medals in 2026 and two ranked judoka (Asvesta 20, Antoniou 21); Cypriots entered in Zagreb, Tashkent and Tokyo in Nov–Dec. |
| 9 | Handball | 14 days | League with six clubs in European cups; Anorthosis play AEK Athens on 25 Oct; the season is on hold after an attack on a referee (sensitive). |
| 10 | Motorsport | 14 days | The Cyprus Rally (23–25 Oct) decides the FIA Middle East title; Vladimiros Tziortzis in the NASCAR Euro Series. |
| 11 | Swimming | 21 days | Kalia Antoniou's two Taranto golds and national records; the 25 m Worlds in Beijing (1–6 Dec). |
| 12 | Water polo | 21 days | Allwyn league from 13–15 Nov with NO Keryneia back after 21 years. |
| 13 | Tennis and padel | 21 days | Davis Cup v Puerto Rico (6–8 Feb 2027) and the first Mediterranean Games tennis medal (Neos / Efstathiou); padel growing. |
| 14 | Cycling | 21 days | Bogdan Zabelinskiy (8th in the U23 time trial at the Worlds), an active federation with the 2027 calendar out (international MTB in Feb). |
| 15 | Rugby union | 21 days | The Mouflons in the Rugby Europe Conference (won 48-17 in Gibraltar), regular English coverage, world-record history. |
| 16 | Karate, taekwondo, boxing, MMA and wrestling | 35 days | Karate (Taranto bronze; Cyprus hosted the 2026 EKF youth Europeans), taekwondo, wrestling, boxing, MMA: thin coverage, cover when results come. |
| 17 | Fencing | 35 days | Alexandros Tofalides, Commonwealth Fencing champion and Cyprus's first Olympic fencer. |
| 18 | Archery and para archery | 35 days | Christos Misos is world para archery champion and No. 1; Cyprus hosts the Aphrodite Cup (28–31 Oct). |
| 19 | Cricket | 35 days | An active expatriate league and a women's team on the rise (37th in the ICC T20I rankings); season Apr–Oct. |
| 20 | Para sport | 35 days | Paralympic medallist Karolina Pelendritou, para powerlifter Maria Markou; inclusion matters for a page that covers everyone. |

**Watch list (beyond the top 20):** Weightlifting (Active federation, small international profile.); Skiing (Troodos season Jan–Mar; Olympian Yianno Kouyoumdjian.); Canoe and rowing (Savvia Hadjicharalambous, Taranto K1 500 m silver.); Chess (Cyprus hosted the 2026 Candidates; women's Olympiad Category D prize.); Multi-sport Games and the Olympic movement (Dakar Youth Olympics (7 Cypriots), Small States Games Monaco (May 2027), European Games (participation unconfirmed, sensitive), LA28 qualifying.). These come into the sweep only when one of their dated events is on.

## General fast sources (all sports)

| Source | Good for | Speed | Tier | Notes |
|---|---|---|---|---|
| [Kerkida.net](https://www.kerkida.net) | live, result, schedule, photos | live, minutes | 2 | fastest outlet seen; Greek; live match threads; transfers there are rumour until a club confirms; IG @kerkida.net_cy |
| [Omada (Reporter)](https://omada.reporter.com.cy) | result, news, photos | very fast, timestamped | 2 | use this subdomain (omada.com.cy is robots-blocked); IG @omada_cy |
| [Cyprus Times Protathlima](https://protathlima.cyprustimes.com) | result, news, photos | very fast | 2 | Pafos 1-1 Riga up at 20:41 |
| [Ant1 Live sport](https://www.ant1live.com/athlitika) | news, result | fast, timestamped | 2 | RSS ant1live.com/rss.xml |
| [Omega Live sport](https://omegalive.com.cy/athlhtika/) | news, result | same day | 2 |  |
| [RIK (CyBC) sport](https://sports.rik.cy) | news, result | same day | 2 | public broadcaster |
| [Politis Gipedo](https://gipedo.politis.com.cy) | result, news, schedule | fast | 2 | RSS gipedo.politis.com.cy/feed; the English edition has name errors |
| [CNA (Cyprus News Agency)](https://www.cna.org.cy/en) | news, result | fast | 2 | authoritative wire; body paywalled; robots crawl-delay 60 s |
| [Cyprus Mail sport](https://cyprus-mail.com/category/sport) | news, result | medium | 2 | best English coverage of individual sports, rally and multi-sport; football reports often next morning |
| [Alphanews sport](https://www.alphanews.live/category/sports/) | news | medium | 2 |  |
| [FotMob Cyprus](https://www.fotmob.com/teams/5793/overview/sip) | schedule, live, result | live | 2 | data service; UTC times; has shown conflicting scores: cross-check |

**Don't rely on:** philenews.com / in-cyprus.philenews.com and Kathimerini Cyprus (refuse automated fetching); omada.com.cy (robots-blocked: use omada.reporter.com.cy); cyprusaa.org and paralympic.org.cy (robots.txt disallows); cssf-shooting.org (robots-blocked); live.gymnastics.sport (FIG live scoring, robots-disallowed); badmintoncyprus.com (hijacked by spam: never link); Flashscore /standings/, /live/, /finished/, /scheduled/ and Sofascore /standings/ paths (robots.txt); Sigmalive English (stale since Aug 2026; Greek site fails to load); Transfermarkt (blocked; never proof of a transfer).

## 1. Football (incl. futsal and women's)

- **Governing body:** Cyprus Football Association (CFA). Site: https://www.cfa.com.cy (Greek /Gr/, English /En/; updated daily). Handles: @cyprusfa_official (Instagram), @CyprusFA (X), facebook.com/cyprusfaofficial (linked from cfa.com.cy).
- Clubs abroad are from FotMob: confirm on the club's own site before posting.
- Spelling: UEFA's current squad page says "Andronikos Kakoullis" (sources/spelling.md said Kakoulli): use the UEFA match page of the day.
- **Competitions we track:**
  - **Cyprus League by Stoiximan (14 teams; 26 rounds, then top 6 / bottom 8)** (domestic, priority B; 2026-08-28 → 2027-05-23 (end estimated); usual days Fri, Sat, Sun, Mon)
    - Kick-offs 15:00–20:00 local, mostly 17:00–19:00; dates published to matchday 16 (2–4 Jan); winter break 22 Dec–1 Jan. Derbies and top-of-table games are priority A.
    - [CFA First Division page](https://www.cfa.com.cy/Gr/competitions/68124755): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [CFA news (dates, venues, referees per matchday)](https://www.cfa.com.cy/Gr/news): schedule, news; 2–3 days ahead; tier 1
    - [Kerkida.net](https://www.kerkida.net): schedule, live, result, photos; live threads, minutes; tier 2 (fastest outlet; Greek; standings at /vathmologies)
    - [Omada (Reporter)](https://omada.reporter.com.cy): result, news; fast, timestamped; tier 2
    - [Politis Gipedo](https://gipedo.politis.com.cy/podosfairo/kypros/a-katigoria): schedule, result, news; hourly; tier 2
    - [FotMob](https://www.fotmob.com/teams/5793/overview/sip): schedule, live, result; live; tier 2 (data service; shows UTC times: convert)
    - [Sofascore Cyprus League](https://www.sofascore.com/tournament/football/cyprus/1st-division/171): live, result; live; tier 2 (cross-check only (its table counted live games on 19 Oct); robots.txt disallows /standings/)
    - [Cyprus Mail local football](https://cyprus-mail.com/category/sport/football-2/local-football): result, news; slow: 1 hour to next morning; tier 2 (English; patchy)
  - **Omonia (Europa League) and Pafos (Conference League) league phase; knockouts from Feb 2027** (international, priority A; 2026-09-16 → 2027-06-02; usual days Thu)
    - [UEFA match centre and fixture articles](https://www.uefa.com): schedule, live, result, photos; live; tier 1 (UEFA times are CET; photos are agency (Getty etc.): not usable)
    - [Omonia @omonoiafootball / Pafos @pafosfc](https://www.uefa.com/uefaeuropaleague/clubs/50077--omonia/): result, photos; live; tier 1 (club full-time posts are tier 1 for their own score)
    - [Kerkida.net](https://www.kerkida.net): schedule, live, result, photos; live threads, minutes; tier 2 (fastest outlet; Greek; standings at /vathmologies)
    - [FotMob](https://www.fotmob.com/teams/5793/overview/sip): schedule, live, result; live; tier 2 (data service; shows UTC times: convert)
  - **Men's national team: Nations League C2 (Armenia v Cyprus 12 Nov 19:00; Cyprus v Montenegro 15 Nov 16:00), EURO 2028 qualifying draw 6 Dec** (international, priority A; 2026-09-25 → 2027-11)
    - UEFA still shows coach Apostolos Mantzios "Suspended until further notice": unexplained, verify before naming a coach.
    - [CFA news (dates, venues, referees per matchday)](https://www.cfa.com.cy/Gr/news): schedule, news; 2–3 days ahead; tier 1
    - [CFA national team page](https://www.cfa.com.cy/Gr/nationalteams/1): schedule, result; ; tier 1
    - [UEFA match centre and fixture articles](https://www.uefa.com): schedule, live, result, photos; live; tier 1 (UEFA times are CET; photos are agency (Getty etc.): not usable)
    - [FotMob](https://www.fotmob.com/teams/5793/overview/sip): schedule, live, result; live; tier 2 (data service; shows UTC times: convert)
  - **Coca-Cola Cup (First and Second Division clubs)** (domestic, priority B; 2026-10-14 → 2027-05 (end estimated))
    - [CFA Cup page](https://www.cfa.com.cy/Gr/competitions/68536042): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [CFA news (dates, venues, referees per matchday)](https://www.cfa.com.cy/Gr/news): schedule, news; 2–3 days ahead; tier 1
    - [Kerkida.net](https://www.kerkida.net): schedule, live, result, photos; live threads, minutes; tier 2 (fastest outlet; Greek; standings at /vathmologies)
  - **Second Division (16), Third Division (16), STOK Elite (16)** (domestic, priority C; 2026-09 → 2027-05 (end estimated); usual days Fri, Sat, Sun)
    - [CFA Second Division](https://www.cfa.com.cy/Gr/competitions/68156043): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [CFA Third Division](https://www.cfa.com.cy/Gr/competitions/68156107): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [CFA STOK Elite](https://www.cfa.com.cy/Gr/competitions/68160192): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [Kerkida.net](https://www.kerkida.net): schedule, live, result, photos; live threads, minutes; tier 2 (fastest outlet; Greek; standings at /vathmologies)
  - **Women's Championship (7 teams, Sundays 11:00; Apollon Ladies won the Super Cup) and women's national team (Nations League draw 3 Nov)** (domestic, priority C; 2026-10-03 → 2027-05 (end estimated); usual days Sun)
    - [CFA Women's Championship](https://www.cfa.com.cy/Gr/competitions/68354866): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [CFA women's national team](https://www.cfa.com.cy/Gr/nationalteams/9): schedule, result; ; tier 1
  - **Futsal Championship (10 teams, Thu/Fri evenings)** (domestic, priority C; 2026-10-08 → 2027-05 (end estimated); usual days Thu, Fri)
    - [CFA futsal page](https://www.cfa.com.cy/Gr/competitions/68497373): schedule, result, table; same night or next morning; tier 1 (robots.txt disallows /images/: never take photos from there)
    - [AEK Larnaca site (futsal reports)](https://www.aek.com.cy): result; same night; tier 1
    - [Kerkida.net](https://www.kerkida.net): schedule, live, result, photos; live threads, minutes; tier 2 (fastest outlet; Greek; standings at /vathmologies)
  - **Youth national teams: U17 EURO qualifiers hosted in Cyprus (Japan friendly 27 Oct; Faroe Islands 30 Oct; Romania 2 Nov, all 15:00, Achna); U19 Round 2 hosted 11–17 Nov (Armenia, Albania)** (international, priority B; 2026-10-27 → 2026-11-17)
    - [CFA news (dates, venues, referees per matchday)](https://www.cfa.com.cy/Gr/news): schedule, news; 2–3 days ahead; tier 1
    - [UEFA match centre and fixture articles](https://www.uefa.com): schedule, live, result, photos; live; tier 1 (UEFA times are CET; photos are agency (Getty etc.): not usable)
    - [Kerkida.net](https://www.kerkida.net): schedule, live, result, photos; live threads, minutes; tier 2 (fastest outlet; Greek; standings at /vathmologies)
- **Photos appear first at:** club Instagram/X at full time; Kerkida galleries the same evening; CFA galleries the next day (no credit lines). UEFA photos are agency: never use.
- **People to follow:** Marcus Edwards (Burnley); Hector Kyprianou (Watford); Nikolaos Panagiotou (FC Utrecht); Loizos Loizou (Crvena Zvezda); Ioannis Pittas (CSKA Sofia); Joel Mall (Young Boys); Stelios Andreou (Estoril); Nicholas Tsaroulla (Notts County).
- **Sport-wide sources:** [CFA news (dates, venues, referees per matchday)](https://www.cfa.com.cy/Gr/news); [Kerkida.net](https://www.kerkida.net); [UEFA match centre and fixture articles](https://www.uefa.com).

## 2. Basketball

- **Governing body:** Cyprus Basketball Federation (CBF/KOK). Site: https://www.cbf.basketball (updated) + results system cbfweb.org. Handles: @basketcyprus (Instagram), facebook.com/basketcyprus, @BasketCyprus (X), YouTube basketFed (linked from cbf.basketball); streams on cbftv.net.
- FIBA and FotMob show UTC times: a FIBA "16:30" is 19:30 in Cyprus until 25 Oct and 18:30 after.
- Omada (23 Oct) reports a Greek-led basketball match-fixing inquiry with a Cyprus angle: AMBER at best, verify before any mention.
- **Competitions we track:**
  - **ECOMMBX Basket League (10 teams, 18 rounds, then play-offs; champions Petrolina AEK)** (domestic, priority B; 2026-10-09 → 2027-05 (end estimated); usual days Fri, Sat, Sun, Mon)
    - Clubs: Petrolina AEK, TRIA EKA AEL, Keravnos, APOEL, DOMUS Apollon, ETHA Engomis, Anorthosis, Achilleas Kaimakliou, ACRO4U Digenis Morphou, Fabbrica EN Paralimniou. Games 17:00–19:30 local.
    - [CBF results system (eCBF)](http://cbfweb.org/eCBF/pubgames.aspx): schedule, result; after the game; tier 1 (http only; competition, round and season dropdowns; current club names)
    - [Cyprus Basketball Federation news](https://www.cbf.basketball): result, news, photos; same night or next day; tier 1
    - [Kerkida basketball](https://www.kerkida.net/eidiseis/alla-spor/mpasket): result, photos; 10–15 minutes after the buzzer; tier 2
    - [Politis Gipedo basketball](https://gipedo.politis.com.cy/kalathosfaira): result; hours; tier 2
    - [Omada (Reporter)](https://omada.reporter.com.cy): result, news; fast, timestamped; tier 2
  - **FIBA Europe Cup (Keravnos Group D, Petrolina AEK Group E), EuroCup Women (AEL), ENBL (TRIA EKA AEL)** (international, priority B; 2026-10-07 → 2027-04 (end estimated); usual days Tue, Wed)
    - [FIBA event pages (Europe Cup, EuroCup Women, national teams)](https://www.fiba.basketball/en/events/fiba-europe-cup-26-27): schedule, live, result, photos; live; tier 1 (live box scores; times shown in UTC: convert)
    - [FIBA EuroCup Women](https://www.fiba.basketball/en/events/eurocup-women-26-27): schedule, live, result; live; tier 1
    - [Cyprus Basketball Federation news](https://www.cbf.basketball): result, news, photos; same night or next day; tier 1
    - [Kerkida basketball](https://www.kerkida.net/eidiseis/alla-spor/mpasket): result, photos; 10–15 minutes after the buzzer; tier 2
  - **National teams: men's EuroBasket 2029 pre-qualifiers (North Macedonia away 26 Nov, Austria away 29 Nov, North Macedonia home 28 Feb); women's (BIH away 11 Nov, Norway home 14 Nov, Limassol)** (international, priority A; 2026-11-11 → 2027-02-28)
    - [FIBA event pages (Europe Cup, EuroCup Women, national teams)](https://www.fiba.basketball/en/events/fiba-europe-cup-26-27): schedule, live, result, photos; live; tier 1 (live box scores; times shown in UTC: convert)
    - [Cyprus Basketball Federation news](https://www.cbf.basketball): result, news, photos; same night or next day; tier 1
    - [Kerkida basketball](https://www.kerkida.net/eidiseis/alla-spor/mpasket): result, photos; 10–15 minutes after the buzzer; tier 2
  - **Women's Division A (AEL four-time champions), men's and women's cups and super cups** (domestic, priority C; dates to confirm)
    - [CBF results system (eCBF)](http://cbfweb.org/eCBF/pubgames.aspx): schedule, result; after the game; tier 1 (http only; competition, round and season dropdowns; current club names)
    - [CBF women's championship](https://www.cbf.basketball/el/womens-championship): result; ; tier 1
    - [Kerkida basketball](https://www.kerkida.net/eidiseis/alla-spor/mpasket): result, photos; 10–15 minutes after the buzzer; tier 2
- **Photos appear first at:** CBF news photos (uncredited: credit "Cyprus Basketball Federation"), FIBA galleries, Kerkida, club sites (keravnosbc.com, aek.com.cy).
- **People to follow:** Aeneas Jung (VfL Kirchheim Knights (Germany)).
- **Sport-wide sources:** [Cyprus Basketball Federation news](https://www.cbf.basketball); [Kerkida basketball](https://www.kerkida.net/eidiseis/alla-spor/mpasket).

## 3. Volleyball (indoor and beach)

- **Governing body:** Cyprus Volleyball Federation (CVF). Site: https://volleyball.org.cy (updated daily; today, next games, results and tables pages). Handles: @cyprus.volleyball.federation (Instagram), facebook.com/cyprusvolleyballfederation, @CyprusVolley (X), YouTube (linked from volleyball.org.cy).
- **Competitions we track:**
  - **Allwyn A Division men (8 teams; starts Fri 6 Nov 2026, Fridays 20:00) and League Cup "Giorgos Dimitriou"** (domestic, priority B; 2026-11-06 → 2027-05 (end estimated); usual days Fri, Mon)
    - Teams: Anorthosis, APOEL, Anagennisi Derynia, AE Karava, Nea Salamina, Omonia, Pafiakos, Foinikas Pylas. Omonia won the Super Cup 3-1 v Pafiakos (16 Oct). Live on RIK and AlfaSports.TV.
    - [CVF results](https://volleyball.org.cy/archives/calendar/recent-results): result; same night; tier 1
    - [CVF next games](https://volleyball.org.cy/next-games): schedule; ; tier 1
    - [CVF live scores (DataProject)](https://kop-web.dataproject.com/MainLiveScore.aspx): live; live; tier 1 (JavaScript-heavy)
    - [Kerkida volleyball](https://www.kerkida.net/eidiseis/alla-spor/petosfaira): result, photos; within about 2 hours; tier 2 (same-night photo galleries)
  - **Allwyn A Division women (8 teams; starts Tue 10 Nov 2026, Tuesdays 20:00); AEL won the Super Cup 3-2 (19 Oct)** (domestic, priority C; 2026-11-10 → 2027-05 (end estimated); usual days Tue, Sat)
    - [CVF results](https://volleyball.org.cy/archives/calendar/recent-results): result; same night; tier 1
    - [Kerkida volleyball](https://www.kerkida.net/eidiseis/alla-spor/petosfaira): result, photos; within about 2 hours; tier 2 (same-night photo galleries)
  - **CEV: Pafiakos (men's Champions League early rounds; lost the home leg 1-3 to Mladost Zagreb), Olympiada Neapolis (women's Challenge Cup, at Dinamo Zagreb 3 Nov)** (international, priority B; 2026-10-20 → 2027-03)
    - [CEV competition pages (old site)](https://www-old.cev.eu/Competition-Area/competition.aspx?ID=1947&PID=3533): schedule, result; same day; tier 1 (the new cev.eu pages return no data when fetched)
    - [CEV live scores](https://livescores.cev.eu): live; live; tier 1
    - [Kerkida volleyball](https://www.kerkida.net/eidiseis/alla-spor/petosfaira): result, photos; within about 2 hours; tier 2 (same-night photo galleries)
  - **Beach volleyball: national tour (summer, Limassol), CEV and FIVB events** (mixed, priority C; 2027-05 → 2027-08)
    - [CVF beach events](https://volleyball.org.cy/bvb-events): schedule, result; ; tier 1
    - [CEV beach rankings](https://www.cev.eu/beach/rankings/): ranking; ; tier 1
- **Photos appear first at:** Kerkida galleries the same night; CVF Instagram/Facebook; CEV for European ties.
- **People to follow:** Manolina Konstantinou (outside hitter; Olympiacos Piraeus per Wikipedia (confirm with the club)).
- **Sport-wide sources:** [Super Sport 104 (ex Sport FM)](https://supersport104.com/category/alla-athlhmata/).

## 4. Athletics and running

- **Governing body:** KOEAS (Cyprus Amateur Athletic Association). Site: https://www.koeas.org.cy (very active, dated news). Handles: @koeas (Instagram) and facebook.com/koeas.cy (linked from koeas.org.cy).
- **Competitions we track:**
  - **KOEAS road-race series, national championships (track Apr–Jul), Larnaca Marathon (Nov), XM Limassol Marathon (3–4 Apr 2027)** (domestic, priority C; year-round)
    - [KOEAS results 2026](https://www.koeas.org.cy): schedule, result; same or next day; tier 1
    - [World Athletics](https://worldathletics.org/competition/calendar-results): result; hours; tier 1
    - [Politis Gipedo athletics](https://gipedo.politis.com.cy/alla-sport/stivos): news, result; same day; tier 2
  - **European Athletics Indoors (Valencia, 4–7 Mar 2027), Balkan championships, European Games (Istanbul, 16–27 Jun 2027), Diamond League and World Indoor Tour** (international, priority B; year-round)
    - [World Athletics](https://worldathletics.org/competition/calendar-results): schedule, live, result; live; tier 1
    - [European Athletics](https://www.european-athletics.com): schedule, result, photos; live; tier 1
    - [Cyprus Mail athletics](https://cyprus-mail.com/category/sport/athletics): news, result; same day; tier 2
    - [KOEAS](https://www.koeas.org.cy): news; same or next day; tier 1
- **Photos appear first at:** @koeas first; World Athletics and European Athletics galleries.
- **People to follow:** Iosif Kesidis (hammer, world No. 12, Taranto gold); Elena Kulichenko (high jump, world No. 22); Filippa Fotopoulou (long jump, Taranto gold (not Olivia)); Milan Trajkovic (110 m / 60 m hurdles); Marina Hadjicosta (discus, born 2009, World U20 bronze); Olivia Fotopoulou (200 m).
- **Sport-wide sources:** [KOEAS](https://www.koeas.org.cy).

## 5. Shooting (shotgun)

- **Governing body:** Shooting Sport Federation of Cyprus. Site: cssf-shooting.org (robots.txt refuses fetching: do not fetch). Handles: UNCONFIRMED.
- **Competitions we track:**
  - **ISSF World Championship (Doha, 1–14 Nov 2026), World Cup Final (Rome, 3–8 Dec), World Cups, European Shotgun Championships; Junior Worlds Shotgun in Larnaca (7–16 May 2027)** (international, priority B; year-round)
    - [ISSF competitions](https://www.issf-sports.org/competitions): schedule, live, result, photos; live; tier 1
    - [ISSF athlete pages](https://www.issf-sports.org/athletes/SHCYPW1904198401): ranking; ; tier 1
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
    - [Politis English sport](https://en.politis.com.cy/news/sports/): news, result; same day; tier 2 (name errors seen (Taranto list): cross-check names)
- **Photos appear first at:** ISSF competition galleries (issf-sports.org/competitions/<id>/galleries).
- **People to follow:** Konstantia Nikolaou (skeet, ISSF world ranking 9 (ISSF spelling; not "Konstantina")); Nicolas Vasiliou (skeet, Taranto bronze); Andreas Pontikis (skeet, European U23 champion 2026).
- **Sport-wide sources:** [ISSF](https://www.issf-sports.org).

## 6. Sailing

- **Governing body:** Cyprus Sailing Federation (CYSAF). Site: https://www.cysaf.org.cy (poorly maintained, undated news). Handles: @cyprus_sailing_federation (Instagram), facebook.com/CyprusSailingFederation (linked from cysaf.org.cy).
- **Competitions we track:**
  - **ILCA 7 circuit: Grand Slams (Palma, Hyères, Los Angeles), European and World Championships** (international, priority B; 2027-03 → 2027-08)
    - [Regatta results sites (e.g. ilca-worlds.org)](https://www.ilca-worlds.org): live, result; same day; tier 1
    - [World Sailing](https://www.sailing.org): news, ranking, photos; same day; tier 1
    - [Cyprus Mail: Kontides tag](https://cyprus-mail.com/tag/pavlos-kontides/): news; same day; tier 2 (tag page lags)
    - [Politis English sport](https://en.politis.com.cy/news/sports/): news, result; same day; tier 2 (name errors seen (Taranto list): cross-check names)
  - **National championship series and regattas in Cyprus** (domestic, priority C; year-round)
    - [CYSAF results](https://www.cysaf.org.cy/championships/national-championships/results/): result; slow; tier 1
    - [CYSAF calendar](https://www.cysaf.org.cy/championships/national-championships/calendar/): schedule; slow; tier 1
- **Photos appear first at:** event photographers on the regatta sites, World Sailing, CYSAF Instagram.
- **People to follow:** Pavlos Kontides (ILCA 7; 2026 European champion; 2x Olympic silver).
- **Sport-wide sources:** [World Sailing](https://www.sailing.org).

## 7. Gymnastics (artistic and rhythmic)

- **Governing body:** Cyprus Gymnastics Federation. Site: none found. Handles: UNCONFIRMED (no website found).
- **Competitions we track:**
  - **FIG World Championships (Rotterdam, 17–25 Oct 2026; finals 24–25 Oct), World Cups and World Challenge Cups, European Championships, European Games 2027** (international, priority B; year-round)
    - [FIG events and results](https://www.gymnastics.sport/site/events/searchresults.php): schedule, result; same day; tier 1 (FIG live scoring (live.gymnastics.sport) is robots-disallowed: never read it)
    - [European Gymnastics](https://www.europeangymnastics.com): result, news; same day; tier 1
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
    - [Sigmalive English](https://en.sigmalive.com/category/sports/): news; same day; tier 2 (sometimes first in English; some items undated)
- **Photos appear first at:** FIG and European Gymnastics galleries; CNA.
- **People to follow:** Marios Georgiou (artistic; European horizontal bar silver 2026; Taranto all-around gold); Neofytos Kyriakou (artistic); Vera Tugolukova (rhythmic).
- **Sport-wide sources:** [CNA (Cyprus News Agency)](https://www.cna.org.cy/en).

## 8. Judo

- **Governing body:** Pancyprian Judo Federation. Site: none found. Handles: UNCONFIRMED (no website found).
- **Competitions we track:**
  - **IJF World Tour (Zagreb GP 13–15 Nov, Tokyo GS 5–6 Dec), Junior Worlds (Tashkent 19–21 Nov), Masters, European Championships 2027 (Apeldoorn), European Games** (international, priority B; year-round)
    - [IJF country page (entries, rankings)](https://www.ijf.org/index.php/country/cyp): schedule, result, ranking; live; tier 1
    - [JudoBase](https://judobase.ijf.org): live, result; live; tier 1
    - [EJU](https://www.eju.net): result, news; same day; tier 1
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
- **Photos appear first at:** IJF media gallery.
- **People to follow:** Sofia Asvesta (−52 kg, IJF 20, Taranto gold); Giannis Antoniou (+100 kg, IJF 21, Commonwealth gold); Petros Christodoulides (−66 kg, Taranto silver).
- **Sport-wide sources:** [IJF](https://www.ijf.org).

## 9. Handball

- **Governing body:** Cyprus Handball Federation (CHF). Site: https://chf.com.cy (active; standings on the homepage). Handles: instagram.com/cyprushandballfederation, facebook.com/cyprushandballfederation, YouTube (linked from chf.com.cy).
- **Competitions we track:**
  - **Allwyn A Division men and women (round 1 postponed on 19 Oct after an arson attack on a referee; new date not set); men's B from 10 Nov** (domestic, priority C; 2026-10-24 → 2027-07 (end estimated))
    - The arson attack on referee Giorgos Panayides is a violence story: AMBER only (PLAYBOOK 5).
    - [CHF](https://chf.com.cy): schedule, result, table; same day; tier 1
    - [Politis handball](https://gipedo.politis.com.cy/alla-sport/handball): result, news; same day; tier 2
    - [Super Sport 104 (ex Sport FM)](https://supersport104.com/category/alla-athlhmata/): news, result; not measured; tier 2
  - **EHF European Cup: Sabbianco Anorthosis (lost 21-37 at AEK Athens; return leg Sun 25 Oct, Kition, Larnaca: time to confirm)** (international, priority B; 2026-09-12 → 2027-05-30)
    - [EHF European Cup news](https://ehfec.eurohandball.com/men/2026-27/): schedule, result; same day; tier 1 (match pages are JavaScript templates)
    - [CHF](https://chf.com.cy): result; same day; tier 1
    - [Politis handball](https://gipedo.politis.com.cy/alla-sport/handball): result, news; same day; tier 2
- **Photos appear first at:** CHF site and social accounts; Politis (copies CHF releases).
- **Sport-wide sources:** [Politis handball](https://gipedo.politis.com.cy/alla-sport/handball).

## 10. Motorsport

- **Governing body:** Cyprus Automobile Association (FIA member) and the Cyprus Motorsport Federation. Site: cyprusaa.org (robots.txt refuses fetching: do not fetch); federation site not found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **52nd Petrolina Cyprus Rally (23–25 Oct 2026, Larnaca; final round of the FIA Middle East Rally Championship)** (international, priority A; 2026-10-23 → 2026-10-25)
    - The 2025 rally was cancelled after the FIA declared Cypriot competitions unrecognised (licence dispute): handle history with care.
    - [Speed & Rally live results](https://www.cyprusspeedrallyresults.com/rally/d9f1d263-c54a-4774-b91f-c813ad85aa0b): live, result; live; tier 1 (official timing; MERC and local classifications)
    - [Cyprus Rally](https://www.cyprusrally.com.cy/en/results-2026): schedule, result, news; event week; tier 1
    - [FIA MERC](https://www.fia.com/championship/middle-east-rally-championship): result, photos; same day; tier 1 (its calendar dates for Cyprus are stale)
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2
  - **Cyprus Rally Championship, Pancyprian Hill Climb Championship, time attack, karting** (domestic, priority C; dates to confirm)
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
    - [EKO press releases (hill climb, time attack)](https://www.eko.com.cy/en/ta-nea-mas/deltia-typou/): news; fast; tier 3 (sponsor PR: tip only, confirm elsewhere)
  - **NASCAR Euro Series (Vladimiros Tziortzis: OPEN and V8GP) and Cypriots in other series** (abroad, priority B; 2027-04 → 2027-10)
    - [EuroNASCAR](https://www.euronascar.com): schedule, result; same day; tier 1
    - [Cyprus Mail](https://cyprus-mail.com/category/sport/other-sport): news; same day; tier 2
- **Photos appear first at:** Cyprus Rally Facebook, Cyprus Mail, FIA MERC; Tziortzis via EuroNASCAR.
- **People to follow:** Vladimiros Tziortzis (NASCAR Euro Series (OPEN and V8GP); his "3rd overall" claim comes only from his own release: not confirmed by the series (PLAYBOOK 10, 22 Oct)); Simos Galatariotis / Panayiotis Yiangou (rally (Rally2)).
- **Sport-wide sources:** [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport).

## 11. Swimming

- **Governing body:** KOEK (Cyprus Swimming Federation). Site: https://koek.org.cy (very active). Handles: @koekfed (Instagram) and a Flickr photo account (linked from koek.org.cy).
- **Competitions we track:**
  - **World Aquatics Swimming Championships 25 m (Beijing, 1–6 Dec 2026), European championships, European Games 2027** (international, priority B; year-round)
    - [World Aquatics](https://www.worldaquatics.com): schedule, live, result; live; tier 1
    - [KOEK](https://koek.org.cy): news, result; same or next day; tier 1
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
  - **National championships, open-water cups (Protaras, 24 Oct), masters meets** (domestic, priority C; year-round)
    - [KOEK results](https://koek.org.cy): result; same or next day; tier 1
    - [Kerkida other sports](https://www.kerkida.net/eidiseis/alla-spor): news, result; hours; tier 2
- **Photos appear first at:** KOEK Flickr and Instagram; World Aquatics.
- **People to follow:** Kalia Antoniou (sprint free/fly, two Taranto golds).
- **Sport-wide sources:** [KOEK](https://koek.org.cy).

## 12. Water polo

- **Governing body:** KOEK (Cyprus Swimming Federation). Site: https://koek.org.cy. Handles: @koekfed (Instagram), Flickr (linked from koek.org.cy).
- **Competitions we track:**
  - **Allwyn men's championship (8 teams; NO Keryneia back after 21 years): Super Cup APOEL v Larnaca Fri 13 Nov, matchday 1 Sun 15 Nov** (domestic, priority C; 2026-11-13 → 2027-05 (end estimated); usual days Sat, Sun)
    - [KOEK news](https://koek.org.cy): schedule, news; days; tier 1
    - [KOEK water polo results](https://koek.org.cy/archiki-selida/idatosferisi/apotelesmata-agonon-vathmologies/): result, table; slow; tier 1
    - [Super Sport 104 (ex Sport FM)](https://supersport104.com/category/alla-athlhmata/): news, result; not measured; tier 2
- **Photos appear first at:** KOEK Flickr and Instagram.

## 13. Tennis and padel

- **Governing body:** Cyprus Tennis Federation (also runs padel). Site: https://www.tennis.com.cy (weak: undated, no results). Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Davis Cup World Group II, Round 1: Cyprus v Puerto Rico (6–8 Feb 2027); Billie Jean King Cup** (international, priority A; 2027-02-06 → 2027-02-08)
    - [Davis Cup](https://www.daviscup.com): schedule, live, result; live; tier 1
    - [Kerkida tennis](https://www.kerkida.net/eidiseis/alla-spor/tennis): news; same day; tier 2
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
  - **ITF / ATP / WTA events with Cypriot players; padel tour** (international, priority C; year-round)
    - [ITF](https://www.itftennis.com): result; next day; tier 1 (ranking fields need JavaScript)
    - [Politis Gipedo tennis](https://gipedo.politis.com.cy/alla-sport/tenis): news; same day; tier 2
- **People to follow:** Petros Chrysochos (ITF career-high 354; also padel); Lefteris Neos / Melios Efstathiou (Taranto doubles bronze).

## 14. Cycling

- **Governing body:** Cyprus Cycling Federation (KOP). Site: https://www.cypruscycling.org (very active; 2027 calendar published). Handles: facebook.com/cypruscyclingfederation and YouTube (linked from its site); no Instagram listed.
- **Competitions we track:**
  - **Cyprus Mediterranean Challenge MTB Cups (31 Jan–7 Feb 2027), road cups, national championships (ITT 23 Jun, road 27 Jun 2027), Troodos MTB (17–18 Jul)** (domestic, priority C; 2027-01-31 → 2027-07-18)
    - [KOP news and results PDFs](https://www.cypruscycling.org): schedule, result, photos; 1–5 days; tier 1
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
  - **UCI World and European championships, U23 road racing** (international, priority C; dates to confirm)
    - [UCI](https://www.uci.org): result; live; tier 1
    - [KOP](https://www.cypruscycling.org): news, result; 1–5 days; tier 1
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
- **Photos appear first at:** KOP site albums and Facebook.
- **People to follow:** Bogdan Zabelinskiy (U23 ITT 8th at the 2026 Worlds; Taranto silver (UCI spelling to check)).

## 15. Rugby union

- **Governing body:** Cyprus Rugby Federation (the Mouflons). Site: https://www.cyprus-rugby.com (English, active). Handles: @cyprus_rugby (Instagram), @Cyprus_Rugby (X), facebook.com/CyprusRugby (linked from its site).
- Cyprus held the world record of 24 straight Test wins (ended Nov 2014): archive material.
- **Competitions we track:**
  - **Rugby Europe Men's Conference Pool D (won 48-17 in Gibraltar, 17 Oct; next Cyprus v Israel 3 Apr 2027, Andorra v Cyprus 17 Apr)** (international, priority B; 2026-10-17 → 2027-04-17)
    - [Rugby Europe](https://www.rugbyeurope.eu/competitions/season-2627/xv-competitions/mens-xv-competitions/mens-conference-202627/): schedule, result, table; same day; tier 1
    - [CRF news](https://www.cyprus-rugby.com/updates): result, news; 1–3 days; tier 1
    - [Cyprus Mail rugby](https://cyprus-mail.com/category/sport/rugby): news; about 2 days; tier 2
  - **Cyprus Rugby Championship (5 teams incl. British Forces sides), Rugby Cup, 7s and beach championships; men's 7s (2026 Conference 1 bronze)** (domestic, priority C; dates to confirm)
    - [CRF club rugby](https://www.cyprus-rugby.com/club-rugby/cyprus-rugby-championship): schedule, result; ; tier 1
    - [Cyprus Mail rugby](https://cyprus-mail.com/category/sport/rugby): news; ; tier 2
- **Photos appear first at:** CRF Instagram/Facebook and WhatsApp channel; Cyprus Mail.

## 16. Karate, taekwondo, boxing, MMA and wrestling

- **Governing body:** Cyprus Karate Federation (cypruskarate.org, undated posts); taekwondo, wrestling and boxing federations have no websites. Site: http://www.cypruskarate.org. Handles: UNCONFIRMED.
- Charalampos Grigoriou (UFC) is listed "Not Fighting" since Aug 2024: never present him as active.
- "Wrestling" in Cyprus Mail is often Pro Wrestling Cyprus (entertainment), not Olympic wrestling.
- **Competitions we track:**
  - **EKF/WKF karate, World Taekwondo, UWW events; European Games 2027 (karate, taekwondo, wrestling, boxing, kickboxing, muaythai)** (international, priority C; dates to confirm)
    - [European Karate Federation](https://2022.europeankaratefederation.net): news, result; same day; tier 1
    - [World Taekwondo](https://www.worldtaekwondo.org): result; ; tier 1
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
- **People to follow:** Sissy Yamouki (karate +68 kg, Taranto bronze (WKF spelling to check)).

## 17. Fencing

- **Governing body:** Cyprus Fencing Federation. Site: http://www.fencing.org.cy (updated Sep 2026; results and rankings pages). Handles: X @CYFencing (linked from its site).
- **Competitions we track:**
  - **FIE World Cups (Nov 2026–Jun 2027), European championships, Commonwealth Fencing Championships** (international, priority C; 2026-11 → 2027-07)
    - [FIE](https://fie.org): schedule, result; ; tier 1
    - [Cyprus Fencing Federation](http://www.fencing.org.cy): result, news; days; tier 1
    - [Sigmalive English](https://en.sigmalive.com/category/sports/): news; same day; tier 2 (sometimes first in English; some items undated)
- **People to follow:** Alexandros Tofalides (foil; Commonwealth Fencing champion 2026; Paris 2024 Olympian).

## 18. Archery and para archery

- **Governing body:** Cyprus Archery Federation. Site: http://www.archery.org.cy (active, Oct 2026). Handles: UNCONFIRMED (footer icons are placeholders).
- **Competitions we track:**
  - **Aphrodite Mediterranean Archery & Para Cup (Pyla/Larnaca, 28–31 Oct 2026); World Archery and Para Series** (mixed, priority C; 2026-10-28 → 2026-10-31)
    - [Cyprus Archery Federation](http://www.archery.org.cy): schedule, news; days; tier 1
    - [World Archery](https://www.worldarchery.sport): result; ; tier 1
    - [Kerkida other sports](https://www.kerkida.net/eidiseis/alla-spor): news, result; hours; tier 2
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
- **People to follow:** Christos Misos (para archery VI1, world champion and No. 1).

## 19. Cricket

- **Governing body:** Cyprus Cricket (calls itself the Cyprus Cricket Federation; ICC Associate per Wikipedia). Site: https://www.cricket.cy (few posts). Handles: @cypruscricket on Instagram, X, Facebook, TikTok and Threads (linked from cricket.cy).
- **Season:** Apr–Oct.
- **Competitions we track:**
  - **T20, 40-over and T10 cups at Happy Valley, Episkopi; men's and women's internationals (women 37th in the ICC T20I rankings)** (mixed, priority C; 2027-04 → 2027-10)
    - [Cyprus Mail cricket](https://cyprus-mail.com/category/sport/cricket): result, news; weekly (Mondays); tier 2
    - [cricket.cy](https://www.cricket.cy/category/news/): news; slow; tier 1
    - [ICC media releases](https://www.icc-cricket.com/media-releases): news, result; ; tier 1

## 20. Para sport

- **Governing body:** Cyprus National Paralympic Committee. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **World Para championships and series (archery, swimming, athletics, powerlifting)** (international, priority C; dates to confirm)
    - [IPC](https://www.paralympic.org): result, news; ; tier 1
    - [Sigmalive English Paralympics tag](https://en.sigmalive.com/tag/paralympics): news; same day; tier 2
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)
- **People to follow:** Karolina Pelendritou (para swimming, Paris 2024 medallist); Maria Markou (para powerlifting).

## 21. Weightlifting

- **Governing body:** Cyprus Weightlifting Federation. Site: http://www.weightlifting.org.cy (active). Handles: Facebook and YouTube linked from its site.
- **Competitions we track:**
  - **IWF and European championships, Pancyprian championships** (mixed, priority C; dates to confirm)
    - [Weightlifting federation](http://www.weightlifting.org.cy): news, result; days; tier 1
    - [IWF](https://iwf.sport): result; ; tier 1
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
- **People to follow:** Dimitris Minasidis (weightlifting).

## 22. Skiing

- **Governing body:** Cyprus Ski Federation. Site: http://www.cyprusski.com (undated). Handles: UNCONFIRMED.
- **Season:** Jan–Mar on Troodos.
- **Competitions we track:**
  - **FIS race on Troodos (Zeus piste) and FIS races abroad** (mixed, priority C; 2027-01 → 2027-03)
    - [FIS](https://www.fis-ski.com): result; live; tier 1
    - [Cyprus Ski Federation](http://www.cyprusski.com): news; slow; tier 1
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
- **People to follow:** Yianno Kouyoumdjian (alpine, Milano Cortina slalom 34th).

## 23. Canoe and rowing

- **Governing body:** Canoe (no website); Cyprus Rowing Federation (site stale since 2018). Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **ICF World Cups, European and World championships** (international, priority C; dates to confirm)
    - [ICF rankings and results](https://rankings.canoeicf.com/athlete/87038/competitions): result; ; tier 1
    - [Canoe ICF](https://www.canoeicf.com): schedule, result; ; tier 1
    - [Cyprus Mail other sport](https://cyprus-mail.com/category/sport/other-sport): news, result; same day; tier 2 (full text; often CNA copy; cover photos usually uncredited)
- **People to follow:** Savvia Hadjicharalambous (canoe K1 500 m, Taranto silver (ICF spelling)).

## 24. Chess

- **Governing body:** Cyprus Chess Federation. Site: none found. Handles: UNCONFIRMED.
- The 2026 Olympiad "silver" was a Category D prize (91st of 189 overall): always say so.
- **Competitions we track:**
  - **Cyprus Open, Olympiad, youth world championships** (mixed, priority C; year-round)
    - [FIDE](https://www.fide.com): news, result; ; tier 1
    - [chess-results.com](https://chess-results.com): live, result; live; tier 2
    - [Cyprus Mail chess](https://cyprus-mail.com): news; weekly; tier 2

## 25. Multi-sport Games and the Olympic movement

- **Governing body:** Cyprus Olympic Committee (KOE); Cyprus National Paralympic Committee; Cyprus Sport Organisation (KOA). Site: https://www.olympic.org.cy (Greek, updated); paralympic.org.cy refuses fetching (robots.txt); cyprussports.org errors. Handles: @cyprusolympic on Instagram, X, Facebook and YouTube (linked from olympic.org.cy).
- **Competitions we track:**
  - **Youth Olympic Games Dakar (31 Oct–13 Nov 2026; 7 Cypriots in 6 sports), Games of the Small States of Europe (Monaco, 17–22 May 2027), European Games (Istanbul, 16–27 Jun 2027: Cyprus participation UNCONFIRMED and politically sensitive), LA28 qualifying** (international, priority B; dates to confirm)
    - [Cyprus Olympic Committee news](https://www.olympic.org.cy/index.php/gr/news): news, result; 1–3 days; tier 1
    - [Olympics.com](https://www.olympics.com): schedule, result; live; tier 1
    - [CNA (Cyprus News Agency)](https://www.cna.org.cy/en): news, result; same day; tier 2 (headline and lede only (paywall); no sport category)

## Dated events (also in the JSON; `tools/sweep.py week` lists them)

| Date | Sport | Event | Who | Confirmed |
|---|---|---|---|---|
| 2026-10-23 → 2026-10-25 | motorsport | 52nd Petrolina Cyprus Rally, Larnaca (MERC title decider; finish Sun 25 Oct 17:00) | Yiangou, Galatariotis | yes |
| 2026-10-24 → 2026-10-25 | gymnastics | Artistic Gymnastics World Championships, apparatus finals, Rotterdam | Marios Georgiou if qualified | yes |
| 2026-10-25 | handball | EHF European Cup R2 return leg: Sabbianco Anorthosis v AEK Athens, Kition, Larnaca (first leg 21-37; time 19:00 or 20:15: confirm) |  | yes |
| 2026-10-27 → 2026-11-02 | football | U17: Cyprus v Japan (friendly), then EURO qualifiers v Faroe Islands (30 Oct) and Romania (2 Nov), 15:00, Achna |  | yes |
| 2026-10-28 → 2026-10-31 | archery | Aphrodite Mediterranean Archery & Para Cup, Pyla/Larnaca | Christos Misos | yes |
| 2026-10-31 → 2026-11-13 | multi-sport | Youth Olympic Games, Dakar (7 Cypriots in 6 sports) |  | yes |
| 2026-11-01 → 2026-11-14 | shooting | ISSF World Championship, Doha (first LA28 quota event) | Nikolaou, Vasiliou, Pontikis if selected | yes |
| 2026-11-03 | volleyball | CEV women's Challenge Cup: Dinamo Zagreb v Olympiada Neapolis, 18:00 |  | yes |
| 2026-11-05 | football | Europa League: N.E.C. v Omonia; Conference League: Twente v Pafos |  | yes |
| 2026-11-06 | volleyball | Allwyn A Division men starts (women Tue 10 Nov) |  | yes |
| 2026-11-11 → 2026-11-14 | basketball | Women's EuroBasket pre-qualifiers: Bosnia and Herzegovina v Cyprus (Sarajevo); Cyprus v Norway Sat 14 Nov, Limassol |  | yes |
| 2026-11-11 → 2026-11-17 | football | U19 EURO qualifying Round 2 hosted in Cyprus (v Armenia, Albania): dates to confirm |  | to confirm |
| 2026-11-12 | football | Nations League: Armenia v Cyprus, 19:00 Cyprus time (a point secures 2nd) | national team | yes |
| 2026-11-13 → 2026-11-15 | water-polo | Super Cup APOEL v NO Larnaca; league matchday 1 on Sun 15 Nov |  | yes |
| 2026-11-13 → 2026-11-15 | judo | Zagreb Grand Prix (6 Cypriots entered) |  | yes |
| 2026-11-15 | football | Nations League: Cyprus v Montenegro, 16:00 (decides 1st/2nd place) | national team | yes |
| 2026-11-15 | athletics | Radisson Hotels Larnaka Marathon |  | yes |
| 2026-11-26 → 2026-11-29 | basketball | Men's EuroBasket 2029 pre-qualifiers: North Macedonia v Cyprus (Skopje); Austria v Cyprus Sun 29 Nov (Vienna) |  | yes |
| 2026-11-26 | football | Europa League: Juventus v Omonia; Conference League: Pafos v Midtjylland |  | yes |
| 2026-12-01 → 2026-12-06 | swimming | World Aquatics Swimming Championships (25 m), Beijing | Kalia Antoniou if selected | yes |
| 2026-12-05 → 2026-12-06 | judo | Tokyo Grand Slam (5 Cypriots entered) |  | yes |
| 2026-12-06 | football | EURO 2028 qualifying draw, Belfast |  | yes |
| 2026-12-10 | football | Europa League: Omonia v Celtic; Conference League: Mjällby v Pafos (Pafos v Hearts 17 Dec) |  | yes |
| 2027-01-24 | athletics | Bank of Cyprus Nicosia Marathon |  | yes |
| 2027-01-31 → 2027-02-07 | cycling | Cyprus Mediterranean Challenge MTB (UCI), Tochni and Pyrga |  | yes |
| 2027-02-06 → 2027-02-08 | tennis | Davis Cup World Group II R1: Cyprus v Puerto Rico (venue to confirm) |  | yes |
| 2027-02-18 → 2027-02-25 | football | Conference League knockout play-offs (if Pafos finish 9th–24th) |  | yes |
| 2027-02-28 | basketball | Men's EuroBasket pre-qualifiers: Cyprus v North Macedonia |  | yes |
| 2027-03-04 → 2027-03-07 | athletics | European Athletics Indoor Championships, Valencia (confirm dates with European Athletics) | Kulichenko, F. Fotopoulou, Trajkovic | to confirm |
| 2027-04-03 → 2027-04-04 | athletics | XM Limassol Marathon |  | yes |
| 2027-05-07 → 2027-05-16 | shooting | ISSF Junior World Championship Shotgun, Larnaca |  | yes |
| 2027-05-17 → 2027-05-22 | multi-sport | Games of the Small States of Europe, Monaco |  | yes |

## Gaps to close (weekly desk, step 6a)

- Instagram handles for most clubs (basketball clubs except Keravnos; Omonia 29M, Nea Salamina, Krasava, Karmiotissa in football; all volleyball, handball, water polo and cricket clubs) and for every athlete except Vladimiros Tziortzis.
- Football: Cup second phase and final; Second/Third Division formats; First Division matchday 17–26 dates; venue of Cyprus v Montenegro; women's national team November friendlies; U19 Round 2 dates; why UEFA lists coach Mantzios as suspended.
- Basketball: cup formats and dates; women's league start; ENBL schedule; FIBA Europe Cup second round; men's head coach.
- Volleyball: 2025-26 champions; Pafiakos return-leg date; national-team calendar. Handball: new date for A Division round 1; 2026-27 team lists. Water polo: women's league, cup, European entry.
- Motorsport: the federation's site and the domestic rally, hill-climb and karting calendars (cyprusaa.org refuses fetching).
- Individual sports: websites for the judo, taekwondo, gymnastics, wrestling and boxing federations and the Paralympic Committee (its site refuses fetching); most 2027 international calendars; ATP/WTA rankings need a manual check.
- Names of the 7 Cypriots at the Dakar Youth Olympics; whether Cyprus attends the 2027 European Games (sensitive).
- Fan pages that break news fast (tips only, tier 3) and follower counts beyond the football clubs.
