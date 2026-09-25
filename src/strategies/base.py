from abc import ABC, abstractmethod


class OperationStrategy(ABC):
    """Base abstract class for all calculation strategies."""

    @abstractmethod
    def execute(self, *args: float) -> float:
        pass
