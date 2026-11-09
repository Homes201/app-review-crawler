import csv
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from App_store_app_review_crawler import collect as collect_apple
from Google_play_app_review_crawler import collect as collect_google
from review_output import FIELDS, save_reviews


class ReviewCollectionTests(unittest.TestCase):
    def test_google_paginates_deduplicates_and_stops_at_date(self):
        calls = []
        pages = [
            ([{"reviewId": "a", "at": datetime(2026, 11, 9), "content": "A", "score": 4}], "next"),
            ([{"reviewId": "a", "at": datetime(2026, 11, 9)},
              {"reviewId": "b", "at": datetime(2026, 10, 1)}], None),
        ]

        def fetch(*args, **kwargs):
            calls.append(kwargs)
            return pages.pop(0)

        rows = collect_google("com.example.app", limit=5, after=date(2026, 11, 1), fetch=fetch)
        self.assertEqual([row["review_id"] for row in rows], ["a"])
        self.assertEqual(calls[1]["continuation_token"], "next")

    def test_app_store_has_same_csv_schema_and_limit(self):
        review = {"id": {"label": "r1"}, "updated": {"label": "2026-11-09T12:00:00+09:00"},
                  "im:rating": {"label": "5"}, "content": {"label": "좋아요"},
                  "title": {"label": "제목"}}
        rows = collect_apple(app_id=123, limit=2, fetch=lambda url: {"feed": {"entry": [review, review]}})
        self.assertEqual(len(rows), 1)
        self.assertEqual(tuple(rows[0]), FIELDS)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "reviews.csv"
            save_reviews(path, rows)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                self.assertEqual(list(csv.DictReader(handle))[0]["review"], "좋아요")


if __name__ == "__main__":
    unittest.main()
