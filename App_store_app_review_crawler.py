"""Collect a bounded batch of recent public App Store reviews."""

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from review_output import safe_name, save_reviews


def fetch_json(url):
    request = Request(url, headers={"User-Agent": "app-review-crawler/1.0"})
    with urlopen(request, timeout=15) as response:
        return json.load(response)


def lookup_app_id(name, fetch=fetch_json):
    url = "https://itunes.apple.com/search?" + urlencode({
        "term": name, "country": "kr", "entity": "software", "limit": 20,
    })
    matches = [item for item in fetch(url).get("results", [])
               if item.get("trackName", "").casefold() == name.casefold()]
    if len(matches) != 1:
        raise ValueError("앱 이름을 하나로 특정할 수 없습니다. App Store의 숫자 --app-id를 입력하세요.")
    return int(matches[0]["trackId"])


def collect(app_name=None, app_id=None, limit=200, after=None, fetch=fetch_json):
    if not app_name and not app_id:
        raise ValueError("app_name or app_id is required")
    if limit < 1:
        raise ValueError("limit must be positive")
    app_id = app_id or lookup_app_id(app_name, fetch)
    rows, seen = [], set()
    for page in range(1, 11):  # The public RSS feed exposes at most ten pages.
        url = f"https://itunes.apple.com/kr/rss/customerreviews/id={app_id}/page={page}/sortBy=mostRecent/json"
        entries = fetch(url).get("feed", {}).get("entry", [])
        if not entries:
            break
        reached_cutoff = False
        for item in entries:
            if "im:rating" not in item:
                continue
            reviewed_at = datetime.fromisoformat(item["updated"]["label"])
            if after and reviewed_at.date() < after:
                reached_cutoff = True
                break
            review_id = item["id"]["label"]
            if review_id in seen:
                continue
            seen.add(review_id)
            rows.append({
                "store": "app_store", "app_id": app_id,
                "review_id": review_id, "review": item.get("content", {}).get("label", ""),
                "score": item["im:rating"]["label"], "review_date": reviewed_at,
                "app_version": item.get("im:version", {}).get("label", ""),
                "thumbs_up_count": item.get("im:voteSum", {}).get("label", ""),
                "title": item.get("title", {}).get("label", ""),
            })
            if len(rows) >= limit:
                return rows
        if reached_cutoff:
            break
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-name", help="Exact App Store name")
    parser.add_argument("--app-id", type=int, help="Numeric App Store ID (recommended)")
    parser.add_argument("--limit", type=int, default=200, help="Maximum reviews per run (default: 200)")
    parser.add_argument("--after", type=date.fromisoformat, help="Include reviews from YYYY-MM-DD")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.app_name and not args.app_id:
        parser.error("--app-name or --app-id is required")
    output = args.output or Path(f"app_store_{safe_name(str(args.app_id or args.app_name))}_reviews.csv")
    rows = collect(args.app_name, args.app_id, args.limit, args.after)
    save_reviews(output, rows)
    print(f"Saved {len(rows)} reviews to {output}")


if __name__ == "__main__":
    main()
