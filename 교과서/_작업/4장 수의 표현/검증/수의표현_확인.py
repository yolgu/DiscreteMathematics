"""4장 수의 표현에 싣는 계산을 다시 푼다. 틀린 것이 있으면 종료 코드 1."""
import sys
from fractions import Fraction

failures: list[str] = []


def check(label: str, actual: object, expected: object) -> None:
    status: str = "ok" if actual == expected else "틀림"
    if actual != expected:
        failures.append(label)
    print(f"[{status}] {label}: {actual!r} (기대 {expected!r})")


def digit_value(symbol: str) -> int:
    return int(symbol, 16)


def positional_value(text: str, base: int) -> Fraction:
    """'9B.FE3' 같은 글자를 자리값 전개로 계산한다."""
    whole, _, fraction = text.partition(".")
    value: Fraction = Fraction(0)
    for position, symbol in enumerate(reversed(whole)):
        value += digit_value(symbol) * Fraction(base) ** position
    for position, symbol in enumerate(fraction, start=1):
        value += digit_value(symbol) * Fraction(base) ** -position
    return value


def to_base(value: int, base: int) -> str:
    digits: str = "0123456789ABCDEF"
    if value == 0:
        return "0"
    out: str = ""
    while value > 0:
        out = digits[value % base] + out
        value //= base
    return out


def fraction_to_binary(fraction: Fraction, limit: int) -> str:
    bits: str = ""
    for _ in range(limit):
        if fraction == 0:
            break
        fraction *= 2
        bit: int = int(fraction)
        bits += str(bit)
        fraction -= bit
    return bits


def ones_complement(bits: str) -> str:
    return "".join("1" if bit == "0" else "0" for bit in bits)


def twos_complement(bits: str) -> str:
    width: int = len(bits)
    return format((int(ones_complement(bits), 2) + 1) % (1 << width), f"0{width}b")


def twos_by_shortcut(bits: str) -> str:
    """최하위 비트부터 첫 1까지는 그대로 두고 나머지를 뒤집는다."""
    last_one: int = bits.rfind("1")
    if last_one == -1:
        return bits
    return ones_complement(bits[:last_one]) + bits[last_one:]


def sign_magnitude_value(bits: str) -> int:
    magnitude: int = int(bits[1:], 2)
    return -magnitude if bits[0] == "1" else magnitude


def ones_value(bits: str) -> int:
    if bits[0] == "0":
        return int(bits, 2)
    return -int(ones_complement(bits[1:]), 2)


def twos_value(bits: str) -> int:
    raw: int = int(bits, 2)
    return raw - (1 << len(bits)) if bits[0] == "1" else raw


def ones_code(value: int, width: int) -> str:
    if value >= 0:
        return format(value, f"0{width}b")
    return ones_complement(format(-value, f"0{width}b"))


def twos_code(value: int, width: int) -> str:
    return format(value % (1 << width), f"0{width}b")


def add_ones(x: str, y: str) -> tuple[str, str]:
    width: int = len(x)
    total: int = int(x, 2) + int(y, 2)
    raw: str = format(total, f"0{width}b")
    if total >= 1 << width:
        total = (total - (1 << width)) + 1
    return raw, format(total, f"0{width}b")


def add_twos(x: str, y: str) -> tuple[str, str]:
    width: int = len(x)
    total: int = int(x, 2) + int(y, 2)
    return format(total, f"0{width}b"), format(total % (1 << width), f"0{width}b")


