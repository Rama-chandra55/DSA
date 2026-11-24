import io
import json
import os
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

import daily_solver


class GeminiFallbackTests(unittest.TestCase):
    def make_response(self, payload):
        response_text = json.dumps(payload)
        api_payload = {
            "candidates": [
                {"content": {"parts": [{"text": response_text}]}}
            ]
        }
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps(api_payload).encode("utf-8")
        return response

    def test_timeout_moves_to_next_model_without_waiting(self):
        response = self.make_response({"skip": False, "code": "class Solution:\n    pass"})
        with (
            patch.object(daily_solver, "KEY", "test-key"),
            patch.object(daily_solver, "MODEL", "primary-model"),
            patch.object(daily_solver, "GEMINI_RUN_DEADLINE", None),
            patch.dict(
                os.environ,
                {
                    "GEMINI_FALLBACK_MODEL": "fallback-model",
                    "GEMINI_SECONDARY_FALLBACK_MODEL": "secondary-model",
                },
            ),
            patch.object(
                daily_solver,
                "urlopen",
                side_effect=[TimeoutError("simulated timeout"), response],
            ) as mocked_urlopen,
        ):
            result = daily_solver.gemini(
                "test prompt",
                timeout=2,
                max_total_seconds=10,
            )

        self.assertEqual("class Solution:\n    pass", result["code"])
        self.assertEqual(2, mocked_urlopen.call_count)
        fallback_request = mocked_urlopen.call_args_list[1].args[0]
        self.assertIn("fallback-model:generateContent", fallback_request.full_url)

    def test_review_uses_small_decision_only_response(self):
        code = "class Solution:\n    def solve(self):\n        return True\n"
        problem = {
            "title": "Example",
            "id": "1",
            "content": "Return true for this example problem.",
        }
        with patch.object(
            daily_solver,
            "gemini",
            return_value={"approved": True, "issues": []},
        ) as mocked_gemini:
            reviewed = daily_solver.review(problem, code)

        self.assertEqual(code, reviewed)
        self.assertEqual(512, mocked_gemini.call_args.kwargs["max_output_tokens"])
        self.assertEqual(30, mocked_gemini.call_args.kwargs["timeout"])

    def test_review_rejects_unverified_solution(self):
        code = "class Solution:\n    def solve(self):\n        return True\n"
        problem = {
            "title": "Example",
            "id": "1",
            "content": "Return true for this example problem.",
        }
        with patch.object(
            daily_solver,
            "gemini",
            return_value={
                "approved": False,
                "issues": ["An edge case is not handled."],
            },
        ):
            with self.assertRaisesRegex(
                RuntimeError, "An edge case is not handled"
            ):
                daily_solver.review(problem, code)


    def test_all_models_retry_after_transient_503_and_succeed(self):
        response = self.make_response(
            {"skip": False, "code": "class Solution:\n    pass"}
        )

        def unavailable():
            return HTTPError(
                "https://generativelanguage.googleapis.com/test",
                503,
                "Service Unavailable",
                {},
                io.BytesIO(b'{"error":{"code":503,"status":"UNAVAILABLE"}}'),
            )

        with (
            patch.object(daily_solver, "KEY", "test-key"),
            patch.object(daily_solver, "MODEL", "primary-model"),
            patch.object(daily_solver, "GEMINI_RUN_DEADLINE", None),
            patch.dict(
                os.environ,
                {
                    "GEMINI_FALLBACK_MODEL": "fallback-model",
                    "GEMINI_SECONDARY_FALLBACK_MODEL": "secondary-model",
                    "GEMINI_TERTIARY_FALLBACK_MODEL": "",
                    "GEMINI_QUATERNARY_FALLBACK_MODEL": "",
                    "GEMINI_RETRY_ROUNDS": "2",
                    "GEMINI_RETRY_BACKOFF_SECONDS": "1",
                },
            ),
            patch.object(
                daily_solver,
                "urlopen",
                side_effect=[
                    unavailable(),
                    unavailable(),
                    unavailable(),
                    response,
                ],
            ) as mocked_urlopen,
            patch.object(daily_solver.time, "sleep") as mocked_sleep,
        ):
            result = daily_solver.gemini(
                "test prompt",
                timeout=2,
                max_total_seconds=20,
            )

        self.assertEqual("class Solution:\n    pass", result["code"])
        self.assertEqual(4, mocked_urlopen.call_count)
        mocked_sleep.assert_called_once_with(1)
        retried_request = mocked_urlopen.call_args_list[3].args[0]
        self.assertIn("primary-model:generateContent", retried_request.full_url)

    def test_all_models_fail_after_configured_retry_rounds(self):
        def unavailable():
            return HTTPError(
                "https://generativelanguage.googleapis.com/test",
                503,
                "Service Unavailable",
                {},
                io.BytesIO(b'{"error":{"code":503,"status":"UNAVAILABLE"}}'),
            )

        with (
            patch.object(daily_solver, "KEY", "test-key"),
            patch.object(daily_solver, "MODEL", "primary-model"),
            patch.object(daily_solver, "GEMINI_RUN_DEADLINE", None),
            patch.dict(
                os.environ,
                {
                    "GEMINI_FALLBACK_MODEL": "fallback-model",
                    "GEMINI_SECONDARY_FALLBACK_MODEL": "",
                    "GEMINI_TERTIARY_FALLBACK_MODEL": "",
                    "GEMINI_QUATERNARY_FALLBACK_MODEL": "",
                    "GEMINI_RETRY_ROUNDS": "2",
                    "GEMINI_RETRY_BACKOFF_SECONDS": "1",
                },
            ),
            patch.object(
                daily_solver,
                "urlopen",
                side_effect=[unavailable(), unavailable(), unavailable(), unavailable()],
            ) as mocked_urlopen,
            patch.object(daily_solver.time, "sleep") as mocked_sleep,
        ):
            with self.assertRaisesRegex(RuntimeError, "after 2 round"):
                daily_solver.gemini(
                    "test prompt",
                    timeout=2,
                    max_total_seconds=20,
                )

        self.assertEqual(4, mocked_urlopen.call_count)
        mocked_sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
