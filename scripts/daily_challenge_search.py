import json
import re
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ALFA_API = "https://alfa-leetcode-api.onrender.com"
POTD_ARCHIVE = "https://leetcodethehardway.com/potd/"


class SourceHTTPError(RuntimeError):
    def __init__(self, status_code, detail, retry_after_seconds=None):
        super().__init__(f"Source returned HTTP {status_code}: {detail}")
        self.status_code = status_code
        self.retry_after_seconds = retry_after_seconds


def parse_retry_after(headers, detail=""):
    value = headers.get("Retry-After") if headers else None
    if value:
        try:
            return max(0, int(value.strip()))
        except (AttributeError, ValueError):
            try:
                retry_at = parsedate_to_datetime(value)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(
                    0,
                    int((retry_at - datetime.now(timezone.utc)).total_seconds()),
                )
            except (TypeError, ValueError, OverflowError):
                pass

    match = re.search(
        r"(?:try again|retry)\s+(?:in|after)\s+"
        r"(\d+)\s*(seconds?|minutes?|hours?)",
        detail,
        re.IGNORECASE,
    )
    if not match:
        return None

    delay = int(match.group(1))
    unit = match.group(2).lower()
    if unit.startswith("hour"):
        delay *= 3600
    elif unit.startswith("minute"):
        delay *= 60
    return delay


class DailyArchiveParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in {"td", "th"} and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in {"td", "th"} and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def fetch_text(url, timeout=35):
    request = Request(
        url,
        headers={
            "Accept": "application/json, text/html",
            "User-Agent": "DSA-Daily-Challenge-Search/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8")
    except HTTPError as error:
        detail = error.read().decode(errors="replace")[:250]
        raise SourceHTTPError(
            error.code,
            detail,
            parse_retry_after(error.headers, detail),
        ) from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError(f"Source is unavailable: {error}") from error


def fetch_json(url):
    try:
        return json.loads(fetch_text(url))
    except json.JSONDecodeError as error:
        raise RuntimeError("Source returned invalid JSON") from error


def normalize_question(data):
    if not isinstance(data, dict):
        raise RuntimeError("Question source returned an invalid record")

    if isinstance(data.get("data"), dict):
        data = data["data"]
    if isinstance(data.get("question"), dict):
        data = data["question"]

    title = data.get("questionTitle") or data.get("title")
    slug = data.get("titleSlug") or data.get("slug")
    question_text = data.get("question")
    content = question_text if isinstance(question_text, str) else data.get("content")
    problem_id = data.get("questionFrontendId") or data.get("id")

    tags = data.get("topicTags") or data.get("tags") or []
    tags = [
        item.get("name", "") if isinstance(item, dict) else str(item)
        for item in tags
    ]

    similar = data.get("similarQuestions") or data.get("similar_questions") or []
    if isinstance(similar, str):
        try:
            similar = json.loads(similar)
        except json.JSONDecodeError:
            similar = []

    if not title or not slug:
        raise RuntimeError("Question source omitted its title or slug")

    return {
        "id": str(problem_id or ""),
        "title": title,
        "slug": slug,
        "difficulty": data.get("difficulty", ""),
        "tags": tags,
        "link": data.get("questionLink") or data.get("link")
        or f"https://leetcode.com/problems/{slug}/",
        "content": content or "",
        "similar_questions": similar if isinstance(similar, list) else [],
        "is_paid_only": data.get("isPaidOnly", False),
    }


def archive_problem(target_date):
    page = fetch_text(POTD_ARCHIVE)
    parser = DailyArchiveParser()
    parser.feed(page)

    for row in parser.rows:
        if len(row) < 2 or row[0].strip() != target_date:
            continue
        match = re.search(r"(\d+)\s*[–—-]\s*(.+)", row[1])
        if not match:
            raise RuntimeError("Daily archive row has an unexpected format")
        return {
            "date": target_date,
            "id": match.group(1),
            "title": match.group(2).strip(),
        }

    return None


def fetch_problem_by_slug(slug):
    query = urlencode({"titleSlug": slug})
    data = fetch_json(f"{ALFA_API}/select/raw?{query}")
    problem = normalize_question(data)
    if not problem.get("content"):
        raise RuntimeError(f"No problem statement found for {slug}")
    return problem


def fetch_verified_daily_problem(
    target_date,
    attempts=5,
    retry_seconds=30,
    max_retry_delay=120,
    max_rate_limit_retries=1,
):
    last_reason = "The sources have not published today's challenge yet"
    attempts = max(1, int(attempts))
    retry_seconds = max(1, int(retry_seconds))
    max_retry_delay = max(1, int(max_retry_delay))
    rate_limit_retries = 0

    for attempt in range(1, attempts + 1):
        try:
            data = fetch_json(f"{ALFA_API}/daily")
            api_date = data.get("date") if isinstance(data, dict) else None
            problem = normalize_question(data)
            archived = archive_problem(target_date)

            if api_date != target_date:
                last_reason = f"API date is {api_date}, expected {target_date}"
            elif archived is None:
                last_reason = f"Archive has not listed {target_date} yet"
            elif problem["id"] != archived["id"]:
                last_reason = (
                    f"Problem ID mismatch: API={problem['id']}, "
                    f"archive={archived['id']}"
                )
            elif re.sub(r"[^a-z0-9]", "", problem["title"].casefold()) != (
                re.sub(r"[^a-z0-9]", "", archived["title"].casefold())
            ):
                last_reason = "The two sources disagree on the problem title"
            elif not problem.get("content"):
                last_reason = "The API has not returned the full problem statement"
            elif problem.get("is_paid_only"):
                last_reason = "Today's challenge is marked as premium"
            else:
                print(
                    f"Verified {target_date}: #{problem['id']} "
                    f"{problem['title']} using both sources."
                )
                return target_date, problem

        except SourceHTTPError as error:
            last_reason = str(error)

            if error.status_code == 429:
                delay = error.retry_after_seconds
                if delay is None:
                    delay = min(
                        retry_seconds * (2 ** rate_limit_retries),
                        max_retry_delay,
                    )

                if delay > max_retry_delay:
                    print(
                        "Source rate-limited this runner (HTTP 429) and "
                        f"requested a {delay}-second cooldown. Stopping this "
                        "run without making more requests; the next scheduled "
                        "run will retry."
                    )
                    return None, None

                if rate_limit_retries >= max_rate_limit_retries:
                    print(
                        "Source is still rate-limiting this runner after "
                        "the allowed retry. Stopping without more requests."
                    )
                    return None, None

                rate_limit_retries += 1
                print(
                    f"Source returned HTTP 429. Respecting its "
                    f"{delay}-second cooldown before one retry "
                    f"({rate_limit_retries}/{max_rate_limit_retries})."
                )
                if delay:
                    time.sleep(delay)
                continue

            if error.status_code not in {408, 500, 502, 503, 504}:
                print(f"Daily challenge verification stopped: {last_reason}")
                return None, None

        except Exception as error:
            last_reason = str(error)

        print(
            f"Challenge verification {attempt}/{attempts} for "
            f"{target_date} was not successful: {last_reason}"
        )
        if attempt < attempts:
            delay = min(
                retry_seconds * (2 ** (attempt - 1)),
                max_retry_delay,
            )
            print(f"Retrying verification in {delay} seconds.")
            time.sleep(delay)

    print(f"Daily challenge was not verified: {last_reason}")
    return None, None
