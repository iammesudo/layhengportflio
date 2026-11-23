const { chromium, devices } = require('playwright');
const OUT = process.argv[2] || '/tmp/claude-0/-home-user/ac673f5a-9913-5072-85e2-02bcdc1e999e/scratchpad/kb/shots';
const only = process.argv[3] ? process.argv[3].split(',') : null;
const B = 'http://localhost:5185/samples/interior/';
const PAGES = ['', 'projects/', 'projects/house-in-toul-kork/', 'projects/shophouse-in-daun-penh/', 'projects/flat-by-the-river/', 'projects/guest-rooms-in-kampot/', 'projects/coffee-room-in-bkk1/', 'projects/joinery-in-tonle-bassac/', 'studio.html', 'services.html', 'journal.html', 'contact.html'];
const VIEWS = { desk: { viewport: { width: 1440, height: 900 } }, ipad: devices['iPad Pro 11'], phone: devices['iPhone 13'] };
const fs = require('fs'); fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  for (const [vn, opt] of Object.entries(VIEWS)) {
    if (only && !only.includes(vn)) continue;
    const ctx = await b.newContext(opt);
    for (const pg of PAGES) {
      const p = await ctx.newPage(); const errs = [];
      p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()) });
      p.on('pageerror', e => errs.push('pageerror: ' + e.message));
      p.on('requestfailed', r => errs.push('failed: ' + r.url()));
      p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()) });
      await p.goto(B + pg, { waitUntil: 'networkidle' });
      await p.waitForTimeout(pg === '' ? 4200 : 1600);
      const name = (pg.replace(/\/$/, '').replace(/\//g, '_').replace('.html', '') || 'home');
      await p.screenshot({ path: `${OUT}/${vn}-${name}-0.png` });
      const H = await p.evaluate(() => document.documentElement.scrollHeight);
      const vh = await p.evaluate(() => innerHeight);
      for (let y = 0; y < H; y += Math.round(vh * .6)) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(120); }
      await p.waitForTimeout(1500);
      const ov = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth, wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && getComputedStyle(e).position !== 'fixed' && r.width > 0 }).slice(0, 5).map(e => e.tagName + '.' + e.className) }));
      if (vn !== 'desk' || !pg.includes('toul')) {
        await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(400);
        await p.screenshot({ path: `${OUT}/${vn}-${name}-full.png`, fullPage: true });
      }
      console.log(vn, pg || 'home', 'H=' + H, ov.sw > ov.iw ? 'OVERFLOW ' + JSON.stringify(ov) : 'ok', errs.length ? errs.join(' | ') : '');
      await p.close();
    }
    await ctx.close();
  }
  await b.close();
})();
