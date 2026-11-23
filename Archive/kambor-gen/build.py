#!/usr/bin/env python3
"""Builds the static pages of the Atelier Kambor concept site (fictional studio)."""
import json, os, sys

ROOT = "/home/user/layhengportflio/Portfolio 2026/samples/interior/"
SIZES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sizes.json")))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Hanken+Grotesk:wght@400;500&display=swap" rel="stylesheet">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Khmer:wght@300&display=swap&text=%E1%9E%80%E1%9F%86%E1%9E%94%E1%9F%84%E1%9E%9A" rel="stylesheet">')

def img(P, name, alt, sizes="100vw", lazy=True, cls="", extra=""):
    w, h = SIZES[name]
    sw = 800; sh = round(h * 800 / w)
    return (f'<img{" class=%s" % chr(34)+cls+chr(34) if cls else ""} src="{P}img/{name}-s.webp" '
            f'srcset="{P}img/{name}-s.webp 800w, {P}img/{name}-l.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}"{" loading=%slazy%s" % (chr(34),chr(34)) if lazy else ""} decoding="async"{extra}>')

def ln(text, i=0):
    return f'<span class="ln" style="--i:{i}"><span>{text}</span></span>'

NAV = [("projects/", "Projects", "projects"), ("studio.html", "Studio", "studio"), ("services.html", "Services", "services"),
       ("journal.html", "Journal", "journal"), ("contact.html", "Contact", "contact")]

