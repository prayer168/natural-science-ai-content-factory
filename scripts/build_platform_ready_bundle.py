#!/usr/bin/env python3
"""Create platform-ready review files from Canonical JSON.

This script intentionally does NOT claim to create the latest official import XLSX.
Official templates change; use the current template adapter at export time.
"""
import argparse, csv, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()
    items = json.loads(Path(args.json).read_text(encoding="utf-8"))
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    (out / "canonical.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    with (out / "kahoot-ready.csv").open("w", encoding="utf-8-sig", newline="") as f:
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

    with (out / "wayground-ready.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","target_type","fallback_type","question","options_json","correct_answer_json","teacher_note","manual_step"])
        for q in items:
            a = q.get("wayground_adapter", {})
            w.writerow([q.get("id"), a.get("target_type"), a.get("fallback_type"), q.get("stem"), json.dumps(q.get("options",[]), ensure_ascii=False), json.dumps(q.get("correct_answer",[]), ensure_ascii=False), a.get("teacher_note",""), a.get("manual_step_if_needed","")])

    md = ["# 教師解析\n"]
    for q in items:
        md += [f"## {q.get('id')}\n", f"**題目：** {q.get('stem','')}\n", f"**解析：** {q.get('explanation','')}\n", f"**主要迷思：** {q.get('misconception','')}\n", f"**補救：** {q.get('remediation','')}\n"]
    (out / "teacher-notes.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Created bundle in {out}")

if __name__ == "__main__":
    main()
