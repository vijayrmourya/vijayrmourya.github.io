#!/usr/bin/env python3
"""Validate data/*.yaml before the site is built.

    python3 tools/validate.py

Checks structure, required keys, and cross-references between files. Exits
non-zero on error so CI can block a broken build.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

# file stem -> required top-level keys
REQUIRED_KEYS = {
    "site": ["identity", "links", "seo", "nav", "pages", "footer"],
    "experience": ["experiences", "achievements", "conferences", "skills", "career_stats", "metadata"],
    "home": ["hero", "impact_metrics", "tech_logos", "key_achievements", "what_i_do_best"],
    "projects": ["hero", "groups"],
    "services": ["hero", "core_services", "how_i_work", "engagement_models", "cta"],
    "pages": ["contact", "study"],
    "badges": ["certifications"],
}

REQUIRED_JOB_FIELDS = ["id", "company", "location", "role", "start_date", "end_date", "order", "projects", "tech_stack"]


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def load(report: Report) -> dict:
    data = {}
    for path in sorted(DATA_DIR.glob("*.yaml")):
        try:
            data[path.stem] = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            report.error(f"{path.name}: invalid YAML - {exc}")
    return data


def check_required_keys(data: dict, report: Report) -> None:
    for stem, keys in REQUIRED_KEYS.items():
        if stem not in data:
            report.error(f"missing data file: data/{stem}.yaml")
            continue
        for key in keys:
            if key not in (data[stem] or {}):
                report.error(f"data/{stem}.yaml: missing top-level key '{key}'")


def check_experience(data: dict, report: Report) -> None:
    experience = data.get("experience") or {}
    jobs = experience.get("experiences") or []
    seen_ids, seen_orders = set(), set()

    for job in jobs:
        label = job.get("id", "<no id>")
        for field in REQUIRED_JOB_FIELDS:
            if field not in job:
                report.error(f"experience '{label}': missing field '{field}'")

        if job.get("id") in seen_ids:
            report.error(f"experience: duplicate id '{job.get('id')}'")
        seen_ids.add(job.get("id"))

        if job.get("order") in seen_orders:
            report.error(f"experience '{label}': duplicate order {job.get('order')}")
        seen_orders.add(job.get("order"))

        for project in job.get("projects") or []:
            if not project.get("title"):
                report.error(f"experience '{label}': a project block has no title")
            if not project.get("highlights"):
                report.error(f"experience '{label}': project '{project.get('title')}' has no highlights")

        if not job.get("summary"):
            report.warn(f"experience '{label}': no 'summary' - homepage card will be blank")


def check_nav_and_pages(data: dict, report: Report) -> None:
    site = data.get("site") or {}
    nav_keys = {item.get("key") for item in site.get("nav") or []}
    page_keys = set((site.get("pages") or {}).keys())

    for key in nav_keys:
        if key not in page_keys:
            report.error(f"site.yaml: nav item '{key}' has no entry under pages:")
        target = ROOT / f"{key}.html"
        template = TEMPLATE_DIR / f"{key}.html.j2"
        if not template.exists() and not target.exists():
            report.error(f"site.yaml: nav item '{key}' has neither a template nor an HTML file")

    for key, page in (site.get("pages") or {}).items():
        for field in ("title", "description"):
            if not (page or {}).get(field):
                report.error(f"site.yaml: pages.{key} missing '{field}'")


def check_assets(data: dict, report: Report) -> None:
    for tool in (data.get("home") or {}).get("tech_logos") or []:
        logo = tool.get("logo")
        if not logo:
            report.error(f"home.yaml: tech logo '{tool.get('name')}' has no 'logo'")
            continue
        path = ROOT / "assets" / "logos" / logo
        if not path.exists():
            report.error(f"home.yaml: missing logo file assets/logos/{logo}")
        elif "<svg" not in path.read_text(encoding="utf-8", errors="ignore")[:400]:
            report.error(f"home.yaml: assets/logos/{logo} is not a valid SVG")

    avatar = ((data.get("site") or {}).get("identity") or {}).get("avatar")
    if avatar and not (ROOT / avatar).exists():
        report.error(f"site.yaml: avatar not found at {avatar}")


def check_projects(data: dict, report: Report) -> None:
    for group in (data.get("projects") or {}).get("groups") or []:
        for project in group.get("projects") or []:
            name = project.get("name", "<unnamed>")
            if not project.get("url"):
                report.error(f"projects.yaml: '{name}' has no url")
            has_structured = all(project.get(f) for f in ("problem", "approach", "demonstrates"))
            if not project.get("body") and not has_structured:
                report.error(f"projects.yaml: '{name}' needs either 'body' or problem/approach/demonstrates")
            if not project.get("tags"):
                report.warn(f"projects.yaml: '{name}' has no tags")


def main() -> None:
    report = Report()
    data = load(report)

    if not report.errors:
        check_required_keys(data, report)
        check_experience(data, report)
        check_nav_and_pages(data, report)
        check_assets(data, report)
        check_projects(data, report)

    for warning in report.warnings:
        print(f"  warn  {warning}")
    for error in report.errors:
        print(f"  ERROR {error}")

    if report.errors:
        sys.exit(f"\nValidation failed: {len(report.errors)} error(s).")
    print(f"Validation passed ({len(data)} data files, {len(report.warnings)} warning(s)).")


if __name__ == "__main__":
    main()