def head(P, title, desc, extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#EDE7DC">
<script>(function(h){{h.classList.add('js');try{{if(sessionStorage.getItem('kb-go')){{sessionStorage.removeItem('kb-go');if(!matchMedia('(prefers-reduced-motion: reduce)').matches)h.classList.add('arrive')}}}}catch(e){{}}}})(document.documentElement)</script>
{FONTS}
<link rel="stylesheet" href="{P}assets/kambor.css">
{extra}</head>
'''

def top(P, cur, home=False):
    home_href = P or "./"
    links = "".join(f'<li><a href="{P}{h}"{" aria-current=%spage%s" % (chr(34),chr(34)) if k==cur else ""}>{t}</a></li>' for h,t,k in NAV)
    plinks = "".join(f'<li><a href="{P}{h}"{" aria-current=%spage%s" % (chr(34),chr(34)) if k==cur else ""}>{t}<small>0{i+1}</small></a></li>' for i,(h,t,k) in enumerate(NAV))
    return f'''<body class="{"home" if home else "page-"+cur}">
<a class="skip" href="#main">Skip to content</a>
<div class="ribbon" role="note"><i aria-hidden="true"></i><span>Fictional studio<span class="dot"> · </span><span class="long">concept site </span>by Loem Layheng</span><span class="dot">·</span><a href="{P}../../#p/kambor" data-back>Back to portfolio</a></div>
<div class="curtain" aria-hidden="true"></div>
<header class="nav" id="nav">
  <a class="mark" href="{home_href}" aria-label="Atelier Kambor, home">Atelier <em>Kambor</em></a>
  <nav aria-label="Main"><ul>{links}</ul></nav>
  <a class="enq" href="{P}contact.html#enquiry">Start a project</a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="panel"><span class="t">Menu</span><i aria-hidden="true"></i></button>
</header>
<div class="panel" id="panel">
  <nav aria-label="Main, small screens"><ul><li><a href="{home_href}"{' aria-current="page"' if cur=="home" else ""}>Home<small>00</small></a></li>{plinks}</ul></nav>
  <div><a class="btn fill" href="{P}contact.html#enquiry">Start a project <span class="arr" aria-hidden="true">→</span></a><p>Fictional studio. A concept site by Loem Layheng.</p></div>
</div>
'''

PLANE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 11.5 21 4l-3.2 16-6.1-4.6-3 3.1.4-4.6L17 7.6 7.2 13.4z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'

def tg(nid, label="Message us on Telegram", cls="btn fill"):
    return (f'<span class="tg-wrap"><button class="{cls}" type="button" data-note="{nid}" aria-expanded="false" aria-controls="{nid}">{label} <span class="arr" aria-hidden="true">→</span></button>'
            f'<span class="tg-note" id="{nid}" hidden>Atelier Kambor is invented, so there is no Telegram account behind this button. On a real studio site it would open a chat.</span></span>')

def cta(P, h1="Start with", h2="one room."):
    return f'''<section class="cta on-dark" aria-labelledby="cta-h">
  <p class="eyebrow">Enquiries</p>
  <h2 id="cta-h" class="rv">{ln(h1)}{ln("<em>"+h2+"</em>",1)}</h2>
  <div class="cta-row">
    <p>Tell us about the space, who lives or works there and roughly when you want to start. We usually reply the same day, in Khmer or English.</p>
    <div class="acts">{tg("tg-cta")}<a class="btn" href="{P}contact.html#enquiry">Send an enquiry <span class="arr" aria-hidden="true">→</span></a></div>
  </div>
</section>
'''

def footer(P):
    home_href = P or "./"
    return f'''<footer class="foot on-dark">
  <p class="fmark" aria-label="Atelier Kambor">Atelier <em>Kambor</em> <span class="km" lang="km" aria-hidden="true">កំបោរ</span></p>
  <div class="fgrid">
    <div><small>Studio</small><p>Street 2XX, Boeung Keng Kang 1<br>Phnom Penh, Cambodia</p><p style="margin-top:10px">Monday to Friday, 8:00 to 17:00<br>Saturday mornings by appointment</p></div>
    <div><small>Talk to us</small><ul><li><a href="{P}contact.html">Telegram, first choice</a></li><li><a href="mailto:studio@kambor.example">studio@kambor.example</a></li><li>+855 XX XXX XXX</li><li>Khmer and English</li></ul></div>
    <div><small>Pages</small><ul><li><a href="{home_href}">Home</a></li><li><a href="{P}projects/">Projects</a></li><li><a href="{P}studio.html">Studio</a></li><li><a href="{P}services.html">Services</a></li><li><a href="{P}journal.html">Journal</a></li><li><a href="{P}contact.html">Contact</a></li></ul></div>
    <div><small>Elsewhere</small><ul><li class="ph-link">Instagram</li><li class="ph-link">Facebook</li><li class="ph-link">WhatsApp</li></ul><p style="margin-top:10px;font-size:13px;color:#A89A88">Placeholders: the studio has no accounts.</p></div>
  </div>
  <div class="fict">
    <p><strong>This studio does not exist.</strong> Names, people, projects and the address are invented. Photos: Unsplash.</p>
    <p>Concept site designed and built by Loem Layheng<span class="sep"> · </span><a href="{P}../../#p/kambor" data-back>Back to portfolio</a></p>
  </div>
</footer>
'''

def scripts(P, extra=""):
    return f'''<script src="{P}../../vendor/lenis.min.js"></script>
<script src="{P}assets/kambor.js"></script>
{extra}</body>
</html>
'''

# ---------------------------------------------------------------- content
TYPES = [("homes", "Homes"), ("shophouses", "Shophouses"), ("hospitality", "Hospitality"), ("renovations", "Renovations"), ("furniture", "Furniture")]
TNAME = dict(TYPES)

MATS = {  # name, texture class, note
    "lime": ("Lime plaster", "t-lime", "It breathes, so walls dry out after the rains instead of blistering. Kambor is the Khmer word for lime."),
    "terrazzo": ("Terrazzo, poured on site", "t-terrazzo", "Stone chips set in cement, ground and polished in place. Cool underfoot, and it can be polished again in twenty years."),
    "hardwood": ("Reclaimed hardwood", "t-teak", "Old beams and boards, re-sawn and oiled, never lacquered. Already dry, so it does not twist in the rains."),
    "rattan": ("Rattan and woven palm", "t-rattan", "For screens, seat backs and lamps. Light to move, and air passes straight through it."),
    "stone": ("Kampot stone", "t-stone", "A grey stone from the south, for steps, sills and wet floors. It does not get slippery when it rains."),
    "tile": ("Khmer handmade tiles", "t-tile", "Patterned cement tiles, pressed by hand, the kind laid in old shophouse halls. Broken ones can be matched."),
    "cloth": ("Local cotton and silk", "t-cloth", "Woven in the provinces. Cotton for covers that wash and dry fast in the wet season, silk for one cushion or a curtain."),
}

PROJECTS = [
  dict(slug="house-in-toul-kork", t="House in <em>Toul Kork</em>", plain="House in Toul Kork", types=["homes"], place="Toul Kork, Phnom Penh",
       cover="p-toulkork", cover_alt="A tall room of board-marked concrete and dark timber with a low sofa and rust cushions",
       size="New house on two floors, about 240 m²", scope="Full interior, built-in joinery, lighting, planting of the court",
       team="Founder and lead designer, project architect, site coordinator",
       short="A new concrete house for three generations, planned around a planted court.",
       brief="Three generations moving from a flat into a new concrete house on a narrow plot. They wanted it to stay cool without the air conditioning on all day, and the grandmother wanted to see the garden from her chair.",
       changes=["Moved the stair so the front door opens onto light, not a corridor.",
                "Cut a court into the middle of the plan. Every main room now has a window onto it.",
                "Took the roof past the living-room glass, so no direct sun reaches the sofa.",
                "Pale floors that carry daylight deep inside. The lamps stay off until dusk.",
                "A shoe bench and a tiled wash spot at the door, where the family actually comes in."],
       mats=["lime", "hardwood", "terrazzo", "rattan", "stone"], gallery=[]),
  dict(slug="shophouse-in-daun-penh", t="Shophouse in <em>Daun Penh</em>", plain="Shophouse in Daun Penh", types=["shophouses", "renovations"], place="Daun Penh, Phnom Penh",
       cover="shophouse-2", cover_alt="A living room under a dark timber ceiling, with a woven pendant, a round mirror, a low cabinet and a herringbone floor",
       size="1960s shophouse, four floors on a narrow front", scope="Renovation of the whole house, light well, new stair, joinery",
       team="Founder and lead designer, project architect, site coordinator",
       short="A print shop below and a family above, opened up with a light well.",
       brief="A 1960s shophouse with a print shop on the ground floor and the owner's family above. Dark in the middle, hot under the roof, one steep stair, and the family had to walk through the shop to get home.",
       changes=["Opened a light well from the roof down to the living room.",
                "A new timber stair beside the light well, gentler than the old one.",
                "Kept the old cement tiles in the shop. Lifted, cleaned and relaid the broken ones.",
                "Separate doors for the shop and the home, so the family can come in after closing.",
                "A ventilated roof over the top floor, so the bedrooms cool down at night."],
       mats=["tile", "hardwood", "lime", "terrazzo"],
       gallery=[("shophouse-3", "A dining table beside a concrete stair with a timber screen and tall glass doors", "The new stair, with a timber screen in place of a wall.")],
       ba=True),
  dict(slug="flat-by-the-river", t="Flat by the <em>river</em>", plain="Flat by the river", types=["homes", "renovations"], place="Chroy Changvar, Phnom Penh",
       cover="p-river", cover_alt="A pale kitchen with a long window onto palms and garden trees",
       size="Two-bedroom flat, about 110 m²", scope="Kitchen and living room, built-in storage, balcony, lighting",
       team="Founder and lead designer, furniture and sourcing lead",
       short="A tired rented flat, opened up to the river light.",
       brief="A flat the owners had rented out for years and took back to live in. Small rooms, a closed kitchen, and a balcony used for storage. The budget was for one floor, not a rebuild.",
       changes=["Took down the kitchen wall, so the window lights the whole living space.",
                "Built-in storage along one wall, which freed the balcony to become a room again.",
                "Ceiling fans in every room. The air conditioning now runs only at night.",
                "Kept the existing floor and laid rugs instead of replacing it, which kept the budget for joinery."],
       mats=["hardwood", "rattan", "cloth"],
       gallery=[("river-3", "A long living room with a clerestory window, a grey sofa, leather stools and plants by tall glass", "The living room once the kitchen wall came down."),
                ("river-2", "A small balcony with two timber armchairs, cushions, a pouf and hanging plants", "The balcony, cleared and furnished as a room.")]),
  dict(slug="guest-rooms-in-kampot", t="Guest rooms in <em>Kampot</em>", plain="Guest rooms in Kampot", types=["hospitality"], place="Kampot",
       cover="p-kampot", cover_alt="A calm bedroom with a pale pink arch painted behind the bed and a woven pendant",
       size="Eight rooms in a family guesthouse", scope="Colour, furniture, linen and lighting, room by room",
       team="Founder and lead designer, furniture and sourcing lead, site coordinator",
       short="Eight rooms in soft lime colours, refitted between two rainy seasons.",
       brief="A family guesthouse near the river wanted to refit its rooms between two rainy seasons without closing for long. New paint, new beds and linen, and lamps people can read by.",
       changes=["Each room in its own soft lime colour, mixed on site with the painters.",
                "Beds, side tables and luggage benches made by a workshop in town.",
                "Covers and curtains in local cotton, easy to wash and quick to dry.",
                "Worked floor by floor, so half the rooms stayed open the whole time."],
       mats=["lime", "cloth", "hardwood", "rattan"],
       gallery=[("kampot-3", "A bed with rust linen and striped cushions against a grey plaster wall, with a small side table", "A room in a warmer colour, with local cotton on the bed.")]),
  dict(slug="coffee-room-in-bkk1", t="Coffee room in <em>BKK1</em>", plain="Coffee room in BKK1", types=["hospitality", "shophouses"], place="Boeung Keng Kang 1, Phnom Penh",
       cover="coffee-2", cover_alt="A dark timber bar with a stone counter, a glass cabinet and a teal stool",
       size="Ground floor of a shophouse, about 90 m²", scope="Layout, bar, built-in seating, shading, lighting",
       team="Founder and lead designer, project architect, furniture and sourcing lead",
       short="A small roaster's room where people stay for an hour, not ten minutes.",
       brief="A small roaster wanted a room on a busy street where people stay for an hour, not ten minutes. The front faced the afternoon sun and the bar blocked the window.",
       changes=["Moved the bar to the back, so the front is all seats and shade.",
                "A deep awning and a timber screen to keep the afternoon sun off the glass.",
                "One long bench along the side wall, built in, with storage under the seat.",
                "Woven pendants hung low over the tables, so the room feels smaller and calmer at night."],
       mats=["hardwood", "rattan", "terrazzo", "stone"],
       gallery=[("coffee-4", "A long timber table with white chairs under a beam of hanging bulbs", "The long table, under one beam of lamps."),
                ("coffee-3", "A sitting area with two woven pendants, a grey sofa, a round table and plants", "The quiet corner by the side wall.")]),
  dict(slug="joinery-in-tonle-bassac", t="Joinery in <em>Tonle Bassac</em>", plain="Joinery in Tonle Bassac", types=["furniture"], place="Tonle Bassac, Phnom Penh",
       cover="library-1", cover_alt="A floor-to-ceiling plywood bookcase full of books beside a tall window",
       size="Built-in pieces for a three-bedroom flat", scope="Furniture made to order with a local workshop",
       team="Furniture and sourcing lead, founder and lead designer",
       short="A library wall, a vanity and a cabinet, made to measure in town.",
       brief="A couple with a lot of books and very little storage. They wanted furniture made to measure by people who would come back to fix it, and nothing that would swell in the wet season.",
       changes=["A floor-to-ceiling library wall in plywood with a hardwood edge.",
                "A floating vanity in the bathroom, lifted off the floor so it stays dry.",
                "A narrow wall cabinet for towels, open at the front so air moves through.",
                "Made with a workshop on the edge of the city, from drawings in Khmer and English."],
       mats=["hardwood", "rattan", "stone"],
       gallery=[("library-2", "A floating timber vanity with a dark basin and an open shelf of towels against a green wall", "The vanity, hung on the wall to keep it out of the wet."),
                ("library-3", "A tall timber wall cabinet with open cubbies on a pale pink wall", "The towel cabinet, open at the front.")]),
]

STAGES = [
  ("First talk and site visit", "Free, about an hour", "We listen, measure and take photos. You tell us how you live, what must stay and what the budget is.", "Notes from the visit and a fixed design fee in writing."),
  ("Concept", "Usually two to three weeks", "A first idea of the rooms: how they connect, where the light and air come from, and what it might cost.", "Mood boards, a layout plan and a first idea of cost."),
  ("Design development", "Usually three to six weeks", "The idea becomes drawings. We choose materials with you, with samples in your hand, not on a screen.", "Drawings, 3D views and a materials board."),
  ("Build drawings and quotes", "One to three weeks", "A drawing set any builder can price, in Khmer or English. We help you compare the quotes.", "A full drawing set and itemised contractor quotes."),
  ("Site and build", "A few weeks for a room, a few months for a house", "We visit site every week and send photo updates on Telegram, so you do not have to stand in the dust.", "Weekly site visits and photo updates."),
  ("Handover and styling", "The last week", "We walk through every room with you, fix the snag list, place the furniture and hang the lamps.", "A snag list, a final walk-through and a care guide."),
]

JOURNAL = [
  dict(id="cool-house", t="Keeping a house cool without more air-con", kind="Climate", season="Hot season note", read="Four minute read",
       teaser="Shade, moving air and walls that breathe do most of the work. The air conditioner is the last tool, not the first.",
       img=("shade", "A living room with a deep roof overhang, a timber wall and tall glass doors open to a shaded terrace")),
  dict(id="terrazzo", t="How terrazzo is poured on site", kind="Materials", season="Dry season note", read="Three minute read",
       teaser="Chips of stone, grey or white cement, water and patience. Why we pour it in the dry months, and why it lasts.",
       tex="t-terrazzo"),
  dict(id="workshop", t="A morning at the joinery workshop", kind="Workshop", season="Rainy season note", read="Three minute read",
       teaser="Where our furniture is made, what dry wood means in a wet country, and why we oil and never lacquer.",
       img=("chair", "A dining chair with solid timber legs and a grey upholstered seat on a plain background")),
]

# ---------------------------------------------------------------- pages
def write(rel, s):
    assert "—" not in s, rel + " contains an em dash"
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(s); print("wrote", rel, len(s))

def swatch_list():
    out = []
    for i, k in enumerate(MATS):
        n, c, note = MATS[k]
        out.append(f'<li class="{"on" if i==0 else ""}"><button type="button" class="sw" aria-expanded="{"true" if i==0 else "false"}"><span class="tex {c}"></span>'
                   f'<span class="no" aria-hidden="true">0{i+1}</span><span class="vl" aria-hidden="true">{n}</span><span class="lbl"><b>{n}</b><span>{note}</span></span></button></li>')
    return "\n    ".join(out)

def chips(keys):
    return "".join(f'<li><span class="tex {MATS[k][1]}" aria-hidden="true"></span>{MATS[k][0]}</li>' for k in keys)

# ---------- home
def home():
    P = ""
    feats = PROJECTS[:4]
    rows = "\n    ".join(
        f'<li><a class="prow" href="projects/{p["slug"]}/"><figure class="inline">{img(P,p["cover"],"",sizes="100vw")}</figure>'
        f'<span class="n">0{i+1}</span><h3>{p["t"]}</h3><span class="meta"><b>{" · ".join(TNAME[t] for t in p["types"])}</b>{p["place"]}</span></a></li>'
        for i, p in enumerate(feats))
    strip = "".join(f'<img src="img/{p["cover"]}-s.webp" alt="" loading="lazy" decoding="async">' for p in feats)
    doors = [("homes", "Homes", "Villas, flats and borey houses."), ("shophouses", "Shophouses", "Shop below, family above."),
             ("hospitality", "Hospitality", "Cafés, small hotels and guesthouses."), ("renovations", "Renovations", "Old Khmer and colonial buildings, tired flats."),
             ("furniture", "Furniture", "Made to order with local workshops.")]
    drows = "\n    ".join(f'<li><a class="door-row" href="services.html#{k}"><span class="n">0{i+1}</span><b>{t}</b><span class="d">{d}</span><span class="a" aria-hidden="true">→</span></a></li>' for i,(k,t,d) in enumerate(doors))
    stages = "\n    ".join(f'<li class="rise" style="--i:{i}"><small>0{i+1}</small><b>{s[0]}</b><p>{s[3]}</p><span class="dur">{s[1]}</span></li>' for i, s in enumerate(STAGES))
    jl = journal_list(P)
    s = head(P, "Atelier Kambor · Interior studio in Phnom Penh (fictional)",
             "Concept site for an invented interior design studio in Phnom Penh, designed and built by Loem Layheng. The studio, its people and its projects do not exist. Photos from Unsplash.",
             '<link rel="preload" as="image" href="img/hero-l.webp" imagesrcset="img/hero-s.webp 800w, img/hero-l.webp 1560w" imagesizes="100vw">\n')
    s += top(P, "home", home=True)
    s += f'''<main id="main">
<section class="hero" aria-label="Introduction">
  <div class="door">{img(P,"hero","A bedroom in dark teak at dusk: a low bed, warm lamps and a doorway onto a small planted court",lazy=False,extra=' fetchpriority="high"')}</div>
  <div class="hero-type">
    <h1 aria-label="Atelier Kambor">{ln("Atelier")}{ln("<em>Kambor</em>",1)}</h1>
    <div class="hero-side">
      <p class="eyebrow reveal">Interior studio · Phnom Penh</p>
      <p class="reveal">Homes, shophouses, cafés and small hotels, designed for heat, rain and family life.</p>
    </div>
  </div>
</section>

<section class="statement-sec grid12" aria-labelledby="st-h">
  <p class="eyebrow" id="st-h">The studio</p>
  <p class="statement">We are a small studio in Boeung Keng Kang, started by a Khmer designer who trained abroad and came home. We design rooms for the way people here <em>actually live</em>: heat, rain, family, shoes at the door.</p>
  <ul class="facts">
    <li><b>Five kinds of project</b><p>Homes, shophouses, hospitality, renovations and furniture.</p></li>
    <li><b>Khmer and English</b><p>In meetings, on site, and on every drawing and quote.</p></li>
    <li><b>Phnom Penh first</b><p>Siem Reap and Kampot regularly. Further away, ask us.</p></li>
    <li><b>Itemised quotes</b><p>No hidden commissions from suppliers, ever.</p></li>
  </ul>
</section>

<a class="feature" href="projects/house-in-toul-kork/">
  <span class="fimg">{img(P,"living","A living room under a timber ceiling, with a leather sofa, a rattan chair and a woven pendant, glazed on two sides onto trees",sizes="100vw")}</span>
  <span class="fcap"><span class="eyebrow">Featured project · Homes · Toul Kork</span><b>House in <em>Toul Kork</em></b><span class="fd">Three generations, one planted court, five rooms that stay cool without the air-con on all day.</span><span class="more">Walk through the house <span aria-hidden="true">→</span></span></span>
</a>

<section class="sec paper" aria-labelledby="proj-h">
  <div class="sec-head">
    <p class="eyebrow">Selected projects</p>
    <h2 id="proj-h" class="rv">{ln("Recent")}{ln("<em>work</em>",1)}</h2>
    <p>Houses, a shophouse, guest rooms and a coffee room. Every project on this site is invented.</p>
  </div>
  <ol class="plist" id="plist">
    {rows}
  </ol>
  <div class="preview" aria-hidden="true"><div class="strip" id="strip">{strip}</div></div>
  <div class="list-foot"><span>Four of six projects</span><a class="more" href="projects/">All projects <span aria-hidden="true">→</span></a></div>
</section>

<section class="sec" aria-labelledby="svc-h">
  <div class="sec-head">
    <p class="eyebrow">What we design</p>
    <h2 id="svc-h" class="rv">{ln("Five")}{ln("<em>kinds of room</em>",1)}</h2>
    <p>One room or a whole building. If you only need furniture, or one consultation at home, that is fine too.</p>
  </div>
  <ul class="doors">
    {drows}
  </ul>
</section>

<section class="sec paper" aria-labelledby="pr-h">
  <div class="sec-head">
    <p class="eyebrow">How a project runs</p>
    <h2 id="pr-h" class="rv">{ln("From the first")}{ln("<em>visit to the keys</em>",1)}</h2>
    <p>Six stages, each with something you can hold. Fees are fixed after the first visit and paid in stages. <a href="services.html#process">The full process</a></p>
  </div>
  <ol class="stages rv">
    {stages}
  </ol>
</section>

<section class="sec" aria-labelledby="jr-h">
  <div class="sec-head">
    <p class="eyebrow">Journal</p>
    <h2 id="jr-h" class="rv">{ln("Notes on")}{ln("<em>heat and materials</em>",1)}</h2>
    <p>Short notes from the studio and the workshop.</p>
  </div>
  {jl}
</section>
</main>
'''
    s += cta(P) + footer(P) + scripts(P)
    write("index.html", s)

def journal_list(P):
    items = []
    for j in JOURNAL:
        media = (f'<span class="jimg">{img(P,j["img"][0],"",sizes="(max-width:700px) 100vw, 33vw")}</span>' if "img" in j
                 else f'<span class="jimg" style="position:relative"><span class="tex {j["tex"]}"></span></span>')
        items.append(f'<li><a href="{P}journal.html#{j["id"]}">{media}<small>{j["kind"]} · {j["season"]}</small><b>{j["t"]}</b><p>{j["teaser"]}</p></a></li>')
    return '<ul class="jlist">\n    ' + "\n    ".join(items) + '\n  </ul>'

# ---------- projects index
def projects_index():
    P = "../"
    counts = {k: sum(k in p["types"] for p in PROJECTS) for k, _ in TYPES}
    btns = f'<button type="button" data-f="all" data-name="All" aria-pressed="true">All<sup>{len(PROJECTS)}</sup></button>' + "".join(
        f'<button type="button" data-f="{k}" data-name="{n}" aria-pressed="false">{n}<sup>{counts[k]}</sup></button>' for k, n in TYPES)
    cards = []
    for i, p in enumerate(PROJECTS):
        cls = ["", " b", " c"][i % 3]
        sizes = "(max-width:1000px) 100vw, 55vw" if cls != " b" else "(max-width:1000px) 100vw, 32vw"
        cards.append(f'<li class="pcard{cls}" data-types="{" ".join(p["types"])}"><a href="{p["slug"]}/"><div class="pimg">{img(P,p["cover"],p["cover_alt"],sizes=sizes,lazy=i>1)}</div>'
                     f'<div class="cap"><span class="n">0{i+1}</span><h2>{p["t"]}</h2><span class="meta">{" · ".join(TNAME[t] for t in p["types"])} · {p["place"]}</span></div></a></li>')
    s = head(P, "Projects · Atelier Kambor (fictional studio)", "Six invented interior projects in Phnom Penh and Kampot: homes, shophouses, hospitality, renovations and furniture. Concept site by Loem Layheng.")
    s += top(P, "projects")
    s += f'''<main id="main">
<header class="phead">
  <p class="eyebrow">Projects · {len(PROJECTS)}</p>
  <h1 class="rv">{ln("Rooms we")}{ln("<em>have made</em>",1)}</h1>
  <p class="intro">Homes, a shophouse, guest rooms, a coffee room and a set of furniture. Each page shows the brief, what we changed and the materials. Every project here is invented for this concept site.</p>
</header>
<div class="filters" role="group" aria-label="Filter projects by type"><span class="lbl" aria-hidden="true">Show</span>{btns}</div>
<p class="pcount" id="pcount" aria-live="polite"></p>
<ul class="pgrid" id="pgrid">
  {"""
  """.join(cards)}
</ul>
</main>
'''
    s += cta(P) + footer(P) + scripts(P)
    write("projects/index.html", s)

# ---------- case pages
SHOP_SVG = '''<svg viewBox="0 0 640 330" role="img" aria-labelledby="ba-t" data-state="before">
  <title id="ba-t">Long section through the shophouse, before and after the renovation</title>
  <defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#2B241F" stroke-opacity=".28" stroke-width="1"/></pattern></defs>
  <g fill="none" stroke="#2B241F" stroke-width="1.2">
    <line x1="10" y1="300" x2="630" y2="300"/>
    <line x1="60" y1="300" x2="60" y2="30"/><line x1="580" y1="300" x2="580" y2="30"/>
  </g>
  <text x="14" y="318">Street</text><text x="566" y="318">Lane</text>
  <g class="lay before">
    <rect x="236" y="92" width="150" height="136" fill="url(#hatch)" stroke="none"/>
    <g fill="none" stroke="#2B241F" stroke-width="1.2">
      <line x1="60" y1="230" x2="580" y2="230"/><line x1="60" y1="160" x2="580" y2="160"/><line x1="60" y1="90" x2="580" y2="90"/>
      <line x1="56" y1="30" x2="584" y2="30" stroke-width="2.4"/>
      <polyline points="400,300 420,300 440,230 460,230 480,160 500,160 520,90"/>
      <rect x="60" y="262" width="6" height="38" fill="#2B241F"/>
    </g>
    <text x="80" y="284">Print shop</text><text x="80" y="214">Living</text><text x="80" y="144">Bedrooms</text><text x="80" y="74">Storage, too hot to use</text>
    <text x="250" y="200">Dark middle</text>
  </g>
  <g class="lay after">
    <rect x="300" y="30" width="70" height="200" fill="#9C4A2F" fill-opacity=".08" stroke="none"/>
    <g fill="none" stroke="#2B241F" stroke-width="1.2">
      <line x1="60" y1="230" x2="580" y2="230"/>
      <line x1="60" y1="160" x2="300" y2="160"/><line x1="370" y1="160" x2="580" y2="160"/>
      <line x1="60" y1="90" x2="300" y2="90"/><line x1="370" y1="90" x2="580" y2="90"/>
      <line x1="56" y1="30" x2="300" y2="30" stroke-width="2.4"/><line x1="370" y1="30" x2="584" y2="30" stroke-width="2.4"/>
      <line x1="300" y1="30" x2="370" y2="30" stroke-dasharray="4 3"/>
      <line x1="56" y1="16" x2="584" y2="16"/>
      <polyline points="380,300 400,300 450,230 460,230 510,160 520,160 570,90"/>
      <rect x="60" y="262" width="6" height="38" fill="#2B241F"/><rect x="60" y="244" width="6" height="12" fill="#2B241F"/>
      <rect x="380" y="232" width="2" height="68" fill="#2B241F" stroke="none"/>
    </g>
    <g fill="none" stroke="#9C4A2F" stroke-width="1.2" stroke-dasharray="3 4">
      <line x1="250" y1="-10" x2="325" y2="225"/><line x1="280" y1="-10" x2="350" y2="215"/>
    </g>
    <g fill="none" stroke="#6A4630" stroke-width="1.2">
      <path d="M470 24c10-6 20-6 30 0"/><path d="M200 24c10-6 20-6 30 0"/>
    </g>
    <text x="80" y="284">Shop, own door</text><text x="80" y="214" class="hl">Living, now in daylight</text><text x="80" y="144">Bedrooms</text><text x="80" y="74">Study and drying room</text>
    <text x="310" y="52" class="hl">Light well</text><text x="80" y="11">Ventilated roof</text><text x="420" y="214">New stair</text>
  </g>
</svg>'''

WALK_SCRIPT = r'''<script>
(function(){
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const ROOMS = [
  {name:'Entrance', img:'entrance', w:1200, alt:'A white plaster wall with a patch of window light above a teak sideboard and an armchair, on an oak herringbone floor',
   note:'The door opens onto light, not a corridor. A high window throws one bright shape onto the plaster by late morning, and an old teak sideboard takes keys and post.',
   mat:'Lime plaster · teak · oak herringbone', cap:'Late morning'},
  {name:'Living', img:'living', w:1600, alt:'A living room under a timber ceiling, with a leather sofa, a rattan chair and a woven pendant, glazed on two sides onto trees',
   note:'Glass on two sides, but the roof reaches far past it, so the sun never lands on the sofa. A rattan chair and a woven lamp keep the room light to move around.',
   mat:'Timber ceiling · rattan · deep eaves', cap:'Midday, in shade'},
  {name:'Kitchen', img:'kitchen', w:1600, alt:'A dining table of warm wood under a timber ceiling, with a sliding wall open to a green garden',
   note:'Cooking and eating in one room that faces the garden. A pale floor carries daylight deep inside, so the lamps stay off until dusk.',
   mat:'Teak · polished stone · garden light', cap:'Afternoon'},
  {name:'Bedroom', img:'bedroom', w:1600, alt:'A low bed on a base of old timber beams, white linen and soft cushions against a rough plaster wall',
   note:'Very little in the room: a bed on old timber beams, white linen, a rough plaster wall that holds the cool of the night into the morning.',
   mat:'Reclaimed timber · lime render · linen', cap:'Early morning'},
  {name:'Courtyard', img:'courtyard', w:1600, alt:'An open-air bath of pale stone against a rough plaster wall, with a palm and white pebbles',
   note:'An open-air bath under a strip of sky. Rough lime render, river pebbles and one palm. When it rains, the rain is part of the room.',
   mat:'Rough render · pebble · open sky', cap:'After rain'}
];
const B='../../img/';
const names=document.querySelector('.names'),notes=document.querySelector('.notes'),roomsEl=document.querySelector('.rooms'),photos=document.querySelector('.walk-photos');
ROOMS.forEach((r,i)=>{
  names.insertAdjacentHTML('beforeend',`<h3 class="${i?'':'on'}" ${i?'aria-hidden="true"':''}>${r.name}</h3>`);
  notes.insertAdjacentHTML('beforeend',`<div class="note ${i?'':'on'}" ${i?'aria-hidden="true"':''}><p>${r.note}</p><p class="mat">${r.mat}</p></div>`);
  roomsEl.insertAdjacentHTML('beforeend',`<li><button type="button" data-i="${i}" ${i?'':'aria-current="true"'}>${r.name}</button></li>`);
  photos.insertAdjacentHTML('beforeend',`<figure class="ph ${i?'':'vis'}" style="z-index:${i?0:2}"><img src="${B}${r.img}-s.webp" srcset="${B}${r.img}-s.webp 800w, ${B}${r.img}-l.webp ${r.w}w" sizes="(max-width:1000px) 100vw, 62vw" alt="${r.alt}" ${i>1?'loading="lazy"':''} decoding="async"><figcaption>${r.cap}</figcaption></figure>`);
});
const walk=document.getElementById('walk');
const phs=[...photos.children],hs=[...names.children],ns=[...notes.children],btns=[...roomsEl.querySelectorAll('button')],nowEl=document.getElementById('now');
const planRm=[...document.querySelectorAll('.plan .rm')],planTx=[...document.querySelectorAll('.plan text')],you=document.querySelector('.plan .you'),PC=[[160,150],[60,60],[60,150],[250,95],[160,60]];
planRm[0].classList.add('on');planTx[0].classList.add('on');
let cur=0,walkTop=0,walkLen=1,vh=innerHeight,ticking=false,zTop=3;
function measure(){vh=innerHeight;walkTop=walk.getBoundingClientRect().top+scrollY;walkLen=Math.max(1,walk.offsetHeight-vh)}
function setRoom(i){
  if(i===cur)return;const down=i>cur,prev=cur;cur=i;
  hs.forEach((h,j)=>{h.classList.toggle('on',j===i);h.classList.toggle('above',j<i);h.setAttribute('aria-hidden',j!==i)});
  ns.forEach((n,j)=>{n.classList.toggle('on',j===i);n.setAttribute('aria-hidden',j!==i)});
  btns.forEach((b,j)=>{if(j===i)b.setAttribute('aria-current','true');else b.removeAttribute('aria-current')});
  nowEl.textContent=String(i+1).padStart(2,'0');
  planRm.forEach((r,j)=>r.classList.toggle('on',j===i));planTx.forEach((t,j)=>t.classList.toggle('on',j===i));
  you.style.transform=`translate(${PC[i][0]}px,${PC[i][1]}px)`;
  const el=phs[i];
  phs.forEach((p,j)=>{if(j!==i&&j!==prev){p.classList.remove('vis');p.style.zIndex=0}});
  el.classList.add('vis');el.style.zIndex=++zTop;
  if(RM){phs[prev].classList.remove('vis');return}
  el.style.transition='none';el.style.clipPath=down?'inset(100% 0 0 0)':'inset(0 0 100% 0)';
  el.firstElementChild.style.scale='1.12';
  el.getBoundingClientRect();
  el.style.transition='clip-path 1.6s var(--soft)';el.style.clipPath='inset(0 0 0 0)';
  el.firstElementChild.style.transition='scale 2.2s var(--out)';el.firstElementChild.style.scale='1';
  const p=phs[prev];clearTimeout(p._t);clearTimeout(el._t);
  p._t=setTimeout(()=>{if(cur!==prev){p.classList.remove('vis')}},1700);
}
function onScroll(){
  ticking=false;const y=scrollY;
  const p=Math.min(1,Math.max(0,(y-walkTop)/walkLen));
  const f=p*ROOMS.length,i=Math.min(ROOMS.length-1,Math.floor(f));
  setRoom(i);
  btns.forEach((b,j)=>b.style.setProperty('--p',Math.min(1,Math.max(0,f-j)).toFixed(3)));
  if(!RM){phs.forEach((ph,j)=>{if(ph.classList.contains('vis')){const l=Math.min(1.5,Math.max(-.5,f-j));ph.firstElementChild.style.transform=`translate3d(0,${((l-.5)*-6).toFixed(2)}%,0)`}})}
}
addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});
addEventListener('resize',()=>{measure();onScroll()});
addEventListener('load',()=>{measure();onScroll()});
measure();onScroll();
btns.forEach((b,j)=>b.addEventListener('click',()=>{
  measure();const top=walkTop+walkLen*((j+.5)/ROOMS.length);
  if(window.__lenis)window.__lenis.scrollTo(top);else scrollTo({top,behavior:RM?'auto':'smooth'});
}));
})();
</script>
'''

WALK_HTML = '''<section class="walk" id="walk" aria-labelledby="walk-h">
  <div class="walk-frame">
    <div class="walk-text">
      <p class="eyebrow" id="walk-h">A walk through the house</p>
      <svg class="plan" viewBox="-2 -2 304 194" role="img" aria-label="Floor plan of the house, with the current room marked">
        <rect class="rm" x="120" y="110" width="80" height="80"/><rect class="rm" x="0" y="0" width="120" height="110"/><rect class="rm" x="0" y="110" width="120" height="80"/><rect class="rm" x="200" y="0" width="100" height="190"/><rect class="rm" x="120" y="0" width="80" height="110"/>
        <path d="M145 190H0V0H300V190H175M120 0V70M120 92V190M200 0V58M200 80V190M0 110H48M72 110H120M120 110H148M172 110H200"/>
        <rect class="court" x="132" y="12" width="56" height="86"/>
        <text x="128" y="182">Entrance</text><text x="8" y="16">Living</text><text x="8" y="182">Kitchen</text><text x="208" y="16">Bedroom</text><text x="137" y="24">Court</text>
        <circle class="you" r="3.2" cx="0" cy="0" style="transform:translate(160px,150px)"/>
      </svg>
      <p class="count" aria-hidden="true"><span class="now"><span id="now">01</span></span><span>/ 05</span></p>
      <div class="names" aria-live="polite"></div>
      <div class="notes"></div>
      <ol class="rooms" aria-label="Rooms"></ol>
    </div>
    <div class="walk-photos"></div>
  </div>
