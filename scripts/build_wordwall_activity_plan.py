#!/usr/bin/env python3
"""Create a traceable, manual Wordwall activity design from Canonical JSON."""

import argparse
import json
from pathlib import Path


ACTIVITY_LABELS = {
    "quiz": "測驗",
    "match": "配對",
    "group_sort": "分組分類",
    "random_wheel": "隨機轉盤",
    "other": "其他教學活動",
}


def _answers(question):
    options = question.get("options") or []
    indices = question.get("correct_answer") or []
    return [options[i - 1] for i in indices if isinstance(i, int) and 1 <= i <= len(options)]


def _sources(question):
    sources = question.get("sources") or []
    if not sources:
        return "待補來源；本題不可標記已查證。"
    return "<br>".join(
        f"[{source.get('title', '來源')}]({source.get('url', '')}) — "
        f"{source.get('supports', '支持主張待補')}"
        for source in sources
    )


def activity_for_question(question):
    adapter = question.get("wordwall_adapter") or {}
    explicit = adapter.get("activity_type")
    if explicit in ACTIVITY_LABELS:
        return explicit
    kind = question.get("canonical_type")
    if kind == "match":
        return "match"
    if kind == "categorize":
        return "group_sort"
    if kind in {"single_choice", "multi_select", "true_false", "fill_blank"}:
        return "quiz"
    if kind in {"open_response", "experiment_design"}:
        return "random_wheel"
    return "other"


def _steps(activity):
    return {
        "quiz": "教師在 Wordwall 中人工建立測驗項目，輸入題幹、選項、正解與回饋；逐項對照本稿及 Canonical ID。",
        "match": "教師人工建立兩側配對項目，依正解表逐組輸入配對；完成後逐項測試配對結果。",
        "group_sort": "教師人工建立分類組別與項目，依答案鍵放入正確組別；若稿件標示待補，先補足分類證據再建置。",
        "random_wheel": "教師人工建立轉盤提示項目，使用參考答案與來源引導口頭說明；此形式不取代需要評分的答案檢查。",
        "other": "教師依教學目標在 Wordwall 人工選擇合適活動形式；若目前版本沒有等價形式，停止並保留本稿。",
    }[activity]


def build_plan(questions, title="Wordwall 活動設計稿"):
    if not isinstance(questions, list) or not questions:
        raise ValueError("Canonical 題庫必須是非空題目陣列")
    unverified = [q.get("id", "未知 ID") for q in questions if q.get("verification_status") != "verified"]
    lines = [
        f"# {title}",
        "",
        "> 本文件是依 Canonical 母題庫整理的人工建置設計稿，不是 Wordwall 官方匯入檔。未核實平台當期活動功能與匯入規格；請勿宣稱可直接匯入或已發布。",
        "",
        f"- 活動項目數：{len(questions)}",
        f"- 科學／QA 狀態：{'待查核：' + '、'.join(unverified) if unverified else 'Canonical 題目均標記 verified；平台建置仍須教師逐項核對。'}",
        "- 來源原則：沿用各 Canonical 題目的逐題來源；不得以本活動稿取代來源查證。",
        "",
    ]
    for index, question in enumerate(questions, 1):
        activity = activity_for_question(question)
        adapter = question.get("wordwall_adapter") or {}
        answers = _answers(question)
        lines += [
            f"## {index}. {question.get('id', 'Canonical ID 待補')} — {ACTIVITY_LABELS[activity]}",
            "",
            f"- 學習目標：{question.get('learning_objective', '待補')}",
            f"- 題目／提示：{question.get('stem', '待補')}",
            f"- 項目：{'；'.join(adapter.get('items', question.get('options') or [question.get('stem', '待補')]))}",
            f"- 正解／配對：{'；'.join(adapter.get('answer_pairs', [])) if adapter.get('answer_pairs') else '、'.join(answers) if answers else '待教師依 Canonical 解析補足／核對'}",
            f"- 分類答案鍵：{json.dumps(adapter.get('groups', question.get('groups', '未提供；待教師補足')), ensure_ascii=False)}",
            f"- 解說／教師提示：{question.get('explanation', '待補')}",
            f"- 來源與支持主張：{_sources(question)}",
            f"- 題目查證狀態：{question.get('verification_status', '待確認')}",
            f"- 教師建置步驟：{_steps(activity)}",
            "",
        ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", required=True, help="Canonical JSON 題目陣列")
    parser.add_argument("--output", required=True, help="Wordwall 人工活動設計稿輸出路徑")
    parser.add_argument("--title", default="Wordwall 活動設計稿")
    args = parser.parse_args()
    questions = json.loads(Path(args.json).read_text(encoding="utf-8-sig"))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_plan(questions, args.title), encoding="utf-8")
    print(f"Wordwall 人工活動設計稿已產生：{output}")


if __name__ == "__main__":
    main()
