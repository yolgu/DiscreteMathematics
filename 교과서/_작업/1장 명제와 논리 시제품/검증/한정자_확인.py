"""1장 시제품 3절(변수를 포함한 명제와 한정자)에 싣는 계산과 정리를 다시 확인한다.

- 예제 1-24: P(x, y): x = 2y의 P(1, 2), P(2, 1)
- 예제 1-26: D = {1, 2, 3, 4}, P(x): x^2 < 10의 ∀xP(x), ∃xP(x)
- 범위를 좁힌 한정자: 정수 -10~10에서 ∀x((0 < x ≤ 4) → x^2 < 10), ∃x(0 < x ≤ 4 ∧ x^2 < 10)과
  잘못 쓴 ∀x(0 < x ≤ 4 ∧ x^2 < 10), ∃x(0 < x ≤ 4 → x^2 < 10)
- 정리 (한정자의 부정): 원소 1~4개인 논의영역의 모든 술어에서 ¬∀xP(x) ≡ ∃x¬P(x), ¬∃xP(x) ≡ ∀x¬P(x),
  그리고 원소 네 개일 때 ∀, ∃를 ∧, ∨로 펼친 식
- 정리 (한정자의 순서): 원소 1~3개인 논의영역의 모든 두 변수 술어에서
  ∃y∀xP(x, y)이면 ∀x∃yP(x, y), 거꾸로는 반례가 있음, ∀x∀y ≡ ∀y∀x, ∃x∃y ≡ ∃y∃x
- 예제 (한정자가 둘인 명제의 부정): 같은 범위의 모든 술어에서 ¬∃x∀yP ≡ ∀x∃y¬P, ¬∀x∃yP ≡ ∃x∀y¬P
- 예제 1-27: 실수 x, y, P(x, y): x^2 < y^2. 실수 전체를 다 돌 수 없으므로 논증에 쓰는 식을 여러 유리수 점에서 확인
- 1-1 그림: x + 1 ≥ 2 와 x ≥ 1이 같은 판정
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product


def is_double(x: int, y: int) -> bool:
    return x == 2 * y


def square_below_ten(x: int) -> bool:
    return x * x < 10


def implies(antecedent: bool, consequent: bool) -> bool:
    return (not antecedent) or consequent


def sample_reals() -> list[Fraction]:
    numerators: range = range(-40, 41)
    samples: list[Fraction] = sorted({Fraction(n, d) for n in numerators for d in (1, 2, 3, 7)})
    return samples


def check_quantifier_negation(size: int) -> bool:
    domain: list[int] = list(range(1, size + 1))
    for truth_values in product((False, True), repeat=size):
        predicate: dict[int, bool] = dict(zip(domain, truth_values))
        for_all: bool = all(predicate[x] for x in domain)
        exists: bool = any(predicate[x] for x in domain)
        if (not for_all) != any(not predicate[x] for x in domain):
            return False
        if (not exists) != all(not predicate[x] for x in domain):
            return False
        if size == 4:
            expanded_and: bool = predicate[1] and predicate[2] and predicate[3] and predicate[4]
            expanded_or: bool = predicate[1] or predicate[2] or predicate[3] or predicate[4]
            if for_all != expanded_and or exists != expanded_or:
                return False
    return True


TwoPlacePredicate = dict[tuple[int, int], bool]


def all_two_place_predicates(size: int) -> list[TwoPlacePredicate]:
    domain: list[int] = list(range(size))
    pairs: list[tuple[int, int]] = [(x, y) for x in domain for y in domain]
    predicates: list[TwoPlacePredicate] = [dict(zip(pairs, values)) for values in product((False, True), repeat=len(pairs))]
    return predicates


def check_quantifier_order(size: int) -> tuple[bool, bool, bool, bool, bool]:
    """(∃y∀x → ∀x∃y가 늘 성립, 거꾸로 반례가 있음, ∀∀ 순서 무관, ∃∃ 순서 무관, 둘인 명제의 부정 두 식)"""
    domain: list[int] = list(range(size))
    implication_holds: bool = True
    converse_fails_somewhere: bool = False
    universal_commutes: bool = True
    existential_commutes: bool = True
    nested_negation_holds: bool = True
    for predicate in all_two_place_predicates(size):
        exists_y_all_x: bool = any(all(predicate[(x, y)] for x in domain) for y in domain)
        all_x_exists_y: bool = all(any(predicate[(x, y)] for y in domain) for x in domain)
        exists_x_all_y: bool = any(all(predicate[(x, y)] for y in domain) for x in domain)
        implication_holds = implication_holds and implies(exists_y_all_x, all_x_exists_y)
        converse_fails_somewhere = converse_fails_somewhere or (all_x_exists_y and not exists_y_all_x)
        all_all_xy: bool = all(all(predicate[(x, y)] for y in domain) for x in domain)
        all_all_yx: bool = all(all(predicate[(x, y)] for x in domain) for y in domain)
        some_some_xy: bool = any(any(predicate[(x, y)] for y in domain) for x in domain)
        some_some_yx: bool = any(any(predicate[(x, y)] for x in domain) for y in domain)
        universal_commutes = universal_commutes and all_all_xy == all_all_yx
        existential_commutes = existential_commutes and some_some_xy == some_some_yx
        negated_exists_all: bool = all(any(not predicate[(x, y)] for y in domain) for x in domain)
        negated_all_exists: bool = any(all(not predicate[(x, y)] for y in domain) for x in domain)
        nested_negation_holds = nested_negation_holds and (not exists_x_all_y) == negated_exists_all and (not all_x_exists_y) == negated_all_exists
    return implication_holds, converse_fails_somewhere, universal_commutes, existential_commutes, nested_negation_holds


def main() -> int:
    problems: int = 0
    print("예제 1-24: P(1, 2) =", is_double(1, 2), "/ P(2, 1) =", is_double(2, 1))

    domain: list[int] = [x for x in range(-10, 11) if 0 < x <= 4]
    print("예제 1-26: D =", domain, "/ P(x) 값 =", {x: square_below_ten(x) for x in domain})
    print("  ∀xP(x) =", all(square_below_ten(x) for x in domain), "/ ∃xP(x) =", any(square_below_ten(x) for x in domain))
    print("  반례:", [x for x in domain if not square_below_ten(x)], "/ 예:", [x for x in domain if square_below_ten(x)])

    integers: range = range(-10, 11)
    restricted_for_all: bool = all(implies(0 < x <= 4, x * x < 10) for x in integers)
    restricted_exists: bool = any(0 < x <= 4 and x * x < 10 for x in integers)
    wrong_for_all: bool = all(0 < x <= 4 and x * x < 10 for x in integers)
    wrong_exists: bool = any(implies(0 < x <= 4, x * x < 10) for x in integers)
    wrong_exists_witnesses: list[int] = [x for x in integers if implies(0 < x <= 4, x * x < 10) and not (0 < x <= 4)]
    print("범위를 좁힌 한정자(정수 -10~10): ∀x((0<x≤4) → x²<10) =", restricted_for_all, "/ ∃x(0<x≤4 ∧ x²<10) =", restricted_exists)
    print("  잘못 쓴 ∀x(0<x≤4 ∧ x²<10) =", wrong_for_all, "/ ∃x(0<x≤4 → x²<10) =", wrong_exists, "(범위 밖의 x로 참이 되는 예:", wrong_exists_witnesses[:3], ")")
    if restricted_for_all or not restricted_exists:
        problems += 1

    for size in range(1, 5):
        negation_holds: bool = check_quantifier_negation(size)
        print(f"한정자의 부정(원소 {size}개, 술어 {2 ** size}가지 모두):", negation_holds)
        problems += 0 if negation_holds else 1

    for size in range(1, 4):
        implication_holds, converse_fails, universal_commutes, existential_commutes, nested_negation = check_quantifier_order(size)
        print(f"한정자의 순서(원소 {size}개, 두 변수 술어 {2 ** (size * size)}가지 모두): ∃y∀x → ∀x∃y {implication_holds},"
              f" 거꾸로 반례 있음 {converse_fails}, ∀∀ 순서 무관 {universal_commutes}, ∃∃ 순서 무관 {existential_commutes},"
              f" 둘인 명제의 부정 {nested_negation}")
        problems += 0 if (implication_holds and universal_commutes and existential_commutes and nested_negation) else 1
        if size >= 2 and not converse_fails:
            problems += 1

    reals: list[Fraction] = sample_reals()
    witness_works: bool = all(x * x < (abs(x) + 1) ** 2 for x in reals)
    zero_blocks_every_x: bool = not any(x * x < 0 for x in reals)
    same_value_blocks_every_y: bool = not any(y * y < y * y for y in reals)
    absolute_value_matches: bool = all((x * x < y * y) == (abs(x) < abs(y)) for x in reals[::7] for y in reals[::7])
    negation_witness_works: bool = all(x * x >= 0 * 0 for x in reals)
    print("예제 1-27 ③ y=|x|+1로 x²<y²:", witness_works, f"(점 {len(reals)}개)")
    print("  ④ y=0이면 x²<0인 x가 없음:", zero_blocks_every_x)
    print("  ∃y∀x: x=y이면 늘 거짓:", same_value_blocks_every_y)
    print("  x²<y² ⇔ |x|<|y|:", absolute_value_matches)
    print("  ④의 부정 ∀x∃y(x²≥y²): y=0으로 모든 x에서 참:", negation_witness_works)
    problems += sum(not check for check in (witness_works, zero_blocks_every_x, same_value_blocks_every_y, absolute_value_matches, negation_witness_works))

    number_line_matches: bool = all((x + 1 >= 2) == (x >= 1) for x in reals)
    print("x+1≥2 ⇔ x≥1:", number_line_matches)
    problems += 0 if number_line_matches else 1
    print("문제:", problems)
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
