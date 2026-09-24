from kivy.app import App
from src.ui import CalculatorUI


class CalculatorApp(App):
    def build(self):
        return CalculatorUI()


if __name__ == "__main__":
    CalculatorApp().run()