"""묶음 4 반례증명법과 존재증명법: 핵심 정리, 보기 4, 문제 21~26."""

from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction

from model import Demand, Item, Layout, Option, Section, WorkedExample
from number_tools import NATURALS, SAMPLE, is_integer, is_natural, is_odd, is_prime
from proof_methods import EXAMPLE_METHOD_SHOWS, EXAMPLES_PROVE_FOR_ALL, ONE_COUNTEREXAMPLE_REFUTES_FOR_ALL

SUMMARY: str = r"""
<ul>
  <li><strong>반례증명법</strong>: \(\forall x\,P(x)\)가 거짓임을, \(P(x)\)를 거짓으로 만드는 \(x\) 하나(반례)로 보입니다. \(\neg\forall x\,P(x) \equiv \exists x\,\neg P(x)\)이기 때문입니다.</li>
  <li><strong>존재증명법</strong>: \(\exists x\,P(x)\)가 참임을, \(P(x)\)를 참으로 만드는 \(x\) 하나로 보입니다.</li>
  <li><strong>예 하나로 끝나지 않는 것</strong>: 성립하는 예를 아무리 많이 들어도 \(\forall x\,P(x)\)가 참이라는 증명은 되지 않습니다. \(\exists x\,P(x)\)가 거짓임을 보일 때도 \(\neg\exists x\,P(x) \equiv \forall x\,\neg P(x)\)이므로 모든 \(x\)를 다뤄야 합니다.</li>
  <li><strong>논의영역</strong>: 반례와 예는 반드시 논의영역 안에서 찾습니다. 자연수는 1, 2, 3, …입니다. 소수는 1보다 큰 자연수 가운데 1과 자기 자신으로만 나누어떨어지는 수이고, 1은 소수가 아닙니다.</li>
</ul>
"""


def _square_plus_n_plus_one(n: int) -> int:
    return n * n + n + 1


def _worked_check() -> bool:
    values: list[int] = [_square_plus_n_plus_one(n) for n in range(1, 5)]
    return values == [3, 7, 13, 21] and [is_prime(v) for v in values] == [True, True, True, False] and 21 == 3 * 7


WORKED: WorkedExample = WorkedExample(
    title="보기 4 반례와 예로 판정하기",
    body=r"""
<p>다음 두 명제의 참, 거짓을 판정하세요.</p>
<ul>
  <li>(가) 모든 자연수 \(n\)에 대해 \(n^2 + n + 1\)은 소수이다.</li>
  <li>(나) 어떤 자연수 \(n\)에 대해 \(n^2 + n + 1\)은 소수이다.</li>
</ul>
<p class="solution-label">풀이</p>
<p>작은 값부터 넣어 봅니다. \(n = 1, 2, 3\)이면 \(n^2 + n + 1\)은 3, 7, 13으로 모두 소수입니다. 그러나 이것만으로 (가)가 참이라고 할 수는 없습니다. \(n = 4\)이면 \(16 + 4 + 1 = 21 = 3 \times 7\)이라 소수가 아닙니다. 반례 \(n = 4\)가 있으므로 (가)는 거짓입니다(반례증명법).</p>
<p>(나)는 \(n = 1\)이면 \(1 + 1 + 1 = 3\)이 소수이므로, 예 하나로 참입니다(존재증명법).</p>
<p>같은 식에 붙은 한정자만 다른데 진릿값이 다릅니다. 처음 세 값에서 성립했다는 사실이 (나)의 증명은 되지만 (가)의 증명은 되지 않는다는 점에 주의하세요.</p>
""",
    check=_worked_check,
)


def _value_option(x: Fraction, text: str, why_wrong: str = "") -> Option[Fraction]:
    return Option(x, text, why_wrong)


