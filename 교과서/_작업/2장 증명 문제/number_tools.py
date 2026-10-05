"""정수와 자연수에 관한 문항을 판정하는 도구.

정수는 끝없이 많으므로 확인의 무게를 나누어 둔다.
- 반례나 예 하나는 그 값을 넣어 바로 판정한다. 이것은 그 자체로 결정적이다.
- 홀짝처럼 나머지에만 기대는 주장(정수 계수 다항식의 홀짝 등)은 나머지마다 확인하면 모든 정수를 덮는다.
- 그 밖에 '모든 정수'에 대한 주장은 해설의 추론이 근거이고, 표본 구간의 계산은 보조 확인이다.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from fractions import Fraction

SAMPLE: range = range(-60, 61)
NATURALS: range = range(1, 61)


def is_even(n: int) -> bool:
    return n % 2 == 0


def is_odd(n: int) -> bool:
    return n % 2 == 1


def is_multiple(n: int, divisor: int) -> bool:
    return n % divisor == 0


def is_prime(n: int) -> bool:
    return n > 1 and all(n % divisor for divisor in range(2, n))


def is_integer(x: Fraction) -> bool:
    return x.denominator == 1


def is_natural(x: Fraction) -> bool:
    return is_integer(x) and x >= 1


def holds_on_sample(claim: Callable[[int], bool], sample: Iterable[int] = SAMPLE) -> bool:
    """표본 구간의 모든 값에서 성립하는가. '모든 정수'에 대해서는 보조 확인일 뿐이다."""
    return all(claim(n) for n in sample)


def holds_on_residues(claim: Callable[[int], bool], modulus: int) -> bool:
    """claim이 n을 modulus로 나눈 나머지에만 기댈 때, 나머지마다 확인하면 모든 정수를 덮는다.

    그 기댐(주기성)도 표본 구간에서 함께 확인한다.
    """
    return all(claim(r) for r in range(modulus)) and all(claim(n) == claim(n % modulus) for n in SAMPLE)


def first_failure(claim: Callable[[int], bool], sample: Iterable[int]) -> int | None:
    return next((n for n in sample if not claim(n)), None)
