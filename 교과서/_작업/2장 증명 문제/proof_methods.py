"""교과서 2장의 증명법이 p → q를 보이려고 무엇을 놓고 무엇을 보이는지, 그리고 역, 이, 대우의 이름.

증명법의 출발점은 정의로 정해진 것이라 계산으로 고를 수 없다. 대신 각 증명법이 실제로 보이는 명제가
p → q와 동치라는 점은 METHOD_CHECKS에서 진리표로 확인한다.
"""

from __future__ import annotations

from logic_tools import equivalent, parse

from logic_check import IMPLIES, Connective, Formula, Negation  # noqa: E402  logic_tools가 스킬 폴더를 경로에 넣은 뒤에만 불러올 수 있다

# 증명법마다 처음 참이라고 놓는 것
START: dict[str, str] = {
    "직접증명법": "p",
    "대우증명법": "¬q",
    "모순증명법": "p ∧ ¬q",
}

# 증명법마다 실제로 보이는 명제. 모두 p → q와 동치여야 한다.
SHOWS: dict[str, str] = {
    "직접증명법": "p → q",
    "대우증명법": "¬q → ¬p",
    "모순증명법": "¬(p ∧ ¬q)",
}

METHOD_CHECKS: tuple[tuple[str, bool], ...] = tuple(
    (f"{method}이 보이는 {shown}은 p → q와 동치", equivalent(shown, "p → q")) for method, shown in SHOWS.items()
)

# 교과서 3-3과 4절이 정한 원칙. 문항에서 이 원칙에 어긋나는 주장을 판정할 때 쓴다.
EXAMPLES_PROVE_FOR_ALL: bool = False  # 예를 아무리 많이 들어도 ∀가 참이라는 증명은 되지 않는다
ONE_COUNTEREXAMPLE_REFUTES_FOR_ALL: bool = True  # ∀가 붙은 명제는 반례 하나로 거짓이다
INDUCTION_HYPOTHESIS_IS_LEGITIMATE: bool = True  # 귀납 가정에서 P(k)를 가정하는 것은 정해진 단계다

# 교과서 표 2-2: 예 하나로 판정하는 두 방법이 보이는 것
EXAMPLE_METHOD_SHOWS: dict[str, str] = {
    "반례증명법": "∀x P(x)가 거짓",
    "존재증명법": "∃x P(x)가 참",
}


def relative_name(original: str, other: str) -> str:
    """other가 함축명제 original의 역, 이, 대우 가운데 무엇인지. 셋 다 아니면 빈 글자."""
    implication: Connective = parse(original)
    condition: Formula = implication.left
    conclusion: Formula = implication.right
    relatives: dict[str, Formula] = {
        "역": Connective(IMPLIES, conclusion, condition),
        "이": Connective(IMPLIES, Negation(condition), Negation(conclusion)),
        "대우": Connective(IMPLIES, Negation(conclusion), Negation(condition)),
    }
    target: Formula = parse(other)
    return next((name for name, relative in relatives.items() if relative == target), "")
