from abc import ABC, abstractmethod
import operator


class OperationStrategy(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass


class AdditionStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return operator.add(a, b)


class SubtractionStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return operator.sub(a, b)


class MultiplicationStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        return operator.mul(a, b)


class DivisionStrategy(OperationStrategy):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return operator.truediv(a, b)