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
    // cover objects: record every text box so check_objects.py can test it against the object's pixels
    const boxes = await p.evaluate(() => {
      if (!document.querySelector('.ci-post__object')) return null;
      const els = [...document.querySelectorAll('.ci-post__main *, .ci-post__foot > *')].filter(e => e.children.length === 0 || e.matches('p, .ci-tag, .ci-cta, .ci-swipe'));
      return els.map(e => { const q = e.getBoundingClientRect(); return { text: (e.textContent || '').trim().slice(0, 40), x: q.left, y: q.top, w: q.width, h: q.height }; })
        .filter(b => b.w > 0 && b.h > 0);
    });
    if (boxes) { fs.mkdirSync(path.join(dir, 'objects', 'boxes'), { recursive: true }); fs.writeFileSync(path.join(dir, 'objects', 'boxes', id + '.json'), JSON.stringify(boxes)); }
    await p.screenshot({ path: path.join(dir, 'posts', id, nn + '.png') });
  }
  await b.close();
  console.log('rendered', files.length);
})();
