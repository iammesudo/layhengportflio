/* Atelier Kambor · fictional interior studio · concept site by Loem Layheng */
(function(){
const D=document,html=D.documentElement;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer=matchMedia('(hover:hover) and (pointer:fine)');
const $=(s,r=D)=>r.querySelector(s),$$=(s,r=D)=>[...r.querySelectorAll(s)];

/* ---------- material textures (generated once, shared as CSS variables) ---------- */
(function(){
  const noise=(f,o,id)=>`url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='${id}'><feTurbulence type='fractalNoise' baseFrequency='${f}' numOctaves='4' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .2  0 0 0 0 .15  0 0 0 0 .1  0 0 0 ${o} 0'/></filter><rect width='100%' height='100%' filter='url(%23${id})'/></svg>`).replace(/%2523/g,'%23')}")`;
  const r=html.style;
  r.setProperty('--noise-lg',noise('.012',.55,'a'));
  r.setProperty('--grain',noise('.3 .006',.5,'b'));
  r.setProperty('--fine',noise('.9',.22,'c'));
  r.setProperty('--trowel',noise('.004',.5,'d'));
  const cane=`<svg xmlns='http://www.w3.org/2000/svg' width='30' height='30'><rect width='30' height='30' fill='%23C9A066'/><rect y='0' width='30' height='4' fill='%23DDBA82'/><rect x='0' width='4' height='30' fill='%23B88E55'/><path d='M0 0L30 30M30 0L0 30' stroke='%23E3C28C' stroke-width='3.2' opacity='.85'/><polygon points='12,6.5 18,6.5 23.5,12 23.5,18 18,23.5 12,23.5 6.5,18 6.5,12' fill='%233A2819'/><polygon points='12,6.5 18,6.5 23.5,12 23.5,13.2 17.6,7.8 12.4,7.8 6.5,13.2 6.5,12' fill='%23000' opacity='.35'/></svg>`;
  r.setProperty('--cane',`url("data:image/svg+xml,${cane}")`);
  let s=7;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
  let pores='';for(let i=0;i<120;i++){pores+=`<ellipse cx='${(rnd()*300).toFixed(1)}' cy='${(rnd()*300).toFixed(1)}' rx='${(1+rnd()*4).toFixed(1)}' ry='${(1+rnd()*3).toFixed(1)}' fill='%23${rnd()>.5?'5a2414':'c47a55'}' opacity='${(.35+rnd()*.5).toFixed(2)}'/>`}
  r.setProperty('--pores',`url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>${pores}</svg>")`);
  const cols=['9C4A2F','6A4630','5E6F5E','2B241F','C9B79A','B07A57','8E8A80'];
  let chips='';for(let i=0;i<190;i++){const x=rnd()*320,y=rnd()*320,rr=2+rnd()*(rnd()>.9?11:5);let p='';const k=5+Math.floor(rnd()*3);for(let j=0;j<k;j++){const a=j/k*6.283+rnd()*.6,d=rr*(.6+rnd()*.5);p+=`${(x+Math.cos(a)*d).toFixed(1)},${(y+Math.sin(a)*d).toFixed(1)} `}
    chips+=`<polygon points='${p}' fill='%23${cols[Math.floor(rnd()*cols.length)]}' opacity='${(.55+rnd()*.45).toFixed(2)}'/>`}
  r.setProperty('--terrazzo',`url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'>${chips}</svg>")`);
})();

/* ---------- reveals ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -10% 0px'});
$$('.rv,.cover').forEach(el=>io.observe(el));

/* ---------- nav: solid over content, mobile menu ---------- */
const nav=$('#nav'),isHome=D.body.classList.contains('home');
const menuBtn=$('.menu-btn'),panel=$('#panel');
function setMenu(open){
  D.body.classList.toggle('menu-open',open);menuBtn.setAttribute('aria-expanded',open);
  menuBtn.querySelector('.t').textContent=open?'Close':'Menu';
  panel.inert=!open;
  if(open){const a=panel.querySelector('a');a&&a.focus()}
}
if(menuBtn&&panel){
  panel.inert=true;
  menuBtn.addEventListener('click',()=>setMenu(!D.body.classList.contains('menu-open')));
  addEventListener('keydown',e=>{if(e.key==='Escape'&&D.body.classList.contains('menu-open')){setMenu(false);menuBtn.focus()}});
  matchMedia('(min-width:1001px)').addEventListener('change',e=>{if(e.matches)setMenu(false)});
}

