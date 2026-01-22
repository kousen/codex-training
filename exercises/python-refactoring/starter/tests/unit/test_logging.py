"""Unit tests for logging utilities."""

from __future__ import annotations

import logging

from utils.logging import configure_logging


def test_configure_logging_sets_level() -> None:
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.NOTSET)

    configure_logging(level=logging.DEBUG)
    logger = logging.getLogger()
    assert logger.level == logging.DEBUG
