"""2장 증명 문제집과 해설의 HTML을 만든다.

먼저 모든 문항의 선택지 판정과 해설 속 확인을 돌린다. 하나라도 어긋나면 HTML을 쓰지 않고 종료 코드 1로 끝난다.
검증 결과는 검증_결과.txt에 남긴다.
"""

from __future__ import annotations

import html
import sys
from collections import Counter
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

from items_a import SECTION_A
from items_b import SECTION_B
from items_c import SECTION_C
from items_d import SECTION_D
from items_e import SECTION_E
from items_f import SECTION_F
from logic_check import FormulaError
from logic_tools import equivalent, parse
from model import CHOICE_LABELS, Demand, Item, Section
from proof_methods import METHOD_CHECKS

HERE: Path = Path(__file__).resolve().parent

# 묶음 번호가 교과서 절 번호와 달라서, 묶음마다 교과서의 어느 부분을 다루는지 함께 둔다.
SECTION_SOURCES: tuple[tuple[Section, str], ...] = (
    (SECTION_A, "1. 증명의 정의, 2. 직접증명법"),
    (SECTION_B, "3-1) 대우증명법"),
    (SECTION_C, "3-2) 모순증명법"),
    (SECTION_D, "3-3) 반례증명법과 존재증명법"),
    (SECTION_E, "4. 수학적 귀납법"),
    (SECTION_F, "1~4 전체"),
)
SECTIONS: tuple[Section, ...] = tuple(section for section, _ in SECTION_SOURCES)
REVISIT_SECTION: Section = SECTION_F

WORKBOOK_TITLE: str = "2장 증명 문제집"
ANSWER_KEY_TITLE: str = "2장 증명 해설"
WORKBOOK_HTML: Path = HERE / "문제집.html"
ANSWER_KEY_HTML: Path = HERE / "해설.html"
REPORT: Path = HERE / "검증_결과.txt"

