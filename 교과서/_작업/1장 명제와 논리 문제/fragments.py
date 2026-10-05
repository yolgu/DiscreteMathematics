"""문항과 해설에 되풀이해 쓰는 HTML 조각과, 같은 데이터로 하는 유도 확인."""

from __future__ import annotations

import html
from collections.abc import Sequence
from dataclasses import dataclass

from logic_tools import Formula, all_rows, equivalent, law_applies, parse


@dataclass(frozen=True)
class Step:
    """동치 유도의 한 줄. label은 문제에서 줄을 가리키는 이름((가) 등), 없으면 빈 글자."""

    formula: str
    reason: str
    label: str = ""


def derivation_html(start: str, steps: Sequence[Step]) -> str:
    rows: list[str] = [f'<tr><td class="step-sign"></td><td>{html.escape(start)}</td><td class="step-reason"></td></tr>']
    for step in steps:
        sign: str = f"{step.label} ≡" if step.label else "≡"
        rows.append(
            f'<tr><td class="step-sign">{sign}</td><td>{html.escape(step.formula)}</td>'
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