</section>
'''

def case(i):
    p = PROJECTS[i]; P = "../../"; nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    types = " · ".join(TNAME[t] for t in p["types"])
    changes = "".join(f'<li>{c}</li>' for c in p["changes"])
    extra_head = f'<link rel="preload" as="image" href="{P}img/{p["cover"]}-l.webp" imagesrcset="{P}img/{p["cover"]}-s.webp 800w, {P}img/{p["cover"]}-l.webp {SIZES[p["cover"]][0]}w" imagesizes="100vw">\n'
    s = head(P, f'{p["plain"]} · Atelier Kambor (fictional studio)',
             f'{p["short"]} An invented project by a fictional interior studio in Phnom Penh. Concept site by Loem Layheng.', extra_head)
    s += top(P, "projects")
    s += f'''<main id="main">
<header class="phead case-head">
  <p class="eyebrow"><a class="link" href="../">Projects</a> · 0{i+1} · {types}</p>
  <h1 class="rv">{ln(p["t"].split(" <em>")[0])}{ln("<em>"+p["t"].split("<em>")[1], 1)}</h1>
  <dl class="case-facts">
    <div><dt>Type</dt><dd>{types}</dd></div>
    <div><dt>Where</dt><dd>{p["place"]}</dd></div>
    <div><dt>Size</dt><dd>{p["size"]}</dd></div>
    <div><dt>Scope</dt><dd>{p["scope"]}</dd></div>
    <div><dt>Status</dt><dd>Invented for this concept site</dd></div>
  </dl>
