# Loem Layheng: CV + Portfolio

Personal CV and portfolio website. Owner: Loem Layheng, presented as **Creative & product designer** (job title: Digital Touchpoint Officer / Product Owner for SmartNas at Smart Axiata). Built in Nov 2026 to apply to creative agencies (Melon Rouge, Phnom Penh).

This repo (`iammesudo/layhengportflio`, public) is the whole project. Clone it, work in a branch, push, and Vercel builds a preview.

## Layout

| Path | What it is | Status |
|---|---|---|
| `CV/loem_layheng_cv_2026.html` + `.pdf` | **Current CV.** Classic LaTeX style (Computer Modern font), one column, 2 A4 pages | Live |
| `CV/loem_layheng_cv_2026_v1-premium.*` | Earlier "premium" CV design | Backup only |
| `CV/loem_layheng_cv.html` | Old CV (Youding era) | Archive |
| `Portfolio 2026/` | **Current website** (the only folder Vercel serves) | Live |
| `Archive/Portfolio 2026 classic/` | Previous site (light, big-type list), kept for rollback | Backup only |
| `Archive/metamorphosis-gen/` | Generator for the Metamorphosis comic (build.py, template.html, stage.js) | Source |
| `Archive/kambor-gen/` | Generator for the Atelier Kambor site (build.py + QA scripts; `sizes.json` missing, so re-running needs care) | Source |
| `vercel.json` | Serves `Portfolio 2026/`, old-URL redirects, security headers (CSP etc.) | Keep |
| `.claude/launch.json` | Local preview server config for the Claude desktop app | Optional |

The old website (`Portfolio Website/`) is not in the repo. It lives in git history before commit `fa4562a`.

## Website (`Portfolio 2026/`)

Design "Option B · Corridor": dark, image-led, Bricolage Grotesque + Instrument Serif, per-project colours.

### Structure (`index.html`, all CSS + JS inline, hash routing)
- **Home:** huge "Layheng" + "designs it, then builds it", then a sideways corridor of 6 room panels (wheel/drag on desktop, stacked on phones) ending in a "Get in touch" card. Home remembers its scroll position.
- **Panels:** 01 The Metamorphosis → `#p/metamorphosis`, 02 Atelier Kambor → `#p/kambor`, 03 Case studies → `#cases`, 04 Web projects → `#web`, 05 Product work → `#work`, 06 Experience & tools → `#experience`. Every panel opens a page inside the portfolio.
- **Project pages `#p/<slug>`:** one template for all 7 projects in the `PROJECTS` array (Metamorphosis, Kambor, Rebrand Notes, QR menu platform with its 6-theme drag canvas, 520 Staycation, EasySurvey, Odile). Hero, summary, what I did, live preview in a browser frame (iframe for same-origin samples, screenshot + "Open live site ↗" for external ones), prev/next, All work.
- **Product cases `#work/<id>`:** SmartNas, EZorder, AI Chatbot, Dropship Store, Poster AI, with Problem, Journey diagram, What I did, Result, mock screens (`mocks.js`).
- **Header:** Work (full-screen index dialog of all projects), About (`#about`), Resume (PDF), Contact (`#contact`).
- **About:** yellow opener with a rounded portrait card (`img/me.webp`, transparent cut-out on amber; the source photo is only 360px, so keep it small), what I do, Now facts. **Contact:** Telegram, email with copy button, resume, Phnom Penh local time.
- Data arrays near the top of the script: `ROOMS`, `PROJECTS`, `STUDIES` (add new case studies here), `BUILDS`, `THEMES`, `TOOLS`, `XP`, `CASES`.
- Old hashes (`#built`, `#design`, `#toolkit`, `#smartnas`, etc.) redirect.

### Sample sites (`samples/`, all `noindex`, all clearly labelled)
- `metamorphosis/`: Kafka's novella as a pinned, full-screen woodcut-style comic. Scenes change in place on scroll (ink bleed, wipes, zooms). First 2 scenes inline, the rest lazy-loaded from `scenes/`. Quotes from Gutenberg #5200 (Wyllie translation). Edit via `Archive/metamorphosis-gen/`.
- `interior/`: **Atelier Kambor**, a fictional Phnom Penh interior studio. 12 pages: home, projects index with filters, 6 project pages (House in Toul Kork keeps the room-by-room walk-through and floor plan), studio, services (stages, fees in words, FAQ), journal, contact (Telegram first, enquiry form that sends nothing). Shared `assets/kambor.css/js`. Unsplash photos with srcset.
- `rebrand/`: **Rebrand Notes**, a short independent study of Burberry, Jaguar, Mastercard and Airbnb with before/after sliders; all sources in one section at the end. Real logos, labelled "Not affiliated".
- `odile/`: a full portfolio for an invented designer, Odile Rask. Fictional ribbon on every page.
- "Back to portfolio" in every sample returns to its `#p/<slug>` page (history.back() when coming from the portfolio).

