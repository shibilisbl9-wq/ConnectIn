// Render scene.html / textures.html variants to PNG in headless Chromium (WebGL via SwiftShader).
// Pages are fetched from a local static server rooted at brand/ (see render_all.sh).
// usage: node shoot.js <page> <query> <out.png> [<page> <query> <out.png> ...]
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = `http://127.0.0.1:${process.env.PORT || 8765}/`;
(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  for (let i = 0; i < args.length; i += 3) {
    const [pg, query, out] = args.slice(i, i + 3);
    const page = await browser.newPage();
    page.on('pageerror', e => console.log('[error]', e.message));
    await page.goto(`${BASE}${pg}?${query}`);
    await page.waitForFunction(() => window.__done === true, null, { timeout: 600000 });
    const data = await page.evaluate(() => document.querySelector('canvas').toDataURL('image/png'));
    fs.writeFileSync(out, Buffer.from(data.split(',')[1], 'base64'));
    console.log(out);
    await page.close();
  }
  await browser.close();
})();
