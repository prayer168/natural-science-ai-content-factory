# Canonical 題庫資料規格 v1.1

Canonical 是唯一母題庫。平台檔案全部由它轉譯。

最小 JSON 範例：
```json
{
  "id": "G6-WEATHER-001",
  "grade": 6,
  "unit": "探索天氣變化",
  "activity": "氣象資料判讀",
  "learning_objective": "能依氣象資料作合理推論",
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
  "source_note": "教材或查證來源",
  "verification_status": "verified",
  "kahoot_adapter": {},
  "wayground_adapter": {}
}
```

## 狀態值
verification_status: draft | needs_review | verified | blocked
manual_required: true | false
