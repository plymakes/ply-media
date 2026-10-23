# SportsWire brand guide (for the newsroom)

Source of truth: Geoffry's brand kit (`brand/logos/README.txt`, brand sheet, Aug 2026) and the posts published 19 Aug – 7 Sep 2026 (best examples in `brand/reference/`). `tools/render.py` already implements everything below; this page is for judgement calls.

## Identity
- Mark: three rounded rising bars with a 10° lean, tallest bar in the page accent. Never rotate, outline, gradient or re-slant the bars. Clearspace = one bar width.
- Wordmark: `sportswire.lb` / `sportswire.cy`, Rubik ExtraBold lowercase (the wordmark only), suffix in the accent.
- Accent once per layout as a rule of thumb: the eyebrow, a couple of headline words, "vs." and one key number is the most a card carries.

## House style, Geoffry's notes (23 Oct 2026), both pages
1. **Fewer words per image.** Headline at most 8 words, deck at most 12, and about 30 words on a whole card (40 on an archive story slide). The caption carries the detail. The gate counts.
2. **More images, bigger, most of all the first image.** The first slide of every post is photo-led whenever any credited photo exists: the renderer gives it the biggest band the photo allows (up to the full card) and only shrinks it if the text needs room. Spotlights, previews, quizzes and votes get photos too.
3. **Capitals for names.** Clubs, athletes, countries and places always start with a capital ("Riyadi into the final.", "Cyprus vs. Montenegro"). Headlines are sentence case, no longer lowercase. The gate flags names written in lower case.
4. **"vs.", never "v"**, and in the accent colour. Write "Omonia vs. Benfica" (or "v", which the cards turn into an accent "vs."); captions say "vs." too.
5. **Logos everywhere.** A crest for every club and a flag for every country (`"crest": "flag:lb"`, `flag:cy`, `flag:gb-eng`: 270 flags in `brand/flags/`) on scores, fixtures, schedules, matchups, quiz and vote options. Results without a photo show big logos above the names; `matchup` announces a game with two big logos, "vs." and the time.
Previews: `brand/template-previews/house-style-*.png`.

## Colour
| Token | Hex | Use |
|---|---|---|
| Ink | #16171B | dark cards, text on bone |
| Bone | #F3F1EB | light cards (the brand is light-first) |
| White | #FAFAF8 | text on ink, tiles |
| LB signal red | #FF3B30 | Lebanon accent on every background |
| CY amber (light) | #E38C00 | Cyprus accent on bone |
| CY amber (dark) | #FFB300 | Cyprus accent on ink |

Alternate dark and light cards so the grid doesn't stack the same colour: results and big nights usually dark, tables, numbers, fixtures and explainers usually light.

## Type
- Headlines: Rubik ExtraBold, **sentence case with capitalised names** (since 23 Oct 2026; before that they were lowercase), tight, ending with a full stop ("Korea led for half the night. Then we took the place over."). Short, punchy, two lines; at most 8 words.
- Body / deck / captions on cards: Manrope.
- Scores, times, labels, eyebrows, handles: JetBrains Mono, tracked uppercase for labels.

## Card anatomy (top to bottom)
1. Mark + `SPORTSWIRE LEBANON` / `SPORTSWIRE CYPRUS`, optional section or `01 / 03` at top right.
2. Eyebrow in the accent, mono, tracked: competition · stage.
3. Headline.
4. Deck: one or two plain sentences of context.
5. The data block (score panel, table, rows, tiles, fixtures list).
6. Footer: a bold one-liner or a muted note on the left, `@SPORTSWIRE.LB` / `.CY` on the right.

## Voice
- Warm, confident, partisan for the country, neutral between local clubs. "We" for the national team; never "we" for a club.
- Short sentences. Facts first, then the feeling. Numbers do the talking.
- Defeats reported plainly and kindly ("a hard one", "nothing to be sorry about"). Never mock a team, player or referee.
- Captions: a hook line, two or three short paragraphs of facts, one line on what's next, a source line, then @mentions and 3–5 hashtags. One flag emoji at the end is the house sign-off. Arabic (Lebanese dialect) or Greek words only where they add warmth, never for facts.

## Images
- Club crests (`brand/crests/`) and country flags (`brand/flags/`, `"crest": "flag:<code>"`) on score panels, rows, fixtures, matchups and entity blocks, always on their white tile. As many logos as the card holds.
- Event photos (any source, always credited: PLAYBOOK, Images and rights) sit in a **hero band** across the top of the card that fades into ink; on the first slide the band is as big as the photo allows (up to the whole card); the eyebrow becomes a solid accent pill and the headline overlaps the foot of the photo. Photo cards are always dark. The credit runs small, top right, in mono caps ("PHOTO: SAGESSE SC").
- In Reels the photo band is taller and slowly pushes in while the text builds underneath; the first frame is the photo alone, which makes a strong hook.
- One photo per card; on carousels, photos on as many slides as there are good, different, credited pictures (the hook slide always first). Never collage, filter, recolour or put stickers on a photo.
- Never AI-generated images of real people.

## From the Archive (history series)

A deliberate exception to the clean look: aged newsprint, letterpress serif (Playfair Display), typewriter labels (Special Elite), body copy in Old Standard TT, sepia ink and the page colour dulled to an old print colour (LB oxblood #9E2A1F, CY ochre #9A6416). Photos appear as aged prints (sepia, grain, cream border, a slight tilt, photo corners) with a typewritten credit. Headlines in this series are sentence case. Everything else about the voice stays the same: short, factual, warm. Rules and slide recipe: `history/README.md`; builder: `tools/archive.py`.
