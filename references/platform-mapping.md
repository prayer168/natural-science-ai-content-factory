# Kahoot × Wayground 平台轉譯矩陣

| Canonical | Kahoot 安全策略 | Wayground 優先策略 |
|---|---|---|
| true_false | True/False 或二選一 | Multiple Choice / True-False |
| single_choice | Quiz | Multiple Choice |
| multi_select | Multi-select（依當次支援） | Multi-select |
| fill_blank | 若匯入不支援則手動版 | Fill in the Blank |
| reorder | 改寫為順序判斷或手動版 | Reorder |
| categorize | 改寫為單選組題或手動版 | Categorize |
| match | 改寫成配對概念選擇 | Match / Match Table |
| hotspot | 圖像單選替代 | Hotspot |
| labeling | 圖像單選替代 | Labeling |
| open_response | 手動版或回饋題 | Open-ended |
| passage_set | 拆成共同情境題 | Passage + questions |
| experiment_design | 情境單選/多選 | 多題型混合 |

永遠保存 `fallback_type`。平台功能或方案不明時，標記 unknown，不猜測。
