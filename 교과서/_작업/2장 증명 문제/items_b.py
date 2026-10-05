"""묶음 2 대우증명법: 핵심 정리, 보기 2, 문제 11~15."""

from __future__ import annotations

from collections.abc import Callable

from expr_tools import same_polynomial
from fragments import CalcStep, Calculation, computed_truth_table
from logic_tools import entails, equivalent
from model import Demand, Item, Layout, Option, Section, WorkedExample
from number_tools import holds_on_residues, is_even, is_odd
from proof_methods import START, relative_name

SUMMARY: str = """
<ul>
  <li><strong>대우</strong>: p → q의 대우는 가정과 결론을 모두 부정하고 자리도 바꾼 ¬q → ¬p이고, 원래 명제와 동치입니다. 자리만 바꾼 역 q → p와 부정만 한 이 ¬p → ¬q는 원래 명제와 동치가 아닙니다.</li>
  <li><strong>대우증명법</strong>: p → q 대신 대우 ¬q → ¬p를 증명합니다. ¬q를 참이라고 놓고 ¬p를 이끌어 내는, 대우에 대한 직접증명법입니다.</li>
  <li><strong>언제 쓰나</strong>: 가정 p가 '~이 아니다'처럼 부정문이거나, p를 식으로 옮겨도 계산이 막힐 때 씁니다. 부정하면 정의대로 식으로 옮기기 쉬워지는 경우가 많습니다.</li>
  <li><strong>부정 옮기기</strong>: 정수는 짝수와 홀수 가운데 꼭 하나이므로 '짝수가 아니다'는 '홀수이다'와 같습니다. 여러 명제가 이어진 문장은 드모르간의 법칙으로 부정합니다. 'A이고 B'의 부정은 '¬A이거나 ¬B', 'A이거나 B'의 부정은 '¬A이고 ¬B'입니다.</li>
</ul>
"""

WORKED_CALCULATION: Calculation = Calculation(
    first="3*(2*k) + 1",
    first_latex="3n + 1",
    steps=(
        CalcStep("3*(2*k) + 1", r"\(n = 2k\)를 넣음"),
        CalcStep("6*k + 1", "곱셈"),
        CalcStep("2*(3*k) + 1", "앞의 항에서 2를 묶어 냄"),
    ),
)


def _worked_check() -> bool:
    statement_holds: bool = holds_on_residues(lambda n: not is_even(3 * n + 1) or is_odd(n), 2)
    return WORKED_CALCULATION.holds() and statement_holds and equivalent("¬q → ¬p", "p → q")


WORKED: WorkedExample = WorkedExample(
    title="보기 2 대우증명법으로 증명하기",
    body=rf"""
<p>정수 \(n\)에 대해 \(3n + 1\)이 짝수이면 \(n\)은 홀수임을 대우증명법으로 증명하세요.</p>
<p class="solution-label">풀이</p>
<p>p: \(3n + 1\)은 짝수이다, q: \(n\)은 홀수이다로 놓습니다. 가정 p를 그대로 쓰면 \(3n + 1 = 2m\)에서 \(n = \frac{{2m - 1}}{{3}}\)이 되어, \(n\)이 홀수인지 알아보기 어렵습니다. 그래서 대우를 증명합니다.</p>
<p>¬q는 '\(n\)은 홀수가 아니다', 곧 '\(n\)은 짝수이다'이고, ¬p는 '\(3n + 1\)은 짝수가 아니다', 곧 '\(3n + 1\)은 홀수이다'입니다. 대우 ¬q → ¬p는 '\(n\)이 짝수이면 \(3n + 1\)은 홀수이다'입니다.</p>
<p>¬q가 참이라고 놓으면 \(n = 2k\ (k \in Z)\)입니다.</p>
{WORKED_CALCULATION.html()}
<p>정수는 곱셈에 닫혀 있으므로 \(3k\)는 정수이고, \(3n + 1\)은 '2 × 정수 + 1' 꼴이라 홀수입니다. ¬p가 참입니다.</p>
<p>∴ 대우 ¬q → ¬p가 참이므로, 이와 동치인 p → q도 참입니다. Q.E.D.</p>
""",
    check=_worked_check,
)

