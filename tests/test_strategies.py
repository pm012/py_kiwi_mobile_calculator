import pytest
from src.strategies import (
    OperationStrategy,
    AdditionStrategy,
    SubtractionStrategy,
    MultiplicationStrategy,
    DivisionStrategy
)


def test_addition():
    strategy = AdditionStrategy()
    assert strategy.execute(5, 3) == 8
    assert strategy.execute(-1, 1) == 0


def test_subtraction():
    strategy = SubtractionStrategy()
    assert strategy.execute(10, 4) == 6
    assert strategy.execute(0, 5) == -5


def test_multiplication():
    strategy = MultiplicationStrategy()
    assert strategy.execute(4, 3) == 12
    assert strategy.execute(-2, 3) == -6


def test_division():
    strategy = DivisionStrategy()
    assert strategy.execute(10, 2) == 5
    assert strategy.execute(7, 2) == 3.5


def test_division_by_zero():
    strategy = DivisionStrategy()
    with pytest.raises(ZeroDivisionError):
        strategy.execute(5, 0)


def test_abstract_strategy_instantiation():
    """Перевірка заборони створення екземпляра абстрактного класу."""
    with pytest.raises(TypeError):
        OperationStrategy()

    