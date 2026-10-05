"""4절 추론: 핵심 정리, 보기 4, 문제 30~36. 섞어 풀기: 문제 37~40."""

from __future__ import annotations

import html
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from fragments import computed_truth_table, truth_table_html
from logic_tools import entails, equivalent, is_contradiction, is_tautology, rule_matches, truth_column, value
from model import Demand, Item, Layout, Option, Section, WorkedExample, formula_option

Argument = tuple[tuple[str, ...], str]

SUMMARY: str = """
<ul>
  <li><strong>정당한 추론</strong>: 전제가 모두 참인 모든 경우에 결론도 참인 추론입니다. 진리표에서 전제가 모두 참인 줄만 골라, 그 줄에서 결론이 모두 참인지 봅니다. 전제가 모두 참인데 결론이 거짓인 줄이 하나라도 있으면 부당한 추론입니다.</li>
  <li><strong>항진명제로 옮기기</strong>: (전제 ∧ 전제) → 결론이 항진명제이면 정당한 추론입니다.</li>
  <li><strong>닮았지만 부당한 추론</strong>: p → q, q ∴ p는 후건 긍정의 오류, p → q, ¬p ∴ ¬q는 전건 부정의 오류입니다. 역과 이를 원래 명제처럼 쓴 것입니다.</li>
</ul>
<table class="prose-table">
  <caption>이 장의 논리적 추론 법칙</caption>
  <thead><tr><th>법칙</th><th>추론 꼴</th></tr></thead>
  <tbody>
    <tr><td>논리곱</td><td>p, q ∴ p ∧ q</td></tr>
    <tr><td>선언적 부가</td><td>p ∴ p ∨ q</td></tr>
    <tr><td>단순화</td><td>p ∧ q ∴ p (또는 q)</td></tr>
    <tr><td>긍정논법</td><td>p, p → q ∴ q</td></tr>
    <tr><td>부정논법</td><td>¬q, p → q ∴ ¬p</td></tr>
    <tr><td>선언적 삼단논법</td><td>p ∨ q, ¬p ∴ q</td></tr>
    <tr><td>가설적 삼단논법</td><td>p → q, q → r ∴ p → r</td></tr>
  </tbody>
</table>
"""


def argument_text(argument: Argument) -> str:
    premises, conclusion = argument
    return html.escape(f"{', '.join(premises)} ∴ {conclusion}")


def argument_option(argument: Argument, why_wrong: str = "") -> Option[Argument]:
    """추론 선택지. 찍는 글과 판정하는 전제, 결론이 같은 데이터에서 나온다."""
    return Option(argument, argument_text(argument), why_wrong)


def is_valid(argument: Argument) -> bool:
    premises, conclusion = argument
    return entails(premises, conclusion)


def _row_holds(true_formulas: Sequence[str], also_true: str, **row: bool) -> bool:
    """주어진 경우에 true_formulas와 also_true가 모두 참인가. 해설에 든 반례를 확인할 때 쓴다."""
    return all(value(text, **row) for text in [*true_formulas, also_true])


def _all_false_refutes(premises: Sequence[str], conclusion: str) -> bool:
    """변수가 모두 F인 경우에 전제는 모두 참이고 결론은 거짓인가."""
    return _row_holds(premises, f"¬({conclusion})", p=False, q=False, r=False)


WORKED_ARGUMENT: Argument = (("¬p → q", "¬q"), "p")


def _worked_check() -> bool:
    rows_with_true_premises: list[tuple[bool, ...]] = [
        (p, q)
        for (p, q), first, second in zip(
            ((True, True), (True, False), (False, True), (False, False)),
            truth_column("¬p → q", ["p", "q"]),
            truth_column("¬q", ["p", "q"]),
        )
        if first and second
    ]
    return (
        rows_with_true_premises == [(True, False)]
        and is_valid(WORKED_ARGUMENT)
        and rule_matches("부정논법", ["¬q", "¬p → q"], "¬(¬p)")
        and equivalent("¬(¬p)", "p")
    )