ITEM_11: Item[str] = Item(
    number=11,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '정수 \(n\)에 대해 \(n^2\)이 짝수이면 \(n\)은 짝수이다'를 대우증명법으로 증명할 때, 실제로 증명할 명제를 고르세요.</p>",
    options=(
        Option("q → p", r"\(n\)이 짝수이면 \(n^2\)은 짝수이다.", "가정과 결론의 자리만 바꾼 역 q → p입니다. 역은 원래 명제와 동치가 아니므로, 이것을 증명해도 원래 명제를 증명한 것이 되지 않습니다."),
        Option("¬p → ¬q", r"\(n^2\)이 짝수가 아니면 \(n\)은 짝수가 아니다.", "부정만 하고 자리를 바꾸지 않은 이 ¬p → ¬q입니다. 이는 원래 명제와 동치가 아닙니다."),
        Option("¬q → p", r"\(n\)이 짝수가 아니면 \(n^2\)은 짝수이다.", r"자리는 바꿨지만 '\(n^2\)이 짝수'를 부정하지 않았습니다. 대우는 양쪽을 모두 부정합니다. 실제로 \(n = 1\)이면 이 명제는 거짓입니다."),
        Option("q → ¬p", r"\(n\)이 짝수이면 \(n^2\)은 짝수가 아니다.", r"자리를 바꾸고 결론 쪽만 부정했습니다. \(n = 2\)이면 \(n^2 = 4\)는 짝수이므로 이 명제는 거짓입니다."),
        Option("¬q → ¬p", r"\(n\)이 짝수가 아니면 \(n^2\)은 짝수가 아니다."),
    ),
    answer=5,
    judge=lambda formula: equivalent(formula, "p → q"),
    solution=rf"""
<p>p: \(n^2\)은 짝수이다, q: \(n\)은 짝수이다로 놓으면 원래 명제는 p → q이고, 대우는 ¬q → ¬p입니다. 가정과 결론을 모두 부정하고 자리도 바꾼 '\(n\)이 짝수가 아니면 \(n^2\)은 짝수가 아니다'를 증명합니다.</p>
{computed_truth_table(["p", "q"], ["p → q", "¬q → ¬p", "q → p", "¬p → ¬q"])}
<p>진리표에서 p → q와 ¬q → ¬p의 열은 같고, 역과 이의 열은 다릅니다. 정수는 짝수 아니면 홀수이므로 대우는 '\(n\)이 홀수이면 \(n^2\)은 홀수이다'와 같은 말이고, 문제 7의 계산으로 증명됩니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_12: Item[Callable[[], bool]] = Item(
    number=12,
    demand=Demand.FOUNDATION,
    stem="<p>명제 p → q를 증명하라는 문제에, 한 학생이 ¬p → ¬q를 증명해 제출했습니다. 이 풀이에 대한 평가로 까닭까지 옳은 것을 고르세요.</p>",
    options=(
        Option(lambda: relative_name("p → q", "¬p → ¬q") == "대우", "¬p → ¬q는 p → q의 대우이므로 바른 증명이다.", "대우는 부정한 뒤 자리도 바꾼 ¬q → ¬p입니다. ¬p → ¬q는 자리를 바꾸지 않았으므로 이입니다."),
        Option(lambda: relative_name("p → q", "¬p → ¬q") == "역" and equivalent("q → p", "p → q"), "¬p → ¬q는 p → q의 역이고, 역은 원래 명제와 동치이므로 바른 증명이다.", "역은 자리만 바꾼 q → p입니다. 게다가 역은 원래 명제와 동치가 아닙니다."),
        Option(lambda: relative_name("p → q", "¬p → ¬q") == "이" and equivalent("¬p → ¬q", "p → q"), "¬p → ¬q는 p → q의 이이고, 이는 원래 명제와 동치이므로 바른 증명이다.", "이라는 이름은 맞지만, 이는 원래 명제와 동치가 아닙니다. p가 참이고 q가 거짓이면 p → q는 거짓인데 ¬p → ¬q는 참입니다."),
        Option(lambda: relative_name("p → q", "¬p → ¬q") == "이" and not equivalent("¬p → ¬q", "p → q"), "¬p → ¬q는 p → q의 이이고 p → q와 동치가 아니므로, p → q를 증명한 것이 아니다."),
        Option(lambda: not equivalent("¬p → ¬q", "q → p"), "¬p → ¬q는 q → p와도 동치가 아니므로, p → q를 증명한 것이 아니다.", "결론은 맞지만 까닭이 틀렸습니다. ¬p → ¬q는 q → p의 대우라서 q → p와 동치입니다. 이와 역은 서로 동치입니다."),
    ),
    answer=4,
    judge=lambda claim: claim(),
    solution=f"""
<p>¬p → ¬q는 p → q의 가정과 결론을 부정하기만 하고 자리는 바꾸지 않았으므로 이입니다. 진리표에서 두 명제를 견주어 봅니다.</p>
{computed_truth_table(["p", "q"], ["p → q", "¬p → ¬q"])}
<p>둘째 줄과 셋째 줄에서 두 열이 다르므로 동치가 아닙니다. 그래서 ¬p → ¬q가 참이라고 보여도 p → q가 참이라는 보장은 없습니다. 대우증명법으로 풀려면 자리까지 바꾼 ¬q → ¬p를 증명해야 합니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_13_CALCULATION: Calculation = Calculation(
    first="5*(2*k) + 2",
    first_latex="5n + 2",
    steps=(
        CalcStep("5*(2*k) + 2", r"\(n = 2k\)를 넣음"),
        CalcStep("10*k + 2", "곱셈"),
        CalcStep("2*(5*k + 1)", "2를 묶어 냄"),
    ),
)

ITEM_13: Item[str] = Item(
    number=13,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '정수 \(n\)에 대해 \(5n + 2\)가 홀수이면 \(n\)은 홀수이다'를 대우증명법으로 증명하려고 합니다. 처음에 참이라고 놓고 출발할 것을 고르세요.</p>",
    options=(
        Option("p", r"\(5n + 2\)가 홀수이다.", "가정 p에서 출발하는 것은 직접증명법입니다. 대우증명법은 ¬q → ¬p를 증명하므로 ¬q에서 출발합니다."),
        Option("¬q", r"\(n\)이 짝수이다."),
        Option("¬p", r"\(5n + 2\)가 짝수이다.", "¬p는 대우증명법에서 마지막에 이끌어 낼 결론입니다. ¬p에서 출발해 ¬q를 보이면 ¬p → ¬q, 곧 이를 증명하게 됩니다."),
        Option("q", r"\(n\)이 홀수이다.", "q는 원래 명제의 결론입니다. q에서 출발해 p를 보이면 역 q → p를 증명하게 됩니다."),
        Option("예", r"\(n = 2\)이다.", r"특정한 값 하나는 출발점이 될 수 없습니다. 모든 짝수에 대해 보여야 하므로 \(n = 2k\ (k \in Z)\)처럼 임의의 짝수로 놓습니다."),
    ),
    answer=2,
    judge=lambda start: start == START["대우증명법"],
    solution=rf"""
<p>p: \(5n + 2\)는 홀수이다, q: \(n\)은 홀수이다로 놓으면 대우 ¬q → ¬p는 '\(n\)이 홀수가 아니면 \(5n + 2\)는 홀수가 아니다', 곧 '\(n\)이 짝수이면 \(5n + 2\)는 짝수이다'입니다. 대우를 직접증명법으로 보이므로 ¬q, 곧 '\(n\)이 짝수이다'를 참이라고 놓고 출발합니다.</p>
<p>\(n = 2k\ (k \in Z)\)로 쓰면 다음과 같습니다.</p>
{ITEM_13_CALCULATION.html()}
<p>\(5k + 1\)은 정수이므로 \(5n + 2\)는 짝수이고, ¬p가 참입니다. 따라서 대우가 참이고 원래 명제도 참입니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_14: Item[str] = Item(
    number=14,
    demand=Demand.FOUNDATION,
    stem=r"""<p>다음 증명을 읽고, 이 증명으로 참임이 보장되는 명제를 고르세요.</p>
<p class="quote">\(n\)이 홀수라고 놓으면 \(n = 2k + 1\ (k \in Z)\)이고, \(n^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1\)이므로 \(n^2\)은 홀수이다.</p>""",
    options=(
        Option("q → p", r"\(n^2\)이 홀수이면 \(n\)은 홀수이다.", "위 증명이 보인 명제의 역입니다. 이 명제 자체는 참이지만, 위 증명은 '\\(n\\)이 홀수'에서 출발했으므로 이것을 보인 것은 아닙니다. 역은 원래 명제와 동치가 아니어서 저절로 따라 나오지 않습니다."),
        Option("¬p → ¬q", r"\(n\)이 짝수이면 \(n^2\)은 짝수이다.", "위 증명이 보인 명제의 이입니다. 보기 1에서 따로 증명한 참인 명제이지만, 위 증명에서 따라 나오지는 않습니다."),
        Option("¬q → ¬p", r"\(n^2\)이 짝수이면 \(n\)은 짝수이다."),
        Option("q → ¬p", r"\(n^2\)이 홀수이면 \(n\)은 짝수이다.", r"자리를 바꾸고 결론 쪽만 부정했습니다. \(n = 1\)이면 \(n^2 = 1\)은 홀수인데 \(n\)은 짝수가 아니므로 거짓인 명제입니다."),
        Option("¬p → q", r"\(n\)이 짝수이면 \(n^2\)은 홀수이다.", r"가정 쪽만 부정했습니다. \(n = 2\)이면 \(n^2 = 4\)는 짝수이므로 거짓인 명제입니다."),
    ),
    answer=3,
    judge=lambda formula: entails(["p → q"], formula),
    solution=r"""
<p>증명은 '\(n\)이 홀수'에서 출발해 '\(n^2\)이 홀수'에 닿았습니다. p: \(n\)은 홀수이다, q: \(n^2\)은 홀수이다로 놓으면 이 증명이 직접 보인 것은 p → q입니다.</p>
<p>p → q가 참이면 이와 동치인 대우 ¬q → ¬p도 참입니다. ¬q는 '\(n^2\)이 홀수가 아니다', 곧 '\(n^2\)이 짝수이다'이고 ¬p는 '\(n\)이 짝수이다'이므로, '\(n^2\)이 짝수이면 \(n\)은 짝수이다'가 보장됩니다. 다시 말해 위 글은 이 명제의 대우증명법이기도 합니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_15_CALCULATION: Calculation = Calculation(
    first="(2*a + 1)*(2*b + 1)",
    first_latex="mn",
    steps=(
        CalcStep("(2*a + 1)*(2*b + 1)", r"\(m = 2a + 1\), \(n = 2b + 1\)을 넣음"),
        CalcStep("4*a*b + 2*a + 2*b + 1", "전개"),
        CalcStep("2*(2*a*b + a + b) + 1", "앞의 세 항에서 2를 묶어 냄"),
    ),
)

ITEM_15_STATEMENT: str = "r → (p ∨ q)"

ITEM_15: Item[str] = Item(
    number=15,
    demand=Demand.VARIATION,
    stem=r"<p>명제 '두 정수 \(m\), \(n\)에 대해 \(mn\)이 짝수이면 \(m\)과 \(n\) 가운데 적어도 하나는 짝수이다'를 대우증명법으로 증명할 때, 실제로 증명할 명제를 고르세요.</p>",
    options=(
        Option("(¬p ∧ ¬q) → ¬r", r"\(m\)과 \(n\)이 모두 홀수이면 \(mn\)은 홀수이다."),
        Option("(¬p ∨ ¬q) → ¬r", r"\(m\)과 \(n\) 가운데 적어도 하나가 홀수이면 \(mn\)은 홀수이다.", r"'적어도 하나는 짝수'를 부정하면서 '적어도 하나'를 그대로 두었습니다. 드모르간의 법칙에 따라 '\(m\)이 짝수이거나 \(n\)이 짝수'의 부정은 '\(m\)도 홀수이고 \(n\)도 홀수'입니다. 실제로 \(m = 1\), \(n = 2\)이면 이 명제는 거짓입니다."),
        Option("(p ∨ q) → r", r"\(m\)과 \(n\) 가운데 적어도 하나가 짝수이면 \(mn\)은 짝수이다.", "가정과 결론의 자리만 바꾼 역입니다. 이 명제도 참이지만 원래 명제와 동치가 아니므로, 이것을 증명해서는 원래 명제를 증명한 것이 되지 않습니다."),
        Option("¬r → (¬p ∧ ¬q)", r"\(mn\)이 홀수이면 \(m\)과 \(n\)은 모두 홀수이다.", "부정은 바르게 했지만 자리를 바꾸지 않은 이입니다. 이는 원래 명제와 동치가 아닙니다."),
        Option("(¬p ∧ ¬q) → r", r"\(m\)과 \(n\)이 모두 홀수이면 \(mn\)은 짝수이다.", r"가정 쪽은 바르게 부정했지만 결론 쪽 '\(mn\)은 짝수'를 부정하지 않았습니다. \(m = n = 1\)이면 거짓인 명제입니다."),
    ),
    answer=1,
    judge=lambda formula: equivalent(formula, ITEM_15_STATEMENT),
    solution=rf"""
<p>p: \(m\)은 짝수이다, q: \(n\)은 짝수이다, r: \(mn\)은 짝수이다로 놓으면 원래 명제는 r → (p ∨ q)이고, 대우는 ¬(p ∨ q) → ¬r입니다. 드모르간의 법칙으로 ¬(p ∨ q) ≡ ¬p ∧ ¬q이고, 짝수가 아니면 홀수이므로 대우는 '\(m\)과 \(n\)이 모두 홀수이면 \(mn\)은 홀수이다'입니다.</p>
<p>이 대우는 바로 증명됩니다. \(m = 2a + 1\), \(n = 2b + 1\ (a, b \in Z)\)로 놓으면 다음과 같습니다.</p>
{ITEM_15_CALCULATION.html()}
<p>\(2ab + a + b\)는 정수이므로 \(mn\)은 홀수입니다. 가정이 '\(mn\)은 짝수'로 시작하는 원래 명제보다, '모두 홀수'에서 출발하는 대우가 식으로 옮기기 훨씬 쉽습니다.</p>
""",
    layout=Layout.LONG,
)

def _implication_fails(condition: bool, conclusion: bool) -> bool:
    """조건은 참인데 결론은 거짓인가. 해설에 든 반례를 확인할 때 쓴다."""
    return condition and not conclusion


SECTION_B: Section = Section(
    title="2. 대우증명법",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_11, ITEM_12, ITEM_13, ITEM_14, ITEM_15),
    checks=(
        ("문제 11 오답: n = 1에서 ③ 거짓, n = 2에서 ④ 거짓", lambda: _implication_fails(not is_even(1), is_even(1 * 1)) and _implication_fails(is_even(2), not is_even(2 * 2))),
        ("문제 13 해설: 계산 유도와 명제가 모든 정수에서 참", lambda: ITEM_13_CALCULATION.holds() and holds_on_residues(lambda n: not is_odd(5 * n + 2) or is_odd(n), 2)),
        ("문제 14 해설: 증명한 계산이 항등식", lambda: same_polynomial("(2*k + 1)**2", "4*k**2 + 4*k + 1") and same_polynomial("4*k**2 + 4*k + 1", "2*(2*k**2 + 2*k) + 1")),
        ("문제 15 해설: 계산 유도의 줄마다 항등식", ITEM_15_CALCULATION.holds),
        ("문제 15 해설: ¬(p ∨ q) → ¬r이 원래 명제와 동치", lambda: equivalent("¬(p ∨ q) → ¬r", ITEM_15_STATEMENT)),
        ("문제 15 오답: m = 1, n = 2에서 ② 거짓, m = n = 1에서 ⑤ 거짓", lambda: _implication_fails(is_odd(1) or is_odd(2), is_odd(1 * 2)) and _implication_fails(is_odd(1) and is_odd(1), is_even(1 * 1))),
    ),
)
