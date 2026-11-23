const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs=[];p.on('console',m=>errs.push(m.text()));p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://localhost:5185/samples/interior/studio.html', { waitUntil: 'networkidle' });
  await p.locator('#swatches').scrollIntoViewIfNeeded(); await p.waitForTimeout(1500);
  await p.locator('#swatches').screenshot({ path: 'shots/sw.png' });
  console.log(errs.join('\n'), await p.evaluate(()=>getComputedStyle(document.querySelector('.t-terrazzo')).backgroundImage.slice(0,120)));
  await b.close();
})();