WORKED: WorkedExample = WorkedExample(
    title="보기 4 추론이 정당한지 판단하기",
    body=f"""
<p>추론 ¬p → q, ¬q ∴ p가 정당한지 판단하세요.</p>
<p class="solution-label">풀이</p>
<p>진리표를 만들고, 전제 ¬p → q와 ¬q가 모두 참인 줄만 봅니다.</p>
{computed_truth_table(["p", "q"], ["¬p → q", "¬q"], "보기 4의 두 전제")}
<p>¬q가 참인 줄은 둘째 줄과 넷째 줄입니다. 그 가운데 ¬p → q도 참인 것은 둘째 줄뿐입니다. 넷째 줄은 ¬p가 T, q가 F라서 함축이 거짓입니다. 전제가 모두 참인 줄은 둘째 줄 하나이고, 거기서 결론 p는 T입니다. 따라서 정당한 추론입니다.</p>
<p>추론 법칙으로도 볼 수 있습니다. ¬p → q에서 결론 q가 거짓(¬q)이므로 부정논법으로 조건을 부정한 ¬(¬p)를 얻고, 이중 부정법칙으로 p가 됩니다. 법칙의 꼴 속 p 자리에 ¬p 같은 식이 들어가도 법칙은 그대로 쓸 수 있습니다.</p>
""",
    check=_worked_check,
)

