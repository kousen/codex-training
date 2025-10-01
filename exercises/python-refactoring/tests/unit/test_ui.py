"""Tests for the graphical calculator UI helpers."""

from __future__ import annotations

import tkinter as tk

import pytest

pytestmark = pytest.mark.skip(reason="Tkinter UI tests require an interactive display")

from ui.calculator_app import CalculatorApp


@pytest.fixture()
def tk_root() -> tk.Tk:
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        pytest.skip(f'Tkinter unavailable: {exc}')
    root.withdraw()
    yield root
    root.destroy()


def test_ui_performs_calculation(tk_root: tk.Tk) -> None:
    app = CalculatorApp(root=tk_root)
    app.left_operand.set("3")
    app.right_operand.set("4")
    app.selected_operation.set("add")

    app.calculate()

    assert app.result_value.get() == "Result: 7"
