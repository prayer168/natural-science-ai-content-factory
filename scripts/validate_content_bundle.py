#!/usr/bin/env python3
"""Deterministically validate a local Canonical/Kahoot/Wayground/Wordwall review bundle."""
import argparse
import csv
import json
from pathlib import Path


REQUIRED_QUESTION_FIELDS = (
    "id", "grade", "unit", "activity", "learning_objective", "curriculum_alignment", "phase",
    "cognitive_level", "difficulty", "canonical_type", "stem", "options",
    "correct_answer", "explanation", "misconception", "remediation",
    "evidence_required", "source_note", "sources", "verification_status",
    "kahoot_adapter", "wayground_adapter",
)
PHASES = {"diagnosis", "inquiry", "ai_evidence", "differentiation"}
STATUSES = {"draft", "needs_review", "verified", "blocked"}
PLATFORM_STATUSES = {"supported", "unknown", "manual_required"}
CANONICAL_TYPES = {"single_choice", "multi_select", "true_false", "fill_blank", "reorder",
                   "categorize", "match", "data_interpretation", "image_question", "hotspot",
                   "labeling", "open_response", "passage_set", "experiment_design"}
NO_FIXED_ANSWER_TYPES = {"open_response", "experiment_design"}


def _load_json(path, errors):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"無法讀取 {path.name}：{exc}")
        return None


def _read_csv(path, errors):
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))
    except (OSError, csv.Error) as exc:
        errors.append(f"無法讀取 {path.name}：{exc}")
        return None


def _int_list(value):
    return isinstance(value, list) and all(type(item) is int for item in value)


def _platform_file(bundle, platform, manifest, legacy_name):
    candidates = [
        bundle / path for path in (manifest.get("outputs") or [])
        if isinstance(path, str) and path.startswith(f"{platform}/") and path.lower().endswith(".csv")
    ]
    if candidates and candidates[0].is_file():
        return candidates[0]
    legacy = bundle / legacy_name
    if legacy.is_file():
        return legacy
    nested = sorted((bundle / platform).glob("*.csv")) if (bundle / platform).is_dir() else []
    return nested[0] if len(nested) == 1 else bundle / platform / legacy_name


