"""1장 3절(변수를 포함한 명제와 한정자)에 싣는 계산을 다시 푼다.

- 예제 1-24: P(x, y): x = 2y의 P(1, 2), P(2, 1)
- 예제 1-26: D = {1, 2, 3, 4}, P(x): x^2 < 10의 ∀xP(x), ∃xP(x)
- 한정자의 부정: 원소 네 개인 논의영역에서 가능한 모든 P(x)(16가지)에 대해
  ¬∀xP(x) ≡ ∃x¬P(x), ¬∃xP(x) ≡ ∀x¬P(x), ∀xP(x) ≡ P(1)∧…∧P(4)
- 예제 1-27: 실수 x, y, P(x, y): x^2 < y^2.
  실수 전체를 다 돌 수는 없으므로, 본문의 논증에 쓰는 식을 여러 유리수 점에서 확인한다.
  ③ y = |x| + 1이면 y^2 - x^2 = 2|x| + 1 > 0
  ④ y = 0이면 어떤 x도 x^2 < 0을 만족하지 않음
  순서를 바꾼 ∃y∀x: 어떤 y를 골라도 x = y이면 x^2 < y^2이 거짓
  x^2 < y^2 와 |x| < |y|가 같은 판정
- 1-1 그림: x + 1 ≥ 2 와 x ≥ 1이 같은 판정
"""

from fractions import Fraction
from itertools import product


def is_double(x: int, y: int) -> bool:
    return x == 2 * y


def square_below_ten(x: int) -> bool:
    return x * x < 10


def sample_reals() -> list[Fraction]:
    numerators: range = range(-40, 41)
    samples: list[Fraction] = sorted({Fraction(n, d) for n in numerators for d in (1, 2, 3, 7)})
    return samples


def check_quantifier_negation(domain: list[int]) -> bool:
    for truth_values in product((False, True), repeat=len(domain)):
        predicate: dict[int, bool] = dict(zip(domain, truth_values))
        for_all: bool = all(predicate[x] for x in domain)
        exists: bool = any(predicate[x] for x in domain)
        conjunction_matches: bool = for_all == (predicate[1] and predicate[2] and predicate[3] and predicate[4])
        negated_for_all_matches: bool = (not for_all) == any(not predicate[x] for x in domain)
        negated_exists_matches: bool = (not exists) == all(not predicate[x] for x in domain)
        if not (conjunction_matches and negated_for_all_matches and negated_exists_matches):
            return False
    return True


def main() -> None:
    print("예제 1-24: P(1, 2) =", is_double(1, 2), "/ P(2, 1) =", is_double(2, 1))

    domain: list[int] = [x for x in range(-10, 11) if 0 < x <= 4]
    print("예제 1-26: D =", domain, "/ P(x) 값 =", {x: square_below_ten(x) for x in domain})
    print("  ∀xP(x) =", all(square_below_ten(x) for x in domain), "/ ∃xP(x) =", any(square_below_ten(x) for x in domain))
    print("  반례:", [x for x in domain if not square_below_ten(x)], "/ 예:", [x for x in domain if square_below_ten(x)])

    print("한정자의 부정(16가지 P 모두):", check_quantifier_negation([1, 2, 3, 4]))

    reals: list[Fraction] = sample_reals()
    witness_works: bool = all(x * x < (abs(x) + 1) ** 2 for x in reals)
    zero_blocks_every_x: bool = not any(x * x < 0 for x in reals)
    same_value_blocks_every_y: bool = not any(y * y < y * y for y in reals)
    absolute_value_matches: bool = all((x * x < y * y) == (abs(x) < abs(y)) for x in reals[::7] for y in reals[::7])
    print("예제 1-27 ③ y=|x|+1로 x^2<y^2:", witness_works, f"(점 {len(reals)}개)")
    print("  ④ y=0이면 x^2<0인 x가 없음:", zero_blocks_every_x)
    print("  ∃y∀x: x=y이면 늘 거짓:", same_value_blocks_every_y)
    print("  x^2<y^2 ⇔ |x|<|y|:", absolute_value_matches)

    number_line_matches: bool = all((x + 1 >= 2) == (x >= 1) for x in reals)
    print("x+1≥2 ⇔ x≥1:", number_line_matches)


if __name__ == "__main__":
    main()
