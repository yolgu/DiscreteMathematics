"""문항과 해설에 되풀이해 쓰는 HTML 조각과, 같은 데이터로 하는 유도 확인."""

from __future__ import annotations

import html
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction

from expr_tools import IDENTITY_POINTS, evaluate, identities_hold, latex
from logic_tools import Formula, all_rows, equivalent, law_applies, parse


# ---- 명제의 동치 유도 ----

@dataclass(frozen=True)
class Step:
    """동치 유도의 한 줄. label은 문제에서 줄을 가리키는 이름((가) 등), 없으면 빈 글자."""

    formula: str
    reason: str
    label: str = ""


def derivation_html(start: str, steps: Sequence[Step], hidden: str = "") -> str:
    """hidden에 줄 이름을 주면 그 줄의 식은 가리고 이름만 찍는다(빈칸 문제)."""
    rows: list[str] = [f'<tr><td class="step-sign"></td><td>{html.escape(start)}</td><td class="step-reason"></td></tr>']
    for step in steps:
        is_hidden: bool = bool(hidden) and step.label == hidden
        sign: str = f"{step.label} ≡" if step.label and not is_hidden else "≡"
        shown: str = step.label if is_hidden else html.escape(step.formula)
        rows.append(
            f'<tr><td class="step-sign">{sign}</td><td>{shown}</td>'
            f'<td class="step-reason">{html.escape(step.reason)}</td></tr>'
        )
    return '<table class="derivation">' + "".join(rows) + "</table>"


def chain_holds(start: str, steps: Sequence[Step]) -> bool:
    """이웃한 줄끼리 모두 동치인가."""
    formulas: list[str] = [start, *(step.formula for step in steps)]
    return all(equivalent(before, after) for before, after in zip(formulas, formulas[1:]))


def laws_named_correctly(start: str, steps: Sequence[Step]) -> bool:
    """줄마다 적은 이름이 법칙 하나뿐일 때, 그 법칙으로 바로 앞 줄에서 그 줄이 나오는가."""
    formulas: list[str] = [start, *(step.formula for step in steps)]
    return all(law_applies(step.reason, before, step.formula) for before, step in zip(formulas, steps))


def computed_truth_table(names: Sequence[str], formulas: Sequence[str], caption: str = "") -> str:
    """진리표의 값은 손으로 적지 않고 식에서 계산해 채운다."""
    parsed: list[Formula] = [parse(text) for text in formulas]
    rows: list[list[bool]] = [
        [row[name] for name in names] + [formula.evaluate(row) for formula in parsed] for row in all_rows(names)
    ]
    return truth_table_html([*names, *formulas], rows, caption)


def truth_table_html(headers: Sequence[str], rows: Sequence[Sequence[bool]], caption: str = "") -> str:
    head: str = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body: str = "".join(
        "<tr>" + "".join(f"<td>{'T' if cell else 'F'}</td>" for cell in row) + "</tr>" for row in rows
    )
    caption_html: str = f"<caption>{caption}</caption>" if caption else ""
    return f'<table class="truth">{caption_html}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


# ---- 수의 계산 유도 ----

@dataclass(frozen=True)
class CalcStep:
    """계산 유도의 한 줄. expression은 expr_tools 문법이라 찍는 식과 확인하는 식이 같은 문자열이다."""

    expression: str
    reason: str


@dataclass(frozen=True)
class Calculation:
    """=로 이어지는 계산 유도 표.

    첫 줄이 ⋯이 든 합처럼 식으로 쓸 수 없으면 first_latex로 찍고, 같은 값을 주는 first_value(k)로 확인한다.
    """

    first: str
    steps: tuple[CalcStep, ...]
    first_latex: str = ""
    first_value: Callable[[int], Fraction] | None = None

    def html(self, blank: int | None = None, blank_label: str = "(가)") -> str:
        """blank에 줄 번호(steps의 위치)를 주면 그 줄의 식은 가리고 blank_label만 찍는다(빈칸 문제)."""
        first: str = self.first_latex or latex(self.first)
        rows: list[str] = [rf'<tr><td class="step-sign"></td><td>\({first}\)</td><td class="step-reason"></td></tr>']
        for index, step in enumerate(self.steps):
            shown: str = blank_label if index == blank else rf"\({latex(step.expression)}\)"
            rows.append(f'<tr><td class="step-sign">=</td><td>{shown}</td><td class="step-reason">{step.reason}</td></tr>')
        return '<table class="derivation">' + "".join(rows) + "</table>"

    def holds(self) -> bool:
        expressions: list[str] = [step.expression for step in self.steps]
        if self.first_value is None:
            return identities_hold([self.first, *expressions])
        first_link: bool = all(self.first_value(k) == evaluate(expressions[0], k=k) for k in IDENTITY_POINTS)
        return first_link and identities_hold(expressions)
