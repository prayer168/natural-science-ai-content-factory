# Kahoot × Wayground × Wordwall 平台轉譯矩陣

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

## Wordwall 人工活動設計

Wordwall 與其他平台共用 Canonical 題目 ID、教材來源、科學查證與 QA 結果。活動形式是教學設計建議；每次執行前若未查明 Wordwall 當期功能和匯入規格，輸出只能標示為人工建置稿，不得宣稱可直接匯入。

| Canonical 題型／目標 | Wordwall 活動設計建議 | 必須保留 |
|---|---|---|
| `single_choice`, `true_false`, `multi_select` | 測驗 | 題幹、選項、所有正解、解析、Canonical ID |
| `match` | 配對 | 兩側項目、每組正確配對、Canonical ID |
| `categorize` | 分組分類 | 分組名稱、每個項目的正確組別、Canonical ID |
| 概念提取、口語暖身 | 隨機轉盤 | 轉盤項目、對應提示／參考答案、教師引導步驟、Canonical ID |
| 其他適切題型 | 依目標設計活動稿 | 可核對答案或配對、Canonical ID、來源、人工建置步驟 |

Wordwall 活動稿至少包含：活動名稱與目標、推薦活動形式、項目和正解／配對、逐題 Canonical ID、每題來源與支持主張、教師人工建置步驟，以及「功能與匯入規格未核實，不可視為直接匯入檔」聲明。引用的題目若非 `verified`，活動稿必須保留待查狀態並禁止宣稱可交付使用。

永遠保存 `fallback_type`。平台功能或方案不明時，標記 unknown，不猜測。
