import logging
import json
import sys
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):
    """
    Emit logs as JSON.

    Structured logs are essential in production. Free-text logs cannot be
    reliably queried, aggregated, or alerted on. Every log entry includes
    a timestamp, level, logger name, message, and any extra fields passed
    by the caller.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include any extra fields the caller passed
        for key, value in record.__dict__.items():
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "message",
            }:
                log_entry[key] = value

        return json.dumps(log_entry, default=str)


def configure_logging(level: str = "INFO") -> None:
    """
    Configure structured JSON logging for the application.

    Call this once at startup. All subsequent loggers will inherit this config.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers = [handler]
