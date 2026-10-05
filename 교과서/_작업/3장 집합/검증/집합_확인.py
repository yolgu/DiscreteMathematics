"""3장 책에 싣는 집합 예제의 답, 기수 공식, 대수법칙, 증명의 각 줄을 원소를 모두 돌아 다시 계산한다.

법칙과 증명은 작은 전체집합의 모든 부분집합 조합에서 확인한다. 실행하면 확인한 항목과
결과를 출력하고, 기대와 다른 항목이 하나라도 있으면 종료 코드 1을 돌려준다.
"""

import sys
from fractions import Fraction
from itertools import combinations, product
from typing import Callable, Hashable, Iterable

Set = frozenset


class Report:
    """확인 항목의 결과를 모아 출력한다."""

    def __init__(self) -> None:
        self.failures: int = 0
        self.count: int = 0

    def expect(self, label: str, actual: object, expected: object) -> None:
        self.count += 1
        ok: bool = actual == expected
        if not ok:
            self.failures += 1
        mark: str = "맞음" if ok else "!!! 다름"
        print(f"[{mark}] {label}: {show(actual)}" + ("" if ok else f" (기대: {show(expected)})"))


def show(value: object) -> str:
    """중첩된 frozenset을 책에 쓰는 꼴의 중괄호 표기로 바꾼다."""
    if isinstance(value, frozenset):
        if not value:
            return "∅"
        return "{" + ", ".join(sorted(show(v) for v in value)) + "}"
    if isinstance(value, tuple):
        return "(" + ", ".join(show(v) for v in value) + ")"
    return str(value)


def letters(first: str, last: str) -> Set:
    return Set(chr(c) for c in range(ord(first), ord(last) + 1))


def power_set(base: Iterable[Hashable]) -> Set:
    items: list[Hashable] = list(base)
    return Set(Set(chosen) for size in range(len(items) + 1) for chosen in combinations(items, size))


def cartesian(left: Set, right: Set) -> Set:
    return Set(product(left, right))


def is_partition(blocks: Set, whole: Set) -> bool:
    """분할의 네 성질: 빈 조각 없음, 부분집합, 합집합이 전체, 서로 다른 조각은 서로소."""
    block_list: list[Set] = list(blocks)
    no_empty: bool = all(len(b) > 0 for b in block_list)
    all_subsets: bool = all(b <= whole for b in block_list)
    covers: bool = Set().union(*block_list) == whole if block_list else not whole
    disjoint: bool = all(not (x & y) for x, y in combinations(block_list, 2))
    return no_empty and all_subsets and covers and disjoint


def all_partitions(whole: Set) -> Set:
    candidates: Set = power_set(power_set(whole) - {Set()})
    return Set(p for p in candidates if is_partition(p, whole))


def check_section_1(r: Report) -> None:
    print("\n== 1절 집합의 개념 ==")
    a: Set = Set(x for x in range(-10, 11) if -4 <= x <= 4)
    r.expect("예제 3-5 A의 원소", a, Set(range(-4, 5)))
    r.expect("예제 3-5 |A|", len(a), 9)
    c: Set = Set(z for z in range(-1000, 1001) if z ** 3 == 2)
    r.expect("예제 3-5 C (정수 -1000~1000에서 z³ = 2)", len(c), 0)
    r.expect("1³ < 2 < 2³", 1 ** 3 < 2 < 2 ** 3, True)
    p: Fraction = Fraction(1, 3)
    q: Fraction = Fraction(1, 2)
    middle: Fraction = (p + q) / 2
    r.expect("두 유리수 1/3, 1/2 사이의 평균은 그 사이의 유리수", (middle, p < middle < q), (Fraction(5, 12), True))

    a8: Set = Set(x for x in range(-10, 11) if -3 < x <= 3)
    e8: Set = Set({-2, -1, 0, 1, 2, 3})
    r.expect("예제 3-8 A = E", a8 == e8, True)
    c8_first: list[int] = [2 ** k for k in range(0, 6)]
    r.expect("예제 3-8 C의 앞 여섯 원소(k = 0부터)", c8_first, [1, 2, 4, 8, 16, 32])
    r.expect("k > 0이면 1이 빠짐", 1 in [2 ** k for k in range(1, 6)], False)

    r.expect("{1, 2}와 {1, 3}은 공통 원소 1이 있어도 다름", Set({1, 2}) == Set({1, 3}), False)
    r.expect("{1, 2, 3}과 {4, 5, 6}은 기수가 같아도 다름", (len(Set({1, 2, 3})) == len(Set({4, 5, 6})), Set({1, 2, 3}) == Set({4, 5, 6})), (True, False))
    r.expect("{1, 2, 3} = {3, 2, 1} = {1, 1, 2, 3}", Set([1, 2, 3]) == Set([3, 2, 1]) == Set([1, 1, 2, 3]), True)


