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
| `Archive/Portfolio 2026 classic/` | Previous site (light, big-type list) kept for rollback | Backup only |
| `vercel.json` | Tells Vercel to serve `Portfolio 2026/` and holds the old-URL redirects | Keep |
| `.claude/launch.json` | Local preview server config for the Claude desktop app | Optional |

The old website (`Portfolio Website/`) is not in the repo. It lives in git history before commit `fa4562a`.

## Website (`Portfolio 2026/`)

Redesigned Nov 2026 for creative-agency applications (Melon Rouge, Phnom Penh). The design is "Option B · Corridor": dark, image-led. The previous site is kept in `Archive/Portfolio 2026 classic/` (not served) and in git history before this change.

- `index.html`: all CSS + JS inline. Home = huge cropped name "Layheng" + "designs it, then builds it", then 5 room panels in a sideways corridor (wheel or drag on desktop, stacked on phones). Content lives in arrays near the top of the script: `ROOMS`, `BUILDS`, `THEMES`, `TOOLS`, `XP`, `CASES`.
- Rooms (hash routes): `#built` (Metamorphosis, Rebrand Notes, Atelier Kambor, menu platform, 520 Staycation, EasySurvey, the Odile sample), `#design` (the 6 menu themes as design systems, cards link to the live demos), `#work` (product cases, each at `#work/<id>`; old `#smartnas` links redirect), `#toolkit`, `#experience` (CV timeline).
- `samples/metamorphosis/` (Kafka reading site, Fraunces, quotes from Gutenberg #5200 Wyllie translation; re-check quotes against gutenberg.org, it was down during the build), `samples/rebrand/` (Rebrand Notes: Burberry, Jaguar, Mastercard, Airbnb, sourced from Wikipedia; the 2023 Burberry knight file was rate-limited, add `Logo_Burberry_04.svg` later), `samples/interior/` (Atelier Kambor, fictional Phnom Penh studio, Unsplash photos, photographers not yet credited by name).
- `samples/odile/`: "Option A · Index" built as a portfolio for an invented designer, Odile Rask. Everything in it is fictional and every page carries a "Fictional sample" ribbon. Keep it labelled.
- `img/`: webp screenshots of the live sites (captured with Playwright). The Phsar Toch logo is blurred. Re-capture if the live sites change.
- `mocks.js`: SVG mock screens for the Product work cases (unchanged).
- Motion: one curve (`--io`) with 4 durations (.3/.5/.7/.9s) plus expo-out for reveals. Khmer/English hello loader (once per visit, hard-cut word swaps), curtain page transition in the room colour, word-mask title reveals, blend cursor with labels, magnetic buttons (desktop only). Reduced motion turns it all off.
- Fonts: Bricolage Grotesque + Instrument Serif (Google Fonts); theme display fonts load subset to the shop names; loader fonts self-hosted in `fonts/`.
- `Loem_Layheng_CV.pdf`: copy of the current CV. **Re-copy it from `CV/` whenever the CV changes.**
- Not shown on purpose: Learn Here, Everything (owner's choice), menu platform pricing and business plan.

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

- **Metamorphosis comic rebuild (paused):** owner wants `samples/metamorphosis/` redone as a full-screen illustrated vertical comic (manhwa style), German Expressionist woodcut look in hand-built SVG, Gregor's insect form shown, no instructional text. Work in progress saved in `Archive/wip-metamorphosis-comic/index.html` (figures still look like blobs, needs better human figures). The served sample is still the older type-only version. Copy the WIP back into `Portfolio 2026/samples/metamorphosis/` when finished and regenerate `img/sample-metamorphosis.webp`.
- **Motion phases:** phase 1 done (Lenis momentum scroll). Next: draggable infinite canvas (inertia), WebGL scroll effects (image warp on scroll).

- No `og:image` (link preview picture) yet.
- Not tested on Safari / iPhone or Firefox.
- Smart Axiata start month and Youding Product Owner end month are placeholders ("2026").
- Old misspelled address should redirect (308) to the new one (dashboard step).
- Leftover branches `new-portfolio-2026` and `update-dropship-store` on GitHub can be deleted.
