"""문항을 판정하는 계산 도구.

명제 논리식은 교과서 스킬의 logic_check.py 파서로 읽는다. 진리표는 모든 줄을 빠짐없이 돌고,
동치 법칙과 추론 법칙은 식의 모양을 법칙의 꼴과 맞대어 확인한다.
"""

from __future__ import annotations

import itertools
import sys
from collections.abc import Callable, Iterator, Mapping, Sequence
from fractions import Fraction
from pathlib import Path

SKILL_SCRIPTS: Path = Path.home() / ".claude" / "skills" / "lecture-to-textbook" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from logic_check import (  # noqa: E402  스킬 폴더를 경로에 넣은 뒤에만 불러올 수 있다
    AND,
    OR,
    Connective,
    Constant,
    Formula,
    Negation,
    Parser,
    Variable,
)

Assignment = Mapping[str, bool]
Binding = dict[str, Formula]


def parse(text: str) -> Formula:
    """교과서처럼 대괄호로 묶은 식도 읽는다."""
    return Parser(text.replace("[", "(").replace("]", ")")).parse()


def all_rows(names: Sequence[str]) -> list[dict[str, bool]]:
    """교과서 진리표 순서: T가 먼저, 앞 변수가 가장 느리게 바뀐다."""
    return [dict(zip(names, values)) for values in itertools.product((True, False), repeat=len(names))]


def variable_names(*formulas: Formula) -> list[str]:
    return sorted(set().union(*(formula.variables() for formula in formulas)))


def value(text: str, **assignment: bool) -> bool:
    return parse(text).evaluate(assignment)


def truth_column(text: str, names: Sequence[str]) -> tuple[bool, ...]:
    formula: Formula = parse(text)
    return tuple(formula.evaluate(row) for row in all_rows(names))


def equivalent(left: str, right: str) -> bool:
    first: Formula = parse(left)
    second: Formula = parse(right)
    return all(first.evaluate(row) == second.evaluate(row) for row in all_rows(variable_names(first, second)))


def is_tautology(text: str) -> bool:
    formula: Formula = parse(text)
    return all(formula.evaluate(row) for row in all_rows(variable_names(formula)))


def is_contradiction(text: str) -> bool:
    formula: Formula = parse(text)
    return not any(formula.evaluate(row) for row in all_rows(variable_names(formula)))


def entails(premises: Sequence[str], conclusion: str) -> bool:
    """전제가 모두 참인 모든 줄에서 결론도 참인가(정당한 추론인가)."""
    parsed_premises: list[Formula] = [parse(text) for text in premises]
    parsed_conclusion: Formula = parse(conclusion)
    names: list[str] = variable_names(*parsed_premises, parsed_conclusion)
    return all(
        parsed_conclusion.evaluate(row)
        for row in all_rows(names)
        if all(premise.evaluate(row) for premise in parsed_premises)
    )


def count_true_rows(text: str, names: Sequence[str]) -> int:
    return sum(truth_column(text, names))


# ---- 식의 모양 맞대기: 법칙의 꼴 속 p, q, r은 아무 식이나 들어갈 수 있는 자리다 ----

def match(pattern: Formula, term: Formula, binding: Binding) -> Binding | None:
    if isinstance(pattern, Variable):
        bound: Formula | None = binding.get(pattern.name)
        if bound is None:
            return {**binding, pattern.name: term}
        return binding if bound == term else None
    if isinstance(pattern, Constant):
        return binding if pattern == term else None
    if isinstance(pattern, Negation):
        return match(pattern.operand, term.operand, binding) if isinstance(term, Negation) else None
    if isinstance(pattern, Connective) and isinstance(term, Connective) and pattern.operator == term.operator:
        left: Binding | None = match(pattern.left, term.left, binding)
        return None if left is None else match(pattern.right, term.right, left)
    return None


def substitute(pattern: Formula, binding: Binding) -> Formula:
    if isinstance(pattern, Variable):
        return binding[pattern.name]
    if isinstance(pattern, Negation):
        return Negation(substitute(pattern.operand, binding))
    if isinstance(pattern, Connective):
        return Connective(pattern.operator, substitute(pattern.left, binding), substitute(pattern.right, binding))
    return pattern


def rewrite_once(term: Formula, lhs: Formula, rhs: Formula) -> set[Formula]:
    """식의 한 자리에서 lhs 꼴을 rhs 꼴로 바꾼 결과를 모두 모은다."""
    results: set[Formula] = set()
    binding: Binding | None = match(lhs, term, {})
    if binding is not None and rhs.variables() <= binding.keys():
        results.add(substitute(rhs, binding))
    if isinstance(term, Negation):
        results |= {Negation(inner) for inner in rewrite_once(term.operand, lhs, rhs)}
    if isinstance(term, Connective):
        results |= {Connective(term.operator, left, term.right) for left in rewrite_once(term.left, lhs, rhs)}
        results |= {Connective(term.operator, term.left, right) for right in rewrite_once(term.right, lhs, rhs)}
    return results


