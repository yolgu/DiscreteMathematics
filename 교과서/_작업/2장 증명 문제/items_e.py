"""묶음 5 수학적 귀납법: 핵심 정리, 보기 5, 문제 27~35."""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction

from expr_tools import latex, same_polynomial
from fragments import CalcStep, Calculation
from logic_tools import INFERENCE_RULES, rule_matches
from model import Demand, Item, Layout, Option, Section, WorkedExample
from number_tools import NATURALS, is_even, is_multiple
from proof_methods import INDUCTION_HYPOTHESIS_IS_LEGITIMATE

SUMMARY: str = r"""
<ul>
  <li><strong>수학적 귀납법</strong>: 자연수 \(n\)에 관한 명제 \(P(n)\)이 모든 \(n\)에 대해 성립함을 세 단계로 보입니다.
    <ol>
      <li>기본 과정: 초깃값, 곧 논의영역의 가장 작은 값을 넣어 \(P\)가 참임을 계산해 보입니다. 논의영역이 \(n \ge 1\)이면 \(P(1)\)입니다.</li>
      <li>귀납 가정: 임의의 \(k\)에 대해 \(P(k)\)가 참이라고 가정합니다.</li>
      <li>귀납 단계: 귀납 가정을 이용해 \(P(k+1)\)이 참임을 증명합니다. \(P(k+1)\)은 \(P(n)\)의 \(n\) 자리에 \(k + 1\)을 넣은 명제입니다.</li>
    </ol>
  </li>
  <li><strong>세 단계로 충분한 까닭</strong>: 귀납 단계는 \(P(k) \rightarrow P(k+1)\)을 직접증명법으로 보인 것입니다. 기본 과정의 값에서 시작해 긍정논법을 되풀이하면 사슬이 논의영역의 모든 값에 닿습니다.</li>
  <li><strong>쓸 수 있는 곳</strong>: 초깃값에서 1씩 나아가며 모두 만날 수 있는 수(자연수, 0 이상의 정수 등)에 관한 명제에 씁니다. 실수에는 '바로 다음 수'가 없어 쓸 수 없습니다.</li>
  <li>\(n! = 1 \times 2 \times \cdots \times n\)이고, \((k+1)! = k! \times (k+1)\)입니다.</li>
</ul>
"""


def _sum_to(n: int) -> Fraction:
    return Fraction(sum(range(1, n + 1)))


WORKED_CALCULATION: Calculation = Calculation(
    first="",
    first_latex=r"1 + 2 + \cdots + k + (k + 1)",
    first_value=lambda k: _sum_to(k + 1),
    steps=(
        CalcStep("k*(k + 1)/2 + (k + 1)", r"귀납 가정 \(P(k)\)"),
        CalcStep("(k + 1)*(k/2 + 1)", r"\(k + 1\)로 묶음"),
        CalcStep("(k + 1)*(k + 2)/2", "괄호 안을 통분"),
    ),
)


def _worked_check() -> bool:
    return WORKED_CALCULATION.holds() and all(_sum_to(n) == Fraction(n * (n + 1), 2) for n in NATURALS)


WORKED: WorkedExample = WorkedExample(
    title="보기 5 수학적 귀납법으로 증명하기",
    body=rf"""
<p>\(n \ge 1\)일 때 \(1 + 2 + \cdots + n = \frac{{n(n+1)}}{{2}}\)임을 수학적 귀납법으로 증명하세요.</p>
<p class="solution-label">풀이</p>
<p>\(P(n)\): \(1 + 2 + \cdots + n = \frac{{n(n+1)}}{{2}}\)로 놓습니다. \(n \ge 1\)이므로 초깃값은 1입니다.</p>
<p><strong>기본 과정</strong> \(n = 1\)이면 좌변은 1, 우변은 \(\frac{{1 \times 2}}{{2}} = 1\)이므로 \(P(1)\)은 참입니다.</p>
<p><strong>귀납 가정</strong> 임의의 자연수 \(k\)에 대해 \(P(k)\): \(1 + 2 + \cdots + k = \frac{{k(k+1)}}{{2}}\)가 성립한다고 가정합니다.</p>
<p><strong>귀납 단계</strong> \(P(k+1)\): \(1 + 2 + \cdots + k + (k+1) = \frac{{(k+1)(k+2)}}{{2}}\)를 증명합니다. 좌변의 앞부분 \(1 + 2 + \cdots + k\)는 \(P(k)\)의 좌변과 같으므로 귀납 가정으로 바꿀 수 있습니다.</p>
{WORKED_CALCULATION.html()}
<p>마지막 줄은 \(P(k+1)\)의 우변이므로 \(P(k+1)\)이 참입니다.</p>
<p>∴ 수학적 귀납법에 따라 \(n \ge 1\)일 때 \(1 + 2 + \cdots + n = \frac{{n(n+1)}}{{2}}\)입니다. Q.E.D.</p>
""",
    check=_worked_check,
)


# ---- 문제 27: 가정하는 것 ----

def _even_sum(n: int) -> int:
    return sum(2 * i for i in range(1, n + 1))


