from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    log_level: str
    message: str
