"""Logging helpers used across the refactored project."""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def configure_logging(level: int = logging.INFO) -> None:
    """Configure application logging.

    Args:
        level: Logging threshold passed to ``logging.basicConfig``.
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def log_call(logger: logging.Logger) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log calls and exceptions for a function.

    Args:
        logger: Logger receiving debug and exception messages.

    Returns:
        A decorator that wraps the target function.
    """

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logger.debug("Calling %s", function.__name__)
            try:
                return function(*args, **kwargs)
            except Exception:
                logger.exception("%s failed", function.__name__)
                raise

        return wrapper

    return decorator
