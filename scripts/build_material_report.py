#!/usr/bin/env python3
"""Build one traceable Markdown report from a generated material batch."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from build_wordwall_activity_plan import ACTIVITY_LABELS, activity_for_question


TYPE_LABELS = {
    "single_choice": "單選題",
    "multi_select": "多選題",
    "true_false": "是非題",
    "fill_blank": "填空題",
    "reorder": "排序題",
    "categorize": "分類題",
    "match": "配對題",
    "data_interpretation": "資料判讀題",
    "image_question": "圖像題",
    "hotspot": "圖像熱點題",
    "labeling": "標示題",
    "open_response": "開放作答題",
    "passage_set": "閱讀組題",
    "experiment_design": "實驗設計題",
}

FILE_PURPOSES = {
    "canonical.json": "平台中立母題庫（答案索引 1 起算）",
    "Kahoot/kahoot-ready.csv": "Kahoot 檢閱素材；非官方匯入範本",
    "Wayground/wayground-ready.csv": "Wayground 檢閱素材；非官方匯入範本",
    "Wordwall/wordwall-activity-plan.md": "Wordwall 人工活動設計稿；非官方匯入檔",
    "teacher-notes.md": "教師答案、解析、迷思與補救建議",
    "batch-manifest.json": "單元範圍、日期、來源及課綱對照 metadata",
    "自動檢查報告.md": "結構與平台同步 hook 結果",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def md(value):
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def code_list(entries):
    if not entries:
        return "待補：manifest 尚未提供經核對的代碼"
    return "、".join(f"`{entry.get('code', '待補')}`" for entry in entries)


def code_table(title, entries):
    lines = [f"### {title}", "", "| 代碼 | 課綱文字 | 本教材對應 | 核對狀態 | 課綱來源 |", "|---|---|---|---|---|"]
    if not entries:
        return lines + ["| 待補 | 尚未提供代碼及課綱文字 | 不推定 | 待核對 | 待補 |", ""]
    for entry in entries:
        source = entry.get("source_url") or "待補"
        status = entry.get("status", "待核對")
        lines.append(
            f"| `{md(entry.get('code', '待補'))}` | {md(entry.get('description', '待補'))} | "
            f"{md(entry.get('alignment_note', '待補'))} | {md(status)} | {md(source)} |"
        )
    return lines + [""]


def build_report(batch):
    batch = batch.resolve()
    root_manifest_path = batch / "manifest.json"
    root_manifest = load_json(root_manifest_path) if root_manifest_path.is_file() else {}
    unit_dirs = sorted(
        path for path in batch.iterdir()
        if path.is_dir() and (path / "canonical.json").is_file()
    )
    if not unit_dirs:
        raise ValueError(f"找不到含 canonical.json 的單元資料夾：{batch}")

    generated = datetime.now().astimezone().isoformat(timespec="seconds")
    batch_date = root_manifest.get("build_date") or root_manifest.get("date") or "待補：manifest 未記錄建置日期"
    title = root_manifest.get("title") or batch.name
    upload_status = root_manifest.get("upload_status") or root_manifest.get("platform_upload_status") or "待確認"
    units = []
    for folder in unit_dirs:
        unit_manifest_path = folder / "batch-manifest.json"
        manifest = load_json(unit_manifest_path) if unit_manifest_path.is_file() else {}
        root_unit = next(
            (item for item in root_manifest.get("units", []) if item.get("folder") == folder.name),
            {},
        )
        first_question = load_json(folder / "canonical.json")[0]
        manifest = {**root_unit, **manifest}
        manifest.setdefault("grade", first_question.get("grade"))
        manifest.setdefault("semester", "上學期" if "上" in " ".join(manifest.get("activities", [])) else "待補")
        manifest.setdefault("unit", first_question.get("unit"))
        manifest.setdefault("publisher", root_unit.get("publisher"))
        questions = load_json(folder / "canonical.json")
        if not isinstance(questions, list):
            raise ValueError(f"canonical.json 必須是 JSON 陣列：{folder}")
        if not questions:
            raise ValueError(f"canonical.json 不可為空：{folder}")
        auto_path = folder / "自動檢查報告.md"
        manual_path = folder / "驗證報告.md"
        auto_text = auto_path.read_text(encoding="utf-8-sig") if auto_path.is_file() else ""
        manual_text = manual_path.read_text(encoding="utf-8-sig") if manual_path.is_file() else ""
        auto_pass = "AUTOMATED PASS" in auto_text
        manual_pass = manual_text.lstrip().startswith("# 驗證報告：PASS")
        item_types = Counter(q.get("canonical_type", "unknown") for q in questions)
        difficulty = Counter(q.get("difficulty", "待補") for q in questions)
        source_count = sum(bool(q.get("sources")) for q in questions)
        platforms = {}
        for platform, key in (("Kahoot", "kahoot_adapter"), ("Wayground", "wayground_adapter")):
            platforms[platform] = Counter((q.get(key) or {}).get("target_type", "待補") for q in questions)
        wordwall_activities = Counter(ACTIVITY_LABELS[activity_for_question(q)] for q in questions)
        units.append({
            "folder": folder,
            "manifest": manifest,
            "questions": questions,
            "auto_pass": auto_pass,
            "manual_pass": manual_pass,
            "item_types": item_types,
            "difficulty": difficulty,
            "source_count": source_count,
            "platforms": platforms,
            "wordwall_activities": wordwall_activities,
        })

    all_auto = all(unit["auto_pass"] for unit in units)
    all_manual = all(unit["manual_pass"] for unit in units)
    status = "驗證通過" if all_auto and all_manual else "待驗證／有未通過項目"
    lines = [
        f"# 教材建置報告：{title}", "",
        f"- 批次名稱：`{md(batch.name)}`",
        f"- 批次建置日期：{md(batch_date)}（依 manifest；不是本報告的產生日期）",
        f"- 報告產生時間：{generated}",
        f"- 本機批次位置：`{batch}`",
        f"- 教材／驗證狀態：**{status}**（自動 hook：{'六單元全部 PASS' if all_auto else '有缺漏或未通過'}；逐題複核：{'六單元全部 PASS' if all_manual else '有缺漏或未通過'}）",
        f"- 平台發布狀態：{md(upload_status)}；除非列出可重開資源網址／ID，否則不視為已上傳。",
        "",
        "> 課綱代碼只從 manifest 明列的官方對照資料輸出；缺少證據時標示待核對。難易度是本批題庫標籤，不是官方難度等級。平台 CSV 是檢閱輸出，除非另有當期官方範本驗證，不代表可直接匯入。",
        "",
        "## 批次教材摘要", "",
        "| 教材名稱 | 建置日期 | 年級／學期／版本 | 題數 | Canonical 題型 | 難度分布 | Wordwall 活動稿類型 | 學習內容代碼 | 學習表現代碼 | 驗證 | 本機位置 |",
        "|---|---|---|---:|---|---|---|---|---|---|---|",
    ]

    for unit in units:
        manifest = unit["manifest"]
        qs = unit["questions"]
        mapping = manifest.get("curriculum_mapping") or {}
        content = mapping.get("learning_content", [])
        performance = mapping.get("learning_performance", [])
        unit_title = manifest.get("material_title") or f"四年級上學期自然｜{manifest.get('publisher', '版本待補')}｜{manifest.get('unit', '單元待補')}｜10題單選評量"
        date = manifest.get("build_date") or batch_date
        level = f"{manifest.get('grade', '年級待補')}年級／{manifest.get('semester', '學期待補')}／{manifest.get('publisher', '版本待補')}"
        types = "、".join(f"{TYPE_LABELS.get(k, k)} {v} 題" for k, v in sorted(unit["item_types"].items()))
        diffs = "、".join(f"{k} {v} 題" for k, v in sorted(unit["difficulty"].items()))
        wordwall_types = "、".join(f"{k} {v} 項" for k, v in sorted(unit["wordwall_activities"].items()))
        checks = f"AUTO {'PASS' if unit['auto_pass'] else '待確認'}／MANUAL {'PASS' if unit['manual_pass'] else '待確認'}"
        lines.append(
            f"| {md(unit_title)} | {md(date)} | {md(level)} | {len(qs)} | {md(types)} | {md(diffs)} | {md(wordwall_types)} | "
            f"{code_list(content)} | {code_list(performance)} | {checks} | `{unit['folder']}` |"
        )

    lines += ["", "## 單元建置與查證紀錄", ""]
    for index, unit in enumerate(units, 1):
        folder, manifest, questions = unit["folder"], unit["manifest"], unit["questions"]
        mapping = manifest.get("curriculum_mapping") or {}
        unit_title = manifest.get("material_title") or f"四年級上學期自然｜{manifest.get('publisher', '版本待補')}｜{manifest.get('unit', '單元待補')}｜10題單選評量"
        lines += [
            f"### {index}. {unit_title}", "",
            f"- 建置日期：{md(manifest.get('build_date') or batch_date)}",
            f"- 教材名稱／檔名：{md(manifest.get('material_title', unit_title))}；Canonical：`canonical.json`；題目 ID：`{md(questions[0].get('id', ''))}`–`{md(questions[-1].get('id', ''))}`。",
            f"- 年級／學期／出版社版本：{md(manifest.get('grade', '待補'))}年級／{md(manifest.get('semester', '待補'))}／{md(manifest.get('publisher', '待補'))}。",
            f"- 單元／活動：{md(manifest.get('unit', '待補'))}／{md('、'.join(manifest.get('activity_scope', [])) or '待補')}。",
            f"- 題數與題型：{len(questions)} 題；" + "、".join(f"{TYPE_LABELS.get(k, k)} {v} 題" for k, v in sorted(unit["item_types"].items())) + "。",
            f"- 難易度分布：" + "、".join(f"{k} {v} 題" for k, v in sorted(unit["difficulty"].items())) + "（依 Canonical difficulty 欄位統計）。",
            f"- Kahoot 題型：" + "、".join(f"{k} {v} 題" for k, v in sorted(unit["platforms"]["Kahoot"].items())) + "；Wayground 題型：" + "、".join(f"{k} {v} 題" for k, v in sorted(unit["platforms"]["Wayground"].items())) + "。",
            f"- Wordwall 活動設計建議：" + "、".join(f"{k} {v} 項" for k, v in sorted(unit["wordwall_activities"].items())) + "；僅為人工建置稿，不代表已確認平台支援或已上傳。",
            f"- 存放位置：`{folder}`",
            f"- 來源覆蓋：{unit['source_count']}/{len(questions)} 題有逐題來源記錄。",
            f"- 程式 hook：{'PASS' if unit['auto_pass'] else '待確認／未通過'}（`自動檢查報告.md`）；逐題科學與評量複核：{'PASS' if unit['manual_pass'] else '待確認／未通過'}（`驗證報告.md`）。",
            "",
        ]
        lines += code_table("課綱學習內容", mapping.get("learning_content", []))
        lines += code_table("課綱學習表現", mapping.get("learning_performance", []))
        lines += [
            f"**對照方法與限制：** {md(mapping.get('mapping_note', '待補：尚未記錄對照方法。'))}", "",
            "#### 題目、來源與課綱索引", "",
            "| 題目 ID | 題目名稱／題幹 | Canonical 題型／難度 | 學習內容代碼 | 學習表現代碼 | 來源與支持主張 | 狀態 |",
            "|---|---|---|---|---|---|---|",
        ]
        for q in questions:
            q_sources = "<br>".join(
                f"[{md(src.get('title', '來源待補'))}]({src.get('url', '')})：{md(src.get('supports', '支持主張待補'))}"
                for src in q.get("sources", [])
            ) or "來源待補"
            q_content = q.get("learning_content_codes") or [entry.get("code", "待補") for entry in mapping.get("learning_content", [])]
            q_performance = q.get("learning_performance_codes") or [entry.get("code", "待補") for entry in mapping.get("learning_performance", [])]
            item_status = "來源與題目狀態已記錄" if q.get("verification_status") == "verified" else q.get("verification_status", "待確認")
            lines.append(
                f"| `{md(q.get('id', ''))}` | {md(q.get('stem', ''))} | {TYPE_LABELS.get(q.get('canonical_type'), q.get('canonical_type', '待補'))}／{md(q.get('difficulty', '待補'))} | "
                f"{', '.join(f'`{md(code)}`' for code in q_content)} | {', '.join(f'`{md(code)}`' for code in q_performance)} | {q_sources} | {md(item_status)} |"
            )
        lines += ["", "#### 檔案清冊與完整性指紋", "", "| 檔名 | 用途 | 絕對位置 | 大小（bytes） | SHA-256 |", "|---|---|---|---:|---|"]
        for filename, purpose in FILE_PURPOSES.items():
            path = folder / filename
            if not path.is_file() and filename.startswith(("Kahoot/", "Wayground/", "Wordwall/")):
                platform = filename.split("/", 1)[0]
                suffix = ".md" if platform == "Wordwall" else ".csv"
                declared = [
                    folder / relative for relative in manifest.get("outputs", [])
                    if isinstance(relative, str) and relative.startswith(f"{platform}/") and relative.lower().endswith(suffix)
                ]
                if declared and declared[0].is_file():
                    path = declared[0]
                    filename = str(path.relative_to(folder))
            if not path.is_file() and filename.startswith(("Kahoot/", "Wayground/")):
                legacy = folder / Path(filename).name
                if legacy.is_file():
                    path = legacy
            if path.is_file():
                lines.append(f"| `{filename}` | {purpose} | `{path.resolve()}` | {path.stat().st_size} | `{sha256(path)}` |")
            elif filename.startswith("Wordwall/") and not any(
                isinstance(relative, str) and relative.startswith("Wordwall/")
                for relative in manifest.get("outputs", [])
            ):
                lines.append(f"| `{filename}` | {purpose} | `{path.resolve()}` | 舊版批次未產生 | — |")
            else:
                lines.append(f"| `{filename}` | {purpose} | `{path.resolve()}` | 缺檔 | 缺檔 |")
        revision_history = manifest.get("revision_history", [])
        lines += ["", "#### 修訂紀錄", ""]
        if revision_history:
            lines += ["| 日期 | 檔案 | 修訂內容 | 修訂後驗證 |", "|---|---|---|---|"]
            for entry in revision_history:
                lines.append(f"| {md(entry.get('date', '待補'))} | {md(entry.get('files', '待補'))} | {md(entry.get('change', '待補'))} | {md(entry.get('verification', '待補'))} |")
        else:
            lines.append("目前 manifest 未記錄修訂事件；若本報告在後續修訂後更新，請先將修訂追加至 `revision_history`。")
        lines += ["", "---", ""]

    lines += [
        "## 批次來源、版本與限制", "",
        f"- 課程地圖：{md(root_manifest.get('course_map', '未記錄'))}",
        f"- 課綱文件：{md(root_manifest.get('curriculum_source', '各單元 manifest 所列來源；未填者視為待核對'))}",
        f"- 平台狀態：{md(upload_status)}。本報告不會把平台檢閱 CSV 推定為官方匯入檔，也不會把尚未確認的資源列成已上傳。",
        f"- 報告程式：`scripts/build_material_report.py`；來源檔案雜湊可用於辨認本報告所列的輸出版本。",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", required=True, help="包含各單元 bundle 的批次資料夾")
    parser.add_argument("--output", help="輸出報告路徑；預設為批次資料夾/教材建置報告.md")
    args = parser.parse_args()
    batch = Path(args.batch).resolve()
    output = Path(args.output).resolve() if args.output else batch / "教材建置報告.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(batch), encoding="utf-8")
    print(f"教材建置報告已產生：{output}")


if __name__ == "__main__":
    main()
