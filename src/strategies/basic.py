from src.strategies.base import OperationStrategy
import math

# ==========================================
# Basic arithmetic strategies (Binary)
# ==========================================

class AdditionStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return a + b


class SubtractionStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return a - b


class MultiplicationStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return a * b


class DivisionStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b


class PowerStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return math.pow(a, b)