def check_section_2(r: Report) -> None:
    print("\n== 2절 집합의 종류 ==")
    empty: Set = Set()
    r.expect("∅와 {∅}는 다름", empty == Set({empty}), False)
    r.expect("|{∅}|", len(Set({empty})), 1)

    a: Set = Set({"a"})
    b: Set = Set({"a", "b", "w", "x", "y"})
    c: Set = Set({"x", "y"})
    d: Set = Set({"w", "x"})
    e: Set = Set({"a", "b", "w", "x", "y", "z"})
    r.expect("예제 3-10 A ⊂ B, C ⊂ B, B ⊂ E, C ⊂ E, A ⊂ E", (a < b, c < b, b < e, c < e, a < e), (True,) * 5)
    r.expect("예제 3-10 C ⊆ D, D ⊆ C", (c <= d, d <= c), (False, False))
    r.expect("예제 3-10 C ∩ D", c & d, Set({"x"}))

    ab: Set = Set({"a", "b"})
    dd: Set = Set({"d"})
    a11: Set = Set({ab, "c", dd})
    r.expect("예제 3-11 |A|", len(a11), 3)
    r.expect("예제 3-11 {a, b} ∈ A, c ∈ A, {d} ∈ A", (ab in a11, "c" in a11, dd in a11), (True, True, True))
    r.expect("예제 3-11 {a, b} ⊆ A는 거짓, d ∈ A는 거짓", (ab <= a11, "d" in a11), (False, False))
    r.expect("예제 3-11 {{d}} ⊂ A", Set({dd}) < a11, True)
    r.expect("예제 3-11 {{a, b}, c, {d}} = A", Set({ab, "c", dd}) == a11, True)

    universe: Set = Set({1, 2, 3, 4})
    subsets: list[Set] = list(power_set(universe))
    r.expect("모든 A에 대해 A ⊆ A, ∅ ⊆ A, A ⊆ U", all(s <= s and empty <= s and s <= universe for s in subsets), True)
    transitive: bool = all(x <= z for x in subsets for y in subsets for z in subsets if x <= y and y <= z)
    r.expect("A ⊆ B이고 B ⊆ C면 A ⊆ C (U의 모든 부분집합)", transitive, True)
    equal_iff: bool = all((x == y) == (x <= y and y <= x) for x in subsets for y in subsets)
    r.expect("A = B ⇔ (A ⊆ B ∧ B ⊆ A) (U의 모든 부분집합)", equal_iff, True)


