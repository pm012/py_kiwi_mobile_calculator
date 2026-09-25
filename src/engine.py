# src/engine.py
import ast
import math
import operator as op
import re
from typing import Dict

from src.strategies.base import OperationStrategy
from src.strategies.basic import (
    AdditionStrategy,
    SubtractionStrategy,
    MultiplicationStrategy,
    DivisionStrategy,
    PowerStrategy,
)
from src.strategies.scientific import (
    SquareRootStrategy,
    SquareStrategy,
    SinStrategy,
    CosStrategy,
    TanStrategy,
    Log10Strategy,
    NaturalLogStrategy,
    FactorialStrategy,
)
from src.strategies.programmer import (
    BitwiseAndStrategy,
    BitwiseOrStrategy,
    BitwiseXorStrategy,
    BitwiseNotStrategy,
    LeftShiftStrategy,
    RightShiftStrategy,
    ModuloStrategy,
)


class SafeEvaluator(ast.NodeVisitor):
    """Safe AST parser for expressions supporting math functions, constants, and bitwise ops."""

    ALLOWED_OPERATORS = {
        # Standard arithmetic operators
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.Mod: op.mod,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
        # Bitwise operators
        ast.BitAnd: op.and_,
        ast.BitOr: op.or_,
        ast.BitXor: op.xor,
        ast.LShift: op.lshift,
        ast.RShift: op.rshift,
        ast.Invert: op.invert,
    }

    ALLOWED_FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "log": math.log10,
        "ln": math.log,
        "fact": lambda x: float(math.factorial(int(x))),
    }

    ALLOWED_NAMES = {
        "pi": math.pi,
        "e": math.e,
    }

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    def visit_Name(self, node):
        if node.id in self.ALLOWED_NAMES:
            return self.ALLOWED_NAMES[node.id]
        raise ValueError(f"Unsupported name: {node.id}")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)

        if op_type == ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero")
        if op_type == ast.Mod and right == 0:
            raise ZeroDivisionError("Modulo by zero")

        if op_type in self.ALLOWED_OPERATORS:
            return self.ALLOWED_OPERATORS[op_type](int(left) if op_type in {ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift} else left, 
                                                  int(right) if op_type in {ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift} else right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in self.ALLOWED_OPERATORS:
            val = int(operand) if op_type == ast.Invert else operand
            return self.ALLOWED_OPERATORS[op_type](val)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.ALLOWED_FUNCTIONS:
            args = [self.visit(arg) for arg in node.args]
            return self.ALLOWED_FUNCTIONS[node.func.id](*args)
        raise ValueError("Unsupported function call")

    def eval(self, expr: str) -> float:
        try:
            node = ast.parse(expr, mode="eval")
            return self.visit(node.body)
        except (SyntaxError, TypeError, MemoryError, KeyError) as e:
            raise ValueError(f"Invalid expression: {expr}") from e


class CalculatorEngine:
    """Engine for the calculator with support for standard, scientific, and programmer strategies."""

    def __init__(self):
        self.evaluator = SafeEvaluator()
        self.strategies: Dict[str, OperationStrategy] = {
            "+": AdditionStrategy(),
            "-": SubtractionStrategy(),
            "*": MultiplicationStrategy(),
            "/": DivisionStrategy(),
            "^": PowerStrategy(),
            "sqrt": SquareRootStrategy(),
            "sqr": SquareStrategy(),
            "sin": SinStrategy(),
            "cos": CosStrategy(),
            "tan": TanStrategy(),
            "log": Log10Strategy(),
            "ln": NaturalLogStrategy(),
            "fact": FactorialStrategy(),
            "AND": BitwiseAndStrategy(),
            "OR": BitwiseOrStrategy(),
            "XOR": BitwiseXorStrategy(),
            "NOT": BitwiseNotStrategy(),
            "<<": LeftShiftStrategy(),
            ">>": RightShiftStrategy(),
            "MOD": ModuloStrategy(),
        }
        self.last_operator = ""
        self.last_operand = ""
        self.last_result = None

    def evaluate(self, expression: str) -> str:
        expression = expression.strip()

        if not expression:
            if self.last_result is not None and self.last_operator and self.last_operand:
                expression = f"{self.last_result}{self.last_operator}{self.last_operand}"
            else:
                return ""

        # Correct leading zeros before parentheses:
        # "0(3+5)*9" -> "(3+5)*9"
        # "00(2+2)"  -> "(2+2)"
        # Leave "0" alone (i.e., "0" without parentheses remains "0")
        expression = re.sub(r'^0+(?=\()', '', expression)

        # Conversion of operators to Python AST syntax
        formatted_expr = (
            expression.replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
            .replace("XOR", "^")
            .replace("AND", "&")
            .replace("OR", "|")
            .replace("MOD", "%")
        )

        try:
            match = re.search(r'(\*\*|[\+\-\*/&\|\^%]|<<|>>)\s*([\d.]+)$', formatted_expr)
            if match:
                self.last_operator = match.group(1)
                self.last_operand = match.group(2)

            result = self.evaluator.eval(formatted_expr)
            self.last_result = result
            return self._format_result(result)
        except (ZeroDivisionError, ValueError, OverflowError):
            return "ERROR"
    def execute_scientific_unary(self, op_code: str, value_str: str) -> str:
        if op_code not in self.strategies:
            return "ERROR"
        try:
            val = float(value_str)
            res = self.strategies[op_code].execute(val)
            self.last_result = res
            return self._format_result(res)
        except (ValueError, ZeroDivisionError, OverflowError):
            return "ERROR"

    def execute_programmer_unary(self, op_code: str, value_str: str) -> str:
        """Handle unary operations and number base conversions (BIN, HEX, OCT, NOT)."""
        try:
            clean_str = value_str.strip().lower()
            
            # Підтримка читання 0x/0X, 0b/0B, 0o/0O
            if clean_str.startswith(("0x", "0b", "0o")):
                val = int(clean_str, 0)
            else:
                val = int(float(clean_str))
            
            if op_code == "NOT":
                res = self.strategies["NOT"].execute(val)
                return str(int(res))
            elif op_code == "BIN":
                return bin(val)
            elif op_code == "HEX":
                # returns '0XFF' (0X + верхній регістр)
                raw_hex = hex(val)
                return f"0X{raw_hex[2:].upper()}" if raw_hex.startswith("0x") else raw_hex.upper()
            elif op_code == "OCT":
                return oct(val)
            return "ERROR"
        except (ValueError, TypeError, OverflowError):
            return "ERROR"
        
    def toggle_sign(self, text: str) -> str:
        text = text.strip()
        if not text or text in {"0", "ERROR"}:
            return text
        if text.startswith("-"):
            return text[1:]
        return "-" + text

    def convert_percent(self, text: str) -> str:
        text = text.strip()
        try:
            if "%" in text and not text.endswith("%"):
                parts = text.split("%")
                if len(parts) == 2:
                    x, y = float(parts[0]), float(parts[1])
                    return self._format_result((x / 100) * y)

            clean_text = text.rstrip("%")
            val = float(clean_text)
            return self._format_result(val / 100)
        except ValueError:
            return "ERROR"

    def _format_result(self, val: float) -> str:
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(round(val, 8))