from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from src.engine import CalculatorEngine

Window.size = (400, 600)


class CalculatorUI(BoxLayout):
    def __init__(self, engine: CalculatorEngine = None, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=10, **kwargs)
        self.engine = engine or CalculatorEngine()
        self.is_scientific = False

        # Display
        self.result = TextInput(
            font_size=40,
            size_hint_y=0.18,
            readonly=True,
            halign="right",
            multiline=False,
            background_color=[0.2, 0.2, 0.2, 1],
            foreground_color=[1, 1, 1, 1],
            text="0"
        )
        self.add_widget(self.result)

        # Mode toggle
        self.mode_btn = Button(
            text="Switch to Scientific Mode",
            size_hint_y=0.08,
            background_color=[0.2, 0.6, 0.8, 1],
            on_press=self.toggle_mode
        )
        self.add_widget(self.mode_btn)

        # Keyboard container
        self.keypad_container = BoxLayout(orientation='vertical', size_hint_y=0.74)
        self.add_widget(self.keypad_container)

        self._render_keypad()

    def toggle_mode(self, instance):
        self.is_scientific = not self.is_scientific
        self.mode_btn.text = "Switch to Basic Mode" if self.is_scientific else "Switch to Scientific Mode"
        Window.size = (500, 650) if self.is_scientific else (400, 600)
        self._render_keypad()

    def _render_keypad(self):
        self.keypad_container.clear_widgets()

        if self.is_scientific:
            sci_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.3)
            sci_buttons = ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', '^', '(', ')']
            for btn_text in sci_buttons:
                button = Button(
                    text=btn_text,
                    font_size=20,
                    background_color=[0.4, 0.4, 0.6, 1],
                    on_press=self.button_click
                )
                sci_grid.add_widget(button)
            self.keypad_container.add_widget(sci_grid)

        # Base grid
        base_grid = GridLayout(cols=4, spacing=5, size_hint_y=0.7 if self.is_scientific else 1.0)
        base_buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '00', '.', '=']
        ]

        for row in base_buttons:
            for item in row:
                button = Button(
                    text=item,
                    font_size=26,
                    background_color=self._get_button_color(item),
                    on_press=self.button_click
                )
                base_grid.add_widget(button)
        self.keypad_container.add_widget(base_grid)

    def _get_button_color(self, label: str):
        if label in {'C', '+/-', '%'}:
            return [0.6, 0.6, 0.6, 1]
        elif label in {"/", "*", "-", "+", "="}:
            return [0.988, 0.631, 0.012, 1]
        return [0.3, 0.3, 0.3, 1]

    def button_click(self, instance):
        text = instance.text

        if text == "C":
            self.result.text = "0"
            self.engine = CalculatorEngine()
        elif text == "=":
            self.result.text = self.engine.evaluate(self.result.text)
        elif text == "+/-":
            self.result.text = self.engine.toggle_sign(self.result.text)
        elif text == "%":
            self.result.text = self.engine.convert_percent(self.result.text)
        elif text in {'sin', 'cos', 'tan', 'log', 'ln', 'sqrt'}:
            # Calls for unary strategies through the engine method
            self.result.text = self.engine.execute_scientific_unary(text, self.result.text)
        else:
            self.append_text(text)

    def append_text(self, text: str):
        if self.result.text in {"0", "ERROR"} and text not in {"+", "-", "*", "/", ".", "^", ")", "("}:
            self.result.text = text
        else:
            self.result.text += text