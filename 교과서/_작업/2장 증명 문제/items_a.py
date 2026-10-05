"""묶음 1 증명의 정의와 직접증명법: 핵심 정리, 보기 1, 문제 1~10."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction

from expr_tools import latex, same_polynomial
from fragments import CalcStep, Calculation, computed_truth_table
from logic_tools import all_rows, entails, equivalent, value
from model import Demand, Item, Layout, Option, Section, WorkedExample
from number_tools import SAMPLE, holds_on_residues, holds_on_sample, is_even, is_multiple, is_odd
from proof_methods import START

SUMMARY: str = r"""
<ul>
  <li><strong>공리</strong>: 증명 없이 참으로 받아들이는 명제(무증명 명제)입니다. <strong>정의</strong>는 용어나 기호의 뜻을 확실하게 정한 문장이나 식으로, 처음부터 끝까지 같은 뜻으로만 씁니다. <strong>정리</strong>는 공리와 정의, 앞서 증명된 정리를 통해 참으로 확인된 명제이고, <strong>증명</strong>은 명제가 참임을 확인하는 과정입니다. 증명은 정당한 추론을 한 걸음씩 이어 갑니다.</li>
  <li><strong>직접증명법</strong>: 함축명제 p → q를 그대로 증명합니다. p가 참이라고 놓고, 공리와 정의와 정리를 이용해 q가 참임을 이끌어 냅니다.</li>
  <li><strong>배수, 짝수, 홀수의 정의</strong>: 정수 \(a\)가 정수 \(b\)의 배수라는 것은 \(a = bm\)인 정수 \(m\)이 있다는 뜻입니다. 3의 배수는 \(n = 3k\ (k \in Z)\)로 씁니다. 이 문제집에서는 짝수와 홀수도 정의대로 씁니다. 정수 \(n\)이 짝수라는 것은 \(n = 2k\)인 정수 \(k\)가 있다는 뜻이고, 홀수라는 것은 \(n = 2k + 1\)인 정수 \(k\)가 있다는 뜻입니다. 정수는 짝수와 홀수 가운데 꼭 하나입니다.</li>
  <li><strong>닫혀 있다</strong>: 어떤 수의 모임 안에서 계산한 결과가 늘 그 모임 안에 남을 때, 그 모임은 그 연산에 닫혀 있다고 합니다. 정수는 덧셈, 뺄셈, 곱셈에 닫혀 있고 나눗셈에는 닫혀 있지 않습니다.</li>
</ul>
"""

# 첫 줄은 n^2으로 찍고, 값은 n = 2k를 넣은 식으로 확인한다
WORKED_CALCULATION: Calculation = Calculation(
    first="(2*k)**2",
    first_latex="n^2",
    steps=(
        CalcStep("(2*k)**2", r"\(n = 2k\)를 넣음"),
        CalcStep("4*k**2", "거듭제곱을 풂"),
        CalcStep("2*(2*k**2)", "2를 앞으로 묶어 냄"),
    ),
)


def _worked_check() -> bool:
    return WORKED_CALCULATION.holds() and holds_on_residues(lambda n: is_odd(n) or is_even(n * n), 2)


WORKED: WorkedExample = WorkedExample(
    title="보기 1 직접증명법으로 증명하기",
    body=rf"""
<p>정수 \(n\)이 짝수이면 \(n^2\)도 짝수임을 직접증명법으로 증명하세요.</p>
<p class="solution-label">풀이</p>
<p>먼저 문장을 명제 둘로 나눕니다. p: 정수 \(n\)은 짝수이다. q: \(n^2\)은 짝수이다. 증명할 것은 p → q이고, 직접증명법이므로 p가 참이라고 놓고 출발합니다.</p>
<p>'짝수'라는 말로는 계산을 할 수 없으므로 정의로 식을 만듭니다. \(n\)이 짝수이므로 \(n = 2k\ (k \in Z)\)로 쓸 수 있습니다. 목표는 \(n^2\)을 '2 × 정수' 꼴로 쓰는 것입니다. 그래야 q에 나오는 '짝수'의 정의에 맞습니다.</p>
{WORKED_CALCULATION.html()}
<p>정수는 곱셈에 닫혀 있으므로 \(2k^2 = 2 \times k \times k\)는 정수입니다. 따라서 \(n^2 = 2(2k^2)\)은 짝수이고, q가 참입니다.</p>
<p>∴ 함축명제 p → q는 참입니다. Q.E.D.</p>
""",
    check=_worked_check,
)


# ---- 문제 1, 2: 증명의 재료 ----

ITEM_1: Item[str] = Item(
    number=1,
    demand=Demand.FOUNDATION,
    stem="<p>공리에 대한 설명으로 옳은 것을 고르세요.</p>",
    options=(
        Option("정리", "앞서 증명된 정리와 정의를 이용해 참으로 확인된 명제이다.", "정리에 대한 설명입니다. 공리는 다른 명제에 기대어 참임을 확인하지 않고 그대로 받아들입니다."),
        Option("정의", "용어나 기호의 뜻을 확실하게 정한 문장이나 식이다.", "정의에 대한 설명입니다. '3의 배수'의 뜻을 정한 것은 정의이고, '실수 \\(a\\), \\(b\\)에 대해 \\(a = b\\)이면 \\(a + 1 = b + 1\\)이다'처럼 참으로 받아들이는 명제가 공리입니다."),
        Option("가정", "한 증명 안에서만 잠시 참이라고 놓고 출발하는 명제이다.", "직접증명법에서 p를 참이라고 놓는 것과 같은 가정에 대한 설명입니다. 가정은 그 증명 안에서만 쓰지만, 공리는 어느 증명에서나 출발점으로 씁니다."),
        Option("공리", "증명 없이 참으로 받아들이는 명제이다."),
        Option("증명", "명제가 참임을 한 걸음씩 확인해 가는 과정이다.", "증명에 대한 설명입니다. 공리는 과정이 아니라 명제입니다."),
    ),
    answer=4,
    judge=lambda concept: concept == "공리",
    solution=r"""
