"""2장 책에 싣는 계산과 판정을 다시 푼다.

- 예제 2-5, 2-23: n = 3k이면 n^3 = (3k)^3 = 27k^3 = 3(9k^3)이고 n^3은 3의 배수
- 정수의 닫힘: 덧셈, 뺄셈, 곱셈은 정수 안에서 끝나고 나눗셈은 아님(1 ÷ 2)
- 예제 2-14: n^3이 3의 배수가 아니면 n도 3의 배수가 아님
- 예제 2-32, 2-35: (a+1)^2와 a^2. 값, 차 2a + 1, 만나는 점 a = -1/2
- 반례증명법의 근거: 원소 네 개인 논의영역의 모든 P(x)에서 ¬∀xP(x) ≡ ∃x¬P(x), ¬∃xP(x) ≡ ∀x¬P(x)
- 예제 2-41: n! ≥ 2^(n-1)과 귀납 단계의 줄마다
- 예제 2-42: n비트 나열의 개수, 4비트 목록, k비트에서 (k+1)비트를 만드는 두 배 만들기
"""

from fractions import Fraction
from itertools import product
from math import factorial

INTEGER_SAMPLES: range = range(-300, 301)


def cube_of_multiple_of_three_is_multiple(k: int) -> bool:
    n: int = 3 * k
    steps_agree: bool = n ** 3 == (3 * k) ** 3 == 27 * k ** 3 == 3 * (9 * k ** 3)
    return steps_agree and n ** 3 % 3 == 0


def contrapositive_example_holds(n: int) -> bool:
    cube_not_multiple: bool = n ** 3 % 3 != 0
    return (not cube_not_multiple) or n % 3 != 0


def square_gap(a: Fraction) -> Fraction:
    return (a + 1) ** 2 - a ** 2


def real_samples() -> list[Fraction]:
    samples: list[Fraction] = sorted({Fraction(n, d) for n in range(-60, 61) for d in (1, 2, 3, 4, 7)})
    return samples


def quantifier_negation_holds(domain_size: int) -> bool:
    for truth_values in product((False, True), repeat=domain_size):
        for_all: bool = all(truth_values)
        exists: bool = any(truth_values)
        if (not for_all) != any(not value for value in truth_values):
            return False
        if (not exists) != all(not value for value in truth_values):
            return False
    return True


def induction_step_lines_hold(k: int) -> bool:
    factorial_splits: bool = factorial(k + 1) == factorial(k) * (k + 1)
    hypothesis_scales: bool = factorial(k) * (k + 1) >= 2 ** (k - 1) * (k + 1)
    factor_at_least_two: bool = 2 ** (k - 1) * (k + 1) >= 2 ** (k - 1) * 2
    exponent_rewrites: bool = 2 ** (k - 1) * 2 == 2 ** ((k + 1) - 1)
    return factorial_splits and hypothesis_scales and factor_at_least_two and exponent_rewrites


def bit_strings(length: int) -> list[str]:
    strings: list[str] = ["".join(bits) for bits in product("01", repeat=length)]
    return strings


def doubled_by_prefix(shorter: list[str]) -> list[str]:
    longer: list[str] = [bit + string for bit in "01" for string in shorter]
    return longer


def main() -> None:
    print("예제 2-5, 2-23: k가 -300~300일 때 모두 성립:", all(cube_of_multiple_of_three_is_multiple(k) for k in INTEGER_SAMPLES))

    closed_under_add_sub_mul: bool = all(
        isinstance(a + b, int) and isinstance(a - b, int) and isinstance(a * b, int)
        for a in range(-20, 21) for b in range(-20, 21)
    )
    print("정수의 닫힘: 덧셈, 뺄셈, 곱셈:", closed_under_add_sub_mul, "/ 1 ÷ 2 =", Fraction(1, 2), "(정수 아님)")

    print("예제 2-14: n이 -300~300일 때 모두 성립:", all(contrapositive_example_holds(n) for n in INTEGER_SAMPLES))

    reals: list[Fraction] = real_samples()
    minus_one: Fraction = Fraction(-1)
    print("예제 2-32: a = -1이면 (a+1)^2 =", (minus_one + 1) ** 2, ", a^2 =", minus_one ** 2)
    print("  차 = 2a + 1:", all(square_gap(a) == 2 * a + 1 for a in reals), f"(점 {len(reals)}개)")
    half: Fraction = Fraction(-1, 2)
    print("  a = -1/2에서 같음:", square_gap(half) == 0, "/ a < -1/2이면 (a+1)^2 < a^2:", all(square_gap(a) < 0 for a in reals if a < half))
    print("  a ≥ -1/2이면 (a+1)^2 ≥ a^2:", all(square_gap(a) >= 0 for a in reals if a >= half))
    print("예제 2-35: a = 1이면", (Fraction(1) + 1) ** 2, "≥", Fraction(1) ** 2, "/ a = 0이면", (Fraction(0) + 1) ** 2, "≥", Fraction(0) ** 2)

    print("한정자의 부정(원소 네 개, P 16가지):", quantifier_negation_holds(4))

    print("예제 2-41: 1! =", factorial(1), ", 2^(1-1) =", 2 ** 0)
    print("  n = 1~80에서 n! ≥ 2^(n-1):", all(factorial(n) >= 2 ** (n - 1) for n in range(1, 81)))
    print("  k = 1~80에서 귀납 단계의 줄마다 성립:", all(induction_step_lines_hold(k) for k in range(1, 81)))
    print("  등호가 되는 n:", [n for n in range(1, 81) if factorial(n) == 2 ** (n - 1)])

    print("예제 2-42: n = 1~14에서 나열 개수 = 2^n:", all(len(bit_strings(n)) == 2 ** n for n in range(1, 15)))
    print("  1비트:", bit_strings(1))
    print("  4비트(", len(bit_strings(4)), "개):", bit_strings(4))
    doubling_matches: bool = all(
        len(set(doubled_by_prefix(bit_strings(k)))) == 2 * len(bit_strings(k)) and set(doubled_by_prefix(bit_strings(k))) == set(bit_strings(k + 1))
        for k in range(1, 14)
    )
    print("  앞에 0이나 1을 붙여 두 배로 만들면 겹침도 빠짐도 없음(k = 1~13):", doubling_matches)
    print("  2비트에서 3비트:", bit_strings(2), "→", doubled_by_prefix(bit_strings(2)))


if __name__ == "__main__":
    main()