def check_section_3(r: Report) -> None:
    print("\n== 3절 집합의 연산 ==")
    a: Set = letters("a", "d")
    b: Set = letters("d", "h")
    c: Set = Set({"c", "d", "e"})
    r.expect("예제 3-12 A ∪ B ∪ C", a | b | c, letters("a", "h"))
    r.expect("예제 3-13 A ∩ B ∩ C", a & b & c, Set({"d"}))

    a15: Set = letters("a", "g")
    b15: Set = letters("e", "l")
    c15: Set = letters("k", "n")
    r.expect("예제 3-15 |A|, |B|, |C|", (len(a15), len(b15), len(c15)), (7, 8, 4))
    r.expect("예제 3-15 |A∩B|, |B∩C|, |C∩A|, |A∩B∩C|", (len(a15 & b15), len(b15 & c15), len(c15 & a15), len(a15 & b15 & c15)), (3, 2, 0, 0))
    r.expect("예제 3-15 |A ∪ B| = 7 + 8 − 3", (len(a15 | b15), 7 + 8 - 3), (12, 12))
    r.expect("예제 3-15 |A ∩ C| = 7 + 4 − 11", (len(a15 & c15), len(a15 | c15), 7 + 4 - 11), (0, 11, 0))
    r.expect("예제 3-15 |A ∪ B ∪ C| = 7 + 8 + 4 − 3 − 2 − 0 + 0", (len(a15 | b15 | c15), 7 + 8 + 4 - 3 - 2 - 0 + 0), (14, 14))

    universe: Set = Set({1, 2, 3, 4})
    subsets: list[Set] = list(power_set(universe))
    two: bool = all(len(x | y) == len(x) + len(y) - len(x & y) for x in subsets for y in subsets)
    r.expect("|A ∪ B| = |A| + |B| − |A ∩ B| (U의 모든 부분집합)", two, True)
    disjoint: bool = all(len(x | y) == len(x) + len(y) for x in subsets for y in subsets if not (x & y))
    r.expect("서로소이면 |A ∪ B| = |A| + |B|", disjoint, True)
    three: bool = all(
        len(x | y | z) == len(x) + len(y) + len(z) - len(x & y) - len(y & z) - len(z & x) + len(x & y & z)
        for x in subsets for y in subsets for z in subsets
    )
    r.expect("세 집합의 기수 공식 (U의 모든 부분집합)", three, True)
    for inside in (1, 2, 3):
        added: int = inside
        subtracted: int = inside * (inside - 1) // 2
        added_back: int = 1 if inside == 3 else 0
        r.expect(f"표 3-2 집합 {inside}개에 속한 영역: 더함 {added}, 뺌 {subtracted}, 다시 더함 {added_back}", added - subtracted + added_back, 1)

    a18: Set = letters("a", "j")
    b18: Set = letters("g", "n")
    r.expect("예제 3-18 A − B", a18 - b18, letters("a", "f"))
    r.expect("B − A", b18 - a18, letters("k", "n"))
    r.expect("예제 3-19 A ⊕ B", a18 ^ b18, letters("a", "f") | letters("k", "n"))
    xor_def: bool = all((x ^ y) == Set(e for e in universe if (e in x) != (e in y)) for x in subsets for y in subsets)
    r.expect("x ∈ A ⊕ B ⇔ (x ∈ A) ⊕ (x ∈ B)", xor_def, True)
    diff_by_complement: bool = all((x - y) == (x & (universe - y)) for x in subsets for y in subsets)
    r.expect("X − Y = X ∩ Y'", diff_by_complement, True)

    samples: dict[Fraction, bool] = {
        Fraction(-34): True, Fraction(-33): False, Fraction(-3301, 100): True,
        Fraction(0): False, Fraction(7199, 100): False, Fraction(72): True, Fraction(100): True,
    }
    in_x_complement: Callable[[Fraction], bool] = lambda t: not (-33 <= t < 72)
    r.expect("예제 3-20 X'의 경계값(−34, −33, −33.01, 0, 71.99, 72, 100)", {t: in_x_complement(t) for t in samples}, samples)

    a21: Set = Set({1, 2})
    b21: Set = Set({"a", "b", "c"})
    ab21: Set = cartesian(a21, b21)
    ba21: Set = cartesian(b21, a21)
    r.expect("예제 3-21 A × B", ab21, Set({(1, "a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c")}))
    r.expect("예제 3-21 B × A", ba21, Set({("a", 1), ("a", 2), ("b", 1), ("b", 2), ("c", 1), ("c", 2)}))
    r.expect("예제 3-21 A × B = B × A인가", ab21 == ba21, False)
    r.expect("예제 3-21 |A × B|, |B × A|", (len(ab21), len(ba21)), (6, 6))

    a23: Set = Set({1, 2, 3})
    pa: Set = power_set(a23)
    r.expect("예제 3-23 |P(A)|", len(pa), 8)
    r.expect("예제 3-23 P(A)", pa, Set({Set(), Set({1}), Set({2}), Set({3}), Set({1, 2}), Set({1, 3}), Set({2, 3}), Set({1, 2, 3})}))
    empty: Set = Set()
    b23: Set = Set({empty, Set({empty})})
    pb: Set = power_set(b23)
    expected_pb: Set = Set({empty, Set({empty}), Set({Set({empty})}), b23})
    r.expect("예제 3-23 P(B)", pb, expected_pb)
    r.expect("예제 3-23 |P(B)|", len(pb), 4)
    r.expect("예제 3-23 ∅ ∈ B이고 ∅ ⊆ B", (empty in b23, empty <= b23), (True, True))
    sizes: list[int] = [len(power_set(range(n))) for n in range(7)]
    r.expect("|P(A)| = 2ⁿ (n = 0~6)", sizes, [2 ** n for n in range(7)])
    bits: list[str] = ["".join("1" if k in s else "0" for k in (1, 2, 3)) for s in pa]
    r.expect("{1, 2, 3}의 부분집합과 3비트 나열은 하나씩 짝지어짐", sorted(bits), sorted(f"{n:03b}" for n in range(8)))