def rewrite_everywhere(term: Formula, lhs: Formula, rhs: Formula) -> Formula:
    """안쪽부터 lhs 꼴이 보이는 자리를 모두 바꾼다. 이중 부정을 두 곳에서 한꺼번에 지우는 줄을 위한 것이다."""
    if isinstance(term, Negation):
        term = Negation(rewrite_everywhere(term.operand, lhs, rhs))
    elif isinstance(term, Connective):
        term = Connective(term.operator, rewrite_everywhere(term.left, lhs, rhs), rewrite_everywhere(term.right, lhs, rhs))
    binding: Binding | None = match(lhs, term, {})
    if binding is not None and rhs.variables() <= binding.keys():
        return substitute(rhs, binding)
    return term


EQUIVALENCE_LAWS: dict[str, tuple[tuple[str, str], ...]] = {
    "항등법칙": (("p ∧ T", "p"), ("p ∨ F", "p")),
    "지배법칙": (("p ∧ F", "F"), ("p ∨ T", "T")),
    "부정법칙": (("p ∧ ¬p", "F"), ("p ∨ ¬p", "T")),
    "이중 부정법칙": (("¬(¬p)", "p"),),
    "멱등법칙": (("p ∧ p", "p"), ("p ∨ p", "p")),
    "교환법칙": (("p ∧ q", "q ∧ p"), ("p ∨ q", "q ∨ p")),
    "결합법칙": (("(p ∧ q) ∧ r", "p ∧ (q ∧ r)"), ("(p ∨ q) ∨ r", "p ∨ (q ∨ r)")),
    "분배법칙": (("p ∨ (q ∧ r)", "(p ∨ q) ∧ (p ∨ r)"), ("p ∧ (q ∨ r)", "(p ∧ q) ∨ (p ∧ r)")),
    "드모르간의 법칙": (("¬(p ∧ q)", "¬p ∨ ¬q"), ("¬(p ∨ q)", "¬p ∧ ¬q")),
    "흡수법칙": (("p ∧ (p ∨ q)", "p"), ("p ∨ (p ∧ q)", "p")),
    "함축법칙": (("p → q", "¬p ∨ q"),),
}


def law_applies(law: str, before: str, after: str) -> bool:
    """before의 한 자리, 또는 같은 꼴이 보이는 모든 자리에 law를 (어느 방향으로든) 써서 after가 되는가."""
    source: Formula = parse(before)
    target: Formula = parse(after)
    for left, right in EQUIVALENCE_LAWS[law]:
        for lhs, rhs in ((parse(left), parse(right)), (parse(right), parse(left))):
            if target in rewrite_once(source, lhs, rhs) or rewrite_everywhere(source, lhs, rhs) == target:
                return True
    return False


def laws_that_apply(before: str, after: str) -> list[str]:
    return [law for law in EQUIVALENCE_LAWS if law_applies(law, before, after)]


def commutation_variants(term: Formula) -> set[Formula]:
    """∧와 ∨의 양쪽을 바꾸어 얻는 모든 모양(바꾸지 않은 모양 포함)."""
    if isinstance(term, Negation):
        return {Negation(inner) for inner in commutation_variants(term.operand)}
    if isinstance(term, Connective):
        variants: set[Formula] = set()
        for left in commutation_variants(term.left):
            for right in commutation_variants(term.right):
                variants.add(Connective(term.operator, left, right))
                if term.operator in (AND, OR):
                    variants.add(Connective(term.operator, right, left))
        return variants
    return {term}


def canonical(term: Formula) -> Formula:
    """∧와 ∨의 양쪽을 글자 순서로 정렬한 모양. 교환법칙만큼의 차이를 지운다."""
    if isinstance(term, Negation):
        return Negation(canonical(term.operand))
    if isinstance(term, Connective):
        left: Formula = canonical(term.left)
        right: Formula = canonical(term.right)
        if term.operator in (AND, OR) and right.parenthesized() < left.parenthesized():
            left, right = right, left
        return Connective(term.operator, left, right)
    return term


def law_applies_up_to_commutation(law: str, before: str, after: str) -> bool:
    """교과서처럼 교환법칙을 따로 적지 않고 law를 쓴 줄인가. 해설 유도의 줄 이름을 확인할 때만 쓴다."""
    target: Formula = canonical(parse(after))
    for source in commutation_variants(parse(before)):
        for left, right in EQUIVALENCE_LAWS[law]:
            for lhs, rhs in ((parse(left), parse(right)), (parse(right), parse(left))):
                results: set[Formula] = rewrite_once(source, lhs, rhs) | {rewrite_everywhere(source, lhs, rhs)}
                if any(canonical(result) == target for result in results):
                    return True
    return False


