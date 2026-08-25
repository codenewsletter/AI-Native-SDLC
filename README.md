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
- **Wordmark.** `tools/verify.js` measures Newsreader 700's cap-height ratio
  in-browser — **0.71875**, stable from 400px to 8000px, so the kit's `.72em` square
  is right to within 0.025px at 20px — and asserts the square's bottom edge lands on
  the text baseline at every size the page renders it. Measured 0.00px.

## The square rule

Every radius token is `0` and there are no shadow tokens. Cards, buttons, inputs and
diagram nodes are all square, and structure comes from alignment and one hairline
border. Two places where that changed the design rather than just the CSS:

- **The autonomy matrix and the advisory/enforced sort lost their outer card.** Both
  were a grid of bordered cells sitting inside another bordered box; with rounding
  gone, the nested frame was the loudest thing on the screen. One frame is enough.
- **Hover states stopped moving.** Cells darken their border instead of lifting.

## Figures

Four diagrams, all authored as inline SVG from generators in `tools/figures/`, so
the geometry is computed rather than hand-placed. Re-run a generator and paste its
output back into `index.html` to change one:

```
python3 tools/figures/line-and-loop.py     # The shift
python3 tools/figures/cycle-time.py        # The gap
python3 tools/figures/adoption-map.py      # Rollout
```

Three of them follow diagrams in [Anthropic's AI-Native SDLC
playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), redrawn in The
Code's palette and credited in each figure's caption. Two deliberate departures:

- **The loop's hub is labelled "agents", not a product mark.** The page bills itself
  vendor-neutral, and a logo in the centre would contradict that.
- **The cycle-time figure has a third row the original doesn't.** Anthropic's version
  ends at "cycle time reclaimed"; this page's argument is that the reclaimed time
  refills with queue, so row 3 shows that and the caption says whose claim is whose.
  Rows 1 and 3 end at the same x on purpose.

The fourth, the lifecycle loop in Move 03, is ours.

## One open decision

**An unverified claim was pulled from the page.** The paragraph in Move 04 originally
cited "8x more code shipped, ~80% AI-written" carrying a `[verify]` marker. It now
makes the same argument without the two numbers, and the marker survives as an HTML
comment above that paragraph. Source it to the Jason Clinton post and restore the
figures, or leave the qualitative version.

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
