/* The Metamorphosis: one pinned stage, scenes change in place, driven by scroll progress. */
(() => {
  const doc = document.documentElement;
  const RM = matchMedia('(prefers-reduced-motion: reduce)');
  const reduced = () => RM.matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const seg = (p, a, b) => clamp((p - a) / (b - a));
  const eio = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const eout = t => 1 - Math.pow(1 - t, 3);

  const track = document.querySelector('.track');
  const veil = document.querySelector('.veil');
  const T = .7; // length of each arrival, in viewport heights of scroll

  // deterministic jitter for ragged ink edges
  let seed = 1915;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

  function bind(sc) {
    const el = sc.el;
    sc.svg = el.querySelector('svg.art');
    sc.fx = sc.svg ? sc.svg.getAttribute('preserveAspectRatio') : null;
    sc.layers = Array.from(el.querySelectorAll('.ly')).map(g => ({ g, d: parseFloat(g.dataset.d) }));
    sc.apples = Array.from(el.querySelectorAll('.apple'));
    sc.rays = el.querySelector('.rays'); sc.sun = el.querySelector('.sunrays'); sc.hand = el.querySelector('.hand-m');
    sc.spin = el.querySelector('.spin'); sc.fig = el.querySelector('.stretchfig');
    if (sc.svg) {
      if (sc.pf && vw / vh < .8) sc.svg.setAttribute('preserveAspectRatio', sc.pf);
      if (!sc.vis || reduced()) sc.svg.pauseAnimations();
    }
  }
  const S = Array.from(document.querySelectorAll('.scene')).map((el, i) => {
    const o = (el.dataset.o || '50% 50%').split(' ').map(v => parseFloat(v) / 100);
    const jag = Array.from({ length: 64 }, () => rnd());
    const caps = Array.from(el.querySelectorAll('.caps > *'));
    const sc = { el, i, o, jag, caps, tr: el.dataset.tr || 'none', len: parseFloat(el.dataset.len || 1.3),
      pf: el.dataset.pf, art: el.querySelector('.art-wrap'), start: 0 };
    return sc;
  });

  // the first scenes are inline; the rest of the drawings arrive after first paint
  function loadScenes() {
    const jobs = S.filter(sc => sc.el.querySelector('.art-ph'));
    jobs.forEach(sc => {
      const ph = sc.el.querySelector('.art-ph');
      fetch(ph.dataset.src).then(r => r.ok ? r.text() : Promise.reject(r.status)).then(txt => {
        ph.insertAdjacentHTML('afterend', txt);
        ph.remove();
        bind(sc);
        lastY = -1;
      }).catch(() => {});
    });
  }
  let vw = innerWidth, vh = innerHeight, total = 0;
  function layout() {
    vw = innerWidth; vh = innerHeight;
    let s = 0;
    S.forEach(sc => { sc.start = s; s += sc.len; });
    total = s;
    track.style.height = (total * vh + vh) + 'px';
    const portrait = vw / vh < .8;
    S.forEach(sc => { if (sc.svg && sc.pf && sc.fx) sc.svg.setAttribute('preserveAspectRatio', portrait ? sc.pf : sc.fx); });
  }

  // where a point of the drawing (fractions of the viewBox) lands on screen, given "slice" fitting
  function focus(sc) {
    if (!sc.svg) return [vw * sc.o[0], vh * sc.o[1]];
    const vb = sc.svg.viewBox.baseVal;
    const k = Math.max(vw / vb.width, vh / vb.height);
    const par = sc.svg.getAttribute('preserveAspectRatio') || '';
    const ax = par.includes('xMin') ? 0 : par.includes('xMax') ? 1 : .5;
    const ay = par.includes('YMin') ? 0 : par.includes('YMax') ? 1 : .5;
    return [(vw - vb.width * k) * ax + sc.o[0] * vb.width * k, (vh - vb.height * k) * ay + sc.o[1] * vb.height * k];
  }

  const px = (x, y) => `${x.toFixed(1)}px ${y.toFixed(1)}px`;
  function inkClip(sc, k) {
    const [cx, cy] = focus(sc);
    const far = Math.max(Math.hypot(cx, cy), Math.hypot(vw - cx, cy), Math.hypot(cx, vh - cy), Math.hypot(vw - cx, vh - cy));
    const R = far * 1.25 * eout(k);
    const n = sc.jag.length, pts = [];
    for (let i = 0; i < n; i++) {
      const a = i / n * Math.PI * 2;
      const j = sc.jag[i], spike = j > .86 ? (j - .86) * 2.6 : 0;
      const r = R * (.84 + j * .2 + spike * (1 - k));
      pts.push(px(cx + Math.cos(a) * r, cy + Math.sin(a) * r));
    }
    return `polygon(${pts.join(',')})`;
  }
  function wipeClip(sc, k) {
    const x0 = -.35 * vw + eio(k) * 1.75 * vw, pts = [px(-10, -10)], n = 18;
    for (let i = 0; i <= n; i++) {
      const y = i / n * vh, tooth = (sc.jag[i] - .5) * 46 + (i % 2 ? 14 : -14);
      pts.push(px(x0 - y * .32 + tooth, y));
    }
    pts.push(px(-10, vh + 10));
    return `polygon(${pts.join(',')})`;
  }
  function rayClip(sc, k) {
    const [cx, cy] = focus(sc);
    const R = Math.hypot(vw, vh) * 1.5, a0 = Math.PI * .5 - .3, span = eio(k) * Math.PI * 2.02;
    const pts = [px(cx, cy)], n = 40;
    for (let i = 0; i <= n; i++) {
      const a = a0 + span * i / n;
      pts.push(px(cx + Math.cos(a) * R, cy + Math.sin(a) * R));
    }
    return `polygon(${pts.join(',')})`;
  }

  function setT(el, origin, t) { if (!el) return; el.style.transformBox = 'view-box'; el.style.transformOrigin = origin; el.style.transform = t; }

  function beats(sc, t) {
    const rm = reduced();
    const tt = rm ? 1 : t;
    sc.layers.forEach(({ g, d }) => { g.style.transform = rm ? '' : `translate(0px, ${((.5 - t) * d * 160).toFixed(1)}px)`; });
    sc.apples.forEach((a, i) => {
      const k = eout(seg(tt, .35 + i * .06, .7 + i * .05));
      a.style.transform = `translate(${((1 - k) * 60).toFixed(1)}px, ${(-(1 - k) * 760).toFixed(1)}px)`;
    });
    setT(sc.rays, '1180px 380px', `rotate(${((tt - .5) * 12).toFixed(2)}deg)`);
    setT(sc.sun, '1180px 300px', `rotate(${(tt * 16).toFixed(2)}deg)`);
    setT(sc.hand, '800px 470px', `rotate(${(tt * 30).toFixed(2)}deg)`);
    setT(sc.spin, '800px 470px', `rotate(${(tt * -8).toFixed(2)}deg)`);
    const st = eio(seg(tt, .4, .85));
    setT(sc.fig, '800px 900px', `scale(${(.97 + st * .05).toFixed(4)}, ${(.92 + st * .1).toFixed(4)})`);
    // captions come in one by one once the scene has arrived, and stay until it leaves
    const n = sc.caps.length, a0 = sc.i === 0 ? 0 : T / sc.len;
    sc.caps.forEach((c, j) => c.classList.toggle('on', t >= a0 + .04 + j * ((1 - a0 - .15) / Math.max(1, n))));
  }

  function show(sc, on) {
    if (sc.vis === on) return;
    sc.vis = on;
    sc.el.classList.toggle('vis', on);
    if (sc.svg) { if (on && !reduced()) sc.svg.unpauseAnimations(); else sc.svg.pauseAnimations(); }
  }
  function reset(sc) {
    sc.el.style.clipPath = ''; sc.el.style.opacity = ''; sc.el.style.zIndex = '';
    if (sc.art) { sc.art.style.transform = ''; sc.art.style.transformOrigin = ''; }
  }

  let lastY = -1;
  function frame() {
    const y = scrollY;
    if (y === lastY) return;
    lastY = y;
    const P = y / vh;
    let cur = 0;
    S.forEach((sc, i) => { if (P >= sc.start) cur = i; });
    const inc = S[cur], k = cur === 0 ? 1 : clamp((P - inc.start) / T);
    const out = S[cur - 1];
    const rm = reduced();
    veil.style.opacity = 0;
    S.forEach((sc, i) => {
      if (i === cur || (i === cur - 1 && k < 1)) return;
      show(sc, false); reset(sc);
    });
    // the scene that is leaving
    if (out && k < 1) {
      show(out, true); reset(out);
      out.el.style.zIndex = cur;
      beats(out, clamp((P - out.start) / out.len));
      if (!rm && inc.tr === 'zoom') {
        const [fx, fy] = focus(inc);
        const z = eio(k);
        out.art.style.transformOrigin = px(fx, fy);
        out.art.style.transform = `scale(${(1.05 + z * 2.6).toFixed(4)})`;
        out.el.style.opacity = (1 - seg(k, .55, 1)).toFixed(3);
      }
    }
    // the scene that is arriving (or holding)
    show(inc, true); reset(inc);
    inc.el.style.zIndex = cur + 1;
    const t = clamp((P - inc.start) / inc.len);
    beats(inc, t);
    if (inc.art && !rm) inc.art.style.transform = `scale(${(1 + t * .06).toFixed(4)})`;
    if (k < 1) {
      if (rm) inc.el.style.opacity = k.toFixed(3);
      else if (inc.tr === 'ink') inc.el.style.clipPath = inkClip(inc, k);
      else if (inc.tr === 'wipe') inc.el.style.clipPath = wipeClip(inc, k);
      else if (inc.tr === 'ray') inc.el.style.clipPath = rayClip(inc, k);
      else if (inc.tr === 'zoom') {
        inc.el.style.opacity = seg(k, .4, 1).toFixed(3);
        inc.art.style.transform = `scale(${(1.35 - .35 * eout(k)).toFixed(4)})`;
      } else if (inc.tr === 'black') {
        veil.style.opacity = (k < .5 ? k * 2 : 2 - k * 2).toFixed(3);
        inc.el.style.opacity = k < .5 ? 0 : 1;
      }
    }
  }

  function loop() { frame(); requestAnimationFrame(loop); }

  // smooth momentum on fine pointers only
  function startLenis() {
    if (reduced() || !window.Lenis || !matchMedia('(pointer: fine)').matches) return;
    const lenis = new window.Lenis({ lerp: .09, smoothWheel: true });
    const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }

  layout();
  S.forEach(bind);
  loop();
  addEventListener('resize', () => { layout(); lastY = -1; });
  RM.addEventListener && RM.addEventListener('change', () => { S.forEach(sc => { sc.vis = null; }); lastY = -1; });
  const ready = () => { startLenis(); setTimeout(loadScenes, 60); };
  if (document.readyState === 'complete') ready(); else addEventListener('load', ready);
})();