</header>
<figure class="cover" style="margin-top:0">{img(P,p["cover"],p["cover_alt"],lazy=False,extra=' fetchpriority="high"')}</figure>

<section class="brief grid12" aria-labelledby="brief-h">
  <p class="eyebrow" id="brief-h">The brief</p>
  <p class="lead">{p["brief"]}</p>
  <h2 class="eyebrow changes-h" id="ch-h">What we changed</h2>
  <ol class="changes" aria-labelledby="ch-h">{changes}</ol>
  <p class="team-line">Studio team: {p["team"]}. No client names, on this site or any other.</p>
</section>
'''
    if p["slug"] == "house-in-toul-kork":
        s += WALK_HTML
    if p.get("ba"):
        s += f'''<section class="ba grid12" aria-labelledby="ba-h">
  <p class="eyebrow" id="ba-h">Before and after</p>
  <div class="ba-body">
    <div class="ba-tabs" role="group" aria-label="Show the section drawing"><button type="button" data-s="before" aria-pressed="true" data-cap="Before: one steep stair, rooms in a row and a dark middle on every floor. The top floor stored paper and was too hot to use.">Before</button><button type="button" data-s="after" aria-pressed="false" data-cap="After: a light well from the roof down to the living room, a gentler stair beside it, a ventilated roof and a separate door for the family.">After</button></div>
    <div class="ba-fig">{SHOP_SVG}</div>
    <p class="ba-cap" aria-live="polite">Before: one steep stair, rooms in a row and a dark middle on every floor. The top floor stored paper and was too hot to use.</p>
  </div>
