"""계산 문항의 식을 다루는 도구.

식은 파이썬 산술 문법(2*k**2 + 1, (k+1)*(k+2)/2, factorial(k+1))으로 한 번만 적고,
찍을 KaTeX와 확인할 값을 모두 그 문자열에서 만든다. 그래서 문제집에 찍힌 식과 검증한 식이 어긋날 수 없다.

다항식 항등식은 변수마다 차수보다 많은 점에서 값이 같으면 항등식이다. same_polynomial은 변수마다
1부터 11까지 11개 점에서 값을 맞대므로, 변수마다 10차 이하인 다항식이면 이 확인이 곧 증명이다.
"""

from __future__ import annotations

import ast
import itertools
import math
from collections.abc import Callable, Sequence
from fractions import Fraction

Number = int | Fraction

ADD_LEVEL: int = 1
MULT_LEVEL: int = 2
UNARY_LEVEL: int = 3
POWER_LEVEL: int = 4
ATOM_LEVEL: int = 5

IDENTITY_POINTS: range = range(1, 12)

OPERATIONS: dict[type, Callable[[Fraction, Fraction], Fraction]] = {
    ast.Add: lambda left, right: left + right,
    ast.Sub: lambda left, right: left - right,
    ast.Mult: lambda left, right: left * right,
    ast.Div: lambda left, right: left / right,
    ast.Pow: lambda left, right: left ** int(right),
}


def _tree(expression: str) -> ast.expr:
    return ast.parse(expression, mode="eval").body


# ---- 값 ----

def evaluate(expression: str, **values: Number) -> Fraction:
    return _value(_tree(expression), {name: Fraction(number) for name, number in values.items()})


def _value(node: ast.expr, values: dict[str, Fraction]) -> Fraction:
    if isinstance(node, ast.Constant):
        return Fraction(node.value)
    if isinstance(node, ast.Name):
        return values[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_value(node.operand, values)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "factorial":
        return Fraction(math.factorial(int(_value(node.args[0], values))))
    if isinstance(node, ast.BinOp):
        return OPERATIONS[type(node.op)](_value(node.left, values), _value(node.right, values))
    raise ValueError(f"계산할 수 없는 식입니다: {ast.unparse(node)}")


def variables_of(*expressions: str) -> list[str]:
    names: set[str] = set()
    for expression in expressions:
        names |= {node.id for node in ast.walk(_tree(expression)) if isinstance(node, ast.Name) and node.id != "factorial"}
    return sorted(names)


def same_polynomial(left: str, right: str) -> bool:
    """두 다항식이 항등식으로 같은가. 변수마다 11개 점에서 값을 맞댄다."""
    names: list[str] = variables_of(left, right)
    return all(
        evaluate(left, **dict(zip(names, point))) == evaluate(right, **dict(zip(names, point)))
        for point in itertools.product(IDENTITY_POINTS, repeat=len(names))
    )


# ---- KaTeX ----

def latex(expression: str) -> str:
    return _latex(_tree(expression))[0]


def _latex(node: ast.expr) -> tuple[str, int]:
    """식의 KaTeX와 그 식의 결합 수준. 결합 수준은 괄호를 칠지 정하는 데 쓴다."""
    if isinstance(node, ast.Constant):
        return str(node.value), ATOM_LEVEL
    if isinstance(node, ast.Name):
        return node.id, ATOM_LEVEL
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return "-" + _wrapped(node.operand, POWER_LEVEL), UNARY_LEVEL
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "factorial":
        return _wrapped(node.args[0], ATOM_LEVEL) + "!", POWER_LEVEL
    if isinstance(node, ast.BinOp):
        return _binary_latex(node)
    raise ValueError(f"KaTeX로 옮길 수 없는 식입니다: {ast.unparse(node)}")


def _binary_latex(node: ast.BinOp) -> tuple[str, int]:
    if isinstance(node.op, (ast.Add, ast.Sub)):
        sign: str = "+" if isinstance(node.op, ast.Add) else "-"
        # 오른쪽의 덧셈, 뺄셈은 적은 사람이 일부러 묶은 것이므로 괄호를 살린다: k^2 + (2k + 1)
        right: str = _wrapped(node.right, MULT_LEVEL)
        return f"{_wrapped(node.left, ADD_LEVEL)} {sign} {right}", ADD_LEVEL
    if isinstance(node.op, ast.Mult):
        left: str = _wrapped(node.left, MULT_LEVEL)
        right = _wrapped(node.right, POWER_LEVEL)
        joined: str = left + right if right[0].isalpha() or right[0] == "(" or right.startswith(r"\left(") else rf"{left} \times {right}"
        return joined, MULT_LEVEL
    if isinstance(node.op, ast.Div):
        return rf"\frac{{{_latex(node.left)[0]}}}{{{_latex(node.right)[0]}}}", ATOM_LEVEL
    if isinstance(node.op, ast.Pow):
        exponent: str = _latex(node.right)[0]
        return f"{_wrapped(node.left, ATOM_LEVEL)}^{{{exponent}}}" if len(exponent) > 1 else f"{_wrapped(node.left, ATOM_LEVEL)}^{exponent}", POWER_LEVEL
    raise ValueError(f"KaTeX로 옮길 수 없는 연산입니다: {ast.unparse(node)}")


def _wrapped(node: ast.expr, minimum_level: int) -> str:
    """결합 수준이 minimum_level보다 낮으면 괄호로 묶는다. 분수가 든 괄호는 키를 맞춘다."""
    text, level = _latex(node)
    if level >= minimum_level:
        return text
    return rf"\left({text}\right)" if r"\frac" in text else f"({text})"


# ---- 계산 유도 표 ----

def identities_hold(expressions: Sequence[str]) -> bool:
    """이웃한 줄끼리 모두 항등식인가."""
    return all(same_polynomial(before, after) for before, after in zip(expressions, expressions[1:]))
