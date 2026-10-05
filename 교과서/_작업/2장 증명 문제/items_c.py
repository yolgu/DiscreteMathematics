"""묶음 3 모순증명법: 핵심 정리, 보기 3, 문제 16~20."""

from __future__ import annotations

from expr_tools import same_polynomial
from fragments import CalcStep, Calculation, Step, chain_holds, computed_truth_table, derivation_html, laws_named_correctly
from logic_tools import entails, equivalent, is_contradiction, law_applies
from model import Demand, Item, Layout, Option, Section, WorkedExample, formula_option
from number_tools import holds_on_residues, is_even, is_odd

SUMMARY: str = """
<ul>
  <li><strong>근거가 되는 동치</strong>: p → q ≡ ¬(p ∧ ¬q)입니다. 함축법칙, 이중 부정법칙, 드모르간의 법칙을 차례로 써서 얻습니다.</li>
  <li><strong>p ∧ ¬q의 뜻</strong>: p가 참이고 q가 거짓인 경우, 곧 p → q가 거짓이 되는 유일한 경우입니다.</li>
  <li><strong>모순증명법</strong>(귀류법): p ∧ ¬q가 참이라고 가정하고, 어떤 명제 r과 그 부정 ¬r이 함께 참이라는 결과, 곧 모순명제 r ∧ ¬r을 이끌어 냅니다. 모순명제는 참일 수 없으므로 p ∧ ¬q는 거짓이고, ¬(p ∧ ¬q), 곧 p → q가 참입니다.</li>
</ul>
"""

WORKED_CALCULATION: Calculation = Calculation(
    first="(2*a + 1) + (2*b + 1)",
    first_latex="m + n",
    steps=(
        CalcStep("(2*a + 1) + (2*b + 1)", r"\(m = 2a + 1\), \(n = 2b + 1\)을 넣음"),
        CalcStep("2*a + 2*b + 2", "괄호를 풂"),
        CalcStep("2*(a + b + 1)", "2를 묶어 냄"),
    ),
)


def _worked_check() -> bool:
    statement_holds: bool = all(
        holds_on_residues(lambda n, m=m: not is_odd(m + n) or is_even(m) or is_even(n), 2) for m in range(2)
    )
    return WORKED_CALCULATION.holds() and statement_holds and equivalent("¬(p ∧ ¬q)", "p → q")


WORKED: WorkedExample = WorkedExample(
    title="보기 3 모순증명법으로 증명하기",
    body=rf"""
<p>두 정수 \(m\), \(n\)에 대해 \(m + n\)이 홀수이면 \(m\)과 \(n\) 가운데 적어도 하나는 짝수임을 모순증명법으로 증명하세요.</p>
<p class="solution-label">풀이</p>
<p>p: \(m + n\)은 홀수이다, q: \(m\)과 \(n\) 가운데 적어도 하나는 짝수이다로 놓습니다. 드모르간의 법칙에 따라 ¬q는 '\(m\)과 \(n\)은 모두 홀수이다'입니다.</p>
<p>p ∧ ¬q, 곧 '\(m + n\)은 홀수이고 \(m\)과 \(n\)은 모두 홀수이다'가 참이라고 가정합니다. ¬q에 따라 \(m = 2a + 1\), \(n = 2b + 1\ (a, b \in Z)\)로 쓸 수 있습니다.</p>
{WORKED_CALCULATION.html()}
<p>\(a + b + 1\)은 정수이므로 \(m + n\)은 짝수, 곧 ¬p가 참입니다. 그런데 가정에 따르면 p도 참이므로 p ∧ ¬p가 참이어야 합니다. p ∧ ¬p는 모순명제라 참일 수 없습니다. 따라서 p ∧ ¬q는 거짓이고 ¬(p ∧ ¬q)가 참입니다.</p>
<p>∴ 이와 동치인 p → q가 참입니다. Q.E.D.</p>
<p>이 증명에서 부딪친 것은 q와 ¬q가 아니라 가정에 든 p와 계산으로 얻은 ¬p입니다. 어떤 명제와 그 부정이 함께 참이 되면, 그것이 무엇이든 모순입니다.</p>
""",
    check=_worked_check,
)

