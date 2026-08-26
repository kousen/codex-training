"""Backward-compatible facade for the refactored processing application."""

from codex_refactoring.cli import (
    DEFAULT_OPERATIONS,
    build_parser,
    load_and_process,
    main,
    process,
    run_pipeline,
    save_results,
)

__all__ = [
    "DEFAULT_OPERATIONS",
    "build_parser",
    "load_and_process",
    "main",
    "process",
    "run_pipeline",
    "save_results",
]


if __name__ == "__main__":  # pragma: no cover - exercised by subprocess tests
    raise SystemExit(main())
