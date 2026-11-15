/* ================= Mock screens =================
   Illustrative only. To use a real screenshot later, replace a mock with `<img src="..." alt="...">`. */
const T = (x, y, s, w, fill, txt, anchor) => `<text x="${x}" y="${y}" font-family="Inter,sans-serif" font-size="${s}" font-weight="${w}" fill="${fill}"${anchor ? ` text-anchor="${anchor}"` : ''}>${txt}</text>`;
const R = (x, y, w, h, r, fill, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" ${extra}/>`;
const bar = (x, y, w, fill = '#D9D5CC', h = 5) => R(x, y, w, h, h / 2, fill);

// Phone shell: 180 x 370
const phone = body => `<svg viewBox="0 0 180 370" xmlns="http://www.w3.org/2000/svg">
  ${R(0, 0, 180, 370, 30, '#0B0C0E')}${R(6, 6, 168, 358, 25, '#FBFAF7')}
  ${R(66, 13, 48, 13, 6.5, '#0B0C0E')}
  ${T(22, 23, 8, 600, '#111', '9:41')}${R(140, 17, 18, 7, 2, 'none', 'stroke="#111" stroke-width="1"')}${R(142, 19, 12, 3, 1, '#111')}
  ${body}
  ${R(62, 352, 56, 4, 2, '#111')}
</svg>`;
// Browser shell: 480 x 310
const web = (title, body, url = 'console') => `<svg viewBox="0 0 480 310" xmlns="http://www.w3.org/2000/svg">
  ${R(0, 0, 480, 310, 10, '#FBFAF7')}${R(0, 0, 480, 28, 10, '#ECE9E2')}${R(0, 18, 480, 10, 0, '#ECE9E2')}
  <circle cx="16" cy="14" r="4" fill="#E06C5A"/><circle cx="29" cy="14" r="4" fill="#E8B14C"/><circle cx="42" cy="14" r="4" fill="#7DBE6B"/>
  ${R(160, 7, 160, 14, 7, '#FBFAF7')}${T(240, 17, 7.5, 400, '#888', url, 'middle')}
  ${T(24, 56, 13, 700, '#111', title)}
  ${body}
</svg>`;


/* ---------- SmartNas telco mock pieces (illustrative layout, no real assets) ---------- */
const G = '#16A34A', GD = '#0E7A35';
const telDefs = `<defs>
  <linearGradient id="tBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFEBD7"/><stop offset=".45" stop-color="#EEF7F0"/><stop offset="1" stop-color="#F7FAF8"/></linearGradient>
  <linearGradient id="tTop" x1="0" x2="1"><stop offset="0" stop-color="#8E3CA8"/><stop offset="1" stop-color="#F07A23"/></linearGradient>
  <linearGradient id="tHist" x1="0" x2="1"><stop offset="0" stop-color="#119A3B"/><stop offset="1" stop-color="#F2DC3C"/></linearGradient>
  <linearGradient id="tPromo" x1="0" x2="1"><stop offset="0" stop-color="#DDF3E2"/><stop offset="1" stop-color="#9FDDB0"/></linearGradient>
  <linearGradient id="tWarm" x1="0" x2="1"><stop offset="0" stop-color="#F2B53A"/><stop offset="1" stop-color="#C2307A"/></linearGradient>
  <linearGradient id="tBtn" x1="0" x2="1"><stop offset="0" stop-color="#0F9A3E"/><stop offset="1" stop-color="#2BD12B"/></linearGradient>
</defs>`;
// every phone gets its own gradient ids, so a hidden copy can't break the visible one
let telN = 0;
const telInner = body => { const k = ++telN; return `${R(0, 0, 180, 370, 30, '#0B0C0E')}${telDefs}${R(6, 6, 168, 358, 25, 'url(#tBg)')}
  ${R(62, 12, 56, 15, 7.5, '#0B0C0E')}<circle cx="74" cy="19.5" r="4" fill="none" stroke="#3BE07A" stroke-width="1.6"/>
  ${T(22, 23, 8, 600, '#111', '9:41')}${[0, 1, 2, 3].map(i => R(130 + i * 4, 21 - i * 1.5, 2.6, 3 + i * 1.5, .8, '#111')).join('')}${R(150, 16, 16, 8, 2.5, '#111')}
  ${body}`.replace(/id="t(\w+)"/g, `id="t$1_${k}"`).replace(/url\(#t(\w+)\)/g, `url(#t$1_${k})`); };
const tel = body => `<svg viewBox="0 0 180 370" xmlns="http://www.w3.org/2000/svg">${telInner(body)}</svg>`;
const telIcon = (x, y, kind) => {
  const s = `fill="none" stroke="${G}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"`;
  return {
    signal: `<path d="M${x - 5} ${y + 5}v-2M${x - 1.5} ${y + 5}v-4.5M${x + 2} ${y + 5}v-7M${x + 5.5} ${y + 5}v-9.5" ${s}/>`,
    shield: `<path d="M${x} ${y - 6}l6 2.5v3.5c0 4-2.6 6-6 7-3.4-1-6-3-6-7v-3.5z M${x - 2.5} ${y + .5}l1.8 1.8 3.4-3.6" ${s}/>`,
    chip: `<rect x="${x - 5}" y="${y - 5}" width="10" height="10" rx="2" ${s}/><rect x="${x - 2}" y="${y - 2}" width="4" height="4" fill="${G}"/>`,
    globe: `<circle cx="${x}" cy="${y}" r="6" ${s}/><path d="M${x - 6} ${y}h12M${x} ${y - 6}c-3 3.5-3 8.5 0 12M${x} ${y - 6}c3 3.5 3 8.5 0 12" ${s}/>`,
    dollar: `<path d="M${x - 6} ${y - 1}l6-5 6 5v7h-12z" ${s}/><path d="M${x + 1.6} ${y}h-2.4a1.2 1.2 0 0 0 0 2.4h1.2a1.2 1.2 0 0 1 0 2.4h-2.4" ${s}/>`,
    cal: `<rect x="${x - 6}" y="${y - 5}" width="12" height="11" rx="2" ${s}/><path d="M${x - 6} ${y - 1.5}h12M${x - 3} ${y + 2.5}l2 1.8 3.5-3.5" ${s}/>`,
    bolt: `<path d="M${x + 1} ${y - 7}l-6 8.5h5l-1 6.5 6-8.5h-5z" fill="${G}"/>`,
    head: `<path d="M${x - 6} ${y + 1}v-1.5a6 6 0 0 1 12 0v1.5" ${s}/><rect x="${x - 7}" y="${y + 1}" width="3" height="4" rx="1" fill="${G}"/><rect x="${x + 4}" y="${y + 1}" width="3" height="4" rx="1" fill="${G}"/>`,
    car: `<path d="M${x - 6} ${y + 2}v-2l2-4h8l2 4v2z" ${s}/><circle cx="${x - 3}" cy="${y + 3}" r="1.3" fill="${G}"/><circle cx="${x + 3}" cy="${y + 3}" r="1.3" fill="${G}"/>`,
    cup: `<path d="M${x - 5} ${y - 4}h9v5a4.5 4.5 0 0 1-9 0z" ${s}/><path d="M${x + 4} ${y - 2}h1.5a1.8 1.8 0 0 1 0 3.6H${x + 4}" ${s}/>`,
    film: `<rect x="${x - 6}" y="${y - 5}" width="12" height="10" rx="2" ${s}/><path d="M${x - 1.5} ${y - 2}l4 2-4 2z" fill="${G}"/>`,
    bag: `<path d="M${x - 5} ${y - 3}h10l-1 9h-8z" ${s}/><path d="M${x - 2.5} ${y - 3}a2.5 2.5 0 0 1 5 0" ${s}/>`
  }[kind];
};
const badge = (x, y, txt, fill = '#E8455C') => { const w = txt.length * 3.6 + 7; return `${R(x, y, w, 9, 4.5, fill)}${T(x + w / 2, y + 6.6, 5.4, 600, '#fff', txt, 'middle')}`; };
const telNav = active => {
  const y0 = 333;
  return `${R(6, 322, 168, 30, 0, '#ffffffee')}` + [['Home', 'home'], ['Internet', 'wifi'], ['Chat bot', 'bot'], ['Settings', 'user']].map(([l, k], i) => {
    const x = 28 + i * 41.5, on = i === active, col = on ? G : '#222';
    const ic = {
      home: `<path d="M${x - 6} ${y0 + 1}l6-5.5 6 5.5v6h-12z" fill="${on ? G : 'none'}" stroke="${col}" stroke-width="1.4" stroke-linejoin="round"/>`,
      wifi: `<path d="M${x - 5} ${y0 - 1}a7 7 0 0 1 10 0M${x - 3} ${y0 + 1.5}a4 4 0 0 1 6 0" fill="none" stroke="${col}" stroke-width="1.4" stroke-linecap="round"/>${R(x - 6, y0 + 3.5, 12, 4, 2, col)}`,
      bot: `<path d="M${x - 6} ${y0 - 3}h12a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-7l-3.5 2.5v-2.5h-1.5a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2z" fill="none" stroke="${col}" stroke-width="1.4" stroke-linejoin="round"/><circle cx="${x - 2.5}" cy="${y0 + 1}" r="1.1" fill="${col}"/><circle cx="${x + 2.5}" cy="${y0 + 1}" r="1.1" fill="${col}"/><path d="M${x} ${y0 - 3}v-2.5" stroke="${col}" stroke-width="1.2"/>`,
      user: `<circle cx="${x}" cy="${y0 + 1}" r="6.5" fill="#CBD5CF"/><circle cx="${x}" cy="${y0 - .5}" r="2.4" fill="#fff"/>`
    }[k];
    return `${ic}${T(x, 348, 6.2, on ? 700 : 500, col, l, 'middle')}`;
  }).join('');
};

function telHome() {
  return `
  ${R(14, 34, 92, 20, 10, '#ffffffcc')}<circle cx="25" cy="44" r="6.5" fill="#B9C7BE"/>${T(35, 46.5, 7.5, 700, '#111', '0XX XXX XXX')}
  <circle cx="155" cy="44" r="10" fill="#ffffffcc"/><path d="M151.5 47h7l-1-1.5v-3a2.5 2.5 0 0 0-5 0v3zM154 48.5h2" fill="none" stroke="${G}" stroke-width="1.3" stroke-linecap="round"/>
  ${R(12, 62, 156, 100, 14, '#ffffffee')}
  ${R(20, 71, 9, 9, 2.5, 'none', `stroke="${G}" stroke-width="1.3"`)}${T(24.5, 78, 5.5, 700, G, '$', 'middle')}${T(33, 78.5, 7, 500, '#555', 'Main Balance ›')}
  ${R(116, 68, 46, 16, 8, G)}${T(132, 79, 8, 700, '#fff', '856', 'middle')}<circle cx="153" cy="76" r="5.5" fill="#F7C948"/>${T(153, 78.3, 5.5, 800, '#C98A1B', 'P', 'middle')}
  ${T(20, 106, 21, 700, '#E07A12', '5.80')}${R(68, 93, 24, 13, 6.5, '#E8A33B')}${T(80, 102, 6.8, 700, '#fff', 'USD', 'middle')}
  ${T(20, 120, 6.5, 400, '#777', 'Expires on 28.07.29')}
  <circle cx="142" cy="108" r="15" fill="#E6F4EA"/><path d="M135 110h14v8h-14zM133.5 106h17v4h-17zM142 106v12" fill="#fff" stroke="${G}" stroke-width="1.1" stroke-linejoin="round"/><path d="M142 106c-2-4-6-4-6-1.5s6 1.5 6 1.5c2-4 6-4 6-1.5s-6 1.5-6 1.5" fill="none" stroke="${G}" stroke-width="1.1"/>
  ${R(18, 132, 62, 20, 10, 'url(#tTop)')}${T(52, 145, 7.5, 700, '#fff', 'Top Up', 'middle')}<circle cx="31" cy="142" r="4" fill="#fff" opacity=".9"/>
  <path d="M90 133l9 3v6c0 5-4 8-9 9-5-1-9-4-9-9v-6z" fill="${GD}" stroke="#E7C35A" stroke-width="1.2"/>${T(90, 145, 5.5, 800, '#F2D06B', 'VIP', 'middle')}
  ${R(100, 132, 62, 20, 10, 'url(#tHist)')}${T(134, 145, 7.5, 700, '#fff', 'History', 'middle')}<circle cx="113" cy="142" r="4" fill="none" stroke="#fff" stroke-width="1.2"/>
  ${R(12, 170, 156, 46, 10, 'url(#tPromo)')}
  ${T(19, 185, 6.6, 500, '#123', 'Point discounts on')}${T(19, 194, 6.6, 500, '#123', 'rewards! Limited stock.')}
  ${R(19, 200, 52, 11, 5.5, G)}${T(45, 207.6, 5.6, 700, '#fff', 'Check it now ›', 'middle')}
  ${R(118, 178, 14, 26, 3, '#fff', 'stroke="#cfd8d2"')}${R(134, 186, 22, 18, 4, '#203327')}${R(126, 196, 34, 16, 4, '#2BB34F', 'opacity=".9"')}<circle cx="150" cy="182" r="4" fill="#E8455C" opacity=".85"/>
  ${R(6, 222, 168, 142, 18, '#ffffff')}
  ${R(14, 230, 74, 18, 9, '#fff', 'stroke="#DDE8E0"')}${T(51, 241.8, 6.6, 700, G, 'Mobile Services', 'middle')}
  ${R(92, 230, 74, 18, 9, '#F1F3F2')}${T(129, 241.8, 6.6, 500, '#333', 'Lifestyle', 'middle')}${badge(146, 225, 'New')}
  ${T(16, 264, 8.5, 700, '#111', 'Quick Menu')}${R(134, 256, 32, 13, 6.5, '#EEF1EF')}${R(135.5, 257.5, 15, 10, 5, '#fff')}
  ${R(12, 272, 156, 46, 10, '#F7F9F8')}
  ${[['5G', 'signal'], ['Cyber', 'shield'], ['eSIM', 'chip'], ['Roaming', 'globe']].map(([l, k], i) => `${R(18 + i * 37.5, 278, 31, 24, 7, '#fff')}${telIcon(33.5 + i * 37.5, 290, k)}${T(33.5 + i * 37.5, 312, 5.6, 500, '#222', l, 'middle')}`).join('')}
  ${badge(25, 273, 'Hot')}
  ${telNav(0)}`;
}

function telInternet() {
  return `
  ${T(16, 44, 8.6, 600, '#123', 'Get your router ready')}${T(16, 55, 8.6, 600, '#123', 'to enjoy Home Internet')}
  ${R(16, 62, 70, 15, 7.5, 'url(#tWarm)')}${T(51, 72, 6.2, 700, '#fff', 'Activate router ↗', 'middle')}
  ${R(132, 38, 24, 42, 5, '#fff', 'stroke="#d5dfd8"')}${T(144, 52, 5.5, 800, G, '5G', 'middle')}<circle cx="144" cy="70" r="2" fill="${G}"/>${R(108, 70, 22, 12, 6, '#2BB34F', 'opacity=".35"')}
  ${R(6, 88, 168, 276, 18, '#ffffff')}
  ${R(12, 96, 156, 50, 10, '#F7F9F8')}
  ${[['Top up', 'dollar'], ['Book', 'cal'], ['Coverage', 'bolt'], ['Support', 'head']].map(([l, k], i) => `${R(18 + i * 37.5, 103, 31, 24, 7, '#fff')}${telIcon(33.5 + i * 37.5, 115, k)}${T(33.5 + i * 37.5, 138, 5.6, 500, '#222', l, 'middle')}`).join('')}
  ${badge(26, 98, 'New')}${badge(101, 98, 'Hot')}
  ${R(6, 152, 168, 40, 0, '#E3F4E7')}${T(14, 166, 8.4, 700, '#111', 'Find your ideal')}${T(14, 176, 8.4, 700, '#111', 'Home Internet')}${T(14, 186, 5.6, 400, '#555', 'Plans that fit your lifestyle')}
  ${R(110, 172, 58, 14, 7, 'url(#tWarm)')}${T(139, 181.5, 6, 700, '#fff', 'Explore plans ↗', 'middle')}
  ${R(14, 198, 74, 16, 8, '#fff', 'stroke="#DDE8E0"')}${T(51, 208.8, 6.6, 600, G, 'Wireless', 'middle')}
  ${R(92, 198, 74, 16, 8, '#F1F3F2')}${T(129, 208.8, 6.6, 500, '#555', 'Fiber+', 'middle')}
  ${[['500 GB', '15', 'Chill'], ['1000 GB', '18', 'Pro']].map(([gb, usd, tier], i) => {
    const x = 14 + i * 78;
    return `${R(x, 220, 74, 98, 9, '#fff', `stroke="${i ? '#E3EBE5' : '#C2307A'}" stroke-width="${i ? 1 : 1.2}"`)}
      ${i ? '' : `${R(x + 14, 220, 46, 10, 5, 'url(#tWarm)')}${T(x + 37, 227, 5.4, 700, '#fff', 'Best for you', 'middle')}`}
      ${T(x + 8, 245, 5.4, 700, G, '5G')}${R(x + 44, 238, 24, 10, 3, '#F7E7F1')}${T(x + 56, 245, 5.4, 600, '#C2307A', tier, 'middle')}
      ${T(x + 8, 263, 10, 700, '#111', gb)}${T(x + 8, 274, 5.6, 400, '#333', 'Up to 200 Mbps')}
      ${T(x + 8, 290, 8.5, 700, '#111', usd + ' USD')}${R(x + 46, 283, 22, 10, 3, '#E6F4EA')}${T(x + 57, 290, 5, 600, G, '30 days', 'middle')}
      ${R(x + 8, 298, 58, 13, 6.5, 'url(#tBtn)')}${T(x + 37, 306.6, 6, 700, '#fff', 'Select plan', 'middle')}`;
  }).join('')}
  ${telNav(1)}`;
}

function telProfile() {
  const ic = (x, y, k, col = G) => {
    const st = `fill="none" stroke="${col}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"`;
    return {
      swap: `<circle cx="${x - 1}" cy="${y - 2.5}" r="2.4" ${st}/><path d="M${x - 5} ${y + 4.5}a4 4 0 0 1 7-2.6" ${st}/><path d="M${x + 2} ${y + 2.5}a2.2 2.2 0 1 0 2.2-2.2" ${st}/>`,
      globe: `<circle cx="${x}" cy="${y}" r="5" ${st}/><path d="M${x - 3} ${y - 3.5}c1.5 1 1 3 3 3.2s1.5 2.5.5 4M${x + 4.5} ${y - 1.5}c-1.5 0-2 1.5-1 2.5" ${st}/>`,
      bell: `<path d="M${x - 4} ${y + 2.5}h8l-1.2-1.6v-2.8a2.8 2.8 0 0 0-5.6 0v2.8zM${x - 1} ${y + 4.5}h2" ${st}/>`,
      lock: `<rect x="${x - 4}" y="${y - 1}" width="8" height="6.5" rx="1.5" ${st}/><path d="M${x - 2.4} ${y - 1}v-1.8a2.4 2.4 0 0 1 4.8 0v1.8" ${st}/>`,
      devices: `<rect x="${x - 4.5}" y="${y - 5}" width="6" height="10" rx="1.2" ${st}/><circle cx="${x + 3}" cy="${y + 2}" r="2.4" ${st}/>`,
      card: `<rect x="${x - 5}" y="${y - 3.5}" width="10" height="7" rx="1.5" ${st}/><path d="M${x - 5} ${y - 1}h10M${x - 3} ${y + 1.5}h2.5" ${st}/>`,
      info: `<circle cx="${x}" cy="${y}" r="5" ${st}/><path d="M${x} ${y - .5}v3M${x} ${y - 2.6}v.1" ${st}/>`,
      help: `<circle cx="${x}" cy="${y}" r="5" ${st}/><circle cx="${x}" cy="${y}" r="2.2" ${st}/><path d="M${x - 3.5} ${y - 3.5}l2 2M${x + 3.5} ${y - 3.5}l-2 2M${x - 3.5} ${y + 3.5}l2-2M${x + 3.5} ${y + 3.5}l-2-2" ${st}/>`,
      agent: `<path d="M${x - 4.5} ${y + 1}v-1a4.5 4.5 0 0 1 9 0v1" ${st}/><rect x="${x - 5.5}" y="${y}" width="2.2" height="3.4" rx="1" fill="${col}"/><rect x="${x + 3.3}" y="${y}" width="2.2" height="3.4" rx="1" fill="${col}"/>`,
      out: `<path d="M${x - 1} ${y - 4.5}h-3.5v9h3.5M${x} ${y}h5M${x + 3} ${y - 2}l2 2-2 2" ${st}/>`
    }[k];
  };
  const chev = (y) => `<path d="M158 ${y - 2.5}l2.5 2.5-2.5 2.5" fill="none" stroke="#555" stroke-width="1.1" stroke-linecap="round"/>`;
  const row = (y, k, label, right = chev, last = false) => `${ic(24, y, k)}${T(36, y + 2.5, 7.2, 500, '#111', label)}${right(y)}${last ? '' : `<path d="M36 ${y + 11}h132" stroke="#EDF1EE"/>`}`;
  const group = (y, rows) => `${R(12, y, 156, rows.length * 22 + 2, 9, '#fff')}${rows.map(([k, l, right = chev], i) => row(y + 12 + i * 22, k, l, right, i === rows.length - 1)).join('')}`;
  const toggle = y => `${R(140, y - 5, 22, 11, 5.5, G)}<circle cx="156.5" cy="${y + .5}" r="4" fill="#fff"/>`;
  return `
  <path d="M62 84 C62 52 66 40 92 40 H174 V96 H6 V90 C30 90 62 98 62 84Z" fill="#ffffffaa"/>
  <circle cx="36" cy="62" r="22" fill="#fff"/><circle cx="36" cy="62" r="19.5" fill="#C9D6CD"/>
  <circle cx="36" cy="57" r="6.5" fill="#fff" opacity=".9"/><path d="M24 76a12 9 0 0 1 24 0" fill="#fff" opacity=".9"/>
  <circle cx="52" cy="77" r="7" fill="${G}" stroke="#fff" stroke-width="1.6"/><circle cx="52" cy="75.3" r="1.8" fill="none" stroke="#fff" stroke-width="1"/><path d="M48.8 80a3.2 2.4 0 0 1 6.4 0" fill="none" stroke="#fff" stroke-width="1"/>
  ${T(74, 60, 10.5, 800, '#111', 'Loem Layheng')}${T(74, 75, 7.5, 500, '#666', '0XX XXX XXX')}
  <circle cx="126" cy="72.5" r="3.6" fill="${G}"/><path d="M124.4 72.6l1.1 1.1 2.1-2.2" fill="none" stroke="#fff" stroke-width=".9"/>
  <path d="M162 61l3 3-3 3" fill="none" stroke="#444" stroke-width="1.2" stroke-linecap="round"/>
  ${R(6, 92, 168, 272, 18, '#F3F6F4')}
  ${group(100, [['swap', 'Switch account']])}
  ${group(130, [['globe', 'Language', y => `${T(154, y + 2.5, 6.6, 400, '#777', 'English', 'end')}${chev(y)}`], ['bell', 'Notification', toggle]])}
  ${group(182, [['lock', 'Security PIN'], ['devices', 'Manage devices'], ['card', 'Payment methods']])}
  ${group(256, [['info', 'About'], ['help', 'Help center']])}
  ${R(12, 306, 156, 20, 9, '#fff')}${ic(24, 316, 'out', '#D6456B')}${T(36, 318.5, 7.2, 500, '#D6456B', 'Sign out')}
  ${telNav(3)}`;
}

const mocks = {
  // SmartNas: telco app style (illustrative layout, no real assets)
  smartPhone: () => tel(telHome()),
  smartWeb: () => `<svg viewBox="0 0 480 310" xmlns="http://www.w3.org/2000/svg">
    <svg x="70" y="3" width="148" height="304" viewBox="0 0 180 370">${telInner(telInternet())}</svg>
    <svg x="262" y="3" width="148" height="304" viewBox="0 0 180 370">${telInner(telProfile())}</svg>
  </svg>`,

  ezPhone: c => phone(`
    ${T(20, 52, 8, 500, '#888', 'TABLE 12 · DINE-IN')}${T(20, 70, 16, 700, '#111', 'Menu')}
    ${['All', 'Rice', 'Noodles', 'Drinks'].map((l, i) => `${R(18 + i * 38, 82, 34, 16, 8, i ? '#ECE9E2' : c)}${T(35 + i * 38, 93, 6.8, 600, i ? '#555' : '#fff', l, 'middle')}`).join('')}
    ${[['Bai sach chrouk', '$3.50', '#E8C9A0'], ['Kuy teav', '$3.00', '#F0DCC0'], ['Lok lak', '$4.75', '#D9B48F'], ['Iced coffee', '$1.80', '#C8A27C']].map(([n, p, col], i) => {
      const y = 110 + i * 54;
      return `${R(18, y, 144, 46, 12, '#fff', 'stroke="#ECE9E2"')}<circle cx="41" cy="${y + 23}" r="15" fill="${col}"/>
        ${T(64, y + 19, 8.5, 600, '#111', n)}${T(64, y + 33, 8, 700, c, p)}
        ${R(138, y + 15, 16, 16, 8, i === 1 ? c : '#ECE9E2')}${T(146, y + 26.5, 10, 500, i === 1 ? '#fff' : '#111', i === 1 ? '2' : '+', 'middle')}`;
    }).join('')}
    ${R(18, 328, 144, 26, 13, '#111')}${T(32, 344.5, 8, 600, '#fff', 'View cart · 3 items')}${T(150, 344.5, 8, 700, '#fff', '$9.80', 'end')}
  `),
  ezWeb: c => web('Kitchen board', `
    ${T(456, 56, 8, 500, '#888', 'Live · Branch 1', 'end')}
    ${['New', 'Cooking', 'Ready'].map((h, k) => {
      const x = 24 + k * 148;
      return `${R(x, 72, 140, 222, 10, '#F3F1EB')}${T(x + 12, 92, 8.5, 700, '#111', h)}${R(x + 112, 83, 18, 13, 6.5, k === 0 ? c : '#E2DED5')}${T(x + 121, 92.5, 7, 700, k === 0 ? '#fff' : '#555', [3, 2, 1][k], 'middle')}
        ${Array.from({ length: [3, 2, 1][k] }, (_, j) => {
          const y = 104 + j * 62;
          return `${R(x + 8, y, 124, 54, 8, '#fff', 'stroke="#E2DED5"')}${T(x + 18, y + 16, 8, 700, '#111', '#A' + (12 + j + k * 3))}${T(x + 122, y + 16, 7, 500, k === 2 ? '#2E8B57' : '#999', ['2 min', '6 min', 'Done'][k], 'end')}${bar(x + 18, y + 26, 80)}${bar(x + 18, y + 36, 56, '#E2DED5')}${R(x + 8, y, 3, 54, 1.5, k === 0 ? c : k === 1 ? '#C98A1B' : '#2E8B57')}`;
        }).join('')}`;
    }).join('')}
  `, 'kitchen · ezorder'),

  botPhone: c => phone(`
    <circle cx="30" cy="54" r="11" fill="${c}"/>${T(30, 57.5, 9, 700, '#fff', '✦', 'middle')}
    ${T(48, 52, 9, 700, '#111', 'POS Assistant')}${T(48, 63, 6.8, 500, '#2E8B57', '● Online')}
    ${R(18, 82, 112, 30, 10, '#fff', 'stroke="#E2DED5"')}${T(28, 95, 7.5, 400, '#333', 'Hi! What can I help')}${T(28, 105, 7.5, 400, '#333', 'you with today?')}
    ${R(76, 120, 86, 22, 10, c)}${T(84, 134, 7.5, 500, '#fff', 'Printer not printing')}
    ${R(18, 150, 128, 64, 10, '#fff', 'stroke="#E2DED5"')}
    ${T(28, 164, 7.5, 600, '#111', 'Let’s check 3 things:')}${T(28, 178, 7.2, 400, '#444', '1. Power and USB cable')}${T(28, 190, 7.2, 400, '#444', '2. Paper roll direction')}${T(28, 202, 7.2, 400, '#444', '3. Printer set as default')}
    ${R(18, 222, 62, 20, 10, 'none', `stroke="${c}"`)}${T(49, 235, 7, 600, c, 'It works now', 'middle')}
    ${R(86, 222, 60, 20, 10, 'none', `stroke="${c}"`)}${T(116, 235, 7, 600, c, 'Talk to CS', 'middle')}
    ${R(96, 252, 66, 22, 10, c)}${T(104, 266, 7.5, 500, '#fff', 'It works now')}
    ${R(18, 282, 100, 22, 10, '#fff', 'stroke="#E2DED5"')}${T(28, 296, 7.5, 400, '#333', 'Great, glad it’s fixed!')}
    ${R(18, 322, 144, 24, 12, '#fff', 'stroke="#E2DED5"')}${T(30, 337, 7.5, 400, '#aaa', 'Type a message…')}<circle cx="150" cy="334" r="8" fill="${c}"/>
  `),
  botWeb: c => {
    const node = (x, y, w, label, fill = '#fff', ink = '#111') => `${R(x, y, w, 26, 8, fill, fill === '#fff' ? 'stroke="#D9D5CC"' : '')}${T(x + w / 2, y + 16.5, 8, 600, ink, label, 'middle')}`;
    const line = (x1, y1, x2, y2) => `<path d="M${x1} ${y1} C${x1} ${(y1 + y2) / 2} ${x2} ${(y1 + y2) / 2} ${x2} ${y2}" fill="none" stroke="#C9C4BA" stroke-width="1.4"/>`;
    return web('Conversation flow', `
      ${line(240, 98, 240, 120)}${line(240, 146, 110, 172)}${line(240, 146, 240, 172)}${line(240, 146, 370, 172)}
      ${line(110, 198, 240, 232)}${line(240, 198, 240, 232)}${line(370, 198, 240, 232)}${line(240, 258, 160, 272)}${line(240, 258, 320, 272)}
      ${node(190, 72, 100, 'Greeting', c, '#fff')}${node(180, 120, 120, 'Identify issue')}
      ${node(60, 172, 100, 'Printer')}${node(190, 172, 100, 'Payment')}${node(320, 172, 100, 'Menu sync')}
      ${node(180, 232, 120, 'Resolved?')}${node(100, 272, 120, 'Close + rate', '#E7F2EA', '#2E8B57')}${node(260, 272, 120, 'Escalate to CS', '#111', '#fff')}
    `, 'flows · builder');
  },

  // Dropship Store: sample Shopify-style store (illustrative, no real shop or logo)
  shopPhone: c => phone(`
    ${T(20, 52, 12, 800, '#111', 'LUMA')}${T(62, 52, 6.5, 500, '#999', 'home goods')}
    <path d="M146 44h12l-1.5 9h-9z" fill="none" stroke="#111" stroke-width="1.3" stroke-linejoin="round"/><path d="M149 44a3 3 0 0 1 6 0" fill="none" stroke="#111" stroke-width="1.3"/>
    <circle cx="159" cy="42" r="5" fill="${c}"/>${T(159, 44.3, 6, 700, '#fff', '1', 'middle')}
    ${R(14, 62, 152, 128, 14, '#F4EEE4')}
    <ellipse cx="90" cy="172" rx="34" ry="5" fill="#000" opacity=".08"/>
    <circle cx="90" cy="138" r="18" fill="#FFE7A8" opacity=".7"/>
    <path d="M90 104l-20 26h40z" fill="${c}"/><rect x="88" y="130" width="4" height="34" fill="#3b3b3b"/><rect x="74" y="162" width="32" height="6" rx="3" fill="#3b3b3b"/>
    ${[0, 1, 2].map(i => `<circle cx="${82 + i * 8}" cy="182" r="2.2" fill="${i ? '#d6cfc3' : '#111'}"/>`).join('')}
    ${T(16, 210, 10, 700, '#111', 'Mini Desk Lamp')}
    ${[0, 1, 2, 3, 4].map(i => `<path d="M${19 + i * 9} 216.5l1.3 2.6 2.9.4-2.1 2 .5 2.9-2.6-1.4-2.6 1.4.5-2.9-2.1-2 2.9-.4z" fill="${i < 4 ? '#F2B53A' : '#E2DED5'}"/>`).join('')}
    ${T(66, 223.5, 6.5, 500, '#888', '128 reviews')}
    ${T(16, 246, 14, 800, '#111', '$24.90')}${T(78, 246, 8, 500, '#aaa', '$39.00')}<path d="M78 243.5h24" stroke="#aaa" stroke-width=".9"/>
    ${R(110, 236, 34, 13, 6.5, c, 'opacity=".14"')}${T(127, 245, 6.5, 700, c, '-36%', 'middle')}
    ${T(16, 266, 6.8, 600, '#888', 'COLOUR')}
    ${['#111', c, '#E9E3D7'].map((col, i) => `<circle cx="${24 + i * 20}" cy="280" r="7" fill="${col}" stroke="${i ? '#d6cfc3' : c}" stroke-width="${i ? 1 : 2}"/>`).join('')}
    ${R(16, 298, 148, 26, 13, '#111')}${T(90, 314.5, 8.5, 700, '#fff', 'Add to cart', 'middle')}
    ${T(90, 337, 6.2, 500, '#888', 'Free shipping · arrives in 7 to 12 days', 'middle')}
  `),
  shopWeb: c => web('Store overview', `
    ${R(352, 42, 104, 22, 11, c)}${T(404, 56, 8, 600, '#fff', '+ New campaign', 'middle')}
    ${R(24, 74, 214, 220, 10, '#fff', 'stroke="#E2DED5"')}${T(36, 94, 9, 700, '#111', 'Recent orders')}
    ${[['#1042', 'Paid', '#2E8B57'], ['#1041', 'Fulfilling', '#C98A1B'], ['#1040', 'Shipped', '#3B6FD8'], ['#1039', 'Shipped', '#3B6FD8'], ['#1038', 'Delivered', '#2E8B57']].map(([n, s, col], i) => {
      const y = 106 + i * 36;
      return `${R(34, y, 194, 30, 7, i % 2 ? '#fff' : '#F7F5F0')}${R(40, y + 6, 18, 18, 5, ['#F4EEE4', '#E9E3D7', '#F0D9D2', '#DCE4EE', '#E6F4EA'][i])}
        ${T(64, y + 13, 7.2, 700, '#111', n)}${bar(64, y + 18, 50, '#E2DED5', 4)}
        ${R(162, y + 8, 58, 14, 7, col, 'opacity=".14"')}${T(191, y + 18, 6.6, 600, col, s, 'middle')}`;
    }).join('')}
    ${R(248, 74, 208, 220, 10, '#fff', 'stroke="#E2DED5"')}${T(260, 94, 9, 700, '#111', 'Ad campaigns')}
    ${[['Facebook', '#1877F2', 'Active', .78], ['Instagram', '#D6457B', 'Active', .62], ['TikTok', '#111', 'Testing', .35]].map(([ch, col, st, p], i) => {
      const y = 108 + i * 58;
      return `${R(258, y, 188, 50, 8, '#F7F5F0')}<circle cx="273" cy="${y + 16}" r="7" fill="${col}"/>
        ${T(286, y + 19, 7.6, 700, '#111', ch)}${R(392, y + 9, 46, 14, 7, st === 'Active' ? '#2E8B57' : '#C98A1B', 'opacity=".15"')}${T(415, y + 19, 6.4, 600, st === 'Active' ? '#2E8B57' : '#C98A1B', st, 'middle')}
        ${T(266, y + 38, 6.2, 500, '#888', 'Spend')}${R(292, y + 34, 146, 5, 2.5, '#E2DED5')}${R(292, y + 34, 146 * p, 5, 2.5, c)}`;
    }).join('')}
  `, 'admin · sample store'),

  posterPhone: c => phone(`
    ${T(20, 54, 15, 700, '#111', 'New brief')}${T(20, 68, 7.5, 400, '#888', 'Fill in once, get every size')}
    ${[['Brand', 'Kafe Lumo'], ['Offer', '20% off all drinks']].map(([l, v], i) => `${T(20, 92 + i * 46, 7, 600, '#888', l.toUpperCase())}${R(18, 98 + i * 46, 144, 26, 8, '#fff', 'stroke="#E2DED5"')}${T(28, 114 + i * 46, 8.5, 500, '#111', v)}`).join('')}
    ${T(20, 184, 7, 600, '#888', 'COLOURS')}
    ${[c, '#111', '#F2C14E', '#FBFAF7'].map((col, i) => `<circle cx="${32 + i * 26}" cy="202" r="10" fill="${col}" stroke="#D9D5CC"/>`).join('')}
    ${T(20, 232, 7, 600, '#888', 'SIZES')}
    ${['1:1', '4:5', '9:16', 'A4'].map((l, i) => `${R(18 + i * 36, 238, 32, 18, 9, i < 3 ? '#111' : '#ECE9E2')}${T(34 + i * 36, 250, 7, 600, i < 3 ? '#fff' : '#555', l, 'middle')}`).join('')}
    ${R(18, 314, 144, 28, 14, c)}${T(90, 331.5, 8.5, 700, '#fff', 'Generate 12 posters', 'middle')}
  `),
  posterWeb: c => web('Results · Kafe Lumo', `
    ${T(456, 56, 8, 500, '#888', '12 variants', 'end')}
    ${Array.from({ length: 6 }, (_, i) => {
      const x = 24 + i * 73, h = [96, 120, 150, 96, 120, 150][i], y = 230 - h;
      const bg = [c, '#111', '#F2C14E', '#111', c, '#F2C14E'][i], ink = bg === '#F2C14E' ? '#111' : '#fff';
      return `${R(x, y, 66, h, 6, bg)}<circle cx="${x + 46}" cy="${y + 22}" r="13" fill="${ink}" opacity=".18"/>
        ${T(x + 8, y + h - 30, 13, 800, ink, '20%')}${T(x + 8, y + h - 18, 7, 500, ink, 'OFF DRINKS')}${T(x + 8, y + h - 8, 5.5, 400, ink, 'Kafe Lumo')}
        ${T(x + 33, 246, 7, 500, '#888', ['1:1', '4:5', '9:16', '1:1', '4:5', '9:16'][i], 'middle')}`;
    }).join('')}
    ${R(24, 266, 432, 26, 8, '#F3F1EB')}${T(36, 282, 8, 500, '#555', 'All sizes exported · brand colours checked')}${T(444, 282, 8, 700, c, 'Download all', 'end')}
  `, 'poster-ai · results')
};
