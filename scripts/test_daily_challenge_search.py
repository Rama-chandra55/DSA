import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import daily_challenge_search as daily


class RetryAfterTests(unittest.TestCase):
    def test_parses_retry_after_seconds_header(self):
        self.assertEqual(
            3600,
            daily.parse_retry_after({"Retry-After": "3600"}, ""),
        )

    def test_parses_retry_after_hint_from_response_body(self):
        self.assertEqual(
            3600,
            daily.parse_retry_after(
                {},
                "Too many requests from this IP, try again in 1 hour",
            ),
        )

    def test_fetch_text_preserves_rate_limit_metadata(self):
        response_error = HTTPError(
            "https://example.com/daily",
            429,
            "Too Many Requests",
            {"Retry-After": "3600"},
            io.BytesIO(b"Too many requests"),
        )
        with patch.object(daily, "urlopen", side_effect=response_error):
            with self.assertRaises(daily.SourceHTTPError) as raised:
                daily.fetch_text("https://example.com/daily")

        self.assertEqual(429, raised.exception.status_code)
        self.assertEqual(3600, raised.exception.retry_after_seconds)

    def test_long_rate_limit_stops_without_repeating_requests(self):
        rate_limit = daily.SourceHTTPError(
            429,
            "Too many requests, try again in 1 hour",
            3600,
        )
        with (
            patch.object(daily, "fetch_json", side_effect=rate_limit) as fetch,
            patch.object(daily.time, "sleep") as sleep,
        ):
            result = daily.fetch_verified_daily_problem("2026-11-15")

        self.assertEqual((None, None), result)
        self.assertEqual(1, fetch.call_count)
        sleep.assert_not_called()

    def test_short_rate_limit_waits_and_retries_once(self):
        target_date = "2026-11-15"
        problem_data = {
            "date": target_date,
            "questionFrontendId": "1524",
            "title": "Number of Sub-arrays With Odd Sum",
            "titleSlug": "number-of-sub-arrays-with-odd-sum",
            "question": "Given an array, return the required count.",
            "difficulty": "Medium",
            "topicTags": [],
        }
        archive_data = {
            "id": "1524",
            "title": "Number of Sub-arrays With Odd Sum",
        }
        rate_limit = daily.SourceHTTPError(
            429,
            "Temporary rate limit",
            30,
        )

        with (
            patch.object(
                daily,
                "fetch_json",
                side_effect=[rate_limit, problem_data],
            ) as fetch,
            patch.object(daily, "archive_problem", return_value=archive_data),
            patch.object(daily.time, "sleep") as sleep,
        ):
            result = daily.fetch_verified_daily_problem(target_date)

        self.assertEqual(target_date, result[0])
        self.assertEqual("1524", result[1]["id"])
        self.assertEqual(2, fetch.call_count)
        sleep.assert_called_once_with(30)


if __name__ == "__main__":
    unittest.main()