ITEM_30: Item[Argument] = Item(
    number=30,
    demand=Demand.FOUNDATION,
    stem="<p>정당한 추론을 고르세요.</p>",
    options=(
        argument_option((("p → q", "q"), "p"), "후건 긍정의 오류입니다. p가 F, q가 T이면 두 전제는 모두 참인데 결론 p는 거짓입니다. q가 참이라고 조건 p까지 참인 것은 아닙니다."),
        argument_option((("p → q", "¬p"), "¬q"), "전건 부정의 오류입니다. p가 F, q가 T이면 두 전제는 모두 참인데 결론 ¬q는 거짓입니다. 조건이 거짓일 때 함축은 결론에 대해 아무것도 말해 주지 않습니다."),
        argument_option((("p ∨ q", "p"), "¬q"), "∨를 '둘 중 하나만'으로 읽은 답입니다. p와 q가 모두 T이면 두 전제는 참인데 결론 ¬q는 거짓입니다. 선언적 삼단논법은 p가 거짓일 때 q를 얻는 법칙입니다."),
        argument_option((("p → q",), "q → p"), "함축에서 그 역을 끌어냈습니다. p가 F, q가 T이면 전제 p → q는 참인데 결론 q → p는 거짓입니다. 함축과 역은 동치가 아닙니다."),
        argument_option((("p → q", "¬q"), "¬p")),
    ),
    answer=5,
    judge=is_valid,
    solution=f"""
<p>p → q, ¬q ∴ ¬p는 부정논법입니다. 진리표에서 확인하면, ¬q가 참인 줄은 q가 F인 둘째 줄과 넷째 줄이고, 그 가운데 p → q가 참인 것은 넷째 줄뿐입니다. 넷째 줄에서 p는 F이므로 결론 ¬p는 참입니다.</p>
{computed_truth_table(["p", "q"], ["p → q", "¬q", "¬p"], "전제 p → q, ¬q와 결론 ¬p")}
<p>뜻으로 읽으면, p이면 q인데 q가 아니라면 p일 수가 없습니다. 함축 p → q와 동치인 대우 ¬q → ¬p에 긍정논법을 쓴 것과 같습니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_31_ARGUMENT: Argument = (("p → q", "q → r"), "p → r")

ITEM_31: Item[str] = Item(
    number=31,
    demand=Demand.FOUNDATION,
    stem="<p>다음 추론에 쓰인 추론 법칙을 고르세요.</p><p class=\"quote\">비밀번호를 세 번 틀리면 계정이 잠긴다. 계정이 잠기면 관리자에게 문의해야 한다. 그러므로 비밀번호를 세 번 틀리면 관리자에게 문의해야 한다.</p>",
    options=(
        Option("긍정논법", "긍정논법", "긍정논법은 p, p → q ∴ q처럼 조건 p 자체가 전제로 주어져야 합니다. 이 추론에는 '비밀번호를 세 번 틀렸다'는 전제가 없고, 결론도 함축입니다."),
        Option("부정논법", "부정논법", "부정논법은 결론의 부정 ¬q가 전제에 있어야 합니다. 이 추론에는 무엇이 아니라는 전제가 없습니다."),
        Option("선언적 삼단논법", "선언적 삼단논법", "선언적 삼단논법은 '또는'으로 이은 전제 p ∨ q가 있어야 합니다. 이 추론의 전제는 모두 '이면'으로 된 함축입니다."),
        Option("가설적 삼단논법", "가설적 삼단논법"),
        Option("단순화", "단순화", "단순화는 p ∧ q에서 한쪽을 떼어 내는 법칙입니다. 이 추론에는 '그리고'로 이은 전제가 없습니다."),
    ),
    answer=4,
    judge=lambda rule: rule_matches(rule, ITEM_31_ARGUMENT[0], ITEM_31_ARGUMENT[1]),
    solution="""
<p>p: 비밀번호를 세 번 틀린다, q: 계정이 잠긴다, r: 관리자에게 문의해야 한다로 놓으면 이 추론은 p → q, q → r ∴ p → r입니다. 첫째 전제의 결론 q가 둘째 전제의 조건이 되어 두 함축이 이어지므로 가설적 삼단논법(추이)입니다.</p>
<p>법칙을 고를 때는 문장을 기호로 옮긴 뒤 전제와 결론의 모양을 봅니다. 전제가 모두 함축이고 결론도 함축이면 가설적 삼단논법을 먼저 떠올립니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_32_NOTATION: str = "p: 비가 온다, q: 경기가 취소된다"

ITEM_32: Item[Argument] = Item(
    number=32,
    demand=Demand.FOUNDATION,
    stem="<p><strong>부당한</strong> 추론을 고르세요.</p>",
    options=(
        Option((("p → q", "p"), "q"), "비가 오면 경기가 취소된다. 비가 왔다. 그러므로 경기가 취소되었다.", "p → q, p ∴ q로 긍정논법입니다. 정당한 추론입니다."),
        Option((("p → q", "q"), "p"), "비가 오면 경기가 취소된다. 경기가 취소되었다. 그러므로 비가 왔다."),
        Option((("p → q", "¬q"), "¬p"), "비가 오면 경기가 취소된다. 경기가 취소되지 않았다. 그러므로 비가 오지 않았다.", "p → q, ¬q ∴ ¬p로 부정논법입니다. 비가 왔다면 경기가 취소되었을 텐데 취소되지 않았으니 비는 오지 않았습니다. 정당한 추론입니다."),
        Option((("p ∨ r", "¬p"), "r"), "비가 오거나 바람이 불었다. 비가 오지 않았다. 그러므로 바람이 불었다.", "r: 바람이 분다로 놓으면 p ∨ r, ¬p ∴ r로 선언적 삼단논법입니다. 정당한 추론입니다."),
        Option((("p → q", "q → r"), "p → r"), "비가 오면 경기가 취소된다. 경기가 취소되면 표값을 돌려준다. 그러므로 비가 오면 표값을 돌려준다.", "r: 표값을 돌려준다로 놓으면 p → q, q → r ∴ p → r로 가설적 삼단논법입니다. 정당한 추론입니다."),
    ),
    answer=2,
    judge=lambda argument: not is_valid(argument),
    solution=f"""
<p>{ITEM_32_NOTATION}로 놓으면 이 추론은 p → q, q ∴ p입니다. 결론 q를 긍정했다고 조건 p까지 긍정한 후건 긍정의 오류입니다.</p>
<p>p가 F, q가 T인 경우, 곧 비는 오지 않았는데 다른 까닭(운동장 공사 등)으로 경기가 취소된 경우를 생각해 봅니다. 두 전제 '비가 오면 경기가 취소된다'와 '경기가 취소되었다'는 모두 참이지만, 결론 '비가 왔다'는 거짓입니다. 전제가 모두 참인데 결론이 거짓인 경우가 있으므로 부당한 추론입니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_33: Item[Argument] = Item(
    number=33,
    demand=Demand.VARIATION,
    stem="<p><strong>부당한</strong> 추론을 고르세요.</p>",
    options=(
        argument_option((("p → q", "p → r"), "q ∧ r")),
        argument_option((("p → q", "q → r"), "p → r"), "가설적 삼단논법 그대로입니다. 정당한 추론입니다."),
        argument_option((("p ∨ q", "p → r", "q → r"), "r"), "결론 r이 거짓이라고 해 봅니다. p → r과 q → r이 참이려면 p와 q가 모두 거짓이어야 하는데, 그러면 p ∨ q가 거짓입니다. 전제가 모두 참이면서 r이 거짓인 경우가 없으므로 정당합니다. p와 q 가운데 어느 쪽이 참이든 r에 닿는다는 뜻입니다."),
        argument_option((("p → q", "q → r", "¬r"), "¬p"), "p → q와 q → r에 가설적 삼단논법을 쓰면 p → r이고, 여기에 ¬r로 부정논법을 쓰면 ¬p입니다. 정당한 추론입니다."),
        argument_option((("p ∧ q", "q → r"), "p ∧ r"), "p ∧ q에 단순화를 써서 p와 q를 얻고, q와 q → r에 긍정논법을 써서 r을 얻은 뒤, p와 r에 논리곱을 쓰면 p ∧ r입니다. 정당한 추론입니다."),
    ),
    answer=1,
    judge=lambda argument: not is_valid(argument),
    solution=f"""
<p>p → q, p → r ∴ q ∧ r은 두 함축의 조건이 모두 p인데, 전제 어디에도 p가 참이라는 말이 없습니다. p가 F이면 q와 r이 무엇이든 두 함축은 참입니다. 예를 들어 p, q, r이 모두 F이면 두 전제는 참인데 결론 q ∧ r은 거짓입니다.</p>
{truth_table_html(["p", "q", "r", "p → q", "p → r", "q ∧ r"], [[False, False, False, True, True, False]], "전제가 모두 참인데 결론이 거짓인 한 경우")}
<p>전제 p가 하나 더 있다면 긍정논법을 두 번 써서 q와 r을 얻고, 논리곱으로 q ∧ r을 얻을 수 있습니다. 나머지 넷은 모두 법칙을 이어 쓰거나 결론이 거짓인 경우를 따져 보면 정당하다는 것을 확인할 수 있습니다.</p>
""",
    layout=Layout.MEDIUM,
)

Claim = tuple[str, str]
CLAIM_TESTS: dict[str, Callable[[str], bool]] = {
    "항진명제": is_tautology,
    "사건명제": lambda formula: not is_tautology(formula) and not is_contradiction(formula),
}


def claim_option(formula: str, kind: str, why_wrong: str = "") -> Option[Claim]:
    return Option((formula, kind), f"{html.escape(formula)}가 {kind}이다.", why_wrong)


ITEM_34: Item[Claim] = Item(
    number=34,
    demand=Demand.FOUNDATION,
    stem="<p>추론 p ∨ q, ¬p ∴ q가 정당한 추론이라는 것을 바르게 나타낸 것을 고르세요.</p>",
    options=(
        claim_option("[(p ∨ q) ∧ ¬p] → q", "사건명제", "이 함축은 모든 줄에서 참인 항진명제입니다. 사건명제라면 거짓인 줄이 있다는 뜻이고, 그 줄은 전제가 모두 참인데 결론이 거짓인 줄이므로 오히려 부당한 추론이 됩니다."),
        claim_option("(p ∨ q) ∧ ¬p ∧ q", "항진명제", "전제와 결론을 모두 ∧로 이었습니다. 이 식은 p가 F, q가 T일 때만 참인 사건명제입니다. 추론은 전제와 결론을 함축으로 묶어야 합니다."),
        claim_option("[(p ∨ q) ∧ ¬p] → q", "항진명제"),
        claim_option("q → [(p ∨ q) ∧ ¬p]", "항진명제", "함축의 방향이 거꾸로입니다. p와 q가 모두 T이면 q는 참인데 (p ∨ q) ∧ ¬p는 거짓이므로 이 식은 거짓이 되는 줄이 있습니다."),
        claim_option("[(p ∨ q) ∧ ¬p] ↔ q", "항진명제", "추론은 전제에서 결론으로 한 방향만 보장하면 됩니다. p와 q가 모두 T이면 q는 참인데 (p ∨ q) ∧ ¬p는 거짓이라 쌍방 조건이 거짓이므로 항진명제가 아닙니다."),
    ),
    answer=3,
    judge=lambda claim: CLAIM_TESTS[claim[1]](claim[0]),
    solution=f"""
<p>전제를 ∧로 이어 결론과 함축으로 묶은 [(p ∨ q) ∧ ¬p] → q가 항진명제이면 정당한 추론입니다. 함축이 거짓인 줄은 앞이 참이고 뒤가 거짓인 줄, 곧 전제가 모두 참인데 결론이 거짓인 줄이기 때문입니다.</p>
{computed_truth_table(["p", "q"], ["(p ∨ q) ∧ ¬p", "[(p ∨ q) ∧ ¬p] → q"], "선언적 삼단논법에 대응하는 항진명제")}
<p>전제가 모두 참인 줄은 셋째 줄뿐이고, 거기서 q는 T이므로 함축은 모든 줄에서 참입니다. 이것이 선언적 삼단논법입니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_35_PREMISES: tuple[str, ...] = ("p → q", "¬r → ¬q")

ITEM_35: Item[str] = Item(
    number=35,
    demand=Demand.CHALLENGE,
    stem="<p>두 전제 p → q, ¬r → ¬q에 전제 (가)를 하나 더하면 결론 r을 정당하게 끌어낼 수 있습니다. (가)에 알맞은 것을 고르세요.</p>",
    options=(
        formula_option("¬p", "p가 거짓이면 p → q는 q에 대해 아무것도 말해 주지 않습니다. p, q, r이 모두 F이면 세 전제는 참인데 결론 r은 거짓입니다."),
        formula_option("¬r", "¬r을 더하면 ¬r → ¬q와 긍정논법으로 ¬q가 나올 뿐, 결론과 반대인 ¬r이 전제가 되어 r을 끌어낼 수 없습니다. p, q, r이 모두 F이면 세 전제는 참인데 r은 거짓입니다."),
        formula_option("r → p", "r에서 p로 가는 함축이라, r을 얻는 데 쓰려면 오히려 r을 먼저 알아야 합니다. p, q, r이 모두 F이면 세 전제는 참인데 r은 거짓입니다."),
        formula_option("q → r", "¬r → ¬q의 대우라서 이미 있는 전제와 같은 말을 한 번 더 한 셈입니다. 새 정보가 없으므로 p, q, r이 모두 F일 때 세 전제는 참인데 r은 거짓입니다."),
        formula_option("p"),
    ),
    answer=5,
    judge=lambda extra: entails([*ITEM_35_PREMISES, extra], "r"),
    solution="""
<p>먼저 ¬r → ¬q를 대우로 바꾸면 q → r입니다. 함축과 대우는 동치이므로 같은 전제로 써도 됩니다. 이제 전제는 p → q, q → r이고, 가설적 삼단논법으로 p → r을 얻습니다.</p>
<p>p → r에서 r을 끌어내려면 긍정논법에 필요한 조건 p가 있어야 합니다. 그래서 (가)는 p입니다. 정리하면 p, p → q에서 긍정논법으로 q, q와 q → r에서 다시 긍정논법으로 r입니다.</p>
""",
    layout=Layout.SHORT,
)


@dataclass(frozen=True)
class Line:
    """추론 풀이의 한 줄: 이름, 얻은 명제, 근거로 든 줄, 쓴 법칙."""

    label: str
    name: str
    formula: str
    cited: tuple[str, ...]
    rule: str

    def reason(self) -> str:
        return f"{', '.join(self.cited)}에 {self.rule}"


ITEM_36_PREMISES: dict[str, str] = {"A": "p → q", "B": "q → r", "C": "r ∨ s", "D": "¬s"}
ITEM_36_LINES: tuple[Line, ...] = (
    Line("(가)", "E", "r", ("C", "D"), "선언적 삼단논법"),
    Line("(나)", "F", "q", ("B", "E"), "긍정논법"),
    Line("(다)", "G", "p → r", ("A", "B"), "가설적 삼단논법"),
    Line("(라)", "H", "r ∨ p", ("E",), "선언적 부가"),
    Line("(마)", "I", "r ∧ ¬s", ("E", "D"), "논리곱"),
)


def _known_formulas() -> dict[str, str]:
    return {**ITEM_36_PREMISES, **{line.name: line.formula for line in ITEM_36_LINES}}


def line_is_wrong(line: Line) -> bool:
    cited: list[str] = [_known_formulas()[name] for name in line.cited]
    return not (rule_matches(line.rule, cited, line.formula) and entails(cited, line.formula))


def _item_36_table() -> str:
    premise_rows: list[str] = [
        f'<tr><td class="step-sign">{name}</td><td>{html.escape(formula)}</td><td class="step-reason">전제</td></tr>'
        for name, formula in ITEM_36_PREMISES.items()
    ]
    line_rows: list[str] = [
        f'<tr><td class="step-sign">{line.label} {line.name}</td><td>{html.escape(line.formula)}</td>'
        f'<td class="step-reason">{line.reason()}</td></tr>'
        for line in ITEM_36_LINES
    ]
    return '<table class="derivation">' + "".join(premise_rows + line_rows) + "</table>"


def _line_option(line: Line, why_wrong: str = "") -> Option[Line]:
    return Option(line, line.label, why_wrong)


ITEM_36: Item[Line] = Item(
    number=36,
    demand=Demand.FOUNDATION,
    stem=f"<p>전제 A, B, C, D에서 추론 법칙으로 새 명제를 얻었습니다. 법칙을 <strong>잘못</strong> 쓴 줄을 고르세요.</p>{_item_36_table()}",
    options=(
        _line_option(ITEM_36_LINES[0], "C의 r ∨ s에서 D가 s를 부정하므로 남은 r이 참입니다. 선언적 삼단논법을 바르게 썼습니다."),
        _line_option(ITEM_36_LINES[1]),
        _line_option(ITEM_36_LINES[2], "A의 결론 q가 B의 조건이므로 두 함축이 이어집니다. 가설적 삼단논법을 바르게 썼습니다."),
        _line_option(ITEM_36_LINES[3], "참인 r에 무엇을 ∨로 붙여도 참입니다. 붙이는 명제가 p처럼 참인지 모르는 것이어도 됩니다. 선언적 부가를 바르게 썼습니다."),
        _line_option(ITEM_36_LINES[4], "E의 r과 D의 ¬s가 모두 참이므로 둘을 ∧로 이은 것도 참입니다. 논리곱을 바르게 썼습니다."),
    ),
    answer=2,
    judge=line_is_wrong,
    solution="""
<p>(나)는 B: q → r과 E: r에서 q를 얻었습니다. 함축의 결론 r이 참이라고 조건 q까지 참이라고 한 것이므로, 긍정논법이 아니라 후건 긍정의 오류입니다. 긍정논법은 조건 q가 참일 때 결론 r을 얻는 법칙입니다.</p>
<p>실제로 p, q가 F이고 r이 T, s가 F이면 A, B, C, D와 E는 모두 참인데 q는 거짓입니다. 이 전제들로부터 q가 참이라고 말할 수는 없습니다.</p>
""",
    layout=Layout.SHORT,
)

SECTION_D: Section = Section(
    title="4. 추론",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_30, ITEM_31, ITEM_32, ITEM_33, ITEM_34, ITEM_35, ITEM_36),
    checks=(
        ("문제 31: 기호로 옮긴 추론이 정당", lambda: is_valid(ITEM_31_ARGUMENT)),
        ("문제 33 해설: 반례 p, q, r 모두 F", lambda: _all_false_refutes(("p → q", "p → r"), "q ∧ r")),
        ("문제 35 해설: ¬r → ¬q ≡ q → r, 그리고 p 하나로 r", lambda: equivalent("¬r → ¬q", "q → r") and entails(["p → q", "q → r", "p"], "r")),
        ("문제 35 오답: p, q, r 모두 F가 반례", lambda: all(_all_false_refutes((*ITEM_35_PREMISES, extra), "r") for extra in ("¬p", "¬r", "r → p", "q → r"))),
        ("문제 36 해설: p, q F, r T, s F에서 전제와 E는 참, q는 거짓", lambda: _row_holds(["p → q", "q → r", "r ∨ s", "¬s", "r"], "¬q", p=False, q=False, r=True, s=False)),
    ),
)


# ---- 섞어 풀기 ----

ITEM_37_COLUMN: tuple[bool, ...] = (False, True, False, False)

ITEM_37: Item[str] = Item(
    number=37,
    demand=Demand.FOUNDATION,
    stem=f"<p>진리표의 ㉠ 열에 알맞은 명제를 고르세요.</p>{truth_table_html(['p', 'q', '㉠'], [[p, q, v] for (p, q), v in zip(((True, True), (True, False), (False, True), (False, False)), ITEM_37_COLUMN)])}",
    options=(
        formula_option("¬p ∧ q", "p와 q의 자리를 바꿨습니다. ¬p ∧ q는 p가 F, q가 T인 셋째 줄에서만 참입니다."),
        formula_option("p ⊕ q", "p ⊕ q는 둘의 값이 다른 둘째 줄과 셋째 줄에서 참입니다. ㉠은 셋째 줄에서 F입니다."),
        formula_option("p ∧ ¬q"),
        formula_option("p → q", "p → q는 둘째 줄에서만 거짓입니다. ㉠과 정반대이므로, ㉠은 p → q의 부정입니다."),
        formula_option("p ∨ ¬q", "p ∨ ¬q는 셋째 줄에서만 거짓입니다. 참인 줄이 하나뿐인 열은 ∧로 만들어야 합니다."),
    ),
    answer=3,
    judge=lambda formula: truth_column(formula, ["p", "q"]) == ITEM_37_COLUMN,
    solution=f"""
<p>㉠은 p가 T, q가 F인 둘째 줄에서만 참입니다. 참인 줄이 하나뿐이므로 'p가 참이고 q가 거짓'을 ∧로 이은 p ∧ ¬q입니다.</p>
{computed_truth_table(["p", "q"], ["p ∧ ¬q"])}
<p>함축 p → q가 거짓인 줄도 바로 이 줄이므로 p ∧ ¬q ≡ ¬(p → q)입니다. 2절의 함축법칙과 드모르간의 법칙으로도 확인할 수 있습니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_38: Item[str] = Item(
    number=38,
    demand=Demand.FOUNDATION,
    stem=r"<p>\(\forall x\,(P(x) \rightarrow Q(x))\)가 거짓임을 보이려고 합니다. 논의영역에서 어떤 \(x\)를 하나 찾으면 되는지 고르세요.</p>",
    options=(
        Option("p ∧ q", r"\(P(x)\)와 \(Q(x)\)가 모두 참인 \(x\)", r"T → T는 참이므로 이런 \(x\)는 함축을 거짓으로 만들지 못합니다."),
        Option("¬p ∧ ¬q", r"\(P(x)\)와 \(Q(x)\)가 모두 거짓인 \(x\)", "조건이 거짓이면 함축은 참입니다. F → F는 참입니다."),
        Option("¬p ∧ q", r"\(P(x)\)는 거짓이고 \(Q(x)\)는 참인 \(x\)", r"F → T는 참입니다. 이런 \(x\)는 함축의 역 \(Q(x) \rightarrow P(x)\)를 거짓으로 만듭니다."),
        Option("p ∧ ¬q", r"\(P(x)\)는 참이고 \(Q(x)\)는 거짓인 \(x\)"),
        Option("¬q", r"\(Q(x)\)가 거짓인 \(x\)", r"\(Q(x)\)가 거짓이어도 \(P(x)\)까지 거짓이면 F → F로 함축은 참입니다. \(P(x)\)가 참이라는 조건이 함께 있어야 합니다."),
    ),
    answer=4,
    judge=lambda condition: entails([condition], "¬(p → q)"),
    solution=r"""
<p>∀가 붙은 명제는 반례 하나로 거짓이 됩니다. 반례는 \(P(x) \rightarrow Q(x)\)를 거짓으로 만드는 \(x\)이고, 함축이 거짓인 경우는 조건이 참이고 결론이 거짓일 때뿐입니다. 그래서 \(P(x)\)는 참이고 \(Q(x)\)는 거짓인 \(x\)를 하나 찾으면 됩니다.</p>
<p>한정자의 부정으로 써도 같습니다. \(\neg\forall x\,(P(x) \rightarrow Q(x)) \equiv \exists x\,\neg(P(x) \rightarrow Q(x)) \equiv \exists x\,(P(x) \land \neg Q(x))\)입니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_39: Item[Callable[[], bool]] = Item(
    number=39,
    demand=Demand.FOUNDATION,
    stem="<p>옳지 <strong>않은</strong> 것을 고르세요.</p>",
    options=(
        Option(lambda: equivalent("p", "p ∨ q"), "p와 p ∨ q는 논리적 동치이다."),
        Option(lambda: entails(["p ∧ q"], "p"), "p ∧ q에서 p를 끌어내는 추론은 정당하다.", "단순화입니다. p ∧ q가 참이면 p도 참이므로 옳은 설명입니다."),
        Option(lambda: entails(["p"], "p ∨ q"), "p에서 p ∨ q를 끌어내는 추론은 정당하다.", "선언적 부가입니다. p가 참이면 p ∨ q도 참이므로 옳은 설명입니다."),
        Option(lambda: equivalent("p ∧ (p ∨ q)", "p"), "p ∧ (p ∨ q) ≡ p이다.", "흡수법칙입니다. 진리표에서 두 식의 열이 같으므로 옳은 설명입니다."),
        Option(lambda: is_tautology("p → (p ∨ q)"), "p → (p ∨ q)는 항진명제이다.", "선언적 부가에 대응하는 항진명제입니다. p가 참이면 p ∨ q도 참이라 거짓인 줄이 없으므로 옳은 설명입니다."),
    ),
    answer=1,
    judge=lambda claim: not claim(),
    solution=f"""
<p>p에서 p ∨ q를 끌어내는 추론은 정당하지만, 거꾸로 p ∨ q에서 p는 나오지 않습니다. p가 F, q가 T이면 p ∨ q는 참이고 p는 거짓입니다. 두 명제의 진릿값이 다른 경우가 있으므로 논리적 동치가 아닙니다.</p>
{computed_truth_table(["p", "q"], ["p ∨ q"])}
<p>동치는 양쪽 방향의 함축이 모두 항진명제인 것이고, 정당한 추론은 전제에서 결론으로 한쪽 방향만 보장합니다. 셋째 줄이 그 차이를 보여 줍니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_40_NOTATION: str = "p: 숙제를 끝냈다, q: 게임을 했다, r: 늦게 잤다"
ITEM_40_PREMISES: tuple[str, ...] = ("p → q", "q → r", "r")

ITEM_40: Item[str] = Item(
    number=40,
    demand=Demand.VARIATION,
    stem="<p>세 문장 (가), (나), (다)가 모두 참일 때, 반드시 참인 것을 고르세요.</p><p class=\"quote\">(가) 숙제를 끝냈으면 게임을 했다.<br>(나) 게임을 했으면 늦게 잤다.<br>(다) 늦게 잤다.</p>",
    options=(
        Option("p", "숙제를 끝냈다.", "(다)에서 (나)를 거꾸로, 다시 (가)를 거꾸로 따라간 후건 긍정의 오류입니다. 숙제도 게임도 하지 않고 늦게 잔 경우에 세 문장은 모두 참이지만 이 문장은 거짓입니다."),
        Option("p → r", "숙제를 끝냈으면 늦게 잤다."),
        Option("q", "게임을 했다.", "(나)와 (다)에서 게임을 했다고 한 후건 긍정의 오류입니다. 게임을 하지 않고도 늦게 잘 수 있습니다."),
        Option("¬p", "숙제를 끝내지 않았다.", "숙제를 끝내고 게임을 하고 늦게 잔 경우에도 세 문장은 모두 참입니다. 이때 이 문장은 거짓이므로 반드시 참인 것은 아닙니다."),
        Option("q → p", "게임을 했으면 숙제를 끝냈다.", "(가)의 역입니다. 숙제는 끝내지 않고 게임을 하고 늦게 잔 경우에 세 문장은 모두 참이지만 이 문장은 거짓입니다."),
    ),
    answer=2,
    judge=lambda formula: entails(ITEM_40_PREMISES, formula),
    solution=f"""
<p>{ITEM_40_NOTATION}로 놓으면 (가)는 p → q, (나)는 q → r, (다)는 r입니다. (가)와 (나)에 가설적 삼단논법을 쓰면 p → r, 곧 '숙제를 끝냈으면 늦게 잤다'가 반드시 참입니다.</p>
<p>(다)는 함축의 결론 r이 참이라는 것뿐이라, 이것만으로 조건 p나 q가 참이라고 할 수 없습니다. 결론을 긍정했다고 조건을 긍정하는 것이 후건 긍정의 오류입니다.</p>
""",
    layout=Layout.MEDIUM,
)

SECTION_E: Section = Section(
    title="5. 섞어 풀기",
    summary="",
    worked=None,
    items=(ITEM_37, ITEM_38, ITEM_39, ITEM_40),
    note="1절부터 4절까지의 유형이 섞여 있습니다. 어느 절의 방법을 쓸지부터 스스로 정해야 합니다. 앞 문제를 다 푼 뒤 며칠 지나서, 해설과 핵심 정리를 보지 않고 풀어 보세요.",
    checks=(
        ("문제 37 해설: p ∧ ¬q ≡ ¬(p → q)", lambda: equivalent("p ∧ ¬q", "¬(p → q)")),
        ("문제 38 해설: ¬(P → Q) ≡ P ∧ ¬Q", lambda: equivalent("¬(p → q)", "p ∧ ¬q")),
        ("문제 40 오답: p, q F, r T에서 세 문장 참, p와 q 거짓", lambda: _row_holds(ITEM_40_PREMISES, "¬p ∧ ¬q", p=False, q=False, r=True)),
        ("문제 40 오답: 모두 T에서 세 문장 참, ¬p 거짓", lambda: _row_holds(ITEM_40_PREMISES, "p", p=True, q=True, r=True)),
        ("문제 40 오답: p F, q T, r T에서 세 문장 참, q → p 거짓", lambda: _row_holds(ITEM_40_PREMISES, "¬(q → p)", p=False, q=True, r=True)),
    ),
)
