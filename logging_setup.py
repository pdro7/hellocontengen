# logging_setup.py
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level":     record.levelname,
            "message":   record.getMessage(),
        }
        # Si usas extra_fields, añádelo al JSON
        if hasattr(record, "extra_fields"):
            base.update(record.extra_fields)
        return json.dumps(base)