</section>
'''
    if p["gallery"]:
        g = p["gallery"]
        s += '<section class="gallery" aria-label="More photos">'
        s += f'<figure class="g1{' solo' if len(g)==1 else ''}"><div class="gi">{img(P,g[0][0],g[0][1],sizes="(max-width:1000px) 100vw, 55vw")}</div><figcaption>{g[0][2]}</figcaption></figure>'
        if len(g) > 1:
            s += f'<figure class="g2"><div class="gi">{img(P,g[1][0],g[1][1],sizes="(max-width:1000px) 100vw, 32vw")}</div><figcaption>{g[1][2]}</figcaption></figure>'
        s += '</section>\n'
    s += f'''<section class="mats grid12" aria-labelledby="mat-h">
  <p class="eyebrow" id="mat-h">Materials</p>
  <ul class="chips">{chips(p["mats"])}</ul>
  <p class="team-line">See them all in the <a class="link" href="../../studio.html#materials">materials library</a>, or come and touch the samples at the studio.</p>
</section>
<a class="next" href="../{nxt["slug"]}/">
  <div class="grid12"><p class="eyebrow">Next project</p><b>{nxt["t"]}</b><span class="nimg">{img(P,nxt["cover"],"",sizes="260px")}</span></div>
</a>
</main>
'''
    s += cta(P) + footer(P) + scripts(P, WALK_SCRIPT if p["slug"] == "house-in-toul-kork" else "")
    write(f'projects/{p["slug"]}/index.html', s)

# ---------- studio
def portrait(kind, initial, body, headc, label):
    back = {
      "arch": '<path d="M48 250V96a52 52 0 0 1 104 0v154" fill="#E4DCCE"/>',
      "grid": '<g stroke="#2B241F" stroke-opacity=".18" stroke-width="1">' + "".join(f'<line x1="{x}" y1="20" x2="{x}" y2="250"/>' for x in range(20, 200, 20)) + "".join(f'<line x1="0" y1="{y}" x2="200" y2="{y}"/>' for y in range(20, 250, 20)) + '</g><path d="M128 40l50 0-50 50z" fill="none" stroke="#9C4A2F" stroke-width="1.5"/>',
      "slats": "".join(f'<rect x="0" y="{y}" width="200" height="9" fill="#E4DCCE"/>' for y in range(14, 250, 22)),
      "cane": '<circle cx="100" cy="112" r="78" fill="#C49A5E" opacity=".35"/><circle cx="100" cy="112" r="78" fill="none" stroke="#6A4630" stroke-opacity=".4" stroke-dasharray="2 5" stroke-width="6"/>',
      "bubble": '<path d="M26 36h120a12 12 0 0 1 12 12v44a12 12 0 0 1-12 12H70l-20 18v-18H26a12 12 0 0 1-12-12V48a12 12 0 0 1 12-12z" fill="#E4DCCE"/><g fill="#9C4A2F"><circle cx="66" cy="70" r="3.5"/><circle cx="86" cy="70" r="3.5"/><circle cx="106" cy="70" r="3.5"/></g>',
    }[kind]
    return (f'<svg viewBox="0 0 200 250" role="img" aria-label="{label}">{back}'
            f'<path d="M36 250c0-58 28-84 64-84s64 26 64 84z" fill="{body}"/>'
            f'<circle cx="100" cy="118" r="32" fill="{headc}"/>'
            f'<text x="12" y="34" font-family="Cormorant, Georgia, serif" font-style="italic" font-size="28" fill="#2B241F">{initial}</text></svg>')

def studio():
    P = ""
    people = [
      ("Chantrea", "Founder and lead designer", "Trained in interior architecture abroad, worked in studios there, then came home and started Kambor. Leads every concept.", portrait("arch", "C", "#9C4A2F", "#C49A5E", "Abstract portrait: a figure in laterite red in front of an arched doorway")),
      ("Vibol", "Project architect", "Turns ideas into drawings a builder can price. Prepares the drawings for permits and checks every structural change.", portrait("grid", "V", "#2B241F", "#9C4A2F", "Abstract portrait: a dark figure in front of a drawing grid and a set square")),
      ("Rithy", "Site coordinator", "On site every week. Sends the photo updates on Telegram and keeps the snag list honest.", portrait("slats", "R", "#5E6F5E", "#D9B98A", "Abstract portrait: a green figure in front of horizontal slats")),
      ("Sophea", "Furniture and sourcing", "Works with the workshops, weavers and tile makers. Knows who can make what, and how long it really takes.", portrait("cane", "S", "#6A4630", "#9C4A2F", "Abstract portrait: a brown figure in front of a woven cane circle")),
      ("Malis", "Studio assistant", "Answers Telegram, books site visits and makes sure nobody waits too long for a reply.", portrait("bubble", "M", "#C49A5E", "#5E6F5E", "Abstract portrait: a rattan-coloured figure under a speech bubble")),
    ]
    plist = "\n    ".join(f'<li class="person">{sv}<b>{n}</b><small>{r}</small><p>{d}</p></li>' for n, r, d, sv in people)
    values = [
      ("We say no when the brief is not right for us.", "If we are not the right studio, we tell you at the first visit, and often who might be."),
      ("Every quote is itemised.", "Furniture and materials at cost plus a clear handling fee, shown on every line."),
      ("No commissions from suppliers.", "We choose a tile because it is right for the floor, not because someone pays us to."),
      ("Drawings any builder can price.", "Keep your own contractor if you like. We hand them a full set and visit site."),
      ("Khmer and English, on paper too.", "Every drawing, quote and care guide in the language you prefer."),
      ("Things you can repair.", "Lime, oiled wood, cement tiles, woven cane. When something wears, it can be fixed here."),
    ]
    vlist = "\n    ".join(f'<li class="rise" style="--i:{i}"><b>{a}</b><p>{b}</p></li>' for i, (a, b) in enumerate(values))
    stages = "\n    ".join(f'<li class="rise" style="--i:{i}"><small>0{i+1}</small><b>{s[0]}</b><p>{s[3]}</p><span class="dur">{s[1]}</span></li>' for i, s in enumerate(STAGES))
    s = head(P, "Studio · Atelier Kambor (fictional studio)", "About the invented interior studio Atelier Kambor in Phnom Penh: who we are, the people, what we believe and the materials library. Concept site by Loem Layheng.")
    s += top(P, "studio")
    s += f'''<main id="main">
