"""1장 시제품의 정리와 보조정리 진술을 작은 경우 전부로 확인한다.

- 보조정리 (쌍대와 부정): 변수 p, q, r과 T, F에 ¬, ∧, ∨를 두 겹까지 붙인 모든 식 A에 대해
  ¬A ≡ (A의 쌍대에서 변수마다 ¬를 붙인 식)
- 정리 (쌍대 원리): 같은 범위의 식 가운데 서로 동치인 모든 짝 A ≡ B에 대해 A의 쌍대 ≡ B의 쌍대
- 표 1-10의 한 줄에 놓인 두 식이 서로 쌍대인지
- 정리 (정당한 추론과 항진명제): 변수 둘의 진리함수 16가지로 만든, 전제 두 개 이하의 모든 추론에서
  "전제가 모두 참인 모든 경우에 결론이 참" ⟺ "(전제들의 논리곱) → 결론이 항진명제"
- 정리 (논리적 추론 법칙)의 증명 표: 법칙마다 전제가 모두 참인 경우와 그때의 결론 값
- 가설적 삼단논법의 경우 나누기 증명
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import product
from typing import Callable

VARIABLES: tuple[str, ...] = ("p", "q", "r")


@dataclass(frozen=True)
class Formula:
    """¬, ∧, ∨, T, F와 변수로 만든 식. kind는 var, T, F, not, and, or 가운데 하나."""

    kind: str
    name: str = ""
    left: Formula | None = None
    right: Formula | None = None

    def evaluate(self, assignment: dict[str, bool]) -> bool:
        if self.kind == "var":
            return assignment[self.name]
        if self.kind == "T":
            return True
        if self.kind == "F":
            return False
        if self.kind == "not":
            return not self.left.evaluate(assignment)
        if self.kind == "and":
            return self.left.evaluate(assignment) and self.right.evaluate(assignment)
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def dual(self) -> Formula:
        """∧와 ∨, T와 F를 모두 맞바꾼 식."""
        swapped_kind: dict[str, str] = {"and": "or", "or": "and", "T": "F", "F": "T"}
        kind: str = swapped_kind.get(self.kind, self.kind)
        left: Formula | None = self.left.dual() if self.left is not None else None
        right: Formula | None = self.right.dual() if self.right is not None else None
        return Formula(kind, self.name, left, right)

    def with_negated_variables(self) -> Formula:
        """변수 p 자리마다 ¬p를 넣은 식."""
        if self.kind == "var":
            return Formula("not", left=self)
        left: Formula | None = self.left.with_negated_variables() if self.left is not None else None
        right: Formula | None = self.right.with_negated_variables() if self.right is not None else None
        return Formula(self.kind, self.name, left, right)


def all_assignments() -> list[dict[str, bool]]:
    assignments: list[dict[str, bool]] = [dict(zip(VARIABLES, values)) for values in product((True, False), repeat=len(VARIABLES))]
    return assignments


def truth_column(formula: Formula, assignments: list[dict[str, bool]]) -> tuple[bool, ...]:
    return tuple(formula.evaluate(assignment) for assignment in assignments)


def formulas_up_to_depth(depth: int) -> list[Formula]:
    atoms: list[Formula] = [Formula("var", name) for name in VARIABLES] + [Formula("T"), Formula("F")]
    built: list[Formula] = list(atoms)
    for _ in range(depth):
        previous: list[Formula] = built
        built = list(atoms)
        built.extend(Formula("not", left=inner) for inner in previous)
        for left_part, right_part in product(previous, repeat=2):
            built.append(Formula("and", left=left_part, right=right_part))
            built.append(Formula("or", left=left_part, right=right_part))
    return built


def check_duality(formulas: list[Formula]) -> tuple[int, int, int]:
    """보조정리가 깨지는 식의 수, 쌍대 원리가 깨지는 동치 묶음의 수, 동치 묶음의 수."""
    assignments: list[dict[str, bool]] = all_assignments()
    lemma_failures: int = 0
    duals_by_column: dict[tuple[bool, ...], set[tuple[bool, ...]]] = {}
    for formula in formulas:
        column: tuple[bool, ...] = truth_column(formula, assignments)
        dual_formula: Formula = formula.dual()
        negated_dual_column: tuple[bool, ...] = truth_column(dual_formula.with_negated_variables(), assignments)
        if negated_dual_column != tuple(not value for value in column):
            lemma_failures += 1
        duals_by_column.setdefault(column, set()).add(truth_column(dual_formula, assignments))
    principle_failures: int = sum(1 for dual_columns in duals_by_column.values() if len(dual_columns) != 1)
    return lemma_failures, principle_failures, len(duals_by_column)


def var(name: str) -> Formula:
    return Formula("var", name)


def neg(inner: Formula) -> Formula:
    return Formula("not", left=inner)


def conj(left_part: Formula, right_part: Formula) -> Formula:
    return Formula("and", left=left_part, right=right_part)


def disj(left_part: Formula, right_part: Formula) -> Formula:
    return Formula("or", left=left_part, right=right_part)


def check_law_pairs_are_duals() -> list[str]:
    """표 1-10에서 한 줄의 왼쪽 식(양변)의 쌍대가 오른쪽 식(양변)과 같은지."""
    p: Formula = var("p")
    q: Formula = var("q")
    r: Formula = var("r")
    true: Formula = Formula("T")
    false: Formula = Formula("F")
    rows: dict[str, tuple[tuple[Formula, Formula], tuple[Formula, Formula]]] = {
        "항등": ((conj(p, true), p), (disj(p, false), p)),
        "지배": ((conj(p, false), false), (disj(p, true), true)),
        "부정": ((conj(p, neg(p)), false), (disj(p, neg(p)), true)),
        "멱등": ((conj(p, p), p), (disj(p, p), p)),
        "교환": ((conj(p, q), conj(q, p)), (disj(p, q), disj(q, p))),
        "결합": ((conj(conj(p, q), r), conj(p, conj(q, r))), (disj(disj(p, q), r), disj(p, disj(q, r)))),
        "분배": ((disj(p, conj(q, r)), conj(disj(p, q), disj(p, r))), (conj(p, disj(q, r)), disj(conj(p, q), conj(p, r)))),
        "드모르간": ((neg(conj(p, q)), disj(neg(p), neg(q))), (neg(disj(p, q)), conj(neg(p), neg(q)))),
        "흡수": ((conj(p, disj(p, q)), p), (disj(p, conj(p, q)), p)),
    }
    mismatches: list[str] = []
    for law, ((left_side, right_side), (dual_left, dual_right)) in rows.items():
        if left_side.dual() != dual_left or right_side.dual() != dual_right:
            mismatches.append(law)
    return mismatches


TruthFunction = tuple[bool, bool, bool, bool]
ROWS_TWO: list[tuple[bool, bool]] = [(True, True), (True, False), (False, True), (False, False)]


def check_validity_theorem() -> tuple[int, int]:
    """(확인한 추론 수, 두 판정이 어긋난 수)"""
    functions: list[TruthFunction] = list(product((True, False), repeat=4))
    premise_sets: list[tuple[TruthFunction, ...]] = [()]
    premise_sets.extend((single,) for single in functions)
    premise_sets.extend(product(functions, repeat=2))
    checked: int = 0
    disagreements: int = 0
    for premises in premise_sets:
        for conclusion in functions:
            valid: bool = all(conclusion[row] for row in range(4) if all(premise[row] for premise in premises))
            tautology: bool = all((not all(premise[row] for premise in premises)) or conclusion[row] for row in range(4))
            checked += 1
            if valid != tautology:
                disagreements += 1
    return checked, disagreements


def implies(antecedent: bool, consequent: bool) -> bool:
    return (not antecedent) or consequent


InferenceRule = tuple[list[Callable[[bool, bool], bool]], Callable[[bool, bool], bool]]

INFERENCE_RULES: dict[str, InferenceRule] = {
    "논리곱 p, q ∴ p ∧ q": ([lambda p, q: p, lambda p, q: q], lambda p, q: p and q),
    "선언적 부가 p ∴ p ∨ q": ([lambda p, q: p], lambda p, q: p or q),
    "단순화 p ∧ q ∴ p": ([lambda p, q: p and q], lambda p, q: p),
    "단순화 p ∧ q ∴ q": ([lambda p, q: p and q], lambda p, q: q),
    "긍정논법 p, p → q ∴ q": ([lambda p, q: p, lambda p, q: implies(p, q)], lambda p, q: q),
    "부정논법 ¬q, p → q ∴ ¬p": ([lambda p, q: not q, lambda p, q: implies(p, q)], lambda p, q: not p),
    "선언적 삼단논법 p ∨ q, ¬p ∴ q": ([lambda p, q: p or q, lambda p, q: not p], lambda p, q: q),
}


def letter(value: bool) -> str:
    return "T" if value else "F"


def report_inference_rules() -> int:
    failures: int = 0
    for name, (premises, conclusion) in INFERENCE_RULES.items():
        supporting_rows: list[tuple[bool, bool]] = [row for row in ROWS_TWO if all(premise(*row) for premise in premises)]
        described: str = ", ".join(f"(p, q) = ({letter(p)}, {letter(q)}) → 결론 {letter(conclusion(p, q))}" for p, q in supporting_rows)
        print(f"  {name}: {described}")
        if not all(conclusion(*row) for row in supporting_rows):
            failures += 1
    return failures


def check_hypothetical_syllogism_cases() -> bool:
    """p가 F이면 p → r이 바로 참, p가 T이면 두 전제에서 q, r이 차례로 참."""
    for p, q, r in product((True, False), repeat=3):
        if not (implies(p, q) and implies(q, r)):
            continue
        if not p and not implies(p, r):
            return False
        if p and not (q and r):
            return False
    return True


def main() -> int:
    formulas: list[Formula] = formulas_up_to_depth(2)
    lemma_failures, principle_failures, groups = check_duality(formulas)
    print(f"쌍대 보조정리: 식 {len(formulas)}개 가운데 깨지는 식 {lemma_failures}개")
    print(f"쌍대 원리: 동치 묶음 {groups}개 가운데 쌍대끼리 동치가 아닌 묶음 {principle_failures}개")
    mismatched_laws: list[str] = check_law_pairs_are_duals()
    print("표 1-10 한 줄의 두 식이 서로 쌍대:", "모두 그렇다" if not mismatched_laws else f"아닌 줄 {mismatched_laws}")
    checked, disagreements = check_validity_theorem()
    print(f"정당한 추론과 항진명제: 추론 {checked}개 가운데 두 판정이 어긋난 것 {disagreements}개")
    print("추론 법칙 증명 표 (전제가 모두 참인 경우와 그때의 결론):")
    rule_failures: int = report_inference_rules()
    syllogism_holds: bool = check_hypothetical_syllogism_cases()
    print("가설적 삼단논법 경우 나누기:", syllogism_holds)
    problems: int = lemma_failures + principle_failures + len(mismatched_laws) + disagreements + rule_failures + (0 if syllogism_holds else 1)
    print("문제:", problems)
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
