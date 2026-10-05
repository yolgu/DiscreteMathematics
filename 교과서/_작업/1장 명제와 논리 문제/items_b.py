"""2절 논리적 동치: 핵심 정리, 보기 2, 문제 13~22."""

from __future__ import annotations

import html

from fragments import Step, chain_holds, computed_truth_table, derivation_html, laws_named_correctly
from logic_tools import (
    arithmetic_holds,
    dual,
    equivalent,
    law_applies,
    law_applies_up_to_commutation,
    laws_that_apply,
    parse,
    value,
)
from model import Demand, Item, Layout, Option, Section, WorkedExample, formula_option

SUMMARY: str = """
<ul>
  <li><strong>논리적 동치</strong> p ≡ q: 두 명제의 진릿값이 모든 경우에 같다는 뜻입니다. p ↔ q가 항진명제라는 말과 같습니다. 동치는 진리표의 열을 견주거나, 동치 법칙으로 한쪽 식을 다른 쪽 식으로 바꾸어 보입니다.</li>
  <li><strong>쌍대</strong>: ¬, ∧, ∨, T, F만으로 된 식에서 ∧와 ∨, T와 F를 모두 맞바꾼 식입니다. 두 식이 동치이면 쌍대끼리도 동치입니다.</li>
  <li><strong>식을 바꾸는 요령</strong>: →가 있으면 함축법칙으로 먼저 없앱니다. 괄호 전체에 걸린 ¬는 드모르간의 법칙으로 안으로 들이며 ∧와 ∨를 맞바꿉니다. 두 괄호에 같은 명제가 같은 연산자로 붙어 있으면 분배법칙을 거꾸로 써서 묶어 냅니다.</li>
  <li><strong>곱하기와 더하기 비유</strong>: T를 1, F를 0, ∧를 곱하기, ∨를 더하기로 옮기면 여러 법칙을 산수처럼 볼 수 있지만, ∨ 쪽에서 1 + 1이 나오는 곳은 산수로 성립하지 않습니다.</li>
</ul>
<table class="prose-table">
  <caption>이 장의 동치 법칙. 한 줄의 두 식은 서로 쌍대입니다.</caption>
  <thead><tr><th>법칙</th><th>식</th><th>쌍대인 식</th></tr></thead>
  <tbody>
    <tr><td>항등법칙</td><td>p ∧ T ≡ p</td><td>p ∨ F ≡ p</td></tr>
    <tr><td>지배법칙</td><td>p ∧ F ≡ F</td><td>p ∨ T ≡ T</td></tr>
    <tr><td>부정법칙</td><td>p ∧ ¬p ≡ F</td><td>p ∨ ¬p ≡ T</td></tr>
    <tr><td>이중 부정법칙</td><td colspan="2">¬(¬p) ≡ p</td></tr>
    <tr><td>멱등법칙</td><td>p ∧ p ≡ p</td><td>p ∨ p ≡ p</td></tr>
    <tr><td>교환법칙</td><td>p ∧ q ≡ q ∧ p</td><td>p ∨ q ≡ q ∨ p</td></tr>
    <tr><td>결합법칙</td><td>(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)</td><td>(p ∨ q) ∨ r ≡ p ∨ (q ∨ r)</td></tr>
    <tr><td>분배법칙</td><td>p ∨ (q ∧ r)<br>≡ (p ∨ q) ∧ (p ∨ r)</td><td>p ∧ (q ∨ r)<br>≡ (p ∧ q) ∨ (p ∧ r)</td></tr>
    <tr><td>드모르간의 법칙</td><td>¬(p ∧ q) ≡ ¬p ∨ ¬q</td><td>¬(p ∨ q) ≡ ¬p ∧ ¬q</td></tr>
    <tr><td>흡수법칙</td><td>p ∧ (p ∨ q) ≡ p</td><td>p ∨ (p ∧ q) ≡ p</td></tr>
    <tr><td>함축법칙</td><td colspan="2">p → q ≡ ¬p ∨ q</td></tr>
  </tbody>
</table>
"""

