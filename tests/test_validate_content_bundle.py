import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "items-example.json"
BUILDER = ROOT / "scripts" / "build_platform_ready_bundle.py"


class BundleValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.bundle = Path(self.temp.name) / "batch"
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--json", str(SAMPLE), "--outdir", str(self.bundle)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(result.returncode, 0, (result.stdout or "") + (result.stderr or ""))

    def tearDown(self):
        self.temp.cleanup()

    def test_generated_bundle_passes_automatic_checks_but_requires_review(self):
        report = (self.bundle / "自動檢查報告.md").read_text(encoding="utf-8")
        self.assertIn("AUTOMATED PASS — REVIEW REQUIRED", report)
        self.assertNotIn("# 驗證報告：PASS", report)

    def test_platform_answer_drift_blocks_bundle(self):
        path = self.bundle / "Wayground" / "wayground-ready.csv"
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        rows[0]["correct_answer_json"] = "[4]"
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_content_bundle.py"), "--bundle", str(self.bundle)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(result.returncode, 1)
        report = (self.bundle / "自動檢查報告.md").read_text(encoding="utf-8")
        self.assertIn("與 Canonical 題庫不一致", report)
        self.assertIn("BLOCKED", report)


if __name__ == "__main__":
    unittest.main()