# 교과서 HTML과 같은 KaTeX 설정. errorColor는 print_pdf.py가 그리지 못한 수식을 찾는 표지다.
KATEX_HEAD: str = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {delimiters: [{left: '\\\\[', right: '\\\\]', display: true}, {left: '\\\\(', right: '\\\\)', display: false}], throwOnError: false, errorColor: '#cc0001', output: 'html'})"></script>
<link rel="stylesheet" href="textbook.css">
<link rel="stylesheet" href="workbook.css">
"""


# ---- 검증 ----

@dataclass
class Verification:
    lines: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def record(self, passed: bool, description: str) -> None:
        self.lines.append(f"{'통과' if passed else '실패'}  {description}")
        if not passed:
            self.failures.append(description)

    def note(self, description: str) -> None:
        self.lines.append(f"참고  {description}")


def all_items() -> list[Item]:
    return [item for section in SECTIONS for item in section.items]


def verify() -> Verification:
    verification: Verification = Verification()
    items: list[Item] = all_items()
    verification.record(
        [item.number for item in items] == list(range(1, len(items) + 1)),
        f"문제 번호가 1부터 {len(items)}까지 빠짐없이 이어짐",
    )
    for description, passed in METHOD_CHECKS:
        verification.record(passed, description)
    for item in items:
        verify_item(item, verification)
    for section in SECTIONS:
        if section.worked is not None:
            verification.record(section.worked.check(), section.worked.title)
        for description, check in section.checks:
            verification.record(check(), description)

    positions: Counter[int] = Counter(item.answer for item in items)
    verification.note("정답 위치: " + ", ".join(f"{label} {positions[index]}개" for index, label in enumerate(CHOICE_LABELS, start=1)))
    demands: Counter[Demand] = Counter(item.demand for item in items)
    verification.note("수준: " + ", ".join(f"{demand.value} {demands[demand]}개" for demand in Demand))
    return verification


def verify_item(item: Item, verification: Verification) -> None:
    verdicts: list[bool] = item.verdicts()
    shown: str = " ".join("T" if verdict else "F" for verdict in verdicts)
    verification.record(
        len(item.options) == len(CHOICE_LABELS) and verdicts.count(True) == 1 and verdicts[item.answer - 1],
        f"문제 {item.number}: 맞는 선택지는 {CHOICE_LABELS[item.answer - 1]} 하나뿐 ({shown})",
    )
    verification.record(
        all(bool(option.why_wrong) == (index != item.answer) for index, option in enumerate(item.options, start=1)),
        f"문제 {item.number}: 틀린 선택지 넷에만 틀린 까닭이 있음",
    )
    for first, second in combinations(formula_payloads(item), 2):
        if equivalent(first, second):
            verification.note(f"문제 {item.number}: 선택지 {first}와 {second}는 서로 동치")


def formula_payloads(item: Item) -> list[str]:
    """찍는 글이 곧 판정하는 식인 선택지(formula_option)의 식. 뜻이 겹치는 선택지를 찾는 데 쓴다."""
    return [
        option.payload
        for option in item.options
        if isinstance(option.payload, str) and option.text == html.escape(option.payload) and is_formula(option.payload)
    ]


def is_formula(text: str) -> bool:
    try:
        parse(text)
    except FormulaError:
        return False
    return True


# ---- 문제집과 해설 HTML ----

def document(title: str, body: str) -> str:
    return (
        '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        f"<title>{title}</title>\n{KATEX_HEAD}</head>\n<body>\n{body}\n</body>\n</html>\n"
    )


def number_range(section: Section) -> str:
    return f"{section.items[0].number}~{section.items[-1].number}번"


def item_side(item: Item) -> str:
    return (
        f'<div class="item-side"><span class="item-number">{item.number}</span>'
        f'<span class="demand">{item.demand.value}</span></div>'
    )


def choices_html(item: Item) -> str:
    rows: str = "".join(
        f'<li><span class="choice-label">{label}</span><span>{option.text}</span></li>'
        for label, option in zip(CHOICE_LABELS, item.options)
    )
    return f'<ol class="choices {item.layout.value}">{rows}</ol>'


def workbook_item(item: Item) -> str:
    return (
        f'<div class="item">{item_side(item)}<div class="item-body">'
        f'{item.stem}{choices_html(item)}<div class="work-space"></div></div></div>'
    )


def workbook_section(section: Section) -> str:
    parts: list[str] = [f'<section class="part">\n<h2>{section.title}</h2>']
    if section.summary:
        parts.append(f'<div class="summary"><p class="summary-title">핵심 정리</p>{section.summary}</div>')
    if section.note:
        parts.append(f'<div class="note"><p class="note-title">풀기 전에</p><p>{section.note}</p></div>')
    if section.worked is not None:
        parts.append(f'<div class="example"><p class="example-title">{section.worked.title}</p>{section.worked.body}</div>')
    parts.extend(workbook_item(item) for item in section.items)
    parts.append("</section>")
    return "\n".join(parts)


def workbook_cover() -> str:
    coverage: str = "".join(
        f"<tr><td>{section.title}</td><td>{source}</td><td>{number_range(section)}</td></tr>"
        for section, source in SECTION_SOURCES
    )
    return f"""<section class="cover">
<h1>{WORKBOOK_TITLE}</h1>
<p class="cover-sub">이산수학 교과서 2장의 내용을, 다섯 선택지 가운데 하나를 고르는 문제 {len(all_items())}개로 연습합니다.</p>
<h2>다루는 범위</h2>
<table class="prose-table"><thead><tr><th>묶음</th><th>교과서</th><th>문제</th></tr></thead><tbody>{coverage}</tbody></table>
<h2>풀기 전에 알아 둘 것</h2>
<ul>
  <li>교과서 2장을 한 번 읽었다고 보고 시작합니다. 문제에 필요한 정의와 증명법은 묶음마다 핵심 정리에 다시 모아 두었습니다.</li>
  <li>묶음 번호는 교과서의 절 번호와 다릅니다. 위 표에서 묶음마다 교과서의 어느 부분을 다루는지 확인하세요.</li>
  <li>1장의 명제와 논리를 씁니다. 함축 p → q, 부정 ¬, 동치 ≡, 긍정논법 같은 추론 규칙이 나옵니다.</li>
  <li>\\(Z\\)는 정수 전체의 집합이고, \\(k \\in Z\\)는 '\\(k\\)는 정수'라는 뜻입니다. 자연수는 1, 2, 3, ⋯입니다.</li>
