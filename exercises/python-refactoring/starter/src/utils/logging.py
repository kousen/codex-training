"""Logging helpers used across the project."""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

LOGGER_NAME = "legacy_processor"

P = ParamSpec("P")
R = TypeVar("R")


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the application logger.

    Args:
        level: Standard library logging level.

    Returns:
        Configured logger instance.
    """

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
    return logger


def log_exceptions(
    logger: logging.Logger,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log any exception raised by the wrapped callable.

    Args:
        logger: Logger used to record failures.

    Returns:
        Decorator that logs and re-raises exceptions.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.exception("Unhandled error in %s", func.__name__)
                raise

        return wrapper

    return decorator