def dual(formula: Formula) -> Formula:
    """∧와 ∨, T와 F를 모두 맞바꾼 식. ¬, ∧, ∨, T, F만 있는 식에만 쓴다."""
    if isinstance(formula, Constant):
        return Constant(not formula.value)
    if isinstance(formula, Negation):
        return Negation(dual(formula.operand))
    if isinstance(formula, Connective):
        if formula.operator not in (AND, OR):
            raise ValueError(f"쌍대는 ∧와 ∨만 있는 식에서 정의합니다: {formula.parenthesized()}")
        swapped: str = OR if formula.operator == AND else AND
        return Connective(swapped, dual(formula.left), dual(formula.right))
    return formula


INFERENCE_RULES: dict[str, tuple[tuple[tuple[str, ...], str], ...]] = {
    "논리곱": ((("p", "q"), "p ∧ q"),),
    "선언적 부가": ((("p",), "p ∨ q"),),
    "단순화": ((("p ∧ q",), "p"), (("p ∧ q",), "q")),
    "긍정논법": ((("p", "p → q"), "q"),),
    "부정논법": ((("¬q", "p → q"), "¬p"),),
    # 교과서의 꼴(p ∨ q, ¬p ∴ q)에 교환법칙으로 순서만 바꾼 꼴을 함께 둔다.
    "선언적 삼단논법": ((("p ∨ q", "¬p"), "q"), (("p ∨ q", "¬q"), "p")),
    "가설적 삼단논법": ((("p → q", "q → r"), "p → r"),),
}


def rule_matches(rule: str, premises: Sequence[str], conclusion: str) -> bool:
    """전제(순서 무관)와 결론이 rule의 꼴에 맞는가."""
    parsed_premises: list[Formula] = [parse(text) for text in premises]
    parsed_conclusion: Formula = parse(conclusion)
    for pattern_premises, pattern_conclusion in INFERENCE_RULES[rule]:
        if len(pattern_premises) != len(parsed_premises):
            continue
        patterns: list[Formula] = [parse(text) for text in pattern_premises]
        for ordering in itertools.permutations(parsed_premises):
            binding: Binding | None = {}
            for pattern, premise in zip(patterns, ordering):
                binding = match(pattern, premise, binding) if binding is not None else None
            if binding is not None and match(parse(pattern_conclusion), parsed_conclusion, binding) is not None:
                return True
    return False


# ---- T를 1, F를 0으로, ∧를 곱하기, ∨를 더하기로 옮긴 산수 ----

def arithmetic(formula: Formula, numbers: Mapping[str, int]) -> int:
    if isinstance(formula, Constant):
        return 1 if formula.value else 0
    if isinstance(formula, Variable):
        return numbers[formula.name]
    if isinstance(formula, Connective) and formula.operator == AND:
        return arithmetic(formula.left, numbers) * arithmetic(formula.right, numbers)
    if isinstance(formula, Connective) and formula.operator == OR:
        return arithmetic(formula.left, numbers) + arithmetic(formula.right, numbers)
    raise ValueError(f"곱하기와 더하기로 옮길 수 없는 식입니다: {formula.parenthesized()}")


def arithmetic_holds(left: str, right: str) -> bool:
    first: Formula = parse(left)
    second: Formula = parse(right)
    names: list[str] = variable_names(first, second)
    return all(
        arithmetic(first, dict(zip(names, values))) == arithmetic(second, dict(zip(names, values)))
        for values in itertools.product((0, 1), repeat=len(names))
    )


# ---- 한정자: 유한 논의영역은 원소를 모두 돌고, 술어 P, Q는 가능한 모든 해석을 돈다 ----

Predicate = Callable[[int], bool]
QuantifiedClaim = Callable[[Sequence[int], Predicate, Predicate], bool]


def interpretations(max_size: int) -> Iterator[tuple[list[int], Predicate, Predicate]]:
    """원소가 1개부터 max_size개인 논의영역과, 그 위의 술어 P, Q의 모든 진릿값 배정."""
    for size in range(1, max_size + 1):
        domain: list[int] = list(range(size))
        for p_values in itertools.product((True, False), repeat=size):
            for q_values in itertools.product((True, False), repeat=size):
                yield domain, (lambda x, table=p_values: table[x]), (lambda x, table=q_values: table[x])


def same_in_every_interpretation(first: QuantifiedClaim, second: QuantifiedClaim, max_size: int = 4) -> bool:
    return all(first(domain, p, q) == second(domain, p, q) for domain, p, q in interpretations(max_size))


def rational_grid(low: int, high: int, steps_per_unit: int) -> list[Fraction]:
    """실수 문항의 보조 확인용 유리수 격자점. 격자에서 반례가 없다는 것은 증명이 아니라 보조 근거다."""
    return [Fraction(n, steps_per_unit) for n in range(low * steps_per_unit, high * steps_per_unit + 1)]


def is_prime(number: int) -> bool:
    return number > 1 and all(number % divisor for divisor in range(2, number))
