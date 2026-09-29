# Wayground × AI 自然科教材工廠：開發對話紀錄

> 專案名稱：Natural Science AI Content Factory  
> 中文名稱：自然科 AI 教材工廠版  
> 目前版本：v1.2.0  
> 用途：保留從需求形成、功能設計、Skill 迭代、GitHub 規劃到 Wiki 文件化的完整開發脈絡，作為後續版本迭代、決策追蹤與簽核依據。

---

## 1. 對話起點：了解 Wayground 與 AI 教材開發

### 使用者
我想了解「wayground」這套軟體如何在教學上使用。

另外，我要如何利用AI開發wayground的教材？

### ChatGPT
Wayground 很適合放進自然科 AI 命題＋多元評量流程。Wayground 前身為 Quizizz，現在不只是遊戲化測驗，也整合教學、練習、評量、AI 生成與學習分析。

建議把 Wayground 用在四個層次：

1. 課前診斷：5–8 題概念診斷。
2. 課中探究：Presentation 搭配穿插問題。
3. 課後形成性評量：Quiz / Assessment。
4. 補救與差異化：AI 改寫、翻譯、調整難度。

自然科可搭配多種題型，例如選擇、填空、分類、排序、拖拉、圖像判讀等。

建議的 AI 協作流程為：

課綱／教材  
→ ChatGPT／Claude／Gemini  
→ AI 設計評量藍圖  
→ AI 產生題目  
→ 教師進行科學正確性與迷思檢查  
→ Wayground  
→ 學生作答  
→ Wayground 學習報告  
→ AI 再分析  
→ 下一輪差異化教學

這可與「診斷 → 探究 → AI 證據 → 差異化」四階段流程整合。

---

## 2. 技術文章需求

### 使用者
請幫我定制一個 PDF 技術文檔，步驟流程越詳細越好，還有要跟 AI 協作的提示詞也是越詳細越好，都寫到這份技術文章裡面。

### ChatGPT
規劃技術文章內容包含：

- Wayground 教學定位
- 帳號與教材建立
- AI 產題
- 題型轉換
- 查證
- 匯入
- 課堂實施
- 學習報告分析
- 可直接複製的完整提示詞

並強調繁體中文 PDF 的字型嵌入與手機顯示，避免亂碼。

同時確認 Wayground 可從 Prompt、PDF、PPTX、DOCX、圖片、網站、YouTube、Spreadsheet、Google Forms 等來源產生 Assessment，也支援 ChatGPT 直接連接 Wayground 建立 Assessment / Flashcards。

---

## 3. 將技術文章升級為 Skill

### 使用者
針對這篇技術文章，請幫我生成一個技能。這個技能可以批次生產 Wayground 的教材，可以參考之前我所建置批次生成kahoot題目的提示詞或技能。

### ChatGPT
決定不只做提示詞，而是做成可重複執行的 Wayground 批次教材生成 Skill。

參考既有 `natural-science-kahoot-assessment` 的成熟架構：

- 快速模式
- 截圖／網站批次模式
- 完整評量模式
- 兩層驗證
- 批次索引
- ZIP 交付

Wayground 版保留相同骨架，但把題型與輸出調整成多元互動教材，而不是只做四選一。

並規劃兩條主要批次路徑：

### A 路徑：平台中立題庫
批次產生 Wayground 可直接審閱的題庫／互動教材資料。

### B 路徑：官方 Spreadsheet
取得當次 Wayground 官方 Spreadsheet template 後，自動把批次題庫灌入範本產生 `.xlsx`。

重要設計原則：

> 不把今天的 Wayground Excel 欄位格式永久寫死。

這樣未來 Wayground 改版時仍可繼續使用。

---

## 4. Natural Science Wayground Batch v1.0.0

### ChatGPT
建立：

**《自然科 Wayground AI 批次教材生成 Skill v1.0.0》**

主要能力：

- PDF／PPTX／Word／圖片／截圖／網站／YouTube逐字稿／文字教材／既有題庫
- 批次轉成 Assessment、Passage、Presentation、Interactive Video 規劃
- Wayground 題庫
- 教師解析
- 迷思診斷
- 差異化教材

核心四階段：

> 診斷 → 探究 → AI 證據 → 差異化

題型規劃包含：

- Multiple Choice
- Multi-select
- Fill in the Blank
- Drop-down
- Drag-and-Drop
- Categorize
- Match
- Match Table Grid
- Reorder
- Passage
- Hotspot
- Labeling
- Open-ended
- Audio / Video Response

並加入：

`fallback_type`

用來處理不同帳號方案造成的題型限制。

資料架構採：

