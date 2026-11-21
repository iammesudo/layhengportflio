# Loem Layheng: CV + Portfolio

Personal CV and portfolio website. Owner: Loem Layheng, Product Owner (Digital Touchpoint Officer at Smart Axiata, SmartNas digital channels).

This repo (`iammesudo/layhengportflio`, public) is the whole project. Clone it, work in a branch, push, and Vercel builds a preview.

## Layout

| Path | What it is | Status |
|---|---|---|
| `CV/loem_layheng_cv_2026.html` + `.pdf` | **Current CV.** Classic LaTeX style (Computer Modern font), one column, 2 A4 pages | Live |
| `CV/loem_layheng_cv_2026_v1-premium.*` | Earlier "premium" CV design | Backup only |
| `CV/loem_layheng_cv.html` | Old CV (Youding era) | Archive |
| `Portfolio 2026/` | **Current website** (the only folder Vercel serves) | Live |
| `vercel.json` | Tells Vercel to serve `Portfolio 2026/` and holds the old-URL redirects | Keep |
| `.claude/launch.json` | Local preview server config for the Claude desktop app | Optional |

The old website (`Portfolio Website/`) is not in the repo. It lives in git history before commit `fa4562a`.

## Website (`Portfolio 2026/`)

- `index.html`: all CSS + JS inline. Project content (text, "What I did", results) is the `projects` array near the top of the script. Wrap words in `*stars*` in `intro` to get the highlighter sweep.
- `mocks.js`: the mock screens as SVG strings. SmartNas uses telco-style screens (`telHome`, `telInternet`, `telProfile`); Dropship Store uses a sample shop "LUMA" (`shopPhone`, `shopWeb`). To use a real screenshot, swap a mock for `<img>`.
- Projects (in order): SmartNas, EZorder, AI Chatbot, Dropship Store (Shopify, Facebook/Instagram/TikTok ads, international buyers, 2023 to 2024), Poster AI. Bulk QR Tool was removed (it was a vibe-coded tool).
- `fonts/`: self-hosted loader fonts (MiSans Khmer, MiSans Latin, Zen Kaku Gothic New + IBM Plex Sans KR subsets). Main font is Inter from Google Fonts.
- `Loem_Layheng_CV.pdf`: copy of the current CV. **Re-copy it from `CV/` whenever the CV changes.**
- Features: Khmer + English hello loader (once per visit), project list with hover previews, project pages with title fly-in (View Transitions), About/Contact panel, 3 colour moods (Paper default, Forest, Cobalt). No intro text above the project list (user removed it).
- Mock parallax runs only on desktop (hover + ≥1100px). On phones/tablets it is off because it made the mock shadows flicker while scrolling.

### Run locally
`python -m http.server 5173 --directory "Portfolio 2026"` (also in `.claude/launch.json` as `portfolio`). Open http://localhost:5173.

### Rebuild the CV PDF
The CV is `CV/loem_layheng_cv_2026.html`, printed with headless Chrome:

`chrome --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=CV/loem_layheng_cv_2026.pdf file:///<full path>/CV/loem_layheng_cv_2026.html`

Then check it is still **2 pages, A4**, and copy it to `Portfolio 2026/Loem_Layheng_CV.pdf`. The Computer Modern font loads from the jsDelivr CDN (`computer-modern@0.1.2`), so printing needs internet; without it the CV falls back to Georgia and the page count can change.

### Deploy
- Live: **https://layheng-portfolio.vercel.app** (added 2026-11-15). The old misspelled https://layhengportflio.vercel.app still serves the same site; set it to redirect (308) to the new address in Vercel → Settings → Domains. The Vercel project and GitHub repo keep the old spelling `layhengportflio` (only visible to the owner).
- Vercel auto-deploys from this repo, branch `main`. Every other branch gets a private preview URL.
- Flow: commit to a branch → push → open the Vercel preview and test it → merge to `main` (fast-forward) → verify the live site. Preview URLs need a Vercel login (or a share link).
- `vercel.json` redirects old page URLs (about.html, project-*.html, old CV filename) to the new site. Keep it. `/project-cstool.html` redirects to `/` (the QR project was removed).
- Rollback: Vercel dashboard → Deployments → Instant Rollback.
- The Vercel connector used in earlier sessions is read-only (domain/settings changes return 403). Do those in the Vercel dashboard.

## Rules for content

- **No em dashes (—)** anywhere in CV or site. Use commas, colons, full stops or "·".
- **No AI-sounding slogans** (the user rejected "Show it, don't just write it"). Plain, factual wording.
- **No invented numbers.** Results are written in words. (The only real metric, "up to 75% faster" setup from the Bulk QR tool, is in the CV but no longer on the site.)
- **Mock screens must not show real data:** no real phone numbers (use `0XX XXX XXX`), no real logos, mascot or photos. Each mock frame carries an italic confidentiality note.
- Say "vibe coding" plainly, without explaining it in brackets.
- CV title under the name is just "Product Owner".

## Design taste (from the owner)

- Judges against real award-style sites; wants crafted motion, not "generic text motion". Liked: minimal big-type project list (adriangnzl.es), Dennis Snellenberg's loader, Cuberto's text reveals. Rejected: a card-based "premium" template ("I hate it").
- Wants every section interactive, a unique text highlight, per-project colours instead of one fixed accent.
- Prefers real-looking mock-ups (laid out like the real app) with an italic confidentiality note over abstract placeholders.
- Before visual work: study the reference sites, say what was borrowed, and test motion in a real browser (desktop, phone, tablet, keyboard) before showing it. Run a QA pass before each deploy.

## Open items

- No `og:image` (link preview picture) yet.
- Not tested on Safari / iPhone or Firefox.
- Smart Axiata start month and Youding Product Owner end month are placeholders ("2026").
- Old misspelled address should redirect (308) to the new one (dashboard step).
- Leftover branches `new-portfolio-2026` and `update-dropship-store` on GitHub can be deleted.
