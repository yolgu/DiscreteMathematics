"""3절 변수를 포함한 명제와 한정자: 핵심 정리, 보기 3, 문제 23~29."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from fractions import Fraction

from logic_tools import Predicate, QuantifiedClaim, is_prime, rational_grid, same_in_every_interpretation
from model import Demand, Item, Layout, Option, Section, WorkedExample

SUMMARY: str = r"""
<ul>
  <li><strong>논의영역과 명제함수</strong>: 변수 \(x\)가 속하는 범위를 논의영역 \(D\)라고 합니다. 명제함수 \(P(x)\)는 \(x\)에 \(D\)의 값을 넣어야 비로소 명제가 됩니다.</li>
  <li><strong>전체한정자</strong> \(\forall x\,P(x)\): \(D\)의 모든 원소에 대해 \(P(x)\)가 참일 때만 참입니다. 거짓임을 보이려면 \(P(x)\)가 거짓인 \(x\) 하나, 곧 반례 하나면 됩니다.</li>
  <li><strong>존재한정자</strong> \(\exists x\,P(x)\): \(D\)의 원소 가운데 하나라도 \(P(x)\)를 참으로 만들면 참입니다.</li>
  <li><strong>한정자의 부정</strong>: \(\neg\forall x\,P(x) \equiv \exists x\,\neg P(x)\), \(\neg\exists x\,P(x) \equiv \forall x\,\neg P(x)\)입니다. 부정하면 ∀와 ∃가 맞바뀌고 ¬는 \(P(x)\) 쪽으로 들어갑니다.</li>
  <li><strong>한정자가 둘일 때</strong>: 왼쪽부터 읽습니다. \(\forall x\,\exists y\,P(x, y)\)는 \(x\)마다 \(y\)를 따로 골라도 되지만, \(\exists y\,\forall x\,P(x, y)\)는 먼저 고른 \(y\) 하나가 모든 \(x\)에 통해야 합니다.</li>
</ul>
"""

WORKED_DOMAIN: tuple[int, ...] = (1, 2, 3)


def _worked_check() -> bool:
    values: dict[int, bool] = {x: x * x <= 4 for x in WORKED_DOMAIN}
    for_all: bool = all(values.values())
    exists: bool = any(values.values())
    exists_counterexample: bool = any(not truth for truth in values.values())
    return values == {1: True, 2: True, 3: False} and not for_all and exists and exists_counterexample == (not for_all)


WORKED: WorkedExample = WorkedExample(
    title="보기 3 유한한 논의영역에서 한정자의 진릿값 구하기",
    body=r"""
<p>논의영역이 \(D = \{1, 2, 3\}\)이고 명제함수 \(P(x)\)가 \(x^2 \le 4\)일 때, \(\forall x\,P(x)\), \(\exists x\,P(x)\), \(\neg\forall x\,P(x)\)의 진릿값을 구하세요.</p>
<p class="solution-label">풀이</p>
<p>원소가 셋뿐이니 모두 넣어 봅니다. \(P(1)\)은 \(1 \le 4\)로 참, \(P(2)\)는 \(4 \le 4\)로 참, \(P(3)\)은 \(9 \le 4\)로 거짓입니다. \(P(2)\)에서 4와 4는 같으므로 '작거나 같다'를 만족한다는 점에 주의합니다.</p>
<p>\(\forall x\,P(x)\)는 모든 원소에서 참이어야 하는데 3이 반례이므로 거짓입니다. \(\exists x\,P(x)\)는 1 하나만으로도 참입니다. \(\neg\forall x\,P(x)\)는 \(\exists x\,\neg P(x)\), 곧 '\(x^2 &gt; 4\)인 \(x\)가 있다'와 같고, \(x = 3\)이 있으므로 참입니다. \(\forall x\,P(x)\)가 거짓이니 그 부정이 참이라는 것과도 맞습니다.</p>
""",
    check=_worked_check,
)

ITEM_23: Item[tuple[int, int]] = Item(
    number=23,
    demand=Demand.FOUNDATION,
    stem=r"<p>정수 \(x\), \(y\)에 대한 명제함수 \(P(x, y)\)가 \(x = 2y + 1\)일 때, 참인 명제를 고르세요.</p>",
    options=(
        Option((3, 7), r"\(P(3, 7)\)", r"\(x = 3\), \(y = 7\)이므로 \(2 \times 7 + 1 = 15\)이고 \(3 \ne 15\)입니다. 값을 넣는 순서를 바꾸면 참으로 보입니다. \(P(x, y)\)의 첫째 자리가 \(x\)입니다."),
        Option((4, 3), r"\(P(4, 3)\)", r"\(2 \times 3 + 1 = 7\)이므로 \(4 \ne 7\)입니다. \(2y\)를 \(y\)로 계산하면 \(3 + 1 = 4\)가 되어 참으로 보입니다."),
        Option((5, 3), r"\(P(5, 3)\)", r"\(2 \times 3 + 1 = 7\)이므로 \(5 \ne 7\)입니다. \(2y - 1\)로 잘못 계산하면 5가 나옵니다."),
        Option((6, 3), r"\(P(6, 3)\)", r"\(2 \times 3 + 1 = 7\)이므로 \(6 \ne 7\)입니다. \(+1\)을 빠뜨리면 6이 나옵니다."),
        Option((7, 3), r"\(P(7, 3)\)"),
    ),
    answer=5,
    judge=lambda pair: pair[0] == 2 * pair[1] + 1,
    solution=r"""
