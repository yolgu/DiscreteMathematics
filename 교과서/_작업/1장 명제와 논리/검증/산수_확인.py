"""1장 책에 싣는 산수 계산을 다시 푼다.

- 예제 1-3: 2^n = n^2을 만족하는 정수 n
- 표 1-8: T = 1, F = 0으로 놓고 AND를 곱하기, OR를 더하기로 옮겼을 때
  각 법칙이 보통 산수로 성립하는지(0과 1을 모두 넣어 본다)
"""

from fractions import Fraction
from itertools import product
from typing import Callable


def power_of_two(n: int) -> Fraction:
    return Fraction(2) ** n


def integer_solutions(lower: int, upper: int) -> list[int]:
    solutions: list[int] = [n for n in range(lower, upper + 1) if power_of_two(n) == n * n]
    return solutions


ArithmeticLaw = Callable[..., tuple[int, int]]

ARITHMETIC_LAWS: dict[str, tuple[int, ArithmeticLaw]] = {
    "AND 정의 p∧q ↔ p×q": (2, lambda p, q: (p * q, int(p == 1 and q == 1))),
    "OR 정의 p∨q ↔ p+q": (2, lambda p, q: (p + q, int(p == 1 or q == 1))),
    "항등 p∧T≡p ↔ p×1=p": (1, lambda p: (p * 1, p)),
    "항등 p∨F≡p ↔ p+0=p": (1, lambda p: (p + 0, p)),
    "지배 p∧F≡F ↔ p×0=0": (1, lambda p: (p * 0, 0)),
    "지배 p∨T≡T ↔ p+1=1": (1, lambda p: (p + 1, 1)),
    "멱등 p∧p≡p ↔ p×p=p": (1, lambda p: (p * p, p)),
    "멱등 p∨p≡p ↔ p+p=p": (1, lambda p: (p + p, p)),
    "교환 p×q=q×p": (2, lambda p, q: (p * q, q * p)),
    "교환 p+q=q+p": (2, lambda p, q: (p + q, q + p)),
    "결합 (pq)r=p(qr)": (3, lambda p, q, r: ((p * q) * r, p * (q * r))),
    "결합 (p+q)+r=p+(q+r)": (3, lambda p, q, r: ((p + q) + r, p + (q + r))),
    "분배 p(q+r)=pq+pr": (3, lambda p, q, r: (p * (q + r), p * q + p * r)),
    "분배 p+qr=(p+q)(p+r)": (3, lambda p, q, r: (p + q * r, (p + q) * (p + r))),
}


def counterexamples(arity: int, law: ArithmeticLaw) -> list[tuple[int, ...]]:
    found: list[tuple[int, ...]] = []
    for values in product((0, 1), repeat=arity):
        left, right = law(*values)
        if left != right:
            found.append(values)
    return found


def main() -> None:
    print("예제 1-3: -200 ≤ n ≤ 200에서 2^n = n^2인 정수 n =", integer_solutions(-200, 200))
    print("  n=2:", power_of_two(2), "=", 2 * 2, "/ n=4:", power_of_two(4), "=", 4 * 4)
    print()
    print("표 1-8: 0과 1을 모두 넣었을 때 산수 식의 양쪽이 다른 경우(반례)")
    for name, (arity, law) in ARITHMETIC_LAWS.items():
        found: list[tuple[int, ...]] = counterexamples(arity, law)
        verdict: str = "성립" if not found else f"깨짐, 반례 {found}"
        print(f"  {name}: {verdict}")
    print()
    print("본문 계산: 1 + 1×1 =", 1 + 1 * 1, "/ (1+1)×(1+1) =", (1 + 1) * (1 + 1))


if __name__ == "__main__":
    main()
