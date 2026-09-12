#!/usr/bin/env python3
"""Build every page of the portfolio from data/*.yaml and templates/*.j2.

    python3 tools/build.py              # render all pages
    python3 tools/build.py --pages      # skip the JSON asset generators
    python3 tools/build.py index study  # render only the named pages

Data files in data/ are merged into a single render context keyed by filename,
so data/experience.yaml is available to templates as `experience`.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

# Pages rendered from templates/<name>.html.j2 into <name>.html.
# 404.html is intentionally excluded: it is a standalone redirect stub with no site chrome.
PAGES = ["index", "experience", "projects", "certifications", "services", "study", "contact"]

# JSON assets consumed by scripts.js at runtime.
ASSET_GENERATORS = [
    "generate_badge_certifications.py",
]

MONTHS = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
    "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec",
}

# An "&" that is not already the start of a character entity.
BARE_AMPERSAND = re.compile(r"&(?!#?\w+;)")


def finalize(value):
    """Escape bare ampersands in rendered values so output is valid HTML.

    Markup values (pre-rendered JSON-LD) pass through untouched.
    """
    if isinstance(value, Markup) or not isinstance(value, str):
        return value
    return BARE_AMPERSAND.sub("&amp;", value)


def pretty_date(value: str) -> str:
    """Turn '2023-07' into 'Jul 2023'; pass through 'present' as 'Present'."""
    text = str(value)
    if text.lower() in {"present", "current"}:
        return "Present"
    if "-" in text:
        year, _, month = text.partition("-")
        return f"{MONTHS.get(month, month)} {year}"
    return text


def load_data() -> dict:
    """Merge every data/*.yaml into one context dict keyed by filename stem."""
    context = {}
    for path in sorted(DATA_DIR.glob("*.yaml")):
        with path.open(encoding="utf-8") as handle:
            context[path.stem] = yaml.safe_load(handle)
    missing = {"site", "experience"} - context.keys()
    if missing:
        sys.exit(f"Missing required data file(s): {', '.join(sorted(missing))}")
    return context


def build_json_ld(site: dict) -> str:
    identity, links, seo = site["identity"], site["links"], site["seo"]
    payload = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": identity["name"],
        "jobTitle": identity["job_title"],
        "description": " ".join(identity["description"].split()),
        "url": identity["base_url"],
        "sameAs": [links["linkedin"], links["github"], links["medium"]],
        "knowsAbout": seo["knows_about"],
        "alumniOf": {"@type": "EducationalOrganization", "name": seo["alumni_of"]},
        "worksFor": {"@type": "Organization", "name": seo["works_for"]},
        "email": identity["email"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": identity["location"]["city"],
            "addressRegion": identity["location"]["region"],
            "addressCountry": identity["location"]["country"],
        },
    }
    return json.dumps(payload, indent=8, ensure_ascii=False)


def make_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
        finalize=finalize,
    )
    env.filters["pretty_date"] = pretty_date
    return env


def render_pages(env: Environment, context: dict, only: list[str]) -> list[str]:
    written = []
    for key in only:
        template_path = TEMPLATE_DIR / f"{key}.html.j2"
        if not template_path.exists():
            print(f"  skip {key:<15} (no template)")
            continue
        html = env.get_template(f"{key}.html.j2").render(page_key=key, **context)
        (ROOT / f"{key}.html").write_text(html, encoding="utf-8")
        written.append(key)
        print(f"  ok   {key}.html")
    return written


def run_asset_generators() -> None:
    for script in ASSET_GENERATORS:
        path = ROOT / "tools" / script
        if not path.exists():
            print(f"  skip {script} (not found)")
            continue
        result = subprocess.run(
            [sys.executable, str(path)], capture_output=True, text=True, cwd=ROOT
        )
        status = "ok  " if result.returncode == 0 else "FAIL"
        print(f"  {status} {script}")
        if result.returncode != 0:
            print(result.stdout, result.stderr, sep="\n")
            sys.exit(f"Asset generator failed: {script}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", nargs="*", help="page keys to render (default: all)")
    parser.add_argument("--pages-only", action="store_true", help="skip JSON asset generators")
    args = parser.parse_args()

    context = load_data()
    context["json_ld"] = Markup(build_json_ld(context["site"]))
    context["build_time"] = datetime.now().isoformat(timespec="seconds")

    targets = args.pages or PAGES
    unknown = set(targets) - set(PAGES)
    if unknown:
        sys.exit(f"Unknown page(s): {', '.join(sorted(unknown))}")

    print(f"Loaded data: {', '.join(k for k in context if isinstance(context[k], (dict, list)))}")
    print("Rendering pages:")
    written = render_pages(make_environment(), context, targets)

    if not args.pages_only:
        print("Generating JSON assets:")
        run_asset_generators()

    print(f"\nDone. {len(written)} page(s) written.")


if __name__ == "__main__":
    main()
