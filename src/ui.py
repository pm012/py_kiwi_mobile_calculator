# src/ui.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from src.engine import CalculatorEngine


class CalculatorUI(BoxLayout):
    def __init__(self, engine: CalculatorEngine = None, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=10, **kwargs)
        self.engine = engine or CalculatorEngine()
        self.current_mode = "basic"

        # Дисплей
        self.result = TextInput(
            font_size=36,
            size_hint_y=0.15,
            readonly=True,
            halign="right",
            multiline=False,
            background_color=[0.2, 0.2, 0.2, 1],
            foreground_color=[1, 1, 1, 1],
            text="0"
        )
        self.add_widget(self.result)

        # Панель навігації
        self.mode_panel = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=0.08)
        self.add_widget(self.mode_panel)

        # Клавіатура
        self.keypad_container = BoxLayout(orientation='vertical', size_hint_y=0.77)
        self.add_widget(self.keypad_container)

        self._update_layout()

    def set_mode(self, mode: str):
        if self.current_mode == mode:
            return
        
        self.current_mode = mode
        
        # Очищення екрану та скидання стану двигуна при зміні режиму
        self.result.text = "0"
        self.engine = CalculatorEngine()
        
        self._update_layout()

    def _update_layout(self):
        if self.current_mode == "scientific":
            Window.size = (500, 650)
        elif self.current_mode == "programmer":
            Window.size = (520, 650)
        else:
            Window.size = (400, 600)

        self.mode_panel.clear_widgets()
        modes = [("Basic", "basic"), ("Scientific", "scientific"), ("Programmer", "programmer")]
        
        for label, mode_key in modes:
            btn = Button(
                text=label,
                font_size=14,
                background_color=[0.2, 0.7, 0.5, 1] if self.current_mode == mode_key else [0.3, 0.3, 0.3, 1],
                disabled=(self.current_mode == mode_key)
            )
            btn.bind(on_press=lambda instance, m=mode_key: self.set_mode(m))
            self.mode_panel.add_widget(btn)

        self._render_keypad()

    def _render_keypad(self):
        self.keypad_container.clear_widgets()

        if self.current_mode == "scientific":
            sci_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.3)
            sci_buttons = ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', '^', '(', ')']
            for btn_text in sci_buttons:
                button = Button(text=btn_text, font_size=18, background_color=[0.4, 0.4, 0.6, 1], on_press=self.button_click)
                sci_grid.add_widget(button)
            self.keypad_container.add_widget(sci_grid)

        elif self.current_mode == "programmer":
            prog_grid = GridLayout(cols=4, spacing=5, size_hint_y=0.35)
            prog_buttons = ['AND', 'OR', 'XOR', 'NOT', '<<', '>>', 'MOD', 'BIN', 'HEX', 'OCT', '(', ')']
            for btn_text in prog_buttons:
                button = Button(text=btn_text, font_size=16, background_color=[0.5, 0.3, 0.5, 1], on_press=self.button_click)
                prog_grid.add_widget(button)
            self.keypad_container.add_widget(prog_grid)

        base_grid = GridLayout(cols=4, spacing=5, size_hint_y=0.65 if self.current_mode != "basic" else 1.0)
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
                    font_size=24,
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
            self.result.text = self.engine.execute_scientific_unary(text, self.result.text)
        elif text in {'NOT', 'BIN', 'HEX', 'OCT'}:
            self.result.text = self.engine.execute_programmer_unary(text, self.result.text)
        else:
            self.append_text(text)

    def append_text(self, text: str):
        if self.result.text in {"0", "ERROR"} and text not in {"+", "-", "*", "/", ".", "^", ")", "(", "AND", "OR", "XOR", "<<", ">>", "MOD"}:
            self.result.text = text
        else:
            self.result.text += text