<p>공리는 별도의 증명 없이 참으로 받아들여 이용하는 명제입니다. 어떤 명제를 증명하려면 이미 참인 명제가 있어야 하고, 그 명제도 또 다른 명제에 기대야 합니다. 이렇게 거슬러 올라가는 일이 끝없이 이어지지 않으려면 어딘가에 멈출 출발점이 있어야 하고, 그것이 공리입니다.</p>
<p>네 낱말을 견주어 정리하면, 공리와 정리는 둘 다 참인 명제이지만 공리는 증명 없이 받아들이고 정리는 증명으로 확인합니다. 정의는 말의 뜻을 정한 약속이고, 증명은 정리에 이르는 과정입니다.</p>
""",
    layout=Layout.LONG,
)

PROOF_GROUNDS: frozenset[str] = frozenset({"공리", "정의", "정리", "앞 걸음"})

ITEM_2: Item[str] = Item(
    number=2,
    demand=Demand.FOUNDATION,
    stem="<p>명제 A를 증명하고 있습니다. 이 증명의 근거로 쓸 수 <strong>없는</strong> 것을 고르세요.</p>",
    options=(
        Option("A 자신", "아직 증명하지 않은 명제 A 자신"),
        Option("공리", "증명 없이 참으로 받아들이는 공리", "공리는 증명의 출발점입니다. 증명되지 않았다고 못 쓰는 것이 아니라, 증명 없이 참으로 받아들이기로 정했기 때문에 근거로 씁니다."),
        Option("정의", "용어의 뜻을 정한 정의", "정의는 말을 식으로 옮기는 다리입니다. '3의 배수'를 \\(n = 3k\\)로 옮길 수 있는 것도 정의 덕분입니다."),
        Option("정리", "앞서 증명된 정리", "한번 증명된 정리는 다음 증명의 재료가 됩니다. 교과서 예제 2-14가 예제 2-5를 근거로 쓴 것이 그 예이고, 매번 공리에서 다시 시작할 필요는 없습니다."),
        Option("앞 걸음", "같은 증명에서 앞서 정당한 추론으로 이끌어 낸 명제", "증명은 정당한 추론을 한 걸음씩 이어 가는 일이므로, 앞 걸음에서 얻은 명제는 다음 걸음의 전제가 됩니다."),
    ),
    answer=1,
    judge=lambda ground: ground not in PROOF_GROUNDS,
    solution="""
<p>증명은 이미 참이라고 알고 있는 것에서 출발해 정당한 추론을 이어 A에 닿는 과정입니다. 그 출발점이 되는 것이 공리, 정의, 앞서 증명된 정리이고, 증명 중간에 정당한 추론으로 얻은 명제도 다음 걸음의 근거가 됩니다.</p>
<p>A 자신을 근거로 쓰면 'A가 참이다'를 'A가 참이다'로 보이는 셈이라 아무것도 확인하지 못합니다. 증명할 것을 미리 참으로 놓고 쓰는 이런 잘못은 문제를 풀 때 '결론을 가정하고 출발하는' 모습으로 자주 나타나니 주의하세요.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 3, 4: 직접증명법의 출발 ----

def _p_false_rows_all(implication_value: bool) -> bool:
    """p가 거짓인 모든 줄에서 p → q의 값이 implication_value인가."""
    return all(value("p → q", **row) == implication_value for row in all_rows(["p", "q"]) if not row["p"])


def _false_rows_of_implication() -> list[tuple[bool, bool]]:
    return [(row["p"], row["q"]) for row in all_rows(["p", "q"]) if not value("p → q", **row)]


