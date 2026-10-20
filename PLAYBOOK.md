# Ply social media playbook

> **Not Ply:** the `sportswire/` folder is a separate project (SportsWire sports news pages) that shares this repo only for image hosting. Ply runs never read, use, change, move or delete anything inside `sportswire/`, and never count its posts, logs or brand as Ply's. Ply's files are everything outside that folder.

This repository is the working folder for Ply's Instagram. Images in `posts/` are public on purpose: Metricool reads them from
`https://raw.githubusercontent.com/plymakes/ply-media/main/posts/<file>.png`.

## The brand

- Name: Ply (full name Ply Makes). Instagram @plymakes. Slogan (since 17 Oct 2026): "Made in layers. Made in Lebanon." Arabic: "طبقة فوق طبقة، من لبنان". The old slogan "Ply makes it yours." is retired.
- What Ply is (decided 17 Oct 2026): a small studio in Lebanon that designs and 3D-prints calm, useful homeware. Launch line-up (changed 18 Oct 2026 evening by Geoffry, replaces the ribbed planter, fluted bud vase and coaster set): textured tabletop planters and vases in two textures, **Quilt** (soft diamond pillows) and **Tile** (grid of soft squares, a nod to Beirut cement tiles): Quilt planter and Tile planter (small and medium, seven drainage holes, a drip tray hidden under the pot that twists off to empty), Quilt vase and Tile vase (20 cm, dried or faux stems), and a planter-and-vase set. Product colours: Ivory White, Charcoal, Dark Green, Desert Tan (these are product colour names; the brand palette below is unchanged). No coasters at launch. NO customisation at launch: no names, no custom prints, no spare parts, no lights. Never promise personalisation. The owner (Geoffry) lives in Cyprus; a helper in Lebanon runs the printer.
- New pieces (20 Oct 2026, Geoffry): **Loom** soap rest ($12) and **Pleat** pot with a dish lid ($14), minimal fine-ribbed designs in the same four colours. Names follow one family with Quilt and Tile (craft and textile words). Studio renders: `shop/products/loom-soap-rest-*.jpg`, `shop/products/pleat-pot-*.jpg` (Bone background, labelled as 3D renders). Shopify: drafts until Geoffry publishes. Voice for these (inspired by Conifer Homewares): one idea per post, short calm lines, design first, no hard sell. Don't say "two designs" or "three pieces" any more; say "a few pieces" or name them. Posts 56–60 (26 Oct–7 Nov) introduce them.
- Product images (changed 19 Oct 2026 by Geoffry): posts and Reels MAY show the studio renders in `shop/products/` (Quilt and Tile planters, vases, sets, `shop/banners/drainage-square.jpg`). Always say they are 3D renders (in the caption, and on the image when it is a designed post) until real photos of the first prints exist. Once real photos exist they come first, and a "render ➜ real" post shows the difference honestly. Never use the old ribbed planter, fluted bud vase, coaster or set-of-three images.
- Fixed 19 Oct: reel 08 "three pieces", post 42 "three colours", post 46 "guess the three" and post 55 "what's next" were replaced or re-captioned for Quilt and Tile; story kit 04 was redone with the four product colours.
- Website launch (tentative, Geoffry to confirm): Tuesday 1 December 2026 at plymakes.com; First Layer early access Monday 30 November (the Shopify password page is on; the password is the early-access key). Countdown and launch posts exist as drafts until the date is confirmed. Prices (Shopify): small planter $14, medium planter $22, vase $16, planter-and-vase set $36 (crosses the free-delivery line). Delivery in Lebanon by Wakilni.
- First Layer list: DM "FIRST" or comment 🧡 for first look, first pick of the (small) first batch and ordering before everyone else. Prices only in posts Geoffry has approved (drafts).
- Rules, colours, type and logos: `brand/brand-guide.md`, `brand/tokens.json`, `brand/logos/`.
- Brand direction since 17 Oct 2026: **Atelier** (logo route A6, the "Ply Makes" signature). Colours: Bone #EFEAE2, Charcoal #1C1B19, Terracotta #B4532A (single accent), Sand #CDBFA8, Clay #DDB8A2, Stone #8A857C. Fonts: Fraunces 500 (headlines; Fraunces 700 for the print cut), Space Grotesk (labels, body), Noto Naskh Arabic (Arabic). The old cobalt/sun/coral "stack" brand is retired (archived in brand/archive-stack/).
- Voice: plain, warm, calm English, speaking to "you"; short calm lines ("Fewer things. Made well.", "Designed here. Printed here."); one call to action per post; one or two emojis per caption; 2–4 hashtags; an Arabic line now and then.

## How posts are made

- Feed posts are 1080 × 1350 PNGs in the Atelier style. `tools/atelier_posts.py` is the reference: its `page()` layout (tracked label + @plymakes, serif headline, illustration, body line, "Ply." mark bottom right) and `stagger()` pill lists. Copy it into a new script for each batch and change only the content. Latest batch: `tools/brand_posts_launch.py` (product-free posts), `tools/reels_brand.py` (product-free Reels), `tools/reels_renders_2026_10_19.py` (Reels built from the renders) and `tools/stories_2026_10_19.py` (Stories, with renders). Reels: `tools/reels.py` (1080 × 1920, frame-by-frame, ffmpeg). Stories: 1080 × 1920 with the same layout. (`tools/showcase_posts_07_26.py` is the retired old style: do not use.)
- Product carousels can also use the Shopify render URLs directly (`https://cdn.shopify.com/s/files/1/1108/8963/2135/files/<file>.jpg`, listed by the Shopify product media); Metricool copies them.
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
- Plan: Metricool Starter since 19 Oct 2026 (Geoffry upgraded): no monthly post cap (fair use). The old 20-a-month budget no longer applies.
- Rhythm (Geoffry asked for more posts, 19 Oct 2026): one feed post a day at 10:00 (a second feed post at 15:00 is used on some days for the new pieces; check Metricool, not only this log, for free slots) (best time from `getBestTimeToPostByNetwork`), 2–3 Reels a week at 18:00, and 1–2 scheduled Stories a day (usually 12:00 and/or 20:00). Keep the schedule filled about 14 days ahead. Don't repeat the same render two days running; mix product posts with tips, polls, process and Lebanon/heritage posts.
- Stories that need an Instagram sticker (poll, quiz, countdown, link) can't get the sticker from Metricool, so they stay in the "story kit" Geoffry posts by hand (max 3 a week; the image leaves the lower half free for the sticker). All other Stories are scheduled in Metricool.
- Real-photo moments (printer unboxing, first print timelapse, render ➜ real, Wakilni test parcel, first orders) are drafts whose caption starts with "[DRAFT: ...]"; never switch them on yourself: Geoffry swaps in the photo or video.
- Highlights: About, Ideas, How it works, Christmas. Tools can't add Highlights, so each Story's log entry suggests one and the daily brief tells Geoffry.
- Pre-launch goals until the printer arrives (about 10 Nov): 250 followers, 40 people on the first-access list (comments/DMs asking to be notified), 5%+ engagement on poll and quiz posts.
- Posts that mention a price, discount, offer, giveaway or delivery promise: create them with `"draft": true` and list them in the weekly summary for Geoffry to approve. Everything else uses `"autoPublish": true`.
- Record every scheduled post in `content-log.json`.