> Canonical JSON → Wayground 官方 Template → XLSX

並建立 Excel 轉換腳本：

`/scripts/build_wayground_xlsx.py`

專案結構包含：

```text
wayground-natural-science-batch/
├── SKILL.md
├── README.md
├── VERSION
├── references/
│   ├── prompt-library.md
│   ├── output-schema.md
│   └── wayground-current-capabilities.md
├── scripts/
│   └── build_wayground_xlsx.py
└── examples/
    ├── batch-manifest-example.yaml
    ├── items-example.json
    ├── mock-wayground-template.xlsx
    └── generated-test.xlsx
```

---

## 5. 升級為 Kahoot × Wayground 雙平台題庫引擎 v1.1.0

### 使用者
好

### ChatGPT
決定升級成：

**V1.1「Wayground × Kahoot 雙平台自然科題庫引擎」**

核心架構：

> 教材 → Canonical 母題庫 → Kahoot + Wayground

原則：

> 同一題只命一次，不分別維護兩套內容。

修改答案、迷思概念、解析或學習目標時，只改母題庫，再重新分流到兩個平台。

V1.1 加入：

- Kahoot × Wayground 雙平台轉譯
- 診斷 → 探究 → AI 證據 → 差異化
- 整單元、整冊、多活動批次處理
- Canonical JSON 母題庫
- Kahoot 安全降級機制
- Wayground 互動題型升級
- `fallback_type`
- 科學內容查證
- 評量品質 QA
- 教師解析與補救教學
- 批次索引與驗證摘要
- 12 組完整 AI 協作提示詞

並建立：

`build_platform_ready_bundle.py`

輸出：

```text
canonical.json
kahoot-ready.csv
wayground-ready.csv
teacher-notes.md
```

另外加入：

- P11：Kahoot 題庫 → Canonical → Wayground 升級
- P12：Wayground 題庫 → Kahoot 安全版本

---

## 6. 升級為自然科 AI 教材工廠版 v1.2.0

### 使用者
好

### ChatGPT
決定升級為：

**V1.2「自然科 AI 教材工廠版」**

英文名稱：

**Natural Science AI Content Factory**

主要目標：

從「單一題庫生成」升級到：

> 教材來源自動辨識單元  
> → 批次建立多份 Kahoot＋Wayground 教材包  
> → 產生索引  
> → 驗證摘要  
> → 教師解析

並加入重要保護機制：

> **先盤點、後生產**

遇到整冊 PDF 或教材網站時，不直接大量出題，而是先產生：

- 教材盤點表
- batch manifest
- 年級
- 單元
- 活動
- 來源頁碼
- 預計題數
- 風險

再依 manifest 執行。

目的是避免：

- 單元切錯
- 不同活動混題
- 批次做到一半才發現來源缺漏

---

## 7. GitHub Repository 命名與發布規劃

### 使用者
commit and push to github repo:自然科 AI 教材工廠版(英文名)

### ChatGPT
英文 repo 名定為：

`natural-science-ai-content-factory`

完整名稱：

**Natural Science AI Content Factory**

中文名稱：

**自然科 AI 教材工廠版**

原本規劃：

- 建立 GitHub repository
- commit
- push
- 建立版本標籤

但因 GitHub 瀏覽器當下未登入，新 repository 尚未完成建立。

---

## 8. README 與 Git 版本

### 使用者
build readme.md and git version

### ChatGPT
建立：

- `README.md`
- `VERSION`
- `CHANGELOG.md`
- `.gitignore`
- 更新 `SKILL.md`

版本定為：

**v1.2.0**

Git tag 規劃：

```bash
git tag -a v1.2.0 -m "Natural Science AI Content Factory v1.2.0"
git push origin v1.2.0
```

專案核心文件已明確定義為：

> 命題一次，多平台輸出  
> 先盤點、後生產  
> 先驗證、再交付

---

# 9. 建議的 Git 專案文件架構

建議 repository 採用以下結構：

```text
natural-science-ai-content-factory/
├── README.md
├── VERSION
├── CHANGELOG.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── DECISIONS.md
├── SKILL.md
├── .gitignore
│
├── docs/
│   ├── development-process.md
│   ├── architecture.md
│   ├── batch-workflow.md
│   ├── validation-workflow.md
│   ├── release-process.md
│   ├── conversation-history.md
│   └── version-history/
│       ├── v1.0.0.md
│       ├── v1.1.0.md
│       └── v1.2.0.md
│
├── references/
├── scripts/
├── examples/
└── wiki/
```

---

# 10. 每一種開發資訊應放在哪個檔案

## README.md

用途：

> 專案首頁。