def check_section_4(r: Report) -> None:
    print("\n== 4절 집합의 대수법칙 ==")
    universe: Set = Set({1, 2, 3})
    subsets: list[Set] = list(power_set(universe))
    empty: Set = Set()

    def comp(x: Set) -> Set:
        return universe - x

    triples: list[tuple[Set, Set, Set]] = list(product(subsets, repeat=3))
    laws: dict[str, Callable[[Set, Set, Set], bool]] = {
        "항등 A∪∅=A, A∩U=A": lambda a, b, c: a | empty == a and a & universe == a,
        "지배 A∪U=U, A∩∅=∅": lambda a, b, c: a | universe == universe and a & empty == empty,
        "멱등": lambda a, b, c: a | a == a and a & a == a,
        "교환": lambda a, b, c: a | b == b | a and a & b == b & a,
        "결합": lambda a, b, c: a | (b | c) == (a | b) | c and a & (b & c) == (a & b) & c,
        "분배 ∪, ∩": lambda a, b, c: a | (b & c) == (a | b) & (a | c) and a & (b | c) == (a & b) | (a & c),
        "이중 보 (A')'=A": lambda a, b, c: comp(comp(a)) == a,
        "보 A∪A'=U, A∩A'=∅": lambda a, b, c: a | comp(a) == universe and a & comp(a) == empty,
        "보 ∅'=U, U'=∅": lambda a, b, c: comp(empty) == universe and comp(universe) == empty,
        "드모르간": lambda a, b, c: comp(a | b) == comp(a) & comp(b) and comp(a & b) == comp(a) | comp(b),
        "흡수": lambda a, b, c: a | (a & b) == a and a & (a | b) == a,
        "곱집합 분배 A×(B∩C), A×(B∪C)": lambda a, b, c: (
            cartesian(a, b & c) == cartesian(a, b) & cartesian(a, c)
            and cartesian(a, b | c) == cartesian(a, b) | cartesian(a, c)
        ),
    }
    for name, law in laws.items():
        r.expect(f"표 3-5 {name} (U = {{1, 2, 3}}의 부분집합 세 개 조합 모두)", all(law(a, b, c) for a, b, c in triples), True)

    pairs: list[tuple[Set, Set]] = list(product(subsets, repeat=2))
    absorb_1: list[Callable[[Set, Set], Set]] = [
        lambda a, b: a & (a | b), lambda a, b: (a | empty) & (a | b), lambda a, b: a | (empty & b), lambda a, b: a | empty, lambda a, b: a,
    ]
    absorb_2: list[Callable[[Set, Set], Set]] = [
        lambda a, b: a | (a & b), lambda a, b: (a & universe) | (a & b), lambda a, b: a & (universe | b), lambda a, b: a & universe, lambda a, b: a,
    ]
    for label, steps in (("예제 3-25 A∩(A∪B)의 다섯 줄", absorb_1), ("예제 3-25 A∪(A∩B)의 다섯 줄", absorb_2)):
        r.expect(label + "이 모두 같음", all(len({step(a, b) for step in steps}) == 1 for a, b in pairs), True)

    xor_steps: list[Callable[[Set, Set], Set]] = [
        lambda a, b: (a | b) - (a & b),
        lambda a, b: (a | b) & comp(a & b),
        lambda a, b: (a | b) & (comp(a) | comp(b)),
        lambda a, b: ((a | b) & comp(a)) | ((a | b) & comp(b)),
        lambda a, b: ((a & comp(a)) | (b & comp(a))) | ((a & comp(b)) | (b & comp(b))),
        lambda a, b: (empty | (b & comp(a))) | ((a & comp(b)) | empty),
        lambda a, b: (b & comp(a)) | (a & comp(b)),
        lambda a, b: (b - a) | (a - b),
        lambda a, b: (a - b) | (b - a),
        lambda a, b: a ^ b,
    ]
    r.expect("번호 없는 예제 (A∪B)−(A∩B) = A⊕B의 열 줄이 모두 같음", all(len({step(a, b) for step in xor_steps}) == 1 for a, b in pairs), True)


def check_section_5(r: Report) -> None:
    print("\n== 5절 집합의 분할 ==")
    whole: Set = Set({"a", "b", "c"})
    found: Set = all_partitions(whole)
    expected: Set = Set({
        Set({Set({"a"}), Set({"b"}), Set({"c"})}),
        Set({Set({"a", "b"}), Set({"c"})}),
        Set({Set({"a", "c"}), Set({"b"})}),
        Set({Set({"a"}), Set({"b", "c"})}),
        Set({whole}),
    })
    r.expect("예제 3-30 {a, b, c}의 분할 개수", len(found), 5)
    r.expect("예제 3-30 분할 다섯 가지", found, expected)
    r.expect("{{a, b, c}}는 분할", is_partition(Set({whole}), whole), True)
    r.expect("{{a, b}, {b, c}}는 분할이 아님(겹침)", is_partition(Set({Set({"a", "b"}), Set({"b", "c"})}), whole), False)
    r.expect("{{a}, {b}}는 분할이 아님(c가 빠짐)", is_partition(Set({Set({"a"}), Set({"b"})}), whole), False)
    r.expect("{∅, {a, b, c}}는 분할이 아님(빈 조각)", is_partition(Set({Set(), whole}), whole), False)


def main() -> int:
    report: Report = Report()
    check_section_1(report)
    check_section_2(report)
    check_section_3(report)
    check_section_4(report)
    check_section_5(report)
    print(f"\n확인한 항목: {report.count}, 기대와 다른 항목: {report.failures}")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
