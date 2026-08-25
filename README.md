# The AI-Native SDLC

A single-page field guide for engineering leaders, built on **The Code** design kit.
Static HTML, CSS and one dependency-free JS file. No build step — open `index.html`
or serve the directory.

```
npm run dev            # serve on http://127.0.0.1:5177
npm run contrast       # WCAG check on the palette (python3, no deps)
npm run verify         # headless render checks (needs `npm i` + network)
```

## Layout

```
index.html            the page
assets/
  tokens.css          brand: palette, type scale, space scale, motion
  brand.css           brand: the wordmark, with its measured geometry
  base.css            brand: reset + reusable components
  page.css            page-only: layout and composites
  app.js              copy buttons, scrollspy, progress, scorecard
  mark.svg            the standalone mark, used as the favicon
kit/
  README.md           the rules that are easy to get wrong
  brand.html          copy-paste wordmark markup
tools/
  contrast.py         asserts every colour pair the design depends on
  verify.js           asserts the wordmark baseline and horizontal overflow
```

`tokens.css`, `brand.css` and `base.css` mirror **the-code-kit**. Fix brand-level
bugs there first, then copy across; anything page-specific belongs in `page.css`.

## What was verified, and how

Both checks are reproducible, not asserted:

- **Palette.** `tools/contrast.py` computes WCAG ratios for all thirteen colour
  pairs the page relies on and exits non-zero if any falls short. It confirmed the
  kit's own figures exactly — `#288CFF` is 3.17:1 on the background and 3.34:1
  against white, so it stays a fill colour; `--accent-ink` `#0F6FDB` is 4.62:1 and
  carries links and small text.
- **Wordmark.** `tools/verify.js` measures Playfair Display 700's cap-height ratio
  in-browser (**0.7188**, so the kit's `.72em` square is right to within 0.02px at
  20px) and asserts the square's bottom edge lands on the text baseline at every
  size the page renders it. Measured 0.00px.

## Two open decisions

Both are one-line changes, flagged rather than silently settled:

1. **Section headings are serif.** `h1`, the `<h2>`s, the big statistics and the
   scorecard total all use Playfair Display; everything functional is Inter and
   everything countable is JetBrains Mono. The kit handover is ambiguous here — it
   reserves serif for "the wordmark and display headlines" but also notes the
   newsletter landing page sets headlines in sans. To move the section headings to
   Inter and leave serif to the wordmark, page title and numerals, change one rule
   in `page.css`:

   ```css
   .section h2 { font-family: var(--sans); font-weight: 600; letter-spacing: -.02em; }
   ```

2. **One unverified claim was pulled from the page.** The paragraph in Move 04
   originally cited "8x more code shipped, ~80% AI-written" carrying a `[verify]`
   marker. It now makes the same argument without the two numbers, and the marker
   survives as an HTML comment above that paragraph. Source it to the Jason Clinton
   post and restore the figures, or leave the qualitative version.

## The kit's `translateY` was removed

`brand.css` drops the `translateY(.048em)` nudge the handover documented. With the
markup in `kit/brand.html` — an inline-flex `.brand` with `align-items: baseline`
and an **empty** inline-block mark — the browser already puts the square's bottom
margin edge on the baseline. The nudge measured as a 0.96px error at 20px, not a
correction. `npm run verify` is the regression test. If the mark ever gains inner
content or becomes an inline `<svg>`, that baseline rule stops holding and the
offset has to be re-measured.

## Deploying

Any static host. There is nothing to build; upload the repository root.
The three brand faces load from Google Fonts and each has a real fallback stack.

For a single self-contained file — one HTML with the CSS, JS and favicon
inlined, for pasting into a CMS or an email-tool landing page:

```
python3 tools/build-single.py dist/ai-native-sdlc.html
python3 tools/build-single.py --fragment dist/fragment.html   # no <html> shell
```
