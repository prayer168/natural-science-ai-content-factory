#!/usr/bin/env python3
"""Create platform-ready review files from Canonical JSON.

This script intentionally does NOT claim to create the latest official import XLSX.
Official templates change; use the current template adapter at export time.
"""
import argparse, csv, json, subprocess, sys
from pathlib import Path
from build_wordwall_activity_plan import build_plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--filename-stem", help="依素材編號、學年度、年級、學期、版本、單元、日期組成的檔名，不含副檔名")
    args = ap.parse_args()
    items = json.loads(Path(args.json).read_text(encoding="utf-8"))
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    kahoot_dir, wayground_dir, wordwall_dir = (out / name for name in ("Kahoot", "Wayground", "Wordwall"))
    for directory in (kahoot_dir, wayground_dir, wordwall_dir):
        directory.mkdir(parents=True, exist_ok=True)
    stem = args.filename_stem
    kahoot_name = f"{stem}.csv" if stem else "kahoot-ready.csv"
    wayground_name = f"{stem}.csv" if stem else "wayground-ready.csv"
    wordwall_name = f"{stem}.md" if stem else "wordwall-activity-plan.md"
    (out / "canonical.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    with (kahoot_dir / kahoot_name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","question","answer1","answer2","answer3","answer4","correct_answer_numbers","time_limit","manual_step"])
        for q in items:
            a = q.get("kahoot_adapter", {})
            opts = (q.get("options") or []) + [""] * 4
            correct = q.get("correct_answer", [])
            # Canonical examples use one-based answer indexes (e.g. [2]);
            # support legacy string answers without silently emitting blanks.
            if not correct:
                correct = q.get("correct_answer_numbers", [])
            if not correct and q.get("correct_answer_number") is not None:
                correct = [q["correct_answer_number"]]
            w.writerow([q.get("id"), q.get("stem"), *opts[:4], ",".join(map(str,correct)), a.get("time_limit",20), a.get("manual_step_if_needed","")])

    with (wayground_dir / wayground_name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","target_type","fallback_type","question","options_json","correct_answer_json","teacher_note","manual_step"])
        for q in items:
            a = q.get("wayground_adapter", {})
            w.writerow([q.get("id"), a.get("target_type"), a.get("fallback_type"), q.get("stem"), json.dumps(q.get("options",[]), ensure_ascii=False), json.dumps(q.get("correct_answer",[]), ensure_ascii=False), a.get("teacher_note",""), a.get("manual_step_if_needed","")])

    md = ["# 教師解析\n"]
    for q in items:
        md += [f"## {q.get('id')}\n", f"**題目：** {q.get('stem','')}\n", f"**解析：** {q.get('explanation','')}\n", f"**主要迷思：** {q.get('misconception','')}\n", f"**補救：** {q.get('remediation','')}\n"]
    (out / "teacher-notes.md").write_text("\n".join(md), encoding="utf-8")
    (wordwall_dir / wordwall_name).write_text(build_plan(items, out.name), encoding="utf-8")
    manifest = {
        "batch_name": out.name,
        "question_count": len(items),
        "activities": sorted({f"{q.get('grade')}年級／{q.get('unit')}／{q.get('activity')}" for q in items}),
        "outputs": ["canonical.json", f"Kahoot/{kahoot_name}", f"Wayground/{wayground_name}",
                    f"Wordwall/{wordwall_name}", "teacher-notes.md"],
        "platform_upload_status": "尚未上傳",
    }
    (out / "batch-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    validator = Path(__file__).with_name("validate_content_bundle.py")
    result = subprocess.run([sys.executable, str(validator), "--bundle", str(out)], check=False)
    status = "AUTOMATED PASS — PROFESSIONAL REVIEW REQUIRED" if result.returncode == 0 else "BLOCKED"
    print(f"Created review bundle in {out}; status={status}")
    return result.returncode

if __name__ == "__main__":
    raise SystemExit(main())
