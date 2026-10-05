#!/usr/bin/env bash
# 3장 책에 싣는 진리표와, 집합의 대수법칙에 대응하는 명제의 동치를 logic_check.py로 다시 계산한다.
# p, q, r은 각각 'x ∈ A', 'x ∈ B', 'x ∈ C'를 뜻한다. T는 'x ∈ U', F는 'x ∈ ∅'에 해당한다.
# 성립해야 하는 것은 종료 코드 0, 성립하지 않아야 하는 것은 1이 나와야 한다.

export PATH="/mingw64/bin:$PATH"
CHECK="python /c/Users/wndls/.claude/skills/lecture-to-textbook/scripts/logic_check.py"
failures=0

expect_holds() {
  echo "### 성립해야 함: $*"
  $CHECK "$@"
  if [ $? -ne 0 ]; then echo "!!! 기대와 다름"; failures=$((failures + 1)); fi
  echo
}

expect_fails() {
  echo "### 성립하지 않아야 함: $*"
  $CHECK "$@"
  if [ $? -ne 1 ]; then echo "!!! 기대와 다름"; failures=$((failures + 1)); fi
  echo
}

echo "===== 2절 포함관계 정리 ====="
echo "(1) A ⊆ A: p → p는 항진명제"
expect_holds table "p → p"
echo "(2) ∅ ⊆ A: 표 3-1, 조건이 거짓인 셋째와 넷째 줄"
expect_holds table "p → q"
expect_holds equiv "F → q" "T"
echo "(3) A ⊆ U: 결론이 늘 참이면 함축도 늘 참"
expect_holds equiv "p → T" "T"
echo "(4) 추이: 가설적 삼단논법"
expect_holds argument "p → q" "q → r" --conclusion "p → r"
echo "(5) 상등 ⇔ 두 포함"
expect_holds equiv "(p → q) ∧ (q → p)" "p ↔ q"

echo "===== 3절 연산의 정의와 배타적 논리합 ====="
echo "대칭차집합: (x∈A ∧ x∉B) ∨ (x∉A ∧ x∈B)는 p ⊕ q"
expect_holds equiv "(p ∧ ¬q) ∨ (¬p ∧ q)" "p ⊕ q"
echo "차집합 X − Y = X ∩ Y'의 명제 꼴은 정의 그대로"
expect_holds equiv "p ∧ ¬q" "p ∧ ¬q"
echo "차집합은 교환되지 않음: A − B와 B − A"
expect_fails equiv "p ∧ ¬q" "q ∧ ¬p"

echo "===== 표 3-5 대수법칙에 대응하는 동치 ====="
expect_holds equiv "p ∨ F" "p"
expect_holds equiv "p ∧ T" "p"
expect_holds equiv "p ∨ T" "T"
expect_holds equiv "p ∧ F" "F"
expect_holds equiv "p ∨ p" "p"
expect_holds equiv "p ∧ p" "p"
expect_holds equiv "p ∨ q" "q ∨ p"
expect_holds equiv "p ∧ q" "q ∧ p"
expect_holds equiv "p ∨ (q ∨ r)" "(p ∨ q) ∨ r"
expect_holds equiv "p ∧ (q ∧ r)" "(p ∧ q) ∧ r"
expect_holds equiv "p ∨ (q ∧ r)" "(p ∨ q) ∧ (p ∨ r)"
expect_holds equiv "p ∧ (q ∨ r)" "(p ∧ q) ∨ (p ∧ r)"
expect_holds equiv "¬(¬p)" "p"
expect_holds equiv "p ∨ ¬p" "T"
expect_holds equiv "p ∧ ¬p" "F"
expect_holds equiv "¬F" "T"
expect_holds equiv "¬T" "F"
expect_holds equiv "¬(p ∨ q)" "¬p ∧ ¬q"
expect_holds equiv "¬(p ∧ q)" "¬p ∨ ¬q"
expect_holds equiv "p ∨ (p ∧ q)" "p"
expect_holds equiv "p ∧ (p ∨ q)" "p"

echo "곱집합의 분배법칙: p는 a ∈ A, q는 b ∈ B, r은 b ∈ C"
expect_holds equiv "p ∧ (q ∧ r)" "(p ∧ q) ∧ (p ∧ r)"
expect_holds equiv "p ∧ (q ∨ r)" "(p ∧ q) ∨ (p ∧ r)"

echo "===== 예제 3-24 드모르간의 법칙: 원소 증명의 명제 꼴 ====="
expect_holds chain "¬(p ∨ q)" "¬p ∧ ¬q"
expect_holds chain "¬(p ∧ q)" "¬p ∨ ¬q"

echo "===== 예제 3-25 흡수법칙: 각 줄의 명제 꼴 ====="
expect_holds chain "p ∧ (p ∨ q)" "(p ∨ F) ∧ (p ∨ q)" "p ∨ (F ∧ q)" "p ∨ F" "p"
expect_holds chain "p ∨ (p ∧ q)" "(p ∧ T) ∨ (p ∧ q)" "p ∧ (T ∨ q)" "p ∧ T" "p"

echo "===== 번호 없는 예제 (A∪B)−(A∩B) = A⊕B: 각 줄의 명제 꼴 ====="
expect_holds chain "(p ∨ q) ∧ ¬(p ∧ q)" "(p ∨ q) ∧ (¬p ∨ ¬q)" "((p ∨ q) ∧ ¬p) ∨ ((p ∨ q) ∧ ¬q)" "((p ∧ ¬p) ∨ (q ∧ ¬p)) ∨ ((p ∧ ¬q) ∨ (q ∧ ¬q))" "(F ∨ (q ∧ ¬p)) ∨ ((p ∧ ¬q) ∨ F)" "(q ∧ ¬p) ∨ (p ∧ ¬q)" "(p ∧ ¬q) ∨ (q ∧ ¬p)" "p ⊕ q"

echo "기대와 다른 결과: $failures"
exit $failures
