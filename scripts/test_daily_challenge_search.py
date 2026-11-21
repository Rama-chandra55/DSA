import io
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch

import daily_challenge_search as sources


def problem(problem_id="1", title="Two Sum"):
    return {
        "id": problem_id,
        "title": title,
        "slug": "two-sum",
        "content": "<p>Find two numbers.</p>",
        "is_paid_only": False,
    }


class RetryAfterParsingTests(unittest.TestCase):
    def test_parses_retry_after_seconds_header(self):
        self.assertEqual(
            3600,
            sources.parse_retry_after({"Retry-After": "3600"}, ""),
        )

    def test_parses_retry_after_hint_from_response_body(self):
        self.assertEqual(
            3600,
            sources.parse_retry_after(
                {},
                "Too many requests from this IP, try again in 1 hour",
            ),
        )


class DailySourceVerificationTests(unittest.TestCase):
    def setUp(self):
        sources._HTTP_CACHE.clear()
        sources._SOURCE_COOLDOWNS.clear()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        sources.COOLDOWN_FILE = Path(self.temp_dir.name) / "cooldowns.json"

    def test_oj_and_archive_verify_without_calling_third_source(self):
        with (
            patch.object(sources, "fetch_oj_daily_problem", return_value=problem()),
            patch.object(
                sources,
                "archive_problem",
                return_value={"id": "1", "title": "Two Sum"},
            ),
            patch.object(
                sources,
                "fetch_alfa_daily_problem",
                side_effect=AssertionError("third source should not be called"),
            ),
        ):
            date, result = sources.fetch_verified_daily_problem("2026-11-19")

        self.assertEqual("2026-11-19", date)
        self.assertEqual("1", result["id"])

    def test_oj_rate_limit_falls_back_to_archive_and_alfa(self):
        with (
            patch.object(
                sources,
                "fetch_oj_daily_problem",
                side_effect=sources.SourceHTTPError(429, "slow down", 1200),
            ),
            patch.object(
                sources,
                "archive_problem",
                return_value={"id": "1", "title": "Two Sum"},
            ),
            patch.object(sources, "fetch_alfa_daily_problem", return_value=problem()),
            patch.object(sources.time, "sleep") as sleep,
        ):
            date, result = sources.fetch_verified_daily_problem("2026-11-19")
            sleep.assert_not_called()

        self.assertEqual("2026-11-19", date)
        self.assertEqual("1", result["id"])

    def test_alfa_is_not_needed_when_oj_and_archive_match(self):
        with (
            patch.object(sources, "fetch_oj_daily_problem", return_value=problem()),
            patch.object(
                sources,
                "archive_problem",
                return_value={"id": "1", "title": "Two Sum"},
            ),
            patch.object(
                sources,
                "fetch_alfa_daily_problem",
                side_effect=AssertionError("third source should not be called"),
            ),
        ):
            date, result = sources.fetch_verified_daily_problem("2026-11-19")

        self.assertEqual("2026-11-19", date)
        self.assertEqual("1", result["id"])

    def test_disagreement_is_rejected_when_no_majority_exists(self):
        with (
            patch.object(sources, "fetch_oj_daily_problem", return_value=problem()),
            patch.object(
                sources,
                "archive_problem",
                return_value={"id": "2", "title": "Add Two Numbers"},
            ),
            patch.object(
                sources,
                "fetch_alfa_daily_problem",
                return_value=problem("3", "Longest Substring"),
            ),
        ):
            date, result = sources.fetch_verified_daily_problem("2026-11-19")

        self.assertIsNone(date)
        self.assertIsNone(result)

    def test_missing_primary_sources_skip_unverified_alfa_request(self):
        with (
            patch.object(sources, "fetch_oj_daily_problem", return_value=None),
            patch.object(sources, "archive_problem", return_value=None),
            patch.object(
                sources,
                "fetch_alfa_daily_problem",
                side_effect=AssertionError("one source alone cannot verify the challenge"),
            ),
        ):
            date, result = sources.fetch_verified_daily_problem("2026-11-19")

        self.assertIsNone(date)
        self.assertIsNone(result)

    def test_oj_fetching_response_is_not_polled(self):
        with patch.object(
            sources,
            "fetch_json",
            return_value={"status": "fetching", "retry_after": 30},
        ) as fetch:
            result = sources.fetch_oj_daily_problem("2026-11-19")

        self.assertIsNone(result)
        self.assertEqual(1, fetch.call_count)

    def test_429_retry_after_persists_across_fresh_runner(self):
        error = HTTPError(
            "https://example.test/daily",
            429,
            "Too Many Requests",
            {"Retry-After": "1229"},
            io.BytesIO(b"rate limited"),
        )
        with patch.object(sources, "urlopen", side_effect=error) as mocked:
            with self.assertRaises(sources.SourceHTTPError):
                sources.fetch_text("https://example.test/daily")
            sources._SOURCE_COOLDOWNS.clear()
            with self.assertRaises(sources.SourceHTTPError) as raised:
                sources.fetch_text("https://example.test/another")

        self.assertEqual(1, mocked.call_count)
        self.assertEqual(429, raised.exception.status_code)
        self.assertGreater(raised.exception.retry_after_seconds, 0)
        self.assertTrue(sources.COOLDOWN_FILE.exists())
        self.assertIn("example.test", sources.load_source_cooldowns())

    def test_successful_get_is_cached_briefly(self):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"ok": true}'
        with patch.object(sources, "urlopen", return_value=response) as mocked:
            first = sources.fetch_text("https://example.test/data")
            second = sources.fetch_text("https://example.test/data")

        self.assertEqual('{"ok": true}', first)
        self.assertEqual(first, second)
        self.assertEqual(1, mocked.call_count)

    def test_oj_accepts_missing_top_level_source_when_record_identifies_leetcode(self):
        payload = {
            "date": "2026-11-21",
            "source": None,
            "problems": [
                {
                    "id": "3331",
                    "source": "leetcode",
                    "slug": "find-subtree-sizes-after-changes",
                    "title": "Find Subtree Sizes After Changes",
                    "content": "<p>Given a tree...</p>",
                    "paid_only": 0,
                    "tags": ["Tree"],
                }
            ],
        }
        with patch.object(sources, "fetch_json", return_value=payload):
            result = sources.fetch_oj_daily_problem("2026-11-21")

        self.assertEqual("3331", result["id"])
        self.assertEqual("Find Subtree Sizes After Changes", result["title"])

    def test_oj_rejects_missing_top_level_source_without_leetcode_record(self):
        payload = {
            "date": "2026-11-21",
            "source": None,
            "problems": [
                {
                    "id": "abc123",
                    "source": "atcoder",
                    "slug": "sample",
                    "title": "Sample",
                    "content": "<p>Statement</p>",
                }
            ],
        }
        with patch.object(sources, "fetch_json", return_value=payload):
            result = sources.fetch_oj_daily_problem("2026-11-21")

        self.assertIsNone(result)

    def test_oj_problem_normalizes_paid_only_and_content_fields(self):
        payload = {
            "date": "2026-11-19",
            "source": "leetcode.com",
            "problems": [
                {
                    "id": "1",
                    "source": "leetcode",
                    "slug": "two-sum",
                    "title": "Two Sum",
                    "content": "<p>Statement</p>",
                    "paid_only": 0,
                    "tags": ["Array"],
                }
            ],
        }
        with patch.object(sources, "fetch_json", return_value=payload):
            result = sources.fetch_oj_daily_problem("2026-11-19")

        self.assertEqual("1", result["id"])
        self.assertEqual("<p>Statement</p>", result["content"])
        self.assertFalse(result["is_paid_only"])


if __name__ == "__main__":
    unittest.main()
