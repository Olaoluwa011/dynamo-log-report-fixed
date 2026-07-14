import hashlib
import json
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")

EXPECTED_LOG_SHA256 = (
    "e83c0cb8dd9c33cbe0954cc038bd0ff90834cf48747e257d931dce5b2408d38e"
)


def load_report():
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def test_success_criterion_1_valid_json_and_exact_keys() -> None:
    """Success criterion 1: report.json is valid JSON with exactly the required keys."""
    assert REPORT_PATH.is_file(), "Missing /app/report.json"

    try:
        report = load_report()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AssertionError(f"/app/report.json is not valid JSON: {exc}") from exc

    assert isinstance(report, dict), "/app/report.json must contain a JSON object"
    assert set(report.keys()) == {
        "total_requests",
        "unique_ips",
        "top_path",
    }, "The report must contain exactly total_requests, unique_ips, and top_path"


def test_success_criterion_2_total_requests() -> None:
    """Success criterion 2: total_requests is an integer equal to 6."""
    report = load_report()

    assert type(report["total_requests"]) is int, (
        "total_requests must be an integer"
    )
    assert report["total_requests"] == 6, (
        "total_requests must equal the number of non-empty request lines"
    )


def test_success_criterion_3_unique_ips() -> None:
    """Success criterion 3: unique_ips is an integer equal to 3."""
    report = load_report()

    assert type(report["unique_ips"]) is int, "unique_ips must be an integer"
    assert report["unique_ips"] == 3, (
        "unique_ips must equal the number of distinct client IP addresses"
    )


def test_success_criterion_4_top_path() -> None:
    """Success criterion 4: top_path is the most frequently requested path."""
    report = load_report()

    assert report["top_path"] == "/index.html", (
        "top_path must be /index.html"
    )


def test_success_criterion_5_access_log_unchanged() -> None:
    """Success criterion 5: /app/access.log is not modified."""
    assert LOG_PATH.is_file(), "Missing /app/access.log"

    actual_digest = hashlib.sha256(LOG_PATH.read_bytes()).hexdigest()
    assert actual_digest == EXPECTED_LOG_SHA256, (
        "/app/access.log was modified"
    )