def validate(bundle):
    bundle = Path(bundle)
    errors, warnings = [], []
    expected = ("canonical.json", "teacher-notes.md", "batch-manifest.json")
    for filename in expected:
        if not (bundle / filename).is_file():
            errors.append(f"缺少必要檔案：{filename}")

    questions = _load_json(bundle / "canonical.json", errors) if (bundle / "canonical.json").is_file() else None
    if not isinstance(questions, list) or not questions:
        if questions is not None:
            errors.append("canonical.json 必須是非空題目陣列")
        questions = []
    manifest_path = bundle / "batch-manifest.json"
    manifest = {}
    if manifest_path.is_file():
        manifest = _load_json(manifest_path, errors)
        if not isinstance(manifest, dict):
            errors.append("batch-manifest.json 必須是 JSON 物件")
        elif manifest.get("question_count") != len(questions):
            errors.append("batch-manifest.json 的 question_count 與 Canonical 題數不一致")

    ids = set()
    expected_ids = []
    expected_kahoot = {}
    expected_wayground = {}
    for index, q in enumerate(questions, 1):
        where = f"第 {index} 題"
        if not isinstance(q, dict):
            errors.append(f"{where}不是 JSON 物件")
            continue
        missing = [key for key in REQUIRED_QUESTION_FIELDS if key not in q]
        if missing:
            errors.append(f"{where}缺少欄位：{', '.join(missing)}")

        qid = q.get("id")
        if not isinstance(qid, str) or not qid.strip():
            errors.append(f"{where}的 id 必須是非空文字")
        elif qid in ids:
            errors.append(f"題目 ID 重複：{qid}")
        else:
            ids.add(qid)
            expected_ids.append(qid)

        for field in ("unit", "activity", "learning_objective", "stem", "explanation",
                      "misconception", "remediation", "evidence_required", "source_note"):
            if not isinstance(q.get(field), str) or not q[field].strip():
                errors.append(f"{qid or where}：{field} 不可空白")
        if type(q.get("grade")) is not int or not 1 <= q["grade"] <= 9:
            errors.append(f"{qid or where}：grade 須為 1–9 的整數")
        if q.get("phase") not in PHASES:
            errors.append(f"{qid or where}：phase 無效")
        if q.get("canonical_type") not in CANONICAL_TYPES:
            errors.append(f"{qid or where}：canonical_type 無效")
        for field in ("cognitive_level", "difficulty"):
            if not isinstance(q.get(field), str) or not q[field].strip():
                errors.append(f"{qid or where}：{field} 不可空白")
        if q.get("verification_status") != "verified":
            errors.append(f"{qid or where}：verification_status 必須是 verified")

        sources = q.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{qid or where}：至少需要一筆逐題查證來源")
        else:
            for source in sources:
                if not isinstance(source, dict) or not all(
                    isinstance(source.get(key), str) and source[key].strip()
                    for key in ("title", "url", "supports")
                ) or not source.get("url", "").startswith("https://"):
                    errors.append(f"{qid or where}：來源需含 title、https URL 與 supports 主張")
                    break

        options = q.get("options")
        answers = q.get("correct_answer")
        if (not isinstance(options, list) or any(not isinstance(opt, str) or not opt.strip() for opt in options)
                or (not options and q.get("canonical_type") not in NO_FIXED_ANSWER_TYPES)):
            errors.append(f"{qid or where}：options 必須是非空白文字陣列；開放作答題型可留空")
            options = []
        if not _int_list(answers):
            errors.append(f"{qid or where}：correct_answer 必須是 1 起算整數索引陣列")
            answers = []
        elif len(set(answers)) != len(answers):
            errors.append(f"{qid or where}：correct_answer 不可重複")
        elif any(answer < 1 or answer > len(options) for answer in answers):
            errors.append(f"{qid or where}：correct_answer 超出選項範圍")
        elif q.get("canonical_type") not in NO_FIXED_ANSWER_TYPES and not answers:
            errors.append(f"{qid or where}：此題型必須有正確答案索引")
        if q.get("canonical_type") == "single_choice" and len(answers) != 1:
            errors.append(f"{qid or where}：single_choice 必須且只能有一個正解")
        if q.get("canonical_type") == "true_false" and (len(options) != 2 or len(answers) != 1):
            errors.append(f"{qid or where}：true_false 必須有兩個選項及一個正解")

        for platform in ("kahoot", "wayground"):
            adapter = q.get(f"{platform}_adapter")
            if not isinstance(adapter, dict) or not adapter.get("target_type"):
                errors.append(f"{qid or where}：缺少 {platform} adapter 題型")
            elif adapter.get("support_status", "supported") not in PLATFORM_STATUSES:
                errors.append(f"{qid or where}：{platform} support_status 無效")
            elif adapter.get("support_status", "supported") != "supported":
                warnings.append(f"{qid or where}：{platform} 需要人工處理或平台支援仍未知")
        wayground = q.get("wayground_adapter")
        if isinstance(wayground, dict) and not wayground.get("fallback_type"):
            errors.append(f"{qid or where}：Wayground adapter 缺少 fallback_type")

        if isinstance(qid, str):
            expected_kahoot[qid] = (q.get("stem"), options, answers)
            expected_wayground[qid] = (q.get("stem"), options, answers,
                                       (q.get("wayground_adapter") or {}).get("target_type"),
                                       (q.get("wayground_adapter") or {}).get("fallback_type"))

    kahoot_path = _platform_file(bundle, "Kahoot", manifest, "kahoot-ready.csv")
    wayground_path = _platform_file(bundle, "Wayground", manifest, "wayground-ready.csv")
    if not kahoot_path.is_file():
        errors.append(f"缺少必要檔案：{kahoot_path.relative_to(bundle) if kahoot_path.is_relative_to(bundle) else kahoot_path.name}")
    if not wayground_path.is_file():
        errors.append(f"缺少必要檔案：{wayground_path.relative_to(bundle) if wayground_path.is_relative_to(bundle) else wayground_path.name}")
    kahoot_rows = _read_csv(kahoot_path, errors) if kahoot_path.is_file() else None
    wayground_rows = _read_csv(wayground_path, errors) if wayground_path.is_file() else None

    def check_rows(rows, platform):
        if rows is None:
            return
        seen = set()
        for row in rows:
            qid = row.get("id")
            expected = (expected_kahoot if platform == "Kahoot" else expected_wayground).get(qid)
            if qid in seen:
                errors.append(f"{platform} CSV 有重複題目：{qid}")
            seen.add(qid)
            if expected is None:
                errors.append(f"{platform} CSV 出現 Canonical 不存在的題目：{qid}")
                continue
            if platform == "Kahoot":
                stem, options, answers = expected
                try:
                    csv_answers = [int(x) for x in row.get("correct_answer_numbers", "").split(",") if x]
                except ValueError:
                    csv_answers = []
                    errors.append(f"Kahoot 題目 {qid} 的正解索引無效")
                csv_options = [row.get(f"answer{i}", "") for i in range(1, 5)]
                if row.get("question") != stem or csv_options[:len(options)] != options:
                    errors.append(f"Kahoot 題目 {qid} 的題幹或選項與 Canonical 不一致")
                if csv_answers != answers:
                    errors.append(f"Kahoot 題目 {qid} 的正解與 Canonical 不一致")
            else:
                stem, options, answers, target, fallback = expected
                try:
                    csv_options = json.loads(row.get("options_json", ""))
                    csv_answers = json.loads(row.get("correct_answer_json", ""))
                except json.JSONDecodeError:
                    csv_options, csv_answers = None, None
                if (row.get("question") != stem or csv_options != options or csv_answers != answers
                        or row.get("target_type") != target or row.get("fallback_type") != fallback):
                    errors.append(f"Wayground 題目 {qid} 與 Canonical 題庫不一致")
        missing_ids = set(expected_kahoot if platform == "Kahoot" else expected_wayground) - seen
        if missing_ids:
            errors.append(f"{platform} CSV 缺少題目：{', '.join(sorted(missing_ids))}")

    check_rows(kahoot_rows, "Kahoot")
    check_rows(wayground_rows, "Wayground")

    declared_wordwall = [
        bundle / path for path in (manifest.get("outputs") or [])
        if isinstance(path, str) and path.startswith("Wordwall/") and path.lower().endswith(".md")
    ]
    wordwall_path = next((path for path in declared_wordwall if path.is_file()), None)
    if declared_wordwall and wordwall_path is None:
        errors.append("manifest 宣告的 Wordwall 活動稿不存在")
    elif wordwall_path is not None:
        try:
            wordwall_text = wordwall_path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            errors.append(f"無法讀取 Wordwall 活動稿：{exc}")
        else:
            if "不是 Wordwall 官方匯入檔" not in wordwall_text:
                errors.append("Wordwall 活動稿缺少人工設計稿／非官方匯入檔聲明")
            for qid in expected_ids:
                if qid not in wordwall_text:
                    errors.append(f"Wordwall 活動稿缺少 Canonical ID：{qid}")
            for question in questions:
                qid = question.get("id")
                for source in question.get("sources") or []:
                    url = source.get("url") if isinstance(source, dict) else None
                    if url and url not in wordwall_text:
                        errors.append(f"Wordwall 活動稿 {qid} 缺少 Canonical 來源：{url}")

    if (bundle / "teacher-notes.md").is_file() and not (bundle / "teacher-notes.md").read_text(encoding="utf-8-sig").strip():
        errors.append("teacher-notes.md 不可為空")

    return errors, warnings, len(questions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, help="本機教材批次資料夾")
    args = parser.parse_args()
    bundle = Path(args.bundle).resolve()
    errors, warnings, count = validate(bundle)
    status = "AUTOMATED PASS — REVIEW REQUIRED" if not errors else "BLOCKED"
    report = [f"# 自動檢查報告：{status}", "", f"- 批次資料夾：`{bundle}`", f"- Canonical 題目數：{count}",
              "- 專業逐題複核：尚待技能確認；本程式不代替科學查證及評量審查"]
    if warnings:
        report += ["", "## 注意事項", *[f"- {item}" for item in warnings]]
    if errors:
        report += ["", "## 阻擋問題", *[f"- {item}" for item in errors]]
    else:
        report += ["", "## 阻擋問題", "- 無（仍須完成來源與專業逐題複核）"]
    (bundle / "自動檢查報告.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"{status}: {count} 題；報告：{bundle / '自動檢查報告.md'}")
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
