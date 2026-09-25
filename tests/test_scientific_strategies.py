# tests/test_scientific_strategies.py
import math
import pytest
from src.strategies.scientific import (
    SquareRootStrategy,
    SquareStrategy,
    SinStrategy,
    CosStrategy,
    TanStrategy,
    Log10Strategy,
    NaturalLogStrategy,
    FactorialStrategy,
)
from src.strategies.basic import PowerStrategy


def test_square_root_strategy():
    strategy = SquareRootStrategy()
    assert strategy.execute(16) == 4.0
    assert strategy.execute(0) == 0.0

    with pytest.raises(ValueError):
        strategy.execute(-4)


def test_square_strategy():
    strategy = SquareStrategy()
    assert strategy.execute(5) == 25.0
    assert strategy.execute(-4) == 16.0


def test_trigonometric_strategies():
    sin_strat = SinStrategy()
    cos_strat = CosStrategy()
    tan_strat = TanStrategy()

    # sin(90°) = 1, cos(0°) = 1, tan(45°) = 1
    assert pytest.approx(sin_strat.execute(90)) == 1.0
    assert pytest.approx(sin_strat.execute(0)) == 0.0
    assert pytest.approx(cos_strat.execute(0)) == 1.0
    assert pytest.approx(tan_strat.execute(45)) == 1.0


def test_logarithm_strategies():
    log10_strat = Log10Strategy()
    ln_strat = NaturalLogStrategy()

    assert log10_strat.execute(100) == 2.0
    assert pytest.approx(ln_strat.execute(math.e)) == 1.0

    with pytest.raises(ValueError):
        log10_strat.execute(0)

    with pytest.raises(ValueError):
        ln_strat.execute(-5)


def test_factorial_strategy():
    strategy = FactorialStrategy()
    assert strategy.execute(5) == 120.0
    assert strategy.execute(0) == 1.0

    with pytest.raises(ValueError):
        strategy.execute(-1)

    with pytest.raises(ValueError):
        strategy.execute(3.5)


def test_power_strategy():
    strategy = PowerStrategy()
    assert strategy.execute(2, 3) == 8.0
    assert strategy.execute(5, 0) == 1.0
    assert strategy.execute(4, 0.5) == 2.0