WORKED_START: str = "¬(p → q)"
WORKED_STEPS: tuple[Step, ...] = (
    Step("¬(¬p ∨ q)", "함축법칙"),
    Step("¬(¬p) ∧ ¬q", "드모르간의 법칙"),
    Step("p ∧ ¬q", "이중 부정법칙"),
)

WORKED: WorkedExample = WorkedExample(
    title="보기 2 동치 법칙으로 식 바꾸기",
    body=f"""
<p>¬(p → q) ≡ p ∧ ¬q임을 동치 법칙으로 보이세요.</p>
<p class="solution-label">풀이</p>
<p>→가 남아 있으면 드모르간의 법칙 같은 다른 법칙을 쓸 수 없으므로, 먼저 함축법칙으로 →를 ¬와 ∨로 바꿉니다. 그러면 괄호 전체에 ¬가 걸린 꼴이 되니, 드모르간의 법칙으로 ¬를 안으로 들이면서 ∨를 ∧로 바꿉니다. 마지막으로 부정이 두 번 걸린 ¬(¬p)를 이중 부정법칙으로 정리합니다.</p>
{derivation_html(WORKED_START, WORKED_STEPS)}
<p>결과를 말로 읽으면 'p이면 q'라는 약속이 깨지는 것은 p가 참인데 q가 거짓인 경우라는 뜻입니다. 함축의 진리표에서 거짓인 줄이 TF 하나뿐이었던 것과 맞습니다.</p>
""",
    check=lambda: chain_holds(WORKED_START, WORKED_STEPS) and laws_named_correctly(WORKED_START, WORKED_STEPS),
)

