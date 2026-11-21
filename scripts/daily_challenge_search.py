import json
import os
import re
import time
from pathlib import Path
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


ALFA_API = "https://alfa-leetcode-api.onrender.com"
OJ_API = "https://oj-api.gdst.dev"
POTD_ARCHIVE = "https://leetcodethehardway.com/potd/"
_HTTP_CACHE = {}
_SOURCE_COOLDOWNS = {}
COOLDOWN_FILE = Path(
    os.getenv("SOURCE_COOLDOWN_FILE", ".github/source-cooldowns.json")
)


def load_source_cooldowns():
    try:
        data = json.loads(COOLDOWN_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError):
        print("Source cooldown cache could not be read; starting with an empty cache.")
        return {}


def save_source_cooldowns(cooldowns):
    temporary = COOLDOWN_FILE.with_suffix(COOLDOWN_FILE.suffix + ".tmp")
    try:
        COOLDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_text(
            json.dumps(cooldowns, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(COOLDOWN_FILE)
    except OSError as error:
        print(f"Could not persist source cooldowns: {error}")
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


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


def fetch_text(url, timeout=35, cache_seconds=90):
    now = time.monotonic()
    cached = _HTTP_CACHE.get(url)
    if cached and cached[0] > now:
        return cached[1]

    host = urlparse(url).netloc
    cooldown_until = _SOURCE_COOLDOWNS.get(host, 0)
    persisted = load_source_cooldowns()
    try:
        persisted_until = float(persisted.get(host, 0) or 0)
    except (TypeError, ValueError):
        persisted_until = 0
    if persisted_until > time.time():
        remaining = max(1, int(persisted_until - time.time()))
        _SOURCE_COOLDOWNS[host] = max(
            cooldown_until,
            now + remaining,
        )
        raise SourceHTTPError(
            429,
            f"{host} is cooling down; retry after approximately {remaining}s",
            remaining,
        )
    if cooldown_until > now:
        remaining = max(1, int(cooldown_until - now))
        raise SourceHTTPError(
            429,
            f"{host} is cooling down; retry after approximately {remaining}s",
            remaining,
        )
    if host in persisted:
        persisted.pop(host, None)
        save_source_cooldowns(persisted)

    request = Request(
        url,
        headers={
            "Accept": "application/json, text/html",
            "User-Agent": "DSA-Daily-Challenge-Search/1.1",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            if cache_seconds > 0:
                _HTTP_CACHE[url] = (time.monotonic() + cache_seconds, body)
            return body
    except HTTPError as error:
        detail = error.read().decode(errors="replace")[:250]
        retry_after = parse_retry_after(error.headers, detail)
        if error.code == 429:
            cooldown = retry_after if retry_after is not None else 60
            retry_after = cooldown
            _SOURCE_COOLDOWNS[host] = max(
                _SOURCE_COOLDOWNS.get(host, 0),
                time.monotonic() + cooldown,
            )
            persisted = load_source_cooldowns()
            try:
                previous_until = float(persisted.get(host, 0) or 0)
            except (TypeError, ValueError):
                previous_until = 0
            persisted[host] = max(
                previous_until,
                time.time() + cooldown,
            )
            save_source_cooldowns(persisted)
        raise SourceHTTPError(error.code, detail, retry_after) from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError(f"Source is unavailable: {error}") from error


def fetch_json(url, cache_seconds=90):
    try:
        return json.loads(fetch_text(url, cache_seconds=cache_seconds))
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

    paid_only = data.get("isPaidOnly", data.get("paid_only", False))
    if isinstance(paid_only, str):
        paid_only = paid_only.strip().casefold() in {"1", "true", "yes"}

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
        "is_paid_only": bool(paid_only),
    }


def _normalised_title(title):
    return re.sub(r"[^a-z0-9]", "", str(title).casefold())


def _same_problem(problem, reference):
    if not problem or not reference:
        return False
    return (
        str(problem.get("id", "")) == str(reference.get("id", ""))
        and _normalised_title(problem.get("title"))
        == _normalised_title(reference.get("title"))
    )


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


def fetch_oj_daily_problem(target_date):
    query = urlencode({"domain": "com", "date": target_date})
    payload = fetch_json(
        f"{OJ_API}/api/v1/daily?{query}",
        cache_seconds=60,
    )
    if not isinstance(payload, dict):
        raise RuntimeError("OJ API returned an invalid daily response")

    if payload.get("status") == "fetching":
        retry_after = payload.get("retry_after")
        print(
            "OJ API does not have this date cached yet"
            + (f"; it suggests retrying in {retry_after}s." if retry_after else ".")
            + " Not polling it repeatedly."
        )
        return None

    if payload.get("date") != target_date:
        print(
            f"OJ API date mismatch: received {payload.get('date')}, "
            f"expected {target_date}."
        )
        return None

    records = payload.get("problems")
    if not isinstance(records, list):
        print("OJ API daily response did not contain a problems list.")
        return None

    daily_source = payload.get("source")
    if daily_source not in {"leetcode.com", "leetcode"}:
        if daily_source is not None:
            print(f"OJ API returned an unexpected source: {daily_source}.")
            return None

        # Some API responses omit the top-level source. Accept that response
        # only when the actual daily problem record explicitly identifies
        # itself as a LeetCode problem.
        has_leetcode_record = any(
            isinstance(item, dict)
            and item.get("source") in {"leetcode", "leetcode.com"}
            for item in records
        )
        if not has_leetcode_record:
            print(
                "OJ API omitted its top-level source and no problem record "
                "explicitly identified LeetCode."
            )
            return None
        print(
            "OJ API omitted its top-level source; checking the explicit "
            "source on the daily problem record."
        )

    record = next(
        (
            item for item in records
            if isinstance(item, dict)
            and item.get("source") in {"leetcode", "leetcode.com"}
        ),
        None,
    )
    if not record:
        print("OJ API daily response did not contain a LeetCode problem.")
        return None

    problem = normalize_question(record)
    if not problem.get("id") or not problem.get("content"):
        print("OJ API did not return a complete problem statement.")
        return None
    if problem.get("is_paid_only"):
        print("OJ API marked the daily challenge as premium; skipping it.")
        return None
    return problem


def fetch_alfa_daily_problem(target_date):
    payload = fetch_json(f"{ALFA_API}/daily", cache_seconds=60)
    if not isinstance(payload, dict) or payload.get("date") != target_date:
        actual_date = payload.get("date") if isinstance(payload, dict) else None
        print(
            f"Alfa API date mismatch: received {actual_date}, "
            f"expected {target_date}."
        )
        return None

    problem = normalize_question(payload)
    if not problem.get("id") or not problem.get("content"):
        print("Alfa API did not return a complete problem statement.")
        return None
    if problem.get("is_paid_only"):
        print("Alfa API marked the daily challenge as premium; skipping it.")
        return None
    return problem


def fetch_problem_by_slug(slug):
    query = urlencode({"titleSlug": slug})
    data = fetch_json(f"{ALFA_API}/select/raw?{query}")
    problem = normalize_question(data)
    if not problem.get("content"):
        raise RuntimeError(f"No problem statement found for {slug}")
    return problem


def _source_error(label, error):
    if isinstance(error, SourceHTTPError) and error.status_code == 429:
        delay = error.retry_after_seconds
        delay_text = (
            "an unspecified cooldown"
            if delay is None else f"a {delay}-second cooldown"
        )
        print(
            f"{label} was rate-limited ({error}). Respecting {delay_text}; "
            "that host will not be requested again during this run."
        )
    else:
        print(f"{label} is unavailable: {error}")


def fetch_verified_daily_problem(target_date):
    """Verify with OJ API + archive, then use Alfa as a one-request tie-breaker."""
    oj_problem = None
    archived = None
    alfa_problem = None

    try:
        oj_problem = fetch_oj_daily_problem(target_date)
        if oj_problem:
            print(
                f"OJ API returned #{oj_problem['id']} "
                f"{oj_problem['title']} for {target_date}."
            )
    except Exception as error:
        _source_error("OJ API", error)

    try:
        archived = archive_problem(target_date)
        if archived:
            print(
                f"Daily archive returned #{archived['id']} "
                f"{archived['title']} for {target_date}."
            )
    except Exception as error:
        _source_error("Daily archive", error)

    if oj_problem and archived and _same_problem(oj_problem, archived):
        print(
            f"Verified {target_date}: #{oj_problem['id']} "
            f"{oj_problem['title']} using OJ API and daily archive."
        )
        return target_date, oj_problem

    if not oj_problem and not archived:
        print(
            "Neither primary source returned a verifiable daily challenge. "
            "Skipping the Alfa request because one source alone cannot "
            "confirm the problem."
        )
        return None, None

    try:
        alfa_problem = fetch_alfa_daily_problem(target_date)
        if alfa_problem:
            print(
                f"Alfa API returned #{alfa_problem['id']} "
                f"{alfa_problem['title']} for {target_date}."
            )
    except Exception as error:
        _source_error("Alfa API", error)

    if oj_problem and alfa_problem and _same_problem(oj_problem, alfa_problem):
        print(
            f"Verified {target_date}: #{oj_problem['id']} "
            f"{oj_problem['title']} using OJ API and Alfa API."
        )
        return target_date, oj_problem

    if archived and alfa_problem and _same_problem(alfa_problem, archived):
        print(
            f"Verified {target_date}: #{alfa_problem['id']} "
            f"{alfa_problem['title']} using daily archive and Alfa API."
        )
        return target_date, alfa_problem

    if oj_problem and archived and alfa_problem:
        print(
            "Daily challenge sources disagree. Refusing to generate a "
            "solution from conflicting problem records."
        )
    else:
        print(
            f"No two sources could verify the LeetCode daily challenge "
            f"for {target_date}. Skipping generation to avoid solving "
            "an outdated or unverified problem."
        )
    return None, None
