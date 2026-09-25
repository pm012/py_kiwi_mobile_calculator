import pytest
from src.strategies.programmer import (
    BitwiseAndStrategy,
    BitwiseOrStrategy,
    BitwiseXorStrategy,
    BitwiseNotStrategy,
    LeftShiftStrategy,
    RightShiftStrategy,
    ModuloStrategy,
)


def test_bitwise_and():
    strategy = BitwiseAndStrategy()
    assert strategy.execute(12, 5) == 4.0  # 1100 & 0101 = 0100


def test_bitwise_or():
    strategy = BitwiseOrStrategy()
    assert strategy.execute(12, 5) == 13.0  # 1100 | 0101 = 1101


def test_bitwise_xor():
    strategy = BitwiseXorStrategy()
    assert strategy.execute(12, 5) == 9.0  # 1100 ^ 0101 = 1001


def test_bitwise_not():
    strategy = BitwiseNotStrategy()
    assert strategy.execute(0) == -1.0


def test_shifts():
    assert LeftShiftStrategy().execute(2, 3) == 16.0  # 2 << 3
    assert RightShiftStrategy().execute(16, 2) == 4.0  # 16 >> 2


def test_modulo():
    strategy = ModuloStrategy()
    assert strategy.execute(10, 3) == 1.0
    with pytest.raises(ZeroDivisionError):
        strategy.execute(10, 0)