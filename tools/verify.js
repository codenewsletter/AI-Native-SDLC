/* Renders the page in headless Chromium and asserts the things that are
   easy to break silently:

     1. no console errors, no failed requests
     2. the wordmark square lands exactly on the Playfair baseline
     3. the page never scrolls horizontally, at any of three widths

   Usage:  npm run dev   (in one shell)
           npm run verify

   Needs the real Playfair Display metrics — the baseline assertion is
   meaningless against a fallback serif, so a missing face fails loudly
   rather than passing quietly.

   Env:
     URL=…        page to check          (default http://127.0.0.1:5177/)
     CHROME=…     chromium binary        (default: playwright's own)
     FONT_CSS=…   a local @font-face css served in place of Google Fonts,
                  for running this offline
*/
const { chromium } = require('playwright');
const fs = require('fs');

const URL = process.env.URL || 'http://127.0.0.1:5177/';
const WIDTHS = [390, 768, 1280];
const fails = [];

(async () => {
  const browser = await chromium.launch(
    process.env.CHROME ? { executablePath: process.env.CHROME } : {}
  );

  for (const width of WIDTHS) {
    const page = await browser.newPage({ viewport: { width, height: 1000 } });
    const noise = [];
    page.on('console', m => { if (m.type() === 'error') noise.push(m.text()); });
    page.on('pageerror', e => noise.push('pageerror: ' + e.message));
    page.on('requestfailed', r => noise.push('requestfailed: ' + r.url()));

    if (process.env.FONT_CSS) {
      const css = fs.readFileSync(process.env.FONT_CSS, 'utf8');
      await page.route('https://fonts.googleapis.com/**', r =>
        r.fulfill({ contentType: 'text/css', body: css }));
    }

    await page.goto(URL, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    const families = await page.evaluate(() =>
      [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
    for (const need of ['Playfair Display', 'Inter', 'JetBrains Mono']) {
      if (!families.includes(need)) fails.push(`[${width}] font not loaded: ${need}`);
    }

    const overflow = await page.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (overflow > 0) fails.push(`[${width}] page scrolls horizontally by ${overflow}px`);

    const marks = await page.evaluate(() => {
      const c = document.createElement('canvas').getContext('2d');
      c.font = '700 400px "Playfair Display"';
      const capRatio = c.measureText('H').actualBoundingBoxAscent / 400;
      return [...document.querySelectorAll('.brand')].map(brand => {
        // a zero-size inline-block: flex baseline alignment puts its bottom
        // edge exactly on the text baseline, which is what we compare against
        const probe = document.createElement('span');
        probe.style.cssText = 'display:inline-block;width:0;height:0;padding:0;margin:0';
        brand.appendChild(probe);
        const baseline = probe.getBoundingClientRect().bottom;
        probe.remove();
        const r = brand.querySelector('.brand__mark').getBoundingClientRect();
        const size = parseFloat(getComputedStyle(brand).fontSize);
        return {
          size,
          capRatio: +capRatio.toFixed(4),
          offBaseline: +(r.bottom - baseline).toFixed(3),
          offCapTop: +(r.top - (baseline - capRatio * size)).toFixed(3)
        };
      });
    });

    marks.forEach((m, i) => {
      if (Math.abs(m.offBaseline) > 0.1) fails.push(`[${width}] wordmark #${i} sits ${m.offBaseline}px off the baseline`);
      if (Math.abs(m.offCapTop) > 0.5) fails.push(`[${width}] wordmark #${i} is ${m.offCapTop}px off the cap height`);
    });

    if (noise.length) noise.forEach(n => fails.push(`[${width}] ${n}`));

    console.log(`${String(width).padStart(4)}px  overflow ${overflow}px  ` +
      marks.map(m => `mark@${m.size}px baseline${m.offBaseline >= 0 ? '+' : ''}${m.offBaseline} cap${m.offCapTop >= 0 ? '+' : ''}${m.offCapTop}`).join('  ') +
      `  cap-ratio ${marks[0] ? marks[0].capRatio : 'n/a'}`);

    await page.close();
  }

  await browser.close();

  if (fails.length) {
    console.error('\nFAILED:');
    fails.forEach(f => console.error('  - ' + f));
    process.exit(1);
  }
  console.log('\nall checks pass');
})();
