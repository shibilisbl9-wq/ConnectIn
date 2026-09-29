// Screenshot a moodboard page at 2x once its fonts have loaded.
// usage: node snap.js <page> <out.png>
const { chromium } = require('playwright');
const BASE = `http://127.0.0.1:${process.env.PORT || 8765}/`;
(async () => {
  const [pg, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2400, height: 1500 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('[error]', e.message));
  await page.goto(BASE + pg, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 2400, height: 1500 } });
  console.log(out);
  await browser.close();
})();
