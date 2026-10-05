#!/usr/bin/env bash
# 2장 책에 싣는 동치, 진리표, 추론을 logic_check.py로 다시 계산한다.
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

echo "===== 2 직접증명법: p가 거짓인 줄은 p → q가 늘 참 ====="
expect_holds table "p → q"
expect_holds equiv "F → q" "T"

echo "===== 3-1 대우증명법 ====="
expect_holds equiv "p → q" "¬q → ¬p"
expect_fails equiv "p → q" "¬p → ¬q"
expect_fails equiv "p → q" "q → p"
expect_holds argument "¬q → ¬p" --conclusion "p → q"
expect_fails argument "¬p → ¬q" --conclusion "p → q"
expect_holds equiv "¬(¬q)" "q"

echo "===== 3-2 모순증명법: 유도 세 줄과 표 2-1 ====="
expect_holds chain "p → q" "¬p ∨ q" "¬p ∨ ¬(¬q)" "¬(p ∧ ¬q)"
expect_holds table "¬q" "p ∧ ¬q" "¬(p ∧ ¬q)" "p → q"
expect_holds equiv "¬p → q" "p ∨ q"
expect_fails equiv "¬p → q" "p → q"
expect_holds equiv "q ∧ ¬q" "F"
expect_holds argument "(p ∧ ¬q) → (q ∧ ¬q)" --conclusion "p → q"
expect_holds argument "p → q" "p ∧ ¬q" --conclusion "q ∧ ¬q"
expect_holds argument "¬(p ∧ ¬q)" --conclusion "p → q"

echo "===== 4 수학적 귀납법: 긍정논법의 사슬 ====="
expect_holds argument "p1" "p1 → p2" --conclusion "p2"
expect_holds argument "p1" "p1 → p2" "p2 → p3" "p3 → p4" --conclusion "p4"
expect_fails argument "p1 → p2" "p2 → p3" "p3 → p4" --conclusion "p4"

echo "기대와 다른 결과: $failures"
exit $failures