ITEM_16_STEPS: tuple[Step, ...] = (
    Step("¬p ∨ q", "함축법칙"),
    Step("¬p ∨ ¬(¬q)", "이중 부정법칙", label="(가)"),
    Step("¬(p ∧ ¬q)", "드모르간의 법칙"),
)

ITEM_16: Item[str] = Item(
    number=16,
    demand=Demand.FOUNDATION,
    stem=f"<p>p → q ≡ ¬(p ∧ ¬q)를 보이는 유도입니다. (가)에 알맞은 식을 고르세요.</p>{derivation_html('p → q', ITEM_16_STEPS, hidden='(가)')}",
    options=(
        formula_option("¬p ∨ ¬q", "q에 ¬를 하나만 붙여 뜻이 바뀌었습니다. 이중 부정법칙은 q를 ¬(¬q)로 바꾸는 것이고, ¬ 하나만 붙이면 q의 부정이 됩니다."),
        formula_option("¬(¬p) ∨ q", "¬ 둘을 q가 아니라 p 쪽에 붙이려다 ¬를 하나만 더했습니다. ¬(¬p) ∨ q는 p ∨ q와 같아 p → q와 다른 명제입니다. 다음 줄에서 드모르간의 법칙으로 ¬(p ∧ ¬q)를 만들려면 q 쪽이 ¬( ) 꼴이어야 합니다."),
        formula_option("¬p ∧ ¬(¬q)", "∨를 ∧로 미리 바꾸었습니다. 이중 부정법칙은 ¬(¬q)를 넣기만 하고 연결사는 그대로 둡니다. ∨가 ∧로 바뀌는 것은 다음 줄에서 드모르간의 법칙으로 ¬를 밖으로 꺼낼 때입니다."),
        formula_option("p ∧ ¬q", "마지막 줄의 괄호 안만 옮겨 적었습니다. p ∧ ¬q는 p → q가 거짓인 경우에만 참이라 p → q의 부정입니다. 바깥의 ¬가 빠지면 뜻이 정반대가 됩니다."),
        formula_option("¬p ∨ ¬(¬q)"),
    ),
    answer=5,
    judge=lambda formula: law_applies("이중 부정법칙", "¬p ∨ q", formula) and law_applies("드모르간의 법칙", formula, "¬(p ∧ ¬q)"),
    solution=f"""
<p>이중 부정법칙은 어떤 명제를 두 번 부정해도 뜻이 같다는 법칙입니다. ¬p ∨ q의 q를 ¬(¬q)로 바꾸면 ¬p ∨ ¬(¬q)가 됩니다.</p>
{derivation_html('p → q', ITEM_16_STEPS)}
<p>이렇게 바꾸는 까닭은 다음 줄 때문입니다. ∨의 양쪽이 모두 ¬로 시작하면 드모르간의 법칙 ¬A ∨ ¬B ≡ ¬(A ∧ B)를 A = p, B = ¬q로 써서 ¬를 밖으로 꺼낼 수 있고, 그 결과가 ¬(p ∧ ¬q)입니다.</p>
""",
    layout=Layout.SHORT,
)


def _case_option(condition: str, text: str, why_wrong: str = "") -> Option[str]:
    return Option(condition, text, why_wrong)


