import pytest
from src.engine import CalculatorEngine, SafeEvaluator


@pytest.fixture
def engine():
    return CalculatorEngine()


def test_safe_evaluator_basic():
    evaluator = SafeEvaluator()
    assert evaluator.eval("2+2") == 4
    assert evaluator.eval("10 - 4 * 2") == 2
    assert evaluator.eval("-5 + 3") == -2


def test_safe_evaluator_invalid_expr():
    evaluator = SafeEvaluator()
    # "2 + * 2" є невалідним виразом для AST
    with pytest.raises(ValueError):
        evaluator.eval("2 + * 2")


def test_engine_evaluate_success(engine):
    assert engine.evaluate("10+20") == "30"
    assert engine.evaluate("10 / 4") == "2.5"


def test_engine_zero_division(engine):
    assert engine.evaluate("5/0") == "ERROR"


def test_engine_invalid_syntax(engine):
    assert engine.evaluate("5+*2") == "ERROR"


def test_toggle_sign(engine):
    assert engine.toggle_sign("10") == "-10"
    assert engine.toggle_sign("-10") == "10"
    assert engine.toggle_sign("0") == "0"
    assert engine.toggle_sign("") == ""


def test_convert_percent(engine):
    assert engine.convert_percent("50%") == "0.5"
    assert engine.convert_percent("100%20") == "20"
    assert engine.convert_percent("invalid") == "ERROR"


def test_repeat_equal_operation(engine):
    engine.evaluate("10+5")
    assert engine.last_operator == "+"
    assert engine.last_operand == "5"

def test_safe_evaluator_unsupported_constant():
    evaluator = SafeEvaluator()
    # Текст замість числа у вузлі
    with pytest.raises(ValueError, match="Unsupported constant type"):
        evaluator.eval("'hello'")


def test_safe_evaluator_unary_operators():
    evaluator = SafeEvaluator()
    assert evaluator.eval("+5") == 5
    assert evaluator.eval("-10") == -10


def test_engine_repeat_equal_without_last_result(engine):
    # Empty input without a saved result returns an empty string
    assert engine.evaluate("") == ""
    
    # After successful calculation, a repeated empty expression applies the last operator
    engine.evaluate("10+5")
    assert engine.evaluate("") == "20"  # 15 + 5