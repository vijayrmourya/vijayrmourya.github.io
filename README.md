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

All content is managed through YAML files + Python automation:

### 📛 Badge Certifications (Professional Certs)

```bash
# Or edit YAML directly
vim tools/badge_certifications.yaml
python3 tools/generate_badge_certifications.py
```

**Add badge images:** Download from Credly/Coursera and save to `assets/badges/`

### 📜 Course Certificates (PDF-based)

```bash
# Or edit YAML directly
vim tools/certificates.yaml
python3 tools/generate_certificates_from_yaml.py
```

**Add PDFs:** Place PDFs in `assets/certificates/{Category}/`

### 💼 Work Experience

```bash
# Or edit YAML directly
vim tools/experience.yaml
python3 tools/generate_experience.py
```

### 📝 Medium Posts

```bash
python3 tools/fetch_medium.py
```

---

## 🤖 GitHub Actions Workflows

**Automated Workflows** for content management:

1. **Update Badge Certifications** - Triggered on push
   - Runs when: `badge_certifications.yaml`, generator script, or badges change
   - Generates: `assets/badge_certifications.json`
   - Manual trigger: Available

2. **Update Course Certificates** - Triggered on push
   - Runs when: `certificates.yaml`, generator script, or certificates change
   - Generates: `assets/certificates.json`
   - Manual trigger: Available

3. **Update Experience** - Triggered on push
   - Runs when: `experience.yaml` or generator script changes
   - Generates: `experience.html`
   - Manual trigger: Available

4. **Fetch Medium Posts** - Scheduled daily
   - Runs: Daily at 6:00 AM UTC
   - Fetches: Latest posts from Medium RSS feed
   - Updates: `assets/medium_posts.json`
   - Manual trigger: Available

**Benefits:**
- Path-specific triggers (efficient resource usage)
- Immediate updates on content changes
- Clean commit messages with item counts
- `[skip ci]` prevents workflow loops

---

## 📁 Project Structure

```
vijayrmourya.github.io/
├── *.html                        # Website pages
├── scripts.js                    # Dynamic content rendering
├── styles.css                    # Global styling
├── assets/
│   ├── badges/                   # Certification badge images
│   ├── certificates/             # PDF certificates by category
│   ├── badge_certifications.json # Auto-generated
│   ├── certificates.json         # Auto-generated
│   └── medium_posts.json         # Auto-generated
├── tools/
│   ├── badge_certifications.yaml # Badge certs config
│   ├── certificates.yaml         # Course certs config
│   ├── experience.yaml           # Experience config
│   ├── generate_*.py             # Generator scripts
│   └── fetch_medium.py           # Medium RSS fetcher
└── .github/workflows/            # CI/CD automation
```

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
