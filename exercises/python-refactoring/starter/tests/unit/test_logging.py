"""Unit tests for logging utilities."""

from __future__ import annotations

import logging

import pytest

from utils.logging import configure_logging, log_call


def test_configure_logging_accepts_level() -> None:
    """Logging configuration can be called by applications."""

    configure_logging(logging.DEBUG)


def test_log_call_logs_and_reraises(caplog: pytest.LogCaptureFixture) -> None:
    """Decorator logs exceptions without swallowing them."""

    logger = logging.getLogger("tests.logging")

    @log_call(logger)
    def fail() -> None:
        raise RuntimeError("boom")

    with caplog.at_level(logging.ERROR), pytest.raises(RuntimeError, match="boom"):
        fail()

    assert "fail failed" in caplog.text


def test_log_call_returns_successful_result(caplog: pytest.LogCaptureFixture) -> None:
    """Decorator returns wrapped function results."""

    logger = logging.getLogger("tests.logging")

    @log_call(logger)
    def add(left: int, right: int) -> int:
        return left + right

    with caplog.at_level(logging.DEBUG):
        assert add(2, 3) == 5

    assert "Calling add" in caplog.text