/* ---------- home hero: the door opens ---------- */
const hero=$('.hero');
if(hero){
  const heroImg=hero.querySelector('img');
  const openDoor=()=>{
    if(RM){hero.classList.add('opened');nav.classList.add('show');return}
    requestAnimationFrame(()=>{hero.classList.add('slit');
      setTimeout(()=>{hero.classList.add('opened');setTimeout(()=>nav.classList.add('show'),900)},1150)});
  };
  let opened=false;const go=()=>{if(!opened){opened=true;setTimeout(openDoor,html.classList.contains('arrive')?650:0)}};
  (heroImg.decode?heroImg.decode():Promise.resolve()).then(go,go);setTimeout(go,2500);
  let vh=innerHeight,tick=false;
  const onS=()=>{tick=false;const y=scrollY;
    if(!RM&&y<vh*1.2)heroImg.parentElement.style.transform=`translate3d(0,${(y*.35).toFixed(1)}px,0)`;
    nav.classList.toggle('solid',y>vh*.82)};
  addEventListener('scroll',()=>{if(!tick){tick=true;requestAnimationFrame(onS)}},{passive:true});
  addEventListener('resize',()=>{vh=innerHeight;onS()});onS();
}

/* ---------- project list: preview follows the cursor ---------- */
const pl=$('#plist'),strip=$('#strip'),pv=$('.preview');
if(pl&&pv&&finePointer.matches){
  const rows=$$('.prow',pl);
  if(!RM){
    let mx=innerWidth/2,my=innerHeight/2,px=mx,py=my,running=false,active=false;
    const loop=()=>{px+=(mx-px)*.09;py+=(my-py)*.09;pv.style.transform=`translate3d(${(px+36).toFixed(1)}px,${(py-pv.offsetHeight*.5).toFixed(1)}px,0)`;
      if(active||Math.abs(mx-px)>.5||Math.abs(my-py)>.5)requestAnimationFrame(loop);else running=false};
    const kick=()=>{if(!running){running=true;requestAnimationFrame(loop)}};
    addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;if(active)kick()},{passive:true});
    rows.forEach((row,i)=>{
      const show=()=>{active=true;strip.style.transform=`translateY(${-i*100}%)`;pv.classList.add('on');kick()};
      row.addEventListener('mouseenter',e=>{if(!pv.classList.contains('on')){px=e.clientX;py=e.clientY}show()});
      row.addEventListener('focus',()=>{const r=row.getBoundingClientRect();mx=px=r.right-r.width*.3;my=py=r.top+r.height/2;show()});
      row.addEventListener('blur',()=>{active=false;pv.classList.remove('on')});
    });
    pl.addEventListener('mouseleave',()=>{active=false;pv.classList.remove('on')});
    addEventListener('scroll',()=>{if(active&&!pl.matches(':hover')&&!pl.contains(D.activeElement)){active=false;pv.classList.remove('on')}},{passive:true});
  }else{
    rows.forEach((row,i)=>row.addEventListener('mouseenter',e=>{strip.style.transform=`translateY(${-i*100}%)`;pv.style.transform=`translate3d(${e.clientX+24}px,${e.clientY-140}px,0)`;pv.classList.add('on')}));
    pl.addEventListener('mouseleave',()=>pv.classList.remove('on'));
  }
}

/* ---------- materials library ---------- */
const sw=$('#swatches');
if(sw){
  const items=$$('li',sw);
  const setMat=i=>items.forEach((li,j)=>{li.classList.toggle('on',i===j);li.querySelector('button').setAttribute('aria-expanded',i===j)});
  items.forEach((li,i)=>{const b=li.querySelector('button');
    b.addEventListener('click',()=>setMat(i));b.addEventListener('focus',()=>setMat(i));
    li.addEventListener('mouseenter',()=>{if(finePointer.matches)setMat(i)})});
}

/* ---------- projects index: filter by type ---------- */
const fl=$('.filters'),pg=$('#pgrid');
if(fl&&pg){
  const cards=$$('.pcard',pg),btns=$$('button',fl),count=$('#pcount');
  const layout=()=>{let k=0;cards.forEach(c=>{c.classList.remove('b','c');if(!c.hidden){const m=k%3;if(m===1)c.classList.add('b');if(m===2)c.classList.add('c');k++}});return k};
  const apply=(t,anim)=>{
    const run=()=>{cards.forEach(c=>c.hidden=!(t==='all'||c.dataset.types.split(' ').includes(t)));const n=layout();
      const name=btns.find(b=>b.dataset.f===t).dataset.name;
      count.textContent=t==='all'?`All ${n} projects`:`${n} ${n===1?'project':'projects'} · ${name}`;pg.classList.remove('fading')};
    btns.forEach(b=>b.setAttribute('aria-pressed',b.dataset.f===t));
    if(anim&&!RM){pg.classList.add('fading');setTimeout(run,450)}else run();
  };
  btns.forEach(b=>b.addEventListener('click',()=>{apply(b.dataset.f,true);try{history.replaceState(null,'',b.dataset.f==='all'?location.pathname:'#'+b.dataset.f)}catch(e){}}));
  const h=location.hash.slice(1);apply(btns.some(b=>b.dataset.f===h)?h:'all',false);
}

