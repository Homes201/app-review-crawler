"""Common CSV contract for both stores."""

import csv
import re


FIELDS = (
    "store", "app_id", "review_id", "review", "score", "review_date",
    "app_version", "thumbs_up_count", "title",
)


def safe_name(value):
    return re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE).strip("._") or "app"


def save_reviews(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in FIELDS})