<p>명제함수에 값을 넣으면 명제가 됩니다. \(P(7, 3)\)은 \(x\)에 7, \(y\)에 3을 넣은 것이므로 \(7 = 2 \times 3 + 1\)이고, 양쪽이 모두 7이므로 참인 명제입니다.</p>
<p>값은 \(P(x, y)\)에 적힌 변수의 순서대로 넣습니다. 같은 명제함수라도 넣는 값에 따라 참인 명제가 되기도 하고 거짓인 명제가 되기도 합니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_24_DOMAIN: tuple[int, ...] = (-2, -1, 0, 1, 2)

ITEM_24: Item[Callable[[], bool]] = Item(
    number=24,
    demand=Demand.FOUNDATION,
    stem=r"<p>논의영역이 \(D = \{-2, -1, 0, 1, 2\}\)일 때, 참인 명제를 고르세요.</p>",
    options=(
        Option(lambda: all(x ** 2 >= 0 for x in ITEM_24_DOMAIN), r"\(\forall x\,(x^2 \ge 0)\)"),
        Option(lambda: all(x ** 2 > 0 for x in ITEM_24_DOMAIN), r"\(\forall x\,(x^2 &gt; 0)\)", r"\(x = 0\)이면 \(0^2 = 0\)이고 \(0 &gt; 0\)은 거짓입니다. 0이 반례이므로 거짓입니다."),
        Option(lambda: any(x ** 2 < 0 for x in ITEM_24_DOMAIN), r"\(\exists x\,(x^2 &lt; 0)\)", r"제곱은 음수가 될 수 없으므로 어느 원소도 만족하지 않아 거짓입니다. \((-2)^2\)을 \(-4\)로 계산하면 참으로 보이지만 \((-2)^2 = 4\)입니다."),
        Option(lambda: all(x ** 3 >= 0 for x in ITEM_24_DOMAIN), r"\(\forall x\,(x^3 \ge 0)\)", r"\(x = -1\)이면 \((-1)^3 = -1 &lt; 0\)입니다. 세제곱은 제곱과 달리 부호가 그대로 남으므로 거짓입니다."),
        Option(lambda: any(x + 3 == 0 for x in ITEM_24_DOMAIN), r"\(\exists x\,(x + 3 = 0)\)", r"\(x = -3\)이어야 하는데 \(-3\)은 \(D\)에 없습니다. 논의영역 밖의 값은 넣을 수 없으므로 거짓입니다."),
    ),
    answer=1,
    judge=lambda claim: claim(),
    solution=r"""
<p>원소가 다섯뿐이니 모두 넣어 봅니다. 제곱은 차례로 4, 1, 0, 1, 4이고 모두 0 이상입니다. 모든 원소에서 참이므로 \(\forall x\,(x^2 \ge 0)\)은 참입니다.</p>
<p>∀가 붙은 명제는 원소 하나라도 거짓이면 거짓이므로, 0이나 음수처럼 경계에 있는 값을 빠뜨리지 말고 확인해야 합니다. ∃가 붙은 명제는 반드시 논의영역 안에서 예를 찾아야 합니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_25_DOMAIN: tuple[int, ...] = (1, 2, 3, 4, 5)


def _prime(x: int) -> bool:
    return is_prime(x)


def _odd(x: int) -> bool:
    return x % 2 == 1


ITEM_25: Item[Callable[[], bool]] = Item(
    number=25,
    demand=Demand.VARIATION,
    stem=r"<p>논의영역이 \(D = \{1, 2, 3, 4, 5\}\)이고, \(P(x)\): '\(x\)는 소수이다', \(Q(x)\): '\(x\)는 홀수이다'입니다. 소수는 1보다 큰 자연수 가운데 1과 자기 자신으로만 나누어떨어지는 수입니다. 참인 명제를 고르세요.</p>",
    options=(
        Option(lambda: all(_prime(x) or _odd(x) for x in ITEM_25_DOMAIN), r"\(\forall x\,(P(x) \lor Q(x))\)", r"\(x = 4\)는 소수도 홀수도 아니므로 \(P(4) \lor Q(4)\)가 거짓입니다. 4가 반례입니다."),
        Option(lambda: all((not _prime(x)) or _odd(x) for x in ITEM_25_DOMAIN), r"\(\forall x\,(P(x) \rightarrow Q(x))\)", r"\(x = 2\)는 소수이지만 홀수가 아니므로 \(P(2) \rightarrow Q(2)\)가 T → F로 거짓입니다. '소수는 모두 홀수'라고 생각하면 참으로 보입니다."),
        Option(lambda: any(_prime(x) and not _odd(x) for x in ITEM_25_DOMAIN), r"\(\exists x\,(P(x) \land \neg Q(x))\)"),
        Option(lambda: all((not _odd(x)) or _prime(x) for x in ITEM_25_DOMAIN), r"\(\forall x\,(Q(x) \rightarrow P(x))\)", r"\(x = 1\)은 홀수이지만 소수가 아니므로 \(Q(1) \rightarrow P(1)\)이 거짓입니다. 1을 소수로 착각하면 참으로 보입니다."),
        Option(lambda: any(_prime(x) and x > 5 for x in ITEM_25_DOMAIN), r"\(\exists x\,(P(x) \land x &gt; 5)\)", r"\(D\)에는 5보다 큰 원소가 없습니다. 7은 5보다 큰 소수이지만 논의영역 밖이므로 넣을 수 없습니다."),
    ),
    answer=3,
    judge=lambda claim: claim(),
    solution=r"""
<p>먼저 원소마다 두 명제함수의 값을 정리합니다. 소수는 2, 3, 5이고 홀수는 1, 3, 5입니다.</p>
<p>\(\exists x\,(P(x) \land \neg Q(x))\)는 '소수이면서 홀수가 아닌 원소가 있다'는 뜻입니다. \(x = 2\)는 소수이고 짝수이므로 \(P(2) \land \neg Q(2)\)가 참입니다. 하나라도 있으면 참이므로 이 명제는 참입니다.</p>
<p>②와 ③은 서로 부정 관계입니다. \(\neg\forall x\,(P(x) \rightarrow Q(x)) \equiv \exists x\,\neg(P(x) \rightarrow Q(x)) \equiv \exists x\,(P(x) \land \neg Q(x))\)이므로, 2가 ②의 반례라는 것과 ③이 참이라는 것은 같은 사실입니다.</p>
""",
    layout=Layout.MEDIUM,
)


def _not_all_submitted(domain: Sequence[int], submitted: Predicate, _unused: Predicate) -> bool:
    return not all(submitted(x) for x in domain)


ITEM_26: Item[QuantifiedClaim] = Item(
    number=26,
    demand=Demand.FOUNDATION,
    stem="<p>학생이 한 명 이상 있는 반에서, 명제 '모든 학생이 과제를 제출했다'의 부정을 고르세요.</p>",
    options=(
        Option(lambda d, s, _q: all(not s(x) for x in d), "모든 학생이 과제를 제출하지 않았다.", "'모든'을 그대로 두고 '제출했다'만 부정한 \\(\\forall x\\,\\neg P(x)\\)입니다. 아무도 제출하지 않았다는 뜻으로, 원래 명제의 부정보다 훨씬 강한 말입니다. 한 명만 제출하지 않고 나머지는 제출한 반에서는 원래 명제와 이 문장이 모두 거짓이므로, 이 문장은 원래 명제의 부정이 아닙니다."),
        Option(lambda d, s, _q: any(not s(x) for x in d), "과제를 제출하지 않은 학생이 적어도 한 명 있다."),
        Option(lambda d, s, _q: any(s(x) for x in d), "과제를 제출한 학생이 적어도 한 명 있다.", "'모든'을 '어떤'으로 바꾸기만 하고 '제출했다'를 부정하지 않은 \\(\\exists x\\,P(x)\\)입니다. 모두 제출한 반에서는 원래 명제와 이 문장이 함께 참입니다."),
        Option(lambda d, s, _q: not any(not s(x) for x in d), "과제를 제출하지 않은 학생은 한 명도 없다.", "\\(\\neg\\exists x\\,\\neg P(x) \\equiv \\forall x\\,P(x)\\)이므로 원래 명제와 같은 말입니다. 부정을 두 번 한 셈입니다."),
        Option(lambda d, s, _q: any(s(x) for x in d) and any(not s(x) for x in d), "과제를 제출한 학생도 있고, 제출하지 않은 학생도 있다.", "아무도 제출하지 않은 반에서는 원래 명제의 부정이 참인데 이 문장은 거짓입니다. 부정에 필요한 것은 제출하지 않은 학생이 있다는 것뿐입니다."),
    ),
    answer=2,
    judge=lambda claim: same_in_every_interpretation(claim, _not_all_submitted),
    solution=r"""
<p>\(P(x)\): '\(x\)는 과제를 제출했다'로 놓으면 원래 명제는 \(\forall x\,P(x)\)입니다. 한정자의 부정에 따라 \(\neg\forall x\,P(x) \equiv \exists x\,\neg P(x)\), 곧 '과제를 제출하지 않은 학생이 적어도 한 명 있다'입니다.</p>
<p>'모두 제출했다'가 거짓이 되는 데는 제출하지 않은 학생 한 명이면 충분합니다. 부정하면 ∀는 ∃로 바뀌고, ¬는 '제출했다' 쪽으로 들어갑니다.</p>
""",
    layout=Layout.LONG,
)


def _stem_27(domain: Sequence[int], p: Predicate, q: Predicate) -> bool:
    return not any(p(x) and not q(x) for x in domain)


ITEM_27: Item[QuantifiedClaim] = Item(
    number=27,
    demand=Demand.VARIATION,
    stem=r"<p>\(\neg\exists x\,(P(x) \land \neg Q(x))\)와 동치인 것을 고르세요.</p>",
    options=(
        Option(lambda d, p, q: any((not p(x)) or q(x) for x in d), r"\(\exists x\,(\neg P(x) \lor Q(x))\)", "¬를 안으로 들이면서 ∃를 ∀로 바꾸지 않았습니다. 부정하면 한정자도 맞바뀝니다."),
        Option(lambda d, p, q: all((not p(x)) and q(x) for x in d), r"\(\forall x\,(\neg P(x) \land Q(x))\)", r"드모르간의 법칙에서 ∧를 ∨로 바꾸지 않았습니다. \(\neg(P(x) \land \neg Q(x))\)는 \(\neg P(x) \lor Q(x)\)입니다."),
        Option(lambda d, p, q: all(p(x) and not q(x) for x in d), r"\(\forall x\,(P(x) \land \neg Q(x))\)", "∃를 ∀로 바꾸기만 하고 안쪽을 부정하지 않았습니다. ¬는 한정자를 지나 안쪽 식에 들어가야 합니다."),
        Option(lambda d, p, q: all((not p(x)) or q(x) for x in d), r"\(\forall x\,(P(x) \rightarrow Q(x))\)"),
        Option(lambda d, p, q: all((not q(x)) or p(x) for x in d), r"\(\forall x\,(Q(x) \rightarrow P(x))\)", r"조건과 결론이 바뀐 역의 꼴입니다. 함축법칙으로 \(\neg P(x) \lor Q(x)\)를 되돌리면 \(P(x) \rightarrow Q(x)\)입니다."),
    ),
    answer=4,
    judge=lambda claim: same_in_every_interpretation(claim, _stem_27),
    solution=r"""
<p>바깥의 ¬를 안으로 들입니다. 한정자의 부정으로 ∃가 ∀로 바뀌고 ¬는 안쪽 식에 걸립니다. 그다음은 1, 2절의 동치 법칙입니다.</p>
<p>\[\neg\exists x\,(P(x) \land \neg Q(x)) \equiv \forall x\,\neg(P(x) \land \neg Q(x)) \equiv \forall x\,(\neg P(x) \lor Q(x)) \equiv \forall x\,(P(x) \rightarrow Q(x))\]</p>
<p>둘째 동치는 드모르간의 법칙과 이중 부정법칙, 셋째 동치는 함축법칙입니다. 뜻으로 읽으면 'P이면서 Q가 아닌 \(x\)는 없다'는 'P인 \(x\)는 모두 Q이다'와 같은 말입니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_28_DOMAIN: tuple[int, ...] = (1, 2, 3)


def _sums_to(total: int, x: int, y: int) -> bool:
    return x + y == total


ITEM_28: Item[Callable[[], bool]] = Item(
    number=28,
    demand=Demand.FOUNDATION,
    stem=r"<p>\(x\), \(y\)의 논의영역이 모두 \(D = \{1, 2, 3\}\)이고 \(P(x, y)\)가 \(x + y = 4\)일 때, 참인 명제를 고르세요.</p>",
    options=(
        Option(lambda: any(all(_sums_to(4, x, y) for x in ITEM_28_DOMAIN) for y in ITEM_28_DOMAIN), r"\(\exists y\,\forall x\,P(x, y)\)", r"\(y\) 하나를 먼저 골라 모든 \(x\)에 통해야 합니다. \(y = 1\)이면 \(x = 3\)에서만, \(y = 2\)이면 \(x = 2\)에서만, \(y = 3\)이면 \(x = 1\)에서만 성립하므로 거짓입니다. 한정자의 순서를 바꿔 읽으면 참으로 보입니다."),
        Option(lambda: all(all(_sums_to(4, x, y) for y in ITEM_28_DOMAIN) for x in ITEM_28_DOMAIN), r"\(\forall x\,\forall y\,P(x, y)\)", r"모든 짝에서 성립해야 하는데 \(x = 1\), \(y = 1\)이면 \(1 + 1 = 2 \ne 4\)이므로 거짓입니다."),
        Option(lambda: all(any(_sums_to(4, x, y) for y in ITEM_28_DOMAIN) for x in ITEM_28_DOMAIN), r"\(\forall x\,\exists y\,P(x, y)\)"),
        Option(lambda: all(any(_sums_to(5, x, y) for y in ITEM_28_DOMAIN) for x in ITEM_28_DOMAIN), r"\(\forall x\,\exists y\,(x + y = 5)\)", r"\(x = 1\)이면 \(y = 4\)여야 하는데 4는 \(D\)에 없으므로 거짓입니다."),
        Option(lambda: all(any(_sums_to(4, x, y) and x != y for y in ITEM_28_DOMAIN) for x in ITEM_28_DOMAIN), r"\(\forall x\,\exists y\,(x + y = 4 \land x \ne y)\)", r"\(x = 2\)이면 \(x + y = 4\)를 만족하는 \(y\)는 2뿐인데, \(x \ne y\)를 만족하지 않으므로 거짓입니다."),
    ),
    answer=3,
    judge=lambda claim: claim(),
    solution=r"""
<p>\(\forall x\,\exists y\,P(x, y)\)는 \(x\)가 먼저 주어지고, 그 \(x\)를 보고 \(y\)를 고르는 명제입니다. \(x = 1\)이면 \(y = 3\), \(x = 2\)이면 \(y = 2\), \(x = 3\)이면 \(y = 1\)을 고르면 됩니다. 모든 \(x\)에 대해 알맞은 \(y\)가 있으므로 참입니다.</p>
<p>①은 같은 \(P(x, y)\)에 한정자의 종류와 순서만 바꾼 것인데 거짓입니다. 종류가 다른 한정자는 순서를 바꾸면 뜻이 달라집니다.</p>
""",
    layout=Layout.MEDIUM,
)

# 실수 문항의 보조 확인. 참과 거짓의 근거는 해설의 추론(y = -x를 고름, x = 1 - y가 반례)이고, 격자는 그 추론을 다시 확인한다.
ITEM_29_GRID: list[Fraction] = rational_grid(-5, 5, 4)
_FORALL_EXISTS: bool = all(any(x + y == 0 for y in ITEM_29_GRID) for x in ITEM_29_GRID)
_EXISTS_FORALL: bool = any(all(x + y == 0 for x in ITEM_29_GRID) for y in ITEM_29_GRID)
_NEGATIVE_WORKS: bool = all(x + (-x) == 0 for x in ITEM_29_GRID)
_ONE_MINUS_Y_REFUTES: bool = all((1 - y) + y != 0 for y in ITEM_29_GRID)

ITEM_29: Item[Callable[[], bool]] = Item(
    number=29,
    demand=Demand.VARIATION,
    stem=r"<p>실수 \(x\), \(y\)에 대한 명제함수 \(P(x, y)\)가 \(x + y = 0\)일 때, 옳은 설명을 고르세요.</p>",
    options=(
        Option(lambda: _FORALL_EXISTS and _NEGATIVE_WORKS, r"\(\forall x\,\exists y\,P(x, y)\)는 참이다. \(x\)가 무엇이든 \(y = -x\)로 고르면 되기 때문이다."),
        Option(lambda: not _FORALL_EXISTS, r"\(\forall x\,\exists y\,P(x, y)\)는 거짓이다. \(x = 0\)이면 \(x + y = 0\)을 만족하는 \(y\)가 없기 때문이다.", r"\(x = 0\)이면 \(y = 0\)으로 고르면 \(0 + 0 = 0\)입니다. \(y = -x\)는 \(x = 0\)일 때도 통합니다."),
        Option(lambda: _EXISTS_FORALL, r"\(\exists y\,\forall x\,P(x, y)\)는 참이다. \(y = 0\)으로 고르면 \(x = 0\)일 때 \(x + y = 0\)이기 때문이다.", r"\(\forall x\)이므로 모든 \(x\)에 대해 성립해야 합니다. \(y = 0\)이면 \(x = 1\)에서 \(1 + 0 \ne 0\)입니다. \(x\) 하나에서 성립하는 것은 \(\exists y\,\exists x\,P(x, y)\)를 확인한 것입니다."),
        Option(lambda: _EXISTS_FORALL, r"\(\exists y\,\forall x\,P(x, y)\)는 참이다. 모든 \(x\)에 대해 \(y = -x\)로 고를 수 있기 때문이다.", r"\(y = -x\)는 \(x\)에 따라 바뀌는 값입니다. \(\exists y\,\forall x\)에서는 \(y\)를 \(x\)보다 먼저 하나로 정해야 하므로 \(x\)를 보고 \(y\)를 고를 수 없습니다."),
        Option(lambda: _FORALL_EXISTS == _EXISTS_FORALL, r"\(\forall x\,\exists y\,P(x, y)\)와 \(\exists y\,\forall x\,P(x, y)\)는 진릿값이 같다. 한정자의 순서는 진릿값에 영향을 주지 않기 때문이다.", "종류가 다른 한정자는 순서를 바꾸면 뜻이 달라집니다. 여기서 앞의 것은 참, 뒤의 것은 거짓입니다."),
    ),
    answer=1,
    judge=lambda claim: claim(),
    solution=r"""
<p>\(\forall x\,\exists y\,P(x, y)\)는 \(x\)마다 \(y\)를 따로 골라도 됩니다. 어떤 실수 \(x\)가 주어지든 \(y = -x\)도 실수이고 \(x + (-x) = 0\)이므로 참입니다.</p>
<p>반면 \(\exists y\,\forall x\,P(x, y)\)는 \(y\) 하나를 먼저 정해 두고 모든 \(x\)에 통해야 합니다. 어떤 \(y\)를 골라도 \(x = 1 - y\)이면 \(x + y = 1 \ne 0\)이므로 막힙니다. 따라서 거짓입니다. 두 명제는 한정자의 순서만 다른데 진릿값이 다릅니다.</p>
""",
    layout=Layout.LONG,
)

SECTION_C: Section = Section(
    title="3. 변수를 포함한 명제와 한정자",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_23, ITEM_24, ITEM_25, ITEM_26, ITEM_27, ITEM_28, ITEM_29),
    checks=(
        ("문제 25 해설: 소수와 홀수 목록", lambda: [x for x in ITEM_25_DOMAIN if _prime(x)] == [2, 3, 5] and [x for x in ITEM_25_DOMAIN if _odd(x)] == [1, 3, 5]),
        ("문제 25 해설: ②와 ③은 서로 부정", lambda: same_in_every_interpretation(
            lambda d, p, q: not all((not p(x)) or q(x) for x in d),
            lambda d, p, q: any(p(x) and not q(x) for x in d),
        )),
        ("문제 29 해설: y = -x가 통하고, x = 1 - y가 반례", lambda: _NEGATIVE_WORKS and _ONE_MINUS_Y_REFUTES and _FORALL_EXISTS and not _EXISTS_FORALL),
    ),
)
