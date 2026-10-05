#!/usr/bin/env bash
# 1장 책에 싣는 진리표, 동치 법칙, 동치 증명을 logic_check.py로 다시 계산한다.
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

echo "===== 표 1-1 연산자 넷, 표 1-3 항진과 모순 ====="
expect_holds table "¬p" "p ∧ q" "p ∨ q" "p ⊕ q"
expect_holds table "p ∨ ¬p" "p ∧ ¬p"

echo "===== 1-3 우선순위의 함정 ====="
expect_fails equiv "(¬p) ∧ q" "¬(p ∧ q)"

echo "===== 예제 1-7 ====="
expect_holds table "p ∧ q" "¬p" "¬(p ∧ q)" "¬p ∨ q" "(¬(p ∧ q)) ⊕ (¬p ∨ q)"
expect_holds equiv "(¬(p ∧ q)) ⊕ (¬p ∨ q)" "p"

echo "===== 1-4 함축, 쌍방조건, 번호 없는 예제 ====="
expect_holds table "p → q" "p ↔ q"
expect_holds table "p → q" "q → p" "(p → q) ∧ (q → p)" "p ↔ q"
expect_holds equiv "(p → q) ∧ (q → p)" "p ↔ q"

echo "===== 1-5 역, 이, 대우 ====="
expect_holds table "p → q" "q → p" "¬p → ¬q" "¬q → ¬p"
expect_holds equiv "p → q" "¬q → ¬p"
expect_holds equiv "q → p" "¬p → ¬q"
expect_fails equiv "p → q" "q → p"
expect_fails equiv "p → q" "¬p → ¬q"

echo "===== 예제 1-19 ====="
expect_holds table "¬p" "p → q" "¬p ∨ q" "¬q" "¬q → ¬p"
expect_holds chain "p → q" "¬p ∨ q" "¬q → ¬p"
expect_holds chain "¬q → ¬p" "¬(¬q) ∨ ¬p" "q ∨ ¬p" "¬p ∨ q"
expect_holds table "(p ↔ q) ↔ ((p → q) ∧ (q → p))"

echo "===== 표 1-7 동치 법칙과 쌍대 ====="
expect_holds equiv "p ∧ T" "p"
expect_holds equiv "p ∨ F" "p"
expect_holds equiv "p ∧ F" "F"
expect_holds equiv "p ∨ T" "T"
expect_holds equiv "p ∧ ¬p" "F"
expect_holds equiv "p ∨ ¬p" "T"
expect_holds equiv "¬(¬p)" "p"
expect_holds equiv "p ∧ p" "p"
expect_holds equiv "p ∨ p" "p"
expect_holds equiv "p ∧ q" "q ∧ p"
expect_holds equiv "p ∨ q" "q ∨ p"
expect_holds equiv "(p ∧ q) ∧ r" "p ∧ (q ∧ r)"
expect_holds equiv "(p ∨ q) ∨ r" "p ∨ (q ∨ r)"
expect_holds equiv "p ∨ (q ∧ r)" "(p ∨ q) ∧ (p ∨ r)"
expect_holds equiv "p ∧ (q ∨ r)" "(p ∧ q) ∨ (p ∧ r)"
expect_holds equiv "¬(p ∧ q)" "¬p ∨ ¬q"
expect_holds equiv "¬(p ∨ q)" "¬p ∧ ¬q"
expect_holds equiv "p ∧ (p ∨ q)" "p"
expect_holds equiv "p ∨ (p ∧ q)" "p"
expect_holds equiv "p → q" "¬p ∨ q"

echo "===== 2-2 결합법칙과 드모르간의 함정 ====="
expect_fails equiv "(p ∧ q) ∨ r" "p ∧ (q ∨ r)"
expect_fails equiv "¬(p ∧ q)" "¬p ∧ ¬q"

echo "===== 2-2 분배법칙의 ∨ 쪽이 성립하는 까닭 ====="
expect_holds chain "(p ∨ q) ∧ (p ∨ r)" "(p ∧ p) ∨ (p ∧ r) ∨ (q ∧ p) ∨ (q ∧ r)" "p ∨ (p ∧ r) ∨ (p ∧ q) ∨ (q ∧ r)" "(p ∧ (T ∨ r ∨ q)) ∨ (q ∧ r)" "(p ∧ T) ∨ (q ∧ r)" "p ∨ (q ∧ r)"

echo "===== 예제 1-20 ====="
expect_holds chain "¬(p ∨ (¬p ∧ q))" "¬p ∧ ¬(¬p ∧ q)" "¬p ∧ (¬(¬p) ∨ ¬q)" "¬p ∧ (p ∨ ¬q)" "(¬p ∧ p) ∨ (¬p ∧ ¬q)" "F ∨ (¬p ∧ ¬q)" "¬p ∧ ¬q"
expect_holds table "¬p" "¬q" "¬p ∧ q" "p ∨ (¬p ∧ q)" "¬(p ∨ (¬p ∧ q))" "¬p ∧ ¬q"

echo "===== 예제 1-21 ====="
expect_holds chain "(p → q) ∧ (p → ¬q)" "(¬p ∨ q) ∧ (¬p ∨ ¬q)" "¬p ∨ (q ∧ ¬q)" "¬p ∨ F" "¬p"


echo "===== 4-2 정당한 추론과 부당한 추론 ====="
expect_holds argument "p → q" "p" --conclusion "q"
expect_fails argument "p → q" "q" --conclusion "p"
expect_fails argument "p → q" "¬p" --conclusion "¬q"
expect_holds table "p → q"
expect_holds table "(p ∧ (p → q)) → q" "(q ∧ (p → q)) → p"

echo "===== 4-3 논리적 추론 법칙 일곱 가지와 대응하는 항진명제 ====="
expect_holds argument "p" "q" --conclusion "p ∧ q"
expect_holds argument "p" --conclusion "p ∨ q"
expect_holds argument "p ∧ q" --conclusion "p"
expect_holds argument "p ∧ q" --conclusion "q"
expect_holds argument "p" "p → q" --conclusion "q"
expect_holds argument "¬q" "p → q" --conclusion "¬p"
expect_holds argument "p ∨ q" "¬p" --conclusion "q"
expect_holds argument "p → q" "q → r" --conclusion "p → r"
expect_holds table "(p ∧ q) → (p ∧ q)" "p → (p ∨ q)" "(p ∧ q) → p" "(p ∧ q) → q"
expect_holds table "(p ∧ (p → q)) → q" "(¬q ∧ (p → q)) → ¬p" "((p ∨ q) ∧ ¬p) → q"
expect_holds table "((p → q) ∧ (q → r)) → (p → r)"
expect_holds argument "¬q → ¬p" "¬q" --conclusion "¬p"

echo "===== 예제 1-30 ====="
expect_holds argument "(¬p ∨ ¬q) → ¬r" "¬r → ¬s" "s" --conclusion "q"
expect_holds argument "(¬p ∨ ¬q) → ¬r" "¬r → ¬s" --conclusion "(¬p ∨ ¬q) → ¬s"
expect_holds argument "(¬p ∨ ¬q) → ¬s" "s" --conclusion "¬(¬p ∨ ¬q)"
expect_holds chain "s" "¬(¬s)"
expect_holds chain "¬(¬p ∨ ¬q)" "¬(¬p) ∧ ¬(¬q)" "p ∧ q"
expect_holds argument "p ∧ q" --conclusion "q"

echo "기대와 다른 결과: $failures"
exit $failures
