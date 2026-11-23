const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('http://localhost:5185/samples/interior/studio.html', { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => [...document.querySelectorAll('#swatches li')].map(li => { const s = getComputedStyle(li); return [li.getBoundingClientRect().width.toFixed(0), s.flexGrow, s.flexBasis, s.minWidth, getComputedStyle(li.querySelector('.sw')).width] }));
  console.log(JSON.stringify(r));
  await b.close();
})();
