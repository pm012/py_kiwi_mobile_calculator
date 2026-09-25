# src/strategies/programmer.py
import math
from src.strategies.base import OperationStrategy


class BitwiseAndStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return float(int(a) & int(b))


class BitwiseOrStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return float(int(a) | int(b))


class BitwiseXorStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return float(int(a) ^ int(b))


class BitwiseNotStrategy(OperationStrategy):
    def execute(self, x: float) -> float:
        return float(~int(x))


class LeftShiftStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return float(int(a) << int(b))


class RightShiftStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return float(int(a) >> int(b))


class ModuloStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        if int(b) == 0:
            raise ZeroDivisionError("Modulo by zero")
        return float(int(a) % int(b))