# Ply social media playbook

This repository is the working folder for Ply's Instagram. Images in `posts/` are public on purpose: Metricool reads them from
`https://raw.githubusercontent.com/plymakes/ply-media/main/posts/<file>.png`.

## The brand

- Name: Ply (full name Ply Makes). Instagram @plymakes. Slogan: "Ply makes it yours." Arabic: "Ply بيعملها إلك".
- What Ply is: a 3D printing studio in Lebanon making personalised gifts, décor, custom prints and spare parts. The owner (Geoffry) lives in Cyprus; a helper in Lebanon runs the printer.
- Rules, colours, type and logos: `brand/brand-guide.md`, `brand/tokens.json`, `brand/logos/`.
- Brand direction since 17 Oct 2026: **Atelier** (logo route A6, the "Ply Makes" signature). Colours: Bone #EFEAE2, Charcoal #1C1B19, Terracotta #B4532A (single accent), Sand #CDBFA8, Clay #DDB8A2, Stone #8A857C. Fonts: Fraunces 500 (headlines; Fraunces 700 for the print cut), Space Grotesk (labels, body), Noto Naskh Arabic (Arabic). The old cobalt/sun/coral "stack" brand is retired (archived in brand/archive-stack/).
- Voice: plain, warm, calm English, speaking to "you"; "Ply makes …" campaign lines; one call to action per post; one or two emojis per caption; 2–4 hashtags; an Arabic line now and then.

## How posts are made

- Feed posts are 1080 × 1350 PNGs in the Atelier style. `tools/atelier_posts.py` is the reference: its `page()` layout (tracked label + @plymakes, serif headline, illustration, body line, "Ply." mark bottom right) and `stagger()` pill lists. Copy it into a new script for each batch and change only the content. Reels: `tools/reels.py` (1080 × 1920, frame-by-frame, ffmpeg). Stories: 1080 × 1920 with the same layout. (`tools/showcase_posts_07_26.py` is the retired old style: do not use.)
- Background colours rotate in this order so the grid never stacks a colour on itself: bone, sand, clay, charcoal, terracotta (continue from the last entry in `content-log.json`; in the generator these are P, SU, R, I, C).
- Render with Playwright/Chromium (already installed), look at every PNG before scheduling, fix text that wraps badly.
- Save PNGs to `posts/` with the name `ply-post-NN-short-name.png`, commit and push to `main`, then schedule.

## Honesty rules (never break)

- Never present an illustration as a real product photo, never show a product as available before it is, never invent reviews, customers, numbers or prices.
- Until the printer is running (expected around 10 November 2026), every product mention says "coming soon" or similar.
- After that, real photos and videos from the helper come first; illustrations are for tips, polls and ideas.
- Customer names or photos only with their consent.

## Scheduling

- Metricool brand id (blogId) 7478818, Instagram only (TikTok not connected yet), timezone Asia/Nicosia.
- Rhythm (chosen by Geoffry, 17 Oct 2026): 4-5 feed posts a week plus Stories, at the best time from `getBestTimeToPostByNetwork` (10:00 so far). Keep the schedule filled about 14 days ahead.
- Budget: Metricool free plan publishes at most 20 items per calendar month (each network counts separately). Count feed posts and Stories together and never go over 20 in a month. Extra Stories go into a "story kit" Geoffry posts by hand (max 2 a week).
- Highlights: About, Ideas, How it works, Christmas. Tools can't add Highlights, so each Story's log entry suggests one and the daily brief tells Geoffry.
- Pre-launch goals until the printer arrives (about 10 Nov): 250 followers, 40 people on the first-access list (comments/DMs asking to be notified), 5%+ engagement on poll and quiz posts.
- Posts that mention a price, discount, offer, giveaway or delivery promise: create them with `"draft": true` and list them in the weekly summary for Geoffry to approve. Everything else uses `"autoPublish": true`.
- Record every scheduled post in `content-log.json`.
