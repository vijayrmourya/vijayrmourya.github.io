# Portfolio tooling

The site is generated. **Edit YAML in `data/`, not the HTML files** — every
`*.html` in the repo root is build output and will be overwritten.

## Quick start

```bash
pip install PyYAML Jinja2

python3 tools/validate.py     # check data files
python3 tools/build.py        # render all pages + JSON assets
```

Common variations:

```bash
python3 tools/build.py --pages-only   # skip JSON asset generation
python3 tools/build.py index study    # render only these pages
```

## Layout

```
data/          YAML sources — the single source of truth
templates/     Jinja2 templates (base.html.j2 holds nav, header, footer, meta)
tools/         build.py, validate.py, and the badge/Medium helpers
assets/        images, logos, badges, and generated JSON
*.html         BUILD OUTPUT — gitignored, do not edit by hand
```

`404.html` and `ci-driven-portfolio/index.html` are the exceptions: both are
hand-maintained and committed.

## Where content lives

| File | Contains |
| --- | --- |
| `data/site.yaml` | Identity, tagline, nav, SEO, per-page title/description |
| `data/home.yaml` | Homepage hero, metrics, logo strip, "What I Do Best", "Currently Building" |
| `data/experience.yaml` | Roles, achievements, conferences, skills, career stats |
| `data/projects.yaml` | Projects page entries |
| `data/services.yaml` | Services page |
| `data/pages.yaml` | Contact and Writing/profiles pages |
| `data/badges.yaml` | Credential badges (drives `assets/badge_certifications.json`) |

Anything appearing on more than one page belongs in `site.yaml` or
`experience.yaml` so it is only written once. The homepage company cards, for
example, are derived from `experience.yaml` rather than duplicated.

## Adding content

**A new role** — add an entry to `experiences:` in `data/experience.yaml`.
Required: `id`, `company`, `location`, `role`, `start_date`, `end_date`,
`order`, `projects`, `tech_stack`. Add `summary` so the homepage card is
populated, and `short_name` if the homepage should show a shorter company name.

**A new project** — add to a group in `data/projects.yaml`. Use either
`body` (single paragraph) or all three of `problem` / `approach` /
`demonstrates`.

**A new badge** — `python3 tools/add_badge_certification.py`, then rebuild.

**A new page** — add a `templates/<key>.html.j2` extending `base.html.j2`, an
entry under `pages:` in `site.yaml`, and the key to `PAGES` in `tools/build.py`.

## Notes

- `404.html` is intentionally hand-maintained. It is a standalone redirect stub
  with no site chrome and is excluded from the build.
- Badges render client-side from JSON via `scripts.js`.
- `tools/fetch_medium.py` writes `assets/medium_posts.json` and runs on a daily
  cron, independent of the site build.
- Templates use `StrictUndefined`, so a missing key fails the build instead of
  silently rendering nothing. Use `page.get('key')` for optional values.
- Bare `&` in YAML is escaped to `&amp;` automatically at render time.

## CI

| Workflow | Trigger | Does |
| --- | --- | --- |
| `build.yml` | push to `data/`, `templates/`, `tools/`, `assets/`, `styles.css`, `scripts.js` | validate → build → html-validate → link check → deploy to Pages |
| `fetch_medium.yml` | daily cron 06:00 UTC | refresh `assets/medium_posts.json` and commit it |

Both share the `portfolio-pipeline` concurrency group, so they queue rather than
running at the same time. The Medium commit deliberately omits `[skip ci]` so it
triggers a rebuild and the new posts actually deploy.

**Generated HTML is not committed.** `build.yml` renders the site and publishes it
as a Pages artifact, so GitHub Pages must be set to deploy from **GitHub Actions**
(Settings → Pages → Source), not from a branch.
