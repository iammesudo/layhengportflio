const { chromium, devices } = require('playwright');
const B='http://localhost:5185/samples/interior/';const O='shots/ix-';
(async()=>{
  const b=await chromium.launch();
  const ctx=await b.newContext({viewport:{width:1440,height:900}});const p=await ctx.newPage();
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  // form: submit empty
  await p.goto(B+'contact.html#enquiry',{waitUntil:'networkidle'});await p.waitForTimeout(1200);
  await p.click('button[type=submit]');await p.waitForTimeout(400);
  console.log('focused after empty submit:',await p.evaluate(()=>document.activeElement.id), await p.textContent('#form-errors'));
  await p.locator('.fields').screenshot({path:O+'form-err.png'});
  await p.fill('#f-name','Sokha Test');await p.fill('#f-contact','@sokha');
  await p.check('input[name=type][value=Shophouse]',{force:true});await p.check('input[name=budget][value="One floor"]',{force:true});
  await p.selectOption('#f-start','Before Khmer New Year');
  await p.click('button[type=submit]');await p.waitForTimeout(1500);
  console.log('focused after ok submit:',await p.evaluate(()=>document.activeElement.id));
  await p.screenshot({path:O+'form-done.png'});
  // filters
  await p.goto(B+'projects/',{waitUntil:'networkidle'});await p.waitForTimeout(800);
  await p.click('button[data-f=hospitality]');await p.waitForTimeout(1200);
  console.log('count:',await p.textContent('#pcount'),'url',p.url());
  await p.screenshot({path:O+'filter.png'});
  // before after
  await p.goto(B+'projects/shophouse-in-daun-penh/',{waitUntil:'networkidle'});
  await p.locator('.ba').scrollIntoViewIfNeeded();await p.click('.ba-tabs button[data-s=after]');await p.waitForTimeout(1200);
  await p.locator('.ba-body').screenshot({path:O+'after.png'});
  // curtain nav
  await p.goto(B,{waitUntil:'networkidle'});await p.waitForTimeout(4000);
  await p.click('.nav a[href="studio.html"]');await p.waitForTimeout(350);await p.screenshot({path:O+'curtain-mid.png'});
  await p.waitForURL('**/studio.html');await p.waitForTimeout(300);await p.screenshot({path:O+'arrive-mid.png'});await p.waitForTimeout(1500);await p.screenshot({path:O+'arrived.png'});
  // walk
  await p.goto(B+'projects/house-in-toul-kork/',{waitUntil:'networkidle'});await p.waitForTimeout(800);
  const wt=await p.evaluate(()=>document.getElementById('walk').getBoundingClientRect().top+scrollY);
  for(const k of [0.05,0.3,0.7]){await p.evaluate(y=>scrollTo(0,y),wt+k*4200);await p.waitForTimeout(2200);await p.screenshot({path:O+'walk-'+k+'.png'})}
  // keyboard on home
  await p.goto(B,{waitUntil:'networkidle'});await p.waitForTimeout(4000);
  const seq=[];for(let i=0;i<12;i++){await p.keyboard.press('Tab');seq.push(await p.evaluate(()=>{const a=document.activeElement;return a.tagName+':'+(a.textContent||'').trim().slice(0,22)}))}
  console.log(seq.join(' | '));
  await p.screenshot({path:O+'kbd.png'});
  console.log('errs',errs);
  // phone menu
  const pc=await b.newContext(devices['iPhone 13']);const q=await pc.newPage();
  await q.goto(B+'services.html',{waitUntil:'networkidle'});await q.waitForTimeout(800);
  await q.click('.menu-btn');await q.waitForTimeout(1200);await q.screenshot({path:O+'menu.png'});
  // reduced motion
  const rc=await b.newContext({viewport:{width:1440,height:900},reducedMotion:'reduce'});const r=await rc.newPage();
  await r.goto(B,{waitUntil:'networkidle'});await r.waitForTimeout(500);await r.screenshot({path:O+'rm-home.png'});
  await r.goto(B+'projects/coffee-room-in-bkk1/',{waitUntil:'networkidle'});await r.waitForTimeout(300);await r.screenshot({path:O+'rm-case.png'});
  await b.close();
})();
