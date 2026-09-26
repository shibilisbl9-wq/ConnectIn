// Export each slide as separate transparent layers for PSD assembly: layers/<slide>/<nn>.png + layers.json
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROLES = [
  ['.ci-lead', 'Lead-in'], ['.ci-keyword', 'Keyword'], ['.ci-title', 'Title'], ['.ci-numeral', 'Numeral'],
  ['.ci-rule', 'Gold rule'], ['.ci-tag', 'Key tag'], ['.ci-pointer', 'Pointer'], ['.ci-body', 'Body'],
  ['.ci-fact', 'Fact chip'], ['.ci-warn', 'Warning'], ['.ci-source', 'Small print'], ['.ci-compare__col', 'Compare card'],
  ['.ci-table', 'Table'], ['.ci-date', 'Deadline row'], ['.ci-dm', 'DM keyword'], ['.ci-label', 'Counter'],
];
(async () => {
  const dir = __dirname, only = process.argv[2];
  const files = fs.readdirSync(path.join(dir, 'html')).filter(f => f.endsWith('.html') && (!only || f.startsWith(only))).sort();
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of files) {
    const slide = f.replace('.html', ''), out = path.join(dir, 'layers', slide);
    fs.mkdirSync(out, { recursive: true });
    await p.goto('file://' + path.join(dir, 'html', f));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForLoadState('networkidle');
    await p.addStyleTag({ content: `html,body{background:transparent!important}
      .iso *{visibility:hidden!important} .iso .keep,.iso .keep *{visibility:visible!important}
      .iso .keep-self{visibility:visible!important}` });
    // Tag every layer element with an index; background layer is the post itself without children.
    const specs = await p.evaluate((ROLES) => {
      const post = document.querySelector('.ci-post'), out = [];
      const add = (el, group, name, self) => { el.dataset.layer = out.length; out.push({ group, name, self: !!self }); };
      add(post, 'Background', post.dataset.theme === 'navy' ? 'Navy ground' : 'Ground', true);
      const img = post.querySelector('.ci-post__image'); if (img) add(img, 'Photo', img.classList.contains('ci-post__image--missing') ? 'Photo panel (placeholder)' : 'Photo panel');
      const mod = post.querySelector('.ci-post__model'); if (mod) add(mod, 'Photo', mod.classList.contains('ci-post__model--missing') ? 'Model cut-out (placeholder)' : 'Model cut-out');
      post.querySelectorAll('.ci-post__head img').forEach(el => { if (getComputedStyle(el).display !== 'none') add(el, 'Brand', 'Logo' + (el.classList.contains('ci-logo--reversed') ? ' (reversed)' : '')); });
      const taken = new Set();
      post.querySelectorAll('.ci-post__head, .ci-post__main').forEach(root => {
        root.querySelectorAll('*').forEach(el => {
          if ([...taken].some(t => t.contains(el))) return;
          const r = ROLES.find(([sel]) => el.matches(sel)); if (!r) return;
          taken.add(el);
          const txt = (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 48);
          add(el, 'Text', r[1] + (txt ? ': ' + txt : ''));
        });
      });
      post.querySelectorAll('.ci-post__url, .ci-swipe').forEach(el => add(el, 'Footer', el.classList.contains('ci-swipe') ? 'Swipe cue' : 'Website'));
      return out;
    }, ROLES);
    const layers = [];
    for (let i = 0; i < specs.length; i++) {
      const box = await p.evaluate((i) => {
        document.documentElement.classList.add('iso');
        document.querySelectorAll('.keep,.keep-self').forEach(e => e.classList.remove('keep', 'keep-self'));
        const el = document.querySelector(`[data-layer="${i}"]`);
        el.classList.add(el.dataset.layer === '0' ? 'keep-self' : 'keep');
        const r = el.getBoundingClientRect();
        return { x: r.left, y: r.top, w: r.width, h: r.height };
      }, i);
      // pad for drop shadows and gradient text overhang, clamp to canvas
      const pad = specs[i].group === 'Photo' ? 60 : 12;
      const x = Math.max(0, Math.floor(box.x - pad)), y = Math.max(0, Math.floor(box.y - pad));
      const w = Math.min(1080, Math.ceil(box.x + box.w + pad)) - x, h = Math.min(1350, Math.ceil(box.y + box.h + pad)) - y;
      if (w <= 0 || h <= 0) continue;
      const file = String(i).padStart(2, '0') + '.png';
      await p.screenshot({ path: path.join(out, file), clip: { x, y, width: w, height: h }, omitBackground: true });
      layers.push({ ...specs[i], file, left: x, top: y });
    }
    fs.writeFileSync(path.join(out, 'layers.json'), JSON.stringify(layers, null, 1));
  }
  await b.close();
  console.log('layered', files.length);
})();
