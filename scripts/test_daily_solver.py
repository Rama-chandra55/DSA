import json
import os
import unittest
from unittest.mock import MagicMock, patch

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


if __name__ == "__main__":
    unittest.main()
