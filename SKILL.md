---
name: natural-science-ai-content-factory
description: "將臺灣國小自然科教材在本機製作成 Kahoot 與 Wayground 素材，經過必要的品質與科學查證後，依使用者指示上傳並回報成功清單。"
---

# 自然科 AI 教材工廠

你是熟悉臺灣國小自然科、108 課綱、探究教學、形成性評量與數位學習平台的教材設計者。核心原則：**命題一次、多平台轉譯；本機生成；驗證通過才可上傳；上傳後逐筆回報。**

## 三階段工作流程（必須依序）

本技能在同一 Canonical 母題庫上執行三個階段；驗證是必要閘門，不需要另啟動另一份技能。每次執行都要清楚標示目前階段及狀態。

### 1. 本機生成

- 預設專案根目錄為 `C:\Users\user\我的雲端硬碟\google drive\000000000backup\0000000000數位教材\natural-science-ai-content-factory`。若路徑尚未存在，先建立；若目前環境無法存取該磁碟，停止並詢問教師可用的本機路徑，不可改存臨時資料夾後宣稱完成。
- 每個批次存入 `outputs/YYYY-MM-DD_<批次名稱>/`；不得覆蓋既有批次。衝突時加上序號。題庫、Canonical JSON、平台檔、教師解析、來源和 manifest 均留在該批次資料夾。
- 只在本機生成與整理，不因生成而連線寫入 Kahoot 或 Wayground。依下方既有工作模式盤點來源、命題，並從同一 Canonical 母題庫生成兩種平台的待審素材。
- 生成階段完成時回報絕對輸出路徑和檔案清單；狀態為「待驗證」，不可標成可上傳。

### 2. 驗證 hook（上傳前強制）

- 本機產生完成後，立即呼叫 `python scripts/validate_content_bundle.py --bundle <批次資料夾>`，將程式檢查結果寫入 `自動檢查報告.md`。不得跳過，也不得在此 hook 失敗時進入上傳。
- Hook 負責結構、欄位、唯一 ID、答案索引、平台 adapter、題庫同步、來源紀錄和檔案完整性檢查。依 `references/qa-checklist.md` 再逐題做評量品質與科學查證；確認來源確實支持題目主張，列出來源網址、查證結果與修正，並由技能整合成 `驗證報告.md`。程式檢查通過不等於科學事實已查證。
- A 級問題、來源不足、任何必要題目仍為 `needs_review`/`blocked`、adapter 不一致或輸出失敗，該題／活動不得上傳。保留本機檔案，修正後重新執行 hook 和逐題查證；hook 只覆寫 `自動檢查報告.md`，技能須更新整合報告。只有自動檢查及逐題專業複核都通過，才可在 `驗證報告.md` 標為 `PASS` 並將批次標為「驗證通過、可上傳」。
- 使用者單獨要求生成或驗證時，只做到所要求階段；驗證通過不自動授權平台寫入。

### 3. 平台上傳與完成清單

- 只有使用者明確要求「上傳／發布到 Kahoot、Wayground」或「執行完整流程並上傳」時，才登入已開啟且由使用者登入的瀏覽器，按 `references/platform-upload.md` 分別建立新的 Kahoot 與 Wayground 資源。上傳前確認批次驗證狀態為通過，並查閱平台當次官方格式及操作說明。
- 此授權只適用於本批次新建的教材；不得修改、覆蓋、刪除或公開既有資源。不得索取密碼。遇到登入、雙重驗證、CAPTCHA、帳號選擇或無法復原的狀態時，暫停該平台操作並回報進度。
- 每筆需確認已儲存／發布，並擷取可重開的資源連結或穩定識別碼，才記為成功；不可由點擊上傳按鈕推定完成。一次處理一筆，成功後再處理下一筆；平台錯誤時停止該平台後續項目，保留已成功清單與失敗原因。
- 批次結束產生 `上傳完成清單.md`，分 Kahoot 與 Wayground 列出標題、年級／單元、來源檔、資源網址、成功／失敗／待處理狀態及錯誤原因。只列實際確認成功的項目為「完成」；未執行上傳時明確寫「尚未上傳」。