</ul>
<h2>푸는 방법</h2>
<ul>
  <li>각 문제에서 알맞은 답을 <strong>하나만</strong> 고르세요.</li>
  <li>묶음마다 핵심 정리와 보기를 먼저 읽으세요. 보기는 풀이까지 보여 주는 예제입니다. 문제는 보기와 닮은 것부터 시작해, 스스로 판단할 것이 차츰 늘어나는 순서로 놓았습니다.</li>
  <li>문제 번호 아래의 표시는 문제가 요구하는 수준입니다. 기초는 정의와 증명법을 그대로 쓰는 문제, 변형은 조건이나 표현이 바뀌어 방법을 골라야 하는 문제, 도전은 여러 단계를 이어야 하는 문제입니다.</li>
  <li>정답과 풀이는 따로 묶은 「{ANSWER_KEY_TITLE}」에 있습니다. 해설에는 틀린 선택지 넷이 왜 틀렸는지도 적었습니다.</li>
  <li>마지막 섞어 풀기({number_range(REVISIT_SECTION)})는 앞 문제를 다 풀고 며칠 지난 뒤, 해설을 보지 않고 풀어 보세요.</li>
</ul>
</section>"""


def workbook_body() -> str:
    return "\n".join([workbook_cover(), *(workbook_section(section) for section in SECTIONS)])


def answer_grid() -> str:
    items: list[Item] = all_items()
    rows: list[str] = []
    for start in range(0, len(items), 10):
        chunk: list[Item] = items[start:start + 10]
        rows.append("<tr>" + "".join(f"<th>{item.number}</th>" for item in chunk) + "</tr>")
        rows.append("<tr>" + "".join(f"<td>{CHOICE_LABELS[item.answer - 1]}</td>" for item in chunk) + "</tr>")
    return '<table class="answer-grid">' + "".join(rows) + "</table>"


def answer_key_item(item: Item) -> str:
    wrong_options: str = "".join(
        f'<li><span class="wrong-head"><span class="choice-label">{label}</span> {option.text}</span>{option.why_wrong}</li>'
        for index, (label, option) in enumerate(zip(CHOICE_LABELS, item.options), start=1)
        if index != item.answer
    )
    return (
        f'<div class="solution-item">{item_side(item)}<div class="item-body">'
        f'<div class="restated">{item.stem}</div>'
        f'<p class="answer-line"><strong>정답 {CHOICE_LABELS[item.answer - 1]}</strong> {item.answer_option().text}</p>'
        f'<p class="solution-label">풀이</p>{item.solution}'
        f'<p class="solution-label">다른 선택지</p><ul class="wrong-options">{wrong_options}</ul>'
        "</div></div>"
    )


def answer_key_section(section: Section) -> str:
    items: str = "\n".join(answer_key_item(item) for item in section.items)
    return f'<section class="part">\n<h2>{section.title}</h2>\n{items}\n</section>'


def answer_key_cover() -> str:
    return f"""<section class="cover">
<h1>{ANSWER_KEY_TITLE}</h1>
<p class="cover-sub">「{WORKBOOK_TITLE}」 {len(all_items())}문제의 정답과 풀이입니다. 문제마다 정답에 이르는 풀이를 먼저 적고, 이어서 나머지 선택지 넷이 왜 틀렸는지 적었습니다. 문제는 한 번 더 옮겨 적었습니다.</p>
<h2>정답 한눈에 보기</h2>
{answer_grid()}
</section>"""


def answer_key_body() -> str:
    return "\n".join([answer_key_cover(), *(answer_key_section(section) for section in SECTIONS)])


def main() -> int:
    verification: Verification = verify()
    REPORT.write_text("\n".join(verification.lines) + "\n", encoding="utf-8")
    notes: list[str] = [line for line in verification.lines if line.startswith("참고")]
    print("\n".join(notes))
    if verification.failures:
        print("검증 실패:")
        print("\n".join(f"  {failure}" for failure in verification.failures))
        return 1

    WORKBOOK_HTML.write_text(document(WORKBOOK_TITLE, workbook_body()), encoding="utf-8")
    ANSWER_KEY_HTML.write_text(document(ANSWER_KEY_TITLE, answer_key_body()), encoding="utf-8")
    passed: int = sum(line.startswith("통과") for line in verification.lines)
    print(f"검증 {passed}개 모두 통과. {WORKBOOK_HTML.name}, {ANSWER_KEY_HTML.name}를 만들었습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
