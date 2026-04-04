import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from ghostagency.core.config import LOG_DIR


class StructuredLogger:
    """JSON-structured logger for all agent interactions."""

    def __init__(self, agent_slug: str, client_name: str):
        self.agent_slug = agent_slug
        self.client_name = client_name
        self.log_dir = LOG_DIR / client_name / agent_slug
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _write_log(self, level: str, event: str, **kwargs):
        """Write structured JSON log entry."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "event": event,
            "agent": self.agent_slug,
            "client": self.client_name,
            **kwargs,
        }

        log_file = self.log_dir / f"{datetime.now().strftime('%Y%m%d')}.jsonl"

        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def info(self, event: str, **kwargs):
        """Log informational event."""
        self._write_log("INFO", event, **kwargs)

    def warning(self, event: str, **kwargs):
        """Log warning event."""
        self._write_log("WARNING", event, **kwargs)

    def error(self, event: str, **kwargs):
        """Log error event."""
        self._write_log("ERROR", event, **kwargs)


def get_logger(agent_slug: str, client_name: str) -> StructuredLogger:
    """Get a structured logger for the given agent and client."""
    return StructuredLogger(agent_slug, client_name)
