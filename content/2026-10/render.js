// Render html/*.html to posts/<id>/<nn>.png at 1080 x 1350.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = __dirname, files = fs.readdirSync(path.join(dir, 'html')).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of files) {
    const [id, nn] = f.replace('.html', '').split('-');
    fs.mkdirSync(path.join(dir, 'posts', id), { recursive: true });
    await p.goto('file://' + path.join(dir, 'html', f));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForLoadState('networkidle');
    // flag overflow: anything in main extending into the footer band
    const over = await p.evaluate(() => {
      const m = document.querySelector('.ci-post__main'), ft = document.querySelector('.ci-post__foot');
      const last = [...m.children].pop(); if (!last) return 0;
      return Math.round(last.getBoundingClientRect().bottom - (ft.getBoundingClientRect().top - 24));
    });
    if (over > 0) console.log('OVERFLOW', f, over + 'px');
    const hit = await p.evaluate(() => {
      const img = document.querySelector('.ci-post__image'); if (!img) return null;
      const r = img.getBoundingClientRect();
      const els = [...document.querySelectorAll('.ci-post__main *')].filter(e => e.children.length === 0 || e.matches('p'));
      const bad = els.find(e => { const q = e.getBoundingClientRect(); return q.right > r.left && q.bottom > r.top && q.width > 0; });
      return bad ? bad.textContent.slice(0, 40) : null;
    });
    if (hit) console.log('UNDER IMAGE', f, JSON.stringify(hit));
    await p.screenshot({ path: path.join(dir, 'posts', id, nn + '.png') });
  }
  await b.close();
  console.log('rendered', files.length);
})();
