# Trademark registration: single post

`post.png` is ready to upload as a 1080 × 1350 feed post. `post.html` is the source, built on `brand/`. `img/registered.jpg` is the background render.

**On the image:** *Your trade licence won't protect your* **BRAND** · A TRADEMARK WILL · DM us "TRADEMARK"

The headline follows the brand formula: soft lead-in, one gold keyword, navy tag. It opens with a misconception many founders share, the idea that the trade licence protects the brand, and the tag gives the fix. The brass ® is the single subject: it's the mark a founder is allowed to use once the registration is through.

## Caption

```
Your trade licence registers your company name. It doesn't protect your brand.

In the UAE, your brand is protected when it's registered as a trademark with the Ministry of Economy and Tourism. Until then, someone else can file your name or logo first, and you could be the one who has to rebrand.

We handle it from first search to certificate:

▸ Search: we check your name and logo against registered marks before you pay to file
▸ Classes: we match your application to what you actually sell
▸ Filing: we prepare the documents and submit the application
▸ Follow-up: examination, publication and any objections
▸ Certificate: we see it through to registration
▸ Renewal: protection lasts 10 years, and we handle the renewal

Government fees are AED 6,500 per class: AED 750 to file, AED 750 to publish and AED 5,000 to register. Members of the National Programme for SMEs pay half. Our service fee is separate.

DM us "TRADEMARK" with your brand name to get started.

#UAETrademark #TrademarkRegistration #BrandProtection #DubaiBusiness #DubaiStartup #UAEBusinessSetup #IntellectualProperty
```

**Alt text:** A brushed brass registered-trademark symbol stands on a pale blue studio floor in soft morning light. Text: Your trade licence won't protect your brand. A trademark will. DM us "TRADEMARK". ConnectIn Business Services.

## Before posting

- **The fee figures are regulatory facts.** Someone who files trademarks should confirm them first. They come from Cabinet Resolution No. 102 of 2025, in force since 14 November 2025. I checked them through search results that quote the Ministry's own service pages and through law-firm summaries. The Ministry pages couldn't be opened from this environment.
- **"Our service fee is separate"** assumes you charge a service fee on top of the government fees. Change the line if you quote all-in prices.
- **No website on the image.** The design system and the October posts use `connectin.ae`, but I couldn't confirm that domain. Web search finds ConnectIn Business Services pages on `connectinlegal.com`, and the old posts show a `.com` address. Confirm the right domain before adding one here, and fix the October footers if `connectin.ae` is wrong.
- **One call to action.** The original copy's phone, email and WhatsApp lines were empty placeholders, so the post uses a single DM keyword. If you want a WhatsApp line in the caption, add the real number.

## Facts and sources

| Claim | Source |
| --- | --- |
| A trade name registered with a licensing authority doesn't protect the brand as a trademark | [Meydan Free Zone](https://www.meydanfz.ae/blog/trademark-vs-trade-name), [Emira Legal](https://emiralegal.com/trade-license-vs-trademark-in-uae-who-has-legal-rights-over-a-business-name/), [Filings UAE](https://filings.ae/guides/legal-name-trade-name-and-trademark-know-the-difference) |
| Trademarks are registered with the Ministry of Economy and Tourism; fees are AED 750 application, AED 750 publication and AED 5,000 registration, per class | [MOET: Trademark Registration](https://www.moet.gov.ae/en/w/trademark-registration-1), [MOET: Pay Registration Fees](https://www.moet.gov.ae/en/w/pay-registration-fees-for-trademark), [ABS Partners](https://abspartners.ae/uae-restructures-trademark-fees-under-new-2025-resolution/), [Saba IP](https://www.sabaip.com/uae-new-trademark-fee-amendments-take-effect-under-cabinet-resolution-no-102-of-2025/) |
| Members of the National Programme for SMEs get 50% off government trademark fees | [ABS Partners](https://abspartners.ae/uae-restructures-trademark-fees-under-new-2025-resolution/), [Abou Naja IP](https://abounaja.com/news/uae-trademark-fee-reduction-2025-new-structure-fast-track-services-inclusive-ip-protection) |
| Protection lasts 10 years from the filing date and renews in 10-year periods | [Federal Decree-Law No. 36 of 2021 (WIPO Lex)](https://www.wipo.int/wipolex/en/legislation/details/21302), [Kaden Boriss](https://www.kadenboriss.com/insights/uae-trademark-registration-vs-trade-name) |

## Re-rendering the image

The ® is Urbanist ExtraBold's own glyph (`brand/fonts/Urbanist-ExtraBold.ttf`), extruded in the moodboard studio (`brand/moodboard/src/scene.html`, scene `registered`). Run this from `brand/`, with a static server on port 8765 and `npm install` done in `moodboard/src`:

```sh
node moodboard/src/shoot.js moodboard/src/scene.html \
  "s=registered&vsm=1&face=9&rough=0.22&rot=-0.45&ox=0.26&gx=1.0&gy=1.3&gi=110&ly=1.06&w=3240&h=4050" \
  moodboard/src/raw/registered.png
```

Scale it down to 2160 × 2700 with Lanczos and save it as JPEG quality 92 in `img/registered.jpg`. That reproduces the committed file byte for byte. `post.png` is `post.html` rendered at 2x and scaled down to 1080 × 1350.