<header class="phead">
  <p class="eyebrow">Studio</p>
  <h1 class="rv">{ln("A small studio")}{ln("<em>in Boeung Keng Kang</em>",1)}</h1>
  <p class="intro">Five people, one long table, a wall of samples and a workshop we trust on the edge of the city.</p>
</header>
<section class="about grid12" aria-labelledby="ab-h">
  <p class="eyebrow" id="ab-h">Who we are</p>
  <p class="lead">Chantrea trained abroad, worked in other people's studios, and came home to Phnom Penh to design for the way people here <em>actually live</em>: heat, rain, three generations under one roof, shoes at the door.</p>
  <div class="prose">
    <p>Kambor is the Khmer word for lime. We use it on walls that breathe, and we plan the rest of a house around the same idea: shade first, air moving through, and materials that look better after ten wet seasons than on the first day.</p>
    <p>We are small on purpose. The person who visits your home on the first day is the person who draws it and the person who walks through it with you at handover. We take on a few projects at a time, from one room to a whole building, in Phnom Penh, Siem Reap and Kampot.</p>
  </div>
  <figure><svg viewBox="0 0 300 380" role="img" aria-label="Drawn plan of the studio: an entrance from the street, one long work table, a wall of material samples, a meeting table by a small court, and a model bench at the back" style="display:block;width:100%;height:auto;background:var(--paper);border:1px solid var(--line)">
<g fill="none" stroke="#2B241F" stroke-width="1.2"><path d="M20 20H280V360H170M130 360H20V20"/><rect x="60" y="70" width="70" height="200"/><rect x="190" y="250" width="70" height="70" stroke-dasharray="3 3"/><circle cx="225" cy="285" r="18"/><rect x="180" y="40" width="80" height="50"/></g>
<rect x="22" y="40" width="14" height="300" fill="#9C4A2F" fill-opacity=".18"/>
<g font-family="Hanken Grotesk, sans-serif" font-size="9" letter-spacing="1.2" fill="#6A6056"><text x="72" y="170" transform="rotate(-90 72 170)">LONG TABLE</text><text x="42" y="60" transform="rotate(90 42 60)">SAMPLE WALL</text><text x="186" y="104">MODEL BENCH</text><text x="196" y="244">COURT</text><text x="132" y="374">STREET DOOR</text></g>
<g fill="#6A4630"><circle cx="52" cy="95" r="5"/><circle cx="52" cy="140" r="5"/><circle cx="52" cy="185" r="5"/><circle cx="52" cy="230" r="5"/><circle cx="138" cy="110" r="5"/><circle cx="138" cy="160" r="5"/><circle cx="138" cy="210" r="5"/></g></svg><figcaption>The studio, ground floor. Drawn, like the studio itself.</figcaption></figure>
</section>

<section class="sec paper" aria-labelledby="pp-h">
  <div class="sec-head">
    <p class="eyebrow">People</p>
    <h2 id="pp-h" class="rv">{ln("Who you")}{ln("<em>will meet</em>",1)}</h2>
    <p>First names only. Portraits are drawn shapes: these people are invented.</p>
  </div>
  <ul class="people">
    {plist}
  </ul>
</section>

<section class="sec" aria-labelledby="vl-h">
  <div class="sec-head">
    <p class="eyebrow">What we hold to</p>
    <h2 id="vl-h" class="rv">{ln("Plain")}{ln("<em>promises</em>",1)}</h2>
    <p>Things a client can check us on.</p>
  </div>
  <ul class="values rv">
    {vlist}
  </ul>
</section>

<section class="sec paper" aria-labelledby="hw-h">
  <div class="sec-head">
    <p class="eyebrow">How we work</p>
    <h2 id="hw-h" class="rv">{ln("Six stages,")}{ln("<em>one team</em>",1)}</h2>
    <p>The same people from the first visit to the handover. <a href="services.html#process">Stages, fees and FAQ</a></p>
  </div>
  <ol class="stages rv">
    {stages}
  </ol>
</section>

<section class="sec" id="materials" aria-labelledby="mt-h">
  <div class="sec-head">
    <p class="eyebrow">Materials library</p>
    <h2 id="mt-h" class="rv">{ln("Seven things")}{ln("we <em>build with</em>",1)}</h2>
    <p>Local where we can: they last in the humidity, and the money stays in the country.</p>
  </div>
  <ul class="swatches" id="swatches">
    {swatch_list()}
  </ul>
  <div class="visit">
    <h3>Come and touch <em>the samples</em></h3>
    <p>The library is one wall of the studio: tiles, stones, woods, cane, cloth and lime finishes in every colour we mix. Visit Monday to Friday, 8:00 to 17:00, or on a Saturday morning by appointment.</p>
    <div class="act"><a class="btn" href="contact.html">Plan a visit <span class="arr" aria-hidden="true">→</span></a></div>
  </div>
</section>
</main>
'''
    s += cta(P) + footer(P) + scripts(P)
    write("studio.html", s)

# ---------- services
def services():
    P = ""
    svc = [
      ("homes", "Homes", "Villas, flats, borey houses", "A whole house, one floor or a single room. We plan for heat and rain first, then for how your family uses the rooms: where shoes go, where grandparents sit, where the rice cooker lives.",
       ["Layout and furniture plan", "Built-in storage and joinery", "Lighting, fans and air-con placement", "Materials, colours and soft furnishings"],
       ("A one-bedroom refresh with built-ins", "Fits a smaller budget.", "house-in-toul-kork", "House in Toul Kork")),
      ("shophouses", "Shophouses", "Shop below, family above", "The building type of the city. We bring light into the middle, separate the shop from the home and make the stair something you want to climb.",
       ["Light wells and ventilation", "Separate entrances for shop and home", "New stairs and floors", "Shopfront and signage space"],
       ("A shophouse with a café below and a home above", "A medium to large budget.", "shophouse-in-daun-penh", "Shophouse in Daun Penh")),
      ("hospitality", "Hospitality", "Cafés, small hotels, guesthouses", "Rooms that guests remember and staff can keep clean. We plan around opening dates, and can work in phases so you stay open.",
       ["Layout and flow for staff and guests", "Bars, counters and built-in seating", "Room fit-outs, linen and lighting", "Phased work while you stay open"],
       ("A ten-room guesthouse in Kampot", "A larger budget, done in phases.", "guest-rooms-in-kampot", "Guest rooms in Kampot")),
      ("renovations", "Renovations", "Old Khmer and colonial buildings, tired flats", "We keep what is good, like old tiles, timber and high ceilings, and fix what is not: damp, heat, dark rooms and wiring.",
       ["Survey of the building as it is", "Damp, roof and ventilation fixes", "Keeping and repairing old materials", "Drawings for permits where needed"],
       ("Opening up a 1960s villa", "A larger budget; a single floor fits a smaller one.", "flat-by-the-river", "Flat by the river")),
      ("furniture", "Furniture", "Made to order with local workshops", "Tables, beds, shelving, vanities and benches, drawn by us and made in town from dry hardwood, plywood, cane and stone. We come back to fix them.",
       ["Drawings in Khmer and English", "Workshop visits during making", "Delivery and fitting", "Repairs to anything our workshops made"],
       ("Just furniture, no renovation", "Fits a smaller budget.", "joinery-in-tonle-bassac", "Joinery in Tonle Bassac")),
    ]
    rows = []
    for i, (k, t, sub, d, inc, typ) in enumerate(svc):
        incl = "".join(f"<li>{x}</li>" for x in inc)
        rows.append(f'<li id="{k}"><span class="n">0{i+1}</span><h3>{t}<small>{sub}</small></h3><div><p>{d}</p><ul>{incl}</ul></div>'
                    f'<p class="typ"><b>Typical project</b>{typ[0]}. {typ[1]}<br><br>See: <a class="link" href="projects/{typ[2]}/">{typ[3]}</a></p></li>')
    steps = "\n    ".join(f'<li class="step"><span class="n">0{i+1}</span><h3>{s[0]}</h3><p>{s[2]}<br><span style="color:var(--laterite);font-size:14px">{s[1]}</span></p><p class="get"><b>You get</b>{s[3]}</p></li>' for i, s in enumerate(STAGES))
    faq = [
      ("Do you handle building permits?", "We prepare the drawings for the permit. You or your contractor submit them. If a change needs a permit, we tell you early, before it costs anything."),
      ("Can I keep my own contractor?", "Yes. We hand them a full drawing set and visit site. If you do not have one, we can suggest builders we have worked with, and you choose."),
      ("What about the rainy season?", "We plan roof, wet and outdoor work for the dry months, roughly November to April. Interiors can run all year."),
      ("Which languages do you work in?", "Khmer and English, in meetings, on site and on paper. Every drawing and quote can be in either."),
      ("Can you do just one room, or just furniture?", "Yes. Many projects start with one room. Furniture on its own is welcome too."),
      ("Do you work with landlords and rented flats?", "Yes, with ideas you can take with you or undo when you move: furniture, lighting, curtains, paint."),
      ("Do you work outside Phnom Penh?", "Siem Reap and Kampot regularly, with travel costs agreed up front. Further away, ask us."),
    ]
    faqs = "\n  ".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p class="a">{a}</p></details>' for q, a in faq)
    s = head(P, "Services · Atelier Kambor (fictional studio)", "What the invented studio Atelier Kambor designs, how a project runs, how fees work, and answers to common questions. Concept site by Loem Layheng.")
    s += top(P, "services")
    s += f'''<main id="main">
