"""Tkinter-based graphical interface for the calculator module."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from calculator.calculator import Calculator
from exceptions.custom import CalculatorError, ValidationError


class CalculatorApp:
    """Interactive calculator UI backed by the core Calculator service."""

    _OPERATION_SYMBOLS = {
        "add": "+",
        "sub": "−",
        "mul": "×",
        "div": "÷",
    }

    def __init__(self, root: tk.Tk | None = None) -> None:
        self.root = root or tk.Tk()
        self.root.title("Modern Calculator")
        self.root.resizable(False, False)

        self._calculator = Calculator()
        self._operation_names = tuple(self._calculator.available_operations)

        self.left_operand = tk.StringVar(value="0")
        self.right_operand = tk.StringVar(value="0")
        self.selected_operation = tk.StringVar(value=self._operation_names[0])
        self.result_value = tk.StringVar(value="Result will appear here")
        self._active_operand: str = "left"

        self._build_layout()
        self._bind_events()

    # ------------------------------------------------------------------
    # Layout & styling helpers
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        primary_bg = "#111827"
        card_bg = "#1f2937"
        accent = "#3b82f6"
        text_fg = "#f9fafb"

        self.root.configure(bg=primary_bg)

        style.configure("Calculator.TFrame", background=primary_bg)
        style.configure("Card.TFrame", background=card_bg)
        style.configure("Display.TLabel", background=card_bg, foreground=text_fg, font=("SF Pro Display", 28, "bold"))
        style.configure("Caption.TLabel", background=card_bg, foreground="#9ca3af", font=("SF Pro Text", 11))
        style.configure("Input.TEntry", foreground=text_fg)
        style.configure("Action.TButton", font=("SF Pro Text", 12, "bold"))
        style.map(
            "Action.TButton",
            background=[("!disabled", accent)],
            foreground=[("!disabled", text_fg)],
        )
        style.configure(
            "Keypad.TButton",
            font=("SF Pro Text", 14, "bold"),
            padding=(12, 10),
        )
        style.map(
            "Keypad.TButton",
            background=[("active", "#2563eb"), ("!disabled", "#374151")],
            foreground=[("!disabled", text_fg)],
        )
        style.configure(
            "Operator.TRadiobutton",
            background=card_bg,
            foreground=text_fg,
            font=("SF Pro Text", 12),
            padding=(10, 6),
        )
        style.map(
            "Operator.TRadiobutton",
            background=[("selected", accent), ("!selected", "#374151")],
            foreground=[("selected", text_fg), ("!selected", text_fg)],
        )

        outer = ttk.Frame(self.root, style="Calculator.TFrame", padding=24)
        outer.grid(row=0, column=0, sticky="nsew")

        card = ttk.Frame(outer, style="Card.TFrame", padding=24)
        card.grid(row=0, column=0, sticky="nsew")

        ttk.Label(card, text="Result", style="Caption.TLabel").grid(row=0, column=0, columnspan=4, sticky="w")
        self.result_label = ttk.Label(card, textvariable=self.result_value, style="Display.TLabel", anchor="e")
        self.result_label.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(4, 16))

        input_frame = ttk.Frame(card, style="Card.TFrame")
        input_frame.grid(row=2, column=0, columnspan=4, sticky="ew")
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

        self.left_entry = ttk.Entry(input_frame, textvariable=self.left_operand, justify="right", font=("SF Pro Text", 14), width=12)
        self.left_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.left_entry.bind("<FocusIn>", lambda _evt: self._set_active_operand("left"))
        self.left_entry.focus()

        self.right_entry = ttk.Entry(input_frame, textvariable=self.right_operand, justify="right", font=("SF Pro Text", 14), width=12)
        self.right_entry.grid(row=0, column=1, sticky="ew")
        self.right_entry.bind("<FocusIn>", lambda _evt: self._set_active_operand("right"))

        operator_bar = ttk.Frame(card, style="Card.TFrame")
        operator_bar.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(16, 8))
        for index, operation in enumerate(self._operation_names):
            symbol = self._OPERATION_SYMBOLS.get(operation, operation.upper())
            button = ttk.Radiobutton(
                operator_bar,
                text=f" {symbol} ",
                value=operation,
                variable=self.selected_operation,
                style="Operator.TRadiobutton",
            )
            button.grid(row=0, column=index, padx=4)

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(0, 12))

        ttk.Button(actions, text="Clear", style="Action.TButton", command=self.clear_inputs).grid(row=0, column=0, padx=(0, 12))
        ttk.Button(actions, text="Calculate", style="Action.TButton", command=self.calculate).grid(row=0, column=1)

        keypad = ttk.Frame(card, style="Card.TFrame")
        keypad.grid(row=5, column=0, columnspan=4, sticky="ew")

        keys = [
            ["7", "8", "9", "⌫"],
            ["4", "5", "6", "±"],
            ["1", "2", "3", "="],
            ["0", ".", "C", None],
        ]

        for row_index, row in enumerate(keys):
            for col_index, key in enumerate(row):
                if key is None:
                    continue
                command = self._make_key_command(key)
                ttk.Button(keypad, text=key, style="Keypad.TButton", command=command).grid(row=row_index, column=col_index, padx=6, pady=6, sticky="nsew")

        for col in range(4):
            keypad.columnconfigure(col, weight=1)

    # ------------------------------------------------------------------
    def _bind_events(self) -> None:
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<KP_Enter>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear_inputs())
        self.root.bind("<Key>", self._handle_keyboard)

    def _set_active_operand(self, operand: str) -> None:
        self._active_operand = operand

    # ------------------------------------------------------------------
    # Keypad interaction
    # ------------------------------------------------------------------
    def _make_key_command(self, key: str):
        if key == "=":
            return self.calculate
        if key == "C":
            return self._clear_active_entry
        if key == "⌫":
            return self._backspace_active_entry
        if key == "±":
            return self._negate_active_entry

        return lambda: self._append_character(key)

    def _active_var(self) -> tk.StringVar:
        return self.left_operand if self._active_operand == "left" else self.right_operand

    def _append_character(self, value: str) -> None:
        variable = self._active_var()
        current = variable.get()
        if current == "0" and value != ".":
            variable.set(value)
        else:
            if value == "." and "." in current:
                return
            variable.set(f"{current}{value}")

    def _clear_active_entry(self) -> None:
        self._active_var().set("0")

    def _backspace_active_entry(self) -> None:
        variable = self._active_var()
        value = variable.get()
        if len(value) <= 1:
            variable.set("0")
        else:
            variable.set(value[:-1])

    def _negate_active_entry(self) -> None:
        variable = self._active_var()
        value = variable.get()
        if value.startswith("-"):
            variable.set(value[1:])
        elif value != "0":
            variable.set(f"-{value}")

    def _handle_keyboard(self, event: tk.Event) -> None:  # type: ignore[override]
        char = event.char
        if char.isdigit():
            self._append_character(char)
        elif char == ".":
            self._append_character(char)
        elif char in {"+", "-", "*", "/"}:
            mapping = {"+": "add", "-": "sub", "*": "mul", "/": "div"}
            self.selected_operation.set(mapping[char])
        elif event.keysym == "BackSpace":
            self._backspace_active_entry()

    # ------------------------------------------------------------------
    # Operations
    # ------------------------------------------------------------------
    def calculate(self) -> None:
        operation = self.selected_operation.get()
        left = self.left_operand.get()
        right = self.right_operand.get()

        try:
            result = self._calculator.calculate(operation, left, right)
        except (CalculatorError, ValidationError) as exc:
            messagebox.showerror("Calculation error", str(exc))
            self.result_value.set("Error")
        else:
            self.result_value.set(f"Result: {result:g}")

    def clear_inputs(self) -> None:
        self.left_operand.set("0")
        self.right_operand.set("0")
        self.selected_operation.set(self._operation_names[0])
        self.result_value.set("Result will appear here")
        self._set_active_operand("left")
        self.left_entry.focus_set()

    def run(self) -> None:
        """Start the Tkinter main event loop."""
        self.root.mainloop()


def launch() -> None:
    """Convenience entry point for launching the calculator app."""
    CalculatorApp().run()


if __name__ == "__main__":
    launch()
