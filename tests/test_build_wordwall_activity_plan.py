import unittest

from scripts.build_wordwall_activity_plan import build_plan


class WordwallActivityPlanTests(unittest.TestCase):
    def test_plan_keeps_canonical_answer_source_and_manual_boundary(self):
        question = {
            "id": "G4-WATER-001",
            "learning_objective": "辨識水生植物構造",
            "stem": "哪種構造能讓植物固定在底泥中？",
            "options": ["根", "花瓣", "果實"],
            "correct_answer": [1],
            "canonical_type": "single_choice",
            "explanation": "根可固定植物。",
            "sources": [{"title": "教育部資料", "url": "https://example.gov.tw/science", "supports": "支持根有固定功能。"}],
            "verification_status": "verified",
        }
        plan = build_plan([question], "水生植物活動")
        self.assertIn("G4-WATER-001", plan)
        self.assertIn("正解／配對：根", plan)
        self.assertIn("https://example.gov.tw/science", plan)
        self.assertIn("不是 Wordwall 官方匯入檔", plan)
        self.assertIn("教師在 Wordwall 中人工建立測驗項目", plan)

    def test_categorize_maps_to_group_sort_without_inventing_groups(self):
        question = {
            "id": "G4-WATER-002",
            "canonical_type": "categorize",
            "stem": "依棲地將生物分類。",
            "options": ["魚", "青蛙"],
            "correct_answer": [1],
            "sources": [{"title": "來源", "url": "https://example.gov.tw/habitat", "supports": "分類依據。"}],
            "verification_status": "needs_review",
        }
        plan = build_plan([question])
        self.assertIn("分組分類", plan)
        self.assertIn("未提供；待教師補足", plan)
        self.assertIn("待查核", plan)


if __name__ == "__main__":
    unittest.main()
