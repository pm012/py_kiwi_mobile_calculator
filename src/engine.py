import ast
import operator as op
from typing import Dict, Type
from src.strategies import (
    OperationStrategy,
    AdditionStrategy,
    SubtractionStrategy,
    MultiplicationStrategy,
    DivisionStrategy
)


class SafeEvaluator(ast.NodeVisitor):
    """Безпечний AST-парсер для вираження математичних виразів."""
    ALLOWED_OPERATORS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    def visit_Num(self, node):  # Для сумісності з новішими версіями Python (Constant)
        return node.n

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)

        if op_type == ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero")

        if op_type in self.ALLOWED_OPERATORS:
            return self.ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in self.ALLOWED_OPERATORS:
            return self.ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    def eval(self, expr: str) -> float:
        try:
            node = ast.parse(expr, mode='eval')
            return self.visit(node.body)
        except (SyntaxError, TypeError) as e:
            raise ValueError(f"Invalid expression: {expr}") from e


class CalculatorEngine:
    """Бізнес-логіка калькулятора."""
    def __init__(self):
        self.evaluator = SafeEvaluator()
        self.strategies: Dict[str, OperationStrategy] = {
            '+': AdditionStrategy(),
            '-': SubtractionStrategy(),
            '*': MultiplicationStrategy(),
            '/': DivisionStrategy()
        }
        self.last_operator = ""
        self.last_operand = ""
        self.last_result = None

    def evaluate(self, expression: str) -> str:
        expression = expression.strip()

        # Обробка повторного "= "
        if not expression and self.last_result is not None:
            if self.last_operator and self.last_operand:
                expression = f"{self.last_result}{self.last_operator}{self.last_operand}"

        try:
            result = self.evaluator.eval(expression)
            
            # Збереження даних для повторного обчислення
            for op_char in self.strategies.keys():
                if op_char in expression[1:]:  # Пропускаємо унарний мінус
                    parts = expression.rsplit(op_char, 1)
                    if len(parts) == 2:
                        self.last_operator = op_char
                        self.last_operand = parts[1]
                        break

            self.last_result = result
            return self._format_result(result)
        except (ZeroDivisionError, ValueError, MemoryError):
            return "ERROR"

    def toggle_sign(self, text: str) -> str:
        text = text.strip()
        if not text or text == "0":
            return text
        if text.startswith("-"):
            return text[1:]
        return "-" + text

    def convert_percent(self, text: str) -> str:
        text = text.strip()
        try:
            if "%" in text:
                parts = text.split("%")
                if len(parts) == 2 and parts[0] and parts[1]:
                    x, y = float(parts[0]), float(parts[1])
                    return self._format_result((x / 100) * y)
            elif text.endswith("%") or text.replace(".", "", 1).isdigit():
                clean_text = text.rstrip("%")
                val = float(clean_text)
                return self._format_result(val / 100)
        except ValueError:
            pass
        return "ERROR"

    def _format_result(self, val: float) -> str:
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(round(val, 8))