ITEM_3: Item[Callable[[], bool]] = Item(
    number=3,
    demand=Demand.FOUNDATION,
    stem="<p>직접증명법으로 p → q를 증명할 때는 p가 참이라고 놓고 출발합니다. p가 거짓인 경우를 따로 살피지 않아도 되는 까닭을 고르세요.</p>",
    options=(
        Option(lambda: _p_false_rows_all(False), "p가 거짓이면 p → q도 거짓이 되어, 증명할 것이 없기 때문이다.", "함축의 진리표를 거꾸로 기억했습니다. p가 거짓인 두 줄에서 p → q는 F → T, F → F 모두 참입니다."),
        Option(lambda: entails(["p → q"], "¬p → ¬q"), "p가 거짓이면 q도 반드시 거짓이기 때문이다.", "p → q에서 ¬p → ¬q가 나온다고 본 것인데, ¬p → ¬q는 이라서 원래 명제와 동치가 아닙니다. p가 거짓이어도 q는 참일 수 있습니다."),
        Option(lambda: _p_false_rows_all(True), "p가 거짓이면 q의 진릿값과 상관없이 p → q는 참이기 때문이다."),
        Option(lambda: _false_rows_of_implication() == [(False, False)], "p → q가 거짓이 되는 경우는 p와 q가 모두 거짓일 때뿐이기 때문이다.", "p → q가 거짓이 되는 경우는 p가 참이고 q가 거짓일 때 하나뿐입니다. p와 q가 모두 거짓이면 F → F로 참입니다."),
        Option(lambda: equivalent("p → q", "q → p"), "p → q는 역 q → p와 동치라서, q가 참인 경우만 보아도 되기 때문이다.", "함축과 그 역은 동치가 아닙니다. p가 참이고 q가 거짓이면 p → q는 거짓이지만 q → p는 참입니다."),
    ),
    answer=3,
    judge=lambda claim: claim(),
    solution=f"""
<p>함축의 진리표를 봅니다.</p>
{computed_truth_table(["p", "q"], ["p → q"])}
<p>p가 거짓인 셋째 줄과 넷째 줄에서 p → q는 q와 상관없이 T입니다. p → q가 거짓이 될 수 있는 줄은 p가 T, q가 F인 둘째 줄 하나뿐입니다. 그래서 p가 참일 때 q도 반드시 참임을 보이면 둘째 줄이 일어날 수 없고, p → q는 어떤 경우에도 참이 됩니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_4: Item[str] = Item(
    number=4,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '정수 \(n\)이 홀수이면 \(n^2\)은 홀수이다'를 직접증명법으로 증명하려고 합니다. 처음에 참이라고 놓고 출발할 것을 고르세요.</p>",
    options=(
        Option("q", r"\(n^2\)이 홀수이다.", "증명할 결론을 먼저 참이라고 놓았습니다. 결론에서 출발하면 결론이 참이라는 것을 보인 것이 되지 않습니다."),
        Option("예", r"\(n = 3\)이다.", r"\(n = 3\) 하나에서 성립함을 보일 뿐입니다. 모든 홀수에 대해 보이려면 특정한 값이 아니라 임의의 홀수 \(n\)에서 출발해야 합니다."),
        Option("¬p", r"\(n\)이 홀수가 아니다.", "p가 거짓인 경우에는 p → q가 저절로 참이므로 살필 필요가 없습니다. 여기서 출발하면 결론 쪽에 대해 아무것도 알 수 없습니다."),
        Option("¬q", r"\(n^2\)이 홀수가 아니다.", "결론의 부정에서 출발하는 것은 묶음 2에서 배울 대우증명법의 출발점입니다. 직접증명법은 가정 p에서 출발합니다."),
        Option("p", r"\(n\)이 홀수이다."),
    ),
    answer=5,
    judge=lambda start: start == START["직접증명법"],
    solution=r"""
<p>p: \(n\)은 홀수이다, q: \(n^2\)은 홀수이다로 놓으면 증명할 것은 p → q입니다. 직접증명법은 p → q를 그대로 증명하므로, p가 참이라고 놓고 출발해 q가 참임을 이끌어 냅니다.</p>
<p>그래서 처음 놓는 것은 '\(n\)이 홀수이다'이고, 이어서 홀수의 정의에 따라 \(n = 2k + 1\ (k \in Z)\)로 써서 계산을 시작합니다.</p>
""",
    layout=Layout.MEDIUM,
)


# ---- 문제 5~8: 정의를 식으로 옮기고 계산하기 ----

def _written_as(form: Callable[[int], int], k_values: range) -> Callable[[int], bool]:
    """n이 form(k) 꼴로 쓰이는 k가 k_values 안에 있는가."""
    return lambda n: any(n == form(k) for k in k_values)


INTEGER_KS: range = range(-200, 201)
NATURAL_KS: range = range(1, 201)

ITEM_5: Item[Callable[[int], bool]] = Item(
    number=5,
    demand=Demand.FOUNDATION,
    stem=r"<p>정수 \(n\)이 홀수라는 것을 정의에 맞게 식으로 나타낸 것을 고르세요.</p>",
    options=(
        Option(_written_as(lambda k: 2 * k, INTEGER_KS), r"\(n = 2k\ (k \in Z)\)", r"짝수의 정의입니다. 이 꼴로 쓸 수 있는 정수는 0, \(\pm 2\), \(\pm 4\), …입니다."),
        Option(_written_as(lambda k: 2 * k + 1, INTEGER_KS), r"\(n = 2k + 1\ (k \in Z)\)"),
        Option(_written_as(lambda k: 2 * k + 1, NATURAL_KS), r"\(n = 2k + 1\) (\(k\)는 자연수)", r"\(k\)를 자연수로 제한하면 \(n\)은 3, 5, 7, …만 됩니다. 1이나 \(-1\), \(-3\) 같은 홀수를 나타내지 못합니다."),
        Option(lambda n: n == 2 * n + 1, r"\(n = 2n + 1\)", r"새 문자 없이 \(n\)을 그대로 썼습니다. \(n = 2n + 1\)을 풀면 \(n = -1\)뿐이라, 홀수 전체가 아니라 \(-1\) 하나를 나타냅니다. 정의에 나오는 정수는 \(n\)과 다른 새 문자로 둡니다."),
        # k가 실수이면 k = (n - 1)/2로 늘 고를 수 있다
        Option(lambda n: True, r"\(n = 2k + 1\) (\(k\)는 실수)", r"\(k\)가 실수이면 어떤 정수든 \(k = \frac{n-1}{2}\)로 맞출 수 있습니다. 예를 들어 \(4 = 2 \times 1.5 + 1\)이므로 짝수도 이 꼴이 됩니다. \(k\)가 정수라는 조건이 있어야 홀수만 남습니다."),
    ),
    answer=2,
    judge=lambda written_as: holds_on_sample(lambda n: written_as(n) == is_odd(n)),
    solution=r"""
<p>홀수는 짝수에 1을 더한 정수입니다. 그래서 정수 \(n\)이 홀수라는 것은 \(n = 2k + 1\)이 되는 정수 \(k\)가 있다는 뜻이고, \(n = 2k + 1\ (k \in Z)\)로 씁니다. 예를 들어 \(7 = 2 \times 3 + 1\), \(-3 = 2 \times (-2) + 1\)입니다.</p>
<p>정의를 식으로 옮길 때는 새 문자를 쓰고, 그 문자가 어떤 수인지(여기서는 정수)까지 적어야 합니다. 문자의 범위가 넓거나 좁으면 나타내는 수의 모임이 달라집니다.</p>
""",
    layout=Layout.MEDIUM,
)


def _closed(numbers: Callable[[int], bool], operation: Callable[[int, int], Fraction]) -> bool:
    """표본 안에서 numbers에 드는 두 수를 계산한 결과가 늘 numbers에 드는가(0으로 나누는 경우는 뺀다)."""
    members: list[int] = [n for n in SAMPLE if numbers(n)]
    results: list[Fraction] = [operation(a, b) for a in members for b in members if b != 0]
    return all(result.denominator == 1 and numbers(int(result)) for result in results)


def _is_integer_number(n: int) -> bool:
    return True


def _is_natural_number(n: int) -> bool:
    return n >= 1


ITEM_6: Item[Callable[[], bool]] = Item(
    number=6,
    demand=Demand.FOUNDATION,
    stem="<p>어떤 수의 모임 안에서 계산한 결과가 늘 그 모임 안에 남을 때, 그 모임은 그 연산에 닫혀 있다고 합니다. 옳은 것을 고르세요.</p>",
    options=(
        Option(lambda: _closed(_is_integer_number, lambda a, b: Fraction(a, b)), "정수는 나눗셈에 닫혀 있다.", r"\(1 \div 2 = \frac{1}{2}\)은 정수가 아닙니다. 결과가 모임 밖으로 나가는 경우가 하나라도 있으면 닫혀 있지 않습니다."),
        Option(lambda: _closed(_is_natural_number, lambda a, b: Fraction(a - b)), "자연수는 뺄셈에 닫혀 있다.", r"\(1 - 2 = -1\)은 자연수가 아닙니다. 정수는 뺄셈에 닫혀 있지만 자연수는 그렇지 않습니다."),
        Option(lambda: _closed(is_odd, lambda a, b: Fraction(a + b)), "홀수 전체는 덧셈에 닫혀 있다.", r"\(1 + 1 = 2\)는 짝수입니다. 실제로 \((2a + 1) + (2b + 1) = 2(a + b + 1)\)이라 두 홀수의 합은 늘 짝수입니다."),
        Option(lambda: _closed(is_even, lambda a, b: Fraction(a * b)), "짝수 전체는 곱셈에 닫혀 있다."),
        Option(lambda: not _closed(is_odd, lambda a, b: Fraction(a * b)), "홀수 전체는 곱셈에 닫혀 있지 않다.", r"덧셈에서 닫혀 있지 않다고 곱셈도 그럴 것이라고 넘겨짚었습니다. \((2a + 1)(2b + 1) = 2(2ab + a + b) + 1\)이므로 두 홀수의 곱은 늘 홀수이고, 홀수 전체는 곱셈에 닫혀 있습니다."),
    ),
    answer=4,
    judge=lambda claim: claim(),
    solution=r"""
<p>짝수 두 개를 \(2a\), \(2b\ (a, b \in Z)\)로 놓으면 \(2a \times 2b = 2(2ab)\)입니다. 정수는 곱셈에 닫혀 있으므로 \(2ab\)는 정수이고, 곱은 다시 짝수입니다. 어떤 두 짝수를 곱해도 짝수이므로 짝수 전체는 곱셈에 닫혀 있습니다.</p>
<p>닫혀 있지 않음을 보일 때는 결과가 밖으로 나가는 예 하나로 충분하지만, 닫혀 있음을 보일 때는 이처럼 임의의 두 수로 증명해야 합니다. 몇 쌍을 곱해 보는 것만으로는 부족합니다.</p>
""",
    layout=Layout.MEDIUM,
)

Expansion = tuple[str, str]


def _expansion_option(expansion: Expansion, why_wrong: str = "") -> Option[Expansion]:
    expanded, regrouped = expansion
    return Option(expansion, rf"\(n^2 = {latex(expanded)} = {latex(regrouped)}\)", why_wrong)


ITEM_7_CALCULATION: Calculation = Calculation(
    first="(2*k + 1)**2",
    steps=(
        CalcStep("4*k**2 + 4*k + 1", r"\((a + b)^2 = a^2 + 2ab + b^2\)으로 전개"),
        CalcStep("2*(2*k**2 + 2*k) + 1", "앞의 두 항에서 2를 묶어 냄"),
    ),
)

ITEM_7: Item[Expansion] = Item(
    number=7,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '정수 \(n\)이 홀수이면 \(n^2\)도 홀수이다'를 직접증명법으로 증명하려고 \(n = 2k + 1\ (k \in Z)\)로 놓았습니다. \(n^2\)을 바르게 계산하고 정리한 것을 고르세요.</p>",
    options=(
        _expansion_option(("4*k**2 + 1", "2*(2*k**2) + 1"), r"\((a + b)^2 = a^2 + b^2\)으로 계산해 가운데 항 \(2 \times 2k \times 1 = 4k\)를 빠뜨렸습니다. \(k = 1\)이면 \(n = 3\), \(n^2 = 9\)인데 이 식은 5입니다."),
        _expansion_option(("4*k**2 + 2*k + 1", "2*(2*k**2 + k) + 1"), r"가운데 항을 \(2k \times 1 = 2k\)로만 계산하고 2배를 빠뜨렸습니다. 가운데 항은 \(2 \times 2k \times 1 = 4k\)입니다."),
        _expansion_option(("4*k**2 + 4*k + 1", "2*(2*k**2 + 2*k) + 1")),
        _expansion_option(("2*k**2 + 4*k + 1", "2*(k**2 + 2*k) + 1"), r"\((2k)^2\)을 \(2k^2\)으로 계산했습니다. 괄호 안 전체를 제곱하므로 \((2k)^2 = 4k^2\)입니다."),
        _expansion_option(("4*k**2 + 4*k + 2", "2*(2*k**2 + 2*k + 1)"), r"마지막 항 \(1^2\)을 \(1 + 1 = 2\)로 계산했습니다. 그러면 \(n^2\)이 짝수라는 엉뚱한 결론이 나옵니다. \(1^2 = 1\)입니다."),
    ),
    answer=3,
    judge=lambda expansion: same_polynomial("(2*k + 1)**2", expansion[0]) and same_polynomial(expansion[0], expansion[1]),
    solution=rf"""
<p>\(n = 2k + 1\)을 넣어 전개하고, 홀수의 정의에 맞게 '2 × 정수 + 1' 꼴로 정리합니다.</p>
{ITEM_7_CALCULATION.html()}
<p>정수는 곱셈과 덧셈에 닫혀 있으므로 \(2k^2 + 2k\)는 정수입니다. 따라서 \(n^2\)은 '2 × 정수 + 1' 꼴이고 홀수입니다. 전개할 때는 \((a + b)^2 = a^2 + 2ab + b^2\)의 가운데 항 \(2ab\)를 빠뜨리지 않도록 주의합니다.</p>
""",
    layout=Layout.LONG,
)

PairForm = Callable[[int, int], bool]
PAIR_SAMPLE: range = range(-15, 16)
LETTER_VALUES: range = range(-20, 21)


def _both_multiples_of_three(m: int, n: int) -> bool:
    return is_multiple(m, 3) and is_multiple(n, 3)


ITEM_8: Item[PairForm] = Item(
    number=8,
    demand=Demand.FOUNDATION,
    stem=r"""<p>명제 '두 정수 \(m\), \(n\)이 3의 배수이면 \(m + n\)도 3의 배수이다'를 직접증명법으로 증명했습니다. (가)에 알맞은 것을 고르세요.</p>
<p class="quote">\(m\), \(n\)이 3의 배수라고 놓는다. 3의 배수의 정의에 따라 (가)로 쓸 수 있다. 이 두 식을 더해 3을 묶어 내면 \(m + n\)은 '3 × 정수' 꼴이 되므로 3의 배수이다.</p>""",
    options=(
        Option(lambda m, n: any(m == 3 * k and n == 3 * k for k in LETTER_VALUES), r"\(m = 3k\), \(n = 3k\ (k \in Z)\)", r"두 수에 같은 문자 \(k\)를 쓰면 \(m = n\)이 되어, 3과 6처럼 서로 다른 3의 배수를 나타내지 못합니다. 그러면 \(m = n\)인 경우만 증명한 셈입니다."),
        Option(lambda m, n: any(m == 3 * a for a in LETTER_VALUES) and any(n == 3 * b for b in LETTER_VALUES), r"\(m = 3a\), \(n = 3b\ (a, b \in Z)\)"),
        Option(lambda m, n: any(m + n == 3 * k for k in LETTER_VALUES), r"\(m + n = 3k\ (k \in Z)\)", r"증명할 결론을 식으로 옮겼습니다. 이것을 처음에 쓰면 결론을 가정하고 출발한 셈입니다. 옮겨야 할 것은 가정 '\(m\), \(n\)이 3의 배수'입니다."),
        Option(lambda m, n: (m, n) == (3, 6), r"\(m = 3\), \(n = 6\)", r"특정한 두 수만 다룹니다. 이 두 수에서 \(m + n = 9\)가 3의 배수임을 보여도 다른 3의 배수에 대해서는 아무것도 보이지 못합니다."),
        # a, b가 실수이면 a = m/3, b = n/3으로 늘 고를 수 있다
        Option(lambda m, n: True, r"\(m = 3a\), \(n = 3b\) (\(a\), \(b\)는 실수)", r"\(a\), \(b\)가 실수이면 \(1 = 3 \times \frac{1}{3}\)처럼 어떤 수든 이 꼴이 됩니다. \(a\), \(b\)가 정수라는 조건이 있어야 3의 배수만 나타냅니다."),
    ),
    answer=2,
    judge=lambda form: all(form(m, n) == _both_multiples_of_three(m, n) for m in PAIR_SAMPLE for n in PAIR_SAMPLE),
    solution=r"""
<p>가정 '\(m\), \(n\)이 3의 배수'를 정의에 따라 식으로 옮깁니다. \(m\)과 \(n\)은 서로 다른 수일 수 있으므로 서로 다른 문자를 써서 \(m = 3a\), \(n = 3b\ (a, b \in Z)\)로 놓습니다.</p>
<p>그러면 \(m + n = 3a + 3b = 3(a + b)\)이고, 정수는 덧셈에 닫혀 있으므로 \(a + b\)는 정수입니다. 따라서 \(m + n\)은 3의 배수입니다.</p>
""",
    layout=Layout.MEDIUM,
)


# ---- 문제 9: 근거가 틀린 줄 ----

@dataclass(frozen=True)
class ProofLine:
    """증명 글의 한 줄: 이름, 적은 내용, 오른쪽 칸의 근거, 앞 줄들이 맞을 때 그 근거로 이 줄이 나오는지."""

    label: str
    claim: str
    reason: str
    follows: Callable[[], bool]


ITEM_9_LINES: tuple[ProofLine, ...] = (
    ProofLine("(가)", r"\(n\)이 3의 배수라고 놓는다.", "직접증명법의 가정", lambda: START["직접증명법"] == "p"),
    ProofLine("(나)", r"\(n = 3k\ (k \in Z)\)로 쓸 수 있다.", "3의 배수의 정의", lambda: all(any(n == 3 * k for k in LETTER_VALUES) for n in PAIR_SAMPLE if is_multiple(n, 3))),
    ProofLine("(다)", r"\(n = 6 \times \frac{k}{2}\)이다.", r"\(3k = 6 \times \frac{k}{2}\)", lambda: same_polynomial("3*k", "6*(k/2)")),
    ProofLine("(라)", r"\(\frac{k}{2}\)는 정수이다.", "정수는 나눗셈에 닫혀 있음", lambda: all(Fraction(k, 2).denominator == 1 for k in SAMPLE)),
    ProofLine("(마)", r"따라서 \(n\)은 6의 배수이다.", "(다), (라)와 6의 배수의 정의", lambda: all(is_multiple(6 * m, 6) for m in SAMPLE)),
)


def _proof_table(lines: tuple[ProofLine, ...]) -> str:
    rows: str = "".join(
        f'<tr><td class="step-sign">{line.label}</td><td>{line.claim}</td><td class="step-reason">{line.reason}</td></tr>'
        for line in lines
    )
    return f'<table class="derivation">{rows}</table>'


def _line_option(line: ProofLine, why_wrong: str = "") -> Option[ProofLine]:
    return Option(line, line.label, why_wrong)


ITEM_9: Item[ProofLine] = Item(
    number=9,
    demand=Demand.FOUNDATION,
    stem=rf"<p>다음은 '정수 \(n\)이 3의 배수이면 \(n\)은 6의 배수이다'를 증명하려고 쓴 글입니다. 앞 줄들이 모두 맞다고 할 때, 오른쪽 칸의 근거로 그 줄을 이끌어 낼 수 <strong>없는</strong> 줄을 고르세요.</p>{_proof_table(ITEM_9_LINES)}",
    options=(
        _line_option(ITEM_9_LINES[0], "직접증명법은 가정 p, 곧 '\\(n\\)이 3의 배수'를 참이라고 놓고 출발합니다. 바른 출발입니다."),
        _line_option(ITEM_9_LINES[1], "3의 배수의 정의 그대로입니다."),
        _line_option(ITEM_9_LINES[2], r"\(6 \times \frac{k}{2} = 3k\)이므로 계산은 맞습니다. 문제는 \(\frac{k}{2}\)가 정수인지이고, 그것은 다음 줄의 일입니다."),
        _line_option(ITEM_9_LINES[3]),
        _line_option(ITEM_9_LINES[4], r"(라)가 맞다면 \(n\)은 '6 × 정수' 꼴이므로 6의 배수입니다. 이 줄의 추론 자체는 바르고, 기대고 있는 (라)가 틀렸을 뿐입니다."),
    ),
    answer=4,
    judge=lambda line: not line.follows(),
    solution=r"""
<p>(라)의 근거가 틀렸습니다. 정수는 나눗셈에 닫혀 있지 않습니다. \(k = 1\)이면 \(\frac{k}{2} = \frac{1}{2}\)은 정수가 아닙니다.</p>
<p>(라)가 무너지면 그 위에 선 (마)의 결론도 근거를 잃습니다. 실제로 \(n = 3\)은 3의 배수이지만 6의 배수가 아니므로, 이 명제는 거짓입니다. 증명의 한 줄 한 줄이 맞는지 따질 때는 계산뿐 아니라 '정수이다' 같은 주장의 근거도 확인해야 합니다.</p>
""",
    layout=Layout.SHORT,
)


# ---- 문제 10: 배수 관계를 식으로 ----

TRIPLE_SAMPLE: range = range(-6, 7)
MULTIPLIERS: range = range(-40, 41)


def _is_multiple_of(a: int, b: int) -> bool:
    """정의 그대로: a = bm인 정수 m이 있는가(b = 0이면 a = 0일 때만)."""
    return any(a == b * m for m in MULTIPLIERS)


@dataclass(frozen=True)
class Translation:
    """가정을 옮긴 식이 나타내는 (a, b, c)의 조건과, 그 식에서 이끌어 낸 줄이 맞는지."""

    represents: Callable[[int, int, int], bool]
    derivation_holds: Callable[[], bool]


def _faithful(translation: Translation) -> bool:
    return all(
        translation.represents(a, b, c) == (_is_multiple_of(a, b) and _is_multiple_of(b, c))
        for a in TRIPLE_SAMPLE
        for b in TRIPLE_SAMPLE
        for c in TRIPLE_SAMPLE
    )


ITEM_10: Item[Translation] = Item(
    number=10,
    demand=Demand.VARIATION,
    stem=r"<p>정수 \(a\), \(b\), \(c\)에 대한 명제 '\(a\)가 \(b\)의 배수이고 \(b\)가 \(c\)의 배수이면 \(a\)는 \(c\)의 배수이다'를 직접증명법으로 증명하려고 합니다. 가정을 식으로 옮기고 정리한 것으로 옳은 것을 고르세요.</p>",
    # m과 n이 따로 정해지는 두 식은 하나씩 확인한다. 같은 문자를 쓴 식만 한꺼번에 찾는다.
    options=(
        Option(
            Translation(lambda a, b, c: _is_multiple_of(a, b) and _is_multiple_of(b, c), lambda: same_polynomial("m*(n*c)", "(m*n)*c")),
            r"\(a = mb\), \(b = nc\ (m, n \in Z)\)이므로 \(a = (mn)c\)",
        ),
        Option(
            Translation(lambda a, b, c: any(a == m * b and b == m * c for m in MULTIPLIERS), lambda: same_polynomial("m*(m*c)", "m**2*c")),
            r"\(a = mb\), \(b = mc\ (m \in Z)\)이므로 \(a = m^2c\)",
            r"두 가정에 같은 문자 \(m\)을 썼습니다. 그러면 \(a\)가 \(b\)의 몇 배인지와 \(b\)가 \(c\)의 몇 배인지가 같은 경우만 다룹니다. \(a = 6\), \(b = 2\), \(c = 1\)이면 3배와 2배라 이 꼴로 쓸 수 없습니다.",
        ),
        Option(
            Translation(lambda a, b, c: _is_multiple_of(b, a) and _is_multiple_of(c, b), lambda: same_polynomial("n*(m*a)", "(m*n)*a")),
            r"\(b = ma\), \(c = nb\ (m, n \in Z)\)이므로 \(c = (mn)a\)",
            r"'\(a\)가 \(b\)의 배수'를 \(b = ma\)로 거꾸로 옮겼습니다. \(a\)가 \(b\)의 배수라는 것은 \(a\)가 \(b\)의 몇 배라는 뜻이므로 \(a = mb\)입니다. 예를 들어 6은 2의 배수이고 \(6 = 3 \times 2\)입니다.",
        ),
        Option(
            Translation(lambda a, b, c: _is_multiple_of(a, b) and _is_multiple_of(b, c), lambda: same_polynomial("m*(n*c)", "(m + n)*c")),
            r"\(a = mb\), \(b = nc\ (m, n \in Z)\)이므로 \(a = (m + n)c\)",
            r"\(a = mb\)의 \(b\) 자리에 \(nc\)를 넣으면 \(a = m(nc) = (mn)c\)입니다. 곱해야 할 \(m\)과 \(n\)을 더했습니다.",
        ),
        Option(
            Translation(lambda a, b, c: _is_multiple_of(a, b) and _is_multiple_of(c, b), lambda: all(Fraction(m, n).denominator == 1 for m in TRIPLE_SAMPLE for n in TRIPLE_SAMPLE if n != 0)),
            r"\(a = mb\), \(c = nb\ (m, n \in Z)\)이므로 \(a = \frac{m}{n}c\)",
            r"'\(b\)가 \(c\)의 배수'를 \(c = nb\)로 거꾸로 옮겼습니다. 게다가 \(\frac{m}{n}\)은 정수가 아닐 수 있으므로 이 꼴로는 \(a\)가 \(c\)의 배수라고 할 수 없습니다.",
        ),
    ),
    answer=1,
    judge=lambda translation: _faithful(translation) and translation.derivation_holds(),
    solution=r"""
<p>배수의 정의대로 가정 둘을 \(a = mb\), \(b = nc\ (m, n \in Z)\)로 옮깁니다. 두 가정은 서로 다른 관계이므로 다른 문자를 씁니다.</p>
<p>\(a = mb\)의 \(b\) 자리에 \(nc\)를 넣으면 \(a = m(nc) = (mn)c\)입니다. 정수는 곱셈에 닫혀 있으므로 \(mn\)은 정수이고, 따라서 \(a\)는 \(c\)의 배수입니다. 'A가 B의 배수'는 'A = B × 정수'로 옮긴다는 방향을 늘 확인하세요.</p>
""",
    layout=Layout.LONG,
)

SECTION_A: Section = Section(
    title="1. 증명의 정의와 직접증명법",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_1, ITEM_2, ITEM_3, ITEM_4, ITEM_5, ITEM_6, ITEM_7, ITEM_8, ITEM_9, ITEM_10),
    checks=(
        ("문제 6 해설: 두 짝수의 곱 2a × 2b = 2(2ab)", lambda: same_polynomial("(2*a)*(2*b)", "2*(2*a*b)")),
        ("문제 6 오답: 두 홀수의 합과 곱", lambda: same_polynomial("(2*a + 1) + (2*b + 1)", "2*(a + b + 1)") and same_polynomial("(2*a + 1)*(2*b + 1)", "2*(2*a*b + a + b) + 1")),
        ("문제 7 해설: 계산 유도의 줄마다 항등식", ITEM_7_CALCULATION.holds),
        ("문제 7 오답: k = 1에서 4k² + 1 = 5", lambda: (4 * 1 + 1, (2 * 1 + 1) ** 2) == (5, 9)),
        ("문제 8 해설: 3a + 3b = 3(a + b)", lambda: same_polynomial("3*a + 3*b", "3*(a + b)")),
        ("문제 9 해설: n = 3은 3의 배수이지만 6의 배수가 아님", lambda: is_multiple(3, 3) and not is_multiple(3, 6)),
        ("문제 10 오답: a = 6, b = 2, c = 1은 가정을 만족하지만 같은 문자 m으로는 쓸 수 없음", lambda: _is_multiple_of(6, 2) and _is_multiple_of(2, 1) and not any(6 == m * 2 and 2 == m * 1 for m in MULTIPLIERS)),
    ),
)