放：

- 專案是什麼
- 解決什麼問題
- 核心功能
- 快速開始
- 專案架構
- 最新穩定版本
- 安裝與使用方式
- 文件入口

不要把完整版本歷史全部塞在 README。

---

## VERSION

只放目前版本，例如：

```text
1.2.0
```

它是程式與自動化最容易讀取的版本來源。

---

## CHANGELOG.md

用途：

> 記錄「每個版本實際改了什麼」。

推薦格式：

```markdown
# Changelog

## [1.2.0] - 2026-09-30

### Added
- 自然科 AI 教材工廠模式
- Batch manifest
- 先盤點、後生產流程

### Changed
- Canonical 題庫改為多平台核心資料來源

### Fixed
- 改善 Wayground / Kahoot 題型 fallback 邏輯
```

這是**版本迭代紀錄最主要的檔案**。

---

## ROADMAP.md

用途：

> 記錄「未來準備做什麼」。

例如：

```markdown
# Roadmap

## v1.3
- 自動讀取整冊 PDF
- 自動建立 batch manifest
- 多單元平行批次處理

## v1.4
- 自動分析學生作答
- 再教學教材生成

## v2.0
- 完整教材工廠 Dashboard
```

CHANGELOG 是「已完成」，ROADMAP 是「準備做」。

---

## docs/development-process.md

用途：

> 記錄「這個系統是怎麼開發的」。

這裡最適合放：

- 需求如何形成
- AI 協作模式
- 開發流程
- QA 流程
- Skill 升級流程
- Git 流程
- 版本發布流程
- 簽核流程

如果要讓團隊或未來的自己了解「整個專案怎麼跑」，這份文件最重要。

---

## DECISIONS.md

用途：

> 記錄重要架構決策與「為什麼」。

例如：

```markdown
## ADR-001：採用 Canonical JSON 作為母題庫

### 決策
所有平台輸出均先從 Canonical JSON 生成。

### 原因
避免 Kahoot 與 Wayground 各自維護一套題庫。

### 影響
未來新增平台時只需新增轉譯器。
```

這會比只看 commit log 更容易理解技術脈絡。

進階做法可使用：

```text
docs/adr/
├── 0001-canonical-json.md
├── 0002-wayground-fallback.md
└── 0003-batch-manifest.md
```

---

## docs/conversation-history.md

用途：

> 保存需求形成與 AI 協作歷程。

也就是本文件。

這不應取代 CHANGELOG，而是用來回答：

- 為什麼當初會做 Wayground？
- 為什麼後來加入 Kahoot？
- 為什麼變成教材工廠？
- 為什麼加入 batch manifest？

原始貼文在這個問題後截斷。依前文決策脈絡補全為：哪些功能是從需求逐步演進而來，以及每項決策如何影響目前版本。

---

## 11. 版本歷程文件

`docs/version-history/` 保存各版的範圍與交付摘要，回答「該版本包含什麼」；詳細逐步變更仍以 `CHANGELOG.md` 為準。對話紀錄描述需求形成，不能取代版本紀錄或 Git commit。

- `v1.0.0.md`：Wayground 自然科批次教材 Skill 的初始方向與官方範本優先原則。
- `v1.1.0.md`：以 Canonical 母題庫整合 Kahoot 與 Wayground 的雙平台題庫引擎。
- `v1.2.0.md`：先盤點後生產的 AI 教材工廠流程、批次 manifest 與 QA 交付。

## 12. Wiki 文件化原則

Wiki 用來提供按任務查找的操作說明；repository 內的 `SKILL.md`、schema、腳本與範例才是可版本控制的規格來源。Wiki 頁面應連回對應來源檔案，平台規格則標示查證日期，避免把會變動的匯入限制寫成永久規則。

---

## 13. 目前 repository 狀態

這份對話紀錄是在 v1.2.0 repository 建立後補入。先前「GitHub repository 尚未完成建立」是當時的規劃紀錄，現況已更新如下：

- Repository：<https://github.com/prayer168/natural-science-ai-content-factory>
- 預設分支：`main`
- 發行 tag：`v1.2.0`
- v1.2.0 初始發布 commit：`6f1a310`
- README、VERSION、CHANGELOG 與 Skill metadata 均標示 1.2.0。
- Skill 已補上批次盤點、逐活動 Canonical 題庫、QA 與科學查證規則。
- 平台輸出腳本範例已確認可產生正確答案索引；CSV 是檢閱格式，不等於官方匯入範本。

此紀錄於 2026-09-30 依使用者提供的貼上文字整理；原始貼文尾端不完整，缺漏處已依本對話既有決策補寫。

