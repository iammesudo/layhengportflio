const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
 const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1600/1440});const p=await c.newPage();
 await p.goto('http://localhost:5185/samples/interior/',{waitUntil:'networkidle'});await p.waitForTimeout(5500);
 await p.mouse.move(-10,-10);
 await p.screenshot({path:'hero-cap.png'});await b.close()})();
