from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from src.engine import CalculatorEngine

Window.size = (300, 500)


class CalculatorUI(BoxLayout):
    def __init__(self, engine: CalculatorEngine = None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.engine = engine or CalculatorEngine()

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
                    background_color=self._get_button_color(item),
                    on_press=self.button_click
                )
                grid.add_widget(button)
        self.add_widget(grid)

    def _get_button_color(self, label: str):
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
            self.result.text = self.engine.evaluate(self.result.text)
        elif text == "+/-":
            self.result.text = self.engine.toggle_sign(self.result.text)
        elif text == "%":
            self.result.text = self.engine.convert_percent(self.result.text)
        else:
            self.append_text(text)

    def clear(self):
        self.result.text = "0"
        self.engine = CalculatorEngine()

    def append_text(self, text: str):
        if self.result.text in {"0", "ERROR"} and text not in {"+", "-", "*", "/", "."}:
            self.result.text = text
        else:
            self.result.text += text