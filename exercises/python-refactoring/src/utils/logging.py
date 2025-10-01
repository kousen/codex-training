"""Logging utilities for the refactored application."""

from __future__ import annotations

import logging
import logging.config
from typing import Any, Dict

_DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}


def configure_logging(config: Dict[str, Any] | None = None) -> None:
    """Configure the global logging setup for the project.

    Args:
        config: Optional logging configuration dictionary. When omitted the
            module's default configuration is applied.
    """
    logging.config.dictConfig(config or _DEFAULT_LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """Create or retrieve a project logger configured with the defaults."""
    return logging.getLogger(name)
