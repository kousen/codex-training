"""Usage example for the calculator Strategy pattern."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    """Run a short calculator Strategy pattern example."""
    from src.calculator import (
        AddOperation,
        Calculator,
        DivideOperation,
        MultiplyOperation,
    )

    calculator = Calculator(AddOperation())
    print(f"2 + 3 = {calculator.calculate(2, 3)}")

    calculator.set_operation(MultiplyOperation())
    print(f"6 * 7 = {calculator.calculate(6, 7)}")

    calculator.set_operation(DivideOperation())
    print(f"10 / 2 = {calculator.calculate(10, 2)}")


if __name__ == "__main__":
    main()
