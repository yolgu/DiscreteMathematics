"""1절 명제와 논리 연산자: 핵심 정리, 보기 1, 문제 1~12."""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction

from logic_tools import count_true_rows, entails, equivalent, is_prime, is_tautology, parse, rational_grid, value
from model import Demand, Item, Layout, Option, Section, WorkedExample, formula_option

T: bool = True
F: bool = False

SUMMARY: str = """
<ul>
  <li><strong>명제</strong>: 참인지 거짓인지를 구분할 수 있는 문장이나 수식입니다. 거짓인 문장도 명제입니다. 변수의 값에 따라 참과 거짓이 바뀌는 문장은 그 값이 정해지기 전까지 명제가 아닙니다.</li>
  <li><strong>논리 연산자</strong>: ¬p는 p와 반대 값입니다. p ∧ q는 둘 다 참일 때만 참, p ∨ q는 둘 다 거짓일 때만 거짓입니다(둘 다 참이어도 참). p ⊕ q는 두 값이 다를 때만 참입니다.</li>
  <li><strong>진리표</strong>: p, q의 경우를 TT, TF, FT, FF 순서로 적습니다. 명제가 \\(n\\)개이면 \\(2^n\\)줄입니다.</li>
  <li><strong>우선순위</strong>: ¬를 가장 먼저, ∧와 ∨를 다음에, →와 ↔를 가장 나중에 계산합니다. 괄호 안이 언제나 먼저입니다. ¬p ∧ q는 (¬p) ∧ q입니다.</li>
  <li><strong>항진명제, 모순명제, 사건명제</strong>: 구성명제의 값과 상관없이 늘 참이면 항진명제, 늘 거짓이면 모순명제, 둘 다 아니면 사건명제입니다.</li>
  <li><strong>함축</strong> p → q: p가 참이고 q가 거짓일 때만 거짓입니다. p가 거짓이면 q와 상관없이 참입니다.</li>
  <li><strong>충분조건과 필요조건</strong>: p ⇒ q이면 p는 q의 충분조건, q는 p의 필요조건입니다. 진리집합으로는 P ⊂ Q이고, 작은 집합 쪽이 충분조건입니다.</li>
  <li><strong>쌍방조건명제</strong> p ↔ q: p와 q의 값이 같을 때만 참입니다.</li>
  <li><strong>역, 이, 대우</strong>: p → q의 역은 q → p, 이는 ¬p → ¬q, 대우는 ¬q → ¬p입니다. 원래 명제와 대우는 진릿값이 늘 같고, 역과 이도 서로 늘 같습니다.</li>
</ul>
"""

WORKED: WorkedExample = WorkedExample(
    title="보기 1 우선순위를 지켜 진릿값 계산하기",
    body="""
<p>p, q, r가 모두 F일 때 ¬p ∨ q → r의 진릿값을 구하세요.</p>
<p class="solution-label">풀이</p>
<p>계산하기 전에 순서부터 정합니다. ¬를 가장 먼저, ∨를 그다음, →를 가장 나중에 계산하므로 이 식은 ((¬p) ∨ q) → r로 읽습니다. 이제 안쪽부터 한 겹씩 계산합니다.</p>
<table class="derivation">
  <tr><td class="step-sign"></td><td>¬p = T</td><td class="step-reason">p가 F이므로 뒤집습니다</td></tr>
  <tr><td class="step-sign"></td><td>(¬p) ∨ q = T ∨ F = T</td><td class="step-reason">하나라도 참이면 참</td></tr>
  <tr><td class="step-sign"></td><td>((¬p) ∨ q) → r = T → F = F</td><td class="step-reason">조건이 참이고 결론이 거짓</td></tr>
</table>
<p>따라서 진릿값은 F입니다. →를 먼저 계산해 ¬p ∨ (q → r)로 읽으면 F → F가 T이므로 T ∨ T = T가 되어 답이 달라집니다. 우선순위가 헷갈리면 괄호를 쳐서 계산 순서를 먼저 적어 두세요.</p>
""",
    check=lambda: value("¬p ∨ q → r", p=F, q=F, r=F) is False and value("¬p ∨ (q → r)", p=F, q=F, r=F) is True,
)