<header class="phead">
  <p class="eyebrow">Services</p>
  <h1 class="rv">{ln("What we design,")}{ln("<em>and how</em>",1)}</h1>
  <p class="intro">Five kinds of project, six stages, fees agreed in writing before any drawing starts. If you only want an hour of advice at home, there is a way to start small.</p>
</header>
<section class="sec" style="padding-top:0" aria-labelledby="w-h">
  <h2 class="sr" id="w-h">What we design</h2>
  <ul class="svc">
    {"""
    """.join(rows)}
  </ul>
  <div class="small-start on-dark" id="start-small">
    <p class="eyebrow">Start small</p>
    <h3>A two-hour consult <em>at your home</em></h3>
    <p>A paid visit with Chantrea: we walk through the space with you and leave a written list of ideas you can do yourself or with us later.</p>
    <div class="act"><a class="btn" href="contact.html#enquiry">Ask for a consult <span class="arr" aria-hidden="true">→</span></a></div>
  </div>
</section>

<figure class="band">{img(P,"courtyard","An open-air bath of pale stone against a rough lime wall, with a palm and white pebbles",sizes="100vw")}<figcaption>Shade, moving air and a strip of sky: the start of most of our briefs. From the House in Toul Kork.</figcaption></figure>
<section class="sec paper" id="process" aria-labelledby="p-h">
  <div class="sec-head">
    <p class="eyebrow">How a project runs</p>
    <h2 id="p-h" class="rv">{ln("First visit")}{ln("<em>to handover</em>",1)}</h2>
    <p>Durations are typical, in words, because every space is different.</p>
  </div>
  <ol class="steps">
    {steps}
  </ol>
</section>

<section class="sec" id="fees" aria-labelledby="f-h">
  <div class="two">
    <p class="eyebrow">Fees, in words</p>
    <div class="body">
      <div><h3 id="f-h">How fees work</h3><ul>
        <li><b>A fixed design fee</b>, agreed in writing after the site visit.</li>
        <li><b>Paid in stages:</b> at the start, at concept sign-off, and with the drawings.</li>
        <li><b>Site supervision</b> charged monthly or per visit, whichever suits the job.</li>
        <li><b>Furniture and materials</b> at cost plus a clear handling fee, shown on every quote.</li>
        <li><b>No hidden commissions</b> from suppliers.</li>
      </ul></div>
      <div><h3>What we need to start</h3><ul>
        <li>Photos or a plan of the space.</li>
        <li>A rough budget, even a wide one.</li>
        <li>Who lives or works there.</li>
        <li>Anything that must stay: a cabinet, a shrine, a tree.</li>
        <li>Timing: Khmer New Year, Pchum Ben, a wedding, an opening date.</li>
      </ul></div>
      <div><h3>Where we work</h3><p>Phnom Penh mostly. Siem Reap and Kampot regularly, with travel costs agreed up front. Further away, ask us.</p></div>
      <div><h3>Aftercare</h3><p>A check-in visit a few months after handover. A care guide for wood, stone and fabric in the humidity. Help fixing anything our workshops made.</p></div>
    </div>
  </div>
</section>

<section class="sec paper" id="faq" aria-labelledby="q-h">
  <div class="sec-head">
    <p class="eyebrow">Questions clients ask</p>
    <h2 id="q-h" class="rv">{ln("Before")}{ln("<em>you ask</em>",1)}</h2>
    <p>Something else? Ask on Telegram or in the enquiry form.</p>
  </div>
  <div class="faq">
  {faqs}
  </div>
</section>
</main>
'''
    s += cta(P) + footer(P) + scripts(P)
    write("services.html", s)

# ---------- journal
def journal():
    P = ""
    bodies = {
      "cool-house": ('''<p>Most new houses in the city are built to be cooled by machines: big windows facing the sun, low ceilings, sealed rooms. The air conditioner then fights the building all day. Older houses here did it the other way round.</p>
<h3>Shade first</h3><p>Deep eaves, verandas, screens and trees keep the sun off the walls and the glass. A window in shade lets in light without the heat. This is the cheapest cooling there is, and it works when the power is off.</p>
<h3>Air that moves through</h3><p>Rooms lined up with the breeze, windows on two sides, high vents and a court or light well to pull warm air up and out. A ceiling fan over every bed and sofa does the rest for most of the year.</p>
<h3>Walls that breathe</h3><p>Lime plaster lets damp walls dry out instead of trapping water behind paint. Thick walls hold the cool of the night into the morning.</p>
<p>The air conditioner stays, for the hottest weeks and the bedrooms at night. It just stops being the first tool.</p>''', "A window in shade lets in light without the heat."),
      "terrazzo": ('''<p>Terrazzo is one of the few floors that is made where it lies. It is cool underfoot, it can be polished again in twenty years, and it can carry chips of stone left over from other jobs.</p>
<ol><li>We choose the chips with you: marble, local stone, a little glass, sometimes broken tile. Samples are poured in the studio first.</li>
<li>The chips are mixed with grey or white cement and colour, and poured between thin strips that divide the floor.</li>
<li>The floor cures slowly and is kept damp for days, so it does not crack.</li>
<li>Then it is ground flat, filled, and polished in several passes, finer each time.</li></ol>
<p>We pour in the dry months when we can. Rain and high humidity slow the curing, and a floor that dries unevenly shows it for ever.</p>''', "A floor that dries unevenly shows it for ever."),
      "workshop": ('''<p>Most of our furniture is made in a workshop on the edge of the city, by people we have worked with for years. We bring drawings in Khmer and English, and we change them at the bench when the makers know better.</p>
<h3>Dry wood in a wet country</h3><p>Wood moves with the air. A table made from wet timber will crack or twist in its first rainy season. We use reclaimed hardwood that has dried for years, or plywood with a solid edge where a piece must stay flat.</p>
<h3>Oil, not lacquer</h3><p>Lacquer looks perfect on the first day and peels in the humidity. Oil soaks in, darkens slowly, and can be sanded and oiled again at home. We leave a small bottle with every piece.</p>
<p>And when something breaks, the same workshop comes back to fix it.</p>''', "We leave a small bottle of oil with every piece."),
    }
    notes = []
    for j in JOURNAL:
        body, pull = bodies[j["id"]]
        fig = (f'<figure class="jfig"><div class="gi">{img(P,j["img"][0],j["img"][1],sizes="(max-width:1000px) 100vw, 75vw")}</div><figcaption>Photo for illustration, from Unsplash.</figcaption></figure>' if "img" in j
               else f'<figure class="jfig"><div class="gi texfig"><span class="tex {j["tex"]}" role="img" aria-label="A drawn terrazzo surface: chips of red, brown, green and grey stone in pale cement"></span></div><figcaption>Terrazzo, drawn from a studio sample.</figcaption></figure>')
        notes.append(f'''<article class="jnote grid12" id="{j["id"]}" aria-labelledby="{j["id"]}-h">
  <div class="meta"><small>{j["kind"]}</small><span>{j["season"]} · {j["read"]}</span></div>
  <h2 id="{j["id"]}-h">{j["t"]}</h2>
  {fig}
  <div class="prose">{body}</div>
  <aside aria-label="Pull quote">{pull}</aside>
</article>''')
    toc = "".join(f'<li><a class="link" href="#{j["id"]}">{j["t"]}</a></li>' for j in JOURNAL)
    s = head(P, "Journal · Atelier Kambor (fictional studio)", "Short notes from an invented interior studio in Phnom Penh: keeping a house cool, pouring terrazzo, and a morning at the joinery workshop. Concept site by Loem Layheng.")
    s += top(P, "journal")
    s += f'''<main id="main">
<header class="phead">
  <p class="eyebrow">Journal · {len(JOURNAL)} notes</p>
  <h1 class="rv">{ln("Notes from")}{ln("<em>the studio</em>",1)}</h1>
  <nav class="intro" aria-label="Notes on this page"><ol style="list-style:none;display:grid;gap:8px">{toc}</ol></nav>
