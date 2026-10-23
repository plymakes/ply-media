# Lebanon sports map: the top 20 sports, every competition we track, and the fast sources

Geoffry's brief (23 Oct 2026): "do a deep study into allllllll sports that lebanese participate on local leagues, and international ones. and for every sport check all the tournaments and league to keep track off. those should be listed to go over everytime we'll cover the top 20 sports in lebanon … clubs and individual sports. cover alll games as well … for each sport/ league find multiple viable sources that post fastly about events so we can rely on them for schedules, events, scores, results, and images."

- **Data:** `sources/lebanon-sports.json` (what `tools/sweep.py` reads). This file is the readable version; when they disagree, fix both.
- **Every run:** `python3 tools/sweep.py today` walks all 20 sports in this order with their live competitions, today's dated events, the athletes to look up and the sources to open. `python3 tools/sweep.py coverage` shows which sports are overdue on @sportswire.lb. Every LB spec names its `sport` with an id from the JSON (the gate checks).
- **Weekly upkeep:** RUNBOOK section 3, step 6a: new dates, season starts and ends, dead or slow sources, handles, and the UNCONFIRMED items below.
- **Research:** four parallel researchers on 23 Oct 2026 (basketball and football; other team sports; individual and Olympic sports; motorsport, diaspora, multi-sport and outlets), with WebSearch and WebFetch only. Wikipedia was used as a lead only. Instagram and X can't be fetched, so **no social handle or follower count could be confirmed by fetching**; handles below come from the organisation's own website or are marked UNCONFIRMED. A source listed here is where to look, not proof: every fact still needs PLAYBOOK section 4 (one tier 1, or two tier 2 on different sites).
- **Context:** war resumed in Lebanon on 2 March 2026 (L'Orient Today); leagues were halted and restarted at short notice (handball restarted 1 Oct; the 2025-26 volleyball season finished in July). Expect postponements and late schedule changes; confirm every date and time on the day. Never frame a postponement politically (PLAYBOOK section 5).

## How the ranking was made

Following and media attention in Lebanon (how often the established outlets cover the sport, crowds, federation and club activity), how much is happening in the season ahead (live leagues, national-team windows, championships), and current Lebanese results and names (medals, world titles, athletes abroad). Cover frequency follows the rank: the top sports appear several times a week, the rest at least every two to five weeks through results, spotlights, quizzes, votes or the archive series.

## The top 20 (rank order = sweep order)

| # | Sport | Cover at least every | Why it ranks here |
|---|---|---|---|
| 1 | Basketball | 2 days | The biggest following (@alriyadiclub ~173K, @flb_official ~124K on HypeAuditor), Lebanese clubs winning WASL and the Arab Club Championship in October 2026, Division A from 24 Oct, FIBA qualifiers in November and February. |
| 2 | Football (incl. futsal, women's and beach) | 2 days | National sport by volume of coverage (@thelfadotcom ~68K), Premier League every weekend from 8 Oct, Ansar and Nejmeh in the AFC Challenge League, players abroad in Europe. |
| 3 | Rugby league | 7 days | Lebanon at the 2026 World Cup now (France on 1 Nov), the heaviest English-language coverage of any Lebanese sport, NRL stars with Lebanese heritage. |
| 4 | Volleyball (indoor and beach) | 7 days | Biggest domestic team sport after the top two: 12-team men's league with a five-game final, women three-time West Asian champions, beach West Asia gold in Aug 2026. |
| 5 | MMA, muay thai and kickboxing | 14 days | High engagement: 15 IMMAF youth world medals (Aug 2026), Fatima Hassan double IFMA world champion (Sep 2026), PFL MENA and BRAVE CF cards. |
| 6 | Taekwondo | 14 days | Laetitia Aoun is a national figure (Paris 2024 quarter-final win, President calls her); the LA28 ranking cycle has started. |
| 7 | Motorsport | 14 days | Rally of Lebanon (FIA MERC) and the domestic rally and karting championships, Roger Feghali, Christopher El Feghali in Eurocup-3. |
| 8 | Shooting | 14 days | Lebanon's most decorated individual sport: Samer Sarkis won the only Lebanese gold at Taranto 2026; the ISSF World Championship in Doha (1–14 Nov) is the first LA28 quota event. |
| 9 | Tennis | 14 days | Davis Cup draws national attention (World Group I play-offs in Kazakhstan, Feb 2027); Benjamin Hassan and Hady Habib on tour. |
| 10 | Judo | 14 days | Recent medals (Aqulina Chayeb gold in Tallinn, Jun 2026; Sagaipov Asian bronze 2025); LA28 qualifying from June 2026. |
| 11 | Athletics and running | 21 days | Beirut Marathon (late Nov) and a big running community, the only federation with an updated website (flalbn.org), Aziza Sbaity and ultra record-holder Youssef Assaker. |
| 12 | Handball | 21 days | League live now (restarted 1 Oct, Final Four and final in Nov–Dec), Annahar reports almost every matchday. |
| 13 | Swimming | 21 days | Munzer Kabbara and Lynn El Hajj (national records at the 2025 Worlds; three Islamic Solidarity bronzes). |
| 14 | Skiing | 21 days | Seasonal peak Dec–Mar: FIS races at Mzaar and the Cedars, Andrea El Hayek (Milano Cortina 2026 flag bearer). |
| 15 | Table tennis | 21 days | Two-time Olympian Mariana Sahakian; Lebanese women in Arab and Asian events. |
| 16 | Teqball | 35 days | Won both of Lebanon's medals at the 2026 Asian Games (silver and bronze). |
| 17 | Karate | 35 days | Regular Arab and Asian medals (6 in Amman); Asian Indoor and Martial Arts Games in Riyadh, Dec 2026. |
| 18 | Weightlifting and powerlifting | 35 days | Etienne El Chaer's 2025 World Games powerlifting silver (Lebanon's first World Games medal); LA28 weightlifting qualifying has opened. |
| 19 | Boxing | 35 days | Pro cards in Lebanon and the region, Lebanese Army boxers; low but steady activity. |
| 20 | Para sport | 35 days | Asian Para Games (to 24 Oct 2026), Paralympian Arz Zahreddine; inclusion matters for a page that covers everyone. |

**Watch list (beyond the top 20):** Equestrian (show jumping) (FEI Arab League season Nov–Mar; Jad Dana.); Fencing (Youth medals at West Asian level; FIE season from Nov.); Chess (Active federation; Olympiad and Arab events.); Wrestling (Heritage sport (1952 Olympic medal), military championships.); Rowing, cycling, triathlon, padel, squash, golf and other small sports (Rowing (Youssef El Mays), cycling, triathlon, padel, squash, golf: cover when an event is on.); Rugby union and sevens (Federation close to dormant online (placeholder website); Dubai Sevens 28–29 Nov without a confirmed Lebanese entry.); Ice hockey (Diaspora team based in Montreal (Arab Cup 2023 champions; women bronze at the 2025 Dream Nations Cup); irregular events.); Multi-sport Games and the Olympic movement (Games where Lebanon competes across sports: Youth Olympics Dakar (31 Oct–13 Nov), Asian Indoor and Martial Arts Games (Riyadh, 13–21 Dec), Arab Games 2027, LA28 qualifying.). These come into the sweep only when one of their dated events is on.

## General fast sources (all sports)

| Source | Good for | Speed | Tier | Notes |
|---|---|---|---|---|
| [elsport](https://elsport.com) | news, schedule, result, photos | same day | 2 | fastest Lebanese all-sports outlet; fetch articles as elsport.com/news/show/<id> (long Arabic URLs fail); IG @elsportscom |
| [MTV Lebanon sport](https://www.mtv.com.lb/news/رياضة) | news, result, photos | same day, timestamped | 2 | highest share of Lebanese sport of any outlet checked |
| [Annahar sport](https://www.annahar.com/sports) | news, result, photos | same day | 2 | strong on national-team squads, handball and volleyball; robots.txt disallows /en/ and /fr/ |
| [LBCI sport](https://www.lbcgroup.tv/sports/category/107/رياضة/ar) | news, live, result | live on big nights | 2 |  |
| [L'Orient Today](https://today.lorientlejour.com) | news, result, photos | same day | 2 | best English source; metered paywall |
| [Al Jadeed sport](https://www.aljadeed.tv/news/category/1064/رياضة/ar) | news, result | same day | 2 |  |
| [NNA](https://nna-leb.gov.lb/ar) | news, result | same day | 2 | federation communiqués; article bodies often load only as headlines |
| [Lebanon24 sport](https://www.lebanon24.com/section/6/رياضة) | news | same day | 2 |  |
| [Nidaa al-Watan sport](https://www.nidaalwatan.com/section/21-الرياضة) | news | next day | 2 |  |
| [Al-Akhbar sport](https://www.al-akhbar.com) | news | next day | 2 | use the numeric article URL |
| [FotMob Lebanon](https://www.fotmob.com/teams/5897) | schedule, live, result | live | 2 | data service: scores and stats only |
| [Sofascore Lebanese Premier League](https://www.sofascore.com/tournament/football/lebanon/premier-league/2295) | live, result, table | live | 2 | data service; read the tournament and match pages only (robots.txt disallows /standings/ paths); fixtures need JavaScript |
| [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx) | schedule, result, news | same day | 2 | data service: scores and stats only; partial without subscription; crawl-delay 1 s |
| [365Scores Lebanese Premier League](https://www.365scores.com/ar/football/league/premier-league-566/standings) | live, result, table, schedule | live | 2 | data service; fetches; kick-off times |
| [Malaeeb](http://www.malaeeb.com) | schedule | 2 days ahead | 2 | round fixture lists with venues and kick-off times (D1 and D2) |

**Don't rely on:** kooora.com (Lebanon feed stale since 2022); goalzz.com (redirects to goal.com); lebolymp.org (Olympic Committee site, news stops in 2021); atcl.org.lb (robots.txt refuses fetching); Beirut Today (no sport); Flashscore /standings/, /live/, /finished/, /scheduled/ paths (robots.txt disallows them); Sofascore /standings/ paths (robots.txt disallows them).

## 1. Basketball

- **Governing body:** Lebanese Basketball Federation (FLB/FLBB; president Akram Halabi). Site: https://lebanon.basketball (not updated since 2022: use its social accounts). Handles: @flb_official (Instagram), facebook.com/LBF.basketball (both linked from lebanon.basketball).
- **Competitions we track:**
  - **Lebanese Basketball Championship, Division A (12 teams; new Final 5, best-of-5 semis, best-of-7 final; 3 foreign players)** (domestic, priority B; 2026-10-24 → 2027-06-01)
    - 2026-27 team list and weekly programme: from the FLB poster each week (12th of 2025-26, Tadamon Hrajel, presumably relegated; promoted clubs UNCONFIRMED). Riyadi v Sagesse games are priority A.
    - [FLB Instagram @flb_official](https://www.instagram.com/flb_official/): schedule, result, photos; same day; tier 1 (weekly programme posters and results; Instagram blocks automated reading: find the same post on facebook.com/LBF.basketball or in outlets, or Geoffry sends the link)
    - [FLB Facebook](https://www.facebook.com/LBF.basketball): schedule, result, photos; same day; tier 1
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
    - [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx): schedule, result, news; same day; tier 2 (data service: scores and stats only; partial without subscription; crawl-delay 1 s)
    - [Sofascore Lebanese Division A](https://www.sofascore.com/basketball/tournament/lebanon/first-division/14250): live, result; live; tier 2 (data service; robots.txt disallows /standings/ paths: read the tournament and match pages only)
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [MTV Lebanon sport](https://www.mtv.com.lb/news/رياضة): news, result, photos; same day, timestamped; tier 2 (highest share of Lebanese sport of any outlet checked)
  - **Women's league (starts 1 Dec 2026; 2 foreign players)** (domestic, priority C; 2026-12-01 → 2027-06 (end estimated))
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
    - [FLB Instagram @flb_official](https://www.instagram.com/flb_official/): schedule, result, photos; same day; tier 1 (weekly programme posters and results; Instagram blocks automated reading: find the same post on facebook.com/LBF.basketball or in outlets, or Geoffry sends the link)
    - [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx): schedule, result, news; same day; tier 2 (data service: scores and stats only; partial without subscription; crawl-delay 1 s)
  - **Division 2 and the Lebanese Cup** (domestic, priority C; dates to confirm)
    - [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx): schedule, result, news; same day; tier 2 (data service: scores and stats only; partial without subscription; crawl-delay 1 s)
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
  - **FIBA World Cup 2027 Asian Qualifiers, second round Group F (Japan, Korea, China, Qatar, Saudi Arabia): windows 26–30 Nov 2026 and 25 Feb–1 Mar 2027** (international, priority A; 2026-11-26 → 2027-03-01)
    - Lebanon's exact November opponents and dates: confirm on the FIBA event page (Japan twice, Korea away and China home remain).
    - [FIBA](https://www.fiba.basketball): schedule, live, result, photos; live; tier 1 (LiveStats box scores are tier 1 once final; galleries)
    - [FLB Instagram @flb_official](https://www.instagram.com/flb_official/): schedule, result, photos; same day; tier 1 (weekly programme posters and results; Instagram blocks automated reading: find the same post on facebook.com/LBF.basketball or in outlets, or Geoffry sends the link)
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [LBCI live](https://www.lbcgroup.tv): live, result; live on big nights; tier 2
  - **FIBA West Asia Super League and Basketball Champions League Asia (Al Riyadi won WASL 2025-26, 75-67 v Sagesse, 4 Oct 2026)** (international, priority B; dates to confirm)
    - [FIBA](https://www.fiba.basketball): schedule, live, result, photos; live; tier 1 (LiveStats box scores are tier 1 once final; galleries)
    - [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx): schedule, result, news; same day; tier 2 (data service: scores and stats only; partial without subscription; crawl-delay 1 s)
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
  - **Arab Club Championship (Sagesse won in Beirut, 20 Oct 2026), Dubai International (late Jan–Feb), Abu Dhabi, Damascus and other invitationals** (international, priority B; 2027-01 → 2027-02)
    - Dubai International 2027 dates and Lebanese entrants UNCONFIRMED.
    - [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx): schedule, result, news; same day; tier 2 (data service: scores and stats only; partial without subscription; crawl-delay 1 s)
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
    - [MTV Lebanon sport](https://www.mtv.com.lb/news/رياضة): news, result, photos; same day, timestamped; tier 2 (highest share of Lebanese sport of any outlet checked)
    - [WAM (Emirates News Agency)](https://www.wam.ae): schedule, result; same day; tier 2
  - **Youth national teams (U18 women won FIBA U18 Asia Cup Division B, July 2026) and 3x3** (international, priority C; dates to confirm)
    - [FIBA](https://www.fiba.basketball): schedule, live, result, photos; live; tier 1 (LiveStats box scores are tier 1 once final; galleries)
    - [FLB Instagram @flb_official](https://www.instagram.com/flb_official/): schedule, result, photos; same day; tier 1 (weekly programme posters and results; Instagram blocks automated reading: find the same post on facebook.com/LBF.basketball or in outlets, or Geoffry sends the link)
    - [Annahar basketball](https://www.annahar.com/sports/basketball): schedule, result, news, photos; same night; tier 2 (section page fetches with timestamps; long article URLs exceed the fetch limit)
- **Photos appear first at:** @flb_official and club accounts (fastest), fiba.basketball galleries (national team, WASL, BCL Asia), Annahar and L'Orient Today report photos.
- **People to follow:** Wael Arakji (Al Riyadi, national team (back from ACL injury)); Youssef Khayat (national team); Omar Jamaleddine (national team); Ahmad Farran (national team head coach).
- **Sport-wide sources:** [FIBA](https://www.fiba.basketball); [Asia-Basket Lebanon](https://www.asia-basket.com/Lebanon/basketball.aspx); [Annahar basketball](https://www.annahar.com/sports/basketball).

## 2. Football (incl. futsal, women's and beach)

- **Governing body:** Lebanese Football Association (LFA; president Hashem Haidar). Site: https://www.the-lfa.com.lb (Arabic, updated). Handles: @thelfadotcom on Instagram, X, Threads and Facebook (linked from the-lfa.com.lb); YouTube @LebaneseFootballAssociation (live streams).
- **Competitions we track:**
  - **Lebanese Premier League (12 teams; double round robin, then top six / bottom six with half points)** (domestic, priority B; 2026-10-08 → 2027-06 (end estimated); usual days Thu, Fri, Sat, Sun)
    - Clubs: Al Ahed, Al Ansar (holders), Nejmeh, Safa, Shabab Al Sahel, Sagesse, Tadamon Sour, Jwaya, Mabarra, Riyadi Abbasiyah, Tripoli and Akhaa Ahli Aley (promoted). Kick-offs mostly 15:00–16:30, some 18:00 and 21:45. Ansar v Nejmeh is priority A.
    - [LFA website](https://www.the-lfa.com.lb): schedule, result, news, photos; same or next day; tier 1 (Arabic; updated; its ranking page is stale (2024))
    - [LFA @thelfadotcom (Instagram, X, Threads, Facebook)](https://x.com/thelfadotcom): schedule, result, photos; live / same day; tier 1 (linked from the-lfa.com.lb; read posts via search results or Geoffry's links)
    - [365Scores Lebanese Premier League](https://www.365scores.com/ar/football/league/premier-league-566/standings): live, result, table, schedule; live; tier 2 (data service; fetches; kick-off times)
    - [Malaeeb](http://www.malaeeb.com): schedule; 2 days ahead; tier 2 (round fixture lists with venues and kick-off times (D1 and D2))
    - [Annahar sport](https://www.annahar.com/sports): result, table, news, photos; same night; tier 2
    - [Al-Akhbar sport](https://www.al-akhbar.com): result, news; next morning; tier 2 (use the numeric article URL)
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [Sofascore Lebanese Premier League](https://www.sofascore.com/tournament/football/lebanon/premier-league/2295): live, result; live; tier 2 (robots.txt disallows /standings/ paths)
  - **Second Division (12 teams; started 9–11 Oct 2026)** (domestic, priority C; 2026-10-09 → 2027-06 (end estimated))
    - [Malaeeb](http://www.malaeeb.com): schedule; 2 days ahead; tier 2 (round fixture lists with venues and kick-off times (D1 and D2))
    - [LFA website](https://www.the-lfa.com.lb): schedule, result, news, photos; same or next day; tier 1 (Arabic; updated; its ranking page is stale (2024))
    - [365Scores Lebanese Premier League](https://www.365scores.com/ar/football/league/premier-league-566/standings): live, result, table, schedule; live; tier 2 (data service; fetches; kick-off times)
  - **Lebanese FA Cup (16 clubs, groups then knockout), Super Cup, pre-season tournaments** (domestic, priority B; dates to confirm)
    - [LFA website](https://www.the-lfa.com.lb): schedule, result, news, photos; same or next day; tier 1 (Arabic; updated; its ranking page is stale (2024))
    - [Annahar sport](https://www.annahar.com/sports): result, table, news, photos; same night; tier 2
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
  - **AFC Challenge League: Al Ansar (Group A, Thimphu) and Nejmeh (Group B, Hisor); West knockouts Mar–May 2027** (international, priority A; 2026-10-17 → 2027-05-08)
    - [AFC (www.the-afc.com match centre and news)](https://www.the-afc.com): schedule, result, photos; same day; tier 1 (never api.the-afc.com (robots.txt disallows it))
    - [Global Sports Archive](https://globalsportsarchive.com): result, table; same day; tier 2 (data service)
    - [365Scores Lebanese Premier League](https://www.365scores.com/ar/football/league/premier-league-566/standings): live, result, table, schedule; live; tier 2 (data service; fetches; kick-off times)
    - [Annahar sport](https://www.annahar.com/sports): result, table, news, photos; same night; tier 2
  - **Men's national team (coach Madjid Bougherra): FIFA-window friendlies; out of the 2027 Asian Cup** (international, priority A; year-round)
    - [LFA website](https://www.the-lfa.com.lb): schedule, result, news, photos; same or next day; tier 1 (Arabic; updated; its ranking page is stale (2024))
    - [LFA @thelfadotcom (Instagram, X, Threads, Facebook)](https://x.com/thelfadotcom): schedule, result, photos; live / same day; tier 1 (linked from the-lfa.com.lb; read posts via search results or Geoffry's links)
    - [FotMob](https://www.fotmob.com/teams/5897): schedule, live, result; live; tier 2 (data service; national team and players abroad)
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): result, table, news, photos; same night; tier 2
  - **Youth and women's national teams (WAFF U20 Women's Championship: Lebanon in Group 2; AFC U20 Asian Cup 2027 qualifiers; U-15 festival in Azerbaijan; U17 women)** (international, priority B; dates to confirm)
    - [LFA website](https://www.the-lfa.com.lb): schedule, result, news, photos; same or next day; tier 1 (Arabic; updated; its ranking page is stale (2024))
    - [AFC (www.the-afc.com match centre and news)](https://www.the-afc.com): schedule, result, photos; same day; tier 1 (never api.the-afc.com (robots.txt disallows it))
    - [WAFF](https://www.the-waff.com): schedule, result; days; tier 1
  - **Futsal league and national futsal team, women's league, beach soccer, youth leagues (U15/U17/U20 started 17–18 Oct)** (domestic, priority C; dates to confirm)
    - Research gap: teams and dates still to find (weekly desk).
    - [LFA website](https://www.the-lfa.com.lb): schedule, result, news, photos; same or next day; tier 1 (Arabic; updated; its ranking page is stale (2024))
    - [LFA @thelfadotcom (Instagram, X, Threads, Facebook)](https://x.com/thelfadotcom): schedule, result, photos; live / same day; tier 1 (linked from the-lfa.com.lb; read posts via search results or Geoffry's links)
    - [AFC (www.the-afc.com match centre and news)](https://www.the-afc.com): schedule, result, photos; same day; tier 1 (never api.the-afc.com (robots.txt disallows it))
- **Photos appear first at:** @thelfadotcom and the LFA news pages, club accounts, the-afc.com galleries (Challenge League), Annahar/elsport article photos.
- **People to follow:** Samy Merheg (Alverca (Portugal)); Husseyn Chakroun (Hannover 96 (Germany)); Austin Ayoubi (Adelaide United (Australia)); Omar Chaaban (AFC Wimbledon (England)); Gabriel Bitar (York United (Canada)); Pedro Budib (Pachuca (Mexico); spelling to check with the club); Bassel Jradi (B 93 (Denmark)).
- **Sport-wide sources:** [LFA website](https://www.the-lfa.com.lb); [365Scores Lebanese Premier League](https://www.365scores.com/ar/football/league/premier-league-566/standings); [FotMob](https://www.fotmob.com/teams/5897).

## 3. Rugby league

- **Governing body:** Lebanese Rugby League Federation (LRLF). Site: https://lebanonrl.com. Handles: @lebanonrl on Instagram, X and Facebook (linked from lebanonrl.com).
- **Competitions we track:**
  - **Rugby League World Cup 2026 (Lebanon v France, Sun 1 Nov, CommBank Stadium, Sydney; final 15 Nov)** (international, priority A; 2026-10-17 → 2026-11-15)
    - [RLWC 2026](https://www.rlwc2026.com): schedule, result, photos; live; tier 1 (scores do not fill in on a static fetch)
    - [NRL.com](https://www.nrl.com): result, news, photos; within an hour; tier 2
    - [Zero Tackle match centre](https://www.zerotackle.com): live, result; live; tier 2
    - [LRLF](https://lebanonrl.com): news, photos; same day; tier 1 (home page headlines only; article bodies are JavaScript)
  - **Lebanon Rugby League (domestic; 2026 champions Lycans), College RL, Schools RL, Beach RL** (domestic, priority C; dates to confirm)
    - [LRLF](https://lebanonrl.com): schedule, result, news; days; tier 1
    - [European Rugby League](https://europeanrugbyleague.com): result, news; days; tier 1
  - **NRL and Super League clubs of Cedars players (seasons Mar–Oct)** (abroad, priority C; 2027-03 → 2027-10)
    - [NRL.com](https://www.nrl.com): schedule, result; live; tier 1
    - [Zero Tackle](https://www.zerotackle.com): result, news; live; tier 2
- **People to follow:** Jacob Kiraz (Canterbury Bulldogs); Abbas Miski (Wigan Warriors); Jason Saab (Manly Sea Eagles); Alex Twal (Wests Tigers); Michael Cheika (Lebanon head coach).
- **Sport-wide sources:** [Love Rugby League](https://www.loverugbyleague.com); [International Rugby League](https://www.internationalrugbyleague.com).

## 4. Volleyball (indoor and beach)

- **Governing body:** Lebanese Volleyball Federation (president Walid Kassouf). Site: UNCONFIRMED (volleylebanon.com lists the league but is undated; facebook.com/LebVolley older). Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Men's First Division (12 clubs; 2025-26 champions Chabeb Batroun, 3-2 in the final v Anwar)** (domestic, priority B; dates to confirm; usual days Fri, Sat, Sun)
    - [BetExplorer volleyball Lebanon](https://www.betexplorer.com/volleyball/lebanon/1st-division/): result, schedule; within hours; tier 2 (data service: scores only)
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
    - [NNA Arabic sport](https://nna-leb.gov.lb/ar): result; same day; tier 2 (headline wires only)
    - [MTV Lebanon sport](https://www.mtv.com.lb/news/رياضة): news, result, photos; same day, timestamped; tier 2 (highest share of Lebanese sport of any outlet checked)
  - **Women's league** (domestic, priority C; dates to confirm)
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
  - **National teams (women: West Asian champions 2024-2026) and beach (Asian Tour, WAVA, Arab championships)** (international, priority B; dates to confirm)
    - [AVC](https://asianvolleyball.net): schedule, result, photos; days; tier 1
    - [Volleyball World (FIVB)](https://en.volleyballworld.com): schedule, result; live; tier 1
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
    - [MTV Lebanon sport](https://www.mtv.com.lb/news/رياضة): news, result, photos; same day, timestamped; tier 2 (highest share of Lebanese sport of any outlet checked)
- **People to follow:** Jad Abi Karam and Hadi Shbeib (men's beach (WAVA gold, Aug 2026; check FIVB spelling)); Omar Abi Karam (Batroun; indoor and beach).
- **Sport-wide sources:** [BetExplorer volleyball Lebanon](https://www.betexplorer.com/volleyball/lebanon/1st-division/).

## 5. MMA, muay thai and kickboxing

- **Governing body:** Lebanese MMA federation (IMMAF member) and muay thai federation (IFMA member): names UNCONFIRMED. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **PFL MENA, BRAVE CF and other pro cards with Lebanese fighters** (international, priority B; year-round)
    - [PFL MENA](https://pflmena.com): schedule, result; live; tier 1
    - [Sherdog](https://www.sherdog.com): result; same day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
  - **IMMAF and IFMA world and Asian championships (amateur)** (international, priority B; dates to confirm)
    - [IMMAF](https://immaf.org): result; ; tier 1
    - [IFMA](https://muaythai.sport): result; ; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
- **People to follow:** Fatima Hassan (muay thai, double IFMA world champion 2026); Mohammad Fakhreddine (PFL).
- **Sport-wide sources:** [Annahar martial arts](https://www.annahar.com/sports/martial-arts); [L'Orient Today](https://today.lorientlejour.com).

## 6. Taekwondo

- **Governing body:** Lebanese Taekwondo Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **World Taekwondo Grand Prix series and Grand Prix Final** (international, priority B; dates to confirm)
    - [World Taekwondo](https://www.worldtaekwondo.org): schedule, result, photos; live; tier 1
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
  - **World Taekwondo Championships 2027 (Astana)** (international, priority A; dates to confirm)
    - [World Taekwondo](https://www.worldtaekwondo.org): schedule, result; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
  - **Asian Taekwondo Championships, G-rank Opens (Fujairah, Egypt…)** (international, priority B; dates to confirm)
    - [World Taekwondo](https://www.worldtaekwondo.org): result; ; tier 1
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
- **People to follow:** Laetitia Aoun (−57 kg, Paris 2024 Olympian).
- **Sport-wide sources:** [NNA (National News Agency)](https://nna-leb.gov.lb/en); [L'Orient Today](https://today.lorientlejour.com); [LAU News](https://news.lau.edu.lb).

## 7. Motorsport

- **Governing body:** ATCL, Automobile et Touring Club du Liban (president Nabil "Billy" Karam). Site: atcl.org.lb (robots.txt refuses automated fetching: do not fetch). Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Lebanese Rally Championship and Rally of Lebanon (FIA MERC; 2026 won by Roger Feghali / Joseph Matar)** (domestic, priority B; dates to confirm)
    - [FIA Middle East Rally Championship](https://www.fia.com/championship/middle-east-rally-championship): schedule, result, photos; same or next day; tier 1
    - [Arab News motorsport](https://www.arabnews.com): result; same or next day; tier 2
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
  - **Lebanese Karting Championship (IAME Series Lebanon, RPM track, Mtein)** (domestic, priority C; ? → 2026-11)
    - [IAME Series Lebanon](https://www.iame-motorsport.com): result; about 2 days; tier 1
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
  - **FIA Middle East Rally Championship (Rally Saudi Arabia, Nov 2026: dates conflict on the FIA page)** (international, priority C; dates to confirm)
    - [FIA MERC](https://www.fia.com/championship/middle-east-rally-championship): schedule, result; same day; tier 1
    - [Arab News](https://www.arabnews.com): result; same day; tier 2
  - **Eurocup-3 (Christopher El Feghali, Drivex): Hungaroring 23–25 Oct, Barcelona 6–8 Nov** (abroad, priority B; 2026-04 → 2026-11-08)
    - [Pit Debrief](https://pitdebrief.com): result; same day; tier 2 (official Eurocup-3 results page still to add (weekly desk))
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
- **People to follow:** Christopher El Feghali (Eurocup-3, Drivex); Roger Feghali (rally, 2026 Rally of Lebanon winner).
- **Sport-wide sources:** [FIA news](https://www.fia.com/news).

## 8. Shooting

- **Governing body:** Lebanese Shooting and Hunting Federation (president Boutros Jalkh). Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **ISSF World Cups and World Cup Final (3–8 Dec 2026)** (international, priority B; dates to confirm)
    - [ISSF competitions](https://www.issf-sports.org/competitions): schedule, live, result, photos; live; tier 1
    - [Asian Shooting Confederation](https://www.asia-shooting.org): news, result; 1 day; tier 1
    - [LBCI](https://www.lbcgroup.tv): news, result; same day; tier 2
- **People to follow:** Samer Sarkis (skeet, Mediterranean Games 2026 gold); Alain Moussa (trap, 2018 Asian Games mixed-trap gold).
- **Sport-wide sources:** [ISSF competitions](https://www.issf-sports.org/competitions); [LBCI](https://www.lbcgroup.tv); [NNA (National News Agency)](https://nna-leb.gov.lb/en).

## 9. Tennis

- **Governing body:** Lebanese Tennis Federation (FLT; not flt.lu, that is Luxembourg). Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Davis Cup (2027 World Group I play-offs: Kazakhstan v Lebanon, away, 5–7 Feb 2027)** (international, priority A; 2027-02-05 → 2027-02-07)
    - [Davis Cup](https://www.daviscup.com): schedule, live, result; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
  - **ATP Challenger / ITF tour events with Lebanese players** (international, priority C; year-round)
    - [ATP Tour](https://www.atptour.com): schedule, result; live; tier 1
    - [Tennis Temple](https://en.tennistemple.com): result, ranking; live; tier 2
    - [elsport tennis](https://elsport.com): news; same day; tier 2
- **People to follow:** Benjamin Hassan (ATP No. 497 (19 Oct 2026), Davis Cup No. 1); Hady Habib (first Lebanese man in a Grand Slam main draw (AO 2025)).
- **Sport-wide sources:** [Tennis Temple](https://en.tennistemple.com); [L'Orient Today](https://today.lorientlejour.com).

## 10. Judo

- **Governing body:** Lebanese Judo Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **IJF World Tour (Grand Slams, Grand Prix), Asian and European Opens** (international, priority B; year-round)
    - [IJF / JudoBase](https://judobase.ijf.org): schedule, live, result; live; tier 1
    - [JudoInside](https://www.judoinside.com): result; same day; tier 2
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)
  - **World Judo Championships 2027 (Kazakhstan)** (international, priority A; dates to confirm)
    - [IJF](https://www.ijf.org): schedule, result, photos; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
- **People to follow:** Caramnob Sagaipov (−100 kg, Paris 2024 Olympian); Aqulina Chayeb (−78 kg, 2026 Tallinn European Open gold (check IJF spelling)).
- **Sport-wide sources:** [IJF media](https://www.ijf.org); [L'Orient Today](https://today.lorientlejour.com).

## 11. Athletics and running

- **Governing body:** Lebanese Athletics Federation (FLA). Site: https://flalbn.org. Handles: UNCONFIRMED (none linked on the site).
- **Competitions we track:**
  - **Lebanese Athletics Championships (July) and age-group championships** (domestic, priority C; dates to confirm)
    - [World Athletics results](https://worldathletics.org/competition/calendar-results): result; same day; tier 1
    - [FLA](https://flalbn.org): news, result; days; tier 1
  - **Asian, Arab and West Asian championships; World Athletics Indoor Tour** (international, priority B; dates to confirm)
    - [World Athletics](https://worldathletics.org/competition/calendar-results): schedule, result; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
- **People to follow:** Aziza Sbaity (100 m / 200 m); Youssef Assaker (100 km ultra, national record 8:47:42 (Sep 2026)).
- **Sport-wide sources:** [World Athletics](https://worldathletics.org); [FLA](https://flalbn.org).

## 12. Handball

- **Governing body:** Lebanese Handball Federation (president Abdallah Achour). Site: https://www.ihf.info/member-federations/lebanon/5325 (IHF profile; no own site). Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Lebanon Handball Championship (6 clubs since the 1 Oct restart: Al-Jaish, Al-Sadaka, Shabab Haret Saida, 1875, Al-Wifaq, Beirut Fire Brigade)** (domestic, priority C; 2026-10-01 → 2026-12; usual days Thu, Fri, Sat)
    - [Annahar handball](https://www.annahar.com/sports): schedule, result, photos; same night; tier 2 (a report for nearly every matchday)
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
- **Sport-wide sources:** [Asian Handball Federation](https://asianhandball.org).

## 13. Swimming

- **Governing body:** Lebanese Swimming Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **World Aquatics Championships / World Cup, Asian and Arab championships** (international, priority B; dates to confirm)
    - [World Aquatics](https://www.worldaquatics.com): schedule, live, result; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
- **People to follow:** Munzer Kabbara (IM, national records at the 2025 Worlds); Lynn El Hajj (breaststroke).
- **Sport-wide sources:** [World Aquatics](https://www.worldaquatics.com); [L'Orient Today](https://today.lorientlejour.com).

## 14. Skiing

- **Governing body:** Fédération Libanaise de Ski. Site: none found. Handles: UNCONFIRMED.
- **Season:** Dec–Mar.
- **Competitions we track:**
  - **FIS races in Lebanon (Mzaar Kfardebian, the Cedars) and national championships** (domestic, priority C; 2027-01 → 2027-03)
    - [FIS](https://www.fis-ski.com): schedule, live, result; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
  - **FIS World Cup / Europa Cup / FIS races abroad with Lebanese skiers** (international, priority C; 2026-11 → 2027-03)
    - [FIS](https://www.fis-ski.com): result; live; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
- **People to follow:** Andrea El Hayek (alpine (slalom), Milano Cortina 2026 flag bearer); Manon Ouaiss (alpine, injured before Milano Cortina).
- **Sport-wide sources:** [FIS](https://www.fis-ski.com); [L'Orient Today](https://today.lorientlejour.com).

## 15. Table tennis

- **Governing body:** Lebanese Table Tennis Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **WTT Feeder/Contender, ITTF West Asia and Arab events** (international, priority C; year-round)
    - [World Table Tennis](https://worldtabletennis.com): schedule, result; live; tier 1
    - [ITTF](https://www.ittf.com): ranking, news; ; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
- **People to follow:** Mariana Sahakian (two-time Olympian).
- **Sport-wide sources:** [Annahar sport](https://www.annahar.com/sports); [L'Orient Today](https://today.lorientlejour.com).

## 16. Teqball

- **Governing body:** Lebanese Teqball Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **FITEQ world and Asian events** (international, priority C; dates to confirm)
    - [FITEQ](https://www.fiteq.org): schedule, result; ; tier 1
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [Malaeeb](http://www.malaeeb.com): news; 1 to several days; tier 2
- **People to follow:** Ahmad Arabi / Mohammad Hafez (2026 Asian Games men's doubles silver); Maria Chedid / Qamar Dandal (2026 Asian Games women's doubles bronze).
- **Sport-wide sources:** [elsport](https://elsport.com).

## 17. Karate

- **Governing body:** Lebanese Karate Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **WKF Karate 1 Premier League / Series A, Asian and Arab championships** (international, priority C; dates to confirm)
    - [WKF](https://www.wkf.net): schedule, result; ; tier 1
    - [SportData](https://www.sportdata.org): live, result; live; tier 2
    - [Ici Beyrouth](https://www.icibeyrouth.com): news; 1 day; tier 2
- **Sport-wide sources:** [Annahar martial arts](https://www.annahar.com/sports/martial-arts).

## 18. Weightlifting and powerlifting

- **Governing body:** Lebanese Weightlifting Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **IWF and IPF world, Asian and Arab championships** (international, priority C; dates to confirm)
    - [IWF](https://iwf.sport): schedule, result; ; tier 1
    - [IPF](https://www.powerlifting.sport): result; ; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
- **People to follow:** Etienne El Chaer (powerlifting, 2025 World Games silver); Mahassen Fattouh (weightlifting, Tokyo 2020 Olympian).
- **Sport-wide sources:** [L'Orient Today](https://today.lorientlejour.com); [NNA (National News Agency)](https://nna-leb.gov.lb/en).

## 19. Boxing

- **Governing body:** Lebanese Boxing Federation (World Boxing or IBA: UNCONFIRMED). Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Pro cards in Lebanon and the region; Asian and Arab amateur championships** (mixed, priority C; year-round)
    - [Lebanese Army sport news](https://www.lebarmy.gov.lb/en): news, result; days; tier 1
    - [Annahar martial arts](https://www.annahar.com/sports/martial-arts): news, result; same day; tier 2
    - [LBCI](https://www.lbcgroup.tv): news, result; same day; tier 2
- **Sport-wide sources:** [Annahar sport](https://www.annahar.com/sports).

## 20. Para sport

- **Governing body:** Lebanese Paralympic Committee. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Asian Para Games (Aichi-Nagoya, 18–24 Oct 2026), World Para championships** (international, priority B; 2026-10-18 → 2026-10-24)
    - [IPC](https://www.paralympic.org): result, news; ; tier 1
    - [Asian Paralympic Committee](https://www.asianparalympic.org): schedule, result; ; tier 1
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
- **People to follow:** Arz Zahreddine (para-athletics, Tokyo and Paris Paralympian).
- **Sport-wide sources:** [NNA (National News Agency)](https://nna-leb.gov.lb/en).

## 21. Equestrian (show jumping)

- **Governing body:** Lebanese Equestrian Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **FEI World Cup Arab League and Gulf CSI events (Nov–Mar)** (international, priority C; 2026-11 → 2027-03)
    - [FEI database](https://data.fei.org): schedule, result; ; tier 1
    - [LBCI](https://www.lbcgroup.tv): news, result; same day; tier 2
- **People to follow:** Jad Dana (show jumping).
- **Sport-wide sources:** [LBCI](https://www.lbcgroup.tv).

## 22. Fencing

- **Governing body:** Lebanese Fencing Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **FIE World Cups (season from Nov 2026), Asian and West Asian championships** (international, priority C; 2026-11 → 2027-07)
    - [FIE](https://fie.org): schedule, result; ; tier 1
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
- **Sport-wide sources:** [NNA (National News Agency)](https://nna-leb.gov.lb/en).

## 23. Chess

- **Governing body:** Lebanese Chess Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Olympiad, Arab and Asian championships, zonals** (international, priority C; year-round)
    - [FIDE ratings (LBN)](https://ratings.fide.com): ranking; ; tier 1
    - [chess-results.com](https://chess-results.com): live, result; live; tier 2

## 24. Wrestling

- **Governing body:** Lebanese Wrestling Federation. Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **UWW Ranking Series, Asian and Arab championships, military championships** (international, priority C; dates to confirm)
    - [UWW](https://uww.org): schedule, result; ; tier 1
    - [Lebanese Army sport news](https://www.lebarmy.gov.lb/en): news, result; days; tier 1
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
- **Sport-wide sources:** [NNA (National News Agency)](https://nna-leb.gov.lb/en).

## 25. Rowing, cycling, triathlon, padel, squash, golf and other small sports

- **Governing body:** Several federations; rowing is active (Lebanese Rowing Federation). Site: none found. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **World/Asian/Arab events with Lebanese entries (World Rowing, UCI, World Triathlon, FIP padel, PSA)** (international, priority C; year-round)
    - [World Rowing](https://worldrowing.com): result; ; tier 1
    - [FIP padel](https://www.padelfip.com): result; ; tier 1
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2
    - [NNA (National News Agency)](https://nna-leb.gov.lb/en): news, result; same day; tier 2
- **People to follow:** Youssef El Mays (rowing, lightweight single sculls, 2026 Asian Games B final).
- **Sport-wide sources:** [L'Orient Today](https://today.lorientlejour.com).

## 26. Rugby union and sevens

- **Governing body:** Lebanese Rugby Union Federation. Site: https://www.lebanonrugby.com (placeholder). Handles: @LebanonRugby (X) per Asia Rugby; activity UNCONFIRMED.
- **Competitions we track:**
  - **Domestic championship (last seen 2023), West Asia sevens, university rugby (added for 2026-27)** (mixed, priority C; dates to confirm)
    - [Asia Rugby](https://www.asiarugby.com/unions/lebanon/): news; stale; tier 1
    - [Annahar sport](https://www.annahar.com/sports): news, result, photos; same day; tier 2 (robots.txt disallows /en/ and /fr/: use the Arabic sections)

## 27. Ice hockey

- **Governing body:** Lebanese Ice Hockey Federation (IIHF associate member, based near Montreal). Site: https://www.lebanonicehockey.com. Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Lebanon-Quebec Challenge (Jan), Challenger Series, Dream Nations Cup (women), LATAM Cup** (international, priority C; dates to confirm)
    - [LIHF](https://www.lebanonicehockey.com): schedule, result; slow; tier 1
    - [Dream Nations Cup](https://dreamnationscup.com): schedule, result; event time; tier 1
    - [LBCI](https://www.lbcgroup.tv): news, result; same day; tier 2

## 28. Multi-sport Games and the Olympic movement

- **Governing body:** Lebanese Olympic Committee (president Boutros Jalkh); Lebanese Paralympic Committee. Site: lebolymp.org (news stops in 2021: do not use). Handles: UNCONFIRMED.
- **Competitions we track:**
  - **Youth Olympic Games Dakar, Asian Indoor and Martial Arts Games Riyadh, Arab Games 2027 (Riyadh), Jeux de la Francophonie 2027, LA28 qualifying** (international, priority B; dates to confirm)
    - [Olympic Council of Asia](https://oca.asia): schedule, result, photos; same day; tier 1
    - [Olympics.com](https://www.olympics.com): schedule, result; live; tier 1
    - [elsport](https://elsport.com): news, result, photos; same day; tier 2
    - [L'Orient Today](https://today.lorientlejour.com): news, result, photos; same day to 1 day; tier 2

## Dated events (also in the JSON; `tools/sweep.py week` lists them)

| Date | Sport | Event | Who | Confirmed |
|---|---|---|---|---|
| 2026-10-18 → 2026-10-24 | para-sport | Asian Para Games, Aichi-Nagoya | Lebanon is one of 45 NPCs (entries UNCONFIRMED) | yes |
| 2026-10-23 → 2026-10-25 | motorsport | Eurocup-3 round 7, Hungaroring | Christopher El Feghali | to confirm |
| 2026-10-24 | basketball | Division A 2026-27 season starts | 12 clubs | yes |
| 2026-10-31 → 2026-11-13 | multi-sport | Youth Olympic Games, Dakar | 1 Lebanese athlete (name UNCONFIRMED) | yes |
| 2026-11-01 | rugby-league | RLWC: Lebanon v France, CommBank Stadium, Sydney (kick-off about 08:50 Beirut: confirm on the day) | Cedars | yes |
| 2026-11-01 → 2026-11-14 | shooting | ISSF World Championship, Doha (first LA28 quota event) | Samer Sarkis, Alain Moussa if entered | yes |
| 2026-11-06 → 2026-11-08 | motorsport | Eurocup-3 final round, Barcelona | Christopher El Feghali | to confirm |
| 2026-11-12 → 2026-11-15 | motorsport | Rally Saudi Arabia, MERC final round | Lebanese crews | to confirm |
| 2026-11-24 | football | Premier League rescheduled round 3: Shabab Al Sahel v Ansar, Safa v Nejmeh |  | to confirm |
| 2026-11-26 → 2026-11-30 | basketball | FIBA World Cup 2027 Asian Qualifiers, window 5 (Lebanon's dates and opponents to confirm) | Lebanon men | yes |
| 2026-11-29 | athletics | Beirut Marathon | mass race (42.2K, 21.1K, 10K, 5K…) | to confirm |
| 2026-12-01 | basketball | Women's league 2026-27 starts |  | yes |
| 2026-12-03 → 2026-12-08 | shooting | ISSF World Cup Final | if Lebanese shooters qualify | to confirm |
| 2026-12-05 → 2026-12-06 | judo | Tokyo Grand Slam | Sagaipov, Chayeb if entered | yes |
| 2026-12-13 → 2026-12-21 | multi-sport | Asian Indoor and Martial Arts Games, Riyadh | Lebanese entry UNCONFIRMED | to confirm |
| 2026-12-20 | football | Ansar v Nejmeh, Premier League (Beirut derby) |  | to confirm |
| 2027-02-05 → 2027-02-07 | tennis | Davis Cup World Group I play-offs: Kazakhstan v Lebanon (away) | Benjamin Hassan, Hady Habib | yes |
| 2027-02-25 → 2027-03-01 | basketball | FIBA World Cup 2027 Asian Qualifiers, window 6 | Lebanon men | yes |
| 2027-03-03 → 2027-03-17 | football | AFC Challenge League West quarter-finals (if Ansar or Nejmeh qualify) |  | to confirm |
| 2027-05-08 | football | AFC Challenge League final |  | to confirm |

## Gaps to close (weekly desk, step 6a)

- Instagram handles for almost every federation and club except those in sources/handles.json (Instagram and X can't be fetched; confirm from each organisation's own website, or Geoffry confirms in the app).
- Basketball: the 2026-27 Division A club list (promoted and relegated) and the weekly programme; Lebanon's exact November FIBA fixtures; Lebanese players abroad (NBA/NCAA/Europe/Gulf).
- Football: women's league, futsal league and national futsal team, beach soccer; FA Cup group dates; November FIFA-window friendlies; most club handles (Nejmeh, Ansar, Safa…).
- Volleyball: federation website and handles, 2026-27 start date, women's league clubs.
- Handball: Final Four and final dates. Motorsport: the ATCL domestic calendar (hill climbs, speed tests, drift), the official Eurocup-3 results page.
- Asian Para Games results for Lebanon (to 24 Oct); Lebanon's athlete at the Dakar Youth Olympics; Beirut Marathon date from the organiser.
- Individual-sport federations with no website found (taekwondo, judo, karate, wrestling, boxing, MMA, muay thai, weightlifting, fencing, shooting, table tennis, tennis, ski…): find their Facebook/Instagram pages.
- Fan pages that break news fast (to use as tips only, tier 3) and follower counts for ranking.
