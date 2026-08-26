"""Command-line logging configuration."""

import logging


def configure_logging(verbose: bool = False) -> None:
    """Configure consistent command-line logging.

    Args:
        verbose: Enable debug messages when true.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
