"""Logging configuration for the project."""

from __future__ import annotations

import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
DEFAULT_LEVEL = logging.INFO


def configure_logging(level: int = DEFAULT_LEVEL) -> None:
    """Configure application-wide logging."""
    logging.basicConfig(level=level, format=LOG_FORMAT)
