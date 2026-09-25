import math
from abc import ABC, abstractmethod


class OperationStrategy(ABC):
    """Base abstract class for all calculation strategies."""

    @abstractmethod
    def execute(self, *args: float) -> float:
        pass


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


# ==========================================
# Scientific strategies (Unary)
# ==========================================

class SquareRootStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        if x < 0:
            raise ValueError("Math domain error: negative root")
        return math.sqrt(x)


class SquareStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        return x ** 2


class SinStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        return math.sin(math.radians(x))


class CosStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        return math.cos(math.radians(x))


class TanStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        # Check for infinity for tan(90 + k*180)
        if math.isclose(abs(x % 180), 90, abs_tol=1e-9):
            raise ValueError("Tangent undefined for this angle")
        return math.tan(math.radians(x))


class Log10Strategy(OperationStrategy):
    def execute(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Math domain error: log10(x <= 0)")
        return math.log10(x)


class NaturalLogStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Math domain error: ln(x <= 0)")
        return math.log(x)


class FactorialStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        if x < 0 or not float(x).is_integer():
            raise ValueError("Factorial valid only for non-negative integers")
        return float(math.factorial(int(x)))