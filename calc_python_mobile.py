from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import re

Window.size = (300, 500)

class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.last_expression = ""  # Stores last valid expression
        self.last_operator = ""    # Stores last operator
        self.last_operand = ""     # Stores last operand for repeated calculations
        self.last_result = None    # Stores the last calculated result

        # Display field
        self.result = TextInput(
            font_size=45,
            size_hint_y=0.2,
            readonly=True,
            halign="right",
            multiline=False,
            background_color=[0.2, 0.2, 0.2, 1],
            foreground_color=[1, 1, 1, 1],
            text="0"
        )
        self.add_widget(self.result)

        # Create buttons
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '00', '.', '=']
        ]

        grid = GridLayout(cols=4, spacing=5, padding=10)
        for row in buttons:
            for item in row:
                button = Button(
                    text=item,
                    font_size=32,
                    background_color=self.set_button_color(item),
                    on_press=self.button_click
                )
                grid.add_widget(button)
        self.add_widget(grid)

    def set_button_color(self, label):
        if label in {'C', '+/-', '%'}:
            return [0.6, 0.6, 0.6, 1]
        elif label in {"/", "*", "-", "+", "="}:
            return [0.988, 0.631, 0.012, 1]
        return [0.3, 0.3, 0.3, 1]

    def button_click(self, instance):
        text = instance.text

        if text == "C":
            self.clear()
        elif text == "=":
            self.calculate()
        elif text == "+/-":
            self.toggle_neg()
        elif text == "%":
            self.convert_percent()
        else:
            self.append_text(text)

    def clear(self):
        """Clears the calculator display and resets memory."""
        self.result.text = "0"
        self.last_expression = ""
        self.last_operator = ""
        self.last_operand = ""
        self.last_result = None

    def append_text(self, text):
        """Handles number and operator input."""
        if self.result.text == "0" and text not in {"+", "-", "*", "/", ".", "+/-"}:
            self.result.text = text  # Replace "0" with new number
        else:
            self.result.text += text  # Append normally

    def calculate(self):
        """Evaluates the expression and enables repeated = operations."""
        try:
            expression = self.result.text.strip()

            # Handle repeated "=" functionality
            if not expression and self.last_result is not None:
                if self.last_operator and self.last_operand:
                    expression = f"{self.last_result} {self.last_operator} {self.last_operand}"
                else:
                    return  # Nothing to repeat

            # Extract last valid operator and operand
            match = re.search(r'([\d.]+)\s*([\+\-\*/])\s*([\d.]+)$', expression)
            if match:
                self.last_result = eval(expression)  # Store last result
                self.last_operator = match.group(2)  # Store last operator
                self.last_operand = match.group(3)   # Store last operand
                self.result.text = str(self.last_result)
            else:
                self.result.text = "ERROR"

        except Exception:
            self.result.text = "ERROR"

    def toggle_neg(self):
        """Toggles the sign of the current number."""
        if self.result.text and self.result.text != "0":
            self.result.text = self.result.text[1:] if self.result.text[0] == "-" else "-" + self.result.text

    def convert_percent(self):
        """Handles % calculations."""
        text = self.result.text.strip()

        # Case 1: "X % Y" → (X / 100) * Y
        if "%" in text and text.count("%") == 1:
            parts = text.split("%")
            if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                x, y = float(parts[0]), float(parts[1])
                self.result.text = str((x / 100) * y)
                return

        # Case 2: "X%" → X / 100
        elif text.endswith("%") and text[:-1].strip().isdigit():
            x = float(text[:-1])
            self.result.text = str(x / 100)
            return

        # Invalid % usage
        self.result.text = "ERROR"


class CalculatorApp(App):
    def build(self):
        return Calculator()


if __name__ == "__main__":
    CalculatorApp().run()
