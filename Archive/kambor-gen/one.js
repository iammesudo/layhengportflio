const { chromium, devices } = require('playwright');
(async()=>{const b=await chromium.launch();
 const [url,sel,out,dev]=process.argv.slice(2);
 const c=await b.newContext(dev?devices[dev]:{viewport:{width:1440,height:900}});const p=await c.newPage();
 await p.goto(url,{waitUntil:'networkidle'});await p.waitForTimeout(1500);
 const l=p.locator(sel).first();await l.scrollIntoViewIfNeeded();await p.waitForTimeout(1800);await l.screenshot({path:out});await b.close()})();
