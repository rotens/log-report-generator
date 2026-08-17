from log_report.models import LogEntry
from log_report import parser
from datetime import datetime
import pytest


def test_parse_valid_log_line():
    line = "2026-06-24 14:32:10 ERROR Database connection failed"
    
    expected = LogEntry(
            timestamp=datetime(2026, 6, 24, 14, 32, 10),
            log_level="ERROR",
            message="Database connection failed",
        )
        
    actual = parser.parse_log_line(line)
    
    assert actual == expected
    
def test_parse_empty_line_returns_none():
    actual = parser.parse_log_line("")

    assert actual is None
    
def test_parse_whitespace_only_line_returns_none():
    actual = parser.parse_log_line("   \n")

    assert actual is None
    
def test_parse_line_without_message_returns_none():
    line = "2026-06-24 14:32:10 ERROR"

    actual = parser.parse_log_line(line)

    assert actual is None
    
def test_parse_invalid_timestamp_returns_none():
    line = "2026-02-30 14:32:10 ERROR Invalid date"

    actual = parser.parse_log_line(line)

    assert actual is None
    
def test_parse_unsupported_log_level_returns_none():
    line = "2026-06-24 14:32:10 DEBUG Diagnostic message"

    actual = parser.parse_log_line(line)

    assert actual is None
    
@pytest.mark.parametrize("log_level", ["INFO", "WARNING", "ERROR"])
def test_parse_supported_log_level(log_level):
    line = f"2026-06-24 14:32:10 {log_level} Test message"

    actual = parser.parse_log_line(line)

    assert actual is not None
    assert actual.log_level == log_level