</header>
{"""
""".join(notes)}
</main>
'''
    s += cta(P) + footer(P) + scripts(P)
    write("journal.html", s)

# ---------- contact
MAP_SVG = '''<svg viewBox="0 0 600 420" role="img" aria-labelledby="map-t">
  <title id="map-t">Drawn map: the studio sits on a side street in Boeung Keng Kang 1, between Norodom and Monivong boulevards, south of Sihanouk Boulevard</title>
  <rect width="600" height="420" fill="#F5F1EA"/>
  <g class="blk">
    <rect x="20" y="20" width="120" height="90"/><rect x="160" y="20" width="110" height="90"/><rect x="290" y="20" width="130" height="90"/><rect x="440" y="20" width="140" height="90"/>
    <rect x="20" y="150" width="120" height="100"/><rect x="160" y="150" width="110" height="46"/><rect x="160" y="212" width="110" height="38"/><rect x="290" y="150" width="130" height="100"/><rect x="440" y="150" width="140" height="100"/>
    <rect x="20" y="270" width="120" height="130"/><rect x="160" y="270" width="110" height="130"/><rect x="290" y="270" width="130" height="130"/><rect x="440" y="270" width="140" height="130"/>
  </g>
  <g fill="none" stroke="#2B241F" stroke-opacity=".55" stroke-width="1">
    <line x1="0" y1="130" x2="600" y2="130" stroke-width="3" stroke-opacity=".7"/>
    <line x1="150" y1="0" x2="150" y2="420" stroke-width="3" stroke-opacity=".7"/>
    <line x1="430" y1="0" x2="430" y2="420" stroke-width="3" stroke-opacity=".7"/>
  </g>
  <text x="20" y="124">Sihanouk Blvd</text>
  <text x="158" y="410" transform="rotate(-90 158 410)">Monivong Blvd</text>
  <text x="438" y="410" transform="rotate(-90 438 410)">Norodom Blvd</text>
  <text x="300" y="266">BKK1</text>
  <circle class="ring" cx="232" cy="204" r="10"/>
  <circle class="pin" cx="232" cy="204" r="6"/>
  <text x="246" y="200" class="lbl" style="fill:#9C4A2F">Atelier Kambor</text>
  <path d="M560 380l0-26m0 0l-6 10m6-10l6 10" stroke="#2B241F" fill="none"/><text x="555" y="398">N</text>
</svg>'''

def contact():
    P = ""
    def opts(name, items, req=False, first_id=None):
        out = []
        for i, it in enumerate(items):
            iid = f' id="{first_id}"' if (first_id and i == 0) else ""
            out.append(f'<label><input type="radio" name="{name}" value="{it}"{iid}{" required" if (req and False) else ""}><span>{it}</span></label>')
        return '<div class="opts">' + "".join(out) + "</div>"
    s = head(P, "Contact · Atelier Kambor (fictional studio)", "Contact page and enquiry form for the invented interior studio Atelier Kambor in Phnom Penh. Nothing is sent: this is a concept site by Loem Layheng.")
    s += top(P, "contact")
    s += f'''<main id="main">
<header class="phead">
  <p class="eyebrow">Contact</p>
  <h1 class="rv">{ln("Tell us")}{ln("<em>about the space</em>",1)}</h1>
  <p class="intro">Most clients reach us on Telegram. You can also call, write, visit the studio, or fill in the short form below.</p>
</header>
<section class="reach" aria-labelledby="r-h">
  <h2 class="sr" id="r-h">Ways to reach the studio</h2>
  <div class="reach-grid">
    <div class="reach-main">
      <span class="tg-wrap"><button class="tgbig" type="button" data-note="tg-main" aria-expanded="false" aria-controls="tg-main">{PLANE} Telegram</button>
      <span class="tg-note" id="tg-main" hidden>Atelier Kambor is invented, so there is no Telegram account behind this button. On a real studio site it would open a chat.</span></span>
      <p class="promise">We usually reply the same day, in Khmer or English.</p>
      <ul class="reach-list">
        <li><small>Phone</small><span>+855 XX XXX XXX <span style="color:var(--mute)">(placeholder)</span></span></li>
        <li><small>Email</small><a class="link" href="mailto:studio@kambor.example">studio@kambor.example</a></li>
        <li><small>WhatsApp</small><span>Second choice, same number</span></li>
        <li><small>Studio</small><span>Street 2XX, Boeung Keng Kang 1, Phnom Penh. Ground floor, green door.</span></li>
        <li><small>Hours</small><span>Monday to Friday, 8:00 to 17:00<br>Saturday mornings by appointment<br>Closed for Khmer New Year and Pchum Ben</span></li>
      </ul>
    </div>
    <figure class="map">{MAP_SVG}<figcaption><span>Drawn map, not to scale. The address is invented.</span><span>Map link: placeholder</span></figcaption></figure>
  </div>
</section>

<section class="enq-sec" id="enquiry" aria-labelledby="e-h">
  <div class="sec-head">
    <p class="eyebrow">Enquiry</p>
    <h2 id="e-h" class="rv">{ln("A short")}{ln("<em>enquiry</em>",1)}</h2>
    <p>About three minutes. Only your name, a way to reach you and the kind of project are needed.</p>
  </div>
  <div class="form">
    <div class="side">
      <p class="eyebrow">Good to know</p>
      <p>This is a concept site. The form works, but nothing is sent anywhere and nobody will reply.</p>
      <ul><li>Photos or a plan help most.</li><li>A wide budget is better than none.</li><li>Tell us about festivals or opening dates.</li></ul>
    </div>
    <form class="fields" id="enquiry-form" novalidate aria-describedby="form-errors">
      <p class="form-errors" id="form-errors" role="alert"></p>
      <fieldset class="fset"><legend>About you</legend>
        <div class="frow">
          <div class="field"><label for="f-name">Your name</label><input type="text" id="f-name" name="name" autocomplete="name" required aria-describedby="e-name"><span class="err" id="e-name"></span></div>
          <div class="field"><label for="f-contact">Telegram or phone</label><input type="text" id="f-contact" name="contact" autocomplete="tel" required placeholder="@name or 0XX XXX XXX" aria-describedby="e-contact"><span class="err" id="e-contact"></span></div>
          <div class="field full"><span class="q" id="lang-q">Preferred language <span class="opt">(optional)</span></span><div role="radiogroup" aria-labelledby="lang-q">{opts("lang", ["Khmer", "English", "Either"])}</div></div>
        </div>
      </fieldset>
      <fieldset class="fset"><legend>The project</legend>
        <div class="frow">
          <div class="field full" id="type-q"><span class="q" id="type-l">Kind of project</span><div role="radiogroup" aria-labelledby="type-l" aria-describedby="e-type" aria-required="true">{opts("type", ["Home", "Shophouse", "Hospitality", "Renovation", "Furniture"], first_id="t-homes")}</div><span class="err" id="e-type"></span></div>
          <div class="field"><label for="f-loc">Location <span class="opt">(optional)</span></label><input type="text" id="f-loc" name="location" placeholder="District or town"></div>
          <div class="field"><label for="f-start">Ideal start <span class="opt">(optional)</span></label><select id="f-start" name="start"><option value="">Choose one</option><option>As soon as possible</option><option>In the next three months</option><option>Before Khmer New Year</option><option>After Pchum Ben</option><option>Later, just planning</option></select></div>
          <div class="field full"><span class="q" id="st-q">The space is <span class="opt">(optional)</span></span><div role="radiogroup" aria-labelledby="st-q">{opts("status", ["Empty", "Lived in", "Under construction"])}</div></div>
          <div class="field full"><span class="q" id="b-q">Rough budget <span class="opt">(optional)</span></span><div role="radiogroup" aria-labelledby="b-q">{opts("budget", ["A small refresh", "One floor", "A whole house", "Commercial"])}</div></div>
          <div class="field full"><span class="q" id="file-q">A photo or plan <span class="opt">(optional)</span></span><div class="file"><input type="file" id="f-file" name="file" accept="image/*,.pdf" multiple aria-labelledby="file-q"><label class="pick" for="f-file">Choose files</label><span class="fname" id="f-file-name">No file chosen</span></div></div>
          <div class="field full"><label for="f-msg">Anything else <span class="opt">(optional)</span></label><textarea id="f-msg" name="message" placeholder="Who lives or works there, what must stay, what bothers you most about the space"></textarea></div>
        </div>
      </fieldset>
      <fieldset class="fset"><legend>First site visit <small>Optional, free, about an hour</small></legend>
        <div class="frow">
          <div class="field"><span class="q" id="sl-q">Best time</span><div role="radiogroup" aria-labelledby="sl-q">{opts("slot", ["Weekday morning", "Weekday afternoon"])}</div></div>
          <div class="field"><span class="q" id="h-q">Is someone home to open the door?</span><div role="radiogroup" aria-labelledby="h-q">{opts("home", ["Yes", "Not sure yet"])}</div></div>
        </div>
      </fieldset>
      <div class="submit-row"><p>We confirm visits on Telegram. On this concept site, nothing is sent.</p><button class="btn fill" type="submit">Send enquiry <span class="arr" aria-hidden="true">→</span></button></div>
    </form>
    <div class="done on-dark" id="done" tabindex="-1" hidden aria-labelledby="done-h">
      <p class="eyebrow">Enquiry ready</p>
      <h3 id="done-h">Thank you, <em id="done-name"></em>.</h3>
      <p>On a real studio site, this would reach Malis, who answers enquiries, and you would usually hear back the same day on Telegram.</p>
      <p class="notice"><strong>Nothing was sent.</strong> Atelier Kambor is a fictional studio and this is a concept site by Loem Layheng. Your answers stay in this browser tab and are gone when you leave.</p>
      <dl id="summary"></dl>
      <div class="acts"><button class="btn" type="button" id="edit">Edit answers</button><button class="btn" type="button" id="reset">Start again</button></div>
    </div>
  </div>
</section>
</main>
'''
    s += footer(P) + scripts(P)
    write("contact.html", s)

if __name__ == "__main__":
    home(); projects_index()
    for i in range(len(PROJECTS)): case(i)
    studio(); services(); journal(); contact()
