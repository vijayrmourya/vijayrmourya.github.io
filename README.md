# Vijay Mourya - Portfolio Website

[![Fetch Medium Posts](https://github.com/vijayrmourya/ci-driven-portfolio/actions/workflows/fetch_medium.yml/badge.svg)](https://github.com/vijayrmourya/ci-driven-portfolio/actions/workflows/fetch_medium.yml)
[![Update Experience](https://github.com/vijayrmourya/ci-driven-portfolio/actions/workflows/update_experience.yml/badge.svg)](https://github.com/vijayrmourya/ci-driven-portfolio/actions/workflows/update_experience.yml)
[![Update Certificates](https://github.com/vijayrmourya/ci-driven-portfolio/actions/workflows/update_certificates.yml/badge.svg)](https://github.com/vijayrmourya/ci-driven-portfolio/actions/workflows/update_certificates.yml)

A CI-Driven Personal Portfolio Platform that automates content generation and builds a professional static website using Python scripts and GitHub Actions. The site pulls structured data (certifications, experience, blog posts) from YAML and external sources, automates updates via workflows, and is hosted on GitHub Pages. This repository exemplifies automation, infrastructure-as-code thinking, and architectural delight in a real personal platform.

**Live Site:** [vijayrmourya.github.io](https://vijayrmourya.github.io)

---

## Features

- 📚 **Dynamic Medium Posts** - Automatically fetched from Medium RSS feed
- 🎓 **Course Certificates** - Auto-generated from PDF files
- 🎨 **Modern UI** - Dark theme with responsive design
- ⚡ **Static Site** - Fast loading with client-side rendering

---

## Tech Stack

- HTML, CSS, JavaScript (Vanilla)
- Python 3.11 (automation scripts)
- GitHub Actions (CI/CD)
- GitHub Pages (hosting)

---

## Local Development

```bash
# Clone repository
git clone https://github.com/vijayrmourya/vijayrmourya.github.io.git
cd vijayrmourya.github.io

# Start local server
python3 -m http.server 8000

# Open browser at http://localhost:8000
```

---

## 🛠️ Automation Tools

Every page is generated from YAML in `data/` through Jinja2 templates in
`templates/`. **The `*.html` files in the repo root are build output — don't edit
them by hand.**

### One command per workflow

```bash
make site      # validate + rebuild every page   (same steps as build.yml)
make medium    # refresh Medium posts            (mirrors fetch_medium.yml)
make quality   # html-validate + link check      (build.yml runs this too)

make serve     # build, then preview locally
make check     # everything CI runs, before you push
make help      # list all targets
```

The workflows call the underlying scripts directly, so CI never depends on make.

### 💼 Work Experience

```bash
vim data/experience.yaml
make site
```

### 📛 Badge Certifications

```bash
vim data/badges.yaml        # or: python3 tools/add_badge_certification.py
make site
```

**Add badge images:** download from Credly/Coursera into `assets/badges/`

### 🏠 Homepage, projects, services, contact

```bash
vim data/home.yaml          # hero, metrics, logo strip, "Currently Building"
vim data/projects.yaml      # projects page
vim data/services.yaml      # services page
vim data/pages.yaml         # contact + writing pages
vim data/site.yaml          # identity, nav, SEO, per-page titles
make site
```

See `tools/README.md` for the full schema reference.

---

## 🤖 GitHub Actions Workflows

1. **Build & deploy site** (`build.yml`) — on push
   - Runs when `data/`, `templates/`, `tools/`, `assets/`, `styles.css` or `scripts.js` change
   - Validates data → builds pages → `html-validate` → link check → deploys to GitHub Pages
   - Manual trigger: available

2. **Fetch Medium Posts** (`fetch_medium.yml`) — daily at 06:00 UTC
   - Refreshes `assets/medium_posts.json` and commits it, which triggers a rebuild
   - Manual trigger: available

Both workflows share the `portfolio-pipeline` concurrency group, so they **queue
instead of running in parallel**.

> **Pages deployment:** generated HTML is not committed. The site is published
> from a CI artifact, so Settings → Pages → Source must be set to
> **GitHub Actions**.

**Benefits:**
- Repository holds only source — no generated files to review in diffs
- Data validated before build, so a typo fails fast instead of shipping
- Quality gates run before deploy, not after
- Serialised pipeline avoids racing deploys

---

## 📁 Project Structure

```
vijayrmourya.github.io/
├── Makefile                      # one target per workflow
├── 404.html                      # hand-maintained redirect stub (committed)
├── scripts.js                    # dynamic content rendering
├── styles.css                    # global styling
├── data/                         # single source of truth
│   ├── site.yaml                 # identity, nav, SEO, page metadata
│   ├── home.yaml                 # homepage sections
│   ├── experience.yaml           # roles, achievements, skills, stats
│   ├── projects.yaml             # projects page
│   ├── services.yaml             # services page
│   ├── pages.yaml                # contact + writing pages
│   └── badges.yaml               # credential badges
├── templates/
│   ├── base.html.j2              # nav, header, footer, meta (defined once)
│   └── <page>.html.j2            # one per page
├── assets/
│   ├── badges/                   # certification badge images
│   ├── logos/                    # technology logos
│   └── medium_posts.json         # refreshed daily by CI
├── tools/
│   ├── build.py                  # renders every page
│   ├── validate.py               # data validation
│   ├── fetch_medium.py           # Medium RSS fetcher
│   └── README.md                 # schema reference
└── .github/workflows/            # CI/CD automation
```

Generated pages (`index.html`, `experience.html`, and the rest) are gitignored —
run `make site` to produce them locally.

---

## ⚙️ Configuration

**Medium Username:** Edit `.github/workflows/fetch_medium.yml`
```yaml
env:
  MEDIUM_USERNAME: vjmourya
  MAX_POSTS: '6'
```

**Certification Categories:** Edit YAML files in `tools/`

---

## Contributing

As this is a personal portfolio website, I am not currently accepting pull requests for content or design changes. However, feel free to fork the repository for inspiration or report any technical bugs in the issues tracker.

## License

© 2024-2025 Vijay Mourya. **All Rights Reserved.**

This project is personal and is not licensed for public use, redistribution, or modification. The source code is provided here as a showcase of my technical work and automation architecture. See the [LICENSE](LICENSE) file for more details.

---

**Built with HTML, CSS, JavaScript, Python & GitHub Actions**
