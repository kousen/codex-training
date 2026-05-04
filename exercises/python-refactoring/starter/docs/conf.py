"""Sphinx configuration for the refactored data processor."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

project = "Python Refactoring Starter"
author = "Kousen IT"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
templates_path = ["_templates"]
exclude_patterns = ["_build"]
html_theme = "alabaster"
autodoc_typehints = "description"
