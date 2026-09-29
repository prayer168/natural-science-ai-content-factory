# Canonical 題庫資料規格 v1.1

Canonical 是唯一母題庫。平台檔案全部由它轉譯。

每題一筆 JSON。`correct_answer` 使用 1 起算索引；兩平台均只能由這份母題庫轉譯。題目標記 `verified` 前，`sources` 內需有已開啟查核的網址及其支持主張。

## 交付所需欄位

- 身分與對齊：`id`, `grade`, `unit`, `activity`, `learning_objective`, `curriculum_alignment`
- 評量設計：`phase`, `cognitive_level`, `difficulty`, `canonical_type`, `stem`, `options`, `correct_answer`
- 教學支援：`explanation`, `misconception`, `remediation`, `evidence_required`
- 可追溯性：`source_note`, `sources`（每筆包含 `title`, `url`, `supports`）, `verification_status`
- 平台映射：`kahoot_adapter`, `wayground_adapter`（Wayground 另需 `fallback_type`）

本機交付與上傳閘門要求 `verification_status: "verified"`；不完整草稿仍可保留於本機，但不能上傳。

範例：
```json
{
  "id": "G6-WEATHER-001",
  "grade": 6,
  "unit": "探索天氣變化",
  "activity": "氣象資料判讀",
  "learning_objective": "能依氣象資料作合理推論",
  "curriculum_alignment": "待依本批次提供的課綱或教材來源填寫",
  "phase": "inquiry",
  "cognitive_level": "apply",
  "difficulty": "medium",
  "canonical_type": "data_interpretation",
  "stem": "根據表格，哪一項推論最合理？",
  "options": ["A", "B", "C", "D"],
  "correct_answer": [2],
  "explanation": "...",
  "misconception": "...",
  "remediation": "...",
  "evidence_required": "支持答案的教材或觀測資料",
  "source_note": "題目所據教材段落或來源位置",
  "sources": [
    {"title": "NASA Science: Top Moon Questions", "url": "https://science.nasa.gov/moon/top-moon-questions/", "supports": "月相由從地球看到的月球受光面變化造成，一般月相不是地球影子造成。"}
  ],
  "verification_status": "verified",
  "kahoot_adapter": {"target_type": "quiz", "support_status": "supported"},
  "wayground_adapter": {"target_type": "multiple_choice", "fallback_type": "multiple_choice", "support_status": "supported"}
}
```

## 狀態值
verification_status: draft | needs_review | verified | blocked
manual_required: true | false
