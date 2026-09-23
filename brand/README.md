ConnectIn Business Services helps founders set up, run and close companies in Dubai. The feed is the firm's shop window: every post should read like advice from a senior consultant — calm, exact, a little ahead of the reader — and look like it came from a firm that handles paperwork without mistakes.

The system keeps what already works on the page (navy + gold, a light-italic / heavy-caps headline pair, cool high-key imagery) and removes the noise: one type family instead of four treatments, a gold that is legible, a fixed layout grid, and one marker style.

## Brand in one line

**Neat. Fast. Reliable.** Every visual decision should look like that phrase: aligned edges, few elements, nothing decorative that isn't doing a job.

## Colour

The palette starts from the three inks in the logo file: **navy #032d47** (`brand-navy`), **gold #7c6527** (`brand-gold`) and **grey #606060** (`brand-grey`). Everything else is a step of those.

Two themes, same tokens.

- **Daylight** (`surface` white, `surface-mist` wash) is the default for advisory and carousel posts — roughly 3 in every 4 posts.
- **Navy** (`surface` #032d47, the logo navy) is for announcements, seasonal greetings, milestones and closing slides — the New Year post is the model. Keep it to 1 in every 4 so it stays special.

Rules:

- Headline keyword in `headline` (navy) or `gold`. Secondary emphasis word in `blue`. Body in `ink`, meta in `ink-muted`.
- **One gold word per post.** Gold is the reward, not the paint.
- On Daylight, `gold` is the logo gold itself: 5.6:1 on white, readable at any size. On Navy it lifts to #d4b36a (7.1:1), because the logo gold is only 2.6:1 on navy. The old bright ochre (#d9a441, 2.3:1 on white) and the orange-to-yellow gradient are retired: they don't match the logo either.
- `signal` red only marks a warning (the X on "7 Costly Mistakes", a deadline) and always sits next to a word. No red petals, hearts or decorative red.
- `gold-leaf` is for shapes: the pointer triangle, rules, blocks. Never text on a light ground.
- No gradients except one: `surface-mist` fading to `surface` behind a hero image (top → bottom). No blue-purple, no metallic text.

## Typography

One family: **Urbanist** (Google Fonts, free, 100–900 with true italics). It is a geometric sans close to the current headline face, so the feed keeps its character, but the light italic and the heavy caps now come from the same family and sit together cleanly. Arabic copy uses **IBM Plex Sans Arabic** at matching weights.

The headline is always a **two-voice stack**:

1. `lead-in` — Urbanist 300 italic, sentence case: *Ready to*, *Thinking of starting a*, *Closing your*
2. `keyword` — Urbanist 800 caps, 1–2 words: **LAUNCH**, **BUSINESS**, **STRONGER FOUNDATION**
3. optional `tag` — the navy tag carrying the topic: **BUSINESS SETUP**, **in Dubai**

Rules:

- Max **three** type styles per post (not counting the footer). The current posts often use four or five.
- Never set the lead-in bold or the keyword light. Never mix script fonts in (the *Love Story* script is retired).
- Nothing on the canvas smaller than `caption` (24px on 1080 wide). Current body lines at ~16–18px are unreadable in the feed.
- Casing: sentence case for lead-ins and pointers ("What kind of documents you need"), caps only for the keyword and tag. No Random Title Case In Sentences.

## Layout

Canvas is **1080 × 1350 (4:5)**. Profile grid shows a 3:4 crop, so `margin` (96px) is the safe edge on all sides.

- **Header band** (`header-band`, 240px): logo top-left at the margin. The top-right corner stays empty — Instagram's carousel icon covers it, which is why the handle text there is unreadable today.
- **Headline zone**: left-aligned to the margin, top of the zone at 272px. Left alignment gives every post the same spine, so the 9-grid reads as one brand instead of nine layouts. Centre alignment is reserved for Navy greetings.
- **Image zone**: lower 55% of the canvas, subject cut out on `surface-mist`, allowed to bleed off the bottom or right edge.
- **Footer band** (`footer-band`): website bottom-left in `caption`, swipe cue bottom-right. Handle lives in the caption, not on the image.

See *Post templates* for the three layouts and their grids.

## Imagery

- One subject per post, cut out, lit high-key and cool, on `surface-mist`. The Emirati consultant under the magnifier and the pawn/king chess shot are the right tone.
- Prefer real UAE context (Dubai skyline, DED/free-zone documents, real team photos) over generic stock businessmen in armchairs. Faces of the actual team build trust faster than models.
- If AI-generated, check hands, text in the image and crowds (the mannequin crowd reads as unfinished). Never put fake text inside an image.
- Shadows: `shadow-lift` under the subject only.

## Marks and icons

- **One list/pointer marker**: the gold `gold-leaf` right-pointing triangle (▸). Retire », >>> and mixed chevrons.
- **Swipe cue**: "Swipe" + arrow in a pill, `ink-muted`, bottom-right. Drop the hand icon.
- Numbers: when a post is a count ("7 Costly Mistakes"), the number is a `numeral` shape, not an image.
- **Logo**: always the official artwork from Logos, never retyped. `connectin-logo.png` on white and mist; `connectin-logo-reversed.png` on navy. 260px wide on the 1080 canvas, top-left at the margin, top 72px. Keep clear space of at least the capsule mark's height. Never recolour, stretch, outline or put the standard version on navy or a busy photo.
- The logo's capsule speech bubble is the brand's own shape. The key tag and fact chip use the same rounded-rectangle language (`radius-tag`); don't introduce circles or sharp boxes beside it.

## Voice

See *Voice and copy*. Short version: a question the founder is already asking, one concrete promise, one next step. No hype, no fear-mongering beyond the real cost.