ITEM_17: Item[str] = Item(
    number=17,
    demand=Demand.FOUNDATION,
    stem="<p>모순증명법은 p → q를 증명하려고, 어떤 경우가 일어날 수 없음을 보입니다. 그 경우를 고르세요.</p>",
    options=(
        _case_option("p ∧ q", "p도 참이고 q도 참인 경우", "이 경우 p → q는 T → T로 참입니다. 이 경우가 일어나도 p → q는 깨지지 않습니다."),
        _case_option("p ∧ ¬q", "p는 참이고 q는 거짓인 경우"),
        _case_option("¬p ∧ q", "p는 거짓이고 q는 참인 경우", "F → T는 참입니다. 이 경우는 오히려 역 q → p를 깨는 경우입니다."),
        _case_option("¬p ∧ ¬q", "p도 거짓이고 q도 거짓인 경우", "F → F는 참입니다. 함축은 조건이 거짓이면 늘 참입니다."),
        _case_option("¬q", "q가 거짓인 경우(p는 무엇이든)", "q가 거짓이어도 p까지 거짓이면 F → F로 p → q는 참입니다. 일어날 수 없음을 보일 것은 ¬q만이 아니라 'p가 참인데 q가 거짓', 곧 p ∧ ¬q입니다."),
    ),
    answer=2,
    judge=lambda condition: equivalent(condition, "¬(p → q)"),
    solution=f"""
<p>p → q가 거짓이 되는 경우만 일어나지 않으면 p → q는 참입니다. 진리표에서 확인합니다.</p>
{computed_truth_table(["p", "q"], ["¬q", "p ∧ ¬q", "¬(p ∧ ¬q)", "p → q"])}
<p>p → q가 거짓인 줄은 p가 T, q가 F인 둘째 줄 하나뿐이고, p ∧ ¬q가 참인 줄도 이 줄 하나뿐입니다. 그래서 p ∧ ¬q가 일어날 수 없음을 보이면, 곧 ¬(p ∧ ¬q)를 보이면 p → q가 참입니다. 비와 우산으로 옮기면 '비가 오는데 우산을 챙기지 않은 경우'가 없다는 것을 보이는 셈입니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_18: Item[str] = Item(
    number=18,
    demand=Demand.FOUNDATION,
    stem=r"<p>명제 '정수 \(n\)에 대해 \(n^2\)이 홀수이면 \(n\)은 홀수이다'를 모순증명법으로 증명하려고 합니다. 처음에 참이라고 가정할 것을 고르세요.</p>",
    options=(
        Option("¬q", r"\(n\)은 짝수이다.", "결론의 부정 ¬q만 놓는 것은 대우증명법의 출발점입니다. 모순증명법은 가정 p와 결론의 부정 ¬q를 함께, 곧 p ∧ ¬q를 가정합니다."),
        Option("p ∧ q", r"\(n^2\)은 홀수이고 \(n\)도 홀수이다.", r"명제가 성립할 때의 모습을 가정했습니다. 이 경우는 \(n = 1\)처럼 실제로 일어날 수 있으므로, 여기서는 모순이 나오지 않습니다."),
        Option("¬p ∧ q", r"\(n^2\)은 짝수이고 \(n\)은 홀수이다.", "부정을 결론이 아니라 가정 쪽에 붙였습니다. 이 경우가 일어날 수 없음을 보이면 ¬(¬p ∧ q), 곧 역 q → p를 증명하게 됩니다."),
        Option("p ∧ ¬q", r"\(n^2\)은 홀수이고 \(n\)은 짝수이다."),
        Option("p → ¬q", r"\(n^2\)이 홀수이면 \(n\)은 짝수이다.", "모순증명법은 '가정은 참인데 결론은 거짓'인 상황 하나를 가정합니다. p → ¬q는 그런 상황이 아니라 또 다른 함축명제입니다."),
    ),
    answer=4,
    judge=lambda formula: equivalent(formula, "p ∧ ¬q"),
    solution=r"""
<p>p: \(n^2\)은 홀수이다, q: \(n\)은 홀수이다로 놓습니다. 모순증명법은 p → q가 거짓이 되는 유일한 경우 p ∧ ¬q를 가정하고 모순을 이끌어 냅니다. ¬q는 '\(n\)은 홀수가 아니다', 곧 '\(n\)은 짝수이다'이므로 가정할 것은 '\(n^2\)은 홀수이고 \(n\)은 짝수이다'입니다.</p>
<p>이어서 \(n = 2k\ (k \in Z)\)로 놓으면 \(n^2 = 4k^2 = 2(2k^2)\)이 짝수가 되어, 가정에 든 '\(n^2\)은 홀수'와 부딪칩니다.</p>
""",
    layout=Layout.MEDIUM,
)

ITEM_19_FACT: str = "(p ∧ ¬q) → (q ∧ ¬q)"

ITEM_19: Item[str] = Item(
    number=19,
    demand=Demand.FOUNDATION,
    stem=f"<p>p ∧ ¬q를 가정했더니 모순명제 q ∧ ¬q에 이르렀습니다. 곧 {ITEM_19_FACT}가 참입니다. 이것으로부터 참이라고 결론 내릴 수 있는 명제를 고르세요.</p>",
    options=(
        formula_option("q", "증명 중간에 p에서 q를 이끌어 냈다고 q가 무조건 참인 것은 아닙니다. p와 q가 모두 거짓이면 p ∧ ¬q가 거짓이라 주어진 함축은 참인데, q는 거짓입니다."),
        formula_option("q → p", "역입니다. p가 거짓이고 q가 참이면 주어진 함축은 참인데 q → p는 거짓입니다."),
        formula_option("¬p", "p ∧ ¬q가 거짓이라는 것은 p와 ¬q가 함께 참일 수 없다는 뜻일 뿐, p가 거짓이라는 뜻은 아닙니다. p와 q가 모두 참이어도 주어진 함축은 참입니다."),
        formula_option("p ∧ ¬q", "처음에 가정했던 것 자체입니다. 이 가정이 모순에 이르렀으므로 오히려 p ∧ ¬q는 거짓입니다."),
        formula_option("p → q"),
    ),
    answer=5,
    judge=lambda formula: entails([ITEM_19_FACT], formula),
    solution=f"""
<p>모순명제 q ∧ ¬q는 늘 거짓입니다. 함축은 앞이 참이고 뒤가 거짓일 때만 거짓이므로, {ITEM_19_FACT}가 참이려면 앞의 p ∧ ¬q가 거짓이어야 합니다. 따라서 ¬(p ∧ ¬q)가 참이고, 이와 동치인 p → q가 참입니다.</p>
{computed_truth_table(["p", "q"], ["p ∧ ¬q", ITEM_19_FACT, "p → q"])}
<p>진리표에서도 주어진 함축과 p → q의 열이 같습니다.</p>
""",
    layout=Layout.SHORT,
)

Clash = tuple[str, str]

# 문제 20의 명제: s는 'm + n은 짝수이다', a는 'm은 홀수이다', b는 'n은 홀수이다'
ITEM_20_STATEMENTS_IN_PROOF: frozenset[str] = frozenset({"s", "a", "¬b", "¬s"})


def _clash_option(clash: Clash, text: str, why_wrong: str = "") -> Option[Clash]:
    return Option(clash, text, why_wrong)


def _is_clash_in_proof(clash: Clash) -> bool:
    first, second = clash
    return is_contradiction(f"({first}) ∧ ({second})") and {first, second} <= ITEM_20_STATEMENTS_IN_PROOF


ITEM_20: Item[Clash] = Item(
    number=20,
    demand=Demand.VARIATION,
    stem=r"""<p>다음은 '두 정수 \(m\), \(n\)에 대해 \(m + n\)이 짝수이고 \(m\)이 홀수이면 \(n\)은 홀수이다'를 모순증명법으로 증명한 것입니다. 이 증명에서 함께 참일 수 없어 부딪친 두 명제를 고르세요.</p>
<p class="quote">\(m + n\)은 짝수이고 \(m\)은 홀수이며 \(n\)은 짝수라고 가정한다. \(m = 2a + 1\), \(n = 2b\ (a, b \in Z)\)로 쓰면 \(m + n = 2(a + b) + 1\)이고, \(a + b\)는 정수이므로 \(m + n\)은 홀수이다. 이것은 가정과 모순이다. 따라서 처음의 가정은 거짓이고, 주어진 명제는 참이다.</p>""",
    options=(
        _clash_option(("b", "¬b"), r"'\(n\)은 홀수이다'와 '\(n\)은 짝수이다'", r"모순이 늘 q ∧ ¬q 꼴이라고 생각하면 고르기 쉽습니다. 그런데 이 증명은 '\(n\)은 홀수'를 이끌어 낸 적이 없습니다."),
        _clash_option(("a", "¬a"), r"'\(m\)은 홀수이다'와 '\(m\)은 짝수이다'", r"'\(m\)은 짝수이다'는 가정에도 계산 결과에도 나오지 않습니다."),
        _clash_option(("s", "¬s"), r"'\(m + n\)은 짝수이다'와 '\(m + n\)은 홀수이다'"),
        _clash_option(("s", "¬b"), r"'\(m + n\)은 짝수이다'와 '\(n\)은 짝수이다'", r"둘 다 가정에 든 명제이고, \(m = 2\), \(n = 4\)처럼 함께 참일 수 있습니다. 서로의 부정이 아니므로 모순이 아닙니다."),
        _clash_option(("a", "¬b"), r"'\(m\)은 홀수이다'와 '\(n\)은 짝수이다'", r"\(m = 1\), \(n = 2\)처럼 함께 참일 수 있습니다. 둘은 가정의 두 부분일 뿐 서로 부딪치지 않습니다."),
    ),
    answer=3,
    judge=_is_clash_in_proof,
    solution=r"""
<p>p: '\(m + n\)은 짝수이고 \(m\)은 홀수이다', q: '\(n\)은 홀수이다'로 놓으면 모순증명법은 p ∧ ¬q, 곧 '\(m + n\)은 짝수, \(m\)은 홀수, \(n\)은 짝수'를 가정합니다.</p>
<p>계산하면 \(m + n = (2a + 1) + 2b = 2(a + b) + 1\)이 홀수입니다. 그런데 가정에는 '\(m + n\)은 짝수이다'가 들어 있습니다. r: '\(m + n\)은 짝수이다'로 놓으면 r과 ¬r이 함께 참이 된 것이므로 모순입니다.</p>
<p>모순은 꼭 결론 q와 그 부정일 필요가 없습니다. 가정에 든 명제와 그 부정이 부딪쳐도 p ∧ ¬q가 거짓이라는 결론은 같습니다.</p>
""",
    layout=Layout.LONG,
)

SECTION_C: Section = Section(
    title="3. 모순증명법",
    summary=SUMMARY,
    worked=WORKED,
    items=(ITEM_16, ITEM_17, ITEM_18, ITEM_19, ITEM_20),
    checks=(
        ("문제 16 해설: 유도의 줄마다 동치이고 적은 법칙이 맞음", lambda: chain_holds("p → q", ITEM_16_STEPS) and laws_named_correctly("p → q", ITEM_16_STEPS)),
        ("문제 18 해설: n = 2k이면 n² = 2(2k²)", lambda: same_polynomial("(2*k)**2", "2*(2*k**2)")),
        ("문제 19 해설: 주어진 함축은 p → q와 동치", lambda: equivalent(ITEM_19_FACT, "p → q")),
        ("문제 20 해설: (2a + 1) + 2b = 2(a + b) + 1, 명제가 모든 정수에서 참", lambda: same_polynomial("(2*a + 1) + 2*b", "2*(a + b) + 1") and all(
            holds_on_residues(lambda n, m=m: not (is_even(m + n) and is_odd(m)) or is_odd(n), 2) for m in range(2)
        )),
        ("문제 20 오답: m = 2, n = 4와 m = 1, n = 2에서 두 명제가 함께 참", lambda: (is_even(2 + 4) and is_even(4)) and (is_odd(1) and is_even(2))),
    ),
)
