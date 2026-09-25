import os
# Switch off Kivy graphical windows for tests
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import pytest
from kivy.clock import Clock
from src.ui import CalculatorUI
from src.engine import CalculatorEngine


@pytest.fixture
def ui():
    return CalculatorUI(engine=CalculatorEngine())


def test_ui_initial_state(ui):
    assert ui.result.text == "0"


def test_ui_button_clicks_number_and_clear(ui):
    # Simulation of pressing the '7' button
    class MockInstance:
        text = "7"

    ui.button_click(MockInstance())
    assert ui.result.text == "7"

    # Simulation of pressing 'C' button to clear the display
    MockInstance.text = "C"
    ui.button_click(MockInstance())
    assert ui.result.text == "0"


def test_ui_button_click_operations(ui):
    class MockInstance:
        text = ""

    # Simulation of input: 5 + 3 =
    for btn in ["5", "+", "3", "="]:
        MockInstance.text = btn
        ui.button_click(MockInstance())

    assert ui.result.text == "8"


def test_ui_toggle_sign_and_percent(ui):
    class MockInstance:
        text = "9"

    ui.button_click(MockInstance())
    
    MockInstance.text = "+/-"
    ui.button_click(MockInstance())
    assert ui.result.text == "-9"

    MockInstance.text = "%"
    ui.button_click(MockInstance())
    assert ui.result.text == "-0.09"