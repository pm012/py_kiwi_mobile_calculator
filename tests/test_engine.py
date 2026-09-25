import pytest
from src.engine import CalculatorEngine, SafeEvaluator


@pytest.fixture
def engine():
    return CalculatorEngine()

@pytest.fixture
def evaluator():
    return SafeEvaluator()


def test_leading_zero_with_parentheses(engine):
    assert engine.evaluate("0(3+5)*9") == "72"
    assert engine.evaluate("(3+5)*9") == "72"
    assert engine.evaluate("00(2+2)") == "4"

def test_bitwise_operations(engine):
    assert engine.evaluate("8 XOR 5") == "13"
    assert engine.evaluate("8XOR5") == "13"
    assert engine.evaluate("12 AND 5") == "4"
    assert engine.evaluate("12 OR 5") == "13"
    assert engine.evaluate("8 << 2") == "32"
    assert engine.evaluate("32 >> 2") == "8"
    assert engine.evaluate("10 MOD 3") == "1"

def test_programmer_unary_operations(engine):
    # NOT
    assert engine.execute_programmer_unary("NOT", "12") == "-13"
    assert engine.execute_programmer_unary("NOT", "0b1100") == "-13"
    
    # Conversions
    assert engine.execute_programmer_unary("HEX", "26") == "0X1A"
    assert engine.execute_programmer_unary("OCT", "26") == "0o32"
    assert engine.execute_programmer_unary("BIN", "26") == "0b11010"
    
    # Unsupported operation or invalid input
    assert engine.execute_programmer_unary("UNKNOWN", "10") == "ERROR"
    assert engine.execute_programmer_unary("BIN", "invalid_number") == "ERROR"


def test_safe_evaluator_basic():
    evaluator = SafeEvaluator()
    assert evaluator.eval("2+2") == 4
    assert evaluator.eval("10 - 4 * 2") == 2
    assert evaluator.eval("-5 + 3") == -2
    assert evaluator.eval("2 + 2 * 2") == 6
    assert evaluator.eval("(10 - 2) / 4") == 2.0


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
    assert engine.toggle_sign("12") == "-12"
    assert engine.toggle_sign("-12") == "12"
    assert engine.toggle_sign("0") == "0"
    assert engine.toggle_sign("ERROR") == "ERROR"
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


def test_repeat_last_operation(engine):
    assert engine.evaluate("10 + 5") == "15"
    assert engine.evaluate("") == "20"
    assert engine.evaluate("") == "25"

def test_engine_repeat_equal_without_last_result(engine):
    # Empty input without a saved result returns an empty string
    assert engine.evaluate("") == ""
    
    # After successful calculation, a repeated empty expression applies the last operator
    engine.evaluate("10+5")
    assert engine.evaluate("") == "20"  # 15 + 5

def test_safe_evaluator_bitwise():
    evaluator = SafeEvaluator()
    assert evaluator.eval("12 & 5") == 4
    assert evaluator.eval("12 | 5") == 13
    assert evaluator.eval("2 << 3") == 16


def test_engine_evaluate_expression(engine):
    assert engine.evaluate("10 + 5 × 2") == "20"
    assert engine.evaluate("12 AND 5") == "4"
    assert engine.evaluate("10 MOD 3") == "1"


def test_scientific_unary_operations(engine):
    assert engine.execute_scientific_unary("sqrt", "16") == "4"
    assert engine.execute_scientific_unary("sqr", "5") == "25"
    assert engine.execute_scientific_unary("sin", "90") == "1"
    assert engine.execute_scientific_unary("cos", "0") == "1"
    assert engine.execute_scientific_unary("fact", "5") == "120"
    
    # Error cases
    assert engine.execute_scientific_unary("sqrt", "-1") == "ERROR"
    assert engine.execute_scientific_unary("unknown_op", "5") == "ERROR"
    assert engine.execute_scientific_unary("sqrt", "-1") == "ERROR"


def test_engine_programmer_unary(engine):
    assert engine.execute_programmer_unary("BIN", "10") == "0b1010"
    assert engine.execute_programmer_unary("HEX", "255") == "0XFF"
    assert engine.execute_programmer_unary("OCT", "8") == "0o10"
    assert engine.execute_programmer_unary("NOT", "0") == "-1"


def test_engine_errors(engine):
    assert engine.evaluate("10 / 0") == "ERROR"
    assert engine.evaluate("10 MOD 0") == "ERROR"
    assert engine.evaluate("2 + (3 * ") == "ERROR"
    assert engine.evaluate("unsupported_var + 5") == "ERROR"

def test_engine_programmer_chained_conversions(engine):
    # 26 -> HEX -> OCT -> BIN
    hex_val = engine.execute_programmer_unary("HEX", "26")
    assert hex_val == "0X1A"  # Оновлено префікс на 0X
    
    oct_val = engine.execute_programmer_unary("OCT", hex_val)
    assert oct_val == "0o32"
    
    bin_val = engine.execute_programmer_unary("BIN", oct_val)
    assert bin_val == "0b11010"

def test_evaluator_math_functions_and_constants(engine):
    assert engine.evaluate("sqrt(49)") == "7"
    assert engine.evaluate("pi") != "ERROR"
    assert engine.evaluate("e") != "ERROR"
    assert engine.evaluate("fact(4)") == "24"


# Additional tests for SafeEvaluator to ensure it raises exceptions for unsupported operations
def test_safe_evaluator_direct_exceptions(evaluator):
    with pytest.raises(ValueError, match="Unsupported constant type"):
        evaluator.eval("'string_constant'")

    with pytest.raises(ValueError, match="Unsupported name"):
        evaluator.eval("unknown_variable")

    with pytest.raises(ValueError, match="Unsupported function call"):
        evaluator.eval("non_existing_func(5)")