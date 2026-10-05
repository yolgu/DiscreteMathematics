"""문제집의 문항, 보기, 절을 나타내는 모델.

선택지의 글과 그 선택지를 판정하는 데 쓰는 값(payload)을 한 곳에 둔다.
문제집, 해설, 검증이 모두 이 모델만 읽으므로 선택지가 두 군데에서 어긋날 일이 없다.
"""

from __future__ import annotations

import html
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

P = TypeVar("P")

CHOICE_LABELS: tuple[str, ...] = ("①", "②", "③", "④", "⑤")


class Demand(Enum):
    """문항이 실제로 요구하는 수준."""

    FOUNDATION = "기초"
    VARIATION = "변형"
    CHALLENGE = "도전"


class Layout(Enum):
    """선택지를 한 줄에 몇 개씩 놓을지."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


@dataclass(frozen=True)
class Option(Generic[P]):
    payload: P
    text: str
    why_wrong: str = ""


def formula_option(formula: str, why_wrong: str = "") -> Option[str]:
    """논리식 선택지. 찍는 글과 판정하는 식이 같은 문자열이다."""
    return Option(formula, html.escape(formula), why_wrong)


@dataclass(frozen=True)
class Item(Generic[P]):
    number: int
    demand: Demand
    stem: str
    options: tuple[Option[P], ...]
    answer: int
    judge: Callable[[P], bool]
    solution: str
    layout: Layout

    def verdicts(self) -> list[bool]:
        return [self.judge(option.payload) for option in self.options]

    def answer_option(self) -> Option[P]:
        return self.options[self.answer - 1]


@dataclass(frozen=True)
class WorkedExample:
    title: str
    body: str
    check: Callable[[], bool]


Check = tuple[str, Callable[[], bool]]


@dataclass(frozen=True)
class Section:
    title: str
    summary: str
    # 섞어 풀기 묶음은 유형을 스스로 골라야 하므로 보기를 두지 않는다
    worked: WorkedExample | None
    items: tuple[Item, ...]
    note: str = ""
    # 해설 속 유도의 각 줄처럼, 선택지 판정 밖에서 확인해야 하는 사실
    checks: tuple[Check, ...] = ()