ITEM_1: Item[bool] = Item(
    number=1,
    demand=Demand.FOUNDATION,
    stem="<p>다음 가운데 명제인 것을 고르세요.</p>",
    options=(
        Option(False, "100은 큰 수이다.", "'큰 수'의 기준이 정해져 있지 않아 사람마다 판단이 다릅니다. 참인지 거짓인지 구분할 수 없으므로 명제가 아닙니다."),
        Option(True, "7은 짝수이다."),
        Option(False, r"\(x + 3 = 5\)", r"\(x = 2\)이면 참이고 \(x = 0\)이면 거짓입니다. \(x\)가 정해지지 않은 채로는 참과 거짓을 구분할 수 없으므로 명제가 아닙니다."),
        Option(False, r"\(2 + 3\)", r"값 5를 나타내는 식일 뿐 무엇이 어떻다고 주장하지 않습니다. 참과 거짓을 따질 주장이 없으므로 명제가 아닙니다. \(2 + 3 = 5\)처럼 주장이 있어야 명제입니다."),
        Option(False, "3과 4를 더하시오.", "명령문이라 참과 거짓을 따질 수 없으므로 명제가 아닙니다."),
    ),
    answer=2,
    judge=lambda is_proposition: is_proposition,
    solution="""
<p>명제는 참인지 거짓인지를 <em>구분할 수 있는</em> 문장이나 수식입니다. 7은 홀수이므로 '7은 짝수이다'는 거짓이라고 분명히 구분됩니다. 거짓인 문장도 명제입니다.</p>
<p>명제를 '참인 문장'으로 잘못 기억하면 ②를 지우고 다른 선택지에서 답을 찾게 됩니다. 명제인지 아닌지는 참인지가 아니라 참과 거짓이 하나로 정해지는지로 가립니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_2: Item[bool] = Item(
    number=2,
    demand=Demand.FOUNDATION,
    stem="<p>다음 가운데 명제가 <strong>아닌</strong> 것을 고르세요.</p>",
    options=(
        Option(True, "3은 5보다 크다.", "거짓이라고 분명히 구분되므로 거짓인 명제입니다. 거짓이라고 명제가 아닌 것은 아닙니다."),
        Option(True, "모든 자연수는 0보다 크다.", "자연수 1, 2, 3, …은 모두 0보다 크므로 참인 명제입니다. 자연수를 하나하나 확인할 수 없어도 참과 거짓은 하나로 정해집니다."),
        Option(True, r"\(1 + 1 = 2\)이고 \(2 + 2 = 5\)이다.", "참인 명제와 거짓인 명제를 '그리고'로 이은 합성명제입니다. 논리곱이므로 거짓으로 정해집니다. 거짓인 명제입니다."),
        Option(False, r"\(2x - 1 = 7\)"),
        Option(True, r"\(x^2 = 4\)를 만족하는 정수 \(x\)가 존재한다.", r"\(x\)가 들어 있지만 특정한 \(x\)가 아니라 그런 \(x\)가 있다고 주장합니다. \(x = 2\)가 식을 만족하므로 참인 명제입니다. 이런 문장은 3절의 존재한정자 ∃로 다시 나옵니다."),
    ),
    answer=4,
    judge=lambda is_proposition: not is_proposition,
    solution=r"""
<p>\(2x - 1 = 7\)은 \(x = 4\)이면 참이고 \(x = 0\)이면 거짓입니다. \(x\)의 값이 정해지지 않았으므로 참과 거짓을 하나로 정할 수 없고, 명제가 아닙니다.</p>
<p>⑤에도 \(x\)가 있지만 사정이 다릅니다. ⑤는 \(x\)의 값 하나를 두고 하는 말이 아니라 '그런 \(x\)가 존재한다'는 주장이어서 참과 거짓이 정해집니다. 변수가 있다는 것만으로 명제가 아니라고 판단하지 않도록 합니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_3: Item[str] = Item(
    number=3,
    demand=Demand.FOUNDATION,
    stem="<p>p: '4는 짝수이다', q: '9는 소수이다'일 때, 다음 가운데 진릿값이 참인 것을 고르세요.</p>",
    options=(
        formula_option("p ∧ q", "q가 거짓이므로 T ∧ F = F입니다. 9를 소수로 잘못 보면 참으로 보이지만, 9 = 3 × 3이므로 소수가 아닙니다."),
        formula_option("¬p ∨ q", "¬p는 F이고 q도 F이므로 F ∨ F = F입니다. ¬p를 p로 읽으면 참으로 잘못 계산하게 됩니다."),
        formula_option("¬(p ∨ q)", "p ∨ q = T ∨ F = T이고, 이것을 부정하면 F입니다."),
        formula_option("¬p ⊕ q", "¬p와 q가 모두 F로 값이 같으므로 F입니다. ⊕를 '값이 같으면 참'으로 거꾸로 기억하면 참으로 잘못 계산합니다."),
        formula_option("p ⊕ q"),
    ),
    answer=5,
    judge=lambda formula: value(formula, p=True, q=is_prime(9)),
    solution="""
<p>먼저 두 명제의 진릿값을 정합니다. 4는 짝수이므로 p는 T입니다. 9는 3으로 나누어떨어지므로(9 = 3 × 3) 소수가 아니고, q는 F입니다.</p>
<p>p ⊕ q는 두 값이 다를 때만 참입니다. p는 T, q는 F로 값이 다르므로 p ⊕ q는 T입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_4: Item[str] = Item(
    number=4,
    demand=Demand.FOUNDATION,
    stem="<p>p ∨ q는 참이고 p ⊕ q는 거짓입니다. 다음 가운데 진릿값이 참인 것을 고르세요.</p>",
    options=(
        formula_option("p ∧ q"),
        formula_option("p ∧ ¬q", "p, q가 모두 T이므로 T ∧ F = F입니다. p ∨ q를 '둘 가운데 하나만 참'으로 읽으면 이 답을 고르게 됩니다. 논리합은 둘 다 참인 경우를 포함합니다."),
        formula_option("¬p ↔ q", "F ↔ T = F입니다. ¬p ↔ q는 p와 q의 값이 다를 때 참이므로 p ⊕ q와 같은 뜻입니다. p ⊕ q가 거짓이라는 조건을 거꾸로 읽으면 이 답을 고르게 됩니다."),
        formula_option("¬p ∧ ¬q", "p ⊕ q가 거짓인 경우 가운데 '둘 다 거짓'만 떠올리고, p ∨ q가 참이라는 조건을 빠뜨린 답입니다. 실제로는 F ∧ F = F입니다."),
        formula_option("p → ¬q", "T → F = F입니다. p ⊕ q가 참일 때처럼 'p가 참이면 q는 거짓'이라고 생각한 답인데, 여기서는 p ⊕ q가 거짓입니다."),
    ),
    answer=1,
    judge=lambda formula: entails(["p ∨ q", "¬(p ⊕ q)"], formula),
    solution="""
<p>두 조건으로 p와 q의 값을 찾아냅니다. p ⊕ q가 거짓이므로 p와 q의 값이 같습니다. 곧 둘 다 T이거나 둘 다 F입니다. 둘 다 F이면 p ∨ q가 F가 되어 첫째 조건에 어긋납니다. 따라서 p와 q는 모두 T입니다.</p>
<p>p ∧ q = T ∧ T = T이므로 참인 것은 ①입니다. 진리표로 보면, p ∨ q와 p ⊕ q가 다른 줄은 첫째 줄(TT) 하나뿐입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_5: Item[str] = Item(
    number=5,
    demand=Demand.FOUNDATION,
    stem="<p>p가 T이고 q가 F일 때, 다음 가운데 진릿값이 참인 것을 고르세요.</p>",
    options=(
        formula_option("¬p ∧ q", "¬를 먼저 계산하므로 (¬p) ∧ q = F ∧ F = F입니다. ¬(p ∧ q)로 읽으면 참으로 잘못 계산합니다."),
        formula_option("¬(p ∨ q)", "p ∨ q = T이므로 부정하면 F입니다. ¬를 p와 q에 하나씩 붙이고 ∨는 그대로 두어 ¬p ∨ ¬q = T로 계산하면 틀립니다. ¬를 괄호 안으로 들일 때는 연산자도 바꿔야 합니다(드모르간의 법칙)."),
        formula_option("¬(p ∧ q)"),
        formula_option("p ⊕ ¬q", "¬q = T이므로 T ⊕ T = F입니다. ⊕를 ∨처럼 계산하면 참으로 잘못 계산합니다."),
        formula_option("¬(¬q) ∧ p", "¬(¬q)는 부정을 두 번 한 것이므로 q와 같은 F입니다. F ∧ T = F입니다. 부정을 한 번만 적용하면 참으로 잘못 계산합니다."),
    ),
    answer=3,
    judge=lambda formula: value(formula, p=True, q=False),
    solution="""
<p>괄호 안을 먼저 계산합니다. p ∧ q = T ∧ F = F이고, 이것을 부정하면 ¬(p ∧ q) = T입니다.</p>
<p>이 문제의 선택지는 모두 ¬가 어디까지 걸리는지를 묻습니다. ¬는 바로 뒤의 명제 하나에만 걸리고, 괄호 전체에 걸려면 괄호를 써야 합니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_6: Item[tuple[int, int]] = Item(
    number=6,
    demand=Demand.FOUNDATION,
    stem="<p>합성명제 (p ∨ q) ∧ ¬r의 진리표는 모두 몇 줄이고, 그 가운데 진릿값이 T인 줄은 몇 개인지 고르세요.</p>",
    options=(
        Option((4, 3), "4줄, 3개", "r을 빼고 p, q 두 명제의 경우만 센 답입니다. 명제가 p, q, r 셋이므로 r의 T, F까지 나누어야 합니다."),
        Option((6, 3), "6줄, 3개", "명제가 셋이라 2 × 3 = 6으로 계산한 답입니다. 명제가 하나 늘 때마다 경우가 두 배가 되므로 \\(2^3 = 8\\)줄입니다."),
        Option((8, 2), "8줄, 2개", "p ∨ q를 p ⊕ q처럼 계산해 p, q가 모두 T인 줄을 뺀 답입니다. 논리합은 둘 다 참인 경우도 참입니다."),
        Option((8, 3), "8줄, 3개"),
        Option((8, 6), "8줄, 6개", "¬r 조건을 빠뜨리고 p ∨ q가 참인 줄만 센 답입니다. 8줄 가운데 p ∨ q가 참인 줄은 6개이지만, 그 가운데 r이 F인 줄만 남습니다."),
    ),
    answer=4,
    judge=lambda answer: answer == (2 ** 3, count_true_rows("(p ∨ q) ∧ ¬r", ["p", "q", "r"])),
    solution=r"""
<p>명제가 p, q, r 셋이므로 진리표는 \(2^3 = 8\)줄입니다.</p>
<p>(p ∨ q) ∧ ¬r이 T이려면 ∧의 양쪽이 모두 T여야 합니다. ¬r이 T이려면 r이 F여야 하므로 r이 F인 4줄만 봅니다. 이 4줄에서 p, q는 TT, TF, FT, FF이고, 그 가운데 p ∨ q가 T인 것은 TT, TF, FT의 3줄입니다. 따라서 8줄, 3개입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_7: Item[str] = Item(
    number=7,
    demand=Demand.FOUNDATION,
    stem="<p>다음 가운데 항진명제인 것을 고르세요.</p>",
    options=(
        formula_option("(p ∨ q) → p", "p가 F, q가 T이면 T → F = F이므로 사건명제입니다. 정답 ⑤의 조건과 결론을 바꾼 꼴(역)입니다."),
        formula_option("p → (p ∧ q)", "p가 T, q가 F이면 T → F = F이므로 사건명제입니다. 결론이 p ∧ q이면 p보다 '좁아져서' p가 참이어도 거짓일 수 있습니다."),
        formula_option("p ∧ ¬p", "p와 ¬p 가운데 하나는 늘 거짓이므로 늘 거짓인 모순명제입니다. 값이 한쪽으로만 나온다는 점은 같지만 항진명제는 늘 참입니다."),
        formula_option("(p ⊕ q) ∨ (p ∧ q)", "p ⊕ q는 하나만 참인 경우를, p ∧ q는 둘 다 참인 경우를 덮지만 둘 다 거짓인 경우가 빠졌습니다. p, q가 모두 F이면 F ∨ F = F이므로 사건명제입니다."),
        formula_option("p → (p ∨ q)"),
    ),
    answer=5,
    judge=is_tautology,
    solution="""
<p>p → (p ∨ q)를 p의 값으로 나누어 봅니다. p가 F이면 조건이 거짓이므로 함축은 q와 상관없이 참입니다. p가 T이면 p ∨ q도 T이므로 T → T = T입니다. 어느 경우에도 참이므로 항진명제입니다.</p>
<p>함축이 거짓이 되는 것은 조건이 참이고 결론이 거짓인 경우뿐이므로, 항진명제인지 볼 때는 '조건이 참인데 결론이 거짓일 수 있는가'만 확인하면 됩니다. p가 참이면 p ∨ q는 반드시 참이므로 그런 경우가 없습니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_8: Item[str] = Item(
    number=8,
    demand=Demand.FOUNDATION,
    stem="<p>p가 거짓일 때, q의 진릿값과 상관없이 참인 명제를 고르세요.</p>",
    options=(
        formula_option("p ∧ q", "p가 F이면 q와 상관없이 늘 F입니다. q와 상관없이 값이 정해진다는 점은 맞지만 참이 아니라 거짓으로 정해집니다."),
        formula_option("p → q"),
        formula_option("¬p → q", "이 함축의 조건은 ¬p이고, p가 F이므로 ¬p는 T입니다. 조건이 참이므로 결론 q에 따라 값이 정해져서, q가 F이면 거짓입니다. 무엇이 조건인지 먼저 확인해야 합니다."),
        formula_option("q → p", "q가 T이면 T → F = F입니다. 조건과 결론의 자리를 바꿔 읽은 답입니다."),
        formula_option("p ↔ q", "p가 F이므로 q도 F일 때만 참입니다. q가 T이면 거짓입니다."),
    ),
    answer=2,
    judge=lambda formula: entails(["¬p"], formula),
    solution="""
<p>함축 p → q는 조건 p가 참이고 결론 q가 거짓일 때만 거짓입니다. p가 거짓이면 그런 경우가 생길 수 없으므로 q가 무엇이든 참입니다.</p>
<p>비와 우산으로 말하면, 비가 오지 않은 날에는 우산을 가지고 가든 가지 않든 '비가 오면 우산을 가지고 간다'는 약속을 어긴 것이 아닙니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_9: Item[str] = Item(
    number=9,
    demand=Demand.FOUNDATION,
    stem="<p>정수 \\(n\\)에 대해 p: '\\(n\\)은 4의 배수이다', q: '\\(n\\)은 짝수이다'라고 합니다. 다음 가운데 p → q와 같은 뜻인 문장을 고르세요.</p>",
    options=(
        Option("¬q → p", r"\(n\)이 짝수가 아니면 \(n\)은 4의 배수이다.", "¬q → p입니다. 대우를 만들면서 조건과 결론을 바꾸고 p를 부정하는 것을 빠뜨렸습니다. 대우는 ¬q → ¬p입니다."),
        Option("p ∧ q", r"\(n\)은 4의 배수이고 짝수이다.", "p ∧ q입니다. '이면'을 '그리고'로 읽은 답입니다. 함축은 p가 거짓일 때도 참이지만 p ∧ q는 p가 거짓이면 거짓입니다."),
        Option("q → p", r"\(n\)이 4의 배수인 것은 \(n\)이 짝수이기 위한 필요조건이다.", "p가 q의 필요조건이라는 말은 q ⇒ p, 곧 역 q → p를 뜻합니다. 화살표의 뒤쪽이 필요조건입니다."),
        Option("p → q", r"\(n\)이 짝수인 것은 \(n\)이 4의 배수이기 위한 필요조건이다."),
        Option("p ↔ q", r"\(n\)이 4의 배수인 것은 \(n\)이 짝수이기 위한 필요충분조건이다.", "p ↔ q입니다. 6은 짝수이지만 4의 배수가 아니므로 q에서 p로 가는 방향은 성립하지 않습니다. p → q는 한 방향만 말합니다."),
    ),
    answer=4,
    judge=lambda formula: equivalent(formula, "p → q"),
    solution="""
<p>p → q에서 화살표의 앞 p는 q의 충분조건이고, 화살표의 뒤 q는 p의 필요조건입니다. 따라서 'q는 p이기 위한 필요조건이다', 곧 '\\(n\\)이 짝수인 것은 \\(n\\)이 4의 배수이기 위한 필요조건이다'가 p → q와 같은 뜻입니다.</p>
<p>진리집합으로 확인하면, 4의 배수의 집합 P는 짝수의 집합 Q 안에 들어 있습니다(P ⊂ Q). 4의 배수이려면 짝수인 것이 꼭 필요하고, 그래서 큰 집합 쪽 q가 필요조건입니다.</p>
""",
    layout=Layout.LONG,
)


def _sufficient(condition: Callable[[Fraction], bool], consequence: Callable[[Fraction], bool]) -> bool:
    """실수 조건 사이의 ⇒를 유리수 격자점에서 확인한다(보조 근거). 구간 추론은 해설에 쓴다."""
    return all(consequence(x) for x in rational_grid(-10, 10, 8) if condition(x))


def _p(x: Fraction) -> bool:
    return x > 3


def _q(x: Fraction) -> bool:
    return x > 1


ITEM_10_CLAIMS: dict[str, bool] = {
    "p ⇒ q": _sufficient(_p, _q),
    "q ⇒ p": _sufficient(_q, _p),
    "p ⇔ q": _sufficient(_p, _q) and _sufficient(_q, _p),
    "¬p ⇒ ¬q": _sufficient(lambda x: not _p(x), lambda x: not _q(x)),
    "관계 없음": not _sufficient(_p, _q) and not _sufficient(_q, _p),
}

ITEM_10: Item[str] = Item(
    number=10,
    demand=Demand.FOUNDATION,
    stem="<p>실수 \\(x\\)에 대한 두 조건 p: \\(x &gt; 3\\), q: \\(x &gt; 1\\)에 대해 옳은 것을 고르세요.</p>",
    options=(
        Option("p ⇒ q", "p는 q의 충분조건이다."),
        Option("q ⇒ p", "p는 q의 필요조건이다.", "p가 q의 필요조건이려면 q ⇒ p여야 합니다. 그런데 \\(x = 2\\)는 q를 만족하지만 p는 만족하지 않습니다. 충분조건과 필요조건의 자리를 바꾼 답입니다."),
        Option("p ⇔ q", "p와 q는 서로 필요충분조건이다.", "p ⇒ q는 성립하지만 q ⇒ p는 \\(x = 2\\)에서 깨집니다. 한 방향만 성립하므로 필요충분조건이 아닙니다."),
        Option("¬p ⇒ ¬q", "¬p는 ¬q의 충분조건이다.", "¬p는 \\(x \\le 3\\), ¬q는 \\(x \\le 1\\)입니다. \\(x = 2\\)이면 ¬p는 참이지만 ¬q는 거짓이므로 ¬p ⇒ ¬q가 성립하지 않습니다. ¬p → ¬q는 원래 명제의 이이고, 이는 원래 명제와 동치가 아닙니다."),
        Option("관계 없음", "p와 q 사이에는 충분조건이나 필요조건의 관계가 없다.", "3보다 큰 수는 모두 1보다 크므로 p ⇒ q가 성립합니다. 관계가 있습니다."),
    ),
    answer=1,
    judge=lambda claim: ITEM_10_CLAIMS[claim],
    solution="""
<p>진리집합으로 봅니다. \\(P = \\{x \\mid x &gt; 3\\}\\), \\(Q = \\{x \\mid x &gt; 1\\}\\)입니다. 3보다 큰 수는 모두 1보다 크므로 P ⊂ Q이고, p ⇒ q입니다. 화살표의 앞 p가 충분조건이므로 'p는 q의 충분조건이다'가 옳습니다.</p>
<p>작은 집합 쪽(P)이 충분조건, 큰 집합 쪽(Q)이 필요조건이라고 기억하면 헷갈리지 않습니다. 반대 방향 q ⇒ p는 \\(x = 2\\)처럼 1과 3 사이의 수가 반례가 됩니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_11: Item[str] = Item(
    number=11,
    demand=Demand.FOUNDATION,
    stem="<p>정수 \\(n\\)에 대한 명제 '\\(n\\)이 6의 배수이면 \\(n\\)은 3의 배수이다'의 대우를 고르세요.</p>",
    options=(
        Option("q → p", r"\(n\)이 3의 배수이면 \(n\)은 6의 배수이다.", "조건과 결론의 자리만 바꾼 역 q → p입니다."),
        Option("¬p → ¬q", r"\(n\)이 6의 배수가 아니면 \(n\)은 3의 배수가 아니다.", "조건과 결론을 부정만 한 이 ¬p → ¬q입니다. 자리도 바꿔야 대우입니다."),
        Option("¬q → ¬p", r"\(n\)이 3의 배수가 아니면 \(n\)은 6의 배수가 아니다."),
        Option("¬q → p", r"\(n\)이 3의 배수가 아니면 \(n\)은 6의 배수이다.", "자리를 바꾸고 조건만 부정했습니다(¬q → p). 결론 쪽 p도 부정해야 합니다."),
        Option("p → ¬q", r"\(n\)이 6의 배수이면 \(n\)은 3의 배수가 아니다.", "결론만 부정했습니다(p → ¬q). 대우는 자리를 바꾸고 둘 다 부정합니다."),
    ),
    answer=3,
    judge=lambda form: parse(form) == parse("¬q → ¬p"),
    solution="""
<p>p: '\\(n\\)은 6의 배수이다', q: '\\(n\\)은 3의 배수이다'로 놓으면 원래 명제는 p → q입니다. 대우는 조건과 결론의 자리를 바꾸고 둘 다 부정한 ¬q → ¬p, 곧 '\\(n\\)이 3의 배수가 아니면 \\(n\\)은 6의 배수가 아니다'입니다.</p>
<p>원래 명제는 참이고, 대우도 참입니다. 반면 역 '3의 배수이면 6의 배수이다'는 \\(n = 3\\)에서 거짓입니다. 원래 명제와 진릿값이 늘 같은 것은 역이 아니라 대우입니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_12: Item[str] = Item(
    number=12,
    demand=Demand.FOUNDATION,
    stem="<p>p ↔ q가 참일 때, 다음 가운데 반드시 참인 것을 고르세요.</p>",
    options=(
        formula_option("p ∧ q", "p, q가 모두 F인 경우에는 거짓입니다. p ↔ q를 '둘 다 참'으로 좁게 읽은 답입니다."),
        formula_option("p ∨ q", "p, q가 모두 F인 경우에는 거짓입니다. p ↔ q는 둘 다 거짓인 경우에도 참입니다."),
        formula_option("p ⊕ q", "p ↔ q가 참이면 두 값이 같으므로 p ⊕ q는 늘 거짓입니다. ⊕와 ↔는 서로의 부정입니다."),
        formula_option("¬p ∧ ¬q", "p, q가 모두 T인 경우에는 거짓입니다. 두 경우 가운데 하나만 본 답입니다."),
        formula_option("p → q"),
    ),
    answer=5,
    judge=lambda formula: entails(["p ↔ q"], formula),
    solution="""
<p>p ↔ q가 참이면 p와 q의 값이 같으므로, 가능한 경우는 둘 다 T이거나 둘 다 F인 두 가지입니다. 두 경우를 모두 확인합니다.</p>
<p>p → q는 둘 다 T일 때 T → T = T, 둘 다 F일 때 F → F = T입니다. 두 경우 모두 참이므로 반드시 참입니다. 쌍방조건명제 p ↔ q는 (p → q) ∧ (q → p)와 같으므로, 그 한쪽인 p → q가 참인 것은 당연합니다.</p>
""",
    layout=Layout.SHORT,
)

SECTION_A: Section = Section(
    title="1. 명제와 논리 연산자",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_1, ITEM_2, ITEM_3, ITEM_4, ITEM_5, ITEM_6, ITEM_7, ITEM_8, ITEM_9, ITEM_10, ITEM_11, ITEM_12),
)