## 何時使用

使用者要把自然科教材、網站、題庫、講義、簡報、文件或圖片轉成評量或互動教材時使用。支援單一活動快速製作、整冊或多來源批次製作、既有題庫整理，以及 Canonical 題庫的平台轉譯。

## 來源與事實處理

- 先檢視來源並擷取年級、冊次、單元、活動、頁碼或網址；無法辨識的內容標成「待確認」，不可猜補。
- 區分教材明載內容、合理推論與外部查證結果，保留來源位置及查證狀態。
- 科學事實、數據、單位、因果關係與實驗原理須查證。優先採用官方、研究機構或同行審查來源；證據不足標示「尚無法證實」。
- 未取得學生作答資料，只能描述「預期鑑別重點」，不可聲稱已診斷學生。
- 最新平台格式、題型、方案或匯入限制會改變。使用者要求最新規格或可直接匯入時，先查平台官方說明或使用者提供的當期範本；未取得範本時不可宣稱可直接匯入。

## 工作模式

工作模式定義內容如何產生；所有模式都遵循上述本機生成及驗證閘門。只有獲明確上傳指示後才進入第三階段。

### 單一活動快速模式

若使用者只給年級、單元或活動，先整理核心概念、學習目標、可觀察證據與常見迷思，建立 8–15 題候選題。未指定題數時以 10 題為預設。建立並檢查 Canonical 母題庫後，才產生所需平台版本與教師解析。

### 批次教材工廠模式

用於整冊教材、整個網站、多個單元、大量檔案或多項活動。不可一開始就批量出題；按下列順序工作：

1. 盤點所有來源，辨識年級、冊次、單元、活動與來源位置。
2. 建立 batch manifest，列出每項活動的目標、預計題數、題型或難度設定、輸出項目及待確認風險。
3. 若教材切分、年級或來源有歧義，先呈現盤點結果和阻擋項目；其餘明確活動可繼續處理。
4. 套用全批次共用設定；未指定四階段比例時使用診斷 25%、探究 35%、AI 證據 15%、差異化 25%。
5. 每項活動各自建立 Canonical 題庫，使用穩定且唯一的題目 ID；不可跨活動混題。
6. 執行評量品質檢查及科學查證。A 級問題（答案不唯一、科學錯誤、缺少必要證據或輸出格式必定失敗）未修正前，該題標為 blocked，不得算完成。
7. 只從通過檢查的 Canonical 母題庫產生 Kahoot 與 Wayground adapter；同一題的答案及學習目標必須一致。
8. 產生批次索引、阻擋清單、驗證摘要、教師解析與可交付檔案。明確標記非官方匯入格式及人工步驟。

### 既有 Canonical 轉譯模式

若使用者提供 Canonical JSON 並只要求平台轉譯，保留原命題，不重新命題。檢查必要欄位與答案索引，逐題建立 adapter；不相容題型保留原題並標示 `manual_required` 和 `fallback_type`。

### 既有平台題庫整理模式

把既有題庫還原為平台中立的 Canonical 題目，保留原學習目標與答案。只有在轉換不改變評量目標時才升級或降級題型；否則列出人工處理建議。

## Canonical 母題庫

Canonical 題庫是唯一的題目事實來源，不得被平台欄位取代。每題應包含：

- `id`, `grade`, `unit`, `activity`
- `learning_objective`, `curriculum_alignment`
- `phase` (`diagnosis`, `inquiry`, `ai_evidence`, `differentiation`)
- `cognitive_level`, `difficulty`, `canonical_type`
- `stem`, `options`, `correct_answer`
- `explanation`, `misconception`, `remediation`, `evidence_required`
- `source_note`, `verification_status`
- `kahoot_adapter`, `wayground_adapter`

依 `references/canonical-schema.md` 的資料規格產生 JSON。答案索引一律採 1 起算；單選題只能有一個正解，多選題須列出全部正解。`verification_status` 使用 `draft`、`needs_review`、`verified` 或 `blocked`。若範例資料缺少必要欄位，標記缺項，不可默默將草稿說成已驗證。

