#!/usr/bin/env python3
"""Fetch the latest Medium posts into assets/medium_posts.json.

    python3 tools/fetch_medium.py [output_path]

Environment:
    MEDIUM_USERNAME   Medium handle without the '@' (default: vjmourya)
    MAX_POSTS         number of posts to keep (default: 6)

Exits non-zero on a failed fetch and leaves any existing file untouched, so a
transient Medium outage can never overwrite good data with an empty list.
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from html import unescape
from pathlib import Path

import feedparser

RETRIES = 3
RETRY_DELAY = 5
# Medium returns 403 to some default clients, so identify as a normal browser.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

TAG_RE = re.compile(r"<.*?>")
SCRIPT_STYLE_RE = re.compile(r"<script.*?>.*?</script>|<style.*?>.*?</style>", re.DOTALL)


def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    text = SCRIPT_STYLE_RE.sub("", raw_html)
    text = TAG_RE.sub(" ", text)
    return unescape(" ".join(text.split()))


def excerpt_from_content(entry, length: int = 160) -> str:
    if entry.get("summary"):
        text = clean_html(entry["summary"])
    elif entry.get("content"):
        text = clean_html(entry["content"][0].value)
    else:
        text = ""
    if len(text) > length:
        return text[:length].rsplit(" ", 1)[0] + "..."
    return text


def fetch_feed(feed_url: str):
    """Return a parsed feed with entries, or None if every attempt failed."""
    for attempt in range(1, RETRIES + 1):
        parsed = feedparser.parse(feed_url, agent=USER_AGENT)
        status = parsed.get("status")
        if parsed.entries:
            print(f"Fetched {len(parsed.entries)} entries (HTTP {status})")
            return parsed

        reason = f"HTTP {status}" if status else "no response"
        if parsed.bozo:
            reason += f", parse error: {parsed.get('bozo_exception')!r}"
        print(f"Attempt {attempt}/{RETRIES} returned no entries ({reason})")

        if attempt < RETRIES:
            time.sleep(RETRY_DELAY)
    return None


def main(output_path: str) -> None:
    username = os.getenv("MEDIUM_USERNAME", "vjmourya").strip()
    max_posts = int(os.getenv("MAX_POSTS", "6"))
    feed_url = f"https://medium.com/feed/@{username}"

    print(f"Fetching {feed_url}")
    parsed = fetch_feed(feed_url)

    if parsed is None:
        target = Path(output_path)
        if target.exists():
            sys.exit(
                f"Feed returned no entries after {RETRIES} attempts. "
                f"Keeping the existing {target.name} rather than emptying it."
            )
        sys.exit(f"Feed returned no entries after {RETRIES} attempts and no {target.name} exists.")

    posts = []
    for entry in parsed.entries[:max_posts]:
        published = entry.get("published_parsed")
        posts.append({
            "title": entry.get("title", "Untitled"),
            "link": entry.get("link"),
            "date": datetime(*published[:6]).isoformat() if published else None,
            "excerpt": excerpt_from_content(entry),
        })

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(
            {"source": f"https://medium.com/@{username}", "posts": posts},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(posts)} post(s) to {target}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/medium_posts.json")
