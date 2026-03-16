"""Calculator facade that uses operation strategies."""

from __future__ import annotations

from dataclasses import dataclass, field

from calculator.operations import OperationName, OperationStrategy, StrategyFactory
from calculator.validators import Number


@dataclass(slots=True)
class Calculator:
    """Evaluate arithmetic expressions using pluggable strategies."""

    _factory: type[StrategyFactory] = field(default=StrategyFactory)

    def calculate(
        self, operation: OperationName | str, left: Number, right: Number
    ) -> float:
        """Calculate a result for the supplied operation and operands."""

        strategy: OperationStrategy = self._factory.create(operation)
        return strategy.execute(left, right)
