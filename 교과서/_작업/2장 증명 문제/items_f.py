"""묶음 6 섞어 풀기: 문제 36~40. 앞 묶음의 유형이 섞여 있어 방법부터 골라야 한다."""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable

from expr_tools import evaluate, latex, same_polynomial
from logic_tools import entails, equivalent
from model import Demand, Item, Layout, Option, Section
from number_tools import NATURALS, SAMPLE, holds_on_residues, holds_on_sample, is_even, is_multiple, is_odd


# ---- 문제 36: '어떤'이 붙은 명제의 판정 ----

def _square_plus_one_multiple_of_ten(n: int) -> bool:
    return is_multiple(n * n + 1, 10)


def _first_natural_example() -> int | None:
    return next((n for n in NATURALS if _square_plus_one_multiple_of_ten(n)), None)


ITEM_36: Item[Callable[[], bool]] = Item(
    number=36,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '어떤 자연수 \(n\)에 대해 \(n^2 + 1\)은 10의 배수이다'에 대한 판단으로 옳은 것을 고르세요.</p>",
    options=(
        Option(lambda: _first_natural_example() is None, r"거짓이다. \(n = 1\)이면 \(n^2 + 1 = 2\)라 10의 배수가 아니기 때문이다.", r"\(n = 1\)에서 성립하지 않는다는 것은 예가 아닌 값을 하나 찾은 것일 뿐입니다. '어떤'이 붙은 명제는 예가 하나만 있어도 참이므로, 다른 자연수에서 성립할 수 있습니다. 실제로 \(n = 3\)이 예입니다."),
        Option(lambda: _first_natural_example() is None, "판정할 수 없다. 자연수는 끝없이 많아 모두 확인할 수 없기 때문이다.", r"'어떤'이 붙은 명제가 참임을 보이는 데에는 모든 자연수를 확인할 필요가 없습니다. 예 하나를 찾으면 됩니다(존재증명법). \(n = 3\)이면 \(3^2 + 1 = 10\)입니다."),
        Option(lambda: -3 in NATURALS and _square_plus_one_multiple_of_ten(-3), r"참이다. \(n = -3\)이면 \(n^2 + 1 = 10\)이 10의 배수이기 때문이다.", r"\((-3)^2 + 1 = 10\)은 맞지만, \(-3\)은 자연수가 아니므로 이 명제의 논의영역 밖입니다. 예는 논의영역 안에서 찾아야 합니다."),
        Option(lambda: 3 in NATURALS and _square_plus_one_multiple_of_ten(3), r"참이다. \(n = 3\)이면 \(n^2 + 1 = 10\)이 10의 배수이기 때문이다."),
        Option(lambda: all(_square_plus_one_multiple_of_ten(n) for n in NATURALS), r"참인지 알려면 수학적 귀납법으로 모든 자연수 \(n\)에 대해 \(n^2 + 1\)이 10의 배수임을 보여야 한다.", r"'어떤'이 붙은 명제를 '모든'이 붙은 명제로 바꿔 읽었습니다. 게다가 \(n = 1\)이면 \(n^2 + 1 = 2\)이므로, 모든 자연수에 대해서는 성립하지도 않습니다."),
    ),
    answer=4,
    judge=lambda claim: claim(),
    solution=r"""
<p>'어떤 자연수 \(n\)에 대해'가 붙은 명제는 조건을 만족하는 자연수가 하나라도 있으면 참입니다. 그래서 예 하나를 찾는 존재증명법을 씁니다.</p>
<p>\(n = 1, 2, 3\)을 차례로 넣으면 \(n^2 + 1\)은 2, 5, 10이고, \(n = 3\)에서 10의 배수가 됩니다. 3은 자연수이므로 이 명제는 참입니다. 예가 아닌 값(\(n = 1, 2\))이 있다는 것은 판정에 아무 영향이 없습니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 37: 개수를 세는 귀납 단계 ----

TERNARY_DIGITS: str = "012"


def _ternary_strings(length: int) -> int:
    return sum(1 for _ in itertools.product(TERNARY_DIGITS, repeat=length))


def _counts_next_length(expression: str) -> bool:
    return all(evaluate(expression, k=k) == _ternary_strings(k + 1) for k in range(1, 9))


def _count_option(expression: str, why_wrong: str = "") -> Option[str]:
    return Option(expression, rf"\({latex(expression)}\)개", why_wrong)


ITEM_37: Item[str] = Item(
    number=37,
    demand=Demand.FOUNDATION,
    stem=r"<p>각 자리에 0, 1, 2 가운데 하나를 쓰는 길이 \(n\)의 나열을 삼진 나열이라고 합니다. '길이 \(n\)인 삼진 나열은 모두 \(3^n\)개이다'를 수학적 귀납법으로 증명합니다. 귀납 가정에 따라 길이 \(k\)인 삼진 나열이 \(3^k\)개일 때, 길이 \(k + 1\)인 삼진 나열의 개수를 고르세요.</p>",
    options=(
        _count_option("3**k + 1", r"길이 \(k\)인 나열에 새 나열이 하나 더해진다고 보았습니다. 길이 \(k\)인 나열 하나마다 뒤에 0, 1, 2 가운데 하나를 붙일 수 있으므로, 나열 하나가 셋으로 늘어납니다."),
        _count_option("3**k + 3", r"새 자리에 올 수 있는 글자 3개를 더했습니다. 새 자리의 글자는 길이 \(k\)인 나열 하나하나에 대해 따로 고르므로, 더하는 것이 아니라 곱해야 합니다."),
        _count_option("3*(k + 1)", r"자리 수 \(k + 1\)에 자리마다의 경우 3을 곱했습니다. 자리마다 3가지씩 고르면 3을 자리 수만큼 거듭 곱해야 합니다. \(k = 1\)이면 길이 2인 나열은 00부터 22까지 9개인데 \(3(1 + 1) = 6\)입니다."),
        _count_option("2*3**k", r"새 자리에 0 또는 1의 두 가지만 온다고 보았습니다. 비트 나열과 달리 삼진 나열은 자리마다 0, 1, 2의 세 가지가 올 수 있습니다."),
        _count_option("3*3**k"),
    ),
    answer=5,
    judge=_counts_next_length,
    solution=r"""
<p>길이 \(k + 1\)인 나열은 앞의 \(k\)자리와 마지막 한 자리로 나뉩니다. 앞의 \(k\)자리는 길이 \(k\)인 삼진 나열이므로 귀납 가정에 따라 \(3^k\)가지입니다. 그 하나하나의 뒤에 마지막 자리로 0, 1, 2 가운데 하나를 붙이므로, 나열 하나가 셋으로 늘어납니다.</p>
<p>따라서 개수는 \(3 \times 3^k = 3^{k+1}\)이고, 이것은 \(P(k+1)\)이 말하는 개수와 같습니다. 기본 과정은 길이 1인 나열이 0, 1, 2의 3개, 곧 \(3^1\)개라는 것입니다.</p>
""",
    layout=Layout.SHORT,
)


# ---- 문제 38: 참인 함축명제에서 반드시 참인 것 ----

# p: n이 4의 배수이다, q: n이 짝수이다
CONDITION_CLAUSE: dict[str, str] = {
    "p": r"\(n\)이 4의 배수이면",
    "¬p": r"\(n\)이 4의 배수가 아니면",
    "q": r"\(n\)이 짝수이면",
    "¬q": r"\(n\)이 짝수가 아니면",
}
CONCLUSION_CLAUSE: dict[str, str] = {
    "p": r"\(n\)은 4의 배수이다",
    "¬p": r"\(n\)은 4의 배수가 아니다",
    "q": r"\(n\)은 짝수이다",
    "¬q": r"\(n\)은 짝수가 아니다",
}
CLAUSE_TRUTH: dict[str, Callable[[int], bool]] = {
    "p": lambda n: is_multiple(n, 4),
    "¬p": lambda n: not is_multiple(n, 4),
    "q": is_even,
    "¬q": is_odd,
}
ITEM_38_GIVEN: str = "p → q"


def _statement_option(condition: str, conclusion: str, why_wrong: str = "") -> Option[str]:
    return Option(f"{condition} → {conclusion}", f"{CONDITION_CLAUSE[condition]} {CONCLUSION_CLAUSE[conclusion]}.", why_wrong)


def _fails_at(n: int, condition: str, conclusion: str) -> bool:
    """n이 조건은 만족하는데 결론은 만족하지 않는 반례인가. 해설에 든 반례를 확인할 때 쓴다."""
    return CLAUSE_TRUTH[condition](n) and not CLAUSE_TRUTH[conclusion](n)


ITEM_38: Item[str] = Item(
    number=38,
    demand=Demand.FOUNDATION,
    stem=r"<p>정수 \(n\)에 대해 '\(n\)이 4의 배수이면 \(n\)은 짝수이다'는 참입니다. 이 사실만으로 반드시 참이라고 할 수 있는 명제를 고르세요.</p>",
    options=(
        _statement_option("q", "p", r"원래 명제의 역입니다. 역은 원래 명제와 동치가 아니므로 따로 따져야 하고, 실제로 \(n = 2\)는 짝수이지만 4의 배수가 아니므로 거짓입니다."),
        _statement_option("¬p", "¬q", r"원래 명제의 이입니다. 이는 원래 명제와 동치가 아니므로 따로 따져야 하고, 실제로 \(n = 2\)는 4의 배수가 아니지만 짝수이므로 거짓입니다."),
        _statement_option("¬q", "¬p"),
        _statement_option("¬p", "q", r"조건만 부정하고 결론은 그대로 두었습니다. 원래 명제는 조건이 거짓일 때의 결론에 대해 아무것도 말하지 않습니다. \(n = 1\)은 4의 배수가 아니고 짝수도 아니므로 거짓입니다."),
        _statement_option("¬q", "p", r"결론만 부정해 조건 자리로 옮겼습니다. 대우는 조건과 결론을 둘 다 부정하고 자리를 바꾼 것입니다. \(n = 1\)은 짝수가 아니지만 4의 배수도 아니므로 거짓입니다."),
    ),
    answer=3,
    judge=lambda statement: entails([ITEM_38_GIVEN], statement),
    solution=r"""
<p>원래 명제를 p → q로 놓으면(p: \(n\)이 4의 배수, q: \(n\)이 짝수), ③은 ¬q → ¬p, 곧 대우입니다. 대우는 원래 명제와 동치이므로 원래 명제가 참이면 반드시 참입니다. 이 동치를 이용해 원래 명제 대신 대우를 증명하는 것이 대우증명법입니다.</p>
<p>역(①)과 이(②)는 원래 명제와 동치가 아니어서, 원래 명제가 참이라는 사실만으로는 참이라고 할 수 없습니다. 실제로 이 명제에서는 \(n = 2\)가 둘 모두의 반례입니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 39: 증명이 되지 않는 계획 ----

# p: 3n이 짝수이다, q: n이 짝수이다. 계획마다 해내면 실제로 참임이 보장되는 명제를 둔다.
ITEM_39_TARGET: str = "p → q"

ITEM_39: Item[str] = Item(
    number=39,
    demand=Demand.VARIATION,
    stem=r"<p>명제 '정수 \(n\)에 대해 \(3n\)이 짝수이면 \(n\)은 짝수이다'를 증명하려는 계획입니다. 계획대로 해내더라도 이 명제를 증명한 것이 <strong>아닌</strong> 것을 고르세요.</p>",
    options=(
        Option("q → p", r"\(n\)이 짝수라고 가정하고, \(3n\)이 짝수임을 이끌어 낸다."),
        Option("¬q → ¬p", r"\(n\)이 홀수라고 가정하고, \(3n\)이 홀수임을 이끌어 낸다.", r"결론의 부정(\(n\)이 홀수)에서 조건의 부정(\(3n\)이 홀수)을 이끌어 내는 대우증명법입니다. 대우는 원래 명제와 동치이므로 증명이 됩니다."),
        Option("¬(p ∧ ¬q)", r"\(3n\)이 짝수이고 \(n\)이 홀수라고 가정해, 모순을 이끌어 낸다.", r"조건은 참이고 결론은 거짓인 경우가 일어날 수 없음을 보이는 모순증명법입니다. ¬(p ∧ ¬q)는 p → q와 동치이므로 증명이 됩니다."),
        Option("p → q", r"\(3n\)이 짝수라고 가정하고, \(n\)이 짝수임을 이끌어 낸다.", "조건에서 결론을 이끌어 내는 직접증명법입니다. 이 명제에서는 대우증명법보다 번거로울 수 있지만, 해내기만 하면 증명이 됩니다."),
        Option("¬p ∨ q", r"모든 정수 \(n\)에 대해 '\(3n\)이 홀수이거나 \(n\)이 짝수이다'가 참임을 보인다.", "¬p ∨ q는 함축명제의 정의에 따라 p → q와 동치입니다. 따라서 이것을 보이면 증명이 됩니다."),
    ),
    answer=1,
    judge=lambda shows: not equivalent(shows, ITEM_39_TARGET),
    solution=r"""
<p>p: \(3n\)이 짝수, q: \(n\)이 짝수로 놓으면 증명할 명제는 p → q입니다. 각 계획을 해냈을 때 참임이 보장되는 명제가 p → q와 동치인지 따져 봅니다. ②는 ¬q → ¬p(대우), ③은 ¬(p ∧ ¬q), ④는 p → q, ⑤는 ¬p ∨ q로, 모두 p → q와 동치입니다.</p>
<p>①은 q를 가정해 p를 이끌어 내므로 q → p, 곧 역을 증명하는 계획입니다. 역은 원래 명제와 동치가 아닙니다. 이 명제는 역('\(n\)이 짝수이면 \(3n\)도 짝수이다')도 참이지만, 역을 증명했다고 원래 명제가 증명되지는 않습니다.</p>
""",
    layout=Layout.LONG,
)


# ---- 문제 40: 방법을 골라 판정하기 ----

def _cube_at_least_itself(n: int) -> bool:
    return n ** 3 >= n


def _square_plus_n_even(n: int) -> bool:
    return is_even(n * n + n)


def _square_plus_one_not_multiple_of_three(n: int) -> bool:
    return not is_multiple(n * n + 1, 3)


def _odd_square_minus_one_multiple_of_sixteen(n: int) -> bool:
    return not is_odd(n) or is_multiple(n * n - 1, 16)


ITEM_40: Item[Callable[[], bool]] = Item(
    number=40,
    demand=Demand.CHALLENGE,
    stem="<p>다음 가운데 참인 명제를 고르세요.</p>",
    options=(
        Option(lambda: holds_on_sample(_cube_at_least_itself), r"모든 정수 \(n\)에 대해 \(n^3 \ge n\)이다.", r"0 이상의 정수에서만 확인했습니다. \(n = -2\)이면 \(n^3 = -8\)이고 \(-8 &lt; -2\)이므로 반례입니다. 논의영역이 정수이면 음수도 따져야 합니다."),
        Option(lambda: holds_on_residues(_square_plus_n_even, 2), r"모든 정수 \(n\)에 대해 \(n^2 + n\)은 짝수이다."),
        Option(lambda: not holds_on_residues(_square_plus_one_not_multiple_of_three, 3), r"어떤 정수 \(n\)에 대해 \(n^2 + 1\)은 3의 배수이다.", r"예를 찾지 못했다고 끝나는 것이 아니라, 정말로 예가 없습니다. \(n\)을 3으로 나눈 나머지로 경우를 나누면 \(n^2 + 1\)을 3으로 나눈 나머지는 늘 1 또는 2입니다(위 풀이 참고)."),
        Option(lambda: all(math.factorial(n) > n for n in NATURALS), r"모든 자연수 \(n\)에 대해 \(n! &gt; n\)이다.", r"\(n = 1\)이면 \(1! = 1\)이라 \(1 &gt; 1\)은 거짓입니다(\(n = 2\)도 \(2! = 2\)라 반례입니다). \(n \ge 3\)에서는 성립하지만, '모든'이 붙은 명제는 반례 하나로 거짓입니다."),
        Option(lambda: holds_on_sample(_odd_square_minus_one_multiple_of_sixteen), r"모든 홀수 \(n\)에 대해 \(n^2 - 1\)은 16의 배수이다.", r"\(n = 1\)이면 0이라 16의 배수이지만, \(n = 3\)이면 \(n^2 - 1 = 8\)이라 16의 배수가 아닙니다. 홀수의 제곱에서 1을 뺀 수는 8의 배수이지만 16의 배수라고까지 할 수는 없습니다."),
    ),
    answer=2,
    judge=lambda claim: claim(),
    solution=r"""
<p>'모든'이 붙은 명제는 반례 하나로 거짓이 되고, 참임을 보이려면 모든 경우를 다뤄야 합니다. '어떤'이 붙은 명제는 예 하나로 참이 되고, 거짓임을 보이려면 모든 경우를 다뤄야 합니다. 이에 따라 다섯 명제를 판정합니다.</p>
<p>②는 \(n\)이 짝수인 경우와 홀수인 경우로 나누면 모든 정수를 다룰 수 있습니다. \(n = 2k\)이면 \(n^2 + n = 4k^2 + 2k = 2(2k^2 + k)\), \(n = 2k + 1\)이면 \(n^2 + n = 4k^2 + 6k + 2 = 2(2k^2 + 3k + 1)\)입니다. 정수는 덧셈과 곱셈에 닫혀 있어 괄호 안이 정수이므로, 어느 경우든 \(n^2 + n\)은 짝수입니다. 따라서 ②는 참입니다.</p>
<p>③은 \(n\)을 3으로 나눈 나머지로 경우를 나눕니다. \(n = 3k\)이면 \(n^2 + 1 = 3(3k^2) + 1\), \(n = 3k + 1\)이면 \(n^2 + 1 = 3(3k^2 + 2k) + 2\), \(n = 3k + 2\)이면 \(n^2 + 1 = 3(3k^2 + 4k + 1) + 2\)입니다. 어느 경우에도 3으로 나눈 나머지가 0이 아니므로 예가 없고, ③은 거짓입니다.</p>
<p>①은 \(n = -2\), ④는 \(n = 1\), ⑤는 \(n = 3\)이 반례이므로 거짓입니다.</p>
""",
    layout=Layout.LONG,
)

SECTION_F: Section = Section(
    title="6. 섞어 풀기",
    summary="",
    worked=None,
    items=(ITEM_36, ITEM_37, ITEM_38, ITEM_39, ITEM_40),
    note="1부터 5까지의 유형이 섞여 있습니다. 어떤 증명법이나 판정 방법을 쓸지부터 스스로 정해야 합니다. 앞 문제를 다 푼 뒤 며칠 지나서, 해설과 핵심 정리를 보지 않고 풀어 보세요.",
    checks=(
        ("문제 36 해설: n = 1, 2, 3이면 2, 5, 10이고 3이 처음 예", lambda: [n * n + 1 for n in (1, 2, 3)] == [2, 5, 10] and _first_natural_example() == 3),
        ("문제 37: 길이 1인 삼진 나열은 3개, 3 × 3ᵏ = 3ᵏ⁺¹", lambda: _ternary_strings(1) == 3 and same_polynomial("3*3**k", "3**(k + 1)")),
        ("문제 37 오답: 길이 2인 나열은 9개, 3(1 + 1) = 6", lambda: _ternary_strings(2) == 9 and evaluate("3*(k + 1)", k=1) == 6),
        ("문제 38: 원래 명제가 모든 정수에서 참(4로 나눈 나머지)", lambda: holds_on_residues(lambda n: not CLAUSE_TRUTH["p"](n) or CLAUSE_TRUTH["q"](n), 4)),
        ("문제 38 해설: n = 2는 역과 이의 반례, n = 1은 ④와 ⑤의 반례", lambda: _fails_at(2, "q", "p") and _fails_at(2, "¬p", "¬q") and _fails_at(1, "¬p", "q") and _fails_at(1, "¬q", "p")),
        ("문제 39 해설: 원래 명제와 역이 모두 모든 정수에서 참(짝홀)", lambda: holds_on_residues(lambda n: not is_even(3 * n) or is_even(n), 2) and holds_on_residues(lambda n: not is_even(n) or is_even(3 * n), 2)),
        ("문제 40 해설: 짝홀로 나눈 두 계산", lambda: same_polynomial("(2*k)**2 + 2*k", "2*(2*k**2 + k)") and same_polynomial("(2*k + 1)**2 + (2*k + 1)", "2*(2*k**2 + 3*k + 1)")),
        ("문제 40 해설: 3으로 나눈 나머지별 세 계산", lambda: same_polynomial("(3*k)**2 + 1", "3*(3*k**2) + 1") and same_polynomial("(3*k + 1)**2 + 1", "3*(3*k**2 + 2*k) + 2") and same_polynomial("(3*k + 2)**2 + 1", "3*(3*k**2 + 4*k + 1) + 2")),
        ("문제 40 오답: 반례 n = -2, 1, 2, 3과 n ≥ 3에서 n! > n, n = 1이면 0", lambda: not _cube_at_least_itself(-2) and math.factorial(1) == 1 and math.factorial(2) == 2 and all(math.factorial(n) > n for n in range(3, 61)) and not _odd_square_minus_one_multiple_of_sixteen(3) and _odd_square_minus_one_multiple_of_sixteen(1)),
        ("문제 40 오답: 홀수의 제곱에서 1을 뺀 수는 8의 배수(표본)", lambda: all(is_multiple(n * n - 1, 8) for n in SAMPLE if is_odd(n))),
        ("문제 40 오답: 0 이상의 정수에서는 n³ ≥ n(표본)", lambda: all(_cube_at_least_itself(n) for n in range(0, 61))),
    ),
)
