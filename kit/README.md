# The Code — design kit

The shared visual foundation. Every project carries The Code's logo, so these three
files (`assets/tokens.css`, `assets/brand.css`, `assets/base.css`) travel together
and stay in sync with **the-code-kit**. Page-specific styling never goes in them.

## The rules that are easy to get wrong

### `#288CFF` is a fill colour, not a text colour

Measured on `--bg` `#F9F9F9`: **3.17:1**. White on it: **3.34:1**. That clears AA for
large or bold text — buttons, big statistics, headings ≥19px bold — and fails for
body copy. For links, small text and icons on a light ground use `--accent-ink`
`#0F6FDB` (**4.62:1**).

On the blue wash `--wash` `#E9F2FF`, `--accent-ink` drops to 4.31:1 and fails. Wash
panels use `--accent-ink-on-wash` `#0D66CC` (**4.91:1**) instead — `.card--wash` and
`.do` already do this. Run `python3 tools/contrast.py` after touching any colour.

### Serif carries voice, not chrome

Newsreader carries the wordmark, headings, big statistics and the scorecard total.
Everything functional is Inter. Anything countable — dates, counts, keys, file names,
code — is JetBrains Mono, via `.meta` or a mono-set component. The density is
deliberate: the reader is a senior engineer skimming for structure before prose.

Newsreader is the family `coding-hacks` already used, kept here so the two
properties read as one publication.

### Copy the wordmark, don't retype it

Take the block from `brand.html` verbatim. The spans are jammed together with no
whitespace between them; a newline or a space next to `.brand__mark` opens a visible
gap in the lockup.

### The wordmark's geometry is measured

- `.brand__mark` is `.72em`. Newsreader 700 has a cap-height ratio of **0.71875**,
  measured in-browser and stable from 400px to 8000px, so the square matches the caps
  beside it to within 0.025px at 20px. (The ratio happens to be near-identical to
  Playfair Display's, so `.72em` survived the family change — but that was checked,
  not assumed. Re-measure on any future swap.)
- There is **no** vertical nudge. `.brand` is `inline-flex` with
  `align-items: baseline`, and an empty inline-block takes its bottom margin edge as
  its baseline — so the browser lands the square on the baseline by itself. Measured
  0.00px off. Adding a `translateY` here introduces a ~1px error rather than fixing
  one.
- That baseline rule depends on the mark being **empty**. Put content inside it, or
  switch it to an inline `<svg>`, and you have to re-measure.

`node tools/verify.js` asserts all of this against a real render, at every size the
page uses the mark, and fails loudly if the serif falls back rather than quietly
measuring the wrong font.

## Sizes

| Class | Size |
|---|---|
| `.brand--sm` | 16px |
| `.brand` | 20px (default) |
| `.brand--lg` | 28px |
| `.brand--hero` | `clamp(34px, 5vw, 52px)` |

Add `.brand--invert` on a dark ground: the word goes white and the mark inverts
(white square, blue inner, white cursor).

## Extending the palette

Two tokens were added beyond the authoritative five, both because the page needed a
role the five could not fill, and both measured:

- `--accent-ink-on-wash` `#0D66CC` — links and small text on `--wash`.
- `--alert` `#BF2E1C` (**5.51:1**) — reserved for naming a problem. It has exactly
  two roles on the SDLC page: the "Your problem" callout that opens each move, and
  the queue block in the timeline diagram. If you find yourself reaching for a third
  role, the page has a hierarchy problem, not a palette problem.

Status colours beyond that are deliberately absent. Where the source design used a
red/amber/green scale — the autonomy matrix, the advisory/enforced sort — the kit
uses a single rising blue ladder instead: `--surface` → `#F4F8FF` → `--wash` →
solid `--primary`. Fewer hues, and the direction of the scale is legible without a
legend.