ITEM_27: Item[str] = Item(
    number=27,
    demand=Demand.FOUNDATION,
    stem=r"<p>\(P(n)\): \(2 + 4 + 6 + \cdots + 2n = n(n+1)\)을 수학적 귀납법으로 증명할 때, 증명하지 않고 참이라고 <strong>가정</strong>하는 식을 고르세요.</p>",
    options=(
        Option("기본 과정", r"\(2 = 1 \times 2\)", r"\(n = 1\)을 넣은 \(P(1)\)입니다. 기본 과정에서 좌변 2와 우변 \(1 \times 2\)를 계산해 확인하는 식이지, 가정하는 식이 아닙니다."),
        Option("귀납 가정", r"\(2 + 4 + \cdots + 2k = k(k+1)\)"),
        Option("귀납 단계의 목표", r"\(2 + 4 + \cdots + 2k + 2(k+1) = (k+1)(k+2)\)", r"\(P(k+1)\)은 귀납 단계에서 증명할 목표입니다. 이것을 가정하면 증명할 것을 미리 참으로 놓는 셈입니다."),
        Option("명제 전체", r"\(2 + 4 + \cdots + 2n = n(n+1)\)", r"증명하려는 명제 전체입니다. 모든 \(n\)에 대해 이미 성립한다고 놓으면 증명할 것이 남지 않습니다. 귀납 가정은 임의의 \(k\) 하나에 대한 \(P(k)\)입니다."),
        Option("계산", r"\(k(k+1) + 2(k+1) = (k+1)(k+2)\)", r"귀납 단계에서 \(P(k+1)\)에 닿으려고 계산으로 확인하는 등식입니다. 양변을 전개하면 모두 \(k^2 + 3k + 2\)가 됩니다."),
    ),
    answer=2,
    judge=lambda role: role == "귀납 가정",
    solution=r"""
<p>세 단계 가운데 가정하는 것은 귀납 가정의 \(P(k)\), 곧 임의의 자연수 \(k\)에 대해 \(2 + 4 + \cdots + 2k = k(k+1)\)이 성립한다는 것 하나뿐입니다. 기본 과정의 \(P(1)\)은 계산으로 보이고, \(P(k+1)\)은 이 가정을 이용해 증명합니다.</p>
<p>귀납 단계는 \(2 + 4 + \cdots + 2k + 2(k+1) = k(k+1) + 2(k+1) = (k+1)(k+2)\)로 진행합니다. 둘째 식에서 귀납 가정을 썼습니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 28: 기본 과정 ----

def _odd_sum(n: int) -> int:
    """1 + 3 + ⋯ + (2n - 1). n = 0이면 더할 항이 없어 0이다."""
    return sum(2 * i - 1 for i in range(1, n + 1))


@dataclass(frozen=True)
class BasisAttempt:
    """기본 과정이라고 쓴 글: 넣은 값, 가정했는지, 계산한 좌변과 우변, 내린 판단."""

    n: int
    assumed: bool
    left: int
    right: int
    verdict: bool


ITEM_28_INITIAL: int = 1


def _basis_is_correct(attempt: BasisAttempt) -> bool:
    return (
        attempt.n == ITEM_28_INITIAL
        and not attempt.assumed
        and attempt.left == _odd_sum(attempt.n)
        and attempt.right == attempt.n ** 2
        and attempt.verdict == (attempt.left == attempt.right)
    )


ITEM_28: Item[BasisAttempt] = Item(
    number=28,
    demand=Demand.FOUNDATION,
    stem=r"<p>\(P(n)\): \(1 + 3 + 5 + \cdots + (2n - 1) = n^2\) (\(n \ge 1\))을 수학적 귀납법으로 증명할 때, 기본 과정으로 옳은 것을 고르세요.</p>",
    options=(
        Option(BasisAttempt(1, True, 0, 0, True), r"\(P(1)\)이 참이라고 가정한다.", r"기본 과정의 \(P(1)\)은 가정하는 것이 아니라 \(n = 1\)을 넣어 직접 계산해 보이는 것입니다. 가정하는 것은 귀납 가정의 \(P(k)\)뿐입니다."),
        Option(BasisAttempt(0, False, -1, 0, False), r"\(n = 0\)이면 좌변은 \(2 \times 0 - 1 = -1\), 우변은 \(0^2 = 0\)이므로 성립하지 않는다.", r"이 명제는 \(n \ge 1\)에 대한 것이므로 초깃값은 1입니다. 0은 논의영역 밖이고, 게다가 \(n = 0\)이면 더할 항이 하나도 없으므로 좌변을 \(-1\)로 계산한 것도 맞지 않습니다."),
        Option(BasisAttempt(1, False, 1, 1, True), r"\(n = 1\)이면 좌변은 1, 우변은 \(1^2 = 1\)이므로 \(P(1)\)은 참이다."),
        Option(BasisAttempt(1, False, 9, 1, False), r"\(n = 1\)이면 좌변은 \(1 + 3 + 5 = 9\), 우변은 \(1^2 = 1\)이므로 \(P(1)\)은 거짓이다.", r"좌변은 \(2n - 1\)까지 더하므로 \(n = 1\)이면 마지막 항이 \(2 \times 1 - 1 = 1\)이고, 좌변은 1 하나뿐입니다. 식에 예로 적어 둔 앞 항 1, 3, 5를 모두 더하면 안 됩니다."),
        Option(BasisAttempt(2, False, 4, 4, True), r"\(n = 2\)이면 좌변은 \(1 + 3 = 4\), 우변은 \(2^2 = 4\)이므로 \(P(2)\)가 참이다. 이것으로 기본 과정을 마친다.", r"계산은 맞지만 초깃값이 아닙니다. 사슬은 기본 과정의 값에서 시작하므로, \(P(2)\)에서 시작하면 \(P(1)\)이 빠집니다."),
    ),
    answer=3,
    judge=_basis_is_correct,
    solution=r"""
<p>초깃값은 논의영역 \(n \ge 1\)의 가장 작은 값 1입니다. \(n = 1\)이면 좌변은 마지막 항 \(2 \times 1 - 1 = 1\)까지 더한 것, 곧 1이고 우변은 \(1^2 = 1\)입니다. 양변이 같으므로 \(P(1)\)은 참입니다.</p>
<p>좌변처럼 '⋯'이 든 식은 일반항 \(2n - 1\)을 보고 \(n\)에 맞는 마지막 항이 무엇인지부터 정해야 합니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 29: P(k+1) 쓰기 ----

def _powers_of_two_sum(terms: int) -> int:
    """1 + 2 + 2^2 + ⋯ + 2^(terms-1), 곧 항이 terms개인 합."""
    return sum(2 ** i for i in range(terms))


Sides = tuple[Callable[[int], int], Callable[[int], int]]


def _is_p_of_k_plus_one(sides: Sides) -> bool:
    left, right = sides
    return all(left(k) == _powers_of_two_sum(k + 1) and right(k) == 2 ** (k + 1) - 1 for k in range(1, 21))


ITEM_29: Item[Sides] = Item(
    number=29,
    demand=Demand.FOUNDATION,
    stem=r"<p>\(P(n)\): \(1 + 2 + 2^2 + \cdots + 2^{n-1} = 2^n - 1\) (\(n \ge 1\))을 수학적 귀납법으로 증명합니다. 귀납 단계에서 증명할 \(P(k+1)\)을 바르게 쓴 것을 고르세요.</p>",
    options=(
        Option((lambda k: _powers_of_two_sum(k + 1), lambda k: 2 ** (k + 1) - 1), r"\(1 + 2 + \cdots + 2^{k-1} + 2^k = 2^{k+1} - 1\)"),
        Option((lambda k: _powers_of_two_sum(k), lambda k: 2 ** (k + 1) - 1), r"\(1 + 2 + \cdots + 2^{k-1} = 2^{k+1} - 1\)", r"우변만 바꾸고 좌변에 새로 더해지는 항을 빠뜨렸습니다. \(n = k + 1\)이면 좌변의 마지막 항은 \(2^{(k+1)-1} = 2^k\)입니다."),
        Option((lambda k: _powers_of_two_sum(k + 1), lambda k: 2 ** k - 1), r"\(1 + 2 + \cdots + 2^{k-1} + 2^k = 2^k - 1\)", r"좌변만 바꾸고 우변은 \(P(k)\)의 것을 그대로 두었습니다. 우변도 \(n\) 자리에 \(k + 1\)을 넣어 \(2^{k+1} - 1\)이 됩니다."),
        Option((lambda k: _powers_of_two_sum(k + 2), lambda k: 2 ** (k + 1) - 1), r"\(1 + 2 + \cdots + 2^k + 2^{k+1} = 2^{k+1} - 1\)", r"마지막 항을 \(2^{k+1}\)로 넣었습니다. 일반항은 \(2^{n-1}\)이므로 \(n = k + 1\)이면 \(2^k\)입니다. \(2^n\)에 \(k + 1\)을 넣은 것과 헷갈렸습니다."),
        Option((lambda k: _powers_of_two_sum(k) + 1, lambda k: 2 ** k - 1 + 1), r"\(1 + 2 + \cdots + 2^{k-1} + 1 = 2^k - 1 + 1\)", r"\(P(k+1)\)을 \(P(k)\)의 양변에 1을 더한 식으로 읽었습니다. \(P(k+1)\)은 \(P(n)\)의 \(n\) 자리에 \(k + 1\)을 넣은 명제입니다."),
    ),
    answer=1,
    judge=_is_p_of_k_plus_one,
    solution=r"""
<p>\(P(k+1)\)은 \(P(n)\)의 \(n\) 자리에 \(k + 1\)을 넣은 명제입니다. 좌변의 마지막 항 \(2^{n-1}\)은 \(2^{(k+1)-1} = 2^k\)가 되므로, 좌변은 \(P(k)\)의 좌변에 \(2^k\)를 하나 더 더한 것입니다. 우변은 \(2^{k+1} - 1\)입니다.</p>
<p>이렇게 써 두면 좌변에서 \(P(k)\)의 좌변을 찾아 귀납 가정을 쓸 수 있습니다. \((2^k - 1) + 2^k = 2 \times 2^k - 1 = 2^{k+1} - 1\)이므로 \(P(k+1)\)이 참입니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 30: 귀납 가정을 쓰는 줄 ----

ITEM_30_CALCULATION: Calculation = Calculation(
    first="",
    first_latex=r"1 + 3 + \cdots + (2k - 1) + (2k + 1)",
    first_value=lambda k: Fraction(_odd_sum(k + 1)),
    steps=(
        CalcStep("k**2 + (2*k + 1)", r"귀납 가정 \(P(k)\)"),
        CalcStep("k**2 + 2*k + 1", "괄호를 풂"),
        CalcStep("(k + 1)**2", "완전제곱식으로 묶음"),
    ),
)


def _expression_option(expression: str, why_wrong: str = "") -> Option[str]:
    return Option(expression, rf"\({latex(expression)}\)", why_wrong)


ITEM_30: Item[str] = Item(
    number=30,
    demand=Demand.FOUNDATION,
    stem=rf"<p>\(P(n)\): \(1 + 3 + 5 + \cdots + (2n - 1) = n^2\)의 귀납 단계입니다. 귀납 가정 \(P(k)\)를 쓴 줄 (가)에 알맞은 식을 고르세요.</p>{ITEM_30_CALCULATION.html(blank=0)}",
    options=(
        _expression_option("k**2", r"귀납 가정은 앞부분 \(1 + 3 + \cdots + (2k - 1)\)만 \(k^2\)으로 바꿉니다. 새로 더한 항 \(2k + 1\)은 그대로 남아야 합니다."),
        _expression_option("k**2 + (2*k - 1)", r"새로 더한 항은 \(n = k + 1\)일 때의 마지막 항 \(2(k+1) - 1 = 2k + 1\)입니다. \(2k - 1\)은 이미 \(k^2\) 안에 들어 있는 항입니다."),
        _expression_option("(k + 1)**2 + (2*k + 1)", r"귀납 가정 \(P(k)\)가 아니라 증명할 \(P(k+1)\)의 우변을 썼습니다. 앞부분 \(1 + 3 + \cdots + (2k - 1)\)은 홀수 \(k\)개의 합이므로 \(P(k)\)에 따라 \(k^2\)입니다."),
        _expression_option("(2*k - 1)**2 + (2*k + 1)", r"\(P(k)\)의 우변은 마지막 항의 제곱이 아니라 항의 개수 \(k\)의 제곱입니다. \(k = 2\)이면 \(1 + 3 = 4 = 2^2\)이지 \(3^2\)이 아닙니다."),
        _expression_option("k**2 + (2*k + 1)"),
    ),
    answer=5,
    judge=lambda expression: same_polynomial(expression, "(k + 1)**2"),
    solution=rf"""
<p>좌변의 앞부분 \(1 + 3 + \cdots + (2k - 1)\)은 \(P(k)\)의 좌변과 같으므로 귀납 가정에 따라 \(k^2\)으로 바꿉니다. 마지막 항 \(2k + 1\)은 그대로 둡니다.</p>
{ITEM_30_CALCULATION.html()}
<p>마지막 줄 \((k + 1)^2\)은 \(P(k+1)\)의 우변이므로 \(P(k+1)\)이 참입니다.</p>
""",
    layout=Layout.MEDIUM,
)


# ---- 문제 31: 사슬 ----

# P(1), P(2), P(3), P(4)를 명제 p1, p2, p3, p4로 놓는다. 기본 과정과 귀납 단계가 준 사실이다.
CHAIN_FACTS: frozenset[str] = frozenset({"p1", "p1 → p2", "p2 → p3", "p3 → p4"})
Inference = tuple[tuple[str, ...], str, str]


def _reaches_p3(inferences: tuple[Inference, ...]) -> bool:
    known: set[str] = set(CHAIN_FACTS)
    for premises, conclusion, rule in inferences:
        if not set(premises) <= known or rule not in INFERENCE_RULES or not rule_matches(rule, premises, conclusion):
            return False
        known.add(conclusion)
    return inferences[-1][1] == "p3"


ITEM_31: Item[tuple[Inference, ...]] = Item(
    number=31,
    demand=Demand.FOUNDATION,
    stem=r"<p>기본 과정에서 \(P(1)\)이 참임을, 귀납 단계에서 모든 자연수 \(k\)에 대해 \(P(k) \rightarrow P(k+1)\)이 참임을 보였습니다. 이로부터 \(P(3)\)이 참임을 바르게 이끌어 낸 것을 고르세요.</p>",
    options=(
        Option(((("p1", "p2 → p3"), "p3", "긍정논법"),), r"\(P(1)\)과 \(P(2) \rightarrow P(3)\)에서 긍정논법으로 \(P(3)\)", r"긍정논법은 함축의 조건과 같은 명제가 있어야 합니다. \(P(2) \rightarrow P(3)\)의 조건은 \(P(2)\)인데 가진 것은 \(P(1)\)입니다. 사슬의 고리 하나를 건너뛰었습니다."),
        Option(
            ((("p1 → p2", "p2 → p3"), "p1 → p3", "가설적 삼단논법"), (("p1 → p3",), "p3", "긍정논법")),
            r"\(P(1) \rightarrow P(2)\)와 \(P(2) \rightarrow P(3)\)에서 가설적 삼단논법으로 \(P(1) \rightarrow P(3)\)을 얻으므로 \(P(3)\)",
            r"\(P(1) \rightarrow P(3)\)까지는 맞지만, 함축만으로는 결론 \(P(3)\)이 나오지 않습니다. 기본 과정의 \(P(1)\)을 함께 써야 긍정논법으로 \(P(3)\)을 얻습니다. 첫 고리를 빠뜨린 셈입니다.",
        ),
        Option(((("p3",), "p3", "귀납 가정"),), r"귀납 가정에서 \(P(k)\)를 가정했으므로 \(k = 3\)으로 놓으면 \(P(3)\)", r"귀납 가정은 \(P(k)\)에서 \(P(k+1)\)로 가는 길을 보이려고 잠시 놓는 것이지, \(P(3)\)이 참이라고 받아들이는 것이 아닙니다."),
        Option(
            ((("p1", "p1 → p2"), "p2", "긍정논법"), (("p2", "p2 → p3"), "p3", "긍정논법")),
            r"\(P(1)\)과 \(P(1) \rightarrow P(2)\)에서 긍정논법으로 \(P(2)\), \(P(2)\)와 \(P(2) \rightarrow P(3)\)에서 긍정논법으로 \(P(3)\)",
        ),
        Option(((("p3 → p4",), "p3", "긍정논법"),), r"\(P(3) \rightarrow P(4)\)가 참이므로 긍정논법으로 \(P(3)\)", r"\(P(3) \rightarrow P(4)\)는 \(P(3)\)이 참이면 \(P(4)\)도 참이라는 말일 뿐, \(P(3)\)이 참이라는 말이 아닙니다."),
    ),
    answer=4,
    judge=_reaches_p3,
    solution=r"""
<p>기본 과정에서 \(P(1)\)이 참입니다. 귀납 단계를 \(k = 1\)에 쓰면 \(P(1) \rightarrow P(2)\)가 참이므로, 긍정논법으로 \(P(2)\)가 참입니다. 다시 \(k = 2\)에 쓰면 \(P(2) \rightarrow P(3)\)이 참이므로, 긍정논법으로 \(P(3)\)이 참입니다.</p>
<p>이 사슬을 이어 가면 어떤 자연수에도 닿습니다. 첫 고리(기본 과정)와 고리를 잇는 규칙(귀납 단계)이 모두 있어야 사슬이 됩니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 32: 초깃값 ----

ITEM_32_INITIAL: int = 0


def _basis_value_is_right(start: int | None) -> bool:
    return start == ITEM_32_INITIAL and 2 ** start >= start + 1


ITEM_32: Item[int | None] = Item(
    number=32,
    demand=Demand.FOUNDATION,
    stem=r"<p>\(P(n)\): \(2^n \ge n + 1\)이 0 이상의 모든 정수 \(n\)에 대해 성립함을 수학적 귀납법으로 증명하려고 합니다. 기본 과정에서 확인할 것을 고르세요.</p>",
    options=(
        Option(-1, r"\(P(-1)\): \(2^{-1} = \tfrac{1}{2} \ge -1 + 1\)", r"\(-1\)은 논의영역(0 이상의 정수) 밖입니다. 논의영역에 없는 값의 참, 거짓은 이 명제와 상관이 없습니다."),
        Option(0, r"\(P(0)\): \(2^0 = 1 \ge 0 + 1\)"),
        Option(1, r"\(P(1)\): \(2^1 = 2 \ge 1 + 1\)", r"초깃값을 늘 1로 잡았습니다. 이 명제의 논의영역은 0부터이므로, \(P(1)\)에서 시작하면 \(P(0)\)이 사슬에서 빠집니다."),
        Option(2, r"\(P(2)\): \(2^2 = 4 \ge 2 + 1\)", r"\(P(0)\)과 \(P(1)\)은 양쪽이 같아서 피하고, 부등호가 뚜렷이 성립하는 값을 골랐습니다. 양쪽이 같아도 \(\ge\)는 성립하고, 기본 과정은 논의영역의 가장 작은 값에서 해야 \(P(0)\)과 \(P(1)\)이 사슬에서 빠지지 않습니다."),
        Option(None, r"\(P(k)\): \(2^k \ge k + 1\)", r"\(P(k)\)는 귀납 가정에서 가정하는 것입니다. 기본 과정은 특정한 초깃값을 넣어 계산으로 확인합니다."),
    ),
    answer=2,
    judge=_basis_value_is_right,
    solution=r"""
<p>초깃값은 논의영역의 가장 작은 값입니다. 0 이상의 정수가 논의영역이므로 초깃값은 0이고, \(2^0 = 1\), \(0 + 1 = 1\)이므로 \(1 \ge 1\)로 \(P(0)\)이 참입니다. 양쪽이 같아도 \(\ge\)는 성립합니다.</p>
<p>이어서 귀납 단계에서는 \(2^{k+1} = 2 \times 2^k \ge 2(k + 1) = 2k + 2 \ge k + 2\)로 \(P(k+1)\)을 보입니다. 첫 부등식에 귀납 가정을, 둘째 부등식에 \(k \ge 0\)을 썼습니다.</p>
""",
    layout=Layout.MEDIUM,
)


# ---- 문제 33: 쓸 수 없는 곳 ----

@dataclass(frozen=True)
class StatementDomain:
    """명제의 논의영역: 초깃값과 그 안의 표본 원소들."""

    initial: Fraction
    members: tuple[Fraction, ...]

    def reachable_by_steps(self) -> bool:
        """모든 표본 원소가 초깃값에서 1씩 더해 닿는 값인가."""
        return all((x - self.initial).denominator == 1 and x >= self.initial for x in self.members)


NATURAL_DOMAIN: StatementDomain = StatementDomain(Fraction(1), tuple(Fraction(n) for n in range(1, 21)))
FROM_ZERO_DOMAIN: StatementDomain = StatementDomain(Fraction(0), tuple(Fraction(n) for n in range(0, 21)))
REALS_FROM_ONE: StatementDomain = StatementDomain(Fraction(1), tuple(Fraction(n, 4) for n in range(4, 21)))


def _bit_strings(length: int) -> int:
    return len(list(itertools.product("01", repeat=length)))


ITEM_33: Item[StatementDomain] = Item(
    number=33,
    demand=Demand.FOUNDATION,
    stem="<p>다음 명제는 모두 참입니다. 이 가운데 수학적 귀납법으로 증명하기에 알맞지 <strong>않은</strong> 것을 고르세요.</p>",
    options=(
        Option(NATURAL_DOMAIN, r"모든 자연수 \(n\)에 대해 \(n^3 - n\)은 6의 배수이다.", r"자연수에 관한 명제이므로 쓸 수 있습니다. 배수에 관한 명제도 \(P(k)\)에서 \(P(k+1)\)로 넘어가는 길을 보이면 됩니다."),
        Option(FROM_ZERO_DOMAIN, r"0 이상의 모든 정수 \(n\)에 대해 \(2^n \ge n + 1\)이다.", r"초깃값이 0일 뿐, 0에서 1씩 나아가며 모든 값을 만날 수 있습니다. 기본 과정에서 \(P(0)\)을 확인하면 됩니다(문제 32)."),
        Option(REALS_FROM_ONE, r"1 이상의 모든 실수 \(x\)에 대해 \(x^2 \ge x\)이다."),
        Option(NATURAL_DOMAIN, r"모든 자연수 \(n\)에 대해 \(n! \ge 2^{n-1}\)이다.", "등식이 아니라 부등식이어도 쓸 수 있습니다. 교과서 예제 2-41이 이 명제입니다."),
        Option(NATURAL_DOMAIN, r"\(n\)비트의 나열로 나타낼 수 있는 데이터의 최대 개수는 \(2^n\)이다.", r"식의 계산이 아니라 개수를 세는 명제여도, 자연수 \(n\)에 관한 것이면 쓸 수 있습니다. 교과서 예제 2-42가 이 명제입니다."),
    ),
    answer=3,
    judge=lambda domain: not domain.reachable_by_steps(),
    solution=r"""
<p>수학적 귀납법은 초깃값에서 시작해 \(k\)에서 \(k + 1\)로 한 칸씩 나아가는 사슬로 논의영역 전체를 덮습니다. 1 이상의 실수에는 \(\tfrac{3}{2}\)처럼 1에서 1씩 더해서는 닿지 않는 수가 끝없이 많으므로, 사슬이 논의영역 전체에 닿지 못합니다.</p>
<p>이 명제는 직접증명법으로 보입니다. \(x \ge 1\)이면 \(x &gt; 0\)이고 \(x - 1 \ge 0\)이므로 \(x^2 - x = x(x - 1) \ge 0\)입니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 34: 빠진 단계 ----

def _claim_2n_plus_1_even(n: int) -> bool:
    return is_even(2 * n + 1)


ITEM_34: Item[Callable[[], bool]] = Item(
    number=34,
    demand=Demand.VARIATION,
    stem=r"""<p>다음은 '모든 자연수 \(n\)에 대해 \(2n + 1\)은 짝수이다'를 증명했다는 글입니다. 이 글에 대한 설명으로 옳은 것을 고르세요.</p>
<p class="quote">귀납 가정: 임의의 자연수 \(k\)에 대해 \(2k + 1\)이 짝수라고 가정한다.<br>귀납 단계: \(2(k + 1) + 1 = (2k + 1) + 2\)이다.<br>짝수에 2를 더하면 짝수이므로 \(2(k + 1) + 1\)도 짝수이다.<br>따라서 모든 자연수 \(n\)에 대해 \(2n + 1\)은 짝수이다.</p>""",
    options=(
        Option(lambda: not same_polynomial("2*(k + 1) + 1", "(2*k + 1) + 2"), r"귀납 단계의 식 \(2(k + 1) + 1 = (2k + 1) + 2\)가 틀렸다.", r"\(2(k + 1) + 1 = 2k + 3 = (2k + 1) + 2\)이므로 이 식은 맞습니다."),
        Option(lambda: not all(is_even(e + 2) for e in range(-60, 61, 2)), "'짝수에 2를 더하면 짝수'라는 근거가 틀렸다.", r"짝수 \(2m\)에 2를 더하면 \(2(m + 1)\)로 짝수입니다. 이 근거는 맞습니다."),
        Option(lambda: not INDUCTION_HYPOTHESIS_IS_LEGITIMATE, r"귀납 가정에서 \(2k + 1\)이 짝수라고 증명 없이 놓은 것이 잘못이다.", r"\(P(k)\)를 가정하는 것은 수학적 귀납법의 정해진 단계입니다. 귀납 단계는 \(P(k) \rightarrow P(k+1)\)을 보이는 직접증명법이므로 \(P(k)\)에서 출발하는 것이 맞습니다."),
        Option(lambda: all(_claim_2n_plus_1_even(n) for n in NATURALS), "귀납 단계까지 바르게 보였으므로, 기본 과정이 없어도 이 명제는 참이다.", r"귀납 단계는 \(P(k)\)가 참이면 \(P(k+1)\)도 참이라는 고리일 뿐입니다. 첫 고리 \(P(1)\)이 없으면 사슬이 시작되지 않습니다. 실제로 \(2n + 1\)은 늘 홀수이므로 이 명제는 거짓입니다."),
        Option(lambda: not _claim_2n_plus_1_even(1), r"기본 과정이 빠졌고, 실제로 \(P(1)\)은 거짓이다."),
    ),
    answer=5,
    judge=lambda claim: claim(),
    solution=r"""
<p>이 글에는 귀납 가정과 귀납 단계만 있고 기본 과정이 없습니다. \(n = 1\)을 넣으면 \(2 \times 1 + 1 = 3\)은 홀수이므로 \(P(1)\)은 거짓입니다.</p>
<p>귀납 단계의 계산과 근거는 모두 맞아서 \(P(k) \rightarrow P(k+1)\) 자체는 참입니다. 그러나 긍정논법을 시작할 \(P(1)\)이 없으므로 어느 \(P(n)\)도 참이라고 할 수 없습니다. 실제로 \(2n + 1\)은 홀수의 정의 그대로의 꼴이라 늘 홀수입니다. 기본 과정은 빼먹어도 되는 형식이 아니라 사슬의 첫 고리입니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 35: 부등식의 귀납 단계 ----

ITEM_35_GAP: str = "2*k**2 - (k + 1)**2"
ITEM_35_INITIAL: int = 5


def _gap_positive_from_initial() -> bool:
    """k ≥ 5이면 (k - 1)^2 ≥ 16. (k - 1)^2은 k ≥ 1에서 커지기만 하므로 k = 5의 값이 가장 작다."""
    return (ITEM_35_INITIAL - 1) ** 2 == 16 and all((k - 1) ** 2 >= 16 for k in range(ITEM_35_INITIAL, 200))


ITEM_35: Item[Callable[[], bool]] = Item(
    number=35,
    demand=Demand.CHALLENGE,
    stem=r"""<p>\(P(n)\): \(2^n &gt; n^2\) (\(n \ge 5\))을 수학적 귀납법으로 증명합니다. 귀납 단계는 \(k \ge 5\)일 때의 귀납 가정 \(2^k &gt; k^2\)을 써서 다음과 같이 진행합니다.</p>
\[2^{k+1} = 2 \times 2^k &gt; 2k^2 \ge (k + 1)^2\]
<p>마지막 부등식 \(2k^2 \ge (k + 1)^2\)이 성립하는 까닭으로 옳은 것을 고르세요.</p>""",
    options=(
        Option(lambda: same_polynomial(ITEM_35_GAP, "(k - 1)**2 - 2") and _gap_positive_from_initial(), r"\(2k^2 - (k + 1)^2 = (k - 1)^2 - 2\)이고, \(k \ge 5\)이면 \((k - 1)^2 \ge 16\)이라 이 값이 양수이기 때문이다."),
        Option(lambda: all(2 * k * k >= (k + 1) ** 2 for k in NATURALS), r"모든 자연수 \(k\)에 대해 \(2k^2 \ge (k + 1)^2\)이기 때문이다.", r"\(k = 1\)이면 \(2 &lt; 4\), \(k = 2\)이면 \(8 &lt; 9\)로 성립하지 않습니다. 이 부등식은 \(k\)가 어느 정도 클 때만 성립하므로 \(k \ge 5\)라는 조건을 써야 합니다."),
        Option(lambda: same_polynomial(ITEM_35_GAP, "k**2 - 1"), r"\(2k^2 - (k + 1)^2 = k^2 - 1\)이고, \(k \ge 5\)이면 이 값이 양수이기 때문이다.", r"\((k + 1)^2\)을 \(k^2 + 1\)로 계산했습니다. \((k + 1)^2 = k^2 + 2k + 1\)이므로 차는 \(k^2 - 2k - 1\)입니다."),
        Option(lambda: all(2 * k * k >= (k + 1) ** 2 for k in NATURALS if 2 ** k > k * k), r"귀납 가정 \(2^k &gt; k^2\)의 양변에 2를 곱하면 \(2k^2 \ge (k + 1)^2\)이 나오기 때문이다.", r"양변에 2를 곱하면 \(2^{k+1} &gt; 2k^2\)이 나오고, 이것은 바로 앞 단계입니다. \(2k^2 \ge (k + 1)^2\)은 \(2^k\)와 상관없는 \(k\)에 대한 부등식이라 따로 보여야 합니다. 실제로 \(k = 1\)이면 \(2^1 &gt; 1^2\)인데 \(2 \ge 4\)는 거짓입니다."),
        Option(lambda: same_polynomial(ITEM_35_GAP, "(k - 1)**2"), r"\(2k^2 - (k + 1)^2 = (k - 1)^2\)이므로 늘 0 이상이기 때문이다.", r"괄호를 풀 때 부호를 잘못 처리했습니다. \(2k^2 - (k^2 + 2k + 1) = k^2 - 2k - 1\)이고, 이것은 \((k - 1)^2 = k^2 - 2k + 1\)보다 2만큼 작습니다."),
    ),
    answer=1,
    judge=lambda claim: claim(),
    solution=r"""
<p>두 식의 차를 계산합니다. \(2k^2 - (k + 1)^2 = 2k^2 - (k^2 + 2k + 1) = k^2 - 2k - 1 = (k - 1)^2 - 2\)입니다. 귀납 가정에서 \(k \ge 5\)이므로 \(k - 1 \ge 4\), \((k - 1)^2 \ge 16\)이고, 차는 \(16 - 2 = 14\) 이상의 양수입니다. 따라서 \(2k^2 &gt; (k + 1)^2\)입니다.</p>
<p>앞의 부등식과 이으면 \(2^{k+1} &gt; 2k^2 &gt; (k + 1)^2\), 곧 \(P(k+1)\)이 참입니다. 기본 과정은 \(2^5 = 32 &gt; 25 = 5^2\)입니다. 초깃값이 5인 까닭은 \(n = 2, 3, 4\)에서 \(2^n &gt; n^2\)이 성립하지 않기 때문입니다(\(4 = 4\), \(8 &lt; 9\), \(16 = 16\)).</p>
""",
    layout=Layout.LONG,
)

SECTION_E: Section = Section(
    title="5. 수학적 귀납법",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_27, ITEM_28, ITEM_29, ITEM_30, ITEM_31, ITEM_32, ITEM_33, ITEM_34, ITEM_35),
    checks=(
        ("문제 27: P(1)은 2 = 1 × 2, 귀납 단계의 등식, 명제가 표본 자연수에서 참", lambda: _even_sum(1) == 1 * 2 and same_polynomial("k*(k + 1) + 2*(k + 1)", "(k + 1)*(k + 2)") and same_polynomial("k*(k + 1) + 2*(k + 1)", "k**2 + 3*k + 2") and all(_even_sum(n) == n * (n + 1) for n in NATURALS)),
        ("문제 28: 명제가 표본 자연수에서 참이고 n = 0이면 좌변은 0", lambda: all(_odd_sum(n) == n * n for n in NATURALS) and _odd_sum(0) == 0),
        ("문제 29 해설: (2ᵏ - 1) + 2ᵏ = 2ᵏ⁺¹ - 1, 명제가 표본 자연수에서 참", lambda: all((2 ** k - 1) + 2 ** k == 2 ** (k + 1) - 1 for k in range(0, 60)) and all(_powers_of_two_sum(n) == 2 ** n - 1 for n in NATURALS)),
        ("문제 30 해설: 계산 유도의 줄마다 맞음", ITEM_30_CALCULATION.holds),
        ("문제 30 오답: k = 2이면 1 + 3 = 4 = 2²", lambda: _odd_sum(2) == 4 == 2 ** 2),
        ("문제 32 해설: 명제가 표본 값에서 참이고, k ≥ 0이면 2k + 2 ≥ k + 2", lambda: all(2 ** n >= n + 1 for n in range(0, 61)) and all(2 * k + 2 >= k + 2 for k in range(0, 61))),
        ("문제 33: 다섯 명제가 표본에서 모두 참", lambda: all(is_multiple(n ** 3 - n, 6) for n in NATURALS)
            and all(2 ** n >= n + 1 for n in range(0, 61))
            and all(x * x >= x for x in REALS_FROM_ONE.members)
            and all(math.factorial(n) >= 2 ** (n - 1) for n in range(1, 31))
            and all(_bit_strings(n) == 2 ** n for n in range(1, 11))),
        ("문제 34 해설: P(1)은 3이라 거짓, 2n + 1은 늘 홀수", lambda: not _claim_2n_plus_1_even(1) and not any(_claim_2n_plus_1_even(n) for n in range(-60, 61))),
        ("문제 35 해설: 기본 과정 32 > 25, n = 2, 3, 4에서는 성립하지 않음, 표본에서 n ≥ 5이면 참", lambda: 2 ** 5 > 5 ** 2 and not any(2 ** n > n * n for n in (2, 3, 4)) and all(2 ** n > n * n for n in range(5, 61))),
    ),
)
