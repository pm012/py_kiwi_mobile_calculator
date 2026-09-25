import re

def extract_last_operand(expression: str) -> tuple[str, str]:
    """
    Parses the expression from the end and returns a tuple:
    (base_expression, operand_for_unary_operation)
    
    Приклади:
    - "1+25"        -> ("1+", "25")
    - "1+(2+3)"     -> ("1+", "(2+3)")
    - "1+(2*(3+4))" -> ("1+", "(2*(3+4))")
    - "49"          -> ("", "49")
    """
    expr = expression.strip()
    if not expr:
        return "", ""

    # Case1:  Expression ends with a closing parenthesis ')'
    if expr.endswith(')'):
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            char = expr[i]
            if char == ')':
                depth += 1
            elif char == '(':
                depth -= 1
                if depth == 0:
                    base_part = expr[:i]
                    operand_part = expr[i:]
                    return base_part, operand_part
        # If the parenthesis is unmatched, take the whole expression as the operand
        return "", expr

    # Випадок 2: Вираз закінчується числом (включаючи дробові)
    match = re.search(r'(\d+(?:\.\d+)?)$', expr)
    if match:
        start_idx = match.start(1)
        base_part = expr[:start_idx]
        operand_part = match.group(1)
        return base_part, operand_part

    # Case3:  Expression ends with a binary operator (e.g., "1+")
    return expr, ""