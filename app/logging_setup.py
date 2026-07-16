import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    """Render each log record as one JSON object — one line, machine-readable."""
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Anything passed via logger.info(..., extra={...}) lands here.
        if hasattr(record, "fields"):
            payload.update(record.fields)  # type: ignore[attr-defined]
        return json.dumps(payload)


def configure_logging() -> None:
    """Install the JSON formatter on the root logger — call once at startup."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
