# Moodboard

Two boards that show how ConnectIn should feel. They're built on the design system in `brand/` (tokens, Urbanist, the official logo) and they follow its rules: navy leads, gold is the reward, one idea per image.

| File | What it is |
| --- | --- |
| `moodboard.png` | The mood (4800 × 3000). Brass capsule, Dubai in haze, paperwork in blind light, pawn and king, four materials, colour, type and the graphic kit. |
| `direction.png` | Imagery direction (4800 × 3000). Five current posts to build on, five to retire, and an image recipe with a prompt base for shoots and AI generation. |
| `moodboard.html`, `direction.html` | Sources for both boards. Edit these, then re-render (below). |
| `img/` | The renders and materials used on the main board. |
| `img/feed/` | Crops of ten current posts, taken from Instagram profile screenshots. |
| `src/` | The scripts that make every image in `img/` and both PNGs. |

## The main board

| Tile | What it shows | Why it's there |
| --- | --- | --- |
| The mark, made physical | The capsule from the logo, extruded in brushed brass | The New Year post already put the logo in 3D gold. This is the quiet version: one object, soft light, lots of air. |
| Dubai, morning haze | A supertall and towers fading into fog | Real Dubai, but calm. It's an abstract model, not a copy of any building. |
| Paperwork, handled | Paper on a navy folder, a pen, a brass stamp, window-blind light | This is the service itself. The blind light is the "morning in the office" mood. |
| One move ahead | Navy lacquer pawn in front of an ivory king | The chess post was the strongest metaphor in the feed. This is the cleaned-up version. |
| Materials | Navy wool twill, brushed brass, white marble with a gold vein, a blind-embossed capsule | Material cues for shoots, stationery, the office and 3D work. |
| Colour, type, graphic language | Tokens and components from `brand/` | These are here so the mood and the system are seen together. The rules live in `brand/README.md`. |

The Arabic sample, جاهز للانطلاق, means "Ready to launch". It's set in IBM Plex Sans Arabic SemiBold (Arabic subset from Google Fonts, SIL OFL 1.1: `brand/fonts/IBMPlexSansArabic-SemiBold-arabic.woff2`, licence in `brand/fonts/OFL-IBMPlexSansArabic.txt`). Have a native speaker check any Arabic copy before it's published.

## Limitations

- **Everything on the main board was made in code.** It's all 3D renders (Three.js) and procedural textures. There are no stock photos and no AI images, because this environment can't reach image hosts (Unsplash, Pexels or Higgsfield's CDN). The renders look like clean CG, not photography. Use them as mood references, not as finished campaign images.
- **There are no people on it.** That's the biggest gap. Real photos of the team will build trust faster than any render. Add two or three portraits of the actual consultants, shot in daylight against a mist backdrop, when you have them.
- **The feed crops are low resolution.** Each post is only about 356 px wide in the screenshots, so the direction board looks soft at full size. They're references, not assets.
- **The October Higgsfield images belong here.** The skyline in haze, the brass scale, the marble desk and the three models from `content/2026-10` all fit the recipe. Allow `d8j0ntlcm91z4.cloudfront.net` or drop the files into `content/2026-10/images/`, and they can replace or join these tiles.
- **The capsule trace comes from the 535 px logo PNG.** It works for renders and small marks. It doesn't replace vector artwork.

## Re-rendering

```sh
cd brand/moodboard/src
npm install                        # three, playwright
npx playwright install chromium    # first time only
bash render_all.sh                 # stills and materials into ../img/, then both PNGs
```

- `scene.html?s=capsule|chess|towers|paper` renders the four stills. They share one studio environment, and query parameters set the camera and lights. `render_all.sh` has the exact values used.
- `scene.html?s=registered` renders the brass ® for `content/trademark-registration` from `brand/fonts/Urbanist-ExtraBold.ttf`. The command is in that folder's README.
- `textures.html?t=twill|brass|marble|emboss` renders the four materials.
- `capsule.json` is the capsule outline traced from `assets/Logos/connectin-logo.png`, normalised to a width of 1.
- Rendering is deterministic: the same inputs produce the same files byte for byte.