ITEM_13: Item[str] = Item(
    number=13,
    demand=Demand.FOUNDATION,
    stem="<p>¬(p ⊕ q)와 논리적 동치인 것을 고르세요.</p>",
    options=(
        formula_option("p ∧ q", "진릿값이 T, F, F, F입니다. ¬(p ⊕ q)가 참인 두 줄 가운데 둘 다 거짓인 넷째 줄을 빠뜨린 답입니다."),
        formula_option("p ↔ q"),
        formula_option("¬p ⊕ ¬q", "진릿값이 F, T, T, F로 p ⊕ q와 같습니다. p와 q를 둘 다 뒤집어도 두 값이 같은지 다른지는 그대로이기 때문입니다. ¬를 안으로 나눠 넣는 규칙은 ⊕에는 없습니다."),
        formula_option("¬p ∨ ¬q", "¬(p ∧ q)와 같은 식으로, 진릿값이 F, T, T, T입니다. ⊕를 ∧처럼 보고 드모르간의 법칙을 쓴 답입니다."),
        formula_option("p → q", "진릿값이 T, F, T, T입니다. 셋째 줄(p가 F, q가 T)에서 다릅니다. 한 방향의 약속만으로는 두 값이 같다는 뜻이 되지 않습니다."),
    ),
    answer=2,
    judge=lambda formula: equivalent(formula, "¬(p ⊕ q)"),
    solution=f"""
<p>진리표로 열을 견줍니다. p ⊕ q는 두 값이 다를 때만 참이므로 F, T, T, F이고, 이것을 부정한 ¬(p ⊕ q)는 T, F, F, T입니다. 두 값이 같을 때만 참인 p ↔ q도 T, F, F, T입니다.</p>
{computed_truth_table(["p", "q"], ["p ⊕ q", "¬(p ⊕ q)", "p ↔ q"])}
<p>두 열이 모든 줄에서 같으므로 ¬(p ⊕ q) ≡ p ↔ q입니다. '값이 다르다'를 부정하면 '값이 같다'가 된다고 읽어도 됩니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_14_START: str = "¬(p ∧ ¬q)"
ITEM_14_END: str = "¬p ∨ q"

ITEM_14: Item[str] = Item(
    number=14,
    demand=Demand.FOUNDATION,
    stem=f"""
<p>다음은 ¬(p ∧ ¬q) ≡ ¬p ∨ q를 보이는 과정입니다. (가)에 알맞은 식을 고르세요.</p>
<table class="derivation">
  <tr><td class="step-sign"></td><td>{html.escape(ITEM_14_START)}</td><td class="step-reason"></td></tr>
  <tr><td class="step-sign">≡</td><td>(가)</td><td class="step-reason">드모르간의 법칙</td></tr>
  <tr><td class="step-sign">≡</td><td>{html.escape(ITEM_14_END)}</td><td class="step-reason">이중 부정법칙</td></tr>
</table>
""",
    options=(
        formula_option("¬p ∨ ¬(¬q)"),
        formula_option("¬p ∧ ¬(¬q)", "∧를 ∨로 바꾸지 않았습니다. 이중 부정법칙을 쓰면 ¬p ∧ q가 되어 마지막 줄과 다릅니다."),
        formula_option("¬p ∨ ¬q", "¬q 전체를 부정해야 하는데 부정 하나를 잃었습니다. ¬q를 부정하면 ¬(¬q)입니다. 이렇게 쓰면 다음 줄에서 이중 부정법칙을 쓸 자리도 없습니다."),
        formula_option("p ∨ ¬(¬q)", "p 앞에 ¬를 붙이지 않았습니다. 드모르간의 법칙은 괄호 안의 두 명제를 모두 부정합니다."),
        formula_option("¬p ∧ ¬q", "연산자를 바꾸지 않은 실수와 부정 하나를 잃은 실수가 겹쳤습니다."),
    ),
    answer=1,
    judge=lambda formula: law_applies("드모르간의 법칙", ITEM_14_START, formula) and law_applies("이중 부정법칙", formula, ITEM_14_END),
    solution="""
<p>드모르간의 법칙 ¬(A ∧ B) ≡ ¬A ∨ ¬B에서 A 자리에 p, B 자리에 ¬q가 들어 있습니다. 괄호 안의 두 명제를 각각 부정하고 ∧를 ∨로 바꾸면 ¬p ∨ ¬(¬q)입니다. B 자리의 ¬q를 통째로 부정하므로 ¬(¬q)가 됩니다.</p>
<p>다음 줄에서는 이중 부정법칙으로 ¬(¬q)를 q로 바꾸어 ¬p ∨ q에 닿습니다. 결과 ¬p ∨ q는 함축법칙으로 p → q이므로, 이 동치는 '약속 p → q는 p가 참이고 q가 거짓인 경우가 없다는 것'과 같은 말임을 보여 줍니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_15: Item[str] = Item(
    number=15,
    demand=Demand.FOUNDATION,
    stem="<p>동치 p ∨ (p ∧ q) ≡ p에 해당하는 법칙의 이름을 고르세요.</p>",
    options=(
        Option("분배법칙", "분배법칙", "분배법칙은 p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)처럼 괄호를 풀거나 묶는 법칙입니다. p ∨ (p ∧ q)에 분배법칙을 쓰면 (p ∨ p) ∧ (p ∨ q)가 될 뿐 p 하나로 줄지 않습니다."),
        Option("멱등법칙", "멱등법칙", "멱등법칙은 p ∨ p ≡ p처럼 같은 명제끼리의 연산입니다. 여기서는 p와 p ∧ q를 잇습니다."),
        Option("지배법칙", "지배법칙", "지배법칙은 p ∨ T ≡ T, p ∧ F ≡ F처럼 T나 F가 결과를 정하는 법칙입니다."),
        Option("흡수법칙", "흡수법칙"),
        Option("항등법칙", "항등법칙", "항등법칙은 p ∨ F ≡ p, p ∧ T ≡ p입니다. 결과가 p라는 점이 같아서 헷갈리지만, 상대가 F나 T일 때의 법칙입니다."),
    ),
    answer=4,
    judge=lambda law: law_applies(law, "p ∨ (p ∧ q)", "p"),
    solution="""
<p>p ∧ q가 참이면 p도 반드시 참입니다. 곧 p ∧ q가 참인 경우는 p가 참인 경우 안에 모두 들어 있습니다. 그래서 p에 p ∧ q를 ∨로 더해도 p가 참인 경우가 넓어지지 않고, 결과는 p 그대로입니다. 큰 쪽(p)이 작은 쪽(p ∧ q)을 삼켜 버리므로 흡수법칙이라고 합니다.</p>
<p>쌍대인 p ∧ (p ∨ q) ≡ p도 흡수법칙입니다. 흡수법칙은 분배법칙, 드모르간의 법칙과 함께 꼭 기억해 둘 법칙입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_16_SOURCE: str = "p ∨ (q ∧ T)"

ITEM_16: Item[str] = Item(
    number=16,
    demand=Demand.FOUNDATION,
    stem="<p>식 p ∨ (q ∧ T)의 쌍대를 고르세요.</p>",
    options=(
        formula_option("p ∧ (q ∨ T)", "∧와 ∨는 맞바꾸었지만 T를 F로 바꾸지 않았습니다."),
        formula_option("p ∨ (q ∧ F)", "T는 F로 바꾸었지만 ∧와 ∨를 맞바꾸지 않았습니다."),
        formula_option("p ∧ (q ∨ F)"),
        formula_option("¬p ∧ (¬q ∨ F)", "변수에 ¬를 붙였습니다. 쌍대는 부정을 더하지 않습니다. 드모르간의 법칙으로 식 전체를 부정할 때와 헷갈린 답입니다."),
        formula_option("¬(p ∨ (q ∧ T))", "식 전체의 부정이지 쌍대가 아닙니다."),
    ),
    answer=3,
    judge=lambda formula: parse(formula) == dual(parse(ITEM_16_SOURCE)),
    solution="""
<p>쌍대는 ∧와 ∨를 맞바꾸고, T와 F를 맞바꾼 식입니다. 변수와 ¬는 그대로 둡니다. p ∨ (q ∧ T)에서 바깥의 ∨는 ∧로, 괄호 안의 ∧는 ∨로, T는 F로 바꾸면 p ∧ (q ∨ F)입니다.</p>
<p>참고로 p ∨ (q ∧ T) ≡ p ∨ q이고(항등법칙), 그 쌍대 p ∧ (q ∨ F) ≡ p ∧ q입니다. 두 식이 동치이면 쌍대끼리도 동치라는 성질이 여기서도 보입니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_17_START: str = "¬(¬p ∧ ¬q) ∧ (p ∨ F)"
ITEM_17_LINES: tuple[Step, ...] = (
    Step("¬(¬p ∧ ¬q) ∧ p", "지배법칙", "(가)"),
    Step("(¬(¬p) ∨ ¬(¬q)) ∧ p", "드모르간의 법칙", "(나)"),
    Step("(p ∨ q) ∧ p", "이중 부정법칙", "(다)"),
    Step("p ∧ (p ∨ q)", "교환법칙", "(라)"),
    Step("p", "흡수법칙", "(마)"),
)


def _line_is_misnamed(index: int) -> bool:
    previous: str = ITEM_17_START if index == 0 else ITEM_17_LINES[index - 1].formula
    line: Step = ITEM_17_LINES[index]
    return not law_applies(line.reason, previous, line.formula)


ITEM_17: Item[int] = Item(
    number=17,
    demand=Demand.FOUNDATION,
    stem=f"""
<p>다음은 ¬(¬p ∧ ¬q) ∧ (p ∨ F)를 간단히 하는 과정입니다. 오른쪽에 적은 법칙의 이름이 <strong>틀린</strong> 줄을 고르세요.</p>
{derivation_html(ITEM_17_START, ITEM_17_LINES)}
""",
    options=(
        Option(0, "(가)"),
        Option(1, "(나)", "괄호 전체에 걸린 ¬를 안으로 들이면서 ∧를 ∨로 바꾸었으므로 드모르간의 법칙이 맞습니다."),
        Option(2, "(다)", "¬(¬p)를 p로, ¬(¬q)를 q로 바꾸었으므로 이중 부정법칙이 맞습니다."),
        Option(3, "(라)", "∧의 양쪽을 맞바꾸었으므로 교환법칙이 맞습니다."),
        Option(4, "(마)", "p ∧ (p ∨ q) ≡ p는 흡수법칙이 맞습니다."),
    ),
    answer=1,
    judge=_line_is_misnamed,
    solution="""
<p>(가)는 p ∨ F를 p로 바꾼 줄입니다. F와 ∨를 하면 상대가 그대로 남으므로 항등법칙(p ∨ F ≡ p)입니다. 지배법칙은 p ∨ T ≡ T, p ∧ F ≡ F처럼 결과가 T나 F로 정해지는 법칙이므로 이름이 틀렸습니다.</p>
<p>항등법칙과 지배법칙은 둘 다 T나 F가 들어 있어 헷갈리기 쉽습니다. 결과에 상대 p가 남으면 항등법칙, 결과가 T나 F 하나로 정해지면 지배법칙입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_18_START: str = "(p ∧ q) ∨ (p ∧ ¬q)"
ITEM_18_STEPS: tuple[Step, ...] = (
    Step("p ∧ (q ∨ ¬q)", "분배법칙"),
    Step("p ∧ T", "부정법칙"),
    Step("p", "항등법칙"),
)

ITEM_18: Item[str] = Item(
    number=18,
    demand=Demand.FOUNDATION,
    stem="<p>(p ∧ q) ∨ (p ∧ ¬q)를 가장 간단히 한 것을 고르세요.</p>",
    options=(
        formula_option("q", "두 괄호에 공통으로 들어 있는 것은 q가 아니라 p입니다. q와 ¬q는 서로 반대입니다."),
        formula_option("p ∧ q", "앞 괄호만 남긴 답입니다. 뒤 괄호 p ∧ ¬q가 참인 경우(p가 T, q가 F)에 원래 식은 참이지만 p ∧ q는 거짓입니다."),
        formula_option("T", "q ∨ ¬q가 T인 데까지만 보고 앞의 p ∧를 빠뜨렸습니다. p가 F이면 원래 식은 거짓입니다."),
        formula_option("F", "q ∧ ¬q가 생긴다고 착각한 답입니다. p를 묶어 낸 뒤 괄호 안은 q ∨ ¬q입니다."),
        formula_option("p"),
    ),
    answer=5,
    judge=lambda formula: equivalent(formula, ITEM_18_START),
    solution=f"""
<p>두 괄호에 p ∧가 똑같이 들어 있으므로, 분배법칙 p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)을 거꾸로 써서 p를 밖으로 묶어 냅니다.</p>
{derivation_html(ITEM_18_START, ITEM_18_STEPS)}
<p>뜻으로 읽으면, q가 참이든 거짓이든 p가 참이기만 하면 두 괄호 가운데 하나가 참이 된다는 것입니다. 그래서 결과는 p입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_19_START: str = "(p → q) ∧ (¬p → q)"
ITEM_19_STEPS: tuple[Step, ...] = (
    Step("(¬p ∨ q) ∧ (¬(¬p) ∨ q)", "함축법칙"),
    Step("(¬p ∨ q) ∧ (p ∨ q)", "이중 부정법칙"),
    Step("(¬p ∧ p) ∨ q", "분배법칙(거꾸로, q를 묶어 냄)"),
    Step("F ∨ q", "부정법칙"),
    Step("q", "항등법칙"),
)

ITEM_19: Item[str] = Item(
    number=19,
    demand=Demand.VARIATION,
    stem="<p>(p → q) ∧ (¬p → q)를 가장 간단히 한 것을 고르세요.</p>",
    options=(
        formula_option("¬p", "(p → q) ∧ (p → ¬q) ≡ ¬p라는 결과를 그대로 옮긴 답입니다. 그 식은 조건이 같고 결론이 반대였지만, 이 식은 조건이 반대이고 결론이 같습니다."),
        formula_option("q"),
        formula_option("p ∨ q", "둘째 함축 ¬p → q ≡ p ∨ q만 간단히 하고 첫째 함축을 빠뜨렸습니다. p가 T, q가 F이면 원래 식은 거짓이지만 p ∨ q는 참입니다."),
        formula_option("T", "'p든 ¬p든 하나는 참이니 늘 참'이라고 생각한 답입니다. q가 F이면 두 함축 가운데 조건이 참인 쪽이 거짓이 되므로 원래 식은 거짓입니다."),
        formula_option("F", "¬p ∧ p가 F인 데까지만 보고 그 뒤의 ∨ q를 빠뜨렸습니다."),
    ),
    answer=2,
    judge=lambda formula: equivalent(formula, ITEM_19_START),
    solution=f"""
<p>→가 있으므로 먼저 함축법칙으로 두 함축을 ∨로 바꿉니다. 그러면 두 괄호에 '∨ q'가 똑같이 붙어 있습니다. 교환법칙으로 q를 앞에 둔 꼴 (q ∨ ¬p) ∧ (q ∨ p)로 보면 분배법칙 p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)의 오른쪽 꼴이므로, 거꾸로 써서 q를 묶어 냅니다.</p>
{derivation_html(ITEM_19_START, ITEM_19_STEPS)}
<p>넷째 줄과 다섯째 줄도 엄밀히는 교환법칙으로 ¬p ∧ p를 p ∧ ¬p로, F ∨ q를 q ∨ F로 바꾼 뒤 부정법칙과 항등법칙을 쓴 것입니다. 교환법칙은 이렇게 따로 적지 않고 쓰는 일이 많습니다.</p>
<p>뜻으로 읽으면, p가 참이어도 q이고 p가 거짓이어도 q라는 것입니다. 어느 경우든 q이니 결국 q입니다.</p>
""",
    layout=Layout.SHORT,
)

ITEM_20: Item[tuple[str, str]] = Item(
    number=20,
    demand=Demand.FOUNDATION,
    stem="<p>T를 1, F를 0으로 놓고 ∧를 곱하기(×), ∨를 더하기(+)로 바꾸었을 때, 0과 1을 넣는 모든 경우에 산수 식으로도 성립하는 동치 법칙을 고르세요.</p>",
    options=(
        Option(("p ∨ p", "p"), "p ∨ p ≡ p", "p + p = p가 되는데, p = 1이면 1 + 1 = 2로 1이 아닙니다."),
        Option(("p ∨ T", "T"), "p ∨ T ≡ T", "p + 1 = 1이 되는데, p = 1이면 1 + 1 = 2로 1이 아닙니다."),
        Option(("p ∨ (q ∧ r)", "(p ∨ q) ∧ (p ∨ r)"), "p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)", "p + q × r = (p + q) × (p + r)이 되는데, p = q = r = 1이면 왼쪽은 2, 오른쪽은 4입니다."),
        Option(("p ∧ (q ∨ r)", "(p ∧ q) ∨ (p ∧ r)"), "p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)"),
        Option(("p ∨ (p ∧ q)", "p"), "p ∨ (p ∧ q) ≡ p", "p + p × q = p가 되는데, p = q = 1이면 1 + 1 = 2로 1이 아닙니다."),
    ),
    answer=4,
    judge=lambda law: arithmetic_holds(*law),
    solution="""
<p>p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)을 옮기면 p × (q + r) = p × q + p × r입니다. 이것은 보통 산수의 분배법칙이므로 0과 1뿐 아니라 어떤 수를 넣어도 성립합니다.</p>
<p>나머지 넷은 모두 ∨ 쪽에서 1 + 1이 나와 깨집니다. 논리에서는 T ∨ T가 T이지만 산수에서는 1 + 1이 2가 되기 때문입니다. 비유는 처음 익힐 때 좋은 다리가 되지만, ∨가 1 + 1에 닿는 곳에서는 논리의 법칙으로 돌아와야 합니다.</p>
""",
    layout=Layout.LONG,
)

ITEM_21_START: str = "p → (q → r)"
ITEM_21_STEPS: tuple[Step, ...] = (
    Step("¬p ∨ (¬q ∨ r)", "함축법칙(두 번)"),
    Step("(¬p ∨ ¬q) ∨ r", "결합법칙"),
    Step("¬(p ∧ q) ∨ r", "드모르간의 법칙"),
    Step("(p ∧ q) → r", "함축법칙"),
)

ITEM_21: Item[str] = Item(
    number=21,
    demand=Demand.CHALLENGE,
    stem="<p>p → (q → r)과 논리적 동치인 것을 고르세요.</p>",
    options=(
        formula_option("(p → q) → r", "괄호의 자리를 옮긴 답입니다. →에는 결합법칙이 없습니다. p, q, r가 모두 F이면 원래 식은 T이지만 이 식은 (F → F) → F = T → F = F입니다."),
        formula_option("(p ∨ q) → r", "드모르간의 법칙에서 ∨를 ∧로 바꾸지 않은 답입니다. p가 T, q와 r가 F이면 원래 식은 T이지만 이 식은 T → F = F입니다."),
        formula_option("(p ∧ q) → r"),
        formula_option("(p → q) ∧ (q → r)", "가설적 삼단논법의 전제처럼 읽은 답입니다. p가 F, q가 T, r가 F이면 원래 식은 T이지만 이 식은 T ∧ F = F입니다."),
        formula_option("p → (q ∧ r)", "안쪽의 →를 ∧로 바꾼 답입니다. p가 T, q와 r가 F이면 원래 식은 T이지만 이 식은 T → F = F입니다."),
    ),
    answer=3,
    judge=lambda formula: equivalent(formula, ITEM_21_START),
    solution=f"""
<p>진리표로 다섯 식을 모두 견주면 8줄씩 계산해야 하므로, 동치 법칙으로 원래 식을 바꾸어 봅니다. →가 두 개 있으니 함축법칙으로 둘 다 없애고, 같은 연산자 ∨만 남으면 결합법칙으로 괄호를 옮깁니다. ¬p ∨ ¬q는 드모르간의 법칙으로 ¬(p ∧ q)로 묶고, 마지막에 함축법칙을 거꾸로 써서 →를 되살립니다.</p>
{derivation_html(ITEM_21_START, ITEM_21_STEPS)}
<p>뜻으로 읽으면 'p이면, q이면 r이다'는 'p와 q가 둘 다 참이면 r이다'와 같은 약속입니다. 조건 두 개를 차례로 거는 것과 한꺼번에 거는 것이 같습니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_22: Item[tuple[bool, bool, bool]] = Item(
    number=22,
    demand=Demand.FOUNDATION,
    stem="<p>(p ∧ q) ∨ r과 p ∧ (q ∨ r)이 동치가 <strong>아님</strong>을 보여 주는 p, q, r의 진릿값을 고르세요.</p>",
    options=(
        Option((True, True, False), "p: T, q: T, r: F", "왼쪽은 (T ∧ T) ∨ F = T, 오른쪽은 T ∧ (T ∨ F) = T로 같습니다."),
        Option((True, False, True), "p: T, q: F, r: T", "왼쪽은 (T ∧ F) ∨ T = T, 오른쪽은 T ∧ (F ∨ T) = T로 같습니다."),
        Option((True, False, False), "p: T, q: F, r: F", "왼쪽은 (T ∧ F) ∨ F = F, 오른쪽은 T ∧ (F ∨ F) = F로 같습니다."),
        Option((False, True, False), "p: F, q: T, r: F", "왼쪽은 (F ∧ T) ∨ F = F, 오른쪽은 F ∧ (T ∨ F) = F로 같습니다."),
        Option((False, True, True), "p: F, q: T, r: T"),
    ),
    answer=5,
    judge=lambda row: value("(p ∧ q) ∨ r", p=row[0], q=row[1], r=row[2]) != value("p ∧ (q ∨ r)", p=row[0], q=row[1], r=row[2]),
    solution="""
<p>p: F, q: T, r: T를 넣으면 왼쪽은 (F ∧ T) ∨ T = F ∨ T = T이고, 오른쪽은 F ∧ (T ∨ T) = F ∧ T = F입니다. 값이 다르므로 이 한 경우만으로 두 식이 동치가 아님을 보일 수 있습니다.</p>
<p>어느 경우에 다른지 정리해 둡니다. p가 T이면 두 식 모두 q ∨ r과 값이 같아서 늘 같습니다. p가 F이면 왼쪽은 r, 오른쪽은 F이므로 r이 T일 때만 다릅니다. 결합법칙은 같은 연산자가 이어질 때만 쓸 수 있고, ∧와 ∨가 섞이면 괄호를 옮길 수 없습니다.</p>
""",
    layout=Layout.MEDIUM,
)


SECTION_B: Section = Section(
    title="2. 논리적 동치",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_13, ITEM_14, ITEM_15, ITEM_16, ITEM_17, ITEM_18, ITEM_19, ITEM_20, ITEM_21, ITEM_22),
    checks=(
        ("문제 17의 모든 줄이 앞 줄과 동치", lambda: chain_holds(ITEM_17_START, ITEM_17_LINES)),
        ("문제 17의 (가)에 맞는 법칙은 항등법칙 하나", lambda: laws_that_apply(ITEM_17_START, ITEM_17_LINES[0].formula) == ["항등법칙"]),
        ("문제 18 해설의 유도: 줄마다 동치", lambda: chain_holds(ITEM_18_START, ITEM_18_STEPS)),
        ("문제 18 해설의 유도: 부정법칙, 항등법칙 줄의 이름", lambda: law_applies("부정법칙", "p ∧ (q ∨ ¬q)", "p ∧ T") and law_applies("항등법칙", "p ∧ T", "p")),
        ("문제 18 해설의 유도: 분배법칙 줄의 이름", lambda: law_applies("분배법칙", ITEM_18_START, "p ∧ (q ∨ ¬q)")),
        ("문제 19 해설의 유도: 줄마다 동치", lambda: chain_holds(ITEM_19_START, ITEM_19_STEPS)),
        ("문제 19 해설의 유도: 함축법칙, 이중 부정법칙 줄의 이름", lambda: law_applies("함축법칙", ITEM_19_START, ITEM_19_STEPS[0].formula) and law_applies("이중 부정법칙", ITEM_19_STEPS[0].formula, ITEM_19_STEPS[1].formula)),
        ("문제 19 해설의 유도: 분배, 부정, 항등법칙 줄의 이름(교환법칙은 적지 않고 씀)", lambda: law_applies_up_to_commutation("분배법칙", ITEM_19_STEPS[1].formula, ITEM_19_STEPS[2].formula) and law_applies_up_to_commutation("부정법칙", ITEM_19_STEPS[2].formula, ITEM_19_STEPS[3].formula) and law_applies_up_to_commutation("항등법칙", ITEM_19_STEPS[3].formula, ITEM_19_STEPS[4].formula)),
        ("문제 21 해설의 유도: 줄마다 동치", lambda: chain_holds(ITEM_21_START, ITEM_21_STEPS)),
        ("문제 21 해설의 유도: 결합법칙, 드모르간, 함축법칙 줄의 이름", lambda: law_applies("결합법칙", ITEM_21_STEPS[0].formula, ITEM_21_STEPS[1].formula) and law_applies("드모르간의 법칙", ITEM_21_STEPS[1].formula, ITEM_21_STEPS[2].formula) and law_applies("함축법칙", ITEM_21_STEPS[2].formula, ITEM_21_STEPS[3].formula)),
        ("문제 21 해설의 유도: 함축법칙 두 번", lambda: law_applies("함축법칙", ITEM_21_START, "p → (¬q ∨ r)") and law_applies("함축법칙", "p → (¬q ∨ r)", ITEM_21_STEPS[0].formula)),
        ("문제 16 해설: 원래 식과 쌍대의 동치", lambda: equivalent(ITEM_16_SOURCE, "p ∨ q") and equivalent("p ∧ (q ∨ F)", "p ∧ q")),
        ("문제 14 해설: ¬p ∨ q ≡ p → q", lambda: equivalent("¬p ∨ q", "p → q")),
    ),
)
