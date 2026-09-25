# tests/test_ui.py
import os

os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import pytest
from src.ui import CalculatorUI
from src.helpers import extract_last_operand
from src.engine import CalculatorEngine


class MockButton:
    def __init__(self, text: str):
        self.text = text


@pytest.fixture
def ui():
    return CalculatorUI(engine=CalculatorEngine())


def test_ui_initial_state(ui):
    assert ui.result.text == "0"
    assert ui.current_mode == "basic"


def test_ui_button_clicks_number_and_clear(ui):
    ui.button_click(MockButton("7"))
    assert ui.result.text == "7"

    ui.button_click(MockButton("C"))
    assert ui.result.text == "0"


def test_ui_button_click_operations(ui):
    for btn in ["5", "+", "3", "="]:
        ui.button_click(MockButton(btn))

    assert ui.result.text == "8"


def test_ui_toggle_sign_and_percent(ui):
    ui.button_click(MockButton("9"))
    
    ui.button_click(MockButton("+/-"))
    assert ui.result.text == "-9"

    ui.button_click(MockButton("%"))
    assert ui.result.text == "-0.09"


def test_ui_mode_switching(ui):
    # Switch to scientific mode
    ui.set_mode("scientific")
    assert ui.current_mode == "scientific"

    # Switch to programmer mode
    ui.set_mode("programmer")
    assert ui.current_mode == "programmer"

    # Return to basic mode
    ui.set_mode("basic")
    assert ui.current_mode == "basic"


def test_ui_scientific_operations(ui):
    ui.set_mode("scientific")
    
    # Вводимо 16 і натискаємо sqrt
    ui.button_click(MockButton("1"))
    ui.button_click(MockButton("6"))
    ui.button_click(MockButton("sqrt"))
    assert ui.result.text == "4"


def test_ui_programmer_operations(ui):
    ui.set_mode("programmer")

    # Enter 10 and convert to BIN
    ui.button_click(MockButton("1"))
    ui.button_click(MockButton("0"))
    ui.button_click(MockButton("BIN"))
    assert ui.result.text == "0b1010"

    # Bitwise AND operation: 12 AND 5 =
    ui.button_click(MockButton("C"))
    for btn in ["12", "AND", "5", "="]:
        ui.button_click(MockButton(btn))
    assert ui.result.text == "4"

def test_extract_last_operand_number():
    base, op = extract_last_operand("1+25")
    assert base == "1+"
    assert op == "25"

def test_extract_last_operand_parentheses():
    base, op = extract_last_operand("1+(3+6)")
    assert base == "1+"
    assert op == "(3+6)"

def test_extract_last_operand_nested_parentheses():
    base, op = extract_last_operand("2*(1+(3+6))")
    assert base == "2*"
    assert op == "(1+(3+6))"

def test_ui_scientific_unary_parentheses(ui):
    ui.result.text = "1+(3+6)"
    
    # Emulate pressing the sqrt button
    class MockButton:
        text = "sqrt"
        
    ui.button_click(MockButton())
    
    # Expect "1+3" or "1+3.0"
    assert ui.result.text in ["1+3", "1+3.0"]