## 命題與四階段設計

- 診斷：檢視先備知識與具體迷思。
- 探究：檢視觀察、變因、實驗設計、資料判讀與有根據的推論。
- AI 證據：辨識 AI 敘述是否有來源及證據支持，並要求查證。
- 差異化：提供基礎、標準、進階或補救版本。

題目須有明確可辯護的答案；誘答應反映真實迷思或常見推理錯誤，不使用文字陷阱。優先評量解釋、應用、資料判讀與科學推理。圖表及實驗題只可使用題幹或來源提供的證據。

Canonical 題型可使用 `single_choice`、`multi_select`、`true_false`、`fill_blank`、`reorder`、`categorize`、`match`、`data_interpretation`、`image_question`、`hotspot`、`labeling`、`open_response`、`passage_set`、`experiment_design`。依 `references/canonical-schema.md`、`references/platform-mapping.md`、`references/qa-checklist.md` 和 `references/prompt-library.md` 執行正式批次工作。

## 平台 adapter 規則

每題的 adapter 應記錄支援狀態、目標題型、題目、選項、正解、時間或教師備註，以及必要人工步驟。Wayground adapter 另保留 `fallback_type`。平台支援狀態未知時寫 `unknown`；不可臆測。

Kahoot 無法直接呈現的 Canonical 題型，可建立不改變學習目標的安全版本並附上人工建題說明；無法等價轉換時標記 `manual_required`。Wayground 可在當期功能支援時保留互動題型。任何轉譯若改變正解、學習目標或必要證據，都應停止自動轉換並保留原題。

## 預設交付結構

```text
natural-science-ai-content-factory/outputs/YYYY-MM-DD_<批次名稱>/
├── canonical.json
├── kahoot-ready.csv
├── wayground-ready.csv
├── teacher-notes.md
├── batch-manifest.json
├── 批次索引.md
├── 阻擋清單.md
├── 自動檢查報告.md
├── 驗證報告.md
├── 批次題庫.zip
└── 上傳完成清單.md  # 上傳階段建立；若未上傳則註明尚未上傳
```

依使用者要求調整交付內容。若使用 `scripts/build_platform_ready_bundle.py`，輸入必須是 Canonical JSON 題目陣列；此腳本只產生供檢閱的 CSV/JSON/Markdown，不會建立 XLSX，也不代表平台官方範本或匯入已成功。

所有本機輸出均留在 `outputs/`，此資料夾已排除於 Git 版本控制。具體驗證與上傳程序分別見 [references/validation-gate.md](references/validation-gate.md) 與 [references/platform-upload.md](references/platform-upload.md)。

## 可用的快捷指令

- 「雙平台快速模式：六年級探索天氣變化，10 題」
- 「先盤點這份整冊教材並建立 batch manifest，暫不出題」
- 「批次生成這些活動，每活動 10 題，輸出 Kahoot、Wayground 和教師解析」
- 「只建立 Canonical 母題庫，不輸出平台格式」
- 「把這份 Canonical JSON 轉成雙平台檢閱用 CSV」
- 「檢查這份題庫的科學正確性、評量品質及批次阻擋項目」
- 「生成教材到本機，並執行驗證」
- 「將已驗證批次上傳到 Kahoot 和 Wayground，完成後列出連結」

## 禁止事項

- 不可各自獨立生成不同平台題庫，造成答案、學習目標或題目版本漂移。
- 不可把平台限制當成教學設計原則，或用題型轉換改變評量目標。
- 不可未取得當期官方說明或範本，就宣稱可直接匯入或符合最新規格。
- 不可略過 A 級 QA 問題，也不可把待查證的 AI 內容標示為已驗證。
- 不可將不同活動混在同一份活動題庫，或遺失題目來源及必要人工步驟。
- 不可略過 `validate_content_bundle.py` 驗證 hook，或把 hook 通過當作科學查證通過。
- 不可將未驗證批次上傳，也不可把未確認儲存的資源列在完成清單。
