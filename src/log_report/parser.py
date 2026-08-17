from datetime import datetime
from log_report.models import LogEntry

SUPPORTED_LOG_LEVELS = {"INFO", "WARNING", "ERROR"}

def parse_log_line(line: str) -> LogEntry | None:
    if not line.strip():
        return None
    
    parts = line.split(maxsplit=3)
    
    if len(parts) != 4:
        return None
    
    date_text, time_text, log_level, message = parts

    if log_level not in SUPPORTED_LOG_LEVELS:
        return None

    try:
        timestamp = datetime.strptime(
            f"{date_text} {time_text}",
            "%Y-%m-%d %H:%M:%S",
        )
    except ValueError:
        return None

    return LogEntry(
        timestamp=timestamp,
        log_level=log_level,
        message=message,
    )