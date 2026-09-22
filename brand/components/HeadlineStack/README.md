# HeadlineStack

The two-voice headline every post opens with: a light italic lead-in, a heavy-caps keyword, and an optional key tag.

**Markup:** `.ci-stack` > `p.ci-lead` + `p.ci-keyword` (+ `span.ci-tag`). Add `.ci-keyword--gold` for the one gold word, `.ci-stack--center` only on Navy greeting posts.

**Consumer provides:** the lead-in (2–5 words, sentence case), the keyword (1–2 words; CSS uppercases it), the tag text.

- Do: keep the keyword to what the post is about: LAUNCH, BUSINESS, DOCUMENTS.
- Do: left-align on the 96px margin at y = 224.
- Don't: bold the lead-in, add a third colour, or put a ghost word behind the stack.
- Don't: gold keyword on Daylight AND a gold word elsewhere. One gold word per post.