ITEM_21: Item[Fraction] = Item(
    number=21,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '모든 정수 \(n\)에 대해 \(n^2 &gt; n\)이다'가 거짓임을 보이는 반례를 고르세요.</p>",
    options=(
        _value_option(Fraction(-3), r"\(n = -3\)", r"\((-3)^2 = 9 &gt; -3\)이므로 성립합니다. 제곱을 2배로 계산해 \(-6 &gt; -3\)이 거짓이라고 보면 반례로 착각합니다."),
        _value_option(Fraction(-1), r"\(n = -1\)", r"\((-1)^2 = 1 &gt; -1\)이므로 성립합니다. \((-1)^2\)을 \(-1\)로 계산하면 \(-1 &gt; -1\)이 거짓이 되어 반례로 보입니다. 음수를 제곱하면 양수입니다."),
        _value_option(Fraction(0), r"\(n = 0\)"),
        _value_option(Fraction(1, 2), r"\(n = \tfrac{1}{2}\)", r"\(\left(\tfrac{1}{2}\right)^2 = \tfrac{1}{4} &lt; \tfrac{1}{2}\)이라 부등식이 성립하지 않지만, \(\tfrac{1}{2}\)은 정수가 아닙니다. 반례는 논의영역 안에서 찾아야 합니다."),
        _value_option(Fraction(2), r"\(n = 2\)", r"\(2^2 = 4 &gt; 2\)이므로 성립합니다. 성립하는 값은 예일 뿐이고, 반례는 명제를 거짓으로 만드는 값입니다."),
    ),
    answer=3,
    judge=lambda n: is_integer(n) and not n * n > n,
    solution=r"""
<p>반례는 정수 가운데 \(n^2 &gt; n\)을 거짓으로 만드는 값입니다. \(n = 0\)이면 \(0^2 = 0\)이고 \(0 &gt; 0\)은 거짓이므로 0이 반례입니다. 반례가 하나 있으므로 이 명제는 거짓입니다.</p>
<p>\(n^2 - n = n(n - 1)\)이 0이 되는 \(n = 0\)과 \(n = 1\)이 반례이고, 다른 정수에서는 성립합니다. 반례는 하나만 보이면 되고, 같은 경우(\(0 = 0\))는 \(&gt;\)를 만족하지 않는다는 점이 열쇠입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_22: Item[int] = Item(
    number=22,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '어떤 자연수 \(n\)에 대해 \(2^n &lt; n^2\)이다'가 참임을 보이는 예를 고르세요.</p>",
    options=(
        Option(-1, r"\(n = -1\)", r"\(2^{-1} = \tfrac{1}{2} &lt; 1 = (-1)^2\)으로 부등식은 성립하지만, \(-1\)은 자연수가 아닙니다. 예는 논의영역 안에서 찾아야 합니다."),
        Option(1, r"\(n = 1\)", r"\(2^1 = 2\), \(1^2 = 1\)이므로 \(2 &lt; 1\)은 거짓입니다. 부등호의 방향을 거꾸로 읽으면 성립하는 것처럼 보입니다."),
        Option(2, r"\(n = 2\)", r"\(2^2 = 4\), \(2^2 = 4\)로 양쪽이 같습니다. \(&lt;\)는 같은 경우를 포함하지 않으므로 성립하지 않습니다."),
        Option(3, r"\(n = 3\)"),
        Option(5, r"\(n = 5\)", r"\(2^5 = 32\), \(5^2 = 25\)이므로 \(32 &lt; 25\)는 거짓입니다. \(2^5\)를 \(2 \times 5 = 10\)으로 계산하면 성립하는 것처럼 보입니다."),
    ),
    answer=4,
    judge=lambda n: n >= 1 and 2 ** n < n * n,
    solution=r"""
<p>\(n = 3\)이면 \(2^3 = 8\), \(3^2 = 9\)이고 \(8 &lt; 9\)입니다. 조건을 만족하는 자연수가 하나 있으므로, 존재증명법에 따라 이 명제는 참입니다.</p>
<p>자연수 가운데 이 부등식을 만족하는 것은 사실 3 하나뿐입니다(\(n \ge 5\)이면 \(2^n &gt; n^2\)임은 문제 35에서 증명합니다). 그래도 존재증명법에서는 예 하나만 보이면 충분합니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_23: Item[int] = Item(
    number=23,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '모든 자연수 \(n\)에 대해, \(n\)이 소수이면 \(n\)은 홀수이다'가 거짓임을 보이는 반례를 고르세요.</p>",
    options=(
        Option(1, r"\(n = 1\)", r"1은 소수가 아니므로 조건이 거짓이고, 함축은 조건이 거짓이면 참입니다. \(n = 1\)에서 이 명제는 성립합니다."),
        Option(2, r"\(n = 2\)"),
        Option(3, r"\(n = 3\)", "3은 소수이고 홀수이므로 성립하는 예입니다."),
        Option(4, r"\(n = 4\)", "4는 홀수가 아니지만 소수도 아닙니다. 조건이 거짓이므로 함축은 참입니다. 결론만 보고 고르면 틀립니다."),
        Option(9, r"\(n = 9\)", "9는 홀수이지만 소수가 아닙니다. 이것은 역 '홀수이면 소수이다'의 반례이고, 원래 명제에서는 조건이 거짓이라 성립합니다."),
    ),
    answer=2,
    judge=lambda n: n >= 1 and is_prime(n) and not is_odd(n),
    solution=r"""
<p>\(P(n)\): '\(n\)은 소수이다', \(Q(n)\): '\(n\)은 홀수이다'로 놓으면 명제는 \(\forall n\,(P(n) \rightarrow Q(n))\)입니다. 반례는 \(P(n) \rightarrow Q(n)\)을 거짓으로 만드는 \(n\)이고, 함축이 거짓인 것은 조건이 참이고 결론이 거짓일 때뿐입니다. 그래서 '소수이면서 홀수가 아닌' 자연수를 찾습니다.</p>
<p>2는 소수이고 짝수이므로 반례입니다. 이때 실제로 보인 것은 \(\exists n\,(P(n) \land \neg Q(n))\)입니다.</p>
""",
    layout=Layout.SHORT,
)


def _euler(n: int) -> int:
    return n * n + n + 41


ITEM_24: Item[Callable[[], bool]] = Item(
    number=24,
    demand=Demand.FOUNDATION,
    stem=r"<p>한 학생이 \(n = 1, 2, 3, \ldots, 10\)을 넣어 보니 \(n^2 + n + 41\)이 모두 소수였으므로, '모든 자연수 \(n\)에 대해 \(n^2 + n + 41\)은 소수이다'가 증명되었다고 주장했습니다. 이 주장에 대한 평가로 옳은 것을 고르세요.</p>",
    options=(
        Option(lambda: not EXAMPLES_PROVE_FOR_ALL and not is_prime(_euler(40)) and _euler(40) == 41 ** 2, r"증명이 아니다. 확인하지 않은 \(n\)에서 반례가 나올 수 있고, 실제로 \(n = 40\)이면 \(n^2 + n + 41 = 41^2\)이라 소수가 아니다."),
        Option(lambda: EXAMPLES_PROVE_FOR_ALL, "열 개나 확인했으므로 바른 증명이다.", r"확인하지 않은 자연수 가운데 반례가 있을 수 있으므로, 예를 몇 개 들어도 '모든'이 붙은 명제의 증명은 되지 않습니다."),
        Option(lambda: not EXAMPLES_PROVE_FOR_ALL and _euler(11) % 11 == 0 and not is_prime(_euler(11)), r"증명이 아니다. 확인하지 않은 \(n\)에서 반례가 나올 수 있고, 실제로 \(n = 11\)이면 \(n^2 + n + 41\)이 11의 배수라 소수가 아니다.", r"\(n^2 + n = 121 + 11 = 132\)는 11의 배수이지만, 41을 더한 173은 11의 배수가 아니고 소수입니다. 어떤 값을 반례라고 하려면 그 값에서 명제가 실제로 거짓인지 끝까지 계산해야 합니다."),
        Option(lambda: EXAMPLE_METHOD_SHOWS["존재증명법"] == "∀x P(x)가 참", "예를 들어 보이는 것은 존재증명법이므로, 이 주장은 바른 증명이다.", r"존재증명법은 '어떤'이 붙은 명제가 참임을 보이는 방법입니다. 예로 \(\exists n\)은 보일 수 있어도 \(\forall n\)은 보일 수 없습니다."),
        Option(lambda: not ONE_COUNTEREXAMPLE_REFUTES_FOR_ALL, "증명은 아니지만, 반례가 하나쯤 있어도 이 명제는 여전히 참이라고 할 수 있다.", r"'모든'이 붙은 명제는 반례가 하나만 있어도 거짓입니다. \(\neg\forall n\,P(n) \equiv \exists n\,\neg P(n)\)이기 때문입니다."),
    ),
    answer=1,
    judge=lambda claim: claim(),
    solution=r"""
<p>'모든 자연수'에 대한 명제는 확인한 값이 아무리 많아도 확인하지 않은 값이 끝없이 남습니다. 실제로 \(n = 1\)부터 39까지는 모두 소수가 나오지만, \(n = 40\)이면 \(1600 + 40 + 41 = 1681 = 41^2\)이라 소수가 아닙니다.</p>
<p>반례 하나로 이 명제는 거짓입니다. 예를 많이 드는 것은 참일 것이라는 짐작의 근거는 될 수 있어도 증명은 아닙니다.</p>
""",
    layout=Layout.LONG,
)

# 문제 25: 각 방법이 n^2 ≠ 2를 확인하는 정수의 범위. 모든 정수를 덮어야 ∃가 거짓이라는 증명이 된다.
NumberRange = Callable[[int], bool]


def _covers_all_integers(covered: NumberRange) -> bool:
    return all(covered(n) for n in SAMPLE)


def _square_never_two_by_cases() -> bool:
    small: bool = all(n * n != 2 and n * n <= 1 for n in (-1, 0, 1))
    large: bool = all(n * n >= 4 for n in SAMPLE if abs(n) >= 2)
    return small and large


ITEM_25: Item[Callable[[], bool]] = Item(
    number=25,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '어떤 정수 \(n\)에 대해 \(n^2 = 2\)이다'가 거짓임을 보이는 방법으로 옳은 것을 고르세요.</p>",
    options=(
        Option(lambda: _covers_all_integers(lambda n: n == 1), r"\(n = 1\)을 넣으면 \(1^2 \ne 2\)이므로, 이것으로 거짓임을 보인 것이다.", r"\(n = 1\)에서 성립하지 않는다는 것은 \(\exists n\,(n^2 \ne 2)\)를 보인 것일 뿐입니다. 다른 정수에서 \(n^2 = 2\)가 될 수도 있으므로, '어떤'이 붙은 명제가 거짓이라는 증명은 되지 않습니다."),
        Option(lambda: math.isqrt(2) ** 2 == 2, r"\(n = \sqrt{2}\)이면 \(n^2 = 2\)이므로, 이 명제는 오히려 참이다.", r"\(\sqrt{2}\)는 정수가 아니므로 논의영역 밖의 값입니다. 예는 정수 가운데에서 찾아야 합니다."),
        Option(lambda: _covers_all_integers(lambda n: n in (1, 2, 3)), r"\(n = 1, 2, 3\)을 넣어 모두 \(n^2 \ne 2\)이므로, 이것으로 거짓임을 보인 것이다.", "정수는 끝없이 많으므로 세 개를 확인해도 나머지가 남습니다. 0이나 음수도 확인하지 않았습니다."),
        Option(lambda: _covers_all_integers(lambda n: n >= 1), r"모든 자연수 \(n\)에 대해 \(n^2 \ne 2\)임을 보인다. \(n = 1\)이면 1이고 \(n \ge 2\)이면 \(n^2 \ge 4\)이기 때문이다.", "자연수만 다루었습니다. 논의영역은 정수이므로 0과 음수도 다뤄야 합니다."),
        Option(lambda: _covers_all_integers(lambda n: abs(n) <= 1 or abs(n) >= 2) and _square_never_two_by_cases(), r"모든 정수 \(n\)에 대해 \(n^2 \ne 2\)임을 보인다. \(|n| \le 1\)이면 \(n^2 \le 1\)이고 \(|n| \ge 2\)이면 \(n^2 \ge 4\)이기 때문이다."),
    ),
    answer=5,
    judge=lambda claim: claim(),
    solution=r"""
<p>'어떤'이 붙은 명제가 거짓이라는 것은 그 부정 \(\neg\exists n\,(n^2 = 2) \equiv \forall n\,(n^2 \ne 2)\)가 참이라는 뜻입니다. 그래서 예 하나로는 안 되고, 모든 정수를 빠짐없이 다뤄야 합니다.</p>
<p>정수를 \(|n| \le 1\)인 것(\(-1\), 0, 1)과 \(|n| \ge 2\)인 것으로 나누면 모든 정수가 둘 가운데 한쪽에 들어갑니다. 앞의 것은 \(n^2\)이 1, 0, 1이고, 뒤의 것은 \(n^2 \ge 4\)이므로, 어느 쪽에서도 \(n^2 = 2\)가 되지 않습니다.</p>
""",
    layout=Layout.LONG,
)

DomainValue = tuple[str, Fraction]
DOMAIN_MEMBERSHIP: dict[str, Callable[[Fraction], bool]] = {
    "정수": is_integer,
    "자연수": is_natural,
    "실수": lambda x: True,
}


def _domain_option(domain: str, x: Fraction, text: str, why_wrong: str = "") -> Option[DomainValue]:
    return Option((domain, x), text, why_wrong)


def _refutes_square_at_least_itself(choice: DomainValue) -> bool:
    domain, x = choice
    return DOMAIN_MEMBERSHIP[domain](x) and not x * x >= x


ITEM_26: Item[DomainValue] = Item(
    number=26,
    demand=Demand.VARIATION,
    stem=r"<p>명제 '모든 \(x\)에 대해 \(x^2 \ge x\)이다'는 논의영역에 따라 참일 수도 거짓일 수도 있습니다. 논의영역과 반례를 바르게 짝지어 이 명제가 거짓임을 보인 것을 고르세요.</p>",
    options=(
        _domain_option("실수", Fraction(1, 2), r"논의영역이 실수 전체일 때, 반례 \(x = \tfrac{1}{2}\)"),
        _domain_option("정수", Fraction(0), r"논의영역이 정수 전체일 때, 반례 \(x = 0\)", r"\(0^2 = 0 \ge 0\)이므로 성립합니다. 같은 경우도 \(\ge\)를 만족합니다."),
        _domain_option("정수", Fraction(-1), r"논의영역이 정수 전체일 때, 반례 \(x = -1\)", r"\((-1)^2 = 1 \ge -1\)이므로 성립합니다. 음수는 제곱하면 양수가 되어 오히려 커집니다."),
        _domain_option("자연수", Fraction(1), r"논의영역이 자연수 전체일 때, 반례 \(x = 1\)", r"\(1^2 = 1 \ge 1\)이므로 성립합니다."),
        _domain_option("실수", Fraction(3, 2), r"논의영역이 실수 전체일 때, 반례 \(x = \tfrac{3}{2}\)", r"\(\left(\tfrac{3}{2}\right)^2 = \tfrac{9}{4} \ge \tfrac{3}{2}\)이므로 성립합니다. 분수를 제곱하면 작아진다고 생각하기 쉽지만, 그것은 0과 1 사이의 수일 때만입니다."),
    ),
    answer=1,
    judge=_refutes_square_at_least_itself,
    solution=r"""
<p>반례는 그 논의영역 안에서 \(x^2 &lt; x\)가 되는 값입니다. \(x^2 - x = x(x - 1)\)이 음수가 되는 것은 \(x\)와 \(x - 1\)의 부호가 다를 때, 곧 \(0 &lt; x &lt; 1\)일 때뿐입니다.</p>
<p>이 구간에는 정수가 없으므로 논의영역이 정수나 자연수이면 명제는 참이고, 반례를 찾을 수 없습니다. 논의영역이 실수이면 \(x = \tfrac{1}{2}\)처럼 이 구간의 수가 반례입니다. 실제로 \(\left(\tfrac{1}{2}\right)^2 = \tfrac{1}{4} &lt; \tfrac{1}{2}\)입니다.</p>
""",
    layout=Layout.MEDIUM,
)

GRID: list[Fraction] = [Fraction(n, 8) for n in range(-40, 41)]

SECTION_D: Section = Section(
    title="4. 반례증명법과 존재증명법",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_21, ITEM_22, ITEM_23, ITEM_24, ITEM_25, ITEM_26),
    checks=(
        ("문제 21 해설: 표본 정수 가운데 반례는 0과 1뿐", lambda: [n for n in SAMPLE if not n * n > n] == [0, 1]),
        ("문제 22 해설: 표본 자연수 가운데 2ⁿ < n²인 것은 3뿐", lambda: [n for n in NATURALS if 2 ** n < n * n] == [3]),
        ("문제 24 해설: n = 1~39는 모두 소수, 40에서 1681 = 41²", lambda: all(is_prime(_euler(n)) for n in range(1, 40)) and _euler(40) == 1681 == 41 ** 2),
        ("문제 24 오답: n = 11이면 173이고 소수", lambda: _euler(11) == 173 and is_prime(173)),
        ("문제 26 해설(보조, 유리수 격자): x² < x인 x는 0 < x < 1에만 있음", lambda: all((x * x < x) == (0 < x < 1) for x in GRID)),
    ),
)
