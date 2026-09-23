from datetime import datetime
import re

from log_report.models import LogEntry

SUPPORTED_LOG_LEVELS = {"INFO", "WARNING", "ERROR"}
TIMESTAMP_PATTERN = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2} "
    r"[0-9]{2}:[0-9]{2}:[0-9]{2}"
)
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_log_line(line: str) -> LogEntry | None:
    line = line.rstrip("\r\n")

    if not line.strip():
        return None

    if line[0].isspace() or line[-1].isspace():
        return None

    parts = line.split(" ", maxsplit=3)

    if len(parts) != 4:
        return None

    date_text, time_text, log_level, message = parts

    if not message or message[0].isspace():
        return None

    timestamp_text = f"{date_text} {time_text}"

    if TIMESTAMP_PATTERN.fullmatch(timestamp_text) is None:
        return None

    if log_level not in SUPPORTED_LOG_LEVELS:
        return None

    try:
        timestamp = datetime.strptime(timestamp_text, TIMESTAMP_FORMAT)
    except ValueError:
        return None

    return LogEntry(
        timestamp=timestamp,
        log_level=log_level,
        message=message,
    )
