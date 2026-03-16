"""Tests for logging utilities."""

from __future__ import annotations

import logging
from typing import Any

import pytest

from utils.logging import LOGGER_NAME, configure_logging, log_exceptions


def test_configure_logging_reuses_existing_handler() -> None:
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()

    first = configure_logging(logging.DEBUG)
    second = configure_logging(logging.INFO)

    assert first is second
    assert len(logger.handlers) == 1
    assert logger.level == logging.INFO


def test_log_exceptions_logs_and_reraises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    logger = logging.getLogger("legacy_processor.test")
    captured: list[str] = []

    def fake_exception(message: str, *args: Any, **kwargs: Any) -> None:
        del kwargs
        captured.append(message % args)

    monkeypatch.setattr(logger, "exception", fake_exception)

    @log_exceptions(logger)
    def boom() -> None:
        raise RuntimeError("failure")

    with pytest.raises(RuntimeError, match="failure"):
        boom()

    assert captured == ["Unhandled error in boom"]