### Assets and tech
- `img/`: webp screenshots (Playwright captures; Phsar Toch logo blurred), `img/thumb/` (720px room thumbnails, `cv.webp`), `img/og.jpg` (1200x630 link preview; re-capture if home changes).
- `vendor/lenis.min.js`: self-hosted Lenis 1.1.13 (no third-party scripts).
- Motion: one curve (`--io`), 4 durations, expo-out reveals. Khmer/English hello loader (once per visit), curtain transitions in the room colour, word-mask titles, blend cursor with labels, magnetic buttons, Lenis momentum scroll, drag canvas (menu themes), WebGL scroll warp on screenshots. Desktop / fine pointer only; reduced motion turns it all off. rAF loops stop when idle.
- Works without JS (static room links, loader hidden). `robots.txt`, `sitemap.xml`, canonical.
- `Loem_Layheng_CV.pdf`: copy of the current CV. **Re-copy it from `CV/` whenever the CV changes.**
- Not shown on purpose: Learn Here, Everything (owner's choice), menu platform pricing and business plan.

### Run locally
`python -m http.server 5173 --directory "Portfolio 2026"` (also in `.claude/launch.json` as `portfolio`). Open http://localhost:5173.

### Rebuild the CV PDF
The CV is `CV/loem_layheng_cv_2026.html`. Print with headless Chrome (or Playwright `page.pdf({preferCSSPageSize: true})`):

`chrome --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=CV/loem_layheng_cv_2026.pdf file:///<full path>/CV/loem_layheng_cv_2026.html`

Then check it is still **2 pages, A4**, and copy it to `Portfolio 2026/Loem_Layheng_CV.pdf`. The Computer Modern font loads from jsDelivr (`computer-modern@0.1.2`), so printing needs internet.

### Deploy
- Live: **https://layheng-portfolio.vercel.app**. The old misspelled https://layhengportflio.vercel.app still serves the same site; set it to redirect (308) in Vercel → Settings → Domains.
- Vercel auto-deploys branch `main`; other branches get private preview URLs (need a Vercel login).
- Flow: commit to a branch → push → test the preview → fast-forward `main` → verify the live site.
- `vercel.json` holds redirects and headers (CSP allows self, Google Fonts, data/blob images; adding any new external host needs a CSP update).
- Rollback: Vercel dashboard → Deployments → Instant Rollback, or restore `Archive/Portfolio 2026 classic/`.
- The Vercel connector is read-only for settings (domain changes return 403). Do those in the dashboard.

## Rules for content

- **No em dashes (—)** anywhere in CV or site. Use commas, colons, full stops or "·".
- **No instructional or meta text** on pages ("scroll", "click", "tap", "hover", "this site does…"). Pages say what things are, not how to use them.
- **No AI-sounding slogans.** Plain, factual wording.
- **No invented facts or numbers.** Results are written in words. Fictional things (Odile, Kambor) must stay clearly labelled.
- **Mock screens must not show real data:** no real phone numbers (use `0XX XXX XXX`), no real logos or photos. Each mock frame carries an italic confidentiality note.
- Say "vibe coding" plainly, without explaining it.
- Title everywhere: **Creative & product designer** (CV: "Creative & Product Designer"). Call the CV **"Resume"** on the site. The CV has Selected Projects (520 Staycation as a client project, Metamorphosis, Atelier Kambor); references are "Available on request".

## Design taste (from the owner)

- Judges against award-style sites; wants crafted motion, not generic text motion. Liked: big-type project lists (adriangnzl.es), Dennis Snellenberg's loader, Cuberto's reveals, Lenis / inertia / drag canvas / WebGL scroll. Rejected: card-based "premium" templates, long one-page scrolls for stories (wants pinned, in-place scrollytelling), large photos of himself.
- Wants every section interactive, per-project colours, real-looking mock-ups with a confidentiality note.
- Wants navigation that keeps visitors inside the portfolio, and consistent behaviour across panels.
- Prefers short agent output: just do the work and report briefly.
- Before visual work: study references, test in a real browser (desktop, phone, tablet, keyboard), and run a QA pass before each deploy.

## Open items

- **Next:** more case studies (successful packaging, marketing campaigns, more visual) as new `STUDIES` / `PROJECTS` entries.
- Case pages: "Result" items read as claims; replace with things actually seen. Open the first "What I did" item on mobile.
- iPad home: empty space under the corridor; iPad scroll restore not fully tested.
- EasySurvey screenshot shows the owner's email and an em dash from the live page; re-crop to the photo board.
- Check: the Kambor home hero shows a carved wall panel that may be real artwork; project colours for 520 / EasySurvey / Odile and the new Metamorphosis / Kambor summaries were picked by an agent.
- Metamorphosis: re-check the 31 quotes against https://www.gutenberg.org/cache/epub/5200/pg5200.txt (was down; checked against the GITenberg copy). Ribbon text could be 14px.
- Rebrand Notes: add the 2023 Burberry knight (`Logo_Burberry_04.svg`, was rate-limited). Kambor: credit Unsplash photographers by name.
- Perf (Low): WebGL loop could pause when idle; `img/thumb/m-*.webp` to 320px; `robots.txt` Disallow /samples/ hides their noindex (use `X-Robots-Tag` instead); Metamorphosis no-JS placeholders; CSP still needs `'unsafe-inline'` for inline scripts.
- Not tested on real Safari / iPhone or Firefox.
- Smart Axiata start month and Youding Product Owner end month are placeholders ("2026").
- Old misspelled address should redirect (308) to the new one (dashboard step).
- Leftover branches `new-portfolio-2026` and `update-dropship-store` on GitHub can be deleted.