/* ---------- before / after ---------- */
$$('.ba-body').forEach(b=>{
  const fig=$('.ba-fig svg',b),cap=$('.ba-cap',b),tabs=$$('.ba-tabs button',b);
  tabs.forEach(t=>t.addEventListener('click',()=>{fig.dataset.state=t.dataset.s;tabs.forEach(x=>x.setAttribute('aria-pressed',x===t));cap.textContent=t.dataset.cap}));
});

/* ---------- Telegram / WhatsApp buttons: say plainly there is no account ---------- */
$$('[data-note]').forEach(b=>{
  const n=D.getElementById(b.dataset.note);if(!n)return;
  b.addEventListener('click',()=>{const open=n.hidden;n.hidden=!open;b.setAttribute('aria-expanded',open)});
});

/* ---------- enquiry form ---------- */
const form=$('#enquiry-form');
if(form){
  const done=$('#done'),errBox=$('#form-errors'),sumEl=$('#summary');
  const file=$('#f-file');
  if(file)file.addEventListener('change',()=>{$('#f-file-name').textContent=file.files.length?[...file.files].map(f=>f.name).join(', '):'No file chosen'});
  const req=[['f-name','Please add your name, so we know who to reply to.'],['f-contact','Please add a Telegram name or a phone number.']];
  const setErr=(id,msg)=>{const f=D.getElementById(id),wrap=f.closest('.field'),e=wrap.querySelector('.err');e.textContent=msg||'';wrap.classList.toggle('bad',!!msg);if(f.matches('input,select,textarea'))f.setAttribute('aria-invalid',!!msg)};
  form.addEventListener('submit',e=>{
    e.preventDefault();
    const bad=[];
    req.forEach(([id,msg])=>{const v=D.getElementById(id).value.trim();setErr(id,v?'':msg);if(!v)bad.push(id)});
    const type=form.querySelector('input[name=type]:checked');
    setErr('type-q',type?'':'Please choose the kind of project.');if(!type)bad.push('type-first');
    if(bad.length){
      errBox.textContent=bad.length===1?'One thing is missing, marked below.':`${bad.length} things are missing, marked below.`;
      const first=D.getElementById(bad[0]==='type-first'?'t-homes':bad[0]);first.focus();return;
    }
    errBox.textContent='';
    const val=n=>{const el=form.elements[n];if(!el)return'';if(el instanceof RadioNodeList){return el.value||''}return(el.value||'').trim()};
    const rows=[['Name',val('name')],['Telegram or phone',val('contact')],['Project',val('type')],['Location',val('location')],['The space is',val('status')],['Budget band',val('budget')],['Ideal start',val('start')],['Language',val('lang')],['Site visit',[val('slot'),val('home')?'Someone home: '+val('home').toLowerCase():''].filter(Boolean).join(' · ')],['Files',file&&file.files.length?[...file.files].map(f=>f.name).join(', '):'']].filter(r=>r[1]);
    sumEl.innerHTML='';rows.forEach(([k,v])=>{const dt=D.createElement('dt'),dd=D.createElement('dd');dt.textContent=k;dd.textContent=v;sumEl.append(dt,dd)});
    $('#done-name').textContent=val('name').split(' ')[0];
    form.hidden=true;done.hidden=false;done.focus();
    done.scrollIntoView({block:'start',behavior:RM?'auto':'smooth'});
  });
  $('#edit').addEventListener('click',()=>{done.hidden=true;form.hidden=false;D.getElementById('f-name').focus()});
  $('#reset').addEventListener('click',()=>{form.reset();if(file)$('#f-file-name').textContent='No file chosen';done.hidden=true;form.hidden=false;D.getElementById('f-name').focus()});
}

/* ---------- page curtain between studio pages ---------- */
if(!RM){
  const cur=$('.curtain');
  D.addEventListener('click',e=>{
    const a=e.target.closest('a[href]');if(!a||!cur)return;
    if(e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.target||a.hasAttribute('download'))return;
    const u=new URL(a.href,location.href);
    if(u.origin!==location.origin||!/^https?:$/.test(u.protocol))return;
    if(u.pathname===location.pathname&&u.search===location.search)return;
    e.preventDefault();
    try{if(u.pathname.includes('/samples/interior/'))sessionStorage.setItem('kb-go','1')}catch(err){}
    cur.classList.add('leave');setTimeout(()=>{location.href=u.href},680);
  });
  addEventListener('pageshow',e=>{if(e.persisted&&cur)cur.classList.remove('leave')});
}

/* ---------- momentum scroll (desktop, fine pointer) ---------- */
if(window.Lenis&&!RM&&matchMedia('(pointer: fine)').matches){
  const lenis=new Lenis({lerp:.085});window.__lenis=lenis;
  (function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(0);
  $$('a[href^="#"]:not(.skip)').forEach(a=>a.addEventListener('click',e=>{const id=a.getAttribute('href');if(id.length>1&&D.querySelector(id)){e.preventDefault();lenis.scrollTo(id,{offset:-(D.querySelector('.ribbon').offsetHeight+nav.offsetHeight+16)});history.replaceState(null,'',id)}}));
}
})();
