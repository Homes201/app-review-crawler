"""Collect a bounded batch of recent Google Play reviews."""

import argparse
from datetime import date
from pathlib import Path

from review_output import safe_name, save_reviews


def collect(app_id, limit=200, after=None, lang="ko", country="kr", fetch=None):
    if limit < 1:
        raise ValueError("limit must be positive")
    if fetch is None:
        from google_play_scraper import reviews as fetch
        from google_play_scraper import Sort
        newest = Sort.NEWEST
    else:
        newest = "NEWEST"

    rows, seen, token = [], set(), None
    while len(rows) < limit:
        batch, next_token = fetch(
            app_id, lang=lang, country=country, sort=newest,
            count=min(200, limit - len(rows)), continuation_token=token,
        )
        if not batch:
            break
        reached_cutoff = False
        previous_count = len(rows)
        for item in batch:
            reviewed_at = item.get("at")
            if after and reviewed_at and reviewed_at.date() < after:
                reached_cutoff = True
                break
            review_id = item.get("reviewId")
            if not review_id or review_id in seen:
                continue
            seen.add(review_id)
            rows.append({
                "store": "google_play", "app_id": app_id,
                "review_id": review_id, "review": item.get("content", ""),
                "score": item.get("score", ""), "review_date": reviewed_at,
                "app_version": item.get("appVersion", ""),
                "thumbs_up_count": item.get("thumbsUpCount", ""),
                "title": "",
            })
            if len(rows) == limit:
                break
        if reached_cutoff or len(rows) == previous_count or not next_token or next_token == token:
            break
        token = next_token
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app_id", help="Google Play package ID, e.g. com.example.app")
    parser.add_argument("--limit", type=int, default=200, help="Maximum reviews per run (default: 200)")
    parser.add_argument("--after", type=date.fromisoformat, help="Include reviews from YYYY-MM-DD")
    parser.add_argument("--lang", default="ko")
    parser.add_argument("--country", default="kr")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or Path(f"google_play_{safe_name(args.app_id)}_reviews.csv")
    rows = collect(args.app_id, args.limit, args.after, args.lang, args.country)
    save_reviews(output, rows)
    print(f"Saved {len(rows)} reviews to {output}")


if __name__ == "__main__":
    main()