def main() -> int:
    print("== 1절 수와 그 성질")
    check("예제 4-1 589", 5 * 10**2 + 8 * 10**1 + 9 * 10**0, 589)
    check("예제 4-5 345.734", positional_value("345.734", 10), Fraction(345734, 1000))
    check("유리수 6/8의 하한항", Fraction(6, 8), Fraction(3, 4))
    check("1/7 소수", str(Fraction(10**12, 7) // 1), "142857142857")
    product: complex = (3 + 6j) * 12j
    check("예제 4-6 합", (3 + 6j) + 12j, 3 + 18j)
    check("예제 4-6 곱", product, -72 + 36j)
    check("예제 4-7 합의 역", 9 + (-9), 0)
    check("예제 4-7 곱의 역", 9 * Fraction(1, 9), 1)
    check("시그마 1..4", sum(range(1, 5)), 10)
    product_value: int = 1
    for i in range(1, 5):
        product_value *= i
    check("파이 1..4", product_value, 24)
    check("자리 전개를 시그마로 589", sum(a * 10**i for i, a in enumerate([9, 8, 5])), 589)

    rules_hold: bool = True
    for d in range(-12, 13):
        if d == 0:
            continue
        for k in range(-6, 7):
            for l in range(-6, 7):
                m: int = d * k
                n: int = d * l
                rules_hold = rules_hold and (m + n) % d == 0 and (m - n) % d == 0
                rules_hold = rules_hold and (m * l) % d == 0
    for a in range(-8, 9):
        if a == 0:
            continue
        for k in range(-5, 6):
            for l in range(-5, 6):
                b: int = a * k
                c: int = b * l
                rules_hold = rules_hold and c % a == 0
    check("나누기 규칙 넷(범위 전수)", rules_hold, True)
    check("d|0 (d=7)", 0 % 7 == 0, True)

    check("17 mod 5", 17 % 5, 2)
    check("-7 mod 3", -7 % 3, 2)
    check("-7 = 3*(-3) + 2", 3 * (-3) + 2, -7)
    mod_matches: bool = all(
        n % d == n - d * (n // d) and 0 <= n % d < d
        for n in range(-50, 51) for d in range(1, 13)
    )
    check("파이썬 %가 0≤r<d 정의와 같음(d>0)", mod_matches, True)
    check("n mod d = 0 ⇔ d|n", all((n % d == 0) == any(n == d * q for q in range(-60, 61))
                                   for n in range(-50, 51) for d in range(1, 13)), True)

    print("== 2절 수 체계")
    check("표 4-2 0..16", [(v, to_base(v, 2), to_base(v, 8), to_base(v, 16)) for v in (9, 10, 15, 16)],
          [(9, "1001", "11", "9"), (10, "1010", "12", "A"), (15, "1111", "17", "F"), (16, "10000", "20", "10")])
    value_4_15: Fraction = positional_value("9B.FE3", 16)
    check("예제 4-15 9B.FE3", value_4_15, Fraction(155) + Fraction(15, 16) + Fraction(14, 256) + Fraction(3, 4096))
    check("예제 4-15 소수", float(value_4_15), 155.992919921875)

    check("예제 4-17 101+11", to_base(0b101 + 0b11, 2), "1000")
    check("예제 4-17 100-11", to_base(0b100 - 0b11, 2), "1")
    check("예제 4-17 1101x11", to_base(0b1101 * 0b11, 2), "100111")
    check("예제 4-17 부분곱 합", to_base(0b1101 + (0b1101 << 1), 2), "100111")
    check("예제 4-17 10110÷101", (to_base(0b10110 // 0b101, 2), to_base(0b10110 % 0b101, 2)), ("100", "10"))
    check("강의 판서 1101x101", to_base(0b1101 * 0b101, 2), "1000001")

    check("예제 4-19 939+99", to_base(0x939 + 0x99, 16), "9D2")
    check("예제 4-19 5A4-CE", to_base(0x5A4 - 0xCE, 16), "4D6")
    check("예제 4-19 D82x9", to_base(0xD82 * 9, 16), "7992")
    check("예제 4-19 D82x3", to_base(0xD82 * 3, 16), "2886")
    check("예제 4-19 D82x39", to_base(0xD82 * 0x39, 16), "301F2")
    check("예제 4-19 BB1÷3C", (to_base(0xBB1 // 0x3C, 16), to_base(0xBB1 % 0x3C, 16)), ("31", "35"))
    check("예제 4-19 BB-B4", to_base(0xBB - 0xB4, 16), "7")
    check("예제 4-19 71-3C", to_base(0x71 - 0x3C, 16), "35")
    check("예제 4-19 3C x 3", to_base(0x3C * 3, 16), "B4")

    remainders: list[int] = []
    quotient: int = 163
    while quotient > 0:
        remainders.append(quotient % 2)
        quotient //= 2
    check("163 나머지(위에서 아래로)", remainders, [1, 1, 0, 0, 0, 1, 0, 1])
    check("163 = 10100011", to_base(163, 2), "10100011")
    check("0.875 → .111", fraction_to_binary(Fraction(7, 8), 20), "111")
    check("163.875 = 10100011.111", positional_value("10100011.111", 2), Fraction(163875, 1000))
    check("14 = 1110", to_base(14, 2), "1110")
    check("0.75 → .11", fraction_to_binary(Fraction(3, 4), 20), "11")
    check("14.75 = 1110.11", positional_value("1110.11", 2), Fraction(1475, 100))
    tenth_bits: str = fraction_to_binary(Fraction(1, 10), 24)
    check("0.1의 2진 앞 24자리", tenth_bits, "000110011001100110011001")
    check("0.1이 24자리 안에 끝나지 않음", len(tenth_bits), 24)
    check("0.1 = 0.0(0011 반복): 1/10 = (3/16)/(1-1/16) /2", Fraction(3, 15) / 2, Fraction(1, 10))
    check("8진 243.7", positional_value("243.7", 8), Fraction(163875, 1000))
    check("16진 A3.E", positional_value("A3.E", 16), Fraction(163875, 1000))
    check("010 100 011 . 111", [int(g, 2) for g in ("010", "100", "011", "111")], [2, 4, 3, 7])
    check("1010 0011 . 1110", [to_base(int(g, 2), 16) for g in ("1010", "0011", "1110")], ["A", "3", "E"])
    check("0.0111은 0.111과 다름", positional_value("0.0111", 2) == positional_value("0.111", 2), False)

    print("== 3절 보수의 표현")
    check("3에 대한 7의 보수", 7 - 3, 4)
    check("1의 보수 00110101", ones_complement("00110101"), "11001010")
    check("2의 보수 00110101", twos_complement("00110101"), "11001011")
    check("합 = 2^8 - 1", int("00110101", 2) + int("11001010", 2), 2**8 - 1)
    check("합 = 2^8", int("00110101", 2) + int("11001011", 2), 2**8)
    check("2의 보수 00110100", twos_complement("00110100"), "11001100")
    check("요령 00110100", twos_by_shortcut("00110100"), "11001100")
    check("요령 = 정의(8비트 전수, 0 제외)",
          all(twos_by_shortcut(format(v, "08b")) == twos_complement(format(v, "08b")) for v in range(1, 256)), True)
    check("9의 보수 5,4,3", [9 - d for d in (5, 4, 3)], [4, 5, 6])
    check("10의 보수 5,4,3", [10 - d for d in (5, 4, 3)], [5, 6, 7])
    check("2자리 10의 보수 3", 100 - 3, 97)
    check("0010의 2의 보수(4비트)", twos_complement("0010"), "1110")
    check("00000010의 2의 보수(8비트)", twos_complement("00000010"), "11111110")

    check("예제 4-28 53", to_base(53, 2), "110101")
    check("예제 4-28 +53", "0" + format(53, "07b"), "00110101")
    check("예제 4-28 -53", "1" + format(53, "07b"), "10110101")
    check("-53 1의 보수(부호 두고 절대치 뒤집기)", "1" + ones_complement(format(53, "07b")), "11001010")
    check("-53 2의 보수(부호 두고 절대치 2의 보수)", "1" + twos_complement(format(53, "07b")), "11001011")
    check("-53 1의 보수 = +53 전체 뒤집기", ones_complement("00110101"), ones_code(-53, 8))
    check("-53 2의 보수 = +53 전체 2의 보수", twos_complement("00110101"), twos_code(-53, 8))

    codes: list[str] = [format(v, "04b") for v in range(16)]
    table: list[tuple[str, int, int, int]] = [(c, sign_magnitude_value(c), ones_value(c), twos_value(c)) for c in codes]
    for row in table:
        print("   표 4-3", row)
    check("1의 보수 표(슬라이드 6쪽)", [ones_code(v, 4) for v in range(-7, 0)],
          ["1000", "1001", "1010", "1011", "1100", "1101", "1110"])
    check("2의 보수 표(슬라이드 6쪽)", [twos_code(v, 4) for v in range(-8, 0)],
          ["1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"])
    check("1의 보수 -0 = 1111", ones_value("1111"), 0)
    for width in (4, 8):
        check(f"{width}비트 부호화-절대치 범위", (min(sign_magnitude_value(format(v, f'0{width}b')) for v in range(1 << width)),
                                         max(sign_magnitude_value(format(v, f'0{width}b')) for v in range(1 << width))),
              (-(2 ** (width - 1) - 1), 2 ** (width - 1) - 1))
        check(f"{width}비트 1의 보수 범위", (min(ones_value(format(v, f'0{width}b')) for v in range(1 << width)),
                                      max(ones_value(format(v, f'0{width}b')) for v in range(1 << width))),
              (-(2 ** (width - 1) - 1), 2 ** (width - 1) - 1))
        check(f"{width}비트 2의 보수 범위", (min(twos_value(format(v, f'0{width}b')) for v in range(1 << width)),
                                      max(twos_value(format(v, f'0{width}b')) for v in range(1 << width))),
              (-(2 ** (width - 1)), 2 ** (width - 1) - 1))
    check("0의 표현 개수(부호화-절대치, 1의 보수, 2의 보수)",
          ([r[1] for r in table].count(0), [r[2] for r in table].count(0), [r[3] for r in table].count(0)), (2, 2, 1))
    check("111 = 1000 - 1", 0b111, 0b1000 - 1)
    check("2의 보수로 0의 보수", add_twos(ones_complement("0000"), "0001"), ("10000", "0000"))

    sum_4_5: str = format(0b0100 + 0b0101, "04b")
    check("부호화-절대치 4+5 비트", sum_4_5, "1001")
    check("1001을 부호화-절대치로 읽기", sign_magnitude_value(sum_4_5), -1)
    check("9는 4비트 부호화-절대치 범위 밖", 9 > 2**3 - 1, True)
    raw_m3_m4: int = 0b1011 + 0b1100
    check("부호화-절대치 (-3)+(-4) 비트", format(raw_m3_m4, "05b"), "10111")
    check("넷째 비트까지 읽기", sign_magnitude_value(format(raw_m3_m4 % 16, "04b")), 7)
    check("-7은 범위 안(1111)", sign_magnitude_value("1111"), -7)

    check("10칸 막대 5-3", (5 + (10 - 3)) - 10, 2)
    check("x-y = x+(10-y)-10 (전수)", all(x - y == x + (10 - y) - 10 for x in range(10) for y in range(10)), True)

    check("3-3 1의 보수 1010 방법①", -(2**3 - 1) + int("010", 2), -5)
    check("3-3 1의 보수 1010 방법②", "1" + ones_complement("010"), "1101")
    check("3-3 2의 보수 1011 방법①", -(2**3) + int("011", 2), -5)
    check("3-3 2의 보수 1011 방법②", "1" + twos_complement("011"), "1101")
    method_one_ok: bool = all(
        ones_value(c) == (-(2**3 - 1) + int(c[1:], 2) if c[0] == "1" else int(c, 2))
        and twos_value(c) == (-(2**3) + int(c[1:], 2) if c[0] == "1" else int(c, 2))
        for c in codes
    )
    check("방법① = 정의(4비트 전수)", method_one_ok, True)
    method_two_ok: bool = all(
        ones_value(c) == -int(ones_complement(c[1:]), 2)
        for c in codes if c[0] == "1"
    ) and all(
        twos_value(c) == -int(twos_complement(c[1:]), 2) or c == "1000"
        for c in codes if c[0] == "1"
    )
    check("방법② = 정의(1000 빼고)", method_two_ok, True)
    check("2의 보수 1000의 방법②는 000으로 돌아감", twos_complement("000"), "000")

    print("== 4절 보수의 연산")
    check("① 1의 보수 2-4", add_ones("0010", ones_code(-4, 4)), ("1101", "1101"))
    check("① 1101 → -2", ones_value("1101"), -2)
    check("① 1101을 부호화-절대치로", "1" + ones_complement("101"), "1010")
    check("① 2의 보수 2-4", add_twos("0010", twos_code(-4, 4)), ("1110", "1110"))
    check("① 1110 → -2", twos_value("1110"), -2)
    check("① 1110을 부호화-절대치로", "1" + twos_complement("110"), "1010")
    check("② 1의 보수 4-2", add_ones("0100", ones_code(-2, 4)), ("10001", "0010"))
    check("② 2의 보수 4-2", add_twos("0100", twos_code(-2, 4)), ("10010", "0010"))
    check("③ -2의 1의 보수, 2의 보수", (ones_code(-2, 4), twos_code(-2, 4)), ("1101", "1110"))
    check("③ 1의 보수 -2-4", add_ones("1101", "1011"), ("11000", "1001"))
    check("③ 1001 → -6", ones_value("1001"), -6)
    check("③ 1001을 부호화-절대치로", "1" + ones_complement("001"), "1110")
    check("③ 2의 보수 -2-4", add_twos("1110", "1100"), ("11010", "1010"))
    check("③ 1010 → -6", twos_value("1010"), -6)
    check("③ 1010을 부호화-절대치로", "1" + twos_complement("010"), "1110")
    check("10의 보수 4-2", 4 + (10 - 2), 12)
    check("9의 보수 4-2", (4 + (9 - 2)) - 10 + 1, 2)

    ones_ok: bool = True
    twos_ok: bool = True
    overflow_rule_ok: bool = True
    for x in range(-7, 8):
        for y in range(-7, 8):
            if -7 <= x + y <= 7:
                ones_ok = ones_ok and ones_value(add_ones(ones_code(x, 4), ones_code(y, 4))[1]) == x + y
    for x in range(-8, 8):
        for y in range(-8, 8):
            result: int = twos_value(add_twos(twos_code(x, 4), twos_code(y, 4))[1])
            in_range: bool = -8 <= x + y <= 7
            if in_range:
                twos_ok = twos_ok and result == x + y
            sign_flip: bool = (x >= 0 and y >= 0 and result < 0) or (x < 0 and y < 0 and result >= 0)
            overflow_rule_ok = overflow_rule_ok and (sign_flip == (not in_range))
    check("1의 보수 덧셈(순환 자리올림) 전수", ones_ok, True)
    check("2의 보수 덧셈(자리올림 버림) 전수", twos_ok, True)
    check("부호가 같은데 합의 부호가 바뀜 ⇔ 초과(2의 보수 4비트 전수)", overflow_rule_ok, True)
    check("2의 보수 5+4", add_twos("0101", "0100"), ("1001", "1001"))
    check("1001 → -7", twos_value("1001"), -7)
    check("2의 보수 (-5)+(-4)", add_twos(twos_code(-5, 4), twos_code(-4, 4)), ("10111", "0111"))
    check("-5의 2의 보수 코드", twos_code(-5, 4), "1011")
    check("부호가 다른 두 수는 초과하지 않음", all(-8 <= x + y <= 7 for x in range(-8, 0) for y in range(0, 8)), True)

    print()
    print("틀린 것:", failures if failures else "없음")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
