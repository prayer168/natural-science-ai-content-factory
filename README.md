# Natural Science AI Content Factory

> 自然科 AI 教材工廠版｜Kahoot × Wayground 雙平台批次教材生成系統

![Version](https://img.shields.io/badge/version-v1.2.0-blue)
![Language](https://img.shields.io/badge/language-繁體中文-green)
![Curriculum](https://img.shields.io/badge/curriculum-108課綱-orange)
![Platforms](https://img.shields.io/badge/platforms-Kahoot%20%2B%20Wayground-purple)

**Natural Science AI Content Factory** 是一套為臺灣國小自然科教師設計的 AI 教材批次生產 Skill。它延續 `natural-science-kahoot-assessment` 與 Wayground 批次教材生成流程，將「單份題庫製作」升級為「教材來源盤點 → 單元辨識 → 評量藍圖 → Canonical 母題庫 → Kahoot / Wayground 雙平台輸出 → 教師解析與品質驗證」的完整教材工廠。

核心理念只有一句話：

> **命題一次，多平台輸出；先盤點、後生產；先驗證、再交付。**

## 1. 適合誰使用？

本專案主要服務：

- 臺灣國小三至六年級自然科教師
- 使用 108 課綱進行素養導向評量的教師
- 需要大量建立 Kahoot / Wayground 題庫的教師
- 想把 PDF、PPTX、DOCX、網站、截圖、講義或既有題庫批次轉成互動教材的教師
- 進行前測、形成性評量、後測、複習、迷思診斷或差異化教學的教師
- 需要保留教師解析、迷思概念、補救教學與查證紀錄的教學設計者

## 2. V1.2.0 的主要升級

相較 V1.1 的「Kahoot × Wayground 雙平台題庫引擎」，V1.2.0 進一步加入 **AI 教材工廠模式**。

> 壓縮檔隨附的 `SKILL.md` 已與本版本說明同步至 1.2.0。Skill 會先盤點教材並建立 manifest，再逐活動產生 Canonical 題庫、完成 QA 與科學查證，最後才分流平台格式。

### 2.1 先盤點、後生產

當輸入整冊教材、整個教材網站或大量教學檔案時，不會立即產生數百題，而是先建立 `batch manifest`：

```text
教材來源
  ↓
年級 / 冊次辨識
  ↓
單元辨識
  ↓
活動辨識
  ↓
學習重點與來源位置
  ↓
預計題數 / 題型 / 難度
  ↓
風險與待確認項目
  ↓
批次生產
```

這能降低：

- 單元切分錯誤
- 不同活動混題
- 年級難度混淆
- 來源頁碼遺失
- 批次完成後才發現資料不足

### 2.2 Canonical 母題庫

所有題目先產生成平台中立的 Canonical 題庫，再由平台 adapter 轉譯：

```text
教材 / 課綱 / 教師資料
          ↓
   Canonical 題庫
      ↙         ↘
 Kahoot        Wayground
      ↘         ↙
 教師解析 / Markdown / CSV / 驗證摘要
```

Canonical 題目可保留：

- 題目與答案
- 題型
- 學習目標
- 108 課綱對應
- 認知層次 / DOK
- 難度
- 迷思概念
- 誘答設計理由
- 教師解析
- 補救教學建議
- 資料來源
- 科學查證狀態
- 平台題型映射
- `fallback_type`
- `manual_required`

答案索引使用 1 起算；單選題只能有一個正解，多選題列出所有正解。未查證資料使用 `needs_review`，有 A 級阻擋問題的題目使用 `blocked`。

### 2.3 雙平台輸出

同一份 Canonical 母題庫可以輸出：

- Kahoot-ready 題庫
- Wayground-ready 題庫
- 教師解析版
- Markdown 題庫
- CSV 備份
- 批次索引
- 批次驗證摘要

Wayground 可優先使用多元互動題型；若 Kahoot 無法等價呈現，則建立安全降級版本，而不是硬轉造成評量意義改變。

## 3. 四階段自然科 AI 評量流程

本 Skill 預設支援：

### ① 診斷 Diagnosis

確認學生先備知識與常見迷思。

### ② 探究 Inquiry

聚焦觀察、變因、實驗步驟、資料判讀與推論。

### ③ AI 證據 AI Evidence

讓學生比較 AI 生成內容與實際證據，練習查證、證據引用與科學論證。

### ④ 差異化 Differentiation

依作答結果產生基礎版、標準版、進階版或補救活動。

## 4. 可接受的教材來源

可將下列內容作為批次生產來源：

- PDF 教材
- Word / DOCX
- PowerPoint / PPTX
- 圖片與課本截圖
- 教學網站
- YouTube 逐字稿或教師提供的影片文字稿
- Markdown / TXT
- 既有 Kahoot 題庫
- 既有 Wayground 題庫
- 教師自編講義
- 單元活動清單

若來源內容不清楚，必須標示 `[無法辨識]` 或「待確認」，不得自行猜補。

## 5. 建議工作模式

### 模式 A：單元快速生成

適合單一活動或一堂課。

```text
使用 natural-science-ai-content-factory，
將六年級〈探索天氣變化〉做成 12 題，
包含迷思診斷、資料判讀與生活應用，
輸出 Kahoot 與 Wayground 版本。
```

### 模式 B：整冊教材工廠

適合 PDF、教材網站或整學期資料。

```text
使用 natural-science-ai-content-factory，
先盤點這份五年級自然科教材，
建立年級→單元→活動 batch manifest。
先不要生成正式題目。
完成盤點後，每個活動產生 10 題，
採診斷→探究→AI證據→差異化架構，
最後輸出 Kahoot、Wayground、教師解析與批次驗證摘要。
```

### 模式 C：既有 Kahoot 升級 Wayground

```text
將這份 Kahoot 題庫還原成 Canonical 母題庫，
保留原學習目標與正確答案，
判斷哪些題目適合升級成 Wayground 的
Categorize、Match、Reorder、Labeling、Hotspot 或其他互動題型。
不能等價轉換者標示 manual_required。
```

### 模式 D：Wayground 轉 Kahoot 安全版

```text
將這份 Wayground 題庫轉成 Kahoot 安全版本。
不得為了符合 Kahoot 而改變原評量目標。
無法等價轉換的題目標示 manual_required，
並提供最接近的替代題型與理由。
```

## 6. 批次生產標準流程

```text
Step 01 讀取教材來源
Step 02 辨識年級、冊次、單元、活動
Step 03 建立 batch manifest
Step 04 建立概念地圖與學習重點
Step 05 建立評量藍圖
Step 06 產生候選題
Step 07 設計合理誘答與迷思診斷
Step 08 建立 Canonical 母題庫
Step 09 執行評量品質 QA
Step 10 執行科學內容查證
Step 11 平台題型映射
Step 12 輸出 Kahoot-ready / Wayground-ready
Step 13 產生教師解析與補救建議
Step 14 建立批次索引與驗證摘要
Step 15 打包交付
```

## 7. 評量品質原則

每一題必須至少通過下列檢查：

- 正確答案唯一且可辯護
- 多選題列出全部正確答案
- 題意不含不必要的文字陷阱
- 誘答來自合理迷思或錯誤推理
- 不以答案長度、語氣或專有名詞暗示正解
- 年級與語言難度適切
- 圖表或實驗題只使用題幹中已提供的證據
- 觀察與推論明確區分
- 科學事實、數據、單位與因果關係經查證
- 未查證內容不得標示為已驗證

## 8. Template-first 原則

Kahoot 與 Wayground 的匯入格式可能改版，因此本專案採 **Template-first**：

1. 先取得平台當次最新版官方 template。
2. AI 產生 Canonical 母題庫。
3. Adapter 將 Canonical 題目映射到官方 template。
4. 無法安全映射時停止並標示，而不是硬寫入過時欄位。

因此本專案不把平台欄位永久寫死。

## 9. 專案結構

```text
natural-science-ai-content-factory/
├── README.md
├── SKILL.md
├── VERSION
├── CHANGELOG.md
├── docs/
│   └── conversation-history.md
├── references/
│   ├── canonical-schema.md
│   ├── platform-mapping.md
│   ├── prompt-library.md
│   └── qa-checklist.md
├── examples/
│   ├── batch-manifest-example.yaml
│   ├── items-example.json
│   └── generated-bundle/
│       ├── canonical.json
│       ├── kahoot-ready.csv
│       ├── wayground-ready.csv
│       └── teacher-notes.md
└── scripts/
    └── build_platform_ready_bundle.py
```

### 建立檢閱用輸出

需求為 Python 3，腳本只使用標準函式庫。提供一份 Canonical JSON 題目陣列，即可輸出供檢閱及後續範本映射用的 CSV、JSON 與教師解析 Markdown：

```bash
python scripts/build_platform_ready_bundle.py --json examples/items-example.json --outdir dist/example-bundle
```

這些 CSV 並非平台官方範本。若要直接匯入，請先取得 Kahoot 或 Wayground 當期官方範本，再依照該範本映射欄位。腳本輸出的正確答案索引沿用 Canonical 的 1 起算編號。

## 專案紀錄

需求形成與版本演進的對話紀錄見 [docs/conversation-history.md](docs/conversation-history.md)。已完成版本的變更以 [CHANGELOG.md](CHANGELOG.md) 為準。

## 10. 版本

目前版本：**v1.2.0**

版本規則採 [Semantic Versioning](https://semver.org/)：

- `MAJOR`：資料結構或工作流程有不相容變更
- `MINOR`：新增向下相容功能
- `PATCH`：錯誤修正、提示詞調整、文件改善

Git 發行版本以 `VERSION`、README 與 `SKILL.md` metadata 的 `1.2.0` 相互對應；變更紀錄見 [CHANGELOG.md](CHANGELOG.md)。建議 Git Tag：

```bash
git tag -a v1.2.0 -m "Natural Science AI Content Factory v1.2.0"
git push origin v1.2.0
```

## 11. 專案定位

這不是單純的「AI 出題器」。

它的目標是建立一條可驗證、可批次、可移植、可持續維護的自然科教材生產管線：

> **教材來源 → 教學結構化 → 評量設計 → 科學查證 → 多平台互動教材 → 學習證據 → 再教學**

---

**協作整理：陳賢宗 × ChatGPT**
