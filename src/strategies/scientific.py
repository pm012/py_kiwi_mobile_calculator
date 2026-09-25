from src.strategies.base import OperationStrategy
import math

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