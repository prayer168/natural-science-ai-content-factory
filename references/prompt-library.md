# AI 協作提示詞庫 v1.4

## P01 教材概念地圖
你是臺灣國小自然科課程與評量專家。請分析以下教材，輸出：核心概念、先備知識、可觀察證據、常見迷思、探究活動、適合評量的資料型態、108課綱對應。不要出題。所有不確定資訊標記「待確認」。

## P02 評量藍圖
根據概念地圖建立評量藍圖。每題規劃：學習目標、四階段 phase、認知層次、難度、Canonical 題型、預期迷思、需要的證據。避免全部為記憶題。

## P03 Canonical 正式命題
依藍圖生成 Canonical 題庫 JSON。不得使用 Kahoot 或 Wayground 特有欄位取代母題庫欄位。每題包含 id、stem、options、correct_answer、explanation、misconception、remediation、source_note、verification_status。

## P04 誘答審查
逐題檢查誘答。每個錯誤選項要對應一種合理迷思、錯誤觀察、錯誤因果或常見推理錯誤。刪除可一眼排除的荒謬誘答，保持長度、語氣、文法平行。

## P05 科學查證
逐題列出需查證的科學主張，優先使用官方、研究機構或同行審查來源。輸出：題號、主張、查證結論、來源、是否需修正。證據不足寫「尚無法證實」。

## P06 Kahoot 轉譯
將 Canonical 題庫轉成 Kahoot 平台版本。不得重新命題。若原題型無法由當次官方 Spreadsheet 直接匯入，產生安全降級版並另列 manual_step_if_needed。正解與學習目標不得改變。

## P07 Wayground 轉譯
將 Canonical 題庫轉成 Wayground 平台版本。優先保留互動性：reorder、categorize、match、drag/drop、labeling、hotspot；每題同時提供 fallback_type。若帳號方案或當次匯入格式不明，標記 unknown，不猜測。

## P08 四階段總控
以「診斷→探究→AI證據→差異化」設計完整教材。診斷抓迷思；探究要求觀察、變因與資料；AI證據要求學生判斷 AI 敘述是否有來源支持；差異化提供基礎/標準/進階或補救版本。

## P09 批次總控
請將以下多個「年級/單元/活動」批次建立題庫。先建立 batch manifest，再逐活動建立獨立 Canonical 題庫；每活動不得混題。全部完成評量 QA 與科學查證後，再由同一母題庫分流 Kahoot、Wayground 與 Wordwall 人工活動設計稿。最後輸出批次索引、阻擋清單與驗證摘要。未核實 Wordwall 當期功能／匯入規格時，不得宣稱可直接匯入。

## P10 多平台同步更新
以下是既有 Canonical 題庫與教師修正要求。只修改 Canonical 母題庫；完成後重新生成 Kahoot、Wayground adapter 與 Wordwall 活動稿。請列出變更前後 diff，確認各平台輸出的 correct answer、learning objective、misconception 完全同步。

同步產生 Wordwall 活動設計稿，確認項目、正解／配對、Canonical ID 與來源均對應更新後的 Canonical 題目；此稿為人工建置用途，不代表平台匯入或發布。

## P13 Wordwall 活動設計
只根據已完成來源查證與 QA 的 Canonical 題庫設計 Wordwall 活動稿。依學習目標選擇配對、分組分類、測驗、隨機轉盤或其他適合形式；逐項列出活動項目、正解／配對、Canonical ID、逐題來源與支持主張、教師人工建置步驟。不得另行命題或改變正解。若當期官方活動功能或匯入格式未核實，明確標示「人工建置設計稿，不是官方匯入檔」，不宣稱可直接匯入或已發布；不得加入 Padlet。

## P11 Kahoot → Wayground 升級
以下是既有 Kahoot 題庫。先還原成平台中立 Canonical 題庫，辨識每題真正要測的概念與迷思，再判斷哪些題目值得升級成 reorder/categorize/match/labeling/hotspot。不要為了使用新題型而改變學習目標。

## P12 Wayground → Kahoot 安全降級
以下是 Wayground 題庫。先保留 Canonical 原題，再為 Kahoot 建立可穩定使用的降級版。互動題型無法等價轉換時，標記 manual_required 並解釋損失的互動資訊。
